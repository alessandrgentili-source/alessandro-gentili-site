#!/usr/bin/env python3
"""Strict single-guide Nietzsche EN 05 v1 source and publication contract."""
import hashlib, json, re, runpy, subprocess
from pathlib import Path
from html import unescape

ROOT=Path(__file__).resolve().parents[1]
PAGE="en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/index.html"
SOURCE_COMMIT="84b6796490e2f0dd466620cf31885cc98c27d707"
SOURCE="NIETZSCHE_EN_GUIDE_05_CANDIDATE_v1.md"
SOURCE_SHA256="ad3474f6e660daa93b2dd643fb583ca321dfcf0a9ec43854879574ba77d4401d"
BASE_BLOB="b931563eb49dda77144032583f0f997eced1f380"

def check(ok, message):
    if not ok: raise AssertionError(message)

def git_text(ref,path):
    return subprocess.check_output(["git","show",f"{ref}:{path}"],cwd=ROOT).decode("utf-8")

def words(t): return re.findall(r"[^\W_]+",t,re.UNICODE)

def source_words(source):
    source=re.sub(r"\n(?=#{2,4} )","\n\n",source)
    parts=[]
    for raw in re.split(r"\n[ \t]*\n",source.strip())[4:]:
        x=raw.strip()
        if x=="---": continue
        lines=x.splitlines()
        if len(lines)==1 and re.match(r"^#{2,4} ",x):
            label=re.sub(r"^#{2,4} ","",x)
            if x.startswith("#### "): label=re.sub(r"^\d+\.\s+","",label)
            parts.append(label)
        elif all(l.startswith("|") for l in lines):
            for l in lines:
                cells=[c.strip() for c in l.strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?",c) for c in cells): parts.extend(cells)
        elif all(l.startswith("- ") for l in lines):
            parts.extend(l[2:] for l in lines)
        elif all(re.match(r"^\d+\.\s",l) for l in lines):
            parts.extend(re.sub(r"^\d+\.\s","",l) for l in lines)
        else: parts.append(" ".join(l.strip() for l in lines))
    t=re.sub(r"\[([^\]]+)\]\([^)]+\)",r"\1"," ".join(parts))
    return words(re.sub(r"\*\*|\*|\x60","",t))

def body_words(body):
    body=re.sub(r'<span class="nietzsche-cell-label" aria-hidden="true">.*?</span>',"",body,flags=re.S)
    body=re.sub(r'<span aria-hidden="true" class="nietzsche-faq-number">.*?</span>',"",body,flags=re.S)
    body=re.sub(r"</(?:h2|h3|p|li|td|th|blockquote|summary)>"," ",body)
    return words(unescape(re.sub(r"<[^>]*>","",body)))

def jsonld(s):
    objs=[json.loads(x) for x in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S)]
    check(len(objs)==len({x["@type"] for x in objs}),"Duplicate JSON-LD types")
    return {x["@type"]:x for x in objs}

def verify(path,base):
    relative=path.resolve().relative_to(ROOT).as_posix()
    check(relative==PAGE,"Only Nietzsche EN 05 authorized")
    oldsha=subprocess.check_output(["git","rev-parse",f"{base}:{PAGE}"],cwd=ROOT,text=True).strip()
    check(oldsha==BASE_BLOB,"The expected old Nietzsche guide has changed")
    source=git_text(SOURCE_COMMIT,SOURCE)
    check(hashlib.sha256(source.encode("utf-8")).hexdigest()==SOURCE_SHA256,"Approved manuscript bytes changed")
    before,after=git_text(base,PAGE),path.read_text(encoding="utf-8")
    check(after.count("<h1>")==1 and "<h1>Friedrich Nietzsche</h1>" in after,"Approved heading missing")
    check("Editorial candidate" not in after and "not approved" not in after,"Workflow label leaked")
    Tree=runpy.run_path(str(ROOT/"tools/validate-cerchi-guide.py"))["Tree"]
    check(not Tree(after).malformed,"Malformed HTML")
    for tag in ("title","header","footer"):
        pattern=rf"<{tag}\b[^>]*>.*?</{tag}>"
        check(re.findall(pattern,before,re.S)==re.findall(pattern,after,re.S),"Protected "+tag+" changed")
    for pattern in (r'<meta\b[^>]*>',r'<link rel="(?:canonical|alternate)"[^>]*>',r'<img\b[^>]*>'):
        check(re.findall(pattern,before)==re.findall(pattern,after),"Protected metadata/URL/cover changed")
    cover=r'<figure class="editorial-cover-card guide-cover".*?</figure>'
    check(re.findall(cover,before,re.S)==re.findall(cover,after,re.S),"Cover replaced")
    o,n=jsonld(before),jsonld(after)
    check(set(o)=={"Article","BreadcrumbList"} and set(n)=={"Article","BreadcrumbList","FAQPage"},"JSON-LD schema types changed")
    check(o["BreadcrumbList"]==n["BreadcrumbList"],"Breadcrumb facts changed")
    a,b=dict(o["Article"]),dict(n["Article"])
    check(a.pop("dateModified")=="2026-09-24" and b.pop("dateModified")=="2026-11-05" and a==b,"Article metadata changed")
    for v in ("international-atlas.css","international-nietzsche.css","international-atlas.js","atlas-main","atlas-reader","atlas-reading","atlas-contents"):
        check(v in after,"International component missing "+v)
    check((ROOT/"assets/international-nietzsche.css").is_file(),"Nietzsche CSS missing")
    check("<details open>" in after,"No-JS TOC must remain open")
    ids=re.findall(r'\bid="([^"]+)"',after)
    check(len(ids)==len(set(ids)),"Duplicate IDs")
    old_ids={"introduction","orientation","death-of-god","nihilism","genealogy","recurrence-power","reception","performance","wound","sources"}
    check(old_ids.issubset(set(ids)),"Previous anchors lost")
    check(all(v in ids for v in re.findall(r'href="#([^"]+)"',after)),"Broken in-page links")
    toc=re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',after,re.S)
    check(toc is not None,"Static guide TOC missing")
    articles=re.findall(r'<article class="item guide-section[^\"]*" id="([^"]+)"',after)
    check(len(articles)==32 and re.findall(r'href="#([^"]+)"',toc.group(1))==articles,"TOC/section mapping changed")
    content=re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">',after,re.S)
    check(content is not None,"Reading body missing")
    expected,actual=source_words(source),body_words(content.group(1))
    check(expected==actual,"Manuscript word-order mismatch %s versus %s"%(len(expected),len(actual)))
    check(len(expected)==6486,"Unexpected source token count")
    check(len(re.findall(r'<table class="nietzsche-table(?: [^"]*)?"',after))==2,"Two tables not preserved")
    check('class="atlas-figure nietzsche-shadow-figure"' in after and 'nietzsche-shadow-table' in after,"Shadow test figure missing")
    check('role="region"' in after and 'tabindex="0"' in after,"Keyboard-accessible tables missing")
    def visible(t):return " ".join(unescape(re.sub(r"<[^>]*>","",t)).split())
    qas=[(visible(q),visible(a)) for q,a in re.findall(
        r'<section class="nietzsche-faq"><h3><span aria-hidden="true" class="nietzsche-faq-number">\d+\.</span>(.*?)</h3><p>(.*?)</p></section>',after,re.S)]
    schema=[(x["name"],x["acceptedAnswer"]["text"]) for x in n["FAQPage"]["mainEntity"]]
    check(len(qas)==10 and qas==schema,"FAQPage does not match visible FAQs")
    for label,url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',source):
        check('href="'+url+'"' in after,"Original link missing "+url)
    print("PASS Nietzsche EN 05: %d exact source tokens, 32 sections, 10 matched FAQs, 2 tables, unchanged SEO and cover"%len(actual))

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--base",required=True);args=p.parse_args()
    verify(ROOT/PAGE,args.base)
