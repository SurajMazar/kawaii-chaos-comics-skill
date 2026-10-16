# Strict QA gate — run on EVERY image before keeping, sending or building with it

The owner zooms into everything. Each item below exists because a shipped image failed it ("3 eyes?", "how is there
already a picture", "how can you take a picture from the back of the camera", "Rem's eyes always closed",
"sometimes Rem is short sometimes tall", "looks AI generated", "Sakuta looks like Subaru"). Look at the image at full
size (Read the PNG; zoom/crop with PIL for small regions), then answer every question. Any "no" → redraw.

**Redraw policy:** one targeted edit is fine; if a second round is needed, regenerate fresh with all fixes in the full
prompt — stacked edits degrade proportions and composition.
**How:** ask ChatGPT to fix the specific failure in the same chat (an edit: "keep everything else the same,
fix only …"), or regenerate with a sharper prompt. Max 2 redraws per image; if it still fails, tell the owner exactly
what is off instead of shipping it. Never send a frame you would reject.

## 0. Side-by-side with the master (do this FIRST)
Paste the new image next to `style_ref_master.jpg` at the same size. Compare line weight (thin light pencil, not heavy black),
fills (soft flat crayon, no scratchy hatching), palette (muted), background (warm beige paper tone with faint room hints, not stark white),
character scale (small full-body chibis with air, not crammed heads). If it would not pass as the same artist, redraw.
The character sheet carries DESIGNS only — a sheet drawn slightly heavier will drag the strip's style if the prompt says "copy image 2 exactly";
say "image 2 for designs only, style from image 1" (owner: "the art looks off", 2026-10-15).

## 1. Style
- [ ] ~2-head super-chibis, giant round heads, mitten hands, bean/line eyes — like `style_ref_master.jpg`.
- [ ] Thin sketchy uneven lines, flat muted crayon colours; no gloss, glow, gradients, bokeh, painterly sky.
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
