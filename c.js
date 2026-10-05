/* Armatex · wspólny skrypt stron */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var BASE = document.body.getAttribute('data-base') || '';
  // wersja angielska (/en/): ten sam skrypt, teksty wybierane po <html lang>
  // wersje językowe (/en/, /uk/): ten sam skrypt, teksty wybierane po <html lang>
  var LANG = document.documentElement.lang, EN = LANG === 'en', UK = LANG === 'uk';
  var L = function (pl, en, uk) { return UK ? uk : EN ? en : pl; };
  var UNITS = { en: { karton: 'box', worek: 'bag', 'opak.': 'pack', 'szt.': 'pcs' }, uk: { karton: 'коробка', worek: 'мішок', 'opak.': 'уп.', 'szt.': 'шт.' } };
  var UN = function (u) { return (UNITS[LANG] || {})[u] || u; };
  // nazwa grupy / linii z data/katalog.json w języku strony (grupy: [6] EN, [7] UK; linie: short_en, short_uk)
  var GN = function (g) { return (EN && g[6]) || (UK && g[7]) || g[2]; };
  var SN = function (x) { return (EN && x.short_en) || (UK && x.short_uk) || x.short; };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // Zdjęcie bez wersji _min.webp: wróć do oryginału
  $$('img[data-fb]').forEach(function (img) {
    img.addEventListener('error', function () {
      if (img.dataset.done) return; img.dataset.done = 1;
      var pic = img.parentNode; if (pic.tagName === 'PICTURE') $$('source', pic).forEach(function (s) { s.remove(); });
      img.src = img.dataset.fb;
    });
  });

  // Nawigacja: przezroczysta nad hero, pełna niżej
  var nav = $('#nav'), top = $('.hero, .phead, [data-top]');
  if (top) new IntersectionObserver(function (e) { nav.classList.toggle('is-solid', !e[0].isIntersecting); }, { rootMargin: '-80px 0px 0px 0px' }).observe(top);
  else nav.classList.add('is-solid');

  // Menu: rozwijane pozycje (Oferta, Materiały, język) i menu mobilne
  var dds = $$('.dd');
  function ddClose(d) { d.classList.remove('open'); $('button', d).setAttribute('aria-expanded', false); }
  dds.forEach(function (dd) {
    var ddb = $('button', dd);
    ddb.addEventListener('click', function () {
      dds.forEach(function (x) { if (x !== dd) ddClose(x); });
      var o = dd.classList.toggle('open'); ddb.setAttribute('aria-expanded', o);
    });
    dd.addEventListener('keydown', function (e) { if (e.key === 'Escape') { ddClose(dd); ddb.focus(); } });
  });
  if (dds.length) document.addEventListener('click', function (e) { dds.forEach(function (dd) { if (!dd.contains(e.target)) ddClose(dd); }); });
  var burger = $('#burger');
  if (burger) burger.addEventListener('click', function () {
    var o = document.body.classList.toggle('menu-open'); burger.setAttribute('aria-expanded', o);
    burger.setAttribute('aria-label', o ? L('Zamknij menu', 'Close menu', 'Закрити меню') : L('Otwórz menu', 'Open menu', 'Відкрити меню'));
  });

  // Wejścia + odometr (BYQ Odometer: 2 obroty, 0.85 s + 0.1 s na cyfrę)
  var SP = 2;
  function buildOdo(o) {
    var ds = o.dataset.odo.split('').map(Number), n = ds.length, reels = [];
    o.textContent = '';
    ds.forEach(function (d, i) {
      var box = document.createElement('span'), r = document.createElement('span'), h = '';
      box.className = 'odo-d'; r.className = 'odo-r';
      for (var c = 0; c <= SP; c++) for (var k = 0; k < 10; k++) h += '<span>' + k + '</span>';
      r.innerHTML = h; box.appendChild(r); o.appendChild(box); reels.push([r, d, i]);
      if (!('year' in o.dataset) && n - i > 1 && (n - i - 1) % 3 === 0) { var s = document.createElement('span'); s.className = 'odo-s'; o.appendChild(s); }
    });
    return reels;
  }
  function runOdo(reels) {
    reels.forEach(function (x) {
      x[0].style.transition = reduce ? 'none' : 'transform ' + (0.85 + x[2] * 0.1) + 's cubic-bezier(.165,.84,.44,1)';
      x[0].style.transform = 'translateY(-' + ((SP * 10 + x[1]) / ((SP + 1) * 10) * 100) + '%)';
    });
  }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var t = e.target; io.unobserve(t);
      if (t._reels) runOdo(t._reels); else t.classList.add('on');
    });
  }, { rootMargin: '0px 0px -15% 0px' });
  $$('.odo').forEach(function (o) { o._reels = buildOdo(o); io.observe(o); });
  $$('.in').forEach(function (el, i) { el.style.transitionDelay = (i % 3) * 0.1 + 's'; io.observe(el); });

  // Magnetyczne CTA (BYQ Magnetic Button)
  if (!reduce && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    $$('.mag').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect(), x = e.clientX - r.left - r.width / 2, y = e.clientY - r.top - r.height / 2;
        b.style.setProperty('--mx', x * 0.18 + 'px'); b.style.setProperty('--my', y * 0.3 + 'px');
        b.style.setProperty('--hx', x * 0.4 + 'px'); b.style.setProperty('--hy', y * 0.4 + 'px');
      });
      b.addEventListener('pointerleave', function () { ['--mx', '--my', '--hx', '--hy'].forEach(function (k) { b.style.removeProperty(k); }); });
    });
  }

  // Lista do wyceny: pozycja = [art, {q, l, u, p}], p = [[jednostka, szt. w jednostce], ...], u = indeks w p
  function packFix(v, def) {
    if (!v.p || !v.p.length) { v.p = def || [['szt.', 1]]; v.u = v.p.length - 1; }
    if (!(v.u >= 0 && v.u < v.p.length)) v.u = 0;
    return v;
  }
  function packTxt(v) {
    var u = v.p[v.u], n = u[1];
    if (n === 1) return v.q + ' ' + UN('szt.');
    return v.q + ' × ' + UN(u[0]) + ' (' + n + ' ' + UN('szt.') + ') = ' + String(v.q * n).replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ' + UN('szt.');
  }

  function thumb(src) {
    return '<span class="rfq__im">' + (src ? '<img src="' + BASE + String(src).replace(/[&<>"]/g, '') + '" alt="" width="44" height="44" loading="lazy" decoding="async">' : '') + '</span>';
  }

  if ($('#rfqList')) (function () {
  // ===== Wyszukiwarka (Besco, Tectite, Kuterlite) + zapytanie =====
  var DATA = null, INDEX = null, loading = null, page = 0, PER = 24, hits = [];
  // pole wyszukiwania jest opcjonalne (strona wyszukiwarki pokazuje listę grup i panel listy do wyceny)
  var active = new Set(), qEl = $('#q') || { value: '', addEventListener: function () {}, focus: function () {} }, res = $('#res'), cnt = $('#cnt'), more = $('#more');
  var fmt = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); };
  var norm = function (s) {
    return s.toLowerCase().replace(/[″"]/g, '').replace(/×/g, 'x').replace(/\s*x\s*/g, 'x').replace(/,/g, '.')
      .replace(/ą/g, 'a').replace(/ć/g, 'c').replace(/ę/g, 'e').replace(/ł/g, 'l').replace(/ń/g, 'n').replace(/ó/g, 'o').replace(/ś/g, 's').replace(/[źż]/g, 'z')
      .replace(/\s+/g, ' ').trim();
  };
  var squash = function (s) { return s.toLowerCase().replace(/[\s\-.]/g, ''); };
  function load() {
    if (loading) return loading;
    loading = fetch(BASE + 'data/katalog.json').then(function (r) { return r.json(); }).then(function (d) {
      DATA = d;
      INDEX = d.rows.map(function (r) {
        var g = d.groups[r[0]], s = d.series[g[0]];
        return { r: r, g: g, s: s, sid: s.id, hay: norm([r[1], r[2], g[2], g[3], g[1], s.short, s.brand].join(' ')), art: squash(r[1]) };
      });
      search(); drawRfq(); save();
    }).catch(function () { if (res) res.innerHTML = '<li class="fd__empty" style="display:block">' + L('Nie udało się wczytać katalogu. Odśwież stronę.', 'Could not load the catalogue. Please refresh the page.', 'Не вдалося завантажити каталог. Оновіть сторінку.') + '</li>'; });
    return loading;
  }
  new IntersectionObserver(function (e, o) { if (e[0].isIntersecting) { load(); o.disconnect(); } }, { rootMargin: '600px 0px' }).observe($('#katalog'));
  qEl.addEventListener('focus', load);

  function search() {
    if (!INDEX || !res) return;
    var q = norm(qEl.value), toks = q ? q.split(' ') : [], qa = squash(qEl.value);
    hits = INDEX.filter(function (x) {
      if (active.size && !active.has(x.sid)) return false;
      if (!toks.length) return true;
      if (qa.length > 3 && x.art.indexOf(qa) === 0) return true;
      return toks.every(function (t) { return x.hay.indexOf(t) !== -1 || x.art.indexOf(squash(t)) !== -1; });
    });
    // najpierw dokładny numer artykułu, potem kod grupy (np. T1, K610), potem numery zaczynające się od zapytania
    var rank = function (x) { return x.art === qa ? 3 : squash(x.g[1]) === qa ? 2 : x.art.indexOf(qa) === 0 ? 1 : 0; };
    if (qa) hits = hits.map(function (x, i) { return [rank(x), i, x]; }).sort(function (a, b) { return b[0] - a[0] || a[1] - b[1]; }).map(function (y) { return y[2]; });
    page = 0; res.innerHTML = '';
    // bez frazy i filtra lista wyników jest pusta: niżej są wszystkie grupy produktów
    // wiersz z licznikiem i legendą skrótów tylko przy wynikach
    var idle = !toks.length && !active.size; cnt.parentNode.hidden = idle;
    if (idle) { more.hidden = true; return; }
    render();
    cnt.textContent = fmt(hits.length) + L(' z ', ' of ', ' з ') + fmt(INDEX.length) + L(' pozycji', ' items', ' поз.');
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function render() {
    var slice = hits.slice(page * PER, (page + 1) * PER), h = '';
    if (!hits.length) { res.innerHTML = '<li class="fd__empty" style="display:block">' + L('Brak pozycji dla tego zapytania. Sprawdź numer albo zadzwoń: 513 191 502.', 'No items match this search. Check the number or call +48 513 191 502.', 'Немає позицій за цим запитом. Перевірте номер або зателефонуйте: +48 513 191 502.') + '</li>'; more.hidden = true; return; }
    slice.forEach(function (x) {
      var r = x.r, g = x.g, inq = rfq.has(r[1]), pk = r[3].slice().reverse();
      h += '<li><img src="' + BASE + esc(g[4]) + '" alt="" width="56" height="56" loading="lazy" decoding="async">' +
        '<div><b><a href="' + esc(g[5]) + '">' + esc(GN(g)) + '</a></b><span class="sz">' + esc(r[2]) + '</span><small>' + esc(g[3] ? g[3] + ' · ' : '') + esc(SN(x.s)) + '</small></div>' +
        '<code>' + esc(r[1]) + '</code>' +
        '<span class="pk">' + (pk.length ? '<i>' + pk.map(function (u) { return esc(u[0]); }).join(' / ') + '</i>' + pk.map(function (u) { return fmt(u[1]); }).join(' / ') : '') + '</span>' +
        '<button class="add' + (inq ? ' is-in' : '') + '" type="button" data-art="' + esc(r[1]) + '" aria-label="' + L('Dodaj ', 'Add ', 'Додати ') + esc(r[1]) + L(' do zapytania', ' to the quote list', ' до запиту') + '">' + (inq ? L('Dodano', 'Added', 'Додано') : L('Dodaj', 'Add', 'Додати')) + '</button></li>';
    });
    res.insertAdjacentHTML('beforeend', h);
    page++; more.hidden = page * PER >= hits.length;
    more.firstElementChild.textContent = L('Pokaż kolejne (', 'Show more (', 'Показати ще (') + fmt(hits.length - page * PER) + ')';
  }
  var t0; qEl.addEventListener('input', function () { clearTimeout(t0); t0 = setTimeout(function () { load().then(search); }, 120); });
  if (more) more.firstElementChild.addEventListener('click', render);
  $$('.fd__hint code').forEach(function (c) { c.addEventListener('click', function () { qEl.value = c.dataset.q; load().then(search); }); });
  var flt = $('#flt');
  function drawFilter() {
    if (!flt) return;
    if (!active.size || !DATA) { flt.hidden = true; return; }
    var names = DATA.series.filter(function (x) { return active.has(x.id); }).map(SN);
    flt.innerHTML = '<span class="label">' + L('Filtr', 'Filter', 'Фільтр') + '</span> <span></span> <button type="button">' + L('Wyczyść filtr ×', 'Clear filter ×', 'Очистити фільтр ×') + '</button>';
    flt.children[1].textContent = names.join(', ');
    flt.querySelector('button').addEventListener('click', function () { setSeries([]); qEl.focus(); });
    flt.hidden = false;
  }
  function setSeries(list) {
    active = new Set(list.filter(Boolean));
    load().then(drawFilter);
    $$('.chip').forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.s ? c.dataset.s.split(',').every(function (id) { return active.has(id); }) : !active.size); });
    load().then(search);
  }
  $$('.chip').forEach(function (c) {
    c.addEventListener('click', function () {
      if (!c.dataset.s) return setSeries([]);
      var ids = c.dataset.s.split(','), s = new Set(active), on = ids.every(function (id) { return s.has(id); });
      ids.forEach(function (id) { on ? s.delete(id) : s.add(id); }); setSeries(Array.from(s));
    });
  });
  $$('[data-series]').forEach(function (a) {
    a.addEventListener('click', function () { qEl.value = ''; setSeries(a.dataset.series.split(',')); });
  });

  // Zapytanie (lista pozycji) – pamiętane lokalnie w przeglądarce
  var rfq = new Map(), KEY = 'armatex-rfq';
  try { JSON.parse(localStorage.getItem(KEY) || '[]').forEach(function (x) { rfq.set(x[0], x[1]); }); } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(Array.from(rfq.entries()))); } catch (e) {} }
  function label(art) {
    if (!INDEX) return '';
    for (var i = 0; i < INDEX.length; i++) if (INDEX[i].r[1] === art) return GN(INDEX[i].g) + ' ' + INDEX[i].r[2];
    return '';
  }
  function imgOf(art) {
    if (INDEX) for (var i = 0; i < INDEX.length; i++) if (INDEX[i].r[1] === art) return INDEX[i].g[4];
    return '';
  }
  function packsOf(art) {
    if (INDEX) for (var i = 0; i < INDEX.length; i++) if (INDEX[i].r[1] === art) return INDEX[i].r[3].concat([['szt.', 1]]);
    return null;
  }
  function drawRfq() {
    var ul = $('#rfqList'), h = '', n = rfq.size;
    rfq.forEach(function (v, art) {
      packFix(v, packsOf(art));
      var opts = v.p.map(function (u, i) { return '<option value="' + i + '"' + (i === v.u ? ' selected' : '') + '>' + esc(UN(u[0])) + (u[1] > 1 ? ' (' + fmt(u[1]) + ' ' + UN('szt.') + ')' : '') + '</option>'; }).join('');
      if (!v.i && INDEX) v.i = imgOf(art);
      h += '<li>' + thumb(v.i) + '<div><code>' + esc(art) + '</code><small>' + esc(v.l || label(art)) + '</small></div>' +
        '<button class="rm" type="button" data-art="' + esc(art) + '" aria-label="' + L('Usuń ', 'Remove ', 'Видалити ') + esc(art) + '">×</button>' +
        '<div class="rfq__q"><input type="number" min="1" step="1" value="' + v.q + '" aria-label="' + L('Ilość ', 'Quantity ', 'Кількість ') + esc(art) + '" data-art="' + esc(art) + '">' +
        '<select aria-label="' + L('Jednostka ', 'Unit ', 'Одиниця ') + esc(art) + '" data-art="' + esc(art) + '">' + opts + '</select>' +
        '<span class="tot">' + (v.p[v.u][1] > 1 ? '= ' + fmt(v.q * v.p[v.u][1]) + ' ' + UN('szt.') : '') + '</span></div></li>';
    });
    ul.innerHTML = h;
    $('#rfqN').textContent = n + L(' poz.', ' items', ' поз.'); $('#pillN').textContent = n;
    $('#pill').classList.toggle('on', n > 0);
    $('#toForm').disabled = !n;
    $('#rfqHint').textContent = n ? L('Ustaw ilość i jednostkę (karton, worek, sztuki), potem wyślij zapytanie.', 'Set the quantity and unit (box, bag, pieces), then send the enquiry.', 'Вкажіть кількість і одиницю (коробка, мішок, штуки), потім надішліть запит.') : L('Twoja lista jest pusta. Otwórz linię produktów i dodaj rozmiary na stronie grupy.', 'Your list is empty. Open a product line and add sizes on the product group page.', 'Ваш список порожній. Відкрийте лінію продукції та додайте розміри на сторінці групи.');
  }
  if (res) res.addEventListener('click', function (e) {
    var b = e.target.closest('.add'); if (!b) return;
    var art = b.dataset.art;
    if (rfq.has(art)) rfq.delete(art); else { var nv = packFix({ q: 1, l: label(art), i: imgOf(art) }, packsOf(art)); nv.u = 0; rfq.set(art, nv); }
    b.classList.toggle('is-in', rfq.has(art)); b.textContent = rfq.has(art) ? L('Dodano', 'Added', 'Додано') : L('Dodaj', 'Add', 'Додати');
    save(); drawRfq();
  });
  function upd(e) {
    var i = e.target, v = i.dataset.art && rfq.get(i.dataset.art); if (!v) return;
    if (i.tagName === 'SELECT') v.u = +i.value; else v.q = Math.max(1, parseInt(i.value, 10) || 1);
    save();
    var t = i.parentNode.querySelector('.tot'), n = v.p[v.u][1];
    t.textContent = n > 1 ? '= ' + fmt(v.q * n) + ' ' + UN('szt.') : '';
  }
  $('#rfqList').addEventListener('input', upd);
  $('#rfqList').addEventListener('change', upd);
  $('#rfqList').addEventListener('click', function (e) {
    var b = e.target.closest('.rm'); if (!b) return;
    rfq.delete(b.dataset.art); save(); drawRfq();
    var btn = res && res.querySelector('.add[data-art="' + CSS.escape(b.dataset.art) + '"]'); if (btn) { btn.classList.remove('is-in'); btn.textContent = L('Dodaj', 'Add', 'Додати'); }
  });
  $('#toForm').addEventListener('click', function () {
    var lines = [L('Lista pozycji do wyceny:', 'Items for quotation:', 'Позиції для розрахунку ціни:')];
    rfq.forEach(function (v, art) { lines.push(art + ' · ' + (v.l || label(art)) + ' · ' + packTxt(packFix(v, packsOf(art)))); });
    location.href = 'kontakt.html?temat=' + encodeURIComponent(lines.join('\n')) + '#formularz';
  });
  drawRfq();
  // powrót przyciskiem „Wstecz” (strona z pamięci przeglądarki, bfcache) lub zmiana w innej karcie: wczytaj listę od nowa
  function reloadRfq() {
    rfq = new Map(); try { JSON.parse(localStorage.getItem(KEY) || '[]').forEach(function (x) { rfq.set(x[0], x[1]); }); } catch (e) {}
    drawRfq();
    if (res) $$('.add[data-art]', res).forEach(function (b) { var on = rfq.has(b.dataset.art); b.classList.toggle('is-in', on); b.textContent = on ? L('Dodano', 'Added', 'Додано') : L('Dodaj', 'Add', 'Додати'); });
  }
  window.addEventListener('pageshow', function (e) { if (e.persisted) reloadRfq(); });
  window.addEventListener('storage', function (e) { if (e.key === KEY) reloadRfq(); });
  var q0 = new URLSearchParams(location.search).get('q');
  if (q0) { qEl.value = q0; load().then(search); }
  var seria = new URLSearchParams(location.search).get('seria');
  if (seria && res) setSeries(seria.split(','));
  else if (seria) {   // bez pola wyszukiwania: otwórz linie z listy grup i przewiń do pierwszej
    var first = null;
    seria.split(',').forEach(function (id) { var d = $('details.gl[data-s="' + CSS.escape(id) + '"]'); if (d) { d.open = true; first = first || d; } });
    if (first) setTimeout(function () { first.scrollIntoView({ block: 'start' }); }, 50);
  }

  })();

  // Prefill tematu zapytania z parametru ?temat=
  // Strony grup produktów: ilość + jednostka (karton / worek / opak. / szt.) i "Dodaj" do listy do wyceny (ta sama co w katalogu)
  var qas = $$('.qty[data-add]');
  if (qas.length) (function () {
    var KEY = 'armatex-rfq', list = new Map(), gi = $('.gp__img img'), gimg = gi ? gi.getAttribute('src').replace(/^(\.\.\/)+/, '') : '';
    try { JSON.parse(localStorage.getItem(KEY) || '[]').forEach(function (x) { list.set(x[0], x[1]); }); } catch (e) {}
    function save() { try { localStorage.setItem(KEY, JSON.stringify(Array.from(list.entries()))); } catch (e) {} }
    function packs(sel) { return Array.prototype.map.call(sel.options, function (o) { return [o.dataset.u, +o.dataset.n]; }); }
    function sync() {
      qas.forEach(function (w) {
        var v = list.get(w.dataset.add), b = w.querySelector('.add'), sel = w.querySelector('select');
        if (v) { packFix(v, packs(sel)); w.querySelector('input').value = v.q; sel.value = v.u; }
        w.classList.toggle('is-in', !!v); b.classList.toggle('is-in', !!v); b.textContent = v ? L('Dodano', 'Added', 'Додано') : L('Dodaj', 'Add', 'Додати');
        b.setAttribute('aria-pressed', !!v);
      });
    }
    qas.forEach(function (w) {
      var a = w.dataset.add, inp = w.querySelector('input'), sel = w.querySelector('select');
      function cur() { return { q: Math.max(1, parseInt(inp.value, 10) || 1), l: w.dataset.l, u: +sel.value, p: packs(sel), i: gimg }; }
      w.querySelector('.add').addEventListener('click', function () {
        var added = !list.has(a);
        if (added) list.set(a, cur()); else list.delete(a);
        save(); sync(); changed(added);
      });
      function upd() { if (list.has(a)) { list.set(a, cur()); save(); changed(); } }
      inp.addEventListener('input', upd); sel.addEventListener('change', upd);
    });
    function changed(added) { document.dispatchEvent(new CustomEvent('rfq:change', { detail: { src: 'grp', added: !!added } })); }
    // zmiany z wysuwanego panelu listy (ilość, jednostka, usunięcie)
    document.addEventListener('rfq:change', function (e) {
      if (e.detail && e.detail.src === 'grp') return;
      list = new Map(); try { JSON.parse(localStorage.getItem(KEY) || '[]').forEach(function (x) { list.set(x[0], x[1]); }); } catch (err) {}
      sync();
    });
    sync();
  })();

  // Lista do wyceny na pozostałych stronach: pasek na stronach grup, mały przycisk „Lista” gdzie indziej, wysuwany panel z listą.
  // Wyszukiwarka ma własny panel listy, kontakt ma formularz: tam bez paska i panelu.
  if (!$('#rfqList') && !/\/kontakt(\.html)?$/.test(location.pathname)) (function () {
    var KEY = 'armatex-rfq', grp = !!qas.length, dr = null, opener = null;
    var fmt = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); };
    var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var poz = function (n) { var few = n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14); return EN ? (n === 1 ? 'item' : 'items') : UK ? (n === 1 ? 'позиція' : few ? 'позиції' : 'позицій') : n === 1 ? 'pozycja' : few ? 'pozycje' : 'pozycji'; };
    function read() { var m = new Map(); try { JSON.parse(localStorage.getItem(KEY) || '[]').forEach(function (x) { m.set(x[0], x[1]); }); } catch (e) {} return m; }
    function write(m) { try { localStorage.setItem(KEY, JSON.stringify(Array.from(m.entries()))); } catch (e) {} }
    function changed() { document.dispatchEvent(new CustomEvent('rfq:change', { detail: { src: 'ldr' } })); }
    function send() {
      var lines = [L('Lista pozycji do wyceny:', 'Items for quotation:', 'Позиції для розрахунку ціни:')];
      read().forEach(function (v, art) { lines.push(art + ' · ' + (v.l || '') + ' · ' + packTxt(packFix(v))); });
      location.href = 'kontakt.html?temat=' + encodeURIComponent(lines.join('\n')) + '#formularz';
    }

    // przycisk / pasek
    var bar = document.createElement('div');
    if (grp) {
      bar.className = 'lbar';
      bar.innerHTML = '<p class="lbar__t" aria-live="polite"><span class="lbar__l">' + L('Lista', 'List', 'Список') + '</span> <span class="lbar__n">0</span> <span class="lbar__w">' + L('pozycji', 'items', 'поз.') + '</span> <small>' + L('na liście do wyceny', 'on your quote list', 'у списку для розрахунку ціни') + '</small></p>' +
        '<button class="lbar__show" type="button" aria-haspopup="dialog">' + L('Pokaż listę', 'Show list', 'Показати список') + '</button>' +
        '<button class="mag lbar__send" type="button"><span>' + L('Wyślij zapytanie<span class="lbar__x"> o wycenę</span>', 'Send<span class="lbar__x"> quote</span> request', 'Надіслати<span class="lbar__x"> запит</span>') + '</span></button>';
      $('.lbar__send', bar).addEventListener('click', send);
    } else {
      bar.innerHTML = '<button class="pill" type="button" aria-haspopup="dialog">' + L('Lista', 'List', 'Список') + ' <span class="lbar__n">0</span></button>';
    }
    document.body.appendChild(bar);
    $('button', bar).addEventListener('click', function (e) { open(e.currentTarget); });
    $$('[data-ldr]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); open(a); }); });

    function draw(bump, keep) {
      var m = read(), n = m.size;
      $('.lbar__n', bar).textContent = n;
      if (grp) {
        $('.lbar__w', bar).textContent = poz(n);
        bar.classList.toggle('on', n > 0); document.body.classList.toggle('has-lbar', n > 0);
        if (bump && !reduce) { bar.classList.remove('bump'); void bar.offsetWidth; bar.classList.add('bump'); }
      } else bar.firstChild.classList.toggle('on', n > 0);
      if (!dr) return;
      $('.ldr__n', dr).textContent = n + L(' poz.', ' items', ' поз.');
      $('.ldr__send', dr).disabled = !n;
      if (keep) return;   // edycja w panelu: nie przebudowuj listy, żeby nie zgubić kursora w polu ilości
      var h = '';
      m.forEach(function (v, art) {
        packFix(v);
        var opts = v.p.map(function (u, i) { return '<option value="' + i + '"' + (i === v.u ? ' selected' : '') + '>' + esc(UN(u[0])) + (u[1] > 1 ? ' (' + fmt(u[1]) + ' ' + UN('szt.') + ')' : '') + '</option>'; }).join('');
        h += '<li>' + thumb(v.i) + '<div><code>' + esc(art) + '</code><small>' + esc(v.l || '') + '</small></div>' +
          '<button class="rm" type="button" data-art="' + esc(art) + '" aria-label="' + L('Usuń ', 'Remove ', 'Видалити ') + esc(art) + '">×</button>' +
          '<div class="rfq__q"><input type="number" min="1" step="1" value="' + v.q + '" aria-label="' + L('Ilość ', 'Quantity ', 'Кількість ') + esc(art) + '" data-art="' + esc(art) + '">' +
          '<select aria-label="' + L('Jednostka ', 'Unit ', 'Одиниця ') + esc(art) + '" data-art="' + esc(art) + '">' + opts + '</select>' +
          '<span class="tot">' + (v.p[v.u][1] > 1 ? '= ' + fmt(v.q * v.p[v.u][1]) + ' ' + UN('szt.') : '') + '</span></div></li>';
      });
      $('ul', dr).innerHTML = h;
      $('.ldr__hint', dr).textContent = n ? L('Ustaw ilość i jednostkę (karton, worek, sztuki), potem wyślij zapytanie.', 'Set the quantity and unit (box, bag, pieces), then send the enquiry.', 'Вкажіть кількість і одиницю (коробка, мішок, штуки), потім надішліть запит.') : L('Twoja lista jest pusta. Otwórz linię produktów i dodaj rozmiary na stronie grupy.', 'Your list is empty. Open a product line and add sizes on the product group page.', 'Ваш список порожній. Відкрийте лінію продукції та додайте розміри на сторінці групи.');
      $('.ldr__more', dr).hidden = grp && n > 0;
    }
    function build() {
      dr = document.createElement('div');
      dr.className = 'ldr';
      dr.innerHTML = '<div class="ldr__bg" data-x></div>' +
        '<aside class="rfq ldr__p" role="dialog" aria-modal="true" aria-labelledby="ldrT">' +
        '<div class="ldr__h"><h2 id="ldrT">' + L('Lista do wyceny', 'Quote list', 'Список для розрахунку ціни') + ' <span class="label ldr__n">0</span></h2><button class="ldr__x" type="button" data-x aria-label="' + L('Zamknij listę', 'Close list', 'Закрити список') + '">×</button></div>' +
        '<p class="ldr__hint"></p><ul></ul>' +
        '<button class="mag ldr__send" type="button"><span>' + L('Wyślij zapytanie o wycenę', 'Send quote request', 'Надіслати запит ціни') + '</span></button>' +
        '<p class="ldr__more"><a class="ulink" href="wyszukiwarka.html">' + L('Przejdź do wyszukiwarki produktów', 'Go to the product finder', 'Перейти до пошуку продукції') + '</a></p>' +
        '<p class="rfq__help">' + L('Nie wiesz, co wybrać? <a href="tel:+48513191502">Zadzwoń: 513 191 502</a>', 'Not sure what to choose? <a href="tel:+48513191502">Call +48 513 191 502</a>', 'Не знаєте, що вибрати? <a href="tel:+48513191502">Телефонуйте: +48 513 191 502</a>') + '</p></aside>';
      document.body.appendChild(dr);
      $$('[data-x]', dr).forEach(function (x) { x.addEventListener('click', close); });
      $('.ldr__send', dr).addEventListener('click', send);
      var ul = $('ul', dr);
      function upd(e) {
        var i = e.target, m = read(), v = i.dataset.art && m.get(i.dataset.art); if (!v) return;
        packFix(v);
        if (i.tagName === 'SELECT') v.u = +i.value; else v.q = Math.max(1, parseInt(i.value, 10) || 1);
        write(m); changed();
        var t = i.parentNode.querySelector('.tot'), k = v.p[v.u][1];
        t.textContent = k > 1 ? '= ' + fmt(v.q * k) + ' ' + UN('szt.') : '';
      }
      ul.addEventListener('input', upd); ul.addEventListener('change', upd);
      ul.addEventListener('click', function (e) {
        var b = e.target.closest('.rm'); if (!b) return;
        var m = read(); m.delete(b.dataset.art); write(m); changed(); draw();
        var f = $('.rm', ul) || $('.ldr__x', dr); f.focus();
      });
      dr.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') return close();
        if (e.key !== 'Tab') return;
        var f = $$('button:not([disabled]), a[href], input, select', $('.ldr__p', dr)), a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
      });
    }
    // pozycje dodane przed wprowadzeniem miniatur: zdjęcie grupy z danych katalogu
    var imgs = null;
    function fillImgs() {
      var m = read(), miss = []; m.forEach(function (v, art) { if (!v.i) miss.push(art); });
      if (!miss.length || imgs) return;
      imgs = fetch(BASE + 'data/katalog.json').then(function (r) { return r.json(); }).then(function (d) {
        var by = {}; d.rows.forEach(function (r) { by[r[1]] = d.groups[r[0]][4]; });
        var m2 = read(), ch = false;
        m2.forEach(function (v, art) { if (!v.i && by[art]) { v.i = by[art]; ch = true; } });
        if (ch) { write(m2); draw(); changed(); }
      }).catch(function () { imgs = null; });
    }
    function open(from) {
      if (!dr) build();
      opener = from; draw(); fillImgs();
      document.documentElement.classList.add('ldr-open');
      dr.classList.add('on');
      setTimeout(function () { $('.ldr__x', dr).focus(); }, 30);
    }
    function close() {
      dr.classList.remove('on'); document.documentElement.classList.remove('ldr-open');
      if (opener && opener.isConnected) opener.focus();
    }
    document.addEventListener('rfq:change', function (e) { var d = e.detail || {}; draw(d.added, d.src === 'ldr'); });
    // zmiana listy w innej karcie przeglądarki
    window.addEventListener('storage', function (e) { if (e.key === KEY) { draw(); document.dispatchEvent(new CustomEvent('rfq:change', { detail: { src: 'ldr' } })); } });
    draw();
  })();

  // strony grup i panel listy: po powrocie przyciskiem „Wstecz” (bfcache) odśwież stan listy z pamięci przeglądarki
  window.addEventListener('pageshow', function (e) { if (e.persisted) document.dispatchEvent(new CustomEvent('rfq:change', { detail: { src: 'bf' } })); });

  // Strony systemów: klik w wiersz linii (lub „Produkty ▾”) rozwija pełną listę produktów pod nim
  $$('tr.sy-line.has-prod').forEach(function (tr) {
    var more = tr.nextElementSibling && $('.sy-more', tr.nextElementSibling), btn = $('button.sy-find', tr);
    if (!more) return;
    function sync() { if (btn) btn.setAttribute('aria-expanded', more.open); }
    tr.addEventListener('click', function (e) { if (e.target.closest('a')) return; more.open = !more.open; });
    more.addEventListener('toggle', sync);
  });

  // Do pobrania: filtr po rodzaju i marce
  var dll = $('#dll');
  if (dll) (function () {
    var f = { t: '', b: '' };
    function apply() {
      var n = 0;
      $$('li', dll).forEach(function (li) {
        var ok = (!f.t || li.dataset.t === f.t) && (!f.b || li.dataset.b.split(' ').indexOf(f.b) !== -1);
        li.hidden = !ok; if (ok) n++;
      });
      $('#dllNone').hidden = n > 0;
    }
    $$('.dlf .chip').forEach(function (c) {
      c.addEventListener('click', function () {
        var k = c.dataset.t !== undefined ? 't' : 'b';
        f[k] = c.dataset[k];
        $$('.dlf .chip[data-' + k + ']').forEach(function (x) { x.setAttribute('aria-pressed', x === c); });
        apply();
      });
    });
    // ?rodzaj=katalog (np. link „Katalogi PDF” z wyszukiwarki) ustawia filtr od razu
    var t0 = new URLSearchParams(location.search).get('rodzaj'), c0 = t0 && $('.dlf .chip[data-t="' + CSS.escape(t0) + '"]');
    if (c0) c0.click();
  })();

  var m = $('#m');
  if (m) {
    var temat = new URLSearchParams(location.search).get('temat');
    if (temat) m.value = temat;
    $$('[data-topic]').forEach(function (a) { a.addEventListener('click', function () { m.value = a.dataset.topic; }); });
  }
  // Formularz: walidacja i wysyłka do Netlify Forms (AJAX), bez przeładowania strony
  var form = $('#form');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var st = $('#fs'), bad = null;
    st.className = 'form__s';
    var msg = [];
    $$('[required]', form).forEach(function (i) {
      var val = i.value.trim(), v = i.type === 'checkbox' ? i.checked : val !== '', why = '';
      if (v && i.type === 'email' && !/^[^\s@]+@[^\s@.]+(\.[^\s@.]+)*\.[a-z]{2,}$/i.test(val)) { v = false; why = L('Podaj poprawny adres e-mail, np. jan@firma.pl.', 'Enter a valid e-mail address, e.g. john@company.com.', 'Вкажіть правильну адресу e-mail, напр. ivan@firma.pl.'); }
      if (v && i.type === 'tel' && val.replace(/\D/g, '').length < 9) { v = false; why = L('Podaj numer telefonu (co najmniej 9 cyfr).', 'Enter a phone number (at least 9 digits).', 'Вкажіть номер телефону (щонайменше 9 цифр).'); }
      if (!v && !why) why = i.type === 'checkbox' ? L('Zaznacz zgodę na przetwarzanie danych.', 'Please tick the consent to data processing.', 'Позначте згоду на обробку даних.') : '';
      var f = i.closest('.f'); if (f) f.classList.toggle('is-bad', !v);
      i.setAttribute('aria-invalid', !v);
      if (!v) { if (!bad) bad = i; if (why) msg.push(why); }
    });
    if (bad) {
      var empty = $$('[required]', form).some(function (i) { return i.type !== 'checkbox' && !i.value.trim(); });
      if (empty) msg.unshift(L('Uzupełnij pola oznaczone gwiazdką.', 'Please fill in the fields marked with an asterisk.', 'Заповніть поля, позначені зірочкою.'));
      st.classList.add('is-err'); st.textContent = msg.join(' '); bad.focus(); return;
    }
    var btn = form.querySelector('button[type=submit]');
    btn.disabled = true; st.textContent = L('Wysyłanie…', 'Sending…', 'Надсилання…');
    fetch('/', {
      method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString()
    }).then(function (r) { if (!r.ok) throw new Error('http ' + r.status); })
      .then(function () {
        form.reset(); st.classList.add('is-ok');
        st.textContent = L('Dziękujemy. Zapytanie dotarło, odpowiemy w ciągu jednego dnia roboczego.', 'Thank you. Your enquiry has been received; we will reply within one working day.', 'Дякуємо. Запит отримано, відповімо протягом одного робочого дня.');
        try { localStorage.removeItem('armatex-rfq'); } catch (err) {}
      })
      .catch(function () { st.classList.add('is-err'); st.textContent = L('Nie udało się wysłać formularza. Napisz na biuro@armatex.pl lub zadzwoń: 513 191 502.', 'The form could not be sent. Please e-mail biuro@armatex.pl or call +48 513 191 502.', 'Не вдалося надіслати форму. Напишіть на biuro@armatex.pl або зателефонуйте: +48 513 191 502.'); })
      .then(function () { btn.disabled = false; });
  });
})();
// Wykresy: dymek z wartością przy słupku (hover i fokus klawiatury)
(function(){var tip=document.querySelector('.ctip');if(!tip)return;var b=tip.querySelector('b'),s=tip.querySelector('span');
function show(e,el){var p=el.dataset.tip.split('|');b.textContent=p[2];s.textContent=[p[0],p[1]].filter(Boolean).join(' · ');tip.hidden=false;var r=el.getBoundingClientRect();var x=e&&e.clientX?e.clientX:r.right,y=e&&e.clientY?e.clientY:r.top;tip.style.left=Math.min(x+12,innerWidth-tip.offsetWidth-8)+'px';tip.style.top=(y-tip.offsetHeight-10)+'px';}
document.querySelectorAll('.cb[data-tip]').forEach(function(el){el.addEventListener('pointermove',function(e){show(e,el)});el.addEventListener('focus',function(){show(null,el)});el.addEventListener('pointerleave',function(){tip.hidden=true});el.addEventListener('blur',function(){tip.hidden=true});});})();
