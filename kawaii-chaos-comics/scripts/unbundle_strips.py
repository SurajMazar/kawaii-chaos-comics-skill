#!/usr/bin/env python3
"""Unpack ~/Downloads/<prefix>*_bundle*.bin files whose entries are named <project>.png into
projects/NNN_<project>/raw/strip_vN.png and (re)point its strip.png at the newest take.

    python3 scripts/unbundle_strips.py b2

Entries may use the bare name (rem_puck) or the numbered folder name (046_rem_puck); a new bare name gets the next number.
"<project>__<file>.png" entries are frames of a music video -> music_videos/NN_<project>/<file>.png ("lyric_" is dropped).
"""
import glob, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from new_project import folder

prefix = sys.argv[1] if len(sys.argv) > 1 else ''
for p in sorted(glob.glob(os.path.expanduser(f'~/Downloads/{prefix}*_bundle*.bin')), key=os.path.getmtime):
    d = open(p, 'rb').read(); n = int(d[:10]); meta = json.loads(d[10:10 + n]); off = 10 + n
    for m in meta:
        proj = m['name'].rsplit('.', 1)[0]
        if '__' in proj:   # a frame of a music video
            proj, fn = proj.split('__', 1)
            dst = folder(proj.removeprefix('lyric_'), 'music_videos')
            d0 = os.path.join(dst, 'raw'); os.makedirs(d0, exist_ok=True)
            out = os.path.join(d0, f'{fn}.png'); open(out, 'wb').write(d[off:off + m['size']]); off += m['size']
            shutil.copy(out, os.path.join(dst, f'{fn}.png')); print(os.path.basename(dst), fn, '->', out); continue
        dst = folder(proj)
        raw = os.path.join(dst, 'raw'); os.makedirs(raw, exist_ok=True)
        k = len(glob.glob(os.path.join(raw, 'strip_v*.png'))) + 1
        out = os.path.join(raw, f'strip_v{k}.png')
        open(out, 'wb').write(d[off:off + m['size']]); off += m['size']
        shutil.copy(out, os.path.join(dst, 'strip.png'))
        print(os.path.basename(dst), '->', out)
    os.remove(p)
