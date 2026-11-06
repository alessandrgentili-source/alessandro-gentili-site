#!/usr/bin/env python3
"""Source-pinned Tocqueville EN17 preservation and interaction checks; editorial approval remains human."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
from itertools import zip_longest

ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/alexis-de-tocqueville-democracy-opinion-liberty/index.html'
SOURCE_COMMIT='4f70f26ee130dab2bd5088e14976f8d7ce66c490'
SOURCE_FILE='TOCQUEVILLE_EN_GUIDE_17_CANDIDATE_v1.md'
SOURCE_BLOB='df26bcd2494ce27a12467b46bd9aaa1b08accc26'
BASE_BLOB='9faa1a3a14d68ec10c59fc5f38dd3210ac552650'
URL='https://alessandro-gentili.it/en/cerchi/guides/alexis-de-tocqueville-democracy-opinion-liberty/'

def check(cond, message):
    if not cond:raise AssertionError(message)

def git(ref,path):
    return subprocess.check_output(['git','show',f'{ref}:{path}'],cwd=ROOT,text=True)

def tokens(s):
    return re.findall(r'[^\W_]+',s,re.UNICODE)

def source_tokens(raw):
    body=raw[raw.index("## A reader's route"):]
    result=[]
    for line in body.splitlines():
        line=line.strip()
        if not line or line=='---' or re.match(r'^\|\s*:?-{3,}',line):continue
        heading=bool(re.match(r'^#{2,3}\s',line))
        line=re.sub(r'^#{2,3}\s+','',line)
        if not heading:
            line=re.sub(r'^[-*]\s+','',line)
            line=re.sub(r'^\d+\.\s+','',line)
        line=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',line)
        line=line.replace('**','').replace('*','').replace('`','').replace('|',' ')
        result.append(line)
    return tokens(' '.join(result))

class Editorial(HTMLParser):
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):
        super().__init__(convert_charrefs=True);self.skip=0;self.words=[]
    def handle_starttag(self,tag,attrs):
        if self.skip:
            if tag not in self.VOID:self.skip+=1
        elif dict(attrs).get('data-tocqueville-ui')=='1':self.skip=1
    def handle_startendtag(self,tag,attrs):pass
    def handle_endtag(self,tag):
        if self.skip:self.skip-=1
    def handle_data(self,data):
        if not self.skip:self.words.append(data)

class Plain(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
    def handle_data(self,s):self.parts.append(s)
    def text(self,s):self.feed(s);return ' '.join(''.join(self.parts).split())

def visible(s):return Plain().text(s)
def ld(s):return [json.loads(x) for x in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S)]

def verify(path,base):
    check(path.resolve().relative_to(ROOT).as_posix()==PAGE,'Wrong path')
    check(subprocess.check_output(['git','rev-parse',f'{base}:{PAGE}'],cwd=ROOT,text=True).strip()==BASE_BLOB,'Legacy baseline changed')
    source_rev=subprocess.run(['git','rev-parse',f'{SOURCE_COMMIT}:{SOURCE_FILE}'],cwd=ROOT,text=True,capture_output=True)
    if source_rev.returncode:
        subprocess.run(['git','fetch','--no-tags','origin',SOURCE_COMMIT],cwd=ROOT,check=True)
        source_rev=subprocess.run(['git','rev-parse',f'{SOURCE_COMMIT}:{SOURCE_FILE}'],cwd=ROOT,text=True,capture_output=True,check=True)
    check(source_rev.stdout.strip()==SOURCE_BLOB,'Source blob changed')
    raw=git(SOURCE_COMMIT,SOURCE_FILE)
    original=git(base,PAGE)
    html=path.read_text(encoding='utf8')
    check(html.startswith('<!doctype html>') and html.rstrip().endswith('</html>'),'HTML framing')
    check('<body class="guide-page international-atlas atlas-guide atlas-tocqueville">' in html,'Plato Atlas layout missing')
    check(html.count('<h1>Alexis de Tocqueville</h1>')==1,'One author H1 only')
    check('atlas-contents' in html and 'atlas-breadcrumb' in html,'Accessible contents missing')
    for name in ['international-atlas.css','international-atlas.js','international-tocqueville.css','international-tocqueville.js','/assets/script.js']:
        check(name in html,'Missing asset '+name)
    for name in ['assets/international-tocqueville.css','assets/international-tocqueville.js']:
        check((ROOT/name).is_file(),'Missing artifact '+name)
    for kind in ('title','meta'):
        rx=rf'<{kind}\b[^>]*?(?:/>|</{kind}>)'
        check(re.findall(rx,original,re.S)==re.findall(rx,html,re.S),'Metadata changed: '+kind)
    old_links=re.findall(r'<link\b[^>]*>',original)
    new_links=[x for x in re.findall(r'<link\b[^>]*>',html) if 'international-atlas.css' not in x and 'international-tocqueville.css' not in x]
    check(old_links==new_links,'Canonical/hreflang changed')
    for pat in (r'<header class="site-header".*?</header>',r'<footer class="footer".*?</footer>',r'<figure class="editorial-cover-card guide-cover".*?</figure>'):
        a,b=re.search(pat,original,re.S),re.search(pat,html,re.S)
        check(a is not None and b is not None and a.group()==b.group(),'Site chrome or cover changed')
    pre,post=ld(original),ld(html)
    check(len(pre)==2 and len(post)==3,'JSON-LD count')
    aa,bb=dict(pre[0]),dict(post[0]);check(aa.pop('dateModified')=='2026-09-24' and bb.pop('dateModified')=='2026-11-06' and aa==bb,'Article facts drift')
    check(pre[1]==post[1],'Breadcrumb facts drift')
    check(post[2].get('@type')=='FAQPage' and post[2].get('@id')==URL+'#faq','FAQPage identity')
    pairs=[(visible(q),visible(a)) for q,a in re.findall(r'<section class="tocqueville-faq"><h4>(.*?)</h4><p>(.*?)</p></section>',html,re.S)]
    structured=[(x['name'],x['acceptedAnswer']['text']) for x in post[2]['mainEntity']]
    check(len(pairs)==20 and pairs==structured,'20 visible FAQ differ from schema')
    ids=re.findall(r'\bid="([^"]+)"',html)
    check(len(ids)==len(set(ids)),'Duplicate IDs')
    check(set(re.findall(r'\bid="([^"]+)"',original)).issubset(ids),'Lost historic anchors')
    anchors=re.findall(r'<article class="item guide-section tocqueville-section(?: tocqueville-section--major)?" id="([^"]+)"',html)
    toc=re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',html,re.S)
    check(len(anchors)==36 and toc is not None,'36 article sections missing')
    check(re.findall(r'href="#([^"]+)"',toc.group(1))==anchors,'TOC mismatch')
    for href in re.findall(r'\[[^\]]+\]\((https?://[^)]+)\)',raw):check(f'href="{href}"' in html,'Approved link lost')
    body=re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">',html,re.S)
    check(body is not None,'No source body')
    parser=Editorial();parser.feed(body.group(1))
    actual,expected=tokens(' '.join(parser.words)),source_tokens(raw)
    if actual!=expected:
        i=next((i for i,(a,b) in enumerate(zip_longest(expected,actual)) if a!=b),-1)
        raise AssertionError(f'Editorial source drift at {i}: {len(expected)} vs {len(actual)} tokens, {expected[i:i+6]!r} vs {actual[i:i+6]!r}')
    check(len(actual)==12423,'Unexpected manuscript token count')
    check(len(re.findall(r'<section class="tocqueville-interval-step tocqueville-interval-step-\d"',html))==5,'Five civic interval movements')
    check(len(re.findall(r'<tr\b[^>]*data-original-index="\d+"',re.search(r'<table[^>]*id="tocqueville-life-table"[^>]*>.*?</table>',html,re.S).group(0)))==12,'12 life rows')
    check(len(re.findall(r'<tr\b[^>]*data-original-index="\d+"',re.search(r'<table[^>]*id="tocqueville-glossary-table"[^>]*>.*?</table>',html,re.S).group(0)))==18,'18 glossary rows')
    check('id="tocqueville-interval-0"' in html and 'name="tocqueville-interval"' in html,'Native radio selector missing')
    check('data-tocqueville-ui="1" hidden' in html,'Progressive controls must be hidden without JS')
    css=(ROOT/'assets/international-tocqueville.css').read_text(encoding='utf8')
    js=(ROOT/'assets/international-tocqueville.js').read_text(encoding='utf8')
    for item in ('@media print','tbody tr[hidden]','focus-visible','min-height:44px'):
        check(item in css,'Missing CSS '+item)
    for item in ('beforeprint','afterprint','appendChild','addEventListener','controls.hidden = false','query.focus()'):
        check(item in js,'Missing interaction '+item)
    subprocess.run(['node','--check',str(ROOT/'assets/international-tocqueville.js')],cwd=ROOT,check=True)
    # Behavior test uses actual JavaScript, a deterministic DOM fixture and simulated events.
    subprocess.run(['node','tools/test-tocqueville-interaction.cjs'],cwd=ROOT,check=True)
    print('PASS Tocqueville EN17: 12423 source tokens; 36 sections; 20 visible/schema FAQ; 12+18 interactive rows; 5 interval views; SEO/chrome/cover locked')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--base',required=True)
    verify(ROOT/PAGE,ap.parse_args().base)
