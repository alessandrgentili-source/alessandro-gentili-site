#!/usr/bin/env python3
"""Preserve the approved Mattei pilot and validate its IT publication proposal."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / '.agents/skills/cerchi-publisher/pilots/mattei'
MASTER_SHA = '631f47c16143f1716f44a74cfbdea429ac82d9e1a78452593e9bbdd0e2078b66'
EDITORIAL_HTML_SHA = 'dc748b264ed147a0253b477999e2f24d81d5ecb8f2f60c35b647ad962b5b71e2'
METADATA_SHA = 'c64b5fa666c5047d75296bd710686090d12ba5a0d6f24907ee7a5a1183377244'
COVER_SHA = '3465bb1c205175ded358c540fa377f733dbce1e4d098bc9684a0dc2448f9ea05'
spec = importlib.util.spec_from_file_location('publisher', ROOT / 'tools/validate-cerchi-guide.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
BLOCKS = r'<article class="item guide-section"[^>]*>.*?</article>'


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def emphasis(source):
    return [(('strong' if a else 'em'), v.markdown_plain(a or b))
            for a, b in re.findall(r'\*\*(.+?)\*\*|_(.+?)_', source)]



def verify_enrichment(html, manifest=None):
    # Supplemental figures cannot conceal edits to the original HTML articles.
    clean = re.sub(r'\n<figure class="atlas-figure mattei-figure".*?</figure>', '', html, flags=re.S)
    digest = hashlib.sha256(''.join(re.findall(BLOCKS, clean, re.S)).encode()).hexdigest()
    require(digest == EDITORIAL_HTML_SHA, 'Original editorial HTML changed outside the two approved figures')
    metadata_pattern = r'<title\b.*?</title>|<meta\b[^>]*>|<link\b[^>]*rel="(?:canonical|alternate)"[^>]*>|<script type="application/ld\+json">.*?</script>|<h1\b.*?</h1>'
    digest = hashlib.sha256(''.join(re.findall(metadata_pattern, html, re.S)).encode()).hexdigest()
    require(digest == METADATA_SHA, 'Approved title, H1 or metadata changed')
    if manifest is not None:
        require(manifest.get('editorial_html_sha256') == EDITORIAL_HTML_SHA and manifest.get('approved_metadata_sha256') == METADATA_SHA, 'Enrichment preservation manifest changed')
    tree = v.Tree(html)
    figures = [n for n in tree.root.find('figure') if n.attrs.get('data-editorial-figure')]
    require([f.attrs.get('id') for f in figures] == ['mattei-gas-rete', 'mattei-iran-quote'], 'Exactly the two approved figures are required')
    data = [
        [('1946', 'circa 20'), ('1950', '305')],
        [('1949', 'circa 354'), ('1951', '1.266')],
        [('Parte iraniana · NIOC', '50%'), ('Parte italiana · AGIP Mineraria', '50%')],
        [('Iran · entrate fiscali e dividendi NIOC', '75%'), ('Parte italiana', '25%')],
    ]
    tables = [t for f in figures for t in f.find('table')]
    require(len(tables) == 4, 'Figures need four readable data tables')
    for table, expected in zip(tables, data):
        require(len(list(table.find('caption'))) == 1, 'Each table needs a visible caption/unit')
        body = next(table.find('tbody'))
        actual = [tuple(v.normalized(v.content(c)) for c in row.children if isinstance(c, v.Node) and c.tag in {'th','td'}) for row in body.find('tr')]
        require(actual == expected, 'Figure data, approximation or beneficiary changed')
        require(all(h.attrs.get('scope') in {'col','row'} for h in table.find('th')), 'Table headers need row/column scope')
    captions = [v.normalized(v.content(next(t.find('caption')))) for t in tables]
    require('Milioni di metri cubi' in captions[0] and 'Chilometri' in captions[1], 'Gas/network units missing')
    require('prevista' in captions[3] and 'Utili netti' in captions[3], 'Iranian economic split must be explicitly projected net profits')
    require('non garantisce automaticamente il conseguimento dei profitti previsti' in v.content(figures[1]), 'Forecast/result qualification missing')
    require(not list(tree.root.find('p','lead')), 'Repeated hero subtitle restored')
    links = list(next(tree.root.find('nav','guide-toc')).find('a'))
    require(links[0].attrs.get('href') == '#apertura-editoriale' and 'data-atlas-opening' in links[0].attrs, 'TOC must orient the reader during the introduction')
    print('PASS enrichment: original article HTML and approved metadata byte-preserved; 2 static figures with exact source data/units; introduction in TOC; no duplicate lead')


def verify():
    manifest = json.loads((PILOT / 'manifest.json').read_text())
    page, source, cover = (PILOT / manifest['page'], PILOT / manifest['master']['path'], PILOT / manifest['cover']['path'])
    require(hashlib.sha256(source.read_bytes()).hexdigest() == manifest['master']['sha256'] == MASTER_SHA, 'Approved v3 master hash changed')
    require(hashlib.sha256(cover.read_bytes()).hexdigest() == manifest['cover']['sha256'] == COVER_SHA, 'Approved cover bytes changed')
    require(manifest['mode'] == 'DRAFT' and manifest['language'] == 'it', 'Pilot must remain an Italian draft')
    report = []
    release = manifest.get('release')
    if release:
        released_page = ROOT / release['page']
        require(released_page.read_bytes() == page.read_bytes(), 'Public proposal differs from approved DRAFT')
        require((ROOT / release['cover']).read_bytes() == cover.read_bytes(), 'Public cover differs from approved DRAFT')
        require((ROOT / release['css']).read_bytes() == (PILOT / 'site/assets/cerchi-mattei.css').read_bytes(), 'Public figure CSS differs from approved DRAFT')
        errors = v.validate(released_page, ROOT / release['cover'], source, ROOT, mode='PUBLICATION', report=report)
        report.append('PUBLICATION proposal verified; archived DRAFT retained unchanged; merge/deploy require human approval')
    else:
        errors = v.validate(page, cover, source, ROOT, report=report)
    require(not errors, '\n'.join(errors))
    html, manuscript = page.read_text(), source.read_text()
    verify_enrichment(html, manifest)

    tree = v.Tree(html)
    articles = list(tree.root.find('article', 'guide-section'))
    require(len(articles) == 41, 'Expected introduction plus 40 sections')
    require(len(list(next(tree.root.find('nav', 'guide-toc')).find('a'))) == 41, 'Expected introduction plus 40 numbered TOC anchors')
    source_sections = re.split(r'^## ', manuscript, flags=re.M)[1:]
    # The index is navigation, not a duplicated body section. Subtitle moves to
    # the opening; every original inline emphasis span remains in source order.
    for i, (article, raw) in enumerate(zip(articles, [source_sections[0], *source_sections[2:]])):
        expected = emphasis(raw)
        if i == 0:
            expected = [('em', v.markdown_plain(manuscript.splitlines()[2])), *expected]
        actual = [(n.tag, v.normalized(v.content(n))) for n in v.walk(article) if n.tag in {'strong', 'em'}]
        require(actual == expected, f'Emphasis changed in editorial section {i}')
        expected_items = len(re.findall(r'^\s*(?:[-*+] |\d+\. )', raw.partition('\n')[2], re.M))
        require(len(list(article.find('li'))) == expected_items, f'List item count changed in section {i}')
    for tag in ('header', 'footer'):
        reference = (ROOT / 'cerchi/guide/carl-von-clausewitz-guerra-politica-limiti-della-forza/index.html').read_text()
        pattern = rf'<{tag} class="{ "site-header" if tag == "header" else "footer"}".*?</{tag}>'
        require(re.search(pattern, html, re.S)[0] == re.search(pattern, reference, re.S)[0], f'Shared IT {tag} changed')
    require(not list(tree.root.find('style')), 'Pilot must not add local CSS')
    require(not any(n.tag == 'script' and n.attrs.get('type') != 'application/ld+json' and not n.attrs.get('src') for n in v.walk(tree.root)), 'Pilot must not add inline JS')
    sitemap = (ROOT / 'sitemap.xml').read_text()
    for n in tree.root.find('a'):
        href = n.attrs.get('href', '')
        if href.startswith('/cerchi/guide/'):
            require(v.BASE.rstrip('/') + href in sitemap, f'Pilot links to an unpublished guide: {href}')
    for line in report:
        print(line)
    print('PASS Mattei: immutable master/cover; 41 sections, introduction + 40 numbered TOC anchors, 16 FAQ; emphasis/list integrity; published relations; shared IT shell')
    return page, cover, source


def self_test(page, cover, source):
    original = page.read_text()
    with tempfile.TemporaryDirectory(prefix='cerchi-atlas-') as temporary:
        temp = Path(temporary)
        candidate = temp / 'cerchi/guide' / page.parent.name / 'index.html'
        candidate.parent.mkdir(parents=True)
        local_css = temp / 'assets/cerchi-mattei.css'
        local_css.parent.mkdir()
        local_css.write_bytes((PILOT / 'site/assets/cerchi-mattei.css').read_bytes())

        # Model the pre-publication tree explicitly, so DRAFT and negative
        # publication tests keep their original meaning after this guide ships.
        fixture_root = temp / 'draft-root'
        fixture_root.mkdir()
        for child in ROOT.iterdir():
            if not child.name.startswith('.') and child.name not in {'cerchi', 'sitemap.xml'}:
                (fixture_root / child.name).symlink_to(child, target_is_directory=child.is_dir())
        (fixture_root / 'cerchi/guide').mkdir(parents=True)
        (fixture_root / 'cerchi/triadi').mkdir()
        for guide in (ROOT / 'cerchi/guide').iterdir():
            if guide.name != page.parent.name:
                (fixture_root / 'cerchi/guide' / guide.name).symlink_to(guide, target_is_directory=True)
        for rel in ['sitemap.xml', 'cerchi/index.html', 'cerchi/triadi/index.html']:
            (fixture_root / rel).write_bytes(subprocess.check_output(['git','show','785525b33b38b6aabe5244f0e0ac8c30e8b620d8:'+rel],cwd=ROOT))

        def run(html=original, *, mode='DRAFT', root=fixture_root):
            candidate.write_text(html)
            return v.validate(candidate, cover, source, root, mode)

        require(not run(), 'Temporary IT draft should pass')
        mutations = [
            ('wrong supplementary opening', original.replace('data-atlas-opening href="#apertura-editoriale"', 'data-atlas-opening href="#vita-essenziale"', 1), 'supplementary TOC opening'),
            ('missing title-only declaration', original.replace(' data-atlas-hero="title-only"', '', 1), 'hero needs one short lead'),
            ('altered introduction heading', original.replace('<h2>Introduzione — Il paese che doveva trovare la propria energia</h2>', '<h2>Un titolo diverso</h2>'), 'introduction heading differs'),
            ('missing paragraph', original.replace('<p>Mattei ne diventa presidente.</p>', '', 1), 'source block'),
            ('altered paragraph', original.replace('Mattei ne diventa presidente.', 'Il testo è stato cambiato.', 1), 'source block'),
            ('added paragraph', original.replace('<p>Mattei ne diventa presidente.</p>', '<p>Mattei ne diventa presidente.</p><p>Aggiunta non autorizzata.</p>', 1), 'added or altered'),
            ('wrong working TOC label', original.replace('>2. Perché Mattei è importante</a>', '>2. Le Sette Sorelle</a>'), 'TOC label/section mismatch'),
            ('unknown anchor', original.replace('href="#vita-essenziale"', 'href="#assente"', 1), 'TOC label/section mismatch'),
            ('duplicate ID', original.replace('id="vita-essenziale"', 'id="costellazione"', 1), 'duplicate HTML IDs'),
            ('closed no-JS TOC', original.replace('<details open>', '<details>'), 'open without JS'),
            ('missing Atlas CSS', original.replace('<link rel="stylesheet" href="/assets/international-atlas.css">', ''), 'Atlas CSS'),
            ('missing defer', original.replace('src="/assets/international-atlas.js" defer', 'src="/assets/international-atlas.js"'), 'Atlas JS'),
            ('wrong canonical', original.replace('rel="canonical" href="https://alessandro-gentili.it/', 'rel="canonical" href="https://example.com/', 1), 'canonical must self-reference'),
            ('wrong schema author', original.replace('"name": "Alessandro Gentili"', '"name": "Enrico Mattei"', 1), 'author must be Alessandro'),
            ('wrong language', original.replace('<html lang="it">', '<html lang="en">'), 'document language must match'),
            ('fake hreflang', original.replace('</head>', '<link rel="alternate" hreflang="it" href="'+v.BASE+'cerchi/guide/'+page.parent.name+'/"><link rel="alternate" hreflang="en" href="'+v.BASE+'en/cerchi/guides/missing/">\n</head>'), 'hreflang target does not exist'),
            ('missing relation', original.replace('/cerchi/guide/adam-smith-scambio-simpatia-ricchezza/', '/cerchi/guide/inesistente/'), 'missing local target'),
            ('FAQ answer under wrong question', original.replace('"text": "Nacque ad Acqualagna, nelle Marche, il 29 aprile 1906. Trascorse una parte significativa della giovinezza a Matelica."', '"text": "Mattei ne diventa presidente."'), 'FAQ answer does not match'),
        ]
        for name, html, expected in mutations:
            require(html != original, f'Inactive mutation: {name}')
            errors = run(html)
            require(any(expected in e for e in errors), f'Mutation escaped its gate: {name}: {errors}')
            print('PASS rejected:', name)
        for name, changed in [
            ('gas approximation removed', original.replace('circa 20<span', '20<span', 1)),
            ('wrong gas value', original.replace('>305<span', '>306<span', 1)),
            ('forecast caption removed', original.replace('Ripartizione economica prevista <span>', 'Ripartizione economica <span>', 1)),
            ('projected share changed', original.replace('<td>75%</td>', '<td>70%</td>', 1)),
            ('original text moved into figure', original.replace('<p>Mattei ne diventa presidente.</p>', '', 1).replace('<p class="atlas-label">Sezione 13', '<p>Mattei ne diventa presidente.</p><p class="atlas-label">Sezione 13', 1)),
            ('extra figure', original.replace('</main>', '<figure data-editorial-figure="extra"></figure></main>', 1)),
        ]:
            require(changed != original, 'Inactive enrichment mutation: '+name)
            try:
                verify_enrichment(changed)
            except AssertionError:
                print('PASS rejected enrichment:', name)
            else:
                raise AssertionError('Enrichment mutation escaped: '+name)
        require(any('internal accessible title' in e for e in run(original.replace('aria-labelledby="mattei-gas-rete-title"', 'aria-labelledby="missing"', 1))), 'Figure accessible-title gate lost')
        print('PASS rejected figure with missing accessible title')
        errors = run(mode='PUBLICATION')
        for expected in ('included in sitemap', 'linked from cerchi/index.html', 'linked from cerchi/triadi/index.html'):
            require(any(expected in e for e in errors), f'PUBLICATION gate lost: {expected}')
        print('PASS PUBLICATION refuses unlisted/unconnected IT draft')

        mirror = temp / 'public-root'
        mirror.mkdir()
        for child in ROOT.iterdir():
            if not child.name.startswith('.') and child.name != 'sitemap.xml':
                (mirror / child.name).symlink_to(child, target_is_directory=child.is_dir())
        canonical = v.BASE + 'cerchi/guide/' + page.parent.name + '/'
        (mirror / 'sitemap.xml').write_text((ROOT / 'sitemap.xml').read_text().replace('</urlset>', '<url><loc>'+canonical+'</loc></url></urlset>'))
        require(any('DRAFT candidate must remain absent' in e for e in run(root=mirror)), 'DRAFT allowed a public sitemap entry')
        print('PASS DRAFT refuses sitemap inclusion')
        legacy = original.replace('guide-page international-atlas atlas-guide', 'guide-page')
        legacy = legacy.replace(' data-atlas-hero="title-only"', '')
        legacy = legacy.replace('</h1>', '</h1><p class="lead">Energia, impresa pubblica e autonomia</p>', 1)
        legacy = re.sub(r'<a data-atlas-opening[^>]*>.*?</a>', '', legacy)
        legacy = re.sub(r'<figure class="atlas-figure mattei-figure".*?</figure>', '', legacy, flags=re.S)
        legacy = legacy.replace('<aside class="atlas-contents">', '<article class="item guide-index">').replace('</aside>', '</article>')
        legacy = legacy.replace('<nav class="guide-toc" aria-label="Indice della guida Enrico Mattei">', '<nav class="guide-toc" aria-label="Indice della guida Enrico Mattei"><h2>Indice della guida</h2>')
        require(not run(legacy), 'Legacy guide-index contract regressed')
        require(any('exactly one .guide-index' in e for e in run(legacy.replace('item guide-index', 'item'))), 'Legacy wrapper check weakened')
        print('PASS legacy structure remains valid and missing index remains blocked')

        # A small synthetic EN manuscript tests the same new-guide flow without
        # pretending to translate Mattei or changing any published English page.
        en_page = temp / 'en/cerchi/guides/atlas-fixture/index.html'
        en_page.parent.mkdir(parents=True)
        en_source = temp / 'english.md'
        en_source.write_text('# Atlas fixture\n\n_A complete subtitle._\n\n## Introduction\n\nAn original opening.\n\n## Contents\n\n1. Body\n2. Sources\n3. Continue reading\n4. Editorial closing\n\n## 1. Body\n\nAn original paragraph.\n\n## 2. Sources\n\nA source note.\n\n## 3. Continue reading\n\nA reading direction.\n\n## 4. Editorial closing\n\nAn original conclusion.\n')
        old_url = v.BASE + 'cerchi/guide/' + page.parent.name + '/'
        new_url = v.BASE + 'en/cerchi/guides/atlas-fixture/'
        en_html = original.replace('<link rel="stylesheet" href="/assets/cerchi-mattei.css">', '')
        en_html = en_html.replace(old_url, new_url).replace('<html lang="it">', '<html lang="en">').replace('"inLanguage": "it-IT"', '"inLanguage": "en"')
        en_html = en_html.replace('Guida 34 · Cerchi d’inchiostro', 'Guide 34 · Circles of Ink').replace('Hub Cerchi d’inchiostro', 'Circles of Ink hub').replace('Indice della guida Enrico Mattei', 'Atlas fixture guide contents').replace('Indice della guida', 'In this guide')
        en_html = en_html.replace('href="/cerchi/"', 'href="/en/cerchi/"').replace('href="/cerchi/triadi/"', 'href="/en/cerchi/triads/"')
        en_html = en_html.replace('"item": "'+v.BASE+'"', '"item": "'+v.BASE+'en/"').replace('"item": "'+v.BASE+'cerchi/"', '"item": "'+v.BASE+'en/cerchi/"')
        en_html = re.sub(r'<h1>.*?</h1>', '<h1>Atlas fixture</h1>', en_html, count=1)
        en_html = re.sub(r'<script type="application/ld\+json">\s*{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>', '', en_html, flags=re.S)
        en_html = re.sub(r'<nav class="guide-toc".*?</nav>', '<nav class="guide-toc" aria-label="Atlas fixture guide contents">'+''.join(f'<a href="#{sid}">{i}. {name}</a>' for i,(sid,name) in enumerate([('body','Body'),('sources','Sources'),('continue-reading','Continue reading'),('closing','Editorial closing')],1))+'</nav>', en_html, count=1, flags=re.S)
        en_articles = '<article class="item guide-section" id="opening"><h2>Introduction</h2><p><em>A complete subtitle.</em></p><p>An original opening.</p></article>'
        for sid, name, text in [('body','Body','An original paragraph.'),('sources','Sources','A source note.'),('continue-reading','Continue reading','A reading direction.'),('closing','Editorial closing','An original conclusion.')]:
            actions = '<div class="actions"><a href="/en/cerchi/">Circles of Ink hub</a></div>' if sid == 'continue-reading' else ''
            en_articles += f'<article class="item guide-section" id="{sid}"><h2>{name}</h2><p>{text}</p>{actions}</article>'
        en_html = re.sub(BLOCKS, '', en_html, flags=re.S).replace('<div class="guide-body atlas-reading">', '<div class="guide-body atlas-reading">'+en_articles)
        en_html = en_html.replace('href="#fonti-metodo-e-copyright"', 'href="#sources"')
        shell = (ROOT / 'en/cerchi/guides/carl-von-clausewitz-war-politics-limits-of-force/index.html').read_text()
        for tag, css in [('header', 'site-header'), ('footer', 'footer')]:
            pattern = rf'<{tag} class="{css}".*?</{tag}>'
            en_html = re.sub(pattern, lambda _: re.search(pattern, shell, re.S)[0], en_html, count=1, flags=re.S)
        en_page.write_text(en_html)
        errors = v.validate(en_page, cover, en_source, ROOT)
        require(not errors, 'EN fixture failed: '+ '\n'.join(errors))
        errors = v.validate(en_page, cover, en_source, ROOT, 'PUBLICATION')
        for expected in ('included in sitemap', 'linked from en/cerchi/index.html', 'linked from en/cerchi/triads/index.html'):
            require(any(expected in e for e in errors), f'EN PUBLICATION gate lost: {expected}')
        print('PASS synthetic EN DRAFT and localized PUBLICATION barriers')
        # Legacy TOC aliases remain selective, not an arbitrary href exemption.
        require(v.toc_label_matches('FAQ', 'Domande frequenti'), 'Legacy FAQ alias regressed')
        require(not v.toc_label_matches('Curiosità', 'Vita essenziale'), 'Editorial alias accepts wrong H2')
        require(not v.final_headings_valid(['Fonti', 'Chiusura editoriale', 'Prosegui la lettura']), 'Final order gate regressed')
        print('PASS legacy alias and final-order regression checks')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    paths = verify()
    if args.self_test:
        self_test(*paths)
