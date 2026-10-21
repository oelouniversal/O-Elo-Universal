# Briefing — Página de vendas
## O Elo Universal: Caderno das Leis Herméticas

> **Para o Antigravity:** leia este documento inteiro antes de escrever qualquer código. Ele define o que construir, em que ordem, com quais textos e, principalmente, **o que não pode ser inventado**. Em caso de dúvida entre "completar com algo plausível" e "deixar um marcador de pendência", escolha sempre o marcador.

---

## 0. Como trabalhar

1. **Leia tudo primeiro.** Depois proponha, em poucas linhas, a estrutura de pastas e os tokens de design, e só então construa.
2. **Não invente conteúdo.** Nomes de experimentos, durações, DOIs, descrições de bônus, prazos de garantia, formas de pagamento e textos legais **não estão neste briefing**. Onde faltar dado:
   - primeiro procure em `content.json` (ver seção 3);
   - se não achar, use o marcador `[PREENCHER: o que falta]` ou `[A CONFIRMAR: o que falta]`, visível só em modo de desenvolvimento (ex.: `<mark class="todo">`), e registre em `PENDENCIAS.md`.
3. **Construa em etapas:** (a) base, tokens e layout; (b) seções 1–5; (c) seções 6–9; (d) seções 10–13; (e) revisão contra a seção 9 deste documento.
4. **Mobile-first.** O tráfego virá de Instagram, TikTok e Facebook, quase todo em navegador embutido de celular. Projete em 390 px de largura e depois expanda.
5. **Ao terminar:** entregue um resumo curto do que foi feito e o `PENDENCIAS.md` atualizado. O build de produção deve **listar e avisar** se restar algum marcador de pendência.

---

## 1. Contexto do projeto

- **Marca:** O Elo Universal. Conteúdo e infoproduto sobre as leis herméticas, lei da atração, "física quântica" (só como analogia) e neurociência da crença e do hábito.
- **Produto:** *O Elo Universal: Caderno das Leis Herméticas*. Caderno digital com 7 capítulos (um por lei), cada um com 4 partes: **Tradição, Pista, Experimento, Registro** (mais a "Porta" do capítulo). Preço: **R$ 37, pagamento único**.
- **Subtítulo da capa:** "Sete leis. Sete pistas. Sete experimentos."
- **Frase da marca:** "As leis que conectam tudo — do universo à sua mente."
- **Público (hipótese):** adultos de 25 a 45 anos, inquietos, cansados de misticismo raso e de autoajuda de slogan. Querem rigor com mistério.
- **Posicionamento:** sofisticado, enigmático e sério. Autoridade científica com mistério.
- **Diferencial central: honestidade.** A tradição entra como **mapa**; a ciência entra como **pista ou analogia, nunca como prova**.
- **Fase atual:** tráfego orgânico (vídeos curtos → perfil → link na bio → esta página). Tráfego pago virá depois, com atenção às políticas de Meta e TikTok sobre afirmações científicas e promessas. **Por isso a página já nasce em conformidade com elas.**
- **Fluxo de conversão:** vídeo → perfil → link na bio → página → (isca: Capítulo 1 grátis) ou oferta → checkout.

---

## 2. Stack e requisitos técnicos

- **Página estática de uma só rota**, em HTML/CSS/JS simples (sem framework pesado, a menos que você justifique em uma frase). `lang="pt-BR"`.
- Peso baixo: imagens em WebP/AVIF com `width`/`height`, `loading="lazy"` abaixo da dobra, fontes autohospedadas (sem requisições externas de fonte), nada de bibliotecas grandes para animação.
- **Configuração central** (`config.js` ou equivalente) com, no mínimo:
  - `CHECKOUT_URL`, `FORM_ACTION` (ou endpoint da isca), `CONTATO_EMAIL`, `PRECO_TEXTO` ("R$ 37"),
  - `GARANTIA_TEXTO`, `PAGAMENTO_TEXTO`, `ENTREGA_TEXTO`, `REEMBOLSO_URL`, `PRIVACIDADE_URL`, `TERMOS_URL`,
  - `TRACKING_ATIVO: false`.
  - **Regra:** se um valor for `null`/vazio, o componente que o usaria **não aparece** em produção (e aparece como pendência em dev). Nunca exibir texto inventado no lugar.
- **Sem pixels/analytics por enquanto.** Deixe o gancho pronto e desligado. Se for ligado no futuro, será preciso banner de consentimento (LGPD).
- Os CTAs de compra apontam para `CHECKOUT_URL`; repasse os parâmetros UTM da URL da página, se a plataforma de checkout aceitar.
- **Acessibilidade:** HTML semântico, contraste AA, foco visível, `alt` em toda imagem informativa, respeitar `prefers-reduced-motion`, navegação por teclado completa.
- **SEO/compartilhamento:** `<title>` = "O Elo Universal: Caderno das Leis Herméticas"; meta description própria; Open Graph com imagem 1200×630 (gerar a partir da capa sem texto + título nas fontes da marca).
- Âncoras de seção: `#hero`, `#tensao`, `#ideia`, `#capitulo`, `#experimentos`, `#pista`, `#oferta`, `#capitulo-gratis`, `#preco`, `#quem-fala`, `#faq`, `#cta-final`.
- Cabeçalho mínimo: Marca do Elo + um botão discreto "Quero o caderno". Opcional: barra de CTA fixa no celular, que aparece depois do hero e some quando a seção de preço entra na tela.

---

## 3. Arquivos de entrada (devem estar na pasta do projeto)

| Arquivo / pasta | Para que serve |
|---|---|
| `Guia-de-Identidade-Visual.pdf` | **Fonte da verdade** para paleta, tipografia, ornamentos e regras. Extraia daí os tokens (cores, fontes, espaçamentos). |
| `Ativos-Graficos/` | 7 ornamentos das leis, Marca do Elo, Glifo da Porta (SVG e PNG, variantes para fundo escuro e claro) e capas **sem texto**. |
| `Codigo-Fonte-Editavel/content.json` | **Fonte do conteúdo do caderno:** títulos de seção, nomes e durações dos experimentos, textos dos quadros "O que isso sugere / O que isso NÃO mostra", fontes e DOIs. Use daqui; não reescreva. |
| `Caderno-das-Leis-Hermeticas.pdf` | Para extrair imagens de páginas reais do caderno (ex.: `pdftoppm`) e usar em mockups. |
| Foto/ilustração da Elara (opcional) | Só para a seção 10, se o dono do projeto fornecer. |

Se algum arquivo estiver ausente, **pare e avise** em vez de substituir por algo genérico.

---

## 4. Identidade, tom e linguagem

**Visual**
- Sóbrio, editorial, com mistério. Referência conceitual: o mundo "real" sóbrio do filme Matrix. Grafite, bege e dourado discreto; siga o Guia de Identidade Visual.
- **Evitar:** estética cósmica/nebulosa, roxos de galáxia, mandalas coloridas, estrelinhas, imagens de "guru", gradientes chamativos, emojis em títulos. Use "universo" em vez de "cósmico".
- Imagem principal do hero: a arte da capa (corrente de sete elos de ouro, "árvore-corrente") junto com o caderno (mockup). Use as capas sem texto de `Ativos-Graficos/`.
- Ornamentos das 7 leis servem de ícones dos cartões da seção 5.

**Voz**
- Frases curtas, seguras, sem exclamação e sem gritaria. Segunda pessoa ("você"), português do Brasil.
- Enigmático, mas claro: o leitor sempre entende o que está comprando.

**Linguagem proibida** (também por conta das políticas de anúncio futuras)
- "comprovado", "cientificamente provado", "a ciência prova", "garantido", "resultado garantido", "milagre", "cura", "transforme sua vida em X dias", "atraia dinheiro/riqueza", promessas de ganho financeiro, antes/depois.
- Não afirmar nem insinuar condição pessoal do visitante (saúde, ansiedade, dívidas, solidão etc.). Fale do **hábito de observar**, não do estado da pessoa.
- Sem escassez falsa: **nada** de contador regressivo, "últimas vagas", "oferta por tempo limitado" ou preço "de/por" falso, a menos que seja real e confirmado pelo dono do projeto.

**Linguagem encorajada**
- "observar", "pista", "analogia", "mapa", "testar", "registrar", "o que isso sugere / o que isso não mostra".
- A física quântica aparece, quando aparece, **entre aspas e como analogia**.

---

## 5. Dados do produto (fonte única)

| Campo | Valor |
|---|---|
| Nome | O Elo Universal: Caderno das Leis Herméticas |
| Subtítulo | Sete leis. Sete pistas. Sete experimentos. |
| Frase | As leis que conectam tudo — do universo à sua mente. |
| Preço | R$ 37, pagamento único |
| Leis (ordem) | 1 Mentalismo · 2 Correspondência · 3 Vibração · 4 Polaridade · 5 Ritmo · 6 Causa e Efeito · 7 Gênero |
| Partes do capítulo | Tradição · Pista · Experimento · Registro (+ Porta) |
| Bônus A | Mapa |
| Bônus B | Fontes e Limites |
| Isca | Capítulo 1 grátis (e-mail + consentimento LGPD) |
| Garantia, forma de pagamento, entrega | **[A CONFIRMAR]** conforme a plataforma de checkout |
| Contato, privacidade, termos, reembolso | **[A CONFIRMAR]** |

Atribuições históricas corretas, se citadas: "como acima, assim abaixo" vem da **Tábua de Esmeralda**; as 7 leis nesse formato foram popularizadas pelo **Kybalion (1908)**. Não atribuir a Hermes Trismegisto como fato.

---

## 6. Estrutura da página (13 seções)

Legenda: **E** = essencial · **O** = opcional. Os textos abaixo são **rascunhos editáveis**: mantenha o sentido e a honestidade; ajuste o ritmo se o layout pedir.

### 6.1 Hero — E (peso: metade do esforço)
**Objetivo:** dizer o que é e levar ao clique.
- Sobretítulo: "O Elo Universal"
- **Título (H1):** "Caderno das Leis Herméticas"
- **Subtítulo / promessa de observação:** "Sete leis, sete pistas, sete experimentos. Você não precisa acreditar em nada: precisa observar."
- **CTA principal:** "Quero o caderno" → `CHECKOUT_URL` (ou rola até `#preco`, se o checkout não estiver configurado)
- **CTA secundário:** "Ler o Capítulo 1 grátis" → `#capitulo-gratis`
- **Faixa de confiança (4 itens):** 7 leis · 7 experimentos · fontes citadas · 2 bônus
  - *Nota de honestidade:* o briefing original dizia "fontes **verificadas**". Foi trocado por "fontes **citadas**" porque nem todo capítulo traz referência formal (ver seção 8). Só reverter se o dono do projeto confirmar.
- **Visual:** arte da capa (corrente de sete elos) + mockup do caderno, sem poluir. Acima da dobra no celular: título, subtítulo, CTA principal e parte do visual.

### 6.2 A tensão — E
**Objetivo:** o público se reconhecer, sem ser rotulado.
- Rascunho: "Você já ouviu as sete leis. Em vídeos, em livros, em frases soltas. Concordou com a cabeça. E depois? A maioria das explicações termina onde deveria começar: na prática."
- Fecho: "Se uma lei descreve algo real, ela deve deixar rastros no seu dia. Rastros dá para observar, anotar e comparar."
- Mensagem-chave: para quem já conhece as leis e quer algo que dê para **testar**.

### 6.3 A ideia — E
**Objetivo:** promessa e limite, lado a lado.
- Promessa: **observação, não resultado.**
- Dois blocos curtos: **A tradição como mapa** (o que a tradição afirma) e **a ciência como pista** (o que ela sugere e o que não mostra).
- Rascunho: "Este caderno não promete resultado. Promete método: ler o que a tradição afirma, ver o que a ciência sugere (e o que ela não mostra), testar por alguns dias e registrar o que se repetiu."

### 6.4 Como funciona um capítulo — E
**Objetivo:** tangibilizar o produto.
- Os 4 blocos em sequência: **Tradição → Pista → Experimento → Registro**, cada um com uma linha explicando o papel.
- **Uma página real do caderno** ao lado (imagem extraída do PDF, de preferência do Capítulo 1; escolha uma página legível e bonita, sem cortar texto).
- Use os títulos exatos de seção que aparecem no `content.json`/PDF (ex.: "O que a tradição afirma"); não os reescreva.
- Não descreva a "Porta" além do que o manuscrito diz.

### 6.5 Os sete experimentos — E
**Objetivo:** mostrar o conteúdo.
- **Sete cartões**, um por lei: ornamento da lei, nome da lei, **nome do experimento** e **duração**.
- Dados do experimento (nome e duração em dias) vêm do **Mapa**/`content.json`:

| # | Lei | Experimento | Duração |
|---|---|---|---|
| 1 | Mentalismo | `[PREENCHER: do Mapa]` | `[PREENCHER]` |
| 2 | Correspondência | `[PREENCHER: do Mapa]` | `[PREENCHER]` |
| 3 | Vibração | `[PREENCHER: do Mapa]` | `[PREENCHER]` |
| 4 | Polaridade | `[PREENCHER: do Mapa]` | `[PREENCHER]` |
| 5 | Ritmo | `[PREENCHER: do Mapa]` | `[PREENCHER]` |
| 6 | Causa e Efeito | `[PREENCHER: do Mapa]` | `[PREENCHER]` |
| 7 | Gênero | `[PREENCHER: do Mapa]` | `[PREENCHER]` |

- Grade de 1 coluna no celular (ou carrossel horizontal com indicador), 2–4 colunas no desktop.

### 6.6 Pista, não prova — E
**Objetivo:** prova de método (mostrar o rigor, não só dizer).
- **Exemplo de uma lei em três colunas:** **Tradição · Pista · Limite.** Sugestão: **Lei 2 — Correspondência**, que tem a fonte mais sólida do caderno. **Use o texto exato do Capítulo 2 do `content.json`**; o rascunho abaixo só orienta o sentido:
  - *Tradição:* "o que está em cima é como o que está embaixo" (Tábua de Esmeralda: "como acima, assim abaixo").
  - *Pista:* um estudo-piloto comparou a rede cósmica de galáxias e a rede de neurônios e achou níveis parecidos de complexidade e auto-organização, apesar de uma diferença de escala de mais de 27 ordens de grandeza (Vazza e Feletti, *Frontiers in Physics*, 2020).
  - *Limite:* é um estudo-piloto; semelhança de estrutura não prova a lei, e a ciência não chama isso de lei.
- Abaixo, **as fontes com DOI**: liste os links DOI que existem no `content.json` (capítulos 2 a 7), como links externos (`target="_blank" rel="noopener noreferrer"`). **Não exiba DOI para o Capítulo 1** (não existe) e não afirme que todos os capítulos têm DOI.

### 6.7 O que você recebe — E
**Objetivo:** oferta clara.
- Três itens em cartões:
  1. **O caderno** — 7 capítulos, 7 experimentos, com registro. Formatos: `[A CONFIRMAR]` (existem versão Carta para impressão/tela e versão para celular; confirmar o que entra na oferta).
  2. **Bônus A — Mapa** — visão geral dos sete experimentos. `[CONFIRMAR descrição]`
  3. **Bônus B — Fontes e Limites** — as fontes e os limites de cada pista. `[CONFIRMAR descrição]`
- Não atribuir "valor" em reais aos bônus.

### 6.8 Capítulo 1 grátis — E
**Objetivo:** isca para quem ainda não está pronto para comprar.
- Título: "Leia o Capítulo 1 antes de decidir" · subtítulo curto sobre o que o leitor vai ver (Lei do Mentalismo; use só o que o `content.json` confirma).
- **Formulário:** campo de e-mail (nome opcional) + **checkbox de consentimento LGPD, desmarcado por padrão**, com texto claro de finalidade e link para a política de privacidade.
  - Rascunho do consentimento: "Concordo em receber o Capítulo 1 e e-mails do O Elo Universal. Posso cancelar quando quiser. Política de privacidade."
  - Botão: "Quero ler o Capítulo 1".
- Validação no cliente, estados de erro e sucesso acessíveis (`aria-live`).
- **Se `FORM_ACTION` não estiver configurado:** o formulário fica desativado em produção e mostra pendência em dev. **Nunca simular um envio com sucesso.**
- A entrega do capítulo (e-mail automático ou link) depende da ferramenta de e-mail, ainda **[A DEFINIR]**. Pendência extra: é preciso gerar um PDF só com o Capítulo 1.

### 6.9 Preço — E
**Objetivo:** fechar.
- Cartão único: "**R$ 37** · pagamento único". Recapitulação em 3 linhas do que está incluído.
- CTA: "Quero o caderno" → `CHECKOUT_URL`.
- Linhas de **garantia, forma de pagamento e entrega** só aparecem se configuradas (`[A CONFIRMAR]` conforme a plataforma).
- Sem preço "de/por", sem selo inventado, sem contador.
- Nota para o dono do projeto: compra online no Brasil tem direito de arrependimento de 7 dias (CDC, art. 49). Confirme a política real da plataforma antes de publicar o texto da garantia.

### 6.10 Quem fala — O
**Objetivo:** identidade, de forma poética.
- Rascunho: "O Elo Universal não é uma pessoa. É uma ideia que representa a evolução humana e fala por vozes diferentes, em momentos diferentes. Elara é a primeira."
- Pode usar a imagem da Elara (se fornecida), com legenda "Elara, primeira portadora".
- **Nunca literal:** sem "possessão", "canalização", "entidade", "extraterrestre". A marca **nunca é "Elara"**; ela é só a primeira forma. A evolução é para todos.

### 6.11 Perguntas frequentes — E
Acordeão acessível (`<details>`/`<summary>` ou equivalente). Respostas-rascunho:

- **É religião?** Não. A tradição hermética entra como mapa de leitura, não como doutrina. Não há crença a adotar nem comunidade a seguir para usar o caderno.
- **É prova científica?** Não. A ciência aparece como pista ou analogia, e cada pista vem com o que ela **não** mostra. Onde não há ciência que sustente, o caderno não finge que há.
- **Prometem resultado?** Não. A promessa é de **observação**: um experimento curto por lei, com registro do que você notou.
- **Como recebo?** `[A CONFIRMAR: conforme a plataforma de checkout]`
- **Para quem não serve?** Para quem procura promessa de resultado rápido, prova científica definitiva das leis herméticas ou uma espiritualidade festiva e cheia de slogans.

### 6.12 CTA final — E
- Resuma a oferta em 1–2 linhas e repita os dois CTAs: "Quero o caderno" e "Ler o Capítulo 1 grátis".
- Rascunho: "Sete leis. Sete experimentos. Observe, registre e veja o que se repete."
- **Sem escassez falsa.**

### 6.13 Rodapé — E
- Marca do Elo, frase da marca, contato (`CONTATO_EMAIL`), links para **Privacidade, Termos e Reembolso** (páginas separadas, **textos `[A CONFIRMAR]`**: criar as páginas com estrutura e marcador, **sem redigir texto jurídico próprio**).
- **Aviso de conteúdo educativo** (rascunho a confirmar): "Este material é educativo e de reflexão pessoal. Não promete resultados e não substitui orientação médica, psicológica ou financeira. As referências científicas são apresentadas como pistas e analogias, não como prova das leis herméticas."

---

## 7. Resumo das seções (checagem rápida)

| # | Seção | Função | Prioridade |
|---|---|---|---|
| 1 | Hero | Dizer o que é e levar ao clique | E |
| 2 | A tensão | Reconhecer o público | E |
| 3 | A ideia | Promessa e limite | E |
| 4 | Como funciona um capítulo | Tangibilizar | E |
| 5 | Os sete experimentos | Mostrar o conteúdo | E |
| 6 | Pista, não prova | Prova de método | E |
| 7 | O que você recebe | Oferta | E |
| 8 | Capítulo 1 grátis | Isca | E |
| 9 | Preço | Fechar | E |
| 10 | Quem fala | Identidade | O |
| 11 | Perguntas frequentes | Quebrar objeções | E |
| 12 | CTA final | Último convite | E |
| 13 | Rodapé | Confiança | E |

---

## 8. Lacunas conhecidas e pendências do dono do projeto

Registre todas em `PENDENCIAS.md`. **Não preencha por conta própria.**

1. **Nomes e durações dos 7 experimentos** (do Mapa) — conferir se estão no `content.json`.
2. **Descrição dos bônus** A (Mapa) e B (Fontes e Limites) e se os arquivos existem como entregáveis.
3. **Formatos do caderno** incluídos na oferta (Carta, celular, HTML).
4. **Contagem "7 experimentos" × "2 bônus":** no caderno, os capítulos 6 e 7 aparecem sob um divisor "Capítulos Bônus". Confirmar com o dono do projeto como contar isso na página para não confundir o comprador. Até lá, use "7 leis, 7 experimentos" e "2 bônus" como no briefing, **sem detalhar** quais capítulos são bônus.
5. **Fontes:** Capítulo 1 sem DOI; "pistas de física básica" dos capítulos 3 e 4 sem referência formal; item de Nobel no Capítulo 5 sem URL/DOI. Por isso a página diz "fontes citadas", não "fontes verificadas".
6. **Garantia, pagamento, entrega, checkout** (`CHECKOUT_URL`) — dependem da plataforma.
7. **Ferramenta de e-mail e endpoint do formulário** (`FORM_ACTION`); PDF só com o Capítulo 1.
8. **Contato, política de privacidade, termos, reembolso** (textos).
9. **Créditos/direitos autorais:** não existe texto; não criar página de créditos.
10. **Imagem da Elara** para a seção 10 (opcional).

---

## 9. Critérios de aceite (revisar antes de entregar)

- [ ] As 13 seções existem, na ordem do briefing, com as âncoras da seção 2.
- [ ] Nada de conteúdo inventado: tudo vem do `content.json`, deste briefing ou está marcado como pendência.
- [ ] Nenhuma palavra da lista de "linguagem proibida" aparece; nenhum contador, "últimas vagas" ou preço "de/por".
- [ ] Nenhuma afirmação de que a ciência "prova" algo; toda pista aparece com o seu limite.
- [ ] Sem rolagem horizontal em **390, 820 e 1280 px**; hero completo e CTA visível na primeira tela do celular.
- [ ] Todos os CTAs funcionam (âncoras e `CHECKOUT_URL`); links externos com `rel="noopener noreferrer"`.
- [ ] Formulário com consentimento desmarcado por padrão, validação e estados acessíveis; nada de sucesso simulado.
- [ ] Contraste AA, foco visível, `alt` nas imagens, `prefers-reduced-motion` respeitado.
- [ ] Imagens otimizadas e fontes autohospedadas; sem requisições externas desnecessárias; sem erros de console.
- [ ] Open Graph e meta description configurados; `PENDENCIAS.md` completo e o build avisa sobre marcadores restantes.
