#!/usr/bin/env python3
"""Source-locked Seneca EN 07 revision. Read-only validator, no HTML generation."""
import hashlib
import json
import re
import runpy
import subprocess
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
PAGE = "en/cerchi/guides/seneca-time-self-mastery-death/index.html"
SOURCE_COMMIT = "e6dcc180cc68255a32c7ce5ff707aba0a677ee34"
SOURCE_FILE = "SENECA_EN_GUIDE_07_CANDIDATE_v1.md"
SOURCE_HASH = "d58487c9b880538b1e3d3a67bf0ef9e4407e6aa379ac497792c13cfd71ffd5d7"
ORIGINAL_BLOB = "68155fae8f74f9083ecd2a99208730f813296ce1"

def check(ok, message):
    if not ok:
        raise AssertionError(message)

def git_text(ref,path):
    return subprocess.check_output(["git","show",ref+":"+path],cwd=ROOT).decode("utf-8")

def signature(value):
    return re.findall(r"[^\W_]+", unescape(value), re.UNICODE)

def markdown_body(source):
    content = source[source.index("## A reader's route"):]
    blocks = re.split(r"\n\s*\n",content.strip())
    result=[]
    for block in blocks:
        lines=[l.strip() for l in block.strip().splitlines()]
        if block.strip()=="---":
            continue
        if all(l.startswith("|") for l in lines):
            for line in lines:
                fields=[x.strip() for x in line.strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?",x) for x in fields):
                    result.extend(fields)
        elif all(re.match(r"^\d+\. ",l) for l in lines):
            result.extend(re.sub(r"^\d+\.\s+",'',l) for l in lines)
        elif all(l.startswith("- ") for l in lines):
            result.extend(l[2:] for l in lines)
        elif all(l.startswith("> ") for l in lines):
            result.extend(l[2:] for l in lines)
        else:
            result.append(" ".join(re.sub(r"^#{2,3} ", "", l) for l in lines))
    out=" ".join(result)
    out=re.sub(r"\*\*\d+\.\s+(.+?\?)\*\*",r"**\1**",out)
    out=re.sub(r"\[([^\]]+)\]\([^)]+\)",r"\1",out)
    return re.sub(r"\*\*|\*|\x60","",out)

def html_body(page):
    match=re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">',page,re.S)
    check(match is not None,"Reading body or citation block missing")
    body=match.group(1)
    body=re.sub(r'<div class="seneca-glossary-search"[^>]*>.*?</div>',"",body,flags=re.S)
    body=re.sub(r'<h4 id="seneca-ledger-heading"[^>]*>.*?</h4>',"",body,flags=re.S)
    body=re.sub(r'<legend>.*?</legend>',"",body,flags=re.S)
    body=re.sub(r'<label\b[^>]*>.*?</label>',"",body,flags=re.S)
    body=re.sub(r'<span class="seneca-faq-number"[^>]*>.*?</span>',"",body,flags=re.S)
    body=re.sub(r'<input\b[^>]*\/?>',"",body,flags=re.S)
    body=re.sub(r"</(?:h[1-6]|p|li|th|td|blockquote)>"," ",body)
    return unescape(re.sub(r"<[^>]*>","",body))

def schemas(text):
    objs=[json.loads(v) for v in re.findall(
        r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',text,re.S)]
    check(len(objs)==len({q["@type"] for q in objs}),"Duplicate JSON-LD type")
    return {q["@type"]:q for q in objs}

def verify(path,base):
    check(path.resolve().relative_to(ROOT).as_posix()==PAGE,"Contract applies only to Seneca EN 07")
    original_blob=subprocess.check_output(["git","rev-parse",base+":"+PAGE],cwd=ROOT,text=True).strip()
    check(original_blob==ORIGINAL_BLOB,"Original Seneca page changed from baseline")
    source=git_text(SOURCE_COMMIT,SOURCE_FILE)
    check(hashlib.sha256(source.encode("utf-8")).hexdigest()==SOURCE_HASH,"Approved manuscript SHA differs")
    before,after=git_text(base,PAGE),path.read_text(encoding="utf-8")
    check("candidate v1; not approved" not in after,"Workflow notice leaked into published HTML")
    tree=runpy.run_path(str(ROOT/"tools/validate-cerchi-guide.py"))["Tree"]
    check(not tree(after).malformed,"Malformed HTML nesting")
    for tag in ("title","header","footer"):
        pat=rf"<{tag}\b[^>]*>.*?</{tag}>"
        check(re.findall(pat,before,re.S)==re.findall(pat,after,re.S),"Protected "+tag+" changed")
    for pat in (r'<link rel="(?:canonical|alternate)"[^>]*>',r'<meta\b[^>]*>',r'<img\b[^>]*>',
                r'<figure class="editorial-cover-card guide-cover".*?</figure>'):
        check(re.findall(pat,before,re.S)==re.findall(pat,after,re.S),"Canonical, metadata, image or cover changed")
    old,new=schemas(before),schemas(after)
    check(set(old)=={"Article","BreadcrumbList"} and set(new)=={"Article","BreadcrumbList","FAQPage"},"Schema types unexpected")
    check(old["BreadcrumbList"]==new["BreadcrumbList"],"Breadcrumb JSON-LD changed")
    a,b=dict(old["Article"]),dict(new["Article"])
    check(a.pop("dateModified")=="2026-09-24" and b.pop("dateModified")=="2026-11-05" and a==b,
          "Historical Article facts were changed")
    check(after.count("<h1>")==1 and "<h1>Seneca</h1>" in after,"Approved Seneca H1 altered")
    for required in ("international-atlas.css","international-seneca.css","international-seneca.js",
                     "international-atlas.js","atlas-main","atlas-reading","atlas-guide-opening","atlas-reader"):
        check(required in after,"Required shared/instrument asset missing: "+required)
    check((ROOT/"assets/international-seneca.js").is_file() and (ROOT/"assets/international-seneca.css").is_file(),"Missing scoped instrument files")
    check("<details open>" in after,"TOC must be available without JavaScript")
    ids=re.findall(r'\bid="([^"]+)"',after)
    check(len(ids)==len(set(ids)),"Duplicate IDs")
    check(all(anchor in ids for anchor in re.findall(r'href="#([^"]+)"',after)),"Broken in-page link")
    toc=re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',after,re.S)
    check(toc is not None,"No static TOC")
    links=re.findall(r'href="#([^"]+)"',toc.group(1))
    items=re.findall(r'<article class="item guide-section[^\"]*" id="([^"]+)"',after)
    check(len(items)==36 and links==items,"TOC article order/count changed")
    expect,actual=signature(markdown_body(source)),signature(html_body(after))
    if expect != actual:
        first=next((i for i,(a,b) in enumerate(zip(expect,actual)) if a!=b),min(len(expect),len(actual)))
        raise AssertionError("Source/HTML mismatch at %d, counts %d/%d, source=%r html=%r"%(first,len(expect),len(actual),expect[max(0,first-7):first+10],actual[max(0,first-7):first+10]))
    check(after.count("<table ")==1 and after.count("<tbody>")==1,"Glossary table missing or duplicated")
    gloss=re.search(r'<table class="seneca-table"[^>]*>.*?<tbody>(.*?)</tbody>',after,re.S)
    check(gloss is not None and gloss.group(1).count("<tr>")==20,"20 glossary rows not retained")
    check("data-seneca-search" in after and "data-seneca-glossary" in after,"Interactive glossary filter unavailable")
    check(after.count('type="radio" name="seneca-ledger-view"')==4,"Four native CSS ledger states missing")
    for section in ("seneca-ledger--inner","seneca-ledger--outer","seneca-ledger--together"):
        check(section in after,"Two-ledger section missing "+section)
    check("The two ledgers must be read together." in after,"Critical joint reading lost")
    def normalized(x):
        return " ".join(unescape(re.sub(r"<[^>]*>","",x)).split())
    qa=[(normalized(q),normalized(ans)) for q,ans in re.findall(
        r'<section class="seneca-faq"><h4>(.*?)</h4><p>(.*?)</p></section>',after,re.S)]
    qa=[(re.sub(r"^\d+\.\s+","",q),ans) for q,ans in qa]
    faq=[(q["name"],q["acceptedAnswer"]["text"]) for q in new["FAQPage"]["mainEntity"]]
    check(len(qa)==18 and qa==faq,"Visible FAQ and FAQPage must match 18 pairs exactly")
    for label,url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',source):
        check('href="'+url+'"' in after,"Manuscript link lost: "+url)
    print("PASS Seneca EN 07: %d ordered editorial tokens, 36 articles, 18 matching FAQ, 20 glossary terms, 4 switch states, protected metadata"%(len(expect)))

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--base",required=True)
    args=parser.parse_args()
    verify(ROOT/PAGE,args.base)
