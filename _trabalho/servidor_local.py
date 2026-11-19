#!/usr/bin/env python3
"""
Servidor local que imita a Vercel com "cleanUrls": true (vercel.json).

- /pagina        -> serve site/pagina.html
- /pagina.html   -> 404, como em produção (a Vercel só serve o endereço limpo;
                    os redirecionamentos de vercel.json existem só lá)
- demais arquivos (css, js, imagens, pdf) -> servidos normalmente

Uso:  python _trabalho/servidor_local.py [porta]
Abre em http://127.0.0.1:8765 (só no próprio computador).
"""

import http.server
import os
import pathlib
import sys
import urllib.parse

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def _resolver(self):
        caminho = urllib.parse.urlsplit(self.path).path
        if caminho.endswith(".html"):
            return None  # 404, igual à Vercel
        if caminho != "/" and not os.path.splitext(caminho)[1]:
            alvo = SITE / (urllib.parse.unquote(caminho).lstrip("/") + ".html")
            if alvo.is_file():
                consulta = urllib.parse.urlsplit(self.path).query
                self.path = caminho + ".html" + (("?" + consulta) if consulta else "")
        return True

    def do_GET(self):
        if self._resolver() is None:
            self.send_error(404, "Na Vercel, use o endereço sem .html")
            return
        super().do_GET()

    def do_HEAD(self):
        if self._resolver() is None:
            self.send_error(404)
            return
        super().do_HEAD()


if __name__ == "__main__":
    porta = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"Servindo {SITE} em http://127.0.0.1:{porta} (imitando cleanUrls da Vercel)")
    http.server.ThreadingHTTPServer(("127.0.0.1", porta), Handler).serve_forever()
