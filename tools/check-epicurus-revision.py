#!/usr/bin/env python3
"""Epicurus EN25 v3: source-locked, baseline-locked revision authorization.

This permits only the specific, author-approved International 3.0 conversion.
No global preservation invariant is weakened. It does not certify visual quality.
"""
import argparse
from html import unescape
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAGE = "en/cerchi/guides/epicurus-desire-fear-freedom-before-choice/index.html"
CSS = "assets/international-epicurus.css"
SOURCE_COMMIT = "b952e6d5d96c336ad4a58ca6ca452e4faa58ce81"
SOURCE_FILE = "EPICURUS_25_INTERNATIONAL_3_0_MAIN_ESSAY_ATLAS_APPROVED_v3.md"
SOURCE_BLOB = "174ba814a08de72243d4ee171e5d7c0611999ab5"
BASE_BLOB = "c214e6f198d927f9c9524565f02a80015b90894b"
APPROVED_HTML_BLOB = "833282f7d19d4c5feec51dbed39b42cfefb92b07"
APPROVED_CSS_BLOB = "440a76142da157f6b3794ae16c1cd478dc514ec8"
CANONICAL = "https://alessandro-gentili.it/en/cerchi/guides/epicurus-desire-fear-freedom-before-choice/"


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def git_blob(ref, path):
    return git("rev-parse", f"{ref}:{path}")


def pinned_source():
    try:
        blob = git_blob(SOURCE_COMMIT, SOURCE_FILE)
    except subprocess.CalledProcessError:
        subprocess.run(["git", "fetch", "--no-tags", "origin", SOURCE_COMMIT],
                       cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        blob = git_blob(SOURCE_COMMIT, SOURCE_FILE)
    check(blob == SOURCE_BLOB, "Approved Epicurus source blob changed")
    return subprocess.check_output(
        ["git", "show", f"{SOURCE_COMMIT}:{SOURCE_FILE}"],
        cwd=ROOT, text=True
    )


def plain(value):
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.I)
    value = re.sub(r"</(?:p|h[1-6]|li|td|tr)>", " ", value, flags=re.I)
    return " ".join(unescape(re.sub(r"<[^>]*>", "", value)).split())


def md_plain(value):
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("**", "").replace("*", "").replace("`", "")
    return " ".join(value.split())


def schemas(value):
    return [json.loads(block) for block in re.findall(
        r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        value, flags=re.S
    )]


def verify(path, base):
    check(path.resolve().relative_to(ROOT).as_posix() == PAGE,
          "Wrong guide: Epicurus-only validator")
    check(git_blob(base, PAGE) == BASE_BLOB,
          "Epicurus baseline changed: STOP; review and reauthorize")
    check(git("hash-object", PAGE) == APPROVED_HTML_BLOB,
          "Epicurus HTML differs from the reviewed revision snapshot")
    check(git("hash-object", CSS) == APPROVED_CSS_BLOB,
          "Epicurus scoped CSS differs from the reviewed snapshot")
    source = pinned_source()
    previous = subprocess.check_output(["git", "show", f"{base}:{PAGE}"],
                                       cwd=ROOT, text=True)
    html = path.read_text("utf-8")
    css = (ROOT / CSS).read_text("utf-8")
    check(html.startswith("<!doctype html>") and html.rstrip().endswith("</html>"),
          "HTML document frame damaged")
    for tag in ("html", "head", "body", "main", "header", "footer"):
        check(len(re.findall(rf"<{tag}\b", html)) ==
              len(re.findall(rf"</{tag}>", html)) == 1,
              f"Malformed {tag} frame")
    check(len(re.findall(r"<h1\b", html)) == 1 and
          "<h1>Epicurus: desire, fear and freedom before choice</h1>" in html,
          "H1 has changed")
    check('<body class="guide-page international-atlas atlas-guide atlas-epicurus-v3">' in html,
          "Guide-specific Atlas scope missing")
    for needle in ("/assets/style.css", "/assets/international-atlas.css",
                   "/assets/international-epicurus.css", "/assets/script.js",
                   "/assets/international-atlas.js", "atlas-guide-opening",
                   "atlas-reader", "atlas-contents", "atlas-reading"):
        check(needle in html, f"Required site component missing: {needle}")
    for tag in ("title", "meta", "link"):
        pat = rf"<{tag}\b[^>]*>" if tag != "title" else r"<title>.*?</title>"
        check(re.findall(pat, previous, re.S) == re.findall(pat, html, re.S),
              f"Protected {tag} changed")
    for pattern in (
        r'<header class="site-header".*?</header>',
        r'<footer class="footer".*?</footer>',
        r'<figure class="editorial-cover-card guide-cover">.*?</figure>',
        r'<figure class="atlas-figure epicurus-figure".*?</figure>',
    ):
        old = re.search(pattern, previous, flags=re.S)
        new = re.search(pattern, html, flags=re.S)
        check(old and new and old.group() == new.group(),
              "Site chrome, cover or original native desire tool changed")
    old_ids = set(re.findall(r'\bid="([^"]+)"', previous))
    all_ids = re.findall(r'\bid="([^"]+)"', html)
    check(len(all_ids) == len(set(all_ids)), "Duplicate HTML IDs")
    check(old_ids.issubset(set(all_ids)),
          f"Original deep-link ID removed: {sorted(old_ids-set(all_ids))}")
    for anchor in re.findall(r'href="#([^"]+)"', html):
        check(anchor in all_ids, f"Unresolved local anchor #{anchor}")
    check('<details open>' in html, "No-JS guide contents unavailable")
    check(CANONICAL in html and f'href="{CANONICAL}"' in html,
          "Canonical or citation permalink missing")
    original_schemas, current_schemas = schemas(previous), schemas(html)
    check(len(original_schemas) == 2 and len(current_schemas) == 3,
          "Unexpected Article/Breadcrumb/FAQ schema count")
    older, newer = original_schemas[0].copy(), current_schemas[0].copy()
    check(newer.pop("dateModified") == "2026-11-06",
          "Unexpected revised dateModified")
    older.pop("dateModified", None)
    check(older == newer and original_schemas[1] == current_schemas[1],
          "Protected Article/Breadcrumb data changed")

    faq = re.search(
        r'<article class="item guide-section epicurus-section" id="faq">(.*?)</article>',
        html, flags=re.S
    )
    check(faq is not None, "Visible FAQ article missing")
    pairs = [(plain(question), plain(answer)) for question, answer in
             re.findall(r'<h3\b[^>]*>(.*?)</h3><p>(.*?)</p>',
                        faq.group(1), flags=re.S)]
    structured = [(q.get("name"), q.get("acceptedAnswer", {}).get("text"))
                  for q in current_schemas[2].get("mainEntity", [])]
    check(current_schemas[2].get("@type") == "FAQPage"
          and len(pairs) == 20 and pairs == structured,
          "20 visible FAQ pairs must match FAQPage exactly in order and text")

    headings = re.findall(r'^###\s+.+\{#([a-z0-9-]+)\}\s*$',
                          source, flags=re.M)
    check(len(headings) >= 30 and all(x in all_ids for x in headings),
          "An approved Atlas section or heading was lost")
    index = re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',
                      html, flags=re.S)
    check(index is not None, "Guide TOC missing")
    toc = re.findall(r'href="#([^"]+)"', index.group(1))
    check(len(toc) == 37 and len(toc) == len(set(toc)),
          "Source TOC entries missing or duplicated")
    source_toc = re.findall(r'\[[^\]]+\]\(#([a-z0-9-]+)\)',
                            source[source.index("### Contents"):
                                   source.index("## The main essay")])
    check(toc[2:-1] == source_toc and len(source_toc) == 34,
          "The TOC does not follow the exact approved Markdown order")
    check(len(re.findall(r'<table class="epicurus-semantic-table">', html)) == 4
          and len(re.findall(r"<tbody><tr>", html)) == 4,
          "Approved semantic tables missing")
    check(sum(len(re.findall(r"<tr>", fragment)) for fragment in
              re.findall(r"<tbody>(.*?)</tbody>", html, flags=re.S)) == 37,
          "Approved semantic table rows missing")
    check(len(re.findall(r'<input type="radio" name="epicurus-desire"', html)) == 3
          and len(re.findall(r'<section class="epicurus-panel', html)) == 3,
          "Three original radio states missing")
    check("input:focus-visible+label" in css and "@media print" in css
          and "display:block!important" in css
          and "@media(max-width:700px)" in css,
          "Focus, mobile or full-print safeguard missing")

    body_start = html.find('<div class="guide-body atlas-reading epicurus-v3-reading">')
    check(body_start > 0, "Static Guide 25 reading body missing")
    body = plain(html[body_start:html.index("</main>", body_start)])
    segment = source[source.index("## A reader's route"):
                     source.index("## Cite this English guide")]
    special = ("*Consider three forms", "**01 ·", "**02 ·", "**03 ·",
               "*Need ·", "*Need met", "*Recognition")
    n = 0
    for paragraph in re.split(r"\n\s*\n", segment):
        paragraph = paragraph.strip()
        if (not paragraph or paragraph == "---" or paragraph.startswith(
                ("#", "|", "**The main essay", "**The Atlas desk", "- "))
                or re.match(r"^\d+\.\s", paragraph)
                or paragraph.startswith(special)):
            continue
        expected = md_plain(paragraph)
        check(expected in body, f"Approved paragraph changed or omitted: {expected[:90]}")
        n += 1
    check(n >= 130, f"Only {n} source paragraphs checked; unexpected compression")
    for phrase in ("Consider three forms of desire", "Thirst can be satisfied.",
                   "A richer meal may be welcome.", "Applause may ask for more applause.",
                   "The distinction is practical, not a moral label."):
        check(phrase in html, "Original interactive content omitted: " + phrase)

    print(f"PASS Epicurus EN25 v3: pinned source and HTML/CSS blobs, {n} "
          "exact content blocks, 34 source TOC entries, 20 FAQ pairs, "
          "4 semantic tables, 3 original native radio states, "
          "protected meta/schema/cover and print constraints")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    verify(ROOT / PAGE, args.base)
