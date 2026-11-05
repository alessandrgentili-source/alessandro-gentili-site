#!/usr/bin/env python3
"""Strict source and metadata contract for Freud EN 10 only."""
import hashlib,json,re,runpy,subprocess
from html import unescape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/sigmund-freud-unconscious-desire-civilization/index.html'
SOURCE_COMMIT='dd3d04cebb099f8904ba9316ab0f1118328edd84'
SOURCE_FILE='FREUD_EN_GUIDE_10_CANDIDATE_v1.md'
SOURCE_HASH='b660e74834625ff263217c1c9c5b642137642b1fd34615a618222a7718247b34'
BASE_BLOB='cdd7327c18ebec62c6f801db7f34c23efc8f0057'
def check(ok,msg):
    if not ok:raise AssertionError(msg)
def git(ref,p):
    return subprocess.check_output(['git','show',ref+':'+p],cwd=ROOT).decode('utf-8')
def toks(s):return re.findall(r'[^\W_]+',s,re.UNICODE)
def source_body(s):
    out=[]
    for line in s[s.index("## A reader's route"):].splitlines():
        l=line.strip()
        if not l or l=='---' or re.fullmatch(r'\|[\s:|\-]+\|',l):continue
        l=re.sub(r'^#{1,3}\s+','',l)
        if re.match(r'^\s*\d+\.\s+',line):l=re.sub(r'^\d+\.\s+','',l)
        l=re.sub(r'^[-*]\s+','',l)
        l=re.sub(r'^>\s*','',l)
        l=l.strip('|') if l.startswith('|') else l
        if line.strip().startswith('|'):out.extend(x.strip() for x in l.split('|'))
        else:out.append(l)
    v=' '.join(out)
    v=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',v)
    return re.sub(r'\*\*|\*','',v).replace(chr(96),'')
def visible_body(s):
    s=re.sub(r'<fieldset\b.*?</fieldset>','',s,flags=re.S)
    s=re.sub(r'<div class="freud-glossary-controls">.*?</div>','',s,flags=re.S)
    s=re.sub(r'</(?:h[1-6]|p|li|td|th|blockquote|tr|section|article)>',' ',s)
    return unescape(re.sub(r'<[^>]*>','',s))
def schemas(s):
    v=[json.loads(x) for x in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S)]
    check(len(v)==len({x['@type'] for x in v}),'Duplicate structured data')
    return {x['@type']:x for x in v}
def verify(path,base):
    check(path.resolve().relative_to(ROOT).as_posix()==PAGE,'Unrelated guide')
    blob=subprocess.check_output(['git','rev-parse',base+':'+PAGE],cwd=ROOT,text=True).strip()
    check(blob==BASE_BLOB,'Source page baseline changed')
    source=git(SOURCE_COMMIT,SOURCE_FILE)
    check(hashlib.sha256(source.encode()).hexdigest()==SOURCE_HASH,'Editorial manuscript changed')
    old,new=git(base,PAGE),path.read_text(encoding='utf-8')
    Tree=runpy.run_path(str(ROOT/'tools/validate-cerchi-guide.py'))['Tree']
    check(not Tree(new).malformed,'Malformed HTML')
    check('Editorial candidate' not in new and 'awaiting human approval' not in new,'Workflow disclaimer leaked')
    for tag in ['title','header','footer']:
        rx=rf'<{tag}\b[^>]*>.*?</{tag}>'
        check(re.findall(rx,old,re.S)==re.findall(rx,new,re.S),'Protected '+tag+' changed')
    for rx in [r'<link rel="(?:canonical|alternate)"[^>]*>',r'<meta\b[^>]*>',r'<img\b[^>]*>',r'<figure class="editorial-cover-card guide-cover".*?</figure>']:
        check(re.findall(rx,old,re.S)==re.findall(rx,new,re.S),'SEO or cover changed')
    prior,now=schemas(old),schemas(new)
    check(set(prior)=={'Article','BreadcrumbList'} and set(now)=={'Article','BreadcrumbList','FAQPage'},'Unexpected schemas')
    check(prior['BreadcrumbList']==now['BreadcrumbList'],'Breadcrumb facts changed')
    a,c=dict(prior['Article']),dict(now['Article'])
    check(a.pop('dateModified')=='2026-09-24' and c.pop('dateModified')=='2026-11-05' and a==c,'Article facts changed')
    check(new.count('<h1')==1 and '<h1>Sigmund Freud</h1>' in new,'Wrong H1')
    for term in ['international-atlas.css','international-freud.css','international-atlas.js','international-freud.js','atlas-reader','atlas-contents','atlas-reading']:
        check(term in new,'Missing atlas component '+term)
    check((ROOT/'assets/international-freud.css').is_file() and (ROOT/'assets/international-freud.js').is_file(),'Required assets missing')
    ids=re.findall(r'\bid="([^"]+)"',new)
    check(len(ids)==len(set(ids)) and all(x in ids for x in re.findall(r'href="#([^"]+)"',new)),'Duplicate or broken anchor')
    toc=re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',new,re.S)
    check(toc is not None and '<details open>' in new,'No-JS TOC missing')
    toc_ids=re.findall(r'href="#([^"]+)"',toc.group(1))
    article_ids=re.findall(r'<article class="item guide-section[^\"]*" id="([^"]+)"',new)
    check(len(article_ids)==36 and toc_ids==article_ids,'Section TOC order mismatch')
    part=re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">',new,re.S)
    check(part is not None,'Reader text missing')
    before=toks(source_body(source));after=toks(visible_body(part.group(1)))
    check(len(before)==10865 and before==after,'Manuscript words altered/omitted/reordered')
    check(len(re.findall(r'<tr data-era="(?:early|later)"',new))==8,'Timeline incomplete')
    check(new.count('class="freud-phase"')==5,'Interpretive instrument incomplete')
    check(new.count('<table')==2 and new.count('class="freud-glossary-widget"')==1,'Interactive source tables absent')
    check('id="freud-glossary-query"' in new,'Progressive search missing')
    def plain(v):return ' '.join(unescape(re.sub(r'<[^>]*>','',v)).split())
    pairs=[(plain(q),plain(a)) for q,a in re.findall(r'<section class="freud-faq"><h3>(.*?)</h3><p>(.*?)</p></section>',new,re.S)]
    faq=[(x['name'],x['acceptedAnswer']['text']) for x in now['FAQPage']['mainEntity']]
    check(len(pairs)==20 and pairs==faq,'20 FAQ content/order mismatch')
    for label,url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',source):
        check('href="'+url+'"' in new,'Approved link missing '+url)
    print(f'PASS Freud EN 10: {len(after)} source tokens, 36 articles, 20 exact FAQ, two tables, five-stage instrument')
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--base',required=True)
    args=p.parse_args();verify(ROOT/PAGE,args.base)
