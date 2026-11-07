/* Local consultation only. Every approved entry is present in static HTML. */
(() => {
  'use strict';
  if (!document.body.classList.contains('international-complete-guide')) return;
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const collator = new Intl.Collator('en', { numeric: true, sensitivity: 'base' });
  document.querySelectorAll('[data-consult]').forEach(region => {
    const controls = region.querySelector('[data-consult-controls]');
    const input = controls?.querySelector('input');
    const reset = controls?.querySelector('[data-consult-reset]');
    const status = controls?.querySelector('[role="status"]');
    const rows = [...region.querySelectorAll('[data-consult-row]')];
    if (!input || !reset || !status || !rows.length) return;
    const table = region.dataset.consult === 'table' ? region.querySelector('table') : null;
    const headers = table ? [...table.querySelectorAll('thead th')] : [];
    const original = [...rows];
    const apply = () => {
      const terms = normalize(input.value).trim().split(/\s+/).filter(Boolean);
      let shown = 0;
      rows.forEach(row => {
        const match = terms.every(term => normalize(row.textContent).includes(term));
        row.hidden = !match;
        if (match) shown++;
      });
      status.textContent = `${shown} of ${rows.length} entries`;
    };
    const clearSort = () => headers.forEach(th => th.setAttribute('aria-sort', 'none'));
    if (table) {
      headers.forEach((th, column) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.title = 'Sort by this column';
        while (th.firstChild) button.append(th.firstChild);
        th.append(button);
        th.setAttribute('aria-sort', 'none');
        button.addEventListener('click', () => {
          const direction = th.getAttribute('aria-sort') === 'ascending' ? -1 : 1;
          clearSort();
          th.setAttribute('aria-sort', direction === 1 ? 'ascending' : 'descending');
          [...rows].sort((a, b) => direction * collator.compare(a.cells[column].textContent.trim(), b.cells[column].textContent.trim()) || original.indexOf(a) - original.indexOf(b)).forEach(row => table.tBodies[0].append(row));
        });
      });
    }
    input.addEventListener('input', apply);
    reset.addEventListener('click', () => {
      input.value = '';
      if (table) original.forEach(row => table.tBodies[0].append(row));
      clearSort();
      apply();
      input.focus();
    });
    let screenOrder;
    window.addEventListener('beforeprint', () => {
      if (!table) return;
      screenOrder = [...table.tBodies[0].rows];
      original.forEach(row => table.tBodies[0].append(row));
    });
    window.addEventListener('afterprint', () => screenOrder?.forEach(row => table.tBodies[0].append(row)));
    controls.hidden = false;
    apply();
  });
})();
