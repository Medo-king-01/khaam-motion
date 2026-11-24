# React UI, Charts & GL Transitions Integrations (private-use snapshots)

Vendored source snapshots for data viz, animated UI components, and WebGL transitions. All are **source/reference snapshots** (not installed Khaam runtime deps); use in target React/Remotion/WebGL projects with appropriate dependency installs.

## Snapshot index

| Repo | Integration dir | License | Upstream commit | Snapshot scope | Notes |
|---|---|---|---|---|---|
| [gl-transitions/gl-transitions](https://github.com/gl-transitions/gl-transitions) | `integrations/gl-transitions/` | MIT (repo). **Per-transition license headers may vary** | `0d834855e43354127e176b2868014f42f04b737b` | `transitions/`, `scripts/`, root meta/LICENSE files | GLSL transition effects catalog. |
| [recharts/recharts](https://github.com/recharts/recharts) | `integrations/recharts/` | MIT | `6a02fb6da47e419d4270947e6f6db41c734c5567` | `src/` + root meta/config/types files | React+D3 composable charts. |
| [magicuidesign/magicui](https://github.com/magicuidesign/magicui) | `integrations/magicui/` | MIT | `b0b2e4974b1b68cd5278277c6837a27736e20c3a` | `registry/`, `registry.json`, `lib/hooks/types`, root meta (docs site app/content/public omitted) | Animated React UI components/effects registry. |

## How to use in Khaam

### gl-transitions
- **Best for:** scene-to-scene transitions in WebGL/canvas pipelines.
- **Determinism:** drive transition `progress` by frame/time.
- **Caution:** check individual transition file license headers; keep transitions subtle and readable.

### recharts
- **Best for:** data explainers, KPI/infographic motion, chart-driven stories.
- **Determinism:** animate by frame/data state; avoid hover-only meaning.
- **Arabic:** verify RTL labels, Arabic numerals/font rendering, axis/legend layout.

### magicui
- **Best for:** polished UI effects, promo/product UI blocks, animated text/background components.
- **Usage model:** copy/adapt specific components into a target React/Remotion project; install required deps (React/Tailwind/motion/shadcn utils as needed).
- **Determinism:** prefer frame/time-driven animation for video; avoid scroll/hover-dependent behavior.

## Cautions

- All three are **source snapshots**, not installed runtime dependencies.
- gl-transitions: per-transition licenses may vary — check headers.
- recharts/magicui: React ecosystem dependencies; verify peer deps and bundle impact in target project.
- Apply Khaam rules for Arabic typography, sound discipline, pace, and QA.

## Provenance

Snapshots cloned/selected 2026-11-24 and copied into `integrations/`. See each `integrations/*/KHAAM-INTEGRATION.md`.
