/**
 * Configuração Central — O Elo Universal: Caderno das Leis Herméticas
 * Fonte da verdade para chaves, links comerciais e flags de comportamento.
 * Regra: se um valor for null ou vazio, o componente que o usaria não é renderizado
 * em produção e exibe marcador de pendência em modo de desenvolvimento.
 */

const CONFIG = {
  // Modo de desenvolvimento: exibe marcadores [A CONFIRMAR] e toasts de aviso.
  // Liga sozinho só em ambiente local (localhost, 127.0.0.1 ou arquivo aberto direto);
  // no site publicado fica sempre desligado. Para revisar pendências online, use ?dev=1.
  DEV_MODE: (function () {
    if (typeof window === "undefined" || !window.location) return false;
    var host = window.location.hostname;
    var local = host === "localhost" || host === "127.0.0.1" || host === "" || window.location.protocol === "file:";
    var forcado = /[?&]dev=1(&|$)/.test(window.location.search);
    return local || forcado;
  })(),

  // Dados Comerciais (Fonte: Briefing/DADOS-COMERCIAIS.md)
  NOME_PRODUTO: "O Elo Universal: Caderno das Leis Herméticas",
  PRECO_TEXTO: "R$ 37",
  PAGAMENTO_TEXTO: "pagamento único",
  CONTATO_EMAIL: "oelouniversal@proton.me",

  // Checkout (Fonte: DADOS-COMERCIAIS.md -> Confirmado na Wiven)
  // Se vazio/null: o CTA rola suavemente para #preco e exibe aviso em DEV_MODE
  CHECKOUT_URL: "https://checkout.wiven.com.br/checkout/cmwgi7hp1004901pwfzy4sq1q?offer=3V9KZ68",

  // Garantia, Entrega e Meios de Pagamento (Fonte: DADOS-COMERCIAIS.md -> [A CONFIRMAR])
  // Mantidos como null para NUNCA serem exibidos em produção até confirmação
  GARANTIA_TEXTO: null,
  ENTREGA_TEXTO: null,
  PAGAMENTO_FORMAS_TEXTO: null,

  // Links Legais (Páginas estruturadas com marcadores)
  PRIVACIDADE_URL: "privacidade.html",
  TERMOS_URL: "termos.html",
  REEMBOLSO_URL: "reembolso.html",

  // Isca / Captação do Capítulo 1 (Integrado via FormSubmit AJAX para oelouniversal@proton.me)
  // Se vazio/null: o formulário fica desativado em produção
  FORM_ACTION: "https://formsubmit.co/ajax/oelouniversal@proton.me",

  // Transparência sobre a Elara (Seção 8 da Estratégia de Conversão)
  ELARA_AVISO_IA: true,
  ELARA_TEXTO_IA: "Elara é uma personagem criada com inteligência artificial.",

  // Depoimentos Reais (Vazio até haver depoimentos com autorização por escrito)
  DEPOIMENTOS: [],

  // Urgência Legítima (Nula: proibida qualquer escassez falsa)
  OFERTA_FIM: null,

  // Telemetria inerte (Sem pixels nem scripts de terceiros)
  TRACKING_ATIVO: false,

  // Variantes de teste (Seção 12 da Estratégia de Conversão)
  VARIANTE_HERO: "A", // "A": controle (H1 Caderno...) | "B": promessa de observação
  VARIANTE_CTA: "A",  // "A": Hero -> CHECKOUT_URL (ou #preco se vazio) | "B": Hero -> #preco
  VARIANTE_BARRA_FIXA: true
};

// `const` no escopo global não vira propriedade de window; os outros scripts leem window.CONFIG.
if (typeof window !== "undefined") {
  window.CONFIG = CONFIG;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = CONFIG;
}
