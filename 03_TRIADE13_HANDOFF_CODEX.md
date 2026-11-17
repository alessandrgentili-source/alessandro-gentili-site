# CERCHI D’INCHIOSTRO — TRIADE 13 BILINGUE — HANDOFF CODEX

## Decisione umana del 17 novembre 2026

I due testi allegati sono approvati, congelati e distinti per lingua. Riportarli **integralmente e letteralmente** nelle rispettive sezioni, conservando la domanda, i due paragrafi e le enfasi; trasformazioni consentite: sole marcature HTML accessibili, senza parafrasi. Applicare la composizione leggibile e snella della Triade 11 International come riferimento **solo alla nuova sezione 13**, con domanda in testa, tre cover ufficiali affiancate e il testo breve sotto le cover. Non modificare la Triade 12 o le precedenti. Non creare una pagina autonoma, non aggiungere né trascrivere l'articolo Medium.

## Fonte approvata / SHA-256

- IT `01_TRIADE13_TESTO_IT_APPROVATO.md`: `7f5f8f106fd3869d8248f369d361fba2a5ae07cb906685c1d809a24d03a6c9b0`
- EN `02_TRIAD13_TEXT_EN_APPROVED.md`: `d71d098f187ef4a1427b3e400c7d0376da2b68aafd66e5930c00d4a775341873`

## Baseline e pubblicazione

- Repository: `alessandrgentili-source/alessandro-gentili-site`.
- Baseline post merge PR #358: `36e45bc8b1af40593e25df7092311475e03062f5`; verificare comunque `origin/main` aggiornato.
- Prima dell'intervento verificare `AGENTS.md`, `05` procedura v2.1 e `09` governance; preservare tutti i worktree, preflight dei file e verifica di PR concorrenti.
- Branch per le fonti congelate `input/triad-13-bilingual-source` (non base della PR); branch di pubblicazione `publish/triad-13-bilingual` da `origin/main` aggiornata. Non inserire le fonti Markdown nella PR pubblica.
- Nessun merge autonomo, una sola PR verso `main`, STOP per controllo umano dopo i workflow remoti.

## Vincoli editoriali

- Triade IT: **Conoscenza, conseguenze e decisione**.
- Triad EN: **Knowledge, consequences and decision**.
- Autori nell'ordine Edgar Morin · Rachel Carson · John Maynard Keynes.
- IT: `cerchi/triadi/index.html`, aggiungere la tredicesima card dopo la dodicesima; titolo, domanda e due paragrafi esattamente dalla fonte IT, collegamenti alle tre guide italiane; allineare testo introduttivo/sequenza e metadati necessari, senza riscrivere le dodici triadi precedenti.
- EN: `en/cerchi/triads/index.html`, nuova voce `href="#triad-13"` dopo 12 e nuova `<section class="wrap triad-block" id="triad-13">` dopo 12; domanda e due paragrafi esatti dalla fonte EN; tre cover originali 1600x900 WebP tratte dalle guide su `main`, ciascuna collegata alla guida EN; link statici agli originali IT; accessibilità, alt, lingua, mobile, no-JS. Il blocco 13 segue **il ritmo delle cover e delle note della Triade 11**, non la lunga prosa preliminare della 12.
- Non introdurre cronologie, citazioni, nuovi fatti o note interpretative non approvate. Titoli brevi di servizio / didascalie necessarie alla navigazione devono essere ricavati esattamente dai titoli correnti delle guide, senza nuova prosa.
- Non cambiare editoriale di Morin, Carson o Keynes: le due frasi obsolete di Morin (IT/EN) sono una microcorrezione futura, dipendente da un'approvazione distinta dei Markdown.
- Non modificare cover, macro-cover, CSS o JavaScript. Non aggiungere route `/triad-13/` o `/triade-13/`; entrambe le pagine Triadi esistono e mantengono canonical e hreflang reciproci.
- Non creare link al saggio Medium se è ancora una draft non pubblicata.

## Percorsi verificati su main

| Autore | Originale italiano | International |
|---|---|---|
| Edgar Morin | `/cerchi/guide/edgar-morin-la-conoscenza-e-i-suoi-punti-ciechi/` | `/en/cerchi/guides/edgar-morin-knowledge-and-its-blind-spots/` |
| Rachel Carson | `/cerchi/guide/rachel-carson-la-vita-dopo-l-intervento/` | `/en/cerchi/guides/rachel-carson-life-after-the-intervention/` |
| John Maynard Keynes | `/cerchi/guide/john-maynard-keynes-economia-futuro-incerto/` | `/en/cerchi/guides/john-maynard-keynes-economy-of-an-uncertain-future/` |

## Perimetro file pubblici: 9 file massimo

1. `cerchi/triadi/index.html` — card 13, riferimenti di pagina e dati strutturati.
2. `en/cerchi/triads/index.html` — anchor 13, blocco 13, metadata e schema.
3. `cerchi/index.html` — link e contatori 13, guide IT 39 senza alterazioni.
4. `en/cerchi/index.html` — spostamento semantico delle guide 37–39 nella triade completa e contatori 13/39.
5. `en/index.html` — contatore 13, nessun redesign.
6. `en/positioning/index.html` — contatore triadi 13; **non** cambiare il distinto numero di 11 Thematic paths.
7. `archivio.html` — numero triadi 13, 39 autori per lingua; mantenere guide 39.
8. `llms.txt` — 13 triadi IT/EN e collegamenti già reali, senza affermare che Medium è pubblicato.
9. `tools/check-triad12-international.py` — modifica tecnica controllata per compatibilità con 13; proteggere byte-identici i blocchi 01–12 e l'intero blocco 12, e conservare i controlli negativi.

**Nessuna modifica a `sitemap.xml`**, perché entrambe le URL Triadi sono già presenti e la PR non crea pagine. Vietato introdurre `lastmod` non motivato. Vietate modifiche a `tools/check-i18n-consistency.mjs`, che calcola i conteggi dal corpus, salvo segnalazione STOP e nuova autorizzazione. Nessuna modifica a workflow o altri test senza STOP.

## Gate tecnico obbligatorio

- La pagina IT ha 13 `article.essay-card` relativi a triadi e gli HREF risolvono tutti a pagine esistenti; EN ha 13 blocchi `triad-01`…`triad-13` e 13 voci dell'indice in ordine, con anchor funzionanti.
- I blocchi HTML delle dodici triadi precedenti restano byte-identici (o si interrompe il lavoro): niente revisione della 12, nessuna formattazione di massa.
- Il congelamento del test 12 deve continuare a verificare il SHA della fonte 12, le 7 unità di prosa, i tre autori, le cover, i sei link, i metadati del contenuto **storico** e i casi negativi; cambiare solo il modo in cui consente la successiva aggiunta della triade 13 e i conteggi pubblici aggiornati. Non basta disabilitare il controllo né rimuovere protezioni sulla pagina italiana: sostituire l'eventuale vincolo byte-identical della pagina indice con una verifica esplicita che preservi l'intera sequenza storica 01–12 e consenta soltanto l'append 13 autorizzato.
- Evitare di confondere test del congelamento storico con test del conteggio corrente; aggiungere casi negativi per triade 13 assente, doppia, fuori ordine, link sbagliati, anchor mancante e testi diversi dai Markdown congelati, compatibilmente con il perimetro consentito.
- Canonical/hreflang IT/EN delle due pagine invariati; JSON-LD `CollectionPage` coerente; nessun nuovo JavaScript e nessun CSS; mobile senza overflow e navigazione tastiera, no-JS, screenshot di confronto 11/12/13.
- Conteggi dopo pubblicazione: 39 guide IT, 39 guide EN; 13 triadi IT, 13 triadi EN; gli **11 Thematic paths** EN sono una metrica differente, non modificarla.
- Eseguire verifiche di link e anchor interni, regressioni dei controlli, `node tools/check-i18n-consistency.mjs`, `node tools/check-publication-connections.mjs --self-test`, più CI remota 3/3 PASS e revisione diff limitato ai 9 file.
- Se serve una modifica fuori scope, se i primi 12 blocchi cambiano, se emerge un quarto problema, o se non si può ottenere il layout approvato usando gli stili esistenti: STOP e richiedere nuova autorizzazione; non correggere automaticamente.

## Output

`PASS / MISSING / STOP` con SHA-256 delle due fonti, branch e commit, diff file esatto, screenshot dei blocchi 11/12/13, dati strutturati, controlli, workflow remoti, link PR. Nessun merge autonomo.
