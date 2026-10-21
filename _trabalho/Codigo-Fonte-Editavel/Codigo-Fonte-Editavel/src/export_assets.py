#!/usr/bin/env python3
"""Exporta os ativos gráficos originais (SVG + PNG) para dist/Ativos-Graficos/.
Cada SVG é autônomo: as classes de cor viram um <style> interno. Duas variantes:
  escuro (para fundo grafite) e claro (para fundo papel)."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import ornaments as O

OUT = os.path.join(ROOT, "dist", "Ativos-Graficos")
os.makedirs(os.path.join(OUT, "svg"), exist_ok=True)
os.makedirs(os.path.join(OUT, "png"), exist_ok=True)

THEMES = {
    "escuro": dict(bg="#1B1D21", oa="#D9A94B", ob="#A9BAC5", op="#EDE6DA"),
    "claro":  dict(bg="#F4EFE6", oa="#8E6620", ob="#3B4F5C", op="#5C6168"),
}
NAMES = {1: "01-mentalismo", 2: "02-correspondencia", 3: "03-vibracao", 4: "04-polaridade",
         5: "05-ritmo", 6: "06-causa-e-efeito", 7: "07-genero"}

def standalone(svg, th):
    t = THEMES[th]
    css = (f".oa{{stroke:{t['oa']};color:{t['oa']}}}.ob{{stroke:{t['ob']};color:{t['ob']}}}"
           f".op{{stroke:{t['op']};color:{t['op']}}}")
    svg = re.sub(r"var\(--orn-bg,#[0-9A-Fa-f]{6}\)", t["bg"], svg).replace("currentColor", t["oa"])
    svg = re.sub(r'class="[^"]*"', lambda m: m.group(0), svg, count=1)
    return svg.replace(">", f"><style>{css}</style>", 1)

items = [(NAMES[n], fn()) for n, fn in O.ORN.items()]
items.append(("marca-elo", O.link_mark()))
items.append(("glifo-porta", O.door()))

written = []
for name, svg in items:
    for th in THEMES:
        s = standalone(svg, th)
        p = os.path.join(OUT, "svg", f"{name}_{th}.svg")
        open(p, "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n' + s + "\n")
        written.append((p, th))

# PNGs com fundo transparente (via Chromium), 1024 px no lado maior
from playwright.sync_api import sync_playwright
import render as R
exe = R.chrome_path()
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    pg = br.new_page(device_scale_factor=1)
    for path, th in written:
        svg = open(path, encoding="utf-8").read().split("\n", 1)[1]
        m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
        vw, vh = float(m.group(1)), float(m.group(2))
        k = 1024 / max(vw, vh)
        w, h = round(vw * k), round(vh * k)
        svg = re.sub(r'<svg ', f'<svg width="{w}" height="{h}" ', svg, count=1)
        pg.set_viewport_size({"width": w, "height": h})
        pg.set_content(f'<html><body style="margin:0;background:transparent">{svg}</body></html>')
        out = os.path.join(OUT, "png", os.path.basename(path).replace(".svg", ".png"))
        pg.screenshot(path=out, omit_background=True, clip=dict(x=0, y=0, width=w, height=h))
    br.close()
print(len(written), "SVG e", len(written), "PNG em", OUT)
