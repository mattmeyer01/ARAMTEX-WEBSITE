# Wskazówki dla Claude

Opis projektu, struktura i narzędzia: `README.md`. Rozmawiamy po polsku.

## Publikacja zmian (stała zgoda właściciela)

Produkcja (armatex.pl, Netlify) budowana jest z gałęzi `claude/armatex-website-x62v00`. Zmiany są widoczne na stronie
dopiero po scaleniu pull requesta do tej gałęzi.

Właściciel strony zgodził się na stałe, żeby Claude scalał swoje pull requesty sam, bez pytania:

1. Po wypchnięciu zmian utwórz pull request do `claude/armatex-website-x62v00`.
2. Poczekaj na status `netlify/armatex/deploy-preview` dla ostatniego commita. Scal pull request (metoda `merge`)
   tylko wtedy, gdy podgląd zbudował się poprawnie (`success`). Gdy jest błąd, napraw go albo zgłoś, nie scalaj.
3. Po scaleniu sprawdź na https://armatex.pl, że nowa wersja jest opublikowana (np. nowy `?v=` zmienionego zdjęcia),
   i napisz, co weszło na stronę.

Zgoda obejmuje tylko pull requesty Claude z jego własnymi zmianami, o które poproszono w rozmowie.

## Przy przebudowie stron

- Po zmianach w danych, zdjęciach lub `tools/strony.py` uruchom `python3 tools/strony.py`.
- Generator wpisuje dzisiejszą datę do danych Article poradników i do `sitemap.xml`. Jeśli treść poradnika się nie
  zmieniła, cofnij pliki, w których zmieniła się tylko data, żeby nie przestawiać dat publikacji.
- Zdjęcia od Besco: `tools/zdjecia_besco.py` (opis w skrypcie i w README). Nowe pary plik–grupa sprawdzaj wzrokowo.
