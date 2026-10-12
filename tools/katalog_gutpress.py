"""Składa katalogi Gutpress w identyfikacji Armatex: złączki do gazu (profil V i M) i zawory kulowe.

Użycie:
    pip install playwright==1.56.0 pymupdf fonttools brotli
    python3 tools/katalog_gutpress.py gaz          # → pliki/katalog-gutpress-gaz.pdf
    python3 tools/katalog_gutpress.py zawory       # → pliki/katalog-gutpress-zawory.pdf
    python3 tools/katalog_gutpress.py gaz --out x.pdf

Dane: tools/katalog-pdf/gutpress-gaz.json, gutpress-zawory.json i obrazy w tools/katalog-pdf/gutpress/ (tools/gutpress_dane.py).
Karty są na całą szerokość strony (zdjęcie, tabela zamówień, rysunek techniczny, tabela wymiarów). Ich wysokości mierzymy
w przeglądarce i dopiero potem układamy strony; druk, okładki i styl wspólne z tools/katalog_pdf.py.
"""
import html
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import katalog_pdf as kp  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

e = html.escape
COL_H = 716
GAP = 12


def im(path):
    return kp.asset(path)


def sec(nr, of, name, meta=''):
    m = f'<p class="sm">{e(meta)}</p>' if meta else ''
    return (f'<div class="sh{" meta" if m else ""}"><span class="sn">{nr:02d}</span><div><span class="eyebrow">Dział {nr} z {of}</span>'
            f'<h2>{e(name)}</h2>{m}</div></div>')


def tab(head, rows, cls):
    th = ''.join(f'<th>{e(h)}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{e(kp.size_txt(str(c)))}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def card_gaz(g):
    order = tab(['Rozmiar', 'Kod', 'Opk. 1', 'Opk. 2'], [[kp.size_txt(r[0].replace(' x ', ' × ')), r[1], r[2], r[3]] for r in g['wiersze']], 'ord')
    w = g['wymiary']
    head = w['head']
    tech = tab(head, w['rows'], 'tech')
    draws = ''.join(f'<img src="{im(r)}" alt="">' for r in g['rysunki'])
    return (f'<article class="tc"><div class="hd"><span class="pb">{g["profil"]}</span><div><span class="kod"><em>Besco</em> {e(g["kod"])}</span>'
            f'<h3>{e(g["nazwa"])}</h3></div><p class="op">{e(g["opis"])}</p></div>'
            f'<div class="bd"><div class="fo"><img src="{im(g["zdjecie"])}" alt=""></div>{order}<div class="dr n{len(g["rysunki"])}">{draws}</div></div>'
            f'<div class="tw"><span class="tl">Wymiary [mm]</span>{tech}</div></article>')


def card_zawor(z):
    return (f'<article class="tc zaw"><div class="hd"><span class="pb">{z["profil"]}</span><div><span class="kod"><em>Besco</em> {e(z["kod"])}</span>'
            f'<h3>{e(z["nazwa"])}</h3></div><p class="op">{e(z["zakres"])} · pełny przepływ</p></div>'
            f'<div class="bd zb"><div class="fo big"><img src="{im(z["zdjecie"])}" alt=""></div>'
            f'<ul class="ft"><li><b>Ciśnienie</b>{e(z["pn"])}</li><li><b>Temperatura</b>−20…120 °C</li><li><b>Gwarancja</b>5 lat</li>'
            f'<li><b>Rury</b>miedziane, ze stali węglowej i nierdzewnej</li></ul>'
            f'<div class="dr n1"><img src="{im(z["rysunek"])}" alt=""></div></div>'
            f'<div class="tw"><span class="tl">Wymiary [mm]</span>{tab(z["head"], [[c.replace(".", ",") if i > 1 else c for i, c in enumerate(r)] for r in z["rows"]], "tech")}</div></article>')


def measure(items, css):
    """Wysokości elementów (pt) przy szerokości kolumny strony produktów."""
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body class="gp">'
           f'<div class="meas" style="width:531.28pt">' + ''.join(f'<div class="mi">{x}</div>' for x in items) + '</div></body></html>')
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, 'm.html')
        open(src, 'w', encoding='utf-8').write(doc)
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto('file://' + src)
            pg.wait_for_load_state('networkidle')
            hs = pg.evaluate('() => [...document.querySelectorAll(".mi")].map(el => el.getBoundingClientRect().height * 0.75)')
            b.close()
    return hs


def pack(items, heights, keep_with_next):
    """Układa elementy w strony (jedna kolumna). Nagłówek działu nie zostaje sam na dole strony."""
    pages, cur, rem = [], [], COL_H
    for i, (x, h) in enumerate(zip(items, heights)):
        need = h + (GAP if cur else 0)
        if keep_with_next[i] and i + 1 < len(items):
            need += GAP + heights[i + 1]
        if cur and need > rem:
            pages.append(cur)
            cur, rem = [], COL_H
        assert h <= COL_H, f'element wyższy niż strona: {x[:80]}'
        rem -= h + (GAP if cur else 0)
        cur.append(x)
    pages.append(cur)
    return pages


def frame(no, items):
    return (f'<section class="page prod gp">{kp.head()}<div class="body"><div class="col stack">{"".join(items)}</div></div>'
            f'{kp.foot(no)}</section>')


def cover(c):
    logo_l = f'file://{kp.ROOT}/assets/img/logo-light.png'
    hero = ''.join(f'<img src="{im(x)}" alt="">' for x in c['hero'])
    facts = ''.join(f'<div><b>{v}</b><span>{e(k)}</span></div>' for v, k in c['facts'])
    return f'''<section class="page cover">
  <div class="top">
    {kp.stripes(595.28, 478, [(330, -10, 280, 70, kp.RED), (430, 60, 488, 70, kp.RED2)], 's-cover')}
    <img class="logo" src="{logo_l}" alt="Armatex">
    <span class="tag">Katalog produktów · 2026</span>
    <div class="title">
      <span class="eyebrow">{e(c["eyebrow"])}</span>
      <h1>{e(c["small"])}<b class="long">{e(c["big"])}</b></h1>
      <p>{e(c["sub"])}</p>
    </div>
  </div>
  <div class="hero">{hero}</div>
  <div class="facts">{facts}<div class="pzh badges">{c["badge"]}</div></div>
  <footer><b>armatex.pl</b><span class="brand">Produkty marki{kp.brand_logo()}</span></footer>
</section>'''


def back(dist, txt):
    logo_l = f'file://{kp.ROOT}/assets/img/logo-light.png'
    return f'''<section class="page back">
  {kp.stripes(595.28, 841.89, [(485, 600, 860, 70, kp.RED), (400, 600, 860, 70, kp.RED2)], 's-back')}
  <img class="logo" src="{logo_l}" alt="Armatex">
  <div class="cta">
    <span class="eyebrow">Zamówienia i wyceny</span>
    <h2>Zapytaj o dostępność<br>i ceny dla hurtowni</h2>
    <p>Wyślij listę indeksów – odpowiemy z ceną i terminem. {e(txt)}</p>
  </div>
  <div class="people">
    <div><span class="label">Biuro</span><b>513 191 502</b><a>biuro@armatex.pl</a><p>ul. Składowa 3a, 10-421 Olsztyn<br>pn–pt 7:00–18:00</p></div>
    <div><span class="label">Sprzedaż</span><b>798 807 106</b><a>piotr@armatex.pl</a><p>Piotr Stelmach</p></div>
    <div><span class="label">Magazyn</span><b>512 945 936</b><a>martyna@armatex.pl</a><p>Martyna Zielińska</p></div>
  </div>
  <div class="web"><b>armatex.pl</b><span>Od 1991 roku na rynku instalacyjnym</span></div>
  <div class="dist"><span>{dist}</span>{kp.brand_logo()}</div>
  <footer>
    <span>P.H.U. ARMATEX Sp. J. A. J. Bunda · siedziba: ul. Siewna 24, 10-831 Olsztyn · NIP 7393814110 · KRS 0000371628 · REGON 280563743</span>
    <span>Dane techniczne i numery artykułów według producenta (Besco). Zastrzegamy prawo do zmian. Stan na 2026 r.</span>
  </footer>
</section>'''


def intro(no, h2, lead, specs, boxes, legend, legend_title, toc, extra=''):
    sp = f'<div class="specs n{len(specs)}">' + ''.join(f'<div><span>{e(k)}</span><b>{e(v)}</b></div>' for k, v in specs) + '</div>'
    lg = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in legend)
    tc = ''.join(f'<div class="tsec"><h4><span>{i:02d}</span>{e(n)}<em>{p:02d}</em></h4><p class="tn">{e(d)}</p></div>'
                 for i, (n, d, p) in enumerate(toc, 1))
    b = kp.K['brand']
    bx = f'<div class="box brandbox"><img src="{kp.asset(b["logo"])}" alt=""><div><b>{b["box_title"]}</b><p>{b["box_text"]}</p></div></div>' + boxes
    return f'''<section class="page intro">
  {kp.head()}
  <div class="body">
    <span class="eyebrow">O katalogu</span>
    <h2 class="big">{e(h2)}</h2>
    <p class="lead">{lead}</p>
    {sp}
    <div class="two">
      <div>{bx}<h4 class="h4">{legend_title}</h4><dl class="legend">{lg}</dl></div>
      <div class="toc toc-sections"><h4 class="h4">Spis treści</h4>{tc}{extra}</div>
    </div>
  </div>
  {kp.foot(no)}
</section>'''


def css(faces=''):
    return faces + ''.join(open(os.path.join(kp.DIR, f), encoding='utf-8').read() for f in ('katalog.css', 'gutpress.css')).replace('{ROOT}', kp.ROOT)


def build(blocks, front, back_html, title, label, out, meta):
    """blocks: [(html, keep_with_next)] stron produktów; front(pages_map) → okładka + strona 2 (spis z numerami stron)."""
    heights = measure([b for b, _ in blocks], css())
    pages = pack([b for b, _ in blocks], heights, [k for _, k in blocks])
    where = {}
    for i, p in enumerate(pages):
        for x in p:
            where.setdefault(x, 3 + i)
    prod = ''.join(frame(3 + i, p) for i, p in enumerate(pages))
    last = 3 + len(pages)

    def make(faces):
        return (f'<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>{e(title)}</title><style>{css(faces)}</style></head>'
                f'<body class="gp">{front(where, last)}{prod}{back_html}</body></html>')
    n = kp.drukuj(make, out, label, meta)
    print(f'{out}: {n} stron')


def gaz(out):
    d = json.load(open(os.path.join(kp.DIR, 'gutpress-gaz.json'), encoding='utf-8'))
    kp.K = dict(header='Złączki zaprasowane Gutpress Gaz · profil V i M', head_logo='besco.png', brand=kp.BESCO)
    G = d['grupy']
    n_idx = sum(len(g['wiersze']) for g in G)
    blocks, firsts = [], {}
    meta = {'V': 'Ø 15–28 mm · 5 bar · −20…70 °C · uszczelka HNBR · miedź i brąz',
            'M': 'Ø 15–28 mm · 5 bar · −20…70 °C · uszczelka HNBR · miedź i brąz'}
    for nr, p in enumerate(('V', 'M'), 1):
        s = sec(nr, 4, f'Gutpress Gaz, profil {p}', meta[p])
        blocks.append((s, True))
        firsts[p] = s
        blocks += [(card_gaz(g), False) for g in G if g['profil'] == p]
    rems = rems_block(d)
    blocks.append((sec(3, 4, 'Narzędzia REMS', 'szczęki zaciskowe V i M, zaciskarki promieniowe 32 kN'), True))
    firsts['R'] = blocks[-1][0]
    blocks.append((rems, False))
    inst = inst_blocks(d)
    blocks.append((sec(4, 4, 'Instrukcja zaciskania', 'przygotowanie rury, osadzenie złączki, zaciskanie, BHP'), True))
    firsts['I'] = blocks[-1][0]
    blocks += [(x, False) for x in inst]
    nv = sum(1 for g in G if g['profil'] == 'V')

    def front(where, last):
        c = cover(dict(eyebrow='Produkty marki Besco · instalacje gazowe', small='Złączki zaprasowane do gazu', big='Gutpress Gaz',
                       sub=f'Profil V i M · Ø 15–28 mm · {kp.grupy(len(G))} · {kp.indeksy(n_idx)} · DVGW · INiG',
                       hero=(G[9]['zdjecie'], G[5]['zdjecie'], G[16]['zdjecie']),
                       facts=[('5 bar', 'ciśnienie'), ('−20…70 °C', 'temperatura'), ('Miedź i brąz', 'profil V i M')],
                       badge='<b>DVGW · INiG</b><span>INiG-PIB-KOT-2024/0051</span>'))
        i = intro(2, 'Złączki zaprasowane Gutpress do instalacji gazowych',
                  'Łączniki zaprasowywane z miedzi i brązu do instalacji gazowych i paliwa gazowego, według PN-C 04750:2011, '
                  f'w dwóch profilach zaprasowania: V i M. W katalogu jest {kp.grupy(len(G))} produktów i {kp.indeksy(n_idx)} '
                  'z tabelami wymiarów i rysunkami technicznymi. Armatex jest wyłącznym dystrybutorem w Polsce – zapytaj nas o '
                  'dostępność i ceny dla hurtowni.',
                  [('Zastosowanie', 'Instalacje gazowe'), ('Profile', 'V i M'), ('Średnice', '15–28 mm'), ('Ciśnienie', '5 bar'),
                   ('Temperatura', '−20…70 °C'), ('Materiał', 'Miedź, brąz'), ('Uszczelka', 'HNBR (żółte oznaczenie GAS)'),
                   ('Aprobaty', 'DVGW · INiG')],
                  '<div class="box pzhbox note"><div><b>Krajowa ocena techniczna INiG</b><p>Złączki mają krajową ocenę techniczną '
                  'Instytutu Nafty i Gazu – PIB: INiG-PIB-KOT-2024/0051, wydanie 1. Do instalacji gazowych nie stosuje się złączek '
                  'z linii wodnych.</p></div></div>',
                  [('ww', 'kielich × kielich'), ('wz', 'kielich × bosy koniec'), ('GW', 'gwint wewnętrzny'), ('GZ', 'gwint zewnętrzny'),
                   ('Rp', 'gwint wewnętrzny walcowy'), ('R', 'gwint zewnętrzny stożkowy'), ('T min/max', 'grubość ścianki'),
                   ('Opk. 1/2', 'sztuk w opakowaniu / kartonie')], 'Skróty i oznaczenia',
                  [('Gutpress Gaz, profil V', f'{kp.grupy(nv)} · rysunki i wymiary', where[firsts['V']]),
                   ('Gutpress Gaz, profil M', f'{kp.grupy(len(G) - nv)} · rysunki i wymiary', where[firsts['M']]),
                   ('Narzędzia REMS', 'szczęki zaciskowe i zaciskarki', where[firsts['R']]),
                   ('Instrukcja zaciskania', 'przygotowanie i montaż', where[firsts['I']])])
        return c + i
    build(blocks, front, back('Wyłączny dystrybutor<br>w Polsce', 'Złączki do gazu z linii wodnych nie zastępują.'),
          'Złączki zaprasowane Gutpress Gaz – katalog Armatex 2026', 'gaz', out,
          dict(title='Złączki zaprasowane Gutpress Gaz – katalog Armatex 2026', subject=f'Gutpress Gaz, profil V i M: {kp.indeksy(n_idx)}',
               keywords='Gutpress, gaz, złączki zaprasowane, Besco, INiG, DVGW, Armatex'))


JAWS = {'V': [('V 15', '570115'), ('V 18', '570125'), ('V 22', '570135'), ('V 28', '570145'), ('V 35', '570155')],
        'M': [('M 15', '570110'), ('M 18', '570120'), ('M 22', '570130'), ('M 28', '570140'), ('M 35', '570150')]}
PRESSES = [('REMS Power-Press SE', 'elektryczna prasa promieniowa 32 kN', '572101 R220'),
           ('REMS Power-Press', 'elektryczna prasa promieniowa 32 kN z sygnałem wyłączenia', '577001 R220'),
           ('REMS Power-Press ACC', 'elektrohydrauliczna prasa promieniowa 32 kN z wymuszonym powrotem', '577000 R220'),
           ('REMS Akku-Press 22 V ACC', 'akumulatorowa prasa promieniowa 32 kN z wymuszonym powrotem i kontrolą siły zacisku', '576000 R22'),
           ('REMS Akku-Press 22 V ACC Basic-Pack L-Boxx', 'zestaw z walizką L-Boxx', '576011 R220')]


def rems_block(d):
    imgs = [x['f'] for x in d['rems']]
    jaws = ''.join(f'<div class="jw"><h4>Szczęki zaciskowe profil {p}</h4>' + tab(['Szczęki', 'Nr kat. REMS'], JAWS[p], 'ord') + '</div>' for p in 'VM')
    pr = ''.join(f'<div class="pr"><img src="{im(f)}" alt=""><div><b>{e(n)}</b><p>{e(t)}</p><span>Nr kat. {e(k)}</span></div></div>'
                 for f, (n, t, k) in zip(imgs[1:], PRESSES))
    return (f'<div class="rems"><div class="jaws"><img src="{im(imgs[0])}" alt="">{jaws}</div>'
            f'<p class="note">Złączki zaprasowuj szczękami o profilu zgodnym ze złączką (V lub M). Besco i Armatex zalecają narzędzia REMS.</p>'
            f'<h4 class="h4">Zaciskarki REMS</h4><div class="prs">{pr}</div></div>')


STEPS = [
    ('Przygotowanie', 'Dobierz złączkę o wymiarze odpowiadającym rurze. Sprawdź, czy rura i złączka są czyste, w dobrym stanie, bez uszkodzeń i wad.'),
    ('1. Cięcie', 'Utnij rurę obrotowym obcinakiem do rur.'),
    ('2. Kontrola', 'Rura musi być ucięta równo, odpowiednio ogratowana i bez zarysowań.'),
    ('3. Gratowanie', 'Ogratuj wewnętrzną i zewnętrzną krawędź rury, a potem wytrzyj ją do czysta z opiłków, aby nie uszkodzić o-ringu przy '
                      'wkładaniu. Możesz użyć gratownika A S120.'),
    ('4. Pilnik', 'Jeśli nie masz gratownika, przygotuj końce rury drobnym pilnikiem.'),
    ('5. Głębokość', 'Rura musi wejść w złączkę do oporu. Zaznacz głębokość włożenia głębokościomierzem S110 XPress lub linijką: '
                     'Ø15 – 20 mm, Ø18 – 21 mm, Ø22 – 23 mm, Ø28 – 26 mm, Ø35 – 33 mm.'),
    ('Narzędzia', 'Przed zaciskaniem sprawdź w instrukcji producenta zaciskarki, jak bezpiecznie wykonać połączenie. Besco i Armatex '
                  'zalecają narzędzia REMS.'),
    ('Osadzenie złączki', 'Złączki trzymaj w opakowaniach do chwili montażu, aby środek smarny nie wysechł. Sprawdź, czy o-ring jest '
                          'prawidłowo osadzony w kielichu. Wsuń rurę do oporu, kontrolując zaznaczenie głębokości.'),
    ('Szczęki', 'Włóż szczęki o odpowiedniej wielkości do zaciskarki i umieść je na przetłoczeniu kielicha (miejsce o-ringu).'),
    ('Kąt 90°', 'Podczas zaciskania zachowaj kąt 90° między rurą a szczękami. Zaciskaj tylko rurę podpartą na wspornikach, nie zawieszoną '
                'na kielichu złączki.'),
    ('Zaciskanie', 'Wciśnij włącznik, aby rozpocząć cykl. Gdy szczęki w pełni zacisną się na złączce, łączenie jest zakończone – zwolnij szczęki.'),
    ('Rozmieszczenie', 'Zostaw wokół każdej złączki odpowiedni prześwit, aby szczęki dało się założyć bez przeszkód.'),
]


def inst_blocks(d):
    imgs = [x['f'] for x in d['inst']]
    first = f'<div class="note"><b>{e(STEPS[0][0])}.</b> {e(STEPS[0][1])}</div>'     # w oryginale bez zdjęcia
    assert len(imgs) == len(STEPS) - 1, (len(imgs), len(STEPS))
    cells = ''.join(f'<div class="is"><img src="{im(f)}" alt=""><div><b>{e(t)}</b><p>{e(x)}</p></div></div>'
                    for f, (t, x) in zip(imgs, STEPS[1:]))
    rest = ''
    bhp = ('<div class="note warn2"><b>BHP.</b> Podczas zaciskania noś osłony oczu. Nie uruchamiaj zaciskarki bez zamocowanych szczęk.</div>')
    return [f'{first}<div class="inst">{cells}{rest}</div>{bhp}']


def zawory(out):
    Z = json.load(open(os.path.join(kp.DIR, 'gutpress-zawory.json'), encoding='utf-8'))
    kp.K = dict(header='Zawory kulowe Gutpress · profil V i M', head_logo='besco.png', brand=kp.BESCO)
    n_idx = sum(len(z['rows']) for z in Z)
    blocks, firsts = [], {}
    for nr, p in enumerate(('V', 'M'), 1):
        s = sec(nr, 2, f'Zawory kulowe, profil {p}', 'PN40/25/16 · −20…120 °C · DVGW · WRAS' if p == 'V' else 'PN25 · −20…120 °C · DVGW · WRAS')
        blocks.append((s, True))
        firsts[p] = s
        blocks += [(card_zawor(z), False) for z in Z if z['profil'] == p]
    table_a = tab(['Rura miedziana EN 1057', '15 × 1', '18 × 1', '22 × 1', '28 × 1 / 1,5', '35 × 1,2 / 1,5', '42 × 1,2 / 1,5', '54 × 1,5 / 2'],
                  [['Szczęki REMS', 'R250', 'R250', 'R250', 'R250', 'R250', 'R290', 'R290'],
                   ['Profil V', 'tak', 'tak', 'tak', 'tak', 'nie', 'nie', 'nie'],
                   ['Profil M', 'tak', 'tak', 'tak', 'tak', 'tak', 'tak', 'tak']], 'taba')

    def front(where, last):
        c = cover(dict(eyebrow='Produkty marki Besco · zawory zaprasowywane', small='Zawory kulowe press', big='Gutpress',
                       sub=f'Profil V i M · Ø 15–54 mm · {len(Z)} typów · {kp.indeksy(n_idx)} · DVGW · WRAS · PZH',
                       hero=('gutpress/zaw-v.png', 'gutpress/zaw-m.png'),
                       facts=[('Pełny przepływ', 'kula pełnoprzelotowa'), ('do PN40', 'ciśnienie (profil V, 15–28 mm)'), ('−20…120 °C', 'temperatura')],
                       badge=f'<img src="{im("gutpress/znak-5lat.png")}" alt=""><span>5 lat<br>gwarancji</span>'))
        i = intro(2, 'Zawory kulowe zaprasowywane Gutpress',
                  'Seria zaworów kulowych Gutpress pozwala szybko wykonać instalację narzędziami do zaprasowywania (tabela A). Zawory '
                  'nadają się do wody zimnej i ciepłej, dystrybucji wody pitnej oraz instalacji grzewczych przemysłowych i domowych. '
                  f'W katalogu jest {len(Z)} typów i {kp.indeksy(n_idx)} w profilach V i M. Armatex jest dystrybutorem Besco od 2016 roku – '
                  'zapytaj nas o dostępność i ceny dla hurtowni.',
                  [('Profile', 'V i M'), ('Średnice', '15–54 mm'), ('Ciśnienie V', 'PN40 / PN25 / PN16'), ('Ciśnienie M', 'PN25'),
                   ('Temperatura', '−20…120 °C'), ('Gwarancja', '5 lat'), ('Normy', 'DVGW W570-1, DIN EN 13828'), ('Gwint', 'UNI ISO 228')],
                  f'<div class="box pzhbox note badges3"><div><div class="bdg"><img src="{im("gutpress/znak-wras.png")}" alt="">'
                  f'<img src="{im("gutpress/znak-dvgw.png")}" alt=""><img src="{im("gutpress/znak-pzh.png")}" alt=""></div><b>Zgodność z rurami</b><p>Miedzianymi (EN 1057), ze stali węglowej '
                  '(EN 10305-3) i ze stali nierdzewnej (EN 10312). Zawór: EN 13828:04 / EN 331; połączenia: UNI 11065:03, pr EN 1254-7:05.</p></div></div>',
                  [('PP', 'press × press'), ('PF', 'press × gwint wewnętrzny'), ('PU', 'press × śrubunek z gwintem'), ('H', 'trzpień przedłużony'),
                   ('d, d1, d2', 'średnice [mm]'), ('L, L1, L3, H', 'długości i wysokości [mm]')], 'Oznaczenia',
                  [(f'Zawory kulowe, profil {p}', f'{len([z for z in Z if z["profil"] == p])} typy · '
                    f'{kp.indeksy(sum(len(z["rows"]) for z in Z if z["profil"] == p))}', where[firsts[p]]) for p in 'VM'],
                  extra=f'<h4 class="h4">Tabela A. Zaprasowywanie zaworów</h4>{table_a}')
        return c + i
    build(blocks, front, back('Dystrybutor marki<br>od 2016 roku', 'Wszystkie indeksy Besco znajdziesz też w wyszukiwarce na armatex.pl.'),
          'Zawory kulowe Gutpress – katalog Armatex 2026', 'zawory', out,
          dict(title='Zawory kulowe Gutpress – katalog Armatex 2026', subject=f'Zawory kulowe Gutpress, profil V i M: {kp.indeksy(n_idx)}',
               keywords='Gutpress, zawory kulowe, press, Besco, DVGW, WRAS, Armatex'))


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else ''
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    if what == 'gaz':
        gaz(out or os.path.join(kp.ROOT, 'pliki', 'katalog-gutpress-gaz.pdf'))
    elif what == 'zawory':
        zawory(out or os.path.join(kp.ROOT, 'pliki', 'katalog-gutpress-zawory.pdf'))
    else:
        sys.exit('Podaj: gaz albo zawory')


if __name__ == '__main__':
    main()
