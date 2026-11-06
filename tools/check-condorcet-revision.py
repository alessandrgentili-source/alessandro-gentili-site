#!/usr/bin/env python3
"""Condorcet EN18 source-locked conversion gate. Successful CI is not human editorial approval."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
from itertools import zip_longest

ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/nicolas-de-condorcet-education-progress-decision/index.html'
SOURCE_COMMIT='b0c40687b2779acfddcfd2d96a155ff178a45fc9'
SOURCE_FILE='CONDORCET_EN_GUIDE_18_CANDIDATE_v1.md'
SOURCE_BLOB='8b8016b5db6b4929df12e731e88a34524b60b2d1'
SOURCE_SHA256='16f3e6466a095b2ce94fd52a8545d0510a48e18512b45d5531b3edfd98a54b0b'
BASE_BLOB='6246b4a584edfa9cd1f965603096f464a21433e1'
SOURCE_TOKENS_SHA256='b48bb87a293ee2f64ab6e92a8555f6b42da11709e206d8bf5ae01a78c2f44d8b'
TOKEN_COUNT=13234
URL='https://alessandro-gentili.it/en/cerchi/guides/nicolas-de-condorcet-education-progress-decision/'

def check(ok,message):
    if not ok:raise AssertionError(message)

def git(ref,path):return subprocess.check_output(['git','show',f'{ref}:{path}'],cwd=ROOT)

def schemas(s):
    return [json.loads(x) for x in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S)]

def txt(s):
    class Strip(HTMLParser):
        def __init__(self):super().__init__(convert_charrefs=True);self.content=[]
        def handle_data(self,data):self.content.append(data)
    p=Strip();p.feed(s)
    return ' '.join(''.join(p.content).split())

class Editorial(HTMLParser):
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.skip=0
    def handle_starttag(self,tag,attrs):
        info=dict(attrs);skip_here=info.get('data-condorcet-ui')=='1' or info.get('data-condorcet-formula')=='1'
        if self.skip:
            if tag not in self.VOID:self.skip+=1
        elif skip_here:self.skip=1
    def handle_startendtag(self,tag,attrs):pass
    def handle_endtag(self,tag):
        if self.skip:self.skip-=1
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)

def validate(html,old,source,base):
    check(html.startswith('<!doctype html>') and html.endswith('</html>\n'),'HTML framing')
    check('<body class="guide-page international-atlas atlas-guide atlas-condorcet">' in html,'Plato-style Atlas root missing')
    check(html.count('<h1>')==1 and '<h1>Nicolas de Condorcet</h1>' in html,'Incorrect H1')
    for tag in ('header','main','footer'):
        check(len(re.findall(rf'<{tag}\b',html))==len(re.findall(rf'</{tag}>',html))==1,f'Unbalanced {tag}')
    for a in ('/assets/international-atlas.css','/assets/international-condorcet.css','/assets/international-atlas.js','/assets/international-condorcet.js','/assets/script.js'):
        check(a in html,'Asset missing: '+a)
    for a in ('assets/international-condorcet.css','assets/international-condorcet.js','tools/test-condorcet-interaction.cjs'):
        check((ROOT/a).is_file(),'Asset not committed: '+a)
    check(re.findall(r'<meta\b[^>]*>',old)==re.findall(r'<meta\b[^>]*>',html),'Meta OG/Twitter/description changed')
    before_links=re.findall(r'<link\b[^>]*>',old)
    after_links=[x for x in re.findall(r'<link\b[^>]*>',html) if 'international-atlas.css' not in x and 'international-condorcet.css' not in x]
    check(before_links==after_links,'Canonical/hreflang/stylesheet contract changed')
    check(re.search(r'<title>.*?</title>',old,re.S).group()==re.search(r'<title>.*?</title>',html,re.S).group(),'Title changed')
    for rx in (r'<header class="site-header".*?</header>',r'<footer class="footer".*?</footer>',r'<figure class="editorial-cover-card guide-cover".*?</figure>'):
        check(re.search(rx,old,re.S) and re.search(rx,html,re.S) and re.search(rx,old,re.S).group()==re.search(rx,html,re.S).group(),'Protected header/footer/cover changed')
    a,b=schemas(old),schemas(html)
    check(len(a)==2 and len(b)==3,'Article/Breadcrumb/FAQ schema count')
    earlier,article=dict(a[0]),dict(b[0]);check(earlier.pop('dateModified')=='2026-09-24' and article.pop('dateModified')=='2026-11-06' and earlier==article,'Article schema facts drift')
    check(a[1]==b[1],'Breadcrumb schema changed')
    check(b[2].get('@type')=='FAQPage' and b[2].get('@id')==URL+'#faq','FAQ identity')
    pairs=[(txt(q),txt(ans)) for q,ans in re.findall(r'<section class="condorcet-faq"><h4>(.*?)</h4><p>(.*?)</p></section>',html,re.S)]
    structured=[(x['name'],x['acceptedAnswer']['text']) for x in b[2]['mainEntity']]
    check(len(pairs)==20 and pairs==structured,'20 visible FAQ / structured FAQ mismatch')
    ids=re.findall(r'\bid="([^"]+)"',html)
    check(len(ids)==len(set(ids)) and set(re.findall(r'\bid="([^"]+)"',old)).issubset(ids),'Old anchors lost or duplicated IDs')
    article_ids=re.findall(r'<article\b[^>]*class="[^"]*\bguide-section\b[^"]*"[^>]*\bid="([^"]+)"',html)
    toc=re.search(r'<nav\b[^>]*class="guide-toc"[^>]*>(.*?)</nav>',html,re.S)
    check(toc is not None and len(article_ids)==36,'Missing source sections or contents')
    check(re.findall(r'href="#([^"]+)"',toc.group(1))==article_ids,'TOC section order')
    for uri in re.findall(r'\[[^\]]+\]\((https?://[^)]+)\)',source):check('href="'+uri+'"' in html,'Source link lost: '+uri)
    body=re.search(r'<div class="guide-body atlas-reading">(.*?)<details class="atlas-citation">',html,re.S)
    check(body is not None,'Full source body missing')
    parser=Editorial();parser.feed(body.group(1))
    words=re.findall(r'[^\W_]+',' '.join(parser.parts),re.U)
    fingerprint=hashlib.sha256((' '.join(words)).encode()).hexdigest()
    check(len(words)==TOKEN_COUNT and fingerprint==SOURCE_TOKENS_SHA256, f'Editorial token drift: {len(words)} words, sha={fingerprint}')
    # The source's LaTeX is typeset typographically; its equation is verified as a specific exception.
    check(r'P(\text{correct majority})=p^3+3p^2(1-p)' in source,'Pinned manuscript mathematical premise changed')
    equation=re.search(r'<p\b[^>]*class="condorcet-math"[^>]*>(.*?)</p>',html,re.S)
    check(equation and 'P</i>(correct majority)' in equation.group(1) and '<sup>3</sup>' in equation.group(1) and '<sup>2</sup>' in equation.group(1),'Mathematical equation corrupted')
    check('0.648' in source and '64.8 per cent' in source,'Jury source numerical result drift')
    check(len(re.findall(r'<tr data-original-index="\d+">',html))==24,'Chronology/glossary row coverage')
    for id,n in [('condorcet-life-table',8),('condorcet-glossary-table',16)]:
        table=re.search(r'<table\b[^>]*id="'+id+r'"[^>]*>(.*?)</table>',html,re.S)
        check(table and table.group(1).count('data-original-index=')==n,f'{id}: source table rows')
    voter=re.search(r'<table\b[^>]*id="condorcet-vote-table"[^>]*>(.*?)</table>',html,re.S)
    check(voter and len(re.findall(r'<tr data-voter=',voter.group(1)))==3,'Three true source rankings must remain visible')
    check(len(re.findall(r'class="condorcet-stage condorcet-stage-\d+"',html))==6,'Before-the-count six steps lost')
    check('id="condorcet-probability"' in html and 'id="condorcet-jurors"' in html,'Live probability controls absent')
    css=(ROOT/'assets/international-condorcet.css').read_text();js=(ROOT/'assets/international-condorcet.js').read_text()
    check('@media print' in css and 'display:table-header-group!important' in css and 'data-enhanced="true"' in css,'Responsive/no-JS/print rules')
    check('beforeprint' in js and 'afterprint' in js and 'import(' not in js and 'fetch(' not in js,'Progressive JS with no network dependencies')
    check('data-condorcet-ui="1" hidden' in html,'Progressive UI should hide without JS')
    sitemap=(ROOT/'sitemap.xml').read_text()
    previous=git(base,'sitemap.xml').decode()
    oldtag='<loc>'+URL+'</loc>\n    <lastmod>2026-09-24</lastmod>'
    newtag=oldtag.replace('2026-09-24','2026-11-06')
    check(previous.count(oldtag)==1 and sitemap==previous.replace(oldtag,newtag),'Only Condorcet EN sitemap lastmod may change')
    subprocess.run(['node','--check',str(ROOT/'assets/international-condorcet.js')],cwd=ROOT,check=True)
    subprocess.run(['node',str(ROOT/'tools/test-condorcet-interaction.cjs')],cwd=ROOT,check=True)
    print(f'PASS Condorcet EN18: {len(words)} source-exact lexical tokens + checked math; 36 sections, 20 FAQ, 8+16 searchable rows, 3 pairwise choices, 6 stages; SEO/chrome/cover locked')

def verify(path,base):
    check(path.resolve().relative_to(ROOT).as_posix()==PAGE,'Wrong published path')
    baseblob=subprocess.check_output(['git','rev-parse',f'{base}:{PAGE}'],cwd=ROOT,text=True).strip()
    check(baseblob==BASE_BLOB,'Original main page changed since migration started')
    cmd=['git','rev-parse',f'{SOURCE_COMMIT}:{SOURCE_FILE}']
    r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    if r.returncode:
        subprocess.run(['git','fetch','--no-tags','origin',SOURCE_COMMIT],cwd=ROOT,check=True)
        r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,check=True)
    check(r.stdout.strip()==SOURCE_BLOB,'Pinned source git blob drift')
    source=git(SOURCE_COMMIT,SOURCE_FILE)
    check(hashlib.sha256(source).hexdigest()==SOURCE_SHA256,'Source bytes modified')
    old=git(base,PAGE).decode()
    html=path.read_text()
    validate(html,old,source.decode(),base)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True)
    args=ap.parse_args();verify(ROOT/PAGE,args.base)
