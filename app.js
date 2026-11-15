// Lógica do site: monta a galeria por oficina e abre as peças em 3D.
// Todo texto vindo de dados.js entra na página como texto puro (textContent),
// nunca como HTML, e os endereços são validados antes de serem usados.
(function () {
  "use strict";

  var ID_VALIDO = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
  var FOTO_VALIDA = /^fotos\/[A-Za-z0-9._-]+\.(?:jpg|jpeg|png|webp)$/i;

  var site = typeof SITE === "object" && SITE ? SITE : {};
  var oficinas = (typeof OFICINAS !== "undefined" && Array.isArray(OFICINAS) ? OFICINAS : [])
    .filter(function (o) { return o && ID_VALIDO.test(String(o.id)); });
  var pecas = (typeof PECAS !== "undefined" && Array.isArray(PECAS) ? PECAS : [])
    .filter(function (p) {
      return p && ID_VALIDO.test(String(p.id)) &&
        oficinas.some(function (o) { return o.id === p.oficina; });
    });

  var $ = function (id) { return document.getElementById(id); };
  var texto = function (v) { return v == null ? "" : String(v); };
  var plural = function (n) { return n === 1 ? "1 peça" : n + " peças"; };
  var pecasDa = function (oficinaId) { return pecas.filter(function (p) { return p.oficina === oficinaId; }); };

  // Só aceita endereços https de um site esperado.
  function linkSeguro(valor, hostsPermitidos) {
    try {
      var u = new URL(texto(valor));
      if (u.protocol !== "https:") return "";
      return hostsPermitidos.indexOf(u.hostname) >= 0 ? u.href : "";
    } catch (e) { return ""; }
  }

  // Textos do ateliê
  if (site.nome) $("brand").textContent = texto(site.nome);
  $("about").textContent = texto(site.sobre);
  $("city").textContent = texto(site.cidade);
  var insta = linkSeguro(site.instagram, ["www.instagram.com", "instagram.com"]);
  if (insta) { $("insta").href = insta; $("insta").hidden = false; }
  var fone = texto(site.whatsapp).replace(/\D/g, "");
  if (fone.length >= 10 && fone.length <= 15) {
    $("whats").href = "https://wa.me/" + fone + "?text=" +
      encodeURIComponent("Olá! Vi o portfólio 3D das oficinas e gostaria de falar com o ateliê.");
    $("whats").hidden = false;
  }

  $("total").textContent = oficinas.length === 1
    ? "1 oficina · " + plural(pecas.length)
    : oficinas.length + " oficinas · " + plural(pecas.length);

  // Seletor de oficinas
  var atual = null;
  var caixaOficinas = $("workshops");
  oficinas.forEach(function (o) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "workshop";
    b.dataset.id = o.id;
    b.setAttribute("aria-pressed", "false");
    var nome = document.createElement("strong");
    nome.textContent = texto(o.nome);
    var info = document.createElement("span");
    info.textContent = [texto(o.data), plural(pecasDa(o.id).length)].filter(Boolean).join(" · ");
    b.append(nome, info);
    b.addEventListener("click", function () { location.hash = "oficina-" + o.id; });
    caixaOficinas.appendChild(b);
  });
  if (!oficinas.length) {
    $("pick-label").hidden = true;
    $("workshop-title").textContent = "Nenhuma oficina publicada ainda";
  }

  function mostrarOficina(o) {
    if (!o || (atual && atual.id === o.id)) return;
    atual = o;
    Array.prototype.forEach.call(caixaOficinas.children, function (b) {
      b.setAttribute("aria-pressed", b.dataset.id === o.id ? "true" : "false");
    });
    var lista = pecasDa(o.id);
    $("workshop-title").textContent = [texto(o.nome), texto(o.data)].filter(Boolean).join(" · ");
    $("workshop-count").textContent = plural(lista.length);
    var grid = $("grid");
    grid.textContent = "";
    lista.forEach(function (p, i) {
      var li = document.createElement("li");
      var card = document.createElement("button");
      card.type = "button";
      card.className = "card";

      var cover = document.createElement("div");
      cover.className = "cover";
      var img = document.createElement("img");
      img.src = "modelos/" + p.id + ".webp";
      img.alt = "Vista da peça " + texto(p.nome);
      img.loading = "lazy";
      img.addEventListener("error", function () {
        img.remove();
        var s = document.createElement("span");
        s.className = "no-cover";
        s.textContent = "Peça em processamento";
        cover.appendChild(s);
      });
      cover.appendChild(img);
      var tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = "Peça nº " + String(i + 1).padStart(2, "0");
      cover.appendChild(tag);
      if (p.teste) {
        var t = document.createElement("span");
        t.className = "tag test";
        t.textContent = "Exemplo de teste";
        cover.appendChild(t);
      }

      var body = document.createElement("div");
      body.className = "card-body";
      var h = document.createElement("h4");
      h.textContent = texto(p.nome);
      var see = document.createElement("span");
      see.className = "see";
      see.textContent = "Ver em 3D";
      body.append(h, see);

      card.append(cover, body);
      card.addEventListener("click", function () { location.hash = "peca-" + p.id; });
      li.appendChild(card);
      grid.appendChild(li);
    });
    $("empty").hidden = lista.length > 0;
  }

  // Janela 3D. Cada oficina e cada peça têm endereço próprio
  // (#oficina-<id> e #peca-<id>), que pode virar QR code.
  var dlg = $("viewer"), mv = $("mv"), msg = $("stage-msg");
  mv.addEventListener("load", function () {
    msg.textContent = "Arraste para girar. Use dois dedos ou a roda do mouse para aproximar.";
  });
  mv.addEventListener("error", function () {
    msg.textContent = "Não foi possível carregar esta peça. Tente novamente mais tarde.";
  });

  function abrirPeca(p) {
    var o = oficinas.find(function (x) { return x.id === p.oficina; });
    mostrarOficina(o);
    $("dlg-title").textContent = texto(p.nome);
    $("dlg-meta").textContent = [texto(o.nome), texto(o.data)].filter(Boolean).join(" · ");
    $("dlg-desc").textContent = texto(p.descricao);
    $("dlg-desc").hidden = !p.descricao;
    var fotos = (Array.isArray(p.fotos) ? p.fotos : []).filter(function (f) { return FOTO_VALIDA.test(texto(f)); });
    var box = $("dlg-photos");
    box.textContent = "";
    fotos.forEach(function (src, n) {
      var im = document.createElement("img");
      im.src = src;
      im.alt = "Foto " + (n + 1) + " da peça " + texto(p.nome);
      im.loading = "lazy";
      box.appendChild(im);
    });
    $("dlg-photos-wrap").hidden = fotos.length === 0;
    msg.textContent = "Carregando a peça…";
    mv.setAttribute("alt", "Modelo 3D da peça " + texto(p.nome));
    mv.setAttribute("src", "modelos/" + p.id + ".glb");
    if (!dlg.open) dlg.showModal();
  }

  function rota() {
    var m = /^#(oficina|peca)-([a-z0-9-]+)$/.exec(location.hash);
    var p = m && m[1] === "peca" && pecas.find(function (x) { return x.id === m[2]; });
    if (p) { abrirPeca(p); return; }
    if (dlg.open) dlg.close();
    var o = m && m[1] === "oficina" && oficinas.find(function (x) { return x.id === m[2]; });
    mostrarOficina(o || atual || oficinas[0]);
  }

  dlg.addEventListener("close", function () {
    mv.removeAttribute("src");
    if (/^#peca-/.test(location.hash) && atual) location.hash = "oficina-" + atual.id;
  });
  $("dlg-close").addEventListener("click", function () { dlg.close(); });
  dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
  window.addEventListener("hashchange", rota);
  rota();
})();
