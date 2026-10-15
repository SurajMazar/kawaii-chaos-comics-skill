# Style, locks and prompt templates

Paste these blocks into every ChatGPT image prompt (each message must be self-contained — ChatGPT forgets/drifts).
Attach `style_ref_master.jpg` (image 1) and the piece's character sheet (image 2) to every message.

## Contents
1. The look
2. Strip prompt header
3. Lock lines (add all to every prompt)
4. Character-sheet prompt template
5. Music-video frame template (home frames, polaroid/photo frames)
6. Canon cheat sheet (Rem / Subaru / others)

---

## 1. The look (locked by the owner, 2026-10-09: "always use this art style")

Super-chibi characters (~2 heads tall, giant round heads, stubby bodies, nub mitten hands, simple bean/line eyes) in a
casual hand-drawn doodle webcomic style: rough sketchy pencil/marker outlines with uneven thickness, flat muted crayon
colour that slightly misses the lines, no lighting/gradients, minimal cream backgrounds with 1–2 doodled props,
real-handwriting lettering in simple balloons, doodle emotion marks (sweat drops, shiver squiggles, blush scribbles,
little hearts). Rejected looks: regular/adult proportions, polished glossy anime, painterly skies, glow, bokeh,
detailed rooms/streets/crowds — the owner calls these "AI generated".

Why it matters: the account's identity is the hand-drawn doodle feel. A single polished frame in a reel breaks it.

## 2. Strip prompt header

```
Draw a fan-art comic strip of [CHARACTER A] and [CHARACTER B] from [SERIES]. Portrait 4:5 (1122x1402). One image only.
ATTACHED: image 1 = our comic strips (copy this art style EXACTLY); image 2 = the CHARACTER SHEET (copy faces, hair,
outfits, heights EXACTLY). Ignore the style of any other image in this chat.
LAYOUT: follow the attached wireframe exactly — the numbers are the reading order; draw the panel borders and gutters
like the wireframe (do NOT draw the numbers). Thin cream gutters, dark sketchy borders.
SUPER-CHIBI IN EVERY PANEL: both characters are tiny super-deformed chibis, about 2 heads tall — giant round heads,
tiny stubby bodies, little nub hands, simple dot/line/bean-shaped eyes, expressive cartoon mouths. Keep them on-model:
[canon hair / eyes / outfit / accessories]. No realistic proportions anywhere.
IT MUST NOT LOOK AI-GENERATED — a casual hand-drawn doodle webcomic drawn on an iPad: rough sketchy pencil/marker
outlines with uneven thickness and small overshoots, flat crayon/marker colours that slightly miss the lines, NO shading
or one flat shadow, NO lighting effects, NO gradients, NO glossy shine, NO sparkles/bokeh, NO detailed rendering.
Minimal backgrounds: plain cream/pastel with only a few doodled props, lots of empty space.
Hand-written lettering that looks like real handwriting, simple hand-drawn balloons with tails at the speaker, small cream
caption box for the premise. Spell every line EXACTLY as written; nothing else written anywhere.
Doodle emotion marks: sweat drops, shiver squiggles, blush scribbles, little hearts, "!" marks.
```
Then `Panel 1: … / Panel 2: …` — ONE short line per balloon, punchline in the last (biggest) panel, setup line placed
so it is read before the reply (top-left first). No brand logos (ChatGPT likes to add coffee-chain logos).

## 3. Lock lines — add ALL of these to every prompt

- **COUPLE RULE:** "[A] and [B] are THE couple; every other character is a cameo and is never drawn as either one's love interest."
- **OUTFIT LOCK:** "Outfits exactly as on the character sheet, identical in every panel — never change clothes unless this script says so." Rem/Ram maid outfits have NO orange anywhere; orange appears only on Subaru's tracksuit trim.
- **ANATOMY & CLOTHES CHECK:** "every character has exactly two arms and two legs, each attached naturally to the right body; simple chibi mitten hands with no extra, missing, merged or twisted fingers or limbs; no stretched, melted or warped faces or bodies; when characters hug or hold hands it is clear whose arm is whose; clothes drawn cleanly and consistently (each sleeve belongs to the right arm, outfits never fuse between characters, no random stray colour patches). If a pose would need an awkward limb, choose a simpler pose."
- **REM'S EYES:** "Rem's visible eye (the one not under her fringe) is OPEN in most panels — a big gentle BLUE eye with a highlight; the closed '^ ^' smile in at most ONE panel." (ChatGPT defaults to closed eyes on Rem.)
- **HAND-DRAWN, NOT AI:** "no repeated copy-paste elements; at most 2 speech balloons per panel; varied natural poses; every panel shows ONE clear action a reader understands at a glance."
- **HEIGHT LOCK:** "the top of Rem's head reaches Subaru's eye level in every panel" (Ram = Rem's height; Shaula = Subaru's height). Generally: state the relative heights from the character sheet.
- **BACKGROUND + CAMERA:** "plain cream background with at most one or two simple doodled props per panel; NO detailed rooms, architecture, crowds, street lamps, glowing lights or scenery. Vary the shots (close-up, medium, wide); characters are NOT lined up in a row facing the viewer."
- **COUNT CHECK** for any countable object in the scene, e.g. "each jack-o'-lantern has EXACTLY two eyes, one nose, one mouth — no extra cut-outs"; "ONE camera"; "EXACTLY five polaroids on the board".
- **REAL-WORLD LINE** for the key action of each frame — spell out the physics: which hand holds what, where the lens points, umbrella above heads with the rain landing on the uncovered side, masks over faces (not worn like hats unless pushed up on purpose), cones upright, drips fall down.
- **STORY LOGIC / CONTINUITY** for sequences: "nothing exists before the story makes it (no printed photo before the first photo is taken)"; "same place/day, time moving forward"; "same perspective, same recurring landmark, same props".

## 4. Character-sheet prompt template (make this FIRST for every piece)

```
NEW IMAGE: a CHARACTER SHEET (not a comic), landscape 3:2, plain cream background.
ATTACHED: image 1 = our comic strips (copy ONLY this super-chibi doodle art style; it also shows Rem and Subaru);
images 2..n = official art of [side characters] (copy each DESIGN exactly, redraw in our style).
STYLE LOCK: [the look, section 1, condensed]
[For each character: hair, eye colour, face, outfit item by item, accessories, "NO orange on Rem"]
LAYOUT: everyone standing side by side on one floor line, each shown front + back view, with a faint dashed height
guide ([relative heights]); key props drawn once on their own; small handwritten name labels, nothing else written.
ANATOMY & CLOTHES CHECK: [line]
```
QA it like any image (canon accuracy vs the official refs, outfit details, heights, style, no orange on Rem). Fix
small issues with an EDIT message in the same chat without re-attaching refs ("keep everything else exactly the same,
fix only: 1… 2…"). Save as `<piece>/charsheet.png`.

Designing "a little different" outfits (e.g. a date video): keep face, hair and the signature accessory (Rem's X clip +
pink ribbon), keep the character's colour identity (Rem: blues/white/navy; Subaru: black + a small orange accent),
change the garments (cardigan + blouse + pleated skirt; zip hoodie + tee + jeans). Spell every garment out.

## 5. Music-video frame template

Header (identical for every frame of the piece):
```
I'm making separate frames (one image per message) for a cute Instagram music video of [A] and [B] from [SERIES].
Generate ONLY the frame I ask for, one image, portrait 4:5.
ATTACHED: image 1 = our comic strips (copy this art style EXACTLY); image 2 = the CHARACTER SHEET for this video.
STYLE LOCK … / CHARACTERS ON-MODEL (2-head chibis exactly like image 2, never older/teen faces) / HEIGHT LOCK /
REM'S EYE / OUTFITS (from image 2, identical in every frame) / PROPS / ANATOMY & CLOTHES CHECK
```
Setting block — pick one per frame type:
- **Home frames:** "a plain cream background with only a simple wooden table and two chairs seen from the front at eye level — nothing else", and the ending frame returns to the SAME table, same angle.
- **Photo/polaroid frames:** "the picture IS one instant photo FILLING the whole canvas: thick plain white border, wider at the bottom, bottom border empty, straight, identical framing in every polaroid frame. INSIDE THE PHOTO: flat plain pastel background with only 1–2 simple doodled props; NO detailed boardwalk, lamps, crowds, glowing lights, reflections, bokeh or painted skies. One place, one day, time moving forward; the SAME small doodled landmark in every photo; same selfie perspective (waist-up, eye level). The camera is TAKING the photo, so it is never visible in it — the photographer's arm reaches toward the viewer and is cut off at the edge. Nobody holds a printed photo."
Then `FRAME N: …` — one clear action, the physical details spelled out.

Frame-type lessons from rejected frames:
- Photo-montage frames drift toward detailed, glowing, realistic scenes and older-looking characters → the
  "INSIDE THE PHOTO stays simple" line and the charsheet attachment fix it.
- A picture of a polaroid "already printed" before the story's first photo = logic fail.
- Halloween: carve pumpkins on the table in the pre-chorus, wear the jack-o'-lantern masks only in the chorus, worn the
  SAME way in every chorus frame (over the face), standard jack-o'-lantern face.

## 6. Canon cheat sheet

- **Rem (Re:Zero):** short blue bob, fringe over her right eye, ONE visible big blue eye, white X hair clip + pink
  ribbon, white frilly maid headdress, black maid dress, white frilly apron + ruffled hem, wide black sleeves with
  white frilled cuffs, black collar bow. NO orange. Shorter than Subaru (head top = his eye level). Morning-star flail.
- **Subaru (Re:Zero):** spiky messy black hair, small sharp sanpaku eyes, black tracksuit jacket with white panels and
  orange trim (no logos), black track pants with white side stripes.
- **Watchtower arc / other outfits, Ram, Beatrice, Emilia, Shaula, Echidna (school uniform), Mai × Sakuta (Bunny Girl
  Senpai), Fern × Stark (Frieren), Rimuru + Shinsha (Tensura)…** — see the repo's `couples.md` and `references/owner/`
  official art; build a character sheet from official art before the first strip of any new character.
