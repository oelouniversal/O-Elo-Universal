/**
 * Camada de Telemetria — O Elo Universal
 * Fonte: Seção 11 de ESTRATEGIA-DE-CONVERSAO.md
 * 
 * Estado: INERTE (TRACKING_ATIVO = false).
 * Não carrega scripts de terceiros nem transmite dados pessoais.
 * Toda a estrutura de ganchos de eventos fica pronta para ativação futura.
 */

const Tracking = (function () {
  const eventosRegistrados = [];

  function track(evento, parametros = {}) {
    if (!window.CONFIG || !window.CONFIG.TRACKING_ATIVO) {
      // Inerte quando desativado
      return;
    }

    // Regra rígida de privacidade: nunca registrar dados pessoais (e-mail, nome)
    const payload = {
      evento,
      parametros,
      timestamp: new Date().toISOString()
    };

    eventosRegistrados.push(payload);
    console.debug("[Tracking Evento]", payload);
  }

  function init() {
    // Delegador de cliques para elementos com data-track
    document.addEventListener("click", function (e) {
      const target = e.target.closest("[data-track]");
      if (!target) return;

      const evento = target.getAttribute("data-track");
      const local = target.getAttribute("data-track-local") || "desconhecido";
      track(evento, { local });
    });

    // Observador de seções visíveis (50% na viewport, 1x por visita)
    if ("IntersectionObserver" in window) {
      const secoesObservadas = new Set();
      const observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting && !secoesObservadas.has(entry.target.id)) {
              secoesObservadas.add(entry.target.id);
              track("view_secao", { secao: entry.target.id });
            }
          });
        },
        { threshold: 0.5 }
      );

      document.querySelectorAll("section[id]").forEach(function (section) {
        observer.observe(section);
      });
    }
  }

  return {
    track,
    init,
    getLog: () => [...eventosRegistrados]
  };
})();

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", Tracking.init);
} else {
  Tracking.init();
}
