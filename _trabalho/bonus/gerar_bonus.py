#!/usr/bin/env python3
"""
Gera de novo os dois bônus do Caderno das Leis Herméticas, com texto de verdade (selecionável,
pesquisável) e links clicáveis:

  Bônus A - Mapa das sete leis.pdf      (2 páginas, A4)
  Bônus B - Fontes e Limites.pdf        (11 páginas, A4)

Por que existe: os PDFs originais foram feitos com "Microsoft Print to PDF". Viraram desenho,
sem texto, com o lado direito cortado, páginas em branco e conteúdo escorregando página abaixo.
Não havia arquivo de origem; o texto abaixo foi transcrito das páginas originais em 26/11/2026.

Trechos que estavam cortados e foram COMPLETADOS (conferir):
  [R1] Bônus B, Cap. 1: "...não viram um evento inesperado que atravessava a cena."
  [R2] Bônus B, Cap. 5: "Sustenta a existência do relógio biológico, não a ideia de pêndulo."
  [R3] Bônus A, legenda: "A frase em latim vem da Tábua de Esmeralda."
Os demais cortes eram de uma palavra e foram completados pelo texto do próprio caderno.

Uso:  python _trabalho/bonus/gerar_bonus.py
Saída: _trabalho/bonus/saida/  (os arquivos em Produto/ NÃO são tocados)
Requer: Edge ou Chrome instalado (caminho opcional em CHROME_PATH).
"""

import base64
import html
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
FONTES = RAIZ / "site" / "assets" / "fonts"
SVG = RAIZ / "site" / "assets" / "svg"
SAIDA = AQUI / "saida"

# ---------------------------------------------------------------- conteúdo

LEIS = [
    dict(
        n=1, nome="Mentalismo", orn="01-mentalismo",
        a_trad="o Todo é mente (Kybalion, 1908).",
        a_pista="a atenção filtra o que você percebe (Simons e Chabris, 1999; Nickerson, 1998).",
        a_lim="não prova que pensar cria a realidade.",
        exp="O pensamento repetido", dur="1 dia",
        b_trad="o Todo é mente (Kybalion, 1908).",
        b_cien="a atenção filtra o que percebemos, e tendemos a procurar e interpretar evidências de modo favorável ao que já acreditamos.",
        b_lim="que pensar algo faça esse algo existir.",
        tipos=[
            ("Simons e Chabris (1999)", "estudo experimental.",
             "Voluntários contavam passes de basquete num vídeo, e muitos não viram um evento inesperado que atravessava a cena. "  # [R1]
             "Mostra que o que não recebe atenção pode passar despercebido. Não fala de pensamentos moldando a realidade."),
            ("Nickerson (1998)", "revisão.",
             "Ampla, sobre viés de confirmação. Descreve uma tendência, não uma regra para todas as pessoas e situações."),
        ],
        refs=[
            ("Simons, D. J., & Chabris, C. F. (1999). Gorillas in our midst: sustained inattentional blindness for dynamic events. Perception, 28(9), 1059–1074.",
             "https://doi.org/10.1068/p281059"),
            ("Nickerson, R. S. (1998). Confirmation bias: a ubiquitous phenomenon in many guises. Review of General Psychology, 2(2), 175–220.",
             "https://doi.org/10.1037/1089-2680.2.2.175"),
        ],
    ),
    dict(
        n=2, nome="Correspondência", orn="02-correspondencia",
        a_trad="o que está embaixo é como o que está em cima (Tábua de Esmeralda).",
        a_pista="redes de neurônios e de galáxias com estrutura parecida (Vazza e Feletti, 2020).",
        a_lim="semelhança entre redes não é lei, nem diz algo sobre você.",
        exp="O gesto e o padrão", dur="3 dias",
        b_trad="o que está embaixo é como o que está em cima (Tábua de Esmeralda).",
        b_cien="a rede de neurônios do cérebro e a rede de galáxias do universo têm estruturas com algum grau de semelhança, apesar de escalas muito diferentes.",
        b_lim="que a semelhança seja uma lei da natureza, que o universo seja um cérebro ou que o seu jeito de fazer o pequeno reflita o seu jeito de fazer o grande.",
        tipos=[
            ("Vazza e Feletti (2020)", "relatório breve de pesquisa.",
             "A conectividade dos neurônios foi aproximada por proximidade, não medida conexão a conexão. "
             "Os próprios autores sugerem que princípios parecidos de organização em rede podem estar por trás dos dois sistemas."),
        ],
        refs=[
            ("Vazza, F., & Feletti, A. (2020). The quantitative comparison between the neuronal network and the cosmic web. Frontiers in Physics, 8, 525731.",
             "https://doi.org/10.3389/fphy.2020.525731"),
        ],
    ),
    dict(
        n=3, nome="Vibração", orn="03-vibracao",
        a_trad="nada está parado, tudo vibra (Kybalion).",
        a_pista="o cérebro opera em ritmos oscilatórios (Buzsáki e Draguhn, 2004).",
        a_lim="não sustenta a ideia de “vibrar alto” para atrair coisas.",
        exp="Três momentos", dur="1 dia",
        b_trad="nada está parado, tudo vibra (Kybalion, 1908).",
        b_cien="átomos e moléculas estão em movimento constante, e as redes de neurônios do córtex oscilam em ritmos de tamanhos variados.",
        b_lim="que a “oscilação neural” seja o mesmo que a “vibração” da tradição, nem que as emoções emitam uma frequência que atraia acontecimentos.",
        tipos=[
            ("Buzsáki e Draguhn (2004)", "revisão.",
             "Abre com uma pergunta ainda em aberto: as oscilações são um subproduto inevitável ou parte essencial do projeto do cérebro? "
             "Dizem que o fato de serem preservadas na evolução sugere que têm função. É um indício, não uma conclusão fechada."),
            ("Átomos e moléculas", "física básica.",
             "Que se movem é conhecimento de manual e não depende de um estudo específico."),
        ],
        refs=[
            ("Buzsáki, G., & Draguhn, A. (2004). Neuronal oscillations in cortical networks. Science, 304(5679), 1926–1929.",
             "https://doi.org/10.1126/science.1099745"),
        ],
    ),
    dict(
        n=4, nome="Polaridade", orn="04-polaridade",
        a_trad="os opostos são o mesmo, em graus diferentes (Kybalion).",
        a_pista="reavaliar uma situação pode mudar seu impacto emocional (Gross, 2002).",
        a_lim="é um mecanismo estudado, não terapia nem conversão de sentimentos.",
        exp="A escala e o passo", dur="2 dias",
        b_trad="os opostos são o mesmo em natureza e diferem em grau (Kybalion, 1908).",
        b_cien="quente e frio são graus de um mesmo fenômeno físico, e reavaliar uma situação pode alterar o impacto emocional dela.",
        b_lim="que opostos sejam idênticos em tudo, que qualquer sentimento possa ser trocado à vontade, nem que a reavaliação seja um recurso terapêutico.",
        tipos=[
            ("Gross (2002)", "revisão de estudos experimentais e de diferenças individuais.",
             "Define reavaliação como mudar a maneira de interpretar uma situação para reduzir seu impacto emocional, "
             "e conclui que costuma ser mais eficaz do que suprimir a expressão da emoção. Descreve um mecanismo. Não é uma orientação clínica."),
        ],
        refs=[
            ("Gross, J. J. (2002). Emotion regulation: affective, cognitive, and social consequences. Psychophysiology, 39(3), 281–291.",
             "https://doi.org/10.1017/s0048577201393198"),
        ],
    ),
    dict(
        n=5, nome="Ritmo", orn="05-ritmo",
        a_trad="tudo flui e reflui, como um pêndulo (Kybalion).",
        a_pista="o horário do dia afeta a atenção, e isso varia de pessoa para pessoa (Nobel 2017; Schmidt et al., 2007).",
        a_lim="o “pêndulo que compensa” é metáfora.",
        exp="O mapa da semana", dur="7 dias",
        b_trad="tudo flui e reflui, como um pêndulo, e o ritmo compensa (Kybalion, 1908).",
        b_cien="existe um relógio biológico de cerca de um dia, e o horário afeta atenção, planejamento e memória, de modo diferente de pessoa para pessoa.",
        b_lim="que todo ponto alto seja “pago” por um baixo equivalente, que exista um horário ideal para todos ou que ciclos de meses e de anos sigam o mesmo mecanismo.",
        tipos=[
            ("Prêmio Nobel de Fisiologia ou Medicina de 2017", "",
             "concedido a Jeffrey C. Hall, Michael Rosbash e Michael W. Young pela descoberta de mecanismos moleculares do ritmo circadiano. "
             "O trabalho de base foi feito em moscas-das-frutas. Sustenta a existência do relógio biológico, não a ideia de pêndulo."),  # [R2]
            ("Schmidt e colegas (2007)", "revisão.",
             "Sobre variações cognitivas ao longo do dia em pessoas saudáveis. As flutuações dependem do cronotipo, a preferência individual por manhã ou noite."),
        ],
        refs=[
            ("Schmidt, C., Collette, F., Cajochen, C., & Peigneux, P. (2007). A time to think: circadian rhythms in human cognition. Cognitive Neuropsychology, 24(7), 755–789.",
             "https://doi.org/10.1080/02643290701754158"),
            ("Nobel Assembly at Karolinska Institutet. (2017). The Nobel Prize in Physiology or Medicine 2017: Hall, Rosbash and Young.",
             "https://www.nobelprize.org/prizes/medicine/2017/summary/"),
        ],
    ),
    dict(
        n=6, nome="Causa e Efeito", orn="06-causa-e-efeito",
        a_trad="toda causa tem efeito, e o acaso é uma causa não reconhecida (Kybalion).",
        a_pista="repetir no mesmo contexto torna um comportamento automático, com grande variação entre pessoas (Lally et al., 2010).",
        a_lim="reconhecer uma causa não é se culpar, nem controlar o resultado.",
        exp="A cadeia de causas", dur="4 dias",
        b_trad="toda causa tem seu efeito, e o acaso é uma causa não reconhecida (Kybalion, 1908).",
        b_cien="repetir um comportamento no mesmo contexto tende a torná-lo automático, e duas coisas ocorrerem juntas não prova que uma cause a outra.",
        b_lim="que tudo tenha uma causa identificável e controlável, que o acaso não exista, que o resultado seja culpa da pessoa ou que mudar uma causa mude o resultado.",
        tipos=[
            ("Lally e colegas (2010)", "estudo de campo.",
             "Com 96 voluntários, dos quais 82 tinham dados suficientes. Cada um escolheu um comportamento e o repetiu diariamente por 12 semanas, "
             "registrando por conta própria o quanto ele ficava automático. O tempo até o patamar máximo variou de 18 a 254 dias, e falhar uma vez "
             "não alterou o processo de forma relevante. Os participantes escolheram seus próprios comportamentos, então o resultado não vale como regra geral."),
            ("Correlação e causa", "método.",
             "A distinção entre correlação e causa é princípio básico de método científico."),
        ],
        refs=[
            ("Lally, P., van Jaarsveld, C. H. M., Potts, H. W. W., & Wardle, J. (2010). How are habits formed: modelling habit formation in the real world. European Journal of Social Psychology, 40(6), 998–1009.",
             "https://doi.org/10.1002/ejsp.674"),
        ],
    ),
    dict(
        n=7, nome="Gênero", orn="07-genero",
        a_trad="o Gênero está em tudo (Kybalion); aqui lido como dois movimentos, iniciar e gestar.",
        a_pista="uma pausa depois de esforço real pode ajudar tarefas criativas (Sio e Ormerod, 2009).",
        a_lim="nada sobre homens, mulheres ou “energias”; esperar não substitui iniciar.",
        exp="Iniciar e gestar", dur="4 dias",
        b_trad="o Gênero está em tudo (Kybalion, 1908). O Kybalion usa os termos masculino e feminino e os aplica a todos os planos. "
               "Este caderno adota outra leitura, dois movimentos presentes em qualquer pessoa, iniciar e gestar, sem ligação com sexo ou com gênero.",
        b_cien="uma pausa depois de esforço real tende a ajudar a resolução de problemas, principalmente os criativos.",
        b_lim="nada sobre homens, mulheres ou “energias” masculina e feminina; que esperar sempre funcione; que adiar seja estratégia.",
        tipos=[
            ("Sio e Ormerod (2009)", "meta-análise.",
             "Sobre incubação, o período em que um problema é deixado de lado antes de nova tentativa. Encontrou efeito positivo, maior em pensamento "
             "divergente do que em problemas de insight verbal ou visual, maior com mais preparação prévia e menor quando a pausa é preenchida com "
             "tarefas muito exigentes. Alguns estudos não acharam efeito, e os autores dizem que o uso prático da incubação exige cuidado."),
        ],
        refs=[
            ("Sio, U. N., & Ormerod, T. C. (2009). Does incubation enhance problem solving? A meta-analytic review. Psychological Bulletin, 135(1), 94–120.",
             "https://doi.org/10.1037/a0014212"),
        ],
    ),
]

FECHAMENTO = dict(
    a_txt="Reler os sete registros e procurar o que mais se repetiu, com contraprova.",
    exp="A releitura", dur="1 sessão",
    b_cien="o mesmo filtro do Capítulo 1 age quando procuramos padrões em nossos próprios registros (Nickerson, 1998; referência completa no Capítulo 1).",
    b_lim="que o padrão encontrado seja “o” padrão da sua vida, que explique quem você é ou que não possa mudar.",
)

# ---------------------------------------------------------------- utilidades

e = html.escape


def b64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def fontes_css():
    def ff(fam, arq, peso, estilo="normal"):
        return (f"@font-face{{font-family:'{fam}';src:url(data:font/woff;base64,{b64(FONTES / arq)}) format('woff');"
                f"font-weight:{peso};font-style:{estilo};font-display:block}}")
    return "\n".join([
        ff("Pagella", "Pagella-Regular.woff", 400),
        ff("Pagella", "Pagella-Italic.woff", 400, "italic"),
        ff("Lora", "Lora-Regular.woff", 400),
        ff("Lora", "Lora-SemiBold.woff", 600),
        ff("Lora", "Lora-Italic.woff", 400, "italic"),
        ff("Inter", "Inter-Medium.woff", 500),
        ff("Inter", "Inter-SemiBold.woff", 600),
    ])


def svg_img(nome, classe=""):
    return f'<img class="{classe}" alt="" src="data:image/svg+xml;base64,{b64(SVG / nome)}">'


CSS_BASE = """
@page{size:210mm 297mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{background:#F4EFE6}
body{font-family:'Lora',Georgia,serif;color:#1E2024;font-size:10.5pt;line-height:1.5}
a{color:inherit;text-decoration:none}
.pg{width:210mm;height:297mm;position:relative;overflow:hidden;break-after:page;page-break-after:always}
.pg:last-child{break-after:auto;page-break-after:auto}
.dark{background:radial-gradient(ellipse at 50% 42%,#24272D 0%,#1B1D21 45%,#14161A 100%);color:#EDE6DA}
.light{background:#F4EFE6}
.frame{position:absolute;inset:9mm;border:.6pt solid #8E6620;pointer-events:none}
.frame::after{content:"";position:absolute;inset:1.6mm;border:.4pt solid rgba(217,169,75,.45)}
.ui{font-family:'Inter',sans-serif}
.run{position:absolute;top:13mm;left:20mm;right:20mm;display:flex;justify-content:space-between;align-items:center;
  font:500 7.5pt/1 'Inter',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#5C6168}
.folio{position:absolute;bottom:11mm;left:0;right:0;text-align:center;font:italic 9pt/1 'Pagella',serif;color:#5C6168}
"""

# ---------------------------------------------------------------- Bônus A

def arvore_svg():
    """Árvore-corrente: 7 elos de baixo para cima, o Padrão no topo, raízes embaixo."""
    cx, sp, h, w = 300, 80, 100, 62
    y1 = 700  # centro do elo 1
    partes = [
        '<defs><linearGradient id="ouro" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#F5D78E"/><stop offset=".5" stop-color="#D9A94B"/><stop offset="1" stop-color="#8E6620"/>'
        '</linearGradient></defs>',
        f'<circle cx="{cx}" cy="430" r="250" stroke="rgba(217,169,75,.16)" stroke-width="1.2" fill="none"/>',
        f'<circle cx="{cx}" cy="560" r="250" stroke="rgba(217,169,75,.12)" stroke-width="1.2" fill="none"/>',
    ]
    topo_elo7 = y1 - 6 * sp - h / 2
    # galhos
    for (x, y) in [(170, 118), (215, 80), (385, 80), (430, 118)]:
        partes.append(f'<path d="M{cx} {topo_elo7 + 8} Q {(cx + x) / 2} {topo_elo7 - 10} {x} {y}" '
                      'stroke="#8A8F96" stroke-width="2" fill="none"/>')
        partes.append(f'<circle cx="{x}" cy="{y}" r="9" stroke="#8A8F96" stroke-width="2" fill="#1B1D21"/>')
    # o Padrão
    partes.append(f'<line x1="{cx}" y1="{topo_elo7 - 34}" x2="{cx}" y2="{topo_elo7 + 4}" stroke="url(#ouro)" stroke-width="7"/>')
    partes.append(f'<circle cx="{cx}" cy="{topo_elo7 - 76}" r="42" stroke="url(#ouro)" stroke-width="7" fill="none"/>')
    partes.append(f'<circle cx="{cx}" cy="{topo_elo7 - 76}" r="42" stroke="#1B1D21" stroke-width="1.6" fill="none"/>')
    partes.append(f'<text x="{cx}" y="{topo_elo7 - 150}" text-anchor="middle" class="t-nome">O Padrão</text>')
    partes.append(f'<text x="{cx}" y="{topo_elo7 - 128}" text-anchor="middle" class="t-dur">1 sessão</text>')
    # elos (do 1 ao 7, desenhados de cima para baixo para o de baixo ficar por cima)
    for lei in reversed(LEIS):
        n = lei["n"]
        cy = y1 - (n - 1) * sp
        partes.append(f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{w / 2}" '
                      'stroke="url(#ouro)" stroke-width="8" fill="rgba(20,22,26,.85)"/>')
        partes.append(f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{w / 2}" '
                      'stroke="#14161A" stroke-width="1.6" fill="none"/>')
        partes.append(f'<text x="{cx}" y="{cy + 11}" text-anchor="middle" class="t-num">{n}</text>')
        direita = n % 2 == 1
        tx = cx + 58 if direita else cx - 58
        anc = "start" if direita else "end"
        partes.append(f'<text x="{tx}" y="{cy - 2}" text-anchor="{anc}" class="t-nome">{e(lei["nome"])}</text>')
        partes.append(f'<text x="{tx}" y="{cy + 22}" text-anchor="{anc}" class="t-dur">{e(lei["dur"])}</text>')
    # raízes
    base = y1 + h / 2 - 6
    for (x, y) in [(120, 820), (190, 852), (282, 872), (372, 858), (470, 822)]:
        partes.append(f'<path d="M{cx} {base} Q {(cx + x) / 2} {base + 40} {x} {y}" stroke="#A9BAC5" stroke-width="3" fill="none" stroke-linecap="round"/>')
    return ('<svg class="arvore" viewBox="0 0 600 890" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="Árvore-corrente: sete elos numerados de 1 a 7, de baixo para cima, com O Padrão no topo e as raízes embaixo">'
            + "".join(partes) + "</svg>")


CSS_A = """
.a1 .tit{position:absolute;top:22mm;left:0;right:0;text-align:center}
.a1 h1{font:400 27pt/1.1 'Pagella',serif;color:#EDE6DA;letter-spacing:.01em}
.a1 .sub{margin-top:3mm;font:italic 10.5pt/1.3 'Pagella',serif;color:#C3BDB0}
.a1 .arvore{position:absolute;top:44mm;left:50%;transform:translateX(-50%);width:132mm;height:auto}
.arvore .t-nome{font:400 25px 'Pagella',serif;fill:#EDE6DA}
.arvore .t-dur{font:500 15px 'Inter',sans-serif;fill:#D9A94B}
.arvore .t-num{font:400 30px 'Pagella',serif;fill:#EDE6DA}
.a1 .raizes{position:absolute;top:240mm;left:0;right:0;text-align:center;font:italic 11pt/1 'Pagella',serif;color:#A9BAC5}
.a1 .latim{position:absolute;top:251mm;left:0;right:0;text-align:center;font:italic 9.5pt/1 'Pagella',serif;color:#D9A94B}
.a1 .latim::before,.a1 .latim::after{content:"";display:inline-block;width:16mm;height:.5pt;background:#8E6620;vertical-align:middle;margin:0 4mm}
.a1 .legenda{position:absolute;top:259mm;left:24mm;right:24mm;text-align:center;font:500 7pt/1.55 'Inter',sans-serif;color:#8A8F96}
.a2 .faixa{background:#1B1D21;color:#EDE6DA;padding:11mm 20mm 6mm}
.a2 h1{font:400 24pt/1.1 'Pagella',serif}
.a2 .sub{margin-top:2mm;font:italic 10.5pt/1.3 'Pagella',serif;color:#C3BDB0}
.a2 .uso{margin-top:2mm;font:500 8pt/1.4 'Inter',sans-serif;color:#C3BDB0}
.a2 .leg{margin-top:4mm;display:flex;gap:6mm;font:500 7.5pt/1 'Inter',sans-serif;color:#C3BDB0;align-items:center}
.a2 .leg i{display:inline-block;width:2.2mm;height:2.2mm;border-radius:50%;margin-right:1.5mm;vertical-align:-.2mm}
.a2 .lista{position:relative;margin:4.5mm 20mm 0 20mm;padding-left:12mm}
.a2 .lista::before{content:"";position:absolute;left:3.6mm;top:3mm;bottom:6mm;width:.9pt;background:#D9A94B}
.a2 .item{position:relative;margin-bottom:2.3mm}
.a2 .bola{position:absolute;left:-12mm;top:-.6mm;width:7.4mm;height:7.4mm;border:1.1pt solid #B8892F;border-radius:50%;background:#F4EFE6;
  font:400 9.5pt/6.9mm 'Pagella',serif;text-align:center;color:#1E2024}
.a2 h2{font:600 11pt/1.15 'Lora',serif;margin-bottom:.6mm}
.a2 .lin{display:grid;grid-template-columns:17mm 1fr;font:400 8.2pt/1.36 'Inter',sans-serif;color:#33373D}
.a2 .lin b{font-weight:500;font-size:7.4pt;color:#5C6168}
.a2 .lin.p b{color:#3B4F5C}
.a2 .lin.l b{color:#8E6620}
.a2 .exp{margin-top:1.2mm;display:flex;justify-content:space-between;align-items:center;background:#E6DCC8;border-left:1.6pt solid #B8892F;
  padding:.9mm 3mm;font:500 8.2pt/1.3 'Inter',sans-serif}
.a2 .exp b{font-weight:500;font-size:7.4pt;color:#8E6620;margin-right:3mm}
.a2 .exp .d{color:#7A5818;font-weight:600;white-space:nowrap}
.a2 .pe{position:absolute;bottom:11mm;left:20mm;right:20mm;border-top:.6pt solid #C9BFAB;padding-top:2.5mm;display:flex;justify-content:space-between;
  gap:8mm;font:500 7pt/1.45 'Inter',sans-serif;color:#5C6168}
.a2 .pe strong{font:600 8pt/1 'Pagella',serif;color:#1E2024;white-space:nowrap}
"""


def bonus_a():
    p1 = f'''<section class="pg dark a1">
<div class="frame"></div>
<div class="tit"><h1>Mapa das 7 Leis</h1><p class="sub">Tradição como mapa. Ciência como pista. Você como teste.</p></div>
{arvore_svg()}
<p class="raizes">Raízes: Fontes e Limites</p>
<p class="latim">Quod est superius est sicut quod est inferius</p>
<p class="legenda">Árvore-corrente: sete elos, do primeiro experimento ao último, de baixo para cima, com o fechamento no topo.
As raízes são as fontes (bônus Fontes e Limites). A frase em latim vem da Tábua de Esmeralda.
Inspiração visual, sem ligação com nenhuma tradição simbólica. O detalhe de cada lei está no verso.</p>
</section>'''  # [R3] "A frase em latim"

    itens = []
    for lei in LEIS:
        itens.append(f'''<div class="item"><span class="bola">{lei["n"]}</span>
<h2>{e(lei["nome"])}</h2>
<div class="lin"><b>Tradição</b><span>{e(lei["a_trad"])}</span></div>
<div class="lin p"><b>Pista</b><span>{e(lei["a_pista"])}</span></div>
<div class="lin l"><b>Limite</b><span>{e(lei["a_lim"])}</span></div>
<div class="exp"><span><b>Experimento</b>{e(lei["exp"])}</span><span class="d">{e(lei["dur"])}</span></div>
</div>''')
    f = FECHAMENTO
    itens.append(f'''<div class="item"><span class="bola">∞</span>
<h2>Fechamento: O Padrão</h2>
<div class="lin" style="grid-template-columns:1fr"><span>{e(f["a_txt"])}</span></div>
<div class="exp"><span><b>Experimento</b>{e(f["exp"])}</span><span class="d">{e(f["dur"])}</span></div>
</div>''')
    p2 = f'''<section class="pg light a2">
<div class="faixa">
<h1>Mapa das 7 Leis</h1>
<p class="sub">Tradição como mapa. Ciência como pista. Você como teste.</p>
<p class="uso">Consulta rápida. O método completo está nos capítulos.</p>
<div class="leg"><span><i style="background:#8A8F96"></i>Tradição</span><span><i style="background:#3B4F5C"></i>Pista</span>
<span><i style="background:#B8892F"></i>Limite</span><span><i style="border:1pt solid #B8892F"></i>Experimento</span></div>
</div>
<div class="lista">{"".join(itens)}</div>
<div class="pe"><span>Pistas, não provas. Em cada capítulo, o que a tradição afirma fica separado do que a ciência sugere.
Fontes completas: bônus Fontes e Limites.</span><strong>O Elo Universal</strong></div>
</section>'''
    return documento("Mapa das 7 Leis · O Elo Universal", CSS_A, p1 + p2)


# ---------------------------------------------------------------- Bônus B

def buraco_negro_svg():
    aneis = [(190, 30, .30), (150, 24, .45), (115, 18, .6), (82, 13, .8)]
    tras = "".join(f'<path d="M{200 - rx} 170 A {rx} {ry} 0 0 1 {200 + rx} 170" stroke="rgba(169,186,197,{op})" stroke-width="2.4" fill="none"/>'
                   for rx, ry, op in aneis)
    frente = "".join(f'<path d="M{200 - rx} 170 A {rx} {ry} 0 0 0 {200 + rx} 170" stroke="rgba(169,186,197,{op})" stroke-width="2.4" fill="none"/>'
                     for rx, ry, op in aneis)
    return ('<svg class="emblema" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="Horizonte de eventos de um buraco negro, com anéis de luz em volta">'
            '<defs><linearGradient id="anel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F5D78E"/>'
            '<stop offset="1" stop-color="#8E6620"/></linearGradient></defs>'
            + tras +
            '<path d="M130 172 A 70 70 0 0 1 270 172" stroke="#A9BAC5" stroke-width="3" fill="none"/>'
            '<circle cx="200" cy="172" r="56" fill="#050608" stroke="url(#anel)" stroke-width="6"/>'
            + frente + '</svg>')


CSS_B = """
.b1 .emblema{position:absolute;top:78mm;left:50%;transform:translateX(-50%);width:150mm}
.b1 .tit{position:absolute;top:196mm;left:30mm;right:30mm;text-align:center}
.b1 h1{font:400 30pt/1.1 'Pagella',serif;color:#EDE6DA}
.b1 .sub{margin-top:4mm;font:italic 11pt/1.45 'Pagella',serif;color:#C3BDB0}
.b1 .marca{margin-top:8mm;font:600 9pt/1 'Lora',serif;letter-spacing:.06em;color:#D9A94B}
.txt{padding:32mm 22mm 0}
.txt h1{font:400 22pt/1.15 'Pagella',serif;margin-bottom:6mm}
.txt p{margin-bottom:3.5mm;max-width:150mm}
.txt .leg{margin:6mm 0 7mm;font:500 8.5pt/1 'Inter',sans-serif;color:#33373D}
.txt .leg div{display:flex;align-items:center;gap:3mm;margin-bottom:2.6mm}
.txt .leg i{display:inline-block;width:8mm;height:1.6pt}
.txt h3{font:600 9.5pt/1.3 'Inter',sans-serif;margin:4mm 0 1mm;color:#1E2024}
.txt .tipo{font:400 9pt/1.4 'Inter',sans-serif;color:#5C6168;margin-bottom:2mm}
.txt .nota{margin-top:8mm;font:italic 10pt/1.5 'Pagella',serif;color:#5C6168}
.lei{padding:30mm 20mm 0}
.lei .cab{display:flex;align-items:center;gap:5mm;margin-bottom:7mm}
.lei .num{width:11mm;height:11mm;border:1.2pt solid #B8892F;border-radius:50%;font:400 13pt/10.2mm 'Pagella',serif;text-align:center;flex:none}
.lei h1{font:400 24pt/1 'Pagella',serif;flex:1}
.lei .orn{width:17mm;height:17mm;opacity:.9}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm}
.cols.c2{grid-template-columns:repeat(2,1fr)}
.col{border-top:2.4pt solid #5C6168;padding-top:2mm;font:400 9.4pt/1.5 'Inter',sans-serif;color:#1E2024}
.col.ci{border-color:#3B4F5C}.col.li{border-color:#B8892F}
.col b{display:block;font:500 7.6pt/1.3 'Inter',sans-serif;color:#5C6168;margin-bottom:1.2mm}
.col.ci b{color:#3B4F5C}.col.li b{color:#7A5818}
.lei hr{border:0;border-top:.7pt solid #C9BFAB;margin:7mm 0 5mm}
.lei h2{font:400 12.5pt/1.2 'Pagella',serif;margin:0 0 2.5mm}
.lei .tp{font:400 9.6pt/1.55 'Lora',serif;margin-bottom:2.8mm}
.lei .tp em{color:#5C6168}
.refs{list-style:none;margin-top:6mm}
.refs li{font:400 8pt/1.5 'Inter',sans-serif;color:#33373D;margin-bottom:1.8mm;padding-left:4mm;text-indent:-4mm}
.refs a{color:#3B4F5C;text-decoration:underline;text-decoration-thickness:.4pt;white-space:nowrap}
.dots{display:flex;gap:1.2mm}
.dots i{width:2.6mm;height:2.6mm;border:.8pt solid #8E6620;border-radius:50%}
.dots i.on{background:#B8892F}
.fecho{margin-top:12mm;text-align:center;font:italic 13pt/1 'Pagella',serif;color:#33373D}
.todas h2{font:400 11pt/1.2 'Pagella',serif;margin:5mm 0 1.5mm;color:#7A5818}
"""


def cabecalho(n_ativo):
    dots = "".join(f'<i class="{"on" if i == n_ativo else ""}"></i>' for i in range(1, 8))
    return f'<div class="run"><span>Fontes e Limites</span><span class="dots" aria-hidden="true">{dots}</span><span>O Elo Universal</span></div>'


def refs_html(refs):
    return "".join(f'<li>{e(t)} <a href="{e(u)}">{e(u)}</a></li>' for t, u in refs)


def bonus_b():
    paginas = []
    paginas.append(f'''<section class="pg dark b1">
<div class="frame"></div>
{buraco_negro_svg()}
<div class="tit"><h1>Fontes e Limites</h1>
<p class="sub">O que a tradição afirma. O que a ciência sugere. O que ninguém pode concluir.</p>
<p class="marca">O Elo Universal</p></div>
</section>''')
    paginas.append('''<section class="pg light txt">
<h1>Como ler este bônus</h1>
<p>Nada neste caderno afirma que as leis herméticas foram provadas pela ciência. Em cada capítulo, a tradição aparece de um lado
e as pesquisas do outro, e a ponte entre elas é uma analogia, uma pista.</p>
<p>Sobre a tradição: os sete princípios, nesse formato, foram popularizados pelo Kybalion (1908), livro que os atribui a Hermes
Trismegisto. A tradição hermética antiga é mais variada do que esses sete princípios. A frase “o que está embaixo é como o que está
em cima” vem da Tábua de Esmeralda.</p>
<div class="leg">
<div><i style="background:#5C6168"></i>A tradição afirma</div>
<div><i style="background:#3B4F5C"></i>A ciência sugere</div>
<div><i style="background:#B8892F"></i>O que não permite concluir</div>
</div>
<p class="ui" style="font-size:9.5pt">Sobre os tipos de fonte:</p>
<h3>Estudo experimental</h3><p class="tipo">Pesquisadores testam algo com participantes.</p>
<h3>Revisão</h3><p class="tipo">Especialistas reúnem e interpretam vários estudos.</p>
<h3>Meta-análise</h3><p class="tipo">Reúne os resultados de muitos estudos num cálculo conjunto.</p>
<h3>Relatório breve</h3><p class="tipo">Pesquisa curta, com escopo limitado.</p>
<p class="nota">Na capa, o horizonte de eventos de um buraco negro é o limite do que a luz permite observar, e o brilho em volta
é a luz que chega até nós.</p>
<p class="nota" style="margin-top:3mm">Referências conferidas em outubro de 2026. Todos os links desta edição são clicáveis.</p>
<div class="folio">2</div>
</section>''')
    for lei in LEIS:
        tipos = "".join(
            f'<p class="tp"><b>{e(nome)}</b>: '
            f'{("<em>" + e(tipo) + "</em> ") if tipo else ""}{e(txt)}</p>'
            for nome, tipo, txt in lei["tipos"])
        paginas.append(f'''<section class="pg light lei">
{cabecalho(lei["n"])}
<div class="cab"><span class="num">{lei["n"]}</span><h1>{e(lei["nome"])}</h1>{svg_img(lei["orn"] + "_claro.svg", "orn")}</div>
<div class="cols">
<div class="col"><b>A tradição afirma</b>{e(lei["b_trad"])}</div>
<div class="col ci"><b>A ciência sugere</b>{e(lei["b_cien"])}</div>
<div class="col li"><b>O que não permite concluir</b>{e(lei["b_lim"])}</div>
</div>
<hr>
<h2>Tipo de fonte e limites</h2>
{tipos}
<h2 style="margin-top:6mm">Referências</h2>
<ul class="refs">{refs_html(lei["refs"])}</ul>
<div class="folio">{lei["n"] + 2}</div>
</section>''')
    f = FECHAMENTO
    paginas.append(f'''<section class="pg light lei">
{cabecalho(0)}
<div class="cab"><span class="num">∞</span><h1>Fechamento: O Padrão</h1></div>
<div class="cols c2">
<div class="col ci"><b>A ciência sugere</b>{e(f["b_cien"])}</div>
<div class="col li"><b>O que não permite concluir</b>{e(f["b_lim"])}</div>
</div>
<p class="fecho">Pistas, não provas.</p>
<div class="folio">10</div>
</section>''')
    blocos = "".join(f'<h2>{lei["n"]} · {e(lei["nome"])}</h2><ul class="refs" style="margin-top:0">{refs_html(lei["refs"])}</ul>'
                     for lei in LEIS)
    paginas.append(f'''<section class="pg light lei todas">
{cabecalho(0)}
<div class="cab"><h1>Todas as referências</h1></div>
<p class="tp">As fontes das sete leis numa lista só, na ordem dos capítulos. Cada link leva à página oficial do estudo ou do prêmio.</p>
{blocos}
<div class="folio">11</div>
</section>''')
    return documento("Fontes e Limites · O Elo Universal", CSS_B, "".join(paginas))


# ---------------------------------------------------------------- montagem

def documento(titulo, css, corpo):
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="author" content="O Elo Universal">
<title>{e(titulo)}</title>
<style>{fontes_css()}{CSS_BASE}{css}</style></head>
<body>{corpo}</body></html>'''


def navegador():
    for c in [os.environ.get("CHROME_PATH"),
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              shutil.which("google-chrome"), shutil.which("chromium")]:
        if c and os.path.exists(c):
            return c
    sys.exit("Navegador não encontrado. Defina CHROME_PATH com o caminho do Edge ou do Chrome.")


def imprimir(nav, html_txt, destino):
    with tempfile.TemporaryDirectory() as tmp:
        arq = pathlib.Path(tmp) / "doc.html"
        arq.write_text(html_txt, encoding="utf-8")
        (SAIDA / (destino.stem + ".html")).write_text(html_txt, encoding="utf-8")
        subprocess.run(
            [nav, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             f"--user-data-dir={pathlib.Path(tmp) / 'perfil'}", "--virtual-time-budget=4000",
             f"--print-to-pdf={destino}", arq.as_uri()],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)


def main():
    SAIDA.mkdir(exist_ok=True)
    nav = navegador()
    imprimir(nav, bonus_a(), SAIDA / "Bônus A - Mapa das sete leis.pdf")
    imprimir(nav, bonus_b(), SAIDA / "Bônus B - Fontes e Limites.pdf")
    for p in sorted(SAIDA.glob("*.pdf")):
        print(p.name, p.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
