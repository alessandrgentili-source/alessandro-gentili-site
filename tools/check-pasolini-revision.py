#!/usr/bin/env python3
"""Pasolini EN24: tightly scoped candidate-v3 migration protection.

This gate authorizes one checked technical replacement, not editorial approval.
The HTML is locked to the candidate snapshot; further editorial revisions must
return to Markdown and receive new review before the fingerprint is updated.
Do not use this contract to weaken the generic EN preservation validator.
"""
import argparse
from html import unescape
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAGE = "en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/index.html"
BASE_BLOB = "dabd5716b790291aa5b3d290f525c870cb520a0b"
CANDIDATE_BLOB = "3676de050bbde67208ec3d1ccf6374809fd0b870"
# For traceability only: the external v3 Markdown is NOT a source pinned in Git.
CANDIDATE_MARKDOWN_SHA256 = "1a21955fdaa6b836ec5931fb51d86606e18209f43d2ee58aba617376b59fb8d2"
URL = "https://alessandro-gentili.it/en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/"
LEGACY_LINKS = {
    "introduction": "essay-1-the-hair-that-ceased-to-dissent",
    "orientation": "pasolini-at-a-glance",
    "mutation": "essay-2-the-referendum-and-the-country-it-revealed",
    "homogenization": "essay-3-whose-language-survives",
    "things": "essay-4-what-gennariello-learns-from-things",
    "television": "essay-5-the-television-set-in-the-room",
    "limits": "limits-and-contradictions",
    "wound": "the-contemporary-wound-the-conditions-of-attention",
}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def section(pattern, source, description):
    match = re.search(pattern, source, flags=re.S)
    require(match is not None, "Missing " + description)
    return match.group(0)


def schemas(source):
    raw = re.findall(
        r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        source, re.S,
    )
    return [json.loads(s) for s in raw]


def visible(raw):
    return " ".join(unescape(re.sub(r"<[^>]+>", "", raw)).split())


def check_contract(before, after):
    require(after.startswith("<!doctype html>") and
            after.rstrip().endswith("</html>"), "Incomplete HTML document")
    for tag in ("html", "head", "body", "main", "header", "footer", "h1"):
        require(len(re.findall(rf"<{tag}\b", after)) == 1 and
                len(re.findall(rf"</{tag}>", after)) == 1,
                f"Expected one complete {tag}")
    require('<html lang="en">' in after and
            '<h1>Pier Paolo Pasolini</h1>' in after, "Wrong language or author H1")

    # Existing SEO, site chrome, cover, and scripts are immutable in this task.
    for pattern, label in (
        (r"<title>.*?</title>", "document title"),
        (r"<meta\b[^>]*>", "meta fields"),
        (r"<link\b[^>]*>", "stylesheet/canonical/alternate links"),
        (r'<header class="site-header">.*?</header>', "site header"),
        (r'<footer class="footer">.*?</footer>', "site footer"),
        (r'<figure class="editorial-cover-card guide-cover">.*?</figure>', "cover and alt"),
        (r'<script src="[^"]+"[^>]*></script>', "shared JavaScript"),
    ):
        require(re.findall(pattern, before, re.S) ==
                re.findall(pattern, after, re.S), f"Protected {label} changed")
    require('href="' + URL + '"' in after, "Existing canonical/citation link lost")
    old_schemas, new_schemas = schemas(before), schemas(after)
    require(len(old_schemas) == 2 and len(new_schemas) == 3,
            "Article/Breadcrumb/FAQ schema set must be 2 -> 3")
    old_article, new_article = dict(old_schemas[0]), dict(new_schemas[0])
    require(old_article.pop("dateModified") == "2026-09-23" and
            new_article.pop("dateModified") == "2026-11-06" and
            old_article == new_article,
            "Protected Article facts or revision date changed")
    require(old_schemas[1] == new_schemas[1],
            "BreadcrumbList changed unexpectedly")

    # Historical public links and fragment identifiers still resolve.
    old_ids = set(re.findall(r'\bid="([^"]+)"', before))
    new_ids = re.findall(r'\bid="([^"]+)"', after)
    require(len(new_ids) == len(set(new_ids)), "Duplicate HTML id")
    require(old_ids.issubset(new_ids),
            "Legacy anchor removed: " + repr(sorted(old_ids - set(new_ids))))
    for legacy, target in LEGACY_LINKS.items():
        require(re.search(
            rf'<article class="item guide-section" id="{re.escape(target)}">'
            rf'<h2 id="{re.escape(legacy)}">',
            after,
        ) is not None, "Legacy fragment no longer points to its equivalent: " + legacy)
    for href in re.findall(r'href="([^"]+)"', before):
        if not href.startswith("#"):
            require(f'href="{href}"' in after, "Historical link removed: " + href)
    for fragment in re.findall(r'href="#([^"]+)"', after):
        require(fragment in new_ids, "Broken fragment: #" + fragment)

    # Same native two-state figure, with only the two link destinations updated.
    figure_pattern = r'<figure class="atlas-figure formation-figure".*?</figure>'
    old_figure = section(figure_pattern, before, "old formation figure")
    new_figure = section(figure_pattern, after, "new formation figure")
    expected = (old_figure
                .replace('href="#television"',
                         'href="#essay-5-the-television-set-in-the-room"')
                .replace('href="#wound"',
                         'href="#the-contemporary-wound-the-conditions-of-attention"'))
    require(expected == new_figure, "Interactive figure changed beyond anchors")
    require(len(re.findall(r'type="radio"', new_figure)) == 2 and
            'id="formation-tv"' in new_figure and
            'id="formation-digital"' in new_figure,
            "Radio states missing")
    require('international-pasolini.css' in after and
            'international-atlas.js' in after,
            "Interactive stylesheet/script missing")

    # Every section is a direct child of the Atlas reader, as required by
    # the existing .atlas-reading > .guide-section styles (no new CSS).
    content = section(
        r'<div class="guide-body atlas-reading">.*?</div></div>\s*</main>',
        after, "Atlas reading body",
    )
    require('<section id="main-essay"' not in content and
            '<section id="atlas-desk"' not in content,
            "Nested sections bypass Atlas reading typography")
    article_ids = re.findall(
        r'<article class="item guide-section" id="([^"]+)">',
        content,
    )
    require(len(article_ids) == 37 and
            article_ids[0:2] == ["reader-route", "main-essay"] and
            article_ids[11] == "atlas-desk" and
            all(x.startswith("essay-") for x in article_ids[2:11]),
            "Expected route + main heading + 9 chapters + Atlas heading + 25 desk sections")
    toc = section(r'<nav class="guide-toc"[^>]*>.*?</nav>', after, "Atlas TOC")
    toc_ids = re.findall(r'href="#([^"]+)"', toc)
    require(toc_ids == article_ids, "All 37 TOC entries must mirror article order")

    faq_block = section(
        r'<article class="item guide-section" id="faq">.*?</article>',
        after, "visible FAQ",
    )
    pairs = [
        (visible(question), visible(answer))
        for question, answer in re.findall(
            r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", faq_block, re.S
        )
    ]
    faq_schema = new_schemas[2]
    require(faq_schema.get("@type") == "FAQPage" and
            len(pairs) == len(faq_schema.get("mainEntity", [])) == 20,
            "Exactly 20 visible FAQ / FAQPage required")
    machine_pairs = [
        (entry.get("name"), entry.get("acceptedAnswer", {}).get("text"))
        for entry in faq_schema["mainEntity"]
    ]
    require(pairs == machine_pairs, "Visible FAQ differs from FAQPage (text or order)")


def verify(path, base):
    require(path.resolve().relative_to(ROOT).as_posix() == PAGE,
            "Wrong path for Pasolini-specific migration")
    require(git("rev-parse", f"{base}:{PAGE}") == BASE_BLOB,
            "Pasolini baseline changed: recheck against current main")
    require(git("hash-object", str(path)) == CANDIDATE_BLOB,
            "Pasolini HTML differs from the reviewed v3 technical candidate")
    before = subprocess.check_output(
        ["git", "show", f"{base}:{PAGE}"], cwd=ROOT, text=True
    )
    after = path.read_text(encoding="utf-8")
    check_contract(before, after)
    print("PASS Pasolini EN24 candidate-v3 technical contract: "
          "37 Atlas entries, 20 visible/schema FAQ, two radio states, "
          "legacy anchors/SEO/cover protected; editorial audits still pending")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    verify(ROOT / PAGE, args.base)
