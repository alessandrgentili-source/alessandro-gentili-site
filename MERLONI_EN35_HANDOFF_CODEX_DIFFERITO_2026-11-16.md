# CERCHI D’INCHIOSTRO — INTERNATIONAL
## Merloni EN35 · Handoff Codex DIFFERITO (nessuna esecuzione autorizzata)

**Data:** 16 novembre 2026  
**Stato:** testo EN35 congelato per l'handoff editoriale dall'autore in questa conversazione. **Preparato ≠ pubblicato ≠ indicizzato.**  
**Repository:** `alessandrgentili-source/alessandro-gentili-site`.  
**Modalità del presente handoff:** **READ-ONLY**, salvo ulteriore incarico espresso dell'autore.

## A. Pacchetto e fonte esclusiva

1. `MERLONI_EN35_TESTO_FINALE_APPROVATO_2026-11-16.md` — **unica fonte editoriale autorizzata** per la futura conversione HTML.
2. `MERLONI_EN35_SPECIFICA_VISUAL_ATLAS_INTERNATIONAL_2026-11-16.md` — specifica di layout/figure International; nessuna autorizzazione a riscrivere.
3. `MERLONI_EN35_HANDOFF_CODEX_DIFFERITO_2026-11-16.md` — istruzioni operative differite.

Nel pacchetto ZIP sono presenti **esattamente tre file `.md`**. Non vi sono HTML, codice, PR, commit o asset modificati.

**SHA-256 del master EN approvato:** `553d12922a28b9239cf2a3c83d3e56b2dc0ce11a684e518d5b616f85b74d67ef`. Prima di qualsiasi lavoro tecnico verificarne l'hash ed escludere differenze di contenuto non autorizzate.

## B. Provenienza e audit: descrivere solo ciò che è documentato

- Italiano di riferimento: **Guida IT35**, master revisionato e approvato il **16 novembre 2026**, presente nella branch sorgente `input/guide-35-aristide-merloni-source` con file `CERCHI_GUIDA_ARISTIDE_MERLONI_IT35_FONTE_REVISIONATA_2026-11-16.md`, pubblicato nell'attuale pagina italiana `cerchi/guide/aristide-merloni-impresa-lavoro-destino-luoghi/`.
- Prima traduzione inglese: Claude, file fornito dall'autore `Aristide Merloni — Enterprise and the Fate of Places.md`. Quella versione terminava prima di FAQ, fonti/copyright e chiusura: **non va usata come fonte finale**.
- Revisione integrale successiva: `MERLONI_EN35_EDIZIONE_INTERNATIONAL_CANDIDATA_v0_2_2026-11-16.md`, con il recupero delle 29 sezioni IT, 21 FAQ e della chiusura. L'autore ha trasmesso una valutazione finale Gemini (9,5/10), descrivendola come audit conclusivo, e il **16 novembre 2026 ha autorizzato la versione finale**. Il voto non costituisce di per sé verifica documentale.
- **Limite dei gate:** la relazione Gemini ricevuta non contiene un registro analitico dei rilievi né un benchmark letterario inglese dichiarato come realmente letto. **Non dichiarare superato su quella sola base il gate esterno documentale/letterario richiesto dal tono editoriale**. La decisione umana di congelare questa fonte EN rimane distinta dall'attestazione indipendente di tali audit. Riportare l'eventuale lacuna al momento del preflight di pubblicazione, senza cambiare il testo per conto proprio.
- Controlli mirati effettuati separatamente per la preparazione EN: KAP Arçelik (comunicato **23 giugno 2026** sul completamento del 25% Beko Europe per €71,45 milioni), Ariston Group **Annual Report 2025** (€2.707,1 milioni ricavi), Nomisma/Comune di Fabriano *Destinazione Fabriano* (2016–2023, manifattura −43% / −2.682; addetti totali −8%) e annuncio ufficiale Riello del **1 luglio 2026**. **Non** equivalgono a ricontrollo integrale delle fonti storiografiche e dei dati della guida.
- **Micro-correzione documentale EN successiva alla v0.2**: §17 e FAQ 17 distinguono l'annuncio KAP del 23 giugno 2026 dal giorno effettivo di closing, che l'annuncio non esplicita. Non alterare la fonte italiana congelata. Nessun'altra modifica sostanziale deliberata nel master EN; aggiornati i metadati di stato del file.
- **Cautela storiografica:** gli ordini AGIP ricostruiti da Sori e Bartocci divergono; gli originali non sono stati consultati. Interpretazione di Sori sui costi del lavoro rurale non equivale a intenzione documentata di Merloni. Gli esiti dei tre figli appartengono a generazioni successive. Non usare fatturato consolidato Ariston come misura dell'economia di Fabriano.

## C. Stato tecnico al momento della preparazione (NON assumere invariato in futuro)

- `main` verificato il 16 novembre 2026 intorno al commit `5cdf6e34b9f53900f2203a33924909c31fddd61f`; **non presumerlo più corrente** quando inizierà la fase tecnica.
- Pagina IT35 presente: `cerchi/guide/aristide-merloni-impresa-lavoro-destino-luoghi/index.html`.
- La pagina IT35 già pubblicata fa riferimento alla cover WebP `assets/img/cerchi/cerchi-guida-35-aristide-merloni-impresa-lavoro-destino-luoghi-1600x900.webp`, da leggere/verificare su `main` nel preflight; non generare cover nuova.
- Nessuna pagina EN35 è stata individuata al percorso **ipotetico** `en/cerchi/guides/aristide-merloni-enterprise-fate-of-places/index.html` al controllo del 16 novembre 2026. Non usare questo percorso come URL finale prima di verifica delle convenzioni International su `main` e autorizzazione esplicita.
- La branch IT `input/guide-35-aristide-merloni-source` è **sorgente italiana storica**; non usarla per la pubblicazione EN, né toccarne i file.

## D. Preflight futuro: SOLO dopo nuovo incarico esplicito

1. Verificare `origin`, repository, branch, working tree e `main` aggiornato, inclusi lavori locali non committati. Non fare `reset`, `clean`, cambi branch distruttivi o stash senza autorizzazione.
2. Accertare che la guida EN35 non sia già pubblicata e che cover, IT35 e template International siano realmente presenti.
3. Leggere **da main** almeno tre guide International mature, inclusa la più recente guida Atlas, per template, header, footer, routing, lingua, CSS/JS, SEO, accessibilità e struttura JSON-LD. Non copiare guide legacy.
4. Identificare il **diff previsto e i soli file** potenzialmente necessari per EN35 (pagina, eventuali indici/metadata, sitemap, relazioni linguistiche), distinguendoli dal perimetro standard IT della procedura `05_...v2_1`.
5. Richiedere approvazione **separata ed esplicita dello scope EN** prima di creare branch di pubblicazione o modificare HTML, hub o sitemap.
6. Verificare contenuto e hash del Markdown prima di iniziare; se divergente, **STOP** e tornare all'autore.
7. Confermare che i prerequisiti della pubblicazione differita della triade siano soddisfatti: **IT+EN approvate per tutti e tre gli autori, cover approvate, draft Medium EN con nota italiana pronto, incarico di esecuzione**. Non inferire che sia tutto pronto dal solo pacchetto Merloni.

## E. Conversione autorizzabile: solo testo congelato, nessuna riscrittura

- Convertire integralmente **29 sezioni**, introduzione, indice, **due moduli proprietari**, **cinque tabelle**, 21 FAQ, fonti/copyright e conclusione. Nessuna fusione eliminativa, riordino, omissione, parafrasi o reintegro dalla bozza Claude, dal template o dal sito IT.
- FAQPage **21/21** identiche alle FAQ visibili per testo, numero e ordine. `Article`, `BreadcrumbList`, canonical, Open Graph, alt e altre proprietà solo secondo template verificato; mai inventare date o URL.
- Riutilizzare la cover IT35 approvata senza cambiarne lingua, firma o numerazione. Per i riferimenti a Mattei e Olivetti in §28, **i link presenti puntano alle guide IT**, non a EN non pubblicate; non fabbricare percorsi.
- Conservare le cinque comparazioni con limiti espliciti: figure §3 (lavoratori, perimetri variabili), §10 (luoghi, non mappa a scala), §11 (conflitto AGIP, non vendite certificate), §17 (tre vicende dopo il 1970), §18 (−43% manifattura, −8% totale comune, non additivi).
- Accessibilità da verificare con `lang=en`, HTML semantico, tabella vera, tastiera, contrasto, mobile 1280×900/390×844/320×812, no-JS e stampa. Nessun dato affidato solo al colore o ad animazioni.
- Eseguire test CI senza aggirare validatori, controlli di contenuto e regole di governance. Distinguere test tecnici PASS dalla verifica live e dalla pubblicazione.

## F. STOP e rilascio solo in nuovo incarico

**STOP** se mancano autorizzazioni, fonte/hash, cover, URL e scope non ambigui, condizioni del gate della triade, corrispondenza FAQ/HTML, prove sui dati e sulle visualizzazioni, accessibilità o preflight test. Non modificare le guide italiane o il design globale per risolvere una regressione International.

Nessun commit/push/PR/merge/deploy o uso di Codex è autorizzato da questi documenti. Quando verrà dato l'incarico, PR e revisione umana precederanno ogni merge, e controllo live/sitemap/Search Console seguiranno solo l'eventuale pubblicazione effettiva. La pagina Triadi International è una task distinta, da valutare dopo il terzo autore.
