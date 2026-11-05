/* Gramsci EN 11: progressive glossary search; radios and the essay work without JS. */
(() => {
  'use strict';
  const main = document.querySelector('.atlas-gramsci .atlas-main');
  if (!main) return;
  const controls = main.querySelector('.gramsci-glossary-controls');
  const search = controls?.querySelector('#gramsci-glossary-search');
  const reset = controls?.querySelector('#gramsci-glossary-reset');
  const status = controls?.querySelector('#gramsci-glossary-count');
  const rows = [...main.querySelectorAll('#gramsci-glossary-table tbody tr')];
  if (!controls || !search || !reset || !status || !rows.length) return;
  controls.hidden = false;
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('en').trim();
  const update = () => {
    const q = normalize(search.value);
    let shown = 0;
    for (const row of rows) {
      const match = !q || normalize(row.textContent).includes(q);
      row.hidden = !match;
      if (match) shown++;
    }
    status.textContent = `${shown} of ${rows.length} entries visible`;
  };
  search.addEventListener('input', update);
  reset.addEventListener('click', () => { search.value=''; update(); search.focus(); });
  window.addEventListener('beforeprint', () => { for (const row of rows) row.hidden = false; });
  window.addEventListener('afterprint', update);
  update();
})();

