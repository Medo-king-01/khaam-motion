# Khaam integration — Tegaki handwriting starter

**Upstream package:** [`tegaki`](https://github.com/gkurt/tegaki), reviewed version 1.1.0. This starter is original Khaam integration code; no Tegaki source has been copied into this directory.

## What it is

A small Remotion composition that drives Tegaki's handwriting animation from `useCurrentFrame()`, using Tegaki's bundled Amiri font and a short Arabic sample. Replace the sample only with the user's approved text and visual direction.

## License and versions

- Tegaki renderer code: MIT; package pinned to 1.1.0 in this starter.
- Tegaki's Amiri font: SIL OFL 1.1. Preserve the upstream `FONTS-LICENSE.md` when redistributing the font or generated package assets; check font notices for other font choices.
- Remotion: independently governed by the Remotion License. Confirm eligibility before use; the Tegaki MIT license does not grant Remotion rights.
- Node >=20, React 19.3.1, Remotion 4.0.529. Dependencies install only in the video project, after user approval.

## Khaam adaptation

- `src/ArabicHandwriting.tsx` is a technique demo, not an approved design. Follow the user's style, Arabic rules and pace standard.
- Progress is a pure function of the Remotion frame. Do not replace it with timers, CSS autoplay or wall-clock values.
- Arabic phrase is kept whole and direction is explicit. Test the real text, font, rendered frames, final MP4 and repeated frame seeks before calling the effect available for production.
- Do not use this template to animate scripture or other verified quotations word-by-word. Use the existing still verified-card rules.

## Use

Copy with `python "<skill>/scripts/use_remotion_template.py" tegaki "<project>/remotion"`. Explain package download and ask permission before `npm install`. Then use `npm run dev`, `npm run typecheck`, `npm run still:start`, `npm run still:middle`, and `npm run render` from the copied folder. Inspect the stills and the actual video; see `reference/tegaki.md`.
