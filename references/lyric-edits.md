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
- Times are SONG seconds; every line has start + end. Words are spread evenly over the WHOLE line (owner: text must appear along the duration) and the full line holds ~0.25-0.6 s before it leaves; word_times overrides. Owner fills in their own lyrics; Claude does not reproduce
  copyrighted lyrics.

**Always (owner 2026-10-23: "generate sample everytime"):** after ANY change to lyric_edit.py, a lyric_edit JSON or its pictures, render `<mv>/lyric_edit_sample.json` and send the mp4 — never report a change without a watchable sample.

## v4 (2026-10-24, owner's Yor "good girl" reference reel) — 14_yor / 15_rem / 16_yuno _goodgirl
- `style: block` = the reference lyric-edit look: left-aligned stack, *BIG* word + small rows (Baloo 2 ExtraBold caps,
  white, thick ink outline + soft halo — reads on cream AND night frames), words slide in, big words land. No *…* → first word big. y ≈ 0.15.
- `shots` per line = several cuts inside one line: new picture at `at`, or the same picture as a close-up
  (`zoom` 1.6 + `focus`); `cut` ghost | hard | flash | shake | whoosh. Sweet→dark flip on line 1 = 2 frames + flash.
- `fit: cover` fills 9:16 from 2:3 pictures (sides cropped) — needed when frames have full backgrounds.
- Frames WITH backgrounds (owner: "proper backgrounds") still must look like ONE PANEL CUT FROM THE MASTER STRIP:
  first tries were rejected ("doesn't match our art style", "looks AI generated") for perspective rooms, town views
  through windows, light rays, glossy eyes. Prompt now has STYLE CHECK + simple faces (oval eye + one white dot, flat
  hair shapes) + no decor (banners/sconces/panelling/shiny floors) + night = whole picture dark navy.
  Make + QA ONE frame per character before the batch; side-by-side with style_ref_master.
- Recurring QA catches: "stiletto" → GPT draws shoes (say "gold needle-daggers"); morning star must be ONE weapon
  (handle–chain–ball, she holds the handle); continuity of time of day across consecutive frames; jokes must be BIG
  enough to read (stink lines); Rem/Subaru height on every two-shot.
- Parallel: one ChatGPT tab per character; `__newchat()` (SPA new chat keeps the sender), PICKA input forwards the board
  into the composer's file input; `__dl(name)` re-downloads the latest image if `__send1`'s auto-download stalls.

## Lyric Studio web app (2026-10-24) — `studio/run.sh` → http://localhost:8770
FastAPI (`studio/server.py`, imports lyric_edit.load/write_video → previews are pixel-identical, stills ~20 ms cached)
+ React/TS/Vite/Tailwind/zustand (`studio/web`). Edit lines/timings/text/looks/cuts/close-ups, live play synced to the
song, timeline drag + tap-to-time (T), LRC import, quick/final render with progress, save history in `.studio_history/`.
Point the owner here for editing instead of hand-editing JSON. Port 8770 (8765 is the MediBang site).
