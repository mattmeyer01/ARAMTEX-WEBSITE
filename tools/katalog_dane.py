"""Dane do katalogów PDF Besco 2026, Tectite i Kuterlite → tools/katalog-pdf/<katalog>.json.

Użycie (przed tools/katalog_pdf.py):
    pip install pymupdf
    python3 tools/katalog_dane.py sciezka/katalog-kuterlite-oryginal.pdf

Źródła:
    data/besco-2026.json    linie Besco 2026 (bez INOX, które mają własne katalogi i dane w tools/katalog-pdf/inox-*.json).
                            Sprawdzone z katalogiem Besco 2026: poprawki w POPRAWKI_BESCO.
    data/pegler.json        Tectite (wszystkie serie) i Kuterlite (bez K600 i K700, których Armatex nie sprzedaje:
                            SER_OFF w tools/strony.py). Część wymiarów Kuterlite w danych jest ucięta („x 15mm”),
                            więc taki wymiar bierzemy z oryginalnego katalogu producenta (EN, bez cen) po numerze artykułu.

Wymiary zapisujemy gotowe do druku: „×” zamiast „x”, przecinek dziesiętny, cale ze znakiem ″ (katalog_pdf.py
zamienia ułamki na ½, ¼, ¾).
"""
import json
import os
import re
import sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'tools', 'katalog-pdf')

BESCO_SER = ['cu-press-water-v', 'cu-press-water-m', 'cu-press-gas-v', 'cu-press-gas-m', 'steel-press-m',
             'press-ball-valve', 'cu-solder-en1254', 'cu-ansi-k', 'cu-g-size']
# katalog Besco 2026 a data/besco-2026.json: w trzech wierszach ilość zastąpił numer strony katalogu,
# w trzech numer artykułu ma wtrącone spacje
POPRAWKI_BESCO = {
    'GP4280-28.1': dict(qty=(10, 60)),
    '6811010876108': dict(qty=(1, 1)),
    '4243-54.2': dict(qty=(2, 10)),
    '4243-28.1 1 / 4': dict(art='4243-28.1 1/4'),
    '2359G-15.3 / 4': dict(art='2359G-15.3/4'),
    '2331G-1 5 .1/2': dict(art='2331G-15.1/2'),
}
PEGLER_SER = {'tectite': ['tectite-classic', 'tectite-pro', 'tectite-316', 'tectite-zawory', 'tectite-akcesoria'],
              'kuterlite': ['kuterlite-k900', 'kuterlite-zawory', 'kuterlite-akcesoria']}
THREAD = re.compile(r'GW|GZ|gwint|rubunek|montażowy|× GW')


def inch(t):
    t = t.replace('"', '″').replace('”', '″').strip()
    return t if t.endswith('″') else t + '″'


def besco_size(s, thread, ansi, art):
    s = re.sub(r'\s*(MI|FI)$', '', s.strip())
    meters = s.endswith('Meters')
    s = s.replace(' Meters', '')
    extra = ''
    m = re.match(r'^(.*?)\s*(\(.*\))$', s)
    if m:
        s, extra = m.group(1), ' ' + m.group(2)
    parts = [p.strip() for p in s.split('×')]
    out = []
    for i, p in enumerate(parts):
        if ansi:
            p = inch(p.replace('-', ' '))
        elif i >= 1 and ('/' in p or (thread and p in ('1', '2', '3', '4'))):
            p = inch(p)
        out.append(p.replace('.', ','))
    s = ' × '.join(out)
    if meters:  # rura: średnica × ścianka, długość odcinka
        s = ' × '.join(out[:2]) + f' · {out[2]} m'
    dn = re.search(r'-DN(\d+)$', art)
    if dn:
        s += f' · DN {dn.group(1)}'
    return s + extra.replace('.', ',')


def pegler_size(s):
    s = re.sub(r'(\d)\s*mm\b', r'\1', s.strip().replace('”', '"'))
    if s in ('–', '-', ''):
        return '–'
    if re.match(r'^\d+-\d+$', s):
        return s.replace('-', '–')
    parts = [p.strip() for p in re.split(r'\s*x\s*', s)]
    out = []
    for p in parts:
        if '(' in p:                                            # „22 (1/2")”: cal w nawiasie
            p = p.replace('"', '″')
        elif '"' in p or '/' in p:
            p = inch(re.sub(r'(\d)\.(\d/\d)', r'\1 \2', p))   # 1.1/4" → 1 1/4″
        else:
            p = p.replace('mm', '').strip()
        out.append(p)
    return ' × '.join(out)


def besco():
    d = json.load(open(os.path.join(ROOT, 'data', 'besco-2026.json'), encoding='utf-8'))
    groups, seen = [], {}
    for gi, g in enumerate(d['groups']):
        ser = d['series'][g[0]]['id']
        if ser not in BESCO_SER:
            continue
        rows = []
        for r in d['rows']:
            if r[0] != gi:
                continue
            fix = POPRAWKI_BESCO.get(r[1], {})
            rows.append([r[2], fix.get('art', r[1]), *fix.get('qty', (r[3], r[4]))])
        # gwint: nazwa (GW, GZ, śrubunek…) albo ułamek cala w drugim wymiarze
        thread = bool(THREAD.search(g[2])) or any(re.search(r'×\s*[\d ]*/', r[0]) for r in rows)
        rows = [[besco_size(s, thread, ser == 'cu-ansi-k', a), a, b, c] for s, a, b, c in rows]
        img = f'img/besco/{g[4]}-l.webp'
        if not os.path.exists(os.path.join(ROOT, img)):
            img = f'img/besco/{g[4]}.webp'
        n = seen[g[1]] = seen.get(g[1], 0) + 1
        groups.append(dict(id=g[1] if n == 1 else f'{g[1]}-{n}', kod=g[1], nazwa=g[2], seria=ser, zdjecie=img,
                           gwint=thread or ser == 'cu-ansi-k', wiersze=rows))
    groups.sort(key=lambda g: BESCO_SER.index(g['seria']))   # stabilnie: kolejność z katalogu w obrębie serii
    return groups


def kuterlite_pdf_rows(path):
    """Numer artykułu → (wymiar, opak. 1, opak. 2) z katalogu Kuterlite. W wierszu tabeli przed numerem stoją wymiar
    i dwie ilości; w jednej linii tekstu bywają dwie tabele obok siebie, a długi wymiar (trójniki) zaczyna się linię
    wyżej. Wymiar to słowa w kolumnie wymiaru: do 110 pt na lewo od pierwszej ilości."""
    doc, rows = pymupdf.open(path), {}
    code = re.compile(r'\d{5}K?|\d{6}')
    for page in doc:
        lines = {}
        for w in page.get_text('words'):
            lines.setdefault(round((w[1] + w[3]) / 2 / 3), []).append(w)
        keys = sorted(lines)
        for li, k in enumerate(keys):
            line = sorted(lines[k], key=lambda w: w[0])
            for i, w in enumerate(line):
                if not code.fullmatch(w[4]) or i < 3 or not (line[i - 1][4].isdigit() and line[i - 2][4].isdigit()):
                    continue
                q1 = line[i - 2]
                col = (q1[0] - 110, q1[0] - 2)
                size = [x for x in line[:i - 2] if col[0] <= x[0] <= col[1]]
                for kk in reversed(keys[max(0, li - 3):li]):   # początek wymiaru: do 15 pt wyżej, w kolumnie wymiaru
                    if k - kk > 5:
                        break
                    up = [x for x in sorted(lines[kk], key=lambda x: x[0]) if col[0] <= x[0] <= col[1]]
                    busy = [x for x in lines[kk] if q1[0] - 2 <= x[0] <= w[2] + 2]   # ilości/numer = inny wiersz
                    if busy or any(x[4] in ('dimension', 'qty') for x in up):
                        break
                    if up:
                        size = up + size
                        break
                rows.setdefault(w[4], (' '.join(x[4] for x in size), int(line[i - 2][4]), int(line[i - 1][4])))
    return rows


def pegler(name, kuter_pdf=None):
    d = json.load(open(os.path.join(ROOT, 'data', 'pegler.json'), encoding='utf-8'))
    pdf = kuterlite_pdf_rows(kuter_pdf) if kuter_pdf else {}
    groups, missing = [], []
    for ser in PEGLER_SER[name]:
        for g in d['groups']:
            if g['series'] != ser:
                continue
            rows = []
            for r in g['rows']:
                size = r[0]
                if name == 'kuterlite' and size.startswith(('x ', '(')):   # wymiar ucięty w danych strony
                    if r[1] in pdf:
                        size = pdf[r[1]][0]
                    else:
                        missing.append(r[1])
                rows.append([pegler_size(size), r[1]] + (r[2:4] if len(r) >= 4 else [None, None]))
            img = f'img/pegler/{g["img"]}-l.webp'
            if not os.path.exists(os.path.join(ROOT, img)):
                img = f'img/pegler/{g["img"]}.webp'
            groups.append(dict(id=g['slug'], kod=g['code'], nazwa=g['name'], seria=ser, zdjecie=img,
                               gwint=any('″' in r[0] for r in rows), wiersze=rows))
    if missing:
        sys.exit(f'{name}: brak wymiaru w katalogu producenta dla {missing}')
    ids = [g['id'] for g in groups]
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, dup
    return groups


def main():
    kuter = sys.argv[1] if len(sys.argv) > 1 else None
    for name, groups in (('besco-2026', besco()), ('tectite', pegler('tectite')),
                         ('kuterlite', pegler('kuterlite', kuter) if kuter else None)):
        if groups is None:
            print('kuterlite: pominięty (podaj oryginalny katalog Kuterlite)')
            continue
        json.dump(groups, open(os.path.join(OUT, f'{name}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'{name}: {len(groups)} grup, {sum(len(g["wiersze"]) for g in groups)} indeksów')


if __name__ == '__main__':
    main()
