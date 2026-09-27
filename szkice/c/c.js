/* Szkic C · wspólny skrypt stron (roboczy, niepublikowany) */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var BASE = document.body.getAttribute('data-base') || '';
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

  // Menu: rozwijana oferta i menu mobilne
  var dd = $('.dd');
  if (dd) {
    var ddb = $('button', dd);
    ddb.addEventListener('click', function () { var o = dd.classList.toggle('open'); ddb.setAttribute('aria-expanded', o); });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) { dd.classList.remove('open'); ddb.setAttribute('aria-expanded', false); } });
    dd.addEventListener('keydown', function (e) { if (e.key === 'Escape') { dd.classList.remove('open'); ddb.setAttribute('aria-expanded', false); ddb.focus(); } });
  }
  var burger = $('#burger');
  if (burger) burger.addEventListener('click', function () {
    var o = document.body.classList.toggle('menu-open'); burger.setAttribute('aria-expanded', o);
    burger.setAttribute('aria-label', o ? 'Zamknij menu' : 'Otwórz menu');
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
      if (n - i > 1 && (n - i - 1) % 3 === 0) { var s = document.createElement('span'); s.className = 'odo-s'; o.appendChild(s); }
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

  // Systemy: rozsuwane kafelki (BYQ Expanding Panels). Na dotyku pierwsze stuknięcie otwiera kafelek, drugie przechodzi do systemu.
  var panels = $$('.panel');
  function openPanel(p) { panels.forEach(function (x) { x.classList.toggle('is-open', x === p); }); }
  panels.forEach(function (p) {
    p.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') openPanel(p); });
    p.addEventListener('focus', function () { if (p.matches(':focus-visible')) openPanel(p); });
    p.addEventListener('click', function (e) {
      if (!p.classList.contains('is-open') && innerWidth > 900) { e.preventDefault(); openPanel(p); }
    });
  });

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

  if ($('#q')) (function () {
  // ===== Katalog Besco: wyszukiwarka + zapytanie =====
  var DATA = null, INDEX = null, loading = null, page = 0, PER = 24, hits = [];
  var active = new Set(), qEl = $('#q'), res = $('#res'), cnt = $('#cnt'), more = $('#more');
  var fmt = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); };
  var norm = function (s) {
    return s.toLowerCase().replace(/[″"]/g, '').replace(/×/g, 'x').replace(/\s*x\s*/g, 'x').replace(/,/g, '.')
      .replace(/ą/g, 'a').replace(/ć/g, 'c').replace(/ę/g, 'e').replace(/ł/g, 'l').replace(/ń/g, 'n').replace(/ó/g, 'o').replace(/ś/g, 's').replace(/[źż]/g, 'z')
      .replace(/\s+/g, ' ').trim();
  };
  var squash = function (s) { return s.toLowerCase().replace(/[\s\-.]/g, ''); };
  function load() {
    if (loading) return loading;
    loading = fetch(BASE + 'data/besco-2026.json').then(function (r) { return r.json(); }).then(function (d) {
      DATA = d;
      INDEX = d.rows.map(function (r) {
        var g = d.groups[r[0]], s = d.series[g[0]];
        return { r: r, g: g, s: s, sid: s.id, hay: norm([r[1], r[2], g[2], g[3], g[1], s.short].join(' ')), art: squash(r[1]) };
      });
      search();
    }).catch(function () { res.innerHTML = '<li class="fd__empty" style="display:block">Nie udało się wczytać katalogu. Odśwież stronę.</li>'; });
    return loading;
  }
  new IntersectionObserver(function (e, o) { if (e[0].isIntersecting) { load(); o.disconnect(); } }, { rootMargin: '600px 0px' }).observe($('#katalog'));
  qEl.addEventListener('focus', load);

  function search() {
    if (!INDEX) return;
    var q = norm(qEl.value), toks = q ? q.split(' ') : [], qa = squash(qEl.value);
    hits = INDEX.filter(function (x) {
      if (active.size && !active.has(x.sid)) return false;
      if (!toks.length) return true;
      if (qa.length > 3 && x.art.indexOf(qa) === 0) return true;
      return toks.every(function (t) { return x.hay.indexOf(t) !== -1 || x.art.indexOf(squash(t)) !== -1; });
    });
    if (qa) hits.sort(function (a, b) { return (b.art === qa) - (a.art === qa); });
    page = 0; res.innerHTML = ''; render();
    cnt.textContent = (toks.length || active.size) ? fmt(hits.length) + ' z ' + fmt(INDEX.length) + ' pozycji' : fmt(INDEX.length) + ' pozycji w katalogu';
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function render() {
    var slice = hits.slice(page * PER, (page + 1) * PER), h = '';
    if (!hits.length) { res.innerHTML = '<li class="fd__empty" style="display:block">Brak pozycji dla tego zapytania. Sprawdź numer albo zadzwoń: 798 807 106.</li>'; more.hidden = true; return; }
    slice.forEach(function (x) {
      var r = x.r, g = x.g, inq = rfq.has(r[1]);
      h += '<li><img src="' + BASE + 'img/besco/' + g[4] + '.webp" alt="" width="56" height="56" loading="lazy" decoding="async">' +
        '<div><b>' + esc(g[2]) + '</b><span class="sz">' + esc(r[2]) + '</span><small>' + esc(g[3]) + ' · ' + esc(x.s.short) + '</small></div>' +
        '<code>' + esc(r[1]) + '</code>' +
        '<span class="pk"><i>worek / karton</i>' + r[3] + ' / ' + fmt(r[4]) + '</span>' +
        '<button class="add' + (inq ? ' is-in' : '') + '" type="button" data-art="' + esc(r[1]) + '" aria-label="Dodaj ' + esc(r[1]) + ' do zapytania">' + (inq ? 'Dodano' : 'Dodaj') + '</button></li>';
    });
    res.insertAdjacentHTML('beforeend', h);
    page++; more.hidden = page * PER >= hits.length;
    more.firstElementChild.textContent = 'Pokaż kolejne (' + fmt(hits.length - page * PER) + ')';
  }
  var t0; qEl.addEventListener('input', function () { clearTimeout(t0); t0 = setTimeout(function () { load().then(search); }, 120); });
  more.firstElementChild.addEventListener('click', render);
  $$('.fd__hint code').forEach(function (c) { c.addEventListener('click', function () { qEl.value = c.dataset.q; load().then(search); }); });
  function setSeries(list) {
    active = new Set(list.filter(Boolean));
    $$('.chip').forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.s ? active.has(c.dataset.s) : !active.size); });
    load().then(search);
  }
  $$('.chip').forEach(function (c) {
    c.addEventListener('click', function () {
      if (!c.dataset.s) return setSeries([]);
      var s = new Set(active); s.has(c.dataset.s) ? s.delete(c.dataset.s) : s.add(c.dataset.s); setSeries(Array.from(s));
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
    for (var i = 0; i < INDEX.length; i++) if (INDEX[i].r[1] === art) return INDEX[i].g[2] + ' ' + INDEX[i].r[2];
    return '';
  }
  function drawRfq() {
    var ul = $('#rfqList'), h = '', n = rfq.size;
    rfq.forEach(function (v, art) {
      h += '<li><div><code>' + esc(art) + '</code><small>' + esc(v.l || label(art)) + '</small></div>' +
        '<input type="number" min="1" step="1" value="' + v.q + '" aria-label="Ilość ' + esc(art) + '" data-art="' + esc(art) + '">' +
        '<button class="rm" type="button" data-art="' + esc(art) + '" aria-label="Usuń ' + esc(art) + '">×</button></li>';
    });
    ul.innerHTML = h;
    $('#rfqN').textContent = n + ' poz.'; $('#pillN').textContent = n;
    $('#pill').classList.toggle('on', n > 0);
    $('#toForm').disabled = !n;
    $('#rfqHint').textContent = n ? 'Sprawdź ilości i przenieś listę do formularza.' : 'Dodaj pozycje z listy. Ilości zmienisz tutaj.';
  }
  res.addEventListener('click', function (e) {
    var b = e.target.closest('.add'); if (!b) return;
    var art = b.dataset.art;
    if (rfq.has(art)) rfq.delete(art); else rfq.set(art, { q: 1, l: label(art) });
    b.classList.toggle('is-in', rfq.has(art)); b.textContent = rfq.has(art) ? 'Dodano' : 'Dodaj';
    save(); drawRfq();
  });
  $('#rfqList').addEventListener('input', function (e) {
    var i = e.target; if (!i.dataset.art) return;
    var v = rfq.get(i.dataset.art); if (v) { v.q = Math.max(1, parseInt(i.value, 10) || 1); save(); }
  });
  $('#rfqList').addEventListener('click', function (e) {
    var b = e.target.closest('.rm'); if (!b) return;
    rfq.delete(b.dataset.art); save(); drawRfq();
    var btn = res.querySelector('.add[data-art="' + CSS.escape(b.dataset.art) + '"]'); if (btn) { btn.classList.remove('is-in'); btn.textContent = 'Dodaj'; }
  });
  $('#toForm').addEventListener('click', function () {
    var lines = ['Lista indeksów do wyceny (katalog Besco 2026):'];
    rfq.forEach(function (v, art) { lines.push(art + ' · ' + (v.l || label(art)) + ' · ' + v.q + ' szt.'); });
    location.href = 'kontakt.html?temat=' + encodeURIComponent(lines.join('\n')) + '#formularz';
  });
  drawRfq();
  var seria = new URLSearchParams(location.search).get('seria');
  if (seria) setSeries(seria.split(','));

  })();

  // Prefill z "Poproś o dostęp" i nieaktywny formularz szkicu
  var m = $('#m');
  if (m) {
    var temat = new URLSearchParams(location.search).get('temat');
    if (temat) m.value = temat;
    $$('[data-topic]').forEach(function (a) { a.addEventListener('click', function () { m.value = a.dataset.topic; }); });
  }
  if ($('#form')) $('#form').addEventListener('submit', function (e) { e.preventDefault(); $('#fs').textContent = 'To szkic: formularz jest nieaktywny, nic nie zostało wysłane.'; });
})();
