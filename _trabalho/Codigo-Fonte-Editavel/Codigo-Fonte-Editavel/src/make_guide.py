#!/usr/bin/env python3
"""Guia de identidade visual (PDF, 2 páginas, carta) -> dist/Guia-de-Identidade-Visual.pdf"""
import os, sys, base64
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import ornaments as O
import render as R
from playwright.sync_api import sync_playwright
import pikepdf

def b64(p): return base64.b64encode(open(p, "rb").read()).decode()
F = os.path.join(ROOT, "fonts", "pdf")
fonts = "".join(
    f"@font-face{{font-family:'{fam}';src:url(data:font/woff;base64,{b64(os.path.join(F, fn))}) format('woff');font-weight:{w};font-style:{st}}}"
    for fam, fn, w, st in [("Pagella", "Pagella-Regular.woff", 400, "normal"), ("Pagella", "Pagella-Italic.woff", 400, "italic"),
                           ("Lora", "Lora-Regular.woff", 400, "normal"), ("Lora", "Lora-Italic.woff", 400, "italic"),
                           ("Inter", "Inter-Medium.woff", 500, "normal"), ("Inter", "Inter-SemiBold.woff", 600, "normal")])

# (nome, hex, papel de uso, contraste calculado contra o fundo indicado)
PALETA = [
    ("Grafite 900", "#1B1D21", "Fundo das páginas escuras (capa, aberturas, divisor, contracapa)", None),
    ("Grafite 950", "#14161A", "Fundo profundo e vinheta da capa", None),
    ("Papel", "#F4EFE6", "Fundo das páginas de leitura", None),
    ("Tinta", "#1E2024", "Texto corrido sobre papel", "14,2 : 1 sobre Papel"),
    ("Âmbar 300", "#D9A94B", "Destaques e rótulos sobre grafite", "7,8 : 1 sobre Grafite 900"),
    ("Âmbar 700", "#7A5818", "Rótulos e numerais pequenos sobre papel", "5,7 : 1 sobre Papel"),
    ("Âmbar 600", "#8E6620", "Somente numerais grandes e ornamentos sobre papel", "4,5 : 1 sobre Papel"),
    ("Azul-aço 300", "#A9BAC5", "Segundo traço dos ornamentos sobre grafite", "8,5 : 1 sobre Grafite 900"),
    ("Azul-aço 700", "#3B4F5C", "Segundo traço dos ornamentos sobre papel", "7,5 : 1 sobre Papel"),
    ("Osso", "#EDE6DA", "Texto sobre grafite", "13,6 : 1 sobre Grafite 900"),
]
sw = "".join(
    f'<div class="sw"><i style="background:{h}"></i><b>{n}</b><code>{h}</code><span>{u}</span>'
    + (f'<em>{c}</em>' if c else '') + '</div>' for n, h, u, c in PALETA)

def orn(n, cls="g"):
    return f'<div class="{cls}">{O.ORN[n]()}</div>'
nomes = {1: "Mentalismo", 2: "Correspondência", 3: "Vibração", 4: "Polaridade", 5: "Ritmo", 6: "Causa e Efeito", 7: "Gênero"}
orn_dark = "".join(f'<figure>{orn(n)}<figcaption>{n} · {nomes[n]}</figcaption></figure>' for n in range(1, 8))

html = f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Guia de Identidade Visual — O Elo Universal</title>
<style>{fonts}
@page{{size:8.5in 11in;margin:0}}
:root{{--g9:#1B1D21;--g95:#14161A;--p:#F4EFE6;--ink:#1E2024;--a3:#D9A94B;--a7:#7A5818;--a6:#8E6620;--b3:#A9BAC5;--b7:#3B4F5C;--bone:#EDE6DA;--rule:#C9BFAB;--orn-bg:#F4EFE6}}
*{{box-sizing:border-box}}
html{{font-size:10pt}}
body{{margin:0;background:var(--p);color:var(--ink);font:400 1rem/1.5 'Lora',Georgia,serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:8.5in;height:11in;padding:.7in .8in .6in;position:relative;overflow:hidden;break-after:page;display:flex;flex-direction:column}}
.pg:last-child{{break-after:auto}}
.dark{{background:var(--g9);color:var(--bone);--orn-bg:#1B1D21}}
.kick{{font:600 .66rem/1 'Inter',sans-serif;letter-spacing:.3em;text-transform:uppercase;color:var(--a7)}}
.dark .kick{{color:var(--a3)}}
h1{{font:400 2.5rem/1.05 'Pagella',Palatino,serif;margin:.5rem 0 .4rem}}
h2{{font:400 1.35rem/1.2 'Pagella',Palatino,serif;margin:1.1rem 0 .4rem;padding-bottom:.35rem;border-bottom:.6pt solid var(--rule)}}
.dark h2{{border-color:#3a3e44}}
p{{margin:.3rem 0;font-size:.95rem}}
.lead{{font:italic 1.1rem/1.4 'Pagella',Palatino,serif;color:var(--a7);margin:.2rem 0 .6rem}}
.dark .lead{{color:var(--a3)}}
.sws{{display:grid;grid-template-columns:repeat(5,1fr);gap:.55rem .6rem;margin-top:.5rem}}
.sw{{display:flex;flex-direction:column;gap:.12rem;font-size:.66rem;line-height:1.3}}
.sw i{{display:block;height:.62in;border-radius:3px;border:.6pt solid rgba(0,0,0,.18);margin-bottom:.15rem}}
.sw b{{font:600 .68rem/1.2 'Inter',sans-serif}}
.sw code{{font:500 .66rem/1.2 'Inter',sans-serif;color:#5C6168}}
.sw span{{color:#33373D}}
.sw em{{font-style:normal;font:500 .6rem/1.3 'Inter',sans-serif;color:var(--a7)}}
.dark .sw i{{border-color:rgba(237,230,218,.28)}}
.dark .sw b{{color:var(--bone)}}
.dark .sw code{{color:#aab0b7}}
.dark .sw span{{color:#c9cdd2}}
.dark .sw em{{color:var(--a3)}}
.dark .type small{{color:var(--a3)}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem}}
.spec{{display:grid;grid-template-columns:auto 1fr;gap:.2rem .8rem;font-size:.78rem}}
.spec dt{{font:600 .62rem/1.7 'Inter',sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--a7)}}
.spec dd{{margin:0}}
.dark .spec dt{{color:var(--a3)}}
.type{{display:grid;grid-template-columns:1fr;gap:.55rem;margin-top:.4rem}}
.type div{{border-left:2px solid var(--a6);padding:.05rem 0 .05rem .7rem}}
.type small{{display:block;font:600 .6rem/1.4 'Inter',sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--a7)}}
.t1{{font:400 1.6rem/1.15 'Pagella',Palatino,serif}}
.t2{{font:400 1rem/1.5 'Lora',serif}}
.t3{{font:600 .7rem/1.4 'Inter',sans-serif;letter-spacing:.28em;text-transform:uppercase}}
.grid7{{display:grid;grid-template-columns:repeat(7,1fr);gap:.5rem;margin:.7rem 0}}
.grid7 figure{{margin:0;text-align:center}}
.g{{aspect-ratio:1;background:var(--g9);border-radius:3px;padding:.3rem}}
.g svg{{width:100%;height:100%}}
.grid7 figcaption{{font:500 .58rem/1.3 'Inter',sans-serif;margin-top:.25rem;color:#33373D}}
.orn .oa,.linkmark .oa,.doorglyph .oa{{stroke:var(--a3);color:var(--a3)}}
.orn .ob,.linkmark .ob,.doorglyph .ob{{stroke:var(--b3);color:var(--b3)}}
.orn .op{{stroke:var(--bone);color:var(--bone)}}
.lt .linkmark .oa{{stroke:var(--a6)}} .lt .linkmark .ob{{stroke:var(--b7)}}
.lt .doorglyph .oa{{stroke:var(--a6)}} .lt .doorglyph .ob{{stroke:var(--b7)}}
.marks{{display:flex;gap:1.4rem;align-items:center;margin:.5rem 0}}
.marks svg{{height:.5in;width:auto}}
.chip{{display:flex;align-items:center;gap:.7rem;padding:.55rem .8rem;border-radius:3px}}
.chip.d{{background:var(--g9);--orn-bg:#1B1D21}} .chip.l{{background:#ECE5D7;border:.6pt solid var(--rule)}}
ul.r{{margin:.3rem 0;padding-left:1.1rem;font-size:.85rem}}
ul.r li{{margin:.18rem 0}}
.cover{{position:absolute;right:.8in;top:.7in;width:2.1in;border-radius:3px;box-shadow:0 6px 24px rgba(0,0,0,.45)}}
.foot{{margin-top:auto;font:500 .6rem/1 'Inter',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#5C6168;display:flex;justify-content:space-between;padding-top:.5rem}}
.dark .foot{{color:#8b9198}}
table.m{{border-collapse:collapse;width:100%;font-size:.76rem;margin:.4rem 0}}
table.m th{{font:600 .6rem/1.4 'Inter',sans-serif;letter-spacing:.16em;text-transform:uppercase;text-align:left;color:var(--a7);padding:.3rem .5rem .3rem 0;border-bottom:.6pt solid var(--rule)}}
table.m td{{padding:.3rem .5rem .3rem 0;border-bottom:.6pt solid #E3DBCB;vertical-align:top}}
</style>
<body>
<section class="pg dark">
  <div class="kick">Guia de identidade visual</div>
  <h1>O Elo Universal</h1>
  <p class="lead">Caderno das Leis Herméticas — sistema visual</p>
  <img class="cover" src="data:image/jpeg;base64,{b64(os.path.join(ROOT, 'assets', 'capa-letter.jpg'))}" alt="">
  <div style="max-width:3.7in;margin-top:.6rem">
    <p><b>Conceito.</b> A marca é o elo: uma corrente de sete elos, um por lei, que liga cada ideia à seguinte. A capa é uma arte original (corrente de ouro sobre grafite) e a marca de elo — dois elos entrelaçados — assina todas as páginas.</p>
    <p><b>Tom.</b> Sóbrio, contemplativo, editorial. Páginas escuras marcam entradas e saídas (capa, aberturas de capítulo, divisor, contracapa); páginas claras são para ler e escrever.</p>
  </div>
  <h2>Paleta</h2>
  <div class="sws">{sw}</div>
  <h2>Tipografia</h2>
  <div class="type">
    <div><small>Títulos e numerais · TeX Gyre Pagella</small><span class="t1">Mentalismo — “Tudo o que existe começa como pensamento.”</span></div>
    <div><small>Texto corrido · Lora, 11,5 pt, entrelinha 1,58</small><span class="t2">Antes de qualquer lei, uma pergunta: o que você deixou de ver hoje?</span></div>
    <div><small>Rótulos e interface · Inter Semibold, caixa-alta, espaçamento .2–.4 em</small><span class="t3" style="color:var(--a3)">Tradição · Pista · Experimento · Registro</span></div>
  </div>
  <div class="foot"><span>O Elo Universal · Guia de identidade</span><span>1</span></div>
</section>

<section class="pg lt">
  <div class="kick">Sistema</div>
  <h2 style="margin-top:.3rem">Ornamentos: um glifo por lei</h2>
  <p>Traço fino, dois tons (âmbar e azul-aço), grade 120 × 120. Sobre grafite usam Âmbar 300 / Azul-aço 300; sobre papel, Âmbar 600 / Azul-aço 700.</p>
  <div class="grid7">{orn_dark}</div>
  <div class="marks">
    <div class="chip d">{O.link_mark()}<span style="font:600 .6rem 'Inter';letter-spacing:.2em;color:var(--a3);text-transform:uppercase">Marca do Elo</span></div>
    <div class="chip l">{O.link_mark()}<span style="font:600 .6rem 'Inter';letter-spacing:.2em;color:var(--a7);text-transform:uppercase">Marca do Elo</span></div>
    <div class="chip d">{O.door()}<span style="font:600 .6rem 'Inter';letter-spacing:.2em;color:var(--a3);text-transform:uppercase">Glifo da Porta</span></div>
  </div>
  <h2>Estrutura de cada capítulo</h2>
  <table class="m">
    <tr><th style="width:1.35in">Peça</th><th>Função e tratamento</th></tr>
    <tr><td>Abertura (escura)</td><td>Glifo da lei, nome, epígrafe, mapa 1–4 com o número da página de cada parte e numeral gigante em âmbar a 7 % de opacidade.</td></tr>
    <tr><td>1 · Tradição</td><td>O que a tradição afirma, com selo em itálico que separa afirmação filosófica de fato demonstrado.</td></tr>
    <tr><td>2 · Pista</td><td>A pesquisa e os quadros “O que isso sugere” / “O que isso NÃO mostra” em fundo cinza-quente com filete lateral.</td></tr>
    <tr><td>3 · Experimento</td><td>Passos numerados em linha do tempo vertical; duração destacada à direita.</td></tr>
    <tr><td>4 · Registro</td><td>Página de preencher: linhas, marcas do dia (círculos), tabelas e escalas.</td></tr>
    <tr><td>Porta + Fontes</td><td>Painel escuro com a pergunta que leva à próxima lei, link para o capítulo seguinte e fontes com DOI clicável.</td></tr>
  </table>
  <h2>Formatos e regras de página</h2>
  <div class="cols">
    <dl class="spec">
      <dt>Carta</dt><dd>8,5 × 11 in. Margens 1,25 in laterais; cabeçalho corrente (marca à esquerda, “n · nome da lei” à direita); número de página centrado.</dd>
      <dt>Celular</dt><dd>4,2 × 7,5 in (≈ 9:16). Margens 0,44 in; mesmo corpo de 11,5 pt.</dd>
      <dt>Web</dt><dd>HTML responsivo e autônomo, com capa vertical em telas estreitas e botão flutuante “Sumário”.</dd>
    </dl>
    <ul class="r">
      <li>Páginas escuras ocupam a folha inteira, sem margem branca.</li>
      <li>Rótulos pequenos sobre papel usam Âmbar 700 (5,7 : 1); Âmbar 600 só em numerais grandes.</li>
      <li>Cada capítulo ocupa duas páginas de texto + registro + porta (Carta).</li>
      <li>Fontes e imagens estão embutidas: nenhum arquivo depende de recurso externo.</li>
      <li>Texto de capa nunca fica dentro da imagem: a arte é entregue sem tipografia para reutilização.</li>
    </ul>
  </div>
  <h2>Usos a evitar</h2>
  <ul class="r">
    <li>Âmbar 500 (#B8862F) como cor de texto sobre papel (2,8 : 1, abaixo do mínimo de leitura).</li>
    <li>Recolorir ou girar a marca do elo; usar a corrente da capa como fundo de texto corrido.</li>
    <li>Trocar a fonte de títulos ou aumentar o espaçamento dos rótulos acima de .4 em.</li>
  </ul>
  <div class="foot"><span>Fontes: TeX Gyre Pagella (GUST Font License) · Lora e Inter (SIL Open Font License 1.1)</span><span>2</span></div>
</section>
</body></html>"""

out_html = os.path.join(ROOT, "build", "guia.html")
open(out_html, "w", encoding="utf-8").write(html)
dst = os.path.join(ROOT, "dist", "Guia-de-Identidade-Visual.pdf")
exe = R.chrome_path()
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    pg = br.new_page()
    pg.goto("file://" + out_html, wait_until="load")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(300)
    pg.pdf(path=dst, width="8.5in", height="11in", prefer_css_page_size=True, print_background=True, tagged=True,
           margin=dict(top="0", right="0", bottom="0", left="0"))
    br.close()
with pikepdf.open(dst, allow_overwriting_input=True) as pdf:
    with pdf.open_metadata(set_pikepdf_as_editor=False) as m:
        m["dc:title"] = "Guia de Identidade Visual — O Elo Universal"
        m["dc:language"] = ["pt-BR"]
    pdf.docinfo["/Title"] = "Guia de Identidade Visual — O Elo Universal"
    pdf.Root.Lang = pikepdf.String("pt-BR")
    pdf.Root.ViewerPreferences = pikepdf.Dictionary(DisplayDocTitle=True)
    pdf.save(dst)
print(dst, len(pikepdf.open(dst).pages), "páginas")
