"""Powiększa zdjęcia grup do druku katalogu PDF (ESRGAN ×4) → tools/katalog-pdf/foto/<nazwa>.webp.

Użycie:
    mkdir -p /tmp/esrgan && cd /tmp/esrgan && npm install --legacy-peer-deps \\
        @upscalerjs/esrgan-thick@1.0.0 @tensorflow/tfjs@4.22.0 @tensorflow/tfjs-backend-wasm@4.22.0
    python3 tools/powieksz_zdjecia.py inox-316l /tmp/esrgan/node_modules

Bierze zdjęcia wskazane w tools/katalog-pdf/<linia>.json (białe tło), dodaje 4 px białego marginesu (czystsze brzegi),
liczy w 4 procesach i zapisuje WebP. tools/katalog_pdf.py używa ich zamiast zdjęć ze strony.
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


def main():
    line, mods = sys.argv[1], os.path.abspath(sys.argv[2])
    groups = json.load(open(os.path.join(DIR, f'{line}.json'), encoding='utf-8'))
    os.makedirs(os.path.join(DIR, 'foto'), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        jobs = []
        for g in groups:
            name = os.path.basename(g['zdjecie']).replace('-l.webp', '')
            im = Image.open(os.path.join(ROOT, g['zdjecie'])).convert('RGB')
            pad = Image.new('RGB', (im.width + 2 * PAD, im.height + 2 * PAD), 'white')
            pad.paste(im, (PAD, PAD))
            src, dst = os.path.join(tmp, name + '.raw'), os.path.join(tmp, name + '.out')
            open(src, 'wb').write(struct.pack('<II', *pad.size) + pad.tobytes())
            jobs.append((name, src, dst))
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
