# CERCHI D’INCHIOSTRO — INTERNATIONAL
## Olivetti EN36 · Specifica visual / Atlas e rappresentazione — 16 novembre 2026

**Stato:** pacchetto editoriale **candidato revisionato dopo audit documentale e letterario**, NON approvato dall’autore. La correzione IRUR 1954 deriva da riscontri specialistici e diverge dal master IT, che resta immutato. Pubblicazione tecnica DIFFERITA.  
**Fonte testuale esclusiva per l’eventuale conversione, dopo approvazione:** `OLIVETTI_EN36_TESTO_FINALE_PROPOSTO_AUDIT_v2_2026-11-16.md`.  
**SHA-256 testo:** `ef2877f198a2518e44c2c156bb22880c2458992f1fe4aad3df022c4565b7e641`.

Questa specifica disciplina rappresentazione, tabelle, tipografia, navigazione e accessibilità. **Non** autorizza correzioni, aggiunte, sintesi o riscritture del testo editoriale. Nessun HTML da generare ora.

### 1. Identità e perimetro

- Guida **36**: **Adriano Olivetti — Community and Power**; sottotitolo **Enterprise, institutions and the measure of participation.**
- Dodicesima triade **State · Enterprise · Community**: Mattei = capacità industriale pubblica; Merloni = lavoro e radicamento industriale; Olivetti = istituzioni e potere di partecipare. Distinzioni interpretative, non progetto comune o genealogia inventata.
- **Cover preesistente, identità chiusa:** utilizzare soltanto il WebP approvato della guida IT36 indicato nel markup pubblicato su `main`: `assets/img/cerchi/cerchi-guida-36-adriano-olivetti-la-comunita-e-il-potere-1600x900.webp`. Verificarne esistenza, integrità e resa visiva al preflight futuro; non generare o ritoccare cover, firma, numero e macro-cover.
- **40 sezioni numerate** oltre a introduzione e indice; **4 moduli interpretativi** (10, 12, 16, 21); **3 tabelle** (§8, §16, §20); **timeline testuale in §21**; **20 FAQ**; **20 voci glossario**; cinque percorsi di lettura; 12 domande; bibliografia con limiti di consultazione; copyright; §39 e §40 completi. Ordine e testi vincolanti.
- Branding in pagina secondo il sistema International **esistente su `main`**. Le grafie dei titoli delle opere italiane, gli autori delle fonti e le etichette dei concetti originali restano riconoscibili.

### 2. Le quattro rappresentazioni da trattare con cura

| Unità | Funzione | Resa ammessa | Limite storico/argomentativo |
| --- | --- | --- | --- |
| **§8 — Works, speech, records: what they document** | Sei tipi di documento con data, natura e grado di consultazione. | Tabella semantica a quattro colonne; colonna “Source status” visibile; su mobile scorrimento orizzontale segnalato o trasformazione accessibile che **non** sopprima valori. | **1945/1946** due edizioni, **1959/1960** anno di preparazione/dato editoriale di *Città dell’uomo*: non confondere. Lettura bibliografica ≠ lettura integrale. |
| **§16 — Where the Council could decide** | Differenza giuridica fra consultazione, deliberazione e potere di stanziare risorse. | **Tabella vera** a tre colonne; opzionale schema statico adiacente dei quattro criteri di partecipazione già presenti nel testo. | Art. 28 = **consultivo** su produzione e condizioni; art. 29 = **deliberativo** sulla distribuzione di stanziamenti sociali; **ammontare complessivo** fissato dall'impresa. Non rappresentare cogestione piena. |
| **§20 — Four places, different experiences** | Confronto fra Ivrea, Pozzuoli, La Martella e Canavese/IRUR. | Matrice tipologica a tre colonne, non mappa geografica. | UNESCO = patrimonio architettonico/urbano; Pozzuoli = impianto; La Martella = progetto collettivo; IRUR = istituto territoriale: non equivalenti, nessuna efficacia occupazionale complessiva quantificata. Fondazione IRUR 1954 (non 1955), come rettificato nel testo candidato EN. |
| **§21 — An institution beyond its founder** | Cronologia 1948, 1949–50, 1960, 1963, 1971 e due progetti non compiuti. | Timeline editoriale statica/semantica; leggibile senza JS; date non “a scala”. | Sopravvivenza del Consiglio fino al **5 aprile 1971** ≠ realizzazione della Fondazione proprietaria né della costituzione comunitaria. **1963 è dopo la morte di Adriano**; non attribuirgli l'atto successivo. |

Non inventare un grafico quantitativo per il Consiglio: la differenza è **fra poteri**, non fra percentuali. La composizione originaria 8 eletti e 6 nominati, oltre al presidente/delegato, resta nella prosa del §15; non trasformarla in una rappresentazione di parità o suffragio diretto omogeneo. I 35.000 dipendenti del 1960 appartengono alla ricostruzione attribuita a Renzi e non diventano un dato comparativo con altri periodi senza fonti nuove.

### 3. Moduli, testo, architettura International

- §10 **Place and the right to govern it**: il soggetto della discussione è il potere di istituzioni territoriali, diverso dai poteri dei lavoratori nell'azienda.
- §12 **Expertise, representation and freedom**: distinguere competenza tecnica da legittimazione; non convertire in “tecnocrazia” approvata dall'autore.
- §16 **Participation and its boundaries**: il diagramma segue i limiti delle competenze statutarie, non amplia i poteri.
- §21 **After the founder: the test of institutions**: distinguere opere che restano, organismi che funzionano e potere davvero istituzionalizzato.
- Visual sobri e distinti secondo la materia; evitare card uniformi, effetti decorativi e diagrammi che sembrino prove di risultati mai documentati.
- Le sezioni di consultazione (§25–38) conservano struttura utile al lettore; non trasformarle artificialmente in prosa o in carrellate di card.
- Preservare tutte le enfasi, i corsivi, le tabelle, i limiti epistemici e le avvertenze metodologiche. Se una variazione nel design rischia di comprimere o riordinare il contenuto: **STOP**.

### 4. Accessibilità, SEO/metadata e collegamenti

- HTML semantico futuro: `lang="en"`, H1 unico, indice con ancore funzionanti per Introduzione + 40 sezioni, `table`, `caption`/didascalie coerenti, intestazioni di riga/colonna per celle significative; nessun dato affidato solo al colore, animazioni o JavaScript. Browser con JS disabilitato e versione stampata devono restare completi.
- Test mobile e desktop almeno **320×812**, **390×844**, **1280×900**; verificare scorrimento tabelle, focus da tastiera, gerarchia heading, contrasto e leggibilità.
- `FAQPage`: **20 domande e 20 risposte** esattamente uguali alle FAQ visibili §37 (ordine e testo), senza varianti semantiche.
- `Article` e `BreadcrumbList`, canonical, `og:`, `twitter:` e `hreflang` **solo secondo template verificato su main e URL EN esistente dopo rilascio**. Non inventare URL, date, slug, immagini o reciprocal hreflang.
- Proposta metadata testuale (dalla bozza Claude; da verificare su template): title `Adriano Olivetti — Community and Power | Cerchi d’inchiostro`; description `Adriano Olivetti: enterprise, community and power. His political thought, Ivrea and the real powers of participation, between institutions built and projects left unfinished.`
- **Alt cover**: redigere dall'immagine approvata realmente ispezionata al preflight, senza ripetere come fatto l'ipotesi di una fabbrica vetrata e monti contenuta nei metadati della bozza Claude.
- I riferimenti in §39 a Mattei e Merloni conducono alle pagine **IT pubblicate**; la loro etichetta “Italian edition” è parte del testo. Non trasformarli in URL inglesi prima che esistano e che l'autore approvi il cambio.

### 5. Accettazione e STOP

**Editoriale:** completezza integrale e nessuna sostituzione di frasi approvate. **Documentale:** distinguere azione politica e intenzioni, costituzione progettata e realizzata, poteri statutari e azione reale, prima e dopo 1960, fonte diretta e ricostruzione secondaria. **Visual:** tutte le quattro rappresentazioni sopra rigorose, comprensibili, staticamente accessibili e non suggestive di false equivalenze. **Tecnico:** preflight + test locali e diff ristretto allo scope EN specificamente autorizzato, senza bypass di validatori.

**STOP** in assenza di approvazione umana della versione EN revisionata, di gate indipendenti quando richiesti dal tono editoriale, di scope EN concordato, di cover verificata, di URL/canonical legittimi, o se emergono differenze nel contenuto o dati non supportati.
