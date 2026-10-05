"""Wersje językowe strony (armatex.pl/en/, /uk/): tłumaczenie gotowego HTML według słownika tools/<język>.json.

Tekst strony dzielony jest na odcinki: element z własnym tekstem (zdanie z ewentualnymi <a>, <b> w środku)
albo pojedynczy atrybut (alt, title, aria-label, placeholder, data-l, meta description, ...).
Znaczniki wewnątrz odcinka zamieniane są na <0>…</0>, <1/> itd., więc słownik ma krótkie klucze
bez atrybutów, a tłumaczenie może zmienić szyk zdania.

Kolejność szukania: mapa strony (zdania składane w generatorze, np. opis grupy produktów) → słownik
→ reguły (liczby sztuk, rozmiarów, etykiety z numerem artykułu) → nazwa produktu na początku tekstu.
Brakujące odcinki trafiają do Lang.MISSING; `python3 tools/strony.py` wypisuje je do tools/<język>-brak.json.
"""
import html as H
import json
import os
import re
from urllib.parse import quote, unquote

from bs4 import BeautifulSoup, Comment, Doctype, NavigableString, Tag
from bs4.dammit import EntitySubstitution
from bs4.formatter import HTMLFormatter


class _Fmt(HTMLFormatter):
    def attributes(self, tag):                              # kolejność atrybutów jak w źródle (bs4 domyślnie sortuje)
        return list(tag.attrs.items())


FMT = _Fmt(entity_substitution=EntitySubstitution.substitute_xml, void_element_close_prefix='', empty_attributes_are_booleans=True)

D = os.path.dirname(os.path.abspath(__file__))
INLINE = {'a', 'b', 'strong', 'em', 'i', 'span', 'small', 'code', 'br', 'sup', 'sub', 'abbr', 'mark', 'img', 'svg', 'time',
          'kbd', 's', 'u', 'wbr', 'input', 'select', 'button', 'label', 'q', 'cite', 'picture', 'source', 'textarea'}
ATOMIC = {'svg', 'img', 'br', 'input', 'wbr', 'select', 'picture', 'code', 'textarea'}
SKIP = {'script', 'style', 'svg', 'noscript', 'template', 'code', 'select', 'textarea'}
TATTR = ('alt', 'title', 'aria-label', 'placeholder', 'data-l', 'label')
LETTER = re.compile(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]')
WS = re.compile(r'\s+')
KEEP_DATA = set()                                           # angielskie nazwy z katalogów (zostają bez tłumaczenia)
for _f in ('besco-2026.json', 'pegler.json'):
    try:
        _d = json.load(open(os.path.join(D, '..', 'data', _f), encoding='utf-8'))
        KEEP_DATA.update(g[3] if isinstance(g, list) else (g.get('en') or '') for g in _d['groups'])
    except Exception:
        pass


def norm(s):
    return WS.sub(' ', s).strip()


def pl_plural(n, one, few, many):                           # polska / ukraińska odmiana: 1, 2–4, 5+
    n = int(str(n).replace(' ', '').replace('\u00a0', ''))
    return one if n == 1 else few if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else many


# reguły dla tekstów z liczbami i numerami artykułów (wspólny wzorzec, słowa per język)
WORDS = {
    'en': dict(pcs='pcs', bar='bar', unit={'karton': 'box', 'worek': 'bag', 'opak.': 'pack', 'szt.': 'pcs'}, approx='approx.', qty='Quantity',
               search='Search the {} line', unitw='Unit', add='Add {} to the quote list', rm='Remove {}',
               size=lambda n: 'size' if int(n) == 1 else 'sizes', item=lambda n: 'item' if int(n.replace(' ', '').replace('\u00a0', '')) == 1 else 'items',
               group=lambda n: 'group' if int(n.replace(' ', '').replace('\u00a0', '')) == 1 else 'groups', poz='items'),
    'uk': dict(pcs='шт.', bar='бар', unit={'karton': 'коробка', 'worek': 'мішок', 'opak.': 'уп.', 'szt.': 'шт.'}, approx='бл.', qty='Кількість',
               search='Шукати в лінії {}', unitw='Одиниця', add='Додати {} до запиту', rm='Видалити {}',
               size=lambda n: 'розм.', item=lambda n: pl_plural(n, 'позиція', 'позиції', 'позицій'),
               group=lambda n: pl_plural(n, 'група', 'групи', 'груп'), poz='поз.'),
}


class Lang:
    def __init__(self, code):
        self.code = code
        self.T = json.load(open(os.path.join(D, code + '.json'), encoding='utf-8'))
        self.t = self.T['t']
        self.N = self.T.get('names', {})                   # nazwy produktów i linii
        self.NAMES = sorted(self.N, key=len, reverse=True)
        self.KEEP = set(self.T.get('keep', [])) | KEEP_DATA
        self.MISSING = {}
        w = WORDS[code]
        U = w['unit']
        self.RULES = [
            (re.compile(r'([\d  ]+) szt\.'), lambda m: f"{m[1]} {w['pcs']}"),
            (re.compile(r'(karton|worek|opak\.|szt\.) \(([\d  ]+) szt\.\)'), lambda m: f"{U[m[1]]} ({m[2]} {w['pcs']})"),
            (re.compile(r'(karton|worek|opak\.|szt\.)'), lambda m: U[m[1]]),
            (re.compile(r'(\S+) · (\d+) rozm\.'), lambda m: f"{m[1]} · {m[2]} {w['size'](m[2])}"),
            (re.compile(r'ok\. ([\d  ]+)'), lambda m: f"{w['approx']} {m[1]}"),
            (re.compile(r'([\d  ,.–−…]+) bar'), lambda m: f"{m[1]} {w['bar']}"),
            (re.compile(r'Ilość (?!do )(\S.*)'), lambda m: f"{w['qty']} {m[1]}"),
            (re.compile(r'Szukaj w linii (.+)'), lambda m: w['search'].format(self.N.get(m[1], m[1]))),
            (re.compile(r'Jednostka (\S.*)'), lambda m: f"{w['unitw']} {m[1]}"),
            (re.compile(r'Dodaj (\S+) do zapytania'), lambda m: w['add'].format(m[1])),
            (re.compile(r'Usuń (\S+)'), lambda m: w['rm'].format(m[1])),
            (re.compile(r'([\d  ]+) (indeksów|indeksy|indeks)'), lambda m: f"{m[1]} {w['item'](m[1])}"),
            (re.compile(r'([\d  ]+) (grup|grupy|grupa)'), lambda m: f"{m[1]} {w['group'](m[1])}"),
            (re.compile(r'(\d+) (grup|grupy|grupa) · (\d+) poz\.'), lambda m: f"{m[1]} {w['group'](m[1])} · {m[3]} {w['poz']}"),
        ]


LANGS = {}


def lang(code):
    if code not in LANGS:
        LANGS[code] = Lang(code)
    return LANGS[code]


class Tr:
    def __init__(self, L, page_map=None, page=''):
        self.L = L
        self.pm = page_map or {}
        self.page = page

    def get(self, s, note=True):
        L = self.L
        k = norm(s)
        if not k or not LETTER.search(k):
            return None
        if k in self.pm:
            return self.pm[k]
        if k in L.t:
            return L.t[k]
        if k in L.N:
            return L.N[k]
        for rx, fn in L.RULES:
            m = rx.fullmatch(k)
            if m:
                return fn(m)
        for n in L.NAMES:                                   # „Łuk 90° wz 1/2″”, „Łuk 90° wz GP5001”
            rest = k[len(n):]
            if k.startswith(n + ' ') and not re.search(r'[a-ząćęłńóśźż]{2,}', re.sub(r'Besco|Tectite|Kuterlite|Pegler Yorkshire|Meters|mm\b', '', rest)):
                return L.N[n] + rest
        if note and k not in L.KEEP and re.search(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{3,}', re.sub(r'\b(mm|bar|TPI|Meters|FI|MI|Besco|Tectite|Kuterlite|Pegler|Yorkshire|Armatex|PN|DN|PEX|INOX)\b', '', k)):
            L.MISSING.setdefault(k, self.page)
        return None


def _ph(el, tags):
    out = ''
    for c in el.children:
        if isinstance(c, Comment):
            continue
        if isinstance(c, NavigableString):
            out += str(c)
            continue
        k = len(tags)
        tags.append(c)
        if c.name in ATOMIC:
            out += f'<{k}/>'
        else:
            out += f'<{k}>' + _ph(c, tags) + f'</{k}>'
    return out


def _start(t):
    a = ''.join(f' {k}="{H.escape(" ".join(v) if isinstance(v, list) else v, quote=True)}"' for k, v in t.attrs.items())
    return f'<{t.name}{a}>'


def _rebuild(tr, tags):
    out = ''
    for part in re.split(r'(</?\d+/?>)', tr):
        m = re.fullmatch(r'<(/?)(\d+)(/?)>', part)
        if not m:
            out += H.escape(part, quote=False)
            continue
        t = tags[int(m[2])]
        if m[3]:
            out += str(t)
        elif m[1]:
            out += f'</{t.name}>'
        else:
            out += _start(t)
    return out


def _direct_text(el):
    return any(isinstance(c, NavigableString) and not isinstance(c, Comment) and LETTER.search(c) for c in el.children)


def _inline_only(el):
    return all(not isinstance(d, Tag) or d.name in INLINE for d in el.descendants)


def _visit(el, tr):
    if el.name in SKIP or el.get('translate') == 'no':
        return
    if _inline_only(el) and _direct_text(el):
        tags = []
        key = norm(_ph(el, tags))
        v = tr.get(key)
        if v is not None:
            raw = _ph(el, [])                               # spacje na brzegach zostają jak w oryginale
            lead, trail = re.match(r'\s*', raw)[0], re.search(r'\s*$', raw)[0]
            frag = BeautifulSoup(H.escape(lead) + _rebuild(v, tags) + H.escape(trail), 'html.parser')
            el.clear()
            for c in list(frag.contents):
                el.append(c)
        return
    for c in list(el.children):
        if isinstance(c, Tag):
            _visit(c, tr)
        elif isinstance(c, NavigableString) and not isinstance(c, Comment) and LETTER.search(c):
            v = tr.get(str(c))
            if v is not None:
                lead, trail = re.match(r'\s*', str(c))[0], re.search(r'\s*$', str(c))[0]
                c.replace_with(lead + v + trail)


def _json(o, tr):
    if isinstance(o, dict):
        return {k: (_json(v, tr) if k not in ('@type', '@context', '@id', 'url', 'item', 'image', 'logo', 'telephone', 'email', 'sameAs') else v) for k, v in o.items()}
    if isinstance(o, list):
        return [_json(x, tr) for x in o]
    if isinstance(o, str):
        if '<' in o:                                        # odpowiedź FAQ z odnośnikami
            soup = BeautifulSoup(f'<p>{o}</p>', 'html.parser')
            _visit(soup.p, tr)
            return soup.p.decode_contents()
        if o.startswith('http'):
            return o
        v = tr.get(o)
        return v if v is not None else o
    return o


def translate(html, page='', page_map=None, code='en'):
    tr = Tr(lang(code), page_map, page)
    soup = BeautifulSoup(html, 'html.parser')
    for t in soup.find_all(True):
        if t.get('translate') == 'no' or t.find_parent(attrs={'translate': 'no'}):
            continue
        for a in TATTR:
            if t.has_attr(a) and isinstance(t[a], str):
                v = tr.get(t[a])
                if v is not None:
                    t[a] = v
        if t.name == 'meta' and (t.get('name') == 'description' or t.get('property', '').startswith('og:')) and t.has_attr('content'):
            v = tr.get(t['content'], note=t.get('property') not in ('og:url', 'og:image', 'og:type', 'og:locale', 'og:site_name'))
            if v is not None:
                t['content'] = v
        if t.name == 'a' and 'temat=' in t.get('href', ''):
            u, q = t['href'].split('temat=', 1)
            val, rest = (q.split('#', 1) + [''])[:2]
            val2, extra = (val.split('&', 1) + [''])[:2]
            v = tr.get(unquote(val2))
            if v is not None:
                t['href'] = u + 'temat=' + quote(v) + ('&' + extra if extra else '') + ('#' + rest if rest else '')
        if t.name == 'option':
            v = tr.get(t.get_text())
            if v is not None:
                t.string = v
    for s in soup.find_all('script', type='application/ld+json'):
        try:
            o = json.loads(s.string)
        except Exception:
            continue
        s.string = json.dumps(_json(o, tr), ensure_ascii=False)
    if soup.title and soup.title.string:
        v = tr.get(soup.title.string)
        if v is not None:
            soup.title.string = v
    _visit(soup.body, tr)
    return soup.decode(formatter=FMT)
