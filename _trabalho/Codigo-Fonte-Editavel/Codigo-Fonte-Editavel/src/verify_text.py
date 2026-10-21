#!/usr/bin/env python3
"""Integridade do texto: .docx original x texto extraído de cada PDF (palavras reagrupadas por posição)."""
import re, sys, collections, unicodedata, logging
logging.disable(logging.CRITICAL)
import pdfplumber
def norm(s):
    s = unicodedata.normalize("NFC", s.lower())
    s = s.replace("…", "...").replace("“", '"').replace("”", '"').replace("’", "'")
    s = s.replace("_", " ").replace("○", " ").replace("☐", " ").replace("─", " ").replace("–", " ").replace("—", " ").replace("--", " ")
    return s
def words(s):
    toks = re.findall(r"[0-9a-zà-ÿ][0-9a-zà-ÿ./:]*", norm(s).replace("-", " ").replace("...", " "))
    return [t.rstrip(".:") for t in toks if t.rstrip(".:")]
src = open("build/verify/source.txt", encoding="utf-8").read().replace("(Produto) Capítulos 1 a 5 - Conteúdo", " ")
sw = collections.Counter(words(src)); tot = sum(sw.values())
def pdf_text(path):
    out = []
    with pdfplumber.open(path) as pdf:
        for pg in pdf.pages:
            ws = pg.extract_words(x_tolerance=4.2, y_tolerance=2, keep_blank_chars=False, use_text_flow=False)
            out.append(" ".join(w["text"] for w in ws))
    return "\n".join(out)
for path in sys.argv[1:]:
    t = pdf_text(path)
    pw = collections.Counter(words(t))
    # DOIs podem quebrar em linhas: confirma por busca na cadeia sem espaços
    squashed = re.sub(r"\s+", "", norm(t))
    miss = sw - pw
    for tok in list(miss):
        if tok.startswith("https") and tok.rstrip("/") in squashed:
            del miss[tok]
    n = sum(miss.values())
    print(f"== {path.split('/')[-1]}: original {tot} palavras | preservadas {tot-n} ({100*(tot-n)/tot:.2f}%) | ausentes {n}")
    if n: print("   ausentes:", dict(sorted(miss.items(), key=lambda x: -x[1])[:60]))
