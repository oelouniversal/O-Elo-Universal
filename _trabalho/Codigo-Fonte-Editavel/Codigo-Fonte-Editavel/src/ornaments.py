"""Ornamentos vetoriais originais do caderno: um glifo por lei + marca de elo.
Classes de cor (definidas no CSS): .oa âmbar, .ob azul-acinzentado, .op papel/neutro.
Todos usam viewBox 0 0 120 120 e traço fino, para conviver com a tipografia.
"""
import math

def _svg(inner, cls="orn", vb="0 0 120 120", label=""):
    aria = f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
    return (f'<svg class="{cls}" viewBox="{vb}" xmlns="http://www.w3.org/2000/svg"{aria} '
            f'fill="none" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')

def _f(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")

def mentalismo():
    # O olho como filtro: a atenção recorta o que entra.
    parts = []
    parts.append('<circle class="op" cx="60" cy="60" r="55" stroke-width=".6" opacity=".45"/>')
    parts.append('<circle class="op" cx="60" cy="60" r="48" stroke-width=".4" stroke-dasharray="1 3.2" opacity=".5"/>')
    parts.append('<path class="oa" d="M10 60 Q60 14 110 60 Q60 106 10 60 Z" stroke-width="1.5"/>')
    parts.append('<circle class="oa" cx="60" cy="60" r="19" stroke-width="1.3"/>')
    parts.append('<circle class="ob" cx="60" cy="60" r="12" stroke-width=".9"/>')
    parts.append('<circle class="oa" cx="60" cy="60" r="4.2" fill="currentColor" stroke="none"/>')
    # fios de atenção: raios que saem da pupila e se perdem
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        r0, r1 = 25, 25 + (10 if ang % 90 == 0 else 5)
        parts.append(f'<line class="ob" x1="{_f(60+r0*math.cos(a))}" y1="{_f(60+r0*math.sin(a))}" '
                     f'x2="{_f(60+r1*math.cos(a))}" y2="{_f(60+r1*math.sin(a))}" stroke-width=".7" opacity=".7"/>')
    for (x, y) in [(60, 3), (60, 117), (3, 60), (117, 60)]:
        parts.append(f'<circle class="oa" cx="{x}" cy="{y}" r="1.4" fill="currentColor" stroke="none"/>')
    return _svg("".join(parts), label="Um olho aberto, símbolo do Mentalismo")

def _net(cx, cy, s, flip=1):
    pts = [(0, 0), (-24, 11), (22, 9), (-11, 28), (14, 27), (-34, -3), (36, 24), (2, 14)]
    edges = [(0, 1), (0, 2), (0, 7), (1, 3), (2, 4), (7, 3), (7, 4), (1, 5), (2, 6), (3, 4)]
    out = []
    P = [(cx + x * s, cy + y * s * flip) for x, y in pts]
    for a, b in edges:
        out.append(f'<line x1="{_f(P[a][0])}" y1="{_f(P[a][1])}" x2="{_f(P[b][0])}" y2="{_f(P[b][1])}"/>')
    return out, P

def correspondencia():
    # Como acima, assim abaixo: a mesma rede em duas escalas, espelhada num eixo.
    parts = ['<line class="op" x1="6" y1="60" x2="114" y2="60" stroke-width=".7" opacity=".7"/>',
             '<path class="oa" d="M60 54 L66 60 L60 66 L54 60 Z" stroke-width="1"/>']
    e1, p1 = _net(60, 12, 1.0, 1)
    e2, p2 = _net(60, 108, 0.62, -1)
    parts.append('<g class="oa" stroke-width="1.1">' + "".join(e1) + '</g>')
    parts.append('<g class="ob" stroke-width=".9">' + "".join(e2) + '</g>')
    for (x, y) in p1:
        parts.append(f'<circle class="oa" cx="{_f(x)}" cy="{_f(y)}" r="2.1" fill="currentColor" stroke="none"/>')
    for (x, y) in p2:
        parts.append(f'<circle class="ob" cx="{_f(x)}" cy="{_f(y)}" r="1.5" fill="currentColor" stroke="none"/>')
    return _svg("".join(parts), label="A mesma rede em duas escalas, espelhada")

def _wave(cycles, amp, phase, y0=60, x0=6, x1=114, n=160):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        env = math.sin(math.pi * t) ** 0.6
        y = y0 + amp * env * math.sin(2 * math.pi * cycles * t + phase)
        pts.append(f"{_f(x)} {_f(y)}")
    return "M" + " L".join(pts)

def vibracao():
    parts = ['<line class="op" x1="6" y1="60" x2="114" y2="60" stroke-width=".5" opacity=".5"/>']
    parts.append(f'<path class="op" d="{_wave(2, 14, 0)}" stroke-width=".7" opacity=".55"/>')
    parts.append(f'<path class="ob" d="{_wave(3.5, 22, 0.6)}" stroke-width="1"/>')
    parts.append(f'<path class="oa" d="{_wave(6, 30, 0)}" stroke-width="1.4"/>')
    parts.append('<circle class="oa" cx="6" cy="60" r="1.8" fill="currentColor" stroke="none"/>')
    parts.append('<circle class="oa" cx="114" cy="60" r="1.8" fill="currentColor" stroke="none"/>')
    return _svg("".join(parts), label="Ondas de frequências diferentes")

def polaridade():
    parts = ['<line class="oa" x1="22" y1="60" x2="98" y2="60" stroke-width="1.2"/>']
    for i in range(11):
        x = 22 + 76 * i / 10
        h = 5 if i in (0, 5, 10) else 3
        parts.append(f'<line class="op" x1="{_f(x)}" y1="{60-h}" x2="{_f(x)}" y2="{60+h}" stroke-width=".7" opacity=".8"/>')
    parts.append('<circle class="oa" cx="13" cy="60" r="9" fill="currentColor" stroke="none"/>')
    parts.append('<circle class="ob" cx="107" cy="60" r="9" stroke-width="1.4"/>')
    # marcador na posição 3: o passo de um grau
    mx = 22 + 76 * 0.3
    parts.append(f'<path class="oa" d="M{_f(mx)} 52 L{_f(mx-4)} 44 L{_f(mx+4)} 44 Z" fill="currentColor" stroke="none"/>')
    px = 22 + 76 * 0.4
    parts.append(f'<path class="ob" d="M{_f(px)} 68 L{_f(px-4)} 76 L{_f(px+4)} 76 Z" stroke-width="1"/>')
    return _svg("".join(parts), label="Uma linha entre dois polos")

def ritmo():
    px, py, L = 60, 14, 84
    parts = [f'<line class="op" x1="30" y1="{py}" x2="90" y2="{py}" stroke-width="1"/>',
             f'<circle class="oa" cx="{px}" cy="{py}" r="2.4" fill="currentColor" stroke="none"/>']
    # arco de oscilação
    a0, a1 = math.radians(-38), math.radians(38)
    arc = []
    for i in range(61):
        a = a0 + (a1 - a0) * i / 60
        arc.append(f"{_f(px + L*math.sin(a))} {_f(py + L*math.cos(a))}")
    parts.append('<path class="op" d="M' + " L".join(arc) + '" stroke-width=".6" stroke-dasharray="1.2 3" opacity=".7"/>')
    for ang, op in [(-28, .22), (-14, .35), (0, .5), (14, .7)]:
        a = math.radians(ang)
        x, y = px + L * math.sin(a), py + L * math.cos(a)
        parts.append(f'<circle class="ob" cx="{_f(x)}" cy="{_f(y)}" r="6" stroke-width=".9" opacity="{op}"/>')
    a = math.radians(28)
    x, y = px + L * math.sin(a), py + L * math.cos(a)
    parts.append(f'<line class="oa" x1="{px}" y1="{py}" x2="{_f(x)}" y2="{_f(y)}" stroke-width="1.1"/>')
    parts.append(f'<circle class="oa" cx="{_f(x)}" cy="{_f(y)}" r="7.5" fill="currentColor" stroke="none"/>')
    return _svg("".join(parts), label="Um pêndulo e suas posições")

def _arc(cx, cy, r, a0, a1):
    x0 = cx + r * math.cos(math.radians(a0)); y0 = cy + r * math.sin(math.radians(a0))
    x1 = cx + r * math.cos(math.radians(a1)); y1 = cy + r * math.sin(math.radians(a1))
    sweep = 1 if a1 > a0 else 0
    return f"M{_f(x0)} {_f(y0)} A{_f(r)} {_f(r)} 0 0 {sweep} {_f(x1)} {_f(y1)}"

def _chain(n, x0, cy, w, h, step, classes, widths, bg, span=15):
    """n elos horizontais entrelaçados. Em cada junção o elo da esquerda passa
    por cima no cruzamento superior e por baixo no inferior (e vice-versa)."""
    r = h / 2
    out = []
    for i in range(n):
        x = x0 + i * step
        out.append(f'<rect class="{classes[i]}" x="{_f(x)}" y="{_f(cy-r)}" width="{_f(w)}" height="{_f(h)}" '
                   f'rx="{_f(r)}" stroke-width="{widths[i]}"/>')
    for j in range(n - 1):
        cxA = x0 + j * step + w - r
        cxB = x0 + (j + 1) * step + r
        d = (cxB - cxA) / 2
        ang = math.degrees(math.atan2(math.sqrt(max(r * r - d * d, 0)), d))  # ângulo do cruzamento (inferior) no círculo A
        # topo: A por cima; base: B por cima (j par). Alterna a cada junção.
        top_over_A = (j % 2 == 0)
        for sign in (-1, +1):          # -1 = cruzamento superior, +1 = inferior
            a_over = (top_over_A and sign == -1) or ((not top_over_A) and sign == +1)
            if a_over:
                cx_, cls_, w_ = cxA, classes[j], widths[j]
                a_c = sign * ang
            else:
                cx_, cls_, w_ = cxB, classes[j + 1], widths[j + 1]
                a_c = sign * (180 - ang)
            a0, a1 = a_c - span, a_c + span
            dpath = _arc(cx_, cy, r, a0, a1)
            out.append(f'<path d="{dpath}" stroke="{bg}" stroke-width="{_f(w_ + 3.2)}" stroke-linecap="butt"/>')
            out.append(f'<path class="{cls_}" d="{dpath}" stroke-width="{w_}" stroke-linecap="butt"/>')
    return "".join(out)

def causa_efeito():
    # Três elos encadeados: cada um passa por dentro do seguinte.
    bg = "var(--orn-bg,#1B1D21)"
    parts = [_chain(3, 6, 58, 44, 26, 32, ["oa", "ob", "oa"], [1.7, 1.4, 1.7], bg)]
    parts.append('<line class="op" x1="4" y1="98" x2="116" y2="98" stroke-width=".5" opacity=".5"/>')
    parts.append('<path class="oa" d="M102 92 L112 98 L102 104" stroke-width="1"/>')
    parts.append('<circle class="oa" cx="10" cy="98" r="2.2" fill="currentColor" stroke="none"/>')
    return _svg("".join(parts), label="Três elos encadeados, da causa ao efeito")

def genero():
    parts = ['<line class="op" x1="60" y1="8" x2="60" y2="112" stroke-width=".5" opacity=".55"/>']
    parts.append('<circle class="oa" cx="44" cy="60" r="30" stroke-width="1.5"/>')
    parts.append('<circle class="ob" cx="76" cy="60" r="30" stroke-width="1.5"/>')
    # lente (interseção)
    parts.append('<path d="M60 33.5 A30 30 0 0 1 60 86.5 A30 30 0 0 1 60 33.5 Z" fill="currentColor" class="oa" stroke="none" opacity=".18"/>')
    parts.append('<path class="oa" d="M60 33.5 A30 30 0 0 1 60 86.5 A30 30 0 0 1 60 33.5 Z" stroke-width=".8"/>')
    parts.append('<circle class="oa" cx="60" cy="60" r="3.2" fill="currentColor" stroke="none"/>')
    # iniciar: seta; gestar: semente
    parts.append('<path class="oa" d="M26 60 L38 60 M33 55 L38 60 L33 65" stroke-width="1.2"/>')
    parts.append('<path class="ob" d="M88 66 Q94 54 100 60 Q94 68 88 66 Z" stroke-width="1"/>')
    return _svg("".join(parts), label="Dois círculos que se encontram")

def link_mark(cls="linkmark"):
    # Marca do Elo: dois elos entrelaçados (um passa por dentro do outro).
    bg = "var(--orn-bg,#F4EFE6)"
    inner = _chain(2, 3, 18, 40, 22, 28, ["oa", "ob"], [2.2, 2.2], bg, span=17)
    return _svg(inner, cls=cls, vb="0 0 72 36", label="")

def door(cls="doorglyph"):
    inner = ('<path class="oa" d="M8 54 L8 22 A16 16 0 0 1 40 22 L40 54" stroke-width="1.6"/>'
             '<line class="oa" x1="3" y1="54" x2="45" y2="54" stroke-width="1.6"/>'
             '<path class="ob" d="M14 54 L14 24 A10 10 0 0 1 34 24 L34 54" stroke-width="1" opacity=".8"/>'
             '<circle class="oa" cx="30" cy="40" r="1.4" fill="currentColor" stroke="none"/>')
    return _svg(inner, cls=cls, vb="0 0 48 58", label="")

ORN = {1: mentalismo, 2: correspondencia, 3: vibracao, 4: polaridade, 5: ritmo, 6: causa_efeito, 7: genero}

if __name__ == "__main__":
    # folha de prova dos ornamentos
    html = ['<!doctype html><meta charset="utf-8"><style>',
            ':root{--orn-bg:#1B1D21}body{margin:0;background:#1B1D21;display:grid;grid-template-columns:repeat(4,1fr);gap:24px;padding:24px;width:1100px}',
            '.c{aspect-ratio:1;color:#D9A94B;background:#1B1D21}.c svg{width:100%;height:100%}',
            '.oa{stroke:#D9A94B;color:#D9A94B}.ob{stroke:#A9BAC5;color:#A9BAC5}.op{stroke:#EDE6DA;color:#EDE6DA}',
            '.lm{grid-column:span 2;height:90px}.lm svg{height:100%}</style>']
    for n, fn in ORN.items():
        html.append(f'<div class="c">{fn()}</div>')
    html.append(f'<div class="c lm">{link_mark()}</div><div class="c lm">{door()}</div>')
    open("/home/claude/elo/build/ornaments_proof.html", "w").write("".join(html))
