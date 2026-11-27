# Tegaki: optional handwriting reveal for Arabic motion

[Tegaki](https://github.com/gkurt/tegaki) renders a font as a self-drawing handwriting animation. The upstream project documents Arabic/RTL shaping through HarfBuzz, includes an Amiri font bundle, and has a Remotion example driven by the current frame. Its code package is MIT; bundled font data has separate terms (Amiri is SIL OFL 1.1). Review the upstream [README](https://github.com/gkurt/tegaki/blob/main/README.md) and [font notices](https://github.com/gkurt/tegaki/blob/main/packages/renderer/FONTS-LICENSE.md) before changing versions or distributing font assets. Remotion's own license still applies independently (`reference/remotion.md`).

Tegaki is an **optional, project-local capability**, not a setup dependency and not the default for Arabic text. Use it only when a hand-drawn stroke is part of the approved visual direction: a short title, a signature-like word or an intentional reveal. Ordinary kinetic Arabic text stays whole-word/whole-line and follows `reference/arabic-typography.md`; never split Arabic into isolated characters to imitate handwriting.

When the requested effect resembles an upstream demo, inspect the relevant original scene in `reference/tegaki-upstream/examples/remotion/src/` (for example `Root.tsx`, `Promo.tsx`, or `launch/Write.tsx`) and adapt that known implementation rather than inventing a substitute. Read only the relevant source and font notice. The upstream example is English-first, so replace demo copy/layout with the user's Arabic and run the acceptance tests below.

## Engine choice and installation

- Prefer a Remotion project when the user wants a frame-controlled handwriting reveal. Use the maintained npm package, not copied upstream source. Pin `tegaki` to the version tested for that project (the reviewed upstream version is 1.1.0); install it only inside the video project's Remotion folder and only after explaining the download and getting permission: `npm install --save-exact tegaki@1.1.0`.
- Remotion is not the default for this effect: use it only if already selected or if the benefit justifies its project setup and applicable license. Otherwise offer a simpler, tested native animation.
- Tegaki's CLI emits SVG; it is suitable for a static or otherwise verified asset, but do not assume animated SVG time will seek deterministically in HyperFrames. Do not use CSS/SMIL autoplay as a substitute for frame-controlled video without a seek test.
- Never add Tegaki to the skill's global environment, shared toolkit, or required onboarding. Keep `node_modules` project-local and record package/font versions and licenses in the project notes.

## Frame-controlled Remotion starter

The ready Khaam starter is `templates/remotion/tegaki/`. Copy it with `python "<skill>/scripts/use_remotion_template.py" tegaki "<project>/remotion"`, get permission before installing packages, then use its built-in studio, still and render commands. Its sample is intentionally a short Arabic phrase in Amiri; replace it with the approved copy and visual style. The original upstream Remotion examples are mirrored unchanged for offline study at `reference/tegaki-upstream/examples/remotion/`, with the MIT and font notices beside them. That upstream sample is English-first and its `workspace:*` manifest is not standalone; do not mistake it for an Arabic-ready video template.

The core pattern follows the current Remotion frame, not a wall clock:

```tsx
const frame = useCurrentFrame();
const { durationInFrames } = useVideoConfig();
const progress = Math.min(frame / Math.max(1, durationInFrames - 1), 1);

<TegakiRenderer
  font={amiri}
  text="مرحبا بالعالم"
  direction="rtl"
  time={{ mode: 'controlled', value: progress, unit: 'progress' }}
  style={{ fontSize: 140, color: '#202020', textAlign: 'right' }}
/>
```

This makes animation progress a pure function of the frame. Keep the phrase as Arabic text, not a sequence of letters. Verify actual shaping and stroke order in the rendered output; a package's Arabic support statement is not proof that every font, ligature, mark or mixed-direction phrase works for this job.

## Acceptance test before using it in a delivered video

1. Render a still at frame 0, a middle frame, and the last frame; check RTL order, connected joins, dots, punctuation, clipping, baseline and the finished word.
2. Render a short MP4; inspect it at full size. Test a backward/random frame seek or repeated still render to confirm the same frame is identical. If renderer effects are not applied consistently on seek, do not use the animation in that composition.
3. Try the exact approved Arabic string and selected Amiri font. Test diacritics, tatweel, punctuation or mixed Latin/digits only if the actual text contains them; correct failures with a different font/layout or fallback treatment rather than silently dropping marks.
4. Re-run the normal pace, Arabic and sound checks. Tegaki changes typography, not the approved narration, story, pace, sound or quality gates.
5. Do not describe a still image or an unplayed output as a successful animation test. If the environment cannot render it, report the limitation and leave Tegaki as unverified.
