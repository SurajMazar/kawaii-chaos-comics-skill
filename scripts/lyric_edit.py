#!/usr/bin/env python3
"""Lyric-edit video from a JSON file: one full-screen comic picture per line, lyric text hand-lettered INSIDE the picture's
empty area on a sketchy hand-drawn background (caption box / speech balloon / paper strip), each line with its own animation.

    python3 scripts/lyric_edit.py music_videos/13_rem_lovegrows/lyric_edit.json             # full render
    python3 scripts/lyric_edit.py music_videos/13_rem_lovegrows/lyric_edit.json --preview   # half size, 15 fps (fast check)
    python3 scripts/lyric_edit.py music_videos/13_rem_lovegrows/lyric_edit.json --still 3.2 # PNG of video second 3.2

All times are SONG seconds ([mm:ss.xx] in an .lrc file -> mm*60+ss.xx). Video second 0 = song second "start".
Top level: output, size [w,h], fps, start, end, audio (optional song file, cut from "start"),
           font, font_index, font_size, ink, highlight, paper, text_y, text_width, picture_zoom
lines[]:   start, end, text, image, anim, box, y, size, rotate, highlight, word_times
   anim: pop | drop | slide | wave | type | write | zoom | shake      (default: cycles through them)
   box:  caption | balloon | strip | none                            (default: cycles caption/balloon/strip)
   image: picture for this line (omit to keep the previous one); word_times: exact start of every word (song s)
"""
import argparse, json, math, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

DEF = dict(output='lyric_edit.mp4', size=[1080, 1920], fps=30, start=0.0, end=None, audio=None,
           font='/System/Library/Fonts/Supplemental/ChalkboardSE.ttc', font_index=2, font_size=92,
           ink='#3A2A26', highlight='#E8507A', paper='#FFF8EC', text_y=0.2, text_width=0.78, picture_zoom=0.05)
ANIMS = ['pop', 'drop', 'slide', 'wave', 'type', 'write', 'zoom', 'shake']
BOXES = ['caption', 'balloon', 'strip']


def hexc(s, a=255):
    s = s.lstrip('#'); return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def clamp(x): return min(max(x, 0.0), 1.0)
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_back(x, k=2.0): x = clamp(x) - 1; return 1 + (k + 1) * x ** 3 + k * x ** 2
def bounce(x):
    x = clamp(x)
    if x < 1 / 2.75: return 7.5625 * x * x
    if x < 2 / 2.75: x -= 1.5 / 2.75; return 7.5625 * x * x + .75
    if x < 2.5 / 2.75: x -= 2.25 / 2.75; return 7.5625 * x * x + .9375
    x -= 2.625 / 2.75; return 7.5625 * x * x + .984375


def cover(path, W, H):
    im = Image.open(path).convert('RGB'); s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def wobble_path(pts, rnd, amp):
    """Sample a closed polygon densely and jitter it -> hand-drawn, slightly uneven outline."""
    out = []
    for i in range(len(pts)):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 18))
        for k in range(n):
            t = k / n; out.append((x0 + (x1 - x0) * t + rnd.uniform(-amp, amp), y0 + (y1 - y0) * t + rnd.uniform(-amp, amp)))
    return out


def rounded(x0, y0, x1, y1, r, steps=6):
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(steps + 1):
            a = math.radians(a0 + 90 * k / steps); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sketch_box(kind, w, h, sc, seed, paper, ink):
    """Sketchy background drawn like the comic: cream fill with faint pencil hatching + a doubled wobbly ink outline."""
    pad = int(60 * sc); W, H = int(w + 2 * pad), int(h + 2 * pad + (70 * sc if kind == 'balloon' else 0))
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    x0, y0, x1, y1 = pad, pad, pad + w, pad + h
    if kind == 'strip':                                   # torn paper strip with two tape pieces
        pts = [(x0 - 10 * sc, y0 + 6 * sc), (x1 + 8 * sc, y0 - 4 * sc), (x1 + 14 * sc, y1 + 5 * sc), (x0 - 4 * sc, y1 - 3 * sc)]
        shape = wobble_path(pts, rnd, 3 * sc)
    elif kind == 'balloon':                               # speech balloon with a tail pointing down
        cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 18 * sc, (y1 - y0) / 2 + 22 * sc
        shape = []
        for k in range(72):
            a = 2 * math.pi * k / 72; shape.append((cx + rx * math.cos(a) + rnd.uniform(-2, 2) * sc, cy + ry * math.sin(a) + rnd.uniform(-2, 2) * sc))
        tip = (cx + rx * 0.35, cy + ry + 60 * sc)
        i = max(range(len(shape)), key=lambda j: shape[j][1] - abs(shape[j][0] - cx - rx * 0.25) * 0.5)
        shape = shape[:i - 2] + [tip] + shape[i + 2:]
    else:                                                 # caption box (slightly tilted rounded rectangle)
        shape = wobble_path(rounded(x0, y0, x1, y1, 26 * sc), rnd, 2.5 * sc)
    d.polygon(shape, fill=hexc(paper, 240))
    hatch = Image.new('RGBA', (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(hatch)   # faint pencil grain
    for k in range(int(W * H / (900 * sc * sc))):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H); hd.line([(x, y), (x + 9 * sc, y - 4 * sc)], fill=hexc(ink, 14), width=1)
    mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).polygon(shape, fill=255)
    im.alpha_composite(Image.composite(hatch, Image.new('RGBA', (W, H), (0, 0, 0, 0)), mask))
    for p in range(2):                                    # sketchy double outline, the second pass slightly off
        off = [(x + rnd.uniform(-1.6, 1.6) * sc, y + rnd.uniform(-1.6, 1.6) * sc) for x, y in shape]
        d.line(off + [off[0]], fill=hexc(ink, 235 if p == 0 else 150), width=max(2, int((5 if p == 0 else 3) * sc)), joint='curve')
    if kind == 'strip':
        for tx in (x0 + 30 * sc, x1 - 90 * sc):
            tape = Image.new('RGBA', (int(70 * sc), int(28 * sc)), (236, 222, 190, 190))
            tape = tape.rotate(rnd.uniform(-14, 14), expand=True, resample=Image.BICUBIC)
            im.alpha_composite(tape, (int(tx), int(y0 - 20 * sc)))
    return im, pad


def word_sprite(word, font, fill):
    d0 = ImageDraw.Draw(Image.new('L', (1, 1))); w = int(d0.textlength(word, font=font)) + 8; h = int(font.size * 1.5)
    im = Image.new('RGBA', (w + 16, h), (0, 0, 0, 0)); ImageDraw.Draw(im).text((8, int(font.size * 0.12)), word, font=font, fill=fill)
    return im


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('json'); ap.add_argument('--preview', action='store_true')
    ap.add_argument('--still', type=float, default=None)
    a = ap.parse_args()
    cfg = {**DEF, **json.load(open(a.json))}; base = os.path.dirname(os.path.abspath(a.json))
    W, H = cfg['size']; fps = cfg['fps']; start = cfg['start']
    if a.preview: W, H, fps = W // 2, H // 2, max(1, fps // 2)
    sc = W / cfg['size'][0]
    lines = sorted(cfg['lines'], key=lambda l: l['start'])
    end = cfg['end'] or max(l['end'] for l in lines)
    pics, cur = {}, None
    for i, l in enumerate(lines):
        if l.get('image'): cur = os.path.join(base, l['image'])
        l['_img'] = cur; l['_i'] = i
        l.setdefault('anim', ANIMS[i % len(ANIMS)]); l.setdefault('box', BOXES[i % len(BOXES)])
        if cur and cur not in pics: pics[cur] = cover(cur, W, H)
    fonts, sprites, boxes = {}, {}, {}
    def F(size):
        if size not in fonts: fonts[size] = ImageFont.truetype(cfg['font'], int(size * sc), index=cfg['font_index'])
        return fonts[size]
    tmp = ImageDraw.Draw(Image.new('RGB', (4, 4)))

    def layout(l):
        font = F(l.get('size', cfg['font_size'])); words = l['text'].split(); sp = tmp.textlength(' ', font=font)
        rows, cur_r, w = [], [], 0; maxw = cfg['text_width'] * W
        for k, wd in enumerate(words):
            ww = tmp.textlength(wd, font=font)
            if cur_r and w + sp + ww > maxw: rows.append(cur_r); cur_r, w = [], 0
            cur_r.append((k, wd, ww)); w += (sp if len(cur_r) > 1 else 0) + ww
        if cur_r: rows.append(cur_r)
        lh = int(font.size * 1.25); bw = max(sum(x[2] for x in r) + sp * (len(r) - 1) for r in rows); bh = lh * len(rows)
        pos = []
        for r_i, r in enumerate(rows):
            rw = sum(x[2] for x in r) + sp * (len(r) - 1); x = (bw - rw) / 2
            for k, wd, ww in r: pos.append((k, wd, ww, x, r_i * lh)); x += ww + sp
        return font, words, pos, bw, bh, lh

    def picture(l, st):
        p = pics[l['_img']]; lt = st - l['start']; dur = max(l['end'] - l['start'], 0.1)
        z = 1 + cfg['picture_zoom'] * clamp(lt / dur)
        prev = lines[l['_i'] - 1]['_img'] if l['_i'] > 0 else None
        if l['_img'] != prev: z *= 1 + 0.06 * (1 - ease_out(lt / 0.35))
        w2, h2 = int(W * z), int(H * z); im = p.resize((w2, h2), Image.BILINEAR)
        x, y = (w2 - W) // 2, (h2 - H) // 2; return im.crop((x, y, x + W, y + H)).convert('RGBA')

    def render(st, fidx):
        act = [l for l in lines if l['start'] <= st < l['end']]
        shown = act[0] if act else max([l for l in lines if l['start'] <= st] or [lines[0]], key=lambda l: l['start'])
        fr = picture(shown, st)
        if shown['_i'] > 0:                                   # quick crossfade when the picture changes
            pl = lines[shown['_i'] - 1]; lt = st - shown['start']
            if pl['_img'] != shown['_img'] and 0 <= lt < 0.18: fr = Image.blend(picture(pl, pl['end']), fr, ease_out(lt / 0.18))
        for l in act:
            font, words, pos, bw, bh, lh = layout(l); lt = st - l['start']; dur = l['end'] - l['start']; anim = l['anim']
            n = max(len(words), 1)
            wt = l.get('word_times') or [l['start'] + k * min(0.22, max(dur - 0.4, 0.2) / n) for k in range(n)]
            sung = max([k for k, t0 in enumerate(wt) if t0 <= st] or [-1])
            out_p = ease_out((st - (l['end'] - 0.2)) / 0.2) if st > l['end'] - 0.2 else 0.0
            key = (l['_i'], l['box'])
            mx, my = int(44 * sc), int(26 * sc)
            if key not in boxes: boxes[key] = sketch_box(l['box'], bw + 2 * mx, bh + 2 * my, sc, 1000 + l['_i'], cfg['paper'], cfg['ink']) if l['box'] != 'none' else (None, int(60 * sc))
            bimg, pad = boxes[key]
            layer = Image.new('RGBA', (int(bw + 2 * mx + 2 * pad), int(bh + 2 * my + 2 * pad + 80 * sc)), (0, 0, 0, 0))
            bp = ease_back(lt / 0.25)                         # box pops in first
            if bimg is not None:
                bi = bimg.resize((max(1, int(bimg.width * bp)), max(1, int(bimg.height * bp))), Image.BILINEAR) if bp < 0.999 else bimg
                layer.alpha_composite(bi, (int((layer.width - bi.width) / 2), int((bimg.height - bi.height) / 2)))
            jit = random.Random(fidx // 3)                    # "boiling" hand-lettering: tiny jitter every 3 frames
            for k, wd, ww, x, y in pos:
                t0 = wt[k] + 0.08; p = (st - t0) / 0.3
                if anim == 'zoom': p = (lt - 0.1) / 0.3
                if anim == 'type': p = 1.0 if st >= t0 else 0.0
                if p <= 0: continue
                hot = k == sung
                col = hexc(l.get('highlight', cfg['highlight']) if hot else cfg['ink'])
                sk = (wd, font.size, col)
                if sk not in sprites: sprites[sk] = word_sprite(wd, font, col)
                im = sprites[sk]; dx = dy = 0.0; s = 1.0; alpha = 1.0; rot = 0.0
                if anim == 'pop': s = ease_back(p)
                elif anim == 'drop': dy = -110 * sc * (1 - bounce(p)); alpha = clamp(p * 3)
                elif anim == 'slide': dx = 130 * sc * (1 - ease_out(p)); alpha = clamp(p * 2)
                elif anim == 'wave': s = ease_back(p); dy = 8 * sc * math.sin(st * 6 + k * 0.9)
                elif anim == 'zoom': s = 1 + 0.6 * (1 - ease_out(p)); alpha = clamp(p * 2)
                elif anim == 'shake': s = ease_back(p); rot = 6 * math.sin(st * 30 + k) * (1 - clamp(p))
                elif anim == 'write':                         # revealed left to right, like being written
                    cw = int(im.width * clamp(p));
                    if cw < 2: continue
                    im = im.crop((0, 0, cw, im.height))
                if hot: s *= 1.08
                if s != 1.0 or rot:
                    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
                    if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
                if alpha < 1 or out_p > 0: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha * (1 - out_p))))
                full_w = sprites[sk].width; ox = pad + mx + x + dx + (full_w - im.width) / 2 * (0 if anim == 'write' else 1) - 8
                oy = pad + my + y + dy + (sprites[sk].height - im.height) / 2 - font.size * 0.12
                layer.alpha_composite(im, (int(ox + jit.uniform(-1, 1) * sc), int(oy + jit.uniform(-1, 1) * sc)))
                if hot and p > 0.3:                           # hand-drawn underline under the sung word
                    ud = ImageDraw.Draw(layer); uy = pad + my + y + lh * 0.9
                    ud.line([(pad + mx + x, uy + jit.uniform(-2, 2)), (pad + mx + x + ww * clamp((p - 0.3) / 0.5), uy + jit.uniform(-2, 2))],
                            fill=hexc(l.get('highlight', cfg['highlight']), int(220 * (1 - out_p))), width=max(2, int(5 * sc)))
            if out_p > 0 and bimg is not None:
                layer.putalpha(layer.getchannel('A').point(lambda v: int(v * (1 - out_p))))
            rot = l.get('rotate', [-3, 2, -1.5, 3, -2][l['_i'] % 5])
            if rot: layer = layer.rotate(rot, expand=True, resample=Image.BICUBIC)
            cy = l.get('y', cfg['text_y']) * H - int(30 * sc * out_p)
            fr.alpha_composite(layer, (int(W / 2 - layer.width / 2), int(cy - layer.height / 2)))
        return fr

    if a.still is not None:
        p = os.path.join(base, f'still_{a.still:.2f}.png'); render(start + a.still, int(a.still * fps)).convert('RGB').save(p); print('->', p); return
    out = os.path.join(base, cfg['output']); out = out.replace('.mp4', '_preview.mp4') if a.preview else out
    silent = out.replace('.mp4', '_noaudio.mp4') if cfg['audio'] else out
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', silent],
                          stdin=subprocess.PIPE)
    n = int(round((end - start) * fps))
    for f in range(n):
        ff.stdin.write(render(start + f / fps, f).convert('RGB').tobytes())
        if f % (fps * 5) == 0: print(f'{f / fps:5.1f}s / {n / fps:.1f}s', file=sys.stderr)
    ff.stdin.close(); ff.wait()
    if cfg['audio']:
        aud = cfg['audio'] if os.path.isabs(cfg['audio']) else os.path.join(base, cfg['audio'])
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-ss', str(start), '-i', aud, '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True); os.remove(silent)
    print('->', out)


if __name__ == '__main__':
    main()
