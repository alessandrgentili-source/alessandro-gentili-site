#!/usr/bin/env python3
"""Single approved Clausewitz EN33 conversion: exact source, full inline fidelity,
metadata and native-figure preservation. Does not authorize other revisions."""
import argparse,hashlib,json,re,runpy,subprocess
from pathlib import Path
from html import unescape
ROOT=Path(__file__).resolve().parents[1]
PAGE='en/cerchi/guides/carl-von-clausewitz-war-politics-limits-of-force/index.html'
CSS='assets/international-clausewitz.css'
SOURCE_COMMIT='2d6603f27a6bca927650dd01e37cc821b55a37b9'
SOURCE_FILE='CLAUSEWITZ_EN33_REVIEWED_CANDIDATE_v3.md'
SOURCE_SHA256='09f36278591d3e8433c65daee861f8ea9ab97950e422ff9115bcf29bef6df72e'
BASE_BLOB='1edf7b7ea025836286d6aff607f7696a394425ec'
# Exact approved conversion snapshots; source and structural checks remain mandatory.
HTML_BLOB='54b25737d154c46b12a2629f66558493f9768717'
CSS_BLOB='0073a1c3ce03f53f813457c003e1aa2328335dec'
parser=runpy.run_path(str(ROOT/'tools/validate-cerchi-guide.py'))
Tree,Node,walk,content,normal=(parser[x] for x in ['Tree','Node','walk','content','normalized'])
def check(ok,msg):
 if not ok:raise AssertionError(msg)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def source():
 try:s=subprocess.check_output(['git','show',f'{SOURCE_COMMIT}:{SOURCE_FILE}'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL)
 except subprocess.CalledProcessError:
  subprocess.run(['git','fetch','--no-tags','origin',SOURCE_COMMIT],cwd=ROOT,check=True)
  s=subprocess.check_output(['git','show',f'{SOURCE_COMMIT}:{SOURCE_FILE}'],cwd=ROOT,text=True)
 check(hashlib.sha256(s.encode()).hexdigest()==SOURCE_SHA256,'Approved Markdown hash changed');return s
def inline(s):
 root=Node();i=0
 while i<len(s):
  m=re.match(r'\[([^\]]+)\]\(([^)]+)\)',s[i:])
  if m:n=Node('a',[('href',m[2])]);n.children=inline(m[1]).children;root.children.append(n);i+=len(m[0]);continue
  token=next((t for t in ['**','*','`'] if s.startswith(t,i)),None)
  if token:
   end=s.find(token,i+len(token));check(end>=0,'Unclosed source emphasis')
   n=Node({'**':'strong','*':'em','`':'code'}[token]);n.children=inline(s[i+len(token):end]).children;root.children.append(n);i=end+len(token);continue
  root.children.append(s[i]);i+=1
 return root
def sig(n):return normal(content(n)),[(x.tag,normal(content(x)),x.attrs.get('href')) for x in walk(n) if x.tag in ['strong','em','a','code']]
def same(n,s):check(sig(n)==sig(inline(s)),'Source text/emphasis/link mismatch: '+s[:80])
def kids(n):return [x for x in n.children if isinstance(x,Node)]
def body_blocks(s):
 # Line-oriented CommonMark subset: headings interrupt paragraphs even without blank lines.
 lines=s.strip().splitlines();out=[];i=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[v.strip() for v in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',v) for v in cells):rows.append(cells)
    i+=1
   out.append(('table',rows));continue
  m=re.match(r'^(#{1,4}) (.+)',line)
  if m:out.append(('h'+str(len(m[1])),m[2]));i+=1;continue
  m=re.match(r'^(?:- |\d+\. )(.+)',line)
  if m:
   typ='ul' if line.startswith('- ') else 'ol';items=[]
   while i<len(lines):
    m=re.match(r'^- (.+)' if typ=='ul' else r'^\d+\. (.+)',lines[i].strip())
    if not m:break
    items.append(m[1]);i+=1
   out.append((typ,items));continue
  p=[]
  while i<len(lines) and lines[i].strip() and not re.match(r'^(?:#{1,4} |\|)',lines[i].strip()):p.append(lines[i].strip());i+=1
  out.append(('p',' '.join(p)))
 return out
def compare_blocks(actual,expected):
 check(len(actual)==len(expected),'Content blocks missing/extra/reordered')
 for n,(typ,val) in zip(actual,expected):
  if typ=='table' and n.tag=='div':
   check(len(kids(n))==1 and kids(n)[0].tag=='table','Unexpected table wrapper');n=kids(n)[0]
  check(n.tag==typ,'Block type/order changed: '+typ)
  if typ in ['ul','ol']:
   li=kids(n);check(len(li)==len(val),'List item lost');[same(x,v) for x,v in zip(li,val)]
  elif typ=='table':
   rows=list(n.find('tr'));check(len(rows)==len(val),'Table row lost')
   for row,cells in zip(rows,val):
    cc=kids(row);check(len(cc)==len(cells),'Table column lost');[same(x,v) for x,v in zip(cc,cells)]
  else:same(n,val)
def verify(path,base):
 check(path.resolve().relative_to(ROOT).as_posix()==PAGE,'Wrong author path')
 check(git('rev-parse',f'{base}:{PAGE}')==BASE_BLOB,'Historical Clausewitz baseline changed')
 check(git('hash-object',PAGE)==HTML_BLOB,'Unreviewed Clausewitz HTML snapshot')
 check(git('hash-object',CSS)==CSS_BLOB,'Unreviewed Clausewitz CSS snapshot')
 md=source();old=subprocess.check_output(['git','show',f'{base}:{PAGE}'],cwd=ROOT,text=True);new=path.read_text();tree=Tree(new);check(not tree.malformed,'Malformed HTML')
 allnodes=list(walk(tree.root));byid={n.attrs['id']:n for n in allnodes if 'id' in n.attrs}
 ids=[n.attrs['id'] for n in allnodes if 'id'in n.attrs];check(len(ids)==len(set(ids)),'Duplicate ID')
 oldids=set(re.findall(r'\bid="([^"]+)"',old));check(oldids<=set(ids),'Historical anchor removed')
 for a in [n for n in allnodes if n.tag=='a' and n.attrs.get('href','').startswith('#')]:check(a.attrs['href'][1:] in byid,'Broken fragment')
 for tag in ['html','body','main','header','footer','h1']:check(len([n for n in allnodes if n.tag==tag])==1,'Invalid frame '+tag)
 for pattern in [r'<title>.*?</title>',r'<nav class="wrap atlas-breadcrumb".*?</nav>',r'<div class="atlas-guide-opening">.*?(?=<div class="wrap atlas-reader">)',r'<h1>.*?</h1>',r'<meta\b[^>]*>',r'<link\b[^>]*>',r'<header class="site-header">.*?</header>',r'<footer class="footer">.*?</footer>',r'<figure class="editorial-cover-card guide-cover">.*?</figure>',r'<figure class="atlas-figure clausewitz-figure".*?</figure>',r'<script src="[^"]+"[^>]*></script>']:
  check(re.findall(pattern,old,re.S)==re.findall(pattern,new,re.S),'Protected SEO/chrome/cover/native figure/scripts changed')
 check((ROOT/CSS).read_text().startswith(subprocess.check_output(['git','show',f'{base}:{CSS}'],cwd=ROOT,text=True)),'Native two-state CSS altered')
 oldld=[json.loads(x)for x in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',old,re.S)]
 newld=[json.loads(x)for x in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',new,re.S)]
 check(len(oldld)==2 and len(newld)==3,'Schema set changed');article=dict(newld[0]);check(article.pop('dateModified')=='2026-11-06','Wrong revision date');prior=dict(oldld[0]);prior.pop('dateModified');check(article==prior and newld[1]==oldld[1],'Article/Breadcrumb facts changed')
 reader=md[md.index('## A reader'):md.index('## In this guide')];compare_blocks(kids(byid['reader-route'])[1:],body_blocks(reader)[1:])
 body=md[md.index('## The main essay'):];parts=re.split(r'(?m)^### (.+)\n',body);sections=list(zip(parts[1::2],parts[2::2]));check(len(sections)==35,'Expected ten chapters and 25 Atlas sections')
 articles=[n for n in allnodes if n.tag=='article' and 'clausewitz-section'in n.attrs.get('class','').split()];check(len(articles)==36,'Missing/extra editorial section')
 toc=list(next(n for n in allnodes if n.tag=='nav' and 'guide-toc'in n.attrs.get('class','').split()).find('a'));check(len(toc)==38,'Incomplete TOC')
 for n in toc:target=byid[n.attrs['href'][1:]];same(kids(target)[0],content(n))
 faq=[];checked=0
 for article,(title,prose) in zip(articles[1:],sections):
  children=kids(article);same(children[0],title);check(articles.index(article)>0,'Wrong section order')
  if title.startswith('An original Cerchi instrument'):
   check(children[1].tag=='figure','Native instrument missing');prose=prose[prose.index('**Using the instrument.**'):];compare_blocks(children[2:],body_blocks(prose));checked+=1
  elif title=='Frequently asked questions':
   blocks=body_blocks(prose);check(len(blocks)==40,'Expected 20 FAQ headings/answers');qsections=children[1:];check(len(qsections)==20,'Visible FAQ missing')
   for qsection,j in zip(qsections,range(0,40,2)):
    q,a=blocks[j][1],blocks[j+1][1];qnodes=kids(qsection);check(len(qnodes)==2,'FAQ structure changed');same(qnodes[0],q);same(qnodes[1],a);faq.append((normal(content(qnodes[0])),normal(content(qnodes[1]))))
  else:
   expected=body_blocks(prose)
   if title.startswith('10. '):
    check(expected.pop()==('h2','The Atlas desk'),'Missing Atlas separator');same(kids(byid['atlas-desk'])[0],'The Atlas desk')
   compare_blocks(children[1:],expected);checked+=len(expected)
 machine=[(x['name'],x['acceptedAnswer']['text'])for x in newld[2]['mainEntity']];check(newld[2]['@type']=='FAQPage' and faq==machine,'FAQ/schema mismatch')
 check(len(list(byid['working-glossary'].find('tr')))==19,'Expected 18 glossary terms')
 check('Editorial status' not in content(byid['main-content']) and 'During a future approved conversion' not in new,'Internal workflow exposed')
 print(f'PASS Clausewitz EN33: approved SHA256; {checked} ordered content blocks; all inline spans/lists/table/links; 10+25 sections; 38 TOC; 18 terms; 20 exact FAQ; historic anchors/SEO/cover and native diagram protected')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',required=True);a=p.parse_args();verify(ROOT/PAGE,a.base)
