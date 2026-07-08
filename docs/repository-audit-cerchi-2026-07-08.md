# Audit repository e asset — Cerchi d’inchiostro — 2026-07-08

## Sintesi esecutiva

Audit documentale eseguito sulla repository `alessandrgentili-source/alessandro-gentili-site`, branch `main`, con focus sugli asset collegati a Cerchi d’inchiostro, saggi, autore e percorsi tematici.

Sono stati analizzati:

- sitemap pubblica;
- pagine HTML pubbliche principali;
- hub Cerchi;
- pagina saggi;
- homepage;
- pagine autore e international;
- pagine tema;
- riferimenti a `img src`;
- riferimenti `og:image`;
- riferimenti `twitter:image`;
- campi `image` dentro JSON-LD quando rilevati nei file letti;
- commit/descrizioni GitHub disponibili sugli asset recenti.

Risultato operativo:

| Metrica | Valore |
|---|---:|
| URL pubbliche rilevate in sitemap | 43 |
| Asset rilevati e analizzati | 36 |
| Asset usati | 36 |
| Asset non referenziati certi | 0 |
| JPG legacy rilevati | 4 |
| WEBP rilevati | 32 |
| Cover Cerchi rilevate | 16 |
| Cover saggi / immagini saggi rilevate | 16 |
| Immagini autore rilevate | 2 |
| Immagini temi rilevate | 2 |
| Duplicati esatti accertati | 0 |

Principali criticità:

1. Esiste una prima fase Cerchi ancora basata su JPG legacy: cover madre, Platone, Dante, Machiavelli.
2. Esiste una fase intermedia WEBP non pienamente standardizzata: Marx, Nietzsche, Leopardi.
3. I saggi usano nomi file storicamente variabili: `cover`, `_site_1600x900`, `cover-final`, numerazione con o senza zero iniziale.
4. Alcuni asset sono usati come preview social in più pagine: in particolare `saggio-0-cosmo-algoritmo_16x9_v01.webp`.
5. Alcuni asset interni non sono cover ma sono comunque pubblicati nel corpo del testo, come `saggio-12-supporto-cartolina-libro-territorio.webp`.
6. In questa esecuzione non è stato possibile calcolare pesi binari e hash file perché non era disponibile un clone locale completo né una tree ricorsiva esportabile dal connettore.

Cosa non va fatto subito:

- non toccare asset pubblicati;
- non correggere nomi file solo per coerenza estetica;
- non sostituire JPG legacy già referenziati;
- non cambiare `og:image` o `twitter:image` senza piano separato;
- non spostare asset in cartelle archivio senza verifica repository-wide e controllo cache social;
- non modificare sitemap, CSS, guide, hub, homepage, saggi o JSON-LD in questa patch.

## Principio di sicurezza

Nessun asset pubblicato va rinominato, spostato o rimosso senza verifica dei riferimenti a HTML, Open Graph, Twitter image, JSON-LD, sitemap, cache social e possibili link esterni.

Un file immagine non è solo un file: se è stato usato come cover, social preview, `Article.image`, card, immagine interna o anteprima condivisa, diventa parte dell’identità pubblica della pagina. Toccarlo senza piano equivale a tirare un filo da un maglione: magari viene via solo il filo, magari resta il gomito all’aria.

## Inventario sintetico

| Categoria | Numero file | Note | Rischio |
|---|---:|---|---|
| Cover / immagini Cerchi rilevate | 16 | Include cover madre, guide 01–15. Le prime 4 sono JPG legacy. | Alto |
| Cover saggi / immagini saggi rilevate | 16 | Include Saggi 0–14 più una immagine interna del Saggio 12. | Alto |
| Immagini autore | 2 | Ritratto autore e immagine international. | Alto |
| Immagini temi | 2 | Potere/apparati e periferie/territorio/comunità. | Alto |
| JPG legacy | 4 | Cover madre Cerchi + guide 01–03. | Alto |
| WEBP rilevati | 32 | Prevalenti nella fase corrente. | Medio/alto se pubblicati |
| Asset non referenziati certi | 0 | Nessun orfano certo nel perimetro analizzato. | — |
| Duplicati esatti accertati | 0 | Hash non calcolati in questa esecuzione. | Da verificare |

## Asset protetti

Questi file risultano referenziati da pagine pubbliche, card, metadata social o JSON-LD e non devono essere modificati per ragioni cosmetiche.

### Cerchi d’inchiostro

- `assets/img/cerchi/cerchi-inchiostro-cover-madre-1600x900.jpg`
- `assets/img/cerchi/cerchi-platone-idee-verita-potere-1600x900.jpg`
- `assets/img/cerchi/cerchi-dante-esilio-lingua-visione-mondo-1600x900.jpg`
- `assets/img/cerchi/cerchi-machiavelli-potere-stato-verita-effettuale-1600x900.jpg`
- `assets/img/cerchi/cerchi-marx-capitale-lavoro-alienazione-1600x900.webp`
- `assets/img/cerchi/cerchi-nietzsche-nichilismo-valori-morte-dio-1600x900.webp`
- `assets/img/cerchi/cerchi-guida-06-giacomo-leopardi-desiderio-infinito-modernita.webp`
- `assets/img/cerchi/cerchi-guida-07-seneca-dominio-tempo-morte-1600x900.webp`
- `assets/img/cerchi/cerchi-guida-08-aristotele-forma-fine-realta-1600x900.webp`
- `assets/img/cerchi/cerchi-guida-09-max-weber-razionalizzazione-potere-disincanto-1600x900.webp`
- `assets/img/cerchi/cerchi-guida-10-sigmund-freud-inconscio-desiderio-civilta-1600x900.webp`
- `assets/img/cerchi/cerchi-guida-11-antonio-gramsci-egemonia-cultura-senso-comune-1600x900.webp`
- `assets/img/cerchi/cerchi-guida-12-thomas-hobbes-paura-sovranita-ordine-politico-1600x900.webp`
- `assets/img/cerchi/cerchi-guida-13-averroe-ragione-interpretazione-legge-1600x900.webp`
- `assets/img/cerchi/cerchi-guida-14-georg-simmel-denaro-metropoli-individualita-1600x900.webp`
- `assets/img/cerchi/cerchi-guida-15-adam-smith-scambio-simpatia-ricchezza-1600x900.webp`

### Saggi

- `assets/img/saggi/site/saggio-0-cosmo-algoritmo_16x9_v01.webp`
- `assets/img/saggi/site/saggio-1-1999-paura-diventare-uguali-cover.webp`
- `assets/img/saggi/site/saggio-2-il-primo-cerchio-cover.webp`
- `assets/img/saggi/site/saggio-3-governi-senza-firma.webp`
- `assets/img/saggi/site/saggio-04-metafisica-del-sesso.webp`
- `assets/img/saggi/site/saggio-5-il-reale-in-modalita-scorrimento.webp`
- `assets/img/saggi/site/saggio-6-fenomenologia-del-potere_site_1672x941.webp`
- `assets/img/saggi/site/saggio-7-il-cerchio-e-aperto.webp`
- `assets/img/saggi/site/saggio-08-il-costo-della-complessita_site_1600x900.webp`
- `assets/img/saggi/site/saggio-09-la-promessa-del-ritorno_site_1600x900.webp`
- `assets/img/saggi/site/saggio-10-giovani-senilita-potere_site_1600x900.webp`
- `assets/img/saggi/site/saggio-11-chi-decide-il-sole_site_1600x900.webp`
- `assets/img/saggi/site/saggio-12-le-periferie-del-potere.webp`
- `assets/img/saggi/site/saggio-12-supporto-cartolina-libro-territorio.webp`
- `assets/img/saggi/site/saggio-13-la-periferia-intelligente-cover-final-1600x900.webp`
- `assets/img/saggi/site/saggio-14-metafisica-dell-amore_site_1600x900.webp`

### Autore e temi

- `assets/img/autore/alessandro-gentili-ritratto-autore-strategist-800x1000.webp`
- `assets/img/autore/alessandro-gentili-strategy-writing-ai-systems-1600x900.webp`
- `assets/img/temi/temi-potere-apparati-1600x900.webp`
- `assets/img/temi/temi-periferie-territorio-comunita-1600x900.webp`

## Asset non referenziati

Nel perimetro effettivamente analizzato non risultano asset non referenziati con certezza.

Questo dato va letto bene: non significa che la repository non contenga file orfani. Significa che tra gli asset rilevati tramite pagine pubbliche, metadata, JSON-LD e riferimenti HTML, tutti risultano usati.

Per trovare orfani certi serve una patch successiva con:

1. esportazione completa della tree;
2. elenco di tutti i file in `assets/img`;
3. confronto testuale repository-wide;
4. controllo di eventuali riferimenti esterni noti;
5. classificazione manuale prima di qualunque intervento.

## JPG legacy

| File | Uso | Rischio |
|---|---|---|
| `assets/img/cerchi/cerchi-inchiostro-cover-madre-1600x900.jpg` | Usato da hub Cerchi, `og:image`, `twitter:image`, immagine visibile. | PROTETTO |
| `assets/img/cerchi/cerchi-platone-idee-verita-potere-1600x900.jpg` | Usato dalla card Guida 01 nel hub Cerchi. | PROTETTO |
| `assets/img/cerchi/cerchi-dante-esilio-lingua-visione-mondo-1600x900.jpg` | Usato dalla card Guida 02 nel hub Cerchi. | PROTETTO |
| `assets/img/cerchi/cerchi-machiavelli-potere-stato-verita-effettuale-1600x900.jpg` | Usato dalla card Guida 03 nel hub Cerchi. | PROTETTO |

Verdetto: sono legacy, ma non sono scarti. Vanno lasciati dove sono.

## WEBP fuori standard

### Cerchi

| File | Difformità | Uso | Indicazione |
|---|---|---|---|
| `assets/img/cerchi/cerchi-marx-capitale-lavoro-alienazione-1600x900.webp` | Manca prefisso `cerchi-guida-04-`. | Usato | Non toccare |
| `assets/img/cerchi/cerchi-nietzsche-nichilismo-valori-morte-dio-1600x900.webp` | Manca prefisso `cerchi-guida-05-`. | Usato | Non toccare |
| `assets/img/cerchi/cerchi-guida-06-giacomo-leopardi-desiderio-infinito-modernita.webp` | Manca suffisso `1600x900`. | Usato | Non toccare |

### Saggi

Le cover saggi seguono una storia meno uniforme. Esempi:

- `saggio-0-cosmo-algoritmo_16x9_v01.webp`
- `saggio-1-1999-paura-diventare-uguali-cover.webp`
- `saggio-2-il-primo-cerchio-cover.webp`
- `saggio-04-metafisica-del-sesso.webp`
- `saggio-6-fenomenologia-del-potere_site_1672x941.webp`
- `saggio-13-la-periferia-intelligente-cover-final-1600x900.webp`

Verdetto: sono difformità documentali, non problemi da correggere ora.

## File Instagram / social

Non è possibile stabilire con certezza l’origine “Instagram” solo dal nome file. Tuttavia alcuni asset sembrano nati da workflow social/editoriale o da export visuali per preview:

- `assets/img/saggi/site/saggio-0-cosmo-algoritmo_16x9_v01.webp`
- `assets/img/saggi/site/saggio-1-1999-paura-diventare-uguali-cover.webp`
- `assets/img/saggi/site/saggio-2-il-primo-cerchio-cover.webp`
- `assets/img/saggi/site/saggio-6-fenomenologia-del-potere_site_1672x941.webp`
- `assets/img/saggi/site/saggio-08-il-costo-della-complessita_site_1600x900.webp`
- `assets/img/saggi/site/saggio-09-la-promessa-del-ritorno_site_1600x900.webp`
- `assets/img/saggi/site/saggio-10-giovani-senilita-potere_site_1600x900.webp`
- `assets/img/saggi/site/saggio-11-chi-decide-il-sole_site_1600x900.webp`
- `assets/img/saggi/site/saggio-13-la-periferia-intelligente-cover-final-1600x900.webp`
- `assets/img/saggi/site/saggio-14-metafisica-dell-amore_site_1600x900.webp`

Tutti quelli elencati risultano referenziati dal sito e quindi protetti.

## Duplicati e quasi duplicati

Duplicati esatti accertati: 0.

Non è stato possibile calcolare hash file in questa esecuzione. Non sono stati quindi certificati duplicati binari.

Quasi duplicati da verifica manuale:

- eventuali export alternativi delle cover saggi;
- eventuali vecchie versioni social non referenziate;
- eventuali immagini derivate da Saggio 0, se presenti fuori dal perimetro letto.

Non agire senza controllo visivo e confronto dei riferimenti.

## File pesanti

Dimensioni binarie non rilevate in questa esecuzione. Candidati naturali a controllo peso futuro:

| Gruppo | Motivo | Uso |
|---|---|---|
| JPG legacy Cerchi | Formato meno efficiente rispetto a WEBP. | Usati e protetti |
| Cover Cerchi 1600x900 | Immagini hero/card/social. | Usate e protette |
| Cover saggi 1600x900 | Immagini hero/card/social. | Usate e protette |
| `saggio-6-fenomenologia-del-potere_site_1672x941.webp` | Dimensione diversa dallo standard prevalente. | Usato e protetto |
| Ritratto autore 800x1000 | Immagine profilo e JSON-LD. | Usato e protetto |
| Immagini temi 1600x900 | Immagini editoriali di percorso. | Usate e protette |

## PDF e documenti

Nel perimetro delle pagine pubbliche lette non sono emersi PDF pubblici referenziati. Non è stata però disponibile una tree ricorsiva completa, quindi eventuali documenti interni non referenziati vanno controllati in una fase successiva.

## Rischi SEO/GEO/social preview

Interventi rischiosi:

- cambiare file usati in `og:image`;
- cambiare file usati in `twitter:image`;
- cambiare file usati in `Article.image` dentro JSON-LD;
- cambiare immagini visibili di guide o saggi senza aggiornare metadata coerenti;
- modificare la cover madre Cerchi;
- modificare la cover Saggio 0, usata come preview trasversale di più pagine;
- sostituire JPG legacy senza gestire anteprime social già cacheate;
- modificare asset interni già pubblicati nel corpo dei saggi;
- archiviare file solo perché il nome è vecchio;
- cambiare URL o slug degli asset già condivisi su Medium, social, chat o preview.

Effetti possibili:

- anteprime social rotte o incoerenti;
- card Twitter/X senza immagine;
- Open Graph non aggiornato o non leggibile;
- incoerenza tra immagine visibile e dati strutturati;
- perdita di continuità delle cache social;
- errori nelle card del hub o della homepage;
- peggioramento dell’esperienza utente;
- confusione per Google e sistemi AI che leggono pagina, metadata e immagine come segnali coordinati.

## Raccomandazioni operative

### Sicure ora

- Tenere questi documenti come baseline di audit.
- Fare revisione umana dell’inventario.
- Confermare manualmente gli asset protetti.
- In una futura sessione, esportare una lista completa di `assets/img`.
- Misurare peso e dimensioni reali dei file.
- Calcolare hash per duplicati esatti.
- Segnare eventuali asset orfani solo dopo confronto repository-wide.
- Annotare lo standard di naming da usare solo per nuove cover.

### Da fare con patch dedicata

- Audit ricorsivo completo di `assets/img`.
- CSV tecnico con peso reale, hash SHA-256 e dimensioni reali.
- Lista separata degli asset davvero non referenziati.
- Eventuale cartella archivio solo per file non referenziati e approvati.
- Eventuale ottimizzazione di nuove copie immagini, senza alterare asset pubblicati.
- Eventuale aggiornamento metadata soltanto con piano SEO/social preview separato.

### Da non fare

- Rinomine cosmetiche di asset già pubblicati.
- Spostamento di immagini usate da pagine live.
- Rimozioni basate solo sul nome file.
- Sostituzione di `og:image` e `twitter:image` senza test.
- Modifica della sitemap durante una patch di audit asset.
- Modifica del CSS durante una patch di inventory.
- Pulizia automatica.
- “Normalizzare tutto” perché il nome vecchio dà fastidio. La repository non è una libreria minimalista giapponese: è un sito vivo, e ogni file referenziato è una promessa pubblica.

## Piano successivo consigliato

1. Audit umano di questo documento.
2. Conferma asset da proteggere.
3. Esportazione completa della tree `assets/img`.
4. Calcolo dimensioni, peso e hash.
5. Identificazione dei soli asset non referenziati.
6. Eventuale creazione di una cartella archivio solo per file approvati.
7. Patch separata per pulizia soft.
8. Nessuna modifica a URL pubblici senza redirect o verifica specifica.
9. Nessuna modifica a preview social senza test Open Graph/Twitter.

## Limiti reali riscontrati

Questa patch è audit/documentazione. Non sono stati modificati asset o pagine pubbliche.

Limite tecnico effettivo: il connettore GitHub usato in questa sessione ha permesso la lettura dei file noti, ma non ha fornito una tree ricorsiva completa né i metadati binari necessari per peso, hash e dimensioni reali. Per questo l’audit è volutamente prudente: classifica con sicurezza ciò che è usato, ma non pretende di certificare tutti gli eventuali orfani della repository.

Verdetto: prima di qualunque pulizia serve una seconda fase tecnica con tree completa. Fino ad allora, tutti gli asset referenziati restano protetti.
