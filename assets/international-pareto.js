/* Source-faithful progressive tables. The full text remains readable without JavaScript. */
(() => {
  'use strict';
  const main = document.querySelector('.atlas-pareto .atlas-main');
  if (!main) return;
  const norm = text => String(text).toLocaleLowerCase('en').normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
  const active = [];
  for (const kind of ['life','glossary']) {
    const table = main.querySelector(`#pareto-${kind}-table`);
    const query = main.querySelector(`#pareto-${kind}-query`);
    const sort = main.querySelector(`#pareto-${kind}-sort`);
    const reset = main.querySelector(`#pareto-${kind}-reset`);
    const count = main.querySelector(`#pareto-${kind}-count`);
    const controls = query?.closest('.pareto-table-tools');
    const tbody = table?.querySelector('tbody');
    if (!table || !query || !sort || !reset || !count || !controls || !tbody) continue;
    const rows = Array.from(tbody.querySelectorAll('tr'));
    let sorted = false;
    let snapshot = null;
    const filter = () => {
      const needle = norm(query.value);
      let n = 0;
      for (const row of rows) {
        const shown = norm(row.textContent).includes(needle);
        row.hidden = !shown;
        if (shown) ++n;
      }
      count.textContent = `${n} of ${rows.length} ${kind === 'life' ? 'transitions' : 'terms'}`;
    };
    const reorder = () => {
      const order = sorted
        ? (kind === 'life' ? rows.slice().reverse() : rows.slice().sort((a,b) => norm(a.cells[0].textContent).localeCompare(norm(b.cells[0].textContent),'en')))
        : rows;
      order.forEach(row => tbody.appendChild(row));
      sort.setAttribute('aria-pressed', String(sorted));
      sort.textContent = kind === 'life' ? (sorted ? 'Original order' : 'Reverse order') : (sorted ? 'Original order' : 'Sort A–Z');
      filter();
    };
    const clear = () => { query.value = ''; sorted = false; reorder(); };
    query.addEventListener('input', filter);
    sort.addEventListener('click', () => { sorted=!sorted; reorder(); });
    reset.addEventListener('click', () => { clear(); query.focus(); });
    controls.hidden = false;
    reorder();
    active.push({
      beforePrint() { snapshot={needle:query.value,sorted}; clear(); },
      afterPrint() { if (!snapshot) return; query.value=snapshot.needle;sorted=snapshot.sorted;snapshot=null;reorder(); }
    });
  }
  window.addEventListener('beforeprint', () => active.forEach(x => x.beforePrint()));
  window.addEventListener('afterprint', () => active.forEach(x => x.afterPrint()));
})();
