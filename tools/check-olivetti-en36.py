"""Lock approved Olivetti EN36 content, institutional distinctions and parser gates."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile

import cerchi_ei07 as ei07

ROOT = Path(__file__).resolve().parents[1]
PAGE = Path('en/cerchi/guides/adriano-olivetti-community-power/index.html')
IT = Path('cerchi/guide/adriano-olivetti-la-comunita-e-il-potere/index.html')
COVER = ROOT / 'assets/img/cerchi/cerchi-guida-36-adriano-olivetti-la-comunita-e-il-potere-1600x900.webp'
SOURCE_SHA = 'ef2877f198a2518e44c2c156bb22880c2458992f1fe4aad3df022c4565b7e641'
BASE = '8ac24e982031507a9e82b4d8b683274ded240216'
spec = importlib.util.spec_from_file_location('publisher', ROOT / 'tools/validate-cerchi-guide.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def emphasis(text):
    result = []
    for m in re.finditer(r'\*\*(.+?)\*\*|\*([^*]+?)\*|_([^_]+?)_', text):
        value = m[1] or m[2] or m[3]
        result.append(('strong' if m[1] else 'em', v.markdown_plain(value)))
        if m[1]:
            result.extend(emphasis(value))
    return result


def representations(html, source):
    tree = v.Tree(html)
    require(not tree.malformed, str(tree.malformed))
    visuals = list(tree.root.find('div', 'olivetti-visual'))
    require([x.attrs.get('id') for x in visuals] == ['olivetti-works', 'olivetti-powers', 'olivetti-places'], 'Three distinct source matrices required')
    tables = list(tree.root.find('table'))
    source_tables = re.findall(r'(?m)^\|[^\n]+(?:\n\|[^\n]+)+', source.read_text())
    require(len(tables) == len(source_tables) == 3, 'Exactly three complete source tables required')
    for table, raw in zip(tables, source_tables):
        expected = []
        for line in raw.splitlines():
            cells = [c.strip() for c in line.strip('|').split('|')]
            if not all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
                expected.append(tuple(v.markdown_plain(c) for c in cells))
        actual = [tuple(v.normalized(v.content(c)) for c in row.children if isinstance(c, v.Node) and c.tag in {'th', 'td'}) for row in table.find('tr')]
        require(actual == expected, 'Table data, consultation status or institutional boundary altered')
        require(bool(table.attrs.get('aria-label')) and len(list(table.find('caption'))) == 1, 'Accessible table name/caption required')
        require(all(h.attrs.get('scope') in {'row', 'col'} for h in table.find('th')), 'Semantic table scopes required')
    figures = [n for n in tree.root.find('figure') if 'data-editorial-figure' in n.attrs]
    require([f.attrs.get('id') for f in figures] == ['powers-controls', 'endurance-controls'], 'Only the two prescribed explorations expected')
    for figure, prefix, count in zip(figures, ['powers', 'endurance'], [4, 5]):
        radios = list(figure.find('input'))
        require(len(radios) == count and all(x.attrs.get('type') == 'radio' and x.attrs.get('name') == prefix for x in radios), 'Native radio group incomplete')
        require([x.attrs.get('id') for x in radios] == [f'{prefix}-{i}' for i in range(count)], 'Control IDs changed')
        require([i for i, x in enumerate(radios) if 'checked' in x.attrs] == [0], 'Whole comparison must be initial state')
        require(len(list(figure.find('fieldset'))) == len(list(figure.find('legend'))) == 1, 'Native group name required')
    timeline = next(tree.root.find('ol', 'olivetti-timeline'))
    events = list(timeline.find('li'))
    raw_timeline = source.read_text().split('### An institution beyond its founder\n', 1)[1].split('\n\nThe Camillo Olivetti Foundation:', 1)[0]
    expected_events = [v.markdown_plain(re.sub(r'^\d+\. ', '', line)) for line in raw_timeline.splitlines() if re.match(r'^\d+\. ', line)]
    require([v.normalized(v.content(x)) for x in events] == expected_events and len(events) == 5, '1948–1971 chronology altered')
    require([x.attrs.get('data-event') for x in events] == ['1', '2', '3', '4', '5'], 'Timeline destinations missing')
    require('27 February 1960' in v.content(events[2]), 'Founder boundary must remain the third event')
    unfinished = next(n for n in tree.root.find('p') if n.attrs.get('id') == 'olivetti-unfinished')
    require('not realised' in v.content(unfinished) and 'not adopted' in v.content(unfinished), 'Unfinished projects must remain distinct from Council survival')
    css = (ROOT / 'assets/international-olivetti.css').read_text()
    require('prefers-reduced-motion:reduce' in css and '@media print' in css, 'Motion and print handling missing')
    require(not any('olivetti' in x.attrs.get('src', '') for x in tree.root.find('script')), 'Local JS is not needed')


def check(source, self_test=False):
    require(hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA, 'Approved EN36 SHA mismatch')
    require(hashlib.sha256(COVER.read_bytes()).hexdigest() == 'b1b1cead7277cd3ece3db662d8d7108b90be56c3de5529f7c5b0888d00e9f408', 'Approved cover changed')
    html = ei07.historical_bytes(ROOT, PAGE.as_posix()).decode()
    errors = v.validate(ROOT / PAGE, COVER, source, ROOT, mode='PUBLICATION', historical_html=html)
    require(not errors, '\n'.join(errors))
    representations(html, source)
    tree = v.Tree(html)
    articles = list(tree.root.find('article', 'guide-section'))
    require(len(articles) == 41, 'Opening and all 40 sections required')
    raw = re.split(r'(?m)^## ', source.read_text())[1:]
    for part, article in zip(raw[1:], articles):
        expected = emphasis(part)
        actual = [(x.tag, v.normalized(v.content(x))) for x in v.walk(article) if x.tag in {'strong', 'em'}]
        require(actual == expected, 'Emphasis changed in ' + article.attrs['id'])
    require(sum('Interpretive module' in v.content(next(x.find('h2'))) for x in articles) == 4, 'Four interpretive modules required')
    visible = [v.normalized(v.content(x)) for x in articles[37].find('h3')]
    faq = next(json.loads(v.content(x)) for x in tree.root.find('script') if x.attrs.get('type') == 'application/ld+json' and json.loads(v.content(x)).get('@type') == 'FAQPage')
    require(len(visible) == 20 and [v.normalized(x['name']) for x in faq['mainEntity']] == visible, 'FAQ schema order must exactly match all 20 visible FAQ')
    source_links = re.findall(r'\[[^]]+\]\(([^)]+)\)', source.read_text())
    links = [x.attrs.get('href') for a in articles for x in a.find('a')]
    require(all(x in links for x in source_links), 'Original Italian-edition links changed')
    original = subprocess.check_output(['git', 'show', f'{BASE}:{IT}'], cwd=ROOT, text=True)
    italian = ei07.historical_bytes(ROOT, IT.as_posix()).decode()
    it_url = 'https://alessandro-gentili.it/' + str(IT.parent) + '/'
    en_url = 'https://alessandro-gentili.it/' + str(PAGE.parent) + '/'
    alternates = '\n' + '\n'.join(f'<link rel="alternate" hreflang="{lang}" href="{url}" />' for lang, url in [('it', it_url), ('en', en_url), ('x-default', it_url)])
    nav = f'<nav class="wrap atlas-breadcrumb" aria-label="Edizioni linguistiche"><a href="/{PAGE.parent}/" lang="en" hreflang="en">English edition</a></nav>\n'
    require(italian.count(alternates) == italian.count(nav) == 1 and italian.replace(alternates, '', 1).replace(nav, '', 1) == original, 'IT36 changed beyond exact language links')
    print('PASS EN36: frozen source/cover, 40 sections, 4 modules, 20 ordered FAQ, emphasis, source tables/timeline, institutional distinctions and immutable IT prose')
    if not self_test:
        return
    with tempfile.TemporaryDirectory(prefix='olivetti-en36-') as d:
        root = Path(d).resolve()
        for parent in [Path('.'), Path('en'), Path('en/cerchi'), Path('en/cerchi/guides')]:
            (root / parent).mkdir(parents=True, exist_ok=True)
            exclude = {'.':'en', 'en':'cerchi', 'en/cerchi':'guides', 'en/cerchi/guides':PAGE.parent.name}[str(parent)]
            for p in (ROOT / parent).iterdir():
                if p.name != exclude:
                    (root / parent / p.name).symlink_to(p, target_is_directory=p.is_dir())
        candidate = root / PAGE
        candidate.parent.mkdir()
        candidate.write_text(html)
        require(not v.validate(candidate, COVER, source, root, mode='PUBLICATION'), 'Regression baseline must pass')
        mutations = [
            ('missing closing paragraph', html.replace('<p>There was also a political undertaking, less immediately visible and harder to accept without reservation.</p>', '', 1)),
            ('consultation changed to strategy control', html.replace('Consultation · art. 28</td>', 'Full control · art. 28</td>', 1)),
            ('allocation confused with budget setting', html.replace('The Council decides how to use sums already set by the company.', 'The Council decides the total services budget.', 1)),
            ('wrong IRUR date', html.replace('Institute founded in 1954', 'Institute founded in 1955', 1)),
            ('wrong post-founder chronology', html.replace('<strong>1963</strong> — Representation', '<strong>1953</strong> — Representation', 1)),
            ('missing FAQ', html.replace('<h3>20. What can Adriano Olivetti teach us today?</h3>', '', 1)),
            ('wrong FAQ answer', html.replace('He was born in Ivrea on 11 April 1901', 'He was born in Ivrea on 12 April 1901', 1)),
            ('altered territorial row', html.replace('<th role="rowheader" scope="row">La Martella</th>', '<th role="rowheader" scope="row">Changed</th>', 1)),
            ('closed no-JS contents', html.replace('<details open>', '<details>', 1)),
        ]
        for label, changed in mutations:
            require(changed != html, 'Inactive mutation: ' + label)
            candidate.write_text(changed)
            require(v.validate(candidate, COVER, source, root, mode='PUBLICATION'), 'Content mutation escaped: ' + label)
            print('PASS rejected ' + label)
        candidate.write_text(html)
        parts = re.split(r'(?m)^## ', source.read_text())
        intro_first = parts[0] + '## ' + parts[2] + '## ' + parts[1] + ''.join('## ' + p for p in parts[3:])
        for label, text in [('contents-first approved', source.read_text()), ('introduction-first equivalent', intro_first)]:
            fixture = root / 'source.md'
            fixture.write_text(text)
            require(v.manuscript_structure(fixture) == v.manuscript_structure(source), 'Layouts must preserve the same complete source structure')
            require(not v.validate(candidate, COVER, fixture, root, mode='PUBLICATION'), 'Legitimate source layout rejected: ' + label)
            print('PASS parser ' + label)
        malformed = [
            ('missing introduction', source.read_text().replace('## Introduction — The city at the factory gate', '## Opening', 1)),
            ('duplicate contents', source.read_text().replace('## Contents', '## Contents\n\n## Contents', 1)),
            ('index gap', source.read_text().replace('2. Why Adriano Olivetti matters', '3. Why Adriano Olivetti matters', 1)),
            ('interleaved H2', source.read_text().replace('## Introduction', '## Extra section\n\n## Introduction', 1)),
            ('empty introduction', parts[0] + '## ' + parts[1] + '## Introduction — The city at the factory gate\n\n' + ''.join('## ' + p for p in parts[3:])),
            ('altered introductory prose', source.read_text().replace('In Ivrea, along Via Jervis', 'In Rome, along Via Jervis', 1)),
            ('missing numbered section', source.read_text().replace('## 2. Why Adriano Olivetti matters', '### Why Adriano Olivetti matters', 1)),
        ]
        for label, text in malformed:
            fixture = root / 'source.md'
            fixture.write_text(text)
            require(v.validate(candidate, COVER, fixture, root, mode='PUBLICATION'), 'Malformed/mutated source escaped: ' + label)
            print('PASS rejected source ' + label)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    check(args.source.resolve(), args.self_test)
