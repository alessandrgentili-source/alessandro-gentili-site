# International 3.0 — sistema editoriale e procedura di adattamento

La direzione artistica del prototipo è approvata. Questo documento è il contratto operativo EN: si riusa la composizione, non si riprogetta ogni autore. Il sito resta HTML statico, senza build o dipendenze aggiuntive. Il perimetro di questa PR comprende solo il sistema, l'hub EN e Pasolini; le altre 23 guide e le nove mancanti sono lavori separati.

## Risorse e componenti

Caricare `/assets/international-atlas.css` **dopo** `/assets/style.css`; caricare `/assets/international-atlas.js` con `defer`, dopo lo script comune. Mantenere le classi preesistenti della pagina e aggiungere `international-atlas atlas-guide` al body. Nessuna modifica ai CSS globali, alle cover o a header/footer.

| Componente | Contratto HTML / funzione |
| --- | --- |
| Identità | `.atlas-main` su main, dentro `.international-atlas`: token carta, blu, oro, serif di sistema; nessun font remoto |
| Apertura | `.atlas-breadcrumb`, `.atlas-guide-opening`: hero originale e blocco byline/cover affiancati; su mobile una colonna |
| Lettura | `.wrap.atlas-reader`: `.atlas-contents` + `.guide-body.atlas-reading`; articoli originali come figli diretti, nella stessa sequenza |
| Indice | `.atlas-contents > details[open] > summary` e `nav.guide-toc`: link statici alle sezioni reali, etichetta accessibile con nome autore |
| Corpo | `.guide-section`: paragrafi, liste, titoli e citazioni; ID originali intatti. `#introduction` e `#sources` hanno rispettivamente capilettera e trattamento delle fonti già approvati |
| Relazioni | `.atlas-relation`, `.atlas-nodes`, `.atlas-node`: confronto editoriale opzionale; link EN reali, relazioni motivate; riusabili anche nell'hub |
| Citazione | `details.atlas-citation`: autore della guida, titolo esatto, collana, edizione e canonical; non inventare dati bibliografici |
| Rappresentazione | `figure.atlas-figure` con `aria-labelledby` e `figcaption`: contenitore **opzionale**, con tipografia/spaziatura/stampa comuni; contenuto e controlli specifici del tema |
| Hub | `.atlas-opening`, `.atlas-feature`, `.atlas-routes`, `.atlas-group`, `.atlas-author`: ingressi editoriali e directory statica |

Non rinominare un ID esistente per ottenere il trattamento di introduzione/fonti: se una guida usa ID diversi, mantenerli e lasciare il trattamento base. Non aggiungere capilettera ad aperture non adatte.

Il JS si attiva solo dentro `.international-atlas .atlas-main`. La ricerca si inizializza solo se esiste `.atlas-search`: usa `data-atlas-search`, `data-guide-status`, `.atlas-group`, `.atlas-no-results`, `.atlas-directory-nav`, input e stato live del prototipo. Non genera contenuti o collegamenti; senza JS la directory è integrale e il form resta `hidden`.

L'indice usa gli href, senza nomi o numero di sezioni fissati nel codice. Evidenzia l'ultima sezione il cui inizio ha raggiunto la soglia di lettura (scroll-padding dell'header + scroll-margin del titolo); prima del corpo indica l'apertura, dopo l'ultima voce mantiene quell'orientamento. Durante una figura conserva la sezione precedente. Non forza la selezione in base al solo hash e non sposta il focus durante lo scroll. Si aggiorna su scroll, hash, ripristino cronologia, resize e variazioni di altezza del contenuto. A ≤760 px l'indice è un disclosure; cambiando fascia torna allo stato appropriato. Nella stessa fascia resta valida la scelta del lettore. Senza JS è aperto e tutti i link funzionano.

## Adattare una guida esistente

1. Creare un branch dall'ultima main; annotare il suo SHA come base immutabile. Leggere AGENTS.md e PUBLICATION_WORKFLOW.md; questo sistema EN approvato governa la composizione, mentre Cerchi Publisher resta riferimento di governance. Individuare guida, triade e collegamenti realmente pubblicati.
2. Conservare **byte per byte** tutti gli `<article class="item guide-section" …>…</article>` e la loro sequenza, inclusi fonti e navigazione finale. Conservare anche titolo, sottotitolo, H1, ID, cover/alt, link, header e footer. Non eseguire un formatter sull'intero file. Non copiare il contenuto di Pasolini nell'altro autore.
3. Aggiungere risorse/classi e spostare i blocchi esistenti dentro i contenitori del seguente schema. Usare Pasolini come esempio strutturale completo, mantenendo i contenuti della guida che si sta adattando.
4. Ricostruire l'indice statico dalle sezioni originali nello stesso ordine: ogni voce deve identificare il proprio H2, anche quando mantiene un'abbreviazione editoriale preesistente. Conservare gli href esistenti. Non numerare o riscrivere gli H2 per esigenze grafiche.
5. Inserire eventuali relazioni e rappresentazioni **fra** gli articoli, senza estrarre o sostituire paragrafi. Il testo deve restare comprensibile senza questi moduli. I contenuti supplementari richiedono verifica editoriale: non sono un effetto automatico della migrazione.
6. Eseguire i controlli sotto; confrontare il diff con la base annotata e rivedere desktop, 320 px e modalità senza JS. Aprire una PR circoscritta; nessun merge/deploy implicito.

Schema dei contenitori (i commenti sono istruzioni, non contenuto da pubblicare):

```html
<!-- Body: conservare classi esistenti, aggiungere international-atlas atlas-guide. -->
<a data-atlas-skip class="skip-link" href="#main-content">Skip to content</a>
<!-- Header originale intatto. -->
<main id="main-content" tabindex="-1" class="page guide-page-main atlas-main">
  <!-- Breadcrumb con URL reali; nessuna destinazione futura. -->
  <div class="atlas-guide-opening">
    <!-- Hero originale con wrap hero guide-hero e guide-hero-copy. -->
    <div class="wrap">
      <!-- Byline atlas-byline + figure guide-cover originale. -->
    </div>
  </div>
  <div class="wrap atlas-reader">
    <aside class="atlas-contents">
      <details open>
        <summary>In this guide</summary>
        <nav class="guide-toc" aria-label="NOME AUTORE guide contents">
          <!-- Link statici agli ID originali, nella sequenza del corpo. -->
        </nav>
      </details>
      <!-- Ritorno atlas-back al gruppo reale nell'hub. -->
    </aside>
    <div class="guide-body atlas-reading">
      <!-- Tutti gli articoli originali, intatti e nello stesso ordine. -->
      <!-- Moduli opzionali solo tra articoli. Citazione alla fine. -->
    </div>
  </div>
</main>
<!-- Footer originale intatto; script comune, poi international-atlas.js defer. -->
```

Nessun HTML viene costruito lato client. La pagina resta direttamente leggibile dai crawler e dai lettori senza JavaScript. Il foglio condiviso contiene tutte le regole responsive: niente fogli duplicati per singolo autore o override locali per modificare la direzione artistica.

## Moduli specifici: Pasolini è un esempio, non un obbligo

`assets/international-pasolini.css` contiene esclusivamente layout e controlli `formation-*`; lo carica solo Pasolini, dopo il CSS condiviso. I due pannelli mantengono distinti il contesto storico e l'applicazione contemporanea. Radio nativi, didascalia e link al ragionamento funzionano senza JS; in stampa si leggono entrambi i pannelli.

Altri autori possono richiedere una sequenza temporale, una mappa di relazioni, un confronto, oppure nessuna rappresentazione. Prima di introdurla esplicitare quale passaggio del testo chiarisce e quali limiti evita di confondere. Usare HTML semantico (o SVG con alternativa testuale) e controlli nativi; didascalia e attribuzione visibili, lettura lineare/stampa sempre disponibili. Caricare eventuale CSS/JS specifico solo nella guida interessata, con nomi confinati al modulo. Non aggiungere un'interazione per riempire uno spazio né ridurre l'argomento a una scheda.

## SEO/GEO e integrità

Una migrazione grafica conserva slug, canonical, hreflang reciproci, title/description, Open Graph, Twitter, H1, dati strutturati e date. Non sostituire l'autore della guida (Alessandro Gentili) con l'autore studiato. Le aggiunte `about`/`isPartOf` del prototipo Pasolini sono approvate e coerenti con elementi visibili: non copiarle negli altri autori né considerarle un requisito del sistema. Altri arricchimenti necessitano verifica specifica; il controllo automatico permette nuove proprietà ma rifiuta la modifica di fatti preesistenti.

Verificare fonti, attribuzione, relazione con la triade e collegamenti contestuali. Nessuna FAQ artificiale, risposta generata per AI, keyword forzata o promessa di ranking. Per URL già pubblicate non aggiungere sitemap/lastmod o toccare robots/llms. Controllare le superfici collegate secondo PUBLICATION_WORKFLOW.md; modificarle solo se il cambiamento rende falsa un'informazione già presente. Mai presentare come disponibile una guida futura.

## Controlli ripetibili

Dalla radice, usando lo SHA precedente alla migrazione (qui `origin/main`, dopo fetch):

```sh
python3 tools/check-international-guide.py --base origin/main
node tools/check-international-atlas.mjs
node --check assets/international-atlas.js
python3 tools/check-public-site.py
node tools/check-publication-connections.mjs --self-test
node tools/check-i18n-consistency.mjs
node tools/check-archive-consistency.mjs
git diff --check
```

Il primo comando scopre le guide che caricano il sistema; accetta anche uno o più percorsi espliciti dopo `--base REF`. Controlla articoli identici e ordinati, metadata, fatti JSON-LD, cover, anchor e link originali; verifica corrispondenza/ordine dell'indice. Se la guida usa un wrapper editoriale diverso da `article.guide-section`, si ferma: documentare e verificare la struttura prima di estendere il controllo, senza indebolirlo. La sintassi HTML completa, gli asset e i link locali sono verificati dal gate pubblico. Il test Node copre le regressioni di indice con una fixture DOM; non sostituisce il browser.

La CI International esegue le regressioni JS e, nelle PR, la conservazione delle guide rispetto allo SHA della base. Una nuova guida senza versione precedente richiede la propria procedura editoriale e un'integrazione esplicita dei controlli: questa utility è per adattamenti di testi già pubblicati.

Solo per il perimetro originario a due pagine, `python3 tools/check-international-prototype.py` verifica anche lo scope contro `e9df7f0`. È una prova della presente PR, non il gate delle future estensioni.

Aprire `python3 tools/preview-international.py` → `http://127.0.0.1:8766/__review/`. La vista `/__before/` resta intenzionalmente il confronto storico del prototipo; per future migrazioni usare un checkout della propria base. Testare: 320/390/1280 px; cambio mobile↔desktop; TOC su prima, centrale e ultima voce; scroll avanti/indietro; URL con frammento; Tab/Invio; cambio pannelli; fonti/citazione; assenza di overflow; `/__nojs/` con indice aperto e tutti gli articoli presenti. Nessun audit completo screen reader o risultato Core Web Vitals è implicito in questi test.
