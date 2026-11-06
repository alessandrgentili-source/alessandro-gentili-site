'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const windowHandlers={};
function control(value='') {
  const events={};
  return {value, hidden:false, focused:false, attrs:{}, events, textContent:'',
    addEventListener(name,fn){events[name]=fn;},
    setAttribute(name,val){this.attrs[name]=val;},
    focus(){this.focused=true;},
    closest(){return this.parent;}
  };
}
function row(term,meaning) {
  return {textContent:term+' '+meaning,hidden:false,cells:[{textContent:term},{textContent:meaning}]};
}
function fixture(kind,data){
  const query=control(),sort=control(),reset=control(),count=control();
  const controls={hidden:true};query.parent=controls;
  const rows=data.map(x=>row(x[0],x[1]));
  const tbody={rows:rows.slice(),querySelectorAll(x){assert.equal(x,'tr');return this.rows;},appendChild(x){const i=this.rows.indexOf(x);if(i>=0)this.rows.splice(i,1);this.rows.push(x);}};
  const table={querySelector(x){return x==='tbody'?tbody:null;}};
  return {kind,query,sort,reset,count,controls,rows,tbody,table};
}
const life=fixture('life',[
  ['Megalopolis','Born in Arcadia'],
  ['Pydna','Held after defeat'],
  ['Scipio','Roman political world']]);
const gloss=fixture('glossary',[
  ['Tyche','Fortune'],
  ['Ochlocracy','Démocratic degeneration'],
  ['Anacyclosis','Recurrent constitutional change']]);
const pairs={};for(const f of [life,gloss])for(const part of ['table','query','sort','reset','count'])pairs[`#polybius-${f.kind}-${part}`]=f[part];
const main={querySelector(s){return pairs[s]||null;}};
const document={querySelector(s){return s==='.atlas-polybius .atlas-main'?main:null;}};
const window={addEventListener(name,fn){windowHandlers[name]=fn;}};
vm.runInNewContext(fs.readFileSync('assets/international-polybius.js','utf8'),{document,window});
assert.equal(life.controls.hidden,false);
assert.equal(gloss.controls.hidden,false);
assert.equal(life.count.textContent,'3 of 3 turning points');
assert.equal(gloss.count.textContent,'3 of 3 terms');
life.query.value='pydna';life.query.events.input();
assert.equal(life.rows.filter(x=>!x.hidden).length,1);
assert.match(life.count.textContent,/1 of 3/);
life.sort.events.click();assert.equal(life.tbody.rows[0].cells[0].textContent,'Scipio');
assert.equal(life.sort.attrs['aria-pressed'],'true');
life.reset.events.click();assert.equal(life.query.focused,true);
assert.equal(life.query.value,'');assert.equal(life.tbody.rows[0].cells[0].textContent,'Megalopolis');
gloss.query.value='democratic';gloss.query.events.input();
assert.equal(gloss.rows.filter(x=>!x.hidden).length,1,'accent-insensitive query should match Démocratic');
gloss.sort.events.click();assert.equal(gloss.tbody.rows[0].cells[0].textContent,'Anacyclosis');
gloss.query.value='fortune';gloss.query.events.input();
assert.equal(gloss.rows.filter(x=>!x.hidden).length,1);
windowHandlers.beforeprint();
assert.equal(gloss.rows.filter(x=>!x.hidden).length,3);
assert.equal(gloss.tbody.rows[0].cells[0].textContent,'Tyche');
windowHandlers.afterprint();
assert.equal(gloss.query.value,'fortune');
assert.equal(gloss.tbody.rows[0].cells[0].textContent,'Anacyclosis');
assert.equal(gloss.rows.filter(x=>!x.hidden).length,1);
gloss.reset.events.click();
assert.equal(gloss.count.textContent,'3 of 3 terms');
console.log('PASS Polybius interactions: 2 searchable/sortable tables, diacritics, counts, reset/focus, print restoration');
