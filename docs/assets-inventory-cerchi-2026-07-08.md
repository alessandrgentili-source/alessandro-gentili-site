# Inventario asset — Cerchi d’inchiostro — 2026-07-08

## Nota metodologica

Questo inventario è stato prodotto come audit documentale e conservativo. Sono stati letti sitemap, pagine HTML pubbliche, riferimenti a immagini dentro `img src`, `og:image`, `twitter:image` e campi `image` dei JSON-LD quando rilevati nei file ispezionati.

In questa esecuzione non era disponibile un clone locale completo della repository né una lista ricorsiva della tree tramite il connettore GitHub. Per questo motivo:

- la colonna “Dimensione” resta `non rilevata` dove il connettore non ha esposto il peso binario;
- gli hash dei file non sono stati calcolati;
- l’elenco degli asset non referenziati va considerato prudenziale: non sono emersi asset orfani certi nel perimetro letto, ma serve una scansione ricorsiva completa in una patch futura per chiudere il tema in modo definitivo.

La classificazione privilegia la sicurezza: ogni asset trovato in pagine pubbliche, metadata social, JSON-LD o card live è segnato come `PROTETTO`.

## Riepilogo numerico

| Voce | Numero |
|---|---:|
| Asset rilevati e analizzati | 36 |
| Asset usati | 36 |
| Asset non referenziati certi | 0 |
| Asset da verificare con scansione ricorsiva completa | non quantificabile qui |
| JPG legacy rilevati | 4 |
| WEBP rilevati | 32 |
| Cover Cerchi rilevate | 16 |
| Cover saggi / immagini saggi rilevate | 16 |
| Immagini autore rilevate | 2 |
| Immagini temi rilevate | 2 |
| Duplicati esatti accertati | 0 |

## Tabella dettagliata

| Percorso | Estensione | Dimensione | Dimensioni immagine | Stato uso | Dove è referenziato | Tipo presunto | Rischio modifica | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| assets/img/cerchi/cerchi-inchiostro-cover-madre-1600x900.jpg | jpg | non rilevata | 1600x900 da nome/HTML | USATO | cerchi/index.html: og:image, twitter:image, immagine hero | immagine Open Graph / cover madre Cerchi / legacy | PROTETTO — non rinominare, non spostare, non rimuovere | JPG legacy ancora attivo e usato come preview social del hub Cerchi. |
| assets/img/cerchi/cerchi-platone-idee-verita-potere-1600x900.jpg | jpg | non rilevata | 1600x900 da nome/HTML | USATO | cerchi/index.html card Guida 01; probabile guida Platone e preview | cover guida Cerchi / legacy | PROTETTO — non rinominare, non spostare, non rimuovere | Nome pre-standard, ma pubblicato e referenziato. |
| assets/img/cerchi/cerchi-dante-esilio-lingua-visione-mondo-1600x900.jpg | jpg | non rilevata | 1600x900 da nome/HTML | USATO | cerchi/index.html card Guida 02; probabile guida Dante e preview | cover guida Cerchi / legacy | PROTETTO — non rinominare, non spostare, non rimuovere | Nome pre-standard, ma pubblicato e referenziato. |
| assets/img/cerchi/cerchi-machiavelli-potere-stato-verita-effettuale-1600x900.jpg | jpg | non rilevata | 1600x900 da nome/HTML | USATO | cerchi/index.html card Guida 03; probabile guida Machiavelli e preview | cover guida Cerchi / legacy | PROTETTO — non rinominare, non spostare, non rimuovere | Nome pre-standard, ma pubblicato e referenziato. |
| assets/img/cerchi/cerchi-marx-capitale-lavoro-alienazione-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | index.html, cerchi/index.html, guida Marx / preview probabile | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | WEBP corretto, ma non segue lo standard `cerchi-guida-NN-...`. |
| assets/img/cerchi/cerchi-nietzsche-nichilismo-valori-morte-dio-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | index.html, cerchi/index.html, guida Nietzsche / preview probabile | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | WEBP corretto, ma non segue lo standard `cerchi-guida-NN-...`. |
| assets/img/cerchi/cerchi-guida-06-giacomo-leopardi-desiderio-infinito-modernita.webp | webp | non rilevata | 1600x900 da HTML | USATO | index.html, cerchi/index.html, guida Leopardi / preview probabile | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | Manca suffisso dimensionale nel filename; non correggere ora. |
| assets/img/cerchi/cerchi-guida-07-seneca-dominio-tempo-morte-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | index.html, cerchi/index.html, guida Seneca / preview probabile | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | Coerente con standard attuale. |
| assets/img/cerchi/cerchi-guida-08-aristotele-forma-fine-realta-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | index.html, cerchi/index.html, guida Aristotele, OG/Twitter/JSON-LD probabili | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | Coerente con standard attuale. |
| assets/img/cerchi/cerchi-guida-09-max-weber-razionalizzazione-potere-disincanto-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | index.html, cerchi/index.html, guida Weber / preview probabile | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | Coerente con standard attuale. |
| assets/img/cerchi/cerchi-guida-10-sigmund-freud-inconscio-desiderio-civilta-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | index.html, cerchi/index.html, guida Freud / preview probabile | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | Coerente con standard attuale. |
| assets/img/cerchi/cerchi-guida-11-antonio-gramsci-egemonia-cultura-senso-comune-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | index.html, cerchi/index.html, guida Gramsci / preview probabile | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | Coerente con standard attuale. |
| assets/img/cerchi/cerchi-guida-12-thomas-hobbes-paura-sovranita-ordine-politico-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | index.html, cerchi/index.html, guida Hobbes / preview probabile | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | Coerente con standard attuale. |
| assets/img/cerchi/cerchi-guida-13-averroe-ragione-interpretazione-legge-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | cerchi/index.html, guida Averroè / preview probabile | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | Coerente con standard attuale. |
| assets/img/cerchi/cerchi-guida-14-georg-simmel-denaro-metropoli-individualita-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | cerchi/index.html, guida Simmel / preview probabile | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | Coerente con standard attuale. |
| assets/img/cerchi/cerchi-guida-15-adam-smith-scambio-simpatia-ricchezza-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | cerchi/index.html, guida Adam Smith / preview probabile | cover guida Cerchi | PROTETTO — non rinominare, non spostare, non rimuovere | Coerente con standard attuale. |
| assets/img/saggi/site/saggio-0-cosmo-algoritmo_16x9_v01.webp | webp | non rilevata | 1600x900 da HTML | USATO | index.html, saggi.html, autore.html, home/saggi/autore OG/Twitter, card Saggio 0 | cover saggio / immagine Open Graph | PROTETTO — non rinominare, non spostare, non rimuovere | Asset molto centrale: preview social di più pagine. |
| assets/img/saggi/site/saggio-1-1999-paura-diventare-uguali-cover.webp | webp | non rilevata | 1600x900 da HTML | USATO | saggi.html, pagina Saggio 1 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Nome non pienamente uniforme rispetto ai file `_site_1600x900`. |
| assets/img/saggi/site/saggio-2-il-primo-cerchio-cover.webp | webp | non rilevata | 1600x900 da HTML | USATO | saggi.html, pagina Saggio 2, OG/Twitter probabili | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Nome non pienamente uniforme rispetto ai file `_site_1600x900`. |
| assets/img/saggi/site/saggio-3-governi-senza-firma.webp | webp | non rilevata | 1600x900 da HTML | USATO | saggi.html, pagina Saggio 3 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Nome compatto legacy. |
| assets/img/saggi/site/saggio-04-metafisica-del-sesso.webp | webp | non rilevata | 1600x900 da HTML | USATO | saggi.html, pagina Saggio 4 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Numerazione con zero iniziale diversa da altri saggi. |
| assets/img/saggi/site/saggio-5-il-reale-in-modalita-scorrimento.webp | webp | non rilevata | 1600x900 da HTML | USATO | saggi.html, pagina Saggio 5 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Nome legacy ma attivo. |
| assets/img/saggi/site/saggio-6-fenomenologia-del-potere_site_1672x941.webp | webp | non rilevata | 1672x941 da nome/HTML | USATO | saggi.html, pagina Saggio 6 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Dimensione non 1600x900: candidato a verifica peso/ratio in futura patch. |
| assets/img/saggi/site/saggio-7-il-cerchio-e-aperto.webp | webp | non rilevata | 1600x900 da HTML | USATO | saggi.html, pagina Saggio 7 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Nome legacy ma attivo. |
| assets/img/saggi/site/saggio-08-il-costo-della-complessita_site_1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | saggi.html, pagina Saggio 8 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Nome con zero iniziale e suffisso `_site_`. |
| assets/img/saggi/site/saggio-09-la-promessa-del-ritorno_site_1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | saggi.html, pagina Saggio 9 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Nome con zero iniziale e suffisso `_site_`. |
| assets/img/saggi/site/saggio-10-giovani-senilita-potere_site_1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | saggi.html, index.html precedente/possibile, pagina Saggio 10 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Formato coerente recente. |
| assets/img/saggi/site/saggio-11-chi-decide-il-sole_site_1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | saggi.html, index.html precedente/possibile, pagina Saggio 11 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Formato coerente recente. |
| assets/img/saggi/site/saggio-12-le-periferie-del-potere.webp | webp | non rilevata | 1600x900 da HTML | USATO | index.html, saggi.html, Saggio 12 head/body/Article JSON-LD | cover saggio / immagine Open Graph | PROTETTO — non rinominare, non spostare, non rimuovere | Asset centrale per Saggio 12 e preview social. |
| assets/img/saggi/site/saggio-12-supporto-cartolina-libro-territorio.webp | webp | non rilevata | non rilevabile da HTML | USATO | saggi/saggio-12-le-periferie-del-potere.html immagine interna articolo | immagine interna articolo | PROTETTO — non rinominare, non spostare, non rimuovere | Immagine interna: non è cover, ma è pubblicata nel corpo del saggio. |
| assets/img/saggi/site/saggio-13-la-periferia-intelligente-cover-final-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | index.html, saggi.html, pagina Saggio 13 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | `cover-final` segnala possibile export da workflow grafico/social, ma è pubblicato. |
| assets/img/saggi/site/saggio-14-metafisica-dell-amore_site_1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | index.html, saggi.html, pagina Saggio 14 / preview probabile | cover saggio | PROTETTO — non rinominare, non spostare, non rimuovere | Formato coerente recente. |
| assets/img/autore/alessandro-gentili-ritratto-autore-strategist-800x1000.webp | webp | non rilevata | 800x1000 da nome/HTML | USATO | autore.html body, Person JSON-LD image | immagine autore / profilo | PROTETTO — non rinominare, non spostare, non rimuovere | Usata anche in dati strutturati. |
| assets/img/autore/alessandro-gentili-strategy-writing-ai-systems-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | en.html immagine editoriale | immagine Open Graph potenziale / immagine autore | PROTETTO — non rinominare, non spostare, non rimuovere | Immagine editoriale international. |
| assets/img/temi/temi-potere-apparati-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | temi/potere-apparati.html | immagine interna articolo / percorso tematico | PROTETTO — non rinominare, non spostare, non rimuovere | Immagine editoriale di percorso tema. |
| assets/img/temi/temi-periferie-territorio-comunita-1600x900.webp | webp | non rilevata | 1600x900 da nome/HTML | USATO | temi/periferie-territorio-comunita.html | immagine interna articolo / percorso tematico | PROTETTO — non rinominare, non spostare, non rimuovere | Immagine editoriale di percorso tema. |

## Lettura operativa

Gli asset Cerchi delle guide 01–03 e la cover madre sono ancora JPG e hanno nomi pre-standard, ma sono referenziati in pagine pubbliche e in preview social: sono quindi protetti.

Le guide 04–06 mostrano una transizione di naming: WEBP già corretti come formato, ma non ancora completamente allineati allo standard `cerchi-guida-NN-nome-autore-temi-principali-1600x900.webp`. Anche in questo caso non va proposta alcuna rinomina immediata.

Dalla guida 07 alla guida 15 lo standard è sostanzialmente consolidato: `cerchi-guida-NN-...-1600x900.webp`.

Le immagini dei saggi seguono invece uno standard storico più variabile: `cover`, `_site_1600x900`, `cover-final`, numerazione con o senza zero iniziale. La variabilità va documentata, non corretta a freddo.

## Asset non referenziati

Nel perimetro analizzato non sono stati individuati asset non referenziati con certezza. Questo non dimostra che la repository sia priva di asset orfani: significa soltanto che tutti gli asset emersi dalla lettura delle pagine pubbliche e dei metadata risultano usati.

Per individuare veri orfani serve una patch successiva con accesso a una tree ricorsiva completa, confronto testuale repository-wide e, idealmente, hash binari.

## Candidati a verifica futura

| Percorso / gruppo | Motivo | Rischio |
|---|---|---|
| `assets/img/cerchi/*.jpg` | JPG legacy ancora attivi; verificare peso e opportunità di eventuale copia WEBP futura senza toccare URL pubblici esistenti. | Alto se si cambia il file referenziato; medio solo se si crea nuova variante non collegata |
| `assets/img/saggi/site/*cover*` | Naming variabile, possibile origine da workflow social/editoriale. | Alto se referenziati; basso solo per eventuali file non referenziati da confermare |
| `assets/img/saggi/site/*_site_*.webp` | File probabilmente nati per pubblicazione sito/social. | Protetti se referenziati |
| `assets/img/saggi/site/saggio-6-fenomenologia-del-potere_site_1672x941.webp` | Ratio/dimensione diversa dallo standard prevalente 1600x900. | Protetto; verificare solo peso e resa |
| `assets/img/saggi/site/saggio-12-supporto-cartolina-libro-territorio.webp` | Immagine interna articolo, non cover. | Protetta perché pubblicata nel corpo del saggio |

## Duplicati

Duplicati esatti accertati: 0.

La verifica tramite hash non è stata possibile in questa esecuzione; quindi il valore indica soltanto che non sono emersi duplicati testuali o funzionali certi nel perimetro dei riferimenti letti.

## File pesanti

Il peso binario non è stato rilevabile da questa esecuzione. I principali candidati a controllo peso futuro sono:

- cover 1600x900 delle guide Cerchi;
- cover 1600x900 dei saggi;
- `saggio-6-fenomenologia-del-potere_site_1672x941.webp`;
- immagini JPG legacy della prima fase Cerchi;
- ritratto autore 800x1000;
- immagini temi 1600x900.

Non intervenire sui file: prima misurare, poi decidere.
