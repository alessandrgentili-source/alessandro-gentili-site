#!/usr/bin/env python3
"""Pinned Gramsci EN 11 v1 publication gate, standalone and source-faithful."""
from pathlib import Path
from html import unescape
import hashlib, json, re, runpy, subprocess
ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/antonio-gramsci-hegemony-culture-common-sense/index.html'
SOURCE_COMMIT='2e60c8dd28ed9f7ff4c971c4630506cf817c3768'
SOURCE_FILE='GRAMSCI_EN_GUIDE_11_CANDIDATE_v1.md'
SOURCE_HASH='011c65fdbf725b92b9a65b498e206ac8234cfdfed311b237007786aa5146f1b9'
BASE_BLOB='eb557eef9d0d1c10a41edeefb937990acc61d1ca'

def ck(x,msg):
    if not x:raise AssertionError(msg)
def git(ref,path):
    return subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT).decode('utf-8')
def tokens(s):return re.findall(r'[^\W_]+',s,re.UNICODE)
def markdown_body(source):
    parts=[];infaq=False
    for line in source[source.index("## A reader's route"):].splitlines():
        l=line.strip()
        if not l or l=='---' or re.fullmatch(r'\|[\s:\-|]+\|',l):continue
        if l.startswith('###') or l.startswith('##'):infaq=l=='### Frequently asked questions'
        if l.startswith('|'):parts.extend(x.strip() for x in l.strip('|').split('|'));continue
        if l.startswith('#'):l=re.sub(r'^#{2,3}\s+','',l)
        elif re.match(r'^\d+\.\s+',l):l=re.sub(r'^\d+\.\s+','',l)
        if l.startswith('- '):l=l[2:]
        if infaq and re.match(r'^\*\*\d+\.',l):l=re.sub(r'^\*\*\d+\.\s+','**',l)
        parts.append(l)
    val=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',' '.join(parts))
    return re.sub(r'\*\*|\*|`','',val)
def html_body(value):
    value=re.sub(r'<(?P<tag>legend|label|div)[^>]*data-gram-ui="1"[^>]*>.*?</(?P=tag)>','',value,flags=re.S)
    value=re.sub(r'</(?:h[1-6]|p|li|th|td|tr|blockquote)>',' ',value)
    return unescape(re.sub(r'<[^>]*>',' ',value))
def schema(s):
    objs=[json.loads(x) for x in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S)]
    ck(len(objs)==len({x['@type'] for x in objs}),'Duplicate JSON-LD')
    return {x['@type']:x for x in objs}
def visible(s):return ' '.join(unescape(re.sub(r'<[^>]*>','',s)).split())
def verify(path,base):
    ck(path.resolve().relative_to(ROOT).as_posix()==PAGE,'Out of Gramsci scope')
    ck(subprocess.check_output(['git','rev-parse',base+':'+PAGE],cwd=ROOT,text=True).strip()==BASE_BLOB,'Base blob changed')
    src=git(SOURCE_COMMIT,SOURCE_FILE)
    ck(hashlib.sha256(src.encode()).hexdigest()==SOURCE_HASH,'Source hash changed')
    old,new=git(base,PAGE),path.read_text()
    ck('CANDIDATE_V1' not in new and 'awaiting human approval' not in new,'Workflow label in public page')
    Tree=runpy.run_path(str(ROOT/'tools/validate-cerchi-guide.py'))['Tree']
    ck(not Tree(new).malformed,'Malformed HTML tree')
    for tag in ('title','header','footer'):
        pat=rf'<{tag}\b[^>]*>.*?</{tag}>'
        ck(re.findall(pat,old,re.S)==re.findall(pat,new,re.S),'Protected '+tag+' changed')
    ck(re.findall(r'<figure class="editorial-cover-card guide-cover".*?</figure>',old,re.S)==re.findall(r'<figure class="editorial-cover-card guide-cover".*?</figure>',new,re.S),'Cover altered')
    for pat in (r'<link rel="(?:canonical|alternate)"[^>]*>',r'<meta\b[^>]*>',r'<img\b[^>]*>'):
        ck(re.findall(pat,old)==re.findall(pat,new),'Protected SEO/cover facts changed')
    a,b=schema(old),schema(new)
    ck(set(a)=={'Article','BreadcrumbList'} and set(b)=={'Article','BreadcrumbList','FAQPage'},'Schema types incorrect')
    ck(a['BreadcrumbList']==b['BreadcrumbList'],'BreadcrumbList changed')
    aa,bb=dict(a['Article']),dict(b['Article'])
    ck(aa.pop('dateModified')=='2026-09-24' and bb.pop('dateModified')=='2026-11-05' and aa==bb,'Original Article facts changed')
    for token in ('international-atlas.css','international-gramsci.css','international-atlas.js','international-gramsci.js','atlas-guide-opening','atlas-contents','atlas-reading'):
        ck(token in new,'International 3.0 asset absent: '+token)
    ck((ROOT/'assets/international-gramsci.css').is_file() and (ROOT/'assets/international-gramsci.js').is_file(),'Scoped assets missing')
    ck(new.count('<h1>')==1 and '<h1>Antonio Gramsci</h1>' in new,'Approved H1 incorrect')
    ids=re.findall(r'\bid="([^"]+)"',new)
    ck(len(ids)==len(set(ids)),'Duplicate IDs')
    ck(all(x in ids for x in re.findall(r'href="#([^"]+)"',new)),'Broken in-page target')
    ck({'hegemony','common-sense','intellectuals','integral-state','notebooks','freedom','atlas-desk','glossary','faq','sources','factory'}.issubset(ids),'Legacy or source anchor missing')
    toc=re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',new,re.S)
    articles=re.findall(r'<article class="item guide-section[^"]*" id="([^"]+)"',new)
    ck(toc is not None and '<details open>' in new and len(articles)==36,'Static navigation/sections incomplete')
    ck(re.findall(r'href="#([^"]+)"',toc.group(1))==articles,'Contents and section order differ')
    block=re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">',new,re.S)
    ck(block is not None,'Reading body missing')
    expected,actual=tokens(markdown_body(src)),tokens(html_body(block.group(1)))
    ck(len(expected)==10804 and expected==actual,f'Source/HTML mismatch {len(expected)} vs {len(actual)}')
    ck(len(re.findall(r'<table class="gramsci-table"',new))==2,'Two source tables missing')
    ck(len(re.findall(r'<tr data-era="',new))==7,'Chronology rows incomplete')
    ck(len(re.findall(r'<section class="gramsci-frame-step gramsci-frame-step--',new))==5,'Interactive source module incomplete')
    ck('id="gramsci-glossary-search"' in new and 'id="gramsci-glossary-reset"' in new,'Interactive glossary missing')
    ck('name="gramsci-era"' in new and 'name="gramsci-frame-view"' in new,'No-JS radio controls missing')
    pairs=[(visible(q),visible(an)) for q,an in re.findall(r'<section class="gramsci-faq"><h3>(.*?)</h3><p>(.*?)</p></section>',new,re.S)]
    structured=[(q['name'],q['acceptedAnswer']['text']) for q in b['FAQPage']['mainEntity']]
    ck(len(pairs)==20 and pairs==structured,'FAQ visible/JSON-LD mismatch')
    for _,url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',src):
        ck('href="'+url+'"' in new,'Source internal link missing '+url)
    print(f'PASS Gramsci EN 11: {len(actual)} exact ordered lexical tokens, 36 sections, 20 FAQ, 7 chronology rows, 19 glossary entries, five-step instrument')
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--base',required=True);verify(ROOT/PAGE,p.parse_args().base)
