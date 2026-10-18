# HARD QA GATE — every image, no exceptions (owner, 2026-10-16)

Owner: "it totally looks AI generated", "why are you making a reel from such a messed-up generation",
"choosing one from another is not proper QA" — and every later complaint is folded into the general checks below.

## Process (mandatory)
1. **Judge each image ALONE against the checklist below.** Never compare candidates to pick the "less bad" one.
   A version that fails ANY item is rejected — even if it is the best of the batch. If every version fails:
   fix the prompt (simplify!) and regenerate. Shipping nothing is better than shipping a fail.
2. **Write `<piece>/qa.md`** for the image: for EACH panel, one sentence "what a stranger sees" (written from the
   image, not from the script), then every check A–J as PASS/FAIL with the reason.
3. **Unsure = FAIL.** If you have to explain or squint, it fails.
4. Only when every item passes, append the line `PASS <sha1 of strip.png>` to qa.md.
   `scripts/build_reel.sh` refuses to build a reel without it (and refuses if strip.png changed afterwards).
5. Only then build the reel / send to the owner.

## Zero-tolerance rules for the reviewer (me)
- **No comparing.** "B is better than A" is never a reason to keep B. Each image passes or fails on its own merits.
- **Banned words in qa.md:** "acceptable", "minor", "borderline", "close enough", "mostly", "fine-ish", "ok-ish",
  "reads well enough", "I'll accept". If I'm tempted to write one, that item is a FAIL.
- **Zoom every panel.** Crop each panel at full resolution (PIL) and look at it alone before ticking any item;
  a thumbnail of the whole strip is never enough.
- **Describe before judging.** Write the "what a stranger sees" sentence for every panel *before* re-reading the
  script, then compare. If the sentence doesn't contain the script's key action, the panel fails.
- **The owner's past complaints are tests.** Re-run every rule in style.md (each was a real complaint) on every image.
- **Attempt limit.** Up to 3 fresh full-prompt attempts per strip (fixing the prompt each time). If attempt 3 still
  fails, send the owner the failure list and the best prompt, not the image.
- **Nothing leaves without PASS.** No reel, no send, no "final" commit without the `PASS <sha1>` line. Rejected
  images go to `raw/rejected/` with the failing item in the file name.
- Music videos: every frame gets its own `PASS <sha1> <frame file>` line in `<mv>/qa.md`;
  `scripts/build_music_video.sh` refuses to build otherwise.

## Checklist — every answer must be YES (general principles; every past complaint is an instance of one of these)
**A. The story reads cold.** Describe each panel from the image alone; the description must contain the script's key
   action. The punchline action is the largest, clearest thing in the last panel. Hidden, small or ambiguous → FAIL.
**B. Every object is accounted for.** List every prop the script needs with its count; the image has exactly those —
   nothing missing, nothing extra, nothing duplicated or repeated in rows.
**C. Continuity across panels.** Anything that appears in more than one panel (character, prop, outfit, seat, place,
   lighting) keeps the same size, shape, colour, position and design unless the story changes it. Crop every
   instance and compare them side by side at the same scale — never judge continuity from the whole-strip view.
**D. Cause and effect.** Every change between panels has a visible cause, and every action has its consequence:
   what is split, given, eaten, broken, moved or worn shows the result that action would really produce, and nothing
   appears or disappears without a reason. Ask "what must be true in the next panel because of this one?"
**E. Physically possible.** Bodies, objects and actions behave as in the real world (gravity, reach, who holds what,
   what is visible from where, scale and perspective).
**F. Characters on-model.** Match the character sheet; same proportions and head size in every panel; heights per
   sheet; each character exactly once per panel; group positions unchanged; anatomy correct (count limbs and fingers).
**G. Style = master side by side.** Line, fill, palette, background busyness no greater than style_ref_master.jpg.
**H. Text exact.** Only the script's lines, correctly spelled, tails at speakers, reading order right.
**I. Locks.** Every standing rule in style.md (outfits, colours, eyes, etc.).
**J. Gut check.** Would the owner say "looks AI" or "doesn't make sense"? → FAIL.

## Prompt rules that prevent fails
- Fewest possible props, each with an exact count and a fixed size/design stated once and reused in every panel.
- For every action that changes an object, spell out the resulting state in the following panels.
- Write the punchline action as a close-up with the key object large and centred.
- Background as plain as the master in every prompt. No titles. One action per panel. Max 2 balloons.
- State the fixed LEFT/RIGHT order of every pair in EVERY panel (e.g. "Subaru always on the LEFT of Rem") — GPT swaps partners' sides between panels otherwise.
- Every cause the punchline depends on must be drawn explicitly (e.g. "her hand touching his hand" before the faint).
- Heights are MEASURED, never eyeballed: compare figure heights from ink extents (Rem/Subaru ≈ 0.84 is the house standard; other girls vs partners per canon).
