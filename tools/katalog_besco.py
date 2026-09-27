"""Wyciąga dane i zdjęcia produktów z katalogu Besco (PDF) dla szkicu C.

Użycie:
    pip install pymupdf pillow
    python3 tools/katalog_besco.py sciezka/Besco_2026_catalogue.pdf

Wynik (nadpisywany):
    data/besco-2026.json   dane wyszukiwarki: linie, grupy, pozycje
    img/besco/x<xref>.webp zdjęcia produktów (tło wypalone na kolor kamienny strony)
    img/besco/karta-p3.webp render strony katalogu do sekcji dokumentów

Parser opiera się na stałych kolumnach tabel katalogu 2026 (rozmiar ~200 pt,
numer artykułu ~313 pt, worek ~458 pt, karton ~525 pt). Zakresy stron linii
(SERIES) i parametry z nagłówków (META) trzeba sprawdzić przy nowym wydaniu,
bo część nagłówków jest w PDF grafiką.
"""
import io
import json
import os
import re
import sys

import pymupdf
from PIL import Image, ImageChops

OUT = os.path.join(os.path.dirname(__file__), '..')
STONE = (243, 241, 236)

SERIES = [(3, 11, 'cu-press-water-v'), (12, 16, 'cu-press-gas-v'), (17, 26, 'cu-press-water-m'),
          (27, 30, 'cu-press-gas-m'), (31, 45, 'cu-solder-en1254'), (46, 54, 'cu-ansi-k'),
          (55, 56, 'cu-g-size'), (57, 64, 'steel-press-m'), (65, 65, 'press-ball-valve')]
META = {
    'cu-press-water-v': dict(name='Miedź press, profil V · woda', short='Miedź press V · woda', bar='16 bar', temp='−10…110 °C', media='woda, ogrzewanie, przemysł', std='EN 1254-7', appr=['DVGW', 'KIWA', 'WRAS', 'RISE']),
    'cu-press-water-m': dict(name='Miedź press, profil M · woda', short='Miedź press M · woda', bar='16 bar', temp='−10…110 °C', media='woda, ogrzewanie, przemysł', std='EN 1254-7', appr=['DVGW', 'WRAS', 'RISE']),
    'cu-press-gas-v': dict(name='Miedź press, profil V · gaz', short='Miedź press V · gaz', bar='5 bar', temp='−20…70 °C', media='gaz ziemny, LPG', std='EN 1254-7', appr=['DVGW', 'INiG']),
    'cu-press-gas-m': dict(name='Miedź press, profil M · gaz', short='Miedź press M · gaz', bar='5 bar', temp='−20…70 °C', media='gaz ziemny, LPG', std='EN 1254-7', appr=['DVGW', 'INiG']),
    'steel-press-m': dict(name='Stal węglowa press, profil M', short='Stal węglowa press', bar='16 bar', temp='−10…110 °C', media='ogrzewanie, sprężone powietrze', std='', appr=[]),
    'cu-solder-en1254': dict(name='Miedź lutowana EN 1254', short='Lutowane EN 1254', bar='25 bar', temp='−20…110 °C', media='woda, ogrzewanie, gaz, przemysł', std='EN 1254', appr=['DVGW', 'KIWA', 'WRAS']),
    'cu-ansi-k': dict(name='Miedź calowa ANSI B16.22 · seria K', short='ANSI B16.22 · K', bar='25 bar', temp='−20…110 °C', media='woda, ogrzewanie, gaz, przemysł', std='ANSI B16.22', appr=[]),
    'cu-g-size': dict(name='Miedź G-size · chłodnictwo i przemysł', short='G-size do 80 bar', bar='20–80 bar', temp='−20…150 °C', media='przemysł, chłodnictwo', std='EN 1254', appr=[]),
    'press-ball-valve': dict(name='Zawory kulowe press', short='Zawory kulowe press', bar='16 bar', temp='−10…110 °C', media='woda, ogrzewanie, przemysł', std='', appr=['DVGW', 'WRAS']),
}
ORDER = list(META)

# Nazwy handlowe PL (ww = kielich–kielich, wz = kielich–bosy koniec, GW/GZ = gwint wewn./zewn.)
PL = [('return bend 180', 'Łuk 180° powrotny'),
      ('v press ball balve p x p', 'Zawór kulowy press × press, profil V'), ('v press ball valve p x f', 'Zawór kulowy press × GW, profil V'),
      ('handel v press ball valve', 'Zawór kulowy press × press, trzpień przedłużony'), ('m press lever ball valve', 'Zawór kulowy press × press, profil M'),
      ('bend 90° male', 'Łuk 90° z GZ'), ('female bend 90°', 'Łuk 90° z GW'),
      ('bend tap connector', 'Półśrubunek kątowy 90°'), ('bent tap connector', 'Półśrubunek kątowy 90°'),
      ('bend 90° i/a', 'Łuk 90° wz'), ('bend 90° i/i', 'Łuk 90° ww'), ('bend 90°', 'Łuk 90° ww'),
      ('bend 45° i/a', 'Łuk 45° wz'), ('bend 45° i/i', 'Łuk 45° ww'), ('bend 45°', 'Łuk 45° ww'),
      ('female elbow 90°', 'Kolano 90° z GW'), ('elbow 90° female', 'Kolano 90° z GW'), ('male elbow 90°', 'Kolano 90° z GZ'), ('elbow 90° male', 'Kolano 90° z GZ'),
      ('elbow 90° i/a', 'Kolano 90° wz'), ('elbow 90° i/i', 'Kolano 90° ww'), ('elbow 90°', 'Kolano 90° ww'),
      ('sleeve coupling', 'Mufa przesuwna'), ('straight coupling', 'Mufa'),
      ('female reducing tee', 'Trójnik z GW'), ('female tee', 'Trójnik z GW'), ('threaded tee', 'Trójnik z GW'),
      ('equal tee', 'Trójnik równoprzelotowy'), ('reducing tee', 'Trójnik redukcyjny'),
      ('reducing coupling', 'Mufa redukcyjna ww'), ('fitting reducer', 'Redukcja wz'), ('cap end', 'Zaślepka'),
      ('full crossover', 'Mijanka ww'), ('part crossover', 'Mijanka wz'), ('partial crossover', 'Mijanka wz'),
      ('straight male adaptor', 'Złączka z GZ'), ('straight female adaptor', 'Złączka z GW'), ('male adaptor', 'Złączka z GZ'), ('female adaptor', 'Złączka z GW'),
      ('union bend', 'Śrubunek kątowy 90° z GZ'), ('male straight union', 'Śrubunek z GZ'), ('straight union ag', 'Śrubunek z GZ'), ('straight union mi', 'Śrubunek z GZ'),
      ('male union', 'Śrubunek z GZ'), ('union male', 'Śrubunek z GZ'), ('straight union fi', 'Śrubunek z GW'), ('union female', 'Śrubunek z GW'),
      ('straight union pxp', 'Śrubunek press × press'), ('straight union', 'Śrubunek press × press'),
      ('female tap connector', 'Półśrubunek z GW'), ('staight tap connector', 'Półśrubunek z GW'), ('straight tap connector', 'Półśrubunek z GW'), ('tap connector', 'Półśrubunek z GW'),
      ('wallplate elbow', 'Kolano ścienne z GW'), ('mounting unit cranked', 'Zestaw montażowy wygięty z GW'), ('mounting unit straight', 'Zestaw montażowy prosty z GW'),
      ('copper tube', 'Rura miedziana'), ('press flange adaptor', 'Kołnierz z końcówką press PN 16'), ('flange with press', 'Kołnierz z końcówką press PN 16')]


def series_of(n):
    for a, b, s in SERIES:
        if a <= n <= b:
            return s


def lines_of(page):
    ws = sorted(page.get_text('words'), key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    out = []
    for w in ws:
        yc = (w[1] + w[3]) / 2
        if out and abs(out[-1][0] - yc) <= 3.2:
            out[-1][1].append(w)
        else:
            out.append([yc, [w]])
    for line in out:
        line[1].sort(key=lambda w: w[0])
    return out


def is_row(ws):
    art = [w for w in ws if 300 <= w[0] < 440]
    num = [w for w in ws if w[0] >= 440]
    return bool(art) and len(num) >= 2 and all(re.match(r'^\d+$', w[4]) for w in num[-2:])


def clean_name(t):
    t = re.sub(r'\s+', ' ', t).strip().replace(' °', '°').replace('° ', '°')
    t = re.sub(r'\b(90|45)\b(?!°)', r'\1°', t)
    return re.sub(r'°(?=[a-zA-Z])', '° ', t).strip(' |')


def join_art(ws):
    s = ''
    for i, w in enumerate(ws):
        t = w[4]
        if i and not (t.startswith('-') or (len(ws[i - 1][4]) == 1 and ws[i - 1][4].isalpha())):
            s += ' '
        s += t
    return re.sub(r'^(K\d{4}[A-Z]?) (\d) (\d/\d)$', r'\1-\2 \3', s)


def size_of(ws):
    sz = re.sub(r'\s+', ' ', ' '.join(w[4] for w in ws))
    sz = re.sub(r'^(\d) (\d)(?= [x×]|$)', r'\1\2', sz).replace('x', ' × ')
    sz = re.sub(r'\s*×\s*', ' × ', sz).strip()
    return sz.replace('1/2½', '1/2').replace('-/', '-').replace('"', '″')


def pl_name(en, de):
    e = en.lower().replace(' gas', '').replace('  ', ' ').strip()
    dl = de.lower()
    seal = ' (uszczelnienie płaskie)' if 'flach' in dl else (' (uszczelnienie stożkowe)' if 'konisch' in dl else '')
    for k, v in PL:
        if e.startswith(k):
            return v + (seal if v.startswith('Śrubunek') else '')
    return 'Syfon P' if 'p trap' in dl else None


def parse(doc):
    groups, cur = [], None
    for n in range(SERIES[0][0], SERIES[-1][1] + 1):
        page, ser = doc[n - 1], series_of(n)
        lines = lines_of(page)
        rects = [(r, img[0]) for img in page.get_images(full=True) for r in page.get_image_rects(img[0])]
        i = 0
        while i < len(lines):
            y, ws = lines[i]
            if 'Artikelbild' in [w[4] for w in ws]:
                hdr, code, j = [], None, i + 1
                while j < len(lines) and lines[j][0] - y < 45 and not is_row(lines[j][1]):
                    hdr.append(lines[j])
                    for w in lines[j][1]:
                        if w[0] < 130 and re.match(r'^\([A-Z0-9]+\)$', w[4]):
                            code = w[4][1:-1]
                    j += 1
                skip = {'picture', 'bag', 'box', 'article', 'number', '(Stück/piece)', 'U', 'Artikelnummer'}
                names = [' '.join(w[4] for w in ww if 140 <= w[0] < 305 and w[4] not in skip) for _, ww in hdr]
                names = [x for x in names if x]
                cur = {'series': ser, 'code': code, 'de': clean_name(names[0]) if names else '',
                       'en': clean_name(' '.join(names[1:])) if len(names) > 1 else '', 'page': n, 'y0': y, 'rows': [], 'xref': None}
                groups.append(cur)
                i = j
                continue
            if cur and is_row(ws):
                num = [w for w in ws if w[0] >= 440]
                size = [w for w in ws if 150 <= w[0] < 300]
                if size:
                    cur['rows'].append([join_art([w for w in ws if 300 <= w[0] < 440]), size_of(size), int(num[-2][4]), int(num[-1][4])])
            i += 1
        on_page = [g for g in groups if g['page'] == n]
        for k, g in enumerate(on_page):
            yend = on_page[k + 1]['y0'] if k + 1 < len(on_page) else 9999
            c = [r for r in rects if r[0].x1 < 160 and g['y0'] - 5 <= r[0].y0 < yend and r[0].width > 25]
            if c:
                g['xref'] = max(c, key=lambda r: r[0].width * r[0].height)[1]
    return groups


def image(doc, xref):
    pix = pymupdf.Pixmap(doc, xref)
    if pix.n - pix.alpha >= 4:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    if pix.alpha:
        pix = pymupdf.Pixmap(pix, 0)
    im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    mask = ImageChops.difference(im, Image.new('RGB', im.size, (255, 255, 255))).convert('L').point(lambda v: 255 if v > 14 else 0)
    bb = mask.getbbox()
    if bb:
        im = im.crop((max(0, bb[0] - 6), max(0, bb[1] - 6), min(im.width, bb[2] + 6), min(im.height, bb[3] + 6)))
    return ImageChops.multiply(im, Image.new('RGB', im.size, STONE))


def main(pdf):
    doc = pymupdf.open(pdf)
    groups = parse(doc)
    os.makedirs(os.path.join(OUT, 'img/besco'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'data'), exist_ok=True)
    out_groups, rows, missing = [], [], set()
    for g in groups:
        name = pl_name(g['en'], g['de'])
        if not name:
            missing.add((g['code'], g['en'], g['de']))
        en = g['en'] or ('P Trap' if 'P Trap' in g['de'] else '')
        en = en.replace('Balve', 'Valve').replace('Staight', 'Straight').replace('P xP', 'P×P').replace('P x P', 'P×P').replace('P x F', 'P×F')
        en = re.sub(r'^Handel ', '', en)
        img = f"x{g['xref']}" if g['xref'] else ''
        if img and not os.path.exists(os.path.join(OUT, f'img/besco/{img}.webp')):
            image(doc, g['xref']).save(os.path.join(OUT, f'img/besco/{img}.webp'), 'WEBP', quality=82, method=6)
        gi = len(out_groups)
        out_groups.append([ORDER.index(g['series']), g['code'], name or en, en, img])
        rows += [[gi] + r for r in g['rows']]
    series = []
    for sid in ORDER:
        rs = [r for r in rows if out_groups[r[0]][0] == ORDER.index(sid)]
        meta = dict(META[sid], id=sid, count=len(rs), groups=len({r[0] for r in rs}))
        if sid == 'cu-ansi-k':
            meta['sizes'] = '1/4″–4 1/8″'
        else:
            vals = [float(m.group(1).replace(',', '.')) for r in rs if (m := re.match(r'^(\d+(?:[.,]\d+)?)', r[2]))]
            f = lambda v: str(int(v)) if v == int(v) else str(v).replace('.', ',')
            meta['sizes'] = f'{f(min(vals))}–{f(max(vals))} mm'
        series.append(meta)
    arts = [r[1] for r in rows]
    assert len(arts) == len(set(arts)), 'zduplikowane numery artykułów'
    data = {'src': 'Besco Fittings & Connectors · katalog 2026', 'series': series, 'groups': out_groups, 'rows': rows}
    with open(os.path.join(OUT, 'data/besco-2026.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    pix = doc[2].get_pixmap(dpi=130)
    page = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    page.resize((860, round(page.height * 860 / page.width)), Image.LANCZOS).save(os.path.join(OUT, 'img/besco/karta-p3.webp'), 'WEBP', quality=74, method=6)
    print(f'{len(rows)} pozycji, {len(out_groups)} grup, {len(series)} linii')
    if missing:
        print('Brak polskiej nazwy dla:', sorted(missing))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
