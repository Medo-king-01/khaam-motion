# Khaam integration — HyperFrames upstream assets (Batch 1 + 2 + 3)

**Upstream:** https://github.com/heygen-com/hyperframes  
**Snapshot commit:** `add940201ebe5903c540232210e8f79264ef3a86`  
**License:** Apache License 2.0 (see `UPSTREAM_LICENSE`)  
**Vendored for:** private/personal use inside this Khaam Motion project (at owner's request).

## What this batch includes

This vendors upstream HyperFrames assets in batches for Khaam private-use integration:

**Batch 1:**

- `registry/components/` — 239 reusable components + `CATALOG.md` (hero primitive shelf).
- `registry/examples/` — 9 full example projects.
- `registry/registry.json` — upstream registry index (includes blocks/examples/components entries; blocks not all vendored in this batch).
- `shader-transitions/` — `@hyperframes/shader-transitions` package source snapshot (no `dist/`, no `node_modules`).

**Batch 2:**
- `registry/blocks/` — curated selection of 53 high-value blocks (~5.2M): data charts, flowcharts, lower-thirds, titles, transitions, app/product UI, code/social cards, maps, callouts/stats, handwrite/text effects.

**Batch 3:**
- `registry/blocks/` — completed to full upstream set: 210 blocks total, 769 files, ~89.8M (added remaining 157 blocks).

## What is not included yet (future batches / optional)

- `registry/blocks/` is now fully vendored (210/210 upstream blocks).
- `docs/` (126M), `packages/` other than shader-transitions (93M overall), `skills/` (4.4M), `releases/`, studio/cloud internals — not vendored; use upstream as reference where needed.
- CLI pin bumped to `hyperframes@0.9.88` in `templates/hyperframes/package.json`, `SKILL.md`, `reference/hyperframes.md`, and `scripts/preflight.py` at user request. Smoke test in this sandbox confirmed version resolve + lint/check CLI wiring on the template; browser/render/snapshot were environment-blocked (no Chrome/FFmpeg, Chrome download blocked by sandbox allowlist), so full browser render smoke should be run in a Chrome+FFmpeg environment before relying on 0.9.x for production renders.

## How to use in Khaam

- Use as a **source/reference registry** for HyperFrames compositions. Check `registry/components/CATALOG.md` and component READMEs before building bespoke.
- Mount components as HyperFrames sub-compositions via `data-composition-src`, `data-start`, `data-duration`, `data-track-index`, `data-variable-values` as documented upstream.
- **Arabic/RTL adaptation required:** upstream components are often LTR-first. Apply Khaam rules: `dir="rtl"` on word containers (never on `<html>`), whole-word animation only, Arabic fonts from `assets/fonts/`, no `uppercase`, check IBM Plex «تى» issue, safe area, frame-0 thumbnail readability.
- **Shader transitions:** `shader-transitions/` can complement `gl-transitions/`; install/use in target project with required deps.
- Preserve Apache-2.0 license/NOTICE/provenance when adapting.

## Notes

- Upstream HyperFrames is evolving quickly; this snapshot is for private-use reference/adaptation, not a drop-in replacement for our tested Khaam HyperFrames starter.
- Apply Khaam rules for Arabic typography, sound discipline, pace, and QA.
