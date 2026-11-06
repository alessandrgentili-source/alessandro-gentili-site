'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const repositoryScript=path.join(__dirname,'../assets/international-mosca.js');
const scriptPath=fs.existsSync(repositoryScript)?repositoryScript:path.join(__dirname,'international-mosca.js');
const code=fs.readFileSync(scriptPath,'utf8');
function eventable(node={}){const handlers={};node.addEventListener=(ev,cb)=>{handlers[ev]=cb};node.trigger=ev=>{assert.ok(handlers[ev],`listener ${ev}`);handlers[ev]()};return node}
function setup(kind,values){
 const list=values.map((t,i)=>({textContent:t,hidden:false,cells:[{textContent:t.split('|')[0]}],dataset:{originalIndex:String(i+1)}}));
 const tbody={ordered:list.slice(),querySelectorAll:()=>list.slice(),appendChild(row){this.ordered=this.ordered.filter(x=>x!==row);this.ordered.push(row)}};
 const table={querySelector:sel=>sel==='tbody'?tbody:null};const controls={hidden:true};
 const input=eventable({value:'',focused:false,focus(){this.focused=true},closest:()=>controls});
 const sort=eventable({attrs:{},setAttribute(k,v){this.attrs[k]=v},textContent:''});
 const reset=eventable({});const count={textContent:''};
 return {kind,list,tbody,controls,input,sort,reset,count,table};
}
const life=setup('life',['Palermo|Born in Palermo','The first attack|1884 and 1896','The public intellectual|elected deputy','The enlarged political science|senator','From expectation|Fascism 1925','Late scholarship and death|Rome 1941']);
const gloss=setup('glossary',['Political class|power','Governing minority|groups','Organized minority|organization','Dispersed majority|dispersion','Political formula|legitimacy','Legitimation|justification','Autocratic principle|top down','Liberal principle|bottom up','Aristocratic tendency|hereditary','Democratic tendency|access','Co-optation|entry','Renewal|change','Representative government|elections','Juridical defence|difesa giuridica','State bureaucracy|administration','Political recruitment|selection','Formal sovereignty|claims','Effective government|actual','Functional feudalism|privilege','Institutional restraint|limits','Party organization|parties','Social independence|resources','Elite circulation|Pareto','Freedom of opposition|dissent']);
const tables={life,glossary:gloss};
const main={querySelector(selector){const m=selector.match(/^#mosca-(life|glossary)-(table|query|sort|reset|count)$/);return m?tables[m[1]][({table:'table',query:'input',sort:'sort',reset:'reset',count:'count'})[m[2]]]:null}};
const window=eventable({});const document={querySelector:sel=>sel==='.atlas-mosca .atlas-main'?main:null};
vm.runInNewContext(code,{window,document,console});
assert.equal(life.controls.hidden,false);assert.equal(gloss.controls.hidden,false);
assert.equal(gloss.count.textContent,'24 of 24 terms');assert.equal(life.count.textContent,'6 of 6 turning points');
gloss.input.value='dÍFESA';gloss.input.trigger('input');assert.equal(gloss.count.textContent,'1 of 24 terms');assert.equal(gloss.list.filter(x=>!x.hidden)[0].textContent.startsWith('Juridical'),true);
gloss.input.value='no match';gloss.input.trigger('input');assert.equal(gloss.count.textContent,'0 of 24 terms');
gloss.reset.trigger('click');assert.equal(gloss.count.textContent,'24 of 24 terms');assert.equal(gloss.input.focused,true);
gloss.sort.trigger('click');assert.equal(gloss.tbody.ordered[0].cells[0].textContent,'Aristocratic tendency');assert.equal(gloss.sort.attrs['aria-pressed'],'true');
gloss.sort.trigger('click');assert.equal(gloss.tbody.ordered[0].cells[0].textContent,'Political class');
life.sort.trigger('click');assert.equal(life.tbody.ordered[0].cells[0].textContent,'Late scholarship and death');
life.input.value='1884';life.input.trigger('input');assert.equal(life.count.textContent,'1 of 6 turning points');
window.trigger('beforeprint');assert.equal(life.count.textContent,'6 of 6 turning points');assert.equal(gloss.count.textContent,'24 of 24 terms');
window.trigger('afterprint');assert.equal(life.count.textContent,'1 of 6 turning points');assert.equal(life.tbody.ordered[0].cells[0].textContent,'Late scholarship and death');
life.reset.trigger('click');assert.equal(life.count.textContent,'6 of 6 turning points');assert.equal(life.input.focused,true);
console.log('PASS Mosca interactions: two searchable/sortable tables, diacritics, counts, reset/focus, print restoration');
