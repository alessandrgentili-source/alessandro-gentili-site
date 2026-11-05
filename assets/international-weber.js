/* Weber EN 09 — progressive glossary search; no network, no telemetry.
   The complete glossary and the five-step instrument remain available without JS. */
(() => {
  'use strict';
  const root = document.querySelector('.atlas-weber #glossary');
  if (!root) return;
  const controls = root.querySelector('.weber-glossary-search');
  const input = controls?.querySelector('input[type="search"]');
  const reset = controls?.querySelector('.weber-glossary-reset');
  const status = controls?.querySelector('[role="status"]');
  const entries = [...root.querySelectorAll('.weber-glossary-term')];
  if (!controls || !input || !reset || !status || !entries.length) return;
  const normalize = s => s.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/\s+/g, ' ').trim();
  const entriesWithText = entries.map(el => ({el, text: normalize(el.textContent || '')}));
  const filter = () => {
    const query = normalize(input.value);
    let visible = 0;
    for (const item of entriesWithText) {
      const show = !query || item.text.includes(query);
      item.el.hidden = !show;
      if (show) visible++;
    }
    status.textContent = query ? visible + ' of ' + entries.length + ' entries match.' : 'All ' + entries.length + ' entries shown.';
    reset.disabled = !query;
  };
  controls.hidden = false;
  input.addEventListener('input', filter);
  reset.addEventListener('click', () => { input.value = ''; filter(); input.focus(); });
  filter();
})();
