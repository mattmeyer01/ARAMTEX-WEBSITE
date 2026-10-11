"""Składa „Instrukcję montażu Tectite” w identyfikacji Armatex → pliki/instrukcja-montazu-tectite.pdf.

Użycie:
    pip install playwright==1.56.0 pymupdf fonttools brotli
    python3 tools/instrukcja_tectite.py               # → pliki/instrukcja-montazu-tectite.pdf
    python3 tools/instrukcja_tectite.py --out x.pdf   # podgląd

Treść: instrukcja montażu Tectite od Pegler Yorkshire (dotychczasowy plik), przepisana i uporządkowana; gwarancja
jak na stronie (tools/strony.py, FAQ Tectite). Zdjęcia i rysunki: tools/katalog-pdf/instrukcja/ (wyjęte z oryginału;
małe zdjęcia powiększone 4× ESRGAN, rysunki wektorowe wycięte w 300 dpi, przekroje złożone z kawałków).
Wygląd, nagłówki, okładki i druk wspólne z katalogami (tools/katalog_pdf.py, tools/katalog-pdf/katalog.css).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import katalog_pdf as kp  # noqa: E402

OUT = os.path.join(kp.ROOT, 'pliki', 'instrukcja-montazu-tectite.pdf')
TITLE = 'Instrukcja montażu Tectite'


def im(name):
    return kp.asset(f'instrukcja/{name}.jpg')


def fig(name, cap='', no='', cls=''):
    badge = f'<span class="no">{no}</span>' if no else ''
    capt = f'<figcaption>{cap}</figcaption>' if cap else ''
    return f'<figure class="{cls}"><div class="fr">{badge}<img src="{im(name)}" alt=""></div>{capt}</figure>'


def page(no, body):
    return f'<section class="page ins">{kp.head()}<div class="body">{body}</div>{kp.foot(no)}</section>'


def table(head, rows, cls=''):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="it {cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def callouts(items):
    return '<ol class="callouts">' + ''.join(f'<li><span class="cn">{n}</span><div><b>{t}</b> – {d}</div></li>' for n, t, d in items) + '</ol>'


def cutaway(name, marks):
    """Przekrój z numerami w miejscach, na które wskazywały strzałki w oryginale (ułamki szerokości i wysokości)."""
    dots = ''.join(f'<span class="mk" style="left:{x * 100:.1f}%;top:{y * 100:.1f}%">{n}</span>' for n, x, y in marks)
    return f'<div class="cut"><img src="{im(name)}" alt="">{dots}</div>'


def steps(items):
    return '<div class="steps">' + ''.join(
        f'<div class="st"><div class="ci"><img src="{im(f"krok-{n}")}" alt=""><span>{n}</span></div><h4>{t}</h4><p>{d}</p></div>'
        for n, t, d in items) + '</div>'


DEPTH = [  # głębokość osadzenia rury w złączce (mm): średnica DN → głębokość
    ('Tectite Sprint', [('10', '15'), ('15', '16'), ('22', '18'), ('28', '20')]),
    ('Tectite Classic', [('10–18', '23'), ('22', '27'), ('28', '31')]),
    ('Tectite Pro i 316', [('10–18', '23'), ('22', '27'), ('28', '31'), ('35', '57'), ('42', '62'), ('54', '68')]),
    ('Tectite Carbon', [('15', '28'), ('18', '28'), ('22', '30'), ('28', '32'), ('35', '40'), ('42', '42'), ('54', '45')]),
]


def depth_table():
    cols = ''.join(f'<div class="dc"><h5>{n}</h5><table class="it"><thead><tr><th>DN</th><th>Głębokość</th></tr></thead><tbody>'
                   + ''.join(f'<tr><td>{a} mm</td><td>{b} mm</td></tr>' for a, b in rows) + '</tbody></table></div>'
                   for n, rows in DEPTH)
    return f'<div class="depth">{cols}</div>'


def build_html(faces):
    logo_l = f'file://{kp.ROOT}/assets/img/logo-light.png'
    cover = f'''<section class="page cover">
  <div class="top">
    {kp.stripes(595.28, 478, [(330, -10, 280, 70, kp.RED), (430, 60, 488, 70, kp.RED2)], 's-cover')}
    <img class="logo" src="{logo_l}" alt="Armatex">
    <span class="tag">Instrukcja montażu</span>
    <div class="title">
      <span class="eyebrow">Pegler Yorkshire · system push-fit</span>
      <h1>Instrukcja montażu<b>Tectite</b></h1>
      <p>„Wciśnij i zapomnij” · Sprint · Classic · Pro · 316 · Carbon</p>
    </div>
  </div>
  <div class="hero ins-hero"><img src="{im('przekroj-zlaczka')}" alt=""></div>
  <div class="facts">
    <div><b>Na wcisk</b><span>bez palnika i skomplikowanych narzędzi</span></div>
    <div><b>3 kroki</b><span>zaznacz, wciśnij, sprawdź</span></div>
    <div><b>25 lat</b><span>gwarancji producenta</span></div>
    <div class="pzh"><img class="wide" src="{kp.asset('tectite.png')}" alt="Tectite"></div>
  </div>
  <footer><b>armatex.pl</b><span class="brand">Producent{kp.brand_logo()}</span></footer>
</section>'''

    p2 = page(2, f'''
  <span class="eyebrow">System Tectite</span>
  <h2 class="big">Połączenie na wcisk w trzech krokach</h2>
  <p class="lead">Złączki Tectite służą do szybkiego wykonywania instalacji wodnych i grzewczych bez palnika i skomplikowanych
  narzędzi. Według producenta montaż jest do 5 razy szybszy niż w tradycyjnym systemie skręcanym i pozwala zaoszczędzić
  do 70% kosztów montażu. Producent daje 25 lat gwarancji na Tectite Sprint, Classic, Pro i 316 z rurami innych
  producentów oraz 30 lat z rurami Yorkshire i rurami rekomendowanymi, jeśli montaż jest zgodny z instrukcją.</p>
  <img class="lines" src="{im('logo-linie')}" alt="Tectite Sprint, Classic, Pro, 316, Carbon">
  <h3 class="h3">Wykonywanie połączenia</h3>
  <p>Rura musi być całkowicie wciśnięta do środka złączki, aż do wewnętrznego punktu oporowego.</p>
  <div class="trio">
    <div>{fig('polaczenie-1', no='1')}<h4>Zaznacz głębokość</h4><p>Zaznacz markerem na rurze głębokość wsunięcia
      (tabela 1) – markerem głębokości albo zwykłą taśmą mierniczą. Sprawdź, czy wnętrze złączki jest czyste: na o-ringach
      nie może być piasku ani opiłków.</p></div>
    <div>{fig('polaczenie-2', no='2')}<h4>Wciśnij do oporu</h4><p>Wciśnij pewnie rurę w złączkę, wykonując lekki obrót,
      aż do wewnętrznego punktu oporowego.</p></div>
    <div>{fig('polaczenie-4', no='3')}<h4>Sprawdź połączenie</h4><p>Znak na rurze musi pokryć się z krawędzią złączki.
      Pociągnij lekko za rurę, aby upewnić się, że połączenie jest pewne.</p></div>
  </div>
  <div class="note"><b>Próba szczelności.</b> Po wykonaniu instalacji zalecamy próbę ciśnieniem 1,5 razy większym niż
  planowane ciśnienie robocze.</div>
  <h3 class="h3">Tabela 1. Głębokość osadzenia rury w złączce</h3>
  {depth_table()}''')

    p3 = page(3, f'''
  <span class="eyebrow">Przed montażem</span>
  <h2 class="big">Uwagi montażowe i przygotowanie rury</h2>
  <ul class="ticks">
    <li>Montaż całej rodziny Tectite przebiega praktycznie tak samo; różnice, np. tulejka korygująca do PEX, są opisane niżej.</li>
    <li>Aby chronić wewnętrzne uszczelnienia, wyjmuj złączki z opakowania bezpośrednio przed wykonaniem połączenia.</li>
    <li>Rura powinna dać się całkowicie wcisnąć ręką. Jeśli potrzebna jest duża siła, sprawdź, czy koniec rury nie jest
      uszkodzony (owalność, ostre krawędzie).</li>
    <li>Złączki są wrażliwe na bardzo wysokie temperatury. Przy łączeniu z instalacją lutowaną poczekaj, aż ostygnie –
      inaczej można uszkodzić niemetalowe części złączki.</li>
    <li>Malowanie: złączki Tectite można malować farbami wodnymi; farby olejne i rozpuszczalnikowe są niedopuszczalne.</li>
    <li>Podłączenie do bojlera: rury PEX nie podłączaj bezpośrednio do bojlera ani innego źródła ciepła – wykonaj je rurą
      miedzianą o długości co najmniej 1 m.</li>
  </ul>
  <h3 class="h3">Cięcie</h3>
  <p>Końce rur muszą być czyste, okrągłe (owalność jest niedopuszczalna), bez rys i zadziorów. Rury miedziane tnij
  dobrej jakości przycinakiem rolkowym z ostrymi rolkami, rury PEX – dobrej jakości nożycami do rur.</p>
  <div class="row2">{fig('ciecie-miedz', 'Przycinanie rur miedzianych', '1a')}{fig('ciecie-pex', 'Przycinanie rur PEX', '1b')}</div>
  <h3 class="h3">Gratowanie</h3>
  <p>Po cięciu ogratuj końce rur, aby usunąć wszystkie zadziory. Najlepiej wykonaj małą fazę na zewnętrznej krawędzi –
  pilnikiem, papierem ściernym albo przyrządem T110 (Tectite Classic) lub T115 (Tectite Sprint). Po szlifowaniu oczyść
  rurę z opiłków.</p>
  <div class="row4">{fig('rura-przed', 'Rura przed szlifowaniem')}{fig('rura-po', 'Rura po szlifowaniu')}
    {fig('gratowanie-pilnik', 'Gratowanie pilnikiem', '2')}{fig('krawedz', 'Właściwie przygotowana krawędź: faza 30°, 1 mm')}</div>''')

    p4 = page(4, f'''
  <span class="eyebrow">Przyrządy i tulejki</span>
  <h2 class="big">Przyrządy T110 i T115, tulejka do PEX</h2>
  <p class="lead">Przyrządy T110 (Tectite Classic) i T115 (Tectite Sprint) spełniają trzy funkcje: pozwalają określić średnicę
  rury, oszlifować jej koniec i oznaczyć głębokość osadzenia w złączce.</p>
  <div class="split">{fig('t110-gratowanie', no='3', cls='side')}<div><h4>Gratowanie przyrządem</h4><p>Włóż rurę do
    odpowiedniego gniazda, wciśnij do oporu i wykonaj kilka ruchów obrotowych. Krawędzie zostaną właściwie przygotowane.
    Oczyść rurę z opiłków.</p></div></div>
  <div class="split">{fig('t110-znaczenie', no='4', cls='side')}<div><h4>Oznaczanie głębokości osadzenia</h4><p>Włóż rurę
    do odpowiedniego gniazda, wciśnij do oporu i zaznacz markerem głębokość osadzenia. Znak musi się później pokrywać
    z krawędzią złączki.</p></div></div>
  <div class="split">{fig('tulejka', no='5', cls='side')}<div><h4>Tulejka korygująca do rur PEX</h4><p>Przy rurach PEX zawsze
    stosuj tulejkę korygującą. Koryguje ona błędy okrągłości rury (owalizację po cięciu nożycami) i zwiększa jej
    wytrzymałość. Używaj tulejki w rozmiarze zalecanym przez producenta rury i wciśnij ją w rurę całkowicie, zanim
    wykonasz połączenie ze złączką.</p></div></div>
  <h3 class="h3">Uwagi dla projektantów i wykonawców</h3>
  <h4>Ruchy termiczne</h4>
  <p>Instalację kotwicz tak, aby umożliwić ruch termiczny (rozszerzanie pod wpływem temperatury). Pętle i kompensatory
  pozwalają uniknąć problemów. Proste techniki kompensacji:</p>
  <div class="row4">{fig('kompensacja-1', 'Kompensator U')}{fig('kompensacja-2', 'Kompensator Z')}{fig('kompensacja-3', 'Pętle na odejściach')}
    {fig('kompensacja-4', 'Pętla – tylko dla rur 10 mm')}</div>
  <h4>Czyszczenie chemiczne</h4>
  <p>Niektóre kontrakty wymagają czyszczenia lub przepłukania instalacji środkami chemicznymi przed pełnym uruchomieniem.
  System Tectite jest kompatybilny z szeroką gamą takich produktów – zapytaj nas o szczegóły.</p>''')

    p5 = page(5, f'''
  <span class="eyebrow">Projektowanie</span>
  <h2 class="big">Luzy montażowe</h2>
  <p class="lead">Zostaw miejsce na montaż i demontaż połączeń. Odpowiednie odstępy pozwalają użyć przyrządu demontującego
  (Tectite Classic). Zachowaj też odległości od ścian i zakończeń rur po przejściu przez ścianę.</p>
  <div class="row3">{fig('odstep-1', 'Odstęp między złączkami')}{fig('odstep-2', 'Odległość złączki od ściany')}{fig('odstep-3', 'Koniec rury za ścianą')}</div>
  <div class="row2 tabs">
    <div><h4>Tectite Sprint i Carbon (niedemontowalne)</h4>{table(['Średnica DN', 'Min. odstęp między złączkami', 'Min. odległość od ściany'],
      [('10 mm', '5 mm', '20 mm'), ('15 mm', '5 mm', '21 mm'), ('22 mm', '5 mm', '23 mm'), ('28 mm', '5 mm', '25 mm')])}</div>
    <div><h4>Tectite Classic, Pro i 316 (demontowalne)</h4>{table(['Średnica DN', 'Min. odstęp między złączkami', 'Min. odległość od ściany'],
      [('10 mm', '10 mm', '40 mm'), ('12 mm', '10 mm', '40 mm'), ('15 mm', '10 mm', '40 mm'), ('22 mm', '10 mm', '40 mm'), ('28 mm', '10 mm', '50 mm')])}</div>
  </div>
  <h3 class="h3">Budowa złączki Tectite</h3>
  <p>Złączki Tectite są demontowalne, mają smukły profil i pasują do większości rur.</p>
  {cutaway('przekroj-zlaczka', [(1, .272, .31), (2, .34, .31), (3, .05, .627), (4, .418, .605)])}
  {callouts([(1, 'O-ring', 'wstępnie przesmarowane uszczelnienie z EPDM zapewnia pewne uszczelnienie między rurą a złączką.'),
             (2, 'Pierścień chwytający', 'ze stali nierdzewnej, pewnie mocuje rury z różnych materiałów.'),
             (3, 'Metalowy korpus', 'z mosiądzu DZR: sztywne, mocne i pewne połączenie.'),
             (4, 'Demontowalność', 'złączki Tectite Classic są w pełni demontowalne, co pozwala zmieniać instalację, serwisować ją '
                                   'i naprawiać. Aby zdemontować złączkę, wciśnij pierścień polimerowy specjalnym klipsem lub szczypcami.')])}
  <div class="compat"><span class="eyebrow">Kompatybilne z</span>{fig('rura-tectite', 'rury Tectite')}{fig('rura-miedz', 'rury miedziane')}{fig('rura-pex', 'rury PEX i PB')}</div>''')

    p6 = page(6, f'''
  <span class="eyebrow">Rury Tectite</span>
  <h2 class="big">Rury Tectite i tulejki TectSEAL 3PS</h2>
  <p class="lead">Rura Tectite ma integralną warstwę aluminium, dzięki której zachowuje kształt nadany przez instalatora
  (łuki 90° itp.). Razem z demontowalnymi złączkami mosiężnymi tworzy kompletny system.</p>
  {cutaway('przekroj-rura', [(5, 0.447, 0.208), (6, 0.878, 0.12), (7, 0.979, 0.12), (8, 0.322, 0.475), (9, 0.578, 0.524), (10, 0.949, 0.524)])}
  {callouts([(5, 'Adhezja', 'połączenie warstw PE-Xc i aluminium znacznie ogranicza rozszerzalność termiczną.'),
             (6, 'Wewnętrzny O-ring', 'do wprowadzenia w rurę; z EPDM, wstępnie pokryty środkiem smarnym.'),
             (7, 'Zewnętrzny O-ring', 'do wprowadzenia w złączkę; z EPDM, wstępnie pokryty środkiem smarnym.'),
             (8, 'PE-Xc', 'wewnętrzna i zewnętrzna warstwa pozwala stosować rurę w instalacjach wody pitnej, grzewczych i niskotemperaturowych.'),
             (9, 'Warstwa aluminium', 'zapewnia rurze unikalne właściwości fizyczne i wysoką jakość.'),
             (10, 'Tulejka centrująca', 'ze sztywnego, mocnego materiału Fortron PPS zapewnia pewne połączenie.')])}
  <div class="warn">Rury Tectite – wyłącznie z demontowalnymi złączkami Tectite i tulejkami TectSEAL 3PS.</div>
  <h3 class="h3">Montaż rury Tectite w sześciu krokach</h3>
  {steps([(1, 'Cięcie', 'Utnij rurę przycinarką ręczną dobrej jakości, zapewniającą proste cięcie. Rura musi być czysta i nieuszkodzona.'),
          (2, 'Kalibrowanie', 'Narzędziem kalibrującym Tectite wyrównaj, oczyść i sfazuj krawędź rury. Kalibrowanie koryguje owalność po cięciu.'),
          (3, 'Centrowanie', 'Wciśnij tulejkę TectSEAL 3PS, aż kołnierzyk oprze się o krawędź rury. Wcześniej usuń z rury opiłki.'),
          (4, 'Pomiar', 'Zmierz głębokość wsunięcia i wyraźnie oznacz ją na rurze (także narzędziem kalibrująco-gratująco-oznaczającym Tectite).'),
          (5, 'Podłączanie', 'Wciśnij mocno rurę w złączkę, aż znacznik zrówna się z pierścieniem złączki. Lekki obrót ułatwia montaż.'),
          (6, 'Sprawdzanie', 'Pociągnij rurę do tyłu, aby sprawdzić połączenie. Złączki Tectite pozwalają na obrót połączonej rury.')])}''')

    b = kp.K['brand']
    back = f'''<section class="page back">
  {kp.stripes(595.28, 841.89, [(485, 600, 860, 70, kp.RED), (400, 600, 860, 70, kp.RED2)], 's-back')}
  <img class="logo" src="{logo_l}" alt="Armatex">
  <div class="cta">
    <span class="eyebrow">Zamówienia i wyceny</span>
    <h2>Złączki, rury i narzędzia<br>Tectite od Armatex</h2>
    <p>Pełną ofertę Tectite – złączki Classic, Pro i 316, zawory na wcisk i akcesoria Tec-Tools – znajdziesz w katalogu
    Tectite i na armatex.pl. Wyślij listę indeksów, odpowiemy z ceną i terminem.</p>
  </div>
  <div class="people">
    <div><span class="label">Biuro</span><b>513 191 502</b><a>biuro@armatex.pl</a><p>ul. Składowa 3a, 10-421 Olsztyn<br>pn–pt 7:00–18:00</p></div>
    <div><span class="label">Sprzedaż</span><b>798 807 106</b><a>piotr@armatex.pl</a><p>Piotr Stelmach</p></div>
    <div><span class="label">Magazyn</span><b>512 945 936</b><a>martyna@armatex.pl</a><p>Martyna Zielińska</p></div>
  </div>
  <div class="web"><b>armatex.pl</b><span>Od 1991 roku na rynku instalacyjnym</span></div>
  <div class="dist"><span>{b["dist"]}</span>{kp.brand_logo()}</div>
  <footer>
    <span>P.H.U. ARMATEX Sp. J. A. J. Bunda · siedziba: ul. Siewna 24, 10-831 Olsztyn · NIP 7393814110 · KRS 0000371628 · REGON 280563743</span>
    <span>Instrukcja według materiałów producenta (Pegler Yorkshire). Montaż wykonuj zgodnie z aktualną instrukcją producenta.</span>
  </footer>
</section>'''

    css = faces + ''.join(open(os.path.join(kp.DIR, f), encoding='utf-8').read() for f in ('katalog.css', 'instrukcja.css')).replace('{ROOT}', kp.ROOT)
    return (f'<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>{TITLE}</title><style>{css}</style></head>'
            f'<body class="instrukcja">{cover}{p2}{p3}{p4}{p5}{p6}{back}</body></html>')


def main():
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else OUT
    kp.K = dict(header=TITLE, head_logo='tectite.png', brand=kp.PEGLER)
    n = kp.drukuj(build_html, out, 'instrukcja', dict(title=f'{TITLE} – Armatex', subject='Montaż złączek na wcisk Tectite krok po kroku',
                                                      keywords='Tectite, instrukcja montażu, push-fit, Pegler Yorkshire, Armatex'))
    print(f'{out}: {n} stron')


if __name__ == '__main__':
    main()
