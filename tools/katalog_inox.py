"""Dołącza złączki zaciskane Besco ze stali nierdzewnej (INOX 304 i INOX 316L) do danych strony.

Użycie (po tools/katalog_besco.py, bo dopisuje do jego wyniku):
    pip install pymupdf pillow rapidocr_onnxruntime
    python3 tools/katalog_inox.py Katalog_INOX_304.pdf Katalog_INOX_316L.pdf

Wynik:
    data/besco-2026.json   dopisane linie inox-304-press-m i inox-316l-press-m (poprzednie wpisy INOX są zastępowane)
    img/besco/i304-x<xref>.webp, img/besco/i316-x<xref>.webp   zdjęcia grup

Katalog 304 ma warstwę tekstową. Katalog 316L ma tekst zamieniony na krzywe, więc czytamy go
przez OCR (rapidocr) i sprawdzamy, czy numer artykułu zaczyna się od kodu grupy.
"""
import json
import os
import re
import sys

import pymupdf

sys.path.insert(0, os.path.dirname(__file__))
import katalog_besco as kb  # noqa: E402

OUT = kb.OUT
META = {
    'inox-304-press-m': dict(name='Stal nierdzewna 304 press, profil M', short='INOX 304 press', bar='16 bar', temp='−10…110 °C',
                             media='ogrzewanie', std='', appr=['CE']),
    'inox-316l-press-m': dict(name='Stal nierdzewna 316L press, profil M', short='INOX 316L press', bar='16 bar', temp='−10…110 °C',
                              media='woda, ogrzewanie, przemysł', std='', appr=['DVGW', 'WRAS']),
}
PL_EXTRA = [('bend 90° a/a', 'Łuk 90° zz'), ('by-pass bend', 'Mijanka zz'), ('crossover bend', 'Mijanka zz'),
            ('press flange', 'Kołnierz z końcówką press PN 16'), ('threaded tee', 'Trójnik z GW'),
            ('straight adaptor female', 'Złączka z GW'), ('straight adaptor male', 'Złączka z GZ')]


def en_clean(t):
    t = re.sub(r'([a-z])([A-Z])', r'\1 \2', t)          # „StraightAdaptorFemale” z OCR
    t = re.sub(r'(\d)([A-Za-z])', r'\1 \2', t)
    t = re.sub(r'([A-Za-z])(\d)', r'\1 \2', t)
    t = t.replace(' ala', ' a/a').replace('O x 0', '').strip()
    return kb.clean_name(t)


def pl_name(en, sizes):
    e = en.lower()
    if e.startswith('straight union') and any('MI' in s for s in sizes):
        return 'Śrubunek z GZ'
    for k, v in PL_EXTRA:
        if e.startswith(k):
            return v
    return kb.pl_name(en, '')


def size_clean(s):
    s = s.replace('Ø', '').replace('"', '').replace("'", '').replace('″', '')
    s = re.sub(r'(?<![\d/])0(?=\d)', '', s)               # Ø odczytane przez OCR jako 0
    s = re.sub(r'\s*[x×X]\s*', ' × ', s).replace(',', '.')
    s = re.sub(r'(\d)(MI|FI)$', r'\1 \2', s)
    s = re.sub(r'(?<=\d)\s*(1/[24]|3/4)', lambda m: ' ' + m.group(1), s)  # „11/4” → „1 1/4”
    s = re.sub(r'\b(\d) (1/[24]|3/4)\b', r'\1 \2', s)
    return re.sub(r'\s+', ' ', s).strip()


def parse_304(doc):
    groups, cur = [], None
    for n, p in enumerate(doc):
        lines = kb.lines_of(p)
        rects = [(r, x[0]) for x in p.get_images(full=True) for r in p.get_image_rects(x[0])]
        i = 0
        while i < len(lines):
            y, ws = lines[i]
            if 'Artikelbild' in [w[4] for w in ws]:
                hdr = [l for l in lines[i + 1:i + 6] if l[0] - y < 40]
                en_line = next((l for l in hdr if any(w[4] == 'new' for w in l[1])), hdr[1])
                en = ' '.join(w[4] for w in en_line[1] if 105 <= w[0] < 270)
                cur = {'en': en, 'rows': [], 'page': n, 'y0': y, 'xref': None}
                groups.append(cur)
                i += 1
                continue
            art = [w for w in ws if 270 <= w[0] < 380]
            nums = [w for w in ws if w[0] >= 380]
            if cur and art and len(nums) >= 2 and re.match(r'^\d{4}', art[0][4]):
                size = ' '.join(w[4] for w in ws if 100 <= w[0] < 270)
                cur['rows'].append([' '.join(w[4] for w in art), size, int(nums[-2][4]), int(nums[-1][4])])
            i += 1
        on = [g for g in groups if g['page'] == n]
        for k, g in enumerate(on):
            yend = on[k + 1]['y0'] if k + 1 < len(on) else 9999
            c = [r for r in rects if r[0].x1 < 115 and g['y0'] - 5 <= r[0].y0 < yend and r[0].width > 25]
            if c:
                g['xref'] = max(c, key=lambda r: r[0].width * r[0].height)[1]
    for g in groups:
        codes = {r[0].split('-')[0] for r in g['rows']}
        assert len(codes) == 1, codes
        g['code'] = codes.pop()
    return groups


def parse_316(doc):
    from rapidocr_onnxruntime import RapidOCR
    ocr, groups, cur, z = RapidOCR(), [], None, 3.0
    for n, p in enumerate(doc):
        res, _ = ocr(p.get_pixmap(matrix=pymupdf.Matrix(z, z)).tobytes('png'))
        words = sorted(([min(b[0] for b in box) / z, min(b[1] for b in box) / z, max(b[0] for b in box) / z, max(b[1] for b in box) / z, t]
                        for box, t, _sc in res or []), key=lambda w: ((w[1] + w[3]) / 2, w[0]))
        lines = []
        for w in words:
            yc = (w[1] + w[3]) / 2
            if lines and abs(lines[-1][0] - yc) <= 4:
                lines[-1][1].append(w)
            else:
                lines.append([yc, [w]])
        for line in lines:
            line[1].sort()
        rects = [(r, x[0]) for x in p.get_images(full=True) for r in p.get_image_rects(x[0])]
        i = 0
        while i < len(lines):
            y, ws = lines[i]
            if 'Artikelbild' in ' '.join(w[4] for w in ws):
                en = ' '.join(w[4] for w in lines[i + 2][1] if 120 <= w[0] < 300)
                cur = {'en': en, 'rows': [], 'page': n, 'y0': y, 'xref': None}
                groups.append(cur)
                i += 3
                continue
            art = [w for w in ws if 300 <= w[0] < 420]
            bag = [w for w in ws if 420 <= w[0] < 490]
            box = [w for w in ws if w[0] >= 490]
            size = [w for w in ws if 140 <= w[0] < 300]
            if cur and art and bag and box and size and re.match(r'^\d{6,}$', art[0][4].replace(' ', '')):
                cur['rows'].append([art[0][4].replace(' ', ''), ' '.join(w[4] for w in size), int(bag[0][4]), int(box[0][4])])
            i += 1
        on = [g for g in groups if g['page'] == n]
        for k, g in enumerate(on):
            yend = on[k + 1]['y0'] if k + 1 < len(on) else 9999
            c = [r for r in rects if r[0].x1 < 160 and g['y0'] - 5 <= r[0].y0 < yend and r[0].width > 25]
            if c:
                g['xref'] = max(c, key=lambda r: r[0].width * r[0].height)[1]
    for g in groups:
        g['code'] = g['rows'][0][0][:5]
        assert all(r[0].startswith(g['code']) for r in g['rows']), g['code']
        if not g['en']:   # nagłówek zawinięty w PDF: nazwy jak w katalogu 304
            g['en'] = {'12080': 'Straight Union', '12400': 'Press Flange PN16'}[g['code']]
    return groups


def main(pdf304, pdf316):
    path = os.path.join(OUT, 'data/besco-2026.json')
    data = json.load(open(path, encoding='utf-8'))
    old = [i for i, s in enumerate(data['series']) if s['id'] in META]
    if old:   # ponowne uruchomienie: usuń poprzednie wpisy INOX
        keep = [i for i, g in enumerate(data['groups']) if g[0] not in old]
        remap = {o: n for n, o in enumerate(keep)}
        data['rows'] = [[remap[r[0]]] + r[1:] for r in data['rows'] if r[0] in remap]
        data['groups'] = [data['groups'][i] for i in keep]
        data['series'] = [s for i, s in enumerate(data['series']) if i not in old]
    for sid, pdf, parse, pre in (('inox-304-press-m', pdf304, parse_304, 'i304'), ('inox-316l-press-m', pdf316, parse_316, 'i316')):
        doc = pymupdf.open(pdf)
        si = len(data['series'])
        rows_all = []
        for g in parse(doc):
            en = en_clean(g['en'])
            sizes = [size_clean(r[1]) for r in g['rows']]
            name = pl_name(en, sizes)
            assert name, (sid, g['code'], en)
            img = f"{pre}-x{g['xref']}" if g['xref'] else ''
            if img:
                kb.image(doc, g['xref']).save(os.path.join(OUT, f'img/besco/{img}.webp'), 'WEBP', quality=82, method=6)
            gi = len(data['groups'])
            data['groups'].append([si, g['code'], name, en, img])
            for r, s in zip(g['rows'], sizes):
                rows_all.append([gi, r[0], s, r[2], r[3]])
        vals = [float(m.group(1)) for r in rows_all if (m := re.match(r'^(\d+(?:\.\d+)?)', r[2]))]
        f = lambda v: str(int(v)) if v == int(v) else str(v).replace('.', ',')
        data['series'].append(dict(META[sid], id=sid, count=len(rows_all), groups=len({r[0] for r in rows_all}), sizes=f'{f(min(vals))}–{f(max(vals))} mm'))
        data['rows'] += rows_all
        print(f'{sid}: {len(rows_all)} pozycji, {len({r[0] for r in rows_all})} grup')
    arts = [r[1] for r in data['rows']]
    dup = sorted({a for a in arts if arts.count(a) > 1})
    assert not dup, ('zduplikowane numery artykułów', dup[:20])
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
