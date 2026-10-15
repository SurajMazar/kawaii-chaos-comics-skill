#!/usr/bin/env python3
"""Erase our hand-lettered line from music-video frames, keeping the full picture (no cropping), so the reel has no
text of ours and the REAL song's lyrics can be shown with Instagram's own lyrics display.

    python3 scripts/strip_text.py music_videos/09_anotherlife      # frame*.png -> notext/frame*.png

Each dark ink blob in the top 60% is erased only if the area around it is plain cream (letters float on cream;
hair/outlines always touch coloured picture), so characters are never touched.
"""
import glob, os, sys
import cv2
import numpy as np

for d in sys.argv[1:]:
    os.makedirs(os.path.join(d, 'notext'), exist_ok=True)
    for f in sorted(glob.glob(os.path.join(d, 'frame*.png'))):
        im = cv2.imread(f); h, w = im.shape[:2]
        bg = np.median(im[:20].reshape(-1, 3), axis=0)
        diff = np.abs(im.astype(np.int16) - bg).sum(axis=2)
        ink = (im.max(axis=2) < 130).astype(np.uint8)                   # dark lettering
        nonbg = diff > 45                                                # anything that is not cream
        ink[int(h * 0.6):] = 0
        halo = cv2.dilate(ink, np.ones((9, 9), np.uint8)).astype(bool)
        picture = nonbg & ~halo                                          # non-cream pixels that are not lettering/its edge
        n, lab, stats, _ = cv2.connectedComponentsWithStats(cv2.dilate(ink, np.ones((5, 5), np.uint8)), 8)
        erase = np.zeros((h, w), np.uint8); k = 0
        for i in range(1, n):
            x, y, bw, bh, area = stats[i]
            if area < 30: continue
            pad = 10
            x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(w, x + bw + pad), min(h, y + bh + pad)
            blob = lab[y0:y1, x0:x1] == i
            if picture[y0:y1, x0:x1].mean() < 0.01:                                       # floats on plain cream -> lettering
                erase[y0:y1, x0:x1] |= blob.astype(np.uint8); k += 1
        erase = cv2.dilate(erase, np.ones((5, 5), np.uint8)).astype(bool) & nonbg | cv2.dilate(erase, np.ones((5, 5), np.uint8)).astype(bool)
        out = im.copy(); out[erase] = bg.astype(np.uint8)
        cv2.imwrite(os.path.join(d, 'notext', os.path.basename(f)), out)
        print(os.path.basename(d), os.path.basename(f), f'erased {k} letter blobs')
