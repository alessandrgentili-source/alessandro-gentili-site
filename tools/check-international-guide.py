#!/usr/bin/env python3
"""Guard an existing EN guide migration against a Git reference; no HTML generation.

Usage: python3 tools/check-international-guide.py --base origin/main [GUIDE ...]
With no paths, check guides explicitly using international-atlas.css.
New manuscripts require the separate editorial/publication procedure.
"""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = r'<article\b(?=[^>]*\bclass="[^"]*\bguide-section\b)[^>]*>.*?</article>'


def require(condition, message):
    if not condition:
        raise AssertionError(message)


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.meta, self.alternates, self.ids, self.links, self.images, self.toc = [], [], [], [], [], []
        self.lang = None
        self.in_toc = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'meta':
            self.meta.append(a)
        if tag == 'link' and a.get('rel') in ('canonical', 'alternate'):
            self.alternates.append(a)
        if a.get('id'):
            self.ids.append(a['id'])
        if tag == 'nav' and 'guide-toc' in a.get('class', '').split():
            self.in_toc = True
        if tag == 'a':
            self.links.append(a.get('href'))
            if self.in_toc:
                self.toc.append(a.get('href'))
        if tag == 'img':
            self.images.append((a.get('src'), a.get('alt')))

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.in_toc = False


def preserves(old, new):
    """Existing schema facts cannot change; additions still need editorial review."""
    if isinstance(old, dict):
        return isinstance(new, dict) and all(k in new and preserves(v, new[k]) for k, v in old.items())
    if isinstance(old, list):
        return isinstance(new, list) and len(old) == len(new) and all(preserves(a, b) for a, b in zip(old, new))
    return old == new


def verify(path, base):
    relative = path.resolve().relative_to(ROOT).as_posix()
    require(relative.startswith('en/cerchi/guides/'), f'Not an existing EN guide: {relative}')
    before = subprocess.check_output(['git', 'show', f'{base}:{relative}'], cwd=ROOT, text=True)
    after = path.read_text()
    old, new = Page(before), Page(after)
    blocks = re.findall(BLOCKS, before, re.S)
    require(blocks and blocks == re.findall(BLOCKS, after, re.S), 'Approved articles changed, missing or reordered')
    for tag in ('title', 'h1', 'header', 'footer'):
        pattern = rf'<{tag}\b.*?</{tag}>'
        require(re.findall(pattern, before, re.S) == re.findall(pattern, after, re.S), f'{tag} changed')
    require(old.lang == new.lang == 'en', 'Language changed')
    require(old.meta == new.meta and old.alternates == new.alternates, 'Metadata, canonical or hreflang changed')
    require(all(link in new.links for link in old.links), 'An existing link was removed')
    require(all(image in new.images for image in old.images), 'An approved image or alt was changed')
    require(len(new.ids) == len(set(new.ids)), 'Duplicate IDs')
    require(set(old.ids).issubset(new.ids), 'An existing anchor was removed')
    article_ids = [Page(block).ids[0] for block in blocks if Page(block).ids]
    require(new.toc and len(new.toc) == len(set(new.toc)), 'Empty or duplicate guide contents')
    require(all(href and href.startswith('#') and href[1:] in article_ids for href in new.toc), 'Contents must target original sections')
    order = [article_ids.index(href[1:]) for href in new.toc]
    require(order == sorted(order), 'Contents out of article order')
    require(set(old.toc).issubset(new.toc), 'An existing contents entry was removed')
    pattern = r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'
    old_schema = [json.loads(raw) for raw in re.findall(pattern, before, re.S)]
    new_schema = [json.loads(raw) for raw in re.findall(pattern, after, re.S)]
    require(preserves(old_schema, new_schema), 'An existing JSON-LD fact was changed')
    require('international-atlas.css' in after and 'international-atlas.js' in after, 'Shared assets missing')
    require(re.search(r'<details\s+open(?:\s|>)', after), 'Contents must remain open without JS')
    for token in ('atlas-main', 'atlas-guide-opening', 'atlas-reader', 'atlas-contents', 'atlas-reading'):
        require(token in after, f'Missing shared component: {token}')
    print(f'PASS {relative}: {len(blocks)} original blocks, metadata, schema facts, cover, links and contents preserved')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True, help='Immutable pre-migration commit or fetched base ref')
    parser.add_argument('guides', nargs='*', type=Path)
    args = parser.parse_args()
    paths = args.guides or [p for p in ROOT.glob('en/cerchi/guides/*/index.html') if 'international-atlas.css' in p.read_text()]
    require(paths, 'No International guide found')
    for path in paths:
        verify(path, args.base)
