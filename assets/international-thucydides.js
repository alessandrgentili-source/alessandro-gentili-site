/* Thucydides EN31 — progressively enhanced semantic reference tables.
   All source rows remain visible without JS; the two-decree native radio tool
   is CSS-only and intentionally independent of these controls. */
(() => {
  "use strict";
  const main = document.querySelector(".atlas-thucydides-v3 .atlas-main");
  if (!main) return;

  const normalize = value => String(value).normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase().replace(/\s+/g, " ").trim();

  const active = [];
  for (const key of ["life", "works", "glossary"]) {
    const panel = main.querySelector('[data-thucydides-controls="' + key + '"]');
    const table = main.querySelector("#thucydides-" + key + "-table");
    if (!panel || !table || !table.tBodies.length) continue;
    const tbody = table.tBodies[0], sourceRows = Array.from(tbody.rows);
    const search = panel.querySelector('input[type="search"]');
    const order = panel.querySelector("select");
    const reset = panel.querySelector("button");
    const count = panel.querySelector('[role="status"]');
    const sortedHead = table.querySelector("thead th:nth-child(1)");
    if (!search || !reset || !count) continue;

    const unit = key === "life" ? "events" : key === "works" ? "books" : "terms";
    let printing = false;
    function redraw() {
      if (printing) return;
      const words = normalize(search.value).split(" ").filter(Boolean);
      const rows = [...sourceRows];
      if (order && order.value !== "source") {
        rows.sort((a,b) => {
          const aKey = key === "life" ? Number(a.dataset.timeKey) : Number(a.dataset.sourceIndex);
          const bKey = key === "life" ? Number(b.dataset.timeKey) : Number(b.dataset.sourceIndex);
          const delta = aKey - bKey;
          return (order.value === "asc" ? delta : -delta) ||
            Number(a.dataset.sourceIndex) - Number(b.dataset.sourceIndex);
        });
      }
      tbody.append(...rows);
      let shown = 0;
      for (const row of sourceRows) {
        row.hidden = !words.every(word => normalize(row.textContent).includes(word));
        if (!row.hidden) shown++;
      }
      count.textContent = shown + " of " + sourceRows.length + " " + unit;
      if (order && sortedHead) sortedHead.setAttribute(
        "aria-sort", order.value === "source" ? "none" :
                     order.value === "asc" ? "ascending" : "descending");
    }
    function showForPrint() {
      if (printing) return;
      printing = true;
      tbody.append(...sourceRows);
      sourceRows.forEach(row => { row.hidden = false; });
    }
    function restoreAfterPrint() {
      if (!printing) return;
      printing = false;
      redraw();
    }
    search.addEventListener("input", redraw);
    if (order) order.addEventListener("change", redraw);
    reset.addEventListener("click", () => {
      search.value = "";
      if (order) order.value = "source";
      redraw();
      search.focus();
    });
    panel.hidden = false;
    redraw();
    active.push({ showForPrint, restoreAfterPrint });
  }

  if (!active.length) return;
  let inPrint = false;
  function beforePrint() {
    if (inPrint) return;
    inPrint = true;
    active.forEach(item => item.showForPrint());
  }
  function afterPrint() {
    if (!inPrint) return;
    inPrint = false;
    active.forEach(item => item.restoreAfterPrint());
  }
  window.addEventListener("beforeprint", beforePrint);
  window.addEventListener("afterprint", afterPrint);
  if (typeof window.matchMedia === "function") {
    const media = window.matchMedia("print");
    if (typeof media.addEventListener === "function") media.addEventListener(
      "change", event => { if (event.matches) beforePrint(); else afterPrint(); });
  }
})();
