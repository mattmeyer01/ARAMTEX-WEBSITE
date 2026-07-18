# Armatex.pl — design brief (Phase 0)

## Design read
Strona dla polskich klientów B2B (hurtownie instalacyjne, wykonawcy, działy zakupów w przemyśle):
rejestr emocjonalny to zaufanie techniczne i konkret. Ma sprzedawać pewność dostawy, nie lifestyle.

## Concept spine
**"Karta katalogowa" (archive/dossier).** Cała strona zachowuje się jak techniczna karta
katalogowa produktu: mono etykiety specyfikacji, cyfry indeksowe, linie miary (hairlines),
motyw pieczęci/atestu. Każda sekcja to kolejna rubryka karty.

## Delivery tier
**cinema** (podniesiony z editorial na życzenie klienta): Lenis + GSAP ScrollTrigger,
przypięte hero z nasuwającymi się sekcjami, kinetyczna typografia per znak/słowo,
scrub zdjęć, liczniki metryk, rysująca się linia procesu, magnetyczne CTA.
Wszystko za bramką prefers-reduced-motion, biblioteki self-hosted w assets/vendor/.

## Locked palette
- Tło / papier: `#F4F2EC` (limestone paper), panele: `#ECE9E0`
- Atrament: `#182226` (głęboki chłodny petrol-ink, nie czysta czerń)
- Akcent (jedyny): **kobalt `#1E44B8`** + ciemny pas kobaltowy `#132A66` (sekcja dokumentów)
- Mosiądz/miedź żyją wyłącznie w fotografii produktowej, nigdy w UI.

Obrona: kobalt to kolor technicznych oznaczeń wody i instalacji; odróżnia Armatex od żółci
Viegi i czerwieni Sanhy. Żadna z zakazanych rodzin (grafit+pomarańcz, dark+neon,
beż+mosiądz, fiolet) nie jest użyta.

## Locked type
**Outfit** (display + body, geometric grotesk) + **IBM Plex Mono** (etykiety spec, cyfry
indeksowe, dane). Para z zatwierdzonej listy. Bez serifów: brand czysto techniczny.

## Tier-1 technique
**B1 — Cutout parallax rig** (wow-catalog). Hero: wycięty mosiężny zawór kulowy (cutout PNG)
unosi się nad wygradowanym tłem magazynowym; 3 warstwy (tło / produkt / mono-adnotacje
wymiarowe) poruszają się w różnym tempie na scroll i subtelnie na kursor.
Obrona: spine "karta katalogowa" chce produktu wyjętego z tła jak na rysunku technicznym,
z adnotacjami, które reagują na użytkownika. Reduced-motion: statyczna złożona kompozycja.
Mobile: parallax kursora wyłączony, zostaje delikatny parallax scrollowy.

## Section plan (7 sekcji, 6 rodzin, bez powtórzeń obok siebie)
1. **Hero** — image-as-canvas + cutout parallax; tekst dolny-lewy. (rodzina: full-bleed canvas)
2. **Katalog produktów** — gapless bento 6 kafli kategorii, zdjęcia + cyfry indeksowe. (bento)
3. **Zaplecze / liczby** — oversized metrics strip + wąska kolumna tekstu. (metrics strip)
4. **Proces zamówienia** — 3 kroki poziomo z generowanymi ikonami, linia trasy. (horizontal steps)
5. **Baza dokumentów** — pełny pas kobaltowy (material switch), split treść + wizual dokumentów;
   dostęp tylko na zapytanie. (color-blocked split)
6. **Dla kogo** — naprzemienny blok edytorski: hurtownie / wykonawcy / przemysł. (editorial rows)
7. **Kontakt** — panel formularza w ramie + dane teleadresowe. (framed form panel)

Eyebrow budget: ceil(7/3) = 3 → tylko sekcje 2 ("Katalog"), 5 ("Baza dokumentów"), 7 ("Kontakt").

## Asset plan (Higgsfield)
- Hero: fotografia magazynu armatury (grade petrol-ink) + cutout mosiężnego zaworu (remove_background), 2 kandydaci.
- 6 zdjęć kategorii: zawory kulowe; złączki mosiężne gwintowane; systemy zaprasowywane;
  armatura grzewcza; rury PP-R/PEX; uszczelnienia i akcesoria. Jedna spójna gradacja.
- Płyty sekcyjne: tekstura papieru technicznego + kobaltowa płyta dokumentowa.
- Ikony: 1 arkusz 8 glifów, kreska 2px, ink na jednolitym tle → pocięte + remove_background.
- Logo/monogram: znak "A" z motywem gwintu/przekroju rury, wersje ink i inverse.
- OG image 1200×630 + head kit (favicony, apple-touch, manifest).
- Wizual sekcji dokumentów: stos kart katalogowych z pieczęcią atestu.

## CTA inventory (bespoke chrome, zero wspólnych klas)
- **"Zapytaj o ofertę"** (hero, primary): blok w ramie, wypełnia się kobaltem na hover
  (racjonowany garment, użyty tylko raz). W nav ta sama etykieta jako kompaktowy link
  z przesuwającą się hairline.
- **"Przejdź do katalogu"** (hero secondary / sekcja 2): tekst-link, strzałka jedzie po
  narysowanej ścieżce rury (route path).
- **Kafle kategorii**: cały kafel to CTA; hover = zmiana gradacji zdjęcia + wysuwająca się
  cyfra indeksowa.
- **"Poproś o dostęp"** (dokumenty): pieczęć/stempel; :active fizycznie odbija (skew +
  przesunięcie tekstury), motyw pieczęci atestu.
- **"Wyślij zapytanie"** (submit formularza): narożne klamry celownika domykają się wokół
  etykiety na hover/focus.

## Corner / border language
Wszystko ostre (radius 0), hairline 1px w kolorze ink/20. Głębia przez JEDNĄ zmianę
powierzchni (papier → panel), nigdy karta-w-karcie.

## Second-read moment
Jedna zmiana materiału: pełny kobaltowy pas sekcji "Baza dokumentów" na jasnej stronie.

## Anti-convergence ledger
Pierwszy build w tym czacie. Wszystkie osie wywiedzione ze świata materiałów firmy:
mosiądz, gwint, uszczelka, karta katalogowa, pieczęć atestu, regał magazynowy.
(1) paleta: limestone+kobalt; (2) typografia: Outfit+IBM Plex Mono; (3) hero: image-as-canvas
z cutoutem, NIE lewy-tekst/prawy-obraz; (4) Tier-1: B1; (5) garmenty CTA: rama-fill,
ścieżka rury, stempel, celownik, kafel-grade; (6) narożniki: ostre + hairline.

## Uwagi wykonawcze
- Konwersja: formularz kontaktowy (imię, firma, e-mail, telefon, treść, zgoda), telefon i
  e-mail klikalne w hero/nav/stopce, CTA w każdej sekcji prowadzi do formularza lub katalogu.
- Baza dokumentów NIE jest publiczna: sekcja komunikuje zawartość (atesty PZH, DoP, karty
  katalogowe) i konwertuje przez "Poproś o dostęp" (prefill formularza).
- Strona statyczna (HTML/CSS/JS) w repo GitHub; formularz przez endpoint FormSubmit na
  adres kontaktowy, z fallbackiem mailto.
- Zero em-dash w widocznych tekstach. Jedna etykieta na intencję CTA.
