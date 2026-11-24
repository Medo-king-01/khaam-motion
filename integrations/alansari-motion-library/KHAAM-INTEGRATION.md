# Khaam integration — Alansari.Tech Motion Library

**Upstream:** https://github.com/alansariteach/motion-library  
**Site:** https://alansariteach.github.io/motion-library/  
**Snapshot commit:** `a280b36f5ecacceac8b58cd6af72ea29d7e3db12` (fetched 2026-11-24)  
**License:** No upstream LICENSE file at snapshot time. Permission for private use of this snapshot **inside this skill** was relayed by the skill owner on 2026-11-24 (`UPSTREAM_PERMISSION.md`); its credit line: Ali Alansari (Alansari.Tech).  
**Vendored for:** private/internal use inside this Khaam Motion project only. Do not redistribute this directory outside the private skill.

## What it is
A Gulf-Arabic motion library for AI consumption: 1000 named motion directions (`M-001`–`M-1000`) across 14 categories (TXT, EMP, CAP, TRN, CAM, FX, SOC, LGO, PER, AUD, SCR, TRK, D3, TIM), 16 caption styles (CS), 30 opening hooks (H), 24 palettes (CP), 18 ready elements (EL), 12 Reel recipes (R), 123 fonts list (FA/FE), sound suggestions (SX), 10 colour LUTs (LT) and 10 backgrounds (BG). The upstream design is deliberately AI-native: a tiny `lib/INDEX.md` routes to one small category file — never read everything.

## What is in this snapshot (and what is not)
- `lib/INDEX.md`, `lib/ar/*.md` (24 files), `lib/en/*.md` (24 files) — the "AI payload" (~0.77 MB). Arabic-first; the English files are kept for terminology lookup.
- `sfx/SX-01..28.mp3` + `sfx/CREDITS.md` — 28 effects, all CC0 1.0 per the upstream credits (~0.7 MB). Consumed as *suggested accents*, never as the video's soundtrack (see the reference doc).
- `lut/LT-01..10.cube` + preview `.jpg` + `original.jpg` — 10 colour LUTs for `ffmpeg -vf lut3d` (~8.9 MB).
- `MANIFEST.sha256` — SHA-256 of every vendored file.

**Excluded on purpose:** `examples/` (1,000 MP4 previews), `fonts/` (individual font licences must be checked per file; reference them, do not copy), `index.html` / `studio.html` / `tools/` (site UI and personal pipeline), `video/` (install-video assets), PWA/analytics files, `PROJECT.md` (owner's personal handoff incl. plugin internals), `alansari-motion-library.md/.json` (redundant with `lib/`, and the author distributes the agent library file via his plugin only), `lut/` previews are kept as they are part of `lut/` and aid human pick.

## How this skill adapts it (read `reference/alansari-motion-library.md`)
- The upstream `RULES.md` is **subordinate** to this skill: Khaam Arabic/RTL rules, the diacritics rules, sound v2 (real recordings of what is shown; 3–5 per video; bed or none; no music unless asked; the mix check), determinism on HyperFrames/Remotion, the user's learned taste and brand, and the safe-zone/bio-link/hook gates all win.
- Motion names stay in their fixed English form; everything user-facing is spoken and drawn in Arabic.
- Suggested sounds (`الصوت المقترح`) are hints: prefer this skill's real CC0 recordings in `sounds/library/` (`scripts/motion_sound.py`), falling back to CC0 upstream SX only when listening confirms it fits and sound v2 allows.
- File names and IDs are upstream's; never rename, never re-letter.

## Integrity
`MANIFEST.sha256` lists every file. Re-pin by re-fetching at a new commit and updating this note, `UPSTREAM_PERMISSION.md` status, and the tests/preflight count together.

**Not verified:** no render of any of these motions has been executed; no `hyperframes add` has been run against the registry from this snapshot. Presence and integrity only, like every integration in this skill.
