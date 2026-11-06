#!/usr/bin/env python3
"""Source-pinned full Mosca EN20 migration gate. Technical PASS never means literary approval."""
import argparse, hashlib, html, json, re, subprocess
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/gaetano-mosca-political-class-organization-real-government/index.html'
SOURCE_COMMIT='c0a75c646e5a9eec3e617f3006ca80fbdbe6d754'
SOURCE_BLOB='f045c71b7d5b943601a62b42684ca6cef271b9f0'
SOURCE_FILE='MOSCA_EN_GUIDE_20_CANDIDATE_v1.md'
SOURCE_BRANCH='input/guide-20-gaetano-mosca-en-source-candidate'
BASE_BLOB='8d1ac61d646a700f4fe4c7d26477082eb9109eb1'
URL='https://alessandro-gentili.it/en/cerchi/guides/gaetano-mosca-political-class-organization-real-government/'
TOKENS=13902
SOURCE_DIGEST='9502b8d211659081c2160d55e98a17d0a3075702a14da588a7e5c5913dee3123'
LEGACY=['introduction','political-class','organized-minority','political-formula','recruitment','democracy','legal-defense','wound','sources']

def check(cond,message):
 if not cond:raise AssertionError(message)
def git_show(ref,path=None):
 expr=ref+(':'+path if path else '')
 return subprocess.check_output(['git','show',expr],cwd=ROOT,text=True)
def pinned_source():
 try:return git_show(SOURCE_COMMIT,SOURCE_FILE)
 except subprocess.CalledProcessError:
  subprocess.run(['git','fetch','--no-tags','origin',f'refs/heads/{SOURCE_BRANCH}:refs/remotes/origin/{SOURCE_BRANCH}'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
  return git_show(SOURCE_COMMIT,SOURCE_FILE)
def tokens(text):return re.findall(r'[^\W_]+',text,re.UNICODE)

class EditorialText(HTMLParser):
 VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
 def __init__(self):super().__init__(convert_charrefs=True);self.skip=0;self.parts=[]
 def handle_starttag(self,tag,attrs):
  if self.skip:
   if tag not in self.VOID:self.skip+=1
   return
  if dict(attrs).get('data-mosca-ui')=='1':self.skip=1
 def handle_startendtag(self,tag,attrs):
  if dict(attrs).get('data-mosca-ui')=='1':return
 def handle_endtag(self,tag):
  if self.skip:self.skip-=1
 def handle_data(self,data):
  if not self.skip:self.parts.append(data)

def plain(raw):return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]*>','',raw))).strip()

def verify(path,base=None):
 text=Path(path).read_text(encoding='utf8')
 source=pinned_source()
 actualblob=subprocess.check_output(['git','hash-object','--stdin'],cwd=ROOT,input=source,text=True).strip()
 check(actualblob==SOURCE_BLOB,'Pinned Mosca Markdown source blob differs')
 original=subprocess.check_output(['git','cat-file','-p',BASE_BLOB],cwd=ROOT,text=True)
 check(text.startswith('<!doctype html>') and '<html lang="en">' in text,'Invalid HTML language/doctypes')
 for tag in ('title','h1'):
  check(len(re.findall(rf'<{tag}\b[^>]*>',text))==1,f'Expected one {tag}')
 # All existing stable SEO fields are retained (only the original dateModified may change).
 patterns=[r'<title>.*?</title>',r'<meta name="description"[^>]+>',r'<link rel="canonical"[^>]+>',r'<link rel="alternate"[^>]+>',r'<meta property="og:[^"]+"[^>]+>',r'<meta name="twitter:[^"]+"[^>]+>']
 for pattern in patterns:
  check(re.findall(pattern,original,re.S)==re.findall(pattern,text,re.S),f'Protected SEO altered: {pattern}')
 for name in ['header','footer']:
  pattern=rf'<{name} class="[^"]+">.*?</{name}>'
  check(re.findall(pattern,original,re.S)==re.findall(pattern,text,re.S),f'Original {name} changed')
 cover=r'<figure class="editorial-cover-card guide-cover">.*?</figure>'
 check(re.findall(cover,original,re.S)==re.findall(cover,text,re.S),'Cover/alt changed')
 oldids=set(re.findall(r'\bid="([^"]+)"',original));newids=re.findall(r'\bid="([^"]+)"',text)
 check(oldids.issubset(newids),'Original anchor lost: '+str(sorted(oldids-set(newids))))
 check(len(newids)==len(set(newids)),'Duplicate ID on guide')
 check(f'href="{URL}"' in text,'Cite source link missing')
 check('"dateModified": "2026-11-06"' in text,'Article dateModified must reflect revision date')
 oldschema=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',original,re.S)]
 schema=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)]
 check(len(oldschema)==2 and len(schema)==3,'Article/BreadcrumbList/FAQ schemas missing or extra')
 oldschema[0].pop('dateModified',None);schema[0].pop('dateModified',None)
 check(schema[0]==oldschema[0] and schema[1]==oldschema[1],'Article/Breadcrumb structured data altered')
 check(schema[2].get('@type')=='FAQPage','Expected FAQPage structured data')
 pairs=[(plain(q),plain(a)) for q,a in re.findall(r'<section class="mosca-faq"><h4>(.*?)</h4><p>(.*?)</p></section>',text,re.S)]
 check(len(pairs)==20,'Exactly 20 visible FAQs required')
 structured=[(q.get('name'),q.get('acceptedAnswer',{}).get('text')) for q in schema[2].get('mainEntity',[])]
 check(pairs==structured,'FAQ text/order differs from visible questions and answers')
 anchors=re.findall(r'<article class="item guide-section mosca-section[^"]*" id="([^"]+)">',text)
 check(len(anchors)==37 and len(anchors)==len(set(anchors)),'37 unique source sections required')
 check(len(re.findall(r'<tr data-original-index="\d+">',text))==30,'6 life + 24 glossary source rows required')
 for kind,n in [('life',6),('glossary',24)]:
  table=re.search(rf'<table class="mosca-data-table" id="mosca-{kind}-table">.*?</table>',text,re.S)
  check(table is not None and len(re.findall(r'<tr data-original-index="\d+">',table.group()))==n,f'{kind} table rows missing')
  for ctrl in ['query','sort','reset','count']:check(f'id="mosca-{kind}-{ctrl}"' in text,f'{kind} {ctrl} missing')
 check(len(re.findall(r'<input\b[^>]*\bid="mosca-choice-\d+"[^>]*\btype="radio"',text))==8,'Seven plus All station selectors missing')
 check(len(re.findall(r'class="mosca-choice-step mosca-choice-step-\d+"',text))==7,'Seven source reading steps missing')
 check(len(re.findall(r'data-mosca-ui="1" hidden',text))==2,'No-JS tables must have hidden controls')
 # Extract only the source articles; remove interactive UI text by parser, then compare the immutable source's exact token hash.
 fragments=re.findall(r'<article class="item guide-section mosca-section[^\"]*" id="[^\"]+">(.*?)</article>',text,re.S)
 check(len(fragments)==37,'Could not segment all source articles')
 reader=EditorialText();reader.feed(' '.join(fragments));found=tokens(' '.join(reader.parts))
 fingerprint=hashlib.sha256('\x1f'.join(found).encode('utf8')).hexdigest()
 check(len(found)==TOKENS and fingerprint==SOURCE_DIGEST,f'Editorial source tokens changed: {len(found)} {fingerprint}')
 for dest in re.findall(r'\]\((/[^)]+)\)',source):
  check(f'href="{html.escape(dest,quote=True)}"' in text,f'Original internal link missing {dest}')
 css=(ROOT/'assets/international-mosca.css').read_text();js=(ROOT/'assets/international-mosca.js').read_text()
 check('@media print' in css and 'display:table-row!important' in css and 'display:block!important' in css,'Print must restore tables and all seven steps')
 check('beforeprint' in js and 'afterprint' in js and 'normalize(' in js,'Interactive progressive enhancement missing')
 for script in ['assets/international-mosca.js','tools/test-mosca-interaction.cjs']:
  subprocess.run(['node','--check',str(ROOT/script)],cwd=ROOT,check=True)
 subprocess.run(['node',str(ROOT/'tools/test-mosca-interaction.cjs')],cwd=ROOT,check=True)
 print(f'PASS Mosca EN20: {TOKENS} source-exact tokens; 37 sections; 20 visible/schema FAQs; 6+24 searchable rows; 7 native reading stages; SEO/chrome/cover locked')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('path',nargs='?',default=str(ROOT/PAGE));p.add_argument('--base',default='main');a=p.parse_args();verify(Path(a.path),a.base)
