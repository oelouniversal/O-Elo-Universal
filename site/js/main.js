/**
 * Main Logic — O Elo Universal
 * Gerencia interações de interface, suporte a UTM, fallback de CTAs e modo dev.
 */

document.addEventListener("DOMContentLoaded", function () {
  // 0. Controle estrito de Modo de Desenvolvimento (Fase 2 / Produção)
  if (window.CONFIG && window.CONFIG.DEV_MODE === true) {
    document.body.classList.add("is-dev");
  } else {
    // Em produção: elimina do DOM qualquer bloco exclusivo de desenvolvimento
    document.querySelectorAll(".dev-only").forEach(function (el) {
      el.remove();
    });
  }

  // 1. Tratamento de UTM e Linha de Eco (Seção 9 da Estratégia)
  // A linha de eco SÓ aparece se utm_campaign for exatamente lei1..lei7
  const urlParams = new URLSearchParams(window.location.search);
  const rawUtmCampaign = urlParams.get("utm_campaign");
  const utmCampaign = rawUtmCampaign ? rawUtmCampaign.toLowerCase().trim() : null;

  const LEIS_MAP = {
    lei1: { n: 1, nome: "Mentalismo", id: "experimentos" },
    lei2: { n: 2, nome: "Correspondência", id: "experimentos" },
    lei3: { n: 3, nome: "Vibração", id: "experimentos" },
    lei4: { n: 4, nome: "Polaridade", id: "experimentos" },
    lei5: { n: 5, nome: "Ritmo", id: "experimentos" },
    lei6: { n: 6, nome: "Causa e Efeito", id: "experimentos" },
    lei7: { n: 7, nome: "Gênero", id: "experimentos" }
  };

  const echoContainer = document.getElementById("echo-line");
  if (echoContainer) {
    if (utmCampaign && LEIS_MAP[utmCampaign]) {
      const lei = LEIS_MAP[utmCampaign];
      echoContainer.innerHTML = `Veio do vídeo sobre a <strong>Lei do ${lei.nome}</strong>? Ela é o capítulo ${lei.n} do caderno. <a href="#${lei.id}">Ver experimento</a>`;
      echoContainer.style.display = "block";
    } else {
      echoContainer.style.display = "none";
      echoContainer.innerHTML = "";
    }
  }

  // 2. Comportamento do CTA Primário (Hero e CTA Final)
  const ctaCheckoutElements = document.querySelectorAll(".cta-checkout");
  ctaCheckoutElements.forEach(function (cta) {
    cta.addEventListener("click", function (e) {
      if (!CONFIG.CHECKOUT_URL || CONFIG.CHECKOUT_URL.trim() === "") {
        // Fallback: rola até a seção de preço
        e.preventDefault();
        const precoSecao = document.getElementById("preco");
        if (precoSecao) {
          precoSecao.scrollIntoView({ behavior: "smooth" });
        }

        // Exibe aviso explicativo em modo desenvolvimento
        if (CONFIG.DEV_MODE) {
          showDevToast("CHECKOUT_URL pendente: o CTA rolou para a seção #preco.");
        }
      } else {
        // Repassa parâmetros UTM se houver
        const checkoutUrl = new URL(CONFIG.CHECKOUT_URL, window.location.origin);
        ["utm_source", "utm_medium", "utm_campaign", "utm_content"].forEach(function (param) {
          if (urlParams.get(param)) {
            checkoutUrl.searchParams.set(param, urlParams.get(param));
          }
        });
        cta.href = checkoutUrl.toString();
      }
    });
  });

  // 4. Tratamento do Formulário da Isca (Seção 8 do Briefing)
  const formCapitulo = document.getElementById("form-capitulo");
  const formFeedback = document.getElementById("form-feedback");

  if (formCapitulo && formFeedback) {
    const emailInput = document.getElementById("lead-email");
    const consentInput = document.getElementById("lead-consent");

    // Rastreia primeiro foco no campo de e-mail (Seção 11 da Estratégia)
    let formIniciado = false;
    emailInput.addEventListener("focus", function () {
      if (!formIniciado) {
        formIniciado = true;
        if (window.Tracking) {
          window.Tracking.track("form_inicio", { local: "capitulo-gratis" });
        }
      }
    });

    formCapitulo.addEventListener("submit", function (e) {
      e.preventDefault();

      const emailValido = emailInput.checkValidity() && emailInput.value.includes("@");
      const consentimentoValido = consentInput.checked;

      if (!emailValido) {
        formFeedback.className = "form-status status-info";
        formFeedback.textContent = "Por favor, insira um endereço de e-mail válido.";
        emailInput.focus();
        if (window.Tracking) window.Tracking.track("form_tentativa", { valido: false });
        return;
      }

      if (!consentimentoValido) {
        formFeedback.className = "form-status status-info";
        formFeedback.textContent = "É necessário concordar com os termos de consentimento para receber o capítulo.";
        consentInput.focus();
        if (window.Tracking) window.Tracking.track("form_tentativa", { valido: false });
        return;
      }

      // Validação passou: conferir FORM_ACTION
      if (window.Tracking) window.Tracking.track("form_tentativa", { valido: true });

      if (!CONFIG.FORM_ACTION || CONFIG.FORM_ACTION.trim() === "") {
        // Regra do Briefing: NUNCA simular sucesso fictício
        formFeedback.className = "form-status status-info";
        if (CONFIG.DEV_MODE) {
          formFeedback.innerHTML = "<strong>[A DEFINIR — DEV]:</strong> FORM_ACTION não configurada no <code>config.js</code>. O formulário permanece inativo em produção para não gerar falsa expectativa.";
        } else {
          formFeedback.textContent = "O sistema de entrega automática do Capítulo 1 está em configuração. Por favor, tente novamente em breve.";
        }
      } else {
        // Envio real quando configurado
        formFeedback.className = "form-status status-info";
        formFeedback.textContent = "Enviando...";
        // Implementação de POST com repasse de UTM
      }
    });
  }

  // 5. Barra Fixa Mobile (Seção 6 da Estratégia)
  const stickyBar = document.getElementById("mobile-sticky-bar");
  const heroSection = document.getElementById("hero");
  const precoSection = document.getElementById("preco");
  const formSection = document.getElementById("capitulo-gratis");

  if (stickyBar && heroSection && "IntersectionObserver" in window) {
    let heroVisible = true;
    let precoVisible = false;
    let formVisible = false;

    function updateStickyVisibility() {
      // Aparece após o hero sair, some no preço ou no formulário
      if (!heroVisible && !precoVisible && !formVisible) {
        stickyBar.classList.add("visible");
        stickyBar.setAttribute("aria-hidden", "false");
      } else {
        stickyBar.classList.remove("visible");
        stickyBar.setAttribute("aria-hidden", "true");
      }
    }

    const visibilityObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.target.id === "hero") heroVisible = entry.isIntersecting;
        if (entry.target.id === "preco") precoVisible = entry.isIntersecting;
        if (entry.target.id === "capitulo-gratis") formVisible = entry.isIntersecting;
      });
      updateStickyVisibility();
    }, { threshold: 0 });

    visibilityObserver.observe(heroSection);
    if (precoSection) visibilityObserver.observe(precoSection);
    if (formSection) visibilityObserver.observe(formSection);
  }

  // 6. Rastreamento de Abertura do FAQ (Seção 11 da Estratégia)
  const faqItems = document.querySelectorAll(".faq-item");
  faqItems.forEach(function (faq) {
    faq.addEventListener("toggle", function () {
      if (faq.open && window.Tracking) {
        const perguntaId = faq.getAttribute("data-faq-id") || "faq";
        window.Tracking.track("faq_abre", { pergunta: perguntaId });
      }
    });
  });

  // 7. Sistema de Toast para Modo de Desenvolvimento
  function showDevToast(mensagem) {
    let toast = document.getElementById("dev-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "dev-toast";
      toast.className = "dev-toast dev-only";
      document.body.appendChild(toast);
    }
    toast.textContent = `[DEV]: ${mensagem}`;
    toast.style.display = "block";
    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(function () {
      toast.style.display = "none";
    }, 4500);
  }
});
