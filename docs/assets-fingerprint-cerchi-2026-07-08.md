# PATCH 4B — Verifica tecnica asset e fingerprint Git

Data: 2026-07-08

Repository: `alessandrgentili-source/alessandro-gentili-site`

Base di lavoro: `main` dopo merge della PATCH 4A, commit `7f298de422d0941a59f8e4deb54cc1becdbb554e`.

## Scopo

Questa patch rafforza l'audit asset avviato con la PATCH 4A, aggiungendo una verifica tecnica di esistenza e fingerprint Git per gli asset già censiti come pubblicati o referenziati.

La patch resta intenzionalmente conservativa: non cancella, non rinomina, non sposta, non converte e non ottimizza nessuna immagine.

## Metodo eseguito

1. Sono stati presi come perimetro operativo i 36 asset elencati nell'inventario 4A.
2. Per ogni asset è stata verificata l'esistenza su `main` tramite lettura del file dal repository.
3. Per ogni asset è stato registrato il `git_blob_sha`, utile come fingerprint Git del contenuto.
4. I fingerprint sono stati confrontati tra loro per individuare duplicati binari esatti nel perimetro verificato.
5. Nessuna pagina pubblica, nessun asset e nessun file SEO/GEO è stato modificato.

## Risultati

| Voce | Esito |
|---|---:|
| Asset verificati | 36 |
| Asset trovati su `main` | 36 |
| Asset mancanti nel perimetro verificato | 0 |
| Fingerprint Git raccolti | 36 |
| Fingerprint Git distinti | 36 |
| Duplicati binari esatti nel perimetro verificato | 0 |
| JPG legacy verificati | 4 |
| WEBP verificati | 32 |
| Asset Cerchi verificati | 16 |
| Asset saggi verificati | 16 |
| Asset autore verificati | 2 |
| Asset temi verificati | 2 |

## Lettura operativa

Il dato più importante è che i 36 asset già mappati come usati nella PATCH 4A risultano presenti su `main` e hanno fingerprint Git distinti. Questo riduce il rischio di confondere asset pubblicati con copie duplicate, ma non autorizza ancora nessuna pulizia automatica.

Il fatto che non emergano duplicati binari esatti nel perimetro verificato significa solo che, tra questi 36 asset pubblicati o referenziati, non ci sono due file con lo stesso contenuto Git. Non significa che nella repository non esistano altri asset non referenziati fuori da questo perimetro.

## Limite reale della PATCH 4B

Questa verifica non è una scansione ricorsiva totale della repository. Il connettore disponibile consente la lettura di file noti, ma non ha fornito una directory listing ricorsiva completa di `assets/img` con peso, dimensioni reali e hash SHA-256 calcolato sui binari.

Di conseguenza:

- non è possibile dichiarare che la repository non contenga asset orfani in assoluto;
- non è possibile autorizzare cancellazioni o archiviazioni;
- non è possibile confermare peso reale e dimensioni effettive di ogni immagine;
- è possibile invece confermare che gli asset pubblicati già censiti esistono e sono tracciabili tramite `git_blob_sha`.

## Rischi confermati

Restano protetti e da non modificare per ragioni cosmetiche:

- le 4 immagini JPG legacy di Cerchi;
- le cover Cerchi già pubblicate con naming non perfettamente uniforme;
- le cover saggi con naming storico misto;
- le immagini autore usate anche in dati strutturati;
- le immagini dei percorsi tematici.

Il rischio principale rimane la rottura di riferimenti in `img src`, `og:image`, `twitter:image`, JSON-LD, cache social e link già condivisi.

## Raccomandazione

Non fare pulizia asset ora.

La prossima patch utile, se si lavora da clone locale completo, dovrebbe produrre solo un report tecnico con:

- lista ricorsiva completa di `assets/img`;
- peso reale di ogni file;
- dimensioni effettive lette dal binario;
- SHA-256 calcolato localmente;
- confronto contro tutti i riferimenti testuali della repository;
- elenco separato di candidati orfani, senza cancellarli.

## Inventario fingerprint

| Percorso | Estensione | Git blob SHA | Dimensione dedotta | Classe | Stato |
|---|---:|---|---|---|---|
| `assets/img/cerchi/cerchi-inchiostro-cover-madre-1600x900.jpg` | jpg | `0d97d29d1f8452303cdfa0bfcc70ca1aac0923e2` | 1600x900 da nome/HTML | Cerchi / cover madre | verificato/protetto |
| `assets/img/cerchi/cerchi-platone-idee-verita-potere-1600x900.jpg` | jpg | `d1ad81c99f0135195a346698428944958a51e22c` | 1600x900 da nome/HTML | Cerchi / cover guida 01 legacy | verificato/protetto |
| `assets/img/cerchi/cerchi-dante-esilio-lingua-visione-mondo-1600x900.jpg` | jpg | `5d5176bd355ee0d5844dec05154d140ca0fa28be` | 1600x900 da nome/HTML | Cerchi / cover guida 02 legacy | verificato/protetto |
| `assets/img/cerchi/cerchi-machiavelli-potere-stato-verita-effettuale-1600x900.jpg` | jpg | `c6d574795b9bc54d63af6938bde6029cc8291141` | 1600x900 da nome/HTML | Cerchi / cover guida 03 legacy | verificato/protetto |
| `assets/img/cerchi/cerchi-marx-capitale-lavoro-alienazione-1600x900.webp` | webp | `720863b0d4fc40cb8d019168008e3fabe3003950` | 1600x900 da nome/HTML | Cerchi / cover guida 04 | verificato/protetto |
| `assets/img/cerchi/cerchi-nietzsche-nichilismo-valori-morte-dio-1600x900.webp` | webp | `56e0dfa72f33193bba0e33c5652efeed5f88641f` | 1600x900 da nome/HTML | Cerchi / cover guida 05 | verificato/protetto |
| `assets/img/cerchi/cerchi-guida-06-giacomo-leopardi-desiderio-infinito-modernita.webp` | webp | `c11edb1def7b37819acbc8d530e58c2e1c1c1fdc` | 1600x900 da HTML | Cerchi / cover guida 06 | verificato/protetto |
| `assets/img/cerchi/cerchi-guida-07-seneca-dominio-tempo-morte-1600x900.webp` | webp | `f3ca13f76bb88e318016568d3b0a8d453cc059af` | 1600x900 da nome/HTML | Cerchi / cover guida 07 | verificato/protetto |
| `assets/img/cerchi/cerchi-guida-08-aristotele-forma-fine-realta-1600x900.webp` | webp | `2c1309148e920d948dd01e04b3ce7c072cb7c63c` | 1600x900 da nome/HTML | Cerchi / cover guida 08 | verificato/protetto |
| `assets/img/cerchi/cerchi-guida-09-max-weber-razionalizzazione-potere-disincanto-1600x900.webp` | webp | `0dcb766ac958d1bc0019c2cfce633fe033d44ee8` | 1600x900 da nome/HTML | Cerchi / cover guida 09 | verificato/protetto |
| `assets/img/cerchi/cerchi-guida-10-sigmund-freud-inconscio-desiderio-civilta-1600x900.webp` | webp | `f124631dfff177ab9b5298f434c28e5d3fbb1be7` | 1600x900 da nome/HTML | Cerchi / cover guida 10 | verificato/protetto |
| `assets/img/cerchi/cerchi-guida-11-antonio-gramsci-egemonia-cultura-senso-comune-1600x900.webp` | webp | `915e2035adb7e2b41c514709997b0a9fac6631a4` | 1600x900 da nome/HTML | Cerchi / cover guida 11 | verificato/protetto |
| `assets/img/cerchi/cerchi-guida-12-thomas-hobbes-paura-sovranita-ordine-politico-1600x900.webp` | webp | `33926ffceb0ada16ffd4afa610a8e45d2c65065a` | 1600x900 da nome/HTML | Cerchi / cover guida 12 | verificato/protetto |
| `assets/img/cerchi/cerchi-guida-13-averroe-ragione-interpretazione-legge-1600x900.webp` | webp | `1ee3449e6980729b18986243720e1e38a9f14c50` | 1600x900 da nome/HTML | Cerchi / cover guida 13 | verificato/protetto |
| `assets/img/cerchi/cerchi-guida-14-georg-simmel-denaro-metropoli-individualita-1600x900.webp` | webp | `feb52947606a22cbeb62526a765477924af39ccd` | 1600x900 da nome/HTML | Cerchi / cover guida 14 | verificato/protetto |
| `assets/img/cerchi/cerchi-guida-15-adam-smith-scambio-simpatia-ricchezza-1600x900.webp` | webp | `c77b4779d03349614e1acff22edc00f821187637` | 1600x900 da nome/HTML | Cerchi / cover guida 15 | verificato/protetto |
| `assets/img/saggi/site/saggio-0-cosmo-algoritmo_16x9_v01.webp` | webp | `a776b49c1ecefa8563114fe5fe6326b8eb606586` | 1600x900 da HTML | Saggi / cover saggio 0 e preview trasversale | verificato/protetto |
| `assets/img/saggi/site/saggio-1-1999-paura-diventare-uguali-cover.webp` | webp | `bdafee78d0db81889030e1904b3f72331ba69b56` | 1600x900 da HTML | Saggi / cover saggio 1 | verificato/protetto |
| `assets/img/saggi/site/saggio-2-il-primo-cerchio-cover.webp` | webp | `27afac1e246c6fd120ef6037f779f520f7c0cb37` | 1600x900 da HTML | Saggi / cover saggio 2 | verificato/protetto |
| `assets/img/saggi/site/saggio-3-governi-senza-firma.webp` | webp | `52fc7374f3fdb9f42e679396bc534f889a7d68d5` | 1600x900 da HTML | Saggi / cover saggio 3 | verificato/protetto |
| `assets/img/saggi/site/saggio-04-metafisica-del-sesso.webp` | webp | `8f9dffaad5472bb96f4e5199e29636479833981d` | 1600x900 da HTML | Saggi / cover saggio 4 | verificato/protetto |
| `assets/img/saggi/site/saggio-5-il-reale-in-modalita-scorrimento.webp` | webp | `1898f56874dae00b4b5146dcddc52c30fc4ee9c2` | 1600x900 da HTML | Saggi / cover saggio 5 | verificato/protetto |
| `assets/img/saggi/site/saggio-6-fenomenologia-del-potere_site_1672x941.webp` | webp | `25426ec6ee033e3e46241537dc7fc74310309616` | 1672x941 da nome/HTML | Saggi / cover saggio 6 | verificato/protetto |
| `assets/img/saggi/site/saggio-7-il-cerchio-e-aperto.webp` | webp | `3682605c403229ac815a80a39e59b3436af8dd13` | 1600x900 da HTML | Saggi / cover saggio 7 | verificato/protetto |
| `assets/img/saggi/site/saggio-08-il-costo-della-complessita_site_1600x900.webp` | webp | `5646b781f5a3e9413f3115e6126ceae739d67aec` | 1600x900 da nome/HTML | Saggi / cover saggio 8 | verificato/protetto |
| `assets/img/saggi/site/saggio-09-la-promessa-del-ritorno_site_1600x900.webp` | webp | `9bdb31255946e2d54989047e2e0aa84348bf2d4f` | 1600x900 da nome/HTML | Saggi / cover saggio 9 | verificato/protetto |
| `assets/img/saggi/site/saggio-10-giovani-senilita-potere_site_1600x900.webp` | webp | `494b0adb15d9da96f4d7c115f27ae1cc5f31a691` | 1600x900 da nome/HTML | Saggi / cover saggio 10 | verificato/protetto |
| `assets/img/saggi/site/saggio-11-chi-decide-il-sole_site_1600x900.webp` | webp | `ac2c4c558c5dcdd2bb7131787afb85a438c35c83` | 1600x900 da nome/HTML | Saggi / cover saggio 11 | verificato/protetto |
| `assets/img/saggi/site/saggio-12-le-periferie-del-potere.webp` | webp | `e76b64f6fffea675dc9bf9ae9e2b32b37be7cdd0` | 1600x900 da HTML | Saggi / cover saggio 12 | verificato/protetto |
| `assets/img/saggi/site/saggio-12-supporto-cartolina-libro-territorio.webp` | webp | `c69d7d91381acecb54bc7b26fd16632f59a2f794` | non rilevabile da HTML | Saggi / immagine interna saggio 12 | verificato/protetto |
| `assets/img/saggi/site/saggio-13-la-periferia-intelligente-cover-final-1600x900.webp` | webp | `1c64f4bebd85c431acfa6c80a6551f9866dff6cb` | 1600x900 da nome/HTML | Saggi / cover saggio 13 | verificato/protetto |
| `assets/img/saggi/site/saggio-14-metafisica-dell-amore_site_1600x900.webp` | webp | `d48c0e82020699f55bc7baa97a2dbae06205552e` | 1600x900 da nome/HTML | Saggi / cover saggio 14 | verificato/protetto |
| `assets/img/autore/alessandro-gentili-ritratto-autore-strategist-800x1000.webp` | webp | `ace9cdd4bd1a2b6197c162edb915148ee2d9a47e` | 800x1000 da nome/HTML | Autore / ritratto profilo | verificato/protetto |
| `assets/img/autore/alessandro-gentili-strategy-writing-ai-systems-1600x900.webp` | webp | `e93291d001a90012e2d07a47c597151b014f9b7c` | 1600x900 da nome/HTML | Autore / international | verificato/protetto |
| `assets/img/temi/temi-potere-apparati-1600x900.webp` | webp | `527b81ad46f4660bff6fb599b25f54dba83c72cd` | 1600x900 da nome/HTML | Temi / potere e apparati | verificato/protetto |
| `assets/img/temi/temi-periferie-territorio-comunita-1600x900.webp` | webp | `da808f7e73b5597ee1690006e5b80f37e4796227` | 1600x900 da nome/HTML | Temi / periferie territorio comunità | verificato/protetto |
