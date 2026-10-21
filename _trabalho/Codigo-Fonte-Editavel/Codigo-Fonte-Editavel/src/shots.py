#!/usr/bin/env python3
"""Rasteriza o PDF e monta folhas de contato.  Uso: shots.py <pdf> <prefixo> [dpi] [por_folha] [colunas]"""
import subprocess, sys, os, glob
from PIL import Image, ImageDraw
pdf, prefix = sys.argv[1], sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 60
per = int(sys.argv[4]) if len(sys.argv) > 4 else 8
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 4
out = os.path.join(os.path.dirname(os.path.abspath(pdf)), "shots"); os.makedirs(out, exist_ok=True)
for f in glob.glob(f"{out}/{prefix}-*.png"): os.remove(f)
subprocess.check_call(["pdftoppm", "-r", str(dpi), "-png", pdf, f"{out}/{prefix}"])
files = sorted(glob.glob(f"{out}/{prefix}-*.png"))
print(len(files), "páginas")
ims = [Image.open(f).convert("RGB") for f in files]
w, h = ims[0].size
pad = 14
sheets = []
for s in range(0, len(ims), per):
    chunk = ims[s:s+per]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + pad + 16) + pad), (90, 90, 94))
    d = ImageDraw.Draw(sheet)
    for i, im in enumerate(chunk):
        x = pad + (i % cols) * (w + pad); y = pad + (i // cols) * (h + pad + 16)
        sheet.paste(im, (x, y + 16)); d.text((x, y), f"p.{s+i+1}", fill=(255, 255, 255))
    p = f"{out}/{prefix}-sheet-{s//per+1:02d}.png"; sheet.save(p); sheets.append(p)
print("\n".join(sheets))
