/* Seneca EN 07: optional client-side glossary filter; full glossary is static. */
(() => {
  'use strict';
  const main = document.querySelector('.international-atlas.atlas-seneca .atlas-main');
  if (!main) return;
  const tools = main.querySelector('[data-seneca-search]');
  const table = main.querySelector('[data-seneca-glossary]');
  if (!tools || !table) return;
  const input = tools.querySelector('input[type="search"]');
  const reset = tools.querySelector('[data-seneca-reset]');
  const status = tools.querySelector('[data-seneca-count]');
  const rows = [...table.tBodies[0].rows];
  if (!input || !reset || !status || rows.length !== 20) return;
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('en').trim();
  const values = rows.map(row => normalize(row.textContent));
  const update = () => {
    const query = normalize(input.value);
    let shown = 0;
    rows.forEach((row, i) => {
      const visible = !query || values[i].includes(query);
      row.hidden = !visible;
      if (visible) shown++;
    });
    status.textContent = query ? shown + ' of ' + rows.length + ' terms match the search.' : rows.length + ' terms available.';
  };
  tools.hidden = false;
  input.addEventListener('input', update);
  reset.addEventListener('click', () => { input.value = ''; update(); input.focus(); });
  update();
})();
