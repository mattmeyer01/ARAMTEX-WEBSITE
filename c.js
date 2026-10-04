/* Armatex · wspólny skrypt stron */
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
    if (n === 1) return v.q + ' szt.';
    return v.q + ' × ' + u[0] + ' (' + n + ' szt.) = ' + String(v.q * n).replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' szt.';
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
    }).catch(function () { if (res) res.innerHTML = '<li class="fd__empty" style="display:block">Nie udało się wczytać katalogu. Odśwież stronę.</li>'; });
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
    cnt.textContent = fmt(hits.length) + ' z ' + fmt(INDEX.length) + ' pozycji';
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function render() {
    var slice = hits.slice(page * PER, (page + 1) * PER), h = '';
    if (!hits.length) { res.innerHTML = '<li class="fd__empty" style="display:block">Brak pozycji dla tego zapytania. Sprawdź numer albo zadzwoń: 513 191 502.</li>'; more.hidden = true; return; }
    slice.forEach(function (x) {
      var r = x.r, g = x.g, inq = rfq.has(r[1]), pk = r[3].slice().reverse();
      h += '<li><img src="' + BASE + esc(g[4]) + '" alt="" width="56" height="56" loading="lazy" decoding="async">' +
        '<div><b><a href="' + BASE + esc(g[5]) + '">' + esc(g[2]) + '</a></b><span class="sz">' + esc(r[2]) + '</span><small>' + esc(g[3] ? g[3] + ' · ' : '') + esc(x.s.short) + '</small></div>' +
        '<code>' + esc(r[1]) + '</code>' +
        '<span class="pk">' + (pk.length ? '<i>' + pk.map(function (u) { return esc(u[0]); }).join(' / ') + '</i>' + pk.map(function (u) { return fmt(u[1]); }).join(' / ') : '') + '</span>' +
        '<button class="add' + (inq ? ' is-in' : '') + '" type="button" data-art="' + esc(r[1]) + '" aria-label="Dodaj ' + esc(r[1]) + ' do zapytania">' + (inq ? 'Dodano' : 'Dodaj') + '</button></li>';
    });
    res.insertAdjacentHTML('beforeend', h);
    page++; more.hidden = page * PER >= hits.length;
    more.firstElementChild.textContent = 'Pokaż kolejne (' + fmt(hits.length - page * PER) + ')';
  }
  var t0; qEl.addEventListener('input', function () { clearTimeout(t0); t0 = setTimeout(function () { load().then(search); }, 120); });
  if (more) more.firstElementChild.addEventListener('click', render);
  $$('.fd__hint code').forEach(function (c) { c.addEventListener('click', function () { qEl.value = c.dataset.q; load().then(search); }); });
  var flt = $('#flt');
  function drawFilter() {
    if (!flt) return;
    if (!active.size || !DATA) { flt.hidden = true; return; }
    var names = DATA.series.filter(function (x) { return active.has(x.id); }).map(function (x) { return x.short; });
    flt.innerHTML = '<span class="label">Filtr</span> <span></span> <button type="button">Wyczyść filtr ×</button>';
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
    for (var i = 0; i < INDEX.length; i++) if (INDEX[i].r[1] === art) return INDEX[i].g[2] + ' ' + INDEX[i].r[2];
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
      var opts = v.p.map(function (u, i) { return '<option value="' + i + '"' + (i === v.u ? ' selected' : '') + '>' + esc(u[0]) + (u[1] > 1 ? ' (' + fmt(u[1]) + ' szt.)' : '') + '</option>'; }).join('');
      if (!v.i && INDEX) v.i = imgOf(art);
      h += '<li>' + thumb(v.i) + '<div><code>' + esc(art) + '</code><small>' + esc(v.l || label(art)) + '</small></div>' +
        '<button class="rm" type="button" data-art="' + esc(art) + '" aria-label="Usuń ' + esc(art) + '">×</button>' +
        '<div class="rfq__q"><input type="number" min="1" step="1" value="' + v.q + '" aria-label="Ilość ' + esc(art) + '" data-art="' + esc(art) + '">' +
        '<select aria-label="Jednostka ' + esc(art) + '" data-art="' + esc(art) + '">' + opts + '</select>' +
        '<span class="tot">' + (v.p[v.u][1] > 1 ? '= ' + fmt(v.q * v.p[v.u][1]) + ' szt.' : '') + '</span></div></li>';
    });
    ul.innerHTML = h;
    $('#rfqN').textContent = n + ' poz.'; $('#pillN').textContent = n;
    $('#pill').classList.toggle('on', n > 0);
    $('#toForm').disabled = !n;
    $('#rfqHint').textContent = n ? 'Ustaw ilość i jednostkę (karton, worek, sztuki), potem wyślij zapytanie.' : 'Twoja lista jest pusta. Otwórz linię produktów i dodaj rozmiary na stronie grupy.';
  }
  if (res) res.addEventListener('click', function (e) {
    var b = e.target.closest('.add'); if (!b) return;
    var art = b.dataset.art;
    if (rfq.has(art)) rfq.delete(art); else { var nv = packFix({ q: 1, l: label(art), i: imgOf(art) }, packsOf(art)); nv.u = 0; rfq.set(art, nv); }
    b.classList.toggle('is-in', rfq.has(art)); b.textContent = rfq.has(art) ? 'Dodano' : 'Dodaj';
    save(); drawRfq();
  });
  function upd(e) {
    var i = e.target, v = i.dataset.art && rfq.get(i.dataset.art); if (!v) return;
    if (i.tagName === 'SELECT') v.u = +i.value; else v.q = Math.max(1, parseInt(i.value, 10) || 1);
    save();
    var t = i.parentNode.querySelector('.tot'), n = v.p[v.u][1];
    t.textContent = n > 1 ? '= ' + fmt(v.q * n) + ' szt.' : '';
  }
  $('#rfqList').addEventListener('input', upd);
  $('#rfqList').addEventListener('change', upd);
  $('#rfqList').addEventListener('click', function (e) {
    var b = e.target.closest('.rm'); if (!b) return;
    rfq.delete(b.dataset.art); save(); drawRfq();
    var btn = res && res.querySelector('.add[data-art="' + CSS.escape(b.dataset.art) + '"]'); if (btn) { btn.classList.remove('is-in'); btn.textContent = 'Dodaj'; }
  });
  $('#toForm').addEventListener('click', function () {
    var lines = ['Lista pozycji do wyceny:'];
    rfq.forEach(function (v, art) { lines.push(art + ' · ' + (v.l || label(art)) + ' · ' + packTxt(packFix(v, packsOf(art)))); });
    location.href = 'kontakt.html?temat=' + encodeURIComponent(lines.join('\n')) + '#formularz';
  });
  drawRfq();
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
    var KEY = 'armatex-rfq', list = new Map(), gi = $('.gp__img img'), gimg = gi ? gi.getAttribute('src') : '';
    try { JSON.parse(localStorage.getItem(KEY) || '[]').forEach(function (x) { list.set(x[0], x[1]); }); } catch (e) {}
    function save() { try { localStorage.setItem(KEY, JSON.stringify(Array.from(list.entries()))); } catch (e) {} }
    function packs(sel) { return Array.prototype.map.call(sel.options, function (o) { return [o.dataset.u, +o.dataset.n]; }); }
    function sync() {
      qas.forEach(function (w) {
        var v = list.get(w.dataset.add), b = w.querySelector('.add'), sel = w.querySelector('select');
        if (v) { packFix(v, packs(sel)); w.querySelector('input').value = v.q; sel.value = v.u; }
        w.classList.toggle('is-in', !!v); b.classList.toggle('is-in', !!v); b.textContent = v ? 'Dodano' : 'Dodaj';
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
    var poz = function (n) { return n === 1 ? 'pozycja' : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)) ? 'pozycje' : 'pozycji'; };
    function read() { var m = new Map(); try { JSON.parse(localStorage.getItem(KEY) || '[]').forEach(function (x) { m.set(x[0], x[1]); }); } catch (e) {} return m; }
    function write(m) { try { localStorage.setItem(KEY, JSON.stringify(Array.from(m.entries()))); } catch (e) {} }
    function changed() { document.dispatchEvent(new CustomEvent('rfq:change', { detail: { src: 'ldr' } })); }
    function send() {
      var lines = ['Lista pozycji do wyceny:'];
      read().forEach(function (v, art) { lines.push(art + ' · ' + (v.l || '') + ' · ' + packTxt(packFix(v))); });
      location.href = 'kontakt.html?temat=' + encodeURIComponent(lines.join('\n')) + '#formularz';
    }

    // przycisk / pasek
    var bar = document.createElement('div');
    if (grp) {
      bar.className = 'lbar';
      bar.innerHTML = '<p class="lbar__t" aria-live="polite"><span class="lbar__l">Lista</span> <span class="lbar__n">0</span> <span class="lbar__w">pozycji</span> <small>na liście do wyceny</small></p>' +
        '<button class="lbar__show" type="button" aria-haspopup="dialog">Pokaż listę</button>' +
        '<button class="mag lbar__send" type="button"><span>Wyślij zapytanie<span class="lbar__x"> o wycenę</span></span></button>';
      $('.lbar__send', bar).addEventListener('click', send);
    } else {
      bar.innerHTML = '<button class="pill" type="button" aria-haspopup="dialog">Lista <span class="lbar__n">0</span></button>';
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
      $('.ldr__n', dr).textContent = n + ' poz.';
      $('.ldr__send', dr).disabled = !n;
      if (keep) return;   // edycja w panelu: nie przebudowuj listy, żeby nie zgubić kursora w polu ilości
      var h = '';
      m.forEach(function (v, art) {
        packFix(v);
        var opts = v.p.map(function (u, i) { return '<option value="' + i + '"' + (i === v.u ? ' selected' : '') + '>' + esc(u[0]) + (u[1] > 1 ? ' (' + fmt(u[1]) + ' szt.)' : '') + '</option>'; }).join('');
        h += '<li>' + thumb(v.i) + '<div><code>' + esc(art) + '</code><small>' + esc(v.l || '') + '</small></div>' +
          '<button class="rm" type="button" data-art="' + esc(art) + '" aria-label="Usuń ' + esc(art) + '">×</button>' +
          '<div class="rfq__q"><input type="number" min="1" step="1" value="' + v.q + '" aria-label="Ilość ' + esc(art) + '" data-art="' + esc(art) + '">' +
          '<select aria-label="Jednostka ' + esc(art) + '" data-art="' + esc(art) + '">' + opts + '</select>' +
          '<span class="tot">' + (v.p[v.u][1] > 1 ? '= ' + fmt(v.q * v.p[v.u][1]) + ' szt.' : '') + '</span></div></li>';
      });
      $('ul', dr).innerHTML = h;
      $('.ldr__hint', dr).textContent = n ? 'Ustaw ilość i jednostkę (karton, worek, sztuki), potem wyślij zapytanie.' : 'Twoja lista jest pusta. Otwórz linię produktów i dodaj rozmiary na stronie grupy.';
      $('.ldr__more', dr).hidden = grp && n > 0;
    }
    function build() {
      dr = document.createElement('div');
      dr.className = 'ldr';
      dr.innerHTML = '<div class="ldr__bg" data-x></div>' +
        '<aside class="rfq ldr__p" role="dialog" aria-modal="true" aria-labelledby="ldrT">' +
        '<div class="ldr__h"><h2 id="ldrT">Lista do wyceny <span class="label ldr__n">0 poz.</span></h2><button class="ldr__x" type="button" data-x aria-label="Zamknij listę">×</button></div>' +
        '<p class="ldr__hint"></p><ul></ul>' +
        '<button class="mag ldr__send" type="button"><span>Wyślij zapytanie o wycenę</span></button>' +
        '<p class="ldr__more"><a class="ulink" href="wyszukiwarka.html">Przejdź do wyszukiwarki produktów</a></p>' +
        '<p class="rfq__help">Nie wiesz, co wybrać? <a href="tel:+48513191502">Zadzwoń: 513 191 502</a></p></aside>';
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
        t.textContent = k > 1 ? '= ' + fmt(v.q * k) + ' szt.' : '';
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
      if (v && i.type === 'email' && !/^[^\s@]+@[^\s@.]+(\.[^\s@.]+)*\.[a-z]{2,}$/i.test(val)) { v = false; why = 'Podaj poprawny adres e-mail, np. jan@firma.pl.'; }
      if (v && i.type === 'tel' && val.replace(/\D/g, '').length < 9) { v = false; why = 'Podaj numer telefonu (co najmniej 9 cyfr).'; }
      if (!v && !why) why = i.type === 'checkbox' ? 'Zaznacz zgodę na przetwarzanie danych.' : '';
      var f = i.closest('.f'); if (f) f.classList.toggle('is-bad', !v);
      i.setAttribute('aria-invalid', !v);
      if (!v) { if (!bad) bad = i; if (why) msg.push(why); }
    });
    if (bad) {
      var empty = $$('[required]', form).some(function (i) { return i.type !== 'checkbox' && !i.value.trim(); });
      if (empty) msg.unshift('Uzupełnij pola oznaczone gwiazdką.');
      st.classList.add('is-err'); st.textContent = msg.join(' '); bad.focus(); return;
    }
    var btn = form.querySelector('button[type=submit]');
    btn.disabled = true; st.textContent = 'Wysyłanie…';
    fetch('/', {
      method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString()
    }).then(function (r) { if (!r.ok) throw new Error('http ' + r.status); })
      .then(function () {
        form.reset(); st.classList.add('is-ok');
        st.textContent = 'Dziękujemy. Zapytanie dotarło, odpowiemy w ciągu jednego dnia roboczego.';
        try { localStorage.removeItem('armatex-rfq'); } catch (err) {}
      })
      .catch(function () { st.classList.add('is-err'); st.textContent = 'Nie udało się wysłać formularza. Napisz na biuro@armatex.pl lub zadzwoń: 513 191 502.'; })
      .then(function () { btn.disabled = false; });
  });
})();
// Wykresy: dymek z wartością przy słupku (hover i fokus klawiatury)
(function(){var tip=document.querySelector('.ctip');if(!tip)return;var b=tip.querySelector('b'),s=tip.querySelector('span');
function show(e,el){var p=el.dataset.tip.split('|');b.textContent=p[2];s.textContent=[p[0],p[1]].filter(Boolean).join(' · ');tip.hidden=false;var r=el.getBoundingClientRect();var x=e&&e.clientX?e.clientX:r.right,y=e&&e.clientY?e.clientY:r.top;tip.style.left=Math.min(x+12,innerWidth-tip.offsetWidth-8)+'px';tip.style.top=(y-tip.offsetHeight-10)+'px';}
document.querySelectorAll('.cb[data-tip]').forEach(function(el){el.addEventListener('pointermove',function(e){show(e,el)});el.addEventListener('focus',function(){show(null,el)});el.addEventListener('pointerleave',function(){tip.hidden=true});el.addEventListener('blur',function(){tip.hidden=true});});})();
