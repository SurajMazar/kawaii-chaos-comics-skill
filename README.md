# kawaii-chaos-comics-skill

A Claude skill for making super-chibi doodle anime-couple comic strips, silent strip reels and music-video reels for
Instagram (@kawaiichaos.comics). It covers the locked art style, character sheets, the strict QA + redraw gate,
ChatGPT image generation via Claude in Chrome, reel building, ElevenLabs music/voice, copyright rules, captions and posting.

## Install

- **Claude Code:** copy the folder into your skills directory
  `cp -r kawaii-chaos-comics ~/.claude/skills/`
- **claude.ai:** upload `kawaii-chaos-comics.skill` (Settings → Capabilities → Skills), or open it and click *Save skill*.

## Contents

```
kawaii-chaos-comics/
├── SKILL.md                         rules + strip / music-video workflows
├── references/
│   ├── style-and-prompts.md         style header, lock lines, character-sheet + frame templates
│   ├── qa-gate.md                   strict QA checklist (counts, logic, perspective, real-world plausibility)
│   ├── chatgpt-automation.md        ChatGPT queue "pump" via Claude in Chrome + pitfalls
│   ├── reels-and-music-videos.md    strip reels, music videos, cut timing
│   ├── audio-and-copyright.md       ElevenLabs songs/voices, lyrics & copyright rules
│   ├── posting.md                   captions, pinned comments, posting flow
│   └── style_ref_master.jpg         the locked art-style reference
└── scripts/
    ├── chatgpt_pump.js              in-page ChatGPT image queue
    ├── unbundle_strips.py           unpack downloaded image bundles
    └── strip_text.py                erase hand-lettering from frames
```
