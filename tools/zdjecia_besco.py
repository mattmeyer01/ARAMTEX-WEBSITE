"""Podmienia zdjęcia grup Besco na zdjęcia produktowe od Besco (lepsza jakość niż wycinki z katalogu PDF).

Użycie:
    python3 -I tools/zdjecia_besco.py KATALOG_ZE_ZDJECIAMI
    python3 tools/strony.py
    python3 tools/katalog_pdf.py besco-2026      # katalog PDF też bierze nowe zdjęcia (foto/)

KATALOG_ZE_ZDJECIAMI to rozpakowane paczki od Besco (01-V copper, 03-M copper, 05-M carbon steel), przeszukiwane
rekurencyjnie. Plik dopasowujemy po początku nazwy: GP5001.jpg, 68000(6270).jpg, 23310(2092G,…).jpg.
Pary sprawdzone wzrokowo z obecnymi zdjęciami grup (ten sam kształt i te same końcówki). Numery 5-cyfrowe
(68xxx, 79xxx) są początkiem numerów artykułów w data/besco-2026.json. Pliki bez pary w katalogu 2026
(np. GPG5085, 79040, 2358G, 2030, 2950, 2960) pomijamy.

Dla każdej grupy zapisuje (nadpisuje):
    img/besco/<klucz>.webp          miniatura: dłuższy bok 240 px, tło kamienne strony (jak tools/katalog_besco.py)
    img/besco/<klucz>-l.webp        strona produktu: dłuższy bok 720 px, białe tło (ramka strony robi multiply)
    tools/katalog-pdf/foto/<klucz>.webp   druk katalogu PDF: dłuższy bok 800 px (ok. 300 dpi na okładce), białe tło
Mniejszych zdjęć nie powiększamy.
"""
import os
import sys

from PIL import Image, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlo_produktu import border_median  # noqa: E402

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
STONE = (243, 241, 236)

MAPA = {
    # Gutpress Copper V · woda
    'GP5001': ['x58'], 'GP5002': ['x59'], 'GP5040': ['x60'], 'GP5041': ['x112'], 'GP5270': ['x113'],
    'GP5270S': ['x114'], 'GP5130': ['x115'], 'GP5240': ['x136'], 'GP5243': ['x137'], 'GP5301': ['x152'],
    'GP5085': ['x153'], 'GP5086': ['x154'],
    'GP5131': ['x121'],     # trójnik redukcyjny w tym samym układzie co zdjęcie grupy GP5130 (redukcyjny)
    # Gutpress Copper V · gaz
    'GPG5001': ['x248'], 'GPG5002': ['x249'], 'GPG5040': ['x250'], 'GPG5041': ['x260'], 'GPG5130': ['x261'],
    'GPG5131': ['x262'], 'GPG5240': ['x263'], 'GPG5243': ['x274'], 'GPG5270': ['x275'], 'GPG5301': ['x276'],
    # Gutpress Copper M · woda (68xxx = numery artykułów, w nawiasie stary kod)
    '68000': ['x367'], '68030': ['x354'], '68040': ['x368'], '68100': ['x327'], '68110': ['x341'],
    '68200': ['x314'], '68210': ['x313'], '68230': ['x326'], '68240': ['x334'], '68350': ['x383'],
    '68360': ['x382'], '68410': ['x369', 'x384'], '68430': ['x353', 'x366'],
    # Gutpress Copper M · gaz
    '79000': ['x469'], '79100': ['x471'], '79200': ['x456'], '79210': ['x457'], '79230': ['x458'],
    '79240': ['x459'], '79410': ['x482'], '79430': ['x470'],
    # Gutpress Carbon Steel M
    '23000': ['x877'], '23010': ['x878'], '23020': ['x887'], '23030': ['x888'], '23040': ['x886'],
    '23080': ['x899'], '23100': ['x927'], '23120': ['x936'], '23200': ['x897'], '23210': ['x898'],
    '23230': ['x907'], '23240': ['x908'], '23250': ['x909'], '23260': ['x918'], '23400': ['x949'],
    '23410': ['x917'], '23430': ['x919'], '23450': ['x946'], '23460': ['x947'],
    '23110': ['x937'],      # zwężony koniec przelotu (22 × 22 × 15); x928 i x938 mają zwężone odejście, zostają
    '23310': ['x948'],      # kolano z GZ; Besco: „2092G, wcześniej błędnie 2090G”, w katalogu 2026 nadal 2090G
}


def crop(im, bg, tol):
    """Przycięcie do produktu (piksele różne od tła o więcej niż tol) z marginesem 4%."""
    bb = ImageChops.difference(im, Image.new('RGB', im.size, bg)).convert('L').point(lambda v: 255 if v > tol else 0).getbbox()
    if not bb:
        return im
    m = max(6, round(0.04 * max(bb[2] - bb[0], bb[3] - bb[1])))
    return im.crop((max(0, bb[0] - m), max(0, bb[1] - m), min(im.width, bb[2] + m), min(im.height, bb[3] + m)))


def clean(im):
    """Białe tło i przycięcie do produktu. Dwa przebiegi: zdjęcia bywają wklejone na białe płótno jako jaśniejszy
    prostokąt, więc tło wokół produktu mierzymy jeszcze raz po pierwszym przycięciu."""
    for _ in range(2):
        bg = border_median(im)
        im = fit(crop(im, bg, 24), 1000)
        bg = border_median(im)
        if min(bg) < 200:                   # produkt sięga brzegu: tła nie da się zmierzyć
            continue
        luts = []
        for c in bg:
            luts += [min(255, round(v * 255 / c)) for v in range(256)]
        im = im.point(luts)
        # resztki szumu tła (wszystkie kanały prawie białe) do czystej bieli
        r, g, b = im.split()
        m = ImageChops.darker(ImageChops.darker(r, g), b).point(lambda v: 255 if v >= 246 else 0)
        im = Image.composite(Image.new('RGB', im.size, 'white'), im, m)
    return crop(im, (255, 255, 255), 10)


def fit(im, n):
    im = im.copy()
    im.thumbnail((n, n), Image.LANCZOS)
    return im


def main(src):
    files = {}
    for dp, _, fn in os.walk(src):
        for f in fn:
            stem = os.path.splitext(f.replace('（', '(').replace('）', ')'))[0].split('(')[0].strip()
            if stem in MAPA:
                files[stem] = os.path.join(dp, f)
    brak = sorted(set(MAPA) - set(files))
    if brak:
        sys.exit('Brak plików: ' + ', '.join(brak))
    os.makedirs(os.path.join(R, 'tools/katalog-pdf/foto'), exist_ok=True)
    for stem, keys in MAPA.items():
        im = clean(Image.open(files[stem]).convert('RGB'))
        for k in keys:
            fit(im, 720).save(os.path.join(R, f'img/besco/{k}-l.webp'), 'WEBP', quality=90, method=6)
            th = fit(im, 240)
            ImageChops.multiply(th, Image.new('RGB', th.size, STONE)).save(os.path.join(R, f'img/besco/{k}.webp'), 'WEBP', quality=82, method=6)
            fit(im, 800).save(os.path.join(R, f'tools/katalog-pdf/foto/{k}.webp'), 'WEBP', quality=90, method=6)
        print(stem, '→', ', '.join(keys), im.size)
    print(sum(len(v) for v in MAPA.values()), 'zdjęć grup z', len(MAPA), 'plików')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
