# Music, lyrics, voice — and the copyright line

## Copyright (hard line — explain it kindly, then offer the workaround)

- Never write out lyrics of a real song (not in frames, captions, files or chat), and never bake a copyrighted
  recording into an MP4 (Instagram mutes/blocks it anyway). This holds even when the owner insists — they once asked for
  Katy Perry / Bruno Major lyrics in the frames.
- Workaround that the owner accepted: a **silent, text-free reel** timed to the song's structure + tell them which
  section to pick in the **Instagram app** (Audio → search song → choose section → original-audio volume 0), and that
  Instagram's own **lyrics sticker/display** can show the real lyrics legally.
- If the owner says "don't add music itself / just add song lyrics", they still mean the real song's lyrics → same answer.

## Original songs with ElevenLabs Music (only when the owner wants a song we own)

- Lyrics: rhyming couplets (AABB), even meter ~7–8 syllables per line, plain words, one story beat per frame; ~40–45 s.
  Unrhymed prose lines crammed into 30 s sounded "forced".
- Paste the lyrics into the **custom-lyrics box** (typed newlines get dropped — paste via a ClipboardEvent), one line
  per line; don't put "sing exactly these lines" in the style prompt.
- Make it sound human ("seems AI generated" otherwise): one real instrument, e.g. "live acoustic singer-songwriter,
  one steel-string guitar, warm natural voice, close-mic, recorded in a small room, intimate bedroom demo, slightly
  imperfect, no autotune, no band, minimal production". Generate ~1 min, trim the intro, cut on the beat.
- Post-process lightly: tape/vinyl warmth, small-room reverb, low-pass ~14 kHz, light compression. Offer an
  instrumental-only version too.
- **Credits:** Variants = 1, set the duration you need, lyrics OFF for instrumentals; don't regenerate takes that work.
  If the owner supplies their own track (e.g. a downloaded MP3), use it and cut it to the frames — don't regenerate.
- Log every song + take in the repo's `songs_original.md`.

## Voiceovers (only when the owner explicitly asks — default is no voiceover)

- ElevenLabs v3 / multi-speaker dialogue: put ALL lines of all characters in ONE request (credit-efficient), then
  download the take with the page's download buttons. Library voices can play at 2× — check the rate.
- Match the character: e.g. Fern should sound calm and mature; Subaru energetic; Rem soft and warm.
- Keep the characters "not out of place": voices match canon personality, lines short, timed to panels; add a quiet
  background track under dialogue if the owner wants one.

## Song suggestions for posts

Suggest 3–5 songs that exist in Instagram's library, matching couple + mood, with the section to use
(e.g. "Golden Hour – JVKE, chorus 0:45–1:00"). Series songs first when they fit (fans recognise them), then pop
(Golden Hour, Until I Found You, Nothing – Bruno Major, In Another Life – Katy Perry…). Shortlists per couple/mood:
repo `songs.md`. Record the chosen song in `posting_log.json`.
