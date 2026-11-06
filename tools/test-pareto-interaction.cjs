'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const handlers = {};
const selectMap = new Map();
const mains = {};
const makeControl = () => ({
  value:'', textContent:'', hidden:true, focused:false, attrs:{}, events:{},
  addEventListener(name,fn){ this.events[name]=fn; },
  setAttribute(name,val){ this.attrs[name]=val; },
  focus(){ this.focused=true; },
  closest(){ return this.controls; },
  click(){ this.events.click?.(); },
  input(value){ this.value=value;this.events.input?.(); }
});
function setup(kind,source) {
  const controls=makeControl();const query=makeControl();query.controls=controls;
  const sort=makeControl(),reset=makeControl(),count=makeControl();
  const rows=source.map((text,i)=>({textContent:text,hidden:false,cells:[{textContent:text.split(' · ')[0]}],dataset:{originalIndex:String(i+1)}}));
  const tbody={rows:rows.slice(),querySelectorAll(sel){assert.equal(sel,'tr');return this.rows;},appendChild(row){this.rows=this.rows.filter(x=>x!==row);this.rows.push(row);}};
  const table={querySelector(sel){assert.equal(sel,'tbody');return tbody;}};
  for(const [name,value] of Object.entries({table,query,sort,reset,count}))mains[`#pareto-${kind}-${name==='table'?'table':name}`]=value;
  return {kind,table,query,sort,reset,count,controls,tbody,rows};
}
const life=setup('life',['Paris · 1848 and revolution','Turin · engineering and railways','Italy · free trade disputes','Lausanne · economics 1893','Céligny · sociological treatise','Céligny · death 1923']);
const glossary=setup('glossary',['Residues · enduring inferred elements','Élite · governing few','Action · logical and non-logical','Foxes · political flexibility','Derivations · public reasons','Circulation · movement']);
const main={querySelector(sel){ return mains[sel]??null;}};
const document={querySelector(sel){assert.equal(sel,'.atlas-pareto .atlas-main');return main;}};
const window={addEventListener(name,fn){handlers[name]=fn;}};
vm.runInNewContext(fs.readFileSync('assets/international-pareto.js','utf8'),{document,window,console});
assert.equal(life.controls.hidden,false);
assert.equal(glossary.controls.hidden,false);
assert.match(life.count.textContent,/6 of 6/);
assert.match(glossary.count.textContent,/6 of 6/);
glossary.query.input('elite');
assert.equal(glossary.rows.filter(x=>!x.hidden).length,1,'Accent-insensitive search should match Élite');
assert.equal(glossary.count.textContent,'1 of 6 terms');
glossary.query.input('not-present');
assert.equal(glossary.count.textContent,'0 of 6 terms');
glossary.reset.click();
assert.equal(glossary.count.textContent,'6 of 6 terms');
assert(glossary.query.focused,'Reset restores keyboard focus');
glossary.sort.click();
assert.equal(glossary.sort.attrs['aria-pressed'],'true');
assert.equal(glossary.tbody.rows[0].textContent,'Action · logical and non-logical');
assert.equal(glossary.tbody.rows[5].textContent,'Residues · enduring inferred elements');
glossary.sort.click();
assert.equal(glossary.tbody.rows[0].textContent,'Residues · enduring inferred elements');
life.sort.click();
assert.equal(life.tbody.rows[0].textContent,'Céligny · death 1923');
life.query.input('laUSANNE');
assert.equal(life.count.textContent,'1 of 6 transitions');
life.sort.click();
life.query.input('italy');
glossary.query.input('foxes');
glossary.sort.click();
handlers.beforeprint();
assert.equal(life.count.textContent,'6 of 6 transitions');
assert.equal(glossary.count.textContent,'6 of 6 terms');
assert.equal(life.query.value,'');
assert.equal(glossary.query.value,'');
handlers.afterprint();
assert.equal(life.query.value,'italy');
assert.equal(glossary.query.value,'foxes');
assert.equal(life.count.textContent,'1 of 6 transitions');
assert.equal(glossary.count.textContent,'1 of 6 terms');
assert.equal(glossary.sort.attrs['aria-pressed'],'true');
console.log('PASS Pareto interactions: 2 tables, diacritics, sort/reverse, zero hits, reset/focus, print and state restoration');
