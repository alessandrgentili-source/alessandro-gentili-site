/* Node DOM fixture: real Tocqueville JS; search, sort, reset, print, accents, focus. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const listeners = {};
const all = {};
const counts = {};
function fixture(kind, arr) {
  const key = kind;
  const rows = arr.map((text,i) => ({textContent:text, hidden:false, dataset:{originalIndex:String(i)}, cells:[{textContent:text.split(' — ')[0]}]}));
  const orig = rows.slice();
  const tbody = {
    items:orig.slice(),
    querySelectorAll(q) {assert.equal(q,'tr'); return orig;},
    appendChild(row){this.items=this.items.filter(x=>x!==row);this.items.push(row);}
  };
  const controls={hidden:true};
  const query={value:'',focused:false,closest(s){assert.equal(s,'.tocqueville-table-tools');return controls;},
    addEventListener(s,fn){listeners[key+':query:'+s]=fn;},focus(){this.focused=true;}};
  const sort={textContent:'',attrs:{},addEventListener(s,fn){listeners[key+':sort:'+s]=fn;},setAttribute(k,v){this.attrs[k]=v;}};
  const reset={addEventListener(s,fn){listeners[key+':reset:'+s]=fn;}};
  const count={textContent:''};
  const table={querySelector(s){assert.equal(s,'tbody');return tbody;}};
  Object.assign(all, {
    [`#tocqueville-${key}-table`]:table,
    [`#tocqueville-${key}-query`]:query,
    [`#tocqueville-${key}-sort`]:sort,
    [`#tocqueville-${key}-reset`]:reset,
    [`#tocqueville-${key}-count`]:count
  });
  counts[key]={rows,tbody,controls,query,sort,reset,count};
}
fixture('life',['1805 — Born into French aristocracy','1835 — Democracy in America','1856 — The Old Regime and the Revolution']);
fixture('glossary',['Mores — shared moral habits','Association — association and fairness','Individualism — withdrawal from public life']);
const main={querySelector(q){return all[q]||null;}};
const document={querySelector(q){return q==='.atlas-tocqueville .atlas-main'?main:null;}};
const window={addEventListener(event,fn){listeners['window:'+event]=fn;}};
vm.runInNewContext(fs.readFileSync('assets/international-tocqueville.js','utf8'),{document,window});
assert.equal(counts.life.controls.hidden,false);
assert.equal(counts.glossary.controls.hidden,false);
assert.equal(counts.life.count.textContent,'3 of 3 turning points');
assert.equal(counts.glossary.count.textContent,'3 of 3 terms');
counts.glossary.query.value='ASSOCIATION'; listeners['glossary:query:input']();
assert.equal(counts.glossary.rows.filter(r=>!r.hidden).length,1); // accent and case insensitive
counts.glossary.query.value='association'; listeners['glossary:query:input']();
assert.equal(counts.glossary.rows.filter(r=>!r.hidden).length,1);
counts.glossary.query.value='ASSOCIATION'; listeners['glossary:query:input']();
assert.equal(counts.glossary.rows.filter(r=>!r.hidden).length,1);
counts.glossary.query.value='ASSOCIATION'; listeners['glossary:query:input']();
assert.equal(counts.glossary.rows.filter(r=>!r.hidden).length,1);
listeners['glossary:sort:click']();
assert.equal(counts.glossary.sort.attrs['aria-pressed'],'true');
assert.equal(counts.glossary.tbody.items[0].textContent.startsWith('Association'),true);
listeners['glossary:reset:click']();
assert.equal(counts.glossary.query.value,'');
assert.equal(counts.glossary.query.focused,true);
assert.equal(counts.glossary.count.textContent,'3 of 3 terms');
counts.life.query.value='1835';listeners['life:query:input']();
assert.equal(counts.life.rows.filter(r=>!r.hidden).length,1);
listeners['life:sort:click']();
assert.equal(counts.life.tbody.items[0].textContent.startsWith('1856'),true);
listeners['window:beforeprint']();
assert.equal(counts.life.rows.every(r=>!r.hidden),true);
assert.equal(counts.glossary.rows.every(r=>!r.hidden),true);
listeners['window:afterprint']();
assert.equal(counts.life.rows.filter(r=>!r.hidden).length,1);
assert.equal(counts.life.sort.attrs['aria-pressed'],'true');
assert.equal(counts.life.query.value,'1835');
console.log('PASS Tocqueville interactions: two searchable/sortable tables, accents, count, reset/focus, print and state restoration');
