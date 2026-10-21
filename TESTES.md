# Registro de Testes A/B e Hipóteses
## O Elo Universal: Caderno das Leis Herméticas

> Este documento serve para registrar e acompanhar os testes controlados da página de vendas, conforme a **Estratégia de Conversão (Seção 12)**.
> 
> **Regras do Projeto:**
> 1. Testar **uma coisa por vez** e priorizar grandes mudanças editoriais/estruturais.
> 2. Rodar cada variante até acumular centenas de visitas qualificadas antes de tirar conclusões.
> 3. Anotar eventos atípicos (ex.: vídeo viral ou oscilação de tráfego) para não distorcer a análise.
> 4. Testes são ativados via flags em `site/js/config.js` sem piscar tela nem scripts lentos.

---

## Modelo de Registro de Teste (Template)

```markdown
### [ID DO TESTE] — [Nome do Teste]

- **Hipótese:** [O que se espera e por quê]
- **Variante A (Controle):** [Descrição exata da versão atual]
- **Variante B:** [Descrição exata da nova versão testada]
- **Métrica Principal:** [Métrica primária avaliada: ex. taxa de clique no CTA, compras, captação]
- **Período de Execução:** [Data de início] a [Data de término]
- **Origem / UTMs:** [Campanhas, canais ou vídeos envolvidos]
- **Amostra Total:** [Total de visitas variante A / Total de visitas variante B]
- **Eventos Atípicos / Ruídos:** [Ex.: vídeo com pico atípico de visualizações no TikTok]
- **Resultados Obtidos:**
  - Variante A: [X cliques / Y conversões — Taxa: Z%]
  - Variante B: [X cliques / Y conversões — Taxa: Z%]
- **Decisão / Conclusão:** [Adotar A, adotar B ou inconclusivo]
```

---

## Testes Pré-Configurados na Estratégia de Conversão

### T1 — Promessa de Observação no Título do Hero

- **Hipótese:** Um título que abre com a promessa de observação prática converte mais do que o que abre prioritariamente com o nome do produto.
- **Variante A (Controle):** H1 "Caderno das Leis Herméticas" + subtítulo focado na observação.
- **Variante B:** H1 com a provocação direta: *"Você não precisa acreditar em nada: precisa observar"* e o nome do produto como sobretítulo.
- **Métrica Principal:** Taxa de cliques no CTA primário ("Quero o caderno").
- **Prioridade:** Alta.
- **Status:** Planejado (Aguardando início de tráfego).
- **Período:** —
- **Resultados:** —
- **Decisão:** —

---

### T2 — Destino do CTA do Hero (Checkout Direto vs. Rolar para o Preço)

- **Hipótese:** Para um visitante frio vindo de vídeo curto, rolar até a seção `#preco` (onde há recapitulação e ancoragem) gera menos desistência e mais compras concluídas do que enviar direto para a página de checkout externa.
- **Variante A (Controle Atual):** Hero rola suavemente para `#preco`.
- **Variante B:** Hero redireciona diretamente para `CHECKOUT_URL` da plataforma de pagamento.
- **Métrica Principal:** Taxa de compras concluídas e taxa de saída para o checkout.
- **Prioridade:** Alta.
- **Status:** Planejado (Aguardando configuração de `CHECKOUT_URL`).
- **Período:** —
- **Resultados:** —
- **Decisão:** —

---

### T3 — Posição da Isca Gratuita (Antes ou Depois da Seção de Preço)

- **Hipótese:** Posicionar o Capítulo 1 grátis (Seção 8) antes da Seção de Preço (Seção 9) captura mais leads céticos que comprariam no retorno, sem prejudicar o comprador decidido.
- **Variante A (Controle Atual):** Isca (Capítulo 1 grátis) na Seção 8, antes do Preço (Seção 9).
- **Variante B:** Isca após a Seção de Preço (como alternativa para quem passou pelo preço e não comprou).
- **Métrica Principal:** Volume somado de captação de e-mails + compras diretas.
- **Prioridade:** Média.
- **Status:** Planejado.
- **Período:** —
- **Resultados:** —
- **Decisão:** —

---

### T4 — Barra Fixa de Conversão no Celular (Mobile Sticky Bar)

- **Hipótese:** A barra fixa que surge no rodapé do celular após o hero e desaparece nas seções de preço e formulário eleva a taxa de clique sem irritar o usuário.
- **Variante A (Controle Atual):** Barra fixa ativa no mobile (com preço e botão discreto).
- **Variante B:** Sem barra fixa (apenas botões de fluxo na página).
- **Métrica Principal:** Cliques no CTA primário e profundidade de rolagem até `#preco`.
- **Prioridade:** Média.
- **Status:** Implementada e configurável via `CONFIG.BARRA_FIXA_MOBILE`.
- **Período:** —
- **Resultados:** —
- **Decisão:** —

---

### T5 — Tipo de Visual no Hero (Amostra Interna Real vs. Capa Oficial com Título)

- **Hipótese:** Apresentar uma página interna real do caderno já na primeira dobra convence mais o visitante cético do que apenas a arte da capa do livro.
- **Variante A (Controle Atual):** Capa oficial do caderno em perspectiva com título nítido e relevo.
- **Variante B:** Composição mista exibindo a página 5 (amostra de leitura) em primeiro plano com a capa ao lado.
- **Métrica Principal:** Cliques no CTA e tempo de permanência na Seção 4 (`#capitulo`).
- **Prioridade:** Baixa.
- **Status:** Planejado.
- **Período:** —
- **Resultados:** —
- **Decisão:** —

---

## Log Cronológico de Testes Realizados

*(Nenhum teste executado ainda. Registre aqui as rodadas de testes à medida que as campanhas forem veiculadas.)*
