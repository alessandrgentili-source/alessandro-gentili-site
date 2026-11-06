/* Progressive glossary search. The essay, instrument and glossary all work without JS. */
(() => {
  'use strict';
  const main = document.querySelector('.atlas-averroes .atlas-main');
  if (!main) return;
  const controls = main.querySelector('.averroes-glossary-controls');
  const input = controls?.querySelector('#averroes-glossary-search');
  const reset = controls?.querySelector('#averroes-glossary-reset');
  const status = controls?.querySelector('#averroes-glossary-status');
  const rows = [...main.querySelectorAll('#averroes-glossary-table tbody tr')];
  if (!controls || !input || !reset || !status || !rows.length) return;
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('en').trim();
  const filter = () => {
    const q = normalize(input.value);
    let visible = 0;
    for (const row of rows) {
      row.hidden = Boolean(q) && !normalize(row.textContent || '').includes(q);
      if (!row.hidden) visible++;
    }
    status.textContent = `${visible} of ${rows.length} terms`;
  };
  controls.hidden = false;
  input.addEventListener('input', filter);
  reset.addEventListener('click', () => { input.value = ''; filter(); input.focus(); });
  window.addEventListener('beforeprint', () => { for (const row of rows) row.hidden = false; });
  window.addEventListener('afterprint', filter);
  filter();
})();
