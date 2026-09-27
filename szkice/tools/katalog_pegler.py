"""Katalog Tectite 2026 i cennik Kuterlite (X 2024) -> szkice/data/pegler.json + zdjęcia szkice/img/pegler/.

Użycie:
    pip install pymupdf pillow
    python3 szkice/tools/katalog_pegler.py katalog_tectite_2026.pdf Kuterlite-price-list-Oct-2024.pdf

Zapisuje grupy produktów (kod, nazwa, rozmiary, kody artykułów, opakowania Kuterlite) i po jednym
zdjęciu na grupę. Cen z cennika Kuterlite celowo nie zapisuje. Nazwy Kuterlite są tłumaczone
na polską nomenklaturę (angielska nazwa zostaje w polu "en").
"""
import io, json, os, re, sys, unicodedata
import pymupdf as fitz
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = str.maketrans({'∏': 'ł', 'à': 'ą', '˝': 'ż', 'ƒ': 'ń', 'Ê': 'ś', '´': 'ę', 'ç': 'ć', '˚': 'Ż', 'Â': 'ź', 'ê': 'ź', '¸': 'Ł', 'Ñ': 'Ą'})

SERIES = {
    'tectite-classic': dict(brand='Tectite', name='Tectite Classic', short='Classic', sys='zlaczki-na-wcisk-tectite',
        media='woda, CO · rury miedziane, PEX, PB', facts=[('Ciśnienie', '16 bar (miedź), 12 bar (PEX, PB)'), ('Temperatura', '−24…95 °C z miedzią')],
        appr=['WRAS', 'PZH'], note='Mosiądz DZR, system demontowalny. Rury PEX i PB łączy się z tulejką.'),
    'tectite-pro': dict(brand='Tectite', name='Tectite Pro', short='Pro', sys='zlaczki-na-wcisk-tectite',
        media='rury miedziane, PEX, PB i stal węglowa ocynkowana', facts=[('System', 'push-fit, demontowalny')], appr=[], note='Rury PEX i PB łączy się z tulejką.'),
    'tectite-316': dict(brand='Tectite', name='Tectite 316', short='316', sys='zlaczki-na-wcisk-tectite',
        media='rury ze stali nierdzewnej kwasoodpornej', facts=[('System', 'push-fit')], appr=[], note=''),
    'tectite-zawory': dict(brand='Pegler', name='Zawory na wcisk Pegler', short='zawory', sys='zlaczki-na-wcisk-tectite',
        media='instalacje wody i ogrzewania', facts=[('Końcówki', 'na wcisk Tectite')], appr=[], note=''),
    'tectite-akcesoria': dict(brand='Tectite', name='Akcesoria i narzędzia Tec-Tools', short='akcesoria', sys='zlaczki-na-wcisk-tectite',
        media='przygotowanie rur i montaż systemu Tectite', facts=[], appr=[], note=''),
    'kuterlite-k600': dict(brand='Kuterlite', name='Kuterlite K600', short='K600', sys='zlaczki-skrecane-kuterlite',
        media='rury miedziane', facts=[('Połączenie', 'zaciskowe z pierścieniem')], appr=[], note='Wymiary trójników według oznaczeń brytyjskich (UK), jak w cenniku producenta.'),
    'kuterlite-k900': dict(brand='Kuterlite', name='Kuterlite K900 Pro', short='K900 Pro', sys='zlaczki-skrecane-kuterlite',
        media='rury miedziane', facts=[('Połączenie', 'zaciskowe z pierścieniem')], appr=[], note='Na armatex.pl seria występuje jako KN 900. Wymiary trójników według oznaczeń UK.'),
    'kuterlite-k700': dict(brand='Kuterlite', name='Kuterlite K700', short='K700 PE', sys='zlaczki-skrecane-kuterlite',
        media='rury PE, także przejścia PE × miedź', facts=[('Połączenie', 'zaciskowe do rur PE')], appr=[], note=''),
    'kuterlite-zawory': dict(brand='Kuterlite', name='Zawory Kuterlite', short='zawory', sys='zlaczki-skrecane-kuterlite',
        media='woda, podłączenia urządzeń', facts=[('Końcówki', 'zaciskowe Kuterlite')], appr=[], note=''),
    'kuterlite-akcesoria': dict(brand='Kuterlite', name='Akcesoria Kuterlite', short='akcesoria', sys='zlaczki-skrecane-kuterlite',
        media='nakrętki, pierścienie i tulejki do złączek Kuterlite', facts=[], appr=[], note=''),
}

def tectite_series(page, code):
    if code in ('PT550', 'TX300', 'PT913', 'TX480', 'TX405'): return 'tectite-zawory'
    if page >= 25: return 'tectite-akcesoria'
    if page <= 16: return 'tectite-classic'
    if page <= 20: return 'tectite-pro'
    return 'tectite-316'

def kuter_series(page):
    if page <= 12: return 'kuterlite-k600'
    if page <= 21: return 'kuterlite-k900'
    if page <= 25: return 'kuterlite-k700'
    if page <= 29: return 'kuterlite-zawory'
    return 'kuterlite-akcesoria'

# --- tłumaczenie nazw Kuterlite (najdłuższe dopasowanie początku nazwy)
PL = [
    ('coupling burst repair coupling', 'Złączka naprawcza'), ('air release coupling', 'Złączka z odpowietrznikiem'),
    ('adaptor coupling imperial x metric', 'Złączka przejściowa calowa × metryczna'),
    ('straight coupling, polyethylene x polyethylene', 'Złączka prosta PE × PE'), ('straight coupling, polyethylene x copper', 'Złączka prosta PE × miedź'),
    ('straight coupling', 'Złączka prosta'), ('heater tee', 'Trójnik do grzałki'),
    ('long male coupling', 'Złączka długa z GZ'), ('male coupling', 'Złączka z GZ'),
    ('long tank coupling', 'Złączka zbiornikowa długa z GZ'), ('tank coupling', 'Złączka zbiornikowa z GZ'),
    ('female tap coupling', 'Złączka kranowa z GW'), ('female coupling', 'Złączka z GW'),
    ('cylinder connector', 'Złączka do zasobnika z nakrętką'), ('air release elbow', 'Kolano z odpowietrznikiem'),
    ('slow bend', 'Łuk'), ('long male elbow', 'Kolano długie z GZ'), ('male elbow', 'Kolano z GZ'),
    ('female wall elbow', 'Kolano ścienne z GW'), ('backplate elbow', 'Kolano ścienne z GW'), ('female elbow', 'Kolano z GW'),
    ('elbow', 'Kolano'), ('equal tee', 'Trójnik równoprzelotowy'),
    ('tee, one end and branch reduced', 'Trójnik redukcyjny (koniec i odejście)'), ('tee, end and branch reduced', 'Trójnik redukcyjny (koniec i odejście)'),
    ('tee, both ends reduced', 'Trójnik redukcyjny (oba końce)'), ('tee, one end reduced', 'Trójnik redukcyjny (jeden koniec)'),
    ('tee, with reduced branch', 'Trójnik z redukcją odejścia'), ('tee, reduced branch', 'Trójnik z redukcją odejścia'), ('tee, branch reduced', 'Trójnik z redukcją odejścia'),
    ('cross', 'Czwórnik'), ('straight swivel', 'Przyłącze kranowe proste z nakrętką'), ('bent swivel tap connector', 'Przyłącze kranowe kątowe z nakrętką'),
    ('backplate tee', 'Trójnik ścienny z GW'), ('reducing set', 'Zestaw redukcyjny'), ('tank connector', 'Przyłącze zbiornikowe z kołnierzem'),
    ('stop end', 'Zaślepka'), ('sweep tee', 'Trójnik łukowy'), ('ﬂexible union connector', 'Wąż przyłączeniowy z GW'),
    ('ﬂexible tap connector', 'Wąż przyłączeniowy kranowy prosty'), ('bent ﬂexible tap connector', 'Wąż przyłączeniowy kranowy kątowy'),
    ('male end tee', 'Trójnik z GZ na końcu'), ('male branch tee', 'Trójnik z odejściem GZ'), ('female branch tee', 'Trójnik z odejściem GW'),
    ('female end tee', 'Trójnik z GW na końcu'), ('female tee', 'Trójnik z odejściem GW'), ('female adaptor', 'Adapter z GW'),
    ('one piece reducer', 'Redukcja jednoczęściowa'), ('crossover', 'Mijanka'), ('blanking plug', 'Korek zaślepiający'),
    ('type A end to a type B', 'Adapter typ A × typ B do miedzi miękkiej'), ('adaptor, converts Kuterlite 700 end to copper', 'Adapter PE × miedź do lutowania'),
    ('adaptor, converts metric PE to imperial PE', 'Adapter PE metryczny × calowy'), ('adaptor, polyethylene x male end', 'Adapter PE z końcówką wtykową'),
    ('thick land compression ring', 'Pierścień zaciskowy do rur calowych'), ('compression nut', 'Nakrętka zaciskowa'), ('compression ring', 'Pierścień zaciskowy'),
    ('copper liner', 'Tulejka wzmacniająca'), ('liner', 'Tulejka wzmacniająca'), ('gunmetal stopvalve', 'Zawór odcinający z brązu PE × miedź'),
    ('stopvalve', 'Zawór odcinający'), ('appliance valve, straight', 'Zawór do urządzeń, prosty'), ('appliance valve, angle', 'Zawór do urządzeń, kątowy'),
    ('appliance valve, tee', 'Zawór do urządzeń, trójnikowy'), ('SDZR single check valve', 'Zawór zwrotny pojedynczy'), ('DZR Single check valve', 'Zawór zwrotny pojedynczy z GW'),
    ('DZR double check valve', 'Zawór zwrotny podwójny'), ('DZR Double check valve', 'Zawór zwrotny podwójny z GW'), ('ball valve Isolating valve', 'Zawór kulowy odcinający'),
    ('green (K490L) ball valve', 'Zawór kulowy ćwierćobrotowy z dźwignią'), ('chromium plated brass full bore ball valve', 'Zawór kulowy pełnoprzelotowy chromowany'),
    ('water meter kit', 'Zestaw wodomierzowy'), ('screwed bush', 'Tuleja gwintowana sześciokątna'),
]
PL.sort(key=lambda x: -len(x[0]))

def pl_kuter(code, en):
    low = en.lower()
    for a, b in PL:
        if low.startswith(a.lower()):
            name = b; break
    else:
        raise SystemExit(f'Brak tłumaczenia: {code} {en}')
    if 'male' in low and 'female' not in low and ('coupling' in low or 'elbow' in low):
        name += ' (gwint stożkowy)' if 'taper' in low else ' (gwint walcowy)'
    if 'polyethylene' in low and 'PE' not in name: name += ' PE'
    if code.endswith('CP'): name += ' (chrom)'
    return name

def lines(page, fix=None):
    out, imgs = [], []
    for b in page.get_text('dict')['blocks']:
        if b['type'] == 0:
            for l in b['lines']:
                t = ''.join(s['text'] for s in l['spans']).strip()
                if fix: t = t.translate(fix)
                if t: out.append(dict(x=l['bbox'][0], y=l['bbox'][1], t=t))
    for im in page.get_image_info(xrefs=True):
        x0, y0, x1, y1 = im['bbox']
        if (y1 - y0) > 25 and (x1 - x0) > 25: imgs.append(dict(x=x0, y=y0, xref=im['xref']))
    return out, imgs

def parse_tectite(path):
    d = fitz.open(path); prods = []
    HDR = re.compile(r'^(?:PEGLER |TEC-TOOLS )?((?:T|TX|TS|TT|TC|PT|S)\d{1,4}[A-Z]{0,3})\s+(.+)$')
    for pi in range(8, 28):
        L, I = lines(d[pi], FIX)
        hs = sorted([l for l in L if l['x'] < 330 and l['y'] > 90 and HDR.match(l['t'])], key=lambda l: l['y'])
        for i, h in enumerate(hs):
            y0 = h['y']; y1 = hs[i + 1]['y'] if i + 1 < len(hs) else 10000
            reg = [l for l in L if y0 < l['y'] < y1 - 1]
            kod = [l for l in reg if l['t'] == 'Kod']; roz = [l for l in reg if l['t'] == 'Rozmiar']
            if not kod or not roz: continue
            xk, xr, yh = kod[0]['x'], roz[0]['x'], kod[0]['y']
            codes = [l for l in reg if abs(l['x'] - xk) < 22 and l['y'] > yh + 3 and re.match(r'^[0-9A-Z]{5,7}$', l['t'])]
            sizes = [l for l in reg if abs(l['x'] - xr) < 45 and l['y'] > yh + 3 and l['t'] != 'Kod' and not re.match(r'^\d{1,3}$', l['t'])]
            rows = []
            for c in codes:
                s = sorted([z for z in sizes if abs(z['y'] - c['y']) < 8], key=lambda z: abs(z['y'] - c['y']))
                rows.append([s[0]['t'] if s else '–', c['t']])
            m = HDR.match(h['t'])
            im = [g for g in I if y0 - 30 < g['y'] < y1 - 10]
            code, name = m.group(1), m.group(2).strip().replace('Gradownik', 'Gratownik')
            ser = tectite_series(pi + 1, code)
            if pi + 1 in (15, 16) and 'chrom' not in name: name += ' (chrom)'
            prods.append(dict(series=ser, code=code, name=name, en='', rows=rows, xref=im[0]['xref'] if im else None, doc='t'))
    return prods

def parse_kuter(path):
    d = fitz.open(path); prods = []
    HDR = re.compile(r'^([A-Z]{1,4}\d{2,4}[A-Z0-9]{0,5})\s+(.+)$')
    for pi in range(2, 35):
        L, I = lines(d[pi])
        for side in (0, 1):
            C = sorted([l for l in L if (l['x'] < 300) == (side == 0) and l['y'] > 60], key=lambda l: (l['y'], l['x']))
            Ci = [g for g in I if (g['x'] < 300) == (side == 0)]
            dx = [l['x'] for l in C if l['t'] == 'dimension']
            if not dx: continue
            xs = min(dx)
            hs = [l for l in C if abs(l['x'] - xs) < 6 and HDR.match(l['t'])]
            for i, h in enumerate(hs):
                y0 = h['y']; y1 = hs[i + 1]['y'] if i + 1 < len(hs) else 10000
                reg = [l for l in C if y0 <= l['y'] < y1 - 1]
                dim = [l for l in reg if l['t'] == 'dimension']
                if not dim: continue
                yd = dim[0]['y']
                name = ' '.join(l['t'] for l in reg if l['y'] < yd - 40 and abs(l['x'] - xs) < 6)
                hdr = {l['t']: l['x'] for l in reg if abs(l['y'] - yd) < 2}
                xc, xp1, xp2 = hdr.get('code'), hdr.get('pack 1'), hdr.get('pack 2')
                body = [l for l in reg if l['y'] > yd + 10]
                rows = []
                for c in [l for l in body if xc and abs(l['x'] - xc) < 12 and re.match(r'^[0-9A-Z]{4,8}$', l['t'])]:
                    def near(x):
                        cand = sorted([l for l in body if x is not None and abs(l['x'] - x) < 14 and abs(l['y'] - c['y']) < 9 and re.match(r'^\d+$', l['t'])], key=lambda l: abs(l['y'] - c['y']))
                        return int(cand[0]['t']) if cand else 0
                    dm = sorted([l for l in body if l['x'] < (xp1 or 999) - 5 and abs(l['y'] - c['y']) < 9], key=lambda l: abs(l['y'] - c['y']))
                    rows.append([dm[0]['t'] if dm else '–', c['t'], near(xp1), near(xp2)])
                m = HDR.match(name)
                if not m or not rows: continue
                en = re.sub(r'\s+', ' ', m.group(2)).strip()
                im = [g for g in Ci if y0 - 5 < g['y'] < yd]
                prods.append(dict(series=kuter_series(pi + 1), code=m.group(1), name=pl_kuter(m.group(1), en), en=en, rows=rows, xref=im[0]['xref'] if im else None, doc='k'))
    return prods

def slugify(t):
    t = t.replace('ł', 'l').replace('Ł', 'L').replace('×', 'x').replace('°', '')
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')

def save_img(doc, xref, out):
    pm = fitz.Pixmap(doc, xref)
    if pm.colorspace is None: return None
    if pm.colorspace.n not in (1, 3): pm = fitz.Pixmap(fitz.csRGB, pm)
    try:
        im = Image.open(io.BytesIO(pm.tobytes('png')))
    except Exception:
        # nietypowa przestrzeń barw: surowy plik obrazu przez Pillow
        raw = doc.extract_image(xref)
        im = Image.open(io.BytesIO(raw['image']))
        if im.mode == 'CMYK' and raw.get('ext') == 'jpeg':
            from PIL import ImageOps
            im = ImageOps.invert(im.convert('RGB')) if im.getextrema()[0][0] > 200 else im.convert('RGB')
    if im.mode in ('RGBA', 'LA'):
        bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[-1]); im = bg
    im = im.convert('RGB')
    diff = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).convert('L').point(lambda v: 255 if v > 16 else 0)
    bb = diff.getbbox()
    if bb: im = im.crop((max(bb[0] - 6, 0), max(bb[1] - 6, 0), min(bb[2] + 6, im.width), min(bb[3] + 6, im.height)))
    im.thumbnail((240, 240)); im.save(out, quality=86)
    return im.size

def main(tpath, kpath):
    docs = {'t': fitz.open(tpath), 'k': fitz.open(kpath)}
    prods = parse_tectite(tpath) + parse_kuter(kpath)
    merged, key = [], {}
    for p in prods:
        k = (p['series'], p['code'], p['name'])
        if k in key:
            have = {r[1] for r in key[k]['rows']}
            key[k]['rows'] += [r for r in p['rows'] if r[1] not in have]; continue
        key[k] = p; merged.append(p)
    os.makedirs(os.path.join(ROOT, 'img', 'pegler'), exist_ok=True)
    groups = []
    for p in merged:
        brand = SERIES[p['series']]['brand'].lower()
        slug = f"{'tectite' if p['doc'] == 't' else 'kuterlite'}-{slugify(p['name'])}-{slugify(p['code'])}"
        img = f"{p['doc']}-{slugify(p['code'])}-{slugify(p['name'])[:24]}"
        if p['xref']: save_img(docs[p['doc']], p['xref'], os.path.join(ROOT, 'img', 'pegler', img + '.webp'))
        groups.append(dict(series=p['series'], code=p['code'], name=p['name'], en=p['en'], slug=slug, img=img if p['xref'] else None, rows=p['rows']))
    seen = {}
    for g in groups:
        if g['slug'] in seen:
            print('  ten sam adres:', g['slug'], g['series'], '/', seen[g['slug']])
            g['slug'] += '-' + g['series'].split('-', 1)[1]
        seen[g['slug']] = g['series']
    assert len({g['slug'] for g in groups}) == len(groups), 'duplikat slug'
    out = dict(src='Tectite · katalog 2026; Kuterlite · cennik październik 2024 (bez cen)', series=SERIES, groups=groups)
    json.dump(out, open(os.path.join(ROOT, 'data', 'pegler.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    for s in SERIES:
        gs = [g for g in groups if g['series'] == s]
        print(f"{s:22s} grup {len(gs):3d}  pozycji {sum(len(g['rows']) for g in gs):4d}")
    print('razem grup', len(groups), 'pozycji', sum(len(g['rows']) for g in groups))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
