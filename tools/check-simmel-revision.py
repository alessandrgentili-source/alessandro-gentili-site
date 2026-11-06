#!/usr/bin/env python3
"""Source-locked Simmel EN 14 International 3.0 check. Editorial approval remains human."""
import json,re,subprocess
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/georg-simmel-money-metropolis-individuality/index.html'
SOURCE_COMMIT='3b7446245fdcea1e5106fe9e64f783301b17d25f'
SOURCE_FILE='SIMMEL_EN_GUIDE_14_CANDIDATE_v1.md'
SOURCE_BLOB='3323fef3d68f7d76cba1e3a31c9fa521a4025570'
BASE_BLOB='6d8d10d43c48fb2107954a1ffc888c21dcf8ce8d'
URL='https://alessandro-gentili.it/en/cerchi/guides/georg-simmel-money-metropolis-individuality/'

def ck(cond,message):
    if not cond:raise AssertionError(message)
def git(ref,path):
    return subprocess.check_output(['git','show',f'{ref}:{path}'],cwd=ROOT,text=True)
def tok(s):
    return re.findall(r'[^\W_]+',s,re.UNICODE)
def source_words(md):
    body=md[md.index("## A reader's route"):]
    result=[]
    for raw in body.splitlines():
        line=raw.strip()
        if not line or line=='---':continue
        heading=bool(re.match(r'^#{2,3}\s',line))
        line=re.sub(r'^#{2,3}\s+','',line)
        if not heading:
            line=re.sub(r'^[-*]\s+','',line)
            line=re.sub(r'^\d+\.\s+','',line)
        line=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',line)
        result.append(line.replace('**','').replace('*','').replace(chr(96),''))
    return tok(' '.join(result))
class Editorial(HTMLParser):
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):
        super().__init__(convert_charrefs=True);self.skip=0;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if self.skip:
            if tag not in self.VOID:self.skip+=1
        elif dict(attrs).get('data-simmel-ui')=='1':self.skip=1
    def handle_startendtag(self,tag,attrs):
        # HTMLParser otherwise calls both callbacks for a self-closing input.
        # Neither callback should alter the skip depth of UI-only controls.
        pass
    def handle_endtag(self,tag):
        if self.skip:self.skip-=1
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)
def display(s):
    return ' '.join(unescape(re.sub(r'<[^>]+>',' ',s)).split())
def schemas(s):
    return [json.loads(x) for x in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S)]

def verify(path,base):
    ck(path.resolve().relative_to(ROOT).as_posix()==PAGE,'Wrong page')
    ck(subprocess.check_output(['git','rev-parse',f'{base}:{PAGE}'],cwd=ROOT,text=True).strip()==BASE_BLOB,'Legacy base drift')
    chk=subprocess.run(['git','rev-parse',f'{SOURCE_COMMIT}:{SOURCE_FILE}'],cwd=ROOT,text=True,capture_output=True)
    if chk.returncode:
        subprocess.run(['git','fetch','--no-tags','origin',SOURCE_COMMIT],cwd=ROOT,check=True)
        chk=subprocess.run(['git','rev-parse',f'{SOURCE_COMMIT}:{SOURCE_FILE}'],cwd=ROOT,text=True,capture_output=True,check=True)
    ck(chk.stdout.strip()==SOURCE_BLOB,'Editorial source changed')
    source=git(SOURCE_COMMIT,SOURCE_FILE)
    old=git(base,PAGE)
    html=path.read_text(encoding='utf-8')
    ck(html.startswith('<!doctype html>') and html.endswith('</html>\n'),'HTML framing')
    ck(html.count('<h1>')==1 and '<h1>Georg Simmel</h1>' in html,'Single source H1')
    ck('<body class="guide-page international-atlas atlas-guide atlas-simmel">' in html,'Atlas layout')
    ck('<details open>' in html and 'atlas-reader' in html and 'atlas-contents' in html,'Static contents missing')
    for tag in ('header','main','footer'):
        ck(len(re.findall(rf'<{tag}\b',html))==len(re.findall(rf'</{tag}>',html))==1,tag+' malformed')
    for t in ('international-atlas.css','international-simmel.css','international-atlas.js','international-simmel.js','/assets/script.js'):
        ck(t in html,'Missing asset '+t)
    for f in ('assets/international-simmel.css','assets/international-simmel.js'):
        ck((ROOT/f).is_file(),'Missing file '+f)
    for kind in ('title','meta'):
        rx=rf'<{kind}\b[^>]*?(?:/>|</{kind}>)'
        ck(re.findall(rx,old,re.S)==re.findall(rx,html,re.S),'Protected '+kind+' changed')
    orig_links=re.findall(r'<link\b[^>]*>',old)
    new_links=[x for x in re.findall(r'<link\b[^>]*>',html) if 'international-atlas.css' not in x and 'international-simmel.css' not in x]
    ck(orig_links==new_links,'Canonical/hreflang changed')
    for rx in (r'<header class="site-header".*?</header>',r'<footer class="footer".*?</footer>',r'<figure class="editorial-cover-card guide-cover".*?</figure>'):
        before=re.search(rx,old,re.S);after=re.search(rx,html,re.S)
        ck(before and after and before.group()==after.group(),'Chrome/cover changed')
    a,b=schemas(old),schemas(html)
    ck(len(a)==2 and len(b)==3,'Schema count')
    article=dict(b[0]);earlier=dict(a[0])
    ck(article.pop('dateModified')=='2026-11-06' and earlier.pop('dateModified')=='2026-09-24' and article==earlier,'Article facts')
    ck(a[1]==b[1],'Breadcrumb facts')
    ck(b[2].get('@type')=='FAQPage' and b[2].get('@id')==URL+'#faq','FAQPage identity')
    pairs=[(display(q),display(ans)) for q,ans in re.findall(r'<section class="simmel-faq"><h3>(.*?)</h3><p>(.*?)</p></section>',html,re.S)]
    structured=[(x['name'],x['acceptedAnswer']['text']) for x in b[2]['mainEntity']]
    ck(len(pairs)==20 and pairs==structured,'20 visible FAQ disagree with JSON-LD')
    ids=re.findall(r'\bid="([^"]+)"',html)
    ck(len(ids)==len(set(ids)) and set(re.findall(r'\bid="([^"]+)"',old)).issubset(ids),'Duplicate or lost legacy anchors')
    article_ids=re.findall(r'<article class="item guide-section[^"]*" id="([^"]+)"',html)
    toc=re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',html,re.S)
    ck(toc is not None and len(article_ids)==37,'37 source sections')
    ck(re.findall(r'href="#([^"]+)"',toc.group(1))==article_ids,'TOC order/anchors')
    for href in re.findall(r'\[[^\]]+\]\((https?://[^)]+)\)',source):
        ck('href="'+href+'"' in html,'Approved link lost')
    part=re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">',html,re.S)
    ck(part is not None,'Main article body')
    p=Editorial();p.feed(part.group(1))
    expected,actual=source_words(source),tok(' '.join(p.parts))
    if expected != actual:
        import itertools
        mismatch = next((i for i,(a,b) in enumerate(itertools.zip_longest(expected,actual)) if a != b), -1)
        raise AssertionError(f'Source/HTML drift: {len(expected)} vs {len(actual)} tokens, at {mismatch}: source={expected[max(0,mismatch-6):mismatch+9]!r} html={actual[max(0,mismatch-6):mismatch+9]!r}')
    ck(len(actual)==12437,'Unexpected manuscript token count')
    ck(html.count('class="simmel-step simmel-step-')==5,'Five selectable steps')
    tab=re.search(r'<table\b[^>]*id="simmel-glossary-table".*?</table>',html,re.S)
    ck(tab and len(re.findall(r'<tr\b',tab.group()))==19,'18 glossary entries')
    css=(ROOT/'assets/international-simmel.css').read_text()
    js=(ROOT/'assets/international-simmel.js').read_text()
    ck('@media print' in css and 'tr[hidden]' in css and 'beforeprint' in js,'Print fallback')
    ck('controls.hidden = false' in js and 'input.addEventListener' in js,'Live search')
    ck('name="simmel-view"' in html and 'id="simmel-view-0"' in html,'Radio comparison')
    ck('tabindex="0"' in html and 'role="region"' in html,'Keyboard scrollable table')
    print(f'PASS Simmel EN 14: {len(actual)} source tokens, 37 sections, 20 FAQ, 18 glossary terms, 5 selectable tests')

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True)
    args=ap.parse_args();verify(ROOT/PAGE,args.base)
