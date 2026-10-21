# Pendências e Decisões em Aberto
## O Elo Universal: Caderno das Leis Herméticas

> Este documento registra todas as lacunas de conteúdo, decisões do proprietário do projeto e dados comerciais pendentes de confirmação antes do lançamento oficial e início do tráfego pago, conforme estipulado no **Briefing da Página (Seção 8)** e na **Estratégia de Conversão (Seção 14)**.

---

### Resumo Executivo de Prontidão

| Área | Status na Página (`site/`) | Ação Necessária do Proprietário |
|---|---|---|
| **Página de Vendas (`index.html`)** | **100% pronta e funcional** (13 seções, responsiva, zero erros) | Nenhuma alteração de código necessária; apenas atualizar `config.js` quando dados forem preenchidos. |
| **Preço e Moeda** | Preenchido: **R$ 37, pagamento único** | Confirmado. |
| **E-mail de Contato** | Preenchido: **`oelouniversal@proton.me`** | Confirmado. |
| **URL do Checkout** | `null` em `config.js` (botão rola para `#preco` e avisa em dev) | Cadastrar produto na Hotmart/Kiwify/Eduzz e inserir URL em `CONFIG.CHECKOUT_URL`. |
| **Garantia / CDC** | `null` em `config.js` (oculto na página pública) | Definir prazo real (mínimo 7 dias pelo art. 49 do CDC) e preencher `CONFIG.GARANTIA_TEXTO`. |
| **Meio de Pagamento & Entrega** | `null` em `config.js` (ocultos na página pública) | Preencher em `CONFIG.PAGAMENTO_TEXTO` e `CONFIG.ENTREGA_TEXTO` conforme plataforma. |
| **Isca Digital (Capítulo 1)** | Formulário estático com consentimento LGPD ativo; `FORM_ACTION: null` | Integrar com endpoint da ferramenta de e-mail (ActiveCampaign, Mailchimp, ConvertKit, etc.). |
| **PDF do Capítulo 1** | Amostra visual p. 5 incluída no site; arquivo PDF isolado pendente | Gerar arquivo PDF apenas com o Capítulo 1 para o entregável da isca de e-mail. |
| **Páginas Legais** | Estruturas prontas com marcadores `[PREENCHER]` | Redigir termos formais com assessoria jurídica em `privacidade.html`, `termos.html` e `reembolso.html`. |
| **Telemetria / Pixels** | Estrutura nativa completa, porém `TRACKING_ATIVO: false` | Configurar pixels/GTM apenas quando houver tráfego pago e banner de cookies LGPD aprovado. |

---

## 1. Dados Comerciais e Checkout (Briefing 8.6 e 8.8)

Conforme fonte da verdade em `Briefing/DADOS-COMERCIAIS.md`:

1. **`CHECKOUT_URL` (URL de Checkout):**
   - **Status Atual:** Vazio (`null` em `site/js/config.js`).
   - **Comportamento Atual:** O CTA do hero rola suavemente até a seção de preço (`#preco`). Em modo de desenvolvimento (`DEV_MODE: true`), ao clicar no botão da seção de preço, surge um aviso informativo. Em produção, nenhum link fictício é disparado.
   - **Ação:** Criar o produto na plataforma de pagamento escolhida e preencher o link em `CONFIG.CHECKOUT_URL`. Os parâmetros UTM serão repassados automaticamente.

2. **Garantia e Reembolso:**
   - **Status Atual:** Vazio (`null`). O elemento não é renderizado na página para evitar afirmações não confirmadas.
   - **Lembrete Jurídico:** O Código de Defesa do Consumidor (art. 49) garante 7 dias corridos de arrependimento para compras pela internet no Brasil. Se a plataforma oferecer 15 ou 30 dias, deve ser configurado em `CONFIG.GARANTIA_TEXTO`.

3. **Formas de Pagamento e Entrega:**
   - **Status Atual:** Vazio (`null`). Não renderizado na seção de preço.
   - **Ação:** Confirmar se aceitará PIX, Cartão de Crédito e Boleto, e definir o texto resumido (ex.: *"PIX ou Cartão em até 4x · Acesso imediato no e-mail"*).

---

## 2. Decisões Editoriais e de Conteúdo

1. **Contagem dos Capítulos 6 e 7 (Capítulos Bônus no Caderno):**
   - **Contexto:** No PDF e no `content.json` do caderno original, os capítulos 6 (Causa e Efeito) e 7 (Gênero) aparecem sob uma página divisora intitulada *"Capítulos Bônus"*.
   - **Decisão Adotada Provisoriamente:** Seguindo o briefing e a orientação aprovada na Fase 0, a página apresenta de forma coesa **“Sete leis, sete pistas, sete experimentos e 2 bônus externos (Mapa e Fontes e Limites)”**, sem rotular internamente os capítulos 6 e 7 como bônus para não causar estranheza ao comprador cético.
   - **Ação:** O dono do projeto deve decidir se prefere manter essa apresentação editorial ou se deseja explicitar no futuro que as duas últimas leis são bônus de aprofundamento.

2. **Fontes Científicas e DOIs:**
   - **Capítulos 2 a 7:** Todos possuem registros DOI formais validados e links clicáveis na Seção 6.
   - **Capítulo 1 (Mentalismo):** Não possui link DOI direto no material original (citações conceituais de Simons & Chabris e Nickerson). A página mantém uma nota explícita de transparência informando que apenas fontes formalmente registradas possuem link DOI.
   - **Capítulos 3 e 4:** Pistas de física básica sem referência formal no caderno.
   - **Capítulo 5:** Referência a prêmio Nobel sem URL/DOI. Por essa razão, a página utiliza a expressão precisa **"fontes citadas"** em vez de "fontes verificadas".

3. **Formatos do Caderno Digital Entregues na Oferta:**
   - **Contexto:** O caderno existe nos arquivos internos nas dimensões Carta (para leitura em tela grande ou impressão) e formato mobile.
   - **Status Atual:** O cartão da oferta indica *"O Caderno Digital em alta resolução para leitura e impressão"*.
   - **Ação:** Confirmar se o comprador receberá ambos os PDFs (Carta e Mobile) ou se também haverá versão interativa.

4. **Descrição dos Bônus A e B como Arquivos Entregáveis:**
   - **Bônus A:** O arquivo `Bônus A - Mapa das sete leis.pdf` existe na pasta do produto e confere 100% com os dados da página.
   - **Bônus B:** O documento de Fontes e Limites é derivado do conteúdo editorial. Confirmar a geração do PDF final de entrega para este bônus.

---

## 3. Isca Digital (Capítulo 1 Grátis) e Captura de E-mails

1. **Ferramenta de E-mail (`FORM_ACTION`):**
   - **Status Atual:** `null` em `CONFIG.FORM_ACTION`.
   - **Comportamento:** O formulário valida campos e conformidade LGPD no cliente. Ao tentar submeter, informa amigavelmente que o serviço de envio automatizado está em implantação, sem simular falso envio.
   - **Ação:** Escolher e configurar o serviço de e-mail marketing (ex.: ActiveCampaign, ConvertKit, Mailchimp, Brevo ou webhook n8n) e apontar o `CONFIG.FORM_ACTION` para o endpoint.

2. **Geração do PDF do Capítulo 1 Isolado:**
   - **Ação:** Gerar um arquivo PDF contendo exclusivamente a capa, introdução e o Capítulo 1 com o experimento do pensamento repetido para ser anexado ao primeiro e-mail de nutrição da sequência automática.

---

## 4. Textos Legais e Jurídicos (LGPD e CDC)

As páginas `site/privacidade.html`, `site/termos.html` e `site/reembolso.html` foram criadas com o design system oficial da marca, cabeçalho e rodapé integrados, mas **sem textos inventados**, contendo marcadores `[PREENCHER]` e `[A CONFIRMAR]`.

1. **`site/privacidade.html`:**
   - Preencher a política formal de tratamento de dados pessoais conforme a LGPD (Lei nº 13.709/2018), detalhando o uso exclusivo para envio do material solicitado e descadastro a 1 clique.
2. **`site/termos.html`:**
   - Preencher os termos de uso do produto digital: licença de uso individual e intransferível, direitos autorais e vedação de compartilhamento/pirataria.
3. **`site/reembolso.html`:**
   - Preencher a política de reembolso alinhada com as regras da plataforma de checkout e com o direito de arrependimento legal de 7 dias do CDC.

---

## 5. Identidade da Marca e Personagem Elara

1. **Transparência sobre Inteligência Artificial:**
   - **Status Atual:** Aprovada e ativada em `CONFIG.ELARA_AVISO_IA = true`.
   - **Onde aparece:** Na Seção 10 (`#quem-fala`) e no rodapé da página: *"Elara é uma personagem criada com inteligência artificial."*
2. **Foto/Arte Oficial da Elara:**
   - **Status Atual:** Utiliza o selo geométrico oficial da Marca do Elo em relevo âmbar.
   - **Ação:** Caso o proprietário deseje incluir um retrato ou ilustração oficial da Elara, basta inserir o arquivo de imagem na Seção 10.
3. **Créditos e Direitos Autorais:**
   - Conforme regra do briefing, nenhuma página de créditos externa foi criada; os direitos estão sintetizados no rodapé com a marca e o e-mail de contato.

---

## 6. Testes em Dispositivos Físicos e Navegadores Embutidos

- **Validação Local Automatizada:**
  - Telas testadas: 390 px (mobile), 820 px (tablet), 1280 px (desktop).
  - Ausência de rolagem horizontal: `scrollWidth === innerWidth` em 100% das resoluções.
- **Pendente de Teste Físico em Campo:**
  - Realizar teste prático em celulares reais (iOS e Android) dentro dos **navegadores embutidos (WebViews)** do Instagram, TikTok e Facebook via link na bio antes de alocar verba de tráfego pago.
