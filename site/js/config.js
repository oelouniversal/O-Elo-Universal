/**
 * Configuração Central — O Elo Universal: Caderno das Leis Herméticas
 * Fonte da verdade para chaves, links comerciais e flags de comportamento.
 * Regra: se um valor for null ou vazio, o componente que o usaria não é renderizado
 * em produção e exibe marcador de pendência em modo de desenvolvimento.
 */

const CONFIG = {
  // Modo de desenvolvimento: exibe marcadores [A CONFIRMAR] e toasts de aviso
  DEV_MODE: true,

  // Dados Comerciais (Fonte: Briefing/DADOS-COMERCIAIS.md)
  NOME_PRODUTO: "O Elo Universal: Caderno das Leis Herméticas",
  PRECO_TEXTO: "R$ 37",
  PAGAMENTO_TEXTO: "pagamento único",
  CONTATO_EMAIL: "oelouniversal@proton.me",

  // Checkout (Fonte: DADOS-COMERCIAIS.md -> [A CONFIRMAR])
  // Se vazio/null: o CTA rola suavemente para #preco e exibe aviso em DEV_MODE
  CHECKOUT_URL: "",

  // Garantia, Entrega e Meios de Pagamento (Fonte: DADOS-COMERCIAIS.md -> [A CONFIRMAR])
  // Mantidos como null para NUNCA serem exibidos em produção até confirmação
  GARANTIA_TEXTO: null,
  ENTREGA_TEXTO: null,
  PAGAMENTO_FORMAS_TEXTO: null,

  // Links Legais (Páginas estruturadas com marcadores)
  PRIVACIDADE_URL: "privacidade.html",
  TERMOS_URL: "termos.html",
  REEMBOLSO_URL: "reembolso.html",

  // Isca / Captação do Capítulo 1 (Fonte: Briefing/DADOS-COMERCIAIS.md -> [A DEFINIR])
  // Se vazio/null: o formulário fica desativado em produção
  FORM_ACTION: "",

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

if (typeof module !== "undefined" && module.exports) {
  module.exports = CONFIG;
}
