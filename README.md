# Alessandro Gentili — refined static editorial website

Sito statico multipagina per la piattaforma editoriale di Alessandro Gentili.

## Architettura attuale
- `index.html`
- `saggi.html`
- `metodo-ai.html`
- `portfolio.html`
- `poesia.html`
- `strumenti.html`
- `archivio.html`
- `en.html`
- `contatti.html`
- `assets/style.css`
- `assets/script.js`

## Stack tecnico
- HTML semantico
- CSS condiviso in `assets/style.css`
- JavaScript condiviso in `assets/script.js`
- Nessun framework
- Nessun build step
- Compatibile con GitHub Pages

## Contenuti e comportamento
- Homepage breve come gateway editoriale (hero, CTA principali, 4 cards, proof-of-work, newsletter, contatti).
- Pagine interne dedicate per saggi, metodo/AI, portfolio, poesia, strumenti, archivio, EN e contatti.
- `assets/script.js` gestisce:
  - filtri archivio (`data-filter` / `data-archive-item`);
  - validazione email del form newsletter.

## Placeholder da sostituire prima della pubblicazione
- Canonical URL (`index.html`)
- Open Graph image URL (`index.html`)
- Endpoint Formspree (`index.html`)
- URL definitiva del Saggio 0 (attualmente link Medium)
- Circolo APS manifesto PDF (`assets/docs/manifesto-il-circolo-aps.pdf`)
- Verifica del link pubblico GPT (Scaffale Strategico)

## Nota su file legacy
`delos-reference.html` è un riferimento visivo/legacy e non fa parte del sito in produzione.

## Avvio locale
```bash
python3 -m http.server 8000
```
Apri `http://localhost:8000`.
