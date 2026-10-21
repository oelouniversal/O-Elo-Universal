#!/usr/bin/env python3
"""Gerador do 'Caderno das Leis Herméticas'.
content.json + book.css + ornaments.py  ->  HTML autônomo (fontes e capa embutidas).

Perfis:  letter (PDF 8,5x11 in)  |  mobile (PDF 9:16 para celular)  |  screen (HTML responsivo)
Uso:     python3 build.py <perfil> [pages.json]
"""
import base64, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import ornaments as O

BRAND = "O Elo Universal"

# ------------------------------------------------------------------ perfis
PROFILES = {
    "letter": dict(
        PW="8.5in", PH="11in", PH_SAFE="11in", ROOT="11.5pt",
        MT=".98in", MS="1.25in", MB="1.02in", FOOT_PAD=".42in", HEAD_PAD=".42in",
        CV_T="0.95in", CV_S="1in", CV_B="0.95in", CV_H1="3.5em",
        OP_T="0.95in", OP_B="0.95in", OP_S="1in", BIGNUM="30em", BIGNUM_TOP="0", ORN_W="3.3in",
        GRID_H="2.5em", INNER_H="8.82in", LN="1.95em", PORTA_MAX="62%", HOW_PAD="1.05em", TOC_PAD=".85em", BIGNUM_R=".45in", BIGNUM_B="1.35in", MARGIN_PT="6.9pt", COVER_FILE="capa-letter.jpg"),
    "mobile": dict(
        PW="4.2in", PH="7.5in", PH_SAFE="7.5in", ROOT="11.5pt",
        MT=".62in", MS=".44in", MB=".66in", FOOT_PAD=".2in", HEAD_PAD=".2in",
        CV_T=".5in", CV_S=".4in", CV_B=".55in", CV_H1="2.6em",
        OP_T=".55in", OP_B=".55in", OP_S=".44in", BIGNUM="22em", BIGNUM_TOP="0", ORN_W="2.3in",
        GRID_H="2.4em", INNER_H="6.2in", LN="1.75em", PORTA_MAX="64%", HOW_PAD=".8em", TOC_PAD=".55em", BIGNUM_R=".2in", BIGNUM_B="1.7in", MARGIN_PT="6.6pt", COVER_FILE="capa-mobile.jpg"),
}
PROFILES["screen"] = dict(PROFILES["letter"])
for _k, _v in json.loads(os.environ.get("PROFILE_OVERRIDES", "{}")).items():
    PROFILES[_k.split(".")[0]][_k.split(".")[1]] = _v

# ------------------------------------------------------------------ utilidades
def read(p, mode="r"):
    with open(p, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        return f.read()

def b64(path):
    return base64.b64encode(read(path, "rb")).decode()

URL_RE = re.compile(r"(https?://[^\s<]+)")

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = URL_RE.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', s)
    return s

def nb(s):
    """Espaço não separável entre número e unidade curta (1 dia, 4 dias...)."""
    return re.sub(r"(\d) (dias?)", "\\1\u00a0\\2", s)

def lines(n):
    return '<div class="lines">' + "<i></i>" * n + "</div>"

PARTS = [("tradicao", "Tradição"), ("pista", "Pista"), ("experimento", "Experimento"), ("registro", "Registro")]

# ------------------------------------------------------------------ blocos de texto
def render_blocks(blocks):
    out = []
    for b in blocks:
        t = b["t"]
        if t == "p":
            out.append(f'<p>{inline(b["x"])}</p>')
        elif t == "ul":
            out.append('<ul class="pl">' + "".join(f"<li>{inline(i)}</li>" for i in b["items"]) + "</ul>")
        elif t == "seal":
            out.append(f'<p class="seal">{inline(b["x"])}</p>')
        elif t == "refrao":
            out.append(f'<div class="refrao">{O.link_mark()}<p>{inline(b["x"])}</p></div>')
        elif t == "sugere":
            out.append(f'<div class="callout sugere"><span class="lab">O que isso sugere:</span><p>{inline(b["x"])}</p></div>')
        elif t == "nao":
            body = ""
            if "items" in b:
                body += "<ul>" + "".join(f"<li>{inline(i)}</li>" for i in b["items"]) + "</ul>"
            else:
                body += f'<p>{inline(b["x"])}</p>'
            if b.get("after"):
                body += f'<p class="after">{inline(b["after"])}</p>'
            cls = "callout nao list" if "items" in b else "callout nao"
            out.append(f'<div class="{cls}"><span class="lab">O que isso NÃO mostra:</span>{body}</div>')
        elif t == "note":
            out.append(f'<p class="note">{inline(b["x"])}</p>')
        elif t == "caution":
            out.append(f'<div class="callout caution"><p>{inline(b["x"])}</p></div>')
        elif t == "step":
            out.append("@@STEP@@" + json.dumps(b, ensure_ascii=False) + "@@/STEP@@")
        else:
            raise ValueError(t)
    # passos: marca o último de cada sequência para encerrar a linha-guia
    res = []
    for i, frag in enumerate(out):
        if frag.startswith("@@STEP@@"):
            b = json.loads(frag[8:-9])
            last = not (i + 1 < len(out) and out[i + 1].startswith("@@STEP@@"))
            res.append(render_step(b, last))
        else:
            res.append(frag)
    return "".join(res)

def render_step(b, last):
    h = b["h"]
    if " — " in h:
        k, t = h.split(" — ", 1)
        head = f'<span class="k">{html.escape(k)}</span><span class="t">{html.escape(t)}</span>'
    else:
        head = f'<span class="t">{html.escape(h)}</span>'
    if "ol" in b:
        body = "<ol>" + "".join(f"<li>{inline(i)}</li>" for i in b["ol"]) + "</ol>"
    else:
        body = f'<p>{inline(b["x"])}</p>'
    cls = "step last" if last else "step"
    return f'<div class="{cls}"><div class="rail"><i class="dot"></i></div><div class="sb"><h4>{head}</h4>{body}</div></div>'

# ------------------------------------------------------------------ registro
def render_registro(items):
    out = []
    for it in items:
        k = it["k"]
        if k == "head":
            out.append(f'<div class="reg-head">{html.escape(it["x"])}</div>')
        elif k == "area":
            out.append(f'<div class="fld"><div class="fld-l">{inline(it["label"])}</div>{lines(it["lines"])}</div>')
        elif k == "line":
            out.append(f'<div class="fld inl"><span class="fld-l">{inline(it["label"])}</span><span class="blank"></span></div>')
        elif k == "inline2":
            out.append('<div class="fld two">'
                       f'<div class="half"><span class="fld-l">{inline(it["a"])}</span><span class="blank"></span></div>'
                       f'<div class="half w"><span class="fld-l">{inline(it["b"])}</span><span class="blank"></span></div></div>')
        elif k == "pair":
            out.append('<div class="fld two">'
                       f'<div class="half"><span class="fld-l">{inline(it["a"])}</span><span class="blank"></span></div>'
                       f'<div class="half"><span class="fld-l">{inline(it["b"])}</span><span class="blank"></span></div></div>')
        elif k == "marks":
            out.append(f'<div class="fld"><div class="fld-l">{inline(it["label"])}</div>'
                       f'<div class="marks">{"<i></i>" * it["n"]}</div></div>')
        elif k == "numbered":
            pfx = f'<span class="pfx">{html.escape(it["prefix"])}</span>' if it.get("prefix") else ""
            rows = "".join(f'<div class="nline"><span class="nn">{i}.</span>{pfx}<span class="blank"></span></div>'
                           for i in range(1, it["n"] + 1))
            out.append(f'<div class="fld"><div class="fld-l">{inline(it["label"])}</div>{rows}</div>')
        elif k == "scale":
            out.append(f'<div class="fld"><div class="fld-l">{inline(it["label"])}</div>'
                       f'<div class="scale">{"".join(f"<span>{i}</span>" for i in range(11))}</div></div>')
        elif k == "table":
            th = "".join(f"<th>{html.escape(c)}</th>" for c in it["cols"])
            rows = "".join('<tr><td class="l">' + html.escape(r) + "</td>" + "<td></td>" * (len(it["cols"]) - 1) + "</tr>"
                           for r in it["rows"])
            out.append(f'<div class="tbl"><div class="tcap">{html.escape(it["caption"])}</div><table class="grid"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>')
        elif k == "checktable":
            th = "".join(f"<th>{html.escape(c)}</th>" for c in it["cols"])
            rows = "".join('<tr><td class="l">' + html.escape(r) + '</td><td class="c"><b></b><span>sim</span><b></b><span>não</span></td><td></td></tr>'
                           for r in it["rows"])
            out.append(f'<div class="tbl"><table class="grid check"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>')
        else:
            raise ValueError(k)
    return "".join(out)

# ------------------------------------------------------------------ seções
def sec_head(num, title, cls="", small="", dur=""):
    sm = f"<small>{html.escape(small)}</small>" if small else ""
    d = f'<div class="dur"><b>Duração</b><span>{nb(html.escape(dur))}</span></div>' if dur else ""
    return (f'<header class="sec-head {cls}"><span class="sec-num">{num}</span>'
            f'<h2 class="sec-title">{html.escape(title)}{sm}</h2>{d}</header>')

class Book:
    def __init__(self, profile, pages):
        self.p = PROFILES[profile]
        self.profile = profile
        self.pages = pages
        self.c = json.load(open(os.path.join(HERE, "content.json"), encoding="utf-8"))
        self.chs = self.c["chapters"]

    def pg(self, anchor):
        v = self.pages.get(anchor)
        return str(v) if v else "·"

    # ---------- capa
    def cover(self):
        m = self.c["meta"]
        return f'''<section class="sheet cover" id="capa" aria-label="Capa">
<div class="in">
 <div class="brand">{O.link_mark()}<span>{BRAND}</span></div>
 <div class="tblock">
  <h1><span class="pre">Caderno das</span><span class="big">Leis Herméticas</span></h1>
  <div class="rule"></div>
  <p class="sub">{html.escape(m["subtitle"].rstrip("."))}</p>
  <p class="tag">{html.escape(m["tagline"])}</p>
 </div>
</div></section>'''

    # ---------- como usar
    def how(self):
        return f'''<section class="page-front page-how" id="como-usar">
<div class="fm-head">{O.link_mark()}<span>{BRAND}</span></div>
<h1 class="fm-title">Como usar este caderno</h1>
<p class="fm-lead">Sete leis herméticas, testadas uma de cada vez. A ciência entra como pista, nunca como prova.</p>
<p class="fm-intro">Cada capítulo percorre o mesmo caminho, sempre na mesma ordem.</p>
<ol class="how">
 <li><span class="n">1</span><b>A tradição afirma</b><p>O que a tradição hermética diz sobre a lei. É filosofia e tradição, não física.</p></li>
 <li class="sc"><span class="n">2</span><b>A pista da ciência</b><p>O que a pesquisa encontrou de parecido, o que isso sugere e o que NÃO mostra. Uma pista, não uma prova.</p></li>
 <li class="ex"><span class="n">3</span><b>O experimento</b><p>Um teste curto, de 1 a 7 dias, para observar a lei na sua própria rotina.</p></li>
 <li class="ex"><span class="n">4</span><b>O registro</b><p>O espaço para escrever o que você observou, fechando com uma linha sobre o que percebeu.</p></li>
 <li class="go"><span class="n nx">→</span><b>Porta para a próxima lei</b><p>Uma pergunta que leva ao capítulo seguinte.</p></li>
</ol>
<div class="legend"><span><i style="background:var(--ambar-500)"></i>Tradição</span><span><i style="background:var(--azul-500)"></i>Ciência</span><span><i style="background:var(--graf-700)"></i>Prática</span></div>
</section>'''

    # ---------- sumário
    def toc_row(self, ch):
        return (f'<a class="toc-row" href="#cap-{ch["n"]}"><span class="n">{ch["n"]}</span>'
                f'<span class="nm">{html.escape(ch["name"])}<small>{html.escape(ch["epigraph"])}</small></span>'
                f'<span class="du">{nb(html.escape(ch["experimento"]["duration"]))}</span>'
                f'<span class="pg">{self.pg("cap-%d" % ch["n"])}</span></a>')

    def toc(self):
        main = "".join(self.toc_row(c) for c in self.chs if not c["bonus"])
        bonus = "".join(self.toc_row(c) for c in self.chs if c["bonus"])
        return f'''<section class="page-front page-toc" id="sumario">
<h1 class="toc-title">Sumário</h1>
<div class="toc-sub">Sete leis · Sete pistas · Sete experimentos</div>
<div class="toc-group">Capítulos 1 a 5</div>
{main}
<div class="toc-group">Capítulos Bônus</div>
{bonus}
<div class="toc-group">Fechamento</div>
<a class="toc-row" href="#fechamento"><span class="n">∞</span><span class="nm">O que se repetiu?</span><span class="du"></span><span class="pg">{self.pg("fechamento")}</span></a>
</section>'''

    # ---------- divisória dos bônus
    def divider(self):
        items = "".join(
            f'<a href="#cap-{c["n"]}"><span class="n">{c["n"]}</span><span class="t">{html.escape(c["name"])}</span><span class="p">{self.pg("cap-%d" % c["n"])}</span></a>'
            for c in self.chs if c["bonus"])
        return f'''<section class="sheet dark divider" id="bonus">
{O.link_mark()}
<div class="kick">Capítulos</div>
<h1>Bônus</h1>
<div class="items">{items}</div>
</section>'''

    # ---------- capítulo
    def opener(self, ch):
        n = ch["n"]
        kick = f"Capítulo {n}" + (" · Bônus" if ch["bonus"] else "")
        mp = "".join(
            f'<a href="#cap-{n}-{k}"><span class="n">{i}</span><span class="l">{lab}</span><span class="p">{self.pg("cap-%d-%s" % (n, k))}</span></a>'
            for i, (k, lab) in enumerate(PARTS, 1))
        wem = 37.4 if self.profile != "mobile" else 20.8
        h1 = min(2.9, 0.9 * wem / (0.78 * len(ch["name"])))
        return f'''<section class="sheet dark opener" id="cap-{n}" data-ch="{n}" style="--h1:{h1:.2f}em;--len:{len(ch["name"])}">
<div class="bignum" aria-hidden="true">{n}</div>
<div class="top"><span>{BRAND}</span><a href="#sumario">Sumário</a></div>
<div class="art">{O.ORN[n]()}</div>
<div class="ttl">
 <div class="kick">{kick} · Lei {n} de 7</div>
 <h1>{html.escape(ch["name"])}</h1>
 <div class="rule"></div>
 <p class="epi">{html.escape(ch["epigraph"])}</p>
 <p class="lede">{html.escape(ch["lede"])}</p>
</div>
<nav class="map" aria-label="Neste capítulo">{mp}</nav>
</section>'''

    def body(self, ch):
        n = ch["n"]
        exp = ch["experimento"]
        nxt = self.chs[n] if n < len(self.chs) else None
        if nxt:
            go = f'<a class="go" href="#cap-{nxt["n"]}">Capítulo {nxt["n"]} · {html.escape(nxt["name"])}<i></i></a>'
        else:
            go = '<a class="go" href="#fechamento">Fechamento<i></i></a>'
        fontes = "".join(f"<li>{inline(f)}</li>" for f in ch["fontes"])
        return f'''<div class="cbody ch ch-{n}" data-ch="{n}">
<section class="part first" id="cap-{n}-tradicao">
{sec_head(1, "O que a tradição afirma")}
{render_blocks(ch["tradicao"])}
</section>
<section class="part" id="cap-{n}-pista">
{sec_head(2, "A pista da ciência", "is-pista")}
{render_blocks(ch["pista"])}
</section>
<section class="part" id="cap-{n}-experimento">
{sec_head(3, "O experimento", "is-exp", small=exp["name"], dur=exp["duration"])}
{render_blocks(exp["blocks"])}
</section>
<section class="part registro" id="cap-{n}-registro">
{sec_head(4, "O registro", "is-reg")}
{render_registro(ch["registro"])}
</section>
<section class="portapg" id="cap-{n}-porta">
<div class="porta">
 <div class="glyph">{O.door()}<span class="lab">{html.escape(ch["porta"]["label"])}</span></div>
 <p class="txt">{inline(ch["porta"]["x"])}</p>
 {go}
</div>
<div class="fontes"><h3>Fontes</h3><ol>{fontes}</ol></div>
</section>
</div>'''

    # ---------- fechamento
    def fim(self):
        reg = "".join(
            f'<li><a href="#cap-{c["n"]}-registro"><span class="n">{c["n"]}</span><span class="t">{html.escape(c["name"])}</span>'
            f'<span class="p">{self.pg("cap-%d-registro" % c["n"])}</span></a></li>' for c in self.chs)
        return f'''<section class="page-front page-fim" id="fechamento">
<div class="fm-head">{O.link_mark()}<span>Fechamento</span></div>
<h1 class="fim-q">O que se repetiu?</h1>
<p class="fim-p">Volte aos sete registros e leia-os juntos.</p>
<ol class="reg7">{reg}</ol>
<div class="fld">{lines(5)}</div>
</section>'''

    def back(self):
        m = self.c["meta"]
        return f'''<section class="sheet dark backcover" id="contracapa" aria-label="Contracapa">
{O.link_mark()}
<div class="b">{BRAND}</div>
<p class="t">{html.escape(m["tagline"])}</p>
</section>'''

    # ---------- CSS
    def chapter_pages(self):
        css = []
        for ch in self.chs:
            n = ch["n"]
            name = ch["name"].upper()
            css.append(f'''@page ch{n}{{margin:{self.p["MT"]} {self.p["MS"]} {self.p["MB"]};background:#F4EFE6;
 @top-left{{content:"{BRAND.upper()}";font:600 {self.p["MARGIN_PT"]}/1 'Inter',sans-serif;letter-spacing:.22em;color:#7A5818;vertical-align:bottom;padding-bottom:{self.p["HEAD_PAD"]}}}
 @top-right{{content:"{n} · {name}";font:600 {self.p["MARGIN_PT"]}/1 'Inter',sans-serif;letter-spacing:.22em;color:#5C6168;vertical-align:bottom;padding-bottom:{self.p["HEAD_PAD"]}}}
 @bottom-center{{content:counter(page);font:italic 9.5pt/1 'Pagella',serif;color:#5C6168;vertical-align:top;padding-top:{self.p["FOOT_PAD"]}}}}}
.ch-{n}{{page:ch{n}}}''')
        css.append(f'''@page fim{{margin:{self.p["MT"]} {self.p["MS"]} {self.p["MB"]};background:#F4EFE6;
 @bottom-center{{content:counter(page);font:italic 9.5pt/1 'Pagella',serif;color:#5C6168;vertical-align:top;padding-top:{self.p["FOOT_PAD"]}}}}}''')
        return "\n".join(css)

    def fonts_css(self):
        fd = os.path.join(ROOT, "fonts", "pdf")
        def ff(fam, file, w, style="normal"):
            return (f"@font-face{{font-family:'{fam}';src:url(data:font/woff;base64,{b64(os.path.join(fd, file))}) format('woff');"
                    f"font-weight:{w};font-style:{style};font-display:block}}")
        return "\n".join([
            ff("Pagella", "Pagella-Regular.woff", 400),
            ff("Pagella", "Pagella-Italic.woff", 400, "italic"),
            ff("Lora", "Lora-Regular.woff", 400),
            ff("Lora", "Lora-SemiBold.woff", 600),
            ff("Lora", "Lora-Italic.woff", 400, "italic"),
            ff("Inter", "Inter-Medium.woff", 500),
            ff("Inter", "Inter-SemiBold.woff", 600),
        ])

    def css(self):
        css = read(os.path.join(HERE, "book.css"))
        cover = os.path.join(ROOT, "assets", self.p["COVER_FILE"])
        if not os.path.exists(cover):
            cover = os.path.join(ROOT, "assets", "capa-elos.jpg")
        rep = dict(self.p)
        rep["COVER_URL"] = "data:image/jpeg;base64," + b64(cover)
        mob = os.path.join(ROOT, "assets", "capa-mobile.jpg")
        rep["COVER_URL_MOBILE"] = ("data:image/jpeg;base64," + b64(mob)) if self.profile == "screen" and os.path.exists(mob) else "data:,"
        rep["CHAPTER_PAGES"] = self.chapter_pages()
        for k, v in rep.items():
            css = css.replace("{{%s}}" % k, v)
        left = re.findall(r"\{\{[A-Z_]+\}\}", css)
        assert not left, left
        return self.fonts_css() + "\n" + css

    # ---------- documento
    def document(self):
        parts = [self.cover(), self.how(), self.toc()]
        for ch in self.chs:
            if ch["bonus"] and ch["n"] == min(c["n"] for c in self.chs if c["bonus"]):
                parts.append(self.divider())
            parts.append(self.opener(ch))
            parts.append(self.body(ch))
        parts.append(self.fim())
        parts.append(self.back())
        m = self.c["meta"]
        title = f'{m["title"]} — {BRAND}'
        return f'''<!doctype html>
<html lang="pt-BR" class="p-{self.profile}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="author" content="{BRAND}">
<meta name="description" content="{html.escape(m["tagline"])}">
<title>{html.escape(title)}</title>
<style>
{self.css()}
</style>
</head>
<body class="p-{self.profile}">
{"".join(parts)}
<a class="fab" href="#sumario" aria-label="Ir ao sumário">Sumário</a>
</body>
</html>'''


def build(profile, pages=None, out=None):
    pages = pages or {}
    doc = Book(profile, pages).document()
    out = out or os.path.join(ROOT, "build", f"book-{profile}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    return out

if __name__ == "__main__":
    prof = sys.argv[1] if len(sys.argv) > 1 else "letter"
    pages = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}
    print(build(prof, pages))
