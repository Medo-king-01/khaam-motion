# Khaam integration — Overlay template

**Upstream:** remotion-dev/template-overlay @ 39197f6535fb4878ea128cf61b3e57d41916e900

## What it is
A minimal Remotion overlay: animated card entering with spring/rotate, exiting before end. Good for lower-thirds, callouts, name plates, CTA badges.

## Use in Khaam
- Copy this folder into a `.khaam/projects/<video>/remotion/` (or new Remotion project).
- `npm install` inside the copied project.
- Replace demo text/font/colors with project brand/taste.
- For Arabic text: use Arabic-safe font via `@remotion/fonts`/`@font-face`, keep text direction/layout RTL-aware, avoid splitting Arabic words into letters.
- For transparent overlay export, configure Remotion output for alpha (e.g. ProRes 4444 / PNG sequence / WebM with alpha depending on workflow) and verify in target editor.

## Key files
- `src/Overlay.tsx` — main overlay animation.
- `src/Root.tsx` — composition registration.
- `remotion.config.ts` — Remotion config.
