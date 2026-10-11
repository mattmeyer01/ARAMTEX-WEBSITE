"""Powiększa zdjęcia grup do druku katalogu PDF (ESRGAN ×4) → tools/katalog-pdf/foto/<nazwa>.webp.

Użycie:
    mkdir -p /tmp/esrgan && cd /tmp/esrgan && npm install --legacy-peer-deps \\
        @upscalerjs/esrgan-thick@1.0.0 @tensorflow/tfjs@4.22.0 @tensorflow/tfjs-backend-wasm@4.22.0
    python3 tools/powieksz_zdjecia.py /tmp/esrgan/node_modules inox-316l besco-2026 tectite kuterlite

Bierze zdjęcia wskazane w tools/katalog-pdf/<katalog>.json (białe tło), dodaje 4 px białego marginesu (czystsze brzegi),
liczy w 4 procesach i zapisuje WebP. Pomija zdjęcia, które mają co najmniej MIN_PX na dłuższym boku, i te, które już
są w foto/. tools/katalog_pdf.py używa ich zamiast zdjęć ze strony.
"""
import json
import os
import struct
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'tools', 'katalog-pdf')
PAD = 4
MIN_PX = 300


def main():
    mods, lines = os.path.abspath(sys.argv[1]), sys.argv[2:]
    os.makedirs(os.path.join(DIR, 'foto'), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        jobs, seen = [], set()
        for line in lines:
            for g in json.load(open(os.path.join(DIR, f'{line}.json'), encoding='utf-8')):
                name = os.path.basename(g['zdjecie']).replace('-l.webp', '').replace('.webp', '')
                if name in seen or os.path.exists(os.path.join(DIR, 'foto', name + '.webp')):
                    continue
                seen.add(name)
                im = Image.open(os.path.join(ROOT, g['zdjecie'])).convert('RGB')
                if max(im.size) >= MIN_PX:
                    continue
                pad = Image.new('RGB', (im.width + 2 * PAD, im.height + 2 * PAD), 'white')
                pad.paste(im, (PAD, PAD))
                src, dst = os.path.join(tmp, name + '.raw'), os.path.join(tmp, name + '.out')
                open(src, 'wb').write(struct.pack('<II', *pad.size) + pad.tobytes())
                jobs.append((name, src, dst))
        print(len(jobs), 'zdjęć do powiększenia', flush=True)
        procs = [subprocess.Popen(['node', os.path.join(DIR, 'esrgan.js')] + [a for _, s, d in jobs[k::4] for a in (s, d)],
                                  env={**os.environ, 'MODS': mods}) for k in range(4)]
        if any(p.wait() for p in procs):
            sys.exit('ESRGAN: błąd')
        for name, _, dst in jobs:
            raw = open(dst, 'rb').read()
            w, h = struct.unpack('<II', raw[:8])
            im = Image.frombytes('RGB', (w, h), raw[8:]).crop((4 * PAD, 4 * PAD, w - 4 * PAD, h - 4 * PAD))
            im.save(os.path.join(DIR, 'foto', name + '.webp'), quality=92)
            print(name, im.size)


if __name__ == '__main__':
    main()
