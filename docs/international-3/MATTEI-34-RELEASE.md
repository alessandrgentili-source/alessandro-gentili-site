# Mattei 34 — proposta di rilascio IT

Branch: `feat/cerchi-publisher-atlas-mattei-it`, base `785525b33b38b6aabe5244f0e0ac8c30e8b620d8`. Il rilascio è ora autorizzato fino a commit, push e apertura PR verso main; **merge e deploy restano esclusi fino al controllo umano della PR**.

## Conservazione

Pagina pubblica, cover e CSS specifico sono copie byte-identiche del DRAFT arricchito già validato, conservato in `.agents/skills/cerchi-publisher/pilots/mattei/site/`. Nessuna riscrittura dei 41 articoli, nessuna modifica a H1, metadati, JSON-LD o figure. Master e cover conservano i rispettivi SHA-256 approvati; il gate del pilota controlla inoltre gli hash degli articoli originari e dei metadati.

La copia DRAFT e le prove visive restano disponibili. Per la proposta pubblica si esegue `PUBLICATION`; le regressioni DRAFT vengono eseguite in una fixture temporanea della base precedente alla pubblicazione. Nessuna barriera DRAFT/PUBLICATION è rimossa.

## Perimetro

- Nuovi file pubblici: guida IT `cerchi/guide/enrico-mattei-energia-impresa-pubblica-autonomia/index.html`, cover approvata, `assets/cerchi-mattei.css` confinato a Mattei.
- Skill Cerchi Publisher, contratto Atlas, validatore e CI già preparati nel pilot, con eccezioni esplicite per hero senza duplicazione, apertura nell'indice e figure statiche approvate. Nessuna traduzione automatica senza richiesta esplicita e revisione umana.
- Hub IT: card Guida 34 e conteggio 34.
- Triadi IT: percorso dodicesimo **in apertura**, senza fingere una triade completa; link alla sola guida Mattei e inserimento nel `hasPart` della raccolta.
- Sitemap: solo l'URL IT Mattei, senza lastmod inventato.
- Inventario i18n: Mattei dichiarato IT-only. Nessuna URL EN Mattei, hreflang reciproca o promessa di traduzione pubblicata.
- Archivio: soli conteggi IT 33→34; EN Positioning: correzione della consistenza dell'archivio italiano; Triads EN: solo richiamo esplicito al percorso italiano, con link IT. Le triadi complete restano 11 IT e 11 EN.
- `llms.txt`: conteggio IT e chiarimento sul nuovo percorso italiano.

Home IT/EN, altre guide, CSS e JS globali, robots e tutte le URL preesistenti restano invariati. Nessun nuovo componente grafico o dipendenza.

## Verifiche locali

PASS: PUBLICATION sulla pagina pubblica; integrità pilota e tutte le mutazioni; sito pubblico (116 HTML, 8.100 riferimenti locali); i18n (34 IT / 33 EN, 11 / 11 triadi complete); connessioni editoriali con self-test; archivio; Atlas JS; preservazione guide EN rispetto alla base; regressione Plato EN_REVISION; skill e sintassi YAML. Prove desktop/mobile/no-JS/stampa nel [rapporto del pilot](MATTEI-34-REVIEW.md).

`git diff --check` viene eseguito sul codice e sugli artefatti generati. Il solo master immutabile conserva le righe vuote con spazi finali già presenti nel file approvato: non viene formattato per eliminare tali segnalazioni. Il suo hash verifica separatamente la conservazione esatta.

La CI GitHub viene verificata sulla PR dopo il push; l'esito remoto va letto nei check della PR. Un gate verde non sostituisce il controllo umano e non autorizza il merge. La proposta IT non comprende l'edizione EN, che sarà preparata su branch distinta e sottoposta a revisione editoriale prima di qualunque PR EN.

Rollback: prima del merge modificare o chiudere la PR. Dopo un eventuale merge autorizzato, revert del commit di rilascio e ripetizione dei gate pubblici.
