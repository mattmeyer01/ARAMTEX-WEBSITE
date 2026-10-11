"""Składa katalogi PDF złączek Besco INOX w identyfikacji Armatex.

Użycie:
    pip install playwright==1.56.0 pymupdf fonttools brotli
    python3 tools/katalog_pdf.py inox-304                # → pliki/katalog-besco-inox-304.pdf
    python3 tools/katalog_pdf.py inox-316l               # → pliki/katalog-besco-inox-316l.pdf
    python3 tools/katalog_pdf.py inox-316l --out x.pdf   # podgląd do innego pliku

Dane (tools/katalog-pdf/):
    <linia>.json    grupy i wiersze (wymiar, nr artykułu, woreczek, karton) z katalogu Besco; „zdjecie” to ścieżka od
                    katalogu głównego. INOX 304 z warstwy tekstowej katalogu Besco, INOX 316L z data/besco-2026.json
                    (OCR), sprawdzone wiersz po wierszu z katalogiem.
    pzh.webp        znak „Produkt z atestem” NIZP PZH-PIB
    besco.png       logo Besco (z katalogu producenta, przezroczyste tło; tylko na jasnym tle)
    foto/           zdjęcia powiększone do druku (ESRGAN), gdy zdjęcia ze strony są za małe
    katalog.css     wygląd (kolory i fonty jak w c.css)

Różnice między liniami (teksty, parametry, działy, atest) są w LINES.

Outfit jest fontem zmiennym; Chromium osadza go w PDF jako Type 3, więc przed drukiem robimy z niego
statyczne odmiany 400–700 (fontTools) i podajemy je jako osobne kroje.

Strony produktów mają stały układ (dwie kolumny, stałe wysokości wierszy), więc podział na strony
i spis treści liczymy tutaj. Po złożeniu sprawdzamy w przeglądarce, czy żadna kolumna się nie przelewa.
"""
import html
import json
import os
import re
import sys
import tempfile

import pymupdf
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'tools', 'katalog-pdf')
BESCO = f'file://{DIR}/besco.png'

GW_PRESS, GW_BOSY = 'kielich press × gwint wewnętrzny', 'bosy koniec × gwint wewnętrzny'
GZ_PRESS, GZ_BOSY = 'kielich press × gwint zewnętrzny', 'bosy koniec × gwint zewnętrzny'
LINES = {
    'inox-304': dict(
        name='INOX 304', material='Stal nierdzewna 304', sizes='15–108 mm', sizes_od='od 15 do 108 mm',
        app='Ogrzewanie i woda pitna', app_cover='Ogrzewanie<br>i woda pitna',
        h2='Złączki press ze stali nierdzewnej do instalacji wody pitnej i ogrzewania',
        extra_specs=[], cover_tag='',
        pzh='Złączki INOX 304 mają atest higieniczny Narodowego Instytutu Zdrowia Publicznego PZH – PIB '
            '(B.BK.60110.1654.2026) do instalacji wody pitnej i ciepłej wody użytkowej.',
        pzh_cover='atest higieniczny<br>PZH',
        hero=('3002', '3130', '3270G'),
        sections=[
            ('Mufy, redukcje i zaślepki', ['3270', '3271', '3240', '3243', '3301']),
            ('Łuki i mijanki', ['3002', '3001', '3041', '3040', '3030', '3085', '3086']),
            ('Trójniki', ['3130', '3130R', '3130G']),
            ('Przejścia gwintowane i kołnierzowe', ['3270G', '3281', '3243G', '3280', '3002G', '3001G', '3472G', '3358G', '3331G', '3510']),
        ],
        opis={'3270G': GW_PRESS, '3281': GW_BOSY, '3243G': GZ_PRESS, '3280': GZ_BOSY}),
    'inox-316l': dict(
        name='INOX 316L', material='Stal nierdzewna 316L', sizes='15–168,3 mm', sizes_od='od 15 do 168,3 mm',
        app='Woda, ogrzewanie i przemysł', app_cover='Woda, ogrzewanie<br>i przemysł',
        h2='Złączki press ze stali nierdzewnej 316L do wody, ogrzewania i przemysłu',
        extra_specs=[('Aprobaty', 'DVGW · WRAS'), ('Atest PZH', 'Ø 15–108 mm')], cover_tag=' · DVGW · WRAS',
        pzh='Złączki INOX 316L mają atest higieniczny Narodowego Instytutu Zdrowia Publicznego PZH – PIB '
            '(B.BK.60110.1480.2025) do instalacji wody pitnej i ciepłej wody użytkowej, dla średnic 15–108 mm.',
        pzh_cover='atest PZH<br>Ø 15–108 mm',
        hero=('12200', '12100', '12020'),
        sections=[
            ('Mufy, redukcje i zaślepki', ['12000', '12040', '12430', '12410']),
            ('Łuki i mijanki', ['12200', '12210', '12230', '12240', '12350', '12360']),
            ('Trójniki', ['12100', '12110', '12120']),
            ('Przejścia gwintowane i kołnierzowe', ['12020', '12460', '12010', '12450', '12320', '12310', '12340', '12070', '12080', '12400']),
        ],
        opis={'12020': GW_PRESS, '12460': GW_BOSY, '12010': GZ_PRESS, '12450': GZ_BOSY}),
}
L = None   # bieżąca linia (main)

# Wymiary układu (pt). Wysokości w CSS są te same, więc obliczony podział zgadza się z wydrukiem.
COL_H = 716          # wysokość kolumny na stronie produktów
SEC_H = 58           # nagłówek działu (w kolumnie)
HEAD_H = 84          # głowa karty (zdjęcie + nazwa)
CONT_H = 30          # głowa karty kontynuacji
TH_H = 20            # nagłówek tabeli
ROW_H = 14.5         # wiersz tabeli
PAD_H = 6            # dół karty
GAP = 12             # odstęp między kartami
MIN_SPLIT = 6        # najmniej wierszy w części tabeli po podziale
CTA_H = 330          # panel „zapytaj o wycenę” na końcu

e = html.escape


def card_h(rows, cont=False):
    return (CONT_H if cont else HEAD_H) + TH_H + ROW_H * rows + PAD_H + 1.5  # 1.5 = ramka


def stripes(w, h, bands, cls, rx=0):
    """Pasy jak w logo Armatex: równoległoboki z poziomymi końcami, nachylone pod 50°, przycięte do pola w × h (pt).
    bands: (x lewego dolnego rogu, y góry, y dołu, szerokość, kolor)."""
    t = 1.19  # tg 50°
    polys = ''
    for x0, y0, y1, bw, col in bands:
        dx = (y1 - y0) / t
        pts = f'{x0},{y1} {x0 + bw},{y1} {x0 + bw + dx},{y0} {x0 + dx},{y0}'
        polys += f'<polygon points="{pts}" fill="{col}"/>'
    clip = ''
    if rx:  # zaokrąglony prawy dolny róg (panel z zaokrągleniem)
        clip = (f'<clipPath id="c{cls}"><rect x="-20" y="-20" width="{w + 20}" height="{h + 20}" rx="{rx}"/></clipPath>')
        polys = f'<g clip-path="url(#c{cls})">{polys}</g>'
    return (f'<svg class="stripes {cls}" width="{w}pt" height="{h}pt" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg">{clip}{polys}</svg>')


RED, RED2 = '#dc291e', '#b91f15'


def plural(n, one='indeks', few='indeksy', many='indeksów'):
    if n == 1:
        return one
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return few
    return many


def grupy(n):
    return f'{n} {plural(n, "grupa", "grupy", "grup")}'


def indeksy(n):
    return f'{n} {plural(n)}'


def size_range(rows):
    first = sorted({r[0].split(' × ')[0] for r in rows}, key=lambda x: float(x.replace(',', '.')))
    return f'Ø {first[0]}–{first[-1]} mm' if len(first) > 1 else f'Ø {first[0]} mm'


def paginate(groups):
    """Układa nagłówki działów i karty w kolumny, po kolei, bez pustych miejsc między działami.
    Zwraca listę stron: [[element, ...], [element, ...]], gdzie element to {'sec': (nr, nazwa)} albo kawałek karty."""
    pages = [[[], []]]
    state = {'col': 0, 'rem': COL_H}

    def next_col():
        if state['col'] == 0:
            state['col'] = 1
        else:
            pages.append([[], []])
            state['col'] = 0
        state['rem'] = COL_H

    def put(item, h):
        col = pages[-1][state['col']]
        state['rem'] -= h + (GAP if col else 0)
        col.append(item)

    def gap():
        return GAP if pages[-1][state['col']] else 0

    for si, (name, codes) in enumerate(L['sections']):
        first = groups[codes[0]]['wiersze']
        if SEC_H + GAP + card_h(len(first) if len(first) <= 12 else MIN_SPLIT) + gap() > state['rem']:
            next_col()
        put({'sec': (si + 1, name)}, SEC_H)
        for code in codes:
            g = groups[code]
            rows, start = g['wiersze'], 0
            while start < len(rows):
                cont = start > 0
                left = len(rows) - start
                if card_h(left, cont) + gap() <= state['rem']:
                    take = left
                else:
                    fit = min(int((state['rem'] - gap() - card_h(0, cont)) // ROW_H), left - MIN_SPLIT)
                    empty = not pages[-1][state['col']]
                    take = fit if (fit >= MIN_SPLIT and (left > 12 or empty)) else 0
                    assert take or not empty, f'{g["kod"]}: karta nie mieści się w pustej kolumnie'
                if take:
                    put({'g': g, 'rows': rows[start:start + take], 'cont': cont}, card_h(take, cont))
                    start += take
                else:
                    next_col()
    # koniec: panel wyceny w wolnej kolumnie, notatki w reszcie kolumny z ostatnią kartą
    if state['col'] == 0:
        if state['rem'] > 150:
            put({'notes': True}, 0)
        next_col()
    if state['rem'] < CTA_H:
        next_col()
    put({'cta': True}, CTA_H)
    return pages


FRAC = {'1/2': '½', '1/4': '¼', '3/4': '¾'}


def size_txt(s):
    """Wymiar do druku: „1 1/4″” → „1¼"”, „1/2″” → „½"” (Outfit nie ma znaku ″; numery artykułów bez zmian)."""
    s = s.replace('″', '"')
    s = re.sub(r'(\d) (1/2|1/4|3/4)', lambda m: m.group(1) + FRAC[m.group(2)], s)
    return re.sub(r'(?<![\d/])(1/2|1/4|3/4)', lambda m: FRAC[m.group(1)], s)


def table(part):
    g = part['g']
    unit = 'mm × cal' if g['gwint'] else 'mm'
    rows = ''.join(
        f'<tr><td>{e(size_txt(s))}</td><td class="art">{e(a)}</td><td class="n">{b}</td><td class="n">{c}</td></tr>'
        for s, a, b, c in part['rows'])
    return (f'<table><thead><tr><th>Wymiar <i>{unit}</i></th><th>Nr artykułu</th>'
            f'<th class="n">Opak.</th><th class="n">Karton</th></tr></thead><tbody>{rows}</tbody></table>')


def card(part):
    g = part['g']
    if part['cont']:
        return (f'<article class="card cont"><div class="ch"><b>{e(g["nazwa"])}</b><span>{e(g["kod"])} · cd.</span></div>'
                f'{table(part)}</article>')
    n = len(g['wiersze'])
    opis = f'<p class="opis">{e(L["opis"][g["kod"]])}</p>' if g['kod'] in L['opis'] else ''
    img = foto(g)
    return (f'<article class="card" id="g{e(g["kod"])}"><div class="head"><div class="foto"><img src="{img}" alt=""></div>'
            f'<div class="tt"><span class="kod"><em>Besco</em> {e(g["kod"])}</span><h3>{e(g["nazwa"])}</h3>{opis}'
            f'<p class="meta">{indeksy(n)} · {size_range(g["wiersze"])}</p></div></div>'
            f'{table(part)}</article>')


def sec_head(sec):
    return (f'<div class="sh"><span class="sn">{sec[0]:02d}</span><div><span class="eyebrow">Dział {sec[0]} z {len(L['sections'])}</span>'
            f'<h2>{e(sec[1])}</h2></div></div>')


CTA = f'''<div class="cta">{stripes(150, 190, [(40, 40, 210, 26, RED), (95, 10, 210, 26, RED2)], 's-cta', rx=7)}
  <span class="eyebrow">Zamówienia i wyceny</span>
  <h3>Wyślij listę indeksów – przygotujemy wycenę</h3>
  <p>Podaj numery artykułów i ilości (w opakowaniach lub kartonach). Odpowiemy z ceną i terminem.</p>
  <dl><div><dt>Biuro</dt><dd><b>513 191 502</b>biuro@armatex.pl</dd></div>
      <div><dt>Sprzedaż</dt><dd><b>798 807 106</b>piotr@armatex.pl</dd></div></dl>
  <div class="ws"><b>armatex.pl/wyszukiwarka</b><span>1 936 indeksów Besco z listą do wyceny</span></div>
</div>'''


def block(x):
    if 'sec' in x:
        return sec_head(x['sec'])
    if 'cta' in x:
        return CTA
    if 'notes' in x:
        return '<div class="notes"><span class="eyebrow">Notatki</span><div class="lines">' + '<i></i>' * 40 + '</div></div>'
    return card(x)


def foto(g):
    """Zdjęcie grupy: powiększone do druku (tools/katalog-pdf/foto), a jeśli go nie ma, to ze strony."""
    big = os.path.join(DIR, 'foto', os.path.basename(g['zdjecie']).replace('-l.webp', '.webp'))
    return 'file://' + (big if os.path.exists(big) else os.path.join(ROOT, g['zdjecie']))


def frame(no, cols):
    inner = ''.join('<div class="col">' + ''.join(block(x) for x in col) + '</div>' for col in cols)
    return (f'<section class="page prod"><header class="ph"><img src="file://{ROOT}/assets/img/logo-dark.png" alt="Armatex">'
            f'<span class="r">Złączki zaprasowane {L["name"]} · profil M<img src="{BESCO}" alt="Besco"></span></header>'
            f'<div class="body"><div class="cols">{inner}</div></div>'
            f'<footer class="pf"><span><b>armatex.pl</b> · biuro@armatex.pl · 513 191 502</span><span class="pn">{no:02d}</span></footer></section>')


OUTFIT = {'latin': 'U+0000-00FF, U+2013-2014, U+2018-201F, U+2026, U+2032-2033, U+2212', 'latin-ext': 'U+0100-024F, U+1E00-1EFF'}


def outfit_faces(tmp):
    """Statyczne odmiany Outfit (zmienny font Chromium zamienia w PDF na Type 3)."""
    css = ''
    for sub, rng in OUTFIT.items():
        for w in (400, 500, 600, 700):
            path = os.path.join(tmp, f'outfit-{sub}-{w}.ttf')
            f = TTFont(os.path.join(ROOT, 'assets', 'fonts', f'outfit-{sub}-wght-normal.woff2'))
            f.flavor = None
            instantiateVariableFont(f, {'wght': w}, inplace=True)
            f.save(path)
            css += f'@font-face {{ font-family: "Outfit"; src: url("file://{path}") format("truetype"); font-weight: {w}; unicode-range: {rng}; }}\n'
    return css


def build_html(groups, pages, first_page, faces):
    total = sum(len(g['wiersze']) for g in groups.values())
    # spis treści
    where, sec_page = {}, {}
    for i, cols in enumerate(pages):
        for col in cols:
            for x in col:
                if 'sec' in x:
                    sec_page.setdefault(x['sec'][0], first_page + i)
                elif 'g' in x:
                    where.setdefault(x['g']['kod'], first_page + i)
    toc = ''
    for si, (name, codes) in enumerate(L['sections']):
        items = ''.join(f'<li><span class="k">{e(c)}</span><span class="t">{e(groups[c]["nazwa"])}</span>'
                        f'<span class="d"></span><span class="p">{where[c]:02d}</span></li>' for c in codes)
        toc += (f'<div class="tsec"><h4><span>{si + 1:02d}</span>{e(name)}<em>{sec_page[si + 1]:02d}</em></h4>'
                f'<ol>{items}</ol></div>')

    prod = ''.join(frame(first_page + i, cols) for i, cols in enumerate(pages))
    logo_l = f'file://{ROOT}/assets/img/logo-light.png'
    logo_d = f'file://{ROOT}/assets/img/logo-dark.png'
    pzh = f'file://{DIR}/pzh.webp'
    hero = ''.join(f'<img src="{foto(groups[c])}" alt="">' for c in L['hero'])
    specs = [('Materiał', L['material']), ('Profil zaprasowania', 'M'), ('Średnice', L['sizes']), ('Ciśnienie', '16 bar'),
             ('Temperatura', '−10…110 °C'), ('Zastosowanie', L['app'])] + L['extra_specs']
    specs_html = ''.join(f'<div><span>{e(k)}</span><b>{e(v)}</b></div>' for k, v in specs)
    name_cls = ' long' if len(L['name']) > 8 else ''

    cover = f'''<section class="page cover">
  <div class="top">
    {stripes(595.28, 478, [(330, -10, 280, 70, RED), (430, 60, 488, 70, RED2)], 's-cover')}
    <img class="logo" src="{logo_l}" alt="Armatex">
    <span class="tag">Katalog produktów · 2026</span>
    <div class="title">
      <span class="eyebrow">Produkty marki Besco · stal nierdzewna · system press</span>
      <h1>Złączki zaprasowane<b class="{name_cls}">{L["name"]}</b></h1>
      <p>Profil M · Ø {L["sizes"]} · {grupy(len(groups))} · {indeksy(total)}{L["cover_tag"]}</p>
    </div>
  </div>
  <div class="hero">{hero}</div>
  <div class="facts">
    <div><b>16 bar</b><span>ciśnienie</span></div>
    <div><b>−10…110 °C</b><span>temperatura</span></div>
    <div><b>{L["app_cover"]}</b><span>zastosowanie</span></div>
    <div class="pzh"><img src="{pzh}" alt="PZH – produkt z atestem"><span>{L["pzh_cover"]}</span></div>
  </div>
  <footer><b>armatex.pl</b><span class="brand">Produkty marki<img src="{BESCO}" alt="Besco"></span></footer>
</section>'''

    intro = f'''<section class="page intro">
  <header class="ph"><img src="{logo_d}" alt="Armatex"><span class="r">Złączki zaprasowane {L["name"]} · profil M<img src="{BESCO}" alt="Besco"></span></header>
  <div class="body">
    <span class="eyebrow">O systemie</span>
    <h2 class="big">{L["h2"]}</h2>
    <p class="lead">Złączki zaprasowane Besco {L["name"]} w profilu M łączą rury ze stali nierdzewnej przez zaprasowanie –
    bez gwintowania i spawania. W katalogu jest {grupy(len(groups))} produktów i {indeksy(total)} w średnicach {L["sizes_od"]}.
    Armatex jest dystrybutorem Besco od 2016 roku – zapytaj nas o dostępność i ceny dla hurtowni.</p>
    <div class="specs n{len(specs)}">{specs_html}</div>
    <div class="two">
      <div>
        <div class="box brandbox"><img src="{BESCO}" alt="Besco"><div><b>Produkty marki Besco</b>
          <p>Wszystkie produkty w katalogu to złączki Besco Fittings &amp; Connectors.
          Armatex jest dystrybutorem marki Besco od 2016 roku.</p></div></div>
        <div class="box pzhbox"><img src="{pzh}" alt=""><div><b>Atest higieniczny PZH</b>
          <p>{L["pzh"]}</p></div></div>
        <h4 class="h4">Skróty w nazwach</h4>
        <dl class="legend">
          <div><dt>ww</dt><dd>kielich × kielich</dd></div>
          <div><dt>wz</dt><dd>kielich × bosy koniec</dd></div>
          <div><dt>zz</dt><dd>bosy koniec × bosy koniec</dd></div>
          <div><dt>GW</dt><dd>gwint wewnętrzny</dd></div>
          <div><dt>GZ</dt><dd>gwint zewnętrzny</dd></div>
          <div><dt>M</dt><dd>zaprasowywać szczękami o profilu M</dd></div>
        </dl>
        <h4 class="h4">Jak czytać tabele</h4>
        <dl class="legend">
          <div><dt>Wymiar</dt><dd>średnica rury w mm; gwint w calach (")</dd></div>
          <div><dt>Opak.</dt><dd>liczba sztuk w woreczku</dd></div>
          <div><dt>Karton</dt><dd>liczba sztuk w kartonie</dd></div>
        </dl>
      </div>
      <div class="toc"><h4 class="h4">Spis treści</h4>{toc}</div>
    </div>
  </div>
  <footer class="pf"><span><b>armatex.pl</b> · biuro@armatex.pl · 513 191 502</span><span class="pn">02</span></footer>
</section>'''

    back = f'''<section class="page back">
  {stripes(595.28, 841.89, [(485, 600, 860, 70, RED), (400, 600, 860, 70, RED2)], 's-back')}
  <img class="logo" src="{logo_l}" alt="Armatex">
  <div class="cta">
    <span class="eyebrow">Zamówienia i wyceny</span>
    <h2>Zapytaj o dostępność<br>i ceny dla hurtowni</h2>
    <p>Wyślij listę indeksów – odpowiemy z ceną i terminem. Wszystkie indeksy Besco znajdziesz też w wyszukiwarce na armatex.pl.</p>
  </div>
  <div class="people">
    <div><span class="label">Biuro</span><b>513 191 502</b><a>biuro@armatex.pl</a><p>ul. Składowa 3a, 10-421 Olsztyn<br>pn–pt 7:00–18:00</p></div>
    <div><span class="label">Sprzedaż</span><b>798 807 106</b><a>piotr@armatex.pl</a><p>Piotr Stelmach</p></div>
    <div><span class="label">Magazyn</span><b>512 945 936</b><a>martyna@armatex.pl</a><p>Martyna Zielińska</p></div>
  </div>
  <div class="web"><b>armatex.pl</b><span>Od 1991 roku na rynku instalacyjnym</span></div>
  <div class="dist"><span>Dystrybutor marki<br>od 2016 roku</span><img src="{BESCO}" alt="Besco"></div>
  <footer>
    <span>P.H.U. ARMATEX Sp. J. A. J. Bunda · siedziba: ul. Siewna 24, 10-831 Olsztyn · NIP 7393814110 · KRS 0000371628 · REGON 280563743</span>
    <span>Dane techniczne i numery artykułów według producenta (Besco). Zastrzegamy prawo do zmian. Stan na 2026 r.</span>
  </footer>
</section>'''

    css = faces + open(os.path.join(DIR, 'katalog.css'), encoding='utf-8').read().replace('{ROOT}', ROOT)
    return (f'<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>{e(title())}</title>'
            f'<style>{css}</style></head><body class="{L["id"]}">{cover}{intro}{prod}{back}</body></html>')


def title():
    return f'Złączki zaprasowane Besco {L["name"]} – katalog Armatex 2026'


def main():
    global L
    line = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in LINES else sys.exit('Podaj linię: ' + ', '.join(LINES))
    L = dict(LINES[line], id=line)
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else os.path.join(ROOT, 'pliki', f'katalog-besco-{line}.pdf')
    data = json.load(open(os.path.join(DIR, f'{line}.json'), encoding='utf-8'))
    groups = {g['kod']: g for g in data}
    assert sorted(groups) == sorted(c for _, cs in L['sections'] for c in cs)
    pages = paginate(groups)
    with tempfile.TemporaryDirectory() as tmp:
        doc_html = build_html(groups, pages, 3, outfit_faces(tmp))
        src = os.path.join(tmp, 'katalog.html')
        open(src, 'w', encoding='utf-8').write(doc_html)
        pdf = os.path.join(tmp, 'k.pdf')
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto('file://' + src)
            pg.wait_for_load_state('networkidle')
            pg.evaluate('document.fonts.ready')
            bad = pg.evaluate('''() => [
                ...[...document.querySelectorAll('.col, .body')].filter(el => el.scrollHeight > el.clientHeight + 1),
                ...[...document.querySelectorAll('td, th, h3, .tsec li')].filter(el => el.scrollWidth > el.clientWidth + 1)
              ].map(el => ((el.closest('.page').querySelector('.pn') || {}).textContent || 'okł.') + ' ' + el.tagName + '.'
                          + el.className + ' ' + el.textContent.slice(0, 30))''')
            if bad:
                msg = 'Przelewa się: ' + '; '.join(' '.join(x.split()) for x in bad)
                if '--out' not in sys.argv:
                    sys.exit(msg)
                print(msg)
            pg.pdf(path=pdf, prefer_css_page_size=True, print_background=True)
            b.close()
        d = pymupdf.open(pdf)
        d.set_metadata({'title': title(), 'author': 'P.H.U. ARMATEX Sp. J. A. J. Bunda',
                        'subject': f'Złączki zaprasowane Besco {L["name"]}, profil M, {L["sizes"]}',
                        'keywords': f'{L["name"]}, złączki zaprasowane, press, stal nierdzewna, Besco, Armatex',
                        'creator': 'Armatex', 'producer': 'Armatex'})
        d.xref_set_key(d.pdf_catalog(), 'Lang', '(pl-PL)')
        d.rewrite_images(dpi_threshold=330, dpi_target=300, quality=82)   # zdjęcia jako JPEG (bez tego ~6 MB)
        d.save(out, garbage=4, deflate=True)
        print(f'{out}: {d.page_count} stron, {len(groups)} grup, {sum(len(g["wiersze"]) for g in data)} indeksów')


if __name__ == '__main__':
    main()
