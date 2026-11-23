# Khaam integration — three.js

**Upstream:** https://github.com/mrdoob/three.js  
**Snapshot commit:** `6d91309bfcf9c2779f32dd98b61fcc5415a74912`  
**License:** MIT License  
**Vendored for:** private/personal use inside this Khaam Motion project (at owner's request).

## What it is
Three.js is a JavaScript 3D library for WebGL/WebGPU-based rendering: scenes, cameras, lights, materials, geometries, loaders, math, and many addons/examples in upstream.

## Key capabilities
- 3D scene graph, camera, lighting, materials, geometry, textures.
- WebGL renderer (and upstream WebGPU paths in current versions).
- Math/utilities/loaders/animation system primitives.
- Foundation for product/3D motion scenes in web and Remotion+R3F workflows.

## What this snapshot includes / omits
- **Included:** `src/`, `docs/`, `tsl/`, `examples/jsm/`, `examples/fonts/`, root README/LICENSE/package files.
- **Omitted for size/low benefit:** `manual/` (≈107M), full `examples/` beyond `jsm/`+`fonts/` (many heavy demo assets), `editor/`, `build/`, `test/`.

## How to use in Khaam
- Use as reference for 3D capabilities and as dependency source guidance.
- For Khaam 3D video work, prefer project-local installs and deterministic rendering (frame-driven), then capture via Remotion/@remotion/three or appropriate pipeline.
- Apply Arabic text rules carefully in 3D (prefer tested texture/overlay text; avoid broken 3D glyph shaping).

## Notes
- Preserve MIT license. Record versions in delivery manifests.
