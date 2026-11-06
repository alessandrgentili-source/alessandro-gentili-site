/* Mosca EN20: progressive interactions over the original source tables.
   Without JavaScript all rows and the native seven-station audit remain available. */
(() => {
 'use strict';
 const main=document.querySelector('.atlas-mosca .atlas-main');
 if(!main)return;
 const normalize=s=>String(s).toLocaleLowerCase('en').normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim();
 const widgets=[];
 for(const kind of ['life','glossary']){
  const table=main.querySelector(`#mosca-${kind}-table`);
  const input=main.querySelector(`#mosca-${kind}-query`);
  const sort=main.querySelector(`#mosca-${kind}-sort`);
  const reset=main.querySelector(`#mosca-${kind}-reset`);
  const count=main.querySelector(`#mosca-${kind}-count`);
  const controls=input?.closest('.mosca-table-tools');
  const tbody=table?.querySelector('tbody');
  if(!table||!input||!sort||!reset||!count||!controls||!tbody)continue;
  const original=Array.from(tbody.querySelectorAll('tr'));
  let sorted=false, printState=null;
  const apply=()=>{
   const q=normalize(input.value);
   let shown=0;
   for(const row of original){
    const visible=normalize(row.textContent).includes(q);
    row.hidden=!visible;if(visible)shown++;
   }
   count.textContent=`${shown} of ${original.length} ${kind==='life'?'turning points':'terms'}`;
  };
  const reorder=()=>{
   const next=sorted?original.slice().sort((a,b)=>kind==='life'
    ?Number(b.dataset.originalIndex)-Number(a.dataset.originalIndex)
    :normalize(a.cells[0].textContent).localeCompare(normalize(b.cells[0].textContent),'en')):original;
   next.forEach(row=>tbody.appendChild(row));
   sort.setAttribute('aria-pressed',String(sorted));
   sort.textContent=kind==='life'?(sorted?'Earliest first':'Latest first'):(sorted?'Original order':'Sort A–Z');
   apply();
  };
  const clear=()=>{input.value='';sorted=false;reorder();};
  input.addEventListener('input',apply);
  sort.addEventListener('click',()=>{sorted=!sorted;reorder();});
  reset.addEventListener('click',()=>{clear();input.focus();});
  controls.hidden=false;reorder();
  widgets.push({
   beforePrint(){printState={search:input.value,sorted};clear();},
   afterPrint(){if(!printState)return;input.value=printState.search;sorted=printState.sorted;printState=null;reorder();}
  });
 }
 window.addEventListener('beforeprint',()=>widgets.forEach(w=>w.beforePrint()));
 window.addEventListener('afterprint',()=>widgets.forEach(w=>w.afterPrint()));
})();
