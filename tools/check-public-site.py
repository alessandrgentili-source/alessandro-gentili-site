"""Dependency-free public HTML contract/link checks. Never modifies the site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://alessandro-gentili.it/'
PRESENTATION = 'en/system/the-separation-of-cognitive-powers/'
VIEWERS = {PRESENTATION + 'index.html': 'en', PRESENTATION + 'it.html': 'it'}
MATERIALS = {PRESENTATION + file for file in (
    'reading.html', 'preview.html', 'worksheet.html',
    'lettura.html', 'anteprima.html', 'scheda.html',
)}
SCENES = tuple(str(number) for number in range(1, 9))


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


def is_noindex(page):
    return any(t == 'meta' and a.get('name') == 'robots' and 'noindex' in a.get('content', '') for t, a, _ in page.tags)


def check_viewer(path, page, require):
    language = VIEWERS[path]
    en_url, it_url = map(public_url, VIEWERS)
    expected_alternates = {'en': en_url, 'it': it_url, 'x-default': en_url}
    tags = page.tags

    def attrs(tag):
        return [a for t, a, _ in tags if t == tag]

    require(any(a.get('lang') == language for a in attrs('html')), 'incorrect viewer language')
    require(any(a.get('id') == 'stage' and a.get('aria-label') for a in attrs('main')), 'missing labelled stage')
    scenes = [a for a in attrs('section') if 'scene' in a.get('class', '').split()]
    require([a.get('id') for a in scenes] == [f'scena-{n}' for n in SCENES], 'expected eight ordered scenes')
    require(all(a.get('aria-labelledby') in page.ids for a in scenes), 'scene heading missing')
    require(any(a.get('id') == 'controls' and a.get('aria-label') for a in attrs('nav')), 'missing labelled scene navigation')
    buttons = {a.get('id') for a in attrs('button')}
    require({'prev', 'next', 'scene-menu', 'evidence', 'static', 'fullscreen', 'help', 'close-dialog'} <= buttons,
            'missing viewer controls')
    require(any(a.get('id') == 'detail' and a.get('aria-labelledby') in page.ids for a in attrs('dialog')),
            'missing labelled viewer dialog')
    scripts = [a for a in attrs('script') if 'src' in a]
    require([a['src'] for a in scripts] == ['triads.js', f'content-{language}.js', 'viewer.js']
            and all('defer' in a for a in scripts), 'missing or misordered deferred viewer scripts')

    other_file = 'it.html' if language == 'en' else 'index.html'
    other_language = 'it' if language == 'en' else 'en'
    require(any(a.get('id') == 'alternate-language' and a.get('href') == other_file
                and a.get('hreflang') == other_language for a in attrs('a')), 'missing relative language switch')
    reading_file = 'reading.html' if language == 'en' else 'lettura.html'
    require(attrs('noscript') and any(a.get('href') == reading_file for a in attrs('a')),
            'missing accessible reading fallback')

    url = public_url(path)
    links = attrs('link')
    require([a.get('href') for a in links if a.get('rel') == 'canonical'] == [url], 'incorrect viewer canonical')
    require([a.get('href') for a in links if a.get('rel') == 'stylesheet'] == ['style.css', 'web.css'],
            'missing or misordered viewer stylesheets')
    alternates = [(a.get('hreflang'), a.get('href')) for a in links if a.get('rel') == 'alternate']
    require(len(alternates) == len(expected_alternates) and dict(alternates) == expected_alternates,
            'expected reciprocal hreflang with English default')
    meta = {a.get('name') or a.get('property'): a.get('content') for a in attrs('meta')}
    require(all(meta.get(key) for key in (
        'description', 'og:type', 'og:title', 'og:description', 'og:image:alt', 'og:locale',
        'og:locale:alternate', 'twitter:card', 'twitter:title', 'twitter:description', 'twitter:image:alt',
    )), 'missing viewer metadata')
    image = meta.get('og:image') or ''
    require(meta.get('og:url') == url and image == meta.get('twitter:image')
            and image.startswith(BASE + PRESENTATION + 'assets/')
            and (ROOT / urlsplit(image).path.lstrip('/')).is_file(), 'incorrect social URL or image')
    try:
        work, = map(json.loads, page.blocks)
    except ValueError:
        work = None
    relation = 'translationOfWork' if language == 'en' else 'workTranslation'
    require(isinstance(work, dict) and work.get('@context') == 'https://schema.org'
            and work.get('@type') == 'CreativeWork'
            and work.get('url') == url and work.get('@id') == url + '#presentation'
            and work.get('inLanguage') == language and work.get('image') == image
            and work.get(relation) == {'@id': expected_alternates[other_language] + '#presentation'}
            and work.get('author') == {'@type': 'Person', 'name': 'Alessandro Gentili'},
            'incorrect viewer CreativeWork')


def check(pages, exceptions):
    errors = []
    references = 0
    for path, page in pages.items():
        tags = page.tags
        def require(ok, reason):
            if not ok:
                errors.append(f'{path}: {reason}')
        noindex = is_noindex(page)
        if path in MATERIALS:
            require(noindex, 'presentation material must be noindex')
        elif path in VIEWERS:
            require(not noindex, 'viewer must be indexable')
        elif noindex:
            continue
        require(sum(t == 'h1' for t, _, _ in tags) == 1, 'expected one H1')
        require(sum(t == 'main' for t, _, _ in tags) == 1, 'expected one main landmark')
        require(len(page.ids) == len(set(page.ids)), 'duplicate IDs')
        if path in VIEWERS:
            check_viewer(path, page, require)
        elif path not in MATERIALS:
            require(any(t == 'nav' and 'primary-nav' in a.get('class', '').split() for t, a, _ in tags), 'missing primary navigation')
            missing = []
            if not any(t == 'footer' for t, _, _ in tags):
                missing.append('footer')
            scripts = [a.get('src', '') for t, a, _ in tags if t == 'script' and a.get('src')]
            if not any(urljoin(public_url(path), src) == BASE + 'assets/script.js' for src in scripts):
                missing.append('script')
            require(set(missing) == set(exceptions.get(path, [])), f'common components {missing}; admitted historical omissions {exceptions.get(path, [])}')
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
                fragment = unquote(url.fragment)
                # The standalone viewer interprets numeric scene fragments in viewer.js.
                viewer_scene = path in MATERIALS and target in VIEWERS and fragment in SCENES
                if viewer_scene:
                    fragment = f'scena-{fragment}'
                require(fragment in pages[target].ids, f'line {line}: missing fragment {value}')
    for path in exceptions:
        if exceptions[path] != ['footer']:
            errors.append(f'{path}: only documented historical footer omissions are admitted')
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
        if not is_noindex(page) and public_url(path) not in sitemap:
            errors.append(f'{path}: missing from public sitemap')
    for path in sorted(set(VIEWERS) | MATERIALS):
        if path not in pages:
            errors.append(f'{path}: missing presentation document')
        if path in MATERIALS and public_url(path) in sitemap:
            errors.append(f'{path}: noindex presentation material in sitemap')
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
    # A legacy page may omit its footer, never its working navigation script.
    for path in exceptions:
        original = (ROOT / path).read_text()
        mutated = original.replace('<script src="/assets/script.js"></script>', '')
        assert check({**pages, path: Page(mutated)}, exceptions)[0], 'Legacy script regression escaped checks'
    path = PRESENTATION + 'index.html'
    original = (ROOT / path).read_text()
    for before, after in [
        ('id="controls"', 'id="missing-controls"'),
        ('id="scena-8"', 'id="missing-scene"'),
        ('src="viewer.js"', 'src="triads.js"'),
        ('hreflang="x-default"', 'hreflang="fr"'),
    ]:
        assert check({**pages, path: Page(original.replace(before, after))}, exceptions)[0], 'Viewer regression escaped checks'
    path = PRESENTATION + 'preview.html'
    original = (ROOT / path).read_text()
    for before, after in [('content="noindex"', 'content="index"'), ('index.html#8', 'index.html#9')]:
        assert check({**pages, path: Page(original.replace(before, after))}, exceptions)[0], 'Material regression escaped checks'
    print(f'Public-site checks passed: {len(pages)} HTML documents, {references} local references, JSON-LD and mutation checks. Admitted historical footer omissions: {len(exceptions)}.')


if __name__ == '__main__':
    main()
