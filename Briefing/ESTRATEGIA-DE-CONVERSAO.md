# Estratégia de conversão — Página de vendas
## O Elo Universal: Caderno das Leis Herméticas

> **Para o Antigravity:** este documento complementa o `briefing-pagina-de-vendas.md`. O briefing define **o que construir** e **o que não pode ser inventado**. Este documento define **como a página conduz o visitante à ação**, o que medir e o que testar. **Em caso de conflito, o briefing prevalece**, principalmente nas regras de honestidade, nos dados do produto e nos textos de rótulo dos botões. **Numeração:** "seção X" sem qualificação refere-se a **este documento**. As seções da página descritas no briefing (6.1 a 6.13) aparecem como "seção X do briefing", exceto nas colunas "Seção"/"Onde" das tabelas das seções 4 e 7, que usam os números 1 a 13 do briefing.

---

## 1. Objetivo e métricas

**Ação principal:** clique em "Quero o caderno" → checkout → compra (R$ 37, pagamento único).
**Ação secundária:** e-mail captado pelo "Ler o Capítulo 1 grátis" (com consentimento LGPD).

**Por que duas ações:** o público é cético por natureza (quer rigor com mistério) e chega "frio", vindo de um vídeo curto. Quem ainda não está pronto para comprar pode ler o Capítulo 1 e voltar. A página existe para servir os dois caminhos sem atrapalhar nenhum.

| Métrica | Como se define | Observação |
|---|---|---|
| Taxa de clique no CTA principal | cliques em "Quero o caderno" ÷ visitas | medida na página |
| Chegada à oferta | visitas que alcançam `#preco` ÷ visitas | mostra se a narrativa segura a leitura |
| Taxa de captação | e-mails confirmados ÷ visitas que alcançam `#capitulo-gratis` | medida no formulário |
| Taxa de compra | compras ÷ visitas | **medida na plataforma de checkout**, não na página |
| Interesse em rigor | cliques em DOI ÷ visitas | indicador qualitativo do público cético |

**Sem metas inventadas.** Não existe benchmark confiável para este nicho. As primeiras semanas servem para descobrir o ponto de partida; só depois se fixam metas.

---

## 2. Quem chega e em que estado (hipóteses a validar)

| Fator | Hipótese | Consequência para a página |
|---|---|---|
| Origem | vídeo curto de Instagram, TikTok ou Facebook, link na bio | a página precisa **ecoar a promessa do vídeo** nos primeiros segundos |
| Dispositivo | celular, em navegador embutido do app | mobile-first de verdade; peso baixo; alvos de toque grandes |
| Atenção | poucos segundos antes de decidir se fica | o hero carrega metade do trabalho |
| Mentalidade | curioso, mas desconfiado de misticismo raso | **mostrar método e limites antes de pedir fé** |
| Preço | R$ 37 é baixo; o risco percebido é de "mais do mesmo", não o de gastar | a prova é de **substância**, não de desconto |

---

## 3. Princípios: conversão honesta

A honestidade é o diferencial da marca e **também a principal alavanca de conversão** para este público. O cético confia mais em quem mostra o próprio limite.

**Alavancas permitidas**
- Clareza do que é o produto e do que o visitante vai **fazer** com ele.
- Especificidade: números reais (7 leis, 7 experimentos, durações do Mapa), páginas reais do caderno, fontes com DOI.
- Reduzir risco real: prévia gratuita (Capítulo 1), garantia **somente quando confirmada**, preço único e transparente.
- Mostrar o limite de cada pista ("o que isso NÃO mostra") como sinal de seriedade.
- Facilidade: poucos cliques, formulário curto, botões consistentes.

**Não implementar (nenhum destes, em nenhuma variante de teste)**
- Contador regressivo, "últimas vagas", "só hoje", "oferta por tempo limitado" e preço "de/por" falso.
- "N pessoas estão vendo agora", "X leitores já compraram", avaliações, estrelas ou logos de imprensa que não existam.
- **Depoimentos inventados**, de qualquer pessoa, inclusive da Elara.
- Pop-up ao abrir a página, pop-up de saída (exit-intent), "confirmshaming" ("Não, prefiro continuar sem evoluir"), botão de fechar escondido, checkbox de consentimento pré-marcado.
- Qualquer texto que sugira resultado garantido ou prova científica das leis.

**Urgência legítima (só se o dono do projeto configurar):** uma data real, com mudança real de preço ou de condição naquela data. Se existir, `OFERTA_FIM` aparece em `config`, a página mostra a data (não um contador) e **volta ao normal sozinha quando ela passa**. Se `OFERTA_FIM` estiver vazio, nada disso é renderizado.

---

## 4. A jornada na página

A ordem das seções (briefing, seção 6) segue um arco: **reconhecer → trocar o foco para a prática → prometer só o que dá para cumprir → mostrar o produto → provar o método → oferecer → dar uma saída de baixo risco → fechar → responder dúvidas → convidar de novo.**

| Seção | Trabalho que ela faz no visitante | CTA nela |
|---|---|---|
| 1 Hero | "Isso é para mim? O que é?" | primário + secundário |
| 2 A tensão | "Alguém entendeu meu problema" | nenhum |
| 3 A ideia | "A promessa é honesta e testável" | nenhum |
| 4 Como funciona um capítulo | "Dá para imaginar o que eu vou fazer" | link discreto: "Ler o Capítulo 1 grátis" |
| 5 Os sete experimentos | "Há conteúdo de verdade" | link discreto: "Ler o Capítulo 1 grátis" |
| 6 Pista, não prova | "Esse produto leva a sério a ciência" | link discreto para `#preco` |
| 7 O que você recebe | "Sei exatamente o que levo" | primário: "Quero o caderno" |
| 8 Capítulo 1 grátis | "Posso testar sem risco" | formulário |
| 9 Preço | "O valor é claro e justo" | primário: "Quero o caderno" |
| 10 Quem fala | "Há uma identidade por trás" | nenhum |
| 11 FAQ | "Minhas dúvidas foram respondidas" | link discreto após as respostas |
| 12 CTA final | "Decisão" | primário + secundário |

**Troca assumida:** a isca (seção 8 do briefing) fica **antes** do preço. Isso pode desviar parte dos compradores para a lista de e-mail, mas, na fase orgânica, um lead que lê o Capítulo 1 vale mais do que um visitante que sai. Essa ordem entra no plano de testes (T3).

---

## 5. Hero (metade do esforço)

**Teste dos 5 segundos:** quem olhar o hero por 5 segundos deve saber (1) **o que é** (um caderno sobre as leis herméticas), (2) **o que fará com ele** (observar e testar, não só ler), (3) **que é sério** (faixa de confiança) e (4) **qual é o próximo passo** (um botão claro).

**Primeira tela no celular (390 px de largura, cerca de 700 px de altura):**

```
[ Marca do Elo ]                [Quero o caderno]   (discreto)

O Elo Universal
CADERNO DAS LEIS HERMÉTICAS
Sete leis, sete pistas, sete experimentos.
Você não precisa acreditar em nada: precisa observar.

[        Quero o caderno         ]   <- botão cheio
   Ler o Capítulo 1 grátis            <- link/botão secundário

7 leis · 7 experimentos · fontes citadas · 2 bônus
[ arte da capa + mockup do caderno, começando aqui ]
```

**Regras do hero**
- Título, subtítulo e CTA principal visíveis **sem rolar**. A faixa de confiança e o início do visual também, se couber.
- Um único botão cheio (primário). O secundário tem peso visual menor.
- O visual não pode empurrar o CTA para fora da primeira tela no celular.
- Sem carrossel, vídeo com autoplay ou animação que atrase o carregamento. Uma animação sutil na corrente é aceitável **se** respeitar `prefers-reduced-motion` e não afetar o carregamento.
- Se o visitante veio de uma lei específica (seção 9 deste documento), a linha de eco aparece **abaixo** da faixa de confiança, sem substituir o título.

---

## 6. Regras de CTA

**Rótulos fixos (não variar entre seções):**
- Primário: **"Quero o caderno"**
- Secundário: **"Ler o Capítulo 1 grátis"**
- Formulário: **"Quero ler o Capítulo 1"**

Variar rótulos entre seções confunde e dilui a medição. A exceção é o teste T2 (seção 12 deste documento).

**Comportamento**
- Primário no hero e no CTA final (seção 12 do briefing) → `CHECKOUT_URL` (como no briefing). Se `CHECKOUT_URL` não estiver configurado, rola até `#preco`.
- Primário em "O que você recebe" (seção 7 do briefing) → rola até `#preco`; no preço (seção 9 do briefing) → `CHECKOUT_URL`.
- Secundário → `#capitulo-gratis`.
- O checkout abre na **mesma aba** (navegadores embutidos tratam mal pop-ups e novas janelas).

**Barra fixa no celular (opcional, recomendada)**
- Aparece só depois que o hero sai da tela. Mostra "Quero o caderno" e o preço ("R$ 37") **somente se o preço estiver em `config`**.
- Some quando `#preco` ou `#capitulo-gratis` estão visíveis, e quando o teclado do formulário está aberto.
- Altura enxuta, com margem de segurança para a barra do sistema; não pode cobrir conteúdo importante nem o rodapé.

**Microcopy perto do botão** (só o que for verdadeiro e confirmado)
- Sob o CTA do preço: "Pagamento único" (confirmado). Garantia, formas de pagamento e entrega só entram se estiverem em `config`.
- Sob o formulário: "Você pode cancelar quando quiser." (coerente com o texto de consentimento).
- Nunca "100% seguro", "sem riscos" ou similares sem base.

**Botões:** área de toque mínima de 44 × 44 px, contraste AA, estado de foco visível e estado de carregamento/desativado claro.

---

## 7. Objeções: onde cada uma é respondida

| Objeção provável | Resposta na página | Onde |
|---|---|---|
| "Isso é religião ou seita?" | A tradição entra como mapa de leitura, sem doutrina nem comunidade a seguir | 3, 11 |
| "Isso é pseudociência?" | Cada pista vem com o seu limite; fontes com DOI; a ciência é analogia, não prova | 3, 6, 11 |
| "Vale R$ 37? O que tem dentro?" | Cartões dos 7 experimentos, página real do caderno, lista do que se recebe | 4, 5, 7 |
| "Vou conseguir fazer? Quanto tempo?" | Duração de cada experimento (do Mapa) e a estrutura repetida dos capítulos | 4, 5 |
| "E se eu não gostar?" | Capítulo 1 grátis; garantia **só se confirmada** | 8, 9 |
| "Como recebo? É seguro pagar?" | Texto da plataforma de checkout `[A CONFIRMAR]` | 9, 11 |
| "Quem está por trás disso?" | O Elo Universal e a Elara como primeira portadora, de forma poética, com a transparência da seção 8 deste documento | 10, 13 |
| "Isso não promete milagre?" | A promessa é de observação, não de resultado; "para quem não serve" | 3, 11 |

---

## 8. Prova e confiança

**O que existe hoje (e deve ser bem usado)**
- **Prova de método:** exemplo da Lei 2 em três colunas, fontes com DOI (capítulos 2 a 7), limites declarados.
- **Prova de produto:** página real do caderno, capa, estrutura dos capítulos, Capítulo 1 completo.
- **Prova de postura:** a faixa "fontes citadas", o aviso educativo e "para quem não serve".

**O que não existe (e não pode ser simulado)**
- Depoimentos, número de compradores, avaliações, imprensa, selos. Deixe um componente de depoimentos **pronto e desligado** (`DEPOIMENTOS = []`: lista vazia, nada renderizado). Quando houver depoimentos reais, com **autorização por escrito** do autor, basta preencher a lista.
- Quando existirem números reais (compras, leitores), só exibir se forem verdadeiros na data e acompanhados da referência ("até [data]").

**Transparência sobre a Elara.** Elara e o visual dos vídeos são gerados com inteligência artificial. Para não levar ninguém a achar que é uma pessoa real, a página deve:
1. **Nunca** apresentar a Elara como alguém que "usou e teve resultado" nem atribuir a ela depoimentos.
2. Incluir, de forma discreta (seção 10 do briefing e rodapé), uma frase como: "Elara é uma personagem criada com inteligência artificial." Implemente como `ELARA_AVISO_IA` em `config`, **ativada por padrão**; o dono do projeto pode revisar o texto.

Meta e TikTok têm regras de rotulagem de conteúdo gerado por IA; confira as vigentes ao rodar anúncios.

---

## 9. Alinhamento com o vídeo e UTM

**Convenção de UTM** (a página lê da URL e repassa ao checkout e ao formulário, se a plataforma aceitar):

| Parâmetro | Valores | Exemplo |
|---|---|---|
| `utm_source` | `instagram`, `tiktok`, `facebook` | `instagram` |
| `utm_medium` | `organic` | `organic` |
| `utm_campaign` | `bio` (link na bio) ou `lei1` a `lei7` (link específico de um vídeo) | `lei2` |
| `utm_content` | identificador do vídeo (opcional) | `v02` |

Links específicos por vídeo só são possíveis onde a rede aceita link na legenda (ex.: Facebook). O link na bio usa `utm_campaign=bio`.

**Linha de eco (opcional, recomendada):** se `utm_campaign` for `lei1`…`lei7`, mostra abaixo da faixa de confiança do hero:
"Veio do vídeo sobre a Lei do [Nome]? Ela é o capítulo [n] do caderno." com link para o cartão correspondente em `#experimentos`.
Nomes e ordem das leis: 1 Mentalismo, 2 Correspondência, 3 Vibração, 4 Polaridade, 5 Ritmo, 6 Causa e Efeito, 7 Gênero (o capítulo tem o mesmo número da lei). Sem `utm_campaign` válido, a linha não aparece.

**Privacidade:** UTM não é dado pessoal por si só, mas, ao ser gravado junto com o e-mail do formulário, passa a compor o cadastro. Isso deve constar na política de privacidade `[A CONFIRMAR]`.

---

## 10. Mobile, navegadores embutidos e desempenho

- Teste obrigatório no **navegador embutido** de Instagram, TikTok e Facebook, em celular real, além de Safari/Chrome. Se não for possível testar, registre em `PENDENCIAS.md`.
- Evite o que navegadores embutidos tratam mal: pop-ups e `window.open`, downloads disparados por script, cópia para a área de transferência, dependência de cookies de terceiros.
- Fontes autohospedadas, imagens em WebP/AVIF com dimensões fixas (sem salto de layout).
- **Metas de desempenho** (limiares "bom" do Core Web Vitals), medidas em celular intermediário com rede 4G simulada: LCP ≤ 2,5 s · CLS ≤ 0,1 · INP ≤ 200 ms.
- **Orçamento sugerido:** imagem do hero ≤ 150 KB; HTML + CSS + JS iniciais ≤ 100 KB comprimidos. Se estourar, justifique em `PENDENCIAS.md`.
- Texto legível sem zoom (corpo ≥ 16 px), linhas curtas, espaçamento generoso. A faixa de confiança e os cartões precisam quebrar bem em 320 px.

---

## 11. Medição

**Estado atual:** `TRACKING_ATIVO: false`. A página **não** carrega scripts de terceiros. Implemente só a **estrutura**, para ligar depois sem refatorar:

- Uma função `track(evento, parametros)` que **não faz nada** quando `TRACKING_ATIVO` é falso (ou sem consentimento, quando exigido).
- Elementos rastreáveis com atributos `data-track="nome_do_evento"` e `data-track-local="secao"`.
- **Nenhum dado pessoal** (e-mail, nome) em parâmetros de evento.

| Evento | Quando dispara | Parâmetros |
|---|---|---|
| `view_secao` | seção entra 50% na tela (uma vez por visita) | `secao` (id da âncora) |
| `scroll_profundidade` | 25 / 50 / 75 / 90% da página | `percentual` |
| `clique_cta_primario` | clique em "Quero o caderno" | `local` (hero, oferta, preco, final, barra_fixa) |
| `clique_cta_secundario` | clique em "Ler o Capítulo 1 grátis" | `local` |
| `form_inicio` | primeiro foco no campo de e-mail | — |
| `form_tentativa` | tentativa de envio | `valido` (true/false) |
| `form_sucesso` / `form_erro` | resultado do envio | `codigo_erro` (sem texto livre) |
| `faq_abre` | abre uma pergunta | `pergunta` (id) |
| `clique_doi` | clique em link de fonte | `capitulo` |
| `redireciona_checkout` | saída para `CHECKOUT_URL` | `local` |

**Funil de compra:** visita → alcança `#oferta` → alcança `#preco` → `redireciona_checkout` → compra (na plataforma).
**Funil de captação:** visita → alcança `#capitulo-gratis` → `form_inicio` → `form_sucesso`.

**Enquanto o rastreamento está desligado**, os primeiros números vêm das ferramentas nativas (painel da plataforma de checkout, estatísticas de cada rede, métricas do link na bio). Registre-os manualmente em `TESTES.md`.

**Se ligar rastreamento no futuro:** pixels e cookies de anúncios exigem banner de consentimento granular (LGPD), sem opção pré-marcada, e atualização da política de privacidade. Confirme a base legal com quem cuida do jurídico do projeto.

---

## 12. Plano de testes

Com tráfego orgânico (baixo e irregular), é fácil enxergar padrão onde há só ruído. Regras do projeto:

- Testar **uma coisa por vez** e **mudanças grandes primeiro** (título, destino do CTA, ordem das seções), nunca cor de botão.
- Antes de comparar duas variantes, ter pelo menos **algumas centenas de visitas em cada**. Abaixo disso, trate o resultado como indício, não como conclusão.
- Rodar as variantes em **períodos sequenciais**, anotando em `TESTES.md`: datas, UTMs, vídeos publicados e eventos atípicos (um vídeo viral distorce a semana). Divisão aleatória na página só quando houver volume e rastreamento ligado.
- Implemente as variantes por **flag de configuração** (`VARIANTE_HERO`, `VARIANTE_CTA`, etc.), sem scripts de divisão de tráfego e sem "piscar" de conteúdo. Parâmetro `?v=b` só para revisão interna.
- Nenhuma variante pode infringir a lista "Não implementar" da seção 3.

| ID | Hipótese | A (controle) | B | Métrica principal | Prioridade |
|---|---|---|---|---|---|
| T1 | Um título que abre com a promessa de observação converte mais que o que abre com o nome do produto | H1 "Caderno das Leis Herméticas" + subtítulo atual | H1 com a ideia de observar ("Você não precisa acreditar em nada: precisa observar.") e o nome do produto como sobretítulo | clique no CTA primário | Alta |
| T2 | Rolar até o preço antes do checkout ajuda o visitante frio | Hero → `CHECKOUT_URL` | Hero → `#preco` | `redireciona_checkout` e taxa de compra | Alta |
| T3 | A isca antes do preço ajuda mais do que atrapalha | Isca (seção 8 do briefing) antes do preço (9) | Isca depois do preço | captação **e** compras, juntas | Média |
| T4 | A barra fixa no celular aumenta cliques sem irritar | Sem barra | Com barra | cliques no CTA primário e rolagem até `#preco` | Média |
| T5 | Página real do caderno no hero convence mais que a arte da capa | Capa + mockup | Página real + capa menor | cliques no CTA e `view_secao` do `#capitulo` | Baixa |

---

## 13. Depois do clique: captação e nutrição (fora do código da página)

A página termina o trabalho na captação e na saída para o checkout. A nutrição depende da ferramenta de e-mail, **ainda `[A DEFINIR]`**. Fica registrado o plano para quando ela existir.

**Na captação:** gravar origem (`origem=capitulo1`) e UTMs junto com o consentimento (data e texto exibidos), para poder comprovar o aceite.

**Sequência sugerida (só para quem consentiu; todo e-mail com link de descadastro):**

| # | Objetivo | CTA |
|---|---|---|
| 1 | Entregar o Capítulo 1 e explicar como ler | nenhum (só entrega) |
| 2 | Convidar a fazer o experimento do capítulo e registrar o que notou | nenhum |
| 3 | Mostrar o método: uma pista com o seu limite (com link para a fonte) | nenhum |
| 4 | Apresentar o caderno, o que contém, preço real e respostas às objeções | "Quero o caderno" |
| 5 | Último convite, **sem falsa urgência**, com a opção de continuar só recebendo conteúdo | "Quero o caderno" |

Os textos desses e-mails serão escritos depois. Aqui vale o princípio: e-mails 1 a 3 entregam valor antes de qualquer venda.

**Página de obrigado (opcional, só se a plataforma permitir redirecionar após a compra):** confirma a compra, explica como acessar `[A CONFIRMAR: conforme a plataforma]`, sugere começar pelo Mapa, indica o contato e convida (opt-in) a enviar um retorno. **Sem venda adicional.**

---

## 14. Decisões que dependem do dono do projeto

Registre em `PENDENCIAS.md`. Enquanto não houver resposta, siga o padrão indicado.

| Decisão | Padrão adotado até haver resposta |
|---|---|
| Frase de transparência sobre a Elara (IA) | Ativada, texto configurável (seção 8) |
| Destino do CTA do hero: checkout direto ou `#preco` | Checkout direto (como no briefing); testar em T2 |
| Quando ligar rastreamento e qual ferramenta | Desligado; estrutura pronta (seção 11) |
| Ferramenta de e-mail e entrega do Capítulo 1 | Formulário desativado em produção até configurar `FORM_ACTION` |
| Política real de garantia | Não exibir garantia |
| Existência de oferta com data real | Não exibir (`OFERTA_FIM` vazio) |
| Depoimentos reais e como coletá-los | Componente desligado |

---

## 15. Critérios de aceite de conversão

- [ ] Teste dos 5 segundos: título, subtítulo, CTA primário e faixa de confiança visíveis sem rolar em 390 px.
- [ ] Rótulos de CTA idênticos aos da seção 6 em todas as seções.
- [ ] Mapa de CTAs da seção 4 implementado; uma ação primária clara por tela.
- [ ] Barra fixa (se implementada) aparece depois do hero e some em `#preco` e `#capitulo-gratis`.
- [ ] Nada da lista "Não implementar" (seção 3) existe na página, nem escondido por CSS.
- [ ] Componentes sem conteúdo real (depoimentos, garantia, `OFERTA_FIM`) **não aparecem** em produção.
- [ ] Linha de eco por `utm_campaign` funciona para `lei1`…`lei7` e não aparece sem parâmetro válido.
- [ ] UTMs repassados ao checkout e ao formulário quando a plataforma aceitar.
- [ ] Estrutura de eventos da seção 11 pronta, **inerte** com `TRACKING_ATIVO: false`; nenhum script de terceiros carregado.
- [ ] LCP ≤ 2,5 s, CLS ≤ 0,1, INP ≤ 200 ms em teste de celular com rede 4G simulada (ou resultado registrado em `PENDENCIAS.md`).
- [ ] Testado em navegador embutido de Instagram, TikTok e Facebook (ou registrado como pendente).
- [ ] `TESTES.md` criado (vazio, com o modelo: ID, hipótese, variantes, período, UTMs, eventos atípicos, resultado, decisão).
- [ ] Frase de transparência sobre a Elara presente conforme a seção 8.
