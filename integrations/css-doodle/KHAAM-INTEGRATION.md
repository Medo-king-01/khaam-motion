# Khaam integration — css-doodle

**Upstream:** https://github.com/css-doodle/css-doodle  
**Snapshot commit:** `111e783dc0f054ffb1acd3154c9c5190f8f7eb6b`  
**License:** MIT License  
**Vendored for:** private/personal use inside this Khaam Motion project (at owner's request).

## What it is
css-doodle is a web component for visual art and creative coding. It generates CSS-driven grid/pattern/graphic effects with a compact DSL, useful for generative backgrounds, textures, decorative motion, and abstract visual systems.

## Key capabilities
- `<css-doodle>` web component for generative CSS/grid visuals.
- DSL/functions for randomness, grids, shapes, patterns, transforms, animations.
- Can be used in HTML/CSS/web-based motion pipelines (including Remotion/HTML capture workflows) for generative backgrounds and decorative elements.
- Source in `src/`, docs in `docs/`, build output in `build/`.

## How to use in Khaam
- Use for generative backgrounds, abstract textures, pattern fields, animated decorative layers behind Khaam typography/scenes.
- In web/Remotion pipelines, include the component/build and drive seed/props for deterministic renders where possible.
- Keep it subordinate to the message: Arabic text, pacing, and clarity remain primary; doodle patterns should support, not compete.
- For video export, prefer deterministic seeds/parameters and test render performance.

## Notes
- Preserve upstream LICENSE and provenance.
- Snapshot includes full repo content except `.git`/`node_modules` (small repo).
- Apply Khaam rules for Arabic typography, sound discipline, pace, and QA.
