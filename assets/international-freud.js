/* Freud EN 10: progressive glossary search. Without JS every definition remains visible. */
(()=>{
  'use strict';
  const root=document.querySelector('.international-atlas.atlas-freud');
  if(!root)return;
  const widget=root.querySelector('.freud-glossary-widget');
  if(!widget)return;
  const input=widget.querySelector('#freud-glossary-query');
  const reset=widget.querySelector('#freud-glossary-reset');
  const status=widget.querySelector('#freud-glossary-status');
  const rows=[...widget.querySelectorAll('#freud-glossary-table tbody tr')];
  if(!input||!reset||!status||!rows.length)return;
  const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
  const contents=rows.map(row=>normalize(row.textContent));
  const filter=()=>{
    const term=normalize(input.value);
    let shown=0;
    rows.forEach((row,i)=>{
      row.hidden=!!term&&!contents[i].includes(term);
      if(!row.hidden)shown++;
    });
    status.textContent=term?`${shown} of ${rows.length} glossary entries shown.`:`All ${rows.length} glossary entries shown.`;
    reset.hidden=!term;
  };
  input.hidden=false;
  status.hidden=false;
  reset.hidden=true;
  input.addEventListener('input',filter);
  reset.addEventListener('click',()=>{input.value='';filter();input.focus()});
  window.addEventListener('beforeprint',()=>{rows.forEach(row=>row.hidden=false)});
  window.addEventListener('afterprint',filter);
  filter();
})();
