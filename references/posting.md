# Captions, pinned comments, posting

**Never post unless the owner explicitly asks.** Preparing files, captions and song picks is always fine.

## Caption format

One sweet/funny line written as the couple or a fan would say it (lowercase is fine) + one emoji, blank line,
5 hashtags: couple tag, series tag, 1–2 genre tags, account tag.

```
we bought a camera. now we have 400 photos of the same face 📸💙

#RemxSubaru #ReZero #AnimeEdit #ChibiArt #KawaiiChaosComics
```
Store it in the piece's `synopsis.md` (`**Caption:**` block) → `python3 scripts/update_trackers.py` syncs `captions.json`.

## Pinned comment

A short engagement hook that invites replies, in the account's voice, e.g.
"which photo would you pin on your wall? 1–5 👇" / "rem's flail or fern's zoltraak — who wins? 😭" / "tag the person who
steals your fries 🍟". One line, one emoji, a question.

## Posting flow (when asked)

- **Strip image posts** can go out from the Instagram website via Claude in Chrome. Share to Facebook OFF.
- **Reels need a song from Instagram's library, which only exists in the phone app**, and Instagram web has no drafts.
  So: AirDrop/send `upload/…_strip_reel.mp4` (or the music video) to the owner → in the app: + → Reel → pick video →
  Audio → search the song → choose the 10–15 s section → original audio volume 0 → caption → Share to Facebook OFF → Share.
- Keep the account Personal/Creator (business accounts get a tiny music library).
- After posting: mark it in `posting_log.json` (`posted`, `song`) + README via `update_trackers.py`.

## What to post today?

Rotate couples (not the same couple twice in a row), alternate strips / strip reels / music videos, prefer pieces
that passed QA most recently and haven't been posted (`posting_log.json`). Suggest 1–2 with caption + song ready.

## Milestones

Followers milestone posts (e.g. 1K): a single celebratory chibi image in the same style with the couple(s) holding the
number, a thank-you caption, no lettering errors.
