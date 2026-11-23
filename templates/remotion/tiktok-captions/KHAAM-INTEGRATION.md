# Khaam integration — TikTok captions template

**Upstream:** remotion-dev/template-tiktok @ f51c6c8c99048b08fdc48fe7a9e3a7ef46bf1cbd

## What it is
TikTok/Reels-style word-by-word captions in Remotion. Includes caption page layout and a `sub.mjs` helper for Whisper.cpp caption generation.

## Use in Khaam
- Good for short-form captioned vertical videos.
- **Arabic narration:** do not rely on the English-only Whisper example. Use Khaam narration timings (`reference/voiceover.md`, `scripts/align_voice.py`) or a verified multilingual transcription path, then map timings into the caption components.
- Replace demo font with Arabic-safe font (see `reference/arabic-fonts.md`). `public/theboldfont-license.rtf` is included; read it before using the bundled font.
- The upstream sample video was not vendored (large binary). Put your footage in the video project's `public/`.

## Key files
- `src/CaptionedVideo/` — caption rendering components.
- `src/Root.tsx` — composition registration.
- `sub.mjs`, `whisper-config.mjs` — caption generation helpers (review before running).
- `public/theboldfont.ttf`, `public/theboldfont-license.rtf` — demo font + license.
