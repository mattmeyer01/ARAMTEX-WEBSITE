# Szkice (robocze, niepublikowane)

Strony w tym katalogu nie są podlinkowane z nawigacji. Mają `noindex`, a Netlify dokłada
nagłówek `X-Robots-Tag` dla `/szkice/*` (patrz `netlify.toml`).

| Plik | Co to jest |
|------|------------|
| `landing-b.html` | Szkic B: jasny landing z szybkim zapytaniem i wzorcami BYQ. |
| `c/` | Szkic C (aktualny, dla hurtowni), wersja wielostronicowa: `index.html` (strona główna), strony systemów `zlaczki-zaciskane-press`, `zlaczki-na-wcisk-tectite`, `zlaczki-skrecane-kuterlite`, `zlaczki-lutowane`, `katalog.html` (wyszukiwarka 1 936 indeksów Besco z listą do wyceny), `wspolpraca.html`, `kontakt.html`. Wspólne `c.css` i `c.js`. |
| `landing-c.html` | Poprzednia, jednostronicowa wersja szkicu C (archiwum). |

## Dane i zdjęcia produktów (szkic C)

- `data/besco-2026.json`: 9 linii, 176 grup, 1 936 pozycji (numer artykułu, rozmiar, worek, karton)
  z katalogu Besco Fittings & Connectors 2026. Strona doczytuje plik dopiero przy wyszukiwarce.
- `img/oferta/*.webp`: wycięcia produktów Besco, Tectite i Kuterlite na białym tle (kopie `assets/img/oferta`).
- `img/besco/x<xref>.webp`: zdjęcia produktów wycięte z katalogu. Tło jest wypalone na kolor
  `#F3F1EC` (tło kafli i wyszukiwarki). Przy innym tle trzeba je wygenerować ponownie.
- Odświeżenie z nowego katalogu:

  ```bash
  pip install pymupdf pillow
  python3 szkice/tools/katalog_besco.py sciezka/do/katalogu.pdf
  ```

  Przy nowym wydaniu sprawdź w skrypcie zakresy stron linii (`SERIES`) i parametry z nagłówków
  (`META`), bo część nagłówków katalogu jest w PDF grafiką. PDF katalogu nie jest trzymany w repo.

## Zdjęcia sesyjne Higgsfield

Hero, panele metod łączenia, magazyn i tło kontaktu ładują się z CDN Higgsfield
(`d8j0ntlcm91z4.cloudfront.net`). Przed publikacją warto je pobrać do `img/` i podmienić adresy,
żeby strona nie zależała od zewnętrznego CDN.

## SEO szkicu C

- Pełne nazwy systemów w menu, nagłówkach H1, tytułach i adresach stron (np. „Złączki zaciskane press Besco”).
- Tytuły do około 60 znaków, opisy (`meta description`) do około 160 znaków.
- Dane strukturalne JSON-LD: `Organization` na stronie głównej, `BreadcrumbList` na podstronach,
  `ItemList` linii produktów na stronach systemów. Adresy w danych zakładają docelowe ścieżki w katalogu
  głównym `https://armatex.pl/`; przy innym układzie trzeba je zmienić.
- Szkic ma `noindex`. Przed publikacją usuń go i dodaj `<link rel="canonical">` na każdej stronie.

