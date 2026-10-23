#!/usr/bin/env python3
"""QA step G, mandatory for every image: master crop + the image's character crops at the same scale, side by side.

    python3 scripts/style_check.py projects/NNN_x/raw/strip_a1.png [out.jpg]
Crops the two densest-ink regions of the image (where characters are) and puts them next to a master Rem/Subaru crop.
Look at it BEFORE ticking anything: line darkness/weight, fill texture (clean pencil grain vs watercolour/smudge), eye style.
"""
import sys, os
import numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + '_stylecheck.jpg'
m = Image.open(os.path.join(ROOT, 'references', 'style_ref_master.jpg')).convert('RGB')
crops = [m.crop((0, 280, 330, 600)), m.crop((1340, 420, 1700, 760))]
im = Image.open(src).convert('RGB'); g = np.asarray(im.convert('L')) < 90
H, W = g.shape; win = (320, 360); best = []
for y in range(0, H - win[1], 60):
    for x in range(0, W - win[0], 60):
        best.append((g[y:y + win[1], x:x + win[0]].mean(), x, y))
best.sort(reverse=True); picked = []
for s, x, y in best:
    if all(abs(x - px) > 300 or abs(y - py) > 300 for px, py in picked): picked.append((x, y))
    if len(picked) == 2: break
crops += [im.crop((x, y, x + win[0], y + win[1])) for x, y in picked]
h = 330; crops = [c.resize((int(c.width * h / c.height), h)) for c in crops]
o = Image.new('RGB', (sum(c.width for c in crops) + 40, h), 'white'); x = 0
for i, c in enumerate(crops):
    o.paste(c, (x, 0)); x += c.width + (30 if i == 1 else 10)
o.save(out, quality=92); print(out)
# ORANGE-ON-REM aid (owner 2026-10-22 "orange strips"): mark every orange pixel that sits next to Rem-blue hair pixels' columns
a = np.asarray(im).astype(int); r, gg, b = a[..., 0], a[..., 1], a[..., 2]
orange = (r > 215) & (gg > 95) & (gg < 165) & (b < 70) & (r - gg > 70) & (gg - b > 45)
blue = (b > 170) & (r < 140) & (gg > 110) & (gg < 200)          # Rem's hair
from scipy import ndimage
near = ndimage.binary_dilation(blue, iterations=60)             # within ~60 px of blue hair = Rem's body area
hits = orange & near
ys, xs = np.where(hits)
mark = im.copy(); from PIL import ImageDraw; d = ImageDraw.Draw(mark)
lab, n = ndimage.label(ndimage.binary_dilation(hits, iterations=4))
for sl in ndimage.find_objects(lab):
    if (sl[0].stop - sl[0].start) * (sl[1].stop - sl[1].start) > 60:
        d.rectangle([sl[1].start - 6, sl[0].start - 6, sl[1].stop + 6, sl[0].stop + 6], outline=(255, 0, 255), width=4)
mo = os.path.splitext(out)[0] + '_orange.jpg'; mark.save(mo, quality=85)
print(f'orange pixels near Rem-blue: {int(hits.sum())} -> CHECK the magenta boxes in {mo} (Subaru standing next to Rem also triggers; judge by eye)')
