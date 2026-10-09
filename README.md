# Armatex.pl — strona dla hurtowni

Statyczna strona dystrybutora złączek Besco i Pegler Yorkshire (Tectite, Kuterlite) dla hurtowni
instalacyjnych. Bez procesu budowania na serwerze: HTML + CSS + JS, publikowane z katalogu głównego
(GitHub Pages: `.github/workflows/pages.yml`, Netlify: `netlify.toml`).

## Struktura

- `index.html`: strona główna; strony systemów `zlaczki-zaprasowane-press.html`, `zlaczki-na-wcisk-tectite.html`,
  `zlaczki-skrecane-kuterlite.html`, `zlaczki-lutowane.html`; `wyszukiwarka.html` (wyszukiwarka 1 936 indeksów Besco
  z listą do wyceny), `do-pobrania.html` (katalogi i dokumenty z filtrem), `o-firmie.html`, `wspolpraca.html`, `kontakt.html`.
- Poradniki: `poradniki.html` i artykuły `poradnik-*.html` (dane Article w JSON-LD). Nowy poradnik dodaje się
  wywołaniem `art(...)` w `tools/strony.py`; lista, menu i sitemap aktualizują się same.
- Strony grup produktów: 161 × `besco-*.html`, 224 × `tectite-*.html` / `kuterlite-*.html`. Tabela rozmiarów
  z numerami artykułów, wybór ilości i jednostki (karton, worek, opakowanie, sztuki) i „Dodaj” do listy do wyceny.
  Lista jest zapisywana w przeglądarce (`localStorage`, klucz `armatex-rfq`) i trafia do formularza.
- `c.css`, `c.js`: wspólne style i skrypty.
- `site.webmanifest`: nazwa i ikony strony dla telefonów (ikony w `assets/img/`).
- `data/`: `besco-2026.json` (Besco), `pegler.json` (Tectite, Kuterlite) i `katalog.json` (dane wyszukiwarki, składane przez generator).
- `img/`: logo, hero, zdjęcia produktów (`besco/`, `pegler/`, `oferta/`, `linie/`), obrazek udostępniania (`og/`).
  Zdjęcia grup produktów mają beż `#F3F1EC` wpisany w plik (miniatury w kafelkach, liście do wyceny i wyszukiwarce).
  Jeśli obok leży plik `<nazwa>-l.webp` (to samo zdjęcie na białym tle, czasem większe), strona produktu pokazuje go zamiast miniatury.
  Generator dopisuje do każdego adresu zdjęcia `?v=<skrót treści>`, więc podmiana pliku pod tą samą nazwą
  od razu trafia do przeglądarek mimo 7-dniowego cache `/img/*`.
- `pliki/katalog-besco-2026.pdf`: katalog Besco 2026 (link w menu „Oferta → Katalogi”).
- `pliki/katalog-tectite.pdf`: katalog Tectite Classic (złączki 16 i 20 mm do rur PEX), link na stronie systemu Tectite i w „Do pobrania”.
- `pliki/katalog-kuterlite.pdf`: katalog Kuterlite (K900 Pro, K700, zawory, akcesoria) bez cen: kolumny cen usunięte z cennika producenta.
- `pliki/instrukcja-montazu-tectite.pdf`: instrukcja montażu złączek na wcisk Tectite (strona Tectite, Do pobrania, poradnik „Tectite czy press?”).
- `assets/`: fonty (Outfit, IBM Plex Mono) i favicony.
- `sitemap.xml`, `robots.txt`.
- `tools/`: generator stron i skrypty danych (niżej).

## Zmiany treści: generator

Strony HTML są generowane, więc zmiany w treści rób w `tools/strony.py` (szablon sekcji:
`tools/szablon-c.html`), nie ręcznie w plikach HTML:

```bash
pip install pillow beautifulsoup4
python3 tools/strony.py
```

`c.css` i `c.js` edytuje się bezpośrednio, a potem uruchamia generator: dopisuje on do linków `?v=<hash treści>`, dzięki czemu Netlify może trzymać te pliki w cache przez rok, a po zmianie przeglądarki pobiorą nową wersję. Generator skraca też tytuły do ok. 60 znaków i opisy do 160.

Dane produktów z katalogów PDF (PDF-y nie są trzymane w repo):

```bash
pip install pymupdf pillow
python3 tools/katalog_besco.py sciezka/Besco_2026_catalogue.pdf
python3 tools/katalog_pegler.py katalog_tectite_2026.pdf Kuterlite-price-list-Oct-2024.pdf
```

Przy nowym wydaniu katalogu sprawdź w skryptach zakresy stron i tłumaczenia nazw. Pegler: poza danymi zostało kilka
pozycji o nietypowym układzie tabel (kolektory TM80/TM81, węże TF90/TF92, część akcesoriów Kuterlite).

## Wyszukiwarka

Wyszukiwarka (`wyszukiwarka.html`) czyta `data/katalog.json`, który generator (`tools/strony.py`) składa przy każdym
uruchomieniu z `data/besco-2026.json` i `data/pegler.json` (Besco, Tectite, Kuterlite).

## Wersje językowe (/en/, /ua/)

Generator zapisuje każdą stronę także jako `en/<ta sama nazwa>.html` i `ua/<ta sama nazwa>.html` (ukraiński: katalog `ua/`, kod języka `uk`). Tłumaczenie robi
`tools/i18n.py` na gotowym HTML według słowników `tools/en.json` i `tools/uk.json`:

- `t`: teksty stron (akapity, nagłówki, przyciski, atrybuty alt/aria-label, opisy meta). Znaczniki wewnątrz tekstu
  są zapisane jako `<0>…</0>`, `<1/>` itd.;
- `names`: nazwy produktów, linii i zastosowań (z nich składane są zdania na stronach grup i nazwy w wyszukiwarce);
- `quals`: dopiski linii w pełnych nazwach grup (np. „miedziany press, profil V”);
- `keep`: teksty, których się nie tłumaczy (nazwy własne, skróty aprobat).

Zdania stron grup (opis, tytuł, meta) składa szablon `GT` w `tools/strony.py`. Po zmianie treści po polsku generator
wypisuje liczbę tekstów bez tłumaczenia i zapisuje je do `tools/en-brak.json` i `tools/uk-brak.json` (tekst → strona).
Dopisz tłumaczenia do słowników i uruchom generator ponownie. Teksty JS (lista do wyceny, formularz) są w `c.js`
(funkcja `L('po polsku', 'in English', 'українською')`). Strony mają `hreflang` pl/en/uk, przełącznik języków w menu
i własne strony 404 (`/en/*`, `/ua/*` w `_redirects`; stare adresy `/uk/*` → 301 na `/ua/`). Outfit nie ma cyrylicy: znaki cyrylicy biorą krój Onest
(`assets/fonts/onest-cyrillic-wght-normal.woff2`, licencja OFL), etykiety IBM Plex Mono w wersji z cyrylicą.

## Złączki INOX

`tools/katalog_inox.py` dopisuje do `data/besco-2026.json` linie INOX 304 i INOX 316L (katalogi `pliki/katalog-besco-inox-*.pdf`).
Uruchamiaj go **po** `tools/katalog_besco.py`, bo ten nadpisuje cały plik danych. Katalog 316L ma tekst zamieniony na krzywe,
więc skrypt czyta go przez OCR (`pip install rapidocr_onnxruntime`) i sprawdza numery artykułów względem kodu grupy.

## Formularz

Formularz (strona główna i `kontakt.html`) obsługuje **Netlify Forms** (formularz `zapytanie`,
stała `FORM_NAME` w `tools/strony.py`). Netlify wykrywa go przy wdrożeniu po atrybucie `data-netlify`,
zapisuje zgłoszenia w panelu (Forms) i wysyła powiadomienia. Jednorazowo w panelu Netlify:
**Forms → Enable form detection**, potem po wdrożeniu **Forms → zapytanie → Form notifications →
Email notification** na `biuro@armatex.pl`. Temat maila ustawia ukryte pole `subject`.
Na kopii w GitHub Pages formularz nie działa (pokazuje komunikat z telefonem i e-mailem).

## Przed startem w wyszukiwarkach

1. **Indeksowanie jest włączone** (strona działa pod armatex.pl). Wyjątek: `404.html` ma `noindex`.
2. Adresy kanoniczne, Open Graph, `sitemap.xml` i dane strukturalne zakładają domenę `https://armatex.pl/`
   (stała `SITE` w generatorze).
3. Uzupełnij godziny otwarcia i profile firmy (`openingHours`, `sameAs`) w danych `WholesaleStore`.
4. Przy zmianie domeny ze starej strony ustaw przekierowania 301 ze starych adresów.
5. Tło sekcji kontaktu na stronie głównej ładuje się z CDN Higgsfield (`d8j0ntlcm91z4.cloudfront.net`);
   warto pobrać je do `img/` i podmienić adres.
6. Potwierdź u Besco prawo do udostępniania katalogu PDF.

## Strona 404

`404.html` GitHub Pages podaje pod każdym nieistniejącym adresem, także zagnieżdżonym. Skrypt na początku `<head>`
ustawia `<base>` na katalog strony (`/ARAMTEX-WEBSITE/` na github.io albo `/` na własnej domenie), żeby style,
zdjęcia i linki działały. Wyszukiwarka na 404 przekazuje frazę do `wyszukiwarka.html?q=…`.

## Przekierowania ze starej strony

`_redirects` (Netlify) przekierowuje 301 adresy starej strony armatex.pl na nowe podstrony, np. `/tectite` → Złączki na
wcisk, `/gutpress-v---copper` → Złączki zaprasowane, `/dokumenty` → Do pobrania. Nowy stary adres, który wyjdzie w Google
Search Console jako 404, dopisz tam jako kolejną linię.
