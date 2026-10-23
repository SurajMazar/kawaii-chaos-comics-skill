# Lyric edits (Instagram "lyric video" reels) — owner, 2026-10-23

Format the owner wants (like trending lyric edits): one FULL-SCREEN comic picture per song line, the line's words hand-lettered
INSIDE the picture's empty area, on a sketchy comic background, each line with its own animation, cut exactly on the song's
line timings. Song is added in the Instagram app.

## Pictures (ChatGPT, one image per line, strict QA)
- Character sheet first (outfits used), then one prompt per line. Board = style master + approved MV frames (A2) + sheet.
- TALL 2:3 (1024x1536); the TOP 40% left EMPTY (plain cream / flat sky) for the lettering; character in the lower 60%,
  centred in the middle 70% of the width (edges get cropped to 9:16).
- Each picture ACTS OUT what its line is about (story follows the song, relatable, cute) — not random scenes.
- Anti-AI wording in every prompt: wobbly imperfect sketch lines, flat colour slightly missing the lines, no glossy hair
  shine, no rim light/airbrush, no detailed scenery, no depth-of-field blur. Compare with an approved MV frame side by side.

## Video — scripts/lyric_edit.py + <mv>/lyric_edit.json (v3, 2026-10-23, from the owner's two reference edits)
    $PY scripts/lyric_edit.py music_videos/NN_x/lyric_edit.json [--preview | --still 3.2]
- NO boxes (owner: boxes looked ugly). Words build ON the picture's empty top area. Styles per line:
  verse (cute hand-lettering Gaegu, types on), stack (zig-zag rows, words rise), chorus (Baloo 2 ExtraBold caps,
  yellow/white/red + ink outline, slam). *word* = big Permanent Marker emphasis that pulses; "/" = row break.
- crayon-painted colour stripe behind text (optional), emoji accents, white flash on chorus hits, picture punch-in,
  ghost crossfades, subtle letter jitter on the TEXT only (owner 2026-10-23: no wobble on the image — boil_image 0), black signature end card.
- Fonts live in the repo fonts/ (OFL Google Fonts). Auto shrink-to-fit keeps every row on screen; shared baseline.
- Times are SONG seconds; every line has start + end. Owner fills in their own lyrics; Claude does not reproduce
  copyrighted lyrics.

**Always (owner 2026-10-23: "generate sample everytime"):** after ANY change to lyric_edit.py, a lyric_edit JSON or its pictures, render `<mv>/lyric_edit_sample.json` and send the mp4 — never report a change without a watchable sample.
