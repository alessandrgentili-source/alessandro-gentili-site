# Lente Editoriale Worker v0.2

Backend serverless Cloudflare Worker per il prototipo interno `prototipi/lente-editoriale.html`.

Il Worker espone solo `POST /analyze`, chiama OpenAI lato server e restituisce un JSON normalizzato al frontend. Non usa database, KV, Durable Objects, storage persistente, analytics o logging del contenuto inviato.

## File modificati o creati

- `prototipi/lente-editoriale.html` — aggiorna il prototipo alla v0.2 con chiamata al Worker, stato loading, gestione errori e fallback demo.
- `worker/lente-editoriale/wrangler.toml` — configurazione minima Cloudflare Wrangler.
- `worker/lente-editoriale/src/index.js` — endpoint `POST /analyze`, CORS, validazione payload, prompt server-side, chiamata OpenAI e normalizzazione output.
- `worker/lente-editoriale/README.md` — istruzioni operative e checklist.

## Installare Wrangler

Da questa cartella:

```bash
npm create cloudflare@latest -- --help
npm install --save-dev wrangler
npx wrangler --version
```

In alternativa, se preferisci installazione globale:

```bash
npm install -g wrangler
wrangler --version
```

## Configurare `OPENAI_API_KEY`

Non inserire la chiave nel frontend, in `wrangler.toml` o in repository.

Imposta il secret Cloudflare:

```bash
cd worker/lente-editoriale
npx wrangler secret put OPENAI_API_KEY
```

Poi incolla la chiave quando richiesto da Wrangler.

Per test locale puoi usare un file `.dev.vars` non committato:

```bash
cd worker/lente-editoriale
printf 'OPENAI_API_KEY=<la-tua-chiave-openai>\nALLOW_LOCALHOST=true\n' > .dev.vars
```

Assicurati che `.dev.vars` non venga committato.

## Configurare `OPENAI_MODEL`

Il modello è letto da variabile ambiente `OPENAI_MODEL`. In `wrangler.toml` è presente un fallback prudente:

```toml
[vars]
OPENAI_MODEL = "gpt-4.1-mini"
ALLOW_LOCALHOST = "false"
```

Per cambiare modello, aggiorna `OPENAI_MODEL` in `wrangler.toml` o usa variabili d'ambiente Cloudflare. Scegli un modello che supporti Structured Outputs / JSON schema.

## Test locale

1. Avvia il Worker con localhost abilitato:

```bash
cd worker/lente-editoriale
ALLOW_LOCALHOST=true npx wrangler dev
```

2. Testa una richiesta valida da terminale usando un `Origin` ammesso per sviluppo:

```bash
curl -i 'http://localhost:8787/analyze' \
  -H 'Origin: http://localhost:8080' \
  -H 'Content-Type: application/json' \
  --data '{"text":"Testo di almeno 600 caratteri...","text_type":"essay","audience":"general","goal":"clarify","severity":"standard"}'
```

3. Testa errori attesi:

```bash
curl -i 'http://localhost:8787/analyze' -H 'Origin: http://localhost:8080'
curl -i 'http://localhost:8787/analyze' -H 'Origin: http://localhost:8080' -H 'Content-Type: text/plain' --data 'x'
```

4. Per provare la pagina statica in locale, modifica temporaneamente solo nel tuo ambiente il valore di endpoint o usa un override di sviluppo prima dello script. Non committare endpoint temporanei o chiavi.

## Deploy

```bash
cd worker/lente-editoriale
npx wrangler deploy
```

Dopo il deploy:

- configura `OPENAI_API_KEY` come secret nell'ambiente di produzione;
- lascia `ALLOW_LOCALHOST=false` in produzione;
- verifica che CORS consenta solo `https://alessandro-gentili.it`;
- aggiorna l'endpoint pubblico nel prototipo solo se il nome Worker o il route Cloudflare sono diversi da quelli previsti.

## Test manuali consigliati

- `GET /analyze` deve restituire `405 METHOD_NOT_ALLOWED`.
- `POST /analyze` senza `Content-Type: application/json` deve restituire `400 INVALID_CONTENT_TYPE`.
- `POST /analyze` da origin diverso da `https://alessandro-gentili.it` deve restituire `403 ORIGIN_NOT_ALLOWED`.
- Testo sotto 600 caratteri deve restituire `400 TEXT_TOO_SHORT`.
- Testo sopra 12.000 caratteri deve restituire `413 TEXT_TOO_LONG`.
- Con secret e modello configurati, una richiesta valida deve restituire `ok: true` e `report.meta.version = "0.2"`.
- Se OpenAI restituisce JSON non valido o inutilizzabile, il Worker deve rispondere con errore strutturato `MODEL_JSON_INVALID` senza rompere il frontend.
- Se il backend non risponde, la pagina deve mostrare errore e pulsante per generare il referto demo.

## Nota di pubblicazione

Non pubblicare, linkare o inserire questa pagina in home, menu, sitemap o robots. La pagina deve restare `noindex,nofollow` e prototipo interno.
