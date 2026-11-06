#!/usr/bin/env python3
"""Averroes EN 13 v1: source-pinned, read-only publication gate. No HTML generation."""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import hashlib,json,re,subprocess

ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/averroes-reason-interpretation-law/index.html'
SOURCE_COMMIT='45b32f17941b9b5ffb8cc914f51c57965a89053d'
SOURCE_FILE='AVERROES_EN_GUIDE_13_CANDIDATE_v1.md'
SOURCE_HASH='abd3f63c8c17c9a15f0792901b26f61c2abeb9233ca301488c311af949fc749d'
BASE_BLOB='5d0bbd87ad0575d2a98a053978429bde0447258e'
URL='https://alessandro-gentili.it/en/cerchi/guides/averroes-reason-interpretation-law/'

def require(value,message):
    if not value: raise AssertionError(message)

def git(ref,path):return subprocess.check_output(['git','show',f'{ref}:{path}'],cwd=ROOT)

def tokenize(s):return re.findall(r'[^\W_]+',s,re.UNICODE)

def source_text(md):
    require(md.startswith('# Averroes\n'),'Source title altered')
    require("## A reader's route" in md,'No body')
    src=md[md.index("## A reader's route"):]
    blocks=[]
    for line in src.splitlines():
        x=line.strip()
        if not x or x=='---' or re.fullmatch(r'\|[\s:|\-]+\|',x):continue
        if x.startswith('|'):blocks.extend(cell.strip() for cell in x.strip('|').split('|'));continue
        if x.startswith('#'):x=re.sub(r'^#{1,4}\s*','',x)
        elif x.startswith(('- ','* ')):x=x[2:]
        elif re.match(r'^\d+\.\s+',x):x=re.sub(r'^\d+\.\s+','',x)
        x=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',x)
        blocks.append(x.replace('**','').replace('*','').replace('`',''))
    return ' '.join(blocks)

class EditorialText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.level=0;self.out=[]
    def handle_starttag(self,tag,attrs):
        if self.level:self.level+=1
        elif dict(attrs).get('data-averroes-ui')=='1':self.level=1
    def handle_endtag(self,tag):
        if self.level:self.level-=1
    def handle_data(self,data):
        if not self.level:self.out.append(data)


def schemas(page):
    raw=re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',page,re.S)
    return [json.loads(x) for x in raw]

def verify(path,base):
    require(path.resolve().relative_to(ROOT).as_posix()==PAGE,'Out of Averroes scope')
    require(subprocess.check_output(['git','rev-parse',base+':'+PAGE],cwd=ROOT,text=True).strip()==BASE_BLOB,'Original page SHA changed')
    approved=git(SOURCE_COMMIT,SOURCE_FILE)
    require(hashlib.sha256(approved).hexdigest()==SOURCE_HASH,'Pinned manuscript corrupted')
    md=approved.decode('utf-8')
    old=git(base,PAGE).decode('utf-8');page=path.read_text(encoding='utf-8')
    require(page.startswith('<!doctype html>') and page.endswith('</html>\n'),'Incomplete HTML')
    require('<body class="guide-page international-atlas atlas-guide atlas-averroes">' in page,'Incorrect Atlas body')
    require('<main id="main-content"' in page and 'atlas-reader' in page and 'atlas-contents' in page,'Missing Plato layout')
    require('/assets/international-atlas.css' in page and '/assets/international-averroes.css' in page,'Missing CSS')
    require('/assets/international-averroes.js' in page and '/assets/international-atlas.js' in page,'Missing JS')
    require('id="interpreter-account"' in page and 'id="averroes-glossary-table"' in page,'Missing reading instruments')
    require(len(re.findall(r'\bclass="item guide-section',page))==36,'Sections changed')
    require(len(re.findall(r'\bclass="averroes-step averroes-step-',page))==5,'Reading test missing')
    require(len(re.findall(r'<tr\b',re.search(r'<table\b[^>]*id="averroes-glossary-table".*?</table>',page,re.S).group()))==24,'Glossary changed')
    blocks=re.findall(r'<article\b(?=[^>]*class="item guide-section)[^>]*>.*?</article>',page,re.S)
    require(len(blocks)==36,'Reader body missing section')
    parser=EditorialText();parser.feed(' '.join(blocks))
    a=tokenize(source_text(md));b=tokenize(' '.join(parser.out))
    require(a==b,f'Manuscript mismatch: {len(a)} vs {len(b)} tokens')
    require(len(a)==10868,'Unexpected manuscript token count')
    # Verify head SEO and global chrome remain identical to original, with an updated revision date.
    for tag in ['title','meta','link']:
        oldtags=re.findall(fr'<{tag}\b[^>]*?(?:/>|</{tag}>)',old,re.S)
        newtags=re.findall(fr'<{tag}\b[^>]*?(?:/>|</{tag}>)',page,re.S)
        if tag=='link':newtags=[x for x in newtags if 'international-atlas.css' not in x and 'international-averroes.css' not in x]
        require(oldtags==newtags,f'Protected {tag} changed')
    for pattern in [r'<header class="site-header".*?</header>',r'<footer class="footer".*?</footer>',r'<figure class="editorial-cover-card guide-cover".*?</figure>']:
        before=re.search(pattern,old,re.S)
        after=re.search(pattern,page,re.S)
        require(before and after and before.group()==after.group(),'Chrome or cover modified')
    beforeSchema=schemas(old);nowSchema=schemas(page)
    require(len(beforeSchema)==2 and len(nowSchema)==3,'Schema count changed')
    require(nowSchema[0].get('dateModified')=='2026-11-06','dateModified not updated')
    prev=nowSchema[0].copy();prev['dateModified']=beforeSchema[0].get('dateModified')
    require(prev==beforeSchema[0] and nowSchema[1]==beforeSchema[1],'Original JSON-LD mutated')
    faq=nowSchema[2]
    require(faq.get('@type')=='FAQPage' and faq.get('@id')==URL+'#faq','FAQPage wrong')
    qas=faq.get('mainEntity',[])
    require(len(qas)==20,'20 FAQ required')
    m=re.search(r'<article[^>]*id="faq"[^>]*>(.*?)</article>',page,re.S)
    require(m,'No visible FAQ')
    visible=re.findall(r'<p><strong>(\d+\.\s*.*?)</strong>\s*<br\s*/?>\s*(.*?)</p>',m.group(1),re.S)
    require(len(visible)==20,f'Visible FAQ count {len(visible)}')
    for i,((q,a),schema) in enumerate(zip(visible,qas),1):
        question=' '.join(unescape(re.sub(r'<[^>]+>','',q)).split())
        answer=' '.join(unescape(re.sub(r'<[^>]+>','',a)).split())
        require(question.startswith(str(i)+'. '),'FAQ numbering changed')
        require(schema.get('name')==question,'FAQ question differs')
        require(schema.get('acceptedAnswer',{}).get('text')==answer,'FAQ answer differs')
    ids=re.findall(r'\bid="([^"]+)"',page)
    require(len(ids)==len(set(ids)),'Duplicate IDs')
    toc=re.search(r'<nav class="guide-toc"[^>]*>(.*?)</nav>',page,re.S)
    require(toc,'TOC missing')
    anchors=re.findall(r'href="#([^"]+)"',toc.group(1))
    require(len(anchors)==36 and all(x in ids for x in anchors),'Dead or incomplete TOC links')
    require(all(x in page for x in ['href="/en/cerchi/triads/#triad-05"','lang="en"','hreflang="it"']),'Language or triad links missing')
    css=(ROOT/'assets/international-averroes.css').read_text()
    js=(ROOT/'assets/international-averroes.js').read_text()
    require('@media print' in css and 'tr[hidden]' in css and 'beforeprint' in js,'Filtered rows invisible in print')
    require('controls.hidden = false' in js and 'input.addEventListener' in js,'Glossary not interactive')
    print(f'PASS Averroes EN 13: {len(a)} source-locked tokens, 36 sections, 20 visible/schema FAQ, 23 glossary terms, 5 selectable inquiry stages')

if __name__=='__main__':
    import sys
    verify(ROOT/PAGE,sys.argv[1] if len(sys.argv)>1 else 'origin/main')
