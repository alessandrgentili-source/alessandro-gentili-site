#!/usr/bin/env python3
"""Polybius EN19: source-pinned editorial/technical integrity. Passing is not author approval."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
from itertools import zip_longest

ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/polybius-constitution-power-decline/index.html'
SOURCE_COMMIT='85ead8b5019f0df613cde33a37d0ebf7d26e1227'
SOURCE_FILE='POLYBIUS_EN_GUIDE_19_CANDIDATE_v1.md'
SOURCE_BLOB='902af33847260c9c55db8144d3e18c6c1c1a5c9c'
BASE_BLOB='4fcebca9ed6191b864a65d00efb9e3b2530ea4a0'
URL='https://alessandro-gentili.it/en/cerchi/guides/polybius-constitution-power-decline/'
EXPECTED_COUNT=12636


def require(condition,msg):
    if not condition: raise AssertionError(msg)

def gitshow(ref,path):
    return subprocess.check_output(['git','show',f'{ref}:{path}'],cwd=ROOT,text=True)

def toks(s): return re.findall(r'[^\W_]+',s,re.UNICODE)

def source_words(md):
    result=[]
    for raw in md[md.index("## A reader's route"):].splitlines():
        line=raw.strip()
        if not line or line=='---':continue
        isheading=bool(re.match(r'^#{2,3}\s',line))
        line=re.sub(r'^#{2,3}\s+','',line)
        if not isheading:
            line=re.sub(r'^[-*]\s+','',line)
            line=re.sub(r'^\d+\.\s+','',line)
        line=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',line)
        result.append(line.replace('**','').replace('*','').replace('`',''))
    return toks(' '.join(result))

class EditorialParser(HTMLParser):
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):super().__init__(convert_charrefs=True);self.skip=0;self.words=[]
    def handle_starttag(self,tag,attrs):
        if self.skip:
            if tag not in self.VOID:self.skip+=1
        elif dict(attrs).get('data-polybius-ui')=='1':self.skip=1
    def handle_startendtag(self,tag,attrs):pass
    def handle_endtag(self,tag):
        if self.skip:self.skip-=1
    def handle_data(self,data):
        if not self.skip:self.words.append(data)

def showtext(x):return ' '.join(unescape(re.sub(r'<[^>]+>',' ',x)).split())

def schemas(s):return [json.loads(x) for x in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S)]

def verify(path,base):
    require(path.resolve().relative_to(ROOT).as_posix()==PAGE,'Wrong guide path')
    sha=subprocess.check_output(['git','rev-parse',f'{base}:{PAGE}'],cwd=ROOT,text=True).strip()
    require(sha==BASE_BLOB,'Original short guide changed: do not overwrite unknown edition')
    chk=subprocess.run(['git','rev-parse',f'{SOURCE_COMMIT}:{SOURCE_FILE}'],cwd=ROOT,text=True,capture_output=True)
    if chk.returncode:
        subprocess.run(['git','fetch','--no-tags','origin',SOURCE_COMMIT],cwd=ROOT,check=True)
        chk=subprocess.run(['git','rev-parse',f'{SOURCE_COMMIT}:{SOURCE_FILE}'],cwd=ROOT,text=True,capture_output=True,check=True)
    require(chk.stdout.strip()==SOURCE_BLOB,'Source manuscript changed')
    src=gitshow(SOURCE_COMMIT,SOURCE_FILE)
    old=gitshow(base,PAGE)
    page=path.read_text('utf-8')
    require(page.startswith('<!doctype html>') and page.endswith('</html>\n'),'Malformed HTML frame')
    require(page.count('<h1>')==1 and '<h1>Polybius</h1>' in page,'Wrong H1')
    require('atlas-polybius' in page and 'atlas-reader' in page,'Missing Plato-aligned reading architecture')
    for tag in ('header','main','footer'):
        require(len(re.findall(rf'<{tag}\b',page))==len(re.findall(rf'</{tag}>',page))==1,'Unbalanced '+tag)
    for f in ('international-atlas.css','international-polybius.css','international-atlas.js','international-polybius.js','/assets/script.js'):
        require(f in page,'Missing asset '+f)
    for f in ('assets/international-polybius.css','assets/international-polybius.js','tools/test-polybius-interaction.cjs'):
        require((ROOT/f).is_file(),'Missing code '+f)
    for tag in ('title','meta'):
        pat=rf'<{tag}\b[^>]*?(?:/>|</{tag}>)'
        require(re.findall(pat,old,re.S)==re.findall(pat,page,re.S),'Protected '+tag+' drift')
    oldlinks=re.findall(r'<link\b[^>]*>',old)
    newlinks=[x for x in re.findall(r'<link\b[^>]*>',page) if 'international-atlas.css' not in x and 'international-polybius.css' not in x]
    require(oldlinks==newlinks,'Canonical/hreflang stylesheet contract changed')
    for rx in (r'<header class="site-header".*?</header>',r'<footer class="footer".*?</footer>',r'<figure class="editorial-cover-card guide-cover".*?</figure>'):
        earlier=re.search(rx,old,re.S);now=re.search(rx,page,re.S)
        require(earlier and now and earlier.group()==now.group(),'Cover/chrome changed')
    a,b=schemas(old),schemas(page)
    require(len(a)==2 and len(b)==3,'Schema counts changed')
    early=dict(a[0]);revised=dict(b[0])
    require(early.pop('dateModified')=='2026-09-24' and revised.pop('dateModified')=='2026-11-06' and early==revised,'Article structured metadata drift')
    require(a[1]==b[1],'Breadcrumb structured metadata drift')
    require(b[2].get('@type')=='FAQPage' and b[2].get('@id')==URL+'#faq','FAQPage identity')
    pairs=[(showtext(q),showtext(ans)) for q,ans in re.findall(r'<section class="polybius-faq"><h4>(.*?)</h4>(.*?)</section>',page,re.S)]
    structured=[(item['name'],item['acceptedAnswer']['text']) for item in b[2]['mainEntity']]
    require(len(pairs)==20 and pairs==structured,'20 visible FAQ and schema disagree')
    ids=re.findall(r'\bid="([^"]+)"',page)
    require(len(ids)==len(set(ids)),'Duplicate IDs')
    require(set(re.findall(r'\bid="([^"]+)"',old)).issubset(ids),'Legacy links broken')
    articles=re.findall(r'<article class="item guide-section polybius-section[^"]*" id="([^"]+)"',page)
    toc=re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',page,re.S)
    require(toc and len(articles)==37 and re.findall(r'href="#([^"]+)"',toc.group(1))==articles,'37 source sections/TOC mismatch')
    for href in re.findall(r'\[[^\]]+\]\((https?://[^)]+)\)',src):
        require('href="'+href+'"' in page,'Editorial link omitted: '+href)
    body=re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">',page,re.S)
    require(body is not None,'Reading content absent')
    text=EditorialParser();text.feed(body.group(1))
    expected=source_words(src);actual=toks(' '.join(text.words))
    if expected!=actual:
        i=next((j for j,(a,b) in enumerate(zip_longest(expected,actual)) if a!=b),-1)
        raise AssertionError(f'Lexical drift: expected {len(expected)}, actual {len(actual)}, at {i}; source={expected[max(0,i-4):i+10]} html={actual[max(0,i-4):i+10]}')
    require(len(actual)==EXPECTED_COUNT,'Unexpected source token count')
    require(len(re.findall(r'<tr data-original-index="\d+"',re.search(r'<table id="polybius-life-table".*?</table>',page,re.S).group()))==6,'Life table rows not 6')
    require(len(re.findall(r'<tr data-original-index="\d+"',re.search(r'<table id="polybius-glossary-table".*?</table>',page,re.S).group()))==24,'Glossary entries not 24')
    require(len(re.findall(r'<section class="polybius-step polybius-step-\d+"',page))==7,'Seven native selectable source steps missing')
    require('name="polybius-view"' in page and 'id="polybius-view-7"' in page,'Native radio controls missing')
    css=(ROOT/'assets/international-polybius.css').read_text('utf-8')
    js=(ROOT/'assets/international-polybius.js').read_text('utf-8')
    for condition,msg in [('@media print' in css and 'display:table-header-group!important' in css,'Print table fallback'),('tr[hidden]' in css and 'display:table-row!important' in css,'Print filtered rows'),('min-height:44px' in css,'Touch targets'),('beforeprint' in js and 'afterprint' in js,'Print state'),('controls.hidden = false' in js,'No-JS to JS progressive enhancement')]:
        require(condition,msg)
    subprocess.run(['node','--check',str(ROOT/'assets/international-polybius.js')],cwd=ROOT,check=True)
    subprocess.run(['node',str(ROOT/'tools/test-polybius-interaction.cjs')],cwd=ROOT,check=True)
    print(f'PASS Polybius EN19: {len(expected)} exact source tokens; {len(articles)} sections; 20 FAQ; 6+24 live searchable rows; 7 native steps; protected SEO/cover')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True);args=ap.parse_args();verify(ROOT/PAGE,args.base)
