# International 3.0 — sistema approvato e prototipi

**Branch locale:** `design/international-3-atlas`

**Base:** `e9df7f0f853e35c0cd70f60b3b4b5011efe1cae4`

**Perimetro finale:** sistema riutilizzabile + hub EN + guida EN di Pier Paolo Pasolini. Direzione artistica approvata; PR per controllo umano, senza merge/deploy o modifica a main. Le altre 23 guide e le nove guide future non sono state lavorate.

**Per estendere il sistema:** leggere [SYSTEM.md](SYSTEM.md), con contratto dei componenti, schema HTML, procedura di migrazione e controlli. È la consegna operativa; l’audit precedente è conservato come documento storico.

## Aprire il prototipo

Dalla cartella del repository:

```sh
python3 tools/preview-international.py
```

Aprire **http://127.0.0.1:8766/__review/**. Il server è limitato a localhost. Fermarlo con Ctrl+C.

- Hub: http://127.0.0.1:8766/en/cerchi/
- Guida: http://127.0.0.1:8766/en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/
- Versioni originali: stesse URL precedute da `/__before`.
- Verifica senza JavaScript: stesse URL precedute da `/__nojs` (script bloccati tramite Content-Security-Policy).

La pagina di confronto viene servita solo dal tool locale: non è un file HTML pubblico del sito. Il server applica `X-Robots-Tag: noindex, nofollow` e non espone directory nascoste o documenti interni. Le immagini del confronto sono in `evidence/`.

## Esperienza approvata

**Hub.** Apertura con tre ingressi; triade 08 in evidenza con le cover integrali; tre percorsi trasversali motivati; indice di 33 autori in undici gruppi. I 24 titoli EN pubblicati sono link reali; gli altri nove sono indicati come futuri, senza URL inventati. La ricerca riconosce nomi, parole dei testi e un piccolo vocabolario editoriale: “education” trova anche formazione e pedagogia. Nessuna ricerca remota o generazione di risposte.

**Pasolini.** Titolo e cover affiancati sul desktop; indice laterale contestuale; colonna serif; fonti e attribuzione visibili; confronto fra il contesto televisivo descritto da Pasolini e l’applicazione contemporanea della guida. I controlli radio sono nativi e funzionano anche senza JS. Le etichette riportano al testo, che resta completo. La relazione con Manzoni e Collodi recupera i testi della triade già pubblicata e aggiunge accessi diretti alle due guide EN.

Il confronto è una rappresentazione supplementare del contenuto approvato. Non attribuisce a Pasolini previsioni sulle piattaforme. Il modulo resta specifico di Pasolini e non è obbligatorio per le altre guide.

## Prima / dopo verificabile

| Aspetto | Main | Prototipo |
| --- | --- | --- |
| Testi di Pasolini | 10 blocchi narrativi | Gli stessi 10 blocchi, byte per byte e nello stesso ordine |
| Larghezza del paragrafo desktop | 1.041 px | 683 px |
| Corpo del paragrafo desktop | 17,92 px sans serif | 19,52 px serif |
| Orientamento durante la lettura | Indice separato dal corpo | Indice persistente con sezione attiva; disclosure su mobile |
| Passaggi tra autori | Ritorno alla pagina Triads | Accesso diretto ai due autori della triade |
| Esplorazione dell’hub | 24 schede seriali | Domande trasversali + indice ricercabile e completo |
| Confronto storico/contemporaneo | Solo prosa | Prosa integrale + rappresentazione esplorabile |

Misure rilevate nello stesso browser, viewport 1.280 px (area documento 1.265 px). Sono evidenze di layout, non risultati di un test con lettori.

## File coinvolti

- `en/cerchi/index.html`: nuova composizione dell’hub, percorsi e indice statico.
- `en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/index.html`: impaginazione, indice, confronto, relazione e citazione; Article arricchito con `about` e `isPartOf` coerenti con contenuti visibili.
- `assets/international-atlas.css`: stile caricato soltanto sulle due pagine.
- `assets/international-atlas.js`: ricerca locale, orientamento dell’indice, gestione del fallback del salto al contenuto. Indice aggiornato anche su resize, ripristino cronologia e variazioni del layout; disclosure sincronizzato al breakpoint.
- `assets/international-pasolini.css`: soli controlli e layout del confronto di Pasolini, separati dal contenitore editoriale condiviso.
- `tools/check-international-guide.py`: controllo riutilizzabile di integrità per adattamenti di guide EN esistenti.
- `tools/check-international-atlas.mjs`: regressioni del comportamento dell’indice.
- `.github/workflows/check-internationalization.yml`: esegue i nuovi controlli pertinenti in CI.
- `tools/check-international-prototype.py`: integrità del testo, struttura e perimetro.
- `tools/preview-international.py`: confronto locale con la base Git e modalità senza script.
- `docs/international-3/`: audit conservato, questa consegna e prove visive.

**Invariati:** tutte le altre pagine EN; sito italiano; header e footer originali; CSS e JS globali; cover e macro-cover; canonical, hreflang, title/meta description e H1 della guida; sitemap.xml; robots.txt; llms.txt. Il solo workflow International aggiunge i controlli del sistema. Nessuna nuova dipendenza runtime, font remoto o bitmap generata.

I sette documenti normativi originali forniti il 5 novembre sono stati letti. Le decisioni più recenti della conversazione governano il nuovo design e il perimetro. Cerchi Publisher è stato consultato come risorsa di governance e validazione, senza applicarne il vecchio template come vincolo artistico.

## Verifiche eseguite

PASS:

```sh
python3 tools/check-international-prototype.py
python3 tools/check-international-guide.py --base origin/main
node tools/check-international-atlas.mjs
node tools/check-publication-connections.mjs --self-test
node tools/check-archive-consistency.mjs
node tools/check-i18n-consistency.mjs
python3 tools/check-public-site.py
node --check assets/international-atlas.js
git diff --check
```

- Controllo pubblico: 105 documenti HTML, 6.169 riferimenti locali; JSON-LD e test di regressione. Le 10 eccezioni footer storiche preesistenti rimangono quelle della base.
- Integrità: 10 articoli originali identici; immagini esistenti con dimensioni naturali verificate; titoli, metadata, canonical e hreflang preservati; header/footer identici; tag bilanciati; ID unici e frammenti risolti.
- Browser: navigazione hub → Pasolini; indice e stato attivo; ricerca “education”; assenza risultati; reset; confronto fra ambienti; frecce da tastiera sui radio; Tab e Invio sul salto al contenuto.
- Responsive: hub e guida verificati a 320 e 390 px; guida anche a 1.024 px; desktop a 1.280 px. Nessun overflow nelle misure finali.
- Senza JS: 33 voci statiche nell’hub, 10 blocchi della guida, indice aperto, link e confronto nativo funzionanti. Il controllo di ricerca rimane nascosto.
- Contrasti della nuova palette verificati con formula WCAG: testo blu/carta circa 12,6:1; testo secondario/carta 5,8:1; accenti schiariti su blu oltre 8:1. L’oro è stato scurito per i piccoli testi su carta e sul fondo della triade.
- Risorse: CSS e JS locali, senza dipendenze; Pasolini carica un piccolo CSS specifico aggiuntivo. Nessun benchmark Lighthouse o Core Web Vitals live dichiarato.

## Confini e rischi residui

Questo è un prototipo a due pagine. Triads, Themes e le altre guide conservano il design e le limitazioni linguistiche di main; i link che vi conducono sono reali. Il prototipo non certifica ancora l’autonomia delle 11 triadi: sarà un criterio della fase successiva, insieme alle nove guide approvate.

Il test semantico dei dati strutturati si limita a coerenza locale e sintassi; nessuna promessa di ranking o distribuzione AI. La prova browser non sostituisce un audit completo con screen reader o un test con lettori.

La direzione visiva è conclusa e approvata. La PR consegna il sistema e le due pagine per il controllo umano. Estensione alle altre pagine e nuovi testi restano lavori separati.

## Verifica del consolidamento

Base remota nuovamente verificata: `e9df7f0` (main invariata). Stessa composizione approvata; nessuna revisione estetica aggiuntiva. A 320 px: area documento 305 px e scrollWidth 305 px; paragrafo serif 18,72 px; titolo raggiunto dall’indice a 204 px, sotto l’header (163 px). A 1280 px: area 1265 px senza overflow; voce centrale corretta, titolo a 109 px sotto l’header di 69 px. Prove visive in [system-320.png](evidence/system-320.png) e [system-desktop.png](evidence/system-desktop.png).
