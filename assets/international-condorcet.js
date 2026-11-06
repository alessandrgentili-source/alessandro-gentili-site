/* Condorcet's actual ranked voters and source glossary: progressive, accessible, reversible. */
(() => {
  'use strict';
  const main = document.querySelector('.atlas-condorcet .atlas-main');
  if (!main) return;
  const norm = s => String(s).toLocaleLowerCase('en').normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
  const printRestorers = [];
  for (const kind of ['life', 'glossary']) {
    const table = main.querySelector(`#condorcet-${kind}-table`);
    const search = main.querySelector(`#condorcet-${kind}-query`);
    const sort = main.querySelector(`#condorcet-${kind}-sort`);
    const reset = main.querySelector(`#condorcet-${kind}-reset`);
    const count = main.querySelector(`#condorcet-${kind}-count`);
    const controls = search?.closest('.condorcet-table-tools');
    const tbody = table?.querySelector('tbody');
    if (!table || !search || !sort || !reset || !count || !controls || !tbody) continue;
    const original = Array.from(tbody.querySelectorAll('tr'));
    let sorted = false;
    let snapshot = null;
    const update = () => {
      const q = norm(search.value);
      let visible = 0;
      original.forEach(row => {row.hidden = !norm(row.textContent).includes(q);if (!row.hidden) visible++;});
      count.textContent = `${visible} of ${original.length} ${kind === 'life' ? 'turning points' : 'terms'}`;
    };
    const reorder = () => {
      const ordered = sorted ? original.slice().sort((a,b) => kind === 'life'
        ? Number(b.dataset.originalIndex)-Number(a.dataset.originalIndex)
        : norm(a.cells[0].textContent).localeCompare(norm(b.cells[0].textContent),'en')) : original;
      ordered.forEach(row => tbody.appendChild(row));
      sort.setAttribute('aria-pressed',String(sorted));
      sort.textContent = kind === 'life' ? (sorted?'Original order':'Reverse order') : (sorted?'Original order':'Sort A–Z');
      update();
    };
    const clear = () => {search.value='';sorted=false;reorder();};
    search.addEventListener('input',update);
    sort.addEventListener('click',() => {sorted=!sorted;reorder();});
    reset.addEventListener('click',() => {clear();search.focus();});
    controls.hidden=false;
    reorder();
    printRestorers.push({beforePrint(){snapshot={query:search.value,sorted};clear();},afterPrint(){if(!snapshot)return;search.value=snapshot.query;sorted=snapshot.sorted;snapshot=null;reorder();}});
  }
  const votingTable = main.querySelector('#condorcet-vote-table');
  const voteCtrl = main.querySelector('.condorcet-vote-tools');
  const voteButtons = voteCtrl ? Array.from(voteCtrl.querySelectorAll('button[data-pair]')) : [];
  const voteOutput = main.querySelector('#condorcet-vote-result');
  const votes = votingTable ? Array.from(votingTable.querySelectorAll('tbody tr')) : [];
  if (voteCtrl && voteButtons.length===3 && voteOutput && votes.length===3) {
    const compare = pair => {
      const [a,b] = pair.split('');
      let aVotes=0,bVotes=0;
      for(const row of votes){
        const ranking=Array.from(row.cells).slice(1).map(cell=>cell.textContent.trim());
        const pref=ranking.indexOf(a)<ranking.indexOf(b)?a:b;
        row.dataset.supports = pref===a?'first':'second';
        if(pref===a)aVotes++;else bVotes++;
      }
      voteOutput.textContent = `${aVotes>bVotes?a:b} defeats ${aVotes>bVotes?b:a} by ${Math.max(aVotes,bVotes)} votes to ${Math.min(aVotes,bVotes)}.`;
      voteButtons.forEach(btn=>btn.setAttribute('aria-pressed',String(btn.dataset.pair===pair)));
    };
    voteButtons.forEach(btn=>btn.addEventListener('click',()=>compare(btn.dataset.pair)));
    voteCtrl.hidden=false;
    compare('AB');
  }
  const pInput=main.querySelector('#condorcet-probability');
  const nInput=main.querySelector('#condorcet-jurors');
  const pOutput=main.querySelector('#condorcet-prob-display');
  const answer=main.querySelector('#condorcet-majority-result');
  const calc=main.querySelector('.condorcet-calculator');
  if(pInput&&nInput&&pOutput&&answer&&calc){
    const binom=(n,k) => {let c=1;for(let i=1;i<=k;i++)c=c*(n-i+1)/i;return c;};
    const update=()=>{
      const p=Number(pInput.value)/100,n=Number(nInput.value);
      if(!Number.isInteger(n)||n%2!==1||n<3||n>9||p<0||p>1)return;
      let correct=0;for(let k=(n+1)/2;k<=n;k++)correct+=binom(n,k)*(p**k)*((1-p)**(n-k));
      pOutput.textContent=`${Math.round(p*100)}%`;
      answer.textContent=`${(correct*100).toFixed(1)}%`;
    };
    pInput.addEventListener('input',update);nInput.addEventListener('change',update);
    calc.hidden=false;update();
  }
  const instrument=main.querySelector('#condorcet-instrument');
  if(instrument)instrument.dataset.enhanced='true';
  window.addEventListener('beforeprint',()=>{printRestorers.forEach(t=>t.beforePrint());votes.forEach(r=>delete r.dataset.supports);});
  window.addEventListener('afterprint',()=>{printRestorers.forEach(t=>t.afterPrint());if(voteButtons.length===3){const pressed=voteButtons.find(b=>b.getAttribute('aria-pressed')==='true');pressed?.click();}});
})();
