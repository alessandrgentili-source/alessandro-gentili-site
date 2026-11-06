#!/usr/bin/env python3
"""Tarde EN26 v3 source-locked International revision gate.

Protects exact approved source, existing page facts and exact reviewed HTML/CSS/JS
snapshots. Structural/content checks and a Node interaction harness are also run.
A technical PASS does not certify desktop/mobile visuals or literary quality.
"""
import argparse
from html import unescape
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAGE = "en/cerchi/guides/gabriel-tarde-imitation-belief-desire/index.html"
CSS = "assets/international-tarde.css"
JS = "assets/international-tarde.js"
SOURCE_COMMIT = "9a0ae3dada95c197476b5300901802bda96db94c"
SOURCE_FILE = "TARDE_EN_GUIDE_26_MAIN_ESSAY_ATLAS_APPROVED_v3.md"
SOURCE_BLOB = "81b7d5ac63076282d41823358426d70c8caa3ef5"
BASE_BLOB = "3d712f6f9d8bc5d1ae6833c8a6c51bee44138996"
APPROVED_HTML_BLOB = "7a313c4855eb2b9d44cc6646180336a26591cc02"
APPROVED_CSS_BLOB = "6d38a4f38020b9920ae5d98dd1ad0f0e5a88b8a3"
APPROVED_JS_BLOB = "0b58f2d4c3bb51e7705de61f5adc85c2b2caccea"
URL = "https://alessandro-gentili.it/en/cerchi/guides/gabriel-tarde-imitation-belief-desire/"


def require(ok, msg):
    if not ok:
        raise AssertionError(msg)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def blob(ref, path):
    return git("rev-parse", f"{ref}:{path}")


def pinned_source():
    try:
        found = blob(SOURCE_COMMIT, SOURCE_FILE)
    except subprocess.CalledProcessError:
        subprocess.run(["git", "fetch", "--no-tags", "origin", SOURCE_COMMIT],
                       cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        found = blob(SOURCE_COMMIT, SOURCE_FILE)
    require(found == SOURCE_BLOB, "Approved Tarde EN26 source blob has changed")
    return subprocess.check_output(
        ["git", "show", f"{SOURCE_COMMIT}:{SOURCE_FILE}"],
        cwd=ROOT, text=True)


def plain(text):
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.I)
    text = re.sub(r"</(?:p|li|td|th|tr|h[1-6])>", " ", text, flags=re.I)
    return " ".join(unescape(re.sub(r"<[^>]*>", "", text)).split())


def md_plain(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return " ".join(text.replace("**", "").replace("*", "")
                    .replace("`", "").split())


def find_schema(html):
    return [json.loads(x) for x in re.findall(
        r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        html, re.S)]


def table_md(source, start_marker, end_marker):
    begin = source.index(start_marker)
    end = source.index(end_marker, begin + len(start_marker))
    lines = source[begin:end].splitlines()
    first = next(i for i, line in enumerate(lines) if line.startswith("|"))
    rows = [line for line in lines[first:] if line.startswith("|")]
    def cols(line):
        return [v.strip() for v in line.strip().strip("|").split("|")]
    require(len(rows) >= 3 and rows[1].startswith("| ---"),
            "Invalid approved Markdown table")
    return [[md_plain(cell) for cell in cols(line)]
            for line in [rows[0]] + rows[2:]]


def verify(path, base):
    require(path.resolve().relative_to(ROOT).as_posix() == PAGE,
            "Wrong page path for Tarde-specific contract")
    require(blob(base, PAGE) == BASE_BLOB,
            "Published Tarde baseline changed: STOP")
    require(git("hash-object", PAGE) == APPROVED_HTML_BLOB,
            "Tarde HTML differs from the approved source-conversion snapshot")
    require(git("hash-object", CSS) == APPROVED_CSS_BLOB,
            "Tarde scoped CSS differs from the reviewed snapshot")
    require(git("hash-object", JS) == APPROVED_JS_BLOB,
            "Tarde interactive JS differs from the reviewed snapshot")
    md = pinned_source()
    old = subprocess.check_output(
        ["git", "show", f"{base}:{PAGE}"], cwd=ROOT, text=True)
    html = path.read_text(encoding="utf-8")
    css = (ROOT / CSS).read_text(encoding="utf-8")
    js = (ROOT / JS).read_text(encoding="utf-8")
    previous_css = subprocess.check_output(
        ["git", "show", f"{base}:{CSS}"], cwd=ROOT, text=True)
    require(css.startswith(previous_css),
            "Previous original native Tarde CSS was changed")
    require(html.startswith("<!doctype html>") and
            html.rstrip().endswith("</html>"), "Broken HTML frame")
    for tag in ("html", "head", "body", "main", "header", "footer"):
        require(len(re.findall(rf"<{tag}\b", html)) ==
                len(re.findall(rf"</{tag}>", html)) == 1,
                f"Unexpected {tag} element count")
    require(len(re.findall(r"<h1\b", html)) == 1 and
            "<h1>Gabriel Tarde: imitation, belief and desire</h1>" in html,
            "Page H1 changed")
    require('<body class="guide-page international-atlas atlas-guide atlas-tarde-v3">' in html,
            "Tarde Atlas page scope missing")
    for resource in ("/assets/style.css", "/assets/international-atlas.css",
                     "/assets/international-tarde.css", "/assets/script.js",
                     "/assets/international-atlas.js",
                     "/assets/international-tarde.js", "atlas-reader",
                     "atlas-contents", "atlas-reading", "atlas-guide-opening"):
        require(resource in html, f"Required asset/component missing: {resource}")
    for tag in ("title", "meta", "link"):
        pattern = (r"<title>.*?</title>" if tag == "title" else
                   rf"<{tag}\b[^>]*>")
        require(re.findall(pattern, old, re.S) ==
                re.findall(pattern, html, re.S),
                f"Protected {tag} or canonical/hreflang altered")
    for pattern in (
        r'<header class="site-header".*?</header>',
        r'<footer class="footer".*?</footer>',
        r'<figure class="editorial-cover-card guide-cover">.*?</figure>',
    ):
        a, b = re.search(pattern, old, re.S), re.search(pattern, html, re.S)
        require(a and b and a.group() == b.group(),
                "Approved header/footer/cover/alt changed")
    a = re.search(r'<figure class="atlas-figure tarde-figure".*?</figure>',
                  old, re.S)
    b = re.search(r'<figure class="atlas-figure tarde-figure".*?</figure>',
                  html, re.S)
    require(a and b, "Original native three-way Tarde instrument missing")
    strip_caption = lambda figure: re.sub(
        r"<figcaption>.*?</figcaption>", "", figure, flags=re.S)
    require(strip_caption(a.group()) == strip_caption(b.group()),
            "Original native tool changed apart from typography of caption")
    require("Editorial interpretation of <em>Les Lois de l'imitation</em>" in
            b.group(), "Approved figure caption typography not restored")
    require(len(re.findall(r'<input type="radio" name="tarde-response"',
                           b.group())) == 3
            and len(re.findall(r'<section class="tarde-panel', b.group())) == 3,
            "Three real native radio states must be preserved")

    old_ids = set(re.findall(r'\bid="([^"]+)"', old))
    new_ids = re.findall(r'\bid="([^"]+)"', html)
    require(len(new_ids) == len(set(new_ids)), "Duplicate document IDs")
    require(old_ids.issubset(new_ids),
            "Legacy deep links removed: " + str(sorted(old_ids - set(new_ids))))
    for match in re.findall(r'href="#([^"]+)"', html):
        require(match in new_ids, "Unresolved local link #" + match)
    require('<details open>' in html, "Guide contents unavailable without JS")
    require(f'href="{URL}"' in html, "Canonical or citation URL absent")
    before_schema, after_schema = find_schema(old), find_schema(html)
    require(len(before_schema) == 2 and len(after_schema) == 3,
            "Article/Breadcrumb/FAQ schema count mismatch")
    older, newer = dict(before_schema[0]), dict(after_schema[0])
    require(newer.pop("dateModified") == "2026-11-06",
            "Revised dateModified wrong")
    older.pop("dateModified", None)
    require(newer == older and after_schema[1] == before_schema[1],
            "Protected Article/BreadcrumbList changed")

    faq = re.search(r'<article class="item guide-section tarde-section" id="faq">(.*?)</article>',
                    html, re.S)
    require(faq is not None, "Static visible FAQs missing")
    vis = [(plain(q), plain(a)) for q, a in re.findall(
        r'<h3\b[^>]*>(.*?)</h3><p>(.*?)</p>', faq.group(1), re.S)]
    schema = after_schema[2]
    structured = [(q.get("name"), q.get("acceptedAnswer", {}).get("text"))
                  for q in schema.get("mainEntity", [])]
    require(schema.get("@type") == "FAQPage" and
            len(vis) == len(structured) == 20 and vis == structured,
            "Exactly 20 FAQPage pairs must match visible FAQ in number/order/text")

    source_anchors = re.findall(
        r'^###\s+.+\{#([a-z0-9-]+)\}\s*$', md, flags=re.M)
    require(len(source_anchors) == 34 and
            all(anchor in new_ids for anchor in source_anchors),
            "A source section of the 9+25 blocks was lost")
    toc = re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',
                    html, re.S)
    require(toc is not None, "Guide contents missing")
    actual = re.findall(r'href="#([^"]+)"', toc.group(1))
    expected = re.findall(
        r'\[[^\]]+\]\(#([a-z0-9-]+)\)',
        md[md.index("### Contents"):md.index("## The main essay")])
    require(len(expected) == 34 and
            [x for x in actual if x in expected] == expected and
            len(actual) == len(set(actual)) == 38,
            "Source TOC entries missing, duplicated or reordered")

    for key, from_mark, to_mark, n in (
        ("life", "### A life that illuminates the works {#life}",
         "### Historical and intellectual setting {#context}", 8),
        ("works", "### Works: a map for reading {#works}",
         "### A Cerchi instrument: the fate of an invention {#invention-instrument}", 8),
        ("glossary", "### Working glossary {#glossary}",
         "### Reading paths {#reading-paths}", 20),
    ):
        src = table_md(md, from_mark, to_mark)
        require(len(src) == n + 1, f"Markdown {key} source row count altered")
        fragment = re.search(
            rf'<table class="tarde-data-table" id="tarde-{key}-table">(.*?)</table>',
            html, re.S)
        require(fragment is not None, f"Missing {key} semantic table")
        rows = re.findall(r'<tr\b[^>]*>(.*?)</tr>', fragment.group(1), re.S)
        require(len(rows) == n+1, f"{key} table missing rows")
        converted = [[plain(v) for v in re.findall(
            r'<(?:th|td)\b[^>]*>(.*?)</(?:th|td)>', row, re.S)]
            for row in rows]
        require(converted == src, f"Approved {key} cells changed or reordered")
        require(f'data-tarde-controls="{key}" hidden' in html,
                f"{key} no-JS semantic fallback missing")
        for suffix in ("search", "reset", "count"):
            require(f'id="tarde-{key}-{suffix}"' in html,
                    f"{key} control missing: {suffix}")
        if key != "glossary":
            require(f'id="tarde-{key}-sort"' in html,
                    f"{key} chronological sort missing")
    require("tarde-switch>input:focus-visible+label" in css and
            "@media print" in css and "display:table-row!important" in css,
            "Original focus and complete mobile/print table safeguards missing")
    require("beforeprint" in js and "afterprint" in js and
            'panel.hidden = false' in js,
            "Source table progressive enhancement or print restoration missing")

    bstart = html.find('<div class="guide-body atlas-reading tarde-v3-reading">')
    require(bstart >= 0, "Reader content missing")
    document = plain(html[bstart:html.index("</main>", bstart)])
    document_source = md[md.index("## A reader's route"):
                         md.index("## Cite this English guide")]
    n_paragraphs = 0
    for paragraph in re.split(r"\n\s*\n", document_source):
        paragraph = paragraph.strip()
        if (not paragraph or paragraph == "---" or
            paragraph.startswith(("#", "|", "- ", "*Explore three",
                                  "**Adopt —", "**Resist —",
                                  "**Recombine —", "*New model",
                                  "*Several models", "*Figure caption:",
                                  "**The main essay", "**The Atlas desk"))
            or re.match(r"^\d+\.\s", paragraph)):
            continue
        expected = md_plain(paragraph)
        require(expected in document,
                "Approved prose missing or rewritten: " + expected[:95])
        n_paragraphs += 1
    require(n_paragraphs >= 120,
            f"Too few editorial paragraphs checked: {n_paragraphs}")
    for line in document_source.splitlines():
        match = re.match(r'^[-*]\s+(.+)$|^\d+\.\s+(.+)$', line.strip())
        if match and "](" not in line:
            expected = md_plain(match[1] or match[2])
            require(expected in document, "Approved list item missing: " + expected[:65])
    for url in re.findall(r'\]\((https?://[^)]+|/[^)]+)\)', md):
        require(f'href="{url.replace("&", "&amp;")}"' in html,
                "Approved source link missing: " + url)

    subprocess.run(["node", "--check", JS], cwd=ROOT, check=True)
    subprocess.run(["node", "tools/test-tarde-interaction.cjs"], cwd=ROOT, check=True)
    print("PASS Tarde EN26 v3: source/HTML/CSS/JS pinned, " +
          str(n_paragraphs) + " exact prose blocks, 34 source sections, " +
          "20 visible/schema FAQs, 8+8+20 source-exact table rows, " +
          "3 native radio views, protected cover/SEO and JS interaction harness")


if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("--base", required=True)
    args = arg.parse_args()
    verify(ROOT / PAGE, args.base)
