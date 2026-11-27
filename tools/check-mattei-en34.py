"""Source-lock Mattei EN34 and test rejection of content/figure regressions."""
import argparse
import hashlib
import importlib.util
from pathlib import Path
import re
import tempfile

import cerchi_ei07 as ei07

ROOT = Path(__file__).resolve().parents[1]
PAGE = Path('en/cerchi/guides/enrico-mattei-energy-public-enterprise-autonomy/index.html')
COVER = ROOT / 'assets/img/cerchi/cerchi-guida-34-enrico-mattei-energia-impresa-pubblica-autonomia-1600x900.webp'
SOURCE_SHA = 'e503d332da545fcbc6bb45d3797471c51db5a037b9565c5187fc9598426174f8'
spec = importlib.util.spec_from_file_location('publisher', ROOT / 'tools/validate-cerchi-guide.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def figures(html):
    nodes = list(v.walk(v.Tree(html).root))
    fs = [n for n in nodes if n.tag == 'figure' and 'data-editorial-figure' in n.attrs]
    require([f.attrs.get('id') for f in fs] == ['mattei-en-gas-network', 'mattei-en-iran'], 'EN34 needs the two approved figures')
    tables = [t for f in fs for t in f.find('table')]
    expected = [
        [('Italy: total', '64.0', '509.6'), ('Later ENI grouping: retrospective · included in the total', '12.6', '305.7')],
        [('1949', 'About 354 km'), ('1951', 'About 1,266 km')],
        [('Iranian party · NIOC', '50%'), ('Italian party · AGIP Mineraria', '50%')],
        [('Iran · taxes and NIOC dividends', '75%'), ('Italian side', '25%')],
    ]
    require(len(tables) == len(expected), 'EN34 needs four semantic tables')
    for table, rows in zip(tables, expected):
        require(len(list(table.find('caption'))) == 1, 'Table caption missing')
        actual = [tuple(v.normalized(v.content(c)) for c in tr.children if isinstance(c, v.Node) and c.tag in {'th', 'td'}) for tr in next(table.find('tbody')).find('tr')]
        require(actual == rows, 'EN34 figure data or retrospective qualification changed')
        require(all(h.attrs.get('scope') in {'col', 'row'} for h in table.find('th')), 'Table scope missing')
    text = [v.normalized(v.content(f)) for f in fs]
    require('ENI was established in 1953' in text[0] and 'not additive' in text[0], 'ENI part/whole boundary missing')
    require('projected' in text[1].lower() and 'neither shares of oil deposits nor profits already realised' in text[1], 'Iran forecast/result boundary missing')
    require('failure left exploration costs with the Italian party' in text[1], 'Exploration risk qualification missing')
    require(all('aria-hidden' not in t.attrs for t in tables), 'Data tables cannot be hidden')
    css = (ROOT / 'assets/international-mattei.css').read_text()
    for name, actual in [('total-1946', 64 / 509.6 * 100), ('component-1946', 12.6 / 64 * 100), ('component-1950', 305.7 / 509.6 * 100)]:
        match = re.search(r'\.mattei-en-' + name + r'\s*\{\s*width:([\d.]+)%;', css)
        require(match and abs(float(match[1]) - actual) < .00001, 'Production bars must preserve part/whole and common scale')


def check(source, self_test=False):
    require(hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA, 'Approved EN34 manuscript hash mismatch')
    require(hashlib.sha256(COVER.read_bytes()).hexdigest() == '3465bb1c205175ded358c540fa377f733dbce1e4d098bc9684a0dc2448f9ea05', 'Approved cover changed')
    html = ei07.historical_bytes(ROOT, PAGE.as_posix()).decode()
    errors = v.validate(ROOT / PAGE, COVER, source, ROOT, mode='PUBLICATION', historical_html=html)
    require(not errors, '\n'.join(errors))
    figures(html)
    raw = re.split(r'(?m)^## ', source.read_text())[1:]
    source_sections = [raw[0], *raw[2:]]
    articles = list(v.Tree(html).root.find('article', 'guide-section'))
    require(len(articles) == len(source_sections) == 41, 'All 41 editorial articles required')
    for body, article in zip(source_sections, articles):
        expected = [('strong' if m[1] else 'em', v.markdown_plain(m[1] or m[2] or m[3])) for m in re.finditer(r'\*\*(.+?)\*\*|\*([^*]+?)\*|_([^_]+?)_', body)]
        actual = [(n.tag, v.normalized(v.content(n))) for n in v.walk(article) if n.tag in {'strong', 'em'}]
        if article is articles[0]:
            # Full subtitle is deliberately retained before the opening prose.
            expected.insert(0, ('em', v.manuscript_structure(source)[1]))
        require(actual == expected, 'Original emphasis changed in ' + article.attrs['id'])
    require(len(list(articles[37].find('h3'))) == 16, 'Exactly 16 visible FAQ required')
    print('PASS Mattei EN34: source/cover hashes, 40 sections + introduction, original emphasis, 16 FAQ, metadata, links, publication dependencies, two figures')
    if not self_test:
        return
    for label, heading in [('Why Mattei matters', 'Why Enrico Mattei matters'), ('Writings, speeches and documents', 'Principal writings, speeches and documents'), ('Sources and copyright', 'Sources, method and copyright'), ('The agreement with Iran', 'The agreement with Iran (1957)')]:
        require(v.toc_label_matches(label, heading), 'Reviewed alias rejected')
        require(not v.toc_label_matches(label, heading + ' altered'), 'Alias must not admit arbitrary headings')
    require(v.final_headings_valid(['Sources, method and copyright', 'Continue reading', 'Closing — What capacity is for'], 'en'), 'Approved closing rejected')
    require(not v.final_headings_valid(['Sources, method and copyright', 'Closing — What capacity is for', 'Continue reading'], 'en'), 'Wrong final order accepted')
    mutations = [
        ('deleted source paragraph', html.replace('<p>Mattei wanted a public company able to produce, compete and negotiate.', '<p>Changed.', 1)),
        ('altered national production', html.replace('64.0 million cubic metres in 1946', '20.0 million cubic metres in 1946', 1)),
        ('wrong FAQ schema', html.replace('He led AGIP\'s revival', 'He founded AGIP', 1)),
        ('closed no-JS contents', html.replace('<details open>', '<details>', 1)),
        ('wrong canonical', html.replace('rel="canonical" href="https://alessandro-gentili.it/en/', 'rel="canonical" href="https://example.com/en/', 1)),
    ]
    with tempfile.TemporaryDirectory(prefix='mattei-en34-regressions-') as d:
        root = Path(d).resolve()
        for p in ROOT.iterdir():
            if p.name != 'en': (root / p.name).symlink_to(p, target_is_directory=p.is_dir())
        (root / PAGE).parent.mkdir(parents=True)
        for p in (ROOT / 'en').iterdir():
            if p.name != 'cerchi': (root / 'en' / p.name).symlink_to(p, target_is_directory=p.is_dir())
        for p in (ROOT / 'en/cerchi').iterdir():
            if p.name != 'guides': (root / 'en/cerchi' / p.name).symlink_to(p, target_is_directory=p.is_dir())
        for p in (ROOT / 'en/cerchi/guides').iterdir():
            if p.name != PAGE.parent.name: (root / 'en/cerchi/guides' / p.name).symlink_to(p, target_is_directory=True)
        candidate = root / PAGE
        candidate.write_text(html)
        baseline = v.validate(candidate, COVER, source, root, mode='PUBLICATION')
        require(not baseline, 'Regression fixture baseline failed: ' + '\n'.join(baseline))
        for label, changed in mutations:
            require(changed != html, 'Inactive mutation: ' + label)
            candidate.write_text(changed)
            require(v.validate(candidate, COVER, source, root, mode='PUBLICATION'), 'Regression escaped: ' + label)
            print('PASS rejected ' + label)
    for label, changed in [('incorrect gas figure', html.replace('<td>64.0</td>', '<td>20</td>', 1)), ('realised profits', html.replace('neither shares of oil deposits nor profits already realised', 'profits already realised', 1)), ('lost retrospective grouping', html.replace('Later ENI grouping: retrospective · included in the total', 'ENI production', 1))]:
        require(changed != html, 'Inactive figure mutation')
        try: figures(changed)
        except AssertionError: print('PASS rejected ' + label)
        else: raise AssertionError('Figure regression escaped: ' + label)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    check(args.source.resolve(), args.self_test)
