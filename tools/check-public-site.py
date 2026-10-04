"""Dependency-free public HTML contract/link checks. Never modifies the site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://alessandro-gentili.it/'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags, self.ids, self.blocks = [], [], []
        self.json_open = False
        self.buffer = ''
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs, self.getpos()[0]))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.json_open, self.buffer = True, ''

    def handle_data(self, data):
        if self.json_open:
            self.buffer += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.json_open:
            self.blocks.append(self.buffer)
            self.json_open = False


def public_url(path):
    return BASE + ('' if path == 'index.html' else path.removesuffix('index.html') if path.endswith('/index.html') else path)


def check(pages, exceptions):
    errors = []
    references = 0
    for path, page in pages.items():
        tags = page.tags
        noindex = any(t == 'meta' and a.get('name') == 'robots' and 'noindex' in a.get('content', '') for t, a, _ in tags)
        if noindex:
            continue
        def require(ok, reason):
            if not ok:
                errors.append(f'{path}: {reason}')
        require(sum(t == 'h1' for t, _, _ in tags) == 1, 'expected one H1')
        require(sum(t == 'main' for t, _, _ in tags) == 1, 'expected one main landmark')
        require(len(page.ids) == len(set(page.ids)), 'duplicate IDs')
        require(any(t == 'nav' and 'primary-nav' in a.get('class', '').split() for t, a, _ in tags), 'missing primary navigation')
        missing = []
        if not any(t == 'footer' for t, _, _ in tags):
            missing.append('footer')
        scripts = [a.get('src', '') for t, a, _ in tags if t == 'script' and a.get('src')]
        if not any(urljoin(public_url(path), src) == BASE + 'assets/script.js' for src in scripts):
            missing.append('script')
        require(set(missing) == set(exceptions.get(path, [])), f'common components {missing}; expected legacy debt {exceptions.get(path, [])}')
        if '/guide/' in path or '/guides/' in path:
            require(any(t == 'nav' and 'guide-toc' in a.get('class', '').split() for t, a, _ in tags), 'missing guide TOC')
        for block in page.blocks:
            try:
                json.loads(block)
            except ValueError as error:
                errors.append(f'{path}: invalid JSON-LD: {error}')
        for tag, attrs, line in tags:
            attribute = 'href' if tag in ('a', 'link') else 'src' if tag in ('img', 'script', 'source') else None
            value = attrs.get(attribute, '')
            if not value or value.startswith(('mailto:', 'tel:', 'data:', 'javascript:')):
                continue
            url = urlsplit(urljoin(public_url(path), value))
            if url.netloc != 'alessandro-gentili.it':
                continue
            references += 1
            target = unquote(url.path).lstrip('/') or 'index.html'
            if (ROOT / target).is_dir():
                target = target.rstrip('/') + '/index.html'
            require((ROOT / target).is_file(), f'line {line}: missing local target {value}')
            if url.fragment and target in pages:
                require(unquote(url.fragment) in pages[target].ids, f'line {line}: missing fragment {value}')
    for path in exceptions:
        if path not in pages:
            errors.append(f'Stale legacy exception: {path}')
    return errors, references


def main():
    pages = {}
    # Public inventory comes from the sitemap; also discover omitted public HTML.
    for p in ROOT.rglob('*.html'):
        path = p.relative_to(ROOT).as_posix()
        if any(part.startswith('.') for part in p.relative_to(ROOT).parts) or path.startswith(('prototipi/', 'node_modules/')) or path == 'pinterest-566e0.html':
            continue
        pages[path] = Page(p.read_text())
    exceptions = json.loads((ROOT / 'tools/site-hardening-legacy.json').read_text())
    errors, references = check(pages, exceptions)
    sitemap = {node.text for node in ET.parse(ROOT / 'sitemap.xml').iter() if node.tag.endswith('}loc')}
    for path, page in pages.items():
        noindex = any(t == 'meta' and a.get('name') == 'robots' and 'noindex' in a.get('content', '') for t, a, _ in page.tags)
        if not noindex and public_url(path) not in sitemap:
            errors.append(f'{path}: missing from public sitemap')
    template = (ROOT / '.github/templates/cerchi-guide-template.html').read_text()
    for component in ['site-header', 'primary-nav', '<footer', 'assets/script.js', 'assets/style.css', 'guide-toc']:
        if component not in template:
            errors.append(f'Guide template missing {component}')
    if errors:
        raise SystemExit('\n'.join(errors))
    # Mutations are in memory: prove missing components and broken fragments fail.
    original = (ROOT / 'en/cerchi/guides/plato-ideas-truth-power/index.html').read_text()
    path = 'en/cerchi/guides/plato-ideas-truth-power/index.html'
    for mutated in [original.replace('<footer', '<div').replace('</footer>', '</div>'), original.replace('assets/script.js', 'assets/absent.js'), original.replace('href="#orientation"', 'href="#missing-section"')]:
        assert check({**pages, path: Page(mutated)}, exceptions)[0], 'Mutation escaped checks'
    print(f'Public-site checks passed: {len(pages)} HTML documents, {references} local references, JSON-LD and mutation checks. Explicit unchanged legacy exceptions: {len(exceptions)}.')


if __name__ == '__main__':
    main()
