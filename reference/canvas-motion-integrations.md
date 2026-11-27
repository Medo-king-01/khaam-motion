<!-- Khaam Motion · reference file, loaded on demand from SKILL.md -->
# Canvas / motion / animation integrations (private-use snapshots)

Integrated repos for private use (canvas/motion/3D/particles/animation). Use them as capability references or starter sources; keep Khaam's Arabic/sound/pace/QA rules when adapting outputs.

| Repo | Location | License | Snapshot commit | What to use it for |
|---|---|---|---|---|
| [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | `integrations/motion-canvas/` | MIT | `7b91435c301d530351dcf5ebb91dd139c002e405` | Generator-based 2D programmatic video/animation engine, docs, examples, 2D/core/ui packages. |
| [nexu-io/html-video](https://github.com/nexu-io/html-video) | `integrations/html-video/` | Apache-2.0 | `ae9a8cd3a7ec07daaf36d91e5f8ae020f971b631` | HTML/CSS/data → MP4 workflow, templates, docs, agent/render pipeline patterns. |
| [BintzGavin/helios](https://github.com/BintzGavin/helios) | `integrations/helios/` | Apache-2.0 | `e03e89703f03e551e9fe9f38f2fc1731f8a0bf86` | Web-native programmatic video engine (player/studio/renderer/CLI/plugins/examples). Upstream tests, GitHub workflows, maintainer plans and changelogs are omitted; eight architecture context summaries remain. |
| [raphamorim/awesome-canvas](https://github.com/raphamorim/awesome-canvas) | `integrations/awesome-canvas/` | MIT | `28390e0f2f200bfef5d810d0b34df6fe175a261e` | Curated discovery list for Canvas libraries/examples/articles. |
| [mojs/mojs](https://github.com/mojs/mojs) | `integrations/mojs/` | MIT | `0a9cf9a87dd5637e6fa770755e79048489bcf817` | Web motion toolbelt source/reference (shape/burst/timeline/path/tween patterns). |
| [greensock/GSAP](https://github.com/greensock/GSAP) | `integrations/gsap/` | GSAP Standard License (no-charge, not MIT) | `5e6c35ff8eedea12d4f229129def635277d8b0f2` | High-performance web animation engine (tweens, timelines, easing, plugins). |
| [VincentGarreau/particles.js](https://github.com/VincentGarreau/particles.js) | `integrations/particles.js/` | MIT | `d01286d6dcd61f497d07cc62bd48e692f6508ad5` | Lightweight canvas particle effects library. |
| [mrdoob/three.js](https://github.com/mrdoob/three.js) | `integrations/three.js/` | MIT | `6d91309bfcf9c2779f32dd98b61fcc5415a74912` | 3D library (src+docs+tsl+manual+examples; heavy example assets models/textures/screenshots/sounds/files omitted; editor/build/test omitted). |
| [pmndrs/drei](https://github.com/pmndrs/drei) | `integrations/drei/` | MIT | `bf6f4addf47467d3885de272d94ca5127f6ef68f` | Useful helpers/abstractions for React Three Fiber (selective: src/sandboxes/config; upstream tests omitted, as are .storybook/docs). |
| [tsparticles/tsparticles](https://github.com/tsparticles/tsparticles) | `integrations/tsparticles/` | MIT | `814efd3b661df2e0594168430926331ff753a0e6` | Particles/confetti/fireworks ecosystem (engine/bundles/utils + interactions/plugins/shapes/updaters/effects/paths/presets/cli/palettes; demo/wrappers/websites/templates omitted). |

## Per-repo notes

### motion-canvas
- Strong fit for deterministic, code-driven 2D scenes using generator/timeline patterns.
- Use as reference or separate project base; Khaam default engines remain HyperFrames/Remotion depending on task.
- Check package versions/deps before running; adapt Arabic text with Khaam typography rules.

### html-video
- Useful for template-driven HTML-to-video generation and agent workflows.
- Inspect templates/docs in `integrations/html-video/templates/` and `docs/` before reuse.
- Verify renderer dependencies, fonts, and Arabic shaping/RTL in output.

### helios
- Broad web-native video stack; useful for renderer/player/studio/plugin patterns.
- Upstream test suites, GitHub workflows, and private maintainer plans/performance records are omitted from this reference snapshot; eight `.sys/llmdocs/context-*.md` summaries remain.
- Validate deterministic frame capture and Arabic text/layout before production use.

### awesome-canvas
- Not a runtime engine; a curated index. Use to find techniques/libs, then evaluate licence/maintenance of linked projects.

### mojs
- Good for web motion pattern reference; not a drop-in Khaam video renderer.
- If used in rendered video pipelines, make motion frame-deterministic (no wall-clock dependence).

## Cautions

- Preserve upstream LICENSE files and attribution in manifests/notes when adapting.
- All five are permissive (MIT/Apache-2.0), but linked third-party resources (especially from awesome-canvas) have their own licences.
- For Arabic output: apply `reference/arabic-typography.md` (RTL, whole words, no broken shaping).


### GSAP
- Powerful web animation/timeline/easing reference. License is **GSAP Standard License** (no-charge for most uses) — not MIT/Apache; check terms before redistribution/commercial productized use.
- For video capture, make animations frame-deterministic; avoid wall-clock dependence.

### particles.js
- Simple, lightweight particle backgrounds/effects. Good for small web visual flourishes.
- For deterministic rendering, drive particle state by frame/time seed.

### three.js
- Core 3D capability. Snapshot includes `src/`, `docs/`, `tsl/`, `manual/`, and `examples/` (code/demos/shaders/luts/materialx/jsm/fonts); **omitted** heavy example asset dirs `models/` (~269M), `textures/` (~110M), `screenshots/` (~21M), `sounds/` (~15M), `files/`, plus `editor/`, `build/`, `test/`.
- For Khaam 3D work: project-local deps, deterministic frame loop, careful Arabic text handling (texture/overlay preferred).

### drei (@react-three/drei)
- Helper layer over React Three Fiber/Three.js: controls, staging, loaders, abstractions, Text/Html, shapes/utilities.
- Snapshot includes `src/`, `test/`, `sandboxes/`, key configs; **omitted** `.storybook/` (≈24M) and `docs/` (≈3.2M).
- Use in target R3F/Remotion+Three projects with compatible peer deps; prefer deterministic settings for video capture.

### tsParticles
- Richer particle ecosystem than particles.js. Snapshot includes `engine/`, `bundles/`, `utils/`, `interactions/`, `plugins/`, `shapes/`, `updaters/`, `effects/`, `paths/`, `presets/`, `cli/`, `palettes/`; **omitted** `demo/` (≈324M), wrappers/websites/templates/markdown/scripts.
- Use frame-seeded/deterministic motion for video export.
