"""Check all source text/media, navigation, local targets and portable HTML."""
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit, unquote
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'vendor' / 'pydeps'))
from bs4 import BeautifulSoup
from build import local_link

DIST = ROOT / 'dist'
SOURCE = ROOT / 'source'
CONTENT = json.loads((SOURCE / 'content.json').read_text(encoding='utf-8'))
NAV = json.loads((SOURCE / 'navigation.json').read_text(encoding='utf-8'))
PRESENTATION_CHANGES = json.loads((SOURCE / 'presentation-changes.json').read_text(encoding='utf-8'))
errors = []
checks = {}
def norm(s):
    return re.sub(r'\s+', '', s).replace('\u200b', '')
def assert_ok(condition, message):
    if not condition:
        errors.append(message)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    files = list(DIST.glob('*.html'))
    docs = {p.name: BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser') for p in files}
    assert_ok(len(files) == 13, 'Expected exactly 13 HTML documents')
    expected_nav = []
    for n in NAV:
        expected_nav.append((n['label'], local_link(n['url'])))
        expected_nav.extend((c['label'], local_link(c['url'])) for c in n['children'])
    source_results = []
    for slug, page in CONTENT.items():
        filename = 'index.html' if slug == 'main' else slug + '.html'
        doc = docs[filename]
        body = doc.select_one('main')
        visible = norm(body.get_text(' ', strip=True))
        assert_ok(len(doc.select('h1')) == 1, filename + ': expected one h1')
        nav = doc.select_one('#primary-navigation')
        actual_nav = [(a.get_text(' ', strip=True), a['href']) for a in nav.select('a')]
        assert_ok(actual_nav == expected_nav, filename + ': original navbar labels/order/targets changed')
        assert_ok(len(nav.find_all(recursive=False)) == 10, filename + ': expected 10 top-level nav items')
        assert_ok(len(nav.select('.subnav a')) == 2, filename + ': expected 2 Research children')
        source_html = BeautifulSoup(''.join(s['html'] for s in page['sections']), 'html.parser')
        requested_changes = PRESENTATION_CHANGES.get(slug, {})
        removed_text = {norm(t) for t in requested_changes.get('removed_text_blocks', [])}
        missing = []
        tested = 0
        for element in source_html.select('h1,h2,h3,h4,p,li'):
            text = element.get_text(' ', strip=True)
            if not text or norm(text) == '[E-mail]' or norm(text) in removed_text:
                continue
            tested += 1
            if norm(text) not in visible:
                missing.append(text[:180])
        assert_ok(not missing, filename + ': missing original text ' + repr(missing))
        wanted_images = Counter(i['src'] for i in source_html.select('img[src]')) - Counter(requested_changes.get('removed_images', []))
        got_images = Counter(i['src'] for i in body.select('img[src]'))
        missing_images = wanted_images - got_images
        assert_ok(not missing_images, filename + ': missing source image occurrences ' + repr(dict(missing_images)))
        wanted_frames = Counter(i['src'] for i in source_html.select('iframe[src]'))
        got_frames = Counter(i['src'] for i in body.select('iframe[src]'))
        assert_ok(not wanted_frames - got_frames, filename + ': source videos missing')
        assert_ok(not body.select('.video-fallback,[data-video-src]'), filename + ': expected original inline video players')
        for frame in body.select('.video iframe[src]'):
            assert_ok(not frame.has_attr('hidden'), filename + ': inline video player must be visible')
            assert_ok(frame.get('referrerpolicy') == 'strict-origin-when-cross-origin', filename + ': YouTube referrer policy missing')
        expected_links = {local_link(a['href']) for a in source_html.select('a[href]')}
        actual_links = {a['href'] for a in doc.select('a[href]')}
        # Google Sites generates a duplicate, in-page title outline on Main.
        if slug == 'main':
            expected_links = {a for a in expected_links if not a.startswith('#')}
        absent_links = expected_links - actual_links
        assert_ok(not absent_links, filename + ': source links missing ' + repr(sorted(absent_links)))
        for a in doc.select('a[href]'):
            assert_ok(not ('sites.google.com/view/keylee' in a['href']), filename + ': CCL content link still leaves replacement site')
        source_results.append({'page': filename, 'source_text_blocks': tested, 'missing_text_blocks': len(missing), 'source_images': sum(wanted_images.values()), 'source_videos': sum(wanted_frames.values()), 'links_preserved': not absent_links})
    refs = 0
    fragments = 0
    for filename, doc in docs.items():
        ids = Counter(n['id'] for n in doc.select('[id]'))
        assert_ok(all(n == 1 for n in ids.values()), filename + ': duplicate IDs')
        for node in doc.select('[href],[src]'):
            for attr in ('href', 'src'):
                if not node.has_attr(attr):
                    continue
                url = node[attr]
                p = urlsplit(url)
                if p.scheme or p.netloc:
                    continue
                refs += 1
                target = (DIST / (unquote(p.path) or filename)).resolve()
                assert_ok(target.is_file(), filename + ': missing local file ' + url)
                if p.fragment and target.suffix == '.html':
                    fragments += 1
                    assert_ok(docs.get(target.name) is not None and docs[target.name].find(id=unquote(p.fragment)) is not None, filename + ': missing fragment ' + url)
        for image in doc.select('img'):
            assert_ok(image.has_attr('alt'), filename + ': image missing alt')
        for frame in doc.select('iframe'):
            assert_ok(bool(frame.get('title')), filename + ': iframe missing title')
    checks['source_content'] = source_results
    checks['user_requested_presentation_changes'] = PRESENTATION_CHANGES
    checks['navigation'] = {'pages': 11, 'top_level_items': 10, 'research_children': 2}
    checks['local_references'] = refs
    checks['fragments'] = fragments
    checks['members'] = len(docs['members.html'].select('.person'))
    checks['seminars'] = len(docs['cloud-seminar.html'].select('.seminar'))
    assert_ok(checks['members'] == 20, 'Expected 20 member records')
    current_emails = [a['href'].removeprefix('mailto:') for a in docs['members.html'].select('#current-members .person-email[href^="mailto:"]')]
    expected_current_emails = ['qq490800573@gmail.com', 'bvnm0121@gachon.ac.kr', 'z8086486@gachon.ac.kr', 'wlsdyd5373@gachon.ac.kr', 'whalstn21@gachon.ac.kr']
    current_count = len(docs['members.html'].select('#current-members .person'))
    former_count = len(docs['members.html'].select('#former-members .person'))
    assert_ok(current_emails == expected_current_emails, 'Current Members must match the five user-confirmed email addresses in order')
    assert_ok(current_count == 5 and former_count == 15, 'Expected 5 current and 15 former members')
    assert_ok(len(docs['members.html'].select('hr.member-divider')) == 1, 'Current/former member separator missing')
    checks['member_groups'] = {'current': current_count, 'former': former_count, 'current_emails': current_emails, 'separator': True}
    assert_ok(checks['seminars'] == 6, 'Expected 6 seminars')
    portable = []
    for filename in ('ccl-introduction.html', 'department.html'):
        doc = docs[filename]
        dependencies = [n.get('src') for n in doc.select('[src]')] + [n.get('href') for n in doc.select('link[href]')]
        dependencies += [m[0] or m[1] or m[2] for m in re.findall(r'url\(\s*(?:"([^"]*)"|\x27([^\x27]*)\x27|([^)]*))\s*\)', ''.join(s.get_text() for s in doc.select('style')))]
        bad = [u for u in dependencies if u and not u.startswith('data:')]
        assert_ok(not bad, filename + ': external/sibling asset dependencies ' + repr(bad))
        portable.append({'file': filename, 'embedded_dependencies': len(dependencies), 'external_dependencies': len(bad)})
    checks['single_file_documents'] = portable
    report = {'ok': not errors, 'checks': checks, 'errors': errors}
    (ROOT / 'qa' / 'content-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

if __name__ == '__main__':
    raise SystemExit(main())
