"""Fresh static CCL site. Source snapshots are data, not page templates.

Run from any directory: python src/build.py
Only dist HTML/CSS/JS are required on the web server.
"""
from __future__ import annotations
from pathlib import Path
from html import escape
from urllib.parse import urlsplit, parse_qs
import base64
import json
import mimetypes
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'vendor' / 'pydeps'))
from bs4 import BeautifulSoup

DIST = ROOT / 'dist'
PUBLIC = ROOT / 'public'
SOURCE = ROOT / 'source'
PAGES = json.loads((SOURCE / 'content.json').read_text(encoding='utf-8'))
NAV = json.loads((SOURCE / 'navigation.json').read_text(encoding='utf-8'))
PEOPLE = json.loads((SOURCE / 'members-seminars-notes.json').read_text(encoding='utf-8'))
ASSETS = json.loads((SOURCE / 'asset-map.json').read_text(encoding='utf-8'))
E = lambda s: escape(str(s), quote=True)
LABELS = {
    'main': ('RESEARCH AT CCL', 'Cognitive Computing Lab at Gachon University'),
    'professor': ('PRINCIPAL INVESTIGATOR', 'Meet Professor KangYoon Lee'),
    'cloud-seminar': ('LEARN & CONNECT', 'Exploring cloud technology and industry practice'),
    'members': ('PEOPLE AT CCL', 'People who learn, question and research together'),
    'research': ('RESEARCH AT CCL', 'From distributed data to connected intelligence'),
    'research-2025': ('RESEARCH ARCHIVE / 2025', 'Federated learning · AI agents · Healthcare AI'),
    'research-2024': ('RESEARCH ARCHIVE / ~ 2024', 'Research from the Cognitive Computing Lab'),
    'project': ('COLLABORATIVE RESEARCH', 'Research addressing challenges across healthcare and industry'),
    'publication': ('PAPERS & PATENTS', 'Research shared through publications and patents'),
    'gallery': ('LIFE AT CCL', 'Research, learning and moments together'),
    'contact': ('VISIT & CONNECT', 'Get in touch about research and opportunities at CCL'),
}
SELECTED = [
    ('2026', 'ON-DEVICE AI', 'BitLoRA: Quantization-Compatible Adapter Tuning for 1.58-bit LLM in Federated On-Device AI-Agent', 'InSeo Song, KangYoon Lee', 'Expert Systems with Applications', 'https://doi.org/10.1016/j.eswa.2026.131397'),
    ('2026', 'HEALTHCARE AI', 'FedTFT: Federated Temporal Fusion Transformer for Interpretable Multi-Horizon Psychiatric Risk Prediction Across Cross-Silo Hospitals', 'Akeel Ahamed, Ri-Ra Kang, KangYoon Lee', 'IEEE Journal of Biomedical and Health Informatics', 'https://doi.org/10.1109/JBHI.2026.3690452'),
    ('2024', 'FEDERATED LEARNING', 'FedOps: A Platform of Federated Learning Operations With Heterogeneity Management', 'Jihwan Moon, Semo Yang, KangYoon Lee', 'IEEE Access', 'https://doi.org/10.1109/ACCESS.2024.3349691'),
]

def template(name, **values):
    result = (ROOT / 'templates' / name).read_text(encoding='utf-8')
    for key, value in values.items():
        result = result.replace('{{' + key + '}}', str(value))
    if re.search(r'\{\{[A-Z_]+\}\}', result):
        raise ValueError('Unresolved template value in ' + name)
    return result

def local_link(url):
    for _ in range(3):
        p = urlsplit(url)
        if p.hostname and p.hostname.endswith('google.com') and p.path == '/url':
            q = parse_qs(p.query)
            url = q.get('q', q.get('url', [url]))[0]
        else:
            break
    p = urlsplit(url)
    if p.hostname in (None, 'sites.google.com') and p.path.startswith('/view/keylee'):
        route = p.path.removeprefix('/view/keylee').strip('/')
        name = 'index.html' if route in ('', 'main') else route.replace('/', '-') + '.html'
        return name + ('#' + p.fragment if p.fragment else '')
    if url.rstrip('/') in ('http://ccl.gachon.ac.kr/fedops', 'https://ccl.gachon.ac.kr/fedops'):
        return 'https://ccl.gachon.ac.kr/fedops/'
    return url

def nav(current):
    items = []
    for item in NAV:
        target = local_link(item['url'])
        active = current == target or (target == 'research.html' and current.startswith('research-'))
        link = '<a href="' + E(target) + '"' + (' aria-current="page"' if active else '') + '>' + E(item['label']) + '</a>'
        if item['children']:
            sub = ''.join('<a href="' + E(local_link(c['url'])) + '"' + (' aria-current="page"' if current == local_link(c['url']) else '') + '>' + E(c['label']) + '</a>' for c in item['children'])
            link = '<div class="nav-group">' + link + '<button type="button" class="subnav-toggle" aria-label="Research submenu" aria-expanded="false" aria-controls="research-subnav"><svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"><path d="m2 4 3 3 3-3" fill="none" stroke="currentColor"/></svg></button><div id="research-subnav" class="subnav">' + sub + '</div></div>'
        items.append(link)
    return ''.join(items)

def clean(section, slug):
    """Keep source text/media/anchors while rebuilding its semantic markup."""
    soup = BeautifulSoup(section['html'], 'html.parser')
    for node in soup.select('script,style,link'):
        node.decompose()
    for a in soup.select('a[href]'):
        a['href'] = local_link(a['href'])
    for node in soup.select('[id$="_l"]'):
        alias = soup.new_tag('span', id=node['id'][:-2])
        alias['class'] = 'anchor'
        node.insert_before(alias)
    for node in soup.select('h1'):
        node.name = 'h2'
    classes = {'archive-text': 'prose', 'archive-media': 'media', 'archive-gallery': 'media-grid', 'archive-embed': 'video'}
    for node in soup.select('*'):
        for key in list(node.attrs):
            if key.startswith('on') or key == 'style':
                del node[key]
        if node.get('class'):
            node['class'] = [classes.get(c, c) for c in node['class']]
    for prose in soup.select('.prose'):
        for child in list(prose.children):
            if getattr(child, 'name', None) == 'br':
                child.decompose()
    for image in soup.select('img'):
        image['loading'] = 'lazy'
        image['decoding'] = 'async'
        if not image.get('alt'):
            image['alt'] = re.sub(r'\s+', ' ', section.get('heading') or section.get('text') or LABELS[slug][1]).strip()[:140]
        if not image.find_parent('a'):
            a = soup.new_tag('a', href=image['src'])
            image.wrap(a)
        image.find_parent('a')['data-photo'] = slug
    for frame in soup.select('iframe'):
        frame['loading'] = 'lazy'
        frame['title'] = frame.get('title') or section.get('heading') or LABELS[slug][1]
        embed = urlsplit(frame.get('src', ''))
        if embed.hostname in ('www.youtube.com', 'www.youtube-nocookie.com') and embed.path.startswith('/embed/'):
            frame['referrerpolicy'] = 'strict-origin-when-cross-origin'
            frame['allow'] = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'
            frame['width'], frame['height'] = '960', '540'
    for table in soup.select('table'):
        div = soup.new_tag('div', attrs={'class': 'table-wrap', 'tabindex': '0', 'role': 'region', 'aria-label': 'Research data table'})
        table.wrap(div)
    return soup

def anchors(section):
    soup = BeautifulSoup(section['html'], 'html.parser')
    ids = [section['id']] + [node['id'] for node in soup.select('[id]')]
    ids += [i[:-2] for i in ids if i.endswith('_l')]
    return ''.join('<span class="anchor" id="' + E(i) + '"></span>' for i in dict.fromkeys(ids))

def source_block(section, slug, extra=''):
    return '<section class="document-block ' + extra + '" id="' + E(section['id']) + '">' + str(clean(section, slug)) + '</section>'

def source_intro(slug):
    return anchors(PAGES[slug]['sections'][0])

def page_heading(slug):
    title = PAGES[slug]['title']
    if slug == 'cloud-seminar':
        title = 'Cloud Open Seminar'
    elif slug == 'research-2025':
        title = 'Research · 2025'
    elif slug == 'research-2024':
        title = 'Research · ~ 2024'
    crumb = '<a href="index.html">Main</a><span aria-hidden="true">/</span>'
    if slug.startswith('research-'):
        crumb += '<a href="research.html">Research</a><span aria-hidden="true">/</span>'
    crumb += '<span aria-current="page">' + E(title) + '</span>'
    label, description = LABELS[slug]
    return template('heading.html', CRUMB=crumb, EYEBROW=E(label), TITLE=E(title), DESCRIPTION=E(description))

def selected_papers():
    return ''.join('<a class="selected-paper" href="' + E(doi) + '"><span class="paper-year">' + year + '</span><div><span class="micro-label">' + topic + '</span><h3>' + E(title) + '</h3><p>' + E(authors) + ' · ' + E(journal) + '</p></div><span class="arrow" aria-hidden="true">↗</span></a>' for year, topic, title, authors, journal, doi in SELECTED)

def home():
    original_anchors = ''.join(anchors(s) for s in PAGES['main']['sections'])
    return template('home.html', MAIN_ANCHORS=original_anchors, SELECTED_PAPERS=selected_papers())

def professor():
    sections = PAGES['professor']['sections']
    identity = clean(sections[1], 'professor')
    image = identity.select_one('.media')
    image = str(image.extract()) if image else ''
    result = source_intro('professor') + '<section class="faculty-profile" id="' + E(sections[1]['id']) + '"><div class="faculty-photo">' + image + '</div><div class="faculty-description">' + str(identity) + '</div></section>'
    groups = []
    for sec in sections[2:]:
        if sec.get('heading'):
            groups.append([sec, []])
        elif groups:
            groups[-1][1].append(sec)
    for title, items in groups:
        result += '<section class="resume-section"><div class="resume-label">' + source_block(title, 'professor') + '</div><div class="resume-list">' + ''.join(source_block(s, 'professor') for s in items) + '</div></section>'
    return result

def members():
    cards = {'current': [], 'former': []}
    for i, p in enumerate(PEOPLE['members']['records'], 1):
        membership = p.get('membership')
        if membership not in cards:
            raise ValueError('Member must have current/former membership: ' + p['name'])
        photo = ASSETS[p['photo_url']]
        notes = ''.join('<p class="person-note">' + E(n) + '</p>' for n in p.get('notes_original', []))
        email = '<span class="person-email-label">[E-mail]</span><a class="person-email" href="mailto:' + E(p['email_original']) + '">' + E(p['email_original']) + '</a>' if p.get('email_original') else ''
        links = ''.join('<a class="person-email" href="' + E(l['href']) + '">' + E(l['label']) + '</a>' for l in p.get('links', []))
        cards[membership].append('<article class="person" aria-labelledby="person-' + str(i) + '"><div class="person-top"><a class="person-photo" href="' + E(photo) + '" data-photo="members" aria-label="View photo of ' + E(p['name']) + '"><img src="' + E(photo) + '" alt="' + E(p['name']) + '" width="160" height="200" loading="lazy"></a><span class="person-index">' + f'{i:02d}' + '</span></div><div class="person-body"><h3 class="person-name" id="person-' + str(i) + '">' + E(p['name']) + '</h3><p class="person-status">' + E(p['status_original']) + '</p><p class="person-department">' + E(p['department_original']) + '</p>' + notes + email + links + '</div></article>')
    groups = []
    for key, title, subtitle in [('current', 'Current Members', 'Our current research team'), ('former', 'Former Members', 'Past members of CCL')]:
        groups.append('<section class="member-group" id="' + key + '-members" aria-labelledby="' + key + '-members-title"><header class="member-group-heading"><div><h2 id="' + key + '-members-title">' + title + '</h2><p>' + subtitle + '</p></div><span class="member-group-count">' + str(len(cards[key])) + ' members</span></header><div class="people-grid">' + ''.join(cards[key]) + '</div></section>')
    index = '<nav class="member-index" aria-label="Members index"><a href="#current-members"><span>Current Members</span><b>5</b></a><a href="#former-members"><span>Former Members</span><b>15</b></a></nav>'
    return source_intro('members') + index + '<hr class="member-divider">'.join(groups)


def university_footer():
    data = json.loads((SOURCE / 'university-footer.json').read_text(encoding='utf-8'))
    paragraphs = ''.join('<p>' + E(line.strip()) + '</p>' for line in data['text'].splitlines() if line.strip())
    return '<div class="container university-footer"><a href="' + E(data['href']) + '" target="_blank" rel="noopener"><img src="' + E(data['logo']) + '" alt="Gachon University" width="1652" height="431" loading="lazy"></a><div>' + paragraphs + '</div></div>'

def seminars():
    records = PEOPLE['seminars']['records']
    index = '<nav class="section-index" aria-label="Seminar index">' + ''.join('<a href="#seminar-' + str(i) + '">' + E(p['organization_original']) + '</a>' for i, p in enumerate(records, 1)) + '</nav>'
    result = source_intro('cloud-seminar') + index
    for i, p in enumerate(records, 1):
        labels = {l['label'] for l in p['links']}
        details = ''.join('<p>' + E(b) + '</p>' for b in p['original_blocks'][2:] if b not in labels)
        links = ''.join('<a class="seminar-material" href="' + E(l['href']) + '">' + E(l['label']) + '<span aria-hidden="true"> ↗</span></a>' for l in p['links'])
        pictures = ''.join('<figure><a href="' + E(ASSETS[image['url']]) + '" data-photo="seminar-' + str(i) + '"><img src="' + E(ASSETS[image['url']]) + '" alt="' + E(p['date_original'] + ' · ' + p['organization_original'] + ' · Photo ' + str(n)) + '" width="640" height="480" loading="lazy"></a><figcaption>' + f'{n:02d}' + ' / ' + f'{len(p["images"]):02d}' + '</figcaption></figure>' for n, image in enumerate(p['images'], 1))
        result += '<section class="seminar" id="seminar-' + str(i) + '"><div class="seminar-when"><span class="micro-label">SEMINAR / ' + f'{i:02d}' + '</span><p>' + E(p['date_original']) + '</p></div><div><header class="seminar-heading"><h2>' + E(p['organization_original']) + '</h2>' + details + '<div class="seminar-links">' + links + '</div></header><div class="seminar-photos">' + pictures + '</div></div></section>'
    return result

def research():
    links = ''.join(source_block(s, 'research', 'research-archive-link') for s in PAGES['research']['sections'][1:])
    return source_intro('research') + template('research.html', ARCHIVE_LINKS=links)

def research_archive(slug):
    parts = PAGES[slug]['sections'][1:]
    toc = []
    for section in parts:
        if section.get('heading') and len(section['heading']) < 75:
            toc.append('<a href="#' + E(section['id']) + '">' + E(section['heading']) + '</a>')
    tabs = '<nav class="research-tabs" aria-label="Research by year"><a href="research.html">Research</a><a href="research-2025.html"' + (' aria-current="page"' if slug == 'research-2025' else '') + '>2025</a><a href="research-2024.html"' + (' aria-current="page"' if slug == 'research-2024' else '') + '>~ 2024</a></nav>'
    return source_intro(slug) + tabs + '<div class="reading-layout"><aside class="reading-index"><p class="micro-label">ON THIS PAGE</p>' + ''.join(toc) + '</aside><div class="research-document">' + ''.join(source_block(s, slug) for s in parts) + '</div></div>'

def projects():
    parts = PAGES['project']['sections']
    result = source_intro('project')
    for i, section in enumerate(parts[1:], 1):
        label = 'PLATFORM &amp; ROADMAP' if i == 1 else 'PROJECT ARCHIVE'
        result += '<section class="project-section"><div class="project-label"><span class="micro-label">' + label + '</span></div>' + source_block(section, 'project') + '</section>'
    return result

def publications():
    # The source separates each paper by <br>, with title/authors/venue as <p>.
    # Rebuild records from those boundaries, retaining every paragraph and link.
    output = []
    years = []
    record = []
    in_year = False
    category = ''
    sequence = 0
    def flush():
        nonlocal record, sequence
        if record:
            sequence += 1
            output.append('<article class="publication-entry"><span class="entry-number">' + f'{sequence:02d}' + '</span><div class="entry-copy">' + ''.join(record) + '</div></article>')
            record = []
    for sec in PAGES['publication']['sections'][1:]:
        flush()
        output.append('<span class="anchor" id="' + E(sec['id']) + '"></span>')
        soup = BeautifulSoup(sec['html'], 'html.parser')
        for box in list(soup.find_all('div', class_='archive-text')):
            for child in list(box.children):
                tag = getattr(child, 'name', None)
                if tag == 'br':
                    flush()
                elif tag in ('h1', 'h2'):
                    flush()
                    if in_year:
                        output.append('</section>')
                    year = child.get_text(' ', strip=True)
                    anchor = child.get('id', 'publication-' + year)
                    years.append((anchor, year))
                    output.append('<section class="publication-year" aria-label="' + E(year) + '"><h2 id="' + E(anchor) + '">' + E(year) + '</h2>')
                    if anchor.endswith('_l'):
                        output.append('<span class="anchor" id="' + E(anchor[:-2]) + '"></span>')
                    in_year = True
                    sequence = 0
                elif tag == 'h3':
                    flush()
                    category = child.get_text(' ', strip=True)
                    output.append(str(child))
                    if child.get('id', '').endswith('_l'):
                        output.append('<span class="anchor" id="' + E(child['id'][:-2]) + '"></span>')
                elif tag:
                    for a in child.select('a[href]'):
                        a['href'] = local_link(a['href'])
                    if child.get_text(' ', strip=True):
                        record.append(str(child))
                        if category.lower() != 'paper':
                            flush()
        flush()
    if in_year:
        output.append('</section>')
    index = '<aside class="year-index"><p class="micro-label">BY YEAR</p>' + ''.join('<a href="#' + E(a) + '">' + E(y) + '<span aria-hidden="true">↗</span></a>' for a, y in years) + '</aside>'
    return source_intro('publication') + '<div class="reading-layout publications-layout">' + index + '<div class="publication-document">' + ''.join(output) + '</div></div>'

def gallery():
    sections = PAGES['gallery']['sections'][1:]
    output = []
    years = []
    for s in sections:
        text = re.sub(r'\s+', ' ', s.get('text', '')).strip()
        if re.fullmatch(r'\d{4}(?:\s*~\s*\d{4})?', text):
            years.append((s['id'], text))
            output.append('<h2 class="gallery-year" id="' + E(s['id']) + '">' + E(text) + '</h2>')
        elif not s['imageCount'] and not s['embedCount']:
            soup = clean(s, 'gallery')
            for p in soup.select('p'):
                p.name = 'h3'
            output.append('<div class="album-title" id="' + E(s['id']) + '">' + str(soup) + '</div>')
        else:
            output.append(source_block(s, 'gallery', 'gallery-album'))
    index = '<nav class="section-index" aria-label="Gallery by year">' + ''.join('<a href="#' + E(a) + '">' + E(y) + '</a>' for a, y in years) + '</nav>'
    return source_intro('gallery') + index + '<div class="gallery-document">' + ''.join(output) + '</div>'

def contact():
    sections = PAGES['contact']['sections']
    image = source_block(sections[2], 'contact')
    info = ''.join(source_block(sections[i], 'contact') for i in (1, 3, 4, 5))
    return source_intro('contact') + '<div class="contact-layout"><div class="contact-map"><p class="micro-label">GACHON UNIVERSITY · GLOBAL CAMPUS</p>' + image + '</div><div class="contact-information">' + info + '</div></div>'

def single_files():
    def uri(name, mime):
        return 'data:' + mime + ';base64,' + base64.b64encode((DIST / name).read_bytes()).decode('ascii')
    hero = BeautifulSoup((ROOT / 'templates/home.html').read_text(encoding='utf-8'), 'html.parser').select_one('.hero-visual img')
    if hero is None:
        raise ValueError('Main hero image missing from templates/home.html')
    values = {
        '@@FONT@@': uri('assets/fonts/PretendardVariable.woff2', 'font/woff2'),
        '@@PROFESSOR@@': uri('assets/professor.jpg', 'image/jpeg'),
        '@@FEDOPS@@': uri('assets/fedops-icon.png', 'image/png'),
        '@@MAP@@': uri('assets/research-map.svg', 'image/svg+xml'),
        '@@HERO_IMAGE@@': uri(hero['src'], mimetypes.guess_type(hero['src'])[0] or 'image/png'),
        '@@HERO_ALT@@': E(hero.get('alt', 'Cognitive computing research illustration')),
        '@@HERO_WIDTH@@': E(hero['width']),
        '@@HERO_HEIGHT@@': E(hero['height']),
        '@@FAVICON@@': uri('assets/favicon.svg', 'image/svg+xml'),
        '@@DEPARTMENT_IMAGE@@': uri('assets/department-source-0.jpg', 'image/jpeg'),
    }
    for name in ('ccl-introduction.html', 'department.html'):
        result = (ROOT / 'templates' / name).read_text(encoding='utf-8')
        for key, value in values.items():
            result = result.replace(key, value)
        license_text = (DIST / 'assets/fonts/OFL.txt').read_text(encoding='utf-8')
        result = result.replace('</body>', '<script type="text/plain" id="font-license">' + license_text + '</script></body>')
        (DIST / name).write_text(result, encoding='utf-8')

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    DIST.mkdir(exist_ok=True)
    shutil.copytree(PUBLIC, DIST, dirs_exist_ok=True)
    builders = {'main': home, 'professor': professor, 'members': members, 'cloud-seminar': seminars, 'research': research, 'project': projects, 'publication': publications, 'gallery': gallery, 'contact': contact}
    for slug, page in PAGES.items():
        filename = 'index.html' if slug == 'main' else slug + '.html'
        body = research_archive(slug) if slug.startswith('research-') else builders[slug]()
        body = body if slug == 'main' else page_heading(slug) + '<div class="container page-body">' + body + '</div>'
        result = template('page.html', TITLE=E(page['title']), DESCRIPTION=E(LABELS[slug][1]), PAGE=slug, NAV=nav(filename), BODY=body, UNIVERSITY_FOOTER=university_footer())
        (DIST / filename).write_text(result, encoding='utf-8')
    for name in ('site.css', 'site.js'):
        (DIST / name).write_text((ROOT / 'src' / name).read_text(encoding='utf-8'), encoding='utf-8')
    single_files()
    print('Built 11 CCL pages + 2 independent HTML documents.')

if __name__ == '__main__':
    main()
