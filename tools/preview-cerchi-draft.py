#!/usr/bin/env python3
"""Serve a staged Cerchi draft over the current repository, on loopback only."""
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def handler(candidate):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)

        def translate_path(self, path):
            relative = unquote(urlsplit(path).path).lstrip('/')
            if any(part in {'.', '..'} or part.startswith('.') for part in Path(relative).parts):
                return str(ROOT / '__not_served__')
            staged = (candidate / relative).resolve()
            if staged.is_relative_to(candidate) and staged.exists():
                return str(staged)
            return super().translate_path(path)

        def end_headers(self):
            self.send_header('X-Robots-Tag', 'noindex, nofollow')
            self.send_header('Cache-Control', 'no-store')
            # A second origin with ?nojs is unnecessary: CSP blocks scripts on
            # the requested HTML while static document links retain their URLs.
            if 'nojs' in urlsplit(self.path).query.split('&'):
                self.send_header('Content-Security-Policy', "script-src 'none'; object-src 'none'")
            super().end_headers()
    return Handler


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True, help='staged site root containing cerchi/ or en/')
    parser.add_argument('--port', type=int, default=8767)
    args = parser.parse_args()
    candidate = args.candidate.resolve()
    if not candidate.is_dir():
        parser.error('candidate must be an existing staged site directory')
    print(f'Local DRAFT preview: http://127.0.0.1:{args.port}/ (overlay: {candidate})', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), handler(candidate)).serve_forever()
