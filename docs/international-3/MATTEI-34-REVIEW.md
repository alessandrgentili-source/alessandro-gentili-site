> Rapporto storico del pilot DRAFT e delle sue prove di lettura. Per la successiva proposta di pubblicazione IT autorizzata vedere [MATTEI-34-RELEASE.md](MATTEI-34-RELEASE.md). I limiti «nessun commit/PR» riportati sotto si riferiscono alle fasi del pilot.

# Cerchi Publisher / Atlas IT–EN — revisione locale della Guida 34

Data verifica: 11 novembre 2026. Stato: **DRAFT, NON PUBBLICATA**. Nessun commit, push, PR, merge o deploy eseguito.

## Identità e base

- Directory iniziale: `/Users/alessandrogentili/Documents/ChatGPT/Cerchi d'inchiostro`; è il progetto contenitore, non la radice Git.
- Checkout utilizzato, già presente nel progetto: `international-seven-en/`.
- Origin verificato: `https://github.com/alessandrgentili-source/alessandro-gentili-site.git`.
- Branch iniziale: `publish/international-seven-en-complete-guides`, working tree pulito.
- Main verificata attraverso il connettore GitHub e fetch: `785525b33b38b6aabe5244f0e0ac8c30e8b620d8`.
- Branch locale dedicata da quella base: `feat/cerchi-publisher-atlas-mattei-it`.
- Nessuna PR aperta rilevata al preflight. Nessun nuovo repository, checkout o worktree creato. Gli altri checkout, incluso quello con modifiche preesistenti, non sono stati modificati.

## Confronto read-only e decisioni

Letti AGENTS, PUBLICATION_WORKFLOW, skill Publisher, cerchi-guide-standard, SYSTEM Atlas, template legacy, validatore Publisher, validatori Atlas, i18n, sito pubblico, connessioni editoriali e workflow CI.

| Riferimento | Risultato del confronto |
| --- | --- |
| EN Pasolini | Apertura/cover, indice laterale e colonna Atlas condivisi; saggio principale, Atlas desk e rappresentazione sono contenuto specifico del master EN. |
| EN Tucidide | Stessi contenitori Atlas; parti saggistiche, strumento e classi specifiche non trasferiti al pilota. |
| EN Schmitt | Usa risorse Atlas con successiva articolazione `complete-reader` e indice del manoscritto completo; non è uno scheletro universale da copiare. |
| EN Clausewitz | Conferma apertura, byline, cover, disclosure e colonna; saggio principale/desk restano propri dell'edizione EN. |
| IT Guida 33 | Riferimento per header/footer italiani, metadati, governance e sequenza finale; la card indice legacy viene sostituita dai contenitori Atlas solo nella nuova guida. |

Nessun redesign o JavaScript aggiunto: la pagina riusa `style.css`, `international-atlas.css`, `script.js` e `international-atlas.js`. Le due figure statiche usano anche il solo foglio locale `cerchi-mattei.css`, confinato a `.mattei-guide` e presente esclusivamente nel sito DRAFT. Nessuna migrazione delle guide pubblicate.

## Master e cover

Il Markdown fornito è leggibile e dichiara **Versione editoriale v3 — 31 ottobre 2026**. La cover approvata è un WebP autentico 1600×900. Le copie per la revisione, nello stesso repository verificato, conservano i byte originali:

- Master: SHA-256 `631f47c16143f1716f44a74cfbdea429ac82d9e1a78452593e9bbdd0e2078b66`.
- Cover: SHA-256 `3465bb1c205175ded358c540fa377f733dbce1e4d098bc9684a0dc2448f9ea05`.

Nessuna riscrittura, traduzione o rigenerazione. Conservati paragrafi, enfasi, elenchi, sottotitolo completo, titoli e ordine delle 40 sezioni. Rimossa solo la numerazione iniziale dagli H2 del corpo, secondo lo standard; numeri e abbreviazioni del master restano nell'indice. La versione editoriale compare nella byline; non è stata inventata una data di pubblicazione. L'introduzione resta nel corpo, dopo cover e indice nell'ordine DOM.

I cinque collegamenti canonici nelle relazioni e in Prosegui conducono a Weber, Gramsci, Smith, Machiavelli e McLuhan, già presenti nella sitemap. Merloni e Olivetti restano menzioni testuali future come nel master, senza link o dichiarazioni di disponibilità. Aggiunti i collegamenti funzionali a hub/Triadi in Prosegui, separati dal testo originale. Nessuna traduzione Mattei EN o hreflang fittizia.

## Arricchimento Atlas del pilota

La prosecuzione lavora sulla medesima branch DRAFT, senza commit o pubblicazione. L'indice prima evidenziava la sezione 1 durante l'introduzione. Aggiunta la voce di navigazione non numerata **Introduzione**, marcata `data-atlas-opening`, prima delle 40 voci originali del master: il JS Atlas esistente può ora associare l'apertura alla propria voce. Le 40 etichette numerate restano invariate; non è stata inventata una nuova sezione editoriale. Senza JS non viene dichiarata alcuna voce attiva e tutti i link restano nativi, con disclosure aperto.

Rimosso il lead «Energia, impresa pubblica e autonomia» che ripeteva parte dell'H1. Il hero è marcato `data-atlas-hero="title-only"`: titolo, H1, sottotitolo integrale nell'introduzione e tutti i metadati approvati restano identici.

Due `figure.atlas-figure.mattei-figure`, interne agli articoli pertinenti e separate dai paragrafi originali:

| Figura | Dati e limiti |
| --- | --- |
| Sezione 13 — Gas e infrastrutture | Produzione italiana: **circa 20 milioni di m³ nel 1946**, **305 milioni nel 1950**. Rete: **circa 354 km nel 1949**, **1.266 km nel 1951**. Due serie e scale separate, barre da zero, nessuna interpolazione fra anni non documentati; non viene attribuita tutta la crescita a Mattei. |
| Sezione 18 — Accordo iraniano | Partecipazione SIRIP: **NIOC 50% / AGIP Mineraria 50%**. Ripartizione economica complessiva **prevista**: **Iran 75% / parte italiana 25%**, combinando entrate fiscali e dividendi NIOC. Le percentuali non sono quote dei giacimenti né risultati economici conseguiti. Esplicitati mancata garanzia dei profitti e rischio esplorativo italiano. |

Solo dati del Markdown approvato. Le tabelle HTML, con caption/unità e header `scope`, sono la rappresentazione accessibile; le barre CSS sono decorative (`aria-hidden`) e non richiedono JS. Titolo e didascalia di ogni figura sono collegati da ARIA. Desktop: due pannelli; mobile: pannelli in colonna. Le percentuali restano leggibili come testo, senza affidarsi al colore.

Oltre al confronto con il master, un hash del concatenamento di tutti i 41 articoli HTML originari controlla che, escludendo esclusivamente le due figure autorizzate, gli articoli precedenti siano **identici byte per byte**. Un secondo hash conserva title, meta, canonical/alternates, H1 e tutti gli script JSON-LD. Entrambi sono registrati nel manifest e fissati nel test del pilota.

## Anteprima

Da `international-seven-en/`:

```sh
python3 tools/preview-cerchi-draft.py --candidate .agents/skills/cerchi-publisher/pilots/mattei/site --port 8767
```

- [Anteprima locale](http://127.0.0.1:8767/cerchi/guide/enrico-mattei-energia-impresa-pubblica-autonomia/)
- [Senza JavaScript](http://127.0.0.1:8767/cerchi/guide/enrico-mattei-energia-impresa-pubblica-autonomia/?nojs)

Server attivo solo su loopback. Overlay della pagina e cover DRAFT sulle risorse del checkout; header HTTP `X-Robots-Tag: noindex, nofollow`, nessuna modifica ai metadati pubblici per l'anteprima. `?nojs` applica CSP `script-src 'none'`. Il candidato risiede nell'area interna della skill, non nei percorsi pubblici o nei bundle `.staging` che attiverebbero il workflow di assemblaggio.

Prove visive aggiornate, desktop 1280×900 e mobile 390×844 (le figure lunghe su mobile hanno anche una seconda inquadratura della didascalia):

| Elemento | Desktop | Mobile | Dettaglio mobile |
| --- | --- | --- | --- |
| Indice | [Screenshot](../../.agents/skills/cerchi-publisher/pilots/mattei/evidence/indice-desktop.jpg) | [Screenshot](../../.agents/skills/cerchi-publisher/pilots/mattei/evidence/indice-mobile.jpg) | — |
| Gas e rete | [Screenshot](../../.agents/skills/cerchi-publisher/pilots/mattei/evidence/gas-rete-desktop.jpg) | [Screenshot](../../.agents/skills/cerchi-publisher/pilots/mattei/evidence/gas-rete-mobile.jpg) | [Didascalia](../../.agents/skills/cerchi-publisher/pilots/mattei/evidence/gas-rete-mobile-didascalia.jpg) |
| Iran | [Screenshot](../../.agents/skills/cerchi-publisher/pilots/mattei/evidence/iran-quote-desktop.jpg) | [Screenshot](../../.agents/skills/cerchi-publisher/pilots/mattei/evidence/iran-quote-mobile.jpg) | [Didascalia](../../.agents/skills/cerchi-publisher/pilots/mattei/evidence/iran-quote-mobile-didascalia.jpg) |

Le PNG della prima consegna restano come documentazione del primo DRAFT; i JPG sopra rappresentano l'arricchimento attuale.

## Adeguamenti ai validatori

`validate-cerchi-guide.py` riconosce i percorsi IT/EN e i rispettivi hub/triadi, label e lingue. Atlas ha un contratto distinto dal legacy `.guide-index`, che resta testato. Il nuovo contratto controlla contenitori, CSS nell'ordine corretto, script Atlas defer dopo lo script comune, skip link, indice aperto senza JS e sezioni figlie dirette della colonna. La voce supplementare d'apertura è ammessa soltanto prima delle voci del master e deve puntare univocamente alla vera introduzione; il hero senza lead richiede la dichiarazione esplicita `title-only`. Le figure supplementari restano distinguibili dai paragrafi del master e richiedono contenitore Atlas statico, ID, titolo accessibile e didascalia collegata. I CSS aggiuntivi del candidato sono risolti dalla sua radice di anteprima, senza modificare asset pubblici.

Il parser riconosce `Indice della guida` e i corrispettivi EN; aggiunti nove alias esatti del master Mattei e il titolo finale `Fonti, metodo e copyright`, senza accettare etichette arbitrarie per il solo fatto che il link funzioni. Per Atlas il master strutturato è obbligatorio e il confronto controlla anche testo aggiunto o duplicato, oltre a omissioni/alterazioni. Ogni risposta FAQ JSON-LD corrisponde alla sua domanda visibile, non a una risposta presente altrove.

L'assenza totale di hreflang è corretta per una guida non tradotta. Se presenti, gli alternates conservano controlli di lingua, canonical, esistenza e reciprocità; x-default può essere la guida stessa o la reale controparte italiana. `EN_REVISION` e il contratto conservativo delle guide EN esistenti restano invariati.

`check-cerchi-atlas-pilot.py` verifica hash approvati, contenuto, enfasi, elenchi, shell IT originale e relazioni pubblicate. I self-test respingono 18 mutazioni (destinazione della voce Introduzione, dichiarazione del hero, titolo introduttivo, omissione, alterazione, aggiunta, etichetta errata, anchor assente, ID duplicato, indice chiuso, CSS/JS mancanti, canonical, autore, lingua, hreflang, link e FAQ). Verificano inoltre DRAFT contro una sitemap modificata in un mirror temporaneo, le barriere PUBLICATION IT/EN, una fixture EN sintetica e il contratto legacy con relativo caso negativo. Altri sette casi negativi verificano approssimazioni, dati della figura, etichetta di previsione, percentuali, testo originale spostato dentro una figura, figure aggiuntive e titolo accessibile assente. La fixture EN è solo materiale temporaneo di test, non una traduzione della guida.

CI: aggiunti trigger sulla skill/pilota e il comando `python3 tools/check-cerchi-atlas-pilot.py --self-test` al workflow International esistente. Nessun gate precedente rimosso o disabilitato.

## Esito delle verifiche

| Verifica | Esito locale |
| --- | --- |
| Publisher DRAFT / pilota e self-test | PASS; NON PUBBLICATA; 41 blocchi, voce Introduzione + 40 anchor numerate, 16 FAQ e 2 figure statiche. |
| HTML, asset, link locali e frammenti | PASS sul candidato; PASS sito pubblico: 115 documenti, 7.998 riferimenti. |
| JSON-LD | PASS Article, BreadcrumbList e tutte le 16 coppie FAQ; autore, lingua, canonical e cover coerenti. |
| i18n | PASS: 33 IT / 33 EN pubbliche; il DRAFT non altera l'inventario. |
| Archivio | PASS: 22 saggi, 2 progetti, 6 categorie. |
| Publication connections e mutazioni | PASS; home, numeri pubblici e cronologia invariati. |
| Atlas JS: sintassi e regressioni | PASS (scroll, deep link, resize, cronologia e attivazione confinata). |
| Conservazione guide EN rispetto alla base | PASS; tutte le guide Atlas pubblicate invariate. |
| Plato EN_REVISION e 12 mutazioni | PASS, anche con il master pinned usato dalla CI. |
| Consent revocation / script comune | PASS. |
| Saggio 16 publication | PASS; rieseguito fuori sandbox per consentire il server loopback richiesto dal test. |
| Skill quick_validate / parsing YAML workflow | PASS. PyYAML usato solo in una directory temporanea, senza dipendenze aggiunte al repository. |
| Diff e perimetro | PASS; controllati anche i nuovi file. 78 file protetti/guide pubblicate identici byte per byte alla base. |

La CI remota **non è stata eseguita**, perché non sono stati effettuati push o aperte PR. I comandi pertinenti del workflow sono stati eseguiti localmente; il nuovo gate è predisposto per la futura CI.

Browser: verificati 1280×900, 390×844 e 320×812. Nessun overflow orizzontale; cover caricata alla dimensione naturale corretta. Apertura affiancata desktop e singola colonna mobile. Disclosure chiuso su mobile con JS, aperto desktop, riaperto correttamente al cambio fascia; scelta manuale conservata nella stessa fascia. Ancore prima/centrale/ultima raggiungibili con orientamento coerente; scroll avanti e indietro aggiorna `aria-current` (Unione Sovietica → Idee chiave → Unione Sovietica). Senza JS: indice aperto, tutti i 41 blocchi presenti, ancore native e lettura integrale disponibili. Skip link porta il focus a main; summary e link funzionano con Invio. Verificati lingua, un solo main, label delle nav e alt della cover; riusato il focus visibile del CSS condiviso.

Verifica aggiuntiva dell'indice: introduzione selezionata durante l'apertura; sezione 13 e 18 selezionate durante le rispettive figure, anche a 320 px. Scroll desktop: figura Iran / voce 18 → Egitto / voce 19 → ritorno alla figura / voce 18. Le risorse JS condivise non sono cambiate. Senza JS a 320 px: 41 articoli, 2 figure, 4 tabelle, disclosure aperto, nessun `aria-current`, nessun overflow; verificata navigazione nativa da tastiera alla sezione 18.

Figure: rapporto di contrasto testo/carta su blu **12,57:1** e oro su blu **8,23:1**; in stampa blu su bianco **14,01:1**. I dati non dipendono dai colori. Tutti i selettori del foglio aggiuntivo sono confinati a `.mattei-guide`, senza import, URL esterni o nuove dipendenze.

Stampa: verificata in una prova temporanea applicando le effettive regole `@media print` del CSS Atlas e del foglio locale. Fondo bianco, testo scuro, indice/header/footer nascosti, quattro tabelle e didascalie visibili, barre decorative nascoste, due colonne e `break-inside: avoid` sulle figure. [Prova gas](../../.agents/skills/cerchi-publisher/pilots/mattei/evidence/stampa-gas-regole.jpg) e [prova Iran](../../.agents/skills/cerchi-publisher/pilots/mattei/evidence/stampa-iran-regole.jpg). La prova rende gli stili di stampa nel browser: **non è un PDF paginato né una verifica del dialogo di stampa nativo**.

Limiti: verifica funzionale/visiva e semantica di base, non audit completo con screen reader, certificazione WCAG, Core Web Vitals o nuova revisione storiografica del master. Le fonti e le cautele editoriali restano quelle approvate; non sono state inventate ulteriori verifiche bibliografiche.

## File e perimetro della PR proposta

Titolo proposto: **Cerchi Publisher: layout Atlas IT/EN e pilota Mattei 34 con figure editoriali statiche in DRAFT**.

File modificati:

- `.agents/skills/cerchi-publisher/SKILL.md`: procedimento Atlas IT/EN e confini dei gate.
- `docs/international-3/SYSTEM.md`: estensione del contratto alle nuove guide IT/EN.
- `tools/validate-cerchi-guide.py`: struttura Atlas, master Mattei e controlli bilingui.
- `.github/workflows/check-internationalization.yml`: integrazione del gate del pilota.

File nuovi:

- `tools/check-cerchi-atlas-pilot.py`: integrità e regressioni.
- `tools/preview-cerchi-draft.py`: anteprima locale con overlay e modalità senza JS.
- `.agents/skills/cerchi-publisher/pilots/mattei/master-v3-2026-10-31.md`: copia immutata del master fornito.
- `.agents/skills/cerchi-publisher/pilots/mattei/manifest.json`: base, lingua, stato, URL proposto, hash del master/cover e hash degli articoli/metadati originari.
- `.agents/skills/cerchi-publisher/pilots/mattei/site/cerchi/guide/enrico-mattei-energia-impresa-pubblica-autonomia/index.html`: guida DRAFT Atlas.
- `.agents/skills/cerchi-publisher/pilots/mattei/site/assets/img/cerchi/cerchi-guida-34-enrico-mattei-energia-impresa-pubblica-autonomia-1600x900.webp`: cover approvata immutata.
- `.agents/skills/cerchi-publisher/pilots/mattei/site/assets/cerchi-mattei.css`: solo stili confinati delle figure e regole di stampa.
- `.agents/skills/cerchi-publisher/pilots/mattei/evidence/`: screenshot desktop/mobile delle figure e dell'indice, dettagli delle didascalie e prove delle regole di stampa.
- `docs/international-3/MATTEI-34-REVIEW.md`: questo rapporto.

Esclusi: Home, hub IT/EN, Triadi IT/EN, sitemap, robots, inventario i18n pubblico, CSS/JS condivisi, altre guide, AGENTS e testi editoriali esistenti. Non è una PR di pubblicazione: l'eventuale rilascio richiederà un perimetro autorizzato separato con pagina/cover pubbliche, hub, sitemap, decisione IT-only o coppia reale nell'inventario e gate PUBLICATION verde. La mancanza intenzionale di queste superfici impedisce correttamente di presentare il DRAFT come release pronta.

Rollback prima di qualunque pubblicazione: rimuovere solo i file nuovi e ripristinare i quattro file tecnici modificati rispetto alla base; nessun contenuto pubblico richiede migrazione inversa.


Perimetro specifico della prosecuzione: pagina Mattei, CSS locale del candidato, manifest di conservazione, i due validatori già coinvolti, questo rapporto e screenshot. Skill, SYSTEM, workflow CI e server d'anteprima non hanno ricevuto ulteriori modifiche in questa fase; restano nel diff iniziale del DRAFT. Nessun commit, push, PR, merge o deploy eseguito.
