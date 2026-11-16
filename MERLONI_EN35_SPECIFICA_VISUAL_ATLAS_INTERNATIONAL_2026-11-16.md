# CERCHI D’INCHIOSTRO — INTERNATIONAL
## Merloni EN35 · Specifica visual/Atlas e rappresentazione — 16 novembre 2026

**Stato:** specifica associata al manoscritto EN35 approvato dall'autore il 16 novembre 2026; pubblicazione tecnica DIFFERITA.

**Unica fonte editoriale:** `MERLONI_EN35_TESTO_FINALE_APPROVATO_2026-11-16.md`.

**Regola:** questa specifica indica soltanto impaginazione, visualizzazione e verifiche. Non autorizza aggiunte, tagli o riscritture del testo approvato. Nessun HTML prima del successivo incarico tecnico esplicito.

## 1. Identità e architettura

- Guida **35**, Aristide Merloni, titolo esatto **“Aristide Merloni — Enterprise and the Fate of Places”**; sottotitolo **“Work, industry and the contradictions of development in inland Marche.”**
- Dodicesima triade **State · Enterprise · Community**. Merloni è il nodo dell'impresa e del radicamento territoriale; Mattei e Olivetti sono termini distinti di un confronto editoriale, non membri di un progetto comune.
- Riusare la **cover IT35 già approvata e indicata sulla pagina IT in `main`**, all'URL di asset da confermare nella futura preflight: `assets/img/cerchi/cerchi-guida-35-aristide-merloni-impresa-lavoro-destino-luoghi-1600x900.webp`. Non creare altra cover, numero o logo International.
- Preservare introduzione, indice, **29 sezioni numerate**, **due moduli interpretativi** (*The return of skills*, *The nearby factory and the cost of proximity*), **5 tabelle di contenuto**, **21 FAQ**, fonti/copyright e domanda conclusiva. Costellazione, Idee chiave, Concetti chiave, Glossario, Domande e Nodi rimangono funzioni separate; eventuali fusioni richiedono decisione editoriale.
- La struttura Atlas International resta quella effettivamente verificata su `main` al momento del rilascio; non copiare template legacy o CSS di un altro autore senza confronto. Usare per quanto possibile CSS/JS condivisi, con interventi locali soltanto motivati. Lingua documento `en`.
- Design prima di HTML. La pagina deve risultare leggibile senza JS, su mobile stretto, con tastiera e in stampa. Niente card seriali e infografiche decorative: scene e interpretazioni restano prosa.

## 2. Cinque rappresentazioni già contenute nel Markdown

### Figura A · §3, crescita della forza lavoro

| Anno | Lavoratori (ricostruzione Sori) |
| --- | --- |
| 1930 | 5–6 |
| 1936 | circa 40 |
| 1951 | circa 60 |
| 1970 | circa 2.000 |

- **Funzione:** scala della crescita dell'organizzazione nel corso di quattro decenni. Sono perimetri industriali variabili; **non** una serie statistica omogenea di occupazione nel territorio e **non** una stima dell'effetto sulla migrazione.
- Preferire la tabella HTML presente nel testo, con un piccolo confronto proporzionale opzionale **soltanto** se i valori approssimati sono etichettati correttamente; non interpolare anni intermedi o misurare occupazione locale a partire da questa tabella.

### Figura B · §10, insediamenti e direzione

| Luogo | Cronologia | Attività/qualificazione |
| --- | --- | --- |
| Matelica | 1954 | Bombole GPL |
| Cerreto d'Esi | 1957–1959 | Sviluppo di attività industriali |
| Pianello di Genga | 1965 | Scaldabagni |
| Santa Maria di Fabriano e Melano-Marischio | fine anni 1960–1970 | Ulteriori attività |

- **Funzione:** rappresentare separatamente la diffusione delle fabbriche e la direzione aziendale unitaria. L'ordine è storico/documentale, non una cartografia di distanze; evitare mappe con coordinate non verificate. Il concetto «several plants, one management» è leggibile anche senza animazioni.
- Il rapporto fra prossimità e costi salariali è un'**interpretazione di Sori**, non un risultato quantitativo dimostrato né una dichiarazione documentata dell'imprenditore.

### Figura C · §11, ordini AGIP e conflitto fra fonti

| Fonte | Resoconto |
| --- | --- |
| Ercole Sori, 2009 | Prospettata una commessa di **70.000 bombole**, non realizzata secondo Sori |
| Mario Bartocci, 2013 | Memoria locale che menziona due ordinativi di **50.000 e 100.000 pezzi** |

- **Funzione:** mostrare divergenza di ricostruzioni. Non sommare **70.000 + 50.000 + 100.000**, non rappresentare le cifre come quantità prodotte o consegnate. Mancano i contratti, le fatture e i pagamenti originali; la divergenza resta aperta.
- Preferire tabella affiancata o trattamento editoriale che mantenga **uguale leggibilità delle due testimonianze**, pur distinguendone il diverso valore metodologico.

### Figura D · §17, le tre eredità industriali

- Antonio: iniziativa autonoma 1968; crisi e amministrazione straordinaria **2008**.
- Vittorio: Indesit; controllo Whirlpool **2014**; Beko Europe **2024**; controllo completo di Arçelik **2026**.
- Francesco: attività termosanitarie; sviluppo di Ariston Group e continuità industriale/familiare.
- **Funzione:** tre traiettorie successive, non una scala di successo morale. Non attribuire a Aristide eventi o decisioni dopo il 1970; mantenere distinta la responsabilità dei soggetti societari.
- Precisazione EN rispetto al master IT, autorizzata nella chiusura editoriale: **23 giugno 2026 è data dell'annuncio KAP del completamento dell'acquisto della quota residua, non necessariamente giorno dell'esecuzione materiale**. Non sovrascrivere il manoscritto con la lettura errata del 23 giugno come data di closing.

### Figura E · §18, occupazione locale a Fabriano

| Perimetro (Comune di Fabriano) | Variazione 2016–2023 |
| --- | --- |
| Addetti delle unità locali manifatturiere | **−43%**, pari a **−2.682** persone |
| Addetti di tutte le unità locali | **−8%** |

- **Fonte:** Nomisma/Comune di Fabriano, *Destinazione Fabriano* (gennaio 2025). **Il totale comprende la manifattura**; non sommare le percentuali e non confonderle con variazioni di imprese, di popolazione o con i soli occupati delle aziende Merloni.
- Nelle visualizzazioni comparare i due indicatori sullo stesso intervallo temporale e nel medesimo comune, ma distinguere le basi delle percentuali. Se si usano barre, rappresentare la **variazione percentuale**, non fingere di conoscere una serie annuale completa o i livelli di partenza.

## 3. Regole di resa HTML futura

- Mantenere testo, ordine, titoli, numeri, enfasi, corsivi, link, tabelle, caption, citazioni, note metodologiche e **21 FAQ visibili** in identica formulazione. Il design non può introdurre nuovo contenuto sostanziale.
- Per le cinque tabelle: HTML con `<table>`, `<caption>` pertinente, `<th scope>` e una spiegazione visibile di limiti/perimetri; per elementi grafici aggiuntivi usare `<figure>` e `<figcaption>`. Le informazioni devono essere accessibili senza colore/JS; no JS obbligatorio né dati inventati per la resa.
- Niente grafici circolari su grandezze non additive, mappe localizzate senza coordinate verificate o schemi che facciano delle tre eredità una classifica.
- Glossario e liste di consultazione mantengono densità e leggibilità funzionale; non convertirli in finti capitoli narrativi o in card ripetute. I due moduli mantengono un trattamento tipografico misurato e individuale.
- Indice con link/ancore reali per introduzione + 29 sezioni, un solo H1. Citazioni in body HTML leggibili da tecnologie assistive e dalle persone senza interazioni.
- Metadati: `Article`, `BreadcrumbList`, `FAQPage` con **21 coppie esattamente uguali** alle FAQ visibili (ordine e parole), canonical solo alla pubblicazione, `og:` e card social coerenti, `hreflang` reciproco solo quando entrambe le pagine sono davvero pubblicate. Non inventare date o URL EN.
- Rimandi in §28: alla data di preparazione sono link alle **pagine italiane** pubblicate Mattei e Olivetti; non trasformarli in EN prima di verifica di esistenza e autorizzazione editoriale. Il sito proprietario è la fonte primaria.

## 4. Controlli di accettazione e STOP

**Testo:** 29/29 sezioni, due moduli, cinque tabelle, 21/21 FAQ, bibliografia e copyright; diff semantico contro il Markdown approvato; nessun testo inventato.

**Visual:** tutte e cinque le comparazioni leggibili e non ingannevoli; mobile almeno 1280×900, 390×844, 320×812, tastiera, no-JS, stampa; contrasto/overflow e accessibilità da verificare sul render reale.

**Governance:** nessuna modifica, branch, PR, asset o pagina prima del successivo incarico esplicito con scope EN autorizzato. **STOP** se manca un prerequisito, se l'asset cover non è leggibile, se un dato/una fonte risulta discordante, se le figure violano i limiti dichiarati o se l'HTML non coincide col manoscritto.
