# Khaam integration — drei

**Upstream:** https://github.com/pmndrs/drei  
**Snapshot commit:** `bf6f4addf47467d3885de272d94ca5127f6ef68f`  
**License:** MIT License  
**Vendored for:** private/personal use inside this Khaam Motion project (at owner's request).

## What it is
`@react-three/drei` is a collection of useful helpers and abstractions for `react-three-fiber` (R3F). It speeds up building 3D scenes with ready-made controls, staging, loaders, text, shapes, cameras, environments, and utility components.

## Key capabilities
- **Controls/cameras:** OrbitControls, CameraControls, PerspectiveCamera helpers, etc.
- **Staging/environment:** Environment, Stage, Lightformer, Sky, Stars, ContactShadows, etc.
- **Loaders/abstractions:** useGLTF/useTexture helpers, Html, Billboard, Text/Text3D, Image, etc.
- **Shapes/helpers:** ready geometries, grids, gizmos, bounds, center, etc.
- **Performance/utilities:** instances, LOD, preload, adaptive DPR-related helpers (use carefully in deterministic renders).

## What this snapshot includes / omits
- **Included:** `src/`, `test/`, `sandboxes/`, `.github/`, `README.md`, `LICENSE`, `package.json`, config files (`tsconfig.json`, `rollup.config.js`, `vite.config.ts`, `eslint.config.mjs`, `release.config.js`, `yarn.lock`, prettier/gitignore where present).
- **Omitted for size:** `.storybook/` (~24M), `docs/` (~3.2M), `.git`.

## How to use in Khaam
- Use in R3F/React/Remotion+Three projects as a helper layer over `three.js`/R3F; install dependencies in the target project (not globally in this skill).
- Prefer deterministic camera/light/animation paths for video export; avoid runtime-only/adaptive behaviors that change across frames/machines.
- For Arabic 3D text, prefer Khaam-controlled text/overlay workflows or carefully tested Text3D/font pipelines; verify shaping/RTL.
- Check peer dependencies (React, R3F, Three) against the target project.

## Notes
- Preserve upstream LICENSE and provenance.
- This is a source snapshot for reference/adaptation; it is not an installed dependency of Khaam.
- Apply Khaam rules for Arabic typography, sound discipline, pace, and QA.
