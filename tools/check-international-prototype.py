#!/usr/bin/env python3
"""Integrity and scope gate for the two-page International 3.0 prototype."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASELINE = 'e9df7f0f853e35c0cd70f60b3b4b5011efe1cae4'
HUB = 'en/cerchi/index.html'
GUIDE = 'en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/index.html'
ALLOWED = {HUB, GUIDE, 'assets/international-atlas.css', 'assets/international-atlas.js',
           'assets/international-pasolini.css', 'tools/check-international-guide.py',
           'tools/check-international-atlas.mjs', '.github/workflows/check-internationalization.yml',
           'tools/check-international-prototype.py', 'tools/preview-international.py'}


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASELINE}:{path}'], cwd=ROOT, text=True)


def require(value, message):
    if not value:
        raise AssertionError(message)


class Structure(HTMLParser):
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):
        super().__init__()
        self.stack = []
        self.ids = []
        self.anchors = []
        self.counts = {}
        self.images = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.counts[tag] = self.counts.get(tag, 0) + 1
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.anchors.append(attrs.get('href', ''))
        if tag == 'img':
            self.images.append(attrs)
        if tag not in self.VOID:
            self.stack.append(tag)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)
    def handle_endtag(self, tag):
        require(self.stack and self.stack[-1] == tag, f'Unbalanced HTML closing tag: {tag}')
        self.stack.pop()


before = original(GUIDE)
after = (ROOT / GUIDE).read_text()
blocks = r'<article class="item guide-section".*?</article>'
old_blocks = re.findall(blocks, before, re.S)
new_blocks = re.findall(blocks, after, re.S)
require(old_blocks == new_blocks, 'Original guide articles changed, missing, duplicated or reordered')
require(len(old_blocks) == 10, 'Unexpected baseline guide structure')
for path in (HUB, GUIDE):
    source = (ROOT / path).read_text()
    baseline = original(path)
    structure = Structure()
    structure.feed(source)
    require(not structure.stack, f'{path}: unclosed tags')
    require(all(structure.counts.get(t) == 1 for t in ('html', 'head', 'body', 'main', 'h1')), f'{path}: document landmarks')
    require(len(structure.ids) == len(set(structure.ids)), f'{path}: duplicate IDs')
    require(all(a[1:] in structure.ids for a in structure.anchors if a.startswith('#')), f'{path}: broken local fragment')
    for image in structure.images:
        require(all(image.get(key) for key in ('alt', 'width', 'height', 'src')), f'{path}: incomplete image attributes')
        require((ROOT / image['src'].lstrip('/')).is_file(), f'{path}: missing image')
    for tag in ('header', 'footer'):
        pattern = rf'<{tag}\b.*?</{tag}>'
        require(re.search(pattern, source, re.S)[0] == re.search(pattern, baseline, re.S)[0], f'{path}: {tag} changed')
    for pattern in (r'<title>.*?</title>', r'<meta name="description"[^>]+>', r'<link rel="canonical"[^>]+>', r'<link rel="alternate"[^>]+>'):
        require(re.findall(pattern, source) == re.findall(pattern, baseline), f'{path}: protected metadata changed')
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        json.loads(raw)
    require('href="#main-content">Skip to content</a>' in source, f'{path}: skip link needs static HTML')

hub = (ROOT / HUB).read_text()
require(len(re.findall('data-guide-status="published"', hub)) == 24, 'Hub must expose the 24 actual English editions')
require(len(re.findall('data-guide-status="pending"', hub)) == 9, 'Do not present missing English guides as published')
for path in ROOT.glob('en/cerchi/guides/*/index.html'):
    href = '/' + path.relative_to(ROOT).as_posix().removesuffix('index.html')
    require(f'href="{href}"' in hub, f'Guide missing from static hub: {href}')
require('type="radio" name="formation"' in after, 'Comparison must work with native controls without JS')
require(re.search(r'<h1>.*?</h1>', before)[0] == re.search(r'<h1>.*?</h1>', after)[0], 'Guide title changed')
changed = subprocess.check_output(['git', 'diff', '--name-only', BASELINE], cwd=ROOT, text=True).splitlines()
require(all(p in ALLOWED or p.startswith('docs/international-3/') for p in changed), 'Change outside prototype scope')
require('international-pasolini.css' in after and 'international-pasolini.css' not in hub, 'Pasolini module must be loaded only by its guide')
css = (ROOT / 'assets/international-atlas.css').read_text()
require('formation-' not in css, 'Pasolini-specific controls leaked into shared CSS')
require('.footer' not in css and '.site-header' not in css, 'Do not restyle shared footer/header')
print('Prototype PASS: 10 original articles byte-identical and ordered; 24 real EN guide links; 9 explicit future editions; balanced HTML, static anchors, image dimensions, JSON-LD, metadata, header/footer and scope checked.')
