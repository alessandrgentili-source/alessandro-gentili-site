#!/usr/bin/env python3
"""Validate the explicitly authorized Plato EN v2 revision against its pinned manuscript.

This is a single-publication contract, not a narrative template for other authors.
The original migration gate remains the default for every other page/baseline.
No network access or HTML generation occurs here. CI fetches the source commit.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAGE = 'en/cerchi/guides/plato-ideas-truth-power/index.html'
SOURCE_COMMIT = 'f36e2f29a7ea9ec6e691244c851ad3b877ed236a'
SOURCE_PATH = 'PLATO_EN_GUIDE_01_CANDIDATE_v2.md'
SOURCE_SHA256 = 'cc1f612a1698ce8e5c1a165945341085a77f6eb2bc93962647b0d9e13fe4b378'
BASE_PAGE_SHA256 = 'f91e27dd11b643198858753041330e0aabec3a4810af8e583d3f4344dd8193df'
MODIFIED = '2026-11-05'
WORKFLOW_LABEL = ' · Editorial candidate v2 — not approved for publication'
# Reuse only the repository's strict HTML parser, not its Italian publication policy.
legacy = runpy.run_path(str(ROOT / 'tools/validate-cerchi-guide.py'))
Tree, Node, walk = (legacy[k] for k in ('Tree', 'Node', 'walk'))
normalized, content = (legacy[k] for k in ('normalized', 'content'))


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def git_text(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT).decode('utf-8')


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def applies(relative, before):
    return relative == PAGE and digest(before) == BASE_PAGE_SHA256


def load_source(path=None):
    source = Path(path).read_bytes().decode('utf-8') if path else git_text(SOURCE_COMMIT, SOURCE_PATH)
    require(digest(source) == SOURCE_SHA256, 'Manuscript differs from the authorized source commit/hash')
    return source


def inline(markdown):
    """Return a small inline tree; fail on unrecognized markup rather than dropping it."""
    root = Node()
    def parse(value, node):
        while value:
            if value.startswith('['):
                match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', value)
                require(match is not None, 'Unsupported Markdown link')
                child = Node('a', [('href', match[2])]); parse(match[1], child)
                node.children.append(child); value = value[len(match[0]):]; continue
            token = '**' if value.startswith('**') else '*' if value.startswith('*') else None
            if token:
                end = value.find(token, len(token))
                require(end >= 0, 'Unclosed Markdown emphasis')
                child = Node('strong' if token == '**' else 'em')
                parse(value[len(token):end], child); node.children.append(child)
                value = value[end + len(token):]; continue
            match = re.match(r'[^*\[]+', value)
            require(match is not None, 'Unsupported Markdown inline syntax')
            node.children.append(match[0]); value = value[len(match[0]):]
    parse(markdown, root)
    return root


def signature(node):
    # Text and every emphasis/link span are checked, including nested italics in FAQ 8.
    spans = [(n.tag, normalized(content(n)), n.attrs.get('href'))
             for n in walk(node) if n.tag in ('em', 'strong', 'a')]
    return normalized(content(node)), spans


def md_signature(value):
    return signature(inline(value))


def manuscript_blocks(source):
    lines = source.splitlines(); blocks = []; i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line == '---':
            i += 1; continue
        heading = re.fullmatch(r'(#{1,3}) (.+)', line)
        if heading:
            blocks.append(('h' + str(len(heading[1])), heading[2])); i += 1; continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', x) for x in cells):
                    rows.append(cells)
                i += 1
            require(rows and len({len(row) for row in rows}) == 1, 'Invalid Markdown table')
            blocks.append(('table', rows)); continue
        if line.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '):
                items.append(lines[i][2:]); i += 1
            blocks.append(('ul', items)); continue
        require(not line.startswith(('#', '```', '~~~', '<', '>')), 'Unsupported Markdown block')
        paragraph = []
        while i < len(lines) and lines[i].strip():
            paragraph.append(lines[i].strip()); i += 1
        blocks.append(('p', ' '.join(paragraph)))
    return blocks


def expected_body(blocks):
    result = []; in_faq = False; faq = []
    for kind, value in blocks[3:]:
        if kind == 'h2':
            in_faq = value == 'Frequently asked questions'
        if in_faq and kind == 'p':
            match = re.fullmatch(r'\*\*(.+\?)\*\*\s+(.+)', value)
            require(match is not None, 'Invalid source FAQ paragraph')
            question, answer = match.groups()
            result.extend([('h3', md_signature(question)), ('p', md_signature(answer))])
            faq.append((md_signature(question)[0], md_signature(answer)[0])); continue
        if kind == 'table':
            result.append((kind, [[md_signature(cell) for cell in row] for row in value]))
        elif kind == 'ul':
            result.append((kind, [md_signature(item) for item in value]))
        else:
            result.append(('p' if kind == 'h1' else kind, md_signature(value)))
    return result, faq


def find_one(root, tag=None, cls=None, identifier=None):
    nodes = [n for n in walk(root) if (not tag or n.tag == tag)
             and (not cls or cls in n.attrs.get('class', '').split())
             and (not identifier or n.attrs.get('id') == identifier)]
    require(len(nodes) == 1, f'Expected one {tag or "element"} {cls or identifier or ""}')
    return nodes[0]


def actual_blocks(node):
    result = []
    for child in node.children:
        if not isinstance(child, Node):
            require(not child.strip(), 'Text outside a semantic editorial block'); continue
        if child.tag == 'table':
            rows = []
            for row in child.find('tr'):
                cells = [n for n in row.children if isinstance(n, Node) and n.tag in ('th', 'td')]
                require(cells and cells[0].tag == 'th', 'Table row lacks a semantic header')
                rows.append([signature(cell) for cell in cells])
            result.append(('table', rows))
        elif child.tag == 'ul':
            result.append(('ul', [signature(n) for n in child.children if isinstance(n, Node)]))
        elif child.tag in ('h2', 'h3', 'p'):
            result.append((child.tag, signature(child)))
        else:
            result.extend(actual_blocks(child))
    return result


def verify_html(after, before, source):
    require(applies(PAGE, before), 'Revision must replace the recorded legacy Plato page')
    require(digest(source) == SOURCE_SHA256, 'Unapproved editorial source')
    tree = Tree(after); old = Tree(before)
    require(not tree.malformed, f'Malformed HTML: {tree.malformed}')
    root = tree.root
    for tag in ('title', 'h1', 'footer'):
        pattern = rf'<{tag}\b.*?</{tag}>'
        require(re.findall(pattern, before, re.S) == re.findall(pattern, after, re.S), f'{tag} changed')
    for cls in ('site-header', 'guide-cover'):
        require(content(find_one(old.root, cls=cls)) == content(find_one(root, cls=cls)), f'{cls} text changed')
    header = r'<header class="site-header".*?</header>'
    require(re.findall(header, before, re.S) == re.findall(header, after, re.S), 'Shared header changed')
    require(find_one(root, 'html').attrs.get('lang') == 'en', 'Language must remain EN')
    require(len(list(root.find('h1'))) == 1, 'Exactly one H1 is required')
    require([n.attrs for n in old.root.find('meta')] == [n.attrs for n in root.find('meta')], 'SEO metadata changed')
    for rel in ('canonical', 'alternate'):
        require([n.attrs for n in old.root.find('link') if n.attrs.get('rel') == rel] ==
                [n.attrs for n in root.find('link') if n.attrs.get('rel') == rel], f'{rel} changed')
    images = lambda r: [(n.attrs.get('src'), n.attrs.get('alt')) for n in r.find('img')]
    require(images(old.root) == images(root), 'Cover or alt changed')
    def schemas(r):
        objects = [json.loads(content(n)) for n in r.find('script') if n.attrs.get('type') == 'application/ld+json']
        require(len({o['@type'] for o in objects}) == len(objects), 'Duplicate schema type')
        return {o['@type']: o for o in objects}
    previous, current = schemas(old.root), schemas(root)
    require(set(current) == {'Article', 'BreadcrumbList', 'FAQPage'}, 'Unexpected or missing schemas')
    for kind, value in previous.items():
        expected = deepcopy(value)
        if kind == 'Article': expected['dateModified'] = MODIFIED
        require(current[kind] == expected, f'Protected {kind} facts changed')
    blocks = manuscript_blocks(source)
    require(signature(find_one(root, 'h1')) == md_signature(blocks[0][1]), 'Source title mismatch')
    require(signature(find_one(root, 'p', 'lead')) == md_signature(blocks[1][1]), 'Source subtitle mismatch')
    bylines = re.split(r'\*\*\s+\*\*', blocks[2][1])
    require(len(bylines) == 2, 'Expected two source bylines')
    require(normalized(content(find_one(root, 'p', 'eyebrow'))) == bylines[0].strip('*'), 'Source collection label changed')
    require(normalized(content(find_one(root, 'p', 'atlas-byline'))) == bylines[1].strip('*').replace(WORKFLOW_LABEL, ''), 'Source attribution changed')
    require('Editorial candidate v2' not in after, 'Workflow disclaimer must not be published')
    expected, faq = expected_body(blocks)
    reading = find_one(root, cls='atlas-reading')
    # Repeated mobile labels are presentation aids; each must reproduce its actual column header.
    for table in reading.find('table'):
        headers = [normalized(content(n)) for n in next(table.find('tr')).find('th')]
        for row in list(table.find('tr'))[1:]:
            for index, cell in enumerate(row.find('td'), 1):
                labels = list(cell.find('span', 'plato-cell-label'))
                require(len(labels) == 1 and labels[0].attrs.get('aria-hidden') == 'true'
                        and normalized(content(labels[0])) == headers[index], 'Invalid mobile column label')
                cell.children.remove(labels[0])
    require(actual_blocks(reading) == expected, 'Markdown/HTML block, text, emphasis, link or order mismatch')
    faq_node = find_one(root, identifier='faq')
    visible_faq = [(normalized(content(find_one(n, 'h3'))), normalized(content(find_one(n, 'p'))))
                   for n in faq_node.find('section')]
    schema_faq = [(q['name'], q['acceptedAnswer']['text']) for q in current['FAQPage']['mainEntity']]
    require(len(faq) == 9 and visible_faq == schema_faq == faq, 'All nine FAQ pairs must match source and schema in order')
    ids = [n.attrs['id'] for n in walk(root) if 'id' in n.attrs]
    old_ids = {n.attrs['id'] for n in walk(old.root) if 'id' in n.attrs}
    require(len(ids) == len(set(ids)) and old_ids.issubset(ids), 'Duplicate or lost legacy anchor')
    for link in root.find('a'):
        href = link.attrs.get('href', '')
        require(not href.startswith('#') or href[1:] in ids, 'Broken fragment')
    toc = find_one(root, 'nav', 'guide-toc'); links = list(toc.find('a'))
    sections = [n for n in walk(reading) if n.tag == 'article' or 'plato-part' in n.attrs.get('class', '').split()]
    require([n.attrs.get('href') for n in links] == ['#' + n.attrs['id'] for n in sections], 'TOC must cover both levels and every section in order')
    for link, section in zip(links, sections):
        title = next((n for n in walk(section) if n.tag in ('h2', 'p')), None)
        require(normalized(content(link)) == normalized(content(title)), 'TOC label differs from section title')
    details = find_one(find_one(root, cls='atlas-contents'), 'details')
    require('open' in details.attrs, 'TOC must be open without JavaScript')
    require(len(list(reading.find('h2'))) == 18, 'Unexpected editorial section hierarchy')
    module = find_one(root, 'figure', 'plato-return')
    require(module.attrs.get('aria-labelledby') == 'return-problem' and
            len(list(module.find('tr'))) == 5 and not list(module.find('button')), 'Return module structure changed')
    for asset in ('/assets/international-atlas.css', '/assets/international-plato.css'):
        require(any(n.attrs.get('href') == asset for n in root.find('link')), 'Required stylesheet missing')
    require(any(n.attrs.get('src') == '/assets/international-atlas.js' for n in root.find('script')), 'Shared behaviour missing')
    return len(expected)


def verify(path, base, source_path=None, cover=None):
    require(path.resolve() == (ROOT / PAGE).resolve(), 'No other guide is authorized by this revision contract')
    if cover:
        require(cover.resolve() == (ROOT / 'assets/img/cerchi/cerchi-platone-idee-verita-potere-1600x900.jpg').resolve(), 'Original cover must be preserved')
    source = load_source(source_path); before = git_text(base, PAGE)
    count = verify_html(path.read_text(), before, source)
    print(f'PASS EN revision: {count} ordered blocks, all inline emphasis/links, 3 tables, 9 exact FAQ pairs; protected facts preserved')
    return source, before


def self_test(after, before, source):
    mutations = {
        'lost paragraph': after.replace('<p>This is Plato’s account', '<p>ALTERED This is Plato’s account', 1),
        'lost table cell': after.replace('His new knowledge is inaccessible to them.', '', 1),
        'lost glossary term': after.replace('<em>Epistēmē</em>', '<em>Missing</em>', 1),
        'lost FAQ with italic titles': after.replace('<h3>What changes between the <em>Republic</em> and the <em>Laws</em>?</h3>', '', 1),
        'lost emphasis': after.replace('<em>Apology</em>', 'Apology', 1),
        'extra editorial text': after.replace('</div></div></main>', '<p>Extra text.</p></div></div></main>', 1),
        'changed schema answer': after.replace('"text": "Plato was an Athenian', '"text": "Changed Plato was an Athenian', 1),
        'changed publication date': after.replace('"datePublished": "2026-05-19"', '"datePublished": "2026-11-05"', 1),
        'changed cover': after.replace('alt="Editorial cover for Plato."', 'alt="Changed cover"', 1),
        'wrong TOC order': after.replace('href="#forms"', 'href="#city"', 1),
        'changed source link': after.replace('https://alessandro-gentili.it/en/cerchi/guides/dante-exile-language-divine-comedy/', 'https://example.com/', 1),
    }
    for label, candidate in mutations.items():
        require(candidate != after, f'Ineffective mutation: {label}')
        try:
            verify_html(candidate, before, source)
        except (AssertionError, ValueError, KeyError):
            continue
        raise AssertionError(f'Undetected mutation: {label}')
    try:
        verify_html(after, before, source + '\n')
    except AssertionError:
        pass
    else:
        raise AssertionError('Changed source hash accepted')
    print(f'PASS {len(mutations) + 1} revision mutations: content, FAQ, emphasis, tables, glossary, links, metadata and source hash')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    source, before = verify(ROOT / PAGE, args.base, args.source)
    if args.self_test: self_test((ROOT / PAGE).read_text(), before, source)
