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
    if before == after:
        # Byte-identical published pages are outside this PR's migration scope.
        # Changed guides still pass their pinned editorial preservation contracts.
        print(f'PASS unchanged {relative}')
        return
    old, new = Page(before), Page(after)
    if relative == 'en/cerchi/guides/machiavelli-power-state-effectual-truth/index.html' and before != after:
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-machiavelli-revision.py'))
        revision['verify'](path, base)
        return
    from international_revision import applies, verify as verify_revision
    if applies(relative, before):
        verify_revision(path, base)
        return
    if relative == 'en/cerchi/guides/dante-exile-language-divine-comedy/index.html' and before != after:
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-dante-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/karl-marx-capital-labor-alienation/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-marx-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-nietzsche-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/giacomo-leopardi-desire-infinity-modernity/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-leopardi-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/seneca-time-self-mastery-death/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-seneca-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/aristotle-form-purpose-actuality/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-aristotle-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/max-weber-rationalization-power-disenchantment/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-weber-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/sigmund-freud-unconscious-desire-civilization/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-freud-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/antonio-gramsci-hegemony-culture-common-sense/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-gramsci-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/thomas-hobbes-fear-sovereignty-political-order/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-hobbes-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/averroes-reason-interpretation-law/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-averroes-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/georg-simmel-money-metropolis-individuality/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-simmel-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/adam-smith-exchange-sympathy-wealth/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-smith-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/cicero-republic-law-civic-speech/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-cicero-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/alexis-de-tocqueville-democracy-opinion-liberty/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-tocqueville-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/nicolas-de-condorcet-education-progress-decision/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-condorcet-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/polybius-constitution-power-decline/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-polybius-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/gaetano-mosca-political-class-organization-real-government/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-mosca-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/vilfredo-pareto-elites-residues-circulation/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-pareto-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/epicurus-desire-fear-freedom-before-choice/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-epicurus-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/gabriel-tarde-imitation-belief-desire/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-tarde-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-pasolini-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/thucydides-war-power-crisis-of-language/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-thucydides-revision.py'))
        revision['verify'](path, base)
        return
    if relative == 'en/cerchi/guides/carl-von-clausewitz-war-politics-limits-of-force/index.html':
        from runpy import run_path
        revision = run_path(str(ROOT / 'tools/check-clausewitz-revision.py'))
        revision['verify'](path, base)
        return
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


def verify_new(path):
    """Validate a first-time English Atlas guide; preservation against base is inapplicable."""
    relative = path.resolve().relative_to(ROOT).as_posix()
    require(relative.startswith('en/cerchi/guides/') and relative.endswith('/index.html'),
            f'Invalid new EN guide path: {relative}')
    source = path.read_text()
    page = Page(source)
    canonical = 'https://alessandro-gentili.it/' + relative.removesuffix('index.html')
    canonicals = [link.get('href') for link in page.alternates if link.get('rel') == 'canonical']
    hreflangs = {link.get('hreflang'): link.get('href') for link in page.alternates if link.get('rel') == 'alternate'}
    require(page.lang == 'en', 'New English guide must declare lang=en')
    require(canonicals == [canonical], 'New English guide must have one self-referencing canonical')
    require(hreflangs.get('en') == canonical and bool(hreflangs.get('it')),
            'New English guide must declare its actual IT/EN counterparts')
    require(len(re.findall(r'<h1\b', source)) == 1, 'New English guide needs exactly one H1')
    for tag in ('header', 'main', 'footer'):
        require(len(re.findall(rf'<{tag}\b', source)) == 1 and len(re.findall(rf'</{tag}>', source)) == 1,
                f'New English guide needs a single complete {tag}')
    for token in ('international-atlas.css', 'international-atlas.js', 'atlas-main',
                  'atlas-guide-opening', 'atlas-reader', 'atlas-contents', 'atlas-reading'):
        require(token in source, f'New English guide missing shared asset/component: {token}')
    require(re.search(r'<details\s+open(?:\s|>)', source), 'Guide contents must remain open without JS')
    require(len(page.ids) == len(set(page.ids)), 'Duplicate IDs in new English guide')
    blocks = re.findall(BLOCKS, source, re.S)
    require(blocks, 'New English guide has no static editorial articles')
    article_ids = [Page(block).ids[0] for block in blocks if Page(block).ids]
    require('introduction' in article_ids and 'sources' in article_ids,
            'New English guide must contain opening and sources as static articles')
    require(page.toc and len(page.toc) == len(set(page.toc)), 'Missing or duplicated contents links')
    require(all(href and href.startswith('#') and href[1:] in article_ids for href in page.toc),
            'New guide contents must point to real editorial sections')
    positions = [article_ids.index(href[1:]) for href in page.toc]
    require(positions == sorted(positions), 'Contents are out of editorial order')
    require(page.images and all(src and alt for src, alt in page.images), 'Cover image and alt text required')
    require(all(not src.startswith('/') or (ROOT / src.lstrip('/')).is_file() for src, _ in page.images),
            'Referenced cover is absent from the repository')
    pattern = r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'
    schemas = [json.loads(raw) for raw in re.findall(pattern, source, re.S)]
    article = next((obj for obj in schemas if isinstance(obj, dict) and obj.get('@type') == 'Article'), None)
    breadcrumbs = next((obj for obj in schemas if isinstance(obj, dict) and obj.get('@type') == 'BreadcrumbList'), None)
    require(article is not None and breadcrumbs is not None, 'Article and BreadcrumbList schema required')
    require(article.get('url') == canonical and article.get('mainEntityOfPage') == canonical
            and article.get('inLanguage') == 'en', 'New guide Article facts do not match canonical/language')
    require(article.get('author', {}).get('name') == 'Alessandro Gentili',
            'Editorial authorship must identify Alessandro Gentili')
    require(bool(page.meta) and any(meta.get('name') == 'description' for meta in page.meta),
            'New guide needs an editorial meta description')
    print(f'PASS new {relative}: {len(blocks)} static articles, canonical, TOC, schema, cover and assets')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True, help='Immutable pre-migration commit or fetched base ref')
    parser.add_argument('guides', nargs='*', type=Path)
    args = parser.parse_args()
    paths = args.guides or [p for p in ROOT.glob('en/cerchi/guides/*/index.html') if 'international-atlas.css' in p.read_text()]
    require(paths, 'No International guide found')
    for path in paths:
        relative = path.resolve().relative_to(ROOT).as_posix()
        exists_in_base = subprocess.run(
            ['git', 'cat-file', '-e', f'{args.base}:{relative}'],
            cwd=ROOT, capture_output=True, check=False
        ).returncode == 0
        if exists_in_base:
            verify(path, args.base)
        else:
            verify_new(path)
