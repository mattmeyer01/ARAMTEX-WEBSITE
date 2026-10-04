"""Angielska wersja strony (armatex.pl/en/): tłumaczenie gotowego HTML według słownika tools/en.json.

Tekst strony dzielony jest na odcinki: element z własnym tekstem (zdanie z ewentualnymi <a>, <b> w środku)
albo pojedynczy atrybut (alt, title, aria-label, placeholder, data-l, meta description, ...).
Znaczniki wewnątrz odcinka zamieniane są na <0>…</0>, <1/> itd., więc słownik ma krótkie klucze
bez atrybutów, a tłumaczenie może zmienić szyk zdania.

Kolejność szukania: mapa strony (zdania składane w generatorze, np. opis grupy produktów) → słownik
→ reguły (liczby sztuk, rozmiarów, etykiety z numerem artykułu) → nazwa produktu na początku tekstu.
Brakujące odcinki trafiają do MISSING; `python3 tools/strony.py` wypisuje je do tools/en-brak.json.
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
T = json.load(open(os.path.join(D, 'en.json'), encoding='utf-8'))
MISSING = {}

INLINE = {'a', 'b', 'strong', 'em', 'i', 'span', 'small', 'code', 'br', 'sup', 'sub', 'abbr', 'mark', 'img', 'svg', 'time',
          'kbd', 's', 'u', 'wbr', 'input', 'select', 'button', 'label', 'q', 'cite', 'picture', 'source', 'textarea'}
ATOMIC = {'svg', 'img', 'br', 'input', 'wbr', 'select', 'picture', 'code', 'textarea'}
SKIP = {'script', 'style', 'svg', 'noscript', 'template', 'code', 'select', 'textarea'}
TATTR = ('alt', 'title', 'aria-label', 'placeholder', 'data-l', 'label')
LETTER = re.compile(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]')
PL_CH = re.compile(r'[ĄĆĘŁŃÓŚŹŻąćęłńóśźż]')
WS = re.compile(r'\s+')

N = T.get('names', {})                                     # nazwy produktów i linii
NAMES = sorted(N, key=len, reverse=True)
KEEP = set(T.get('keep', []))                               # teksty bez tłumaczenia (nazwy własne, angielskie nazwy z katalogów)
for _f in ('besco-2026.json', 'pegler.json'):
    try:
        _d = json.load(open(os.path.join(D, '..', 'data', _f), encoding='utf-8'))
        KEEP.update(g[3] if isinstance(g, list) else (g.get('en') or '') for g in _d['groups'])
    except Exception:
        pass
UNIT = {'karton': 'box', 'worek': 'bag', 'opak.': 'pack', 'szt.': 'pcs'}


def norm(s):
    return WS.sub(' ', s).strip()


def plural(n, one, many):
    return one if int(n) == 1 else many


RULES = [
    (re.compile(r'([\d  ]+) szt\.'), lambda m: f'{m[1]} pcs'),
    (re.compile(r'(karton|worek|opak\.|szt\.) \(([\d  ]+) szt\.\)'), lambda m: f'{UNIT[m[1]]} ({m[2]} pcs)'),
    (re.compile(r'(karton|worek|opak\.|szt\.)'), lambda m: UNIT[m[1]]),
    (re.compile(r'(\S+) · (\d+) rozm\.'), lambda m: f'{m[1]} · {m[2]} {plural(m[2], "size", "sizes")}'),
    (re.compile(r'ok\. ([\d  ]+)'), lambda m: f'approx. {m[1]}'),
    (re.compile(r'Ilość (?!do )(\S.*)'), lambda m: f'Quantity {m[1]}'),
    (re.compile(r'Szukaj w linii (.+)'), lambda m: f'Search the {N.get(m[1], m[1])} line'),
    (re.compile(r'Jednostka (\S.*)'), lambda m: f'Unit {m[1]}'),
    (re.compile(r'Dodaj (\S+) do zapytania'), lambda m: f'Add {m[1]} to the quote list'),
    (re.compile(r'Usuń (\S+)'), lambda m: f'Remove {m[1]}'),
    (re.compile(r'([\d  ]+) (indeksów|indeksy|indeks)'), lambda m: f'{m[1]} {plural(m[1], "item", "items")}'),
    (re.compile(r'([\d  ]+) (grup|grupy|grupa)'), lambda m: f'{m[1]} {plural(m[1], "group", "groups")}'),
    (re.compile(r'(\d+) (grup|grupy|grupa) · (\d+) poz\.'), lambda m: f'{m[1]} {plural(m[1], "group", "groups")} · {m[3]} items'),
]


class Tr:
    def __init__(self, page_map=None, page=''):
        self.pm = page_map or {}
        self.page = page

    def get(self, s, note=True):
        k = norm(s)
        if not k or not LETTER.search(k):
            return None
        if k in self.pm:
            return self.pm[k]
        if k in T['t']:
            return T['t'][k]
        if k in N:
            return N[k]
        for rx, fn in RULES:
            m = rx.fullmatch(k)
            if m:
                return fn(m)
        for n in NAMES:                                     # „Łuk 90° wz 1/2″”, „Łuk 90° wz GP5001”
            rest = k[len(n):]
            if k.startswith(n + ' ') and not re.search(r'[a-ząćęłńóśźż]{2,}', re.sub(r'Besco|Tectite|Kuterlite|Pegler Yorkshire|Meters|mm\b', '', rest)):
                return N[n] + rest
        if note and k not in KEEP and re.search(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{3,}', re.sub(r'\b(mm|bar|TPI|Meters|FI|MI|Besco|Tectite|Kuterlite|Pegler|Yorkshire|Armatex|PN|DN|PEX|INOX)\b', '', k)):
            MISSING.setdefault(k, self.page)
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


def translate(html, page='', page_map=None):
    tr = Tr(page_map, page)
    soup = BeautifulSoup(html, 'html.parser')
    for t in soup.find_all(True):
        if t.get('translate') == 'no':
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
