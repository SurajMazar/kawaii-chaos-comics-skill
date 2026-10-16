# HARD QA GATE — every image, no exceptions (owner, 2026-10-16)

Owner: "it totally looks AI generated", "where is the cake sharing", "cakes are all over the place",
"why are you making a reel from such a messed-up generation", "choosing one from another is not proper QA".

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

## Checklist — every answer must be YES
**A. Story reads cold.** Read the panels without the script: does each panel's one-sentence description match the
   script beat? Is the PUNCHLINE ACTION the biggest, clearest thing in the last panel (e.g. the cake visibly being
   split and handed over, shown close)? If the key action is small, hidden or ambiguous → FAIL.
**B. Minimal props, counted.** Only props the script needs, each COUNTED and matching the script exactly
   (e.g. exactly 2 cake slices). NO rows of identical objects (cakes, cups, plates, hearts, lamps) — repeated
   copy-paste props are the #1 "AI-generated" tell → FAIL.
**C. Background no busier than style_ref_master.jpg.** Warm beige paper tone with faint hints; no detailed rooms,
   beams, windows + lamps + shelves together, scenery depth, crowds, painted skies → FAIL.
**D. Style = master side by side:** thin light pencil lines, flat muted crayon fills, no gloss/hatching/glow.
**E. Characters:** on-model vs character sheet; ~2.5-head chibis; same head size every panel; heights per sheet;
   each character exactly once per panel; couples together; seats/positions unchanged between panels.
**F. Hands & anatomy:** count fingers on gesture hands (rock = fist, paper = flat open hand, scissors = two fingers,
   peace sign, pointing); two arms/legs each; clear whose limb is whose; nothing fused.
**G. Real world:** every action physically possible, objects where they would really be (on the table, in the hand
   that holds them, gravity, cameras face their subject, people stand on the floor).
**H. Text:** exactly the script's lines, nothing else (no title, no extra SFX, no Japanese); tails at speakers;
   setup read before reply.
**I. Locks:** outfit lock, no orange on Rem/Ram, Rem's visible eye open (closed max once), eyepatch side, etc.
**J. Gut check:** would the owner say "looks AI"? (busy symmetry, copy-paste, glossy, over-detailed, stiff line-ups,
   cluttered tables) → FAIL.

## Prompt rules that prevent fails
- Fewest possible props; state exact counts ("ONLY two slices of cake in the whole strip").
- Write the punchline action as a CLOSE-UP with the key object large and centred.
- "Background as plain as image 1" in every prompt; no "tavern/restaurant/room" detail words without "faint hint".
- No titles in prompts. One action per panel. Max 2 balloons.
