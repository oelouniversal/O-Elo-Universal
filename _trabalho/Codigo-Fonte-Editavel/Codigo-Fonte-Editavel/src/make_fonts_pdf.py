#!/usr/bin/env python3
"""Converte as fontes para TrueType estático (glyf), subconjunto pt-BR, em WOFF.
Motivo: o Chromium embute OTF/CFF e fontes variáveis como Type 3; TrueType estático sai como fonte
TrueType nativa no PDF (mais nítida em leitores de PDF e tablets)."""
import os
from fontTools import subset
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "fonts"); OUT = os.path.join(SRC, "pdf"); os.makedirs(OUT, exist_ok=True)
UNI = "U+0020-007E,U+00A0-00FF,U+0131,U+0152-0153,U+0160-0161,U+017D-017E,U+2010-2015,U+2018-201E,U+2022,U+2026,U+2030,U+2032-2033,U+2039-203A,U+20AC,U+2190-2193,U+221E,U+25CB"

def otf_to_ttf(font, max_err=1.0):
    order = font.getGlyphOrder()
    gs = font.getGlyphSet()
    glyf = newTable("glyf"); glyf.glyphOrder = order; glyf.glyphs = {}
    for name in order:
        pen = TTGlyphPen(gs)
        gs[name].draw(Cu2QuPen(pen, max_err, reverse_direction=True))
        glyf[name] = pen.glyph()
    font["loca"] = newTable("loca"); font["glyf"] = glyf
    maxp = font["maxp"]; maxp.tableVersion = 0x00010000
    for k in ("maxZones", "maxTwilightPoints", "maxStorage", "maxFunctionDefs", "maxInstructionDefs", "maxStackElements",
              "maxSizeOfInstructions", "maxComponentElements", "maxPoints", "maxContours", "maxCompositePoints",
              "maxCompositeContours", "maxComponentDepth"):
        setattr(maxp, k, 0)
    maxp.maxZones = 1
    font["head"].glyphDataFormat = 0
    font["post"].formatType = 2.0; font["post"].extraNames = []; font["post"].mapping = {}
    for t in ("CFF ", "VORG"):
        if t in font: del font[t]
    font.sfntVersion = "\0\1\0\0"
    return font

def finish(font, name):
    opts = subset.Options(); opts.flavor = "woff"; opts.layout_features = ["kern", "liga", "ccmp", "locl", "mark", "mkmk", "calt", "case", "onum", "lnum"]
    opts.name_IDs = ["*"]; opts.notdef_outline = True; opts.glyph_names = False; opts.hinting = False
    sub = subset.Subsetter(opts); sub.populate(unicodes=subset.parse_unicodes(UNI)); sub.subset(font)
    font.flavor = "woff"
    p = os.path.join(OUT, name + ".woff"); font.save(p)
    print(name, os.path.getsize(p) // 1024, "KB")

for f, out in [("texgyrepagella-regular.otf", "Pagella-Regular"), ("texgyrepagella-italic.otf", "Pagella-Italic"),
               ("Inter-Medium.otf", "Inter-Medium"), ("Inter-SemiBold.otf", "Inter-SemiBold")]:
    finish(otf_to_ttf(TTFont(os.path.join(SRC, f))), out)

for f, w, out in [("Lora-Variable.ttf", 400, "Lora-Regular"), ("Lora-Variable.ttf", 600, "Lora-SemiBold"),
                  ("Lora-Italic-Variable.ttf", 400, "Lora-Italic")]:
    vf = TTFont(os.path.join(SRC, f))
    inst = instancer.instantiateVariableFont(vf, {"wght": w}, inplace=False)
    finish(inst, out)
