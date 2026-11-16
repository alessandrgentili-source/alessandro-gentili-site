"""Verify frozen EN35, five source comparisons and strict FAQ regressions."""
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = Path('en/cerchi/guides/aristide-merloni-enterprise-fate-of-places/index.html')
IT = Path('cerchi/guide/aristide-merloni-impresa-lavoro-destino-luoghi/index.html')
COVER = ROOT / 'assets/img/cerchi/cerchi-guida-35-aristide-merloni-impresa-lavoro-destino-luoghi-1600x900.webp'
SOURCE_SHA = '553d12922a28b9239cf2a3c83d3e56b2dc0ce11a684e518d5b616f85b74d67ef'
BASE = 'a53ebeda88bb701cf354cbbf77627ac830f3bea8'
OLD_CAPTION = b'The 2026 ownership milestone records the completion announced on 23 June, not a dated closing.'
NEW_CAPTION = 'Arçelik announced completion of the acquisition of the remaining 25% on 23 June 2026; the KAP disclosure also records that date as the transaction completion date.'.encode('utf-8')
spec = importlib.util.spec_from_file_location('publisher', ROOT / 'tools/validate-cerchi-guide.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def verify_caption_replacement(before, after):
    """Permit this one approved substitution; preserve every other HTML byte."""
    require(before.count(OLD_CAPTION) == 1 and before.count(NEW_CAPTION) == 0,
            'Previous page must contain exactly one original caption')
    caption = re.findall(rb'<figcaption id="path-help">(.*?)</figcaption>', before, re.S)
    require(len(caption) == 1 and caption[0].count(OLD_CAPTION) == 1,
            'Approved replacement must occur in the timeline caption')
    require(after.count(NEW_CAPTION) == 1 and after.count(OLD_CAPTION) == 0,
            'Corrected page must contain exactly one replacement caption')
    require(after.replace(NEW_CAPTION, OLD_CAPTION, 1) == before,
            'Inverse caption substitution must restore the entire previous HTML byte for byte')


def verify_caption_revision(path, base):
    require(path.resolve().relative_to(ROOT) == PAGE, 'Caption exception is exclusive to Merloni EN35')
    before = subprocess.check_output(['git', 'show', f'{base}:{PAGE}'], cwd=ROOT)
    verify_caption_replacement(before, path.read_bytes())
    print('PASS Merloni EN35: single approved caption replacement; all other HTML bytes unchanged')


def emphasis(text):
    result = []
    # Independent audit of strong/em spans, including italic inside bold FAQ 9.
    for match in re.finditer(r'\*\*(.+?)\*\*|\*([^*]+?)\*|_([^_]+?)_', text):
        value = match[1] or match[2] or match[3]
        result.append(('strong' if match[1] else 'em', v.markdown_plain(value)))
        if match[1]:
            result.extend(emphasis(value))
    return result


def faq_order(html):
    tree = v.Tree(html)
    section = next(n for n in tree.root.find('article') if n.attrs.get('id') == 'frequently-asked-questions')
    visible = [v.normalized(v.content(h)) for h in section.find('h3')]
    schemas = [json.loads(v.content(n)) for n in tree.root.find('script') if n.attrs.get('type') == 'application/ld+json']
    faq = next(s for s in schemas if s.get('@type') == 'FAQPage')
    require([v.normalized(q['name']) for q in faq['mainEntity']] == visible, 'FAQPage order must match all visible questions exactly')


def comparisons(html, source):
    tree = v.Tree(html)
    require(not tree.malformed, str(tree.malformed))
    tables = list(tree.root.find('table'))
    original = re.findall(r'(?m)^\|[^\n]+(?:\n\|[^\n]+)+', source.read_text())
    require(len(tables) == len(original) == 5, 'Exactly five source comparisons required')
    for table, raw in zip(tables, original):
        expected = []
        for line in raw.splitlines():
            cells = [x.strip() for x in line.strip('|').split('|')]
            if not all(re.fullmatch(r':?-{3,}:?', x) for x in cells):
                expected.append(tuple(v.markdown_plain(x) for x in cells))
        actual = [tuple(v.normalized(v.content(c)) for c in row.children if isinstance(c, v.Node) and c.tag in {'td', 'th'}) for row in table.find('tr')]
        require(actual == expected, 'Source comparison data, qualifiers or order changed')
        require(len(list(table.find('caption'))) == 1 and bool(table.attrs.get('aria-label')), 'Accessible table name required')
        require(all(h.attrs.get('scope') in {'row', 'col'} for h in table.find('th')), 'Table header scope required')
    figures = [n for n in v.walk(tree.root) if n.tag == 'figure' and 'data-editorial-figure' in n.attrs]
    require([f.attrs.get('id') for f in figures] == ['plants-controls', 'paths-controls'], 'Only two native explorations expected')
    for figure, prefix, count in zip(figures, ['plant', 'path'], [5, 4]):
        inputs = list(figure.find('input'))
        require(len(inputs) == count, 'Complete selection set required')
        require(all(n.attrs.get('type') == 'radio' and n.attrs.get('name') == prefix for n in inputs), 'Native radio group required')
        require([n.attrs.get('id') for n in inputs] == [f'{prefix}-{i}' for i in range(count)], 'Stable control destinations required')
        require([i for i, n in enumerate(inputs) if 'checked' in n.attrs] == [0], 'All paths must be the initial state')
        require(len(list(figure.find('legend'))) == 1 and len(list(figure.find('fieldset'))) == 1, 'Native group title required')
    css = (ROOT / 'assets/international-merloni.css').read_text()
    require('.merloni-change-1 { width:43%; }' in css and '.merloni-change-2 { width:8%; }' in css, 'Employment bars need the same percentage scale')
    require('prefers-reduced-motion:reduce' in css and '@media print' in css, 'Motion/print handling required')
    require('Arçelik announced completion of the acquisition of the remaining 25% on 23 June 2026; the KAP disclosure also records that date as the transaction completion date.' in v.content(figures[1]), 'KAP completion date must be accurately stated as 23 June 2026')
    require(not any('merloni' in n.attrs.get('src', '') for n in tree.root.find('script')), 'No local JavaScript necessary')


def check(source, self_test=False):
    require(hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA, 'Frozen EN35 SHA mismatch')
    require(COVER.read_bytes() == subprocess.check_output(['git', 'show', f'{BASE}:{COVER.relative_to(ROOT)}'], cwd=ROOT), 'Cover differs from approved main')
    html = (ROOT / PAGE).read_text()
    errors = v.validate(ROOT / PAGE, COVER, source, ROOT, mode='PUBLICATION')
    require(not errors, '\n'.join(errors))
    comparisons(html, source)
    faq_order(html)
    articles = list(v.Tree(html).root.find('article', 'guide-section'))
    raw = re.split(r'(?m)^## ', source.read_text())[1:]
    require(len(articles) == 30, 'Introduction and all 29 sections required')
    for i, (part, article) in enumerate(zip([raw[0], *raw[2:]], articles)):
        expected = emphasis(part)
        if not i:
            expected.insert(0, ('em', v.manuscript_structure(source)[1]))
        actual = [(n.tag, v.normalized(v.content(n))) for n in v.walk(article) if n.tag in {'strong', 'em'}]
        require(actual == expected, 'Emphasis altered in ' + article.attrs['id'])
    require(len(list(articles[26].find('h3'))) == 21, '21 visible FAQ required')
    expected_links = re.findall(r'\[[^]]+\]\(([^)]+)\)', source.read_text())
    links = [n.attrs.get('href') for a in articles for n in a.find('a')]
    require(all(url in links for url in expected_links), 'Original source links changed')
    # The only changes permitted on IT35 are exact alternates and outside-body nav.
    original = subprocess.check_output(['git', 'show', f'{BASE}:{IT}'], cwd=ROOT, text=True)
    italian = (ROOT / IT).read_text()
    it_url = 'https://alessandro-gentili.it/' + str(IT.parent) + '/'
    en_url = 'https://alessandro-gentili.it/' + str(PAGE.parent) + '/'
    alternates = '\n' + '\n'.join(f'<link rel="alternate" hreflang="{lang}" href="{url}" />' for lang, url in [('it', it_url), ('en', en_url), ('x-default', it_url)])
    nav = f'<nav class="wrap atlas-breadcrumb" aria-label="Edizioni linguistiche"><a href="/{PAGE.parent}/" lang="en" hreflang="en">English edition</a></nav>\n'
    require(italian.count(alternates) == italian.count(nav) == 1 and italian.replace(alternates, '', 1).replace(nav, '', 1) == original, 'IT35 changed beyond authorized language links')
    print('PASS EN35: frozen source/cover, 29 sections + opening, 21 FAQ, emphasis, five complete comparisons, native explorations, links/metadata and immutable IT prose')
    if not self_test:
        return
    # The disclosure explicitly dates completion, not only its announcement.
    corrected_caption = NEW_CAPTION.decode('utf-8')
    for label, replacement in [
        ('superseded completion disclaimer', 'The 2026 ownership milestone records the completion announced on 23 June, not a dated closing.'),
        ('wrong completion date', corrected_caption.replace('23 June 2026', '19 June 2026')),
    ]:
        changed = html.replace(corrected_caption, replacement, 1)
        require(changed != html, 'Inactive caption mutation')
        try:
            comparisons(changed, source)
        except AssertionError:
            print('PASS rejected ' + label)
        else:
            raise AssertionError('Caption regression escaped: ' + label)
    before = html.encode('utf-8').replace(NEW_CAPTION, OLD_CAPTION, 1)
    verify_caption_replacement(before, html.encode('utf-8'))
    print('PASS exact caption substitution and inverse restoration')
    caption_cases = [
        ('unchanged old caption', before, before),
        ('missing original', before.replace(OLD_CAPTION, b''), html.encode('utf-8')),
        ('duplicate original', before + OLD_CAPTION, html.encode('utf-8')),
        ('duplicate replacement', before, html.encode('utf-8') + NEW_CAPTION),
        ('wrong date', before, html.encode('utf-8').replace(b'23 June 2026; the KAP', b'19 June 2026; the KAP', 1)),
        ('extra editorial change', before, html.encode('utf-8').replace(b'About 2,000</td>', b'About 3,000</td>', 1)),
        ('extra metadata change', before, html.encode('utf-8').replace(b'<title>', b'<title>Changed ', 1)),
        ('extra markup change', before, html.encode('utf-8') + b'\n'),
    ]
    for label, previous, changed in caption_cases:
        require(previous != before or changed != html.encode('utf-8'), 'Inactive preservation mutation')
        try:
            verify_caption_replacement(previous, changed)
        except AssertionError:
            print('PASS rejected caption exception: ' + label)
        else:
            raise AssertionError('Caption exception escaped: ' + label)
    # Exercise the real dispatcher for EN35 and an unrelated existing guide.
    from unittest.mock import patch
    gate_spec = importlib.util.spec_from_file_location('international_gate', ROOT / 'tools/check-international-guide.py')
    gate = importlib.util.module_from_spec(gate_spec)
    gate_spec.loader.exec_module(gate)
    gate.verify(ROOT / PAGE, '39267b044059b7b6318386d553e4c3efd415e8ec')
    with tempfile.TemporaryDirectory(prefix='merloni-caption-dispatch-') as d:
        fixture = Path(d).resolve()
        other = Path('en/cerchi/guides/enrico-mattei-energy-public-enterprise-autonomy/index.html')
        original = (ROOT / other).read_text()
        candidate = fixture / other
        candidate.parent.mkdir(parents=True)
        candidate.write_text(original.replace('Mattei wanted a public company able to produce, compete and negotiate.', 'Changed.', 1))
        require(candidate.read_text() != original, 'Inactive other-guide mutation')
        with patch.object(gate, 'ROOT', fixture), patch.object(gate.subprocess, 'check_output', return_value=original):
            try:
                gate.verify(candidate, 'fixture-base')
            except AssertionError as error:
                require(str(error) == 'Approved articles changed, missing or reordered', 'Unexpected other-guide rejection')
                print('PASS general integrity gate still rejects changes to another guide')
            else:
                raise AssertionError('Other guide escaped the general integrity gate')
    with tempfile.TemporaryDirectory(prefix='merloni-en35-') as d:
        root = Path(d).resolve()
        # Mirror dependencies without editing any original file.
        for parent in [Path('.'), Path('en'), Path('en/cerchi'), Path('en/cerchi/guides')]:
            (root / parent).mkdir(parents=True, exist_ok=True)
            next_component = {'.':'en', 'en':'cerchi', 'en/cerchi':'guides', 'en/cerchi/guides':PAGE.parent.name}[str(parent)]
            for p in (ROOT / parent).iterdir():
                if p.name != next_component:
                    (root / parent / p.name).symlink_to(p, target_is_directory=p.is_dir())
        candidate = root / PAGE
        candidate.parent.mkdir()
        candidate.write_text(html)
        require(not v.validate(candidate, COVER, source, root, mode='PUBLICATION'), 'Fixture must accept intact page')
        mutations = [
            ('missing paragraph', html.replace('<p>The employment figures show the scale of the change:</p>', '', 1)),
            ('altered approximation', html.replace('<td role="cell">About 2,000</td>', '<td role="cell">2,000</td>', 1)),
            ('altered AGIP account', html.replace('order of 70,000 cylinders held out', 'order of 170,000 cylinders held out', 1)),
            ('altered local denominator', html.replace('Manufacturing local units</th>', 'Merloni companies</th>', 1)),
            ('missing FAQ', html.replace('<h3><strong>9. What does <em>worker-peasant</em> mean?</strong></h3>', '', 1)),
            ('schema answer changed', html.replace('He was born on 24 October 1897', 'He was born on 25 October 1897', 1)),
            ('FAQ reordered', html.replace('8. What was the Merloni model?', '9. What does worker-peasant mean?', 1)),
            ('closed no-JS contents', html.replace('<details open>', '<details>', 1)),
        ]
        for label, changed in mutations:
            require(changed != html, 'Inactive mutation: ' + label)
            candidate.write_text(changed)
            require(v.validate(candidate, COVER, source, root, mode='PUBLICATION'), 'Validator escaped: ' + label)
            print('PASS rejected ' + label)
        def reverse_schema(match):
            schema = json.loads(match[1])
            if schema.get('@type') == 'FAQPage':
                schema['mainEntity'].reverse()
            return '<script type="application/ld+json">' + json.dumps(schema) + '</script>'
        reordered = re.sub(r'<script type="application/ld\+json">(.*?)</script>', reverse_schema, html, flags=re.S)
        try:
            faq_order(reordered)
        except AssertionError:
            print('PASS rejected reordered schema FAQ array')
        else:
            raise AssertionError('Reordered schema FAQ array escaped')
        # Source grammar positive and negative cases, not just rendered mutations.
        q = '**9. What does *worker-peasant* mean?**'
        variants = [
            ('plain bold', '**9. What does worker-peasant mean?**', True),
            ('balanced underscore', '**9. What does _worker-peasant_ mean?**', True),
            ('unbalanced emphasis', '**9. What does *worker-peasant mean?**', False),
            ('mixed strong marker', '**9. What does *worker-peasant* mean?__', False),
            ('out of sequence', '**10. What does *worker-peasant* mean?**', False),
            ('mixed H3 and bold', '### 9. What does worker-peasant mean?', False),
        ]
        for label, replacement, accepted in variants:
            fixture = root / 'source.md'
            fixture.write_text(source.read_text().replace(q, replacement, 1))
            try:
                result = v.manuscript_structure(fixture)
                valid = len(result[4][25][1]) == 21
            except ValueError:
                valid = False
            require(valid == accepted, 'Source grammar regression: ' + label)
            print('PASS source grammar ' + label)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    check(args.source.resolve(), args.self_test)
