# Armatex.pl — strona dla hurtowni

Statyczna strona dystrybutora złączek Besco i Pegler Yorkshire (Tectite, Kuterlite) dla hurtowni
instalacyjnych. Bez procesu budowania na serwerze: HTML + CSS + JS, publikowane z katalogu głównego
(GitHub Pages: `.github/workflows/pages.yml`, Netlify: `netlify.toml`).

## Struktura

- `index.html`: strona główna; strony systemów `zlaczki-zaciskane-press.html`, `zlaczki-na-wcisk-tectite.html`,
  `zlaczki-skrecane-kuterlite.html`, `zlaczki-lutowane.html`; `katalog.html` (wyszukiwarka 1 936 indeksów Besco
  z listą do wyceny), `wspolpraca.html`, `kontakt.html`.
- Strony grup produktów: 161 × `besco-*.html`, 224 × `tectite-*.html` / `kuterlite-*.html`. Tabela rozmiarów
  z numerami artykułów, wybór ilości i jednostki (karton, worek, opakowanie, sztuki) i „Dodaj” do listy do wyceny.
  Lista jest zapisywana w przeglądarce (`localStorage`, klucz `armatex-rfq`) i trafia do formularza.
- `c.css`, `c.js`: wspólne style i skrypty.
- `data/`: `besco-2026.json` (dane wyszukiwarki), `pegler.json` (Tectite, Kuterlite).
- `img/`: logo, hero, zdjęcia produktów (`besco/`, `pegler/`, `oferta/`, `linie/`), obrazek udostępniania (`og/`).
- `pliki/katalog-besco-2026.pdf`: katalog Besco 2026 (link w menu „Oferta → Katalogi”).
- `assets/`: fonty (Outfit, IBM Plex Mono) i favicony.
- `sitemap.xml`, `robots.txt`.
- `tools/`: generator stron i skrypty danych (niżej).

## Zmiany treści: generator

Strony HTML są generowane, więc zmiany w treści rób w `tools/strony.py` (szablon sekcji:
`tools/szablon-c.html`), nie ręcznie w plikach HTML:

```bash
pip install pillow
python3 tools/strony.py
```

`c.css` i `c.js` edytuje się bezpośrednio.

Dane produktów z katalogów PDF (PDF-y nie są trzymane w repo):

```bash
pip install pymupdf pillow
python3 tools/katalog_besco.py sciezka/Besco_2026_catalogue.pdf
python3 tools/katalog_pegler.py katalog_tectite_2026.pdf Kuterlite-price-list-Oct-2024.pdf
```

Przy nowym wydaniu katalogu sprawdź w skryptach zakresy stron i tłumaczenia nazw. Pegler: poza danymi zostało kilka
pozycji o nietypowym układzie tabel (kolektory TM80/TM81, węże TF90/TF92, część akcesoriów Kuterlite).

## Formularz

Formularz (strona główna i `kontakt.html`) wysyła przez [FormSubmit](https://formsubmit.co) na
`armatex1@gmail.com` (stała `FORM_TO` w `tools/strony.py`). Pierwsza wysyłka z nowej domeny może wymagać
potwierdzenia linkiem, który FormSubmit wyśle na ten adres.

## Przed startem w wyszukiwarkach

1. **Indeksowanie jest wyłączone** (`<meta name="robots" content="noindex, nofollow">` w `tools/strony.py`,
   jak w poprzedniej wersji). Usuń tę linię i wygeneruj strony, gdy strona ma być widoczna w Google.
2. Adresy kanoniczne, Open Graph, `sitemap.xml` i dane strukturalne zakładają domenę `https://armatex.pl/`
   (stała `SITE` w generatorze).
3. Uzupełnij godziny otwarcia i profile firmy (`openingHours`, `sameAs`) w danych `WholesaleStore`.
4. Przy zmianie domeny ze starej strony ustaw przekierowania 301 ze starych adresów.
5. Tło sekcji kontaktu na stronie głównej ładuje się z CDN Higgsfield (`d8j0ntlcm91z4.cloudfront.net`);
   warto pobrać je do `img/` i podmienić adres.
6. Potwierdź u Besco prawo do udostępniania katalogu PDF.
