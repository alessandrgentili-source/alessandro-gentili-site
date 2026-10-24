# Contratto di pubblicazione — alessandro-gentili.it

**Versione:** 1.0 · **Data:** 2026-10-24 · **Stato:** proposta in PR, non in produzione prima del merge

## Scopo e responsabilità

Un contenuto non è pubblicato correttamente soltanto perché esistono la sua pagina, la cover e un URL in sitemap. Devono essere coerenti anche i percorsi che lo rendono raggiungibile e le relazioni con contenuti già pubblici.

Queste regole valgono **allo stesso modo** per ChatGPT, Codex Desktop e collaboratori che operano sul repository canonico. Prima di pubblicare leggere **AGENTS.md**, questo documento e, per Cerchi, **.agents/skills/cerchi-publisher/SKILL.md**.

**Prima di modificare:** verificare branch main, commit remoto, PR concorrenti, contenuti realmente pubblici, embargo e perimetro autorizzato. DRAFT, PUBLICATION e deploy sono fasi distinte. Una PR o un deploy riusciti non dimostrano né indicizzazione né traffico né valore prodotto.

Non modificare mai in automatico un corpo editoriale approvato, slug, URL, canonical, hreflang, schema, asset esistenti o visual identity per far passare una checklist. Se serve una variazione del perimetro, proporla e ottenere autorizzazione.

## Matrice delle dipendenze

**O = obbligatorio quando applicabile; V = verificare e aggiornare se pertinente; N = nessuna modifica automatica.** Le verifiche riguardano sia nuove pubblicazioni sia gli aggiornamenti che incidono su titolo, data, collegamenti, copertina o stato di pubblicazione.

| Pubblicazione | File/superfici O | Superfici V | Regola di tutela |
| --- | --- | --- | --- |
| **Saggio IT numerato** | Nuova pagina sotto \`saggi/\`, \`saggi.html\`, \`archivio.html\`, \`sitemap.xml\`, navigazione precedente/successivo sulle pagine coinvolte, prima card della sezione "Ultimi saggi" della \`index.html\` | \`temi/\`, pagine correlate, \`llms.txt\`, note EN esistenti, Medium | La Home conserva **tre card selezionate**; solo la prima è il più recente saggio numerato. Nessun automatismo di pubblicazione client-side |
| **Micro-saggio o testo non numerato** | Pagina, \`saggi.html\`/indice pertinente, \`archivio.html\`, \`sitemap.xml\` | Home se selezionato, temi, link in altri saggi | Non sostituisce automaticamente la prima card del saggio numerato |
| **Guida autore IT** | \`cerchi/guide/<slug>/index.html\`, cover, \`cerchi/index.html\`, \`sitemap.xml\`, inventario \`tools/check-i18n-consistency.mjs\` con coppia EN effettiva **oppure** dichiarazione IT-only | \`cerchi/triadi/index.html\` se esiste/si completa la triade, Costellazioni e guide pertinenti, Home, \`llms.txt\` | La Home NON si aggiorna automaticamente; massimo 9 guide visibili. Hreflang EN solo per equivalenze reali |
| **Guida autore EN** | \`en/cerchi/guides/<slug>/index.html\`, \`en/cerchi/index.html\`, \`sitemap.xml\`, inventario IT/EN e reciprocità \`hreflang\` **se esiste una coppia equivalente** | Triadi EN, Themes EN, Positioning e Home EN per conteggi e percorsi, link Medium EN | Non presumere 1:1 tra intero catalogo IT e inglese |
| **Triade completata IT** | \`cerchi/triadi/index.html\`, link alle tre guide, \`cerchi/index.html\` per numeri e accesso | \`en/cerchi/triads/index.html\`, \`en/cerchi/index.html\`, \`en/index.html\`, \`en/positioning/index.html\`, \`llms.txt\`, Home IT | Il percorso EN può essere un percorso di lettura che rimanda a guide IT, senza fingere l'esistenza delle edizioni EN |
| **Nuova triade/percorso EN** | \`en/cerchi/triads/index.html\`, indice e sezione del percorso, \`en/index.html\`, \`en/positioning/index.html\` per conteggi | \`en/cerchi/index.html\`, Themes EN, guide realmente equivalenti e \`hreflang\` soltanto se pertinente | La quantità delle triadi EN non deve coincidere forzatamente con quella IT; entrambe devono dichiarare la propria situazione effettiva |
| **Pagina portfolio/progetto civile** | Pagina, \`archivio.html\`, \`sitemap.xml\`, hub portfolio pertinente | Home e collegamenti editoriali correlati | Non convertire automaticamente materiale culturale in un case study professionale |
| **Aggiornamento senza nuova URL** | Pagina originaria, verifica link entranti/uscente e metadati soltanto se effettivamente cambiati | Indici, Home, archivi, EN, Medium e social **se** citano informazioni divenute errate | Nessun nuovo lastmod, canonical o richiesta d'indicizzazione per semplice correzione senza evidenza |

### Quali controlli eseguono già i sistemi

- \`tools/check-public-site.py\`: esistenza di asset/link locali, H1, main, JSON-LD sintattico, sitemap, componenti, frammenti.
- \`tools/check-archive-consistency.mjs\`: copertura di saggi e portfolio nell'archivio e nella sitemap; sequenza dei saggi numerati in archivio.
- \`tools/check-i18n-consistency.mjs\`: inventari, canonical, coppie IT/EN, dichiarazioni IT-only, navigazione linguistica.
- \`tools/validate-cerchi-guide.py\`: gate **DRAFT** e **PUBLICATION** della singola guida, fonte editoriale e struttura.
- **Nuovo:** \`tools/check-publication-connections.mjs\`: primo saggio numerato della Home, links tra il nuovo saggio e il suo predecessore, card delle guide negli hub IT/EN, coerenza dei numeri pubblici IT/EN di guide e triadi. Include test di regressione con mutazioni in memoria.

La verifica **non è** un CMS, non prova la bontà della selezione editoriale, né l'efficacia SEO/GEO o la corrispondenza con Medium. La validità semantica di link in Costellazioni e la qualità dei percorsi devono essere revisionate da una persona.

## Sequenza applicabile a ogni pubblicazione

1. **INPUT.** Tipo (saggio numerato, micro-saggio, guida IT, guida EN, triade IT/EN, portfolio o revisione); contenuto definitivo, asset, URL canonica e data di pubblicazione approvati; embargo verificato.
2. **PRE-FLIGHT.** Leggere main e \`AGENTS.md\`; identificare ultima pagina pubblicata e le destinazioni della matrice; individuare PR in corso; distinguere pagine mancanti da eccezioni editoriali autorizzate.
3. **DRAFT.** Preparare il singolo contenuto e le sue dipendenze in un branch separato. Ogni cambiamento alla Home, a indici, a contenuti EN o a file protetti va dichiarato nello scope PR prima del merge. Non toccare contenuti non coinvolti.
4. **RELATION REVIEW.** Verificare manualmente link correlati, ordine dei percorsi, precedente/successivo, dati visibili, numeri nelle descrizioni e reale equivalenza IT/EN. Medium EN porta al sito EN pertinente; Medium IT al sito IT pertinente.
5. **GATE.** Eseguire i controlli pertinenti; per nuove guide usare anche il validatore in modalità PUBLICATION soltanto nel perimetro di pubblicazione autorizzato.
6. **PR.** Descrivere contenuto aggiunto, file di relazione modificati, revisioni umane necessarie, output dei test e rollback. Un test fallito blocca la chiusura della PR, non autorizza ad allargare lo scope.
7. **POST-MERGE.** Solo dopo autorizzazione: deploy, URL live raggiungibili e navigabili, riscontro con lo stato di main. GSC/GA4 sono monitoraggi successivi, non prove immediate di indicizzazione o valore.

### Gate minimo ripetibile

\`\`\`sh
node tools/check-publication-connections.mjs --self-test
node tools/check-archive-consistency.mjs
node tools/check-i18n-consistency.mjs
python3 tools/check-public-site.py
git diff --check
\`\`\`

Per una guida, aggiungere \`python3 tools/validate-cerchi-guide.py ... --mode PUBLICATION\` e relativi argomenti documentati nella skill. I test devono girare anche nella CI; non basta una dichiarazione nel rapporto.

## Politica specifica della homepage

La sezione "Ultimi saggi" mantiene **tre** card; la prima propone il saggio numerato pubblicato più recente (oggi il 19). Le altre **due** sono una scelta editoriale, non necessariamente i due numeri precedenti. L'indice \`saggi.html\` e l'archivio conservano la copertura completa. Per cambiare questa politica serve una decisione esplicita e un adeguamento coerente del test; non disattivarlo per comodità.

Per le guide, la Home resta una selezione autonoma: nessun caricamento obbliga a sostituire le nove card visibili. Nuove triadi possono invece rendere necessario aggiornare spiegazioni e riferimenti nei rispettivi hub.

## Accettazione, STOP e rollback

**Accettazione tecnica:** tutti i controlli pertinenti verdi, inclusa prova che omissione primo saggio Home e conteggi Cerchi errati sono intercettati; PR con diff limitato; nessun errore pubblico verificato dopo un eventuale deploy.

**STOP:** contenuti non definitivi; link a pagine non pubblicate; equivalenze linguistiche non dimostrate; errore nel gate che richiede modifiche al di fuori dello scope; verifiche non riproducibili; PR in conflitto. Non modificare automaticamente sitemap/canonical/metadata editoriali per “sbloccare” una verifica.

**Rollback:** prima del merge chiudere o correggere la PR; dopo un merge autorizzato, revert mirato dei commit coinvolti e nuova verifica dei link e dei cataloghi.

**Costi:** nessun nuovo servizio e nessuna dipendenza software; tempo di manutenzione limitato al controllo delle superfici realmente connesse. Impatto sul traffico o conversioni da verificare successivamente con dati, senza assumerlo.
