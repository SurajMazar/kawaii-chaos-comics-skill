---
name: kawaii-chaos-comics
description: Produce super-chibi doodle anime-couple comic strips, silent strip reels and music-video (lyric/photo-montage) reels for the Instagram account @kawaiichaos.comics (Kawaii Chaos Comics) — Rem × Subaru and other anime couples (Fern × Stark, Mai × Sakuta, Marin × Gojo, Waguri × Rintaro…). Covers the locked art style, character sheets, ChatGPT image generation via Claude in Chrome, a strict QA + redraw gate, reel building with ffmpeg, ElevenLabs music/voice, captions, song picks and posting. Use this skill whenever the user asks for an anime couple comic, strip, reel, music video, character sheet, caption, pinned comment or song suggestion for their comic account, mentions Kawaii Chaos / kawaiichaos, Rem, Subaru, Re:Zero fan comics, or asks to fix/redraw/QA a strip or frame — even if they don't name the skill.
---

# Kawaii Chaos Comics — anime couple strips & reels

The owner runs **@kawaiichaos.comics**: wholesome/funny fan comics about anime couples (mostly **Rem × Subaru**),
drawn in one locked **super-chibi doodle webcomic** style. Every rule below came from the owner catching a real
mistake — they look at every image closely, and anything that "looks AI generated" or breaks logic gets rejected.
Quality beats quantity: one perfect frame is worth more than five fast ones.

Project repo (if it exists on this machine): `~/personal/anime-couple-comics` — read its `AGENTS.md`, `style.md`,
`couples.md`, `songs.md` first; they are the live source of truth and may be newer than this skill. If the repo is not
present (e.g. claude.ai), use this skill's references and do the steps by hand.

## Reference files (read when needed)

| File | Read it when |
|---|---|
| `references/style-and-prompts.md` | writing ANY image prompt — style header, all lock lines, character-sheet prompt, frame prompt templates |
| `references/qa_rules.md` | the HARD QA GATE — read before judging ANY image |
| `references/qa-gate.md` | detailed checklist with the history behind each check |
| `references/chatgpt-automation.md` | generating images in ChatGPT through Claude in Chrome (queue "pump", downloads, pitfalls) |
| `references/reels-and-music-videos.md` | building strip reels or music videos, timing to a song, hard cuts vs dissolves |
| `references/audio-and-copyright.md` | anything with music, lyrics, ElevenLabs songs or voiceovers |
| `references/posting.md` | captions, pinned comments, song picks, posting flow, logging |
| `references/style_ref_master.jpg` | attach to every image prompt (the locked art style) |

## The non-negotiables (short version — details in the references)

1. **Locked style:** ~2-head super-chibis, rough sketchy marker lines, flat muted crayon colours, warm beige paper-tone
   background with faint room hints and ≤2 simple doodled props, small full-body chibis with air around them, handwritten lettering. Never adult/teen proportions, glossy rendering,
   glow, gradients, detailed scenery, crowds or lamps. Attach `style_ref_master.jpg` to every prompt.
2. **Character sheet first:** every piece starts with a character sheet of exactly its cast *in the outfits that piece
   uses* (front + back, height guide, key props), made in a fresh chat, QA'd, then attached to every frame prompt.
   Text descriptions alone drift (Subaru turned into an older teen, Sakuta looked like Subaru, Shaula was off-model).
   For side characters build the sheet from official art the owner provides. The sheet carries DESIGNS only; style always
   comes from `style_ref_master.jpg` (a sheet copied "exactly" dragged one strip's style off).
3. **Couple rule:** the featured couple is always THE couple; others are cameos, never a love interest.
4. **Outfit lock:** clothes never change unless the script asks. Rem/Ram: no orange anywhere (orange is only Subaru's
   tracksuit trim). When the owner wants "different clothes", design the new outfit on the character sheet and keep
   hair/face/signature accessory (Rem's X clip + pink ribbon).
5. **Rem's eye open** in most panels (closed `^ ^` smile at most once). **Height lock:** Rem's head top = Subaru's eye level.
6. **Anti-AI look:** one clear action per panel, ≤2 balloons per panel, no copy-paste repeats, varied shots, no line-ups.
7. **Anatomy lock:** 2 arms, 2 legs, mitten hands, no fused clothes, clear whose arm is whose in hugs.
8. **Logic & continuity:** nothing exists before the story creates it; a sequence keeps one place/day/perspective and
   a recurring landmark; objects work like in the real world (a camera never appears in its own photo; you can't
   shoot from the back of a camera; a jack-o'-lantern has 2 eyes, 1 nose, 1 mouth).
9. **HARD QA GATE on every image** (`references/qa_rules.md`): judge each image alone against an absolute checklist —
   never "pick the better of two"; write `qa.md` per piece (what a stranger sees per panel + PASS/FAIL per check);
   unsure = FAIL; the punchline action must be the clearest thing in the last panel; no rows of identical props;
   reel only after `PASS <sha1>`. If every version fails, simplify the prompt and regenerate.
10. **Copyright:** never reproduce real song lyrics or bake copyrighted songs into a video. Real songs → silent reel;
    the owner adds the song (and Instagram's lyric sticker) in the Instagram app.
11. **Never post** without the owner explicitly asking. Downloads of the owner's own generated images are fine.
12. **Ideas first when asked:** if the owner says "list ideas before doing anything", list and wait; music videos
    must be NEW concepts (check existing synopses — never reuse a strip's joke).

## Workflow — comic strip

1. **Plan** `projects/NNN_<name>/synopsis.md` (`python3 scripts/new_project.py <name>` makes the numbered folder):
   couple, premise, 2–5 panels with one short line each, the punchline in the last panel. The strip must explain
   itself to someone who never saw the anime (panel 1 states the premise). Check the joke actually makes sense.
2. **Character sheet** (see rule 2) → QA → `projects/NNN_<name>/charsheet.png` (reuse only if cast + outfits identical).
3. **Layout:** `python3 scripts/comic_layout.py projects/<name>/layout --panels N` — attach `layout.png`, paste `layout.txt`.
4. **Prompt** = style header + all lock lines + layout + panel script (`references/style-and-prompts.md`), with
   `style_ref_master.jpg` + charsheet attached. One image per message.
5. **Generate** in ChatGPT via Claude in Chrome (`references/chatgpt-automation.md`), download, unbundle.
6. **QA gate** (`references/qa-gate.md`) at full size — redraw what fails.
7. **Reel:** `scripts/build_reel.sh NNN_<name>` → `upload/NNN_<name>_strip_reel.mp4` (silent) + `_strip.png`.
8. **Caption + song shortlist** (`references/posting.md`); `python3 scripts/update_trackers.py`.
9. Show the owner the strip (send the file) — do not post unless asked.

## Workflow — music video (photo montage / lyric reel)

1. Propose 2–3 NEW concepts + a song that fits; wait for the pick if the owner asked to choose.
2. Write the frame list in `music_videos/NN_<name>/synopsis.md`: story order that makes sense (making → montage →
   ending), one place/day for montage frames, a recurring landmark, the same perspective, real-world-plausible actions.
3. Character sheet in the piece's outfits → QA.
4. Queue all frames with identical headers (style + outfits + perspective + logic lines) and charsheet attached.
5. QA every frame, check continuity ACROSS frames (same props, same outfits, same canvas framing), redraw failures.
6. Build: time cuts to the song's beat/sections (`references/reels-and-music-videos.md`) — verses with soft dissolves,
   chorus with hard cuts if the owner wants energy. Real song → `_reel_silent.mp4`.
7. Send the reel + caption + pinned comment + exact song name/section to use in the Instagram app.

## Working style with this owner

- They send short messages, often several in a row while you work — fold each into the current task immediately.
- They are visual and detail-oriented: when they point at a flaw, fix that frame AND add a general rule (in the
  repo's `style.md` + memory) so it never recurs, then re-check every other frame for the same flaw.
- Send finished files (images/reels) rather than describing them; keep text replies short.
- Be careful with paid credits (ChatGPT image quota ~40–50 / 5 h, ElevenLabs credits): QA prompts before sending,
  one image per message, Variants=1, don't regenerate things that already pass.
