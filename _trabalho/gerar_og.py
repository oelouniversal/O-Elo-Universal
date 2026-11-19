#!/usr/bin/env python3
"""
Gera as imagens de compartilhamento (Open Graph, 1200x630) do site.

  site/assets/img/og-vendas.jpg      -> página de vendas (/)
  site/assets/img/og-capitulo-1.jpg  -> página de captura (/capitulo-1)

WhatsApp, Instagram, Facebook e afins só mostram a prévia grande quando a imagem
é paisagem (1200x630), leve (bem abaixo de 300 KB) e referenciada por URL completa
nas meta tags. Este script cuida das duas primeiras partes; as meta tags ficam nos HTML.

Uso:  python _trabalho/gerar_og.py
Requer: Pillow e Google Chrome (ou Edge). Caminho do navegador pode vir em CHROME_PATH.
"""

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTES = RAIZ / "site" / "assets" / "fonts"
SVG = RAIZ / "site" / "assets" / "svg"
IMG = RAIZ / "site" / "assets" / "img"
CAPA = RAIZ / "_trabalho" / "Ativos-Graficos" / "Ativos-Graficos" / "capas" / "Capa-Carta_sem-texto.png"

LARGURA, ALTURA = 1200, 630

BASE = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Pagella; src: url('{fontes}/Pagella-Regular.woff'); }}
@font-face {{ font-family: Pagella; font-style: italic; src: url('{fontes}/Pagella-Italic.woff'); }}
@font-face {{ font-family: Lora; font-style: italic; src: url('{fontes}/Lora-Italic.woff'); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url('{fontes}/Inter-SemiBold.woff'); }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {w}px; height: {h}px; overflow: hidden; }}
body {{
  background: #0E0F13;
  background-image:
    radial-gradient(ellipse 55% 75% at 77% 50%, rgba(217,169,75,.20) 0%, rgba(217,169,75,.05) 45%, transparent 70%),
    radial-gradient(ellipse 90% 70% at 20% 0%, rgba(217,169,75,.07) 0%, transparent 60%);
  color: #EDE6DA; position: relative; font-family: Pagella, Georgia, serif;
}}
/* Sigilo de fundo (círculos concêntricos e heptagrama, como no hero do site) */
.sigilo {{ position: absolute; right: -40px; top: 50%; width: 700px; height: 700px; transform: translateY(-50%); opacity: .55; }}
.moldura {{ position: absolute; inset: 22px; border: 1px solid rgba(217,169,75,.22); }}
.texto {{ position: absolute; left: 84px; top: 0; bottom: 0; width: 600px; display: flex; flex-direction: column; justify-content: center; }}
.marca {{ display: flex; align-items: center; gap: 14px; margin-bottom: 30px; }}
.marca img {{ width: 46px; height: 46px; }}
.kicker {{ font-family: Inter, sans-serif; font-weight: 600; font-size: 17px; letter-spacing: .32em; text-transform: uppercase; color: #D9A94B; }}
h1 {{ font-weight: 400; font-size: {titulo_px}px; line-height: 1.06; color: #F4EFE6; letter-spacing: -.005em; }}
h1 em {{ font-style: italic; color: #E8C27A; }}
.sub {{ font-family: Inter, sans-serif; font-weight: 600; font-size: 19px; letter-spacing: .14em; text-transform: uppercase; color: #C3BDB0; margin-top: 26px; }}
.linha {{ width: 88px; height: 2px; background: linear-gradient(90deg, #D9A94B, rgba(217,169,75,0)); margin: 26px 0 22px; }}
.frase {{ font-family: Lora, Georgia, serif; font-style: italic; font-size: 25px; line-height: 1.4; color: #D8D1C4; max-width: 540px; }}
.visual {{ position: absolute; right: 92px; top: 50%; transform: translateY(-50%); }}
.livro {{
  width: {livro_w}px; display: block; border-radius: 4px 8px 8px 4px;
  border: 1px solid rgba(217,169,75,.55);
  box-shadow: 0 0 0 1px rgba(0,0,0,.6), 0 30px 60px rgba(0,0,0,.65), 0 0 70px rgba(217,169,75,.28);
}}
.lombada {{ position: absolute; left: 0; top: 0; bottom: 0; width: 14px; border-radius: 4px 0 0 4px;
  background: linear-gradient(90deg, rgba(0,0,0,.55), rgba(255,255,255,.06) 60%, transparent); }}
.selo {{ position: absolute; right: -24px; top: -18px; font-family: Inter, sans-serif; font-weight: 600; font-size: 15px;
  letter-spacing: .2em; text-transform: uppercase; color: #121316; background: #D9A94B; padding: 10px 18px; border-radius: 999px;
  box-shadow: 0 8px 24px rgba(0,0,0,.5); }}
</style></head><body>
<svg class="sigilo" viewBox="0 0 800 800" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="400" r="380" stroke="#8E6620" stroke-width="1.2" stroke-dasharray="3 7" opacity=".6"/>
  <circle cx="400" cy="400" r="350" stroke="#D9A94B" stroke-width="1.2" opacity=".5"/>
  <circle cx="400" cy="400" r="280" stroke="#D9A94B" stroke-width="1" stroke-dasharray="2 5" opacity=".5"/>
  <circle cx="400" cy="400" r="210" stroke="#8E6620" stroke-width="1" opacity=".5"/>
  <polygon points="400,190 588,280 610,488 450,600 350,600 190,488 212,280" stroke="#D9A94B" stroke-width="1" stroke-dasharray="4 4" opacity=".35"/>
</svg>
<div class="moldura"></div>
<div class="texto">
  <div class="marca"><img src="{marca}" alt=""><span class="kicker">{kicker}</span></div>
  <h1>{titulo}</h1>
  <p class="sub">{sub}</p>
  <div class="linha"></div>
  <p class="frase">{frase}</p>
</div>
<div class="visual">
  <div style="position:relative">
    <img class="livro" src="{imagem}" alt="">
    {lombada}
    {selo}
  </div>
</div>
</body></html>"""

IMAGENS = [
    {
        "saida": "og-vendas.jpg",
        "kicker": "O Elo Universal",
        "titulo": "Caderno das<br><em>Leis Herméticas</em>",
        "titulo_px": 74,
        "sub": "Sete leis · Sete pistas · Sete experimentos",
        "frase": "Você não precisa acreditar em nada:<br>precisa observar.",
        "imagem": CAPA,
        "livro_w": 330,
        "lombada": True,
        "selo": "",
    },
    {
        "saida": "og-capitulo-1.jpg",
        "kicker": "Capítulo 1 · grátis",
        "titulo": "Leia o Capítulo 1<br><em>antes de decidir</em>",
        "titulo_px": 66,
        "sub": "A Lei do Mentalismo, completa",
        "frase": "A pista do gorila invisível e um experimento de um dia. Em PDF, na hora.",
        "imagem": IMG / "amostra_p4.webp",
        "livro_w": 340,
        "lombada": False,
        "selo": '<span class="selo">Grátis</span>',
    },
]


def achar_navegador():
    for c in (os.environ.get("CHROME_PATH"),
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              shutil.which("google-chrome"), shutil.which("chromium")):
        if c and os.path.exists(c):
            return c
    sys.exit("Navegador não encontrado. Defina CHROME_PATH com o caminho do Chrome ou Edge.")


def gerar(cfg, navegador):
    html = BASE.format(
        fontes=FONTES.as_uri(), marca=(SVG / "marca-elo_claro.svg").as_uri(),
        w=LARGURA, h=ALTURA, kicker=cfg["kicker"], titulo=cfg["titulo"], titulo_px=cfg["titulo_px"],
        sub=cfg["sub"], frase=cfg["frase"], imagem=pathlib.Path(cfg["imagem"]).as_uri(), livro_w=cfg["livro_w"],
        lombada='<span class="lombada"></span>' if cfg["lombada"] else "", selo=cfg["selo"],
    )
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        pagina = tmp / "og.html"
        pagina.write_text(html, encoding="utf-8")
        png = tmp / "og.png"
        # A janela headless no Windows tem largura mínima; captura maior e recorta 1200x630.
        subprocess.run(
            [navegador, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
             f"--user-data-dir={tmp / 'perfil'}", "--virtual-time-budget=5000",
             f"--window-size={LARGURA},{ALTURA + 200}", f"--screenshot={png}", pagina.as_uri()],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
        )
        imagem = Image.open(png).convert("RGB").crop((0, 0, LARGURA, ALTURA))
        destino = IMG / cfg["saida"]
        imagem.save(destino, "JPEG", quality=86, optimize=True, progressive=True)
    kb = destino.stat().st_size / 1024
    aviso = "" if kb < 300 else "  ATENÇÃO: acima de 300 KB, o WhatsApp pode mostrar só miniatura"
    print(f"{destino.relative_to(RAIZ)} · {imagem.size[0]}x{imagem.size[1]} · {kb:.0f} KB{aviso}")


if __name__ == "__main__":
    nav = achar_navegador()
    for c in IMAGENS:
        gerar(c, nav)
