# Khaam integration — gl-transitions

**Upstream:** https://github.com/gl-transitions/gl-transitions  
**Snapshot commit:** `0d834855e43354127e176b2868014f42f04b737b`  
**License:** MIT (repo LICENSE). **Note:** upstream LICENSE states individual transitions in `transitions/` may have their own license specified in their files; check per-transition headers before redistribution/use outside private scope.  
**Vendored for:** private/personal use inside this Khaam Motion project (at owner's request).

## What it is
The open collection of GL Transitions: GLSL fragment-shader transitions that can be used to transition between two visual inputs (images/videos/frames) in WebGL-based pipelines.

## Key capabilities
- Large catalog of GLSL transition effects in `transitions/` (`.glsl` files).
- Useful for WebGL/Canvas/Remotion/custom render pipelines that can render fragment shaders.
- Common transition params (progress, from/to textures, ratio, custom uniforms) depending on transition.

## How to use in Khaam
- Use in WebGL-enabled pipelines (Three.js/R3F custom shader passes, Remotion WebGL/canvas workflows, or custom FFmpeg/gl pipelines where applicable) to create polished scene transitions.
- For deterministic video export, drive `progress` from frame/time, not wall-clock.
- Check per-transition license/header before using any specific transition in distributable output; keep provenance in delivery manifest.
- Keep transitions purposeful and readable; avoid flashy transitions that hurt Arabic readability or pacing.

## Notes
- Snapshot includes `transitions/`, `scripts/`, root metadata/LICENSE files from sparse checkout.
- Preserve upstream LICENSE and per-transition license notices.
- Apply Khaam rules for Arabic typography, sound discipline, pace, and QA.
