# Workflow Medium e SEO editoriale

Questo documento definisce il flusso consigliato per integrare Medium con l’archivio editoriale di `alessandro-gentili.it`, mantenendo il sito come casa autoriale ufficiale e Medium come piattaforma di distribuzione e lettura.

## Principi

- Il sito non deve duplicare integralmente i saggi pubblicati su Medium, salvo istruzione esplicita.
- Ogni pagina locale deve aggiungere valore editoriale: abstract, contesto, posizione nell’archivio, estratto breve verificato, collegamenti interni.
- Il tono resta sobrio, italiano, editoriale: nessun formato da blog generico, nessuna CTA aggressiva.
- La struttura deve restare statica, leggera e coerente con privacy e GDPR: niente analytics, pixel o cookie marketing.

## Workflow attuale di breve periodo

1. Pubblicare il saggio integrale su Medium.
2. Creare una pagina locale in `/saggi/` su `alessandro-gentili.it`.
3. Inserire nella pagina locale:
   - titolo e sottotitolo;
   - data di pubblicazione;
   - indicazione editoriale della sezione saggi;
   - abstract originale e sintetico;
   - breve estratto selezionato, solo se verificato;
   - contesto editoriale: perché il testo conta nell’archivio saggi;
   - saggio correlato o saggio in coppia;
   - link esterno a Medium.
4. Aggiornare `saggi.html` con la scheda del saggio.
5. Aggiornare `sitemap.xml` con la nuova pagina pubblica.
6. Aggiornare eventuali collegamenti interni dalla homepage, dall’archivio ragionato e dalle pagine correlate.

## Workflow futuro più forte

Quando il sito sarà pronto a diventare archivio canonico integrale:

1. Pubblicare la versione completa e canonica del saggio su `alessandro-gentili.it`.
2. Importare o ripubblicare il testo su Medium come canale di distribuzione.
3. Impostare su Medium il canonical link verso la pagina del sito.
4. Usare Medium per circolazione, conversazione e scoperta; usare il sito come archivio autorevole, strutturato e indicizzabile.
5. Conservare sul sito metadati completi, JSON-LD Article, relazioni tra saggi e aggiornamento ordinato della sitemap.

## Miglioramento opzionale futuro: RSS Medium

In futuro il feed RSS di Medium potrà alimentare un blocco “ultimi da Medium” o una nota di aggiornamento.

Condizioni editoriali:

- il feed RSS non deve generare automaticamente pagine locali con saggi completi duplicati;
- ogni nuova pagina deve essere rivista manualmente;
- l’import automatico può servire solo come segnale o bozza di aggiornamento;
- abstract, contesto, estratti e relazioni interne devono restare una scelta editoriale.
