# Khaam integration — Code Hike template

**Upstream:** remotion-dev/template-code-hike @ 9e47d09cef59154ac55824593f3441b0c59e5328

## What it is
Animated code snippet transitions using Code Hike + Remotion. Snippets live in `public/`; transitions/annotations are in `src/`.

## Use in Khaam
- Good for tech explainers, dev tutorials, "before/after code" reels.
- Keep code blocks LTR/monospace. Any Arabic explanation around code should follow `reference/arabic-typography.md`.
- Install deps in the copied video project: `npm install`.
- Check Code Hike dependency licences before redistribution.

## Key files
- `src/Main.tsx`, `src/CodeTransition.tsx` — composition and transitions.
- `src/annotations/` — callout/error/inline token annotations.
- `src/calculate-metadata/` — snippet loading/theme/schema.
- `public/code*.tsx` — example snippets to replace.
