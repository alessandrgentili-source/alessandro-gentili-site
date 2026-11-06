#!/usr/bin/env python3
"""Pareto EN21: exact-source HTML, SEO and interactive apparatus integrity; not literary approval."""
import re, json, sys, subprocess
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
from itertools import zip_longest

ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/vilfredo-pareto-elites-residues-circulation/index.html'
SOURCE_FILE='PARETO_EN_GUIDE_21_CANDIDATE_v1.md'
SOURCE_COMMIT='68a9c4b8390d4d2a04590e645aa4d26f072f060b'
SOURCE_BLOB='edca9340199887646349b7e29c2cfe9ea3085dce'
BASE_BLOB='225223aa50d3b1fc343b3a71a08afe9302834bc3'
URL='https://alessandro-gentili.it/en/cerchi/guides/vilfredo-pareto-elites-residues-circulation/'
EXPECTED=14688
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

def require(cond,msg):
    if not cond:raise AssertionError(msg)

def gitshow(ref,path):return subprocess.check_output(['git','show',f'{ref}:{path}'],cwd=ROOT,text=True)

def tokens(text):return re.findall(r'[^\W_]+',text,re.UNICODE)

def source_tokens(md):
    text=md[md.index("## A reader's route"):]
    text=re.sub(r'(?m)^\d+\.\s+','',text)
    text=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',text)
    return tokens(text)

class EditorialParser(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.inside=False;self.skip=0;self.words=[];self.sectionids=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if tag=='article' and 'pareto-section' in a.get('class','').split():
            require(not self.inside,'Nested source articles');self.inside=True;self.sectionids.append(a.get('id'))
        if not self.inside:return
        if self.skip:
            if tag not in VOID:self.skip+=1
        elif a.get('data-pareto-ui')=='1' and tag not in VOID:self.skip=1
    def handle_startendtag(self,tag,attrs):pass
    def handle_endtag(self,tag):
        if not self.inside:return
        if self.skip:self.skip-=1
        elif tag=='article':self.inside=False
    def handle_data(self,data):
        if self.inside and not self.skip:self.words.append(data)

def schemas(s):return [json.loads(x) for x in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S)]
def clean(s):return ' '.join(unescape(re.sub(r'<[^>]+>',' ',s)).split())

def verify(path,base):
    require(path.resolve().relative_to(ROOT).as_posix()==PAGE,'Wrong guide path')
    blob=subprocess.check_output(['git','rev-parse',f'{base}:{PAGE}'],cwd=ROOT,text=True).strip()
    require(blob==BASE_BLOB,'Concurrent change to previous Pareto page: STOP')
    src_blob=subprocess.run(['git','rev-parse',f'{SOURCE_COMMIT}:{SOURCE_FILE}'],cwd=ROOT,text=True,capture_output=True)
    if src_blob.returncode:
        subprocess.run(['git','fetch','--no-tags','origin',SOURCE_COMMIT],cwd=ROOT,check=True)
        src_blob=subprocess.run(['git','rev-parse',f'{SOURCE_COMMIT}:{SOURCE_FILE}'],cwd=ROOT,check=True,text=True,capture_output=True)
    require(src_blob.stdout.strip()==SOURCE_BLOB,'Source manuscript changed: STOP')
    md=gitshow(SOURCE_COMMIT,SOURCE_FILE);old=gitshow(base,PAGE);text=path.read_text('utf8')
    require(text.startswith('<!doctype html>') and text.endswith('</html>\n'),'Broken document frame')
    require(text.count('<h1>')==1 and '<h1>Vilfredo Pareto</h1>' in text,'Wrong H1')
    require('atlas-pareto' in text and 'atlas-reader' in text,'Missing Plato-aligned Atlas layout')
    for name in ('header','main','footer'):
        require(len(re.findall(rf'<{name}\b',text))==len(re.findall(rf'</{name}>',text))==1,f'Unbalanced {name}')
    for f in ('/assets/international-atlas.css','/assets/international-pareto.css','/assets/international-atlas.js','/assets/international-pareto.js','/assets/script.js'):
        require(f in text,'Missing stylesheet/script '+f)
    for f in ('assets/international-pareto.css','assets/international-pareto.js','tools/test-pareto-interaction.cjs'):
        require((ROOT/f).exists(),'Missing asset '+f)
    require(re.search(r'<title>.+?</title>',old).group()==re.search(r'<title>.+?</title>',text).group(),'Title was modified')
    for tag in ('meta',):
        require(re.findall(rf'<{tag}\b[^>]*>',old)==re.findall(rf'<{tag}\b[^>]*>',text),'SEO metadata was modified')
    original_links=re.findall(r'<link\b[^>]*>',old)
    new_links=[x for x in re.findall(r'<link\b[^>]*>',text) if 'international-atlas.css' not in x and 'international-pareto.css' not in x]
    require(original_links==new_links,'Canonical/hreflang changed')
    for rx in (r'<header class="site-header".*?</header>',r'<footer class="footer".*?</footer>',r'<figure class="editorial-cover-card guide-cover".*?</figure>'):
        a=re.search(rx,old,re.S);b=re.search(rx,text,re.S)
        require(a and b and a.group()==b.group(),'Site chrome or cover altered')
    a,b=schemas(old),schemas(text)
    require(len(a)==2 and len(b)==3,'Structured data count unexpected')
    original_article=dict(a[0]);new_article=dict(b[0]);require(new_article.pop('dateModified')=='2026-11-06','Wrong modified date');original_article.pop('dateModified')
    require(new_article==original_article and b[1]==a[1],'Protected Article/BreadcrumbList modified')
    questions=[(clean(q),clean(ans)) for q,ans in re.findall(r'<section class="pareto-faq"><h4>(.*?)</h4><p>(.*?)</p></section>',text,re.S)]
    schema=b[2];require(schema.get('@type')=='FAQPage' and len(schema.get('mainEntity',[]))==len(questions)==20,'FAQ mismatch count')
    for n,((q,ans),entry) in enumerate(zip(questions,schema['mainEntity']),1):
        require(q==entry['name'] and ans==entry['acceptedAnswer']['text'],f'FAQ mismatch at {n}')
    for oldid in re.findall(r'\bid="([^"]+)"',old):require(re.search(r'\bid="'+re.escape(oldid)+r'"',text),'Original anchor removed '+oldid)
    for url in re.findall(r'href="([^"]+)"',old):
        if url.startswith('/') or url.startswith('http'):require(f'href="{url}"' in text,'Original href removed '+url)
    for link in re.findall(r'\[[^\]]+\]\((/[^)]+)\)',md):require(f'href="{link}"' in text,'Source href missing '+link)
    ed=EditorialParser();ed.feed(text);require(len(ed.ids)==len(set(ed.ids)),'Duplicate IDs')
    source=source_tokens(md);converted=tokens(' '.join(ed.words))
    require(len(source)==len(converted)==EXPECTED,f'Word-count parity failed: {len(source)} != {len(converted)} expected {EXPECTED}')
    for i,(x,y) in enumerate(zip_longest(source,converted)):
        require(x==y,f'Manuscript order/content changed at token {i}: source {x!r}, HTML {y!r}')
    require(len(ed.sectionids)==37,'Lost source sections')
    toc=re.findall(r'<a class="pareto-toc-(?:main|nested)" href="#([^"]+)">',text)
    require(toc==ed.sectionids,'TOC order differs from full source')
    for kind,amount in (('life',6),('glossary',18)):
        tab=re.search(rf'<table id="pareto-{kind}-table".*?</table>',text,re.S)
        require(bool(tab),'Missing interactive table '+kind)
        require(len(re.findall(r'<tr data-row="\d+">',tab.group()))==amount,'Source row count wrong '+kind)
        for suffix in ('query','sort','reset','count'):require(f'id="pareto-{kind}-{suffix}"' in text,'Missing interactive '+kind+' control '+suffix)
    require(len(re.findall(r'<input type="radio" id="pareto-ledger-\d+"',text))==8,'Ledger must expose all seven + all')
    require(len(re.findall(r'<section class="pareto-ledger-panel pareto-ledger-panel-\d+"',text))==7,'Seven ledger views not built')
    js=(ROOT/'assets/international-pareto.js').read_text()
    require('beforeprint' in js and 'afterprint' in js and 'aria-pressed' in js,'Print or sorting behavior absent')
    css=(ROOT/'assets/international-pareto.css').read_text()
    require('@media print' in css and '@media(max-width:560px)' in css and 'display:table-header-group!important' in css,'Print/mobile safeguards absent')
    subprocess.run(['node','--check','assets/international-pareto.js'],cwd=ROOT,check=True)
    subprocess.run(['node','tools/test-pareto-interaction.cjs'],cwd=ROOT,check=True)
    print(f'PASS Pareto EN21: {EXPECTED} source-exact tokens; 37 sections; 20 visible/schema FAQs; 6+18 searchable rows; 7 native stages; SEO/cover protected')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--base',required=True);a=p.parse_args();verify(ROOT/PAGE,a.base)
