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

## Video — scripts/lyric_edit.py + <mv>/lyric_edit.json
    $PY scripts/lyric_edit.py music_videos/NN_x/lyric_edit.json [--preview | --still 3.2]
- Times are SONG seconds (from an .lrc: [mm:ss.xx] -> mm*60+ss.xx); every line has "start" and "end";
  video second 0 = song second "start". Optional "audio" muxes a song file cut from "start".
- Per line: text, image, anim (pop | drop | slide | wave | type | write | zoom | shake), box (caption | balloon | strip | none),
  y (0-1 text position), size, rotate, highlight, word_times (exact start of each word).
- Look: Chalkboard SE Bold hand-lettering in comic ink, sketchy hand-drawn box with pencil grain + doubled wobbly outline,
  sung word pink + hand-drawn underline, "boiling" jitter every 3 frames, picture slow push-in + punch-in on change.
- Lyrics text: Claude does not reproduce copyrighted song lyrics. Ship the JSON with placeholder text; the owner fills in
  their own lyrics (or uses Instagram's lyrics sticker for licensed songs).
