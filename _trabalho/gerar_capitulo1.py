#!/usr/bin/env python3
"""
Gera o PDF de amostra do Capítulo 1 (versões celular e impressão) a partir do caderno completo.

Estrutura da amostra:
  capa · como usar · sumário · Capítulo 1 completo (até a "Porta") · página "o caderno continua" · contracapa

Links internos:
  - links que apontam para páginas incluídas são mantidos;
  - links para capítulos que não estão na amostra (sumário, Porta para o Capítulo 2)
    passam a apontar para a página "o caderno continua".

Saída: site/downloads/ (publicado junto com o site; ver exceção no .vercelignore).

Uso:  python _trabalho/gerar_capitulo1.py
Requer: pypdf e Google Chrome (ou Edge) instalado. Caminho do navegador pode vir em CHROME_PATH.
"""

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import ArrayObject, IndirectObject, NameObject

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PRODUTO = RAIZ / "Produto"
FONTES = RAIZ / "site" / "assets" / "fonts"
MARCA = RAIZ / "site" / "assets" / "svg" / "marca-elo_claro.svg"
SAIDA = RAIZ / "site" / "downloads"

CHECKOUT = (
    "https://checkout.wiven.com.br/checkout/cmwgi7hp1004901pwfzy4sq1q?offer=3V9KZ68"
    "&utm_source=capitulo1-pdf&utm_medium=pdf&utm_campaign=capitulo1"
)

VERSOES = [
    {
        "nome": "celular",
        "origem": "Caderno-das-Leis-Hermeticas_Mobile.pdf",
        "paginas": list(range(0, 10)),  # p1–p10: capa, como usar, sumário, Capítulo 1
        "contracapa": -1,               # última página (era p61 até 26/11/2026)
        "fonte_base_pt": 9.6,
        "saida": "capitulo-1-o-elo-universal.pdf",
    },
    {
        "nome": "impressao",
        "origem": "Caderno-das-Leis-Hermeticas.pdf",
        "paginas": list(range(0, 8)),   # p1–p8
        "contracapa": -1,               # última página (era p41 até 26/11/2026)
        "fonte_base_pt": 15.5,
        "saida": "capitulo-1-o-elo-universal-impressao.pdf",
    },
]

PAGINA_CONTINUA = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<style>
  @font-face {{ font-family: Pagella; src: url('{fontes}/Pagella-Regular.woff'); }}
  @font-face {{ font-family: Pagella; font-style: italic; src: url('{fontes}/Pagella-Italic.woff'); }}
  @font-face {{ font-family: Lora; src: url('{fontes}/Lora-Regular.woff'); }}
  @font-face {{ font-family: Inter; font-weight: 600; src: url('{fontes}/Inter-SemiBold.woff'); }}
  @page {{ size: {w}pt {h}pt; margin: 0; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    width: {w}pt; height: {h}pt; overflow: hidden;
    background: #1B1D21; color: #EDE6DA;
    font-family: Lora, Georgia, serif; font-size: {base}pt;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
    display: flex; align-items: center; justify-content: center;
  }}
  .pagina {{ width: 78%; text-align: center; }}
  .marca {{ width: 3.4em; height: auto; margin-bottom: 1.6em; }}
  .kicker {{
    font-family: Inter, sans-serif; font-weight: 600; font-size: 0.62em;
    letter-spacing: 0.32em; text-transform: uppercase; color: #D9A94B; margin: 0 0 1.4em;
  }}
  h1 {{
    font-family: Pagella, Georgia, serif; font-style: italic; font-weight: 400;
    font-size: 1.95em; line-height: 1.22; margin: 0 0 0.9em; color: #F4EFE6;
  }}
  .lead {{ font-size: 0.95em; line-height: 1.6; color: #C3BDB0; margin: 0 0 1.6em; }}
  .itens {{
    list-style: none; padding: 1.1em 0; margin: 0 0 1.6em;
    border-top: 1px solid rgba(217,169,75,.35); border-bottom: 1px solid rgba(217,169,75,.35);
    font-size: 0.9em; line-height: 1.9; color: #EDE6DA;
  }}
  .preco {{ font-family: Pagella, Georgia, serif; font-size: 2.1em; color: #D9A94B; margin: 0; }}
  .preco-tipo {{
    font-family: Inter, sans-serif; font-weight: 600; font-size: 0.6em; letter-spacing: 0.28em;
    text-transform: uppercase; color: #C3BDB0; margin: 0.5em 0 1.5em;
  }}
  .botao {{
    display: inline-block; font-family: Inter, sans-serif; font-weight: 600; font-size: 0.78em;
    letter-spacing: 0.18em; text-transform: uppercase; text-decoration: none;
    color: #1B1D21; background: #D9A94B; border-radius: 999px; padding: 1em 2.2em;
  }}
  .nota {{ font-size: 0.72em; color: #8F8A80; margin-top: 1.4em; }}
</style></head>
<body><div class="pagina">
  <img class="marca" src="{marca}" alt="">
  <p class="kicker">O caderno continua</p>
  <h1>A porta para o Capítulo 2 está no caderno completo.</h1>
  <p class="lead">Você leu a primeira lei. Faltam seis, no mesmo formato: o que a tradição afirma,
  a pista da ciência com o seu limite, um experimento de 1 a 7 dias e o registro.</p>
  <ul class="itens">
    <li>7 leis · 7 pistas · 7 experimentos</li>
    <li>Bônus A · Mapa das 7 Leis</li>
    <li>Bônus B · Fontes e Limites</li>
  </ul>
  <p class="preco">R$ 37</p>
  <p class="preco-tipo">Pagamento único</p>
  <a class="botao" href="{checkout}">Quero o caderno →</a>
  <p class="nota">Toque no botão para abrir a página de pagamento.</p>
</div></body></html>
"""


def achar_navegador():
    candidatos = [
        os.environ.get("CHROME_PATH"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
    ]
    for c in candidatos:
        if c and os.path.exists(c):
            return c
    sys.exit("Navegador não encontrado. Defina CHROME_PATH com o caminho do Chrome ou Edge.")


def gerar_pagina_continua(navegador, largura, altura, base_pt, destino):
    html = PAGINA_CONTINUA.format(
        fontes=FONTES.as_uri(), marca=MARCA.as_uri(), checkout=CHECKOUT.replace("&", "&amp;"),
        w=largura, h=altura, base=base_pt,
    )
    with tempfile.TemporaryDirectory() as tmp:
        arq = pathlib.Path(tmp) / "continua.html"
        arq.write_text(html, encoding="utf-8")
        subprocess.run(
            [navegador, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             f"--user-data-dir={pathlib.Path(tmp) / 'perfil'}", "--virtual-time-budget=4000",
             f"--print-to-pdf={destino}", arq.as_uri()],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
        )
    leitor = PdfReader(str(destino))
    if len(leitor.pages) != 1:
        sys.exit(f"A página 'o caderno continua' saiu com {len(leitor.pages)} páginas; ajuste fonte_base_pt.")


def destino_da_anotacao(leitor, anotacao):
    """Índice (0-based) da página de destino de um link interno, ou None."""
    dest = anotacao.get("/Dest")
    acao = anotacao.get("/A")
    if dest is None and acao is not None and acao.get("/S") == "/GoTo":
        dest = acao.get("/D")
    if dest is None:
        return None
    dest = dest.get_object() if isinstance(dest, IndirectObject) else dest
    if isinstance(dest, ArrayObject):
        return leitor._get_page_number_by_indirect(dest[0])
    nomeados = leitor.named_destinations
    chave = str(dest)
    if chave in nomeados:
        return leitor.get_destination_page_number(nomeados[chave])
    return None


def montar(versao, navegador):
    origem = PRODUTO / versao["origem"]
    leitor = PdfReader(str(origem))
    caixa = leitor.pages[0].mediabox
    largura, altura = float(caixa.width), float(caixa.height)

    with tempfile.TemporaryDirectory() as tmp:
        continua_pdf = pathlib.Path(tmp) / "continua.pdf"
        gerar_pagina_continua(navegador, largura, altura, versao["fonte_base_pt"], continua_pdf)
        continua = PdfReader(str(continua_pdf))

        incluidas = versao["paginas"]
        novo_indice = {orig: i for i, orig in enumerate(incluidas)}
        indice_continua = len(incluidas)

        # Coleta os links internos antes de copiar as páginas (sem levar referências a páginas fora da amostra)
        links = []
        externos = []  # links para fora (DOIs das fontes): mantidos como estão (26/11/2026)
        for orig in incluidas:
            pagina = leitor.pages[orig]
            for ref in pagina.get("/Annots", []) or []:
                a = ref.get_object()
                if a.get("/Subtype") != "/Link":
                    continue
                acao = a.get("/A")
                if acao is not None and acao.get("/S") == "/URI":
                    externos.append((novo_indice[orig], [float(x) for x in a["/Rect"]], str(acao.get("/URI"))))
                    continue
                alvo = destino_da_anotacao(leitor, a)
                if alvo is None:
                    continue
                alvo_novo = novo_indice.get(alvo, indice_continua)
                links.append((novo_indice[orig], [float(x) for x in a["/Rect"]], alvo_novo))

        escritor = PdfWriter()
        for orig in incluidas:
            escritor.add_page(leitor.pages[orig])
        escritor.add_page(continua.pages[0])
        escritor.add_page(leitor.pages[versao["contracapa"]])

        # Remove as anotações copiadas das páginas de origem e recria só os links válidos
        for i in list(range(len(incluidas))) + [indice_continua + 1]:
            pg = escritor.pages[i]
            if "/Annots" in pg:
                del pg[NameObject("/Annots")]
        for pagina, retangulo, alvo in links:
            escritor.add_annotation(pagina, Link(rect=retangulo, target_page_index=alvo))
        for pagina, retangulo, url in externos:
            escritor.add_annotation(pagina, Link(rect=retangulo, url=url))

        escritor.add_metadata({
            "/Title": "O Elo Universal — Capítulo 1: Mentalismo (amostra)",
            "/Author": "O Elo Universal",
            "/Subject": "Caderno das Leis Herméticas — Capítulo 1 grátis",
        })
        escritor.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)

        SAIDA.mkdir(parents=True, exist_ok=True)
        destino = SAIDA / versao["saida"]
        with open(destino, "wb") as f:
            escritor.write(f)

    redirecionados = sum(1 for _, _, alvo in links if alvo == indice_continua)
    print(f"[{versao['nome']}] {destino.relative_to(RAIZ)} · {len(incluidas) + 2} páginas · "
          f"{destino.stat().st_size / 1024:.0f} KB · {len(links)} links internos "
          f"({redirecionados} levam à página 'o caderno continua')")


if __name__ == "__main__":
    navegador = achar_navegador()
    for v in VERSOES:
        montar(v, navegador)
