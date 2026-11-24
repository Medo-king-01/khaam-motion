# HyperFrames Registry & Upstream Assets (Khaam, Batch 1+2+3)

How to use the vendored HyperFrames upstream registry/assets inside Khaam Motion. This is a **source/reference snapshot** (Apache-2.0) for private use; Khaam's Arabic rules and workflow take precedence.

## What's vendored (Batch 1+2+3)

Location: `integrations/hyperframes/` (upstream commit `add940201ebe5903c540232210e8f79264ef3a86`, Apache-2.0).

- `registry/components/` — 239 reusable components. Start with `registry/components/CATALOG.md` (hero primitive shelf).
- `registry/examples/` — 9 full example projects.
- `registry/registry.json` — upstream registry index (includes blocks/components/examples).
- `shader-transitions/` — `@hyperframes/shader-transitions` source snapshot.
- `registry/blocks/` — full upstream block set (Batch 3 complete): 210 blocks, 769 files, ~89.8M.

**Not vendored:** upstream docs/packages/studio/cloud are reference-only, not vendored. All upstream registry components/examples/blocks are now present locally.

## Discovery workflow

1. **Before building bespoke**, check `integrations/hyperframes/registry/components/CATALOG.md` for a matching primitive.
2. Inspect the component's `README.md`, `registry-item.json`, and demo/composition HTML.
3. If a full example is closer, inspect `integrations/hyperframes/registry/examples/<name>/`.
4. For blocks, check `registry/registry.json` for names; if needed, fetch from upstream in a future curated batch (do not vendor all 92M blindly).

## Mount contract (upstream pattern)

Components are typically mounted as HyperFrames sub-compositions:

```html
<div
  class="clip"
  data-composition-id="<component-name>"
  data-composition-src="./<component>.html"
  data-variable-values='{"text":"..."}'
  data-start="0"
  data-duration="3.5"
  data-track-index="0"
></div>
```

- Check each component README for exact variables, defaults, slots, cues, exit behavior.
- Keep `data-duration`/track layout compatible with Khaam HyperFrames rules.

## Khaam Arabic/RTL adaptation (required)

Upstream components are often LTR-first. Before use in Khaam:

- **Direction:** `dir="rtl"` on containers holding separate Arabic words/spans; never on `<html>`.
- **Motion origin:** prefer `transform-origin: 100% 50%` for RTL reveals where appropriate.
- **No letter splitting:** animate whole words/lines. Never `split("")` for Arabic.
- **Fonts:** replace upstream fonts with Khaam Arabic fonts via `@font-face` from `assets/fonts/`; keep `Display`/`Second` conventions where applicable.
- **No `uppercase`** on Arabic.
- **IBM Plex Sans Arabic:** avoid headlines with «تى» or use tatweel; verify at full size.
- **Harakat/vowelled text:** use Scheherazade New or Noto Naskh Arabic for vowelled quoted text; never Amiri/Amiri Quran in HyperFrames for harakat.
- **Safe area/frame 0:** keep text in safe vertical area; frame 0 readable for thumbnail.
- **Sound/pace:** component animation must serve Khaam pace rules (`reference/pace.md`) and sound rules (`reference/film-sound.md`).

## Shader transitions

`integrations/hyperframes/shader-transitions/` is a small source snapshot of `@hyperframes/shader-transitions` (Apache-2.0). It can complement `integrations/gl-transitions/` (GLSL catalog). Use in target projects with required deps; keep deterministic frame/time-driven progress for video export.

## When to build bespoke

Build bespoke Khaam composition when:
- no registry component fits the mechanic/story;
- Arabic layout/RTL behavior is too entangled to adapt safely;
- the scene needs Khaam-specific kits (`templates/hyperframes/kit/`, word-lit/verified-card/ladder/scene-kit/figure-kit) behavior.

## Provenance

- Upstream: https://github.com/heygen-com/hyperframes
- Commit: `add940201ebe5903c540232210e8f79264ef3a86`
- License: Apache-2.0 (`integrations/hyperframes/UPSTREAM_LICENSE`)
