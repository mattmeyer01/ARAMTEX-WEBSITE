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
- Każda strona ma `rel="canonical"` i znaczniki Open Graph/Twitter z obrazkiem `img/og/armatex-og.jpg`
  (1200 × 630). Dane firmy na stronie głównej: `WholesaleStore` (adres, telefon, handlowcy, marki) i `WebSite`.
  Brakuje godzin otwarcia i linków do profili firmy (`openingHours`, `sameAs`): uzupełnić po uzyskaniu danych.
- Strony grup produktów `besco-*.html` (161 stron, z `data/besco-2026.json`): tabela rozmiarów z numerami
  artykułów i opakowaniami, parametry linii, przycisk „Dodaj” do listy do wyceny, linki do innych grup w linii.
  Linkowane ze stron systemów („Produkty w systemie”) i ze spisu na stronie katalogu.
- Strony grup Pegler Yorkshire `tectite-*.html` i `kuterlite-*.html` (224 strony) z `data/pegler.json`,
  zdjęcia w `img/pegler/`. Dane generuje `tools/katalog_pegler.py` z katalogu Tectite 2026 i cennika
  Kuterlite (październik 2024): kody, rozmiary, opakowania Kuterlite; bez cen. Nazwy Kuterlite są
  tłumaczone na polską nomenklaturę, angielska nazwa zostaje na stronie jako „Nazwa w cenniku”.
  Poza danymi zostało kilka pozycji o nietypowym układzie tabel (kolektory TM80/TM81, węże TF90/TF92,
  część akcesoriów Kuterlite).
- `c/sitemap.xml` (393 adresy) i `c/robots.txt` są przygotowane pod wersję produkcyjną w katalogu głównym
  `https://armatex.pl/`.
- Szkic ma `noindex`. Przed publikacją usuń go ze wszystkich stron.
- `pliki/katalog-besco-2026.pdf`: katalog Besco 2026 (66 stron) z poprawionym tytułem w metadanych
  (oryginał miał tytuł „画册 11.11”). Link w menu „Oferta → Katalogi”, na stronie katalogu i na stronach
  systemów Besco; otwiera się w nowej karcie.
- `img/linie/*.webp`: zdjęcia produktów do tabel „Linie w systemie” (po jednym na linię), wycięte z katalogów
  Besco 2026, Tectite 2026 i cennika Kuterlite na białym tle.
- `img/hero/hero-paleta-*.webp`: zdjęcie hero z paletą towaru (sesja Higgsfield, wybrane przez klienta): 2000 i 1200 px
  na komputer oraz kadr 800 × 1001 na telefon. Lokalny plik, więc działa też bez CDN Higgsfield.
