# Armatex.pl — strona B2B

Statyczna, konwersyjna strona dla dystrybutora armatury instalacyjnej (klienci B2B:
hurtownie, wykonawcy, przemysł). Bez procesu budowania: całość to HTML + CSS + JS,
hostowalna na dowolnym serwerze statycznym (GitHub Pages, Cloudflare Pages, S3, FTP).

## Struktura

- `index.html` — strona główna: hero z parallaxą produktu, katalog (6 grup), zaplecze
  magazynowe, proces zamówienia, baza dokumentów (dostęp na zapytanie), sekcje "dla kogo"
  i kontakt z formularzem.
- `katalog.html` — pełny katalog: 6 grup asortymentowych z listami pozycji i CTA
  zapytania ofertowego per grupa.
- `css/main.css`, `js/main.js` — style i interakcje (parallax, nawigacja, walidacja
  i wysyłka formularza, prefill tematu z parametru `?temat=`).
- `assets/fonts/` — samodzielnie hostowane fonty (Outfit, IBM Plex Mono).
- `assets/img/` — favicony i ikony wygenerowane z monogramu marki.
- `design-brief.md`, `refs/boards.md` — brief projektowy i boardy z generatora.

## Ważne przed startem produkcyjnym

1. **Dane kontaktowe są przykładowe.** Telefon `+48 22 300 40 50`, adres
   `ul. Przemysłowa 12, Pruszków` i e-mail `biuro@armatex.pl` należy podmienić na
   prawdziwe (występują w: `index.html`, `katalog.html`, `js/main.js`).
2. **Formularz** wysyła przez [FormSubmit](https://formsubmit.co) na adres
   `contact@matmeyer.com` (miejsca: atrybut `action` w `index.html` oraz URL w
   `js/main.js`). Pierwsza wysyłka wymaga potwierdzenia aktywacyjnego z FormSubmit.
   Docelowo można podmienić na własny endpoint / CRM.
3. **Zdjęcia** są linkowane z CDN generatora Higgsfield (pełna lista w
   `refs/boards.md`). Rekomendacja: pobrać je i przenieść do `assets/img/`,
   a ścieżki podmienić, żeby uniezależnić się od zewnętrznego CDN.
4. **Metryki oferty** (5 000 pozycji, wysyłka 24 h, wycena 1 dzień) to założenia
   ofertowe. Zweryfikuj przed publikacją.
