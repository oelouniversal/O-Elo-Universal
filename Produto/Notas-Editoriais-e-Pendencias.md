# Caderno das Leis Herméticas — Notas editoriais e pendências

Este documento separa três coisas: **o que foi acrescentado ao seu conteúdo** (para você aprovar ou trocar), **o que o conteúdo ainda não tem** (pendências suas) e **o que foi verificado no arquivo final**.

## 1. Acréscimos editoriais (não vieram do manuscrito)

Nenhum ensinamento, citação, resultado ou número foi criado, cortado ou resumido. Os itens abaixo são "mobília" do livro, montada a partir do documento-base e do próprio manuscrito:

| Peça | Origem | Ação sugerida |
|---|---|---|
| Capa: título "Caderno das Leis Herméticas", subtítulo "Sete leis. Sete pistas. Sete experimentos.", frase "As leis que conectam tudo — do universo à sua mente." | Montados a partir do documento-base; o nome final do produto ainda está em aberto nele | **Confirmar ou trocar o nome.** Basta editar `meta` em `content.json` e gerar de novo |
| Página "Como usar este caderno" | Descreve as quatro partes de cada capítulo (Tradição, Pista, Experimento, Registro) e a Porta, com base na estrutura que o manuscrito já repete | Ler e aprovar |
| Divisor "Capítulos Bônus" | O manuscrito marca os capítulos 6 e 7 como bônus | Aprovar |
| Página "Fechamento — O que se repetiu?" | O título e a pergunta vêm da Porta do capítulo 7, que promete um fechamento **que não foi enviado**. As cinco linhas de escrita e os links para os sete registros são só estrutura | **Enviar o texto de fechamento** ou aprovar esta página como está |
| Contracapa | Marca do Elo + frase da capa | Aprovar |
| Sumário, mapas de abertura, cabeçalhos e numeração | Navegação gerada automaticamente | — |

## 2. Pendências de conteúdo (precisam de você)

1. **Créditos, direitos autorais e contato.** Nada disso existia nos arquivos; por isso **não há página de créditos**. Se quiser uma, envie o texto (autor, ano, aviso de direitos, e-mail/site).
2. **Fonte formal das "pistas de física básica"** nos capítulos 3 (Vibração) e 4 (Polaridade): o texto afirma, mas não traz referência. Não inventei nenhuma.
3. **Capítulo 5 (Ritmo), item de Nobel nas Fontes:** sem URL/DOI. Está impresso como veio.
4. **Capítulo 1:** não traz DOI nas fontes (os capítulos 2 a 7 trazem; os 6 links estão clicáveis).
5. **Nome do produto, preço e formato de venda** seguem em aberto no documento-base.
6. **Rótulos de produção do .docx** ("(Produto) Capítulos 1 a 5 – Conteúdo", "Capítulos Bônus Capítulo 6:", "CAPÍTULO 7 —") foram tratados como etiquetas de trabalho, não como texto do livro. Se algum deles deveria aparecer, avise.

## 3. Decisões de forma (não alteram palavras)

- Títulos de seção aparecem em caixa de sentença ("O que a tradição afirma"), não em caixa-alta como no original. O texto é o mesmo.
- Os quadros "O que isso sugere:" / "O que isso NÃO mostra:" mantêm o texto original, com dois-pontos e a continuação em minúscula.
- Nenhuma palavra do manuscrito foi trocada: a conferência compara, palavra por palavra, o texto dos PDFs com o .docx (ver seção 4).
- A versão **Carta** (8,5 × 11 in) é para imprimir e para tela de computador/tablet; ao imprimir em A4, use "ajustar à página". A versão **Celular** (4,2 × 7,5 in) é um PDF próprio, com os campos de registro fluindo em sequência (61 páginas).
- A arte da capa é original, renderizada em 3D (corrente de sete elos de ouro, um por lei). Não foi usada ferramenta de imagem generativa. A imagem é entregue **sem texto** para poder ser reutilizada.

## 4. O que foi verificado no arquivo final

| Verificação | Resultado |
|---|---|
| Palavras do manuscrito presentes nos PDFs | 3.734 de 3.734 (100%) na Carta e no Celular |
| Mesma ordem do original | 98,8% (Carta) e 98,5% (Celular). O restante é só ordem de leitura em cabeçalhos de grade ("3 · O experimento · duração N dias") e nos rótulos dos passos; nenhuma palavra falta |
| Páginas | Carta 41 · Celular 61; nenhuma página em branco, sem texto fora da área útil, sem faixas brancas em páginas escuras |
| Links | 59 internos (0 quebrados) + 6 DOIs externos nos PDFs; 60 âncoras internas no HTML (0 quebradas) |
| Marcadores (índice lateral) | 48 itens, com capítulos e suas cinco partes |
| Fontes | Todas embutidas (TrueType); HTML sem nenhuma requisição externa e sem erros de console |
| Metadados | Título, autor, idioma pt-BR e PDF com tags de acessibilidade |
| Capa | 282 ppi (Carta) e 342 ppi (Celular) |
| HTML responsivo | Sem rolagem horizontal em 390, 820 e 1280 px de largura |
| Pacote editável | Extraído em pasta limpa, gerou os dois PDFs com mesmo número de páginas e texto idêntico |

**Limites:** a revisão visual foi feita sobre as páginas renderizadas, em folhas de contato e em páginas individuais. Não testei em leitores específicos de celular (iOS Livros, Kindle etc.) nem imprimi em papel.

## 5. Arquivos

| Arquivo | Uso |
|---|---|
| `Caderno-das-Leis-Hermeticas.pdf` | Produto principal (Carta), com sumário e links clicáveis |
| `Caderno-das-Leis-Hermeticas_Mobile.pdf` | Versão otimizada para celular (9:16) |
| `Caderno-das-Leis-Hermeticas.html` | Versão web responsiva, autônoma, com botão "Sumário" |
| `Guia-de-Identidade-Visual.pdf` | Paleta, tipografia, ornamentos e regras |
| `Ativos-Graficos/` | 7 ornamentos das leis + Marca do Elo + Glifo da Porta (SVG e PNG, variantes para fundo escuro e claro) e as capas sem texto |
| `Codigo-Fonte-Editavel.zip` | Conteúdo em `content.json`, estilo em `book.css` e scripts para gerar tudo de novo (instruções no `LEIA-ME.md`) |
