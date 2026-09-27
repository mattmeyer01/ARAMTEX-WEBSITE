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
TEL='<a href="tel:+48798807106">798 807 106</a>'

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
  desc='System push-fit montowany bez narzędzi, prądu i otwartego ognia. Łączy rury miedziane, PEX, PB, ze stali nierdzewnej i węglowej, zależnie od linii.',
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
 dict(slug='zlaczki-skrecane-kuterlite',name='Złączki skręcane',h1='Złączki skręcane Kuterlite',seotitle='Złączki skręcane Kuterlite dla hurtowni | Armatex',metadesc='Złączki skręcane (zaciskowe) Kuterlite: K600 i K900 Pro do miedzi, K700 do rur PE oraz zawory, 6–63 mm. Około 470 indeksów, dostawy do hurtowni w całej Polsce.',tab='Skręcane',brand='Pegler Yorkshire',cnt='ok. 470',cntw='ok. 470 indeksów',sizes='6–63 mm',
  title='Złączki skręcane Kuterlite',
  short='Kuterlite K600 i K900 Pro do miedzi, K700 do rur PE oraz zawory z końcówkami zaciskowymi.',
  desc='Mosiężne złączki zaciskowe z pierścieniem do rur miedzianych i PE. Montaż kluczem, bez lutowania i zaciskarki.',
  who='Serwis i podłączenia urządzeń: kotłów, podgrzewaczy i armatury. Klasyczny towar ladowy z rotacją przez cały rok.',
  arg='Jedna marka na miedź 6–54 mm i rury PE 20–63 mm, razem z zaworami w tym samym systemie.',
  pics=[('kuterlite','Trójnik skręcany Kuterlite'),('kuterlite-kolano','Kolano skręcane Kuterlite'),('kuterlite-zawor','Zawór z końcówkami zaciskowymi Kuterlite')],
  seria='',src='cennik Kuterlite, październik 2024',
  lines=[('Kuterlite K600','Pegler Yorkshire','','6–28 mm','rury miedziane','seria podstawowa',[],'ok. 150','oferta/kuterlite'),
   ('Kuterlite K900 Pro (KN 900)','Pegler Yorkshire','','8–54 mm','rury miedziane','złączki, kolana, przejścia GW/GZ',[],'ok. 185','oferta/kuterlite-kolano'),
   ('Kuterlite K700','Pegler Yorkshire','','20–63 mm','rury PE','złączki PE × PE i PE × miedź',[],'ok. 65','linie/kuterlite-k700'),
   ('Zawory z końcówkami zaciskowymi','Pegler Yorkshire','','15–28 mm','woda, podłączenia urządzeń','kurki, zawory odcinające',[],'ok. 30','oferta/kuterlite-zawor')],
  faq=[('Czym różnią się serie K600, K900 Pro i K700?','K600 to seria podstawowa do rur miedzianych 6–28 mm. K900 Pro obejmuje złączki, kolana i przejścia GW/GZ do miedzi 8–54 mm (na armatex.pl jako KN 900). K700 łączy rury PE 20–63 mm, także z miedzią.'),
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
   "telephone":"+48 798 807 106","email":"armatex1@gmail.com",
   "address":{"@type":"PostalAddress","streetAddress":"ul. Składowa 3a","postalCode":"10-421","addressLocality":"Olsztyn","addressCountry":"PL"},
   "areaServed":{"@type":"Country","name":"Polska"},
   "brand":[{"@type":"Brand","name":"Besco"},{"@type":"Brand","name":"Pegler Yorkshire"}],
   "contactPoint":[
     {"@type":"ContactPoint","contactType":"sales","name":"Piotr Stelmach","telephone":"+48 798 807 106","email":"piotr@armatex.pl","areaServed":"PL","availableLanguage":"pl"},
     {"@type":"ContactPoint","contactType":"sales","name":"Martyna Zielińska","telephone":"+48 515 231 693","email":"martyna@armatex.pl","areaServed":"PL","availableLanguage":"pl"}]},
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
  <meta name="robots" content="noindex, nofollow">
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
    ddcur=' aria-current="page"' if cur in [s['slug'] for s in SYS]+['katalog'] else ''
    kat=(f'<a href="katalog.html"{cs("katalog")}><span class="dd__ico">{ICO_SEARCH}</span><b>Wyszukiwarka indeksów Besco</b><span>1 936 indeksów · lista do wyceny</span></a>'
         f'<a href="{PDF}" target="_blank" rel="noopener"><span class="dd__ico">{ICO_PDF}</span><b>Katalog Besco 2026</b><span>PDF · 3 MB · 66 stron</span></a>')
    mlinks=''.join(f'<a href="{s["slug"]}.html"{cs(s["slug"])}>{s["name"]}<small>{s["brand"]}</small></a>' for s in SYS)
    return f'''<header class="nav" id="nav">
  <div class="wrap">
    <a class="nav__logo" href="index.html" aria-label="Armatex, strona główna">
      <img class="light" src="../img/logo-light.webp" alt="" width="300" height="52">
      <img class="dark" src="../img/logo-dark.webp" alt="" width="300" height="52">
    </a>
    <nav class="nav__links" aria-label="Nawigacja główna">
      <div class="dd"><button type="button" aria-expanded="false" aria-controls="dd-m"{ddcur}>Oferta</button><div class="dd__m" id="dd-m"><span class="dd__h">Systemy złączek</span>{ddlinks}<span class="dd__h">Katalogi</span>{kat}</div></div>
      <a href="wspolpraca.html"{cs("wspolpraca")}>Współpraca</a>
      <a href="kontakt.html"{cs("kontakt")}>Kontakt</a>
    </nav>
    <a class="nav__tel" href="tel:+48798807106">798 807 106</a>
    <a class="mag" href="{"#kontakt" if cur=="index" else "kontakt.html#formularz"}"><span>Zapytaj o ofertę</span></a>
    <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Otwórz menu"><i></i></button>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="Menu mobilne">
  <span class="label">Oferta</span>{mlinks}
  <span class="label">Katalogi</span><a href="katalog.html"{cs("katalog")}>Wyszukiwarka indeksów Besco<small>1 936</small></a><a href="{PDF}" target="_blank" rel="noopener">Katalog Besco 2026<small>PDF · 3 MB</small></a>
  <span class="label">Armatex</span><a href="wspolpraca.html"{cs("wspolpraca")}>Współpraca</a><a href="kontakt.html"{cs("kontakt")}>Kontakt<small>798 807 106</small></a>
</nav>
'''
FOOT='''<footer class="foot">
  <div class="wrap foot__g">
    <div>
      <img src="../img/logo-light.webp" alt="Armatex" width="300" height="52" loading="lazy">
      <p>Dystrybutor złączek i armatury Besco oraz Pegler Yorkshire dla hurtowni instalacyjnych w całej Polsce.</p>
    </div>
    <div><h4>Oferta</h4><ul>'''+''.join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SYS)+'''</ul></div>
    <div><h4>Armatex</h4><ul><li><a href="katalog.html">Wyszukiwarka indeksów Besco</a></li><li><a href="'''+PDF+'''" target="_blank" rel="noopener">Katalog Besco 2026 (PDF)</a></li><li><a href="wspolpraca.html">Współpraca</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
    <div><h4>Kontakt</h4><ul><li><a href="tel:+48798807106">798 807 106</a></li><li><a href="mailto:armatex1@gmail.com">armatex1@gmail.com</a></li><li>ul. Składowa 3a, 10-421 Olsztyn</li></ul></div>
  </div>
  <div class="wrap foot__bar"><span>© 2026 Armatex</span></div>
</footer>
'''
FORM_TO='armatex1@gmail.com'
def live_form(html):
    """Formularz wysyła przez FormSubmit (jak poprzednia wersja strony)."""
    if 'id="form" novalidate>' not in html: return html
    html=html.replace('<form class="form" id="form" novalidate>',
        f'<form class="form" id="form" method="POST" action="https://formsubmit.co/{FORM_TO}" novalidate>\n'
        '        <input type="hidden" name="_subject" value="Zapytanie hurtowni ze strony armatex.pl">\n'
        '        <input type="hidden" name="_template" value="table">\n'
        '        <input type="hidden" name="_captcha" value="false">\n'
        '        <input type="text" name="_honey" class="sr" tabindex="-1" autocomplete="off" aria-hidden="true">')
    for a,b in (('<input id="n" autocomplete="name">','<input id="n" name="Imię i nazwisko" autocomplete="name" required>'),
                ('<input id="c" autocomplete="organization">','<input id="c" name="Firma" autocomplete="organization" required>'),
                ('<input id="e" type="email" autocomplete="email">','<input id="e" name="email" type="email" autocomplete="email" required>'),
                ('<input id="t" type="tel" autocomplete="tel">','<input id="t" name="Telefon" type="tel" autocomplete="tel">'),
                ('<select id="pf">','<select id="pf" name="Profil firmy">'),
                ('<input id="ms" autocomplete="address-level2">','<input id="ms" name="Miasto / województwo" autocomplete="address-level2">'),
                ('<textarea id="m" ','<textarea id="m" name="Zapytanie" required '),
                ('<input type="checkbox" id="ok">','<input type="checkbox" id="ok" name="Zgoda" value="tak" required>')):
        assert a in html, a; html=html.replace(a,b)
    return html

def page(name,title,desc,cur,body,extra=''):
    html=head(title,desc,extra,'' if name=='index.html' else name)+'<body data-base="../">\n\n'+nav(cur)+'\n<main id="top">\n'+body+'\n</main>\n\n'+FOOT+'</body>\n</html>\n'
    # strona w katalogu głównym repo: ścieżki względne bez prefiksów szkicu
    for a,b in (('../../assets/','assets/'),('../img/','img/'),('../pliki/','pliki/'),('../data/','data/'),('<body data-base="../">','<body>')):
        html=html.replace(a,b)
    html=live_form(html)
    open(OUT+name,'w',encoding='utf-8').write(html)

def card(s,cls='syc in'):
    p0,a0=s['pics'][0]
    ims=img(p0,a0)
    return f'<a class="{cls}" href="{s["slug"]}.html"><span class="syc__m">{ims}</span><span class="syc__b"><span class="label syc__k">{s["n"]} · {s["brand"]}</span><h3>{s["name"]}</h3><p>{s["short"]}</p><span class="syc__f"><span class="label">{s["cntw"]} · {s["sizes"]}</span><span class="syc__go">Zobacz →</span></span></span></a>'

def faqlist(items, first_open=True):
    return '\n'.join(f'        <details class="qa" name="faq"{" open" if (i==0 and first_open) else ""}><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for i,(q,a) in enumerate(items))


# ---------------- strona główna
hero=frag('  <section class="hero"','  </section>')
hero=hero.replace('<a class="mag" href="#kontakt" data-topic="Jesteśmy hurtownią i chcemy poznać warunki współpracy (Besco, Pegler Yorkshire)."><span>Warunki dla hurtowni <svg','<a class="mag" href="#kontakt"><span>Zapytaj o ofertę <svg')
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
kontakt_home=kontakt_home.replace('<h3>Zapytanie o warunki współpracy</h3>','<h3>Zapytanie ofertowe</h3>')
steps=frag('      <div class="steps">','      </div>\n      <div class="aud">').replace('      <div class="aud">','').rstrip()
stats='''      <div class="stats">
        <div class="stat"><b><span class="odo" data-odo="30" aria-label="30">30</span><i> lat</i></b><span>na rynku instalacyjnym</span></div>
        <div class="stat"><b><span class="odo" data-odo="24" aria-label="24">24</span><i> h</i></b><span>wysyłka z magazynu w Olsztynie</span></div>
        <div class="stat"><b><span class="odo" data-odo="1" aria-label="1">1</span><i> dzień</i></b><span>na przygotowanie oferty</span></div>
        <div class="stat"><b><span class="odo" data-odo="4" aria-label="4">4</span><i> systemy</i></b><span>łączenia od jednego dystrybutora</span></div>
      </div>'''
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
  <section class="section" id="faq" style="padding-top:0">
    <div class="wrap faq">
      <div class="faq__intro">
        <span class="label kicker">Pytania</span>
        <h2 class="h2">Pytania hurtowni.</h2>
        <p class="lead">Pytania techniczne o poszczególne systemy znajdziesz na ich stronach.</p>
        <a class="ulink" href="tel:+48798807106">Zadzwoń: 798 807 106</a>
      </div>
      <div>
{faqlist([
 ('Jak szybko dostanę ofertę?','W ciągu jednego dnia roboczego. Oferta zawiera ceny hurtowe, dostępność i terminy dostaw dla systemów lub indeksów, które chcesz prowadzić.'),
 ('Jakie marki i systemy dystrybuujecie?','Besco Fittings &amp; Connectors: miedź press w profilach V i M, serie gazowe, stal węglowa press, złączki lutowane i zawory kulowe press. Pegler Yorkshire: złączki na wcisk Tectite, złączki skręcane Kuterlite i zawory na wcisk. Razem około 2 900 indeksów.'),
 ('Jaki jest czas dostawy?','Wysyłka z magazynu w Olsztynie w 24 godziny od potwierdzenia zamówienia. Duże zamówienia dowozimy własnym transportem.'),
 ('Czy mogę zamówić po numerze artykułu Besco?','Tak. <a href="katalog.html">Katalog z wyszukiwarką</a> obejmuje 1 936 pozycji Besco 2026. Dodaj indeksy do listy, podaj ilości i wyślij do wyceny.'),
 ('Jak uzyskać dostęp do dokumentów?','Poproś o dostęp przez formularz. Po weryfikacji hurtowni udostępniamy karty katalogowe, atesty i deklaracje w ciągu jednego dnia roboczego.')])}
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
page('index.html','Złączki Besco i Pegler Yorkshire dla hurtowni | Armatex','Dystrybutor złączek zaciskanych, na wcisk, skręcanych i lutowanych Besco oraz Pegler Yorkshire dla hurtowni w całej Polsce. Około 2 900 indeksów.','index',home,pre+LD_ORG)

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
        <div class="phead__ctas"><a class="mag" href="{ask(s["topic"])}"><span>Zapytaj o ofertę</span></a>{find}</div>
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
        <a class="ulink" href="tel:+48798807106">Zadzwoń: 798 807 106</a>
      </div>
      <div>
{faqlist(s["faq"])}
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <div class="cta">
        <div><h2>Zapytaj o ofertę na {s["name"].lower()} {s["brand"]}.</h2><p>Ceny hurtowe, dostępność i terminy dostaw przygotujemy w ciągu jednego dnia roboczego.</p></div>
        <div class="cta__b"><a class="mag" href="{ask(s["topic"])}"><span>Zapytaj o ofertę</span></a></div>
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
        <div class="phead__ctas"><a class="ghost" href="{PDF}" target="_blank" rel="noopener">Pobierz katalog Besco 2026 (PDF · 3 MB)</a></div>
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
frame=frag('      <figure class="frame" data-hf>','      </figure>')
docs=frag('  <section class="docs" id="dokumenty">','  </section>').replace('<a class="ghost" href="#kontakt" data-topic="Jesteśmy hurtownią i prosimy o dostęp do bazy dokumentów technicznych.">','<a class="ghost" href="'+ask('Jesteśmy hurtownią i prosimy o dostęp do bazy dokumentów technicznych.')+'">').replace('src="img/besco/','src="../img/besco/')
assert 'kontakt.html?temat=' in docs
wsp=f'''
  <section class="phead">
    <div class="wrap">
      <ol class="crumbs"><li><a href="index.html">Armatex</a></li><li aria-current="page">Współpraca</li></ol>
      <div>
        <span class="label kicker">Współpraca z hurtowniami</span>
        <h1>Zaplecze, logistyka i dokumenty.</h1>
        <p class="lead">Dystrybuujemy złączki i armaturę Besco oraz Pegler Yorkshire do hurtowni instalacyjnych w całej Polsce. Tak wygląda współpraca z nami.</p>
        <div class="phead__ctas"><a class="mag" href="{ask('Jesteśmy hurtownią i chcemy rozpocząć współpracę (Besco, Pegler Yorkshire).')}"><span>Zapytaj o ofertę</span></a></div>
      </div>
      <dl class="phead__facts">
        <div><dt class="label">Na rynku</dt><dd>30 lat</dd></div>
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
        <div class="in"><h3>Obsługa</h3><ul><li>Oferta w ciągu jednego dnia roboczego.</li><li>Dwoje handlowców: Piotr Stelmach i Martyna Zielińska.</li><li>Cały program Besco i Pegler Yorkshire na jednej fakturze.</li></ul></div>
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
        <div class="cta__b"><a class="mag" href="kontakt.html#formularz"><span>Zapytaj o ofertę</span></a><a class="ghost" href="tel:+48798807106">798 807 106</a></div>
      </div>
    </div>
  </section>
'''
page('wspolpraca.html','Współpraca z hurtowniami – dystrybutor złączek | Armatex','Jak współpracujemy z hurtowniami instalacyjnymi: magazyn w Olsztynie, wysyłka w 24 godziny, zatowarowanie na sezon i dokumenty do złączek Besco i Pegler Yorkshire.','wspolpraca',wsp,ld_crumbs([('Współpraca','wspolpraca.html')]))

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
page('kontakt.html','Kontakt – zapytanie ofertowe dla hurtowni | Armatex','Kontakt z działem sprzedaży Armatex: złączki Besco i Pegler Yorkshire dla hurtowni. Telefon 798 807 106, Olsztyn, ul. Składowa 3a.','kontakt',kontakt,ld_crumbs([('Kontakt','kontakt.html')]))

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
        desc=f'{G["name"]} {brand} {G["code"]} ({ser["name"]}): {n} {rozm} ({rng}). Numery artykułów{" i opakowania zbiorcze" if kind=="kuterlite" else ""} dla hurtowni.'
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
        <div class="phead__ctas"><a class="mag" href="{ask(topic)}"><span>Zapytaj o ofertę</span></a>{pdfbtn}</div>
      </div>
      <dl class="phead__facts">
{ftxt}
      </dl>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap gp">
      <figure class="gp__img{' gp__img--w' if kind!='besco' else ''}"><img src="{G["img_src"]}" alt="{G["name"]} {G["brand"]} {G["code"]}" decoding="async"></figure>
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
        <div><h2>Zapytaj o ofertę: {G["name"]} {G["code"]}.</h2><p>Dodaj rozmiary do listy przyciskiem „Dodaj” albo od razu napisz do nas. Ceny hurtowe, dostępność i terminy przygotujemy w ciągu jednego dnia roboczego.</p></div>
        <div class="cta__b"><a class="mag" href="{ask(topic)}"><span>Zapytaj o ofertę</span></a><a class="ghost" href="katalog.html#zapytanie">Moja lista</a></div>
      </div>
      {f'<div class="shead" style="margin-top:clamp(3rem,6vw,4.5rem)"><h2 class="sy-h" style="margin:0">Inne produkty w linii</h2>{search}</div><div class="gl__l" style="margin-top:1.2rem">{rel}</div>' if rel else ''}
      <p style="margin-top:2rem"><a class="ulink" href="{sysp["slug"]}.html">Wszystkie {sysp["name"].lower()}</a></p>
    </div>
  </section>
<a class="pill" id="pill" href="katalog.html#zapytanie">Lista <span id="pillN">0</span></a>
'''
    bname={'besco':'Besco','tectite':'Pegler Yorkshire','kuterlite':'Pegler Yorkshire'}[kind]
    lst=ld({"@context":"https://schema.org","@type":"ItemList","name":f'{G["full"]} {G["code"]}',
      "itemListElement":[{"@type":"ListItem","position":i,"item":{"@type":"Product","name":f'{G["full"]} {size_of(r)}',"sku":code_of(r),"mpn":code_of(r),
        "brand":{"@type":"Brand","name":bname},"image":SITE+G['img_src'].replace('../','')}} for i,r in enumerate(rows,1)]})
    crumbs=ld_crumbs([(sysp['name'],sysp['slug']+'.html'),(f'{G["name"]} {G["code"]}',G['slug']+'.html')])
    page(G['slug']+'.html',title,desc,sysp['slug'],body,crumbs+lst)

# ---------------- sitemap.xml i robots.txt (do wersji produkcyjnej)
import datetime
urls=['']+[x['slug']+'.html' for x in SYS]+['katalog.html','wspolpraca.html','kontakt.html']+[G['slug']+'.html' for G in GROUPS]
today=datetime.date.today().isoformat()
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls)+'</urlset>\n'
open(OUT+'sitemap.xml','w',encoding='utf-8').write(sm)
open(OUT+'robots.txt','w',encoding='utf-8').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
print('grupy',len(GROUPS),'url',len(urls))
print('ok')
