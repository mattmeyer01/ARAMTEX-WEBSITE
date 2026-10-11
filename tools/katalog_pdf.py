"""Składa katalogi PDF w identyfikacji Armatex: Besco 2026, Besco INOX 304 i 316L, Tectite, Kuterlite.

Użycie:
    pip install playwright==1.56.0 pymupdf fonttools brotli
    python3 tools/katalog_pdf.py inox-304               # → pliki/katalog-besco-inox-304.pdf
    python3 tools/katalog_pdf.py besco-2026 tectite     # kilka naraz
    python3 tools/katalog_pdf.py wszystkie
    python3 tools/katalog_pdf.py tectite --out x.pdf    # podgląd do innego pliku (jeden katalog)

Dane (tools/katalog-pdf/):
    <katalog>.json  grupy: id, kod, nazwa, seria (katalogi wieloseryjne), zdjecie (ścieżka od katalogu głównego), gwint,
                    wiersze [wymiar, nr artykułu, opak. 1, opak. 2] (ilości None, gdy producent ich nie podaje).
                    INOX 304 z warstwy tekstowej katalogu Besco, INOX 316L z data/besco-2026.json (OCR) sprawdzone
                    wiersz po wierszu z katalogiem; Besco 2026, Tectite i Kuterlite składa tools/katalog_dane.py.
    besco.png, pegler-dark.png, pegler-light.png, tectite.png   logo marek (z katalogów producentów)
    pzh.webp        znak „Produkt z atestem” NIZP PZH-PIB
    foto/           zdjęcia powiększone do druku (tools/powieksz_zdjecia.py), gdy zdjęcia ze strony są za małe
    katalog.css     wygląd (kolory i fonty jak w c.css)

Treść każdego katalogu (okładka, strona 2, działy, marka) jest w KATALOGI; teksty i parametry pochodzą ze strony
(tools/strony.py) i z katalogów producentów.

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
e = html.escape


def asset(name):
    return f'file://{DIR}/{name}'


BESCO = dict(name='Besco', logo='besco.png', logo_dark=None, producer='Besco',
             box_title='Produkty marki Besco',
             box_text='Wszystkie produkty w katalogu to złączki Besco Fittings &amp; Connectors. '
                      'Armatex jest dystrybutorem marki Besco od 2016 roku.',
             rel='Armatex jest dystrybutorem Besco od 2016 roku', dist='Dystrybutor marki<br>od 2016 roku',
             cover_lbl='Produkty marki')
PEGLER = dict(name='Pegler Yorkshire', logo='pegler-dark.png', logo_dark='pegler-light.png', producer='Pegler Yorkshire',
              box_title='Produkty Pegler Yorkshire',
              box_text='Wszystkie produkty w katalogu to wyroby Pegler Yorkshire. '
                       'Armatex jest oficjalnym przedstawicielem Pegler Yorkshire w Polsce.',
              rel='Armatex jest oficjalnym przedstawicielem Pegler Yorkshire w Polsce', dist='Oficjalny przedstawiciel<br>w Polsce',
              cover_lbl='Producent')

GW_PRESS, GW_BOSY = 'kielich press × gwint wewnętrzny', 'bosy koniec × gwint wewnętrzny'
GZ_PRESS, GZ_BOSY = 'kielich press × gwint zewnętrzny', 'bosy koniec × gwint zewnętrzny'
LEGEND_PRESS = [('ww', 'kielich × kielich'), ('wz', 'kielich × bosy koniec'), ('zz', 'bosy koniec × bosy koniec'),
                ('GW', 'gwint wewnętrzny'), ('GZ', 'gwint zewnętrzny')]
OPAK = ('Opak.', 'Karton', 'liczba sztuk w woreczku', 'liczba sztuk w kartonie')
WYSZUKIWARKA = ('armatex.pl/wyszukiwarka', '1 936 indeksów Besco z listą do wyceny')


def inox(name, material, sizes, sizes_od, app, app_cover, h2, extra_specs, cover_tag, pzh, pzh_cover, hero, sections, opis):
    """Katalogi INOX: jedna linia, działy według rodzaju kształtek, spis treści z grupami."""
    return dict(
        file=f'katalog-besco-{name.lower().replace(" ", "-")}.pdf', title=f'Złączki zaprasowane Besco {name}',
        header=f'Złączki zaprasowane {name} · profil M', brand=BESCO, head_logo='besco.png', kod='Besco', qty=OPAK,
        cover=dict(eyebrow='Produkty marki Besco · stal nierdzewna · system press', small='Złączki zaprasowane', big=name,
                   sub=f'Profil M · Ø {sizes} · {{grupy}} · {{indeksy}}{cover_tag}', hero=hero,
                   facts=[('16 bar', 'ciśnienie'), ('−10…110 °C', 'temperatura'), (app_cover, 'zastosowanie')],
                   badge=pzh_cover),
        intro=dict(h2=h2, lead=f'Złączki zaprasowane Besco {name} w profilu M łączą rury ze stali nierdzewnej przez zaprasowanie – '
                               f'bez gwintowania i spawania. W katalogu jest {{grupy}} produktów i {{indeksy}} w średnicach {sizes_od}.',
                   specs=[('Materiał', material), ('Profil zaprasowania', 'M'), ('Średnice', sizes), ('Ciśnienie', '16 bar'),
                          ('Temperatura', '−10…110 °C'), ('Zastosowanie', app)] + extra_specs,
                   boxes=[('pzh', 'Atest higieniczny PZH', pzh)],
                   legend=LEGEND_PRESS + [('M', 'zaprasowywać szczękami o profilu M')], toc='groups'),
        sections=[dict(name=n, ids=ids) for n, ids in sections], opis=opis, ws=WYSZUKIWARKA,
        back='Wszystkie indeksy Besco znajdziesz też w wyszukiwarce na armatex.pl.')


def ser(sid, name, sizes, bar, temp, media, appr=''):
    """Dział katalogu wieloseryjnego = seria z danych; parametry do nagłówka działu i tabeli serii na stronie 2."""
    return dict(seria=sid, name=name, meta=dict(sizes=sizes, bar=bar, temp=temp, media=media, appr=appr))


KATALOGI = {
    'inox-304': inox(
        'INOX 304', 'Stal nierdzewna 304', '15–108 mm', 'od 15 do 108 mm', 'Ogrzewanie i woda pitna', 'Ogrzewanie<br>i woda pitna',
        'Złączki press ze stali nierdzewnej do instalacji wody pitnej i ogrzewania', [], '',
        'Złączki INOX 304 mają atest higieniczny Narodowego Instytutu Zdrowia Publicznego PZH – PIB '
        '(B.BK.60110.1654.2026) do instalacji wody pitnej i ciepłej wody użytkowej.',
        'atest higieniczny<br>PZH', ('3002', '3130', '3270G'),
        [('Mufy, redukcje i zaślepki', ['3270', '3271', '3240', '3243', '3301']),
         ('Łuki i mijanki', ['3002', '3001', '3041', '3040', '3030', '3085', '3086']),
         ('Trójniki', ['3130', '3130R', '3130G']),
         ('Przejścia gwintowane i kołnierzowe', ['3270G', '3281', '3243G', '3280', '3002G', '3001G', '3472G', '3358G', '3331G', '3510'])],
        {'3270G': GW_PRESS, '3281': GW_BOSY, '3243G': GZ_PRESS, '3280': GZ_BOSY}),
    'inox-316l': inox(
        'INOX 316L', 'Stal nierdzewna 316L', '15–168,3 mm', 'od 15 do 168,3 mm', 'Woda, ogrzewanie i przemysł', 'Woda, ogrzewanie<br>i przemysł',
        'Złączki press ze stali nierdzewnej 316L do wody, ogrzewania i przemysłu',
        [('Aprobaty', 'DVGW · WRAS'), ('Atest PZH', 'Ø 15–108 mm')], ' · DVGW · WRAS',
        'Złączki INOX 316L mają atest higieniczny Narodowego Instytutu Zdrowia Publicznego PZH – PIB '
        '(B.BK.60110.1480.2025) do instalacji wody pitnej i ciepłej wody użytkowej, dla średnic 15–108 mm.',
        'atest PZH<br>Ø 15–108 mm', ('12200', '12100', '12020'),
        [('Mufy, redukcje i zaślepki', ['12000', '12040', '12430', '12410']),
         ('Łuki i mijanki', ['12200', '12210', '12230', '12240', '12350', '12360']),
         ('Trójniki', ['12100', '12110', '12120']),
         ('Przejścia gwintowane i kołnierzowe', ['12020', '12460', '12010', '12450', '12320', '12310', '12340', '12070', '12080', '12400'])],
        {'12020': GW_PRESS, '12460': GW_BOSY, '12010': GZ_PRESS, '12450': GZ_BOSY}),
    # parametry linii Besco: data/besco-2026.json (katalog Besco 2026), atesty jak na stronie (tools/strony.py, SYS)
    'besco-2026': dict(
        file='katalog-besco-2026.pdf', title='Złączki Besco 2026', header='Złączki zaprasowane i lutowane Besco 2026',
        brand=BESCO, head_logo='besco.png', kod='Besco', qty=OPAK,
        cover=dict(eyebrow='Produkty marki Besco · miedź, stal i zawory', small='Złączki zaprasowane i lutowane', big='Besco 2026',
                   sub='Press V i M · lutowane EN 1254 · ANSI · G-size · {grupy} · {indeksy}', hero=('GP5130', '5002', 'GPV600'),
                   facts=[('9 linii', 'miedź, stal węglowa, zawory'), ('6–108 mm', 'oraz calowe 1/4"–4 1/8"'),
                          ('Press i lut', 'profile V i M, EN 1254')], badge='atest PZH: miedź<br>do wody V i M'),
        intro=dict(h2='Złączki zaprasowane, lutowane i zawory kulowe Besco',
                   lead='Miedziane złączki zaprasowane Gutpress Copper (profil V i M, woda i gaz), Gutpress Carbon Steel, zawory '
                        'kulowe press oraz kształtki lutowane EN 1254, ANSI B16.22 i G-size: {grupy} produktów i {indeksy}. '
                        'Złączki INOX 304 i 316L mają osobne katalogi.',
                   boxes=[('pzh', 'Atest higieniczny PZH', 'Złączki Gutpress Copper do wody w profilach V i M mają atest higieniczny '
                                                           'Narodowego Instytutu Zdrowia Publicznego PZH – PIB.')],
                   legend=LEGEND_PRESS + [('V, M', 'profil zaprasowania')], toc='sections'),
        sections=[ser('cu-press-water-v', 'Gutpress Copper, profil V · woda', '12–54 mm', '16 bar', '−10…110 °C', 'woda, CO, przemysł', 'DVGW · KIWA · WRAS · RISE · PZH'),
                  ser('cu-press-water-m', 'Gutpress Copper, profil M · woda', '12–108 mm', '16 bar', '−10…110 °C', 'woda, CO, przemysł', 'DVGW · WRAS · RISE · PZH'),
                  ser('cu-press-gas-v', 'Gutpress Copper, profil V · gaz', '15–35 mm', '5 bar', '−20…70 °C', 'gaz ziemny, LPG', 'DVGW · INiG'),
                  ser('cu-press-gas-m', 'Gutpress Copper, profil M · gaz', '15–35 mm', '5 bar', '−20…70 °C', 'gaz ziemny, LPG', 'DVGW · INiG'),
                  ser('steel-press-m', 'Gutpress Carbon Steel, profil M', '12–108 mm', '16 bar', '−10…110 °C', 'CO w obiegu zamkniętym, sprężone powietrze', 'ITB'),
                  ser('press-ball-valve', 'Gutpress Zawory Kulowe V i M', '15–54 mm', '16 bar', '−10…110 °C', 'woda, CO', 'DVGW · WRAS'),
                  ser('cu-solder-en1254', 'Miedź lutowana EN 1254, seria 4000 i 5000', '6–108 mm', '25 bar', '−20…110 °C', 'woda, CO, gaz, przemysł', 'DVGW · KIWA · WRAS'),
                  ser('cu-ansi-k', 'Miedź calowa ANSI B16.22, seria K', '1/4"–4 1/8"', '25 bar', '−20…110 °C', 'woda, CO, gaz, przemysł'),
                  ser('cu-g-size', 'Miedź G-size do wysokich ciśnień', '22–76,1 mm', '20–80 bar', '−20…150 °C', 'chłodnictwo, przemysł')],
        opis={}, ws=WYSZUKIWARKA, back='Wszystkie indeksy Besco znajdziesz też w wyszukiwarce na armatex.pl.'),
    # parametry: data/pegler.json i opis systemu na stronie (tools/strony.py, zlaczki-na-wcisk-tectite)
    'tectite': dict(
        file='katalog-tectite.pdf', title='Złączki i zawory na wcisk Tectite', header='Złączki i zawory na wcisk Tectite',
        brand=PEGLER, head_logo='tectite.png', kod='Tectite', kod_ser={'tectite-zawory': 'Pegler'}, qty=None,
        cover=dict(eyebrow='Pegler Yorkshire · system push-fit', small='Złączki i zawory na wcisk', big='Tectite',
                   sub='Classic · Pro · 316 · zawory · Tec-Tools · {grupy} · {indeksy}', hero=('tectite-trojnik-t24', 'tectite-kolano-t12', 'tectite-zawor-kulowy-na-wcisk-pt550'),
                   facts=[('10–54 mm', 'średnice'), ('Na wcisk', 'bez narzędzi, prądu i ognia'), ('25 lat', 'gwarancji producenta')],
                   badge=None, logo='tectite.png'),
        intro=dict(h2='System push-fit Tectite: złączki i zawory na wcisk',
                   lead='Tectite montuje się bez narzędzi, prądu i otwartego ognia. System łączy rury miedziane, PEX, PB, ze stali '
                        'nierdzewnej i węglowej, zależnie od linii. W katalogu: Tectite Classic, Pro i 316, zawory na wcisk Pegler '
                        'i akcesoria Tec-Tools – {grupy} produktów i {indeksy}.',
                   boxes=[('note', 'Gwarancja i demontaż', 'Producent daje 25 lat gwarancji na Tectite Classic, Pro i 316 z rurami innych '
                                                          'producentów oraz 30 lat z rurami Yorkshire, jeśli montaż jest zgodny z instrukcją. '
                                                          'Złączki Classic, Pro i 316 są demontowalne.')],
                   legend=[('GW', 'gwint wewnętrzny'), ('GZ', 'gwint zewnętrzny'), ('PEX, PB', 'rury łączy się z tulejką wzmacniającą'),
                           ('chrom', 'wersja chromowana')], toc='sections'),
        sections=[ser('tectite-classic', 'Tectite Classic', '10–28 mm', '16 bar z miedzią', '−24…95 °C z miedzią', 'woda, CO · miedź, PEX, PB', 'WRAS · PZH'),
                  ser('tectite-pro', 'Tectite Pro', '15–54 mm', '', '', 'miedź, PEX, PB, stal węglowa ocynkowana · demontowalne'),
                  ser('tectite-316', 'Tectite 316', '15–54 mm', '', '', 'rury ze stali nierdzewnej · demontowalne'),
                  ser('tectite-zawory', 'Zawory i filtry na wcisk Pegler', '15–54 mm', '', '', 'kulowe, odcinające, mieszające, filtr'),
                  ser('tectite-akcesoria', 'Akcesoria i narzędzia Tec-Tools', '', '', '', 'tulejki, gratowniki, mierniki, kalibratory')],
        opis={}, ws=('armatex.pl/zlaczki-na-wcisk-tectite', 'każdy produkt z listą do wyceny'),
        back='Wszystkie produkty Tectite znajdziesz też na armatex.pl, z listą do wyceny.'),
    # parametry: data/pegler.json i opis systemu na stronie (tools/strony.py, zlaczki-skrecane-kuterlite)
    'kuterlite': dict(
        file='katalog-kuterlite.pdf', title='Złączki skręcane Kuterlite', header='Złączki skręcane Kuterlite',
        brand=PEGLER, head_logo='pegler-dark.png', kod='Kuterlite', qty=('Opak. 1', 'Opak. 2', 'mniejsze opakowanie zbiorcze (szt.)',
                                                                        'większe opakowanie zbiorcze (szt.)'),
        cover=dict(eyebrow='Pegler Yorkshire · złączki zaciskowe do miedzi', small='Złączki skręcane', big='Kuterlite',
                   sub='K900 Pro · zawory · akcesoria · {grupy} · {indeksy}', hero=('kuterlite-trojnik-rownoprzelotowy-k918x', 'kuterlite-kolano-k915x', 'kuterlite-zawor-odcinajacy-k551'),
                   facts=[('8–54 mm', 'rury miedziane'), ('Zaciskowe', 'montaż kluczem, bez lutowania'), ('Mosiądz', 'złączki z pierścieniem'),
                          ('Zawory', 'z końcówkami zaciskowymi')],
                   badge=None),
        intro=dict(h2='Złączki zaciskowe Kuterlite do rur miedzianych',
                   lead='Mosiężne złączki zaciskowe z pierścieniem do rur miedzianych 8–54 mm. Montaż kluczem, bez lutowania i zaciskarki. '
                        'W katalogu: seria K900 Pro, zawory z końcówkami zaciskowymi oraz nakrętki, pierścienie i tulejki – '
                        '{grupy} produktów i {indeksy}.',
                   boxes=[('note', 'Opakowania', 'Każda pozycja ma w cenniku producenta dwa opakowania zbiorcze, na przykład złączka '
                                                 'prosta K910X 15 mm: 5 i 150 sztuk. Wymiary trójników według oznaczeń UK.')],
                   legend=[('GW', 'gwint wewnętrzny'), ('GZ', 'gwint zewnętrzny'), ('chrom', 'wersja chromowana'),
                           ('BSP', 'gwint calowy (walcowy lub stożkowy)')], toc='sections'),
        sections=[ser('kuterlite-k900', 'Kuterlite K900 Pro', '8–54 mm', '', '', 'złączki, kolana, trójniki, przejścia GW/GZ do rur miedzianych'),
                  ser('kuterlite-zawory', 'Zawory z końcówkami zaciskowymi', '15–28 mm', '', '', 'kurki i zawory odcinające, podłączenia urządzeń'),
                  ser('kuterlite-akcesoria', 'Akcesoria Kuterlite', '', '', '', 'nakrętki, pierścienie i tulejki')],
        opis={}, ws=('armatex.pl/zlaczki-skrecane-kuterlite', 'każdy produkt z listą do wyceny'),
        back='Wszystkie produkty Kuterlite znajdziesz też na armatex.pl, z listą do wyceny.'),
}
K = None   # bieżący katalog (main)

# Wymiary układu (pt). Wysokości w CSS są te same, więc obliczony podział zgadza się z wydrukiem.
COL_H = 716          # wysokość kolumny na stronie produktów
SEC_H = 58           # nagłówek działu (w kolumnie)
SEC_META_H = 86      # nagłówek działu z parametrami serii
HEAD_H = 84          # głowa karty (zdjęcie + nazwa)
CONT_H = 30          # głowa karty kontynuacji
TH_H = 20            # nagłówek tabeli
ROW_H = 14.5         # wiersz tabeli
PAD_H = 6            # dół karty
GAP = 12             # odstęp między kartami
MIN_SPLIT = 6        # najmniej wierszy w części tabeli po podziale
CTA_H = 330          # panel „zapytaj o wycenę” na końcu
RED, RED2 = '#dc291e', '#b91f15'


def card_h(rows, cont=False):
    return (CONT_H if cont else HEAD_H) + TH_H + ROW_H * rows + PAD_H + 1.5  # 1.5 = ramka


def sec_h(sec):
    return SEC_META_H if sec.get('meta') else SEC_H


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


def plural(n, one='indeks', few='indeksy', many='indeksów'):
    if n == 1:
        return one
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return few
    return many


def num(n):
    return f'{n:,}'.replace(',', ' ')


def grupy(n):
    return f'{num(n)} {plural(n, "grupa", "grupy", "grup")}'


def indeksy(n):
    return f'{num(n)} {plural(n)}'


def size_range(rows):
    first = [r[0].split(' × ')[0].split(' · ')[0].split(' (')[0] for r in rows]
    try:
        vals = sorted(set(first), key=lambda x: float(x.replace(',', '.')))
    except ValueError:      # cale (ANSI), wymiary opisowe: pierwszy i ostatni wiersz
        vals = [v for v in first if v != '–']
        if not vals:
            return ''
        vals = [vals[0], vals[-1]] if vals[0] != vals[-1] else [vals[0]]
        return ' · ' + size_txt(f'{vals[0]}–{vals[-1]}' if len(vals) > 1 else vals[0])
    unit = '' if '″' in vals[0] else ' mm'
    return ' · ' + (f'Ø {vals[0]}–{vals[-1]}{unit}' if len(vals) > 1 else f'Ø {vals[0]}{unit}')


def paginate(groups, sections):
    """Układa nagłówki działów i karty w kolumny, po kolei, bez pustych miejsc między działami.
    Zwraca listę stron: [[element, ...], [element, ...]], gdzie element to {'sec': dział} albo kawałek karty."""
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

    for sec in sections:
        first = groups[sec['ids'][0]]['wiersze']
        if sec_h(sec) + GAP + card_h(len(first) if len(first) <= 12 else MIN_SPLIT) + gap() > state['rem']:
            next_col()
        put({'sec': sec}, sec_h(sec))
        for gid in sec['ids']:
            g = groups[gid]
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


FRAC = {'1/2': '½', '1/4': '¼', '3/4': '¾'}   # Outfit nie ma ósemek (⅛, ⅜…)


def size_txt(s):
    """Wymiar do druku: „1 1/4″” → „1¼"”, „1/2″” → „½"” (Outfit nie ma znaku ″; numery artykułów bez zmian).
    Pozostałe ułamki (np. 3/8) zostają z ukośnikiem."""
    s = s.replace('″', '"')
    s = re.sub(r'(\d) (\d/\d)\b', lambda m: m.group(1) + FRAC.get(m.group(2), ' ' + m.group(2)), s)
    return re.sub(r'(?<![\d/])(\d/\d)(?![\d/])', lambda m: FRAC.get(m.group(1), m.group(1)), s)


COL_W = 256.6     # szerokość kolumny strony (pt)


# zagęszczenie tabeli: (czcionka wymiaru, czcionka numeru, odstępy kolumny wymiaru, odstępy kolumny numeru)
TIGHT = [(8, 7.3, 17, 12), (6.9, 7.3, 17, 12), (6.6, 6.3, 12, 8), (6.4, 6.0, 10, 7)]


def table(part):
    """Tabela grupy. Szerokości kolumn z długości treści (cała grupa, żeby części po podziale były równe): numer
    artykułu dostaje tyle, ile potrzebuje, wymiar resztę; gdy brakuje miejsca, mniejsza czcionka (TIGHT)."""
    g = part['g']
    unit = ('cal' if all('×' not in r[0] or r[0].count('″') == r[0].count('×') + 1 for r in g['wiersze'])
            and g['wiersze'][0][0].endswith('″') else 'mm × cal') if g['gwint'] else 'mm'
    # same cale: bez znaku " (jest w nagłówku) i z łącznikiem jak w katalogu Besco: 1-3/8 (1 3/8 przy małej czcionce czyta się jak 13/8)
    show = (lambda s: re.sub(r'(\d) (\d/\d)', r'\1-\2', s).replace('″', '')) if unit == 'cal' else size_txt
    q = K['qty']
    qw = (42 if len(q[1]) > 6 else 38) if q else 0
    sizes = [show(r[0]) for r in g['wiersze']]
    ls, la = max(len(x) for x in sizes), max(len(r[1]) for r in g['wiersze'])
    hdr = 76 if 'cal' in unit else 52
    for lvl, (fs, fa, ps, pa) in enumerate(TIGHT):
        if lvl == 3 and q:
            qw = 33                                   # ostatni stopień: węższe kolumny ilości
        avail = COL_W - 1.5 - 2 * qw
        need_s, need_a = max(ls * 0.52 * fs + ps, hdr), la * 0.6 * fa + pa
        if need_s + need_a <= avail:
            break
    ws = max(need_s, avail - need_a - max(0, avail - need_s - need_a) * 0.55)
    wa = avail - ws
    cols = f'<col style="width:{ws:.1f}pt"><col style="width:{wa:.1f}pt">' + (f'<col style="width:{qw}pt">' * 2 if q else '')
    cells = (lambda b, c: f'<td class="n">{"–" if b in (None, 0) else b}</td><td class="n">{"–" if c in (None, 0) else c}</td>') if q else (lambda b, c: '')
    rows = ''.join(f'<tr><td>{e(show(s))}</td><td class="art">{e(a)}</td>{cells(b, c)}</tr>' for s, a, b, c in part['rows'])
    head = f'<th class="n">{q[0]}</th><th class="n">{q[1]}</th>' if q else ''
    return (f'<table class="t{lvl}"><colgroup>{cols}</colgroup><thead><tr><th>Wymiar <i>{unit}</i></th>'
            f'<th>Nr artykułu</th>{head}</tr></thead><tbody>{rows}</tbody></table>')


def kod(g):
    return K.get('kod_ser', {}).get(g.get('seria'), K['kod'])


def card(part):
    g = part['g']
    if part['cont']:
        return (f'<article class="card cont"><div class="ch"><b>{e(g["nazwa"])}</b><span>{e(g["kod"])} · cd.</span></div>'
                f'{table(part)}</article>')
    n = len(g['wiersze'])
    opis = f'<p class="opis">{e(K["opis"][g["kod"]])}</p>' if g['kod'] in K['opis'] else ''
    return (f'<article class="card"><div class="head"><div class="foto"><img src="{foto(g)}" alt=""></div>'
            f'<div class="tt"><span class="kod"><em>{e(kod(g))}</em> {e(g["kod"])}</span><h3>{e(g["nazwa"])}</h3>{opis}'
            f'<p class="meta">{indeksy(n)}{size_range(g["wiersze"])}</p></div></div>'
            f'{table(part)}</article>')


def meta_line(m):
    return ' · '.join(x for x in (m['sizes'], m['bar'], m['temp'], m['media'], m['appr']) if x)


def sec_head(sec):
    meta = f'<p class="sm">{e(meta_line(sec["meta"]))}</p>' if sec.get('meta') else ''
    return (f'<div class="sh{" meta" if meta else ""}"><span class="sn">{sec["nr"]:02d}</span><div>'
            f'<span class="eyebrow">Dział {sec["nr"]} z {len(K["sections"])}</span><h2>{e(sec["name"])}</h2>{meta}</div></div>')


def cta():
    return f'''<div class="cta">{stripes(150, 190, [(40, 40, 210, 26, RED), (95, 10, 210, 26, RED2)], 's-cta', rx=7)}
  <span class="eyebrow">Zamówienia i wyceny</span>
  <h3>Wyślij listę indeksów – przygotujemy wycenę</h3>
  <p>Podaj numery artykułów i ilości. Odpowiemy z ceną i terminem.</p>
  <dl><div><dt>Biuro</dt><dd><b>513 191 502</b>biuro@armatex.pl</dd></div>
      <div><dt>Sprzedaż</dt><dd><b>798 807 106</b>piotr@armatex.pl</dd></div></dl>
  <div class="ws"><b>{e(K["ws"][0])}</b><span>{e(K["ws"][1])}</span></div>
</div>'''


def block(x):
    if 'sec' in x:
        return sec_head(x['sec'])
    if 'cta' in x:
        return cta()
    if 'notes' in x:
        return '<div class="notes"><span class="eyebrow">Notatki</span><div class="lines">' + '<i></i>' * 40 + '</div></div>'
    return card(x)


def foto(g):
    """Zdjęcie grupy: powiększone do druku (tools/katalog-pdf/foto), a jeśli go nie ma, to ze strony."""
    big = os.path.join(DIR, 'foto', os.path.basename(g['zdjecie']).replace('-l.webp', '.webp'))
    return 'file://' + (big if os.path.exists(big) else os.path.join(ROOT, g['zdjecie']))


def head(cls=''):
    return (f'<header class="ph"><img src="file://{ROOT}/assets/img/logo-dark.png" alt="Armatex">'
            f'<span class="r">{e(K["header"])}<img class="{cls}" src="{asset(K["head_logo"])}" alt=""></span></header>')


def foot(no):
    return f'<footer class="pf"><span><b>armatex.pl</b> · biuro@armatex.pl · 513 191 502</span><span class="pn">{no:02d}</span></footer>'


def frame(no, cols):
    inner = ''.join('<div class="col">' + ''.join(block(x) for x in col) + '</div>' for col in cols)
    return f'<section class="page prod">{head()}<div class="body"><div class="cols">{inner}</div></div>{foot(no)}</section>'


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


def brand_logo(dark=False):
    b = K['brand']
    if dark and b['logo_dark']:
        return f'<img class="bl" src="{asset(b["logo_dark"])}" alt="{e(b["name"])}">'
    return f'<span class="plate"><img class="bl" src="{asset(b["logo"])}" alt="{e(b["name"])}"></span>' if dark else \
        f'<img class="bl" src="{asset(b["logo"])}" alt="{e(b["name"])}">'


def build_html(groups, sections, pages, first_page, faces):
    total = sum(len(g['wiersze']) for g in groups.values())
    fmt = dict(grupy=grupy(len(groups)), indeksy=indeksy(total))
    where, sec_page = {}, {}
    for i, cols in enumerate(pages):
        for col in cols:
            for x in col:
                if 'sec' in x:
                    sec_page.setdefault(x['sec']['nr'], first_page + i)
                elif 'g' in x:
                    where.setdefault(x['g']['id'], first_page + i)
    toc = ''
    for sec in sections:
        items = ''
        if K['intro']['toc'] == 'groups':
            items = '<ol>' + ''.join(f'<li><span class="k">{e(groups[i]["kod"])}</span><span class="t">{e(groups[i]["nazwa"])}</span>'
                                     f'<span class="d"></span><span class="p">{where[i]:02d}</span></li>' for i in sec['ids']) + '</ol>'
        else:
            n = sum(len(groups[i]['wiersze']) for i in sec['ids'])
            items = f'<p class="tn">{grupy(len(sec["ids"]))} · {indeksy(n)}</p>'
        toc += (f'<div class="tsec"><h4><span>{sec["nr"]:02d}</span>{e(sec["name"])}<em>{sec_page[sec["nr"]]:02d}</em></h4>{items}</div>')

    prod = ''.join(frame(first_page + i, cols) for i, cols in enumerate(pages))
    logo_l = f'file://{ROOT}/assets/img/logo-light.png'
    pzh = asset('pzh.webp')
    c, it, b = K['cover'], K['intro'], K['brand']
    hero = ''.join(f'<img src="{foto(groups[i])}" alt="">' for i in c['hero'])
    name_cls = ' long' if len(c['big']) > 8 else ''
    facts = ''.join(f'<div><b>{v}</b><span>{e(k)}</span></div>' for v, k in c['facts'])
    if c['badge']:
        facts += f'<div class="pzh"><img src="{pzh}" alt="PZH – produkt z atestem"><span>{c["badge"]}</span></div>'
    elif c.get('logo'):
        facts += f'<div class="pzh"><img class="wide" src="{asset(c["logo"])}" alt=""></div>'

    if it.get('specs'):
        specs = f'<div class="specs n{len(it["specs"])}">' + ''.join(f'<div><span>{e(k)}</span><b>{e(v)}</b></div>' for k, v in it['specs']) + '</div>'
    else:   # tabela serii
        rows = ''.join(f'<tr><td><b>{e(s["name"])}</b></td><td>{e(s["meta"]["sizes"] or "–")}</td>'
                       f'<td>{e(" · ".join(x for x in (s["meta"]["bar"], s["meta"]["temp"]) if x) or "–")}</td>'
                       f'<td>{e(s["meta"]["media"])}</td><td>{e(s["meta"]["appr"] or "–")}</td></tr>' for s in sections)
        specs = ('<table class="sers"><thead><tr><th>Seria</th><th>Średnice</th><th>Parametry</th><th>Zastosowanie</th>'
                 f'<th>Atesty</th></tr></thead><tbody>{rows}</tbody></table>')
    boxes = (f'<div class="box brandbox"><img src="{asset(b["logo"])}" alt=""><div><b>{b["box_title"]}</b><p>{b["box_text"]}</p></div></div>')
    for kind, t, txt in it['boxes']:
        img = f'<img src="{pzh}" alt="">' if kind == 'pzh' else ''
        boxes += f'<div class="box pzhbox{" note" if kind != "pzh" else ""}">{img}<div><b>{e(t)}</b><p>{e(txt)}</p></div></div>'
    legend = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in it['legend'])
    q = K['qty']
    read = '<div><dt>Wymiar</dt><dd>średnica rury w mm; gwint w calach (")</dd></div>'
    if q:
        read += f'<div><dt>{q[0]}</dt><dd>{q[2]}</dd></div><div><dt>{q[1]}</dt><dd>{q[3]}</dd></div>'

    cover = f'''<section class="page cover">
  <div class="top">
    {stripes(595.28, 478, [(330, -10, 280, 70, RED), (430, 60, 488, 70, RED2)], 's-cover')}
    <img class="logo" src="{logo_l}" alt="Armatex">
    <span class="tag">Katalog produktów · 2026</span>
    <div class="title">
      <span class="eyebrow">{e(c["eyebrow"])}</span>
      <h1>{e(c["small"])}<b class="{name_cls}">{e(c["big"])}</b></h1>
      <p>{e(c["sub"].format(**fmt))}</p>
    </div>
  </div>
  <div class="hero">{hero}</div>
  <div class="facts">{facts}</div>
  <footer><b>armatex.pl</b><span class="brand">{b["cover_lbl"]}{brand_logo()}</span></footer>
</section>'''

    intro = f'''<section class="page intro">
  {head()}
  <div class="body">
    <span class="eyebrow">O katalogu</span>
    <h2 class="big">{e(it["h2"])}</h2>
    <p class="lead">{e(it["lead"].format(**fmt))} {b["rel"]} – zapytaj nas o dostępność i ceny dla hurtowni.</p>
    {specs}
    <div class="two">
      <div>
        {boxes}
        <h4 class="h4">Skróty w nazwach</h4>
        <dl class="legend{" grid2" if it["toc"] == "sections" else ""}">{legend}</dl>
        <h4 class="h4">Jak czytać tabele</h4>
        <dl class="legend">{read}</dl>
      </div>
      <div class="toc toc-{it["toc"]}"><h4 class="h4">Spis treści</h4>{toc}</div>
    </div>
  </div>
  {foot(2)}
</section>'''

    back = f'''<section class="page back">
  {stripes(595.28, 841.89, [(485, 600, 860, 70, RED), (400, 600, 860, 70, RED2)], 's-back')}
  <img class="logo" src="{logo_l}" alt="Armatex">
  <div class="cta">
    <span class="eyebrow">Zamówienia i wyceny</span>
    <h2>Zapytaj o dostępność<br>i ceny dla hurtowni</h2>
    <p>Wyślij listę indeksów – odpowiemy z ceną i terminem. {e(K["back"])}</p>
  </div>
  <div class="people">
    <div><span class="label">Biuro</span><b>513 191 502</b><a>biuro@armatex.pl</a><p>ul. Składowa 3a, 10-421 Olsztyn<br>pn–pt 7:00–18:00</p></div>
    <div><span class="label">Sprzedaż</span><b>798 807 106</b><a>piotr@armatex.pl</a><p>Piotr Stelmach</p></div>
    <div><span class="label">Magazyn</span><b>512 945 936</b><a>martyna@armatex.pl</a><p>Martyna Zielińska</p></div>
  </div>
  <div class="web"><b>armatex.pl</b><span>Od 1991 roku na rynku instalacyjnym</span></div>
  <div class="dist"><span>{b["dist"]}</span>{brand_logo()}</div>
  <footer>
    <span>P.H.U. ARMATEX Sp. J. A. J. Bunda · siedziba: ul. Siewna 24, 10-831 Olsztyn · NIP 7393814110 · KRS 0000371628 · REGON 280563743</span>
    <span>Dane techniczne i numery artykułów według producenta ({e(b["producer"])}). Zastrzegamy prawo do zmian. Stan na 2026 r.</span>
  </footer>
</section>'''

    css = faces + open(os.path.join(DIR, 'katalog.css'), encoding='utf-8').read().replace('{ROOT}', ROOT)
    return (f'<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>{e(title())}</title>'
            f'<style>{css}</style></head><body class="{K["id"]}">{cover}{intro}{prod}{back}</body></html>')


def title():
    return f'{K["title"]} – katalog Armatex 2026'


def sections_of(groups):
    """Działy katalogu: z listy identyfikatorów (INOX) albo z serii w danych (kolejność jak w pliku)."""
    out = []
    for nr, s in enumerate(K['sections'], 1):
        ids = s.get('ids') or [g['id'] for g in groups.values() if g.get('seria') == s['seria']]
        assert ids, s
        out.append(dict(s, nr=nr, ids=ids))
    used = [i for s in out for i in s['ids']]
    assert sorted(used) == sorted(groups), set(groups) ^ set(used)
    return out


def build(name, out):
    global K
    K = dict(KATALOGI[name], id=name)
    data = json.load(open(os.path.join(DIR, f'{name}.json'), encoding='utf-8'))
    for g in data:
        g.setdefault('id', g['kod'])
    groups = {g['id']: g for g in data}
    sections = sections_of(groups)
    pages = paginate(groups, sections)
    with tempfile.TemporaryDirectory() as tmp:
        doc_html = build_html(groups, sections, pages, 3, outfit_faces(tmp))
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
                ...[...document.querySelectorAll('td, th, h3, .tsec li, .sh h2, .sm')].filter(el => el.scrollWidth > el.clientWidth + 1)
              ].map(el => ((el.closest('.page').querySelector('.pn') || {}).textContent || 'okł.') + ' ' + el.tagName + '.'
                          + el.className + ' ' + el.textContent.slice(0, 30))''')
            if bad:
                msg = f'{name}: przelewa się: ' + '; '.join(' '.join(x.split()) for x in bad)
                if '--out' not in sys.argv:
                    sys.exit(msg)
                print(msg)
            pg.pdf(path=pdf, prefer_css_page_size=True, print_background=True)
            b.close()
        d = pymupdf.open(pdf)
        d.set_metadata({'title': title(), 'author': 'P.H.U. ARMATEX Sp. J. A. J. Bunda',
                        'subject': f'{K["title"]}: {grupy(len(groups))}, {indeksy(sum(len(g["wiersze"]) for g in data))}',
                        'keywords': f'{K["title"]}, {K["brand"]["name"]}, katalog, Armatex',
                        'creator': 'Armatex', 'producer': 'Armatex'})
        d.xref_set_key(d.pdf_catalog(), 'Lang', '(pl-PL)')
        d.rewrite_images(dpi_threshold=330, dpi_target=300, quality=82)   # zdjęcia jako JPEG (bez tego kilka MB)
        d.save(out, garbage=4, deflate=True)
        print(f'{out}: {d.page_count} stron, {grupy(len(groups))}, {indeksy(sum(len(g["wiersze"]) for g in data))}')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    names = list(KATALOGI) if args == ['wszystkie'] else [a for a in args if a != out]
    if not names or any(n not in KATALOGI for n in names):
        sys.exit('Podaj katalog: ' + ', '.join(KATALOGI) + ' albo „wszystkie”')
    for n in names:
        build(n, out if out and len(names) == 1 else os.path.join(ROOT, 'pliki', KATALOGI[n]['file']))


if __name__ == '__main__':
    main()
