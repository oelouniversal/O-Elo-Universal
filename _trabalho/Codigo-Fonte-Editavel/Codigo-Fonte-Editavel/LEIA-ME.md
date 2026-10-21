# Código-fonte editável — Caderno das Leis Herméticas

O livro é gerado a partir de um único arquivo de conteúdo (`src/content.json`) e de uma folha de estilo (`src/book.css`).
Para mudar texto, edite o JSON; para mudar o visual, edite o CSS; depois gere de novo.

## Requisitos
Python 3.10+, `pip install -r requirements.txt` e um Chromium para o Playwright
(`playwright install chromium`, ou aponte `CHROME` em `src/render.py` para um Chromium já instalado).

## Gerar
```
python3 src/render.py letter    # PDF Carta  -> build/caderno-letter.pdf
python3 src/render.py mobile    # PDF celular -> build/caderno-mobile.pdf
python3 src/build.py screen     # HTML responsivo -> build/book-screen.html
python3 src/export_assets.py    # ornamentos em SVG/PNG -> dist/Ativos-Graficos/
python3 src/make_guide.py       # guia de identidade -> dist/Guia-de-Identidade-Visual.pdf
```
O gerador de PDF roda duas ou três passagens para gravar no sumário, nos mapas de capítulo e no fechamento o número
real de cada página.

## Verificar
```
pandoc <manuscrito>.docx -t plain --wrap=none -o build/verify/source.txt
python3 src/verify_text.py build/caderno-letter.pdf build/caderno-mobile.pdf   # integridade do texto
python3 src/qa_pages.py build/caderno-letter.pdf letter                          # bordas, páginas vazias, margens
```

## Arte da capa
`src/make_cover.py` e `src/make_covers.py` re-renderizam a corrente (gcc + OpenMP; `chain.c` é o ray-marcher).
As imagens finais já estão em `assets/`; não é preciso recompilar para gerar o livro.

## Fontes
TeX Gyre Pagella (GUST Font License), Lora e Inter (SIL Open Font License 1.1). `fonts/pdf/` guarda as versões
TrueType em subconjunto usadas na geração; `src/make_fonts_pdf.py` as refaz a partir dos originais.
