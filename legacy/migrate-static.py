"""One-time import of the existing local website, never Google Sites embeds."""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'vendor/pydeps'))
from bs4 import BeautifulSoup, Tag, NavigableString, Comment

OUT = ROOT / 'src/content'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'pages').mkdir(exist_ok=True)


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def node(element):
    if isinstance(element, Comment):
        return None
    if isinstance(element, NavigableString):
        return str(element)
    if not isinstance(element, Tag):
        return None
    if element.name in ('script', 'style'):
        raise ValueError('Executable markup is not content')
    attrs = {k: ' '.join(v) if isinstance(v, list) else v for k, v in element.attrs.items()}
    result = {'tag': element.name, 'attrs': attrs}
    children = [n for e in element.children if (n := node(e)) is not None]
    if children:
        result['children'] = children
    return result


def nodes(element):
    return [n for child in element.children if (n := node(child)) is not None]


baseline = {}
routes = []
for path in sorted((ROOT / 'dist').glob('*.html')):
    html = path.read_text(encoding='utf-8')
    doc = BeautifulSoup(html, 'html.parser')
    baseline[path.name] = {
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'text': (doc.select_one('main') or doc.body).get_text(' ', strip=True),
        'images': [dict(src=i['src'], alt=i.get('alt', '')) for i in doc.select('img[src]')],
        'videos': [i['src'] for i in doc.select('iframe[src]')],
        'anchors': [i['id'] for i in doc.select('[id]')],
    }
    if path.name in ('department.html', 'ccl-introduction.html'):
        continue
    page_id = 'main' if path.name == 'index.html' else path.stem
    heading = doc.select_one('.page-header')
    body = doc.select_one('.page-body') or doc.select_one('main')
    photos = defaultdict(list)
    for link in body.select('a[data-photo]'):
        group = link['data-photo']
        link['data-photo-index'] = str(len(photos[group]))
        photos[group].append({'src': link['href'], 'alt': link.select_one('img').get('alt', '')})
    anchors = [node(e) for e in body.find_all('span', class_='anchor', recursive=False)]
    data = {
        'id': page_id, 'filename': path.name,
        'title': doc.title.get_text().split(' | ')[0],
        'description': doc.select_one('meta[name=description]')['content'],
        'heading': node(heading) if heading else None,
        'anchors': anchors,
        'content': nodes(body) if page_id not in ('members', 'cloud-seminar') else [],
        'photos': dict(photos),
    }
    save(OUT / 'pages' / (page_id + '.json'), data)
    routes.append({'id': page_id, 'filename': path.name})
save(ROOT / 'qa/react-baseline.json', baseline)
save(OUT / 'routes.json', routes)

records = json.loads((ROOT / 'source/members-seminars-notes.json').read_text(encoding='utf-8'))
assets = json.loads((ROOT / 'source/asset-map.json').read_text(encoding='utf-8'))
members = []
for i, p in enumerate(records['members']['records'], 1):
    members.append(dict(id='person-' + str(i), order=i, name=p['name'],
                        status=p['status_original'], department=p['department_original'],
                        email=p.get('email_original') or None, notes=p.get('notes_original', []),
                        links=p.get('links', []), membership=p['membership'], photo=assets[p['photo_url']]))
save(OUT / 'members.json', members)
seminars = []
for i, p in enumerate(records['seminars']['records'], 1):
    labels = {a['label'] for a in p['links']}
    seminars.append(dict(id='seminar-' + str(i), order=i, date=p['date_original'],
                         organization=p['organization_original'],
                         details=[b for b in p['original_blocks'][2:] if b not in labels],
                         links=p['links'], images=[assets[im['url']] for im in p['images']]))
save(OUT / 'seminars.json', seminars)

main = BeautifulSoup((ROOT / 'dist/index.html').read_text(encoding='utf-8'), 'html.parser')
navigation = []
for element in main.select_one('#primary-navigation').find_all(recursive=False):
    link = element if element.name == 'a' else element.select_one('a')
    navigation.append({'label': link.get_text(' ', strip=True), 'href': link['href'],
                       'children': [{'label': a.get_text(' ', strip=True), 'href': a['href']} for a in element.select('.subnav a')]})
save(OUT / 'navigation.json', navigation)
save(OUT / 'footer.json', json.loads((ROOT / 'source/university-footer.json').read_text(encoding='utf-8')))

styles = (ROOT / 'src/site.css').read_text(encoding='utf-8')
sections = [('base', 0), ('layout', styles.index('.site-header {')),
            ('home', styles.index('.home-hero {')), ('pages', styles.index('.page-header {')),
            ('overlays-footer', styles.index('.site-footer {')), ('responsive', styles.index('@media (max-width: 1100px)'))]
(ROOT / 'src/styles').mkdir(exist_ok=True)
for i, (name, start) in enumerate(sections):
    end = sections[i + 1][1] if i + 1 < len(sections) else len(styles)
    css = styles[start:end].replace('url("assets/fonts/', 'url("/assets/fonts/')
    (ROOT / 'src/styles' / (name + '.css')).write_text(css, encoding='utf-8')
(ROOT / 'src/styles/index.css').write_text(''.join('@import "./' + n + '.css";\n' for n, _ in sections), encoding='utf-8')
print('Imported existing local HTML: 11 pages, 20 members, 6 seminars; standalone documents unchanged.')
