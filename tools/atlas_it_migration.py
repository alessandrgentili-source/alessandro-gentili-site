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


def reconstruct(source, edits, additions_only=False):
    pieces = []
    cursor = 0
    previous = -1
    for offset, removed, inserted in edits:
        old, new = removed.encode(), inserted.encode()
        require(type(offset) is int and previous < offset and cursor <= offset <= len(source)
                and source[offset:offset + len(old)] == old and old != new,
                'Invalid Atlas transformation range')
        require(not additions_only or not old, 'EN apparatus transformation must be additive')
        pieces.extend((source[cursor:offset], new))
        cursor = offset + len(old)
        previous = offset
    return b''.join([*pieces, source[cursor:]])


def validate(source, expected, actual, record):
    require(actual == expected and digest(actual) == record['outputSha256'],
            'Atlas output differs from the approved full document: ' + record['pagina'])
    blocks = re.findall(ARTICLES, source, re.S)
    framing = b''.join(len(block).to_bytes(8, 'big') + block for block in blocks)
    require(blocks and digest(framing) == record['articoliSha256'], 'Unexpected source article inventory')
    for pattern in PROTECTED:
        require(re.findall(pattern, source, re.S) == re.findall(pattern, actual, re.S),
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
    approved_entries = approved_entries or {}
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
        is_en = profile == 'apparato-en-v1'
        require(profile in {'legacy-it-v1', 'apparato-en-v1'} and
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
        if path in approved_entries:
            require(entry_digest(baseline, record, recipe_bytes) == approved_entries[path],
                    'Atlas manifest record or recipe differs from the reviewed entry: ' + path)
        edits = json.loads(recipe_bytes, object_pairs_hook=unique_keys)
        require(edits, 'Empty Atlas transformation')
        target = ROOT / path
        require(target.is_file() and not target.is_symlink() and target.resolve() == target,
                'Invalid Atlas page file: ' + path)
        expected = reconstruct(source, edits, additions_only=is_en)
        validate(source, expected, target.read_bytes(), record)
        if not is_en:
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
                               expected.replace(b'<h1>', b'<h1 hidden>', 1)]
            for marker in (b'<article ', b'<aside class="atlas-relation', b'hreflang="'):
                require(marker in expected, 'Ineffective Atlas mutation fixture')
                edits_to_reject.append(expected.replace(marker, b'<!-- changed -->' + marker, 1))
            if not is_en:
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
    for path, source in sources.items():
        peer_lang = b'it' if path.startswith('en/') else b'en'
        peer = re.search(rb'<link rel="alternate" hreflang="' + peer_lang +
                         rb'" href="https://alessandro-gentili\.it/([^"]+)"', source)
        require(peer and peer[1].decode() + 'index.html' in sources,
                'Atlas migration must include both published editions: ' + path)
    if self_test:
        print(f'PASS Atlas: {len(sources)} complete documents and {mutations} rejected mutations')
    return sources, records
