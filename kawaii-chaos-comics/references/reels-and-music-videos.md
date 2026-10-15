# Building reels

Toolchain lives in the repo (`~/personal/anime-couple-comics/scripts`, shared with `../instagram-comic-reels-skill`).
Python with cv2/PIL: `/Users/surajthapa/personal/instagram-comic-reels-skill/.venv/bin/python` (set `PY=` for the .sh scripts).
All reels are **silent** unless the audio is original/owned — the owner adds licensed songs in the Instagram app.

## Folder layout (numbered so the owner can sort by order)

```
projects/NNN_<name>/       strips: synopsis.md, charsheet.png, layout/, raw/, strip.png, strip_reel/
music_videos/NN_<name>/    music videos: synopsis.md, charsheet.png, frame1..N.png, raw/ (+ raw/rejected/), audio/, reel/
upload/NNN_<name>_strip.png, upload/NNN_<name>_strip_reel.mp4
upload/music_videos/NN_<name>_reel.mp4 (+ _reel_silent.mp4, _song.mp3)
```
`python3 scripts/new_project.py <name> [--kind music_videos]` creates the next numbered folder (safe to call twice).

## Strip reel (panel by panel, full strip only at the end)

```bash
scripts/build_reel.sh NNN_<name>      # detect_panels -> strip_reel.py --silent --per 3.6 -> render.py -> ffmpeg
scripts/build_missing.sh              # every project with strip.png but no reel (lock dir prevents double runs)
```
Check the stills / contact sheet: ChatGPT draws rows at other heights than the wireframe → panels cut off or bleeding;
`detect_panels.py` measures the real borders. Characters must never be cut off at the frame edge.

## Music video (lyric reel / photo montage)

- Frames: `music_videos/NN_<name>/frame1..N.png`, all the same canvas size and framing.
- `times.json`: `[{"line": "frame1", "start": 0, "end": 2.4}, …]` — one entry per frame, cut on the song's beats/sections.
- Build:
  ```bash
  $PY scripts/lyric_reel.py music_videos/NN_<name> --times music_videos/NN_<name>/times.json --duration <sec>
  $PY scripts/render.py music_videos/NN_<name>/reel/storyboard.json
  ffmpeg -y -i music_videos/NN_<name>/reel/lyric_reel.mp4 -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
    -movflags +faststart -an upload/music_videos/NN_<name>_reel_silent.mp4
  ```
  With an owned song (ElevenLabs): `scripts/build_music_video.sh NN_<name>` (reel length = song length; needs
  `audio/song.mp3` + `audio/line_times.json`).
- **Dissolves vs hard cuts:** `lyric_reel.py` adds a 0.45 s dissolve (`transition_in`) to every shot after the first.
  The owner wants the chorus to just change frame — delete `transition_in` from the chorus shots in
  `reel/storyboard.json` before `render.py`. Verses/intro keep the soft dissolve.
- **Timing to a real song:** you can't ship the song, but you can time to it. Use the song's known BPM/structure
  (e.g. verse ≈ 2.4–2.6 s per frame, chorus hard cuts on every 2 beats ≈ 1.2–1.6 s, hold the emotional peak frame
  ~3 s, final frame ~3.5 s). With an audio file the owner provides, `scripts/song_times.py` (faster-whisper word
  timestamps) or a beat grid (librosa) gives exact cut points. Tell the owner which section of the song to pick in
  the app (e.g. "start at the chorus, 0:45").
- **Text-free frames:** for real songs the reel carries no lyrics of ours; `python3 scripts/strip_text.py music_videos/NN_<name>`
  erases hand-lettering that floats on cream into `notext/` (characters untouched).
- QA the render: `python3 scripts/qa.py upload/…mp4` → contact sheet; check no character cut off, no ghosted frames.

## Example: polaroid photo-booth video (Golden Hour – JVKE, ~24 s)
Frames 1–4 (making the camera at home) ~2.5 s each with dissolves → photos 5–7 ~1.6 s hard cuts → photo 8 (Ferris
wheel kiss) ~3 s → photo 9 ~2 s → frame 10 (asleep under the corkboard of the day's five photos) ~3.5 s.
