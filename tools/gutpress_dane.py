"""Dane do katalogów Gutpress (gaz V i M, zawory kulowe) z polskich katalogów Besco/Armatex → tools/katalog-pdf/.

Użycie:
    pip install pymupdf pillow
    python3 tools/gutpress_dane.py Katalog_GUTPRESS_gaz_M_i_V.pdf katalog_zawory_gutpress.pdf

Wynik:
    tools/katalog-pdf/gutpress-gaz.json      28 grup (14 profil V, 14 profil M): tabela zamówień (rozmiar, kod, opk. 1, opk. 2)
                                             i tabela wymiarów (Materiał, D1, D2, L1…, O-ring, Cechowanie) jak w katalogu
    tools/katalog-pdf/gutpress/g-*.png       zdjęcia (z-*) i rysunki techniczne (r-*) grup, zdjęcia REMS (rems-*), instrukcja (inst-*)
    tools/katalog-pdf/gutpress-zawory.json   6 zaworów: opis, dane techniczne, tabela wymiarów (przepisana z obrazów katalogu)

Numery artykułów zostają jak w tych katalogach (polskie wydanie), choć część różni się zapisem od katalogu Besco 2026
i data/besco-2026.json (np. GPG4243-1512 i GPG4243-15.1/2). Nazwy grup bierzemy z data/besco-2026.json (tytuły w katalogu
gazowym mają pomyłki, np. „Łuk jednokielichowy GPG5002” przy numerach GPG5001), materiał i rodzaj gwintu z tytułu.
Zdjęcia produktów są małe (ok. 150 px): po tym skrypcie powiększ je tools/powieksz_zdjecia.py.
"""
import io
import json
import os
import re
import sys

import pymupdf
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'tools', 'katalog-pdf')
IMG = os.path.join(OUT, 'gutpress')
LOGO_GP = (34, 35)            # logo „GP V/M” przy tabelach (nie zdjęcie)
HEAD = {'Code': 'Kod', 'Kod': 'Kod', 'Size': 'Kod', 'Material': 'Materiał', 'Materiał': 'Materiał', 'Materl': 'Materiał',
        'Marking': 'Cechowanie', 'Cechowanie': 'Cechowanie', 'Cechowanie': 'Cechowanie', 'O ring': 'O-ring', 'O RING': 'O-ring',
        'RP': 'Rp'}   # klucze bez łączników (Ma-terial, Cecho-wanie: dzielenie wyrazów w komórkach)
# dwie tabele bez nagłówka w katalogu (7270G, 7243G): kolumny z rysunków (gwint, klucz SW)
NO_HEAD = {'7270G': ['Kod', 'Materiał', 'D1', 'D2', 'L1', 'L2', 'A', 'Rp', 'SW', 'O-ring', 'Cechowanie'],
           '7243G': ['Kod', 'Materiał', 'D1', 'D2', 'L1', 'L2', 'A', 'R', 'SW', 'O-ring', 'Cechowanie']}


def png(doc, xref, path):
    im = Image.open(io.BytesIO(doc.extract_image(xref)['image']))
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGB', im.size, 'white')
        bg.paste(im, mask=im.split()[-1])
        im = bg
    smask = doc.extract_image(xref).get('smask')
    im = im.convert('RGB')
    if smask:   # przezroczystość w osobnej masce: tło na biało
        m = Image.open(io.BytesIO(doc.extract_image(smask)['image'])).convert('L').resize(im.size)
        bg = Image.new('RGB', im.size, 'white')
        bg.paste(im, mask=m)
        im = bg
    im.save(path)


def clip(page, rect, path, dpi=300):
    pix = page.get_pixmap(dpi=dpi, clip=rect)
    Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB').save(path)


def site_names():
    b = json.load(open(os.path.join(ROOT, 'data', 'besco-2026.json'), encoding='utf-8'))
    ids = [s['id'] for s in b['series']]
    by_code, by_row = {}, {}
    for i, g in enumerate(b['groups']):
        if ids[g[0]] in ('cu-press-gas-v', 'cu-press-gas-m'):
            by_code[(ids[g[0]][-1], g[1])] = g[2]
            for r in b['rows']:
                if r[0] == i:
                    by_row[r[1]] = g[2]
    return by_code, by_row


def tech_table(t, kod):
    ex = [[(c or '').replace('\n', '').strip() for c in r] for r in t.extract()]
    if ex[0][0] in ('Kod', 'Code', 'Size'):
        head = [HEAD.get(h.replace('-', '').replace('ORING', 'O RING').replace('Materal', 'Materl').replace('Materia l', 'Materl'), h) if h else h
                for h in ex[0]]
        ex = ex[1:]
        if ex and not ex[0][0]:                       # podwiersz Min / Max
            sub, orig = ex[0], list(head)
            for i, v in enumerate(sub):
                if v:
                    head[i] = f'{orig[i] or orig[i - 1]} {v.rstrip(".").lower()}'
            ex = ex[1:]
        head = [h or '' for h in head]
    else:
        head = NO_HEAD[kod]
    assert len(head) == len(ex[0]), (kod, head, ex[0])
    return dict(head=head, rows=ex)


def gaz(path):
    doc = pymupdf.open(path)
    by_code, by_row = site_names()
    groups = []
    for pn, page in enumerate(doc):
        imgs = [(im[0], im[2], im[3], r) for im in page.get_images(full=True) for r in page.get_image_rects(im[0])]
        heads = sorted([r for x, w, h, r in imgs if w > 1400 and h < 100], key=lambda r: r.y0)
        tabs = page.find_tables().tables
        for hi, hr in enumerate(heads):
            y1 = heads[hi + 1].y0 if hi + 1 < len(heads) else 740
            title = page.get_text('text', clip=pymupdf.Rect(0, hr.y0, 440, hr.y1)).replace('\n', ' ')
            prof = page.get_text('text', clip=pymupdf.Rect(560, hr.y0, page.rect.width, hr.y1))
            if not title.strip() or re.search(r'REMS|Cęgi|Zaciskarki', title):
                continue
            title = re.sub(r'\s+', ' ', re.sub(r'GUTPRE\w*', ' ', title)).strip()
            p = 'V' if 'V' in prof else 'M'
            blk = [t for t in tabs if hr.y1 < t.bbox[1] < y1]
            order = [[r[0].strip(), r[1].replace(' ', ''), int(r[2]), int(r[3])] for t in blk for r in t.extract()[1:] if t.extract()[0][0] == 'Rozmiar']
            # kod grupy: z tytułu, chyba że nie zgadza się z numerami w tabeli (pomyłki w tytułach)
            tcode = re.search(r'(GPG\d+\w*|\d{4}\w*)$', title).group(1)
            name = re.sub(r'\s*(GPG\d+\w*|\d{4}\w*)$', '', title)
            if p == 'V':
                pre = order[0][1].split('-')[0]
                kod = tcode if tcode.startswith(pre) else pre + ('R' if order[0][1].count('.') == 2 and pre.endswith('5130') else '')
            else:
                kod = tcode
            site = (next((by_row[r[1]] for r in order if r[1] in by_row), None) or by_code.get((p.lower(), kod))
                    or by_code.get((p.lower(), kod.rstrip('G'))))
            tech = [tech_table(t, kod) for t in blk if t.extract()[0][0] != 'Rozmiar']
            assert len(tech) == 1, (kod, len(tech))
            mat = 'brąz' if 'brąz' in name else 'miedź'
            th = tech[0]['head']
            gw = ' · gwint Rp (wewnętrzny)' if 'Rp' in th else (' · gwint R (zewnętrzny)' if 'R' in th else '')
            pics = sorted([(x, r) for x, w, h, r in imgs if x not in LOGO_GP and not (w > 1400 and h < 100) and r.y0 > hr.y1 and r.y1 < y1],
                          key=lambda z: z[1].width * z[1].height)
            n = len(groups) + 1
            files = []
            for k, (x, r) in enumerate(pics):
                f = f'{"z" if k == 0 else "r"}-{n:02d}-{k}.png'
                if k and doc.extract_image(x)['width'] < 600 and r.width > 240:   # złożony rysunek: renderujemy obszar strony
                    clip(page, r, os.path.join(IMG, f))
                else:
                    png(doc, x, os.path.join(IMG, f))
                files.append(f'gutpress/{f}')
            drawings = sorted(files[1:], key=lambda f: [r.x0 for x, r in pics][files.index(f)])
            groups.append(dict(id=f'{p}-{kod}', kod=kod, profil=p, nazwa=site or name, opis=f'{mat}{gw}', zrodlo=name,
                               zdjecie=files[0], rysunki=drawings, wiersze=order, wymiary=tech[0]))
    # strony REMS (V: s. 10) i instrukcja (s. 20–21)
    def save_page_imgs(pn, prefix, minw=120):
        out = []
        for x in sorted({im[0] for im in doc[pn].get_images(full=True)}):
            r = doc[pn].get_image_rects(x)[0]
            if doc.extract_image(x)['width'] < minw or r.width > 500 or r.y0 > 780 or (prefix == 'rems' and r.y0 < 40):
                continue
            f = f'{prefix}-{len(out) + 1}.png'
            png(doc, x, os.path.join(IMG, f))
            out.append(dict(f=f'gutpress/{f}', y=round(r.y0), x=round(r.x0), w=round(r.width)))
        return sorted(out, key=lambda o: (o['y'], o['x']))
    extra = dict(rems=save_page_imgs(9, 'rems'), inst=save_page_imgs(19, 'inst-a') + save_page_imgs(20, 'inst-b'))
    return groups, extra


ZAWORY = [  # przepisane z obrazów tabel w katalogu zaworów Gutpress 2025 (d1 28 mm w GPV600PP: 28.2 zamiast „2.2”)
    dict(kod='GPV600PP', nazwa='Zawór kulowy press × press, profil V', profil='V', zakres='15–54 mm',
         pn='PN40 (15–28 mm) · PN25 (35 mm) · PN16 (42–54 mm)', page=1,
         head=['Kod', 'Rozmiar', 'd', 'd1', 'd2', 'L1', 'L', 'H', 'L3'],
         rows=[['GPV60015PP', '15', '14.5', '15.3', '23.15', '31.5', '93', '48.5', '91'],
               ['GPV60018PP', '18', '15', '18.3', '26.15', '31.5', '94', '48.5', '91'],
               ['GPV60022PP', '22', '20', '22.2', '31.3', '32', '104', '52', '91'],
               ['GPV60028PP', '28', '25', '28.2', '37.1', '33', '110', '58', '100'],
               ['GPV60035PP', '35', '32', '35.3', '44.5', '33.5', '123', '72.5', '130'],
               ['GPV60042PP', '42', '40', '42.3', '53.5', '49', '158', '78', '130'],
               ['GPV60054PP', '54', '50', '54.3', '65.5', '53.5', '179', '93.5', '156.5']]),
    dict(kod='GPV600PF', nazwa='Zawór kulowy press × GW, profil V', profil='V', zakres='15–54 mm',
         pn='PN40 (15–28 mm) · PN25 (35 mm) · PN16 (42–54 mm)', page=2,
         head=['Kod', 'Rozmiar', 'd', 'd1', 'd2', 'L1', 'L', 'H', 'L3'],
         rows=[['GPV60015012PF', '15 × 1/2″', '14.5', '15.3', '23.15', '31.5', '72', '48.5', '91'],
               ['GPV60018012PF', '18 × 1/2″', '15', '18.3', '26.15', '31.5', '72.5', '48.5', '91'],
               ['GPV60022034PF', '22 × 3/4″', '20', '22.2', '31.3', '32', '80.5', '52', '91'],
               ['GPV60028100PF', '28 × 1″', '25', '28.2', '37.1', '33', '88.5', '58', '100'],
               ['GPV60035114PF', '35 × 1 1/4″', '32', '35.3', '44.5', '33.5', '100', '72.5', '130'],
               ['GPV60042112PF', '42 × 1 1/2″', '40', '42.3', '53.5', '49', '123', '78', '130'],
               ['GPV60054200PF', '54 × 2″', '50', '54.3', '65.5', '53.5', '142', '93.5', '156.5']]),
    dict(kod='GPV600PU', nazwa='Zawór kulowy press × śrubunek, profil V', profil='V', zakres='18–35 mm',
         pn='PN40 (15–28 mm) · PN25 (35 mm)', page=3,
         head=['Kod', 'Rozmiar', 'd1', 'd2', 'd3', 'L1', 'L', 'H', 'L3', 'G'],
         rows=[['GPV60018012PU', '18', '18.3', '26.15', '15', '31.5', '77.5', '48.5', '91', '1/2″'],
               ['GPV60022034PU', '22', '22.2', '31.3', '20', '32', '86.5', '52', '91', '3/4″'],
               ['GPV60028100PU', '28', '28.2', '37.1', '25', '33', '93.5', '58', '100', '1″'],
               ['GPV60035114PU', '35', '35.3', '44.5', '32', '33.5', '120', '72.5', '130', '1 1/4″']]),
    dict(kod='GP600PP', nazwa='Zawór kulowy press × press, profil M', profil='M', zakres='15–54 mm', pn='PN25 (15–54 mm)', page=4,
         head=['Kod', 'Rozmiar', 'd', 'd1', 'd2', 'L1', 'L', 'H', 'L3'],
         rows=[['GP60015PP', '15', '14.5', '15.3', '23.15', '22', '74', '51', '91'],
               ['GP60022PP', '22', '20', '22.3', '31.3', '21', '82', '54.5', '91'],
               ['GP60028PP', '28', '25', '28.3', '37.1', '27', '104.5', '62.5', '100'],
               ['GP60035PP', '35', '32', '35.3', '43.9', '26', '110', '72.5', '130'],
               ['GP60042PP', '42', '40', '42.3', '53', '34', '134.5', '79', '130'],
               ['GP60054PP', '54', '50', '54.3', '65', '35', '149.5', '94.5', '156.5']]),
    dict(kod='GP600PF', nazwa='Zawór kulowy press × GW, profil M', profil='M', zakres='15–54 mm', pn='PN25 (15–54 mm)', page=5,
         head=['Kod', 'Rozmiar', 'd', 'd1', 'd2', 'L1', 'L', 'H', 'L3'],
         rows=[['GP60015012PF', '15 × 1/2″', '14.5', '15.3', '23.15', '22', '61.5', '51', '91'],
               ['GP60022034PF', '22 × 3/4″', '20', '22.2', '31.3', '21', '67', '54.5', '91'],
               ['GP60028100PF', '28 × 1″', '25', '28.3', '37.1', '27', '83', '62.5', '100'],
               ['GP60035114PF', '35 × 1 1/4″', '32', '35.3', '43.9', '26', '91.5', '72.5', '130'],
               ['GP60042112PF', '42 × 1 1/2″', '40', '42.3', '53', '34', '109.5', '79', '130'],
               ['GP60054200PF', '54 × 2″', '50', '54.3', '65', '35', '122', '94.5', '156.5']]),
    dict(kod='GPH600PP', nazwa='Zawór kulowy press × press, trzpień przedłużony, profil M', profil='M', zakres='15–54 mm',
         pn='PN25 (15–54 mm)', page=6,
         head=['Kod', 'Rozmiar', 'd', 'd1', 'd2', 'L1', 'L', 'H1', 'H', 'L3'],
         rows=[['GPH60015PP', '15', '14.5', '15.3', '23.2', '22', '74', '70', '108', '91'],
               ['GPH60018PP', '18', '15', '18.3', '26.2', '21', '77', '70', '108', '91'],
               ['GPH60022PP', '22', '20', '22.3', '31.2', '21', '82', '70', '112', '91'],
               ['GPH60028PP', '28', '25', '28.3', '37.1', '27', '105', '70', '118', '100'],
               ['GPH60035PP', '35', '32', '35.3', '44.5', '26', '110', '70', '127.5', '130'],
               ['GPH60042PP', '42', '40', '42.3', '53.5', '34', '135', '70', '134', '130'],
               ['GPH60054PP', '54', '50', '54.3', '65', '35', '150', '70', '149.5', '156.5']]),
]


def zawory(path):
    doc = pymupdf.open(path)
    out = []
    for z in ZAWORY:
        page = doc[z['page']]
        imgs = sorted([(im[0], doc.extract_image(im[0])['width'], page.get_image_rects(im[0])[0]) for im in page.get_images(full=True)],
                      key=lambda t: -t[2].width * t[2].height)
        imgs = [t for t in imgs if t[1] > 400 and t[2].y1 < 640 and t[0] != 35]   # bez logo Besco (35) i znaków, bez tabeli
        foto = min(imgs, key=lambda t: t[2].y0)                         # zdjęcie u góry, rysunek niżej
        rys = max(imgs, key=lambda t: t[2].y0)
        k = z['kod'].lower()
        png(doc, foto[0], os.path.join(IMG, f'zaw-{k}.png'))
        png(doc, rys[0], os.path.join(IMG, f'zaw-{k}-r.png'))
        out.append(dict({k2: v for k2, v in z.items() if k2 != 'page'}, zdjecie=f'gutpress/zaw-{k}.png',
                        rysunek=f'gutpress/zaw-{k}-r.png'))
    for x, name in ((20, 'zaw-v'), (21, 'zaw-m'), (54, 'znak-wras'), (62, 'znak-dvgw'), (64, 'znak-pzh'), (53, 'znak-5lat')):   # okładka, znaki
        png(doc, x, os.path.join(IMG, f'{name}.png'))
    return out


def main():
    os.makedirs(IMG, exist_ok=True)
    groups, extra = gaz(sys.argv[1])
    json.dump(dict(grupy=groups, **extra), open(os.path.join(OUT, 'gutpress-gaz.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'gaz: {len(groups)} grup, {sum(len(g["wiersze"]) for g in groups)} indeksów, REMS {len(extra["rems"])}, instrukcja {len(extra["inst"])}')
    z = zawory(sys.argv[2])
    json.dump(z, open(os.path.join(OUT, 'gutpress-zawory.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'zawory: {len(z)} typów, {sum(len(x["rows"]) for x in z)} indeksów')


if __name__ == '__main__':
    main()
