/**
 * Main Logic — O Elo Universal
 * Gerencia interações de interface, suporte a UTM, fallback de CTAs e modo dev.
 */

document.addEventListener("DOMContentLoaded", function () {
  // Ativa a classe de controle de Scroll Trigger apenas quando o JS carregar com sucesso
  document.documentElement.classList.add("reveal-ready");

  // 0. Controle estrito de Modo de Desenvolvimento (Fase 2 / Produção)
  if (window.CONFIG && window.CONFIG.DEV_MODE === true) {
    document.body.classList.add("is-dev");
  } else {
    // Em produção: elimina do DOM qualquer bloco exclusivo de desenvolvimento
    document.querySelectorAll(".dev-only").forEach(function (el) {
      el.remove();
    });
  }

  // Scroll Trigger — Revelações Iniciáticas Aceleradas por Hardware (60 FPS)
  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
      function (entries, observer) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target); // Libera o observador após a revelação
          }
        });
      },
      {
        root: null,
        rootMargin: "0px 0px -6% 0px",
        threshold: 0.08
      }
    );

    document.querySelectorAll(".reveal-trigger").forEach(function (el) {
      revealObserver.observe(el);
    });
  } else {
    document.querySelectorAll(".reveal-trigger").forEach(function (el) {
      el.classList.add("is-visible");
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

  // 3. Suporte universal a rolagem suave para links de âncoras internas (#secao)
  // Garante funcionamento confiável e responsivo no mobile (iOS/Android/Safari/Chrome)
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (!targetId || targetId === "#") return;

      // Se for CTA primário de checkout, o bloco anterior já gerencia
      if (this.classList.contains("cta-checkout")) return;

      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({ behavior: "smooth", block: "start" });
        if (window.history && window.history.pushState) {
          window.history.pushState(null, null, targetId);
        }
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
  const ctaFinalSection = document.getElementById("cta-final");

  if (stickyBar && heroSection && "IntersectionObserver" in window) {
    let heroVisible = true;
    let precoVisible = false;
    let formVisible = false;
    let ctaFinalVisible = false;

    function updateStickyVisibility() {
      // Aparece após o hero sair, some no preço, no formulário ou no CTA final
      if (!heroVisible && !precoVisible && !formVisible && !ctaFinalVisible) {
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
        if (entry.target.id === "cta-final") ctaFinalVisible = entry.isIntersecting;
      });
      updateStickyVisibility();
    }, { threshold: 0 });

    visibilityObserver.observe(heroSection);
    if (precoSection) visibilityObserver.observe(precoSection);
    if (formSection) visibilityObserver.observe(formSection);
    if (ctaFinalSection) visibilityObserver.observe(ctaFinalSection);
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

  // 8. Scroll-Linked: Barra de Progresso Áurea (Fallback com requestAnimationFrame 60 FPS)
  const progressBar = document.getElementById("scroll-progress-bar");
  const supportsScrollTimeline =
    window.CSS &&
    window.CSS.supports &&
    (CSS.supports("animation-timeline", "scroll()") || CSS.supports("animation-timeline: scroll()"));

  if (progressBar && !supportsScrollTimeline) {
    let ticking = false;

    function updateProgressBar() {
      const scrollTop = window.scrollY || document.documentElement.scrollTop || 0;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? Math.min(Math.max(scrollTop / docHeight, 0), 1) : 0;
      progressBar.style.transform = `scaleX(${progress})`;
      ticking = false;
    }

    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          window.requestAnimationFrame(updateProgressBar);
          ticking = true;
        }
      },
      { passive: true }
    );

    window.addEventListener("resize", updateProgressBar, { passive: true });
    updateProgressBar();
  }

  // 9. Parallax & Profundidade: Interatividade 3D, Spotlight Alquímico e Fallbacks 60 FPS
  const prefersReduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!prefersReduced) {
    // 9.1 Parallax 3D Interativo no Mockup do Livro (Desktop com Pointer e Mobile com Touch/Giroscópio)
    const bookWrapper = document.querySelector(".book-mockup-wrapper");
    const bookMockup = document.querySelector(".book-mockup");

    if (bookWrapper && bookMockup) {
      if (window.matchMedia("(hover: hover)").matches) {
        bookWrapper.addEventListener("mousemove", function (e) {
          const rect = bookWrapper.getBoundingClientRect();
          const x = (e.clientX - rect.left) / rect.width - 0.5;
          const y = (e.clientY - rect.top) / rect.height - 0.5;
          bookMockup.style.transition = "transform 0.08s ease-out";
          bookMockup.style.transform = `perspective(1000px) rotateY(${x * 14}deg) rotateX(${-y * 12}deg) translateY(-4px)`;
        });

        bookWrapper.addEventListener("mouseleave", function () {
          bookMockup.style.transition = "transform 0.45s cubic-bezier(0.2, 0.8, 0.2, 1)";
          bookMockup.style.transform = "";
        });
      } else {
        // Mobile: Interação ao toque com amortecimento
        bookWrapper.addEventListener("touchstart", function () {
          bookMockup.style.transition = "transform 0.25s ease-out";
          bookMockup.style.transform = "perspective(1000px) rotateY(-4deg) rotateX(4deg) translateY(-6px) scale(1.02)";
        }, { passive: true });

        bookWrapper.addEventListener("touchend", function () {
          bookMockup.style.transition = "transform 0.45s cubic-bezier(0.2, 0.8, 0.2, 1)";
          bookMockup.style.transform = "";
        }, { passive: true });

        // Giroscópio sutil em smartphones sem permissão invasiva (Android/Web API)
        if (window.DeviceOrientationEvent && typeof DeviceOrientationEvent.requestPermission !== "function") {
          let gyroTicking = false;
          window.addEventListener("deviceorientation", function (e) {
            if (!gyroTicking) {
              const rect = bookWrapper.getBoundingClientRect();
              if (rect.top < window.innerHeight && rect.bottom > 0) {
                window.requestAnimationFrame(function () {
                  const gamma = Math.max(Math.min(e.gamma || 0, 25), -25);
                  const beta = Math.max(Math.min((e.beta || 0) - 45, 20), -20);
                  bookMockup.style.transition = "transform 0.15s ease-out";
                  bookMockup.style.transform = `perspective(1000px) rotateY(${gamma * 0.3}deg) rotateX(${-beta * 0.2}deg)`;
                  gyroTicking = false;
                });
                gyroTicking = true;
              }
            }
          }, { passive: true });
        }
      }
    }

    // 9.2 Spotlight Glow Místico nos Cards de Experimentos (Desktop e Touch)
    const expCards = document.querySelectorAll(".card-experimento");
    if (expCards.length > 0) {
      expCards.forEach(function (card) {
        function updateSpotlight(clientX, clientY) {
          const rect = card.getBoundingClientRect();
          const x = clientX - rect.left;
          const y = clientY - rect.top;
          card.style.setProperty("--spotlight-x", `${x}px`);
          card.style.setProperty("--spotlight-y", `${y}px`);
        }

        card.addEventListener("mousemove", function (e) {
          updateSpotlight(e.clientX, e.clientY);
        }, { passive: true });

        card.addEventListener("touchmove", function (e) {
          if (e.touches && e.touches[0]) {
            updateSpotlight(e.touches[0].clientX, e.touches[0].clientY);
          }
        }, { passive: true });
      });
    }

    // 9.3 Animações Sincronizadas dos Símbolos Iniciáticos e Porta da Seção 2 (Scroll-Linked 60 FPS)
    const tensaoSectionEl = document.getElementById("tensao");
    const olhoCardEl = document.getElementById("card-symbol-olho");
    const compassoCardEl = document.getElementById("card-symbol-compasso");
    const seloCardEl = document.getElementById("card-symbol-selo");
    const doorLeafEl = document.querySelector(".door-leaf-wrapper");
    const doorGlowEl = document.querySelector(".door-inner-glow");

    let tickingTensao = false;

    function updateSection2Symbols() {
      if (!tensaoSectionEl) return;
      const rect = tensaoSectionEl.getBoundingClientRect();
      const vh = window.innerHeight;

      if (rect.top < vh && rect.bottom > 0) {
        // Progresso de descida da Seção 2 pela tela (0 a 1)
        const progress = Math.min(Math.max((vh - rect.top) / (vh + rect.height * 0.7), 0), 1);

        // 1. O Triângulo do Olho: cresce e acende dourado radiante
        if (olhoCardEl) {
          const eyeTri = olhoCardEl.querySelector(".olho-triangulo");
          if (eyeTri) {
            const eyeScale = 1.0 + progress * 0.22;
            const eyeGlow = 4 + progress * 14;
            eyeTri.style.transform = `scale(${eyeScale})`;
            eyeTri.style.filter = `drop-shadow(0 0 ${eyeGlow}px rgba(217, 169, 75, ${0.45 + progress * 0.5})) drop-shadow(0 0 3px #FFF9ED)`;
            if (progress > 0.15) {
              eyeTri.style.stroke = "#F5D78E";
              eyeTri.style.fill = `rgba(217, 169, 75, ${0.08 + progress * 0.18})`;
            }
          }
        }

        // 2. Compasso: acende dourado e se movimenta em oscilação de medição
        if (compassoCardEl) {
          const compassoTool = compassoCardEl.querySelector(".compasso-ferramenta");
          if (compassoTool) {
            const compassAngle = Math.sin(progress * Math.PI * 2.5) * 8.5;
            const compassGlow = 4 + progress * 13;
            compassoTool.style.transform = `rotate(${compassAngle}deg)`;
            compassoTool.style.filter = `drop-shadow(0 0 ${compassGlow}px rgba(217, 169, 75, ${0.45 + progress * 0.5}))`;
          }
        }

        // 3. Estrela de Salomão: gira e acende dourado radiante
        if (seloCardEl) {
          const star = seloCardEl.querySelector(".selo-estrela-giratoria");
          if (star) {
            const starAngle = progress * 360;
            const starGlow = 6 + progress * 16;
            star.style.transform = `rotate(${starAngle}deg)`;
            star.style.filter = `drop-shadow(0 0 ${starGlow}px rgba(217, 169, 75, ${0.5 + progress * 0.5})) drop-shadow(0 0 4px #FFF5D6)`;
          }
        }

        // 4. Porta do Manifesto: entreabre e intensifica o feixe de luz mística
        if (doorLeafEl) {
          const doorAngle = -Math.min(progress * 1.6, 1) * 38;
          doorLeafEl.style.transform = `perspective(350px) rotateY(${doorAngle}deg)`;
        }
        if (doorGlowEl) {
          doorGlowEl.style.opacity = `${0.35 + Math.min(progress * 1.4, 1) * 0.65}`;
        }
      }

      tickingTensao = false;
    }

    window.addEventListener(
      "scroll",
      function () {
        if (!tickingTensao) {
          window.requestAnimationFrame(updateSection2Symbols);
          tickingTensao = true;
        }
      },
      { passive: true }
    );

    updateSection2Symbols();

    // 9.4 Fallback de Parallax em Scroll para navegadores sem View Timeline nativa
    const supportsViewTimeline =
      window.CSS &&
      window.CSS.supports &&
      (CSS.supports("animation-timeline", "view()") || CSS.supports("animation-timeline: view()"));

    if (!supportsViewTimeline) {
      const heroVisual = document.querySelector(".hero-visual.parallax-layer");
      const heroGlow = document.querySelector(".hero-ambient-glow");
      const watermarkTensao = document.querySelector(".watermark-tensao");
      const tensaoSection = document.getElementById("tensao");
      const watermarkPortal = document.querySelector(".watermark-portal");
      const ctaFinalSection = document.getElementById("cta-final");

      let tickingParallax = false;

      function updateParallaxElements() {
        const scrollY = window.scrollY || document.documentElement.scrollTop || 0;
        const vh = window.innerHeight;

        // Hero Book & Glow Parallax
        if (scrollY < vh * 1.5) {
          if (heroVisual) {
            heroVisual.style.transform = `translate3d(0, ${-scrollY * 0.08}px, 0)`;
          }
          if (heroGlow) {
            heroGlow.style.transform = `translateX(-50%) translate3d(0, ${scrollY * 0.1}px, 0)`;
          }
        }

        // Tensão Watermark Parallax
        if (watermarkTensao && tensaoSection) {
          const tRect = tensaoSection.getBoundingClientRect();
          if (tRect.top < vh && tRect.bottom > 0) {
            const progress = (tRect.top - vh / 2) * 0.06;
            watermarkTensao.style.transform = `translate3d(0, ${progress}px, 0)`;
          }
        }

        // Portal Watermark Parallax
        if (watermarkPortal && ctaFinalSection) {
          const pRect = ctaFinalSection.getBoundingClientRect();
          if (pRect.top < vh && pRect.bottom > 0) {
            const progress = (pRect.top - vh / 2) * 0.05;
            watermarkPortal.style.transform = `translate3d(-50%, calc(-50% + ${progress}px), 0)`;
          }
        }

        tickingParallax = false;
      }

      window.addEventListener(
        "scroll",
        function () {
          if (!tickingParallax) {
            window.requestAnimationFrame(updateParallaxElements);
            tickingParallax = true;
          }
        },
        { passive: true }
      );

      updateParallaxElements();
    }
  }

  // 10. O Olho Vivo do Capítulo 1 (Mentalismo — Olhar Aleatório Contínuo 60 FPS)
  const livingPupilEl = document.querySelector(".living-pupil");
  const livingGlowEl = document.querySelector(".living-eye-glow");
  const sampleFrameEl = document.querySelector(".notebook-sample-frame");

  if (livingPupilEl && sampleFrameEl && !prefersReduced) {
    let eyeTimer = null;

    // Pontos orgânicos de observação cósmica (em pixels relativos ao centro da íris)
    const gazeTargets = [
      { x: 0, y: 0, wait: 2800 },        // Centro: Fixo no leitor com aura máxima
      { x: -6.5, y: -2, wait: 2300 },    // Olha para a esquerda
      { x: 6, y: -2.5, wait: 2500 },     // Olha para a direita
      { x: -4, y: 4.5, wait: 2200 },     // Olha para baixo/esquerda (texto)
      { x: 5, y: 4, wait: 2400 },        // Olha para baixo/direita (número 1)
      { x: 0, y: -5.5, wait: 2000 },     // Olha para o alto
      { x: 7.5, y: 1, wait: 2600 },      // Direita distante
      { x: -7.5, y: 1.5, wait: 2700 },   // Esquerda distante
      { x: 0, y: 0, wait: 3400 },        // Retorna ao centro
      { x: -3, y: -4, wait: 1900 },      // Canto superior esquerdo
      { x: 3.5, y: -3.5, wait: 2100 }    // Canto superior direito
    ];

    let currentGazeIndex = 0;

    function lookAtRandomPoint() {
      let nextIndex;
      do {
        nextIndex = Math.floor(Math.random() * gazeTargets.length);
      } while (nextIndex === currentGazeIndex && gazeTargets.length > 1);

      currentGazeIndex = nextIndex;
      const target = gazeTargets[currentGazeIndex];

      // Micromovimento humano/orgânico sutil
      const jitterX = (Math.random() - 0.5) * 1.5;
      const jitterY = (Math.random() - 0.5) * 1.2;
      const finalX = target.x + jitterX;
      const finalY = target.y + jitterY;

      // Movimento sacádico do olho (rápido e depois estabilizado)
      livingPupilEl.style.transition = "transform 0.42s cubic-bezier(0.25, 1, 0.4, 1), filter 0.35s ease";
      livingPupilEl.style.transform = `translate(${finalX}px, ${finalY}px)`;

      // Quando o olho olha direto para o leitor (centro), a aura dourada atinge o clímax
      const isCentered = Math.abs(finalX) < 2.5 && Math.abs(finalY) < 2.5;
      if (isCentered) {
        if (livingGlowEl) livingGlowEl.style.opacity = "0.95";
        livingPupilEl.style.filter = "drop-shadow(0 0 12px rgba(245, 215, 142, 0.95)) drop-shadow(0 0 4px #FFFFFF)";
      } else {
        if (livingGlowEl) livingGlowEl.style.opacity = "0.65";
        livingPupilEl.style.filter = "drop-shadow(0 0 7px rgba(217, 169, 75, 0.8))";
      }

      // Intervalo variável entre olhares para parecer uma consciência viva e imprevisível
      const delay = target.wait + (Math.random() * 800 - 400);
      eyeTimer = setTimeout(lookAtRandomPoint, delay);
    }

    // Gerenciamento de desempenho: Ativa apenas quando a moldura do livro estiver visível
    if ("IntersectionObserver" in window) {
      const eyeObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              if (!eyeTimer) {
                lookAtRandomPoint();
              }
            } else {
              clearTimeout(eyeTimer);
              eyeTimer = null;
            }
          });
        },
        { threshold: 0.1 }
      );

      eyeObserver.observe(sampleFrameEl);
    } else {
      lookAtRandomPoint();
    }
  }
});


