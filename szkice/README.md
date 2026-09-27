# Szkice (robocze, niepublikowane)

Strony w tym katalogu nie są podlinkowane z nawigacji. Mają `noindex`, a Netlify dokłada
nagłówek `X-Robots-Tag` dla `/szkice/*` (patrz `netlify.toml`).

| Plik | Co to jest |
|------|------------|
| `landing-b.html` | Szkic B: jasny landing z szybkim zapytaniem i wzorcami BYQ. |
| `landing-c.html` | Szkic C (premium, dla hurtowni): cztery systemy Besco i Pegler Yorkshire w zakładkach, wyszukiwarka 1 936 pozycji Besco z listą do wyceny. |

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
