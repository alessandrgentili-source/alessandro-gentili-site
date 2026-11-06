#!/usr/bin/env node
/* Thucydides EN31: DOM harness for progressive table search/order/print.
   This tests control logic, not genuine browser layout, touch or screen readers. */
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const assert = require("node:assert/strict");
class Control {
 constructor(value="") { this.value=value; this.listeners={}; this.focused=false; }
 addEventListener(type,callback) { this.listeners[type]=callback; }
 dispatch(type) { assert.equal(typeof this.listeners[type],"function"); this.listeners[type]({type}); }
 focus() { this.focused=true; }
}
function fixture(key,count,entries) {
 const rows = Array.from({length:count},(_,i)=>{
   const entry=entries[i]||{time:0,text:"Reference "+i};
   return {dataset:{timeKey:String(entry.time),sourceIndex:String(i)},
     textContent:entry.text,hidden:false};
 });
 const tbody={rows:[...rows],append(...r){this.rows=[...r]}};
 const search=new Control(),order=key==="glossary"?null:new Control("source"),reset=new Control();
 const countLabel={textContent:""}, head={attributes:{},setAttribute(k,v){this.attributes[k]=v}};
 const panel={hidden:true,querySelector(s) {
  if(s==='input[type="search"]')return search;
  if(s==="select")return order;
  if(s==="button")return reset;
  if(s==='[role="status"]')return countLabel;
  throw Error(s);
 }};
 const table={tBodies:[tbody],querySelector:()=>head};
 return {key,rows,tbody,search,order,reset,countLabel,head,panel,table};
}
const life=fixture("life",11,[
 {time:-431,text:"431 BCE Peloponnesian War begins"},
 {time:-430,text:"430 BCE Plague Athens"},
 {time:-427,text:"427 BCE Mytilene debate"},
 {time:-427,text:"427 BCE Corcyra violence"},
 {time:-424,text:"424 BCE Amphipolis exile"},
 {time:-421,text:"421 BCE Peace"},
 {time:-416,text:"416 BCE Melos"},
 {time:-415,text:"415 BCE Sicily begins"},
 {time:-413,text:"413 BCE Sicily catastrophe"},
 {time:-411,text:"411 BCE narrative stops"},
 {time:-404,text:"404 BCE Athens defeated"}
]);
const works=fixture("works",8,[
 {time:0,text:"Book I causes of war"}, {time:1,text:"Book II funeral plague"},
 {time:2,text:"Book III Mytilene Corcyra"}, {time:3,text:"Book IV Amphipolis"},
 {time:4,text:"Book V Melos"}, {time:5,text:"Book VI Sicily"},
 {time:6,text:"Book VII Syracuse"}, {time:7,text:"Book VIII constitutional crisis"}
]);
const glossary=fixture("glossary",24,[
 {time:0,text:"Aitia cause"}, {time:1,text:"Ananke necessity"},
 {time:2,text:"Demos people"}, {time:3,text:"Empire"}
]);
const data={life,works,glossary};
const main={querySelector(s){
 const controls=s.match(/^\[data-thucydides-controls="(.*?)"\]$/);
 if(controls)return data[controls[1]]?.panel||null;
 const table=s.match(/^#thucydides-(.*?)-table$/);
 if(table)return data[table[1]]?.table||null;
 return null;
}};
const windowEvents={};let mediaChange;
const window={
 addEventListener(k,fn){windowEvents[k]=fn},
 matchMedia:()=>({addEventListener(k,fn){assert.equal(k,"change");mediaChange=fn;}})
};
const document={querySelector:s=>s===".atlas-thucydides-v3 .atlas-main"?main:null};
const script=fs.readFileSync(path.resolve(__dirname,"../assets/international-thucydides.js"),"utf8");
vm.runInNewContext(script,{window,document,console});
for(const x of Object.values(data)) {
 assert.equal(x.panel.hidden,false,x.key+" controls must appear with JS");
 const units=x.key==="life"?"events":x.key==="works"?"books":"terms";
 assert.equal(x.countLabel.textContent,x.rows.length+" of "+x.rows.length+" "+units);
 assert(x.rows.every(row=>!row.hidden),x.key+" all source rows initially visible");
}
life.search.value="Mytilene";life.search.dispatch("input");
assert.equal(life.rows.filter(row=>!row.hidden).length,1);
assert.equal(life.countLabel.textContent,"1 of 11 events");
life.order.value="desc";life.order.dispatch("change");
assert.equal(life.tbody.rows[0].dataset.timeKey,"-404");
assert.equal(life.head.attributes["aria-sort"],"descending");
life.order.value="asc";life.order.dispatch("change");
assert.equal(life.tbody.rows[0].dataset.timeKey,"-431");
works.order.value="desc";works.order.dispatch("change");
assert.equal(works.tbody.rows[0].dataset.sourceIndex,"7");
works.search.value="Melos";works.search.dispatch("input");
assert.equal(works.countLabel.textContent,"1 of 8 books");
glossary.search.value="anankE";glossary.search.dispatch("input");
assert.equal(glossary.countLabel.textContent,"1 of 24 terms");
glossary.search.value="nothing-like-this";glossary.search.dispatch("input");
assert.equal(glossary.countLabel.textContent,"0 of 24 terms");
assert.equal(typeof windowEvents.beforeprint,"function");
windowEvents.beforeprint();
for(const x of Object.values(data)){
 assert(x.rows.every(row=>!row.hidden),x.key+" all rows must print");
 assert.deepEqual(x.tbody.rows.map(r=>r.dataset.sourceIndex),x.rows.map(r=>r.dataset.sourceIndex),x.key+" print original order");
}
windowEvents.afterprint();
assert.equal(glossary.rows.filter(r=>!r.hidden).length,0);
assert.equal(works.tbody.rows[0].dataset.sourceIndex,"7");
assert.equal(life.tbody.rows[0].dataset.timeKey,"-431");
life.reset.dispatch("click");
assert.equal(life.search.value,"");
assert.equal(life.order.value,"source");
assert(life.rows.every(r=>!r.hidden));
assert.equal(life.tbody.rows[0].dataset.sourceIndex,"0");
assert(life.search.focused);
assert.equal(typeof mediaChange,"function");
mediaChange({matches:true});
assert(Object.values(data).every(x=>x.rows.every(row=>!row.hidden)));
mediaChange({matches:false});
assert.equal(glossary.rows.filter(r=>!r.hidden).length,0);
console.log("PASS Thucydides EN31: three table searches, BCE/book sorting, reset/focus, no-results feedback, full print state and restoration (DOM harness)");
