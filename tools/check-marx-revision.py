#!/usr/bin/env python3
"""Pinned editorial integrity gate for Marx EN 04 v1.1 only."""
from html import unescape
from pathlib import Path
import hashlib
import json
import re
import subprocess
import runpy

ROOT = Path(__file__).resolve().parents[1]
PAGE = "en/cerchi/guides/karl-marx-capital-labor-alienation/index.html"
SOURCE_COMMIT = "4943241b9457b27048c733477137fa0c031f334e"
SOURCE = "MARX_EN_GUIDE_04_CANDIDATE_v1_1.md"
SOURCE_HASH = "d4e8707f7d992a873bd9efd06299d61bea65d5327247bc8bd5c83748204891c2"
ORIGINAL_BLOB = "5123324a5c492a6662d8e5f00c9f1df2b14dc109"

def check(ok, message):
    if not ok:
        raise AssertionError(message)

def git_text(ref, path):
    return subprocess.check_output(["git", "show", ref + ":" + path], cwd=ROOT).decode("utf-8")

def txt(value):
    return " ".join(unescape(re.sub(r"<[^>]*>", " ", value)).split())

def words(value):
    return re.findall(r"[\w]+", value, re.UNICODE)

def manuscript_body(source):
    blocks = re.split(r"\n\s*\n", source.strip())[3:]
    parts = []
    for block in blocks:
        if block.strip() == "---":
            continue
        lines = block.strip().splitlines()
        if lines[0].startswith("|"):
            for line in lines:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    parts.extend(cells)
        else:
            parts.append(" ".join(re.sub(r"^(?:#{1,3} |>\s*|-\s*)", "", line.strip()) for line in lines))
    result = " ".join(parts)
    result = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", result)
    return re.sub(r"\*\*|\*|\x60", "", result)

def schemas(value):
    data = re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', value, re.S)
    objs = [json.loads(v) for v in data]
    check(len({v["@type"] for v in objs}) == len(objs), "Duplicate schema types")
    return {v["@type"]: v for v in objs}

def verify(path, base):
    relative = path.resolve().relative_to(ROOT).as_posix()
    check(relative == PAGE, "Other guide not authorised")
    original_blob = subprocess.check_output(["git", "rev-parse", base + ":" + PAGE], cwd=ROOT, text=True).strip()
    check(original_blob == ORIGINAL_BLOB, "Published source version changed")
    source = git_text(SOURCE_COMMIT, SOURCE)
    check(hashlib.sha256(source.encode("utf-8")).hexdigest() == SOURCE_HASH, "Source hash differs")
    before, after = git_text(base, PAGE), path.read_text(encoding="utf-8")
    check("awaiting human approval" not in after and "Editorial candidate v1.1" not in after,
          "Editorial workflow disclaimer leaked")
    check(after.count("<h1") == 1 and "<h1>Karl Marx: capital, labour and alienation</h1>" in after, "Approved H1 missing")
    Tree = runpy.run_path(str(ROOT / "tools/validate-cerchi-guide.py"))["Tree"]
    check(not Tree(after).malformed, "Malformed HTML structure")
    for tag in ("title", "header", "footer"):
        pattern = rf"<{tag}\b[^>]*>.*?</{tag}>"
        check(re.findall(pattern, before, re.S) == re.findall(pattern, after, re.S),
              "Protected " + tag + " changed")
    cover = r'<figure class="editorial-cover-card guide-cover".*?</figure>'
    check(re.findall(cover, before, re.S) == re.findall(cover, after, re.S),
          "Cover changed")
    for pattern in (r'<link rel="(?:canonical|alternate)"[^>]*>',
                    r'<meta\b[^>]*>', r'<img\b[^>]*>'):
        check(re.findall(pattern, before) == re.findall(pattern, after),
              "Protected SEO/cover metadata changed")
    older, newer = schemas(before), schemas(after)
    check(set(older) == {"Article", "BreadcrumbList"}, "Legacy schema changed")
    check(set(newer) == {"Article", "BreadcrumbList", "FAQPage"}, "Required schemas missing")
    check(older["BreadcrumbList"] == newer["BreadcrumbList"], "Breadcrumb facts changed")
    a, b = dict(older["Article"]), dict(newer["Article"])
    check(a.pop("dateModified") == "2026-09-24" and
          b.pop("dateModified") == "2026-11-05" and a == b,
          "Original Article facts changed")
    for token in ("international-atlas.css", "international-marx.css",
                  "international-atlas.js", "atlas-main", "atlas-guide-opening",
                  "atlas-reader", "atlas-contents", "atlas-reading"):
        check(token in after, "Missing required template asset: " + token)
    check((ROOT / "assets/international-marx.css").is_file(), "Scoped CSS missing")
    check("<details open>" in after, "No-JS TOC must be visible")
    ids = re.findall(r'\bid="([^"]+)"', after)
    check(len(ids) == len(set(ids)), "Duplicate IDs")
    required = {"introduction", "orientation", "life", "commodity", "alienated-labor", "capital", "history", "wound", "atlas-desk", "works", "ideas", "faq", "sources"}
    check(required.issubset(ids), "Original anchor removed")
    check(all(target in ids for target in re.findall(r'href="#([^"]+)"', after)),
          "Broken internal fragment")
    toc = re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>', after, re.S)
    check(toc is not None, "Missing guide TOC")
    toc_ids = re.findall(r'href="#([^"]+)"', toc.group(1))
    article_ids = re.findall(r'<article class="item guide-section[^"]*" id="([^"]+)"', after)
    check(toc_ids == article_ids and len(toc_ids) == len(set(toc_ids)),
          "Contents order/target mismatch")
    match = re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">', after, re.S)
    check(match is not None, "Static body / citation missing")
    expected, actual = words(manuscript_body(source)), words(txt(match.group(1)))
    check(expected == actual, "Source/HTML text mismatch, expected %s actual %s" %
          (len(expected), len(actual)))
    check(after.count('class="marx-table"') == 2, "Approved tables missing")
    check('class="marx-receipt"' in after and after.count('class="marx-receipt-stage"') == 4, "Receipt and 4 stages missing")
    check("What the reverse does—and does not—show." in after, "Receipt interpretive qualification missing")
    check(len(article_ids) == 21, "Expected 21 manuscript sections")
    check('role="region"' in after and 'tabindex="0"' in after,
          "Responsive tables inaccessible to keyboard")
    # Preserve punctuation adjacency around inline emphasis in FAQ headings/answers.
    inline_text = lambda value: " ".join(unescape(re.sub(r"<[^>]*>", "", value)).split())
    pairs = [(inline_text(q), inline_text(a)) for q,a in re.findall(
        r'<section class="marx-faq"><h3>(.*?)</h3><p>(.*?)</p></section>', after, re.S)]
    faq = [(q["name"], q["acceptedAnswer"]["text"])
           for q in newer["FAQPage"]["mainEntity"]]
    check(len(pairs) == 10 and pairs == faq, "Visible/structured FAQ mismatch")
    for label, url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', source):
        check('href="' + url + '"' in after, "Manuscript link missing: " + url)
    print("PASS Marx EN 04: %d exact ordered words, %d articles, 10 FAQs, 2 accessible tables, 4 receipt stages, protected facts" %
          (len(expected), len(article_ids)))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    verify(ROOT / PAGE, args.base)
