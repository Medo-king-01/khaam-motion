# Khaam integration — lottie-web

**Upstream:** https://github.com/airbnb/lottie-web  
**Snapshot commit:** `bede03d25d232826e0c9dca1733d542d8a7754fb`  
**License:** MIT License  
**Vendored for:** private/personal use inside this Khaam Motion project (at owner's request).

## What it is
Lottie-web is Airbnb's JavaScript library for rendering Adobe After Effects animations exported as JSON (via Bodymovin/Lottie workflow) natively on web.

## Key capabilities
- Render AE/Lottie JSON animations in browser (SVG/Canvas/HTML renderers).
- Player builds for different targets: full, light, canvas, html, svg, worker variants (`build/player/`).
- Programmatic control: play/pause/stop, segments, speed, direction, goToAndStop/play, events, dynamic properties.
- Useful for embedding prebuilt motion assets, icon animations, UI micro-interactions, and AE-exported vector motion into web-based Khaam renders.

## What this snapshot includes / omits
- **Included:** `build/player/` (ready dist builds), `player/` (source), `docs/`, `tasks/`, `projects/`, `index.d.ts`, `rollup.config.js`, root metadata/license files.
- **Omitted for size/low Khaam value:** `demo/` (~5.5M), `test/` (~11M), `gifs/` (~4.2M), `build/extension/` (~19M, AE extension zxp), `build/old_parser/` (~216K).

## How to use in Khaam
- For web/Remotion/Motion Canvas/HTML compositions, use `build/player/lottie.min.js` or an appropriate variant (light/canvas/svg/html/worker) depending on performance/render needs.
- Treat Lottie JSON assets as external/approved assets; verify license/rights for any third-party animation files you embed.
- For deterministic video capture, control playback via frame/time (`goToAndStop`) rather than real-time playback when possible.
- Preserve Arabic/text rules: if text is part of animation, prefer rendering Arabic text in Khaam's controlled text pipeline; AE/Lottie text can be fragile for Arabic shaping.

## Notes
- Preserve upstream LICENSE.md and provenance.
- Lottie animations themselves (JSON files) may have separate licenses/rights; this snapshot covers the lottie-web library only.
- Apply Khaam rules for Arabic typography, sound discipline, pace, and QA.
