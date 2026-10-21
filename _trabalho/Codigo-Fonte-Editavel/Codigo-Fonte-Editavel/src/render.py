#!/usr/bin/env python3
"""HTML -> PDF com Chromium (Playwright). Duas passagens: a primeira descobre em que página cada
âncora caiu (destinos nomeados do PDF); a segunda grava esses números no sumário e nos mapas.
Uso: python3 render.py <letter|mobile> [saida.pdf]
"""
import json, os, sys, re
from playwright.sync_api import sync_playwright
import pikepdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build as B

SIZES = {"letter": (8.5, 11.0), "mobile": (4.2, 7.5)}
CHROME = "/opt/pw-browsers/chromium"

def chrome_path():
    for root, dirs, files in os.walk(CHROME):
        if "chrome" in files and os.access(os.path.join(root, "chrome"), os.X_OK):
            return os.path.join(root, "chrome")
    return None

def to_pdf(html_path, pdf_path, profile):
    w, h = SIZES[profile]
    exe = chrome_path()
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = br.new_page()
        pg.goto("file://" + os.path.abspath(html_path), wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(400)
        pg.pdf(path=pdf_path, width=f"{w}in", height=f"{h}in", prefer_css_page_size=True,
               print_background=True, outline=False, tagged=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        br.close()

def dest_pages(pdf_path):
    """id -> número de página (1-based), lido dos destinos nomeados do PDF."""
    out = {}
    with pikepdf.open(pdf_path) as pdf:
        pages = {p.obj.objgen: i + 1 for i, p in enumerate(pdf.pages)}
        root = pdf.Root
        def resolve(d):
            if isinstance(d, pikepdf.Dictionary) and "/D" in d:
                d = d.D
            if isinstance(d, pikepdf.Array) and len(d) and isinstance(d[0], pikepdf.Object):
                try:
                    return pages.get(d[0].objgen)
                except Exception:
                    return None
            return None
        if "/Dests" in root:
            for k, v in root.Dests.items():
                out[str(k)[1:]] = resolve(v)
        if "/Names" in root and "/Dests" in root.Names:
            def walk(node):
                if "/Names" in node:
                    n = node.Names
                    for i in range(0, len(n), 2):
                        out[str(n[i])] = resolve(n[i + 1])
                for kid in node.get("/Kids", []):
                    walk(kid)
            walk(root.Names.Dests)
    return {k: v for k, v in out.items() if v}

def add_outline(pdf, pages, nchap):
    import json as _j
    c = _j.load(open(os.path.join(HERE, "content.json"), encoding="utf-8"))
    chs = c["chapters"]
    total = len(pdf.pages)
    with pdf.open_outline() as ol:
        ol.root.clear()
        def item(title, page, kids=()):
            it = pikepdf.OutlineItem(title, page - 1)
            it.children.extend(kids)
            return it
        ol.root.append(item("Capa", 1))
        ol.root.append(item("Como usar este caderno", 2))
        ol.root.append(item("Sumário", pages["sumario"]))
        for ch in chs:
            n = ch["n"]
            if ch["bonus"] and n == min(x["n"] for x in chs if x["bonus"]):
                ol.root.append(item("Capítulos Bônus", pages[f"cap-{n}"] - 1))
            reg = pages[f"cap-{n}-registro"]
            kids = [item("O que a tradição afirma", pages[f"cap-{n}-tradicao"]),
                    item("A pista da ciência", pages[f"cap-{n}-pista"]),
                    item("O experimento: " + ch["experimento"]["name"], pages[f"cap-{n}-experimento"]),
                    item("O registro", reg),
                    item(ch["porta"]["label"] + " · Fontes", reg + 1)]
            ol.root.append(item(f"Capítulo {n} — {ch['name']}" + (" (bônus)" if ch["bonus"] else ""), pages[f"cap-{n}"], kids))
        ol.root.append(item("Fechamento: o que se repetiu?", pages["fechamento"]))
        ol.root.append(item("Contracapa", total))

def set_meta(pdf_path, title, subtitle, author, keywords, pages=None):
    with pikepdf.open(pdf_path, allow_overwriting_input=True) as pdf:
        with pdf.open_metadata(set_pikepdf_as_editor=False) as m:
            m["dc:title"] = title
            m["dc:creator"] = [author]
            m["dc:description"] = subtitle
            m["dc:language"] = ["pt-BR"]
            m["pdf:Keywords"] = keywords
        pdf.docinfo["/Title"] = title
        pdf.docinfo["/Author"] = author
        pdf.docinfo["/Subject"] = subtitle
        pdf.docinfo["/Keywords"] = keywords
        pdf.Root.Lang = pikepdf.String("pt-BR")
        if pages: add_outline(pdf, pages, 7)
        pdf.Root.ViewerPreferences = pikepdf.Dictionary(DisplayDocTitle=True)
        pdf.save(pdf_path)

def run(profile, out_pdf=None, final=True):
    out_pdf = out_pdf or os.path.join(ROOT, "build", f"caderno-{profile}.pdf")
    html1 = os.path.join(ROOT, "build", f"book-{profile}.html")
    B.build(profile, {}, html1)
    to_pdf(html1, out_pdf, profile)
    pages = dest_pages(out_pdf)
    for _ in range(2):
        B.build(profile, pages, html1)
        to_pdf(html1, out_pdf, profile)
        new = dest_pages(out_pdf)
        if new == pages:
            break
        pages = new
    json.dump(pages, open(os.path.join(ROOT, "build", f"pages-{profile}.json"), "w"), indent=1, sort_keys=True)
    if final:
        set_meta(out_pdf, "Caderno das Leis Herméticas — O Elo Universal",
                 "As leis que conectam tudo — do universo à sua mente.", "O Elo Universal",
                 "leis herméticas, Kybalion, experimentos, caderno, O Elo Universal", pages)
    return out_pdf, pages

if __name__ == "__main__":
    prof = sys.argv[1] if len(sys.argv) > 1 else "letter"
    out, pages = run(prof, sys.argv[2] if len(sys.argv) > 2 else None)
    print(out, "anchors:", len(pages))
