#!/usr/bin/env python3
"""Local-only review server: prototype, exact main baseline, and no-JS views.

Run from any directory: python3 tools/preview-international.py
No generated review page enters the site's sitemap or deployed source tree.
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import mimetypes
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASELINE = 'e9df7f0f853e35c0cd70f60b3b4b5011efe1cae4'
HUB = '/en/cerchi/'
GUIDE = '/en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/'
IMAGES = {'before-hub.png', 'after-hub.png', 'before-reading.png', 'after-reading.png',
          'after-interaction.png', 'mobile-guide.png', 'mobile-hub.png'}


def review_page():
    return f'''<!doctype html><html lang="it"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>International 3.0 — confronto locale</title>
<style>
body{{margin:0;padding:40px;background:#f8f2e7;color:#182e3e;font:17px/1.6 system-ui}}
main{{max-width:1200px;margin:auto}}h1,h2{{font-family:Georgia,serif;font-weight:normal}}
h1{{font-size:clamp(32px,5vw,54px);line-height:1.1}}a{{color:inherit;text-underline-offset:4px}}
nav{{display:flex;gap:20px;flex-wrap:wrap;margin:30px 0}}nav a{{padding:12px 18px;border:1px solid #806333}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}figure{{margin:0}}img{{width:100%;height:auto;border:1px solid #cfc2aa}}
figcaption{{padding:8px 0;font-size:14px}}section{{margin:50px 0}}li{{margin:12px 0}}
@media(max-width:700px){{body{{padding:24px}}.pair{{grid-template-columns:1fr}}}}
</style><main><p>PROTOTIPO LOCALE · BRANCH design/international-3-atlas</p>
<h1>Cerchi d’inchiostro<br>International 3.0</h1>
<p>Due pagine da esplorare: l’hub e Pasolini. Nessun merge o deploy. Le altre destinazioni conservano l’esperienza attuale.</p>
<nav><a href="{HUB}">Apri il nuovo hub →</a><a href="{GUIDE}">Leggi Pasolini →</a></nav>
<ol><li>Nell’hub: scegli una domanda, oppure cerca “education”, “power” o un autore nell’indice.</li>
<li>In Pasolini: segui l’indice, esplora “An environment that teaches”, passa dalla televisione alle piattaforme e torna ai paragrafi attraverso i collegamenti.</li>
<li>Confronta con <a href="/__before{HUB}">l’hub originale</a> e <a href="/__before{GUIDE}#things">la lettura originale</a>, serviti dal commit {BASELINE[:7]}.</li>
<li>Verifica la <a href="/__nojs{GUIDE}#television">guida senza JavaScript</a> e <a href="/__nojs{HUB}#directory">l’indice senza JavaScript</a>.</li></ol>
<section><h2>L’ingresso nell’atlante</h2><div class="pair">
<figure><a href="/__before{HUB}"><img src="/__review/before-hub.png" alt="Hub originale: presentazione e schede seriali"></a><figcaption>Prima · main</figcaption></figure>
<figure><a href="{HUB}"><img src="/__review/after-hub.png" alt="Nuovo hub: apertura editoriale e tre accessi"></a><figcaption>Dopo · prototipo</figcaption></figure></div></section>
<section><h2>Gli stessi paragrafi, una diversa lettura</h2><div class="pair">
<figure><img src="/__review/before-reading.png" alt="Lettura originale a piena larghezza in pannelli"><figcaption>Prima · pannelli a piena larghezza</figcaption></figure>
<figure><img src="/__review/after-reading.png" alt="Colonna serif con indice laterale"><figcaption>Dopo · colonna di lettura e indice contestuale</figcaption></figure></div></section>
<section><h2>Esplorare una distinzione</h2><a href="{GUIDE}#formation-title"><img style="max-width:100%" src="/__review/after-interaction.png" alt="Confronto esplorabile fra il contesto televisivo e le piattaforme contemporanee"></a></section>
</main></html>'''.encode()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header('X-Robots-Tag', 'noindex, nofollow')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def send_data(self, data, content_type, nojs=False):
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        if nojs:
            self.send_header('Content-Security-Policy', "script-src 'none'; object-src 'none'")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path in ('/__review', '/__review/'):
            return self.send_data(review_page(), 'text/html; charset=utf-8')
        if path.startswith('/__review/'):
            name = path.rsplit('/', 1)[-1]
            asset = ROOT / 'docs' / 'international-3' / 'evidence' / name
            if name in IMAGES and asset.is_file():
                return self.send_data(asset.read_bytes(), 'image/png')
            return self.send_error(404)
        prefix = next((p for p in ('/__before', '/__nojs') if path.startswith(p + '/')), '')
        relative = path[len(prefix):].lstrip('/')
        if not relative or relative.endswith('/'):
            relative += 'index.html'
        if any(part.startswith('.') for part in Path(relative).parts):
            return self.send_error(403)
        candidate = (ROOT / relative).resolve()
        if not candidate.is_relative_to(ROOT):
            return self.send_error(403)
        if candidate.suffix not in ('.html', '.css', '.js', '.webp', '.jpg', '.jpeg', '.png', '.svg', '.ico', '.pdf'):
            return self.send_error(404)
        try:
            if prefix == '/__before':
                data = subprocess.check_output(['git', 'show', f'{BASELINE}:{relative}'], cwd=ROOT, stderr=subprocess.DEVNULL)
            else:
                data = candidate.read_bytes()
        except (OSError, subprocess.CalledProcessError):
            return self.send_error(404)
        if prefix and relative.endswith('.html'):
            # Keep internal navigation and assets in the chosen review mode.
            data = re.sub(rb'((?:href|src)=")/(?!/)', lambda m: m[1] + prefix.encode() + b'/', data)
        content_type = mimetypes.guess_type(relative)[0] or 'application/octet-stream'
        if relative.endswith(('.html', '.css', '.js')):
            content_type += '; charset=utf-8'
        self.send_data(data, content_type, prefix == '/__nojs')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8766)
    args = parser.parse_args()
    print(f'Review: http://127.0.0.1:{args.port}/__review/', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
