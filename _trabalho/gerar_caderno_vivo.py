#!/usr/bin/env python3
"""
Gera os dados do Caderno vivo (versão do caderno para escrever no site) a partir do MESMO
arquivo de conteúdo do PDF: _trabalho/Codigo-Fonte-Editavel/Codigo-Fonte-Editavel/src/content.json.

Se o texto do caderno mudar, rode este script de novo para o Caderno vivo acompanhar.

Saída: site/data/caderno-<TOKEN>.json
O TOKEN é a parte reservada do link (o mesmo da página site/caderno-<TOKEN>.html).

Uso:  python _trabalho/gerar_caderno_vivo.py
"""
import json
import pathlib

TOKEN = "vdx9g64y1a"  # link reservado: https://o-elo-universal.vercel.app/caderno-vdx9g64y1a

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTE = RAIZ / "_trabalho" / "Codigo-Fonte-Editavel" / "Codigo-Fonte-Editavel" / "src" / "content.json"
SAIDA = RAIZ / "site" / "data" / f"caderno-{TOKEN}.json"

ORNAMENTOS = {1: "01-mentalismo", 2: "02-correspondencia", 3: "03-vibracao", 4: "04-polaridade",
              5: "05-ritmo", 6: "06-causa-e-efeito", 7: "07-genero"}

# Fechamento: o mesmo texto aprovado em 26/11/2026 e usado no PDF (build.py, método fim)
FECHAMENTO = {
    "titulo": "O que se repetiu?",
    "abertura": "Você testou sete leis, uma de cada vez. Agora é a vez de olhar para os sete registros juntos. "
                "A pergunta não é se as leis são verdadeiras. É o que se repetiu em você ao longo desses dias.",
    "experimento": {"name": "A releitura", "duration": "1 sessão", "blocks": [
        {"t": "step", "h": "Junte", "x": "Copie, uma embaixo da outra, as sete linhas “o que eu percebi” dos seus registros. Aqui elas aparecem sozinhas, logo abaixo."},
        {"t": "step", "h": "Procure", "x": "Leia as sete juntas. Anote palavras, situações ou reações que aparecem em mais de um registro."},
        {"t": "step", "h": "Nomeie", "x": "Escreva, em uma frase, o padrão que mais se repetiu."},
        {"t": "step", "h": "Contraprova", "x": "Volte aos registros e procure pelo menos um momento que não se encaixa nesse padrão. Anote."},
        {"t": "step", "h": "Conclua", "x": "Reescreva a frase do passo anterior levando em conta a contraprova."},
        {"t": "note", "x": "**Por que a contraprova.** O filtro do Capítulo 1 continua ligado: quem procura um padrão tende a encontrá-lo (Nickerson, 1998). A contraprova é o jeito de não cair nele."},
        {"t": "note", "x": "O padrão que você encontrar é uma pista sobre estes dias. Não é “o” padrão da sua vida, não explica quem você é e não é algo que você não possa mudar."},
    ]},
    "registro": [
        {"k": "area", "label": "Palavras e situações que se repetem:", "lines": 3},
        {"k": "area", "label": "O padrão, em uma frase:", "lines": 2},
        {"k": "area", "label": "A contraprova (um momento que não se encaixa):", "lines": 2},
        {"k": "area", "label": "Minha conclusão, depois da contraprova (uma linha):", "lines": 1},
    ],
    "fecho": "Pistas, não provas. A conclusão é sua, escrita a partir do que você observou.",
}


def main():
    c = json.loads(FONTE.read_text(encoding="utf-8"))
    for ch in c["chapters"]:
        ch["ornamento"] = ORNAMENTOS[ch["n"]]
        # a última linha do registro de cada capítulo é o "o que eu percebi": o fechamento a reúne
        assert "uma linha" in ch["registro"][-1].get("label", ""), ch["n"]
    dados = {"versao": 1, "meta": c["meta"], "capitulos": c["chapters"], "fechamento": FECHAMENTO}
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(dados, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(SAIDA.relative_to(RAIZ), SAIDA.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
