#!/usr/bin/env python3
"""Seven supplied complete EN manuscripts, source-locked conversion only.

No change to the other migration contracts. The source branch is never a PR base.
"""
import argparse
import hashlib
import json
import re
import runpy
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '604872f49f1f7e7b3202f9b57d7b077e7a5775e4'
MANIFEST = ROOT / 'tools/international-complete-guides.json'
parser = runpy.run_path(str(ROOT / 'tools/validate-cerchi-guide.py'))
Tree, Node, walk, content, normal = (parser[k] for k in ['Tree', 'Node', 'walk', 'content', 'normalized'])


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def children(node):
    return [c for c in node.children if isinstance(c, Node)]


def text(node):
    if not isinstance(node, Node):
        return node
    if node.tag == 'math':
        annotations = list(node.find('annotation'))
        require(len(annotations) == 1, 'Missing exact TeX annotation')
        tex = content(annotations[0])
        return (r'\[ ' + tex + r' \]') if node.attrs.get('display') == 'block' else r'\(' + tex + r'\)'
    value = ''.join(text(c) for c in node.children)
    return ' ' if node.tag == 'br' else (' ' + value + ' ' if node.tag in ['p', 'li', 'th', 'td', 'tr', 'blockquote'] else value)


def source_plain(value):
    # This manuscript set has no Markdown links, images, escapes or literal stars.
    return normal(value.replace('*', '').replace('`', ''))


def source_blocks(md):
    lines = md.splitlines()
    output = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line == r'\[':
            values = []
            i += 1
            while lines[i] != r'\]':
                values.append(lines[i])
                i += 1
            output.append(('math', ' '.join(values)))
            i += 1
            continue
        heading = re.fullmatch(r'(#{1,4}) (.+)', line)
        if heading:
            output.append(('h' + str(len(heading[1])), heading[2]))
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            output.append(('table', rows))
            continue
        if line.startswith('> '):
            values = []
            while i < len(lines) and lines[i].startswith('> '):
                values.append(lines[i][2:])
                i += 1
            output.append(('quote', '\n'.join(values)))
            continue
        item = re.match(r'^(- |\d+\. )(.+)', line)
        if item:
            kind = 'ul' if item[1] == '- ' else 'ol'
            values = []
            while i < len(lines):
                item = re.match(r'^- (.+)' if kind == 'ul' else r'^\d+\. (.+)', lines[i])
                if not item:
                    break
                values.append(item[1])
                i += 1
            output.append((kind, values))
            continue
        values = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(?:#{1,4} |\||> |\\\[|\d+\. |- )', lines[i]):
            values.append(lines[i])
            i += 1
        require(values, 'Unsupported Markdown line: ' + line)
        output.append(('p', '\n'.join(values)))
    return output


def source_spans(value):
    """Opening/closing delimiter projection, independent of the HTML renderer."""
    stack, spans = [], []
    for match in re.finditer(r'\*+', value):
        count = len(match[0])
        if match.start() and not value[match.start() - 1].isspace():
            while stack and count >= stack[-1][0]:
                size, start = stack.pop()
                spans.append((start, 'strong' if size == 2 else 'em', source_plain(value[start:match.start()])))
                count -= size
        if count:
            require(match.end() < len(value) and not value[match.end()].isspace(), 'Unbalanced source emphasis')
            while count:
                size = min(2, count)
                stack.append((size, match.end()))
                count -= size
    require(not stack, 'Unclosed source emphasis')
    return [(tag, value) for _, tag, value in sorted(spans, key=lambda x: (x[0], x[1] != 'strong'))]


def compare_inline(node, value):
    require(normal(text(node)) == source_plain(value), 'Text lost/added/rewritten: ' + source_plain(value)[:95])
    actual = [(n.tag, normal(text(n))) for n in walk(node) if n.tag in ['strong', 'em']]
    require(actual == source_spans(value), 'Emphasis changed: ' + source_plain(value)[:95])


def verify_content(html, md, guide):
    tree = Tree(html)
    require(not tree.malformed, 'Malformed HTML: ' + str(tree.malformed))
    nodes = list(walk(tree.root))
    blocks = [n for n in nodes if 'data-source-block' in n.attrs]
    expected = source_blocks(md)
    require(len(blocks) == len(expected) == guide['block_count'], 'Missing/extra manuscript block')
    require([n.attrs['data-source-block'] for n in blocks] == [str(i) for i in range(len(expected))], 'Source order changed')
    for node, (kind, value) in zip(blocks, expected):
        if kind in ['ul', 'ol']:
            require(node.tag == kind and len(children(node)) == len(value), 'List item lost or reordered')
            for item, original in zip(children(node), value):
                require(item.tag == 'li', 'Invalid list')
                compare_inline(item, original)
        elif kind == 'table':
            require(node.tag == 'table', 'Table replaced')
            rows = list(node.find('tr'))
            require(len(rows) == len(value), 'Table row lost')
            for row, originals in zip(rows, value):
                require(len(children(row)) == len(originals), 'Table column lost')
                for cell, original in zip(children(row), originals):
                    compare_inline(cell, original)
        elif kind == 'math':
            require(node.tag == 'div', 'Formula container changed')
            require(normal(text(node)) == normal(r'\[ ' + value + r' \]'), 'Formula/source annotation changed')
        else:
            require(node.tag == ('blockquote' if kind == 'quote' else kind) or kind == 'h4' and node.tag == 'h3', 'Heading/block type changed')
            compare_inline(node, value)
    ids = [n.attrs['id'] for n in nodes if 'id' in n.attrs]
    require(len(ids) == len(set(ids)), 'Duplicate ID')
    require(set(guide['legacy_anchors']) <= set(ids), 'Historical section anchor removed')
    for a in [n for n in nodes if n.tag == 'a' and n.attrs.get('href', '').startswith('#')]:
        require(a.attrs['href'][1:] in ids, 'Broken local fragment: ' + a.attrs['href'])
    for tag in ['html', 'head', 'body', 'header', 'main', 'footer', 'h1']:
        require(len([n for n in nodes if n.tag == tag]) == 1, 'Invalid template: ' + tag)
    require(next(n for n in nodes if n.tag == 'html').attrs.get('lang') == 'en', 'Wrong language')
    previous = 1
    for n in [n for n in nodes if n.tag in ['h1', 'h2', 'h3', 'h4']]:
        level = int(n.tag[1])
        require(level <= previous + 1, 'Skipped heading level')
        previous = level
    toc = list(next(n for n in nodes if n.tag == 'nav' and 'guide-toc' in n.attrs.get('class', '').split()).find('a'))
    require(len(toc) == len(guide['toc_aliases']), 'TOC entry missing')
    for anchor, alias in zip(toc, guide['toc_aliases']):
        require(normal(text(anchor)) == source_plain(alias['label']) and anchor.attrs['href'] == '#' + alias['id'], 'TOC alias/target changed')
        target = next(n for n in nodes if n.attrs.get('id') == alias['id'])
        heading = next((n for n in walk(target) if n.tag in ['h2', 'h3', 'h4']), None)
        require(heading is not None and normal(text(heading)) == source_plain(alias['heading']), 'TOC targets wrong argument')
    faq_start = next(i for i, (kind, val) in enumerate(expected) if kind == 'h2' and val in ['FAQ', 'Frequently Asked Questions'])
    faq = []
    for kind, val in expected[faq_start + 1:]:
        if kind == 'h2':
            break
        if kind in ['h3', 'h4']:
            faq.append([source_plain(val), []])
        else:
            require(kind == 'p', 'Unexpected FAQ structure')
            faq[-1][1].append(source_plain(val))
    schemas = [json.loads(content(n)) for n in nodes if n.tag == 'script' and n.attrs.get('type') == 'application/ld+json']
    machine = next(x for x in schemas if x.get('@type') == 'FAQPage')['mainEntity']
    require(len(faq) == len(machine) == guide['faq_count'], 'FAQ missing')
    require([(q, ' '.join(a)) for q, a in faq] == [(x['name'], x['acceptedAnswer']['text']) for x in machine], 'FAQPage differs from approved visible FAQ')
    glossary = next(n for n in nodes if n.attrs.get('data-consult') == 'glossary')
    require(len([n for n in walk(glossary) if 'data-consult-row' in n.attrs]) == guide['glossary_count'], 'Glossary term missing')


def protections(old, new):
    require(set(re.findall(r'\bid="([^"]+)"', old)) <= set(re.findall(r'\bid="([^"]+)"', new)), 'Historical ID removed')
    for pattern in [r'<meta\b[^>]*>', r'<title>.*?</title>', r'<link\b[^>]*(?:rel="canonical"|rel="alternate")[^>]*>', r'<header\b.*?</header>', r'<footer\b.*?</footer>', r'<figure class="editorial-cover-card guide-cover">.*?</figure>']:
        require(re.findall(pattern, old, re.S) == re.findall(pattern, new, re.S), 'Protected SEO/header/footer/cover changed')
    figures = re.findall(r'<figure class="atlas-figure[^\"]*".*?</figure>', old, re.S)
    require([f.replace('*De rerum natura*', '<em>De rerum natura</em>') for f in figures] == re.findall(r'<figure class="atlas-figure[^\"]*".*?</figure>', new, re.S), 'Published native instrument changed/missing/duplicated')
    original = [json.loads(x) for x in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', old, re.S)]
    revised = [json.loads(x) for x in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', new, re.S)]
    for schema in original:
        if schema['@type'] == 'FAQPage':
            continue
        match = next(x for x in revised if x['@type'] == schema['@type'])
        if schema['@type'] == 'Article':
            match = dict(match)
            require(match.pop('dateModified') == '2026-11-07', 'Wrong revision date')
            schema = dict(schema)
            schema.pop('dateModified')
        require(match == schema, 'Article/Breadcrumb fact changed')
    scripts = re.findall(r'<script src="([^"]+)"', old)
    require(all(new.count('src="' + script + '"') == 1 for script in scripts), 'Shared script removed/duplicated')


def source(guide):
    try:
        raw = subprocess.check_output(['git', 'show', SOURCE + ':' + guide['source']], cwd=ROOT, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        subprocess.run(['git', 'fetch', '--no-tags', 'origin', SOURCE], cwd=ROOT, check=True)
        raw = subprocess.check_output(['git', 'show', SOURCE + ':' + guide['source']], cwd=ROOT)
    require(hashlib.sha256(raw).hexdigest() == guide['source_sha256'], 'Source manuscript changed')
    return raw.decode()


def self_test():
    manifest = json.loads(MANIFEST.read_text())
    rejected = 0
    for guide in manifest['guides']:
        original = (ROOT / guide['page']).read_text()
        md = source(guide)
        old = subprocess.check_output(['git', 'show', manifest['base'] + ':' + guide['page']], cwd=ROOT, text=True)
        mutations = [
            ('source order', original.replace('data-source-block="1"', 'data-source-block="9999"', 1), True),
            ('emphasis', original.replace('<strong>', '', 1).replace('</strong>', '', 1), True),
            ('visible text', re.sub(r'(<p[^>]*data-source-block="1"[^>]*>)', r'\1UNAPPROVED ', original, count=1), True),
            ('FAQ schema', re.sub(r'("@type": "Question",\s*"name": ")[^"]+', r'\1UNAPPROVED FAQ', original, count=1), True),
            ('anchor', original.replace('id="' + guide['legacy_anchors'][0] + '"', 'id="removed-anchor"', 1), True),
            ('template', original.replace('</main>', '', 1), True),
            ('canonical', original.replace('rel="canonical"', 'rel="invalid"', 1), False),
            ('datePublished', re.sub(r'("datePublished": ")[^"]+', r'\g<1>1900-01-01', original, count=1), False)
        ]
        if guide.get('native_figure'):
            mutations.append(('native radio control', original.replace('type="radio"', 'type="checkbox"', 1), False))
        for name, changed, semantic in mutations:
            require(changed != original, 'Invalid mutation fixture: ' + name)
            try:
                verify_content(changed, md, guide) if semantic else protections(old, changed)
            except AssertionError:
                rejected += 1
            else:
                raise AssertionError('Mutation admitted: ' + guide['author'] + ' / ' + name)
    print(f'PASS {rejected} complete-guide semantic/template/SEO mutations; snapshot pins not bypassed in release checks')


def verify(path, base):
    manifest = json.loads(MANIFEST.read_text())
    relative = path.resolve().relative_to(ROOT).as_posix()
    guide = next(g for g in manifest['guides'] if g['page'] == relative)
    require(manifest['source_commit'] == SOURCE, 'Unapproved source commit')
    require(git('rev-parse', base + ':' + relative) == guide['baseline_blob'], 'Published baseline changed')
    require(git('hash-object', relative) == guide['html_blob'], 'Unreviewed guide snapshot')
    require(git('hash-object', guide['italian']) == guide['italian_blob'], 'Italian guide changed')
    for asset, expected in manifest['asset_sha256'].items():
        require(hashlib.sha256((ROOT / asset).read_bytes()).hexdigest() == expected, 'Unreviewed scoped asset: ' + asset)
    if relative == manifest['guides'][0]['page']:
        self_test()
        subprocess.run(['node', '--check', str(ROOT / 'assets/international-complete-guides.js')], check=True)
        subprocess.run(['node', str(ROOT / 'tools/check-international-complete-guides.mjs')], check=True)
    md = source(guide)
    new = path.read_text()
    old = subprocess.check_output(['git', 'show', base + ':' + relative], cwd=ROOT, text=True)
    protections(old, new)
    verify_content(new, md, guide)
    print(f"PASS complete EN {guide['author']}: {guide['block_count']} ordered source blocks, inline emphasis/quotes/math/lists/tables, {guide['faq_count']} FAQ, {guide['glossary_count']} terms; SEO/cover/template preserved")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True)
    args = ap.parse_args()
    for guide in json.loads(MANIFEST.read_text())['guides']:
        verify(ROOT / guide['page'], args.base)
