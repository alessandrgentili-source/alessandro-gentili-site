#!/usr/bin/env python3
"""Source-pinned Smith EN15 review gate. A passing test is not editorial approval."""
import json
import re
import subprocess
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = 'en/cerchi/guides/adam-smith-exchange-sympathy-wealth/index.html'
SOURCE_COMMIT = 'da06d8ec473fae4a82e69b023be084e6a1149c8a'
SOURCE_FILE = 'SMITH_EN_GUIDE_15_CANDIDATE_v1.md'
SOURCE_BLOB = 'a6eae112b4a9c3353eebc948bf7ba763d951b4c5'
BASE_BLOB = '410e3b8e4c80f8733cd89dde01058f5b8c6519d0'
CANONICAL = 'https://alessandro-gentili.it/en/cerchi/guides/adam-smith-exchange-sympathy-wealth/'


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def git(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT, text=True)


def tokens(text):
    return re.findall(r'[^\W_]+', text, flags=re.UNICODE)


def manuscript_tokens(source):
    check(source.startswith('# Adam Smith\n'), 'Unexpected manuscript title')
    check("## A reader's route" in source, 'No reader route')
    paragraphs = []
    for line in source[source.index("## A reader's route"):].splitlines():
        line = line.strip()
        if not line or line == '---':
            continue
        heading = bool(re.match(r'^#{2,3}\s', line))
        line = re.sub(r'^#{2,3}\s+', '', line)
        if not heading:
            line = re.sub(r'^[-*]\s+', '', line)
            line = re.sub(r'^\d+\.\s+', '', line)
        line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
        paragraphs.append(line.replace('**', '').replace('*', '').replace('`', ''))
    return tokens(' '.join(paragraphs))


class EditorialReader(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
            'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skipping = 0
        self.words = []

    def handle_starttag(self, name, attrs):
        if self.skipping:
            if name not in self.VOID:
                self.skipping += 1
        elif dict(attrs).get('data-smith-ui') == '1':
            self.skipping = 1

    def handle_startendtag(self, name, attrs):
        # A self-closing input must not consume a closing tag from its parent.
        pass

    def handle_endtag(self, name):
        if self.skipping:
            self.skipping -= 1

    def handle_data(self, text):
        if not self.skipping:
            self.words.append(text)


def text_of(fragment):
    return ' '.join(unescape(re.sub(r'<[^>]+>', ' ', fragment)).split())


def schemas(page):
    return [json.loads(x) for x in re.findall(
        r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        page, flags=re.S)]


def verify(path, base):
    check(path.resolve().relative_to(ROOT).as_posix() == PAGE, 'Wrong guide path')
    check(subprocess.check_output(['git', 'rev-parse', f'{base}:{PAGE}'],
                                  cwd=ROOT, text=True).strip() == BASE_BLOB,
          'Original Smith page changed since this revision was prepared')
    probe = subprocess.run(['git', 'rev-parse', f'{SOURCE_COMMIT}:{SOURCE_FILE}'],
                           cwd=ROOT, text=True, capture_output=True)
    if probe.returncode:
        subprocess.run(['git', 'fetch', '--no-tags', 'origin', SOURCE_COMMIT],
                       cwd=ROOT, check=True)
        probe = subprocess.run(['git', 'rev-parse', f'{SOURCE_COMMIT}:{SOURCE_FILE}'],
                               cwd=ROOT, text=True, capture_output=True, check=True)
    check(probe.stdout.strip() == SOURCE_BLOB, 'Pinned Markdown source blob changed')
    manuscript = git(SOURCE_COMMIT, SOURCE_FILE)
    old = git(base, PAGE)
    page = path.read_text(encoding='utf-8')
    check(page.startswith('<!doctype html>') and page.endswith('</html>\n'), 'Incomplete page')
    check(page.count('<h1>') == 1 and '<h1>Adam Smith</h1>' in page, 'Invalid H1')
    check('<body class="guide-page international-atlas atlas-guide atlas-smith">' in page,
          'International 3.0 template absent')
    check('<details open>' in page and 'atlas-reader' in page and 'atlas-contents' in page,
          'Static contents/navigation absent')
    for tag in ('header', 'main', 'footer'):
        check(len(re.findall(fr'<{tag}\b', page)) == len(re.findall(fr'</{tag}>', page)) == 1,
              f'{tag} count changed')
    for name in ('/assets/script.js', 'international-atlas.css', 'international-atlas.js',
                 'international-smith.css', 'international-smith.js'):
        check(name in page, f'Missing shared or Smith-specific asset: {name}')
    for name in ('assets/international-smith.css', 'assets/international-smith.js'):
        check((ROOT / name).is_file(), f'Asset not present: {name}')
    for tag in ('title', 'meta'):
        pat = fr'<{tag}\b[^>]*?(?:/>|</{tag}>)'
        check(re.findall(pat, old, re.S) == re.findall(pat, page, re.S),
              f'Protected {tag} values changed')
    old_links = re.findall(r'<link\b[^>]*>', old)
    new_links = [x for x in re.findall(r'<link\b[^>]*>', page)
                 if 'international-atlas.css' not in x and 'international-smith.css' not in x]
    check(old_links == new_links, 'Canonical, hreflang or original stylesheet changed')
    for pat in (r'<header class="site-header".*?</header>',
                r'<footer class="footer".*?</footer>',
                r'<figure class="editorial-cover-card guide-cover".*?</figure>'):
        before, after = re.search(pat, old, re.S), re.search(pat, page, re.S)
        check(before and after and before.group() == after.group(), 'Protected chrome/cover changed')
    orig, new = schemas(old), schemas(page)
    check(len(orig) == 2 and len(new) == 3, 'Article, BreadcrumbList and FAQPage required')
    article, prior = dict(new[0]), dict(orig[0])
    check(article.pop('dateModified') == '2026-11-06'
          and prior.pop('dateModified') == '2026-09-24' and article == prior,
          'Article facts or dates altered')
    check(new[1] == orig[1], 'Breadcrumb structured data changed')
    check(new[2].get('@type') == 'FAQPage'
          and new[2].get('@id') == CANONICAL + '#faq', 'FAQPage schema identity')
    visible = [(text_of(q), text_of(a)) for q, a in re.findall(
        r'<section class="smith-faq"><h3>(.*?)</h3><p>(.*?)</p></section>', page, re.S)]
    structured = [(entry['name'], entry['acceptedAnswer']['text'])
                  for entry in new[2]['mainEntity']]
    check(len(visible) == 20 and visible == structured, 'Visible FAQ/JSON-LD mismatch')
    ids = re.findall(r'\bid="([^"]+)"', page)
    check(len(ids) == len(set(ids)), 'Duplicate HTML id')
    check(set(re.findall(r'\bid="([^"]+)"', old)).issubset(ids), 'Legacy anchor missing')
    article_ids = re.findall(r'<article class="item guide-section[^"]*" id="([^"]+)"', page)
    nav = re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>', page, re.S)
    check(len(article_ids) == 38 and nav is not None,
          f'Unexpected Smith section count {len(article_ids)}')
    check(re.findall(r'href="#([^"]+)"', nav.group(1)) == article_ids,
          'TOC not complete or out of source order')
    for href in re.findall(r'\[[^\]]+\]\((https?://[^)]+)\)', manuscript):
        check('href="' + href + '"' in page, 'Source link dropped: ' + href)
    body = re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">',
                     page, re.S)
    check(body is not None, 'Static reading body missing')
    parser = EditorialReader()
    parser.feed(body.group(1))
    expected, actual = manuscript_tokens(manuscript), tokens(' '.join(parser.words))
    if expected != actual:
        import itertools
        position = next((i for i, pair in enumerate(itertools.zip_longest(expected, actual))
                         if pair[0] != pair[1]), -1)
        raise AssertionError(f'Source/HTML parity fails ({len(expected)}/{len(actual)}), '
                             f'first difference {position}: '
                             f'{expected[position:position+7]!r} vs {actual[position:position+7]!r}')
    check(len(actual) == 13682, 'Pinned source has unexpected token count')
    check(page.count('class="smith-step smith-step-') == 7,
          'Not all seven ledger stages are present')
    glossary = re.search(r'<table\b[^>]*id="smith-glossary-table".*?</table>', page, re.S)
    check(glossary and len(re.findall(r'<tr\b', glossary.group())) == 26,
          '25 glossary entries plus header required')
    css = (ROOT / 'assets/international-smith.css').read_text()
    js = (ROOT / 'assets/international-smith.js').read_text()
    check('@media print' in css and 'tr[hidden]' in css and 'beforeprint' in js,
          'Full print fallback missing')
    check('controls.hidden = false' in js and "input.addEventListener('input', filter)" in js,
          'Glossary does not expose live search')
    for i in range(8):
        check(f'id="smith-view-{i}"' in page, f'Radio view {i} absent')
    check('name="smith-view"' in page and 'role="region"' in page
          and 'tabindex="0"' in page, 'Keyboard accessible controls missing')
    subprocess.run(['node', '--check', str(ROOT / 'assets/international-smith.js')],
                   cwd=ROOT, check=True)
    print('PASS Smith EN15: 13682 source-exact tokens, 38 sections, '
          '20 visible/schema FAQ, 25 glossary rows, 7 native views, protected SEO/cover')


if __name__ == '__main__':
    import argparse
    args = argparse.ArgumentParser()
    args.add_argument('--base', required=True)
    verify(ROOT / PAGE, args.parse_args().base)
