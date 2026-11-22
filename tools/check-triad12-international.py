"""Preserve Triads 01–13 and verify the exact approved bilingual Triad 14 pilot."""
import argparse
from functools import lru_cache
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = 'b28cb6845ea48c83ff3f51bd3b97f18ac2364631'
SHA = '022349195e2cfbfee0e0e7af7d98ca101112c3f364d7efabc07fbfd8a00fcdb0'
PAGE = 'en/cerchi/triads/index.html'
IT_PAGE = 'cerchi/triadi/index.html'
GATEWAY_POSITIONING = b'<a href="/en/positioning/">International gateway</a>'
GATEWAY_HOME = b'<a href="/en/">International gateway</a>'
FROZEN_RELEASE = '36e45bc8b1af40593e25df7092311475e03062f5'
SOURCE13 = 'd5a16500948e533e11a121c3fc5e6226517d80ce'
SOURCES13 = {
    'it': ('01_TRIADE13_TESTO_IT_APPROVATO.md', '7f5f8f106fd3869d8248f369d361fba2a5ae07cb906685c1d809a24d03a6c9b0'),
    'en': ('02_TRIAD13_TEXT_EN_APPROVED.md', 'd71d098f187ef4a1427b3e400c7d0376da2b68aafd66e5930c00d4a775341873'),
}
PAIRS13 = [
    ('edgar-morin-knowledge-and-its-blind-spots', 'edgar-morin-la-conoscenza-e-i-suoi-punti-ciechi'),
    ('rachel-carson-life-after-the-intervention', 'rachel-carson-la-vita-dopo-l-intervento'),
    ('john-maynard-keynes-economy-of-an-uncertain-future', 'john-maynard-keynes-economia-futuro-incerto'),
]
# Author-authorized Italian-only release, 18 November 2026. The private master
# stays outside the public repository. Its complete ordered HTML block/inline
# signature was independently derived with markdown-it from these exact bytes;
# the digest covers every word, heading, emphasis boundary and link destination.
TRIAD14_BASE = '54f6b560f3c8cdce472c95469af4009e09647d38'
TRIAD14_SOURCE_SHA = '9be74bb40dd08229157a91e0867a6880fe250b256a4f1885e5a7e6e90d853600'
TRIAD14_EDITORIAL_SHA = '9664a45e24f5ea216931258ea23798c5b5fac5349dcf059b62285101930112e5'
TRIAD14_PAGE = 'cerchi/triadi/legge-colpa-punizione/index.html'
TRIAD14_URL = 'https://alessandro-gentili.it/cerchi/triadi/legge-colpa-punizione/'
BILINGUAL14_BASE = 'e47640c7289c60b4aecd3be79ba8f4e0a6934d47'
TRIAD14_EN_SOURCE_SHA = '30190402c1ac5129b52bda55d53e58b18a6c366cbbf352031b90a399d5d20e25'
TRIAD14_EN_EDITORIAL_SHA = '8f6a33f3f9bbd4e188de29112ed20783f03986477a75137375f329348bf4b5c6'
TRIAD14_EN_PAGE = 'en/cerchi/triads/law-guilt-punishment/index.html'
TRIAD14_EN_URL = 'https://alessandro-gentili.it/en/cerchi/triads/law-guilt-punishment/'
GUIDES14_EN = ['sophocles-law-guilt-limits-city', 'michel-foucault-life-under-examination', 'cesare-beccaria-limits-right-to-punish']
GUIDES14 = [
    'sofocle-legge-colpa-limite-citta',
    'michel-foucault-la-vita-sotto-esame',
    'cesare-beccaria-limite-diritto-punire',
]

# Approved Italian v0.5 reading under card XII; private master remains outside the site.
TRIAD12_IT_BASE = 'd675643a3e172024951b7de22af287ee7ce1638e'
TRIAD12_IT_SOURCE_SHA = 'be0062cae051cf81d1a3e3e96bcf085d315c875bb2dc2b8aab15e2bb1bb51d8f'
TRIAD12_IT_EDITORIAL_SHA = '01463ebb8585a20da4f102b60dda7d08a8bdf67032a02178e0b1999f880caea8'

SLUGS = [
 ('enrico-mattei-energy-public-enterprise-autonomy', 'enrico-mattei-energia-impresa-pubblica-autonomia'),
 ('aristide-merloni-enterprise-fate-of-places', 'aristide-merloni-impresa-lavoro-destino-luoghi'),
 ('adriano-olivetti-community-power', 'adriano-olivetti-la-comunita-e-il-potere'),
]
spec = importlib.util.spec_from_file_location('publisher', ROOT / 'tools/validate-cerchi-guide.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


@lru_cache(maxsize=None)
def frozen(path, ref=FROZEN_RELEASE):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT)


@lru_cache(maxsize=None)
def source13(language):
    filename, digest = SOURCES13[language]
    data = frozen(filename, SOURCE13)
    require(hashlib.sha256(data).hexdigest() == digest, 'Triad 13 source SHA mismatch: ' + language)
    blocks = data.decode().strip().split('\n\n')
    require(len(blocks) == 4 and blocks[0].startswith('# '), 'Triad 13 source structure changed')
    return [blocks[0][2:], *blocks[1:]]


def cards(markup):
    return re.findall(r'<article class="essay-card"[^>]*>.*?</article>', markup, re.S)


def preserve_carson_markup(data):
    """Permit only the authorized stylesheet and accurate responsive cell labels."""
    path = 'cerchi/guide/rachel-carson-la-vita-dopo-l-intervento/index.html'
    expected = frozen(path).decode()
    if data == expected:
        return
    stylesheet = '<link rel="stylesheet" href="/assets/cerchi-guide-38-carson-it.css" />\n'
    require(data.count(stylesheet) == 1, 'Carson table stylesheet missing or duplicated')
    tables = re.findall(r'<table\b.*?</table>', data, re.S)
    require(len(tables) == 3, 'Carson must retain three complete tables')
    for table in tables:
        headers = [v.content(n) for n in v.Tree(table).root.find('th') if n.attrs.get('scope') == 'col']
        rows = list(v.Tree(table).root.find('tr'))[1:]
        for row in rows:
            cells = [n for n in row.children if isinstance(n, v.Node)]
            require([n.attrs.get('data-label') for n in cells] == headers, 'Carson responsive labels differ from headers')
    restored = data.replace(stylesheet, '', 1)
    for table in tables:
        restored = restored.replace(table, re.sub(r' data-label="[^"]*"', '', table), 1)
    require(restored == expected, 'Carson editorial content or other markup changed')


def restore_triad12_layout(block):
    """Invert only the approved cover-first, 3+4 paragraph column composition."""
    layout = re.search(r'<div class="triad12-prose"><div class="triad12-column">(.*?)</div><div class="triad12-column">(.*?)</div></div>', block, re.S)
    if not layout:
        return block
    require(block.index('<div class="triad-featured-covers">') < layout.start(), 'Triad 12 covers must precede the reading columns')
    columns = [re.findall(r'<p>.*?</p>', x, re.S) for x in layout.groups()]
    require([len(c) for c in columns] == [3, 4], 'Triad 12 columns must preserve all seven paragraphs')
    require(all(''.join(c) == raw for c, raw in zip(columns, layout.groups())), 'Unexpected Triad 12 column markup')
    prose = '<div class="triad12-prose">\n' + '\n'.join(columns[0] + columns[1]) + '\n</div>\n'
    return block.replace(layout[0], '', 1).replace('<div class="triad-featured-covers">', prose + '<div class="triad-featured-covers">', 1)


def verify_triad13(node, language):
    approved = source13(language)
    require(v.content(next(node.find('h2'))) == approved[0], 'Triad 13 title changed: ' + language)
    question = next(node.find('p', 'triad-question'))
    require(v.content(question) == approved[1].replace('**', ''), 'Triad 13 question changed: ' + language)
    prose = next(node.find('div', 'triad-lens'))
    require([v.content(n) for n in prose.find('p')] == [x.replace('**', '') for x in approved[2:]], 'Triad 13 text changed: ' + language)
    require([v.content(n) for n in node.find('strong')] == re.findall(r'\*\*(.+?)\*\*', '\n'.join(approved)), 'Triad 13 emphasis changed: ' + language)
    children = [n for n in node.children if isinstance(n, v.Node)]
    require([n.attrs.get('class') for n in children[:3]] == ['triad-block-head', 'triad-featured-covers', 'triad-lens'], 'Triad 13 must place the question before covers and prose below them')
    require(len(list(node.find('p'))) == (5 if language == 'it' else 6), 'Unapproved Triad 13 prose added')
    require([n.tag for n in node.find('h2')] == ['h2'] and not list(node.find('h3')), 'Unapproved Triad 13 headings')
    expected = [f'/cerchi/guide/{it}/' for _, it in PAIRS13]
    if language == 'en':
        expected = [f'/en/cerchi/guides/{en}/' for en, _ in PAIRS13] + expected
    links = list(node.find('a'))
    require([n.attrs.get('href') for n in links] == expected, 'Triad 13 guide links wrong or out of order: ' + language)
    if language == 'en':
        require(all(n.attrs.get('lang') == n.attrs.get('hreflang') == 'it' for n in links[3:]), 'Triad 13 original-language annotations missing')
    images = list(node.find('img'))
    require(len(images) == 3, 'Triad 13 requires three covers')
    for image, (en, it) in zip(images, PAIRS13):
        guide_path = f'en/cerchi/guides/{en}/index.html' if language == 'en' else f'cerchi/guide/{it}/index.html'
        guide = v.Tree(frozen(guide_path).decode())
        cover = next(n for n in guide.root.find('img') if 'cerchi-guida-' in n.attrs.get('src', ''))
        require(image.attrs.get('src') == cover.attrs['src'] and image.attrs.get('alt') == cover.attrs['alt'], 'Triad 13 approved cover/alt changed')
        require(image.attrs.get('width') == '1600' and image.attrs.get('height') == '900', 'Triad 13 cover dimensions missing')
        asset = image.attrs['src'].lstrip('/')
        require((ROOT / asset).read_bytes() == frozen(asset), 'Triad 13 cover bytes changed')
        if guide_path == 'cerchi/guide/rachel-carson-la-vita-dopo-l-intervento/index.html':
            preserve_carson_markup((ROOT / guide_path).read_text())
        else:
            require((ROOT / guide_path).read_bytes() == frozen(guide_path), 'A published Triad 13 guide changed')


# Exact index-only presentation proposed for Triad 14. Like restore_triad12_layout,
# invert only the approved structural delta before applying every frozen check.
# Both new cards are checked byte-for-byte FIRST: wrong copy, assets, links,
# order or extra content can never be hidden by the inverse presentation mapping.
INDEX14_ALIGNMENT_BASE = 'f5aa5f2525f5bae45ed39f907fa419d7f005a597'
INDEX14_ALIGNMENT_SHA = {'it': '46140ff1c91f3d8aa41b1a428ee78db1308e5870649f0425fc2d71adfca765c2', 'en': 'bc57bb309ddb2d68c8d34ddc7ecdb221de1b62969e3b0b7893da183b5327c3d3'}


def restore_index14_alignment(markup, language):
    require(language in {'it', 'en'}, 'Unsupported index alignment language')
    path = IT_PAGE if language == 'it' else PAGE
    blocks = cards(markup) if language == 'it' else sections(markup)
    require(len(blocks) == 14, 'Exactly fourteen index cards required for alignment')
    current = blocks[13]
    require(hashlib.sha256(current.encode()).hexdigest() == INDEX14_ALIGNMENT_SHA[language], 'Triad 14 index differs from the reviewed presentation: ' + language)
    baseline = frozen(path, INDEX14_ALIGNMENT_BASE).decode()
    previous = cards(baseline)[13] if language == 'it' else sections(baseline)[13]
    return markup.replace(current, previous, 1)


def verify_it(markup):
    markup = restore_index14_alignment(markup, 'it')
    tree = v.Tree(markup)
    require(not tree.malformed, str(tree.malformed))
    previous, current = cards(frozen(IT_PAGE).decode()), cards(markup)
    require(len(previous) == 12 and len(current) == 14, 'Exactly fourteen Italian triad cards required')
    require(current[:12] == previous, 'The twelve historical Italian triads changed or reordered')
    require(current[:13] == cards(frozen(IT_PAGE, TRIAD14_BASE).decode()), 'The thirteen historical Italian triads changed or reordered')
    require('id="tredicesima-triade"' in current[12], 'Italian Triad 13 anchor missing')
    require(len(list(tree.root.find('article', 'essay-card'))) == 14, 'Unexpected Italian triad card')
    node = next(n for n in tree.root.find('article') if n.attrs.get('id') == 'tredicesima-triade')
    verify_triad13(node, 'it')
    card14 = v.Tree(current[13]).root
    require(next(card14.find('article')).attrs.get('id') == 'quattordicesima-triade', 'Italian Triad 14 anchor/order changed')
    require(v.content(next(card14.find('h2'))) == 'Legge, colpa, punizione', 'Triad 14 card title changed')
    require([v.normalized(v.content(n)) for n in card14.find('p')] == [
        'Quattordicesima triade', 'Sofocle · Michel Foucault · Cesare Beccaria',
        'Domanda di lettura: Chi può trasformare un atto in colpa, e fino a dove arriva il diritto di punire?',
    ], 'Triad 14 card question/authors changed or prose added')
    require([n.attrs.get('href') for n in card14.find('a')] == [
        '/cerchi/triadi/legge-colpa-punizione/', *[f'/cerchi/guide/{slug}/' for slug in GUIDES14],
    ], 'Triad 14 reading/guide links changed or reordered')
    before = v.Tree(frozen(IT_PAGE).decode())
    require([n.attrs for n in tree.root.find('link') if n.attrs.get('rel') in {'canonical', 'alternate'}] == [n.attrs for n in before.root.find('link') if n.attrs.get('rel') in {'canonical', 'alternate'}], 'Italian canonical/hreflang changed')
    metas = {n.attrs.get('name', n.attrs.get('property')): n.attrs.get('content') for n in tree.root.find('meta')}
    require(metas['description'] == metas['og:description'] == metas['twitter:description'] and metas['description'].startswith('Le quattordici triadi'), 'Italian triad metadata stale')
    schema = next(json.loads(v.content(n)) for n in tree.root.find('script') if n.attrs.get('type') == 'application/ld+json')
    require(schema['@type'] == 'CollectionPage' and schema['description'] == metas['description'] and schema['url'] == 'https://alessandro-gentili.it/cerchi/triadi/', 'Italian CollectionPage inconsistent')
    require(len(schema['hasPart']) == 42, 'Italian CollectionPage must connect exactly 42 guides')
    previous_schema = next(json.loads(v.content(n)) for n in before.root.find('script') if n.attrs.get('type') == 'application/ld+json')
    additions = []
    for _, it in PAIRS13:
        guide = v.Tree(frozen(f'cerchi/guide/{it}/index.html').decode())
        additions.append({'@type': 'CreativeWork', 'name': v.content(next(guide.root.find('h1'))), 'url': f'https://alessandro-gentili.it/cerchi/guide/{it}/'})
    for slug in GUIDES14:
        guide = v.Tree(frozen(f'cerchi/guide/{slug}/index.html', TRIAD14_BASE).decode())
        additions.append({'@type': 'CreativeWork', 'name': v.content(next(guide.root.find('h1'))), 'url': f'https://alessandro-gentili.it/cerchi/guide/{slug}/'})
    require(schema['hasPart'] == previous_schema['hasPart'] + additions, 'Italian CollectionPage historical entries or new guide links changed')


def editorial_signature(nodes):
    """Canonical editorial structure; transparent spans may support typography."""
    def inline(children):
        result = []
        for child in children:
            if isinstance(child, str):
                parts = [child]
            elif child.tag == 'span':
                parts = inline(child.children)
            else:
                require(child.tag in {'em', 'strong', 'a'}, 'Unapproved Triad 14 inline element')
                parts = [[child.tag, child.attrs.get('href') if child.tag == 'a' else None, inline(child.children)]]
            for part in parts:
                if isinstance(part, str) and result and isinstance(result[-1], str):
                    result[-1] += part
                else:
                    result.append(part)
        return [re.sub(r'\s+', ' ', part) if isinstance(part, str) else part for part in result]
    result = []
    for node in nodes:
        if isinstance(node, str):
            require(not node.strip(), 'Text outside approved Triad 14 blocks')
            continue
        require(node.tag in {'h1', 'h2', 'p'}, 'Unapproved Triad 14 editorial block')
        result.append([node.tag, inline(node.children)])
    return result


def verify_triad14(markup, language="it"):
    require(language in {"it", "en"}, "Unapproved Triad 14 language")
    is_it = language == "it"
    page_url = TRIAD14_URL if is_it else TRIAD14_EN_URL
    guide_slugs = GUIDES14 if is_it else GUIDES14_EN
    tree = v.Tree(markup)
    require(not tree.malformed, str(tree.malformed))
    require(next(tree.root.find('html')).attrs.get('lang') == language, 'Triad 14 language changed')
    articles = list(tree.root.find('article'))
    require(len(articles) == 1 and articles[0].attrs.get('id') == ('lettura-triade-14' if is_it else 'triad14-reading'), 'Triad 14 reading missing/duplicated')
    if is_it:
        article_pattern = r'<article id="lettura-triade-14">.*?</article>'
        require(re.search(article_pattern, markup, re.S)[0] == re.search(article_pattern, frozen(TRIAD14_PAGE, BILINGUAL14_BASE).decode(), re.S)[0], 'Published Italian Triad 14 article changed')
    article = articles[0]
    children = [n for n in article.children if isinstance(n, v.Node)]
    require([n.tag for n in children] == ['header', 'nav', 'div'], 'Unapproved content outside Triad 14 source')
    opening, covers, grid = children
    require('data-source-opening' in opening.attrs and covers.attrs.get('class') == 'reading-covers', 'Triad 14 source/cover structure changed')
    grid_children = [n for n in grid.children if isinstance(n, v.Node)]
    require([n.tag for n in grid_children] == ['nav', 'div'] and grid_children[0].attrs.get('class') == 'reading-contents' and 'data-source-body' in grid_children[1].attrs, 'Triad 14 contents/body structure changed')
    body = grid_children[1]
    require(not any(isinstance(n, str) and n.strip() for n in article.children + grid.children), 'Unapproved text outside Triad 14 source')
    signature = editorial_signature(opening.children + body.children)
    digest = hashlib.sha256(json.dumps(signature, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    require(digest == (TRIAD14_EDITORIAL_SHA if is_it else TRIAD14_EN_EDITORIAL_SHA), 'Triad 14 differs from approved Markdown ' + (TRIAD14_SOURCE_SHA if is_it else TRIAD14_EN_SOURCE_SHA))
    require(len(list(tree.root.find('h1'))) == 1, 'Triad 14 needs one H1')
    question = v.content(list(opening.find('p'))[1]).removeprefix('Domanda di lettura: ' if is_it else 'A question to carry through the three guides: ')
    metas = {n.attrs.get('name', n.attrs.get('property')): n.attrs.get('content') for n in tree.root.find('meta')}
    require(metas['description'] == metas['og:description'] == metas['twitter:description'] == question, 'Triad 14 metadata question changed')
    toc = grid_children[0]
    targets = [n.attrs.get('id') for n in body.find('h2')] + ['le-tre-guide' if is_it else 'read-three-guides']
    require([n.attrs.get('href') for n in toc.find('a')] == ['#' + target for target in targets] and all(len([n for n in tree.root.find() if n.attrs.get('id') == target]) == 1 for target in targets), 'Triad 14 contents targets changed')
    require([(n.attrs.get('hreflang'), n.attrs.get('href')) for n in tree.root.find('link') if n.attrs.get('rel') == 'alternate'] == [('it', TRIAD14_URL), ('en', TRIAD14_EN_URL), ('x-default', TRIAD14_URL)], 'Triad 14 reciprocal hreflang changed')
    edition_navs = list(tree.root.find('nav', 'reading-editions'))
    require(len(edition_navs) == 1 and [(n.attrs.get('href'), n.attrs.get('lang'), n.attrs.get('hreflang')) for n in edition_navs[0].find('a')] == [('/cerchi/triadi/legge-colpa-punizione/', 'it', 'it'), ('/en/cerchi/triads/law-guilt-punishment/', 'en', 'en')], 'Triad 14 static edition links changed')
    if not is_it:
        switches = list(tree.root.find('li', 'language-switcher'))
        require(len(switches) == 1 and [(n.attrs.get('href'), n.attrs.get('lang'), n.attrs.get('hreflang')) for n in switches[0].find('a')] == [('/cerchi/triadi/legge-colpa-punizione/', 'it', 'it'), ('/en/cerchi/triads/law-guilt-punishment/', 'en', 'en')], 'Triad 14 header language links changed')
    require([n.attrs.get('href') for n in tree.root.find('link') if n.attrs.get('rel') == 'canonical'] == [page_url], 'Triad 14 canonical changed')
    schemas = [json.loads(v.content(n)) for n in tree.root.find('script') if n.attrs.get('type') == 'application/ld+json']
    require([s['@type'] for s in schemas] == ['Article', 'BreadcrumbList'] and schemas[0]['inLanguage'] == language and schemas[0]['url'] == page_url, 'Triad 14 Article/Breadcrumb schema changed')
    guide_prefix = 'cerchi/guide' if is_it else 'en/cerchi/guides'
    require([n.attrs.get('href') for n in covers.find('a')] == [f'/{guide_prefix}/{slug}/' for slug in guide_slugs], 'Triad 14 cover links changed')
    images = list(covers.find('img'))
    require(len(images) == 3, 'Triad 14 needs exactly three approved covers')
    for image, slug in zip(images, guide_slugs):
        guide_path = f'{guide_prefix}/{slug}/index.html'
        guide = v.Tree(frozen(guide_path, TRIAD14_BASE).decode())
        cover = next(n for n in guide.root.find('img') if '1600x900' in n.attrs.get('src', ''))
        require(all(image.attrs.get(k) == cover.attrs.get(k) for k in ['src', 'alt', 'width', 'height']), 'Triad 14 approved cover/alt changed')
        asset = image.attrs['src'].lstrip('/')
        require((ROOT / asset).read_bytes() == frozen(asset, TRIAD14_BASE), 'Triad 14 approved cover bytes changed')
        require((ROOT / guide_path).read_bytes() == frozen(guide_path, TRIAD14_BASE), 'A published Triad 14 guide changed')


def canonical_international_links(markup):
    """Apply the approved static navigation migration to a frozen Italian guide."""
    routes = {
        b'en.html': b'/en/positioning/',
        b'metodo-ai.html': b'/en/method/',
        b'strumenti.html': b'/en/system/',
    }
    migrated = re.sub(
        rb'(<a\b[^<>]*?\shref=")\.\./\.\./\.\./(en\.html|metodo-ai\.html|strumenti\.html)"',
        lambda match: match[1] + routes[match[2]] + b'"',
        markup,
    )
    return migrated.replace(GATEWAY_POSITIONING, GATEWAY_HOME)


def verify_protected(protected, read_bytes):
    for path, expected in protected.items():
        # Release indexes evolve; frozen guides, triads and assets do not.
        if path in {'cerchi/index.html', 'sitemap.xml'}:
            continue
        actual = read_bytes(path)
        if path == IT_PAGE and actual != expected:
            verify_it(actual.decode())
            continue
        canonical_guide = path.startswith('cerchi/guide/') and path.endswith('/index.html')
        require(actual == expected or (canonical_guide and actual == canonical_international_links(expected)),
                'Protected file changed: ' + path)


def sections(markup):
    return re.findall(r'<section class="wrap triad-block" id="triad-\d+">.*?</section>', markup, re.S)


def index(markup):
    raw = re.search(r'<nav class="triad-index"[^>]*>(.*?)</nav>', markup, re.S)
    require(raw, 'Triad index missing')
    return re.findall(r'<a\b.*?</a>', raw[1], re.S)


def english_guide_parts():
    historic = sections(frozen(PAGE, BILINGUAL14_BASE).decode())
    slugs = list(dict.fromkeys(re.findall(r'href="/en/cerchi/guides/([^/]+)/"', ''.join(historic)))) + GUIDES14_EN
    require(len(slugs) == len(set(slugs)) == 42, 'Frozen English guide inventory changed')
    result = []
    for slug in slugs:
        path = f'en/cerchi/guides/{slug}/index.html'
        guide = v.Tree(frozen(path, BILINGUAL14_BASE).decode())
        result.append({'@type': 'CreativeWork', 'name': v.content(next(guide.root.find('h1'))), 'url': f'https://alessandro-gentili.it/en/cerchi/guides/{slug}/'})
    return result


def verify_en14_section(node):
    require(v.content(next(node.find('h2'))) == 'Law, Guilt, Punishment', 'English Triad 14 title changed')
    require(v.content(next(node.find('p', 'triad-authors'))) == 'Sophocles · Michel Foucault · Cesare Beccaria', 'English Triad 14 authors changed')
    require(v.content(next(node.find('p', 'triad-question'))) == 'A question to carry through the three guides: Who gets to decide when an act amounts to guilt, and how far may the right to punish extend?', 'English Triad 14 question changed')
    require(len(list(node.find('p'))) == 3 and not list(node.find('h3')), 'Unapproved English Triad 14 index prose')
    require([n.attrs.get('href') for n in node.find('a')] == ['/en/cerchi/triads/law-guilt-punishment/', *[f'/en/cerchi/guides/{slug}/' for slug in GUIDES14_EN]], 'English Triad 14 reading/guide links changed or reordered')
    images = list(node.find('img'))
    require(len(images) == 3, 'English Triad 14 needs three original covers')
    for image, slug in zip(images, GUIDES14_EN):
        guide = v.Tree(frozen(f'en/cerchi/guides/{slug}/index.html', BILINGUAL14_BASE).decode())
        cover = next(n for n in guide.root.find('img') if '1600x900' in n.attrs.get('src', ''))
        require(all(image.attrs.get(k) == cover.attrs.get(k) for k in ['src', 'alt', 'width', 'height']), 'English Triad 14 cover/alt changed')


def verify(markup, before, blocks):
    markup = restore_index14_alignment(markup, 'en')
    tree = v.Tree(markup)
    require(not tree.malformed, str(tree.malformed))
    old_sections, new_sections = sections(before), sections(markup)
    require(len(old_sections) == 11 and len(new_sections) == 14, 'Exactly fourteen English triad sections required')
    require(new_sections[:11] == old_sections, 'Existing eleven triads changed or reordered')
    require(new_sections[:11] + [restore_triad12_layout(new_sections[11])] == sections(frozen(PAGE).decode()), 'The twelve frozen English triads changed or reordered')
    require([re.search(r'id="([^"]+)"', x)[1] for x in new_sections] == [f'triad-{i:02}' for i in range(1, 15)], 'Triad section order changed')
    old_index, new_index = index(before), index(markup)
    require(len(new_index) == 14 and new_index[:11] == old_index, 'Existing index entries changed or twelfth missing')
    require(new_index[:12] == index(frozen(PAGE).decode()), 'The twelve historical index entries changed')
    require([re.search(r'href="([^"]+)"', x)[1] for x in new_index] == [f'#triad-{i:02}' for i in range(1, 15)], 'Native triad anchors incomplete')
    require('State, enterprise and community.' in html.unescape(re.sub('<[^>]+>', '', new_index[11])), 'Twelfth index title changed')
    verify_triad13(next(n for n in tree.root.find('section') if n.attrs.get('id') == 'triad-13'), 'en')
    require(new_sections[:13] == sections(frozen(PAGE, BILINGUAL14_BASE).decode()), 'The thirteen published English triads changed or reordered')
    require(new_index[:13] == index(frozen(PAGE, BILINGUAL14_BASE).decode()), 'The thirteen published English index entries changed or reordered')
    verify_en14_section(next(n for n in tree.root.find('section') if n.attrs.get('id') == 'triad-14'))
    require([n.attrs for n in tree.root.find('link') if n.attrs.get('rel') in {'canonical', 'alternate'}] == [n.attrs for n in v.Tree(frozen(PAGE).decode()).root.find('link') if n.attrs.get('rel') in {'canonical', 'alternate'}], 'English canonical/hreflang changed')
    require('italian-path-in-progress' not in markup, 'Provisional anchor remains')
    triad = next(n for n in tree.root.find('section') if n.attrs.get('id') == 'triad-12')
    require(v.content(next(triad.find('h2'))) == blocks[0][3:], 'Approved title changed')
    require(v.content(next(triad.find('h3'))) == blocks[1][4:], 'Approved question changed')
    prose = next(triad.find('div', 'triad12-prose'))
    paragraphs = list(prose.find('p'))
    require([v.content(p) for p in paragraphs] == blocks[2:], 'Approved paragraphs changed, omitted, added or reordered')
    require([n.tag for n in prose.children if isinstance(n, v.Node)] in (['p'] * 7, ['div', 'div']), 'Essay must remain seven complete paragraphs in its approved reading layout')
    require(len(list(triad.find('p'))) == 10, 'Additional editorial paragraphs not permitted')
    links = list(triad.find('a'))
    expected = [f'/en/cerchi/guides/{en}/' for en, _ in SLUGS] + [f'/cerchi/guide/{it}/' for _, it in SLUGS]
    require([x.attrs.get('href') for x in links] == expected, 'Three English and three Italian guide links required in order')
    require(all(x.attrs.get('lang') == x.attrs.get('hreflang') == 'it' for x in links[3:]), 'Italian language annotations missing')
    images = list(triad.find('img'))
    require(len(images) == 3 and all(x.attrs.get('alt') and x.attrs.get('width') == '1600' and x.attrs.get('height') == '900' for x in images), 'Three accessible original covers required')
    for image, (en, _) in zip(images, SLUGS):
        guide = v.Tree(original(f'en/cerchi/guides/{en}/index.html').decode())
        expected_cover = next(guide.root.find('img')).attrs['src']
        require(image.attrs['src'] == expected_cover and expected_cover.endswith('.webp'), 'Original cover selection changed')
    require([x.attrs for x in tree.root.find('script') if x.attrs.get('src')] == [x.attrs for x in v.Tree(before).root.find('script') if x.attrs.get('src')], 'New JavaScript not permitted')
    metas = {x.attrs.get('name', x.attrs.get('property')): x.attrs.get('content') for x in tree.root.find('meta')}
    require(metas['description'] == metas['og:description'] == metas['twitter:description'] and metas['description'].startswith('Fourteen triads'), 'Metadata counts inconsistent')
    schema = next(json.loads(v.content(x)) for x in tree.root.find('script') if x.attrs.get('type') == 'application/ld+json')
    require(schema['@type'] == 'CollectionPage' and schema['description'].startswith('Fourteen triads') and schema['url'] == 'https://alessandro-gentili.it/en/cerchi/triads/', 'CollectionPage inconsistent')
    require(schema.get('hasPart') == english_guide_parts(), 'English CollectionPage must link exactly the 42 approved guides in order')


def italian_index_baseline(ref):
    baseline = frozen(IT_PAGE, ref)
    require(baseline.count(GATEWAY_POSITIONING) == 1, 'Unexpected frozen International gateway link')
    return baseline.replace(GATEWAY_POSITIONING, GATEWAY_HOME, 1).decode()


def verify_triad12_it_reading(markup):
    """Add only the exact approved v0.5; preserve every pre-existing index byte."""
    markup = restore_index14_alignment(markup, 'it')
    baseline = italian_index_baseline(TRIAD12_IT_BASE)
    matches = re.findall(r'\n<section class="triad12-it-reading" id="lettura-triade-12"[^>]*>.*?</section>', markup, re.S)
    require(len(matches) == 1, 'Exactly one approved Italian Triad 12 reading required')
    added = matches[0]
    require(markup.replace(added, '', 1) == baseline, 'Pre-existing Italian index/card bytes changed')
    twelfth = cards(baseline)[11]
    require(markup.index(added) == markup.index(twelfth) + len(twelfth), 'Italian Triad 12 reading must immediately follow card XII')
    tree = v.Tree(added)
    require(not tree.malformed, str(tree.malformed))
    section = next(tree.root.find('section'))
    children = [n for n in section.children if isinstance(n, v.Node)]
    require(len(children) == 1 and children[0].tag == 'div' and children[0].attrs.get('class') == 'triad12-it-prose', 'Italian Triad 12 source container changed')
    require(not any(isinstance(n, str) and n.strip() for n in section.children), 'Unapproved Italian Triad 12 text outside source')
    normalized = []
    for node in children[0].children:
        if isinstance(node, str):
            normalized.append(node)
            continue
        require(node.tag in {'h2', 'h3', 'p'}, 'Unapproved Italian Triad 12 editorial block')
        # Contextual nesting inside the existing index: H1 -> H2, H2 -> H3.
        source_node = v.Node({'h2': 'h1', 'h3': 'h2', 'p': 'p'}[node.tag])
        source_node.children = node.children
        normalized.append(source_node)
    signature = editorial_signature(normalized)
    digest = hashlib.sha256(json.dumps(signature, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    require(digest == TRIAD12_IT_EDITORIAL_SHA, 'Italian Triad 12 differs from approved Markdown ' + TRIAD12_IT_SOURCE_SHA)
    require(section.attrs.get('aria-labelledby') == 'lettura-triade-12-titolo' and len([n for n in section.find('h2') if n.attrs.get('id') == 'lettura-triade-12-titolo']) == 1, 'Italian Triad 12 accessible heading changed')


def check(source, self_test):
    require(hashlib.sha256(source.read_bytes()).hexdigest() == SHA, 'Approved source SHA-256 mismatch')
    raw = source.read_text().strip().split('\n\n')
    blocks = raw[0].splitlines() + raw[1:]
    require(len(blocks) == 9 and blocks[0].startswith('## ') and blocks[1].startswith('### '), 'Frozen source structure changed')
    markup, before = (ROOT / PAGE).read_text(), original(PAGE).decode()
    verify(markup, before, blocks)
    require(sections(markup)[:13] == sections(frozen(PAGE, TRIAD14_BASE).decode()), 'The thirteen published English triads changed')
    verify_it((ROOT / IT_PAGE).read_text())
    verify_triad12_it_reading((ROOT / IT_PAGE).read_text())
    verify_triad14((ROOT / TRIAD14_PAGE).read_text())
    verify_triad14((ROOT / TRIAD14_EN_PAGE).read_text(), 'en')
    # Keep the baseline inventory; only the hub and sitemap may evolve.
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, 'en/cerchi/guides', 'cerchi', 'sitemap.xml', 'assets/img'], cwd=ROOT, text=True).splitlines()
    protected = {path: original(path) for path in paths}
    # The Tarde FAQ answer must match the visible paragraph, without a Markdown separator.
    tarde = 'cerchi/guide/gabriel-tarde-imitazione-credenza-desiderio/index.html'
    approved_suffix = b'anticipatore diretto. ---"'
    require(protected[tarde].count(approved_suffix) == 1, 'Unexpected frozen Tarde FAQ answer')
    protected[tarde] = protected[tarde].replace(approved_suffix, b'anticipatore diretto."', 1)
    verify_protected(protected, lambda path: (ROOT / path).read_bytes())
    for path in ['en/cerchi/index.html', 'en/index.html', 'en/positioning/index.html', 'archivio.html']:
        text = (ROOT / path).read_text()
        require(re.findall(r'data-corpus-count="en-triads">(\d+)', text) and set(re.findall(r'data-corpus-count="en-triads">(\d+)', text)) == {'14'}, 'Triad count stale: ' + path)
        require('italian-path-in-progress' not in text, 'Provisional reference remains: ' + path)
    require('<strong>11</strong><span>Thematic paths</span>' in (ROOT / 'en/positioning/index.html').read_text(), 'Thematic path count must remain eleven')
    require('English triad reading paths: 14' in (ROOT / 'llms.txt').read_text(), 'Machine-readable inventory stale')
    tests = 0
    if self_test:
        for alignment_language, alignment_path in [('it', IT_PAGE), ('en', PAGE)]:
            current_alignment = (ROOT / alignment_path).read_text()
            alignment_baseline = (
                italian_index_baseline(INDEX14_ALIGNMENT_BASE) if alignment_language == 'it'
                else frozen(alignment_path, INDEX14_ALIGNMENT_BASE).decode()
            )
            require(restore_index14_alignment(current_alignment, alignment_language) == alignment_baseline, 'Alignment changed a pre-existing index byte outside XIV')
            alignment_card = (cards(current_alignment) if alignment_language == 'it' else sections(current_alignment))[13]
            alignment_images = re.findall(r'<img\b[^>]*>', alignment_card)
            alignment_teaser = re.search(r'<div class="triad-lens"><p>(.*?)</p></div>', alignment_card, re.S)[1]
            alignment_cases = [
                ('missing cover', alignment_card.replace(alignment_images[0], '', 1)),
                ('cover source', alignment_card.replace('src="', 'src="/unapproved', 1)),
                ('cover alt', alignment_card.replace('alt="', 'alt="altered ', 1)),
                ('cover order', alignment_card.replace(alignment_images[0], '__FIRST__', 1).replace(alignment_images[1], alignment_images[0], 1).replace('__FIRST__', alignment_images[1], 1)),
                ('teaser changed', alignment_card.replace(alignment_teaser, alignment_teaser + ' Altered.', 1)),
                ('teaser missing', alignment_card.replace('<div class="triad-lens"><p>' + alignment_teaser + '</p></div>', '', 1)),
                ('question changed', alignment_card.replace('Chi può trasformare' if alignment_language == 'it' else 'Who gets to decide', 'Changed question', 1)),
                ('reading link', alignment_card.replace('/cerchi/triadi/legge-colpa-punizione/' if alignment_language == 'it' else '/en/cerchi/triads/law-guilt-punishment/', '/missing/', 1)),
                ('guide link', alignment_card.replace('/cerchi/guide/' if alignment_language == 'it' else '/en/cerchi/guides/', '/missing/', 1)),
                ('extra paragraph', alignment_card.replace('</article>' if alignment_language == 'it' else '</section>', '<p>Additional interpretation.</p>' + ('</article>' if alignment_language == 'it' else '</section>'), 1)),
            ]
            if alignment_language == 'en':
                alignment_cases += [('Italian original link', alignment_card.replace('/cerchi/guide/sofocle-legge-colpa-limite-citta/', '/missing/', 1)), ('Italian reading link', alignment_card.replace('/cerchi/triadi/legge-colpa-punizione/', '/missing/', 1))]
            for label, candidate_card in alignment_cases:
                require(candidate_card != alignment_card, 'Ineffective index alignment mutation: ' + label)
                try:
                    restore_index14_alignment(current_alignment.replace(alignment_card, candidate_card, 1), alignment_language)
                except AssertionError:
                    tests += 1
                else:
                    raise AssertionError('Invalid index alignment mutation accepted: ' + label)
        print('PASS accepted: exact XIV cover/lens/reading/originals layout, all earlier index bytes restored; all historical assertions retained')
        italian12 = (ROOT / IT_PAGE).read_text()
        reading12 = re.search(r'\n<section class="triad12-it-reading" id="lettura-triade-12"[^>]*>.*?</section>', italian12, re.S)[0]
        source12 = re.search(r'<div class="triad12-it-prose">(.*?)</div>', reading12, re.S)[1]
        paragraphs12 = re.findall(r'<p\b.*?</p>', source12, re.S)
        mutations12 = [
            ('gateway destination', italian12.replace(GATEWAY_HOME.decode(), GATEWAY_POSITIONING.decode(), 1)),
            ('missing', italian12.replace(reading12, '', 1)),
            ('duplicated', italian12.replace(reading12, reading12 + reading12, 1)),
            ('position', italian12.replace(reading12, '', 1).replace(cards(italian12)[12], cards(italian12)[12] + reading12, 1)),
            ('title', italian12.replace(reading12, reading12.replace('Triade 12 — Stato, impresa e comunità', 'Triade 12 — Impresa e comunità', 1), 1)),
            ('section heading', italian12.replace(reading12, reading12.replace('La prova del presente</h3>', 'La prova odierna</h3>', 1), 1)),
            ('question', italian12.replace(reading12, reading12.replace('Quando cambia chi guida', 'Quando cambia chi dirige', 1), 1)),
            ('authorial first person', italian12.replace(reading12, reading12.replace('Ho voluto riunire', 'Abbiamo voluto riunire', 1), 1)),
            ('temporal note', italian12.replace(reading12, reading12.replace('18 novembre 2026', '19 novembre 2026', 1), 1)),
            ('emphasis', italian12.replace(reading12, reading12.replace('<em>Riferimenti contemporanei', 'Riferimenti contemporanei', 1).replace('</em>', '', 1), 1)),
        ]
        for i, paragraph in enumerate(paragraphs12, 1):
            mutations12.append((f'paragraph {i} removed', italian12.replace(reading12, reading12.replace(paragraph, '', 1), 1)))
        mutations12.append(('paragraph order', italian12.replace(reading12, reading12.replace(paragraphs12[2], '__FIRST__', 1).replace(paragraphs12[3], paragraphs12[2], 1).replace('__FIRST__', paragraphs12[3], 1), 1)))
        mutations12.append(('paragraph added', italian12.replace(reading12, reading12.replace('</div>', '<p>New interpretation.</p></div>', 1), 1)))
        for _, slug in SLUGS:
            mutations12.append(('guide link ' + slug, italian12.replace(reading12, reading12.replace('/cerchi/guide/' + slug + '/', '/cerchi/guide/missing/', 1), 1)))
        for i, historical in enumerate(cards(italian12), 1):
            mutations12.append((f'card {i} changed', italian12.replace(historical, historical.replace('</h2>', ' changed</h2>', 1), 1)))
        for label, candidate in mutations12:
            require(candidate != italian12, 'Ineffective Italian Triad 12 regression: ' + label)
            try:
                verify_triad12_it_reading(candidate)
            except (AssertionError, StopIteration):
                tests += 1
            else:
                raise AssertionError('Invalid Italian Triad 12 mutation accepted: ' + label)
        verify_triad12_it_reading(italian12)
        print('PASS accepted: complete approved Italian Triad 12 v0.5 below XII; fourteen card bytes and all prior index bytes intact')
        for path in ['cerchi/index.html', 'sitemap.xml']:
            require(path in protected, 'Release surface absent from baseline: ' + path)
            verify_protected(protected, lambda candidate: protected[candidate] + b'\n<!-- Release update -->'
                             if candidate == path else protected[candidate])
        print('PASS accepted: evolving Italian hub and sitemap; baseline protection unchanged elsewhere')
        for label, path in [
            ('historical guide', next(path for path in paths if path.startswith('cerchi/guide/'))),
            ('historical cover', next(path for path in paths if path.startswith('assets/img/cerchi/'))),
        ]:
            try:
                verify_protected(protected, lambda candidate: protected[candidate] + b'altered'
                                 if candidate == path else protected[candidate])
            except AssertionError as error:
                require(str(error) == 'Protected file changed: ' + path, 'Unexpected protection failure')
                tests += 1
                print('PASS rejected: ' + label + ' mutation')
            else:
                raise AssertionError('Invalid protected mutation accepted: ' + label)
        mutations = [
            ('paragraph altered', markup.replace('Their interests met', 'Their interests converged', 1)),
            ('paragraph missing', markup.replace('<p>' + html.escape(blocks[7]) + '</p>', '', 1)),
            ('paragraph added', markup.replace('<div class="triad12-column">', '<div class="triad12-column"><p>Additional interpretation.</p>', 1)),
            ('paragraph reordered', markup.replace(html.escape(blocks[2]), '__FIRST__').replace(html.escape(blocks[3]), html.escape(blocks[2])).replace('__FIRST__', html.escape(blocks[3]))),
            ('question altered', markup.replace('Who builds the future — and who decides what it becomes?', 'Who builds the future?', 1)),
            ('old triad altered', markup.replace(sections(markup)[0], sections(markup)[0].replace('Truth', 'Certainty', 1), 1)),
            ('old index altered', markup.replace(index(markup)[0], index(markup)[0].replace('Truth', 'Certainty', 1), 1)),
            ('index target broken', markup.replace('href="#triad-12"', 'href="#missing"', 1)),
            ('English link broken', markup.replace('/en/cerchi/guides/aristide-merloni-enterprise-fate-of-places/', '/en/cerchi/guides/missing/', 1)),
            ('Italian link missing', markup.replace('href="/cerchi/guide/adriano-olivetti-la-comunita-e-il-potere/"', 'href="#missing"', 1)),
            ('cover changed', markup.replace('src="/assets/img/cerchi/cerchi-guida-34-enrico-mattei', 'src="/assets/img/cerchi/missing-enrico-mattei', 1)),
            ('metadata count stale', markup.replace('Fourteen triads', 'Thirteen triads', 1)),
        ]
        thirteenth = sections(markup)[12]
        thirteenth_index = index(markup)[12]
        mutations += [
            ('Triad 13 missing', markup.replace(thirteenth, '', 1)),
            ('Triad 13 duplicated', markup.replace(thirteenth, thirteenth + thirteenth, 1)),
            ('Triad 13 premature', markup.replace(sections(markup)[11] + '\n' + thirteenth, thirteenth + '\n' + sections(markup)[11], 1)),
            ('Triad 13 index missing', markup.replace(thirteenth_index, '', 1)),
            ('Triad 13 anchor missing', markup.replace('id="triad-13"', 'id="triad-missing"', 1)),
            ('Triad 13 wrong guide', markup.replace('/en/cerchi/guides/' + PAIRS13[0][0] + '/', '/en/cerchi/guides/missing/', 1)),
            ('Triad 13 question altered', markup.replace('Who can afford to wait', 'Who can wait', 1)),
            ('Triad 13 prose altered', markup.replace('Morin examines the limits', 'Morin studies the limits', 1)),
            ('Triad 13 emphasis missing', markup.replace('<strong>who has the freedom to wait, and who must live with the consequences while others decide?</strong>', 'who has the freedom to wait, and who must live with the consequences while others decide?', 1)),
        ]
        current12 = sections(markup)[11]
        column_layout = re.search(r'<div class="triad12-prose"><div class="triad12-column">(.*?)</div><div class="triad12-column">(.*?)</div></div>', current12, re.S)
        swapped = '<div class="triad12-prose"><div class="triad12-column">' + column_layout[2] + '</div><div class="triad12-column">' + column_layout[1] + '</div></div>'
        mutations += [
            ('reading columns inverted', markup.replace(column_layout[0], swapped, 1)),
            ('reading column missing', markup.replace('<div class="triad12-column">' + column_layout[1] + '</div>', '', 1)),
            ('covers after reading columns', markup.replace(column_layout[0], '', 1).replace('<div class="triad-featured-covers"><a href="/en/cerchi/guides/enrico-mattei', column_layout[0] + '<div class="triad-featured-covers"><a href="/en/cerchi/guides/enrico-mattei', 1)),
        ]
        for label, candidate in mutations:
            require(candidate != markup, 'Ineffective regression: ' + label)
            try:
                verify(candidate, before, blocks)
            except (AssertionError, StopIteration):
                tests += 1
            else:
                raise AssertionError('Invalid mutation accepted: ' + label)
        italian = (ROOT / IT_PAGE).read_text()
        last_it = cards(italian)[12]
        italian_mutations = [
            ('missing', italian.replace(last_it, '', 1)),
            ('duplicated', italian.replace(last_it, last_it + last_it, 1)),
            ('premature', italian.replace(last_it, '', 1).replace(cards(italian)[11], last_it + cards(italian)[11], 1)),
            ('wrong guide', italian.replace(last_it, last_it.replace('/cerchi/guide/' + PAIRS13[0][1] + '/', '/cerchi/guide/missing/', 1), 1)),
            ('schema link altered', italian.replace('/cerchi/guide/' + PAIRS13[0][1] + '/', '/cerchi/guide/missing/', 1)),
            ('anchor missing', italian.replace('id="tredicesima-triade"', 'id="missing"', 1)),
            ('text altered', italian.replace('Morin interroga i limiti', 'Morin studia i limiti', 1)),
            ('historic card altered', italian.replace('Stato, impresa e comunità</h2>', 'Stato e comunità</h2>', 1)),
        ]
        for label, candidate in italian_mutations:
            require(candidate != italian, 'Ineffective Italian regression: ' + label)
            try:
                verify_it(candidate)
            except (AssertionError, StopIteration):
                tests += 1
            else:
                raise AssertionError('Invalid Italian mutation accepted: ' + label)
        verify_it(italian)
        # Extend the existing positive/negative suite; no historical mutation
        # or source/guide protection above is removed or made conditional.
        fourteenth = cards(italian)[13]
        italian14_mutations = [
            ('missing', italian.replace(fourteenth, '', 1)),
            ('duplicated', italian.replace(fourteenth, fourteenth + fourteenth, 1)),
            ('premature', italian.replace(fourteenth, '', 1).replace(last_it, fourteenth + last_it, 1)),
            ('anchor', italian.replace('id="quattordicesima-triade"', 'id="missing"', 1)),
            ('title', italian.replace(fourteenth, fourteenth.replace('Legge, colpa, punizione', 'Legge e punizione', 1), 1)),
            ('question', italian.replace(fourteenth, fourteenth.replace('Chi può trasformare', 'Chi deve trasformare', 1), 1)),
            ('authors', italian.replace(fourteenth, fourteenth.replace('Cesare Beccaria', 'Beccaria', 1), 1)),
            ('reading link', italian.replace(fourteenth, fourteenth.replace('/cerchi/triadi/legge-colpa-punizione/', '/cerchi/triadi/missing/', 1), 1)),
            ('guide link', italian.replace(fourteenth, fourteenth.replace('/cerchi/guide/' + GUIDES14[0] + '/', '/cerchi/guide/missing/', 1), 1)),
            ('metadata count', italian.replace('Le quattordici triadi', 'Le tredici triadi', 1)),
            ('historical order', italian.replace(cards(italian)[0], '__FIRST__', 1).replace(cards(italian)[1], cards(italian)[0], 1).replace('__FIRST__', cards(italian)[1], 1)),
        ]
        schema_node = next(n for n in v.Tree(italian).root.find('script') if n.attrs.get('type') == 'application/ld+json')
        schema_text = v.content(schema_node)
        for label, mutate in [
            ('schema guide missing', lambda parts: parts[:-1]),
            ('schema guide duplicate', lambda parts: parts[:-1] + [parts[-2]]),
            ('schema guides reordered', lambda parts: parts[:-3] + list(reversed(parts[-3:]))),
            ('schema reading instead of guide', lambda parts: parts[:-1] + [{'@type': 'Article', 'name': 'Triade 14', 'url': TRIAD14_URL}]),
            ('schema extra reading', lambda parts: parts + [{'@type': 'Article', 'name': 'Triade 14', 'url': TRIAD14_URL}]),
        ]:
            schema = json.loads(schema_text)
            schema['hasPart'] = mutate(schema['hasPart'])
            italian14_mutations.append((label, italian.replace(schema_text, json.dumps(schema, ensure_ascii=False), 1)))
        for i, historical in enumerate(cards(italian)[:13], 1):
            italian14_mutations += [
                (f'historical {i} text', italian.replace(historical, historical.replace('</h2>', ' altered</h2>', 1), 1)),
                (f'historical {i} link', italian.replace(historical, historical.replace('href="', 'href="/missing', 1), 1)),
            ]
        for label, candidate in italian14_mutations:
            require(candidate != italian, 'Ineffective Triad 14 index regression: ' + label)
            try:
                verify_it(candidate)
            except (AssertionError, StopIteration):
                tests += 1
                print('PASS rejected: Triad 14 index ' + label)
            else:
                raise AssertionError('Invalid Triad 14 index mutation accepted: ' + label)
        reading = (ROOT / TRIAD14_PAGE).read_text()
        body = re.search(r'(<div class="reading-prose" data-source-body>)(.*?)(</div>)', reading, re.S)
        paragraphs = re.findall(r'<p\b.*?</p>', body[2], re.S)
        reading_mutations = [
            ('title', reading.replace(' Legge, colpa, punizione</h1>', ' Legge e punizione</h1>', 1)),
            ('question', reading.replace('Chi può trasformare un atto', 'Chi deve trasformare un atto', 1)),
            ('body question', reading.replace('<strong>Domanda di lettura:</strong> Chi può trasformare', '<strong>Domanda di lettura:</strong> Chi deve trasformare', 1)),
            ('heading', reading.replace('Le ferite che arrivano fino a noi</h2>', 'Le ferite di oggi</h2>', 1)),
            ('paragraph removed', reading.replace(paragraphs[0], '', 1)),
            ('paragraph added', reading.replace(paragraphs[0], paragraphs[0] + '<p>Additional interpretation.</p>', 1)),
            ('paragraph order', reading.replace(paragraphs[0], '__FIRST__', 1).replace(paragraphs[1], paragraphs[0], 1).replace('__FIRST__', paragraphs[1], 1)),
            ('closing', reading.replace('Il confine del potere si misura anche qui:', 'Il confine si misura qui:', 1)),
            ('literal text', reading.replace('Sul corpo di Polinice', 'Sul corpo di un uomo', 1)),
            ('emphasis removed', reading.replace('<strong>Sofocle · Michel Foucault · Cesare Beccaria</strong>', 'Sofocle · Michel Foucault · Cesare Beccaria', 1)),
            ('essay link', reading.replace('/saggi/saggio-3-governi-senza-firma.html', '/saggi/missing.html', 1)),
            ('guide link', reading.replace('https://alessandro-gentili.it/cerchi/guide/' + GUIDES14[0] + '/', 'https://alessandro-gentili.it/cerchi/guide/missing/', 1)),
            ('cover', reading.replace('src="/assets/img/cerchi/cerchi-guida-40', 'src="/assets/img/cerchi/missing-40', 1)),
            ('alt', reading.replace('alt="', 'alt="altered ', 1)),
            ('unapproved extra source', reading.replace(paragraphs[-1], paragraphs[-1] + '<p><a href="https://example.org/">New source</a></p>', 1)),
            ('unmarked extra text', reading.replace('</article>', '<p>Additional interpretation.</p></article>', 1)),
            ('English alternate', reading.replace('</head>', '<link rel="alternate" hreflang="en" href="https://alessandro-gentili.it/en/cerchi/triads/law/">\n</head>', 1)),
            ('canonical', reading.replace('rel="canonical" href="' + TRIAD14_URL, 'rel="canonical" href="https://example.org/', 1)),
            ('contents target', reading.replace('href="#le-ferite-che-arrivano-fino-a-noi"', 'href="#missing"', 1)),
        ]
        for label, candidate in reading_mutations:
            require(candidate != reading, 'Ineffective Triad 14 reading regression: ' + label)
            try:
                verify_triad14(candidate)
            except (AssertionError, StopIteration):
                tests += 1
                print('PASS rejected: Triad 14 reading ' + label)
            else:
                raise AssertionError('Invalid Triad 14 reading mutation accepted: ' + label)
        verify_triad14(reading)
        verify_it(italian)
        print('PASS accepted: approved complete Italian Triad 14, exact 42-guide schema, thirteen byte-identical historical cards; English now fourteen')

        en14 = sections(markup)[13]
        en14_entry = index(markup)[13]
        en_mutations = [
            ('missing XIV', markup.replace(en14, '', 1)),
            ('duplicate XIV', markup.replace(en14, en14 + en14, 1)),
            ('XIV anchor', markup.replace('id="triad-14"', 'id="missing"', 1)),
            ('XIV question', markup.replace(en14, en14.replace('Who gets to decide', 'Who may decide', 1), 1)),
            ('XIV guide', markup.replace(en14, en14.replace('/en/cerchi/guides/' + GUIDES14_EN[0] + '/', '/en/cerchi/guides/missing/', 1), 1)),
            ('XIV cover', markup.replace(en14, en14.replace('src="', 'src="/missing', 1), 1)),
            ('XIV index missing', markup.replace(en14_entry, '', 1)),
            ('XIV index target', markup.replace('href="#triad-14"', 'href="#missing"', 1)),
            ('historical order', markup.replace(sections(markup)[0], '__FIRST__', 1).replace(sections(markup)[1], sections(markup)[0], 1).replace('__FIRST__', sections(markup)[1], 1)),
        ]
        for i, historical in enumerate(sections(markup)[:13], 1):
            en_mutations += [
                (f'historical {i} text', markup.replace(historical, historical.replace('</h2>', ' altered</h2>', 1), 1)),
                (f'historical {i} link', markup.replace(historical, historical.replace('href="', 'href="/missing', 1), 1)),
                (f'historical {i} index', markup.replace(index(markup)[i-1], index(markup)[i-1].replace('href="', 'href="/missing', 1), 1)),
            ]
        raw_schema = v.content(next(n for n in v.Tree(markup).root.find('script') if n.attrs.get('type') == 'application/ld+json'))
        for label, transform in [
            ('schema missing', lambda p: p[:-1]),
            ('schema duplicate', lambda p: p[:-1] + [p[-2]]),
            ('schema reordered', lambda p: p[:-3] + list(reversed(p[-3:]))),
            ('schema extra reading', lambda p: p + [{'@type': 'Article', 'url': TRIAD14_EN_URL}]),
        ]:
            schema = json.loads(raw_schema)
            schema['hasPart'] = transform(schema['hasPart'])
            en_mutations.append((label, markup.replace(raw_schema, json.dumps(schema, ensure_ascii=False), 1)))
        for label, candidate in en_mutations:
            require(candidate != markup, 'Ineffective bilingual index regression: ' + label)
            try:
                verify(candidate, before, blocks)
            except (AssertionError, StopIteration):
                tests += 1
            else:
                raise AssertionError('Invalid bilingual index mutation accepted: ' + label)
        en_reading = (ROOT / TRIAD14_EN_PAGE).read_text()
        prose = re.search(r'<div class="reading-prose" data-source-body>(.*?)</div>', en_reading, re.S)[1]
        paras = re.findall(r'<p\b.*?</p>', prose, re.S)
        en_reading_mutations = [
            ('literal text', en_reading.replace('A handful of earth', 'A handful of dust', 1)),
            ('paragraph removed', en_reading.replace(paras[0], '', 1)),
            ('paragraph added', en_reading.replace(paras[0], paras[0] + '<p>New interpretation.</p>', 1)),
            ('paragraph order', en_reading.replace(paras[0], '__FIRST__', 1).replace(paras[1], paras[0], 1).replace('__FIRST__', paras[1], 1)),
            ('heading', en_reading.replace('Wounds in the Present</h2>', 'Wounds Today</h2>', 1)),
            ('body question', en_reading.replace('</strong> Who gets to decide', '</strong> Who may decide', 1)),
            ('emphasis', en_reading.replace('<em>Oedipus the King</em>', 'Oedipus the King', 1)),
            ('Italian original label', en_reading.replace('Italian original)', 'English original)', 1)),
            ('Foucault distinction', en_reading.replace('Foucault was already an explicit interlocutor', 'Foucault was not an explicit interlocutor', 1)),
            ('essay destination', en_reading.replace('/saggi/saggio-3-governi-senza-firma.html', '/en/essays/missing/', 1)),
            ('closing', en_reading.replace('have that reason heard.', 'have that reason recorded.', 1)),
            ('reciprocal hreflang', en_reading.replace('hreflang="it" href="' + TRIAD14_URL, 'hreflang="it" href="https://example.org/', 1)),
            ('static edition link', en_reading.replace('href="/cerchi/triadi/legge-colpa-punizione/" lang="it"', 'href="/missing/" lang="it"', 1)),
        ]
        for label, candidate in en_reading_mutations:
            require(candidate != en_reading, 'Ineffective English reading regression: ' + label)
            try:
                verify_triad14(candidate, 'en')
            except (AssertionError, StopIteration):
                tests += 1
            else:
                raise AssertionError('Invalid English reading mutation accepted: ' + label)
        verify_triad14(en_reading, 'en')
        print('PASS accepted: exact approved EN master, intact Italian article, fourteen native EN sections/entries, exact 42-guide schema per language and reciprocal static editions')
        carson = (ROOT / 'cerchi/guide/rachel-carson-la-vita-dopo-l-intervento/index.html').read_text()
        preserve_carson_markup(carson)
        for label, candidate in [
            ('table text changed', carson.replace('Racconta l&#x27;ambiente', 'Riscrive l&#x27;ambiente', 1)),
            ('responsive label changed', carson.replace('data-label="Opera"', 'data-label="Wrong label"', 1)),
            ('stylesheet missing', carson.replace('/assets/cerchi-guide-38-carson-it.css', '/assets/missing.css', 1)),
        ]:
            require(candidate != carson, 'Ineffective Carson mutation: ' + label)
            try:
                preserve_carson_markup(candidate)
            except AssertionError:
                tests += 1
            else:
                raise AssertionError('Invalid Carson mutation accepted: ' + label)
        verify(markup, before, blocks)
    print(f'PASS: frozen SHA, title/question/seven paragraphs, fourteen English native anchors, frozen twelve IT/EN triads, approved bilingual Triad 13, approved bilingual Triad 14, original covers and exact 42 guide links per language; {tests} rejection regressions and intact positive fixtures.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    check(args.source, args.self_test)
