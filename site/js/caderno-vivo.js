/**
 * Caderno vivo — O Elo Universal (26/11/2026)
 * O caderno para escrever no próprio aparelho. Tudo o que a pessoa escreve fica salvo SÓ no
 * navegador dela (localStorage); nada é enviado para servidor nenhum.
 *
 * Rotas (pelo #):  #inicio · #cap-N · #cap-N-registro · #fechamento · #imprimir
 * Texto: data/caderno-<token>.json, gerado por _trabalho/gerar_caderno_vivo.py a partir do
 * mesmo content.json do PDF.
 */
(function () {
  "use strict";

  var CHAVE = "elo-caderno-vivo-v1";
  var script = document.currentScript;
  var URL_DADOS = script && script.getAttribute("data-dados");
  var main = document.getElementById("cv-conteudo");
  var salvoEl = document.getElementById("cv-salvo");

  var D = null;          // conteúdo do caderno
  var R = ler();          // respostas: { "c1.0": "texto", ... }
  var armazenamentoOk = testarArmazenamento();

  // ------------------------------------------------------------------ armazenamento
  function testarArmazenamento() {
    try {
      localStorage.setItem("__elo_teste", "1");
      localStorage.removeItem("__elo_teste");
      return true;
    } catch (e) {
      return false;
    }
  }

  function ler() {
    try {
      var v = JSON.parse(localStorage.getItem(CHAVE));
      return v && typeof v === "object" ? v : {};
    } catch (e) {
      return {};
    }
  }

  var timerSalvar = null;
  function salvar() {
    clearTimeout(timerSalvar);
    timerSalvar = setTimeout(function () {
      try {
        R._atualizado = new Date().toISOString();
        localStorage.setItem(CHAVE, JSON.stringify(R));
        avisoSalvo("Salvo neste aparelho", false);
      } catch (e) {
        avisoSalvo("Não deu para salvar. Faça uma cópia de segurança no início do caderno.", true);
      }
    }, 300);
  }

  var timerAviso = null;
  function avisoSalvo(texto, erro) {
    if (!salvoEl) return;
    salvoEl.textContent = texto;
    salvoEl.classList.toggle("is-erro", !!erro);
    salvoEl.classList.add("is-on");
    clearTimeout(timerAviso);
    if (!erro) timerAviso = setTimeout(function () { salvoEl.classList.remove("is-on"); }, 1800);
  }

  // ------------------------------------------------------------------ texto
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function inline(s) {
    var h = esc(s);
    h = h.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    h = h.replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
    return h;
  }

  function blocos(lista) {
    return lista.map(function (b) {
      switch (b.t) {
        case "p": return "<p>" + inline(b.x) + "</p>";
        case "ul": return '<ul class="cv-lista">' + b.items.map(function (i) { return "<li>" + inline(i) + "</li>"; }).join("") + "</ul>";
        case "seal": return '<p class="cv-selo">' + inline(b.x) + "</p>";
        case "refrao": return '<p class="cv-refrao">' + inline(b.x) + "</p>";
        case "sugere": return '<div class="cv-quadro cv-sugere"><span class="cv-quadro-rot">O que isso sugere</span><p>' + inline(b.x) + "</p></div>";
        case "nao": {
          var corpo = b.items
            ? "<ul>" + b.items.map(function (i) { return "<li>" + inline(i) + "</li>"; }).join("") + "</ul>"
            : "<p>" + inline(b.x) + "</p>";
          if (b.after) corpo += '<p class="cv-depois">' + inline(b.after) + "</p>";
          return '<div class="cv-quadro cv-nao"><span class="cv-quadro-rot">O que isso NÃO mostra</span>' + corpo + "</div>";
        }
        case "note": return '<p class="cv-nota">' + inline(b.x) + "</p>";
        case "caution": return '<div class="cv-quadro cv-cuidado"><p>' + inline(b.x) + "</p></div>";
        case "step": {
          var partes = b.h.split(" — ");
          var cab = partes.length > 1 ? '<span class="k">' + esc(partes[0]) + "</span>" + esc(partes[1]) : esc(b.h);
          var txt = b.ol
            ? "<ol>" + b.ol.map(function (i) { return "<li>" + inline(i) + "</li>"; }).join("") + "</ol>"
            : "<p>" + inline(b.x) + "</p>";
          return '<div class="cv-passo"><h4>' + cab + "</h4>" + txt + "</div>";
        }
        default: return "";
      }
    }).join("");
  }

  // ------------------------------------------------------------------ registro (campos)
  function idDe(k) { return "cv-" + k.replace(/\./g, "-"); }

  function campoTexto(k, rotulo, multilinha, linhas, extraClasse) {
    var id = idDe(k);
    var valor = R[k] || "";
    var controle = multilinha
      ? '<textarea id="' + id + '" data-k="' + k + '" rows="' + linhas + '">' + esc(valor) + "</textarea>"
      : '<input type="text" id="' + id + '" data-k="' + k + '" value="' + esc(valor) + '">';
    return '<div class="cv-campo' + (extraClasse ? " " + extraClasse : "") + '"><label for="' + id + '">' + inline(rotulo) + "</label>" + controle + "</div>";
  }

  function registro(prefixo, itens) {
    return itens.map(function (it, i) {
      var k = prefixo + "." + i;
      switch (it.k) {
        case "head":
          return '<h4 class="cv-reg-cab">' + esc(it.x) + "</h4>";
        case "area":
          return campoTexto(k, it.label, true, Math.max(2, it.lines + 1));
        case "line":
          return campoTexto(k, it.label, false);
        case "inline2":
        case "pair":
          return '<div class="cv-dois">' + campoTexto(k + ".a", it.a, false) + campoTexto(k + ".b", it.b, false) + "</div>";
        case "marks": {
          var marcas = Array.isArray(R[k]) ? R[k] : [];
          var bolas = "";
          for (var j = 0; j < it.n; j++) {
            bolas += '<button type="button" class="cv-marca" data-marca="' + k + '" data-i="' + j + '" aria-pressed="' + (marcas[j] ? "true" : "false") +
              '" aria-label="Marca ' + (j + 1) + '"></button>';
          }
          var total = marcas.filter(Boolean).length;
          return '<div class="cv-campo"><span class="cv-rotulo" id="' + idDe(k) + '-rot">' + inline(it.label) + "</span>" +
            '<div class="cv-marcas" role="group" aria-labelledby="' + idDe(k) + '-rot">' + bolas +
            '<span class="cv-marcas-total" data-total="' + k + '">' + total + (total === 1 ? " marca" : " marcas") + "</span></div></div>";
        }
        case "numbered": {
          var linhas = "";
          for (var n = 1; n <= it.n; n++) {
            var kn = k + "." + n;
            linhas += '<div class="cv-numerada"><span class="cv-num">' + n + ".</span>" +
              (it.prefix ? '<span class="cv-prefixo">' + esc(it.prefix) + "</span>" : "") +
              '<input type="text" id="' + idDe(kn) + '" data-k="' + kn + '" value="' + esc(R[kn] || "") + '" aria-label="' + esc(it.label + " " + n) + '"></div>';
          }
          return '<div class="cv-campo"><span class="cv-rotulo">' + inline(it.label) + "</span>" + linhas + "</div>";
        }
        case "scale": {
          var opcoes = "";
          for (var s = 0; s <= 10; s++) {
            opcoes += '<label class="cv-escala-op"><input type="radio" name="' + idDe(k) + '" data-k="' + k + '" value="' + s + '"' +
              (String(R[k]) === String(s) ? " checked" : "") + "><span>" + s + "</span></label>";
          }
          return '<fieldset class="cv-campo cv-escala"><legend>' + inline(it.label) + "</legend><div class=\"cv-escala-linha\">" + opcoes + "</div></fieldset>";
        }
        case "table": {
          var cab = it.cols.map(function (c) { return "<th scope=\"col\">" + esc(c) + "</th>"; }).join("");
          var corpo = it.rows.map(function (rot, r) {
            var cels = "";
            for (var c = 1; c < it.cols.length; c++) {
              var kc = k + "." + r + "." + c;
              cels += '<td><input type="text" inputmode="numeric" maxlength="1" data-k="' + kc + '" value="' + esc(R[kc] || "") +
                '" aria-label="' + esc("Dia " + rot + ", " + it.cols[c]) + '"></td>';
            }
            return '<tr><th scope="row">' + esc(rot) + "</th>" + cels + "</tr>";
          }).join("");
          return '<div class="cv-campo cv-tabela-caixa"><span class="cv-rotulo">' + esc(it.caption) + '</span><div class="cv-tabela-rola"><table class="cv-tabela"><thead><tr>' +
            cab + "</tr></thead><tbody>" + corpo + "</tbody></table></div></div>";
        }
        case "checktable": {
          var linhasT = it.rows.map(function (rot, r) {
            var ks = k + "." + r + ".s";
            var kt = k + "." + r + ".t";
            var nome = idDe(ks);
            return '<div class="cv-checklinha"><span class="cv-checkdia">' + esc(it.cols[0]) + " " + esc(rot) + "</span>" +
              '<fieldset class="cv-simnao"><legend>' + esc(it.cols[1]) + "</legend>" +
              '<label><input type="radio" name="' + nome + '" data-k="' + ks + '" value="sim"' + (R[ks] === "sim" ? " checked" : "") + "><span>sim</span></label>" +
              '<label><input type="radio" name="' + nome + '" data-k="' + ks + '" value="não"' + (R[ks] === "não" ? " checked" : "") + "><span>não</span></label></fieldset>" +
              '<label class="cv-checktexto"><span>' + esc(it.cols[2]) + '</span><input type="text" data-k="' + kt + '" value="' + esc(R[kt] || "") + '"></label></div>';
          }).join("");
          return '<div class="cv-campo">' + linhasT + "</div>";
        }
        default:
          return "";
      }
    }).join("");
  }

  // chaves preenchíveis de um registro (para medir o andamento)
  function chaves(prefixo, itens) {
    var out = [];
    itens.forEach(function (it, i) {
      var k = prefixo + "." + i;
      if (it.k === "area" || it.k === "line" || it.k === "marks" || it.k === "scale") out.push(k);
      else if (it.k === "inline2" || it.k === "pair") out.push(k + ".a", k + ".b");
      else if (it.k === "numbered") for (var n = 1; n <= it.n; n++) out.push(k + "." + n);
      else if (it.k === "table") it.rows.forEach(function (_, r) { for (var c = 1; c < it.cols.length; c++) out.push(k + "." + r + "." + c); });
      else if (it.k === "checktable") it.rows.forEach(function (_, r) { out.push(k + "." + r + ".s", k + "." + r + ".t"); });
    });
    return out;
  }

  function preenchido(k) {
    var v = R[k];
    if (Array.isArray(v)) return v.some(Boolean);
    return v != null && String(v).trim() !== "";
  }

  function linhaFinal(cap) { return "c" + cap.n + "." + (cap.registro.length - 1); }

  function estado(cap) {
    var ks = chaves("c" + cap.n, cap.registro);
    var feitos = ks.filter(preenchido).length;
    if (preenchido(linhaFinal(cap))) return { cls: "feito", txt: "Concluído" };
    if (feitos > 0) return { cls: "andamento", txt: "Em andamento" };
    return { cls: "novo", txt: "Não começado" };
  }

  // ------------------------------------------------------------------ telas
  function orn(nome, tam) {
    return '<img src="assets/svg/' + nome + '_escuro.svg" alt="" width="' + tam + '" height="' + tam + '">';
  }

  function telaInicio() {
    var caps = D.capitulos;
    var feitos = caps.filter(function (c) { return estado(c).cls === "feito"; }).length;
    var ultimo = R._rota && /^#(cap-\d|fechamento)/.test(R._rota) ? R._rota : null;
    var itens = caps.map(function (c) {
      var e = estado(c);
      return '<li><a class="cv-item cv-' + e.cls + '" href="#cap-' + c.n + '">' + orn(c.ornamento, 40) +
        '<span class="cv-item-txt"><span class="cv-item-lei">Lei ' + c.n + (c.bonus ? " · bônus" : "") + " · " + esc(c.experimento.duration) + "</span>" +
        '<span class="cv-item-nome">' + esc(c.name) + "</span>" +
        '<span class="cv-item-exp">' + esc(c.experimento.name) + "</span></span>" +
        '<span class="cv-item-estado">' + e.txt + "</span></a></li>";
    }).join("");
    var fimFeito = preenchido("f." + (D.fechamento.registro.length - 1));
    itens += '<li><a class="cv-item cv-' + (fimFeito ? "feito" : feitos === 7 ? "andamento" : "novo") + '" href="#fechamento">' +
      '<img src="assets/svg/marca-elo_escuro.svg" alt="" width="40" height="20" class="cv-item-elo">' +
      '<span class="cv-item-txt"><span class="cv-item-lei">Fechamento · 1 sessão</span><span class="cv-item-nome">O que se repetiu?</span>' +
      '<span class="cv-item-exp">A releitura</span></span><span class="cv-item-estado">' + (fimFeito ? "Concluído" : feitos === 7 ? "Pronto para a releitura" : "Depois das sete") + "</span></a></li>";

    main.innerHTML =
      '<section class="cv-inicio">' +
      '<p class="cv-sobre">Seu caderno</p>' +
      "<h1>Caderno das Leis Herméticas</h1>" +
      '<p class="cv-lead">Leia cada lei, faça o experimento e escreva o registro aqui mesmo. Tudo fica salvo sozinho, <b>só neste aparelho e neste navegador</b>.</p>' +
      (armazenamentoOk ? "" : '<p class="cv-alerta">Este navegador não está deixando salvar. Abra o link no Chrome ou no Safari, fora do modo anônimo.</p>') +
      '<div class="cv-progresso" aria-label="' + feitos + ' de 7 leis concluídas"><div class="cv-progresso-barra"><i style="width:' + Math.round(feitos / 7 * 100) + '%"></i></div>' +
      "<span>" + feitos + " de 7 leis concluídas</span></div>" +
      (ultimo ? '<a class="cv-botao cv-botao-principal" href="' + esc(ultimo) + '">Continuar de onde parei</a>' : '<a class="cv-botao cv-botao-principal" href="#cap-1">Começar pela Lei 1</a>') +
      '<ol class="cv-lista-leis">' + itens + "</ol>" +
      '<section class="cv-ferramentas" aria-labelledby="cv-ferr-tit">' +
      '<h2 id="cv-ferr-tit">Guardar o que você escreveu</h2>' +
      '<p>Como tudo fica só neste aparelho, vale guardar uma cópia de vez em quando.</p>' +
      '<div class="cv-ferramentas-botoes">' +
      '<a class="cv-botao" href="#imprimir">Baixar meu caderno em PDF</a>' +
      '<button type="button" class="cv-botao" id="cv-exportar">Salvar cópia de segurança</button>' +
      '<label class="cv-botao cv-botao-arquivo">Restaurar uma cópia<input type="file" id="cv-importar" accept="application/json,.json"></label>' +
      "</div>" +
      '<p class="cv-miudo">A cópia de segurança é um arquivo pequeno. Para continuar em outro aparelho, abra o mesmo link nele e use “Restaurar uma cópia”.</p>' +
      "</section>" +
      '<p class="cv-miudo cv-rodape">Material educativo e de reflexão pessoal. Não promete resultados e não substitui orientação médica, psicológica ou financeira. Dúvidas: <a href="mailto:oelouniversal@proton.me">oelouniversal@proton.me</a></p>' +
      "</section>";

    document.getElementById("cv-exportar").addEventListener("click", exportar);
    document.getElementById("cv-importar").addEventListener("change", importar);
  }

  function telaCapitulo(n, irParaRegistro) {
    var cap = D.capitulos[n - 1];
    if (!cap) return telaInicio();
    var exp = cap.experimento;
    var prox = D.capitulos[n];
    var porta = prox
      ? '<a class="cv-botao cv-botao-principal" href="#cap-' + prox.n + '">Capítulo ' + prox.n + " · " + esc(prox.name) + "</a>"
      : '<a class="cv-botao cv-botao-principal" href="#fechamento">Ir para o fechamento</a>';
    var ant = n > 1 ? '<a class="cv-link" href="#cap-' + (n - 1) + '">← Capítulo ' + (n - 1) + "</a>" : '<a class="cv-link" href="#inicio">← Sumário</a>';
    var fontes = cap.fontes.map(function (f) { return "<li>" + inline(f) + "</li>"; }).join("");

    main.innerHTML =
      '<article class="cv-cap">' +
      '<header class="cv-abertura">' +
      '<div class="cv-abertura-orn">' + orn(cap.ornamento, 120) + "</div>" +
      '<p class="cv-kick">Capítulo ' + n + (cap.bonus ? " · Bônus" : "") + " · Lei " + n + " de 7</p>" +
      "<h1>" + esc(cap.name) + "</h1>" +
      '<p class="cv-epi">' + esc(cap.epigraph) + "</p>" +
      '<p class="cv-lede">' + esc(cap.lede) + "</p>" +
      '<nav class="cv-mapa" aria-label="Partes do capítulo">' +
      ["tradicao:1:Tradição", "pista:2:Pista", "experimento:3:Experimento", "registro:4:Registro"].map(function (p) {
        var a = p.split(":");
        return '<button type="button" data-ir="cv-' + a[0] + '"><span>' + a[1] + "</span>" + a[2] + "</button>";
      }).join("") +
      "</nav></header>" +
      '<section class="cv-parte" id="cv-tradicao"><h2><span class="cv-num-parte">1</span>O que a tradição afirma</h2>' + blocos(cap.tradicao) + "</section>" +
      '<section class="cv-parte cv-parte-pista" id="cv-pista"><h2><span class="cv-num-parte">2</span>A pista da ciência</h2>' + blocos(cap.pista) + "</section>" +
      '<section class="cv-parte" id="cv-experimento"><h2><span class="cv-num-parte">3</span>O experimento<small>' + esc(exp.name) + "</small></h2>" +
      '<p class="cv-duracao">Duração: ' + esc(exp.duration) + "</p>" + blocos(exp.blocks) + "</section>" +
      '<section class="cv-parte cv-registro" id="cv-registro"><h2><span class="cv-num-parte">4</span>O registro</h2>' +
      '<p class="cv-reg-ajuda">Escreva aqui. Fica salvo sozinho, neste aparelho.</p>' + registro("c" + n, cap.registro) + "</section>" +
      '<section class="cv-porta"><img src="assets/svg/glifo-porta_escuro.svg" alt="" width="40" height="40">' +
      '<span class="cv-porta-rot">' + esc(cap.porta.label) + "</span>" +
      "<p>" + inline(cap.porta.x) + "</p>" + porta + "</section>" +
      '<details class="cv-fontes"><summary>Fontes deste capítulo</summary><ol>' + fontes + "</ol></details>" +
      '<nav class="cv-rodape-nav">' + ant + '<a class="cv-link" href="#inicio">Sumário</a></nav>' +
      "</article>";

    main.querySelectorAll(".cv-mapa [data-ir]").forEach(function (b) {
      b.addEventListener("click", function () {
        var alvo = document.getElementById(b.getAttribute("data-ir"));
        if (alvo) alvo.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
    if (irParaRegistro) {
      var reg = document.getElementById("cv-registro");
      if (reg) setTimeout(function () { reg.scrollIntoView({ block: "start" }); }, 30);
    }
  }

  function telaFechamento() {
    var F = D.fechamento;
    var sete = D.capitulos.map(function (c) {
      var v = R[linhaFinal(c)];
      var tem = v && String(v).trim();
      return '<li><span class="cv-sete-n">' + c.n + "</span><div><span class=\"cv-sete-nome\">" + esc(c.name) + "</span>" +
        (tem ? '<p class="cv-sete-txt">' + esc(v) + "</p>" : '<p class="cv-sete-vazio">Ainda em branco. <a href="#cap-' + c.n + '-registro">Escrever no registro do Capítulo ' + c.n + "</a></p>") +
        "</div></li>";
    }).join("");
    main.innerHTML =
      '<article class="cv-cap">' +
      '<header class="cv-abertura cv-abertura-fim">' +
      '<div class="cv-abertura-orn"><img src="assets/svg/marca-elo_escuro.svg" alt="" width="140" height="70"></div>' +
      '<p class="cv-kick">Fechamento</p><h1>' + esc(F.titulo) + "</h1>" +
      '<p class="cv-lede">' + esc(F.abertura) + "</p></header>" +
      '<section class="cv-parte"><h2><span class="cv-num-parte">1</span>O experimento<small>' + esc(F.experimento.name) + "</small></h2>" +
      '<p class="cv-duracao">Duração: ' + esc(F.experimento.duration) + "</p>" + blocos(F.experimento.blocks) + "</section>" +
      '<section class="cv-parte cv-registro" id="cv-registro"><h2><span class="cv-num-parte">2</span>O registro</h2>' +
      '<h4 class="cv-reg-cab">As sete linhas “o que eu percebi”</h4><ol class="cv-sete">' + sete + "</ol>" +
      registro("f", F.registro) + '<p class="cv-refrao">' + esc(F.fecho) + "</p></section>" +
      '<section class="cv-ferramentas"><h2>Guardar o seu caderno</h2><div class="cv-ferramentas-botoes">' +
      '<a class="cv-botao cv-botao-principal" href="#imprimir">Baixar meu caderno em PDF</a></div></section>' +
      '<nav class="cv-rodape-nav"><a class="cv-link" href="#cap-7">← Capítulo 7</a><a class="cv-link" href="#inicio">Sumário</a></nav>' +
      "</article>";
  }

  // ------------------------------------------------------------------ versão para imprimir / PDF
  function valorImpresso(k) {
    var v = R[k];
    if (v == null || String(v).trim() === "") return '<span class="cv-imp-vazio">(em branco)</span>';
    return esc(v).replace(/\n/g, "<br>");
  }

  function registroImpresso(prefixo, itens) {
    return itens.map(function (it, i) {
      var k = prefixo + "." + i;
      switch (it.k) {
        case "head": return "<h4>" + esc(it.x) + "</h4>";
        case "area":
        case "line": return '<div class="cv-imp-campo"><b>' + inline(it.label) + "</b><p>" + valorImpresso(k) + "</p></div>";
        case "inline2":
        case "pair": return '<div class="cv-imp-campo"><b>' + inline(it.a) + "</b> " + valorImpresso(k + ".a") + " &nbsp; <b>" + inline(it.b) + "</b> " + valorImpresso(k + ".b") + "</div>";
        case "marks": {
          var m = Array.isArray(R[k]) ? R[k].filter(Boolean).length : 0;
          return '<div class="cv-imp-campo"><b>' + inline(it.label) + "</b><p>" + m + (m === 1 ? " marca" : " marcas") + "</p></div>";
        }
        case "numbered": {
          var l = "";
          for (var n = 1; n <= it.n; n++) l += "<li>" + (it.prefix ? esc(it.prefix) + " " : "") + valorImpresso(k + "." + n) + "</li>";
          return '<div class="cv-imp-campo"><b>' + inline(it.label) + "</b><ol>" + l + "</ol></div>";
        }
        case "scale": return '<div class="cv-imp-campo"><b>' + inline(it.label) + "</b><p>" + (R[k] != null ? esc(R[k]) + " de 10" : '<span class="cv-imp-vazio">(em branco)</span>') + "</p></div>";
        case "table": {
          var cab = it.cols.map(function (c) { return "<th>" + esc(c) + "</th>"; }).join("");
          var corpo = it.rows.map(function (rot, r) {
            var cels = "";
            for (var c = 1; c < it.cols.length; c++) cels += "<td>" + esc(R[k + "." + r + "." + c] || "") + "</td>";
            return "<tr><th>" + esc(rot) + "</th>" + cels + "</tr>";
          }).join("");
          return '<div class="cv-imp-campo"><b>' + esc(it.caption) + "</b><table><thead><tr>" + cab + "</tr></thead><tbody>" + corpo + "</tbody></table></div>";
        }
        case "checktable": {
          var linhas = it.rows.map(function (rot, r) {
            return "<tr><th>" + esc(rot) + "</th><td>" + esc(R[k + "." + r + ".s"] || "") + "</td><td>" + esc(R[k + "." + r + ".t"] || "") + "</td></tr>";
          }).join("");
          return '<div class="cv-imp-campo"><table><thead><tr>' + it.cols.map(function (c) { return "<th>" + esc(c) + "</th>"; }).join("") +
            "</tr></thead><tbody>" + linhas + "</tbody></table></div>";
        }
        default: return "";
      }
    }).join("");
  }

  function telaImprimir() {
    var hoje = new Date().toLocaleDateString("pt-BR");
    var caps = D.capitulos.map(function (c) {
      return '<section class="cv-imp-cap"><h2>' + c.n + " · " + esc(c.name) + "</h2>" +
        '<p class="cv-imp-exp">' + esc(c.experimento.name) + " · " + esc(c.experimento.duration) + "</p>" +
        registroImpresso("c" + c.n, c.registro) + "</section>";
    }).join("");
    var sete = D.capitulos.map(function (c) { return "<li><b>" + esc(c.name) + ":</b> " + valorImpresso(linhaFinal(c)) + "</li>"; }).join("");
    main.innerHTML =
      '<div class="cv-imp-barra"><a class="cv-link" href="#inicio">← Voltar</a>' +
      '<button type="button" class="cv-botao cv-botao-principal" id="cv-imprimir">Salvar em PDF ou imprimir</button></div>' +
      '<p class="cv-imp-dica">Na janela que abrir, escolha “Salvar como PDF” (no celular: Compartilhar → Imprimir → Salvar PDF ou Salvar em Arquivos).</p>' +
      '<article class="cv-impressao">' +
      "<header><h1>Meu Caderno das Leis Herméticas</h1><p>O Elo Universal · registros salvos em " + hoje + "</p></header>" +
      caps +
      '<section class="cv-imp-cap"><h2>Fechamento · O que se repetiu?</h2><b>As sete linhas</b><ol>' + sete + "</ol>" +
      registroImpresso("f", D.fechamento.registro) + "</section>" +
      '<p class="cv-imp-fim">Pistas, não provas. A conclusão é sua, escrita a partir do que você observou.</p>' +
      "</article>";
    document.getElementById("cv-imprimir").addEventListener("click", function () { window.print(); });
  }

  // ------------------------------------------------------------------ cópia de segurança
  function exportar() {
    var dados = JSON.stringify({ app: "elo-caderno-vivo", versao: 1, salvo: new Date().toISOString(), respostas: R }, null, 1);
    var blob = new Blob([dados], { type: "application/json" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "caderno-vivo-copia-" + new Date().toISOString().slice(0, 10) + ".json";
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
    avisoSalvo("Cópia de segurança baixada", false);
  }

  function importar(e) {
    var arq = e.target.files && e.target.files[0];
    if (!arq) return;
    var leitor = new FileReader();
    leitor.onload = function () {
      try {
        var obj = JSON.parse(leitor.result);
        if (!obj || obj.app !== "elo-caderno-vivo" || typeof obj.respostas !== "object") throw new Error("formato");
        if (!window.confirm("Restaurar esta cópia? O que está escrito agora neste aparelho será trocado pelo que está na cópia.")) return;
        R = obj.respostas;
        salvar();
        avisoSalvo("Cópia restaurada", false);
        rota();
      } catch (err) {
        avisoSalvo("Este arquivo não é uma cópia do Caderno vivo.", true);
      }
    };
    leitor.readAsText(arq);
  }

  // ------------------------------------------------------------------ edição
  main.addEventListener("input", function (e) {
    var el = e.target;
    var k = el.getAttribute && el.getAttribute("data-k");
    if (!k) return;
    if (el.type === "radio") return;
    R[k] = el.value;
    salvar();
  });

  main.addEventListener("change", function (e) {
    var el = e.target;
    var k = el.getAttribute && el.getAttribute("data-k");
    if (!k || el.type !== "radio") return;
    R[k] = el.value;
    salvar();
  });

  main.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-marca]");
    if (!b) return;
    var k = b.getAttribute("data-marca");
    var i = parseInt(b.getAttribute("data-i"), 10);
    var arr = Array.isArray(R[k]) ? R[k].slice() : [];
    arr[i] = !arr[i];
    R[k] = arr;
    b.setAttribute("aria-pressed", arr[i] ? "true" : "false");
    var total = arr.filter(Boolean).length;
    var t = main.querySelector('[data-total="' + k + '"]');
    if (t) t.textContent = total + (total === 1 ? " marca" : " marcas");
    salvar();
  });

  // ------------------------------------------------------------------ rotas
  function rota() {
    if (!D) return;
    var h = window.location.hash || "#inicio";
    var m;
    if ((m = /^#cap-(\d)(-registro)?$/.exec(h))) {
      telaCapitulo(parseInt(m[1], 10), !!m[2]);
      lembrar(h.replace("-registro", ""));
      if (!m[2]) window.scrollTo(0, 0);
    } else if (h === "#fechamento") {
      telaFechamento();
      lembrar(h);
      window.scrollTo(0, 0);
    } else if (h === "#imprimir") {
      telaImprimir();
      window.scrollTo(0, 0);
    } else {
      telaInicio();
      window.scrollTo(0, 0);
    }
    document.body.setAttribute("data-tela", h.replace("#", "").replace(/-registro$/, "") || "inicio");
  }

  function lembrar(h) {
    if (R._rota === h) return;
    R._rota = h;
    try { localStorage.setItem(CHAVE, JSON.stringify(R)); } catch (e) { /* sem armazenamento */ }
  }

  window.addEventListener("hashchange", rota);

  // ------------------------------------------------------------------ aviso de navegador de aplicativo
  (function () {
    var ua = navigator.userAgent || "";
    var deApp = /Instagram|FBAN|FBAV|FB_IAB|TikTok|musical_ly|BytedanceWebview|Line\//i.test(ua);
    var aviso = document.getElementById("cv-aviso-app");
    if (!aviso) return;
    var dispensado = false;
    try { dispensado = sessionStorage.getItem("elo-aviso-app") === "1"; } catch (e) { /* ignora */ }
    if (deApp && !dispensado) aviso.hidden = false;
    var fechar = document.getElementById("cv-aviso-app-fechar");
    if (fechar) fechar.addEventListener("click", function () {
      aviso.hidden = true;
      try { sessionStorage.setItem("elo-aviso-app", "1"); } catch (e) { /* ignora */ }
    });
  })();

  // ------------------------------------------------------------------ início
  fetch(URL_DADOS, { cache: "no-cache" })
    .then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    })
    .then(function (dados) {
      D = dados;
      rota();
    })
    .catch(function () {
      main.innerHTML = '<p class="cv-alerta">Não foi possível abrir o caderno agora. Verifique a internet e recarregue a página. ' +
        'Se continuar, escreva para <a href="mailto:oelouniversal@proton.me">oelouniversal@proton.me</a>.</p>';
    });
})();
