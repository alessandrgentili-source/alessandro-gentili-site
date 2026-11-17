"""Verify frozen Triad 12 presentation and preserve the eleven published triads."""
import argparse
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
    require(len(old_sections) == 11 and len(new_sections) == 12, 'Exactly twelve triad sections required')
    require(new_sections[:11] == old_sections, 'Existing eleven triads changed or reordered')
    require([re.search(r'id="([^"]+)"', x)[1] for x in new_sections] == [f'triad-{i:02}' for i in range(1, 13)], 'Triad section order changed')
    old_index, new_index = index(before), index(markup)
    require(len(new_index) == 12 and new_index[:11] == old_index, 'Existing index entries changed or twelfth missing')
    require([re.search(r'href="([^"]+)"', x)[1] for x in new_index] == [f'#triad-{i:02}' for i in range(1, 13)], 'Native triad anchors incomplete')
    require('State, enterprise and community.' in html.unescape(re.sub('<[^>]+>', '', new_index[11])), 'Twelfth index title changed')
    require('italian-path-in-progress' not in markup, 'Provisional anchor remains')
    triad = next(n for n in tree.root.find('section') if n.attrs.get('id') == 'triad-12')
    require(v.content(next(triad.find('h2'))) == blocks[0][3:], 'Approved title changed')
    require(v.content(next(triad.find('h3'))) == blocks[1][4:], 'Approved question changed')
    prose = next(triad.find('div', 'triad12-prose'))
    paragraphs = list(prose.find('p'))
    require([v.content(p) for p in paragraphs] == blocks[2:], 'Approved paragraphs changed, omitted, added or reordered')
    require([n.tag for n in prose.children if isinstance(n, v.Node)] == ['p'] * 7, 'Essay must remain seven complete paragraphs')
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
    require(metas['description'] == metas['og:description'] == metas['twitter:description'] and metas['description'].startswith('Twelve triads'), 'Metadata counts inconsistent')
    schema = next(json.loads(v.content(x)) for x in tree.root.find('script') if x.attrs.get('type') == 'application/ld+json')
    require(schema['@type'] == 'CollectionPage' and schema['description'].startswith('Twelve triads') and schema['url'] == 'https://alessandro-gentili.it/en/cerchi/triads/', 'CollectionPage inconsistent')


def check(source, self_test):
    require(hashlib.sha256(source.read_bytes()).hexdigest() == SHA, 'Approved source SHA-256 mismatch')
    raw = source.read_text().strip().split('\n\n')
    blocks = raw[0].splitlines() + raw[1:]
    require(len(blocks) == 9 and blocks[0].startswith('## ') and blocks[1].startswith('### '), 'Frozen source structure changed')
    markup, before = (ROOT / PAGE).read_text(), original(PAGE).decode()
    verify(markup, before, blocks)
    # All author guides, Italian pages, sitemap and existing assets stay byte-identical.
    protected = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, 'en/cerchi/guides', 'cerchi', 'sitemap.xml', 'assets/img'], cwd=ROOT, text=True).splitlines()
    for path in protected:
        require((ROOT / path).read_bytes() == original(path), 'Protected file changed: ' + path)
    for path in ['en/cerchi/index.html', 'en/index.html', 'en/positioning/index.html', 'archivio.html']:
        text = (ROOT / path).read_text()
        require(re.findall(r'data-corpus-count="en-triads">(\d+)', text) and set(re.findall(r'data-corpus-count="en-triads">(\d+)', text)) == {'12'}, 'Triad count stale: ' + path)
        require('italian-path-in-progress' not in text, 'Provisional reference remains: ' + path)
    require('<strong>11</strong><span>Thematic paths</span>' in (ROOT / 'en/positioning/index.html').read_text(), 'Thematic path count must remain eleven')
    require('English triad reading paths: 12' in (ROOT / 'llms.txt').read_text(), 'Machine-readable inventory stale')
    tests = 0
    if self_test:
        mutations = [
            ('paragraph altered', markup.replace('Their interests met', 'Their interests converged', 1)),
            ('paragraph missing', markup.replace('<p>' + html.escape(blocks[7]) + '</p>', '', 1)),
            ('paragraph added', markup.replace('</div>\n<div class="triad-featured-covers"><a href="/en/cerchi/guides/enrico-mattei', '<p>Additional interpretation.</p></div>\n<div class="triad-featured-covers"><a href="/en/cerchi/guides/enrico-mattei', 1)),
            ('paragraph reordered', markup.replace(html.escape(blocks[2]), '__FIRST__').replace(html.escape(blocks[3]), html.escape(blocks[2])).replace('__FIRST__', html.escape(blocks[3]))),
            ('question altered', markup.replace('Who builds the future — and who decides what it becomes?', 'Who builds the future?', 1)),
            ('old triad altered', markup.replace(sections(markup)[0], sections(markup)[0].replace('Truth', 'Certainty', 1), 1)),
            ('old index altered', markup.replace(index(markup)[0], index(markup)[0].replace('Truth', 'Certainty', 1), 1)),
            ('index target broken', markup.replace('href="#triad-12"', 'href="#missing"', 1)),
            ('English link broken', markup.replace('/en/cerchi/guides/aristide-merloni-enterprise-fate-of-places/', '/en/cerchi/guides/missing/', 1)),
            ('Italian link missing', markup.replace('href="/cerchi/guide/adriano-olivetti-la-comunita-e-il-potere/"', 'href="#missing"', 1)),
            ('cover changed', markup.replace('src="/assets/img/cerchi/cerchi-guida-34-enrico-mattei', 'src="/assets/img/cerchi/missing-enrico-mattei', 1)),
            ('metadata count stale', markup.replace('Twelve triads', 'Eleven triads', 1)),
        ]
        for label, candidate in mutations:
            require(candidate != markup, 'Ineffective regression: ' + label)
            try:
                verify(candidate, before, blocks)
            except (AssertionError, StopIteration):
                tests += 1
            else:
                raise AssertionError('Invalid mutation accepted: ' + label)
        verify(markup, before, blocks)
    print(f'PASS: frozen SHA, title/question/seven paragraphs, twelve native anchors, six guide links, original covers, eleven immutable triads; {tests} rejection regressions and intact positive fixture.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    check(args.source, args.self_test)
