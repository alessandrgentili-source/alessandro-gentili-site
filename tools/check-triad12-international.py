"""Preserve frozen Triads 01–12 and verify the approved bilingual Triad 13 append."""
import argparse
from functools import lru_cache
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = 'b28cb6845ea48c83ff3f51bd3b97f18ac2364631'
SHA = '022349195e2cfbfee0e0e7af7d98ca101112c3f364d7efabc07fbfd8a00fcdb0'
PAGE = 'en/cerchi/triads/index.html'
IT_PAGE = 'cerchi/triadi/index.html'
FROZEN_RELEASE = '36e45bc8b1af40593e25df7092311475e03062f5'
SOURCE13 = 'd5a16500948e533e11a121c3fc5e6226517d80ce'
SOURCES13 = {
    'it': ('01_TRIADE13_TESTO_IT_APPROVATO.md', '7f5f8f106fd3869d8248f369d361fba2a5ae07cb906685c1d809a24d03a6c9b0'),
    'en': ('02_TRIAD13_TEXT_EN_APPROVED.md', 'd71d098f187ef4a1427b3e400c7d0376da2b68aafd66e5930c00d4a775341873'),
}
PAIRS13 = [
    ('edgar-morin-knowledge-and-its-blind-spots', 'edgar-morin-la-conoscenza-e-i-suoi-punti-ciechi'),
    ('rachel-carson-life-after-the-intervention', 'rachel-carson-la-vita-dopo-l-intervento'),
    ('john-maynard-keynes-economy-of-an-uncertain-future', 'john-maynard-keynes-economia-futuro-incerto'),
]
SLUGS = [
 ('enrico-mattei-energy-public-enterprise-autonomy', 'enrico-mattei-energia-impresa-pubblica-autonomia'),
 ('aristide-merloni-enterprise-fate-of-places', 'aristide-merloni-impresa-lavoro-destino-luoghi'),
 ('adriano-olivetti-community-power', 'adriano-olivetti-la-comunita-e-il-potere'),
]
spec = importlib.util.spec_from_file_location('publisher', ROOT / 'tools/validate-cerchi-guide.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


@lru_cache(maxsize=None)
def frozen(path, ref=FROZEN_RELEASE):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT)


@lru_cache(maxsize=None)
def source13(language):
    filename, digest = SOURCES13[language]
    data = frozen(filename, SOURCE13)
    require(hashlib.sha256(data).hexdigest() == digest, 'Triad 13 source SHA mismatch: ' + language)
    blocks = data.decode().strip().split('\n\n')
    require(len(blocks) == 4 and blocks[0].startswith('# '), 'Triad 13 source structure changed')
    return [blocks[0][2:], *blocks[1:]]


def cards(markup):
    return re.findall(r'<article class="essay-card"[^>]*>.*?</article>', markup, re.S)


def preserve_carson_markup(data):
    """Permit only the authorized stylesheet and accurate responsive cell labels."""
    path = 'cerchi/guide/rachel-carson-la-vita-dopo-l-intervento/index.html'
    expected = frozen(path).decode()
    if data == expected:
        return
    stylesheet = '<link rel="stylesheet" href="/assets/cerchi-guide-38-carson-it.css" />\n'
    require(data.count(stylesheet) == 1, 'Carson table stylesheet missing or duplicated')
    tables = re.findall(r'<table\b.*?</table>', data, re.S)
    require(len(tables) == 3, 'Carson must retain three complete tables')
    for table in tables:
        headers = [v.content(n) for n in v.Tree(table).root.find('th') if n.attrs.get('scope') == 'col']
        rows = list(v.Tree(table).root.find('tr'))[1:]
        for row in rows:
            cells = [n for n in row.children if isinstance(n, v.Node)]
            require([n.attrs.get('data-label') for n in cells] == headers, 'Carson responsive labels differ from headers')
    restored = data.replace(stylesheet, '', 1)
    for table in tables:
        restored = restored.replace(table, re.sub(r' data-label="[^"]*"', '', table), 1)
    require(restored == expected, 'Carson editorial content or other markup changed')


def restore_triad12_layout(block):
    """Invert only the approved cover-first, 3+4 paragraph column composition."""
    layout = re.search(r'<div class="triad12-prose"><div class="triad12-column">(.*?)</div><div class="triad12-column">(.*?)</div></div>', block, re.S)
    if not layout:
        return block
    require(block.index('<div class="triad-featured-covers">') < layout.start(), 'Triad 12 covers must precede the reading columns')
    columns = [re.findall(r'<p>.*?</p>', x, re.S) for x in layout.groups()]
    require([len(c) for c in columns] == [3, 4], 'Triad 12 columns must preserve all seven paragraphs')
    require(all(''.join(c) == raw for c, raw in zip(columns, layout.groups())), 'Unexpected Triad 12 column markup')
    prose = '<div class="triad12-prose">\n' + '\n'.join(columns[0] + columns[1]) + '\n</div>\n'
    return block.replace(layout[0], '', 1).replace('<div class="triad-featured-covers">', prose + '<div class="triad-featured-covers">', 1)


def verify_triad13(node, language):
    approved = source13(language)
    require(v.content(next(node.find('h2'))) == approved[0], 'Triad 13 title changed: ' + language)
    question = next(node.find('p', 'triad-question'))
    require(v.content(question) == approved[1].replace('**', ''), 'Triad 13 question changed: ' + language)
    prose = next(node.find('div', 'triad-lens'))
    require([v.content(n) for n in prose.find('p')] == [x.replace('**', '') for x in approved[2:]], 'Triad 13 text changed: ' + language)
    require([v.content(n) for n in node.find('strong')] == re.findall(r'\*\*(.+?)\*\*', '\n'.join(approved)), 'Triad 13 emphasis changed: ' + language)
    children = [n for n in node.children if isinstance(n, v.Node)]
    require([n.attrs.get('class') for n in children[:3]] == ['triad-block-head', 'triad-featured-covers', 'triad-lens'], 'Triad 13 must place the question before covers and prose below them')
    require(len(list(node.find('p'))) == (5 if language == 'it' else 6), 'Unapproved Triad 13 prose added')
    require([n.tag for n in node.find('h2')] == ['h2'] and not list(node.find('h3')), 'Unapproved Triad 13 headings')
    expected = [f'/cerchi/guide/{it}/' for _, it in PAIRS13]
    if language == 'en':
        expected = [f'/en/cerchi/guides/{en}/' for en, _ in PAIRS13] + expected
    links = list(node.find('a'))
    require([n.attrs.get('href') for n in links] == expected, 'Triad 13 guide links wrong or out of order: ' + language)
    if language == 'en':
        require(all(n.attrs.get('lang') == n.attrs.get('hreflang') == 'it' for n in links[3:]), 'Triad 13 original-language annotations missing')
    images = list(node.find('img'))
    require(len(images) == 3, 'Triad 13 requires three covers')
    for image, (en, it) in zip(images, PAIRS13):
        guide_path = f'en/cerchi/guides/{en}/index.html' if language == 'en' else f'cerchi/guide/{it}/index.html'
        guide = v.Tree(frozen(guide_path).decode())
        cover = next(n for n in guide.root.find('img') if 'cerchi-guida-' in n.attrs.get('src', ''))
        require(image.attrs.get('src') == cover.attrs['src'] and image.attrs.get('alt') == cover.attrs['alt'], 'Triad 13 approved cover/alt changed')
        require(image.attrs.get('width') == '1600' and image.attrs.get('height') == '900', 'Triad 13 cover dimensions missing')
        asset = image.attrs['src'].lstrip('/')
        require((ROOT / asset).read_bytes() == frozen(asset), 'Triad 13 cover bytes changed')
        if guide_path == 'cerchi/guide/rachel-carson-la-vita-dopo-l-intervento/index.html':
            preserve_carson_markup((ROOT / guide_path).read_text())
        else:
            require((ROOT / guide_path).read_bytes() == frozen(guide_path), 'A published Triad 13 guide changed')


def verify_it(markup):
    tree = v.Tree(markup)
    require(not tree.malformed, str(tree.malformed))
    previous, current = cards(frozen(IT_PAGE).decode()), cards(markup)
    require(len(previous) == 12 and len(current) == 13, 'Exactly thirteen Italian triad cards required')
    require(current[:12] == previous, 'The twelve historical Italian triads changed or reordered')
    require('id="tredicesima-triade"' in current[12], 'Italian Triad 13 anchor missing')
    require(len(list(tree.root.find('article', 'essay-card'))) == 13, 'Unexpected Italian triad card')
    node = next(n for n in tree.root.find('article') if n.attrs.get('id') == 'tredicesima-triade')
    verify_triad13(node, 'it')
    before = v.Tree(frozen(IT_PAGE).decode())
    require([n.attrs for n in tree.root.find('link') if n.attrs.get('rel') in {'canonical', 'alternate'}] == [n.attrs for n in before.root.find('link') if n.attrs.get('rel') in {'canonical', 'alternate'}], 'Italian canonical/hreflang changed')
    metas = {n.attrs.get('name', n.attrs.get('property')): n.attrs.get('content') for n in tree.root.find('meta')}
    require(metas['description'] == metas['og:description'] == metas['twitter:description'] and metas['description'].startswith('Le tredici triadi'), 'Italian triad metadata stale')
    schema = next(json.loads(v.content(n)) for n in tree.root.find('script') if n.attrs.get('type') == 'application/ld+json')
    require(schema['@type'] == 'CollectionPage' and schema['description'] == metas['description'] and schema['url'] == 'https://alessandro-gentili.it/cerchi/triadi/', 'Italian CollectionPage inconsistent')
    require(len(schema['hasPart']) == 39, 'Italian CollectionPage must connect all 39 guides')
    previous_schema = next(json.loads(v.content(n)) for n in before.root.find('script') if n.attrs.get('type') == 'application/ld+json')
    additions = []
    for _, it in PAIRS13:
        guide = v.Tree(frozen(f'cerchi/guide/{it}/index.html').decode())
        additions.append({'@type': 'CreativeWork', 'name': v.content(next(guide.root.find('h1'))), 'url': f'https://alessandro-gentili.it/cerchi/guide/{it}/'})
    require(schema['hasPart'] == previous_schema['hasPart'] + additions, 'Italian CollectionPage historical entries or new guide links changed')


def verify_protected(protected, read_bytes):
    for path, expected in protected.items():
        # Release indexes evolve; frozen guides, triads and assets do not.
        if path in {'cerchi/index.html', 'sitemap.xml'}:
            continue
        actual = read_bytes(path)
        if path == IT_PAGE and actual != expected:
            verify_it(actual.decode())
            continue
        require(actual == expected, 'Protected file changed: ' + path)


def sections(markup):
    return re.findall(r'<section class="wrap triad-block" id="triad-\d+">.*?</section>', markup, re.S)


def index(markup):
    raw = re.search(r'<nav class="triad-index"[^>]*>(.*?)</nav>', markup, re.S)
    require(raw, 'Triad index missing')
    return re.findall(r'<a\b.*?</a>', raw[1], re.S)


def verify(markup, before, blocks):
    tree = v.Tree(markup)
    require(not tree.malformed, str(tree.malformed))
    old_sections, new_sections = sections(before), sections(markup)
    require(len(old_sections) == 11 and len(new_sections) == 13, 'Exactly thirteen triad sections required')
    require(new_sections[:11] == old_sections, 'Existing eleven triads changed or reordered')
    require(new_sections[:11] + [restore_triad12_layout(new_sections[11])] == sections(frozen(PAGE).decode()), 'The twelve frozen English triads changed or reordered')
    require([re.search(r'id="([^"]+)"', x)[1] for x in new_sections] == [f'triad-{i:02}' for i in range(1, 14)], 'Triad section order changed')
    old_index, new_index = index(before), index(markup)
    require(len(new_index) == 13 and new_index[:11] == old_index, 'Existing index entries changed or twelfth missing')
    require(new_index[:12] == index(frozen(PAGE).decode()), 'The twelve historical index entries changed')
    require([re.search(r'href="([^"]+)"', x)[1] for x in new_index] == [f'#triad-{i:02}' for i in range(1, 14)], 'Native triad anchors incomplete')
    require('State, enterprise and community.' in html.unescape(re.sub('<[^>]+>', '', new_index[11])), 'Twelfth index title changed')
    verify_triad13(next(n for n in tree.root.find('section') if n.attrs.get('id') == 'triad-13'), 'en')
    require([n.attrs for n in tree.root.find('link') if n.attrs.get('rel') in {'canonical', 'alternate'}] == [n.attrs for n in v.Tree(frozen(PAGE).decode()).root.find('link') if n.attrs.get('rel') in {'canonical', 'alternate'}], 'English canonical/hreflang changed')
    require('italian-path-in-progress' not in markup, 'Provisional anchor remains')
    triad = next(n for n in tree.root.find('section') if n.attrs.get('id') == 'triad-12')
    require(v.content(next(triad.find('h2'))) == blocks[0][3:], 'Approved title changed')
    require(v.content(next(triad.find('h3'))) == blocks[1][4:], 'Approved question changed')
    prose = next(triad.find('div', 'triad12-prose'))
    paragraphs = list(prose.find('p'))
    require([v.content(p) for p in paragraphs] == blocks[2:], 'Approved paragraphs changed, omitted, added or reordered')
    require([n.tag for n in prose.children if isinstance(n, v.Node)] in (['p'] * 7, ['div', 'div']), 'Essay must remain seven complete paragraphs in its approved reading layout')
    require(len(list(triad.find('p'))) == 10, 'Additional editorial paragraphs not permitted')
    links = list(triad.find('a'))
    expected = [f'/en/cerchi/guides/{en}/' for en, _ in SLUGS] + [f'/cerchi/guide/{it}/' for _, it in SLUGS]
    require([x.attrs.get('href') for x in links] == expected, 'Three English and three Italian guide links required in order')
    require(all(x.attrs.get('lang') == x.attrs.get('hreflang') == 'it' for x in links[3:]), 'Italian language annotations missing')
    images = list(triad.find('img'))
    require(len(images) == 3 and all(x.attrs.get('alt') and x.attrs.get('width') == '1600' and x.attrs.get('height') == '900' for x in images), 'Three accessible original covers required')
    for image, (en, _) in zip(images, SLUGS):
        guide = v.Tree(original(f'en/cerchi/guides/{en}/index.html').decode())
        expected_cover = next(guide.root.find('img')).attrs['src']
        require(image.attrs['src'] == expected_cover and expected_cover.endswith('.webp'), 'Original cover selection changed')
    require([x.attrs for x in tree.root.find('script') if x.attrs.get('src')] == [x.attrs for x in v.Tree(before).root.find('script') if x.attrs.get('src')], 'New JavaScript not permitted')
    metas = {x.attrs.get('name', x.attrs.get('property')): x.attrs.get('content') for x in tree.root.find('meta')}
    require(metas['description'] == metas['og:description'] == metas['twitter:description'] and metas['description'].startswith('Thirteen triads'), 'Metadata counts inconsistent')
    schema = next(json.loads(v.content(x)) for x in tree.root.find('script') if x.attrs.get('type') == 'application/ld+json')
    require(schema['@type'] == 'CollectionPage' and schema['description'].startswith('Thirteen triads') and schema['url'] == 'https://alessandro-gentili.it/en/cerchi/triads/', 'CollectionPage inconsistent')


def check(source, self_test):
    require(hashlib.sha256(source.read_bytes()).hexdigest() == SHA, 'Approved source SHA-256 mismatch')
    raw = source.read_text().strip().split('\n\n')
    blocks = raw[0].splitlines() + raw[1:]
    require(len(blocks) == 9 and blocks[0].startswith('## ') and blocks[1].startswith('### '), 'Frozen source structure changed')
    markup, before = (ROOT / PAGE).read_text(), original(PAGE).decode()
    verify(markup, before, blocks)
    verify_it((ROOT / IT_PAGE).read_text())
    # Keep the baseline inventory; only the hub and sitemap may evolve.
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, 'en/cerchi/guides', 'cerchi', 'sitemap.xml', 'assets/img'], cwd=ROOT, text=True).splitlines()
    protected = {path: original(path) for path in paths}
    verify_protected(protected, lambda path: (ROOT / path).read_bytes())
    for path in ['en/cerchi/index.html', 'en/index.html', 'en/positioning/index.html', 'archivio.html']:
        text = (ROOT / path).read_text()
        require(re.findall(r'data-corpus-count="en-triads">(\d+)', text) and set(re.findall(r'data-corpus-count="en-triads">(\d+)', text)) == {'13'}, 'Triad count stale: ' + path)
        require('italian-path-in-progress' not in text, 'Provisional reference remains: ' + path)
    require('<strong>11</strong><span>Thematic paths</span>' in (ROOT / 'en/positioning/index.html').read_text(), 'Thematic path count must remain eleven')
    require('English triad reading paths: 13' in (ROOT / 'llms.txt').read_text(), 'Machine-readable inventory stale')
    tests = 0
    if self_test:
        for path in ['cerchi/index.html', 'sitemap.xml']:
            require(path in protected, 'Release surface absent from baseline: ' + path)
            verify_protected(protected, lambda candidate: protected[candidate] + b'\n<!-- Release update -->'
                             if candidate == path else protected[candidate])
        print('PASS accepted: evolving Italian hub and sitemap; baseline protection unchanged elsewhere')
        for label, path in [
            ('historical guide', next(path for path in paths if path.startswith('cerchi/guide/'))),
            ('historical cover', next(path for path in paths if path.startswith('assets/img/cerchi/'))),
        ]:
            try:
                verify_protected(protected, lambda candidate: protected[candidate] + b'altered'
                                 if candidate == path else protected[candidate])
            except AssertionError as error:
                require(str(error) == 'Protected file changed: ' + path, 'Unexpected protection failure')
                tests += 1
                print('PASS rejected: ' + label + ' mutation')
            else:
                raise AssertionError('Invalid protected mutation accepted: ' + label)
        mutations = [
            ('paragraph altered', markup.replace('Their interests met', 'Their interests converged', 1)),
            ('paragraph missing', markup.replace('<p>' + html.escape(blocks[7]) + '</p>', '', 1)),
            ('paragraph added', markup.replace('<div class="triad12-column">', '<div class="triad12-column"><p>Additional interpretation.</p>', 1)),
            ('paragraph reordered', markup.replace(html.escape(blocks[2]), '__FIRST__').replace(html.escape(blocks[3]), html.escape(blocks[2])).replace('__FIRST__', html.escape(blocks[3]))),
            ('question altered', markup.replace('Who builds the future — and who decides what it becomes?', 'Who builds the future?', 1)),
            ('old triad altered', markup.replace(sections(markup)[0], sections(markup)[0].replace('Truth', 'Certainty', 1), 1)),
            ('old index altered', markup.replace(index(markup)[0], index(markup)[0].replace('Truth', 'Certainty', 1), 1)),
            ('index target broken', markup.replace('href="#triad-12"', 'href="#missing"', 1)),
            ('English link broken', markup.replace('/en/cerchi/guides/aristide-merloni-enterprise-fate-of-places/', '/en/cerchi/guides/missing/', 1)),
            ('Italian link missing', markup.replace('href="/cerchi/guide/adriano-olivetti-la-comunita-e-il-potere/"', 'href="#missing"', 1)),
            ('cover changed', markup.replace('src="/assets/img/cerchi/cerchi-guida-34-enrico-mattei', 'src="/assets/img/cerchi/missing-enrico-mattei', 1)),
            ('metadata count stale', markup.replace('Thirteen triads', 'Twelve triads', 1)),
        ]
        thirteenth = sections(markup)[12]
        thirteenth_index = index(markup)[12]
        mutations += [
            ('Triad 13 missing', markup.replace(thirteenth, '', 1)),
            ('Triad 13 duplicated', markup.replace(thirteenth, thirteenth + thirteenth, 1)),
            ('Triad 13 premature', markup.replace(sections(markup)[11] + '\n' + thirteenth, thirteenth + '\n' + sections(markup)[11], 1)),
            ('Triad 13 index missing', markup.replace(thirteenth_index, '', 1)),
            ('Triad 13 anchor missing', markup.replace('id="triad-13"', 'id="triad-missing"', 1)),
            ('Triad 13 wrong guide', markup.replace('/en/cerchi/guides/' + PAIRS13[0][0] + '/', '/en/cerchi/guides/missing/', 1)),
            ('Triad 13 question altered', markup.replace('Who can afford to wait', 'Who can wait', 1)),
            ('Triad 13 prose altered', markup.replace('Morin examines the limits', 'Morin studies the limits', 1)),
            ('Triad 13 emphasis missing', markup.replace('<strong>who has the freedom to wait, and who must live with the consequences while others decide?</strong>', 'who has the freedom to wait, and who must live with the consequences while others decide?', 1)),
        ]
        current12 = sections(markup)[11]
        column_layout = re.search(r'<div class="triad12-prose"><div class="triad12-column">(.*?)</div><div class="triad12-column">(.*?)</div></div>', current12, re.S)
        swapped = '<div class="triad12-prose"><div class="triad12-column">' + column_layout[2] + '</div><div class="triad12-column">' + column_layout[1] + '</div></div>'
        mutations += [
            ('reading columns inverted', markup.replace(column_layout[0], swapped, 1)),
            ('reading column missing', markup.replace('<div class="triad12-column">' + column_layout[1] + '</div>', '', 1)),
            ('covers after reading columns', markup.replace(column_layout[0], '', 1).replace('<div class="triad-featured-covers"><a href="/en/cerchi/guides/enrico-mattei', column_layout[0] + '<div class="triad-featured-covers"><a href="/en/cerchi/guides/enrico-mattei', 1)),
        ]
        for label, candidate in mutations:
            require(candidate != markup, 'Ineffective regression: ' + label)
            try:
                verify(candidate, before, blocks)
            except (AssertionError, StopIteration):
                tests += 1
            else:
                raise AssertionError('Invalid mutation accepted: ' + label)
        italian = (ROOT / IT_PAGE).read_text()
        last_it = cards(italian)[12]
        italian_mutations = [
            ('missing', italian.replace(last_it, '', 1)),
            ('duplicated', italian.replace(last_it, last_it + last_it, 1)),
            ('premature', italian.replace(last_it, '', 1).replace(cards(italian)[11], last_it + cards(italian)[11], 1)),
            ('wrong guide', italian.replace(last_it, last_it.replace('/cerchi/guide/' + PAIRS13[0][1] + '/', '/cerchi/guide/missing/', 1), 1)),
            ('schema link altered', italian.replace('/cerchi/guide/' + PAIRS13[0][1] + '/', '/cerchi/guide/missing/', 1)),
            ('anchor missing', italian.replace('id="tredicesima-triade"', 'id="missing"', 1)),
            ('text altered', italian.replace('Morin interroga i limiti', 'Morin studia i limiti', 1)),
            ('historic card altered', italian.replace('Stato, impresa e comunità</h2>', 'Stato e comunità</h2>', 1)),
        ]
        for label, candidate in italian_mutations:
            require(candidate != italian, 'Ineffective Italian regression: ' + label)
            try:
                verify_it(candidate)
            except (AssertionError, StopIteration):
                tests += 1
            else:
                raise AssertionError('Invalid Italian mutation accepted: ' + label)
        verify_it(italian)
        carson = (ROOT / 'cerchi/guide/rachel-carson-la-vita-dopo-l-intervento/index.html').read_text()
        preserve_carson_markup(carson)
        for label, candidate in [
            ('table text changed', carson.replace('Racconta l&#x27;ambiente', 'Riscrive l&#x27;ambiente', 1)),
            ('responsive label changed', carson.replace('data-label="Opera"', 'data-label="Wrong label"', 1)),
            ('stylesheet missing', carson.replace('/assets/cerchi-guide-38-carson-it.css', '/assets/missing.css', 1)),
        ]:
            require(candidate != carson, 'Ineffective Carson mutation: ' + label)
            try:
                preserve_carson_markup(candidate)
            except AssertionError:
                tests += 1
            else:
                raise AssertionError('Invalid Carson mutation accepted: ' + label)
        verify(markup, before, blocks)
    print(f'PASS: frozen SHA, title/question/seven paragraphs, thirteen native anchors, frozen twelve IT/EN triads, approved bilingual Triad 13, original covers and guide links; {tests} rejection regressions and intact positive fixture.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    check(args.source, args.self_test)
