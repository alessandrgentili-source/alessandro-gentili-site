# CERCHI D’INCHIOSTRO — INTERNATIONAL
## Olivetti EN36 · Handoff Codex DIFFERITO — 16 novembre 2026

**Modalità:** documentazione per futura esecuzione; **nessuna attività Codex/GitHub autorizzata** con questo pacchetto.  
**Repository:** `alessandrgentili-source/alessandro-gentili-site`  
**Stato:** pacchetto **candidato dopo audit mirato**, il manoscritto EN36 deve ricevere **approvazione umana esplicita** prima di diventare fonte congelata per HTML. La fase di Codex resta bloccata. Preparato ≠ approvato ≠ pubblicato ≠ indicizzato.

## A. I tre file e la regola della fonte

1. `OLIVETTI_EN36_TESTO_FINALE_PROPOSTO_AUDIT_v2_2026-11-16.md` — **testo integrale revisionato**; diventa fonte esclusiva dopo approvazione dell'autore.
2. `OLIVETTI_EN36_SPECIFICA_VISUAL_ATLAS_INTERNATIONAL_v2_2026-11-16.md` — specifica di design e rappresentazione International; non è una fonte testuale alternativa.
3. `OLIVETTI_EN36_HANDOFF_CODEX_DIFFERITO_v2_2026-11-16.md` — presenti istruzioni e preflight; NON eseguire ora.

Archivio ZIP contenente **esattamente questi tre Markdown**, senza HTML, CSS, JS, PDF, asset o vecchie bozze.

**SHA-256 file 1:** `ef2877f198a2518e44c2c156bb22880c2458992f1fe4aad3df022c4565b7e641`. Per ogni futuro intervento verificare questo hash rispetto al file autorizzato e ricalcolarlo solo a seguito di una nuova decisione editoriale esplicita.

## B. Provenienza, revisione e stato probatorio

- Master IT36 approvato del **31 ottobre 2026**: `CERCHI_GUIDA_ADRIANO_OLIVETTI_FINALE_PROPOSTA_v3_2026-10-31.md` nella branch sorgente `input/guide-36-adriano-olivetti-source`. Il file è stato letto da GitHub e la sua architettura verificata; **non è una branch di pubblicazione International**.
- Guida italiana pubblicata su `main` in `cerchi/guide/adriano-olivetti-la-comunita-e-il-potere/index.html`; cover da metadata pagina IT: `assets/img/cerchi/cerchi-guida-36-adriano-olivetti-la-comunita-e-il-potere-1600x900.webp`.
- Prima traduzione Claude ricevuta dall'autore: `Adriano Olivetti — Community and Power.md`, SHA-256 `971c5f9dfe54243fe9573f61d6b58bee744c346e48bf28fa61196564d7e3747b`. Era **incompleta**, terminava dopo la sezione “Method and limits” al §38 e metadata web, **senza copyright**, **senza §39 e §40**. Non usarla come fonte finale.
- Revisione primaria effettuata in questa sessione: ripristinate dal master approvato la sezione copyright e §§39–40, convertita la biografia §4 dal presente narrativo a una prosa storica coerente, riviste selettivamente apertura, soglie interpretative, forme troppo calchiate e transizioni. Sono stati mantenuti **40 sezioni**, **4 moduli interpretativi**, **3 tabelle**, **20 FAQ**, **20 voci di glossario** e tutti i limiti documentali dichiarati. I riferimenti in §39 sono solo a pagine IT.
- Verifiche esterne MIRATE effettuate nella fase iniziale: UNESCO 2018 Ivrea (sito ufficiale), Davide Cadeddu su due edizioni e sottotitoli de *L’ordine politico delle Comunità*, testo ufficiale della Direttiva (UE) 2024/2831 sul lavoro tramite piattaforma. Queste **non equivalgono** a ricontrollo integrale delle fonti storiche, del Consiglio o dei titoli societari.
- **Revisione aggiuntiva del 16/11 (questa versione candidata v2):** controllo documentale autonomo, con riscontri di fonti esterne, e audit letterario distinto, con lettura effettiva di un saggio benchmark inglese. Entrambi documentati nel rapporto `OLIVETTI_EN36_AUDIT_EDITORIALE_DOCUMENTALE_2026-11-16.md` consegnato separatamente (non parte dello ZIP a tre file). Un errore di data IRUR è stato corretto da 1955 a **1954** in sei punti, e la provenienza della data PNF è stata precisata in due punti. La stessa data IRUR errata figura nel master IT approvato: nessuna modifica IT autorizzata né eseguita. **Gli audit sono passaggi separati compiuti dall’assistente in questa sessione, non un parere esterno umano di terza parte.** La qualificazione di gate soddisfatto e l’approvazione editoriale richiedono giudizio umano esplicito; non simulare PASS da accordo automatico.
- I riferimenti al passato del fascismo, all'assetto del Consiglio di Gestione (art. 28 consultazione / art. 29 distribuzione stanziamenti), alla Fondazione Camillo Olivetti **non attuata**, a Underwood **1959 vs 1960**, a Elea 9003 **1959** e Programma 101 **1965** sono distinzioni strutturali non sacrificabili.

## C. Stato tecnico indicativo e limiti

- `main` osservato il 16 novembre 2026 con SHA `5cdf6e34b9f53900f2203a33924909c31fddd61f`. **Non presumere** che resti corrente.
- Le tre pagine italiane IT34/IT35/IT36 risultano presenti su `main` secondo i controlli su repository. **Non inferire l'esistenza delle corrispondenti pagine EN**; verificare al futuro preflight.
- La cover approvata è la stessa della versione italiana: **nessun nuovo asset grafico da produrre**.
- Lo slug EN36 e il percorso finale devono essere dedotti **dal sistema International reale su `main`**, non dalla traduzione del titolo né da un esempio storico; nessun URL EN è preautorizzato.

## D. Preflight futuro: READ-ONLY prima di qualsiasi sviluppo

1. Solo dopo nuovo incarico dell'autore: verificare repo, `origin`, branch, working tree, `main` aggiornato, accessi, vecchie modifiche locali; non fare `reset`, `clean`, stash o checkout distruttivi.
2. Verificare **approvazione EN36** e gate prescritti; disponibilità di **tutte e tre le guide EN34/35/36** approvate, cover su `main`, draft Medium EN con nota IT e nuovo incarico di pubblicazione. Se un requisito non è provato, STOP.
3. Confrontare SHA-256 di questo file 1 con quello autorizzato; in caso di divergenza STOP.
4. Leggere dalla `main` corrente **almeno tre guide International mature** e il template attuale (header, footer, URL, routing, CSS/JS, lingua, JSON-LD e test). Non copiare layout legacy da memoria.
5. Verificare che EN36 non sia già live e identificare la copertina effettiva e gli slug possibili. Controllare la semantica dei link a Mattei/Merloni, dichiarati “Italian edition”.
6. Preparare un elenco puntuale dei file e il diff di rilascio **solo EN36**, incluso quando necessario hub, sitemap, hreflang e loro scope; autorizzazione **separata ed esplicita** dell'autore allo scope EN prima di creare un branch o modificare file.
7. Applicare `05_PROCEDURA_PUBBLICAZIONE_DIRETTA_GITHUB_v2_1.md` e `09_GOVERNANCE_TECNICA_SITO_v1_0.md` adattando solo ciò che il diverso perimetro EN richiede e autorizzando ogni variazione.

## E. Quando una successiva autorizzazione permetterà la conversione

- Testo in HTML **identico** al Markdown congelato: Introduzione, indice, 40 sezioni, quattro moduli, tre tabelle, cronologia §21, 20 FAQ, fonti/copyright, §39 e §40, paragrafi finali inclusi. Nessuna omissione, modifica, parafrasi, riordino o aggiunta “per migliorare il sito”.
- Visualizzazioni disciplinate esclusivamente dalla specifica: §8 (documenti e grado lettura), §16 (poteri del Consiglio), §20 (quattro esperienze territoriali), §21 (cronologia istituzionale non a scala).
- `FAQPage` esattamente **20/20** domande/risposte visibili, stesso ordine e testo. `Article`, `BreadcrumbList`, canonical, OG, alt e hreflang solo da template verificato e pagine pubblicate.
- Rispettare `lang=en`, un solo H1, index anchor, footer/header correnti, CSS senza regressioni, tabelle con `th scope`, didascalie, tastiera, stampa, no-JS e test viewport 320×812 / 390×844 / 1280×900.
- Non rigenerare o ritoccare cover, non rifare il sito o la pagina Triadi, non cambiare pagine IT, non toccare EN34/EN35 salvo autorizzazioni dedicate.
- Non attenuare i validatori per farli risultare PASS; test tecnici ≠ approvazione ≠ pubblicazione ≠ indicizzazione.

## F. STOP

STOP se il master IT non corrisponde, l'EN non è approvato, i gate sono assenti, gli asset/link/URL non sono provati, lo scope supera l'incarico, il testo cambia rispetto all'hash, i poteri del Consiglio vengono rappresentati in modo errato, i dati cronologici vengono confusi, le FAQ differiscono o la rappresentazione visual non è accessibile.

**Questo documento non autorizza Codex a lavorare sul repository.** Dopo i gate e il successivo incarico, l'autore valuterà il preflight, lo scope e la PR, con merge soltanto umano e controllo live successivo. La pagina Triadi International è attività separata.
