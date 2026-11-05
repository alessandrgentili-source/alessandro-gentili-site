/* Hobbes EN 12. Progressive glossary search. The four-question test works with CSS and no JS. */
(() => {
  'use strict';
  const root = document.querySelector('.atlas-hobbes .atlas-main');
  if (!root) return;
  const controls = root.querySelector('.hobbes-glossary-controls');
  const input = root.querySelector('#hobbes-glossary-query');
  const reset = root.querySelector('#hobbes-glossary-reset');
  const status = root.querySelector('#hobbes-glossary-status');
  const rows = [...root.querySelectorAll('#hobbes-glossary-table tbody tr')];
  if (!controls || !input || !reset || !status || rows.length !== 23) return;
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/\s+/g, ' ').trim();
  const update = () => {
    const term = normalize(input.value);
    let shown = 0;
    for (const row of rows) {
      const matches = normalize(row.textContent).includes(term);
      row.hidden = !matches;
      if (matches) shown++;
    }
    status.textContent = `${shown} of ${rows.length} concepts`;
  };
  controls.hidden = false;
  input.addEventListener('input', update);
  reset.addEventListener('click', () => { input.value = ''; update(); input.focus(); });
  window.addEventListener('beforeprint', () => { rows.forEach(row => { row.hidden = false; }); });
  window.addEventListener('afterprint', update);
  update();
})();
