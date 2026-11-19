#!/usr/bin/env python3
"""
Gera as duas "lentes" da seção "Pista, não prova" (Lei 2 — Correspondência).

Acima: a rede de galáxias (lente de telescópio, dourada).
Abaixo: a rede de neurônios (lente de microscópio, azul-aço).

As duas saem do MESMO algoritmo (aglomerados ligados por filamentos), só com
sementes diferentes: a semelhança visual entre elas é a ilustração do achado
de Vazza e Feletti (2020). Não são imagens científicas reais, e a página diz isso.

O SVG é inserido em site/index.html entre os marcadores:
  <!-- rede:galaxias:inicio --> ... <!-- rede:galaxias:fim -->
  <!-- rede:neuronios:inicio --> ... <!-- rede:neuronios:fim -->

Uso:  python _trabalho/gerar_redes.py
"""

import math
import pathlib
import random
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
INDEX = RAIZ / "site" / "index.html"

C, R = 100.0, 96.0  # centro e raio da lente (viewBox 0 0 200 200)


def dentro(x, y, r=R - 3):
    return (x - C) ** 2 + (y - C) ** 2 <= r * r


def rede(semente, n_aglomerados=12, espalhamento=(6.0, 10.5), fundo=46):
    rnd = random.Random(semente)

    # 1. Centros dos aglomerados (nós), afastados entre si
    centros = []
    while len(centros) < n_aglomerados:
        ang, dist = rnd.uniform(0, 2 * math.pi), R * 0.8 * math.sqrt(rnd.random())
        x, y = C + dist * math.cos(ang), C + dist * math.sin(ang)
        if all(math.hypot(x - a, y - b) > 25 for a, b in centros):
            centros.append((x, y))

    pontos, hubs, arestas = [], [], set()

    def novo(x, y):
        pontos.append((x, y))
        return len(pontos) - 1

    # 2. Pontos em torno de cada aglomerado
    grupos = []
    for (cx, cy) in centros:
        h = novo(cx, cy)
        hubs.append(h)
        grupo = [h]
        sigma = rnd.uniform(*espalhamento)
        for _ in range(rnd.randint(9, 15)):
            x, y = rnd.gauss(cx, sigma), rnd.gauss(cy, sigma)
            if dentro(x, y):
                grupo.append(novo(x, y))
        grupos.append(grupo)

    # 3. Filamentos: cada aglomerado se liga aos 2 ou 3 vizinhos mais próximos
    for i, (ax, ay) in enumerate(centros):
        viz = sorted(range(len(centros)), key=lambda j: math.hypot(centros[j][0] - ax, centros[j][1] - ay))[1:rnd.choice((3, 4))]
        for j in viz:
            bx, by = centros[j]
            passos = max(3, int(math.hypot(bx - ax, by - ay) / 7))
            anterior = hubs[i]
            for k in range(1, passos):
                t = k / passos
                x = ax + (bx - ax) * t + rnd.gauss(0, 2.2)
                y = ay + (by - ay) * t + rnd.gauss(0, 2.2)
                atual = novo(x, y)
                arestas.add(tuple(sorted((anterior, atual))))
                anterior = atual
            arestas.add(tuple(sorted((anterior, hubs[j]))))

    # 4. Poeira de fundo
    for _ in range(fundo):
        ang, dist = rnd.uniform(0, 2 * math.pi), R * math.sqrt(rnd.random())
        novo(C + dist * math.cos(ang), C + dist * math.sin(ang))

    # 5. Conexões locais: cada ponto liga aos 2 vizinhos mais próximos, se perto
    for i, (x, y) in enumerate(pontos):
        perto = sorted(((math.hypot(x - a, y - b), j) for j, (a, b) in enumerate(pontos) if j != i))[:2]
        for d, j in perto:
            if d < 15:
                arestas.add(tuple(sorted((i, j))))

    return pontos, hubs, sorted(arestas)


def svg(tipo, semente, rotulo):
    pontos, hubs, arestas = rede(semente)
    f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
    linhas = "".join(
        f'<path d="M{f(pontos[a][0])} {f(pontos[a][1])}L{f(pontos[b][0])} {f(pontos[b][1])}" pathLength="1"/>'
        for a, b in arestas
    )
    hubset = set(hubs)
    rnd = random.Random(semente + 1)
    nos = "".join(
        f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rnd.uniform(0.5, 1.15))}"/>'
        for i, (x, y) in enumerate(pontos) if i not in hubset
    )
    centros = "".join(f'<circle class="pv-hub" cx="{f(pontos[h][0])}" cy="{f(pontos[h][1])}" r="2.3"/>' for h in hubs)
    return (
        f'<svg class="pv-rede pv-rede--{tipo}" viewBox="0 0 200 200" role="img" aria-label="{rotulo}">'
        f'<defs><radialGradient id="pvFundo-{tipo}" cx="50%" cy="45%" r="60%">'
        f'<stop offset="0%" class="pv-fundo-a"/><stop offset="100%" class="pv-fundo-b"/></radialGradient>'
        f'<clipPath id="pvClip-{tipo}"><circle cx="100" cy="100" r="{f(R)}"/></clipPath>'
        f'<filter id="pvBrilho-{tipo}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.6"/></filter></defs>'
        f'<circle cx="100" cy="100" r="{f(R)}" fill="url(#pvFundo-{tipo})"/>'
        f'<g clip-path="url(#pvClip-{tipo})">'
        f'<g class="pv-linhas">{linhas}</g>'
        f'<g class="pv-nos">{nos}</g>'
        f'<g class="pv-halo" filter="url(#pvBrilho-{tipo})">{centros}</g>'
        f'<g class="pv-hubs">{centros}</g>'
        f'</g></svg>'
    )


def inserir(html, chave, conteudo):
    padrao = re.compile(rf"(<!-- rede:{chave}:inicio -->)(.*?)(<!-- rede:{chave}:fim -->)", re.S)
    if not padrao.search(html):
        raise SystemExit(f"Marcadores de rede:{chave} não encontrados em index.html")
    return padrao.sub(lambda m: m.group(1) + conteudo + m.group(3), html)


if __name__ == "__main__":
    html = INDEX.read_text(encoding="utf-8")
    html = inserir(html, "galaxias", svg("galaxias", 11, "Ilustração de uma rede de galáxias: aglomerados ligados por filamentos"))
    html = inserir(html, "neuronios", svg("neuronios", 29, "Ilustração de uma rede de neurônios: aglomerados ligados por filamentos"))
    INDEX.write_text(html, encoding="utf-8", newline="")
    print("Redes inseridas em", INDEX.relative_to(RAIZ))
