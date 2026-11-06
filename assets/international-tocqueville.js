/* The original Tocqueville chronology and glossary remain readable without JavaScript. Progressive search, sort and print state only. */
(() => {
  'use strict';
  const main = document.querySelector('.atlas-tocqueville .atlas-main');
  if (!main) return;
  const normalize = s => s.toLocaleLowerCase('en').normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
  const tables = [];
  for (const kind of ['life', 'glossary']) {
    const table = main.querySelector(`#tocqueville-${kind}-table`);
    const query = main.querySelector(`#tocqueville-${kind}-query`);
    const sort = main.querySelector(`#tocqueville-${kind}-sort`);
    const reset = main.querySelector(`#tocqueville-${kind}-reset`);
    const count = main.querySelector(`#tocqueville-${kind}-count`);
    const controls = query?.closest('.tocqueville-table-tools');
    const body = table?.querySelector('tbody');
    if (!table || !query || !sort || !reset || !count || !controls || !body) continue;
    const rows = Array.from(body.querySelectorAll('tr'));
    const original = rows.slice();
    let sorted = false;
    let savedPrintState = null;
    const filter = () => {
      const search = normalize(query.value);
      let visible = 0;
      for (const row of rows) {
        const match = normalize(row.textContent).includes(search);
        row.hidden = !match;
        if (match) visible++;
      }
      count.textContent = `${visible} of ${rows.length} ${kind === 'life' ? 'turning points' : 'terms'}`;
    };
    const reorder = () => {
      const order = sorted ? original.slice().sort((a, b) => kind === 'life'
        ? Number(b.dataset.originalIndex) - Number(a.dataset.originalIndex)
        : normalize(a.cells[0].textContent).localeCompare(normalize(b.cells[0].textContent), 'en')) : original;
      order.forEach(row => body.appendChild(row));
      sort.setAttribute('aria-pressed', String(sorted));
      sort.textContent = kind === 'life' ? (sorted ? 'Earliest first' : 'Latest first') : (sorted ? 'Original order' : 'Sort A–Z');
      filter();
    };
    const clear = () => { query.value = ''; sorted = false; reorder(); };
    query.addEventListener('input', filter);
    sort.addEventListener('click', () => { sorted = !sorted; reorder(); });
    reset.addEventListener('click', () => { clear(); query.focus(); });
    controls.hidden = false;
    reorder();
    tables.push({
      beforePrint() {
        savedPrintState = {search: query.value, sorted};
        clear();
      },
      afterPrint() {
        if (!savedPrintState) return;
        query.value = savedPrintState.search;
        sorted = savedPrintState.sorted;
        savedPrintState = null;
        reorder();
      }
    });
  }
  window.addEventListener('beforeprint', () => tables.forEach(t => t.beforePrint()));
  window.addEventListener('afterprint', () => tables.forEach(t => t.afterPrint()));
})();
