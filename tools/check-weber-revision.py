#!/usr/bin/env python3
"""Weber EN 09 v1 source-locked publication audit; strict, page-scoped, read-only."""
from html import unescape
from pathlib import Path
import hashlib, json, re, runpy, subprocess

ROOT = Path(__file__).resolve().parents[1]
PAGE = "en/cerchi/guides/max-weber-rationalization-power-disenchantment/index.html"
SOURCE_COMMIT = "b15fe965566d1dcbdd81f3d2efdf830f26bb4927"
SOURCE_FILE = "WEBER_EN_GUIDE_09_CANDIDATE_v1.md"
SOURCE_HASH = "d02d7c4825d789f91a906ae3a45f1cb830cac961ccd588b8e05ad439e4957bf3"
BASE_BLOB = "ccddea4fb3ebbff8f174c1aa2124af8afd11524d"

def check(v, m):
    if not v: raise AssertionError(m)

def git_text(ref, path):
    return subprocess.check_output(["git","show",ref+":"+path],cwd=ROOT).decode("utf-8")

def words(x):
    return re.findall(r"[^\W_]+",unescape(x),re.UNICODE)

def source_body(source):
    blocks=re.split(r"\n[ \t]*\n",source[source.index("## A reader's route"):].strip())
    parts=[]
    for block in blocks:
        lines=[v.strip() for v in block.strip().splitlines()]
        if block.strip()=="---": continue
        if all(v.startswith("- ") for v in lines): parts.extend(v[2:] for v in lines)
        else: parts.append(" ".join(re.sub(r"^#{2,3} ","",v) for v in lines))
    s=" ".join(parts)
    s=re.sub(r"\[([^\]]+)\]\([^)]+\)",r"\1",s)
    return re.sub(r"\*\*|\*|\x60","",s)

def html_body(page):
    m=re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">',page,re.S)
    check(m is not None,"Reading body/citation missing")
    s=m.group(1)
    s=re.sub(r'<div class="weber-glossary-search"[^>]*>.*?</div>',"",s,flags=re.S)
    s=re.sub(r'<legend>.*?</legend>',"",s,flags=re.S)
    s=re.sub(r'<label\b[^>]*>.*?</label>',"",s,flags=re.S)
    s=re.sub(r'<input\b[^>]*>',"",s)
    s=re.sub(r'</(?:h[1-6]|p|li|th|td|blockquote)>'," ",s)
    return unescape(re.sub(r"<[^>]*>","",s))

def schemas(page):
    all_data=[json.loads(v) for v in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',page,re.S)]
    check(len(all_data)==len({x["@type"] for x in all_data}),"Duplicate JSON-LD types")
    return {x["@type"]:x for x in all_data}

def verify(path,base):
    check(path.resolve().relative_to(ROOT).as_posix()==PAGE,"Wrong target page")
    blob=subprocess.check_output(["git","rev-parse",base+":"+PAGE],cwd=ROOT,text=True).strip()
    check(blob==BASE_BLOB,"Legacy EN page changed from inspected baseline")
    source=git_text(SOURCE_COMMIT,SOURCE_FILE)
    check(hashlib.sha256(source.encode("utf-8")).hexdigest()==SOURCE_HASH,"Approved manuscript SHA differs")
    before,after=git_text(base,PAGE),path.read_text(encoding="utf-8")
    Tree=runpy.run_path(str(ROOT/"tools/validate-cerchi-guide.py"))["Tree"]
    check(not Tree(after).malformed,"Malformed HTML structure")
    for tag in ("title","header","footer"):
        rx=rf"<{tag}\b[^>]*>.*?</{tag}>"
        check(re.findall(rx,before,re.S)==re.findall(rx,after,re.S),"Protected "+tag+" changed")
    for rx in (r'<link rel="(?:canonical|alternate)"[^>]*>',r'<meta\b[^>]*>',r'<img\b[^>]*>',r'<figure class="editorial-cover-card guide-cover".*?</figure>'):
        check(re.findall(rx,before,re.S)==re.findall(rx,after,re.S),"Protected SEO/cover changed")
    old,new=schemas(before),schemas(after)
    check(set(old)=={"Article","BreadcrumbList"} and set(new)=={"Article","BreadcrumbList","FAQPage"},"Required JSON-LD missing")
    check(old["BreadcrumbList"]==new["BreadcrumbList"],"Breadcrumb JSON-LD changed")
    a,b=dict(old["Article"]),dict(new["Article"])
    check(a.pop("dateModified")=="2026-09-24" and b.pop("dateModified")=="2026-11-05" and a==b,"Article facts altered")
    check(after.count("<h1>")==1 and "<h1>Max Weber</h1>" in after,"Approved title missing")
    for a in ("international-atlas.css","international-weber.css","international-atlas.js","international-weber.js","atlas-main","atlas-reader","atlas-reading","atlas-guide-opening"):
        check(a in after,"Asset/template missing: "+a)
    check((ROOT/"assets/international-weber.css").is_file() and (ROOT/"assets/international-weber.js").is_file(),"Scoped assets missing")
    check("<details open>" in after,"TOC not accessible without JS")
    ids=re.findall(r'\bid="([^"]+)"',after)
    check(len(ids)==len(set(ids)),"Duplicate ids")
    check(all(x in ids for x in re.findall(r'href="#([^"]+)"',after)),"Broken in-page link")
    check({"introduction","rationalization","disenchantment","bureaucracy","domination","responsibility","values","wound","sources"}.issubset(set(ids)),"Legacy anchor missing")
    toc=re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',after,re.S)
    check(toc is not None,"TOC missing")
    ids_toc=re.findall(r'href="#([^"]+)"',toc.group(1))
    articles=re.findall(r'<article class="item guide-section[^\"]*" id="([^"]+)"',after)
    check(len(articles)==36 and ids_toc==articles,"TOC does not match 36 sections")
    original,converted=words(source_body(source)),words(html_body(after))
    if original!=converted:
        i=next((i for i,(x,y) in enumerate(zip(original,converted)) if x!=y),min(len(original),len(converted)))
        raise AssertionError(f"Source fidelity mismatch at {i}: {len(original)}/{len(converted)} source={original[max(0,i-5):i+5]} html={converted[max(0,i-5):i+5]}")
    check(len(original)>11000,"Manuscript shorter than expected")
    check(after.count('type="radio" name="weber-view"')==6,"Six interactive radio views missing")
    check(after.count('class="weber-panel weber-panel--')==5,"Five original stages missing")
    for key in ("act","rule","office","person","judgment"):
        check('data-phase="'+key+'"' in after,"Interactive state "+key+" absent")
    check("This instrument has limits." in after,"Instrument caveat missing")
    check(after.count('class="weber-glossary-term"')==24,"Missing 24 glossary entries")
    check('weber-glossary-search" hidden' in after,"No-JS glossary fallback not present")
    def visible(x): return " ".join(unescape(re.sub(r"<[^>]*>","",x)).split())
    qa=[]
    for q,ans in re.findall(r'<section class="weber-faq"><h3>(.*?)</h3><p>(.*?)</p></section>',after,re.S):
        q=re.sub(r'<span class="weber-faq-number"[^>]*>.*?</span>',"",q,flags=re.S)
        qa.append((visible(q),visible(ans)))
    faqs=[(q["name"],q["acceptedAnswer"]["text"]) for q in new["FAQPage"]["mainEntity"]]
    check(len(qa)==20 and qa==faqs,"20 visible FAQs do not match FAQPage JSON-LD")
    for _,url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',source):
        check('href="'+url+'"' in after,"Approved source link absent: "+url)
    print(f"PASS Weber EN 09: {len(original)} original ordered tokens, 36 sections, 20 FAQs, 5 interactive stages, 24 searchable glossary entries, protected metadata")

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--base",required=True)
    a=p.parse_args();verify(ROOT/PAGE,a.base)
