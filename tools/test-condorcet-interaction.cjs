'use strict';
// Dependency-free test of the *actual shipped script* against a minimal eventful DOM.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const events={};
const makeNode=(initial='')=>({value:initial,textContent:'',attrs:{},dataset:{},hidden:true,focused:false,listeners:{},
  addEventListener(type,fn){this.listeners[type]=fn},click(){this.listeners.click?.()},dispatch(type){this.listeners[type]?.()},focus(){this.focused=true},
  setAttribute(key,v){this.attrs[key]=v},getAttribute(key){return this.attrs[key]}});
const map={},main={querySelector(s){return map[s]??null}};
const tables=[];
for(const kind of ['life','glossary']){
  const raw=kind==='life'?[['1743–1765','A talent formed within the old order'],['1793–1794','Concealment and a future history']]:
    [['Agenda','The order of choices'],['Perfectibilité','The possibility of improvement']];
  const rows=raw.map((x,i)=>({textContent:x.join(' '),cells:[{textContent:x[0]},{textContent:x[1]}],dataset:{originalIndex:String(i)},hidden:false}));
  const body={items:rows.slice(),querySelectorAll(s){return s==='tr'?this.items:[]},appendChild(row){this.items=this.items.filter(x=>x!==row);this.items.push(row)}};
  const controls=makeNode();const query=makeNode('');query.closest=()=>controls;
  const sort=makeNode(),reset=makeNode(),count=makeNode();
  const table={querySelector(s){return s==='tbody'?body:null}};
  Object.assign(map,{[`#condorcet-${kind}-table`]:table,[`#condorcet-${kind}-query`]:query,[`#condorcet-${kind}-sort`]:sort,[`#condorcet-${kind}-reset`]:reset,[`#condorcet-${kind}-count`]:count});
  tables.push({kind,rows,query,sort,reset,count,controls,body});
}
const votingRows=[['1','A','B','C'],['2','B','C','A'],['3','C','A','B']].map(rank=>({cells:rank.map(textContent=>({textContent})),dataset:{}}));
const votingTable={querySelectorAll(s){return s==='tbody tr'?votingRows:[]}};
const buttons=['AB','BC','CA'].map(pair=>{const b=makeNode();b.dataset.pair=pair;return b});
const votingControls=makeNode();votingControls.querySelectorAll=s=>s==='button[data-pair]'?buttons:[];
const voteResult=makeNode();
const prob=makeNode('60'),jurors=makeNode('3'),probDisplay=makeNode(),majority=makeNode(),calc=makeNode(),instrument=makeNode();
Object.assign(map,{'#condorcet-vote-table':votingTable,'.condorcet-vote-tools':votingControls,'#condorcet-vote-result':voteResult,
  '#condorcet-probability':prob,'#condorcet-jurors':jurors,'#condorcet-prob-display':probDisplay,'#condorcet-majority-result':majority,
  '.condorcet-calculator':calc,'#condorcet-instrument':instrument});
const document={querySelector(s){return s==='.atlas-condorcet .atlas-main'?main:null}};
const window={addEventListener(type,fn){events[type]=fn}};
const script=fs.readFileSync('assets/international-condorcet.js','utf8');
vm.runInNewContext(script,{document,window});
for(const t of tables){assert.equal(t.controls.hidden,false);assert.match(t.count.textContent,/2 of 2/);}
let t=tables[1];t.query.value='perfectibilite';t.query.dispatch('input');assert.equal(t.rows[0].hidden,true);assert.equal(t.rows[1].hidden,false);assert.match(t.count.textContent,/1 of 2/);
t.sort.click();assert.equal(t.sort.getAttribute('aria-pressed'),'true');t.reset.click();assert.equal(t.query.value,'');assert.equal(t.rows[0].hidden,false);assert.equal(t.rows[1].hidden,false);assert.equal(t.reset.focused,false);assert.equal(t.query.focused,true);
t=tables[0];t.sort.click();assert.equal(t.body.items[0],t.rows[1]);t.query.value='1793';t.query.dispatch('input');assert.equal(t.rows[0].hidden,true);
buttons[0].click();assert.equal(voteResult.textContent,'A defeats B by 2 votes to 1.');
buttons[1].click();assert.equal(voteResult.textContent,'B defeats C by 2 votes to 1.');
buttons[2].click();assert.equal(voteResult.textContent,'C defeats A by 2 votes to 1.');
assert.equal(buttons[2].getAttribute('aria-pressed'),'true');
assert.equal(calc.hidden,false);assert.equal(majority.textContent,'64.8%');prob.value='40';prob.dispatch('input');assert.equal(majority.textContent,'35.2%');
jurors.value='9';jurors.dispatch('change');assert.equal(majority.textContent,'26.7%');
assert.equal(instrument.dataset.enhanced,'true');
events.beforeprint();assert.equal(t.query.value,'');assert.equal(t.rows[0].hidden,false);events.afterprint();assert.equal(t.query.value,'1793');assert.equal(t.rows[0].hidden,true);assert.equal(t.body.items[0],t.rows[1]);
console.log('PASS Condorcet interactions: 2 search/sort/reset tables, accents, 3 pairwise votes, p/n calculator, no-JS enhancement, print restoration');
