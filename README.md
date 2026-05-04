# Alessandro Gentili — static editorial MVP

## Cos’è questo sito
Questa repository contiene un sito statico MVP in un solo file (`index.html`) per presentare il lavoro editoriale e culturale di Alessandro Gentili:
- saggi sulla contemporaneità;
- international notes;
- poesia e voce;
- eventi / portfolio culturale;
- metodo / AI systems;
- laboratorio editoriale.

Il sito usa solo HTML semantico, CSS inline e JavaScript inline (senza framework e senza dipendenze esterne).

## Come modificare i contenuti
Tutti i contenuti sono in `index.html` come `<article>` reali (crawlable), non generati da JavaScript.

Sezioni principali da aggiornare:
- Hero: `#hero`
- Saggi: `#saggi`
- Archivio ragionato (con filtri): `#archivio`
- Poesia e voce: `#poesia`
- Eventi / Portfolio culturale: `#eventi`
- Metodo / AI Systems: `#metodo`
- Laboratorio editoriale: `#laboratorio`
- Newsletter: `#newsletter`
- Contatti: `#contatti`

I filtri archivio usano `data-category` sugli articoli (`saggi`, `international`, `poesia`, `eventi`).

## Dove aggiornare URL canonico, OG image, email, Formspree
In `index.html`:
- Canonical URL: tag `<link rel="canonical" ...>` (TODO comment in `<head>`)
- Open Graph image: `<meta property="og:image" ...>` (TODO comment in `<head>`)
- Open Graph URL: `<meta property="og:url" ...>`
- JSON-LD Person URL placeholder: blocco `<script type="application/ld+json">`
- Email contatto pubblico: sezione `#contatti`
- Formspree ID: `action="https://formspree.io/f/TUO_ID_FORMSPREE"` nel form newsletter

## Test locale
Apri `index.html` direttamente nel browser oppure usa un server statico locale, ad esempio:

```bash
python3 -m http.server 8000
```

Poi visita: `http://localhost:8000`

Verifiche consigliate:
- funzionamento filtri in `Archivio ragionato`;
- validazione email newsletter;
- navigazione da menu;
- resa responsive su mobile e desktop.

## Nota deploy (futuro)
Nessun deploy è incluso in questa fase.
In seguito, questo file può essere pubblicato facilmente su GitHub Pages o Netlify.
