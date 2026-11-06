#!/usr/bin/env python3
"""Thucydides EN31 International v3: source- and snapshot-locked revision validator.
This authorises one approved guide conversion only. Existing guard remains the
default for every other guide. A technical PASS is not a live visual audit.
"""
import argparse
from html import unescape
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAGE = "en/cerchi/guides/thucydides-war-power-crisis-of-language/index.html"
CSS = "assets/international-thucydides.css"
JS = "assets/international-thucydides.js"
SOURCE_FILE = "THUCYDIDES_EN_GUIDE_31_MAIN_ESSAY_ATLAS_APPROVED_v3.md"
SOURCE_COMMIT = "3987fb51445a254f96413f095e9a8725337215c6"
SOURCE_BLOB = "0dc3fd78254572cd96273ffec927408a25fa7a7f"
BASE_BLOB = "c42b0c4114cfee2296b0b8ed0108134b24b70f9f"
APPROVED_HTML_BLOB = "c5ad8030a856be2073c4d04603bc72194a272fcc"
APPROVED_CSS_BLOB = "ae526fe1f3967f4c65835f86b05dfbdcf8149d4b"
APPROVED_JS_BLOB = "d2f5c9efa45e7c70103259087490722d5a3522fd"
CANONICAL = "https://alessandro-gentili.it/en/cerchi/guides/thucydides-war-power-crisis-of-language/"


def check(ok, error):
    if not ok:
        raise AssertionError(error)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def source_at_commit():
    try:
        blob = git("rev-parse", f"{SOURCE_COMMIT}:{SOURCE_FILE}")
    except subprocess.CalledProcessError:
        subprocess.run(["git", "fetch", "--no-tags", "origin", SOURCE_COMMIT],
                       cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        blob = git("rev-parse", f"{SOURCE_COMMIT}:{SOURCE_FILE}")
    check(blob == SOURCE_BLOB, "Approved Thucydides source blob changed")
    return subprocess.check_output(
        ["git", "show", f"{SOURCE_COMMIT}:{SOURCE_FILE}"],
        cwd=ROOT, text=True)


def clean_html(raw):
    raw = re.sub(r"<br\s*/?>", " ", raw, flags=re.I)
    raw = re.sub(r"</(?:p|li|td|th|tr|h[1-6])>", " ", raw, flags=re.I)
    return " ".join(unescape(re.sub(r"<[^>]*>", "", raw)).split())


def clean_markdown(raw):
    raw = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw)
    return " ".join(raw.replace("**", "").replace("*", "")
                    .replace("`", "").split())


def json_schemas(page):
    return [json.loads(obj) for obj in re.findall(
        r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        page, re.S)]


def md_table(text, beginning, next_section):
    start, end = text.index(beginning), text.index(next_section, text.index(beginning)+1)
    lines = text[start:end].splitlines()
    first = next(i for i, line in enumerate(lines) if line.startswith("|"))
    rows = [line for line in lines[first:] if line.startswith("|")]
    check(len(rows) > 2 and re.match(r"^\|\s*:?-{3,}", rows[1]),
          "Malformed source table")
    def cells(line):
        return [clean_markdown(x.strip()) for x in line.strip().strip("|").split("|")]
    return [cells(row) for row in [rows[0]] + rows[2:]]


def verify(path, base):
    check(path.resolve().relative_to(ROOT).as_posix() == PAGE,
          "Wrong guide path for single-guide Thucydides validator")
    check(git("rev-parse", f"{base}:{PAGE}") == BASE_BLOB,
          "Published Thucydides baseline changed: STOP")
    for filename, expected in (
        (PAGE, APPROVED_HTML_BLOB),
        (CSS, APPROVED_CSS_BLOB),
        (JS, APPROVED_JS_BLOB),
    ):
        check(git("hash-object", filename) == expected,
              f"Unreviewed Thucydides file snapshot: {filename}")
    md = source_at_commit()
    original = subprocess.check_output(["git", "show", f"{base}:{PAGE}"],
                                       cwd=ROOT, text=True)
    html = path.read_text("utf-8")
    css = (ROOT / CSS).read_text("utf-8")
    js = (ROOT / JS).read_text("utf-8")
    previous_css = subprocess.check_output(["git", "show", f"{base}:{CSS}"],
                                           cwd=ROOT, text=True)
    check(css.startswith(previous_css),
          "Original native two-decree CSS not preserved")
    check(html.startswith("<!doctype html>") and
          html.rstrip().endswith("</html>"), "HTML document incomplete")
    for tag in ("html", "head", "body", "main", "header", "footer"):
        check(len(re.findall(rf"<{tag}\b", html)) ==
              len(re.findall(rf"</{tag}>", html)) == 1,
              f"Wrong {tag} element count")
    check(len(re.findall(r"<h1\b", html)) == 1 and
          "<h1>Thucydides: war, power and the crisis of language</h1>" in html,
          "Original title/H1 altered")
    check('<body class="guide-page international-atlas atlas-guide atlas-thucydides-v3">' in html,
          "Guide-specific Atlas class missing")
    for token in ("/assets/style.css", "/assets/international-atlas.css",
                  "/assets/international-thucydides.css",
                  "/assets/international-thucydides.js", "/assets/script.js",
                  "/assets/international-atlas.js", "atlas-guide-opening",
                  "atlas-reader", "atlas-contents", "atlas-reading"):
        check(token in html, f"Required site component absent: {token}")
    for tag in ("title", "meta", "link"):
        pattern = (r"<title>.*?</title>" if tag == "title" else
                   rf"<{tag}\b[^>]*>")
        check(re.findall(pattern, original, re.S) ==
              re.findall(pattern, html, re.S),
              f"Protected {tag} / canonical / hreflang changed")
    for pattern in (
        r'<header class="site-header".*?</header>',
        r'<footer class="footer".*?</footer>',
        r'<figure class="editorial-cover-card guide-cover">.*?</figure>',
        r'<figure class="atlas-figure mytilene-figure".*?</figure>',
    ):
        old, new = re.search(pattern, original, re.S), re.search(pattern, html, re.S)
        check(old and new and old.group() == new.group(),
              "Existing header/footer/cover/two-decree module changed")
    require_radio = re.search(
        r'<figure class="atlas-figure mytilene-figure".*?</figure>',
        html, re.S).group()
    check(len(re.findall(r'<input type="radio" name="mytilene-decree"', require_radio)) == 2
          and len(re.findall(r'<section class="mytilene-panel', require_radio)) == 2,
          "Original two-decree radio states missing")
    check("mytilene-switch>input:focus-visible+label" in css
          and "@media print" in css and "display:table-row!important" in css,
          "Native focus/print table safeguards missing")
    existing_ids = set(re.findall(r'\bid="([^"]+)"', original))
    current_ids = re.findall(r'\bid="([^"]+)"', html)
    check(len(current_ids) == len(set(current_ids)), "Duplicated IDs")
    check(existing_ids.issubset(set(current_ids)),
          "Legacy Thucydides anchors removed: " +
          str(sorted(existing_ids - set(current_ids))))
    for anchor in re.findall(r'href="#([^"]+)"', html):
        check(anchor in current_ids, "Unresolved in-page link #" + anchor)
    check("<details open>" in html and
          f'href="{CANONICAL}"' in html,
          "Guide contents without JS or citation URL missing")

    older, newer = json_schemas(original), json_schemas(html)
    check(len(older) == 2 and len(newer) == 3,
          "Article / BreadcrumbList / FAQPage schema count changed")
    oa, na = dict(older[0]), dict(newer[0])
    check(na.pop("dateModified") == "2026-11-06",
          "dateModified not updated")
    oa.pop("dateModified", None)
    check(na == oa and older[1] == newer[1],
          "Protected Article/Breadcrumb structured facts changed")
    faq_section = re.search(
        r'<article class="item guide-section thucydides-section" id="faq">(.*?)</article>',
        html, re.S)
    check(faq_section is not None, "Visible FAQ section absent")
    visible = [(clean_html(q), clean_html(answer)) for q, answer in re.findall(
        r'<h3\b[^>]*>(.*?)</h3><p>(.*?)</p>',
        faq_section.group(1), re.S)]
    faq_schema = newer[2]
    structured = [(q.get("name"), q.get("acceptedAnswer", {}).get("text"))
                  for q in faq_schema.get("mainEntity", [])]
    check(faq_schema.get("@type") == "FAQPage"
          and len(visible) == len(structured) == 20
          and visible == structured, "Visible FAQs and FAQPage differ")

    sections = re.findall(r'^###\s+.+\{#([a-z0-9-]+)\}\s*$', md, flags=re.M)
    check(len(sections) == 35 and
          all(section in current_ids for section in sections),
          "Approved 9 essay + 26 Atlas section anchors missing")
    toc_node = re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',
                         html, re.S)
    check(toc_node is not None, "Guide TOC absent")
    actual = re.findall(r'href="#([^"]+)"', toc_node.group(1))
    expected = re.findall(
        r'\[[^\]]+\]\(#([a-z0-9-]+)\)',
        md[md.index("### Contents"):md.index("## The main essay")])
    check(len(expected) == 35 and
          [anchor for anchor in actual if anchor in expected] == expected
          and len(actual) == len(set(actual)) == 39,
          "TOC not in exact approved Markdown order")

    for key, begin, end, n in (
        ("life", "### A life in the history he wrote {#life}",
         "### The Greek world and its fault lines {#context}", 11),
        ("works", "### The work: eight books, an unfinished war {#works}",
         "### The two-decree instrument {#mytilene-instrument}", 8),
        ("glossary", "### Working glossary {#glossary}",
         "### Reading paths {#reading-paths}", 24),
    ):
        md_rows = md_table(md, begin, end)
        check(len(md_rows) == n+1, f"Incorrect source {key} table rows")
        table = re.search(
            rf'<table id="thucydides-{key}-table" class="thucydides-data-table">(.*?)</table>',
            html, re.S)
        check(table is not None, f"Missing {key} semantic table")
        rows = re.findall(r'<tr\b[^>]*>(.*?)</tr>', table.group(1), re.S)
        check(len(rows) == n+1, f"Wrong number of {key} HTML table rows")
        displayed = [[clean_html(cell) for cell in re.findall(
            r'<(?:td|th)\b[^>]*>(.*?)</(?:td|th)>',
            row, re.S)] for row in rows]
        check(md_rows == displayed, f"Approved {key} data cells modified")
        check(f'data-thucydides-controls="{key}" hidden' in html,
              f"{key} controls must stay hidden with JS off")
        for suffix in ("search","reset","count"):
            check(f'id="thucydides-{key}-{suffix}"' in html,
                  f"Missing {key} {suffix}")
        if key != "glossary":
            check(f'id="thucydides-{key}-sort"' in html,
                  f"Missing {key} original/reverse sort control")

    start = html.index('<div class="guide-body atlas-reading thucydides-v3-reading">')
    body = clean_html(html[start:html.index("</main>", start)])
    document = md[md.index("## A reader's route"):
                  md.index("## Cite this English guide")]
    # The approved native figure is checked unchanged, with its labels and
    # caveat, rather than re-rendering the editorial Markdown schematic.
    figure_start = document.index("#### A closer look · Mytilene, 427 BCE")
    figure_end = document.index("#### A reading procedure: four questions after the vote")
    source_without_diagram = (document[:figure_start] + document[figure_end:])
    paragraphs = 0
    for paragraph in re.split(r"\n\s*\n", source_without_diagram):
        paragraph = paragraph.strip()
        if (not paragraph or paragraph == "---" or
            paragraph.startswith(("#", "|", "- ",
                                  "**The main essay", "**The Atlas desk")) or
            re.match(r"^\d+\.\s", paragraph)):
            continue
        expected = clean_markdown(paragraph)
        check(expected in body, "Approved source prose missing: " + expected[:100])
        paragraphs += 1
    check(paragraphs >= 120, f"Insufficient tested prose blocks: {paragraphs}")
    for line in source_without_diagram.splitlines():
        match = re.match(r'^[-*]\s+(.+)$|^\d+\.\s+(.+)$', line.strip())
        if match and "](" not in line:
            expected = clean_markdown(match[1] or match[2])
            check(expected in body, "Approved list item omitted: " + expected[:75])
    for url in re.findall(r'\]\((https?://[^)]+|/[^)]+)\)', md):
        check(f'href="{url.replace("&", "&amp;")}"' in html,
              "Source Markdown link missing: " + url)
    check("beforeprint" in js and "afterprint" in js and
          "panel.hidden = false" in js and
          "row.hidden = !words.every" in js,
          "Progressive table controls or full print restoration missing")
    subprocess.run(["node","--check", JS], cwd=ROOT, check=True)
    subprocess.run(["node","tools/test-thucydides-interaction.cjs"],
                   cwd=ROOT, check=True)
    print(f"PASS Thucydides EN31 v3: source/HTML/CSS/JS pins, {paragraphs} exact "
          "source prose blocks, 35 source sections, 20 FAQ/schema pairs, "
          "11+8+24 exact semantic table rows, 2 native decree states, "
          "SEO/cover preservation and search/print DOM regression harness")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    verify(ROOT / PAGE, args.base)
