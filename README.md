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

## Placeholder / checklist pre-pubblicazione
- [ ] Sostituire Canonical URL in `index.html`.
- [ ] Sostituire Open Graph URL e Open Graph image.
- [ ] Sostituire endpoint Formspree (`https://formspree.io/f/TUO_ID_FORMSPREE`).
- [ ] Caricare PDF manifesto Circolo APS: `assets/docs/manifesto-il-circolo-aps.pdf`.
- [ ] Confermare URL finale del Saggio 0 (attualmente link Medium).
- [ ] Verificare funzionamento pubblico del link GPT (Scaffale Strategico).

## Nota su file legacy
`delos-reference.html` è un riferimento visuale/legacy e non fa parte della navigazione di produzione.

## Avvio locale
```bash
python3 -m http.server 8000
```
Apri `http://localhost:8000`.
