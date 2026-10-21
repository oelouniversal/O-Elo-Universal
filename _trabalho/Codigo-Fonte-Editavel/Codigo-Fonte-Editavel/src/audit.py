#!/usr/bin/env python3
"""Mede o preenchimento (% da área útil) de cada página de texto do PDF. Uso: audit.py <pdf> <profile>"""
import sys, logging, json
logging.disable(logging.CRITICAL)
import pdfplumber
pdf_path, prof = sys.argv[1], sys.argv[2]
MT, MB = {"letter": (0.98, 1.02), "mobile": (0.62, 0.66)}[prof]
H = {"letter": 11.0, "mobile": 7.5}[prof]
pages = json.load(open(f"/home/claude/elo/build/pages-{prof}.json"))
top, bot = MT * 72, (H - MB) * 72
rows = []
with pdfplumber.open(pdf_path) as pdf:
    for n in range(1, 8):
        o = pages[f"cap-{n}"]; reg = pages[f"cap-{n}-registro"]
        porta = pages.get(f"cap-{n}-porta")
        line = []
        for pn in range(o + 1, reg + 2):
            pg = pdf.pages[pn - 1]
            ws = [w for w in pg.extract_words() if top - 2 < w["top"] < bot + 2]
            if not ws: line.append((pn, 0)); continue
            low = max(w["bottom"] for w in ws)
            line.append((pn, round((low - top) / (bot - top) * 100)))
        rows.append((n, line))
for n, line in rows:
    print(n, "  ".join(f"p{pn}:{f}%" for pn, f in line))
