#!/usr/bin/env python3
"""Controle de qualidade por página: bordas, páginas em branco, texto fora da área útil. Uso: qa_pages.py <pdf> <perfil>"""
import sys, subprocess, glob, os, logging, tempfile
logging.disable(logging.CRITICAL)
import pdfplumber
from PIL import Image
import numpy as np
pdf_path, prof = sys.argv[1], sys.argv[2]
MS = {"letter": 1.25, "mobile": 0.44}[prof]
W, H = {"letter": (8.5, 11.0), "mobile": (4.2, 7.5)}[prof]
tmp = tempfile.mkdtemp()
subprocess.check_call(["pdftoppm", "-r", "50", "-png", pdf_path, f"{tmp}/p"])
files = sorted(glob.glob(f"{tmp}/p-*.png"))
issues = []
with pdfplumber.open(pdf_path) as pdf:
    for i, (f, pg) in enumerate(zip(files, pdf.pages), 1):
        im = np.asarray(Image.open(f).convert("L")).astype(int)
        h, w = im.shape
        body = im[4:-4, 4:-4]
        dark = body.mean() < 90
        # borda: faixa de 2px nos quatro lados deve ser coerente com o miolo
        edges = {"base": im[-2:, :], "topo": im[:2, :], "esq": im[:, :2], "dir": im[:, -2:]}
        for k, e in edges.items():
            if dark and e.mean() > body.mean() + 40:
                issues.append((i, f"borda clara ({k}) em página escura: {e.mean():.0f} vs {body.mean():.0f}"))
        words = pg.extract_words()
        if not words and body.std() < 6:
            issues.append((i, "página em branco"))
        for wd in words:
            if wd["x0"] < 0 or wd["x1"] > pg.width + 0.5 or wd["top"] < 0 or wd["bottom"] > pg.height + 0.5:
                issues.append((i, f"texto fora da página: {wd['text']}")); break
        # texto fora da coluna (somente páginas claras com margens)
        if not dark:
            for wd in words:
                if wd["x1"] > (W - MS * 0.55) * 72 or wd["x0"] < (MS * 0.55) * 72:
                    issues.append((i, f"texto invade margem: {wd['text']} x0={wd['x0']:.0f} x1={wd['x1']:.0f}")); break
print(prof, "páginas:", len(files), "| problemas:", len(issues))
for i in issues: print("  p.%d: %s" % i)
