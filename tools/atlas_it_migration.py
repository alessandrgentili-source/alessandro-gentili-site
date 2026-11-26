"""Reconstruct reviewed Atlas migrations from frozen published bytes."""
from collections import Counter
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / '.github/atlas-it'
IT_PATH = r'cerchi/guide/[a-z0-9-]+/index\.html'
EN_PATH = r'en/cerchi/guides/[a-z0-9-]+/index\.html'
ARTICLES = rb'<article\b[^>]*>.*?</article>'
LUCRETIUS_IT = 'cerchi/guide/lucrezio-atomi-immagini-poesia-della-natura/index.html'
LUCRETIUS_EN = 'en/cerchi/guides/lucretius-atoms-images-poetry-of-nature/index.html'
LUCRETIUS_ENTRIES = {
    LUCRETIUS_IT: 'ff2bd3b75817b20b23f377207436dd517d115b4098ab8a37a2f264409061da38',
    LUCRETIUS_EN: 'e1e2a14d63548a1dc02922b8613ebc189225b6ff0eaf5645a8bc7cd1acf9ab31',
}
EDITORIAL_ENTRIES = {
    'cerchi/guide/dante-vita-opere-commedia-esilio/index.html': 'e6d8ea22aaade1b8af7f6a3da6f8be8fc32e0cd5524269fa14d5ad608d0f465d',
    'cerchi/guide/nietzsche-vita-opere-pensiero/index.html': '5059aa6c732b9ef86d64eb5b6181ec5ab696f51f2b3c4772e078224c89d5e7fe',
    'en/cerchi/guides/dante-exile-language-divine-comedy/index.html': '1c5af530f61845acc269f1a075029eb25c7d1f9415c56a6655e19d43812b4c1d',
    'en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/index.html': '9ad563fba5aa3c394416d932f10afe9005e7ed1ba70553d26ef5e31113ef5f99',
    'cerchi/guide/leopardi-desiderio-infinito-modernita/index.html': 'a3253b0a7dd44c99892d43f4d139777cf882dbe0acd3129f0c25a0dcac08c82b',
    'en/cerchi/guides/giacomo-leopardi-desire-infinity-modernity/index.html': 'ee053e537ab3d8e90e1f894fece078e0d9b95dc1b7820db32c8705e23d5fe3b0',
    'cerchi/guide/weber-razionalizzazione-potere-disincanto/index.html': '452e590307dac3a8244b46fe8677c7eeb2cc41ba6dbdefa8c78a7f128a55b30a',
    'en/cerchi/guides/max-weber-rationalization-power-disenchantment/index.html': 'a00eb31fa55e278e97c4f79cecc5bc33e56a64cbc995e786d8a384ef930934b1',
    'cerchi/guide/seneca-dominio-tempo-morte/index.html': 'e3d556682ae0b9cc4ca5f4416f3221bf267e6a945aa639fe653e2f20a2c13a26',
    'en/cerchi/guides/seneca-time-self-mastery-death/index.html': 'db40807f08d30b2184e45bf5e487d8430615d79b3544658b43ea3af5ff53d5ac',
    'cerchi/guide/cicerone-repubblica-legge-parola-civile/index.html': 'eacb2085a54a1e1a416ef1373ede065bd25964aad2dde56d5f656120d736dae2',
    'en/cerchi/guides/cicero-republic-law-civic-speech/index.html': '71839714c6efb9733b31c583bdd6b420cdd0ec04808f64fda58d2c975803adb6',
}
EDITORIAL_PROFILE = 'editorial-additions-v1'
FRAGMENTS = rb'<nav class="guide-toc"[^>]*>.*?</nav>'
PROTECTED = (
    ARTICLES, FRAGMENTS, rb'<(?:title|h1|header|footer)\b[^>]*>.*?</(?:title|h1|header|footer)>',
    rb'<meta\b[^>]*>', rb'<link rel="(?:canonical|alternate)"[^>]*>',
    rb'<script type="application/ld\+json">.*?</script>', rb'<img\b[^>]*>',
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def unique_keys(pairs):
    result = dict(pairs)
    require(len(result) == len(pairs), 'Duplicate Atlas manifest key')
    return result


def read_json_bytes(path):
    require(path.is_file() and not path.is_symlink(), f'Invalid Atlas data file: {path}')
    return path.read_bytes()


def entry_digest(baseline, record, recipe):
    """Bind the reviewed record, its baseline, and the exact recipe bytes."""
    entry = json.dumps([baseline, record], sort_keys=True, separators=(',', ':')).encode()
    return digest(entry + b'\0' + recipe)


def verify_editorial_entry(baseline, record, recipe):
    path = record['pagina']
    require((record['profilo'] == EDITORIAL_PROFILE) == (path in EDITORIAL_ENTRIES),
            'Editorial profile requires an explicit reviewed entry: ' + path)
    if path in EDITORIAL_ENTRIES:
        require(entry_digest(baseline, record, recipe) == EDITORIAL_ENTRIES[path],
                'Editorial record or recipe differs from the reviewed entry: ' + path)


def editorial_recipe(source, edits, is_en):
    """Only two insertions, outside the historical hero and manuscript body."""
    marker = (b'<div class="wrap atlas-reader">' if is_en else
              b'<section class="wrap section"><figure class="editorial-cover-card guide-cover">')
    end = b'</main>'
    require(source.count(marker) == source.count(end) == 1, 'Ambiguous editorial insertion point')
    require(len(edits) == 2 and all(len(edit) == 3 and edit[1] == '' for edit in edits),
            'Editorial recipe must be two additions')
    require(edits[0][0] == source.index(marker) and edits[1][0] == source.index(end),
            'Editorial insertion moved outside its approved position')
    require('id="editorial-reading-routes"' in edits[0][2] and
            'id="editorial-dialogue"' in edits[1][2], 'Editorial apparatus missing')


def reconstruct(source, edits, additions_only=False):
    pieces = []
    cursor = 0
    previous = -1
    for offset, removed, inserted in edits:
        old, new = removed.encode(), inserted.encode()
        require(type(offset) is int and previous < offset and cursor <= offset <= len(source)
                and source[offset:offset + len(old)] == old and old != new,
                'Invalid Atlas transformation range')
        require(not additions_only or not old, 'Additive apparatus transformation cannot remove bytes')
        pieces.extend((source[cursor:offset], new))
        cursor = offset + len(old)
        previous = offset
    return b''.join([*pieces, source[cursor:]])


def lucretius_consultation(source):
    """Convert only the two legacy Lucretius IT apparatuses, retaining exact inline HTML."""
    def controls(key, label):
        return (
            f'<div class="consult-tools" hidden data-consult-controls>'
            f'<label for="{key}-search">{label}</label>'
            f'<div class="consult-inputs"><input id="{key}-search" type="search"'
            f' autocomplete="off" aria-controls="{key}-entries">'
            '<button type="button" data-consult-reset>Azzera</button></div>'
            '<p role="status" aria-atomic="true"></p></div>'
        ).encode()

    def concepts(heading, body):
        columns = body[0]
        require(columns == b'    <p class="meta"><strong>Concetto</strong><br />Funzione nel pensiero lucreziano</p>',
                'Unexpected Lucretius concept columns')
        entries = []
        for line in body[1:]:
            row = re.fullmatch(rb'    <p>(<strong>.+?</strong>)<br />(.+)</p>', line)
            require(row is not None, 'Unexpected Lucretius concept row')
            term, definition = row.groups()
            entries.append(b'<tr data-consult-row><th scope="row">' + term + b'</th><td>' + definition + b'</td></tr>')
        require(len(entries) == 11, 'Lucretius requires 11 concept rows')
        return b'\n'.join([
            heading,
            b'    <div class="complete-table" data-consult="table">',
            b'      ' + controls('concetti-chiave', 'Cerca nella tabella'),
            b'      <div class="complete-table-region"><table aria-labelledby="lucrezio-concetti-title">',
            b'        <thead><tr><th scope="col"><strong>Concetto</strong></th>'
            b'<th scope="col">Funzione nel pensiero lucreziano</th></tr></thead>',
            b'        <tbody id="concetti-chiave-entries">',
            *(b'          ' + entry for entry in entries),
            b'        </tbody>',
            b'      </table></div>',
            b'    </div>',
        ])

    def glossary(heading, body):
        require(len(body) == 15 and all(
            re.fullmatch(rb'    <p><strong>.+?</strong><br /> .+</p>', line) for line in body),
            'Unexpected Lucretius glossary entries')
        return b'\n'.join([
            b'    <div data-consult="glossary">',
            b'  ' + heading,
            b'      ' + controls('glossario', 'Cerca nel glossario'),
            b'      <div class="consult-entries" id="glossario-entries">',
            *(b'    ' + line.replace(b'<p>', b'<p data-consult-row>', 1) for line in body),
            b'      </div>',
            b'    </div>',
        ])

    for section_id, heading, transform in (
        (b'concetti-chiave', b'Concetti chiave', concepts),
        (b'glossario', b'Glossario', glossary),
    ):
        opening = b'<article class="item guide-section" id="' + section_id + b'">\n'
        pattern = re.escape(opening) + rb'(.*?)\n  </article>'
        matches = list(re.finditer(pattern, source, re.S))
        require(len(matches) == 1, 'Expected exactly one Lucretius consultation section')
        match = matches[0]
        title, *body = match[1].split(b'\n')
        require(title == b'    <h2>' + heading + b'</h2>', 'Unexpected Lucretius consultation heading')
        if section_id == b'concetti-chiave':
            title = title.replace(b'<h2>', b'<h2 id="lucrezio-concetti-title">')
        source = source[:match.start(1)] + transform(title, body) + source[match.end(1):]
    return source


def validate(source, expected, actual, record):
    require(actual == expected and digest(actual) == record['outputSha256'],
            'Atlas output differs from the approved full document: ' + record['pagina'])
    blocks = re.findall(ARTICLES, source, re.S)
    framing = b''.join(len(block).to_bytes(8, 'big') + block for block in blocks)
    require(blocks and digest(framing) == record['articoliSha256'], 'Unexpected source article inventory')
    articles = lucretius_consultation(source) if record['pagina'] == LUCRETIUS_IT else source
    for pattern in PROTECTED:
        reference = articles if pattern == ARTICLES else source
        require(re.findall(pattern, reference, re.S) == re.findall(pattern, actual, re.S),
                f'Protected Atlas content changed: {pattern!r}')
    links = rb'<a\b[^>]*\bhref="([^"]+)"'
    require(Counter(re.findall(links, source)) <= Counter(re.findall(links, actual)),
            'Original Atlas link lost')
    ids = re.findall(rb'\bid="([^"]+)"', actual)
    require(len(ids) == len(set(ids)) and set(re.findall(rb'\bid="([^"]+)"', source)) <= set(ids),
            'Atlas anchors changed or duplicated')
    require(set(re.findall(rb'href="#([^"]+)"', actual)) <= set(ids), 'Unresolved Atlas anchor')
    lead = re.findall(rb'^[ \t]*<p class="lead">[^\n]+\n[ \t]*<p><a href="#[^"]+"[^\n]+\n',
                      source, re.M)
    for block in lead:
        require(actual.count(block) == 1, 'P1 lead and link must remain adjacent byte for byte')


def verified_sources(protected=None, base=None, self_test=False, approved_entries=None):
    """Return historical bytes after full validation, with optional reviewed-entry pins."""
    approved_entries = {**(approved_entries or {}), **LUCRETIUS_ENTRIES}
    manifest = json.loads(read_json_bytes(CONFIG / 'manifesto.json'), object_pairs_hook=unique_keys)
    baseline = manifest['baseline']
    require(manifest['versione'] == 1 and re.fullmatch(r'[0-9a-f]{40}', baseline),
            'Unsupported Atlas manifest')
    if base is not None:
        previous_manifest = subprocess.run(
            ['git', 'show', f'{base}:.github/atlas-it/manifesto.json'], cwd=ROOT,
            capture_output=True, check=False)
        if previous_manifest.returncode == 0:
            previous = json.loads(previous_manifest.stdout, object_pairs_hook=unique_keys)
            require(previous['baseline'] == baseline and
                    all(record in manifest['guide'] for record in previous['guide']),
                    'Published Atlas records and baseline must remain intact')
    sources, records = {}, {}
    mutations = 0
    for record in manifest['guide']:
        path, profile = record['pagina'], record['profilo']
        editorial = profile == EDITORIAL_PROFILE
        is_en = path.startswith('en/') if editorial else profile == 'apparato-en-v1'
        require(profile in {'legacy-it-v1', 'apparato-en-v1', EDITORIAL_PROFILE} and
                re.fullmatch(EN_PATH if is_en else IT_PATH, path)
                and path not in sources and (protected is None or path in protected),
                f'Invalid or unprotected Atlas path: {path}')
        require(git('ls-tree', baseline, '--', path).startswith(b'100644 blob '),
                f'Atlas baseline path is not a regular file: {path}')
        source = git('show', f'{baseline}:{path}')
        require(digest(source) == record['sorgenteSha256'], 'Atlas baseline digest differs: ' + path)
        recipe = record['modifiche']
        require(re.fullmatch(r'\.github/atlas-it/[a-z0-9-]+\.json', recipe)
                and ROOT / recipe != CONFIG / 'manifesto.json', 'Invalid Atlas transformation path')
        recipe_bytes = read_json_bytes(ROOT / recipe)
        verify_editorial_entry(baseline, record, recipe_bytes)
        if path in approved_entries:
            require(entry_digest(baseline, record, recipe_bytes) == approved_entries[path],
                    'Atlas manifest record or recipe differs from the reviewed entry: ' + path)
        edits = json.loads(recipe_bytes, object_pairs_hook=unique_keys)
        require(edits, 'Empty Atlas transformation')
        target = ROOT / path
        require(target.is_file() and not target.is_symlink() and target.resolve() == target,
                'Invalid Atlas page file: ' + path)
        recipe_source = lucretius_consultation(source) if path == LUCRETIUS_IT else source
        if editorial:
            editorial_recipe(source, edits, is_en)
        expected = reconstruct(recipe_source, edits, additions_only=is_en or editorial)
        validate(source, expected, target.read_bytes(), record)
        if not is_en and not editorial:
            figure = record['figura']
            anchor = re.escape(figure['dopoArticolo'].encode())
            figures = re.findall(rb'<article class="item guide-section" id="' + anchor +
                                 rb'">.*?</article>\s*(<figure\b[^>]*>.*?</figure>)', expected, re.S)
            require(figure['tipo'] == 'figura-radio-nativi-v1' and len(figures) == 1
                    and digest(figures[0]) == figure['sha256'], 'Approved Atlas figure changed')
        if is_en:
            revision_base = record['revisioneEN']
            require(re.fullmatch(r'[0-9a-f]{40}', revision_base), 'Invalid EN revision reference')
            git('merge-base', '--is-ancestor', revision_base, baseline)
            if base is not None:
                before = git('show', f'{base}:{path}')
                require(before in (source, expected), 'Atlas EN PR base differs from the frozen source')
        if self_test:
            edits_to_reject = [source, expected + b'\n',
                               re.sub(rb'<h1(?=[\s>])', b'<h1 hidden', expected, count=1)]
            for marker in (b'<article ', b'<aside class="atlas-relation', b'hreflang="'):
                require(marker in expected, 'Ineffective Atlas mutation fixture')
                edits_to_reject.append(expected.replace(marker, b'<!-- changed -->' + marker, 1))
            if editorial:
                for offset, removed, inserted in edits:
                    block = inserted.encode()
                    require(expected.count(block) == 1, 'Ineffective editorial apparatus fixture')
                    edits_to_reject.extend((expected.replace(block, b'', 1),
                                            expected.replace(block, block * 2, 1),
                                            expected.replace(block, block + b'<!-- altered -->', 1)))
                # Even a coordinated candidate/recipe/record edit must fail its reviewed pin.
                tampered = [list(edit) for edit in edits]
                tampered[1][2] += '<!-- altered -->'
                altered = reconstruct(source, tampered, additions_only=True)
                altered_record = {**record, 'outputSha256': digest(altered)}
                cases = (
                    (altered_record, json.dumps(tampered).encode()),
                    ({**record, 'profilo': 'apparato-en-v1' if is_en else 'legacy-it-v1'}, recipe_bytes),
                    (record, recipe_bytes + b' '),
                )
                for invalid_record, invalid_recipe in cases:
                    try:
                        verify_editorial_entry(baseline, invalid_record, invalid_recipe)
                    except AssertionError:
                        mutations += 1
                        continue
                    raise AssertionError('Editorial pin accepted an unapproved entry')
            if not is_en and not editorial:
                p1 = re.search(rb'^.*<p><a href="#[^"]+"[^\n]+\n', source, re.M)[0]
                require(p1 in expected, 'Ineffective P1 mutation fixture')
                edits_to_reject.extend((expected.replace(p1, b'', 1), expected.replace(p1, p1 * 2, 1)))
            for invalid in edits_to_reject:
                require(invalid != expected, 'Ineffective Atlas mutation fixture')
                try:
                    validate(source, expected, invalid, record)
                except AssertionError:
                    mutations += 1
                    continue
                raise AssertionError('Atlas migration accepted an unapproved document')
        sources[path], records[path] = source, record
    require(sources, 'Empty Atlas migration inventory')
    require(approved_entries.keys() <= sources.keys(), 'A reviewed Atlas entry is missing')
    require(EDITORIAL_ENTRIES.keys() <= sources.keys(), 'A reviewed editorial entry is missing')
    for path, source in sources.items():
        peer_lang = b'it' if path.startswith('en/') else b'en'
        peer = re.search(rb'<link rel="alternate" hreflang="' + peer_lang +
                         rb'" href="https://alessandro-gentili\.it/([^"]+)"', source)
        require(peer and peer[1].decode() + 'index.html' in sources,
                'Atlas migration must include both published editions: ' + path)
    if self_test:
        print(f'PASS Atlas: {len(sources)} complete documents and {mutations} rejected mutations')
    return sources, records
