/* Progressive enhancement: original source tables remain completely readable without JavaScript. */
(() => {
  'use strict';
  const main = document.querySelector('.atlas-polybius .atlas-main');
  if (!main) return;
  const norm = text => String(text).toLocaleLowerCase('en').normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
  const active = [];
  for (const kind of ['life', 'glossary']) {
    const table = main.querySelector(`#polybius-${kind}-table`);
    const query = main.querySelector(`#polybius-${kind}-query`);
    const sort = main.querySelector(`#polybius-${kind}-sort`);
    const reset = main.querySelector(`#polybius-${kind}-reset`);
    const count = main.querySelector(`#polybius-${kind}-count`);
    const controls = query?.closest('.polybius-table-tools');
    const tbody = table?.querySelector('tbody');
    if (!table || !query || !sort || !reset || !count || !controls || !tbody) continue;
    const original = Array.from(tbody.querySelectorAll('tr'));
    let reversedOrAlphabetical = false;
    let printSnapshot = null;
    function filter() {
      const needle = norm(query.value);
      let n = 0;
      for (const row of original) {
        const matches = norm(row.textContent).includes(needle);
        row.hidden = !matches;
        if (matches) n++;
      }
      count.textContent = `${n} of ${original.length} ${kind === 'life' ? 'turning points' : 'terms'}`;
    }
    function reorder() {
      const rows = reversedOrAlphabetical
        ? (kind === 'life' ? original.slice().reverse() : original.slice().sort((a,b) => norm(a.cells[0].textContent).localeCompare(norm(b.cells[0].textContent),'en')))
        : original;
      rows.forEach(row => tbody.appendChild(row));
      sort.setAttribute('aria-pressed', String(reversedOrAlphabetical));
      sort.textContent = kind === 'life' ? (reversedOrAlphabetical ? 'Original order' : 'Reverse order') : (reversedOrAlphabetical ? 'Original order' : 'Sort A–Z');
      filter();
    }
    function clear() { query.value=''; reversedOrAlphabetical=false; reorder(); }
    query.addEventListener('input', filter);
    sort.addEventListener('click', () => { reversedOrAlphabetical = !reversedOrAlphabetical; reorder(); });
    reset.addEventListener('click', () => { clear(); query.focus(); });
    controls.hidden = false;
    reorder();
    active.push({
      beforePrint() { printSnapshot = { search: query.value, sorted: reversedOrAlphabetical }; clear(); },
      afterPrint() { if (!printSnapshot) return; query.value=printSnapshot.search; reversedOrAlphabetical=printSnapshot.sorted; printSnapshot=null; reorder(); }
    });
  }
  window.addEventListener('beforeprint', () => active.forEach(x => x.beforePrint()));
  window.addEventListener('afterprint', () => active.forEach(x => x.afterPrint()));
})();
