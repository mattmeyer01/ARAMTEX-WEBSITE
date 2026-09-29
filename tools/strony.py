import re
from urllib.parse import quote
from PIL import Image
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
OUT=R
SRC=open(R+'tools/szablon-c.html',encoding='utf-8').read()
def frag(start,end):
    a=SRC.index(start); b=SRC.index(end,a)+len(end); return SRC[a:b]
def img(n, alt, cls=''):
    w,h=Image.open(f'{R}img/oferta/{n}.webp').size
    return f'<img src="../img/oferta/{n}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"{cls}>'
def ask(t): return 'kontakt.html?temat='+quote(t)+'#formularz'
TEL='<a href="tel:+48513191502">513 191 502</a>'

SYS=[
 dict(slug='zlaczki-zaciskane-press',name='Złączki zaciskane',h1='Złączki zaciskane press Besco',seotitle='Złączki zaciskane press Besco dla hurtowni | Armatex',metadesc='Złączki zaciskane (press) Besco: miedź V i M, linie do gazu, stal węglowa i zawory kulowe. 1 043 indeksy, 12–108 mm, dostawy do hurtowni w całej Polsce.',tab='Zaciskane',brand='Besco',cnt='1 043',cntw='1 043 indeksy',sizes='12–108 mm',
  title='Złączki i zawory zaciskane',
  short='Miedź press w profilach V i M, linie gazowe, stal węglowa i zawory kulowe press.',
  desc='Miedziane systemy press (złączki zaprasowywane) w profilach V i M, serie do gazu, press ze stali węglowej oraz zawory kulowe. Miedź według EN 1254-7.',
  who='Firmy instalacyjne z zaciskarkami: kotłownie, piony i przyłącza w budownictwie wielorodzinnym i obiektach, instalacje gazowe.',
  arg='Profil M można zaciskać szczęką V w zakresie DN12–28, więc jeden stan magazynowy obsłuży klientów z oboma typami szczęk.',
  pics=[('besco-press-v','Miedziany trójnik press'),('besco-gaz','Trójnik press do gazu z żółtym oznaczeniem'),('besco-stal','Trójnik press ze stali węglowej')],
  seria='cu-press-water-v,cu-press-water-m,cu-press-gas-v,cu-press-gas-m,steel-press-m,press-ball-valve',
  src='katalog Besco 2026',
  lines=[('Miedź press, profil V','Besco','cu-press-water-v','12–54 mm','woda pitna, CO, przemysł','16 bar',['DVGW','KIWA','WRAS','RISE'],'257','linie/besco-press-v'),
   ('Miedź press, profil M','Besco','cu-press-water-m','12–108 mm','woda pitna, CO, przemysł','16 bar',['DVGW','WRAS','RISE'],'294','linie/besco-press-m'),
   ('Miedź press do gazu, V i M','Besco','cu-press-gas-v,cu-press-gas-m','15–35 mm','gaz ziemny, LPG','5 bar',['DVGW','INiG'],'211','linie/besco-gaz'),
   ('Stal węglowa press, profil M','Besco','steel-press-m','12–108 mm','CO w obiegu zamkniętym, sprężone powietrze','16 bar',[],'256','linie/besco-stal'),
   ('Zawory kulowe press, kontur V i M','Besco','press-ball-valve','15–54 mm','woda, CO','16 bar',['DVGW','WRAS'],'25','linie/besco-zawor')],
  faq=[('Czym różni się profil V od M?','To kształt końcówki press i szczęki zaciskarki. Miedź Besco jest w obu profilach (V 12–54 mm, M 12–108 mm), stal węglowa w profilu M. Złączki w profilu M można zaciskać także szczęką V w zakresie DN12–28.'),
   ('Które złączki nadają się do gazu?','Linie GP Gas w profilu V i M: średnice 15–35 mm, do 5 bar, od −20 do 70 °C, norma EN 1254-7, atesty DVGW i INiG. Do instalacji gazowych nie stosuje się złączek z linii wodnych.'),
   ('Do czego służy stal węglowa press?','Do zamkniętych instalacji grzewczych i sprężonego powietrza. Profil M, średnice 12–108 mm, do 16 bar, od −10 do 110 °C.'),
   ('Jakie aprobaty mają złączki miedziane press?','Profil V: DVGW, KIWA, WRAS i RISE. Profil M: DVGW, WRAS i RISE. Linie gazowe: DVGW i INiG. Wszystkie według EN 1254-7.'),
   ('Jakie zawory kulowe są w systemie?','Zawory kulowe press × press i press × GW w konturach V i M, 15–54 mm, także z przedłużonym trzpieniem. Do 16 bar, od −10 do 110 °C, aprobaty DVGW i WRAS.')]),
 dict(slug='zlaczki-na-wcisk-tectite',name='Złączki na wcisk',h1='Złączki na wcisk Tectite',seotitle='Złączki na wcisk Tectite (push-fit) dla hurtowni | Armatex',metadesc='Złączki i zawory na wcisk (push-fit) Pegler Yorkshire Tectite: Classic, Pro, 316 i Carbon, 10–54 mm. Około 530 indeksów, dostawy do hurtowni w całej Polsce.',tab='Na wcisk',brand='Pegler Yorkshire',cnt='ok. 530',cntw='ok. 530 indeksów',sizes='10–54 mm',
  title='Złączki i zawory na wcisk Tectite',
  short='Tectite Classic, Pro, 316 i Carbon oraz zawory na wcisk. Montaż bez narzędzi i ognia.',
  desc='System push-fit montowany bez narzędzi, prądu i otwartego ognia. Łączy rury miedziane, PEX, PB, ze stali nierdzewnej i węglowej, zależnie od linii. Armatex jest oficjalnym przedstawicielem Pegler Yorkshire w Polsce.',
  who='Serwisanci, instalatorzy bez zaciskarki i klienci remontowi. Montaż bez narzędzi sprawia, że towar schodzi również przy ladzie.',
  arg='Producent daje 25 lat gwarancji na Tectite Sprint, Classic, Pro i 316, a 30 lat przy rurach Yorkshire.',
  pics=[('tectite-classic','Trójnik na wcisk Tectite Classic'),('tectite-316','Trójnik Tectite 316 ze stali nierdzewnej'),('pegler-tx300','Zawór kulowy na wcisk Pegler')],
  seria='',src='katalog Tectite 2026',
  lines=[('Tectite Classic','Pegler Yorkshire','','10–28 mm','woda, CO · miedź, PEX, PB','16 bar z miedzią',['WRAS','PZH'],'251','oferta/tectite-classic'),
   ('Tectite Pro i Carbon','Pegler Yorkshire','','15–54 mm','woda, CO, chłodzenie · także stal węglowa','Pro demontowalne',[],'115','oferta/tectite-pro'),
   ('Tectite 316','Pegler Yorkshire','','15–54 mm','rury ze stali nierdzewnej','demontowalne',[],'114','oferta/tectite-316'),
   ('Zawory i filtry na wcisk','Pegler Yorkshire','','15–54 mm','PT550, PT913, TX300, TX405, TX480','kulowe, odcinające, mieszające',[],'19','oferta/pegler-pt550'),
   ('Akcesoria i narzędzia Tec-Tools','Pegler Yorkshire','','10–54 mm','tulejki, gratowniki, mierniki','do montażu systemu',[],'ok. 30','linie/tectite-narzedzia')],
  faq=[('Jakie rury łączy Tectite?','Według tabeli kompatybilności producenta: Sprint i Classic łączą rury miedziane oraz PB i PEX z tulejką. Pro dodatkowo stal węglową ocynkowaną. Tectite 316 łączy miedź, stal nierdzewną i stal węglową, a Carbon stal węglową.'),
   ('Które złączki można zdemontować?','Classic, Pro i 316 są demontowalne. Sprint i Carbon są niedemontowalne.'),
   ('Jakie są parametry pracy?','Tectite Classic z rurą miedzianą: do 16 bar, od −24 do 95 °C. Limity dla innych rur i linii podaje tabela temperatur i ciśnień w katalogu producenta.'),
   ('Jaką gwarancję daje producent?','25 lat na Tectite Sprint, Classic, Pro i 316 z rurami innych producentów oraz 30 lat z rurami Yorkshire i rurami rekomendowanymi, jeśli montaż jest zgodny z instrukcją.'),
   ('Jakie zawory są w systemie?','Zawór kulowy PT550 (15–54 mm), filtr skośny PT913 (15–54 mm), zawór TX300 (15 i 22 mm), zawór mieszający TX405 (15 i 22 mm) i zawór odcinający TX480 (15 mm).')]),
 dict(slug='zlaczki-skrecane-kuterlite',name='Złączki skręcane',h1='Złączki skręcane Kuterlite',seotitle='Złączki skręcane Kuterlite dla hurtowni | Armatex',metadesc='Złączki skręcane (zaciskowe) Kuterlite: K600 i K900 Pro do miedzi 6–54 mm, K700 do rur PE 20–32 mm oraz zawory. Około 470 indeksów dla hurtowni.',tab='Skręcane',brand='Pegler Yorkshire',cnt='ok. 470',cntw='ok. 470 indeksów',sizes='6–63 mm',
  title='Złączki skręcane Kuterlite',
  short='Kuterlite K600 i K900 Pro do miedzi, K700 do rur PE oraz zawory z końcówkami zaciskowymi.',
  desc='Mosiężne złączki zaciskowe z pierścieniem do rur miedzianych i PE. Montaż kluczem, bez lutowania i zaciskarki. Armatex jest oficjalnym przedstawicielem Pegler Yorkshire w Polsce.',
  who='Serwis i podłączenia urządzeń: kotłów, podgrzewaczy i armatury. Klasyczny towar ladowy z rotacją przez cały rok.',
  arg='Jedna marka na miedź 6–54 mm i rury PE 20–32 mm, razem z zaworami w tym samym systemie.',
  pics=[('kuterlite','Trójnik skręcany Kuterlite'),('kuterlite-kolano','Kolano skręcane Kuterlite'),('kuterlite-zawor','Zawór z końcówkami zaciskowymi Kuterlite')],
  seria='',src='cennik Kuterlite, październik 2024',
  lines=[('Kuterlite K600','Pegler Yorkshire','','6–28 mm','rury miedziane','seria podstawowa',[],'ok. 150','oferta/kuterlite'),
   ('Kuterlite K900 Pro (KN 900)','Pegler Yorkshire','','8–54 mm','rury miedziane','złączki, kolana, przejścia GW/GZ',[],'ok. 185','oferta/kuterlite-kolano'),
   ('Kuterlite K700','Pegler Yorkshire','','20–32 mm','rury PE','złączki PE × PE i PE × miedź',[],'ok. 65','linie/kuterlite-k700'),
   ('Zawory z końcówkami zaciskowymi','Pegler Yorkshire','','15–28 mm','woda, podłączenia urządzeń','kurki, zawory odcinające',[],'ok. 30','oferta/kuterlite-zawor')],
  faq=[('Czym różnią się serie K600, K900 Pro i K700?','K600 to seria podstawowa do rur miedzianych 6–28 mm. K900 Pro obejmuje złączki, kolana i przejścia GW/GZ do miedzi 8–54 mm (na armatex.pl jako KN 900). K700 łączy rury PE 20–32 mm, także z miedzią i gwintem (tulejki, nakrętki i pierścienie do 63 mm).'),
   ('Czy montaż wymaga narzędzi?','Tylko kluczy. Pierścień zaciska się na rurze przy dokręcaniu nakrętki, bez lutowania i zaciskarki.'),
   ('Czy w systemie są zawory?','Tak: kurki i zawory z końcówkami zaciskowymi w średnicach 15–28 mm.'),
   ('Jak pakowane są złączki?','Każda pozycja ma w cenniku producenta dwa opakowania zbiorcze, na przykład złączka prosta K610 15 mm: 5 i 150 sztuk.')]),
 dict(slug='zlaczki-lutowane',name='Złączki lutowane',h1='Złączki lutowane Besco',seotitle='Złączki lutowane Besco: EN 1254, ANSI, G-size | Armatex',metadesc='Złączki lutowane Besco: kształtki EN 1254 serii 4000 i 5000 (6–108 mm), calowe ANSI B16.22 i G-size do 80 bar. 893 indeksy, dostawy do hurtowni w całej Polsce.',tab='Lutowane',brand='Besco',cnt='893',cntw='893 indeksy',sizes='6–108 mm',
  title='Złączki lutowane',
  short='Kształtki EN 1254 serii 4000 i 5000, calowe ANSI B16.22 i G-size do 80 bar.',
  desc='Miedziane złączki kapilarne do lutu miękkiego i twardego: metryczne serie 4000 i 5000 według EN 1254, calowe ANSI B16.22 oraz G-size do wysokich ciśnień.',
  who='Instalatorzy pracujący w klasycznej technologii, chłodnictwo i klimatyzacja oraz utrzymanie ruchu w przemyśle.',
  arg='Jeden dostawca na kształtki metryczne, calowe i G-size do 80 bar, bez dokładania kolejnej marki.',
  pics=[('besco-lut','Miedziany trójnik lutowany'),('besco-k','Miedziane kolano lutowane')],
  seria='cu-solder-en1254,cu-ansi-k,cu-g-size',src='katalog Besco 2026',
  lines=[('Seria 4000 i 5000, EN 1254','Besco','cu-solder-en1254','6–108 mm','woda, CO, gaz, przemysł','25 bar',['DVGW','KIWA','WRAS'],'513','linie/besco-lut'),
   ('Calowe ANSI B16.22, seria K','Besco','cu-ansi-k','1/4″–4 1/8″','woda, CO, gaz, przemysł','25 bar',[],'315','linie/besco-ansi-k'),
   ('G-size do wysokich ciśnień','Besco','cu-g-size','22–76,1 mm','chłodnictwo, przemysł','20–80 bar · do 150 °C',[],'65','linie/besco-g-size')],
  faq=[('Do jakiego lutowania są te kształtki?','To kształtki kapilarne do lutowania miękkiego i twardego.'),
   ('Jakie parametry ma seria EN 1254?','Średnice 6–108 mm, do 25 bar, od −20 do 110 °C. Aprobaty DVGW, KIWA i WRAS.'),
   ('Czym są seria K i G-size?','Seria K to calowe kształtki według ANSI B16.22 w rozmiarach od 1/4″ do 4 1/8″. G-size to kształtki 22–76,1 mm na ciśnienia 20–80 bar i temperatury do 150 °C, do chłodnictwa i przemysłu.'),
   ('Czy mogę zamówić po numerze artykułu?','Tak. Wszystkie 893 indeksy lutowane Besco znajdziesz w katalogu z wyszukiwarką. Dodaj je do listy i wyślij do wyceny.')]),
]
for i,s in enumerate(SYS,1): s['n']=f'{i:02d}'; s['topic']=f'Proszę o ofertę: {s["h1"][0].lower()+s["h1"][1:]}.'

# ---------------- grupy produktów Besco (z katalogu 2026)
import json, unicodedata
BD=json.load(open(R+'data/besco-2026.json',encoding='utf-8'))
SER_META={
 'cu-press-water-v':dict(short='press V',suf='press-v',qual='miedziany press, profil V',appr=['DVGW','KIWA','WRAS','RISE'],sys='zlaczki-zaciskane-press'),
 'cu-press-water-m':dict(short='press M',suf='press-m',qual='miedziany press, profil M',appr=['DVGW','WRAS','RISE'],sys='zlaczki-zaciskane-press'),
 'cu-press-gas-v':dict(short='press gaz V',suf='gaz-v',qual='press do gazu, profil V',appr=['DVGW','INiG'],sys='zlaczki-zaciskane-press'),
 'cu-press-gas-m':dict(short='press gaz M',suf='gaz-m',qual='press do gazu, profil M',appr=['DVGW','INiG'],sys='zlaczki-zaciskane-press'),
 'steel-press-m':dict(short='stal press',suf='stal',qual='press ze stali węglowej',appr=[],sys='zlaczki-zaciskane-press'),
 'cu-solder-en1254':dict(short='lutowane',suf='lut',qual='miedziany lutowany EN 1254',appr=['DVGW','KIWA','WRAS'],sys='zlaczki-lutowane'),
 'cu-ansi-k':dict(short='lutowane ANSI',suf='ansi-k',qual='lutowany calowy ANSI B16.22',appr=[],sys='zlaczki-lutowane'),
 'cu-g-size':dict(short='lutowane G-size',suf='g-size',qual='lutowany G-size',appr=[],sys='zlaczki-lutowane'),
 'press-ball-valve':dict(short='zawory press',suf='zawor',qual='',appr=['DVGW','WRAS'],sys='zlaczki-zaciskane-press'),
}
def slugify(t):
    t=t.replace('ł','l').replace('Ł','L').replace('×','x').replace('°','')
    t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',t).strip('-')
GROUPS=[]; _key={}
for gi,g in enumerate(BD['groups']):
    ser=BD['series'][g[0]]; k=(g[0],g[1],g[2])
    rows=[r for r in BD['rows'] if r[0]==gi]
    if k in _key: _key[k]['rows']+=rows; continue
    m=SER_META[ser['id']]
    nm=g[2]; full=(nm+' '+m['qual']).strip() if m['qual'] else nm
    G=dict(name=nm,full=full,code=g[1],en=g[3],img=g[4],ser=ser,meta=m,rows=rows,kind='besco',brand='Besco',sid=ser['id'],
           img_src=f'../img/besco/{g[4]}.webp',slug=f"besco-{slugify(nm)}-{m['suf']}-{slugify(g[1])}")
    _key[k]=G; GROUPS.append(G)
PD=json.load(open(R+'data/pegler.json',encoding='utf-8'))
PSER={}
for sid,x in PD['series'].items():
    gs=[g for g in PD['groups'] if g['series']==sid]
    PSER[sid]=dict(x,id=sid,count=sum(len(g['rows']) for g in gs))
for g in PD['groups']:
    ser=PSER[g['series']]; kind='tectite' if g['series'].startswith('tectite') else 'kuterlite'
    GROUPS.append(dict(name=g['name'],full=g['name'],code=g['code'],en=g['en'],img=g['img'],ser=ser,
        meta=dict(short=ser['short'],sys=ser['sys'],appr=ser['appr'],qual=''),rows=g['rows'],kind=kind,
        brand=('Tectite' if ser['brand'] in ('Tectite','Pegler') else 'Kuterlite') if kind=='tectite' else 'Kuterlite',
        sid=g['series'],img_src=(f"../img/pegler/{g['img']}.webp" if g['img'] else '../img/oferta/tectite-classic.webp'),slug=g['slug']))
_slugs=[G['slug'] for G in GROUPS]; assert len(_slugs)==len(set(_slugs)), 'duplikat slug'
def qa(art,l,pk):
    """Wybór ilości: liczba + jednostka (karton/worek/opak./szt.) + Dodaj."""
    opts=''.join(f'<option value="{i}" data-u="{u}" data-n="{n}">{u} ({fmt_int(n)} szt.)</option>' for i,(u,n) in enumerate(pk))
    opts+=f'<option value="{len(pk)}" data-u="szt." data-n="1">szt.</option>'
    import html as _h; l=_h.escape(l,quote=True)
    return (f'<div class="qty" data-add="{art}" data-l="{l}"><input type="number" min="1" step="1" value="1" inputmode="numeric" aria-label="Ilość {art}">'
            f'<select aria-label="Jednostka {art}">{opts}</select><button class="add" type="button">Dodaj</button></div>')

def gcard(G):
    return f'<a class="gcard" href="{G["slug"]}.html"><img src="{G["img_src"]}" alt="" width="56" height="56" loading="lazy" decoding="async"><span><b>{G["name"]}</b><small>{G["code"]} · {len(G["rows"])} rozm.</small></span></a>'
def groups_of(sid): return [G for G in GROUPS if G['sid']==sid]
SYS_BY_SLUG={}
def grp_links(sids, open_first=False):
    out=[]
    for i,sid in enumerate(sids):
        gs=groups_of(sid); ser=gs[0]['ser']
        links=''.join(gcard(G) for G in gs)
        out.append(f'<details class="gl"{" open" if (open_first and i==0) else ""}><summary><b>{ser["name"]}</b><span class="label">{len(gs)} grup · {ser["count"]} indeksów</span></summary><div class="gl__l">{links}</div></details>')
    return '\n'.join(out)


import json
SITE='https://armatex.pl/'
def ld(obj): return '  <script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False)+'</script>\n'
LD_ORG=ld({"@context":"https://schema.org","@graph":[
  {"@type":"WholesaleStore","@id":SITE+"#firma","name":"Armatex","url":SITE,
   "logo":SITE+"img/logo-dark.webp","image":SITE+"img/og/armatex-og.jpg",
   "description":"Dystrybutor złączek i armatury Besco oraz Pegler Yorkshire dla hurtowni instalacyjnych w całej Polsce: złączki zaciskane (press), na wcisk, skręcane i lutowane.",
   "telephone":"+48 513 191 502","email":"biuro@armatex.pl","foundingDate":"1991",
   "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"07:00","closes":"18:00"}],
   "legalName":"P.H.U. ARMATEX Sp. J. A. J. Bunda","taxID":"7393814110",
   "identifier":[{"@type":"PropertyValue","propertyID":"KRS","value":"0000371628"},{"@type":"PropertyValue","propertyID":"REGON","value":"280563743"}],
   "address":{"@type":"PostalAddress","streetAddress":"ul. Składowa 3a","postalCode":"10-421","addressLocality":"Olsztyn","addressCountry":"PL"},
   "areaServed":{"@type":"Country","name":"Polska"},
   "brand":[{"@type":"Brand","name":"Besco"},{"@type":"Brand","name":"Pegler Yorkshire"}],
   "contactPoint":[
     {"@type":"ContactPoint","contactType":"sales","name":"Piotr Stelmach","telephone":"+48 798 807 106","email":"piotr@armatex.pl","areaServed":"PL","availableLanguage":"pl"},
     {"@type":"ContactPoint","contactType":"warehouse","name":"Martyna Zielińska","telephone":"+48 515 231 693","email":"martyna@armatex.pl","areaServed":"PL","availableLanguage":"pl"}]},
  {"@type":"WebSite","@id":SITE+"#www","url":SITE,"name":"Armatex","inLanguage":"pl-PL","publisher":{"@id":SITE+"#firma"}}]})
def ld_crumbs(items):
    el=[{"@type":"ListItem","position":1,"name":"Armatex","item":SITE}]
    for i,(n,u) in enumerate(items,2): el.append({"@type":"ListItem","position":i,"name":n,"item":SITE+u})
    return ld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":el})
def ld_system(s):
    lst=ld({"@context":"https://schema.org","@type":"ItemList","name":s['h1'],
      "itemListElement":[{"@type":"ListItem","position":i,"name":f"{l[0]} ({l[1]}), {l[3]}"} for i,l in enumerate(s['lines'],1)]})
    return ld_crumbs([('Oferta','index.html#systemy'),(s['name'],s['slug']+'.html')])+lst

def head(title,desc,extra='',path=''):
    return f'''<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#0A1F44">
  <link rel="canonical" href="{SITE+path}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pl_PL">
  <meta property="og:site_name" content="Armatex">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{SITE+path}">
  <meta property="og:image" content="{SITE}img/og/armatex-og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Armatex: złączki Besco i Pegler Yorkshire dla hurtowni">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="../../assets/img/favicon-32.png?v=2" type="image/png" sizes="32x32">
  <link rel="icon" href="../../assets/img/icon-192.png" type="image/png" sizes="192x192">
  <link rel="apple-touch-icon" href="../../assets/img/apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">
  <meta name="theme-color" content="#0a1f44">
  <link rel="preload" href="../../assets/fonts/outfit-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="../../assets/fonts/outfit-latin-ext-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{extra}  <link rel="stylesheet" href="c.css">
  <script src="c.js" defer></script>
</head>
'''
PDF='../pliki/katalog-besco-2026.pdf'
ICO_SEARCH='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
ICO_PDF='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3v4a1 1 0 0 0 1 1h4"/><path d="M17 21H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7l5 5v11a2 2 0 0 1-2 2z"/><path d="M12 11v6M9.5 14.5 12 17l2.5-2.5"/></svg>'
def nav(cur):
    cs=lambda k: ' aria-current="page"' if k==cur else ''
    ddlinks=''.join(f'<a href="{s["slug"]}.html"{cs(s["slug"])}>{img(s["pics"][0][0],"")}<b>{s["name"]}</b><span>{s["brand"]} · {s["cntw"]}</span></a>' for s in SYS)
    ddcur=' aria-current="page"' if cur in [s['slug'] for s in SYS]+[] else ''
    kat=(f'<a href="katalog.html"{cs("katalog")}><span class="dd__ico">{ICO_SEARCH}</span><b>Wyszukiwarka indeksów Besco</b><span>1 936 indeksów · lista do wyceny</span></a>'
         f'<a href="{PDF}" target="_blank" rel="noopener"><span class="dd__ico">{ICO_PDF}</span><b>Katalog Besco 2026</b><span>PDF · 2,7 MB · 65 stron</span></a>')
    mlinks=''.join(f'<a href="{s["slug"]}.html"{cs(s["slug"])}>{s["name"]}<small>{s["brand"]}</small></a>' for s in SYS)
    return f'''<header class="nav" id="nav">
  <div class="wrap">
    <a class="nav__logo" href="index.html" aria-label="Armatex, strona główna">
      <img class="light" src="../img/logo-light.webp" alt="" width="300" height="52" fetchpriority="high">
      <img class="dark" src="../img/logo-dark.webp" alt="" width="300" height="52">
    </a>
    <nav class="nav__links" aria-label="Nawigacja główna">
      <div class="dd"><button type="button" aria-expanded="false" aria-controls="dd-m"{ddcur}>Oferta</button><div class="dd__m" id="dd-m"><span class="dd__h">Systemy złączek</span>{ddlinks}<span class="dd__h">Katalogi</span>{kat}</div></div>
      <a href="katalog.html"{cs("katalog")}>Wyszukiwarka</a>
      <a href="wspolpraca.html"{cs("wspolpraca")}>Współpraca</a>
      <a href="do-pobrania.html"{cs("do-pobrania")}>Do pobrania</a>
      <a href="poradniki.html"{cs("poradniki")}>Poradniki</a>
      <a href="o-firmie.html"{cs("o-firmie")}>O firmie</a>
      <a href="kontakt.html"{cs("kontakt")}>Kontakt</a>
    </nav>
    <a class="nav__tel" href="tel:+48513191502">513 191 502</a>
    <a class="mag" href="{"#kontakt" if cur=="index" else "kontakt.html#formularz"}"><span>Zapytaj o wycenę</span></a>
    <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Otwórz menu"><i></i></button>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="Menu mobilne">
  <span class="label">Oferta</span>{mlinks}
  <span class="label">Katalogi</span><a href="katalog.html"{cs("katalog")}>Wyszukiwarka indeksów Besco<small>1 936</small></a><a href="{PDF}" target="_blank" rel="noopener">Katalog Besco 2026<small>PDF · 2,7 MB</small></a>
  <span class="label">Armatex</span><a href="wspolpraca.html"{cs("wspolpraca")}>Współpraca</a><a href="do-pobrania.html"{cs("do-pobrania")}>Do pobrania<small>katalogi i dokumenty</small></a><a href="poradniki.html"{cs("poradniki")}>Poradniki</a><a href="o-firmie.html"{cs("o-firmie")}>O firmie</a><a href="kontakt.html"{cs("kontakt")}>Kontakt<small>513 191 502</small></a>
</nav>
'''
FOOT='''<footer class="foot">
  <div class="wrap foot__g">
    <div>
      <img src="../img/logo-light.webp" alt="Armatex" width="300" height="52" loading="lazy">
      <p>Dystrybutor złączek i armatury Besco oraz Pegler Yorkshire dla hurtowni instalacyjnych w całej Polsce.</p>
    </div>
    <div><h2>Oferta</h2><ul>'''+''.join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SYS)+'''</ul></div>
    <div><h2>Armatex</h2><ul><li><a href="katalog.html">Wyszukiwarka indeksów Besco</a></li><li><a href="'''+PDF+'''" target="_blank" rel="noopener">Katalog Besco 2026 (PDF)</a></li><li><a href="do-pobrania.html">Do pobrania</a></li><li><a href="poradniki.html">Poradniki</a></li><li><a href="o-firmie.html">O firmie</a></li><li><a href="wspolpraca.html">Współpraca</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
    <div><h2>Kontakt</h2><ul><li><a href="tel:+48513191502">513 191 502</a></li><li><a href="mailto:biuro@armatex.pl">biuro@armatex.pl</a></li><li class="foot__addr"><small>Biuro i magazyn</small> ul. Składowa 3a, 10-421 Olsztyn<br>pn–pt 7:00–18:00</li></ul></div>
  </div>
  <div class="wrap foot__bar">
    <div class="foot__co">
      <span class="foot__name">© 2026 P.H.U. ARMATEX Sp. J. A. J. Bunda</span>
      <dl><div><dt>Siedziba</dt><dd>ul. Siewna 24, 10-831 Olsztyn</dd></div><div><dt>NIP</dt><dd>7393814110</dd></div><div><dt>KRS</dt><dd>0000371628</dd></div><div><dt>REGON</dt><dd>280563743</dd></div></dl>
    </div>
    <a href="polityka-prywatnosci.html">Polityka prywatności</a>
  </div>
</footer>
<a class="callfab" href="tel:+48513191502" aria-label="Zadzwoń: 513 191 502"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg><span>Zadzwoń</span></a>
'''
FORM_NAME='zapytanie'   # nazwa formularza w panelu Netlify (Forms); powiadomienia e-mail ustawia się tam
def live_form(html):
    """Formularz obsługuje Netlify Forms: wykrywa go przy wdrożeniu po data-netlify, zapisuje zgłoszenia w panelu i wysyła powiadomienia."""
    if 'id="form" novalidate>' not in html: return html
    html=html.replace('<form class="form" id="form" novalidate>',
        f'<form class="form" id="form" name="{FORM_NAME}" method="POST" data-netlify="true" netlify-honeypot="bot-field" novalidate>\n'
        f'        <input type="hidden" name="form-name" value="{FORM_NAME}">\n'
        '        <input type="hidden" name="subject" data-remove-prefix value="Zapytanie o wycenę ze strony armatex.pl">\n'
        '        <p class="sr" aria-hidden="true"><label>Nie wypełniaj: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>')
    for a,b in (('<input id="n" autocomplete="name">','<input id="n" name="Imię i nazwisko" autocomplete="name">'),
                ('<input id="c" autocomplete="organization">','<input id="c" name="Firma" autocomplete="organization">'),
                ('<input id="e" type="email" autocomplete="email">','<input id="e" name="email" type="email" autocomplete="email" required>'),
                ('<input id="t" type="tel" autocomplete="tel">','<input id="t" name="Telefon" type="tel" autocomplete="tel" inputmode="tel" required>'),
                ('<input id="e" name="email" type="email" autocomplete="email" required>','<input id="e" name="email" type="email" autocomplete="email" inputmode="email" required>'),
                ('<select id="pf">','<select id="pf" name="Profil firmy">'),
                ('<input id="ms" autocomplete="address-level2">','<input id="ms" name="Miasto / województwo" autocomplete="address-level2">'),
                ('<textarea id="m" ','<textarea id="m" name="Zapytanie" '),
                ('<input type="checkbox" id="ok">','<input type="checkbox" id="ok" name="Zgoda" value="tak" required>')):
        assert a in html, a; html=html.replace(a,b)
    for fid,lab in (('e','E-mail'),('t','Telefon')):
        a=f'<label for="{fid}">{lab}</label>'; assert a in html, a
        html=html.replace(a,f'<label for="{fid}">{lab} <span class="req" aria-hidden="true">*</span></label>')
    a='value="tak" required> Wyrażam zgodę na przetwarzanie danych w celu obsługi zapytania. Administratorem danych jest Armatex.</label>'; assert a in html
    html=html.replace(a,'value="tak" required> <span>Wyrażam zgodę na <a href="polityka-prywatnosci.html" target="_blank">przetwarzanie danych</a> w celu obsługi zapytania. Administratorem danych jest Armatex. <span class="req" aria-hidden="true">*</span></span></label>')
    return html


# ---------------- pomocnicze: SEO i zasoby
import hashlib
ASSET_V={f:hashlib.md5(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',f),'rb').read()).hexdigest()[:8] for f in ('c.css','c.js')}

def short_title(t,limit=60):
    # Google ucina tytuły ok. 60 znaków: najpierw zdejmujemy „| Armatex”, potem nazwę linii po „–”
    if len(t)>limit: t=t.replace(' | Armatex','')
    if len(t)>limit and ' – ' in t: t=t.rsplit(' – ',1)[0]
    return t

def short_desc(d,limit=160):
    if len(d)<=limit: return d
    cut=d[:limit]
    i=cut.rfind('. ')
    if i>=100: return cut[:i+1]
    return cut[:cut.rfind(' ')].rstrip(',;:–')+'…'

_WH={}
def img_wh(src):
    f=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',src.replace('../',''))
    if f not in _WH:
        try: w,h=Image.open(f).size; _WH[f]=f'width="{w}" height="{h}"'
        except Exception: _WH[f]=''
    return _WH[f]


# Google czyta sąsiednie elementy inline bez odstępu („BiuroP.H.U.”): wstawiamy spację między
# zamknięciem jednego elementu a treścią następnego. W układach flex/grid spacja nie jest widoczna.
_INL='a|span|b|small|strong|em|i|code|abbr|mark|sup|sub|u|s|time'
_GLUE=re.compile(r'(?<=[\w.,)%°″"])((?:</?(?:'+_INL+r')\b[^>]*>)+)(?=[\w(])')
def _unglue_part(t):
    def f(m):
        g=m.group(1)
        if '</' not in g: return ' '+g if g.startswith('<small') else g
        i=max(k.end() for k in re.finditer(r'</[^>]+>',g))
        return g[:i]+' '+g[i:]
    return _GLUE.sub(f,t)
def unglue(html):
    parts=re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<svg\b.*?</svg>|<head>.*?</head>)',html,flags=re.S)
    return ''.join(x if i%2 else _unglue_part(x) for i,x in enumerate(parts))

def page(name,title,desc,cur,body,extra=''):
    title,desc=short_title(title),short_desc(desc)
    html=head(title,desc,extra,'' if name=='index.html' else name)+'<body data-base="../">\n\n'+nav(cur)+'\n<main id="top">\n'+body+'\n</main>\n\n'+FOOT+'</body>\n</html>\n'
    # strona w katalogu głównym repo: ścieżki względne bez prefiksów szkicu
    for a,b in (('../../assets/','assets/'),('../img/','img/'),('../pliki/','pliki/'),('../data/','data/'),('<body data-base="../">','<body>')):
        html=html.replace(a,b)
    html=live_form(html)
    html=unglue(html)
    html=html.replace('href="c.css"',f'href="c.css?v={ASSET_V["c.css"]}"').replace('src="c.js"',f'src="c.js?v={ASSET_V["c.js"]}"')
    open(OUT+name,'w',encoding='utf-8').write(html)

def card(s,cls='syc in'):
    p0,a0=s['pics'][0]
    ims=img(p0,a0)
    return f'<a class="{cls}" href="{s["slug"]}.html"><span class="syc__m">{ims}</span><span class="syc__b"><span class="label syc__k">{s["n"]} · {s["brand"]}</span><h3>{s["name"]}</h3><p>{s["short"]}</p><span class="syc__f"><span class="label">{s["cntw"]} · {s["sizes"]}</span><span class="syc__go">Zobacz →</span></span></span></a>'

def faqlist(items, first_open=True):
    return '\n'.join(f'        <details class="qa" name="faq"{" open" if (i==0 and first_open) else ""}><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for i,(q,a) in enumerate(items))


# ---------------- strona główna
hero=frag('  <section class="hero"','  </section>')
hero=hero.replace('<a class="mag" href="#kontakt" data-topic="Jesteśmy hurtownią i chcemy poznać warunki współpracy (Besco, Pegler Yorkshire)."><span>Warunki dla hurtowni <svg','<a class="mag" href="#kontakt"><span>Zapytaj o wycenę <svg')
hero=hero.replace('<a class="ghost" href="#katalog">Szukaj po numerze artykułu</a>','<a class="ghost" href="#systemy">Zobacz systemy</a>')
hb=hero[hero.index('<div class="hero__bar">'):hero.index('</div>\n    </div>\n  </section>')]
newbar='<div class="hero__bar">\n'+''.join(f'        <a href="{s["slug"]}.html"><span class="label">{s["n"]}</span><b>{s["name"]}</b></a>\n' for s in SYS)+'        <a class="hb-end" href="katalog.html"><span class="label">Katalog Besco 2026</span><b>1 936 indeksów →</b></a>\n      '
hero=hero.replace(hb,newbar)
hero=hero.replace('src="img/besco/','src="../img/besco/').replace('<p class="label hero__eyebrow">Besco · Pegler Yorkshire · 30 lat na rynku</p>','<p class="label hero__eyebrow">Dystrybutor złączek Besco i Pegler Yorkshire · 30 lat na rynku</p>')
NEW='https://d8j0ntlcm91z4.cloudfront.net/user_33T37u6buO6KWzmObkHx6hwX3AX/hf_20260927_185901_97950f69-3284-44cc-9e7f-6c2349f20305'
OLD_D='https://d8j0ntlcm91z4.cloudfront.net/user_33T37u6buO6KWzmObkHx6hwX3AX/hf_20260927_144146_f71ca1f9-b0b9-46a2-af54-14357f0f5abc'
OLD_M='https://d8j0ntlcm91z4.cloudfront.net/user_33T37u6buO6KWzmObkHx6hwX3AX/hf_20260927_144146_c5cc2103-2b87-4e8f-8352-0e19ac20b5bb'
def hero_img(t): return re.sub(r'\s*<source media="\(max-width: 720px\)"[^>]*>','',t.replace(OLD_D,NEW).replace(OLD_M,NEW)).replace(' media="(min-width: 721px)"','')
hero=re.sub(r'\s*<p class="label hero__eyebrow">[^<]*</p>','',hero)
hero=hero.replace('<h1 id="hero-t">','<h1 id="hero-t"><span class="label hero__eyebrow">Dystrybutor złączek Besco i Pegler Yorkshire</span>',1)
assert hero.count('hero__eyebrow')==1
hero=hero_img(hero).replace('alt="Mosiężny zawór kulowy z czerwoną dźwignią i złączki zaprasowywane"','alt="Paleta z kartonami złączek miedzianych i mosiężnych w magazynie"')
HERO_MEDIA="""<div class="hero__media">
      <picture>
        <source media="(max-width: 720px)" srcset="../img/hero/hero-paleta-m.webp" width="800" height="1001">
        <img src="../img/hero/hero-paleta-2000.webp" srcset="../img/hero/hero-paleta-1200.webp 1200w, ../img/hero/hero-paleta-2000.webp 2000w" sizes="100vw" alt="Paleta z kartonami złączek miedzianych i mosiężnych w magazynie" width="2000" height="1116" fetchpriority="high">
      </picture>
    </div>"""
hero=re.sub(r'<div class="hero__media" data-hf>.*?</picture>\s*</div>',lambda m: HERO_MEDIA,hero,flags=re.S)
assert 'hero-paleta-2000' in hero and 'data-hf>' not in hero.split('hero__media')[1][:5]
assert 'hb-end' in hero and 'data-topic' not in hero
kontakt_home=frag('  <section class="section close" id="kontakt">','  </section>')
# tło sekcji kontaktu: lokalne zdjęcie palety (to samo co w hero), bez zewnętrznego CDN
kontakt_home=re.sub(r'<div class="close__bg" aria-hidden="true" data-hf><img [^>]*></div>',
    '<div class="close__bg" aria-hidden="true"><img src="../img/hero/hero-paleta-1200.webp" srcset="../img/hero/hero-paleta-1200.webp 1200w, ../img/hero/hero-paleta-2000.webp 2000w" sizes="100vw" alt="" width="2000" height="1116" loading="lazy" decoding="async"></div>',kontakt_home)
assert 'cloudfront' not in kontakt_home
kontakt_home=kontakt_home.replace('<h2 class="h2">Porozmawiajmy o warunkach dla Twojej hurtowni.</h2>','<h2 class="h2">Porozmawiajmy o ofercie dla Twojej hurtowni.</h2>')
kontakt_home=kontakt_home.replace('<h3>Zapytanie o warunki współpracy</h3>','<h2 class="form__t">Zapytanie o wycenę</h2>')
steps=frag('      <div class="steps">','      </div>\n      <div class="aud">').replace('      <div class="aud">','').rstrip()
stats='''      <div class="stats">
        <div class="stat"><b><span class="odo" data-odo="1991" data-year aria-label="1991">1991</span><i> r.</i></b><span>założenia przedsiębiorstwa</span></div>
        <div class="stat"><b><span class="odo" data-odo="24" aria-label="24">24</span><i> h</i></b><span>wysyłka z magazynu w Olsztynie</span></div>
        <div class="stat"><b><span class="odo" data-odo="1" aria-label="1">1</span><i> dzień</i></b><span>na przygotowanie oferty</span></div>
        <div class="stat"><b><span class="odo" data-odo="4" aria-label="4">4</span><i> systemy</i></b><span>łączenia od jednego dystrybutora</span></div>
      </div>'''
docs=frag('  <section class="docs" id="dokumenty">','  </section>').replace('<a class="ghost" href="#kontakt" data-topic="Jesteśmy hurtownią i prosimy o dostęp do bazy dokumentów technicznych.">','<a class="ghost" href="'+ask('Jesteśmy hurtownią i prosimy o dostęp do bazy dokumentów technicznych.')+'">').replace('src="img/besco/','src="../img/besco/')
assert 'kontakt.html?temat=' in docs
home=f'''
{hero}

  <!-- 2 · SYSTEMY -->
  <section class="section" id="systemy">
    <div class="wrap">
      <div class="rg__head">
        <div>
          <span class="label kicker">Oferta dla hurtowni · Besco i Pegler Yorkshire</span>
          <h2 class="h2">Cztery systemy. Około 2 900 indeksów.</h2>
          <p class="lead" style="margin-top:1rem">Dystrybuujemy złączki i armaturę Besco oraz Pegler Yorkshire do hurtowni instalacyjnych w całej Polsce. Wybierz system, żeby zobaczyć linie, parametry i argumenty sprzedażowe.</p>
        </div>
        <a class="ulink" href="katalog.html">Szukaj po numerze artykułu</a>
      </div>
      <div class="sys">
        {chr(10).join("        "+card(s) for s in SYS).lstrip()}
      </div>
    </div>
  </section>

  <!-- 3 · CO ZYSKUJE HURTOWNIA -->
  <section class="section section--stone" id="zysk">
    <div class="wrap">
      <div class="yard__grid">
        <div>
          <span class="label kicker">Współpraca</span>
          <h2 class="h2">Partner, na którym oprzesz swoje stany.</h2>
        </div>
        <p class="lead">Trzymamy pełne stany najczęściej rotujących pozycji Besco i Pegler Yorkshire, dlatego typowe zamówienie hurtowni kompletujemy tego samego dnia. O brakach rynkowych informujemy z wyprzedzeniem.</p>
      </div>
{stats}
      <div class="gain">
        <div class="in"><span class="label">01</span><b>Pełny program z jednego źródła</b><p>Cztery systemy łączenia i dwie marki w jednej dostawie, na jednej fakturze.</p></div>
        <div class="in"><span class="label">02</span><b>Dostawy w całej Polsce</b><p>Duże zamówienia dowozimy własnym transportem.</p></div>
        <div class="in"><span class="label">03</span><b>Zatowarowanie na sezon</b><p>Rezerwacje stanów i wspólne planowanie dostaw przed sezonem grzewczym.</p></div>
        <div class="in"><span class="label">04</span><b>Dokumenty dla Twoich klientów</b><p>Atesty, deklaracje i karty katalogowe do każdej pozycji.</p></div>
      </div>
      <p style="margin-top:2rem"><a class="ulink" href="wspolpraca.html">Więcej o współpracy</a></p>
    </div>
  </section>

  <!-- 4 · JAK ZACZĄĆ -->
  <section class="section" id="start">
    <div class="wrap">
      <span class="label kicker">Pierwsze zamówienie</span>
      <h2 class="h2">Jak zacząć współpracę.</h2>
{steps}
    </div>
  </section>

  <!-- 5 · PYTANIA -->
{docs.replace('<section class="docs"','<section class="docs docs--w"',1)}

  <section class="section" id="faq" style="padding-top:0">
    <div class="wrap faq">
      <div class="faq__intro">
        <span class="label kicker">Pytania</span>
        <h2 class="h2">Pytania partnerów.</h2>
        <p class="lead">Od hurtowni, firm instalacyjnych i wykonawców. Pytania techniczne o poszczególne systemy znajdziesz na ich stronach.</p>
        <a class="ulink" href="tel:+48513191502">Zadzwoń: 513 191 502</a>
      </div>
      <div>
{faqlist([
 ('Jak szybko dostanę ofertę?','W ciągu jednego dnia roboczego. Oferta zawiera ceny hurtowe, dostępność i terminy dostaw dla systemów lub indeksów, które chcesz prowadzić.'),
 ('Czy współpracujecie tylko z hurtowniami?','Hurtownie instalacyjne to nasi główni partnerzy i pod nie ustawiamy stany, logistykę oraz warunki. Obsługujemy też firmy instalacyjne, generalnych wykonawców, zakłady przemysłowe i zarządców budynków, zwłaszcza przy większych inwestycjach i zamówieniach projektowych. <a href="kontakt.html#formularz">Napisz, czego potrzebujesz</a>, a dobierzemy formę współpracy.'),
 ('Jakie marki i systemy dystrybuujecie?','Besco Fittings &amp; Connectors: miedź press w profilach V i M, serie gazowe, stal węglowa press, złączki lutowane i zawory kulowe press. Pegler Yorkshire: złączki na wcisk Tectite, złączki skręcane Kuterlite i zawory na wcisk. Razem około 2 900 indeksów.'),
 ('Jaki jest czas dostawy?','Wysyłka z magazynu w Olsztynie w 24 godziny od potwierdzenia zamówienia. Duże zamówienia dowozimy własnym transportem.'),
 ('Czy mogę zamówić po numerze artykułu Besco?','Tak. <a href="katalog.html">Katalog z wyszukiwarką</a> obejmuje 1 936 pozycji Besco 2026. Dodaj indeksy do listy, podaj ilości i wyślij do wyceny.'),
 ('Jak uzyskać dostęp do dokumentów?','Poproś o dostęp przez formularz. Po weryfikacji firmy udostępniamy karty katalogowe, atesty i deklaracje w ciągu jednego dnia roboczego.')])}
      </div>
    </div>
  </section>

  <!-- 6 · KONTAKT -->
{kontakt_home}
'''
pre=''.join('  '+l+'\n' for l in re.findall(r'<link rel="preload" as="image"[^>]*>',SRC))
pre=re.sub(r'\s*<link rel="preload" as="image"[^>]*>','',pre)
pre+='  <link rel="preload" as="image" href="../img/hero/hero-paleta-2000.webp" imagesrcset="../img/hero/hero-paleta-1200.webp 1200w, ../img/hero/hero-paleta-2000.webp 2000w" imagesizes="100vw" media="(min-width: 721px)" fetchpriority="high">\n'
pre+='  <link rel="preload" as="image" href="../img/hero/hero-paleta-m.webp" media="(max-width: 720px)" fetchpriority="high">\n'
pre=pre.replace('<link rel="preload" as="image" href="'+NEW+'_min.webp" media="(max-width: 720px)" fetchpriority="high" data-hf>','') if pre.count(NEW+'_min.webp')>1 else pre
page('index.html','Armatex – Dystrybutor złączek Besco i Pegler Yorkshire','Armatex (P.H.U. ARMATEX Sp. J. A. J. Bunda), Olsztyn: dystrybutor złączek Besco i Pegler Yorkshire dla hurtowni w całej Polsce. Od 1991 r., wysyłka w 24 h.','index',home,pre+LD_ORG)

# ---------------- strony systemów
def thumb(ph,alt):
    w,h=Image.open(f'{R}img/{ph}.webp').size
    return f'<img src="../img/{ph}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">'

def prod_section(s):
    sids=(s['seria'].split(',') if s['seria'] else [])+[k for k,v in PSER.items() if v['sys']==s['slug']]
    if not sids: return ''
    n=sum(len(groups_of(x)) for x in sids)
    return f"""  <section class="section section--tight" id="produkty" style="padding-top:0">
    <div class="wrap">
      <div class="shead"><h2 class="sy-h" style="margin:0">Produkty w systemie</h2><span class="label" style="color:var(--ink-40)">{n} grup produktów · rozmiary, numery i opakowania</span></div>
      <div class="gls">
{grp_links(sids, True)}
      </div>
    </div>
  </section>
"""

def lines_table(s):
    rows=[]
    for nm,b,ser,d,z,par,ap,c,ph in s['lines']:
        appr=''.join(f'<span class="appr">{a}</span>' for a in ap)
        act=f'<a class="sy-find" href="katalog.html?seria={ser}#katalog">Indeksy</a>' if ser else '<a class="sy-find" href="#produkty">Produkty</a>'
        bc='pegler' if b.startswith('Pegler') else 'besco'
        rows.append(f'              <tr><th scope="row"><span class="sy-row"><span class="sy-thumb">{thumb(ph,nm)}</span><span><b>{nm}</b><span class="label sy-br sy-br--{bc}">{b}</span></span></span></th><td class="num" data-l="Średnice">{d}</td><td data-l="Zastosowanie">{z}</td><td data-l="Parametry"><span><span class="sy-par">{par}</span>{appr}</span></td><td class="num sy-cnt" data-l="Indeksy">{c}</td><td class="sy-act">{act}</td></tr>')
    return '\n'.join(rows)
for s in SYS:
    others=[o for o in SYS if o is not s]
    figs=''.join(f'<span>{img(p,a)}</span>' for p,a in s['pics'])
    find=(f'<a class="ghost" href="katalog.html?seria={s["seria"]}#katalog">Szukaj indeksów</a><a class="ghost ghost--pdf" href="{PDF}" target="_blank" rel="noopener">Katalog PDF</a>') if s['seria'] else ''
    body=f'''
  <section class="phead">
    <div class="wrap">
      <ol class="crumbs"><li><a href="index.html">Armatex</a></li><li><a href="index.html#systemy">Oferta</a></li><li aria-current="page">{s["name"]}</li></ol>
      <div>
        <span class="label kicker">{s["n"]} · {s["brand"]}</span>
        <h1>{s["h1"]}</h1>
        <p class="lead">{s["desc"]}</p>
        <div class="phead__ctas"><a class="mag" href="{ask(s["topic"])}"><span>Zapytaj o wycenę</span></a>{find}</div>
      </div>
      <dl class="phead__facts">
        <div><dt class="label">Indeksy</dt><dd>{s["cnt"]}</dd></div>
        <div><dt class="label">Średnice</dt><dd>{s["sizes"]}</dd></div>
        <div><dt class="label">Producent</dt><dd>{s["brand"]}</dd></div>
      </dl>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <div class="sy-intro">
        <figure class="sy-pics sy-pics--{len(s["pics"])}">{figs}</figure>
        <div>
          <span class="label kicker">Dla Twojej hurtowni</span>
          <h2 class="sy-h">Komu to sprzedasz i jak.</h2>
          <dl class="sy-facts">
            <div><dt class="label">Kto kupuje w Twojej hurtowni</dt><dd>{s["who"]}</dd></div>
            <div class="sy-arg"><dt class="label">Argument sprzedażowy</dt><dd>{s["arg"]}</dd></div>
          </dl>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--tight" id="linie" style="padding-top:0">
    <div class="wrap">
      <div class="shead"><h2 class="sy-h" style="margin:0">Linie w systemie</h2><span class="label" style="color:var(--ink-40)">Źródło: {s["src"]}</span></div>
      <div class="sy-tw">
        <table class="sy-lines">
          <caption class="sr">{s["title"]}: linie produktów</caption>
          <thead><tr><th scope="col">Linia</th><th scope="col">Średnice</th><th scope="col">Zastosowanie</th><th scope="col">Parametry</th><th scope="col" class="num">Indeksy</th><th scope="col"><span class="sr">Akcja</span></th></tr></thead>
          <tbody>
{lines_table(s)}
          </tbody>
        </table>
      </div>
    </div>
  </section>

{prod_section(s)}
  <section class="section section--tight section--stone" id="faq">
    <div class="wrap faq">
      <div class="faq__intro">
        <span class="label kicker">Pytania techniczne</span>
        <h2 class="h2">Co warto wiedzieć.</h2>
        <p class="lead">Odpowiedzi według dokumentacji producenta. Resztę wyjaśni handlowiec.</p>
        <a class="ulink" href="tel:+48513191502">Zadzwoń: 513 191 502</a>
      </div>
      <div>
{faqlist(s["faq"])}
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <div class="cta">
        <div><h2>Zapytaj o wycenę na {s["name"].lower()} {s["brand"]}.</h2><p>Ceny hurtowe, dostępność i terminy dostaw przygotujemy w ciągu jednego dnia roboczego.</p></div>
        <div class="cta__b"><a class="mag" href="{ask(s["topic"])}"><span>Zapytaj o wycenę</span></a></div>
      </div>
      <div class="shead" style="margin-top:clamp(3rem,6vw,4.5rem)"><h2 class="sy-h" style="margin:0">Pozostałe systemy</h2><a class="ulink" href="index.html#systemy">Wszystkie systemy</a></div>
      <div class="sys sys--3">
        {chr(10).join("        "+card(o) for o in others).lstrip()}
      </div>
    </div>
  </section>
'''
    page(f'{s["slug"]}.html',s['seotitle'],s['metadesc'],s['slug'],body,ld_system(s))

# ---------------- katalog
fd=frag('      <div class="fd__g">','        </aside>\n      </div>')
kat=f'''
  <section class="phead">
    <div class="wrap">
      <ol class="crumbs"><li><a href="index.html">Armatex</a></li><li aria-current="page">Katalog Besco</li></ol>
      <div>
        <span class="label kicker">Wyszukiwarka indeksów</span>
        <h1>Katalog złączek Besco 2026</h1>
        <p class="lead">Zbuduj listę indeksów do wyceny. Wpisz numer artykułu Besco, średnicę albo nazwę. Dodaj indeksy, które chcesz prowadzić, podaj ilości i wyślij listę. Ofertę przygotujemy w jeden dzień roboczy.</p>
        <div class="phead__ctas"><a class="ghost" href="{PDF}" target="_blank" rel="noopener">Pobierz katalog Besco 2026 (PDF · 2,7 MB)</a></div>
      </div>
      <dl class="phead__facts">
        <div><dt class="label">Indeksy</dt><dd>1 936</dd></div>
        <div><dt class="label">Linie</dt><dd>9</dd></div>
        <div><dt class="label">Pakowanie</dt><dd>worek / karton</dd></div>
      </dl>
    </div>
  </section>

  <section class="section finder section--tight" id="katalog" aria-label="Wyszukiwarka katalogu Besco 2026">
    <div class="wrap">
{fd}
      <div class="shead" style="margin-top:clamp(3rem,6vw,4.5rem)"><h2 class="sy-h" style="margin:0">Wszystkie grupy produktów</h2><span class="label" style="color:var(--ink-40)">{len(GROUPS)} grup · Besco, Tectite, Kuterlite</span></div>
      <p class="lead" style="margin-top:.8rem;max-width:none">Każda grupa ma własną stronę z tabelą rozmiarów, numerami artykułów, opakowaniami zbiorczymi i parametrami linii.</p>
      <div class="gls">
{grp_links([x['id'] for x in BD['series']]+list(PSER))}
      </div>
      <p class="lead" style="margin-top:2.5rem;max-width:none">Indeksy Pegler Yorkshire (Tectite, Kuterlite) podaj w <a href="kontakt.html#formularz">formularzu zapytania</a>. Linie i parametry znajdziesz na stronach systemów <a href="zlaczki-na-wcisk-tectite.html">złączki na wcisk Tectite</a> i <a href="zlaczki-skrecane-kuterlite.html">złączki skręcane Kuterlite</a>.</p>
    </div>
  </section>
<a class="pill" id="pill" href="#zapytanie">Lista <span id="pillN">0</span></a>
'''
kat=kat.replace('<button class="mag" type="button" id="toForm" disabled><span>Przenieś do formularza</span></button>','<button class="mag" type="button" id="toForm" disabled><span>Wyślij listę do wyceny</span></button>')
page('katalog.html','Katalog złączek Besco 2026 – wyszukiwarka indeksów | Armatex','Katalog złączek Besco 2026: wyszukiwarka 1 936 indeksów z opakowaniami zbiorczymi. Zbuduj listę i wyślij ją do wyceny dla swojej hurtowni.','katalog',kat,ld_crumbs([('Katalog złączek Besco','katalog.html')]))

# ---------------- współpraca
frame='''      <figure class="frame">
        <img src="../img/hero/hero-paleta-1200.webp" srcset="../img/hero/hero-paleta-1200.webp 1200w, ../img/hero/hero-paleta-2000.webp 2000w" sizes="(max-width: 1280px) 100vw, 1280px" alt="Paleta z kartonami złączek w magazynie Armatex w Olsztynie" width="1200" height="670" loading="lazy" decoding="async">
      </figure>'''
wsp=f'''
  <section class="phead">
    <div class="wrap">
      <ol class="crumbs"><li><a href="index.html">Armatex</a></li><li aria-current="page">Współpraca</li></ol>
      <div>
        <span class="label kicker">Współpraca z hurtowniami</span>
        <h1>Zaplecze, logistyka i dokumenty.</h1>
        <p class="lead">Dystrybuujemy złączki i armaturę Besco oraz Pegler Yorkshire do hurtowni instalacyjnych w całej Polsce. Tak wygląda współpraca z nami.</p>
        <div class="phead__ctas"><a class="mag" href="{ask('Jesteśmy hurtownią i chcemy rozpocząć współpracę (Besco, Pegler Yorkshire).')}"><span>Zapytaj o wycenę</span></a></div>
      </div>
      <dl class="phead__facts">
        <div><dt class="label">Na rynku</dt><dd>od 1991</dd></div>
        <div><dt class="label">Wysyłka</dt><dd>24 h</dd></div>
        <div><dt class="label">Magazyn</dt><dd>Olsztyn</dd></div>
      </dl>
    </div>
  </section>

  <section class="section section--tight" id="zaplecze">
    <div class="wrap">
      <div class="yard__grid">
        <div>
          <span class="label kicker">Zaplecze</span>
          <h2 class="h2">Magazyn w Olsztynie.</h2>
        </div>
        <p class="lead">Trzymamy pełne stany najczęściej rotujących pozycji Besco i Pegler Yorkshire, dlatego typowe zamówienie hurtowni kompletujemy tego samego dnia. O brakach rynkowych informujemy z wyprzedzeniem, zanim zabraknie towaru na Twoich półkach.</p>
      </div>
{frame}
      <div class="facts">
        <div class="in"><h3>Logistyka</h3><ul><li>Wysyłka z magazynu w 24 godziny od potwierdzenia zamówienia.</li><li>Duże zamówienia dowozimy własnym transportem.</li><li>Zamawianie w pełnych opakowaniach producenta.</li></ul></div>
        <div class="in"><h3>Zatowarowanie</h3><ul><li>Ceny progowe dla odbiorców regularnych.</li><li>Rezerwacje stanów pod kontrakty Twoich klientów.</li><li>Wspólne planowanie dostaw przed sezonem grzewczym.</li></ul></div>
        <div class="in"><h3>Obsługa</h3><ul><li>Oferta w ciągu jednego dnia roboczego.</li><li>Sprzedaż: Piotr Stelmach, magazyn: Martyna Zielińska.</li><li>Cały program Besco i Pegler Yorkshire na jednej fakturze.</li></ul></div>
      </div>
    </div>
  </section>

{docs}

  <section class="section section--tight" id="projekty">
    <div class="wrap">
      <span class="label kicker">Poza hurtowniami</span>
      <h2 class="h2">Obsługujemy też projekty i przemysł.</h2>
      <div class="aud aud--2">
        <div class="in"><span class="label">Projekty</span><h3>Kompletacja pod większe inwestycje</h3><p>Wyceniamy całe specyfikacje, kompletujemy dostawy etapami i doradzamy zamienniki, kiedy pozycja ma długi termin.</p></div>
        <div class="in"><span class="label">Przemysł</span><h3>Utrzymanie ruchu bez przestojów</h3><p>Kształtki G-size do 80 bar, stal węglowa do sprężonego powietrza i dokumentacja wymagana przez działy UR.</p></div>
      </div>
      <div class="cta" style="margin-top:clamp(3rem,6vw,4.5rem)">
        <div><h2>Porozmawiajmy o współpracy.</h2><p>Napisz, które systemy chcesz prowadzić. Ofertę przygotujemy w ciągu jednego dnia roboczego.</p></div>
        <div class="cta__b"><a class="mag" href="kontakt.html#formularz"><span>Zapytaj o wycenę</span></a><a class="ghost" href="tel:+48513191502">513 191 502</a></div>
      </div>
    </div>
  </section>
'''
page('wspolpraca.html','Współpraca z hurtowniami – dystrybutor złączek | Armatex','Współpraca z Armatex dla hurtowni: magazyn w Olsztynie, wysyłka w 24 h, zatowarowanie na sezon, dokumenty do złączek Besco i Pegler Yorkshire.','wspolpraca',wsp,ld_crumbs([('Współpraca','wspolpraca.html')]))

# ---------------- kontakt
kon=kontakt_home.replace('<section class="section close" id="kontakt">','<section class="section close close--top" id="formularz" data-top>')
kon=kon.replace('<span class="label kicker">Kontakt</span>\n        <h2 class="h2">Porozmawiajmy o ofercie dla Twojej hurtowni.</h2>','<ol class="crumbs"><li><a href="index.html">Armatex</a></li><li aria-current="page">Kontakt</li></ol>\n        <span class="label kicker" style="margin-top:1.5rem">Kontakt</span>\n        <h1 class="h2">Porozmawiajmy o ofercie dla Twojej hurtowni.</h1>')
assert '<h1 class="h2">' in kon
kontakt=f'''
{kon}

  <section class="section section--tight">
    <div class="wrap">
      <span class="label kicker">Zanim napiszesz</span>
      <h2 class="h2">Co warto podać w zapytaniu.</h2>
      <div class="gain gain--3">
        <div class="in"><span class="label">01</span><b>Systemy lub indeksy</b><p>Które systemy chcesz prowadzić. Numery Besco zbierzesz w <a href="katalog.html">katalogu z wyszukiwarką</a>.</p></div>
        <div class="in"><span class="label">02</span><b>Szacowane ilości</b><p>Miesięcznie albo na sezon, żeby oferta od razu obejmowała dostępność.</p></div>
        <div class="in"><span class="label">03</span><b>Lokalizację hurtowni</b><p>Miasto lub województwo i preferowany sposób dostawy.</p></div>
      </div>
    </div>
  </section>
'''
page('kontakt.html','Kontakt – zapytanie ofertowe dla hurtowni | Armatex','Kontakt z Armatex: tel. 513 191 502, biuro@armatex.pl, ul. Składowa 3a, Olsztyn, pn–pt 7:00–18:00. Zapytania o złączki Besco i Pegler Yorkshire.','kontakt',kontakt,ld_crumbs([('Kontakt','kontakt.html')]))

# ---------------- strony grup produktów (Besco, Tectite, Kuterlite)
SYSD={x['slug']:x for x in SYS}
def fmt_int(n): return f'{n:,}'.replace(',',' ')
def rozm_w(n): return 'rozmiar' if n==1 else ('rozmiary' if 2<=n%10<=4 and not 12<=n%100<=14 else 'rozmiarów')
for G in GROUPS:
    ser=G['ser']; m=G['meta']; sysp=SYSD[m['sys']]; rows=G['rows']; kind=G['kind']; n=len(rows)
    sizes=[r[0] if kind!='besco' else r[2] for r in rows]
    first,last=sizes[0],sizes[-1]; rng=first if n==1 else f'{first} – {last}'
    unit=' mm' if kind=='besco' and not any(c in rng for c in '″"/MIFIAG') else ''
    rozm=rozm_w(n)
    if kind=='besco':
        h1=f'{G["full"][0].upper()+G["full"][1:]} {G["code"]}'
        title=f'{G["name"]} {G["code"]} Besco – {m["short"]} | Armatex'
        desc=f'{G["full"][0].upper()+G["full"][1:]} Besco {G["code"]}: {n} {rozm} ({rng}{unit}), {ser["bar"]}, {ser["temp"]}. Numery artykułów i opakowania zbiorcze dla hurtowni.'
        if len(desc)>160: desc=f'{G["name"]} Besco {G["code"]} ({m["short"]}): {n} {rozm} ({rng}{unit}), {ser["bar"]}. Numery artykułów i opakowania zbiorcze dla hurtowni.'
        kicker=f'Besco · {ser["name"]}'
        lead=f'{G["name"]} z linii {ser["name"][0].lower()+ser["name"][1:]}: {n} {rozm} od {first} do {last}{unit}. Zastosowanie: {ser["media"]}. {("Norma " + ser["std"] + ".") if ser["std"] else ""}'
        facts=[('Rozmiary',str(n)),('Ciśnienie',ser['bar']),('Temperatura',ser['temp'])]
        cols=['Worek','Karton']; extra=lambda r:[f'{r[3]} szt.',f'{fmt_int(r[4])} szt.']; code_of=lambda r:r[1]; size_of=lambda r:r[2]
        params=[('Linia',ser['name']),('Zastosowanie',ser['media'])]+([('Norma',ser['std'])] if ser['std'] else [])
        src='katalog Besco 2026'; en_label='Nazwa w katalogu'
    else:
        brand=G['brand']; h1=f'{G["name"]} {brand} {G["code"]}'
        title=f'{G["name"]} {G["code"]} {brand} – {ser["short"]} | Armatex'
        rng_mm=re.sub(r'(\d)mm',r'\1 mm',rng)
        desc=f'{G["name"]} {brand} {G["code"]} ({ser["name"]}): {n} {rozm} ({rng_mm}). Numery artykułów{" i opakowania zbiorcze" if kind=="kuterlite" else ""} dla hurtowni.'
        if len(desc)<=128: desc+=' Wycena w 1 dzień roboczy.'
        kicker=f'Pegler Yorkshire · {ser["name"]}'
        note=ser['note']
        if kind=='kuterlite' and 'rójnik' not in G['name']: note=re.sub(r'\s*Wymiary trójników[^.]*\.','',note).strip()
        lead=f'{G["name"]} z linii {ser["name"]}: {n} {rozm} ({rng}). Zastosowanie: {ser["media"]}. {note}'
        facts=[('Rozmiary',str(n))]+[tuple(f) for f in ser['facts'][:2]]
        if len(facts)<3: facts.append(('Producent','Pegler Yorkshire'))
        if kind=='kuterlite': cols=['Opak. 1','Opak. 2']; extra=lambda r:[f'{r[2]} szt.' if r[2] else '–',f'{fmt_int(r[3])} szt.' if r[3] else '–']
        else: cols=[]; extra=lambda r:[]
        code_of=lambda r:r[1]; size_of=lambda r:r[0]
        params=[('Linia',ser['name']),('Zastosowanie',ser['media'])]+[tuple(f) for f in ser['facts'][2:]]
        src='cennik Kuterlite, październik 2024' if kind=='kuterlite' else 'katalog Tectite 2026'; en_label='Nazwa w cenniku'
    appr=''.join(f'<span class="appr">{a}</span>' for a in m['appr'])
    if appr: params.append(('Aprobaty',appr))
    if G['en']: params.append((en_label,G['en']))
    topic=f'Proszę o ofertę: {G["name"]} {G["brand"]} {G["code"]}.'
    if kind=='besco': packs=lambda r:[('karton',r[4]),('worek',r[3])]
    elif kind=='kuterlite': packs=lambda r:[('opak.',x) for x in sorted({r[3],r[2]}-{0,None,''},reverse=True)]
    else: packs=lambda r:[]
    ths=''.join(f'<th scope="col" class="num">{c}</th>' for c in cols)
    trs='\n'.join('            <tr><th scope="row" data-l="Rozmiar">'+size_of(r)+'</th><td class="num" data-l="Nr artykułu"><code>'+code_of(r)+'</code></td>'
        +''.join(f'<td class="num" data-l="{c}">{v}</td>' for c,v in zip(cols,extra(r)))
        +f'<td class="sy-act">{qa(code_of(r),G["name"]+" "+size_of(r),packs(r))}</td></tr>' for r in rows)
    same=[x for x in groups_of(G['sid']) if x is not G]
    rel=''.join(gcard(x) for x in same)
    pdfbtn=f'<a class="ghost ghost--pdf" href="{PDF}" target="_blank" rel="noopener">Katalog PDF</a>' if kind=='besco' else f'<a class="ghost" href="{sysp["slug"]}.html#produkty">Wszystkie {sysp["name"].lower()}</a>'
    search=(f'<a class="ulink" href="katalog.html?seria={ser["id"]}#katalog">Szukaj w linii {ser["short"]}</a>' if kind=='besco'
            else f'<a class="ulink" href="{sysp["slug"]}.html#produkty">Wszystkie linie systemu</a>')
    ptxt='\n'.join(f'          <div><dt class="label">{k}</dt><dd>{v}</dd></div>' for k,v in params)
    ftxt='\n'.join(f'        <div><dt class="label">{k}</dt><dd>{v}</dd></div>' for k,v in facts)
    body=f'''
  <section class="phead">
    <div class="wrap">
      <ol class="crumbs"><li><a href="index.html">Armatex</a></li><li><a href="{sysp["slug"]}.html">{sysp["name"]}</a></li><li aria-current="page">{G["name"]} {G["code"]}</li></ol>
      <div>
        <span class="label kicker">{kicker}</span>
        <h1>{h1}</h1>
        <p class="lead">{lead.strip()}</p>
        <div class="phead__ctas"><a class="mag" href="{ask(topic)}"><span>Zapytaj o wycenę</span></a>{pdfbtn}</div>
      </div>
      <dl class="phead__facts">
{ftxt}
      </dl>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap gp">
      <figure class="gp__img{' gp__img--w' if kind!='besco' else ''}"><img src="{G["img_src"]}" alt="{G["name"]} {G["brand"]} {G["code"]}" {img_wh(G["img_src"])} decoding="async"></figure>
      <div>
        <div class="shead"><h2 class="sy-h" style="margin:0">Rozmiary i numery artykułów</h2><span class="label" style="color:var(--ink-40)">Źródło: {src}</span></div>
        <div class="sy-tw">
          <table class="sy-lines gp__t">
            <caption class="sr">{G["name"]} {G["brand"]} {G["code"]}: rozmiary i numery artykułów</caption>
            <thead><tr><th scope="col">Rozmiar</th><th scope="col" class="num">Nr artykułu</th>{ths}<th scope="col" class="qh">Ilość do zapytania</th></tr></thead>
            <tbody>
{trs}
            </tbody>
          </table>
        </div>
        <dl class="gp__p">
{ptxt}
        </dl>
      </div>
    </div>
  </section>

  <section class="section section--tight" style="padding-top:0">
    <div class="wrap">
      <div class="cta">
        <div><h2>Zapytaj o wycenę: {G["name"]} {G["code"]}.</h2><p>Dodaj rozmiary do listy przyciskiem „Dodaj” albo od razu napisz do nas. Ceny hurtowe, dostępność i terminy przygotujemy w ciągu jednego dnia roboczego.</p></div>
        <div class="cta__b"><a class="mag" href="{ask(topic)}"><span>Zapytaj o wycenę</span></a><a class="ghost" href="katalog.html#zapytanie">Moja lista</a></div>
      </div>
      {f'<div class="shead" style="margin-top:clamp(3rem,6vw,4.5rem)"><h2 class="sy-h" style="margin:0">Inne produkty w linii</h2>{search}</div><div class="gl__l" style="margin-top:1.2rem">{rel}</div>' if rel else ''}
      <p style="margin-top:2rem"><a class="ulink" href="{sysp["slug"]}.html">Wszystkie {sysp["name"].lower()}</a></p>
    </div>
  </section>
<a class="pill" id="pill" href="katalog.html#zapytanie">Lista <span id="pillN">0</span></a>
'''
    bname={'besco':'Besco','tectite':'Pegler Yorkshire','kuterlite':'Pegler Yorkshire'}[kind]
    lst=ld({"@context":"https://schema.org","@type":"ItemList","name":f'{G["full"]} {G["code"]}',
      "itemListElement":[{"@type":"ListItem","position":i,"name":f'{bname} {G["full"]} {size_of(r)}, nr art. {code_of(r)}'} for i,r in enumerate(rows,1)]})
    crumbs=ld_crumbs([(sysp['name'],sysp['slug']+'.html'),(f'{G["name"]} {G["code"]}',G['slug']+'.html')])
    page(G['slug']+'.html',title,desc,sysp['slug'],body,crumbs+lst)

# ---------------- O firmie, Poradniki, Do pobrania
import datetime as _dt
DZIS=_dt.date.today().isoformat()
def gslug(code, name_part=''):
    """Adres strony grupy produktów po kodzie (i fragmencie nazwy, gdy kod się powtarza)."""
    for G in GROUPS:
        if G['code']==code and name_part in G['name']: return G['slug']+'.html'
    raise KeyError(code)
def glink(code, text, name_part=''): return f'<a href="{gslug(code,name_part)}">{text}</a>'
def phead(crumbs, kicker, h1, lead, facts=(), ctas=''):
    cr=''.join(f'<li><a href="{u}">{n}</a></li>' for n,u in crumbs[:-1])+f'<li aria-current="page">{crumbs[-1][0]}</li>'
    fx=''.join(f'<div><dt class="label">{k}</dt><dd>{v}</dd></div>' for k,v in facts)
    return f'''
  <section class="phead">
    <div class="wrap">
      <ol class="crumbs"><li><a href="index.html">Armatex</a></li>{cr}</ol>
      <div>
        <span class="label kicker">{kicker}</span>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        {('<div class="phead__ctas">'+ctas+'</div>') if ctas else ''}
      </div>
      {('<dl class="phead__facts">'+fx+'</dl>') if fx else ''}
    </div>
  </section>
'''
CTA_BOX=f'''      <div class="cta" style="margin-top:clamp(3rem,6vw,4.5rem)">
        <div><h2>Porozmawiajmy o ofercie dla Twojej hurtowni.</h2><p>Napisz, które systemy chcesz prowadzić. Ofertę przygotujemy w ciągu jednego dnia roboczego.</p></div>
        <div class="cta__b"><a class="mag" href="kontakt.html#formularz"><span>Zapytaj o wycenę</span></a><a class="ghost" href="tel:+48513191502">513 191 502</a></div>
      </div>'''

# ---- O firmie
firma=phead([('O firmie','o-firmie.html')],'O firmie','Armatex. Dystrybutor złączek dla hurtowni.',
  'Działamy od 1991 roku i jesteśmy oficjalnym przedstawicielem Pegler Yorkshire w Polsce. Z magazynu w Olsztynie dostarczamy złączki i armaturę Besco oraz Pegler Yorkshire do hurtowni w całej Polsce.',
  [('Na rynku','od 1991'),('Indeksy','ok. 2 900'),('Wysyłka','24 h')],
  f'<a class="mag" href="{ask("Jesteśmy hurtownią i chcemy poznać ofertę Armatex.")}"><span>Zapytaj o wycenę</span></a><a class="ghost" href="wspolpraca.html">Jak współpracujemy</a>')+f'''
  <section class="section section--tight">
    <div class="wrap">
      <div class="yard__grid">
        <div>
          <span class="label kicker">Czym się zajmujemy</span>
          <h2 class="h2">Hurtownia hurtowni instalacyjnych.</h2>
        </div>
        <p class="lead">Nie sprzedajemy inwestorom i nie wykonujemy instalacji. Naszymi klientami są hurtownie, dlatego cała oferta, logistyka i obsługa są ustawione pod ich zatowarowanie: pełne opakowania producenta, stany na najczęściej rotujące pozycje i jedna faktura na cały program.</p>
      </div>
      <div class="gain gain--3">
        <div class="in"><span class="label">01</span><b>Cztery metody łączenia</b><p>Złączki zaciskane, na wcisk, skręcane i lutowane od dwóch producentów. Około 2 900 indeksów w jednym miejscu.</p></div>
        <div class="in"><span class="label">02</span><b>Magazyn w Olsztynie</b><p>ul. Składowa 3a. Typowe zamówienie hurtowni kompletujemy tego samego dnia, wysyłka w 24 godziny od potwierdzenia.</p></div>
        <div class="in"><span class="label">03</span><b>Oferta w jeden dzień</b><p>Na zapytanie odpowiadamy w ciągu jednego dnia roboczego: ceny, dostępność i terminy dostaw.</p></div>
      </div>
    </div>
  </section>

  <section class="section section--tight section--stone">
    <div class="wrap">
      <span class="label kicker">Marki</span>
      <h2 class="h2">Dwóch producentów, pełne programy.</h2>
      <div class="aud aud--2">
        <div class="in"><span class="label">Besco Fittings &amp; Connectors</span><h3>Press, gaz, stal i lutowane</h3><p>Miedź press w profilach V i M (12–108 mm), linie do gazu, stal węglowa press, kształtki lutowane EN 1254, calowe ANSI i G-size oraz zawory kulowe press. 1 936 pozycji z katalogu 2026 w naszej <a href="katalog.html">wyszukiwarce</a>. Aprobaty DVGW, KIWA, WRAS, RISE i INiG, zależnie od linii.</p></div>
        <div class="in"><span class="label">Pegler Yorkshire · oficjalny przedstawiciel w Polsce</span><h3>Tectite i Kuterlite</h3><p>Jako oficjalny przedstawiciel Pegler Yorkshire w Polsce prowadzimy złączki na wcisk <a href="zlaczki-na-wcisk-tectite.html">Tectite</a> (Classic, Pro, 316, Carbon) z gwarancją producenta 25 lat oraz złączki skręcane <a href="zlaczki-skrecane-kuterlite.html">Kuterlite</a> do miedzi i rur PE, razem z zaworami.</p></div>
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <span class="label kicker">Zespół</span>
      <h2 class="h2">Z kim rozmawiasz.</h2>
      <div class="team">
        <div class="in"><span class="team__av" aria-hidden="true">PS</span><div><span class="label">Sprzedaż</span><b>Piotr Stelmach</b><p><a href="tel:+48798807106">798 807 106</a> · <a href="mailto:piotr@armatex.pl">piotr@armatex.pl</a></p></div></div>
        <div class="in"><span class="team__av" aria-hidden="true">MZ</span><div><span class="label">Magazyn</span><b>Martyna Zielińska</b><p><a href="tel:+48515231693">515 231 693</a> · <a href="mailto:martyna@armatex.pl">martyna@armatex.pl</a></p></div></div>
        <div class="in"><span class="team__av" aria-hidden="true">B</span><div><span class="label">Biuro</span> <b>P.H.U. ARMATEX Sp. J. A. J. Bunda</b> <p>ul. Składowa 3a, 10-421 Olsztyn<br>pn–pt 7:00–18:00</p><p><a href="tel:+48513191502">513 191 502</a> · <a href="mailto:biuro@armatex.pl">biuro@armatex.pl</a></p></div></div>
      </div>
{CTA_BOX}
    </div>
  </section>
'''
page('o-firmie.html','O firmie – Armatex, dystrybutor złączek dla hurtowni','P.H.U. ARMATEX Sp. J. A. J. Bunda z Olsztyna: od 1991 r. na rynku instalacyjnym, oficjalny przedstawiciel Pegler Yorkshire w Polsce, dystrybutor Besco.','o-firmie',firma,ld_crumbs([('O firmie','o-firmie.html')]))

# ---- Poradniki
PSRC='Źródło danych: katalog Besco Fittings &amp; Connectors 2026'
ART=[]
def art(slug,title,seo,desc,lead,mins,body,rel,src=PSRC):
    ART.append(dict(slug=slug,title=title,desc=desc,lead=lead,mins=mins))
    toc=''.join(f'<li><a href="#{a}">{t}</a></li>' for a,t in re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>',body))
    rl=''.join(f'<li>{x}</li>' for x in rel)
    html=phead([('Poradniki','poradniki.html'),(title,slug+'.html')],f'Poradnik · {mins} min czytania',title,lead)+f'''
  <section class="section section--tight">
    <div class="wrap art">
      <article class="prose">
{body}
        <p class="prose__src">{src}. Stan na {DZIS[:4]} r.</p>
      </article>
      <aside class="art__side">
        <div class="art__box"><span class="label">W tym poradniku</span><ol>{toc}</ol></div>
        <div class="art__box"><span class="label">Powiązane</span><ul>{rl}</ul></div>
        <a class="mag" href="{ask('Pytanie po poradniku: '+title)}"><span>Zapytaj o wycenę</span></a>
      </aside>
    </div>
  </section>
'''
    ldart=ld({"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"inLanguage":"pl-PL",
      "datePublished":DZIS,"dateModified":DZIS,"mainEntityOfPage":SITE+slug+'.html',"image":SITE+"img/og/armatex-og.jpg",
      "author":{"@type":"Organization","name":"Armatex","url":SITE},"publisher":{"@id":SITE+"#firma"}})
    page(slug+'.html',seo,desc,'poradniki',html,ld_crumbs([('Poradniki','poradniki.html'),(title,slug+'.html')])+ldart)

art('poradnik-profil-v-czy-m','Profil V czy M? Jak dobrać złączki zaciskane do zaciskarki',
 'Profil V czy M – złączki zaciskane Besco | Armatex',
 'Czym różni się profil V od M w złączkach zaciskanych, które linie Besco są w którym profilu i jak dobrać zatowarowanie hurtowni do szczęk klientów.',
 'Złączki zaciskane różnią się kształtem końcówki, a ten musi pasować do szczęk zaciskarki. Wyjaśniamy, czym są profile V i M i jak ustawić pod nie stany hurtowni.',5,f'''
        <h2 id="co-to">Co oznacza profil złączki</h2>
        <p>W systemach press złączkę zaciska się szczęką zaciskarki. Szczęka ma określony kontur, a złączka musi mieć końcówkę o tym samym konturze, żeby zaprasowanie było szczelne. Najczęściej spotykane kontury w instalacjach miedzianych to <strong>V</strong> i <strong>M</strong>. Oznaczenie konturu jest na szczęce, więc instalator zwykle wie, w jakim profilu pracuje.</p>
        <p>Dla hurtowni oznacza to prostą rzecz: klient z szczękami V kupi złączki V, a klient z szczękami M kupi złączki M. Dwa profile to dwa osobne stany magazynowe tej samej kształtki.</p>
        <h2 id="besco">Które linie Besco są w którym profilu</h2>
        <div class="tw"><table>
          <thead><tr><th>Linia</th><th>Profil</th><th>Średnice</th><th>Parametry</th><th>Aprobaty</th></tr></thead>
          <tbody>
            <tr><td>Miedź press · woda</td><td>V</td><td>12–54 mm</td><td>16 bar, −10…110 °C</td><td>DVGW, KIWA, WRAS, RISE</td></tr>
            <tr><td>Miedź press · woda</td><td>M</td><td>12–108 mm</td><td>16 bar, −10…110 °C</td><td>DVGW, WRAS, RISE</td></tr>
            <tr><td>Miedź press · gaz</td><td>V i M</td><td>15–35 mm</td><td>5 bar, −20…70 °C</td><td>DVGW, INiG</td></tr>
            <tr><td>Stal węglowa press</td><td>M</td><td>12–108 mm</td><td>16 bar, −10…110 °C</td><td>–</td></tr>
            <tr><td>Zawory kulowe press</td><td>V i M</td><td>15–54 mm</td><td>16 bar, −10…110 °C</td><td>DVGW, WRAS</td></tr>
          </tbody>
        </table></div>
        <p>Miedź według EN 1254-7. Średnice powyżej 54 mm (do 108 mm) są w profilu M, zarówno w miedzi, jak i w stali węglowej.</p>
        <h2 id="zgodnosc">Czy M można zacisnąć szczęką V?</h2>
        <p>Według katalogu Besco 2026 złączki w profilu M można zaciskać także szczęką V w zakresie <strong>DN12–28</strong>. W tych średnicach jeden stan złączek M obsłuży klientów z oboma typami szczęk. Powyżej 28 mm trzymaj się profilu zgodnego ze szczęką.</p>
        <h2 id="stany">Jak ustawić stany w hurtowni</h2>
        <ul>
          <li><strong>Małe średnice (12–28 mm):</strong> tu jest największa rotacja. Zapytaj stałych klientów, jakimi szczękami pracują, i ustaw proporcje V do M według tej odpowiedzi.</li>
          <li><strong>Duże średnice (35–108 mm):</strong> powyżej 54 mm Besco oferuje tylko profil M, więc to on obsługuje większe inwestycje i kotłownie.</li>
          <li><strong>Gaz:</strong> linie gazowe to osobne indeksy (GPG i seria 7000). Nie zastępuje się ich złączkami z linii wodnych.</li>
          <li><strong>Pełne opakowania:</strong> każda pozycja ma w katalogu dwa opakowania zbiorcze (worek i karton), np. łuk {glink('GP5001','GP5001','Łuk 90')} 15 mm: 10 i 120 sztuk.</li>
        </ul>
        <h2 id="zamowienie">Jak zamówić</h2>
        <p>Wszystkie indeksy znajdziesz w <a href="katalog.html?seria=cu-press-water-v#katalog">wyszukiwarce profilu V</a> i <a href="katalog.html?seria=cu-press-water-m#katalog">profilu M</a>. Dodaj pozycje do listy, ustaw ilości w kartonach lub workach i wyślij do wyceny.</p>''',
 ['<a href="zlaczki-zaciskane-press.html">Złączki zaciskane press Besco</a>',glink('GP5001','Łuk 90° wz, profil V (GP5001)','Łuk 90'),glink('6001','Łuk 90° wz, profil M (6001)','Łuk 90'),'<a href="poradnik-numery-artykulow-besco.html">Jak czytać numery artykułów Besco</a>'])

art('poradnik-numery-artykulow-besco','Jak czytać numery artykułów Besco',
 'Numery artykułów Besco – jak je czytać | Armatex',
 'Budowa numeru artykułu Besco: przedrostek linii, numer kształtu, przyrostki i rozmiar. Przykłady dla press V i M, gazu, stali, lutowanych, ANSI i G-size.',
 'Numer artykułu Besco mówi, z jakiej linii jest kształtka, jaki ma kształt i rozmiar. Po tym poradniku odczytasz go bez zaglądania do katalogu.',4,f'''
        <h2 id="budowa">Budowa numeru</h2>
        <p>Większość numerów ma cztery części: <strong>przedrostek linii</strong>, <strong>numer kształtu</strong>, opcjonalny <strong>przyrostek</strong> i <strong>rozmiar</strong> po myślniku. Na przykład <code>GP5001-15</code> to łuk 90° wz z linii press V do wody, średnica 15 mm.</p>
        <h2 id="linie">Przedrostek: z jakiej linii jest kształtka</h2>
        <div class="tw"><table>
          <thead><tr><th>Początek numeru</th><th>Linia</th><th>Przykład</th></tr></thead>
          <tbody>
            <tr><td>cyfry 5… / 4…</td><td>Miedź lutowana EN 1254</td><td><code>5001-15</code></td></tr>
            <tr><td>GP</td><td>Miedź press, profil V, woda</td><td><code>GP5001-15</code></td></tr>
            <tr><td>GPG</td><td>Miedź press, profil V, gaz</td><td><code>GPG5001-15</code></td></tr>
            <tr><td>6…</td><td>Miedź press, profil M, woda</td><td>grupa <code>6001</code></td></tr>
            <tr><td>7…</td><td>Miedź press, profil M, gaz</td><td>grupa <code>7001</code></td></tr>
            <tr><td>2…</td><td>Stal węglowa press, profil M</td><td><code>2270-15</code></td></tr>
            <tr><td>K</td><td>Miedź calowa ANSI B16.22, seria K</td><td><code>K5001-1/2</code></td></tr>
            <tr><td>G</td><td>Miedź G-size do wysokich ciśnień</td><td><code>G5001-22</code></td></tr>
            <tr><td>GPV, GP600</td><td>Zawory kulowe press</td><td><code>GPV60015PP</code></td></tr>
          </tbody>
        </table></div>
        <h2 id="ksztalt">Numer kształtu</h2>
        <p>Ostatnie trzy cyfry numeru grupy oznaczają kształt i powtarzają się w różnych liniach. Łuk 90° wz to 5001 w lutowanych, GP5001 w press V, 6001 w press M i G5001 w G-size.</p>
        <div class="tw"><table>
          <thead><tr><th>Numer</th><th>Kształt</th><th>Numer</th><th>Kształt</th></tr></thead>
          <tbody>
            <tr><td>…001</td><td>Łuk 90° wz</td><td>…130</td><td>Trójnik</td></tr>
            <tr><td>…002</td><td>Łuk 90° ww</td><td>…270</td><td>Mufa</td></tr>
            <tr><td>…040</td><td>Łuk 45° wz</td><td>…240</td><td>Mufa redukcyjna ww</td></tr>
            <tr><td>…041</td><td>Łuk 45° ww</td><td>…243</td><td>Redukcja wz</td></tr>
            <tr><td>…090</td><td>Kolano 90° ww</td><td>…301</td><td>Zaślepka</td></tr>
            <tr><td>…092</td><td>Kolano 90° wz</td><td>…085 / …086</td><td>Mijanka ww / wz</td></tr>
          </tbody>
        </table></div>
        <p>W liniach lutowanej i press V pierwsza cyfra <strong>4</strong> zamiast 5 oznacza zwykle element z gwintem, np. {glink('4270','4270 (złączka z GW)')} obok {glink('5270','5270 (mufa)')}.</p>
        <h2 id="przyrostki">Przyrostki literowe</h2>
        <ul>
          <li><strong>R</strong>: wersja redukcyjna, np. {glink('6130R','6130R, trójnik redukcyjny w profilu M')}.</li>
          <li><strong>G</strong>: wersja z gwintem w profilu M i w stali, np. {glink('6090G','6090G, kolano 90° z GW')}.</li>
          <li><strong>S</strong>: wersja przesuwna, np. {glink('GP5270S','GP5270S, mufa przesuwna')}.</li>
        </ul>
        <h2 id="rozmiar">Rozmiar po myślniku</h2>
        <ul>
          <li><code>-15</code>: jedna średnica, 15 mm.</li>
          <li><code>-28.12</code>: kilka średnic oddzielonych kropką, np. mufa redukcyjna 28 × 12 mm.</li>
          <li><code>-15.1/2</code>: średnica i gwint w calach, np. śrubunek {glink('4331','4331-15.1/2')} to 15 mm × 1/2″.</li>
        </ul>
        <p>Wyjątek: w liniach press M (woda i gaz) numery artykułów w tabelach katalogu to długie kody liczbowe, np. <code>682001212</code>. Wpisz je do wyszukiwarki w całości albo szukaj po numerze grupy, np. <code>6001</code>.</p>
        <h2 id="szukaj">Szukanie po numerze</h2>
        <p>Nasza <a href="katalog.html">wyszukiwarka</a> rozpoznaje numery grup i artykułów, także bez myślnika i kropek. Wpisz np. <code>GP5001</code>, żeby zobaczyć wszystkie średnice łuku, albo pełny numer, żeby od razu dodać pozycję do listy.</p>''',
 ['<a href="katalog.html">Wyszukiwarka indeksów Besco</a>','<a href="poradnik-profil-v-czy-m.html">Profil V czy M?</a>','<a href="zlaczki-lutowane.html">Złączki lutowane Besco</a>'])

GAS_V=[G for G in groups_of('cu-press-gas-v')]
gas_list=''.join(f'<li><a href="{G["slug"]}.html">{G["name"]}</a> <code>{G["code"]}</code></li>' for G in GAS_V)
art('poradnik-zlaczki-zaciskane-do-gazu','Złączki zaciskane do gazu: parametry, aprobaty i oznaczenia',
 'Złączki zaciskane do gazu Besco – parametry i aprobaty | Armatex',
 'Złączki press do gazu Besco w profilu V i M: średnice 15–35 mm, 5 bar, −20…70 °C, EN 1254-7, aprobaty DVGW i INiG. Numery, kształty i różnice względem linii wodnych.',
 'Linie gazowe to osobne indeksy z innymi parametrami niż złączki do wody. Zebraliśmy, co trzeba wiedzieć, zanim wprowadzisz je na półkę.',4,f'''
        <h2 id="parametry">Parametry linii gazowych Besco</h2>
        <div class="tw"><table>
          <thead><tr><th></th><th>Profil V</th><th>Profil M</th></tr></thead>
          <tbody>
            <tr><td>Oznaczenie</td><td>GPG…</td><td>seria 7000</td></tr>
            <tr><td>Średnice</td><td>15–35 mm</td><td>15–35 mm</td></tr>
            <tr><td>Ciśnienie</td><td>do 5 bar</td><td>do 5 bar</td></tr>
            <tr><td>Temperatura</td><td>−20…70 °C</td><td>−20…70 °C</td></tr>
            <tr><td>Media</td><td>gaz ziemny, LPG</td><td>gaz ziemny, LPG</td></tr>
            <tr><td>Norma</td><td>EN 1254-7</td><td>EN 1254-7</td></tr>
            <tr><td>Aprobaty</td><td>DVGW, INiG</td><td>DVGW, INiG</td></tr>
            <tr><td>Pozycje w katalogu</td><td>110</td><td>101</td></tr>
          </tbody>
        </table></div>
        <h2 id="roznice">Czym różnią się od złączek do wody</h2>
        <p>Linie wodne press pracują do 16 bar i od −10 do 110 °C, a gazowe do 5 bar i od −20 do 70 °C. Do instalacji gazowych nie stosuje się złączek z linii wodnych, nawet jeśli pasują wymiarem i profilem. Dlatego w magazynie i na półce warto trzymać je osobno, z wyraźnym opisem „gaz”.</p>
        <p>Profil V lub M dobiera się tak samo jak w linii wodnej, według szczęk zaciskarki klienta. Więcej w poradniku <a href="poradnik-profil-v-czy-m.html">Profil V czy M?</a>.</p>
        <h2 id="ksztalty">Kształty w linii V (GPG)</h2>
        <ul class="cols">{gas_list}</ul>
        <h2 id="dokumenty">Dokumenty dla klientów</h2>
        <p>Przy instalacjach gazowych instalatorzy i inwestorzy częściej pytają o dokumenty. Aprobaty i deklaracje do linii gazowych udostępniamy hurtowniom w <a href="do-pobrania.html">bazie dokumentów</a> po weryfikacji. Samą instalację gazową wykonuje instalator z uprawnieniami, zgodnie z przepisami.</p>''',
 ['<a href="katalog.html?seria=cu-press-gas-v,cu-press-gas-m#katalog">Wszystkie indeksy gazowe w wyszukiwarce</a>','<a href="zlaczki-zaciskane-press.html">Złączki zaciskane press Besco</a>','<a href="do-pobrania.html">Do pobrania: katalogi i dokumenty</a>'])

art('poradnik-metody-laczenia-rur','Zaciskane, na wcisk, skręcane czy lutowane? Porównanie metod łączenia',
 'Złączki zaciskane, na wcisk, skręcane, lutowane – porównanie | Armatex',
 'Porównanie czterech metod łączenia rur: złączki zaciskane (press), na wcisk (push-fit), skręcane i lutowane. Narzędzia, średnice, rury i typowi klienci.',
 'Każda metoda łączenia ma swoich klientów. Porównujemy narzędzia, zakresy średnic i zastosowania, żeby łatwiej było ułożyć ofertę hurtowni.',5,f'''
        <h2 id="tabela">Porównanie w jednej tabeli</h2>
        <div class="tw"><table>
          <thead><tr><th></th><th>Zaciskane (press)</th><th>Na wcisk</th><th>Skręcane</th><th>Lutowane</th></tr></thead>
          <tbody>
            <tr><td>Marka w ofercie</td><td>Besco</td><td>Tectite</td><td>Kuterlite</td><td>Besco</td></tr>
            <tr><td>Narzędzia</td><td>zaciskarka ze szczękami V lub M</td><td>obcinak, gratownik, miernik głębokości</td><td>klucze</td><td>palnik, lut, topnik</td></tr>
            <tr><td>Średnice</td><td>12–108 mm</td><td>10–54 mm</td><td>6–54 mm (miedź), 20–32 mm (PE)</td><td>6–108 mm, calowe 1/4″–4 1/8″</td></tr>
            <tr><td>Rury</td><td>miedź, stal węglowa</td><td>miedź, PEX i PB z tulejką, stal zależnie od linii</td><td>miedź, PE</td><td>miedź</td></tr>
            <tr><td>Ogień przy montażu</td><td>nie</td><td>nie</td><td>nie</td><td>tak</td></tr>
            <tr><td>Demontaż</td><td>nie</td><td>Classic, Pro i 316 tak</td><td>tak, pierścień zostaje na rurze</td><td>tylko przez rozlutowanie</td></tr>
          </tbody>
        </table></div>
        <h2 id="press">Zaciskane (press)</h2>
        <p>Szybki montaż bez ognia, ale wymaga zaciskarki ze szczękami w odpowiednim profilu. Typowi klienci to firmy instalacyjne przy kotłowniach, pionach i większych inwestycjach. Besco ma także linie do gazu i stal węglową do ogrzewania i sprężonego powietrza. <a href="zlaczki-zaciskane-press.html">Złączki zaciskane Besco</a></p>
        <h2 id="wcisk">Na wcisk (push-fit)</h2>
        <p>Montaż bez zaciskarki, prądu i ognia: rurę trzeba uciąć, zgratować i wsunąć na wymaganą głębokość. Dobre do serwisu, remontów i prac w miejscach, gdzie nie można użyć palnika. Producent daje 25 lat gwarancji na Tectite Sprint, Classic, Pro i 316. <a href="zlaczki-na-wcisk-tectite.html">Złączki na wcisk Tectite</a></p>
        <h2 id="skrecane">Skręcane</h2>
        <p>Pierścień zaciska się na rurze przy dokręcaniu nakrętki. Wystarczą klucze. To klasyczny towar ladowy do podłączeń kotłów, podgrzewaczy i armatury, a seria K700 łączy też rury PE. <a href="zlaczki-skrecane-kuterlite.html">Złączki skręcane Kuterlite</a></p>
        <h2 id="lutowane">Lutowane</h2>
        <p>Kształtki kapilarne do lutowania miękkiego i twardego. Najszerszy zakres średnic i rozmiarów, w tym calowe ANSI B16.22 i G-size do 80 bar dla chłodnictwa i przemysłu. <a href="zlaczki-lutowane.html">Złączki lutowane Besco</a></p>
        <h2 id="oferta">Co to oznacza dla hurtowni</h2>
        <p>Te metody nie konkurują ze sobą, tylko obsługują różnych klientów: instalatora z zaciskarką, serwisanta bez narzędzi, klienta przy ladzie i chłodnika. Pełna oferta czterech metod od jednego dostawcy pozwala obsłużyć ich wszystkich z jednej faktury.</p>''',
 ['<a href="index.html#systemy">Wszystkie systemy złączek</a>','<a href="poradnik-profil-v-czy-m.html">Profil V czy M?</a>','<a href="poradnik-zlaczki-zaciskane-do-gazu.html">Złączki zaciskane do gazu</a>'],
 src='Źródło danych: katalogi Besco 2026 i Tectite 2026, cennik Kuterlite (październik 2024)')

# ---- Poradniki: stal, Tectite czy press, Kuterlite a press, PE, aprobaty
art('poradnik-zlaczki-do-stali-weglowej','Złączki do stali węglowej: gdzie wolno, a gdzie nie',
 'Złączki do stali węglowej – gdzie stosować | Armatex',
 'Gdzie stosować złączki do rur ze stali węglowej: ogrzewanie, chłodzenie, sprężone powietrze. Czego unikać: woda pitna i układy otwarte. Besco press i Tectite.',
 'Złączki do stali węglowej są tańsze i mocne, ale nie wszędzie się nadają. Zebraliśmy, do czego przewidują je producenci i gdzie lepiej sięgnąć po miedź lub stal nierdzewną.',5,f'''
        <h2 id="zastosowania">Do czego producenci przewidują stal węglową</h2>
        <p>W naszej ofercie są trzy rozwiązania do rur ze stali węglowej. Każde ma w katalogu producenta jasno opisane zastosowanie:</p>
        <div class="tw"><table>
          <thead><tr><th></th><th>Besco stal węglowa press</th><th>Tectite Carbon</th><th>Tectite Pro z rurą stalową</th></tr></thead>
          <tbody>
            <tr><td>Połączenie</td><td>zaciskane, profil M</td><td>na wcisk, niedemontowalne</td><td>na wcisk, demontowalne</td></tr>
            <tr><td>Średnice</td><td>12–108 mm</td><td>15–54 mm</td><td>15–54 mm</td></tr>
            <tr><td>Zastosowanie wg katalogu</td><td>ogrzewanie, sprężone powietrze</td><td>niewentylowane, zamknięte obiegi grzewcze i chłodzące</td><td>tylko obiegi zamknięte</td></tr>
            <tr><td>Parametry</td><td>16 bar, −10…110 °C</td><td>20 bar do 30 °C, 16 bar przy 65 °C, 10 bar przy 114 °C</td><td>jak Tectite Pro z miedzią, w obiegu zamkniętym</td></tr>
            <tr><td>Rury</td><td>stal węglowa</td><td>stal węglowa, także pokryta tworzywem</td><td>stal węglowa ocynkowana, miedź, PEX, PB</td></tr>
          </tbody>
        </table></div>
        <p>Wspólny mianownik: <strong>układy zamknięte</strong>, czyli instalacje grzewcze i chłodzące, w których krąży ta sama woda, oraz sprężone powietrze w linii Besco.</p>
        <h2 id="gdzie-nie">Gdzie stali węglowej nie stosować</h2>
        <ul>
          <li><strong>Woda pitna, ciepła i zimna woda użytkowa.</strong> Żaden z tych katalogów nie przewiduje stali węglowej do wody pitnej. Tu sprawdzą się miedź press Besco, <a href="zlaczki-na-wcisk-tectite.html">Tectite Classic i Sprint</a> z atestem PZH albo Tectite 316 ze stali nierdzewnej.</li>
          <li><strong>Układy otwarte.</strong> Tectite Carbon jest opisany wyłącznie do niewentylowanych obiegów zamkniętych, a Tectite Pro z rurą stalową tylko do obiegów zamkniętych. W układzie otwartym do wody stale dopływa świeży tlen, a stal węglowa w natlenionej wodzie koroduje.</li>
          <li><strong>Gaz.</strong> Besco nie opisuje stali press do gazu. Do instalacji gazowych mamy osobne linie z miedzi (GPG i seria 7000) z aprobatami DVGW i INiG. Więcej w poradniku <a href="poradnik-zlaczki-zaciskane-do-gazu.html">Złączki zaciskane do gazu</a>.</li>
        </ul>
        <h2 id="nierdzewna">Stal węglowa to nie stal nierdzewna</h2>
        <p>Nazwy są podobne, ale to dwa różne materiały. Tectite 316 jest ze stali nierdzewnej i według producenta jest projektowany do instalacji wody pitnej oraz przemysłu spożywczego i farmaceutycznego. Złączki do stali węglowej łączą rury stalowe w ogrzewaniu i chłodzeniu. Nie zamienia się ich między sobą i nie łączy z rurami innego rodzaju niż przewiduje producent.</p>
        <h2 id="hurtownia">Co to oznacza dla hurtowni</h2>
        <ul>
          <li><strong>Pytaj o medium.</strong> Przy zamówieniu złączek do stali warto dopytać, czy chodzi o ogrzewanie, chłodzenie czy wodę użytkową. Jedno pytanie oszczędza reklamację.</li>
          <li><strong>Opisz półkę.</strong> Kształtki stalowe i miedziane press wyglądają inaczej, ale stalowe z różnych systemów łatwo pomylić. Wyraźny opis „stal węglowa, obiegi zamknięte” pomaga przy ladzie.</li>
          <li><strong>Profil M.</strong> Linia stalowa Besco jest w profilu M, więc klient potrzebuje szczęk M. Zobacz poradnik <a href="poradnik-profil-v-czy-m.html">Profil V czy M?</a></li>
        </ul>
        <h2 id="zamowienie">Jak zamówić</h2>
        <p>Wszystkie kształtki stalowe Besco znajdziesz w <a href="katalog.html?seria=steel-press-m#katalog">wyszukiwarce</a>, np. {glink('2270','mufa 2270','Mufa')}, {glink('2001','łuk 90° wz 2001','Łuk 90')} czy {glink('2510','kołnierz PN 16 2510','Kołnierz')}. Tectite Carbon i Pro wycenimy na zapytanie.</p>''',
 ['<a href="zlaczki-zaciskane-press.html">Złączki zaciskane press Besco</a>','<a href="zlaczki-na-wcisk-tectite.html">Złączki na wcisk Tectite</a>','<a href="poradnik-tectite-czy-press.html">Tectite czy press?</a>','<a href="poradnik-profil-v-czy-m.html">Profil V czy M?</a>'],
 src='Źródło danych: katalogi Besco 2026 i Tectite 2026')

art('poradnik-tectite-czy-press','Tectite czy press? Kiedy złączki na wcisk, a kiedy zaciskane',
 'Tectite czy press – złączki na wcisk czy zaciskane | Armatex',
 'Złączki na wcisk Tectite czy zaciskane press Besco? Porównanie narzędzi, średnic, rur, ciśnień i temperatur. Kiedy które wybrać i jak ułożyć ofertę hurtowni.',
 'Obie metody łączą rury bez ognia, ale sprawdzają się w innych sytuacjach. Porównujemy Tectite i press Besco na danych z katalogów producentów.',5,f'''
        <h2 id="porownanie">Porównanie w jednej tabeli</h2>
        <div class="tw"><table>
          <thead><tr><th></th><th>Na wcisk Tectite</th><th>Zaciskane press Besco</th></tr></thead>
          <tbody>
            <tr><td>Narzędzia</td><td>obcinak, gratownik, znacznik głębokości</td><td>zaciskarka ze szczękami V lub M</td></tr>
            <tr><td>Średnice</td><td>10–54 mm (zależnie od linii)</td><td>12–108 mm</td></tr>
            <tr><td>Rury</td><td>miedź, PEX i PB z tulejką, stal węglowa (Pro, Carbon), stal nierdzewna (316)</td><td>miedź; stal węglowa w osobnej linii</td></tr>
            <tr><td>Demontaż</td><td>Classic, Pro i 316 tak; Sprint i Carbon nie</td><td>nie</td></tr>
            <tr><td>Gaz</td><td>do gazu polecamy linie press Besco</td><td>osobne linie GPG i seria 7000, DVGW i INiG</td></tr>
            <tr><td>Gwarancja producenta</td><td>25 lat (Sprint, Classic, Pro, 316), 30 lat z rurami Yorkshire</td><td>–</td></tr>
          </tbody>
        </table></div>
        <h2 id="parametry">Ciśnienie i temperatura</h2>
        <p>Press Besco do wody pracuje do <strong>16 bar</strong> w zakresie <strong>−10…110 °C</strong>. W Tectite dopuszczalne ciśnienie zależy od linii, rury i temperatury:</p>
        <div class="tw"><table>
          <thead><tr><th>Tectite z rurą</th><th>do 30 °C</th><th>65 °C</th><th>maks. temperatura</th></tr></thead>
          <tbody>
            <tr><td>Sprint, Pro (do 28 mm), 316 (do 28 mm) · miedź lub stal nierdzewna</td><td>20 bar</td><td>16 bar</td><td>10 bar przy 114 °C</td></tr>
            <tr><td>Pro i 316 (od 35 mm)</td><td>16 bar</td><td>10 bar</td><td>6 bar przy 90 °C</td></tr>
            <tr><td>Classic · miedź</td><td>16 bar</td><td>10 bar</td><td>6 bar przy 95 °C</td></tr>
            <tr><td>Sprint, Classic · PEX lub PB</td><td>12 bar (do 20 °C)</td><td>6 bar</td><td>3 bar przy 92 °C</td></tr>
          </tbody>
        </table></div>
        <p>Minimalna temperatura w tabeli Tectite to −24 °C z miedzią i −20 °C z PEX. Producent zaleca próbę ciśnieniową każdego układu po montażu, ciśnieniem do 1,5 raza wyższym od roboczego.</p>
        <h2 id="tectite">Kiedy Tectite</h2>
        <ul>
          <li><strong>Serwis i remonty:</strong> bez zaciskarki, prądu i palnika. Wystarczy uciąć rurę prostopadle, zgratować, zaznaczyć głębokość i wsunąć.</li>
          <li><strong>Miejsca, gdzie nie wolno użyć ognia</strong> ani nie zmieści się zaciskarka.</li>
          <li><strong>Rury z tworzywa:</strong> PEX i PB z tulejką, także przejścia z miedzi na tworzywo w jednym systemie.</li>
          <li><strong>Gdy liczy się demontaż:</strong> Classic, Pro i 316 można rozłączyć, np. przy tymczasowych podłączeniach.</li>
        </ul>
        <h2 id="press">Kiedy press</h2>
        <ul>
          <li><strong>Nowe inwestycje i duże średnice:</strong> press Besco w profilu M sięga 108 mm, Tectite 54 mm.</li>
          <li><strong>Gaz:</strong> do instalacji gazowych mamy linie press z aprobatami DVGW i INiG.</li>
          <li><strong>Firmy z zaciskarką:</strong> dla nich press to szybki, powtarzalny montaż. Profil dobiera się do szczęk, zobacz <a href="poradnik-profil-v-czy-m.html">Profil V czy M?</a></li>
        </ul>
        <h2 id="hurtownia">Co to oznacza dla hurtowni</h2>
        <p>Tectite i press nie konkurują, tylko obsługują różnych klientów: serwisanta i instalatora bez zaciskarki oraz firmę wykonawczą przy większych instalacjach. Oba systemy są w naszej ofercie, więc hurtownia zamówi je na jednej fakturze.</p>''',
 ['<a href="zlaczki-na-wcisk-tectite.html">Złączki na wcisk Tectite</a>','<a href="zlaczki-zaciskane-press.html">Złączki zaciskane press Besco</a>','<a href="poradnik-metody-laczenia-rur.html">Porównanie czterech metod łączenia</a>','<a href="poradnik-zlaczki-do-stali-weglowej.html">Złączki do stali węglowej</a>'],
 src='Źródło danych: katalogi Besco 2026 i Tectite 2026')

art('poradnik-kuterlite-a-zlaczki-zaciskane','Kuterlite a złączki zaciskane: czym się różnią złączki skręcane od press',
 'Złączki skręcane Kuterlite a zaciskane press | Armatex',
 'Złączki zaciskowe (skręcane) Kuterlite i zaciskane press to dwa różne systemy. Różnice: narzędzia, pierścień, średnice, rury, demontaż, zastosowania.',
 '„Zaciskowe” i „zaciskane” brzmią prawie tak samo, ale to dwie różne metody łączenia. Wyjaśniamy, czym Kuterlite różni się od złączek press i kiedy które wybrać.',4,f'''
        <h2 id="nazwy">Zaciskowe czy zaciskane: skąd pomyłka</h2>
        <p><strong>Złączki zaciskowe</strong> to potoczna nazwa złączek skręcanych: na rurę zakłada się nakrętkę i pierścień zaciskowy, a przy dokręcaniu nakrętki pierścień zaciska się na rurze. Tak działa <a href="zlaczki-skrecane-kuterlite.html">Kuterlite</a>. <strong>Złączki zaciskane (press)</strong> zaciska się zaciskarką ze szczęką o określonym profilu, tak działa <a href="zlaczki-zaciskane-press.html">press Besco</a>. Klient, który prosi o „zaciskowe”, zwykle ma na myśli skręcane, ale warto dopytać.</p>
        <h2 id="porownanie">Porównanie</h2>
        <div class="tw"><table>
          <thead><tr><th></th><th>Skręcane (zaciskowe) Kuterlite</th><th>Zaciskane press Besco</th></tr></thead>
          <tbody>
            <tr><td>Jak powstaje połączenie</td><td>nakrętka i pierścień zaciskowy, dokręcane kluczem</td><td>szczęka zaciskarki zaciska końcówkę złączki</td></tr>
            <tr><td>Narzędzia</td><td>klucze</td><td>zaciskarka ze szczękami V lub M</td></tr>
            <tr><td>Średnice</td><td>miedź 6–54 mm, PE 20–32 mm</td><td>12–108 mm</td></tr>
            <tr><td>Rury</td><td>miedź, PE (seria K700), rury calowe z pierścieniem K978C</td><td>miedź; stal węglowa w osobnej linii</td></tr>
            <tr><td>Demontaż</td><td>tak, pierścień zostaje na rurze</td><td>nie</td></tr>
            <tr><td>Części zamienne</td><td>osobno nakrętki i pierścienie, np. {"<a href='kuterlite-pierscien-zaciskowy-k978b.html'>K978B</a>"}</td><td>–</td></tr>
          </tbody>
        </table></div>
        <h2 id="serie">Serie Kuterlite</h2>
        <ul>
          <li><strong>K600:</strong> seria podstawowa do rur miedzianych 6–28 mm, np. <a href="kuterlite-zlaczka-prosta-k610.html">złączka prosta K610</a>.</li>
          <li><strong>K900 Pro:</strong> złączki, kolana i przejścia GW/GZ do miedzi 8–54 mm. Końcówki typu A są do miedzi półtwardej (EN 1057 R250), a adapter <a href="kuterlite-adapter-typ-a-x-typ-b-do-miedzi-miekkiej-k900.html">K1870X</a> zmienia je na typ B do miedzi miękkiej (R220).</li>
          <li><strong>K700:</strong> złączki do rur PE oraz przejścia PE × miedź i PE × gwint. Więcej w poradniku <a href="poradnik-zlaczki-do-rur-pe.html">Dobór złączki do rury PE</a>.</li>
        </ul>
        <h2 id="kiedy">Kiedy które</h2>
        <ul>
          <li><strong>Skręcane:</strong> podłączenia kotłów, podgrzewaczy i armatury, naprawy, miejsca, gdzie połączenie może trzeba będzie rozebrać. To towar ladowy: wystarczą klucze.</li>
          <li><strong>Zaciskane press:</strong> całe instalacje, piony, kotłownie, duże średnice i gaz (osobne linie z aprobatami DVGW i INiG).</li>
        </ul>
        <h2 id="hurtownia">Co to oznacza dla hurtowni</h2>
        <p>Skręcane i press to dwie osobne grupy klientów i dwa osobne stany. Przy skręcanych opłaca się trzymać też nakrętki i pierścienie na sztuki, bo klienci dokupują je przy naprawach.</p>''',
 ['<a href="zlaczki-skrecane-kuterlite.html">Złączki skręcane Kuterlite</a>','<a href="zlaczki-zaciskane-press.html">Złączki zaciskane press Besco</a>','<a href="poradnik-zlaczki-do-rur-pe.html">Dobór złączki do rury PE</a>','<a href="poradnik-metody-laczenia-rur.html">Porównanie metod łączenia</a>'],
 src='Źródło danych: katalog Besco 2026, cennik Kuterlite (październik 2024)')

art('poradnik-zlaczki-do-rur-pe','Dobór złączki do rury PE: rozmiary, tulejki i przejścia',
 'Złączki do rur PE – jak dobrać | Armatex',
 'Jak dobrać złączkę skręcaną do rury PE: średnice 20, 25 i 32 mm, tulejka wzmacniająca, przejścia PE × miedź i PE × gwint, rury calowe. Seria Kuterlite K700.',
 'Rura PE, np. na przyłączu wody, często trzeba połączyć z miedzią albo gwintem. Pokazujemy, jak w pięciu krokach dobrać złączkę z serii Kuterlite K700.',4,f'''
        <h2 id="kroki">Dobór w pięciu krokach</h2>
        <ol>
          <li><strong>Średnica zewnętrzna rury.</strong> Kształtki K700 są w rozmiarach <strong>20, 25 i 32 mm</strong>. Rozmiar złączki to średnica zewnętrzna rury PE.</li>
          <li><strong>Metryczna czy calowa?</strong> Stare rury calowe (normy BS 1972 i BS 3284) łączy się przez adapter <a href="kuterlite-adapter-pe-metryczny-x-calowy-k710im.html">K710IM</a>: 20 mm × 1/2″, 25 mm × 3/4″, 32 mm × 1″.</li>
          <li><strong>Na co przechodzimy?</strong> PE × PE, PE × miedź albo PE × gwint (tabela niżej).</li>
          <li><strong>Tulejka wzmacniająca.</strong> <a href="kuterlite-tulejka-wzmacniajaca-k766m.html">K766M</a> w rozmiarze rury (20–63 mm). Do rur calowych BS 1972 klasy C jest <a href="kuterlite-tulejka-wzmacniajaca-k1766c.html">K1766C</a> (3/8″, 1/2″, 3/4″).</li>
          <li><strong>Części zamienne.</strong> Nakrętki <a href="kuterlite-nakretka-zaciskowa-k778a.html">K778A</a> i pierścienie <a href="kuterlite-pierscien-zaciskowy-k778b.html">K778B</a> są też na sztuki, w rozmiarach 20, 25, 32 i 63 mm.</li>
        </ol>
        <h2 id="przejscia">Przejścia z rury PE</h2>
        <div class="tw"><table>
          <thead><tr><th>Potrzeba</th><th>Złączka</th><th>Rozmiary</th></tr></thead>
          <tbody>
            <tr><td>PE × PE, prosto</td><td><a href="kuterlite-zlaczka-prosta-pe-x-pe-k710.html">K710</a></td><td>20, 25, 32 mm; redukcje 25 × 20 i 32 × 25 mm</td></tr>
            <tr><td>PE × miedź, skręcane</td><td><a href="kuterlite-zlaczka-prosta-pe-x-miedz-k710kp.html">K710KP</a></td><td>20 × 15, 25 × 22, 32 × 28 mm</td></tr>
            <tr><td>PE × miedź, do lutowania</td><td><a href="kuterlite-adapter-pe-x-miedz-do-lutowania-k701.html">K701</a> (z pierścieniem lutu bezołowiowego)</td><td>25 × 22, 32 × 28 mm</td></tr>
            <tr><td>PE × gwint zewnętrzny</td><td><a href="kuterlite-zlaczka-z-gz-gwint-stozkowy-pe-k711.html">K711</a>, kolano <a href="kuterlite-kolano-z-gz-gwint-stozkowy-pe-k716.html">K716</a></td><td>20 × 1/2″, 25 × 3/4″, 32 × 1″</td></tr>
            <tr><td>PE × gwint wewnętrzny</td><td><a href="kuterlite-zlaczka-z-gw-pe-k712.html">K712</a>, kolano <a href="kuterlite-kolano-z-gw-pe-k717.html">K717</a>, ścienne <a href="kuterlite-kolano-scienne-z-gw-pe-k717w.html">K717W</a></td><td>20 × 1/2″, 25 × 3/4″, 32 × 1″</td></tr>
            <tr><td>Rozgałęzienie</td><td>trójniki <a href="kuterlite-trojnik-rownoprzelotowy-pe-k718.html">K718</a>, <a href="kuterlite-trojnik-z-redukcja-odejscia-pe-k718b.html">K718B</a>, <a href="kuterlite-trojnik-z-odejsciem-gw-pe-k730.html">K730</a></td><td>20, 25, 32 mm</td></tr>
          </tbody>
        </table></div>
        <p>Redukcję rozmiaru PE da się też zrobić zestawem <a href="kuterlite-zestaw-redukcyjny-k748r.html">K748R</a> (25 × 20, 32 × 20, 32 × 25 mm).</p>
        <h2 id="uwagi">Zanim wydasz towar</h2>
        <ul>
          <li>Zapytaj klienta o średnicę zewnętrzną rury, a nie o „cal”. Rura PE 25 mm to nie rura 3/4″.</li>
          <li>Do każdej złączki PE doliczaj tulejkę wzmacniającą w rozmiarze rury.</li>
          <li>Ciśnienie i zastosowanie instalacji zależą także od samej rury PE. Przy nietypowym zastosowaniu potwierdzimy dobór z dokumentacją producenta.</li>
        </ul>''',
 ['<a href="zlaczki-skrecane-kuterlite.html">Złączki skręcane Kuterlite</a>','<a href="poradnik-kuterlite-a-zlaczki-zaciskane.html">Kuterlite a złączki zaciskane</a>','<a href="poradnik-metody-laczenia-rur.html">Porównanie metod łączenia</a>'],
 src='Źródło danych: cennik Kuterlite (październik 2024)')

art('poradnik-aprobaty-dvgw-kiwa-wras','Aprobaty DVGW, KIWA, WRAS, RISE i INiG: co oznaczają',
 'Aprobaty DVGW, KIWA, WRAS, RISE, INiG – co oznaczają | Armatex',
 'Co oznaczają aprobaty DVGW, KIWA, WRAS, RISE i INiG na złączkach, które linie Besco i Tectite je mają i jakie dokumenty są potrzebne w Polsce: atest PZH i DoP.',
 'Na złączkach i w katalogach widać skróty kilku instytucji z różnych krajów. Wyjaśniamy, co każdy z nich oznacza i o jakie dokumenty pytają klienci w Polsce.',5,f'''
        <h2 id="skroty">Co oznacza każdy skrót</h2>
        <div class="tw"><table>
          <thead><tr><th>Skrót</th><th>Instytucja i kraj</th><th>Czego dotyczy</th></tr></thead>
          <tbody>
            <tr><td><strong>DVGW</strong></td><td>Deutscher Verein des Gas- und Wasserfaches, Niemcy</td><td>certyfikacja wyrobów do instalacji gazowych i wodnych</td></tr>
            <tr><td><strong>KIWA</strong></td><td>Kiwa, Holandia</td><td>certyfikacja wyrobów do instalacji wodnych, m.in. wody pitnej</td></tr>
            <tr><td><strong>WRAS</strong></td><td>Water Regulations Advisory Scheme, Wielka Brytania</td><td>zgodność z brytyjskimi przepisami o armaturze wodnej (Water Supply (Water Fittings) Regulations 1999)</td></tr>
            <tr><td><strong>RISE</strong></td><td>Research Institutes of Sweden, Szwecja</td><td>badania i certyfikacja wyrobów, m.in. instalacyjnych</td></tr>
            <tr><td><strong>INiG</strong></td><td>Instytut Nafty i Gazu – Państwowy Instytut Badawczy, Polska</td><td>badania i certyfikacja wyrobów dla gazownictwa</td></tr>
            <tr><td><strong>PZH</strong></td><td>Narodowy Instytut Zdrowia Publicznego PZH – Państwowy Instytut Badawczy, Polska</td><td>atest higieniczny: wyrób może mieć kontakt z wodą przeznaczoną do spożycia</td></tr>
          </tbody>
        </table></div>
        <p>Obok aprobat w katalogach pojawia się norma. <strong>EN 1254-7</strong> to europejska norma dla złączek z końcówkami zaciskanymi (press) do rur metalowych, a <strong>EN 1254</strong> w ogóle obejmuje złączki z miedzi i jej stopów.</p>
        <h2 id="linie">Które linie mają które aprobaty</h2>
        <div class="tw"><table>
          <thead><tr><th>Linia</th><th>Aprobaty wg katalogu</th></tr></thead>
          <tbody>
            <tr><td>Besco miedź press, profil V · woda</td><td>DVGW, KIWA, WRAS, RISE</td></tr>
            <tr><td>Besco miedź press, profil M · woda</td><td>DVGW, WRAS, RISE</td></tr>
            <tr><td>Besco miedź press do gazu, V i M</td><td>DVGW, INiG</td></tr>
            <tr><td>Besco lutowane EN 1254</td><td>DVGW, KIWA, WRAS</td></tr>
            <tr><td>Besco zawory kulowe press</td><td>DVGW, WRAS</td></tr>
            <tr><td>Tectite Sprint i Classic</td><td>WRAS, PZH</td></tr>
            <tr><td>Tectite Pro i 316</td><td>WRAS</td></tr>
          </tbody>
        </table></div>
        <p>Aprobata może obejmować tylko część średnic albo zastosowań danej linii. Zakres i ważność zawsze potwierdza sam certyfikat.</p>
        <h2 id="polska">Jakie dokumenty są potrzebne w Polsce</h2>
        <p>Zagraniczne aprobaty są mocnym argumentem jakościowym: wyrób przeszedł badania w kraju o wysokich wymaganiach. Na polskiej budowie klienci najczęściej pytają jednak o dwa dokumenty:</p>
        <ul>
          <li><strong>Atest higieniczny PZH</strong> przy instalacjach wody pitnej.</li>
          <li><strong>Deklarację właściwości użytkowych (DoP)</strong>, którą producent wystawia dla wyrobu budowlanego.</li>
        </ul>
        <p>Przy instalacjach gazowych częściej pojawia się pytanie o certyfikat INiG. Co dokładnie jest wymagane w danej inwestycji, określa projekt i inspektor nadzoru.</p>
        <h2 id="dokumenty">Jak zdobyć dokumenty</h2>
        <p>Atesty, deklaracje i certyfikaty do linii Besco i Pegler Yorkshire udostępniamy hurtowniom w <a href="do-pobrania.html">bazie dokumentów</a> po weryfikacji. Jeśli klient pyta o konkretny indeks, podaj jego numer w <a href="kontakt.html#formularz">zapytaniu</a>, a dobierzemy właściwy dokument.</p>''',
 ['<a href="do-pobrania.html">Do pobrania: katalogi i dokumenty</a>','<a href="poradnik-zlaczki-zaciskane-do-gazu.html">Złączki zaciskane do gazu</a>','<a href="zlaczki-zaciskane-press.html">Złączki zaciskane press Besco</a>','<a href="zlaczki-na-wcisk-tectite.html">Złączki na wcisk Tectite</a>'],
 src='Źródło danych: katalogi Besco 2026 i Tectite 2026')

cards=''.join(f'<a class="pcard2" href="{a["slug"]}.html"><span class="label">Poradnik · {a["mins"]} min</span><b>{a["title"]}</b><p>{a["lead"]}</p><span class="pcard2__go" aria-hidden="true">Czytaj →</span></a>' for a in ART)
porad=phead([('Poradniki','poradniki.html')],'Poradniki','Poradniki dla hurtowni instalacyjnych.',
  'Praktyczna wiedza o złączkach Besco i Pegler Yorkshire: dobór profilu, numery artykułów, gaz, stal węglowa, rury PE, porównania metod łączenia i aprobaty.')+f'''
  <section class="section section--tight">
    <div class="wrap">
      <div class="pgrid">{cards}</div>
{CTA_BOX}
    </div>
  </section>
'''
page('poradniki.html','Poradniki o złączkach dla hurtowni | Armatex','Poradniki o złączkach Besco i Pegler Yorkshire: profil V czy M, gaz, stal węglowa, rury PE, Tectite czy press, Kuterlite, aprobaty DVGW, KIWA i WRAS.','poradniki',porad,
  ld_crumbs([('Poradniki','poradniki.html')])+ld({"@context":"https://schema.org","@type":"ItemList","name":"Poradniki Armatex","itemListElement":[{"@type":"ListItem","position":i,"url":SITE+a['slug']+'.html',"name":a['title']} for i,a in enumerate(ART,1)]}))

# ---- Do pobrania
DOCS=[
 ('besco','katalog','Katalog Besco Fittings &amp; Connectors 2026','Pełny katalog: press V i M, gaz, stal, lutowane, ANSI, G-size, zawory. Numery artykułów i opakowania.','PDF · 2,7 MB · 65 stron',f'<a class="ghost ghost--pdf" href="{PDF}" target="_blank" rel="noopener">Pobierz</a>'),
 ('besco','katalog','Wyszukiwarka indeksów Besco','1 936 pozycji z katalogu 2026 z listą do wyceny. Szybsza niż przeglądanie PDF.','online','<a class="ghost" href="katalog.html">Otwórz</a>'),
 ('pegler','katalog','Katalog Tectite 2026','Złączki i zawory na wcisk Pegler Yorkshire: Classic, Pro, 316, Carbon, akcesoria Tec-Tools.','PDF · wyślemy e-mailem',f'<a class="ghost" href="{ask("Prosimy o przesłanie katalogu Tectite 2026.")}">Poproś</a>'),
 ('besco pegler','atest','Atesty higieniczne','Atesty PZH do złączek stosowanych w instalacjach wody pitnej.','dla hurtowni po weryfikacji',f'<a class="ghost" href="{ask("Jesteśmy hurtownią i prosimy o dostęp do atestów higienicznych.")}">Poproś o dostęp</a>'),
 ('besco pegler','dop','Deklaracje właściwości użytkowych','Deklaracje DoP do wyrobów budowlanych, do przekazania klientom i inwestorom.','dla hurtowni po weryfikacji',f'<a class="ghost" href="{ask("Jesteśmy hurtownią i prosimy o dostęp do deklaracji właściwości użytkowych.")}">Poproś o dostęp</a>'),
 ('besco pegler','aprobata','Certyfikaty i aprobaty producentów','DVGW, KIWA, WRAS, RISE, INiG, zależnie od linii produktów.','dla hurtowni po weryfikacji',f'<a class="ghost" href="{ask("Jesteśmy hurtownią i prosimy o dostęp do certyfikatów i aprobat.")}">Poproś o dostęp</a>'),
]
TYPES=[('','Wszystko'),('katalog','Katalogi'),('atest','Atesty'),('dop','Deklaracje'),('aprobata','Aprobaty')]
BRANDS=[('','Obie marki'),('besco','Besco'),('pegler','Pegler Yorkshire')]
chips=lambda k,L: ''.join(f'<button type="button" class="chip" data-{k}="{v}" aria-pressed="{str(not v).lower()}">{n}</button>' for v,n in L)
rows=''.join(f'<li data-b="{b}" data-t="{t}"><div><b>{n}</b><p>{d}</p></div><span class="label">{m}</span>{btn}</li>' for b,t,n,d,m,btn in DOCS)
dl=phead([('Do pobrania','do-pobrania.html')],'Do pobrania','Katalogi i dokumenty.',
  'Katalogi pobierzesz od razu. Atesty, deklaracje i aprobaty udostępniamy hurtowniom po weryfikacji, w ciągu jednego dnia roboczego.',
  [('Katalog Besco','PDF'),('Dokumenty','po weryfikacji')])+f'''
  <section class="section section--tight">
    <div class="wrap">
      <div class="dlf" role="group" aria-label="Filtr dokumentów">
        <div class="dlf__g"><span class="label">Rodzaj</span>{chips('t',TYPES)}</div>
        <div class="dlf__g"><span class="label">Marka</span>{chips('b',BRANDS)}</div>
      </div>
      <ul class="dll" id="dll">{rows}</ul>
      <p class="dll__none" id="dllNone" hidden>Brak dokumentów dla tego filtra.</p>
{CTA_BOX}
    </div>
  </section>
'''
page('do-pobrania.html','Do pobrania: katalogi i dokumenty złączek | Armatex','Katalog Besco 2026 do pobrania, katalog Tectite oraz atesty, deklaracje właściwości użytkowych i aprobaty dla hurtowni po weryfikacji.','do-pobrania',dl,ld_crumbs([('Do pobrania','do-pobrania.html')]))


# ---- Polityka prywatności
POL_OD='27 września 2026 r.'
pol_body='''
        <p>Ta polityka opisuje, jakie dane osobowe zbieramy przez stronę armatex.pl, w jakim celu, jak długo je przechowujemy i jakie prawa Ci przysługują. Opisuje też, jakie informacje strona zapisuje w Twojej przeglądarce.</p>

        <h2 id="administrator">1. Administrator danych</h2>
        <p>Administratorem danych osobowych jest <strong>P.H.U. ARMATEX Sp. J. A. J. Bunda</strong> z siedzibą w Olsztynie, ul. Siewna 24, 10-831 Olsztyn, wpisana do rejestru przedsiębiorców Krajowego Rejestru Sądowego pod numerem KRS 0000371628, NIP 7393814110, REGON 280563743 (dalej: „Armatex”).</p>
        <p>W sprawach dotyczących danych osobowych możesz się z nami skontaktować:</p>
        <ul>
          <li>e-mailem: <a href="mailto:biuro@armatex.pl">biuro@armatex.pl</a>,</li>
          <li>telefonicznie: <a href="tel:+48513191502">513 191 502</a>,</li>
          <li>listownie: ul. Składowa 3a, 10-421 Olsztyn (biuro i magazyn) lub na adres siedziby.</li>
        </ul>

        <h2 id="zakres">2. Jakie dane zbieramy</h2>
        <p><strong>Formularz zapytania.</strong> Gdy wysyłasz formularz, otrzymujemy dane, które w nim podasz: adres e-mail i numer telefonu (wymagane) oraz opcjonalnie imię i nazwisko, nazwę firmy, profil firmy, miejscowość lub województwo i treść zapytania, w tym listę pozycji do wyceny.</p>
        <p><strong>Kontakt e-mailowy i telefoniczny.</strong> Gdy piszesz lub dzwonisz do nas bezpośrednio, przetwarzamy dane podane w tej korespondencji lub rozmowie.</p>
        <p><strong>Dane techniczne.</strong> Przy każdym wyświetleniu strony serwer hostingu automatycznie rejestruje dane techniczne, takie jak adres IP, data i godzina, adres odwiedzanej podstrony oraz typ przeglądarki. Nie używamy ich do identyfikowania osób.</p>
        <p>Podanie danych jest dobrowolne, ale bez adresu e-mail i numeru telefonu nie będziemy mogli odpowiedzieć na zapytanie wysłane przez formularz.</p>

        <h2 id="cele">3. Cele i podstawy prawne przetwarzania</h2>
        <div class="tw"><table>
          <thead><tr><th>Cel</th><th>Podstawa prawna (RODO)</th></tr></thead>
          <tbody>
            <tr><td>Odpowiedź na zapytanie, przygotowanie wyceny lub oferty</td><td>art. 6 ust. 1 lit. a (zgoda wyrażona w formularzu) oraz art. 6 ust. 1 lit. b (działania na Twoje żądanie przed zawarciem umowy)</td></tr>
            <tr><td>Dalszy kontakt handlowy i obsługa współpracy z firmą, którą reprezentujesz</td><td>art. 6 ust. 1 lit. f (prawnie uzasadniony interes: kontakt z kontrahentami)</td></tr>
            <tr><td>Realizacja zamówień i umów, rozliczenia, obowiązki księgowe i podatkowe</td><td>art. 6 ust. 1 lit. b i c</td></tr>
            <tr><td>Ustalenie, dochodzenie lub obrona roszczeń</td><td>art. 6 ust. 1 lit. f</td></tr>
            <tr><td>Zapewnienie działania i bezpieczeństwa strony (dane techniczne)</td><td>art. 6 ust. 1 lit. f</td></tr>
          </tbody>
        </table></div>
        <p>Nie podejmujemy wobec Ciebie decyzji w sposób zautomatyzowany i nie profilujemy Cię.</p>

        <h2 id="odbiorcy">4. Komu przekazujemy dane</h2>
        <p>Nie sprzedajemy danych. Dostęp do nich mają upoważnieni pracownicy Armatex oraz podmioty, które świadczą dla nas usługi i przetwarzają dane w naszym imieniu:</p>
        <ul>
          <li><strong>Netlify, Inc.</strong>: hosting strony (w tym rejestrowanie danych technicznych) oraz obsługa formularza: przechowuje wysłane zgłoszenia i przesyła powiadomienia na naszą skrzynkę e-mail,</li>
          <li><strong>dostawcy poczty e-mail</strong>, na których działa nasza skrzynka,</li>
          <li><strong>GitHub, Inc.</strong>: przechowywanie kodu strony i jej kopia w serwisie GitHub Pages (dane techniczne przy wyświetleniu tej kopii),</li>
          <li>biuro rachunkowe, firmy kurierskie i transportowe, dostawcy IT: w zakresie potrzebnym do realizacji zamówień i obsługi firmy.</li>
        </ul>
        <p>Dane możemy też przekazać organom publicznym, jeśli wymaga tego prawo.</p>

        <h2 id="transfer">5. Przekazywanie danych poza EOG</h2>
        <p>Część usługodawców (Netlify, GitHub, dostawcy poczty) może przetwarzać dane poza Europejskim Obszarem Gospodarczym, w szczególności w Stanach Zjednoczonych. Odbywa się to na podstawie mechanizmów przewidzianych w RODO, w szczególności decyzji Komisji Europejskiej stwierdzającej odpowiedni stopień ochrony (EU-US Data Privacy Framework) albo standardowych klauzul umownych zatwierdzonych przez Komisję. Informacje o zastosowanych zabezpieczeniach przekażemy na Twoją prośbę.</p>

        <h2 id="okres">6. Jak długo przechowujemy dane</h2>
        <ul>
          <li><strong>Zapytania, na które nie doszło do współpracy:</strong> do 12 miesięcy od ostatniego kontaktu albo do wycofania zgody lub skutecznego sprzeciwu, jeśli nastąpi wcześniej.</li>
          <li><strong>Dane związane z zamówieniami i umowami:</strong> przez czas współpracy, a potem do upływu terminów przedawnienia roszczeń i przez okres wymagany przepisami podatkowymi i rachunkowymi (co do zasady 5 lat od końca roku podatkowego).</li>
          <li><strong>Zgłoszenia z formularza w panelu Netlify:</strong> usuwamy je okresowo, najpóźniej w terminach podanych wyżej dla zapytań.</li>
          <li><strong>Dane techniczne w logach hostingu:</strong> przez okres ustalony przez dostawcę hostingu, zwykle nie dłużej niż kilka tygodni.</li>
        </ul>

        <h2 id="prawa">7. Twoje prawa</h2>
        <p>Masz prawo:</p>
        <ul>
          <li>dostępu do swoich danych i otrzymania ich kopii,</li>
          <li>sprostowania danych,</li>
          <li>usunięcia danych,</li>
          <li>ograniczenia przetwarzania,</li>
          <li>przenoszenia danych,</li>
          <li>wniesienia sprzeciwu wobec przetwarzania opartego na prawnie uzasadnionym interesie,</li>
          <li>wycofania zgody w dowolnym momencie; wycofanie nie wpływa na zgodność z prawem przetwarzania, którego dokonano przed wycofaniem.</li>
        </ul>
        <p>Aby skorzystać z tych praw, napisz na <a href="mailto:biuro@armatex.pl">biuro@armatex.pl</a>. Masz też prawo wnieść skargę do Prezesa Urzędu Ochrony Danych Osobowych (ul. Stawki 2, 00-193 Warszawa, <a href="https://uodo.gov.pl" rel="noopener" target="_blank">uodo.gov.pl</a>).</p>

        <h2 id="cookies">8. Pliki cookies i pamięć przeglądarki</h2>
        <p><strong>Strona nie używa plików cookies</strong> ani narzędzi analitycznych, reklamowych czy śledzących.</p>
        <p>Strona korzysta z pamięci przeglądarki (localStorage) tylko w jednym celu: zapamiętuje <strong>listę pozycji do wyceny</strong>, którą sam tworzysz przyciskiem „Dodaj” w katalogu i na stronach produktów. Lista zawiera numery artykułów, nazwy produktów, ilości i jednostki. Zostaje wyłącznie na Twoim urządzeniu i nie jest do nas wysyłana, dopóki sam nie przeniesiesz jej do formularza i go nie wyślesz. To funkcja, o którą prosisz, dlatego nie wymaga odrębnej zgody (art. 399 ustawy – Prawo komunikacji elektronicznej).</p>
        <p>Listę usuwamy automatycznie po wysłaniu formularza. Możesz ją też usunąć w każdej chwili: przyciskiem „×” przy pozycjach na liście albo czyszcząc dane witryny w ustawieniach przeglądarki.</p>

        <h2 id="zewnetrzne">9. Treści i usługi zewnętrzne</h2>
        <p>Wszystkie pliki strony (teksty, zdjęcia, czcionki, skrypty) są wczytywane z naszego hostingu, bez zewnętrznych serwerów. Strona zawiera linki do innych serwisów, np. <a href="https://uodo.gov.pl" rel="noopener" target="_blank">uodo.gov.pl</a>. Za zasady prywatności tych serwisów odpowiadają ich właściciele.</p>

        <h2 id="bezpieczenstwo">10. Bezpieczeństwo</h2>
        <p>Strona jest udostępniana przez szyfrowane połączenie (HTTPS). Dostęp do danych z zapytań mają tylko osoby, które ich potrzebują do obsługi klientów.</p>

        <h2 id="zmiany">11. Zmiany polityki</h2>
        <p>Możemy aktualizować tę politykę, np. gdy dodamy nowe funkcje strony. Aktualna wersja jest zawsze dostępna na tej stronie. Jeśli zaczniemy używać plików cookies lub narzędzi analitycznych, poprosimy o zgodę przed ich uruchomieniem.</p>
'''
pol_toc=''.join(f'<li><a href="#{a}">{t}</a></li>' for a,t in re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>',pol_body))
pol=phead([('Polityka prywatności','polityka-prywatnosci.html')],'Dokumenty','Polityka prywatności.',
  f'Zasady przetwarzania danych osobowych i informacja o plikach cookies na stronie armatex.pl. Obowiązuje od {POL_OD}')+f'''
  <section class="section section--tight">
    <div class="wrap art">
      <article class="prose">
{pol_body}
        <p class="prose__src">Obowiązuje od {POL_OD}</p>
      </article>
      <aside class="art__side">
        <div class="art__box"><span class="label">Spis treści</span><ol>{pol_toc}</ol></div>
      </aside>
    </div>
  </section>
'''
page('polityka-prywatnosci.html','Polityka prywatności i cookies | Armatex','Polityka prywatności armatex.pl: administrator danych, cele przetwarzania, okres przechowywania, Twoje prawa i informacja o plikach cookies.','polityka',pol,ld_crumbs([('Polityka prywatności','polityka-prywatnosci.html')]))

# ---- 404
n404=f'''
  <section class="phead">
    <div class="wrap">
      <div>
        <span class="label kicker">Błąd 404</span>
        <h1>Nie znaleźliśmy tej strony.</h1>
        <p class="lead">Adres mógł się zmienić po przebudowie strony. Znajdź produkt po numerze artykułu albo zapytaj nas bezpośrednio.</p>
        <form class="e404" action="katalog.html" method="get" role="search">
          <label class="sr" for="q404">Numer artykułu lub nazwa</label>
          <input id="q404" name="q" type="search" placeholder="np. GP5001-22 albo trójnik 28" autocomplete="off">
          <button class="mag" type="submit"><span>Szukaj w katalogu</span></button>
        </form>
        <div class="phead__ctas"><a class="ghost" href="kontakt.html#formularz">Zapytaj o wycenę</a><a class="ghost" href="tel:+48513191502">513 191 502</a></div>
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <span class="label kicker">Przydatne strony</span>
      <h2 class="h2">Może szukasz jednej z nich.</h2>
      <div class="gain">'''+''.join(f'<a class="e404__c" href="{x["slug"]}.html"><span class="label">{x["brand"]}</span><b>{x["name"]}</b><p>{x["sizes"]} · {x["cntw"]}</p></a>' for x in SYS)+'''</div>
      <p class="lead" style="margin-top:2rem">Albo przejdź do <a href="index.html">strony głównej</a>, <a href="do-pobrania.html">katalogów do pobrania</a> lub <a href="poradniki.html">poradników</a>.</p>
    </div>
  </section>
'''
page('404.html','Nie znaleziono strony | Armatex','Strona nie istnieje. Znajdź produkt w katalogu Armatex lub zapytaj o wycenę.','404',n404)
h=open(OUT+'404.html',encoding='utf-8').read()
h=re.sub(r'\s*<link rel="canonical"[^>]*>','',h); h=h.replace('<meta charset="utf-8">','<meta charset="utf-8">\n  <meta name="robots" content="noindex">',1); h=re.sub(r'\s*<meta property="og:url"[^>]*>','',h)
# GitHub Pages podaje 404.html pod dowolnym adresem: baza ścieżek ustawiana przed wczytaniem CSS
h=h.replace('<head>\n','<head>\n  <script>document.write(\'<base href="\'+(/^\\/aramtex-website\\//i.test(location.pathname)?location.pathname.match(/^\\/[^/]+\\//)[0]:\'/\')+\'">\')</script>\n',1)
open(OUT+'404.html','w',encoding='utf-8').write(h)

# ---------------- sitemap.xml i robots.txt (do wersji produkcyjnej)
import datetime
urls=['']+[x['slug']+'.html' for x in SYS]+['katalog.html','do-pobrania.html','o-firmie.html','poradniki.html']+[a['slug']+'.html' for a in ART]+['wspolpraca.html','kontakt.html','polityka-prywatnosci.html']+[G['slug']+'.html' for G in GROUPS]
today=datetime.date.today().isoformat()
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls)+'</urlset>\n'
open(OUT+'sitemap.xml','w',encoding='utf-8').write(sm)
open(OUT+'robots.txt','w',encoding='utf-8').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
print('grupy',len(GROUPS),'url',len(urls))
print('ok')
