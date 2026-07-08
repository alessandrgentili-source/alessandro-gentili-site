# Cerchi d’inchiostro — standard operativo guide autore

## 1. Scopo dello standard

Questo documento definisce il contratto operativo interno per creare e revisionare le guide autore di Cerchi d’inchiostro. Lo standard serve a mantenere coerenza strutturale, visiva, SEO, semantica e di navigazione tra guide di generazioni diverse, senza modificare pagine pubbliche o contenuti editoriali fuori da patch dedicate.

La regola generale è conservativa: quando esiste un modello approvato, non si crea una nuova variante. Prima si individua la guida più recente e più coerente, poi si applica quello standard.

## 2. Struttura obbligatoria della guida

Ogni guida autore deve contenere:

1. meta title;
2. meta description;
3. canonical self-referencing;
4. Open Graph title, description, image;
5. Twitter card/title/description/image;
6. Article JSON-LD;
7. BreadcrumbList JSON-LD;
8. FAQPage JSON-LD quando sono presenti FAQ visibili;
9. hero compatto;
10. cover 1600x900;
11. indice `.guide-toc`;
12. sezioni corpo;
13. Fonti;
14. Prosegui la lettura;
15. Chiusura editoriale.

## 3. Hero standard

Il hero deve essere compatto e uniforme. Deve contenere solo:

- eyebrow: `Guida NN · Cerchi d’inchiostro`;
- H1;
- sottotitolo/lead breve, massimo circa 90 caratteri;
- CTA primarie:
  - `Hub Cerchi d’inchiostro`;
  - `Triadi` oppure guida precedente/successiva della stessa triade, secondo il modello già approvato.

Non inserire nel hero lunghi paragrafi, apertura editoriale lunga, newsletter o varianti strutturali.

L’apertura editoriale lunga appartiene al corpo guida e deve comparire dopo cover/indice, secondo il modello reale della guida più recente, senza creare un nuovo design.

## 4. Indice standard

Ogni guida deve avere:

```html
<nav class="guide-toc" aria-label="Indice della guida NOME AUTORE">
```

Il blocco deve avere il titolo visivo:

```text
Indice della guida
```

Regole operative:

- non inserire una riga duplicata “Indice” prima del titolo;
- le voci dell’indice devono essere coerenti con gli H2;
- ogni `href` deve avere un `id` corrispondente;
- i titoli corpo non devono essere numerati;
- le voci indice possono essere numerate solo come testo della pillola, se il modello corrente le usa.

## 5. Ordine finale standard

Ogni guida deve chiudere in questo ordine:

1. Fonti;
2. Prosegui la lettura;
3. Chiusura editoriale.

La Chiusura editoriale deve essere l’ultimo blocco narrativo della guida.

## 6. Prosegui la lettura standard

Il blocco “Prosegui la lettura” serve alla navigazione editoriale, non alla newsletter.

Deve contenere:

- link all’hub Cerchi;
- link alla pagina Triadi, quando pertinente;
- link agli altri autori della stessa triade;
- pochi link trasversali ad autori già pubblicati, solo se semanticamente utili.

Regole:

- ogni autore citato nel blocco deve essere linkato se la guida è pubblicata;
- non citare guide future non pubblicate;
- non trasformare il blocco in un archivio completo;
- non inserire CTA newsletter nel blocco Prosegui;
- non duplicare lo stesso link nello stesso blocco;
- non lasciare titoli autore come testo non cliccabile se la pagina esiste.

## 7. Regole newsletter

La CTA newsletter non deve apparire dentro il blocco Prosegui delle guide autore, salvo richiesta esplicita.

La newsletter può essere richiamata:

- nel footer;
- in pagine indice;
- in pagine contatti;
- in blocchi dedicati se approvati.

## 8. Regole asset

Per le nuove guide, usare il naming standard:

```text
cerchi-guida-NN-nome-autore-temi-principali-1600x900.webp
```

Regole:

- non rinominare asset già pubblicati per ragioni cosmetiche;
- non modificare immagini già referenziate da pagine live, `og:image`, Twitter image, JSON-LD o sitemap senza patch dedicata;
- per asset legacy, creare prima inventario;
- usare WebP 1600x900 per nuove cover;
- non introdurre JPG per nuove cover, salvo eccezione approvata.

## 9. Regole triadi e hub

Quando una triade viene completata, aggiornare sempre:

- `cerchi/triadi/index.html`;
- meta description della pagina triadi;
- JSON-LD CollectionPage;
- card visibile della nuova triade;
- link alle tre guide;
- eventuale testo “Da dove iniziare”.

Non lasciare una triade pubblicata assente dalla pagina Triadi.

Quando una nuova guida viene pubblicata, aggiornare sempre:

- `cerchi/index.html`;
- card guida;
- numero guida;
- titolo;
- descrizione;
- immagine;
- alt;
- CTA.

Non modificare homepage automaticamente. La homepage resta soggetta alla regola delle 9 guide visibili.

## 10. Checklist finale

Per ogni patch su guide Cerchi, verificare:

- [ ] H1 presente;
- [ ] canonical self-referencing;
- [ ] meta title;
- [ ] meta description;
- [ ] cover esistente;
- [ ] `og:image`;
- [ ] `twitter:image`;
- [ ] Article JSON-LD valido;
- [ ] BreadcrumbList valido;
- [ ] FAQPage valido se presente;
- [ ] indice presente;
- [ ] href indice/id coerenti;
- [ ] assenza placeholder;
- [ ] assenza link PDF non richiesti;
- [ ] Prosegui la lettura coerente;
- [ ] Chiusura editoriale ultima;
- [ ] sitemap aggiornata solo quando viene pubblicata nuova pagina;
- [ ] homepage non modificata salvo richiesta esplicita.

## 11. Scheda madre sintetica

Questa scheda è un promemoria interno, non una guida reale e non un contenuto pubblicabile.

```text
Guida: NN
Autore: NOME AUTORE
Triade: NOME TRIADE / gruppo editoriale
URL previsto: /cerchi/guide/slug-autore/
Cover: cerchi-guida-NN-nome-autore-temi-principali-1600x900.webp
Hero lead: una frase breve, massimo circa 90 caratteri
CTA hero: Hub Cerchi d’inchiostro + Triadi o guida correlata approvata
Sezioni H2: elenco dei titoli puliti, non numerati
Fonti: fonti essenziali e verificabili
Prosegui la lettura: hub, triadi, autori della stessa triade pubblicati, pochi trasversali
Chiusura editoriale: ultimo blocco narrativo, fluido e non schematico
JSON-LD: Article + BreadcrumbList; FAQPage solo se FAQ visibili
Controlli: checklist completa prima della pubblicazione
```
