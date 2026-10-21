# Marketing Armatex z Claude Code

Jeden temat tygodniowo, opracowany na wszystkie kanały: blog, LinkedIn, Facebook, Instagram, wizytówka Google,
pomysł na film YouTube; raz w miesiącu newsletter. Szkice pisze Claude, publikację zatwierdza człowiek.

## Jak używać

Otwórz Claude Code w tym repozytorium i napisz, np.:

- „Zrób pakiet na ten tydzień” (temat z `plan.md` i szkice na wszystkie kanały),
- „Zrób pakiet o INOX 304”,
- „Post na LinkedIn o profilu V i M”,
- „Pomysł na film na YouTube”,
- „Newsletter za listopad”,
- „Raport z marketingu za ostatni miesiąc”.

Proces opisuje skill `.claude/skills/omnichannel/SKILL.md`. Agenci kanałów są w `.claude/agents/`.

## Pliki

| Plik | Co zawiera |
|---|---|
| `marka.md` | kim jesteśmy, do kogo mówimy, ton, zasady faktów, linki; wspólne dla wszystkich kanałów |
| `ustawienia.md` | tryb (szkice / harmonogram), narzędzia, e-mail zespołu na pomysły YouTube |
| `plan.md` | bank tematów i rejestr zrobionych pakietów |
| `szkice/` | pakiety tygodniowe (`<data>-<temat>/`) i newslettery |
| `youtube/pomysly.md` | pomysły na filmy wysłane do zespołu i decyzje (tak / nie / później) |

## Kanały i agenci

| Kanał | Agent | Co robi |
|---|---|---|
| Blog | `redaktor-poradnikow` | nowy poradnik przez `art(...)` w `tools/strony.py` |
| LinkedIn | `linkedin` | 2 posty B2B tygodniowo |
| Facebook | `facebook` | 2 posty + propozycja wpisu do grup (wklejana ręcznie) |
| Instagram | `instagram` | karuzela, opis, brief grafiki, opcjonalnie reel |
| Wizytówka Google | `wizytowka-google` | 1 wpis tygodniowo, szkice odpowiedzi na opinie |
| YouTube | `youtube` | pomysł na film e-mailem do zespołu; po „TAK” scenariusz, tytuł i opis |
| Newsletter | `newsletter` | wydanie miesięczne z treści z pakietów |

## Zasady

- Nic nie jest publikowane ani wysyłane bez akceptacji człowieka.
- Fakty tylko z danych produktów i istniejących stron (`marka.md`, „Fakty: zasada żelazna”).
- Katalogi `marketing/` i `.claude/` nie trafiają na stronę (wycinane przy publikacji na GitHub Pages,
  na Netlify zablokowane w `_redirects`).
