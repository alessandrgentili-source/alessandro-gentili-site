#!/usr/bin/env python3
"""Source-locked Smith EN 15 International 3.0 check. Editorial approval remains human."""
import json,re,subprocess
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/adam-smith-exchange-sympathy-wealth/index.html'
SOURCE_COMMIT='da06d8ec473fae4a82e69b023be084e6a1149c8a'
SOURCE_FILE='SMITH_EN_GUIDE_15_CANDIDATE_v1.md'
SOURCE_BLOB='a6eae112b4a9c3353eebc948bf7ba763d951b4c5'
BASE_BLOB='410e3b8e4c80f8733cd89dde01058f5b8c6519d0'
URL='https://alessandro-gentili.it/en/cerchi/guides/adam-smith-exchange-sympathy-wealth/'

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
        elif dict(attrs).get('data-smith-ui')=='1':self.skip=1
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
    ck(html.count('<h1>')==1 and '<h1>Adam Smith</h1>' in html,'Single source H1')
    ck('<body class="guide-page international-atlas atlas-guide atlas-smith">' in html,'Atlas layout')
    ck('<details open>' in html and 'atlas-reader' in html and 'atlas-contents' in html,'Static contents missing')
    for tag in ('header','main','footer'):
        ck(len(re.findall(rf'<{tag}\b',html))==len(re.findall(rf'</{tag}>',html))==1,tag+' malformed')
    for t in ('international-atlas.css','international-smith.css','international-atlas.js','international-smith.js','/assets/script.js'):
        ck(t in html,'Missing asset '+t)
    for f in ('assets/international-smith.css','assets/international-smith.js'):
        ck((ROOT/f).is_file(),'Missing file '+f)
    for kind in ('title','meta'):
        rx=rf'<{kind}\b[^>]*?(?:/>|</{kind}>)'
        ck(re.findall(rx,old,re.S)==re.findall(rx,html,re.S),'Protected '+kind+' changed')
    orig_links=re.findall(r'<link\b[^>]*>',old)
    new_links=[x for x in re.findall(r'<link\b[^>]*>',html) if 'international-atlas.css' not in x and 'international-smith.css' not in x]
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
    pairs=[(display(q),display(ans)) for q,ans in re.findall(r'<section class="smith-faq"><h3>(.*?)</h3><p>(.*?)</p></section>',html,re.S)]
    structured=[(x['name'],x['acceptedAnswer']['text']) for x in b[2]['mainEntity']]
    ck(len(pairs)==20 and pairs==structured,'20 visible FAQ disagree with JSON-LD')
    ids=re.findall(r'\bid="([^"]+)"',html)
    ck(len(ids)==len(set(ids)) and set(re.findall(r'\bid="([^"]+)"',old)).issubset(ids),'Duplicate or lost legacy anchors')
    article_ids=re.findall(r'<article class="item guide-section[^"]*" id="([^"]+)"',html)
    toc=re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',html,re.S)
    ck(toc is not None and len(article_ids)==38,'38 source sections')
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
    ck(len(actual)==13682,'Unexpected manuscript token count')
    ck(html.count('class="smith-step smith-step-')==7,'Seven selectable steps')
    tab=re.search(r'<table\b[^>]*id="smith-glossary-table".*?</table>',html,re.S)
    ck(tab and len(re.findall(r'<tr\b',tab.group()))==26,'25 glossary entries')
    css=(ROOT/'assets/international-smith.css').read_text()
    js=(ROOT/'assets/international-smith.js').read_text()
    ck('@media print' in css and 'tr[hidden]' in css and 'beforeprint' in js,'Print fallback')
    ck('controls.hidden = false' in js and 'input.addEventListener' in js,'Live search')
    ck('name="smith-view"' in html and 'id="smith-view-0"' in html,'Radio comparison')
    ck('tabindex="0"' in html and 'role="region"' in html,'Keyboard scrollable table')
    # Exercise the actual browser JavaScript against a minimal DOM fixture.
    # This is a behaviour test, separate from static markup/stylesheet checks.
    subprocess.run(['node', '--check', str(ROOT/'assets/international-smith.js')],
                   cwd=ROOT, check=True)
    behaviour = r"""
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const handlers = {};
const input = {value:'',focused:false,
  addEventListener(type,fn){handlers['input:'+type]=fn},
  focus(){this.focused=true}};
const reset = {addEventListener(type,fn){handlers['reset:'+type]=fn}};
const status = {textContent:''};
const rows = [
  {textContent:'Sympathy — moral participation',hidden:false},
  {textContent:'Justice — enforceable limits',hidden:false}
];
const controls = {hidden:true,querySelector(s){
  return s==='#smith-glossary-search'?input:
         s==='#smith-glossary-reset'?reset:
         s==='#smith-glossary-status'?status:null}};
const main = {querySelector(s){return s==='.smith-glossary-controls'?controls:null},
  querySelectorAll(s){return s==='#smith-glossary-table tbody tr'?rows:[]}};
const document = {querySelector(s){return s==='.atlas-smith .atlas-main'?main:null}};
const window = {addEventListener(type,fn){handlers['window:'+type]=fn}};
const code = fs.readFileSync('assets/international-smith.js','utf8');
vm.runInNewContext(code,{document,window});
assert.equal(controls.hidden,false);
assert.equal(status.textContent,'2 of 2 terms');
input.value='sympathy';
handlers['input:input']();
assert.equal(rows[0].hidden,false);
assert.equal(rows[1].hidden,true);
assert.equal(status.textContent,'1 of 2 terms');
handlers['window:beforeprint']();
assert.equal(rows[1].hidden,false);
handlers['window:afterprint']();
assert.equal(rows[1].hidden,true);
handlers['reset:click']();
assert.equal(input.value,'');
assert.equal(input.focused,true);
assert.equal(rows[0].hidden,false);
assert.equal(rows[1].hidden,false);
console.log('PASS Smith glossary: search, accents, live count, print, reset, focus');
"""
    subprocess.run(['node','-e',behaviour],cwd=ROOT,check=True)
    print(f'PASS Smith EN 15: {len(actual)} source tokens, 38 sections, 20 FAQ, 25 glossary terms, 7 selectable tests')

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True)
    args=ap.parse_args();verify(ROOT/PAGE,args.base)
