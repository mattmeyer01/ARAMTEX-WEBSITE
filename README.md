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
- Intro przy wejściu na stronę: granatowa kurtyna z logo, „rurą” wypełnianą według postępu ładowania (cztery złączki =
  cztery metody łączenia) i licznikiem 0–100 %; przy 100 % krótki błysk i kurtyna się rozpływa (całość ok. 1,5 s: pasek 0,85 s, pauza 0,25 s, zanikanie 0,4 s). Skrypt `INTRO_JS` w `tools/strony.py` (na początku
  `<body>`, przełącznik `INTRO_ON`, czasy `INTRO_MIN`/`INTRO_MAX`, teksty PL/EN/UK w `INTRO_TXT`), style `.pl` w `c.css`.
  Pokazuje się tylko przy wejściu z zewnątrz (odsyłacz spoza strony albo brak), nie przy przejściach między podstronami,
  nie przy „wstecz”, nie w karcie otwartej w tle, nie przy `prefers-reduced-motion`, przy oszczędzaniu danych ani na 404. Kliknięcie
  albo Esc kończy je od razu. Nic nie zapisuje w przeglądarce. Animacje wejścia strony (`.hero`, `.phead`, `.in`, liczniki) czekają, aż kurtyna zacznie znikać
  (klasa `intro` na `<html>`, zdarzenie `armatex:intro`).
- Pasek nowości nad menu (INOX 304) i okno z opisem: `bar_html()` w `tools/strony.py`, style `.abar` i `.adlg`
  w `c.css`, obsługa w `c.js`. Pasek nie ma przycisku zamykania i jest na każdej stronie (klasa `has-bar`
  w znaczniku `<html>`). `BAR_ID` to identyfikator komunikatu w statystykach, `BAR_ID=None` wyłącza pasek na wszystkich stronach.
- Statystyki odwiedzin: Plausible Analytics (bez cookies i bez zapisu w przeglądarce). Skrypt wstawia `head()`
  z napisu `PLAUSIBLE` w `tools/strony.py` na wszystkie strony poza przekierowaniami; pusty napis go wyłącza.
  Narzędzie opisuje polityka prywatności (pkt 2, 3, 4, 6, 8 i 9), więc przy jego zmianie trzeba ją też poprawić.
  Zdarzenia dla celów w panelu Plausible wysyła `track()` w `c.js` (nazwy muszą być identyczne jak cele):
  `Zapytanie wysłane` (po udanym wysłaniu formularza; props `profil`, `pozycje`, `skad`), `Telefon` i `E-mail`
  (props `kontakt`, `miejsce`), `Dodaj do wyceny` (`kod`, `miejsce`), `Lista do formularza` (`pozycje`),
  `Pasek nowości: okno` i `Pasek nowości: przejście` (`komunikat` = `BAR_ID`), `Zgoda cookies` (wybór w oknie zgody;
  `wybor`: `wszystkie`, `statystyki`, `marketing` albo `odrzucone`). Strony 404 wysyłają `404`
  (`JS404` w `tools/strony.py`). Pobrania plików, linki wychodzące i wysłania formularzy (`Form: Submission`)
  liczy sam Plausible. Nowe zdarzenie trzeba też dopisać do polityki prywatności (pkt 2).
- Menedżer tagów Google (GTM): `GTM_ID` w `tools/strony.py` (pusty wyłącza GTM). `head()` wstawia przed kodem GTM
  tryb zgody Google z domyślnym „brak zgody” (`ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage`),
  więc tagi Google z kontenera (GA4, Google Ads) nie zapisują cookies. Fragment `noscript` stoi zaraz po `<body>`.
- Okno zgody na pliki cookies (`c.js`, style `.ck` w `c.css`): „Akceptuję wszystkie”, „Odrzucam” i „Ustawienia”
  (kategorie Statystyki → `analytics_storage`, Marketing → `ad_storage`, `ad_user_data`, `ad_personalization`).
  Wybór zostaje w przeglądarce (klucz `armatex-zgoda`, wersja `ZV`, 12 miesięcy) i w `<head>` (`GTM_HEAD`) trafia do
  trybu zgody Google przed kodem GTM; wersja i okres muszą być takie same w obu miejscach. Każdy wybór wysyła do
  dataLayer zdarzenie `zgoda_cookies` (`zgoda_statystyki`, `zgoda_marketing`: `granted`/`denied`) i do Plausible
  `Zgoda cookies`. Wycofanie zgody usuwa cookies `_ga*`, `_gid`, `_gat*`, `_gcl*`, `_fbp`, `_fbc`.
  Przycisk „Ustawienia cookies” jest w stopce i w polityce prywatności (`data-zgoda`).
  W GTM tagi Google (GA4, Google Ads) korzystają z trybu zgody same. Tagi spoza Google (np. Meta Pixel) uruchamiaj
  wyzwalaczem „Zdarzenie niestandardowe” `zgoda_cookies` z warunkiem `zgoda_marketing` równa się `granted`
  (zmienna warstwy danych). Każde nowe narzędzie trzeba też opisać w polityce prywatności.
- Zdarzenia dla GTM: `track()` w `c.js` wysyła działania także do dataLayer (`DL` w `c.js`): `zapytanie_wyslane`,
  `telefon`, `email`, `dodaj_do_wyceny`, `lista_do_formularza`, `pasek_nowosci_okno`, `pasek_nowosci_przejscie`
  (te same props co w Plausible). Konfiguracja GA4 w kontenerze: tag Google uruchamiany zdarzeniem `zgoda_cookies`
  przy `zgoda_statystyki` = `granted` (raz na stronę), zdarzenia GA4 na regułach z tymi nazwami (`zapytanie_wyslane`
  jako `generate_lead`); wszystkie tagi wymagają zgody `analytics_storage`.
- `img/`: logo, hero, zdjęcia produktów (`besco/`, `pegler/`, `oferta/`, `linie/`), obrazek udostępniania (`og/`).
  Zdjęcia grup produktów mają beż `#F3F1EC` wpisany w plik (miniatury w kafelkach, liście do wyceny i wyszukiwarce).
  Jeśli obok leży plik `<nazwa>-l.webp` (to samo zdjęcie na białym tle, czasem większe), strona produktu pokazuje go zamiast miniatury.
  Strona produktu kładzie zdjęcie na beżowej ramce (`mix-blend-mode: multiply`), więc jego tło musi być białe, inaczej
  w ramce widać drugą, ciemniejszą. Brakujące pliki `-l` tworzy `python3 tools/tlo_produktu.py` (dzieli piksele przez kolor
  tła miniatury), a generator ostrzega, gdy któreś zdjęcie dałoby podwójną ramkę.
  67 grup Gutpress (miedź V i M do wody i gazu, stal węglowa) ma zdjęcia produktowe od Besco zamiast wycinków z katalogu PDF:
  `python3 -I tools/zdjecia_besco.py <rozpakowane paczki zdjęć>` zapisuje miniaturę, wersję `-l` (720 px) i wersję do druku
  w `tools/katalog-pdf/foto/` (800 px); pary plik–grupa (sprawdzone wzrokowo) są w skrypcie.
  Generator dopisuje do każdego adresu zdjęcia `?v=<skrót treści>`, więc podmiana pliku pod tą samą nazwą
  od razu trafia do przeglądarek mimo 7-dniowego cache `/img/*`.
- `pliki/katalog-*.pdf`: katalogi Armatex (Besco 2026, Besco INOX 304 i 316L, Tectite, Kuterlite) składane z danych przez
  `tools/katalog_pdf.py` (niżej, „Katalogi PDF”). Katalog Besco 2026 jest w menu „Oferta → Katalogi”.
- `pliki/instrukcja-montazu-tectite.pdf`: instrukcja montażu Tectite w identyfikacji Armatex (`tools/instrukcja_tectite.py`); link na stronie Tectite, w „Do pobrania” i w poradniku „Tectite czy press?”.
- `assets/`: fonty (Outfit, IBM Plex Mono) i favicony.
- `sitemap.xml`, `robots.txt`, `llms.txt`. `llms.txt` (format llmstxt.org) to streszczenie strony dla asystentów AI
  (ChatGPT, Claude, Perplexity): firma, systemy z liniami i parametrami, poradniki, pytania partnerów i hurtowni, zamawianie.
  Składa go generator z tych samych danych co strony (`SYS`, `ART`, `HOME_FAQ`, `WSP_FAQ`), więc nie edytuj go ręcznie.
- Pytania i odpowiedzi (FAQ): strona główna (`HOME_FAQ`), strony systemów (`faq` w `SYS`), Współpraca (`WSP_FAQ`)
  i poradniki (`ART_FAQ`, sekcja „Najczęstsze pytania” na końcu artykułu). Każda lista trafia też do danych FAQPage
  (`ld_faq()`), więc pytania w danych strukturalnych są zawsze takie same jak na stronie. Odpowiedzi tylko z treści strony.
- `tools/`: generator stron i skrypty danych (niżej).

## Zmiany treści: generator

Strony HTML są generowane, więc zmiany w treści rób w `tools/strony.py` (szablon sekcji:
`tools/szablon-c.html`), nie ręcznie w plikach HTML:

```bash
pip install pillow beautifulsoup4
python3 tools/strony.py
```

`c.css` i `c.js` edytuje się bezpośrednio, a potem uruchamia generator: dopisuje on do linków `?v=<hash treści>`, dzięki czemu Netlify może trzymać te pliki w cache przez rok, a po zmianie przeglądarki pobiorą nową wersję. Generator skraca też tytuły do ok. 60 znaków i opisy do 160.

Dane produktów z oryginalnych katalogów producentów (PDF-y nie są trzymane w repo; pliki w `pliki/` to już katalogi
Armatex składane z tych danych, nie źródła):

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

`tools/katalog_inox.py` dopisuje do `data/besco-2026.json` linie INOX 304 i INOX 316L z oryginalnych katalogów Besco
(INOX 304: `Katalog_INOX_304.pdf`, INOX 316L: oryginalny katalog Besco INOX 316L).
Uruchamiaj go **po** `tools/katalog_besco.py`, bo ten nadpisuje cały plik danych. Katalog 316L ma tekst zamieniony na krzywe,
więc skrypt czyta go przez OCR (`pip install rapidocr_onnxruntime`) i sprawdza numery artykułów względem kodu grupy.
Skrypt czyta oryginalne katalogi Besco, a nie `pliki/katalog-besco-inox-*.pdf`, które są już katalogami Armatex (niżej).

## Katalogi PDF

Wszystkie katalogi w `pliki/` są katalogami Armatex składanymi z danych:
`python3 tools/katalog_pdf.py <katalog>` albo `wszystkie` (`pip install playwright==1.56.0 pymupdf fonttools brotli`).
Katalogi: `besco-2026`, `inox-304`, `inox-316l`, `tectite`, `kuterlite`. Każdy ma okładkę, stronę o katalogu ze spisem
treści (INOX: parametry i grupy; wieloseryjne: tabela serii), strony produktów w dwóch kolumnach (działy, karty ze
zdjęciem i tabelą), panel wyceny i tylną okładkę z kontaktami. Treść każdego katalogu (teksty, parametry serii, atesty,
marka) jest w `KATALOGI` w skrypcie, wygląd w `tools/katalog-pdf/katalog.css` (kolory i fonty jak w `c.css`), logo
marek w `tools/katalog-pdf/`. Podział na strony i spis treści liczy skrypt; jeśli coś się przelewa, przerywa pracę.
Podgląd do innego pliku: `--out x.pdf`. Po zmianie liczby stron lub rozmiaru pliku popraw opisy w `DOCS` i w menu
w `tools/strony.py` (oraz w `tools/en.json`, `tools/uk.json`).

Instrukcję montażu Tectite (`pliki/instrukcja-montazu-tectite.pdf`, 7 stron) składa `python3 tools/instrukcja_tectite.py`
tym samym stylem i drukiem (`drukuj()` w `tools/katalog_pdf.py`, dodatki w `tools/katalog-pdf/instrukcja.css`). Treść
pochodzi z instrukcji Pegler Yorkshire, zdjęcia i rysunki z `tools/katalog-pdf/instrukcja/` (wyjęte z oryginału, małe
zdjęcia powiększone ESRGAN).

Katalogi Gutpress (`pliki/katalog-gutpress-gaz.pdf`, 20 stron, i `pliki/katalog-gutpress-zawory.pdf`, 6 stron) składa
`python3 tools/katalog_gutpress.py gaz` / `zawory`: karty na całą szerokość ze zdjęciem, tabelą zamówień, rysunkiem
technicznym i tabelą wymiarów; wysokości kart mierzy przeglądarka. Dane i obrazy (`tools/katalog-pdf/gutpress-*.json`,
`tools/katalog-pdf/gutpress/`) składa `python3 tools/gutpress_dane.py <katalog gazowy>.pdf <katalog zaworów>.pdf` z polskich
katalogów Besco/Armatex; numery artykułów są jak w tych katalogach (część różni się zapisem od `data/besco-2026.json`).
Strony produktów linii gazowych i zaworów kulowych linkują do tych katalogów (`PDF_INOX` w `tools/strony.py`).

Dane: `tools/katalog-pdf/<katalog>.json`. INOX 304 z warstwy tekstowej katalogu Besco (296 indeksów), INOX 316L
z `data/besco-2026.json` sprawdzony z katalogiem (253). Besco 2026, Tectite i Kuterlite składa
`python3 tools/katalog_dane.py oryginalny-katalog-kuterlite.pdf` z `data/besco-2026.json` i `data/pegler.json`:
Besco 2026 sprawdzony z katalogiem producenta (poprawki w `POPRAWKI_BESCO`), Kuterlite bez serii K600 i K700
(jak na stronie), z wymiarami uciętymi w danych strony odczytanymi z oryginalnego katalogu Kuterlite.
Zdjęcia: `img/besco/*-l.webp` i `img/pegler/`, chyba że w `tools/katalog-pdf/foto/` leży wersja powiększona do druku
(zdjęcia ze strony mają zwykle 100–250 px): `python3 tools/powieksz_zdjecia.py <node_modules> <katalog>...`
(model ESRGAN z pakietu npm `@upscalerjs/esrgan-thick`, instalacja w opisie skryptu). Grupy ze zdjęciami od Besco
mają w `foto/` wersję z `tools/zdjecia_besco.py`, bez powiększania.

## Formularz

Formularz (strona główna i `kontakt.html`) obsługuje **Netlify Forms** (formularz `zapytanie`,
stała `FORM_NAME` w `tools/strony.py`). Netlify wykrywa go przy wdrożeniu po atrybucie `data-netlify`,
zapisuje zgłoszenia w panelu (Forms) i wysyła powiadomienia. Jednorazowo w panelu Netlify:
**Forms → Enable form detection**, potem po wdrożeniu **Forms → zapytanie → Form notifications →
Email notification** na `biuro@armatex.pl`. Temat maila ustawia ukryte pole `subject`.
Po udanym wysłaniu karta formularza zamienia się w potwierdzenie (`formOk` w `c.js`, style `.form--ok`/`.form__ok` w `c.css`):
rysowany znak ✓, adres e-mail, na który odpowiemy (z formularza, wstawiany jako tekst), liczba pozycji z listy do wyceny,
telefon i przycisk „Wyślij kolejne zapytanie”. Fokus przechodzi na tytuł potwierdzenia.
Na kopii w GitHub Pages formularz nie działa (pokazuje komunikat z telefonem i e-mailem).

## Przed startem w wyszukiwarkach

1. **Indeksowanie jest włączone** (strona działa pod armatex.pl). Wyjątek: `404.html` ma `noindex`.
2. Adresy kanoniczne, Open Graph, `sitemap.xml` i dane strukturalne zakładają domenę `https://armatex.pl/`
   (stała `SITE` w generatorze).
3. Godziny otwarcia (`openingHoursSpecification`) i profil LinkedIn (`sameAs`) są w danych `WholesaleStore`. Adres profilu
   (`LINKEDIN` w `tools/strony.py`) jest też w stopce (Kontakt), w sekcji kontaktu i jako przycisk w nagłówku strony „O firmie”. Kolejne profile dopisz do `sameAs`.
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
