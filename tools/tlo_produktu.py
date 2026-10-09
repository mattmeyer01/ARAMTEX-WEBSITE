"""Zdjęcia na stronę produktu: białe tło zamiast beżu.

Strona produktu pokazuje zdjęcie na beżowej ramce z mix-blend-mode: multiply, więc tło zdjęcia musi być
białe, inaczej wychodzi ciemniejszy prostokąt w ramce. Miniatury (kafelki, lista do wyceny) mają za to beż
wpisany w plik. Dla każdego zdjęcia grupy bez pliku <nazwa>-l.webp skrypt tworzy go z miniatury: dzieli
każdy kanał przez kolor tła zdjęcia (mediana brzegu). Tło staje się białe, a produkt po zmieszaniu z beżem
ramki wygląda tak jak na miniaturze; tło z gradientem lub cieniem przy brzegu dodatkowo wybiela
(jasne, neutralne piksele połączone z brzegiem). Zdjęć, w których produkt sięga brzegu, nie rusza.

Użycie: python3 tools/tlo_produktu.py, potem python3 tools/strony.py (nowe ?v= w adresach).
"""
import json, os
from PIL import Image, ImageChops, ImageDraw, ImageFilter

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


def border_median(im):
    w, h = im.size
    px = [im.getpixel((x, y)) for x in range(w) for y in (0, 1, h - 2, h - 1)]
    px += [im.getpixel((x, y)) for y in range(h) for x in (0, 1, w - 2, w - 1)]
    return tuple(sorted(c[i] for c in px)[len(px) // 2] for i in range(3))


def white_bg(im, bg):
    luts = []
    for c in bg:
        luts += [min(255, round(v * 255 / c)) for v in range(256)]
    im = im.point(luts)
    # resztki szumu tła (wszystkie kanały prawie białe) do czystej bieli
    r, g, b = im.split()
    m = ImageChops.darker(ImageChops.darker(r, g), b).point(lambda v: 255 if v >= 246 else 0)
    return flood_white(Image.composite(Image.new('RGB', im.size, (255, 255, 255)), im, m))


def flood_white(im):
    """Tło z gradientem lub cieniem przy brzegu: jasne, neutralne piksele połączone z brzegiem do bieli (miękka krawędź)."""
    w, h = im.size
    r, g, b = im.split()
    mn = ImageChops.darker(ImageChops.darker(r, g), b); mx = ImageChops.lighter(ImageChops.lighter(r, g), b)
    px = sorted(mn.getpixel((x, y)) for x in range(w) for y in (0, h - 1))
    t = max(190, min(238, px[len(px) // 2] - 28))            # próg jasności względem tła tego zdjęcia
    cand = ImageChops.multiply(ImageChops.subtract(mx, mn).point(lambda v: 255 if v <= 18 else 0),
                               mn.point(lambda v: 255 if v >= t else 0))
    m = Image.new('L', (w + 2, h + 2), 255); m.paste(cand, (1, 1))
    ImageDraw.floodfill(m, (0, 0), 128)
    m = m.crop((1, 1, w + 1, h + 1)).point(lambda v: 255 if v == 128 else 0).filter(ImageFilter.GaussianBlur(0.7))
    return Image.composite(Image.new('RGB', im.size, (255, 255, 255)), im, m)


def group_images():
    out = []
    for g in json.load(open(R + '/data/besco-2026.json', encoding='utf-8'))['groups']:
        out.append('img/besco/%s.webp' % g[4])
    for g in json.load(open(R + '/data/pegler.json', encoding='utf-8'))['groups']:
        if g.get('img'): out.append('img/pegler/%s.webp' % g['img'])
    return list(dict.fromkeys(out))


def main():
    made, skipped = [], []
    for p in group_images():
        f = os.path.join(R, p); big = f[:-5] + '-l.webp'
        if not os.path.exists(f) or os.path.exists(big): continue
        im = Image.open(f).convert('RGB'); bg = border_median(im)
        if min(bg) >= 250: continue                       # już białe tło: strona produktu bierze miniaturę
        if min(bg) < 215: skipped.append((p, bg)); continue
        white_bg(im, bg).save(big, 'WEBP', quality=90, method=6)
        made.append(p)
    print('utworzone -l:', len(made))
    for p, bg in skipped: print('pominięte (produkt przy brzegu):', p, bg)


if __name__ == '__main__':
    main()
