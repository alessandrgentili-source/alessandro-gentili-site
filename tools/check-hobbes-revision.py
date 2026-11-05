#!/usr/bin/env python3
"""Pinned source-and-metadata contract for approved Hobbes EN 12 v1 only."""
from pathlib import Path
import re, json, subprocess, hashlib, runpy
from html import unescape

ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/thomas-hobbes-fear-sovereignty-political-order/index.html'
SOURCE_COMMIT='336aaa081a133327cd66ca2f5b58ec9efd9e4b4c'
SOURCE_FILE='HOBBES_EN_GUIDE_12_CANDIDATE_v1.md'
SOURCE_HASH='bb177f1f69cfd509079365b6a790f8964520ef46611000ff6f3823d0f25f6ba6'
BASE_BLOB='b122ca50e2b3b119dab085a3a4225c2514f5175a'
MODIFIED='2026-11-06'

def ck(x,msg):
    if not x:raise AssertionError(msg)
def git(ref,path):
    return subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT).decode('utf-8')
def tok(s):return re.findall(r'[^\W_]+',s,re.UNICODE)
def source_body(s):
    s=s[s.index("## A reader's route"):]
    parts=[]
    for line in s.splitlines():
        l=line.strip()
        if not l or l=='---' or re.fullmatch(r'\|[\s:|\-]+\|',l):continue
        if l.startswith('|'):
            parts.extend(x.strip() for x in l.strip('|').split('|'))
            continue
        heading=l.startswith('##')
        l=re.sub(r'^#{2,3}\s+','',l)
        l=re.sub(r'^[-*]\s+','',l)
        if not heading:l=re.sub(r'^\d+\.\s+','',l)
        l=re.sub(r'^\*\*\d+\.\s+','**',l)
        parts.append(l)
    s=' '.join(parts)
    s=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s)
    return re.sub(r'\*\*|\*|`','',s)
def html_body(s):
    s=re.sub(r'<(?P<tag>div|legend|label|figcaption)\b[^>]*data-hobbes-ui="1"[^>]*>.*?</(?P=tag)>','',s,flags=re.S)
    # Numbered question labels are rendered as headings, without the source's list numbers.
    s=re.sub(r'<strong>([1-4])\.\s+', '<strong>',s)
    s=re.sub(r'</(?:h[1-6]|p|li|th|td|tr|blockquote)>',' ',s)
    return unescape(re.sub(r'<[^>]+>',' ',s))
def schema(s):
    objs=[json.loads(x) for x in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S)]
    ck(len(objs)==len({x['@type'] for x in objs}),'Duplicate JSON-LD types')
    return {x['@type']:x for x in objs}
def visible(s):return ' '.join(unescape(re.sub(r'<[^>]*>','',s)).split())
def verify(path,base):
    ck(path.resolve().relative_to(ROOT).as_posix()==PAGE,'Out of Hobbes scope')
    b=subprocess.check_output(['git','rev-parse',base+':'+PAGE],cwd=ROOT,text=True).strip()
    ck(b==BASE_BLOB,'Legacy base blob changed')
    src=git(SOURCE_COMMIT,SOURCE_FILE)
    ck(hashlib.sha256(src.encode('utf-8')).hexdigest()==SOURCE_HASH,'Approved source SHA-256 mismatch')
    before=git(base,PAGE);after=path.read_text(encoding='utf-8')
    ck('awaiting human approval' not in after and 'Editorial candidate v1' not in after,'Workflow marker leaked')
    Tree=runpy.run_path(str(ROOT/'tools/validate-cerchi-guide.py'))['Tree']
    ck(not Tree(after).malformed,'Malformed HTML tree')
    for tag in ('title','header','footer'):
        rx=rf'<{tag}\b[^>]*>.*?</{tag}>'
        ck(re.findall(rx,before,re.S)==re.findall(rx,after,re.S),'Protected '+tag+' changed')
    for rx in (r'<link rel="(?:canonical|alternate)"[^>]*>',r'<meta\b[^>]*>',r'<img\b[^>]*>'):
        ck(re.findall(rx,before)==re.findall(rx,after),'Protected SEO/cover metadata changed')
    rx=r'<figure class="editorial-cover-card guide-cover".*?</figure>'
    ck(re.findall(rx,before,re.S)==re.findall(rx,after,re.S),'Original cover changed')
    a,b=schema(before),schema(after)
    ck(set(a)=={'Article','BreadcrumbList'} and set(b)=={'Article','BreadcrumbList','FAQPage'},'Structured data types changed')
    ck(a['BreadcrumbList']==b['BreadcrumbList'],'Original breadcrumb JSON-LD changed')
    aarticle,barticle=dict(a['Article']),dict(b['Article'])
    ck(aarticle.pop('dateModified')=='2026-09-24' and barticle.pop('dateModified')==MODIFIED and aarticle==barticle,'Article facts changed')
    for t in ('international-atlas.css','international-hobbes.css','international-hobbes.js','international-atlas.js','atlas-main','atlas-guide-opening','atlas-reader','atlas-reading'):
        ck(t in after,'Required International asset missing: '+t)
    ck((ROOT/'assets/international-hobbes.css').is_file() and (ROOT/'assets/international-hobbes.js').is_file(),'Scoped assets missing')
    ck('<details open>' in after,'No-JS TOC missing')
    ids=re.findall(r'\bid="([^"]+)"',after)
    ck(len(ids)==len(set(ids)),'Duplicate IDs')
    anchors=re.findall(r'href="#([^"]+)"',after)
    ck(all(id in ids for id in anchors),'Broken page anchors')
    for prev in ('state-of-nature','fear','covenant','sovereignty','religion','not-hobbes','wound','sources'):
        ck(prev in ids,'Original public anchor missing: '+prev)
    nav=re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',after,re.S)
    ck(nav is not None,'TOC missing')
    toc=re.findall(r'href="#([^"]+)"',nav.group(1))
    articleids=re.findall(r'<article class="item guide-section[^"]*" id="([^"]+)"',after)
    ck(len(articleids)==36 and toc==articleids,'36 ordered guide sections and TOC expected')
    body=re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">',after,re.S)
    ck(body is not None,'Reading body missing')
    expected,actual=tok(source_body(src)),tok(html_body(body.group(1)))
    ck(expected==actual,'Source text changed or reordered: %d vs %d lexical tokens'%(len(expected),len(actual)))
    ck(len(actual)==11653,'Unexpected source lexical count')
    ck(after.count('class="hobbes-test-step ') ==4,'Four test steps missing')
    ck(len(re.findall(r'<tr>',after))==24,'Glossary table must have 23 rows plus header')
    ck('type="search" id="hobbes-glossary-query"' in after,'Interactive glossary search absent')
    ck('name="hobbes-test-view"' in after and 'id="hobbes-test-all"' in after,'Accessible no-JS radio views absent')
    ck('tabindex="0"' in after and 'role="region"' in after,'Responsive glossary region not keyboard accessible')
    pairs=[(visible(q),visible(a)) for q,a in re.findall(r'<section class="hobbes-faq"><h3>(.*?)</h3><p>(.*?)</p></section>',after,re.S)]
    j=[(q['name'],q['acceptedAnswer']['text']) for q in b['FAQPage']['mainEntity']]
    ck(len(pairs)==20 and pairs==j,'Visible FAQ differ from 20 JSON-LD Q/A')
    for _,url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',src):
        ck('href="'+url+'"' in after,'Approved internal link lost: '+url)
    print('PASS Hobbes EN 12: %d source-exact tokens, 36 articles, 20 FAQs, 23 searchable glossary terms, 4 radio steps; SEO/cover protected'%(len(actual)))
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--base',required=True)
    args=parser.parse_args()
    verify(ROOT/PAGE,args.base)
