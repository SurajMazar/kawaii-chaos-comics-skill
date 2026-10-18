# Strict QA gate — run on EVERY image before keeping, sending or building with it

The owner zooms into everything, and every rule below is a complaint they actually made. QA is **absolute, not
comparative**: an image passes only if every item passes. Picking "the better of two" is NOT QA — owner:
"choosing one from another is not a proper qa", after a cluttered "Luck Stat" strip with cakes everywhere and an
invisible punchline was chosen over a worse sibling and turned into a reel.

## The hard gate (process — mandatory)
1. Judge each image ALONE. A version that fails any item is rejected even if it is the best of the batch. If all
   fail: simplify the prompt and regenerate (max 3 fresh attempts, then send the owner the failure list instead).
2. Crop and look at EVERY panel at full resolution before ticking anything.
3. Write `<piece>/qa.md`: per panel one sentence "what a stranger sees" (written from the image BEFORE re-reading the
   script), then items A–J below as PASS/FAIL with reasons.
4. Unsure = FAIL. Banned words in qa.md: acceptable, minor, borderline, close enough, mostly, fine-ish, "I'll accept".
5. Only when all pass: append `PASS <sha1 of strip.png>` (music videos: `PASS <sha1> <frame file>` per frame).
   The repo's `scripts/build_reel.sh` / `build_music_video.sh` refuse to build without it. No reel, no send, no
   final commit before that line exists. Rejected images go to `raw/rejected/<name>_<failed item>.png`.

## A–J checklist (every answer must be YES)
- **A Story reads cold:** each panel's stranger-sentence contains the script beat; the PUNCHLINE ACTION is the
  biggest, clearest thing in the last panel (shown close). Small/hidden/ambiguous key action → FAIL.
- **B Minimal props, counted:** only scripted props, each counted exactly. Rows of identical objects (cakes, cups,
  plates, hearts, lamps) are the #1 AI tell → FAIL.
- **C Background no busier than the master:** warm beige paper, faint hints only.
- **D Style = master side by side** (sections 0–1).
- **E Characters** (sections 1, 3): on-model, ~2.5-head chibis, same head size every panel, heights per sheet, each
  character exactly once per panel, couples together, seats unchanged.
- **F Hands & anatomy** (section 4): count fingers on gesture hands (rock = fist, paper = open hand, scissors = two fingers).
- **G Real world** (section 7). **H Text** (section 8). **I Locks** (section 3). **J Gut check:** would the owner say
  "looks AI"? → FAIL.

Prompt rules that prevent fails: fewest possible props with exact counts ("ONLY two slices of cake in the whole
strip"); punchline as a close-up with the key object large and centred; "background as plain as image 1"; no titles.

The detailed checks behind A–J follow.

## 0. Side-by-side with the master (do this FIRST)
Paste the new image next to `style_ref_master.jpg` at the same size. Compare, as seen in the MASTER (never from notes): line weight (bold dark sketchy marker
outlines, uneven thickness), eyes (simple dot/bean/line, no detailed irises), fills (clean flat colour, no grain/noise/aura gradients),
background (minimal cream),
character scale (small full-body chibis with air, not crammed heads). If it would not pass as the same artist, redraw.
The character sheet carries DESIGNS only — a sheet drawn slightly heavier will drag the strip's style if the prompt says "copy image 2 exactly";
say "image 2 for designs only, style from image 1" (owner: "the art looks off", 2026-10-15).

## 1. Style
- [ ] ~2-head super-chibis, giant round heads, mitten hands, bean/line eyes — like `style_ref_master.jpg`.
- [ ] Bold dark sketchy marker lines with uneven thickness, flat colours; no gloss, glow, gradients, crayon noise, auras, bokeh, painterly sky.
- [ ] Character sheets pass this same style check before use (owner 2026-10-18: a tall, crayon-textured Loid/Yor sheet "looks AI").
- [ ] Mostly plain cream/pastel background, ≤2 simple doodled props. No detailed streets, lamps, crowds, rooms.
- [ ] COUNT HEADS in every panel: each character has the master's chibi proportions (~2.5 heads, normal
      chibi body — not stretched, not a squashed stump) and the same size panel to panel. Standing / serving /
      walking poses get stretched to adult legs (butler Subaru at ~3.5 heads — owner: "subaru?"); say "tiny 2-head chibi,
      same size as the other panels, very short legs" in those panel prompts.
- [ ] Compare HEAD SIZES panel to panel: nobody shrinks or grows. Don't seat characters "on the far side" of a table —
      GPT shrinks them (owner: "why did Rem and Fern become smaller now"); keep everyone at the same distance from the viewer.
- [ ] Same style as every other frame of the piece (compare side by side on a contact sheet).

## 2. Not AI-looking
- [ ] No copy-paste repeats (identical balloons, props, hearts in a grid).
- [ ] Natural varied poses; not a stiff line-up facing the viewer; shots vary across panels.
- [ ] One clear action per panel; ≤2 balloons per panel.

## 3. On-model (compare with the character sheet)
- [ ] Faces/hair/eye colour/outfits match the sheet exactly (no character looking like another one).
- [ ] Heights consistent (Rem's head top = Subaru's eye level) across all panels/frames.
- [ ] Outfit lock: nobody's clothes changed unless the script says so. **Rem/Ram: zero orange** (check sleeves near
      Subaru — ChatGPT bleeds his orange trim onto her).
- [ ] Rem's visible eye OPEN in most panels (closed `^ ^` max once).

- [ ] Group scenes: each couple sits/stands TOGETHER (double date = G-B-B-G with the boys in the middle when they talk);
      the same seat order in every panel (owner: "why are boys and girls sitting separately").

## 4. Anatomy (zoom on hugs, hand-holding, overlaps)
- [ ] Each character: 2 eyes, 2 arms, 2 legs, mitten hands; no extra/merged/twisted limbs; no warped faces.
- [ ] Clear whose arm is whose; sleeves belong to the right arm; clothes not fused between characters.

## 5. Detail & count check — COUNT the parts
- [ ] Every countable object has the right number of parts (jack-o'-lantern = exactly 2 eyes + 1 nose + 1 mouth;
      "five polaroids" = five; ONE camera; no duplicated props or accessories).
- [ ] The action matches the script (who holds what, where the knife cuts, who speaks).

## 6. Story logic & continuity (across the whole piece)
- [ ] Nothing exists before the story creates it (no printed photo before the first photo is taken, no finished craft
      before it is made).
- [ ] Montage locations connect: one route on one day (or a clearly shown sequence), same season/weather, time of day
      moving forward, a recurring landmark visible (e.g. the same Ferris wheel in every photo).
- [ ] Same perspective within a sequence: same camera angle/height and framing; props, outfits, accessories and
      background objects identical unless the story changes them. "Things cannot change suddenly."
- [ ] All frames share the same canvas size and framing (every polaroid fills the frame the same way).

## 7. Real-world plausibility — ask "could this physically happen?"
- [ ] Cameras: the lens faces the subject; a photo never shows the camera taking it (selfie = arm reaching toward the
      viewer, camera out of frame); nobody shoots from the back of a camera; viewfinder side faces the photographer.
- [ ] Camera orientation: if the LENS is visible, the camera is shooting the viewer — a selfie or a flash in someone's
      face needs the camera seen from the side/back with the lens pointing at that person.
- [ ] Held things are gripped by a hand attached to the right person; cups/cones upright; knives cut where the blade is;
      umbrellas above heads with rain landing on the uncovered side.
- [ ] Standing characters stand on the FLOOR beside furniture, whole body visible to the shoes — never overlapping or "in"
      a chair (owner: "why are they standing on the chair").
- [ ] Clothes/accessories sit correctly (masks over faces, hats on heads, straps over shoulders); gravity works.
- [ ] Light and time of day agree with the scene and with the sequence order.
- [ ] Perspective and scale consistent (a distant Ferris wheel is small).

## 8. Text
- [ ] Every line spelled exactly as written; nothing else written; setup read before punchline (top-left first).
- [ ] No brand logos. Music-video frames for real songs: no lettering at all (or erase with `scripts/strip_text.py`).

## Tools
- Contact sheet of all frames to compare style/continuity: PIL paste resized frames side by side, then Read it.
- `python3 scripts/qa.py reel.mp4` (repo) → contact sheet every 0.5 s of a rendered reel; check cut-off characters,
  gutters peeking at the edges, ghosted frames.
- When the owner flags a new kind of flaw: fix it, add a general rule to `style.md` + this checklist, then re-check every
  other frame of the piece for the same flaw.
