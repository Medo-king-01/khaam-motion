# Direction, verified motion and focused QC

A Khaam adaptation of ideas reviewed in [ReelForge](https://github.com/gongnyang/reelforge) (Apache-2.0; reviewed at commit `740bf70dc1f068734e054e922c0a602e50f69ebd`, 2026-11-27). The exact upstream gallery reference files are included offline in `reference/reelforge-gallery/` with their license and notices; the ReelForge application/pipeline is not installed or required. The upstream gallery remains a reference, not a Khaam-tested template. Khaam's Arabic, taste, pace, sound, licensing and user-gate rules always win. Load this with `reference/adaptive-direction.md` for a motion-heavy or technically risky project.

## Plan the visual event, not just the text

At Gate A, each storyboard beat should name the scene's purpose, dominant visual event, main motion, entry/exit or handoff, and what must be tested. For a narrated story, align it to the approved words with `scripts/cues.py`; for other videos, use the approved beat/timing plan. Define a loose energy arc (quiet → build → peak → resolve) only when it helps the brief. Do not impose ReelForge's numeric intensity, BPM grid, scene count, layout bans or Korean copy system on Khaam projects.

Choose a starting technique by scene intent from the installed resources: the user's chosen style first, then `reference/alansari-motion-library.md`, `reference/hyperframes-registry.md`, `reference/bang-motion.md`, or the relevant engine guide. The catalog is a source of candidates, not a mandate. Preserve the approved brief and visual identity; never repeat a technique just because it exists in a gallery.

## Technique ideas from ReelForge, translated for Khaam

These examples make the upstream ideas discoverable without treating its engine-specific fragments as drop-in templates. Exact source is available offline under `reference/reelforge-gallery/fragments/`; the upstream links below point to the same reviewed commit. They are **not yet verified in Khaam**; build the equivalent with our selected engine and test it in the target project.

| Upstream idea | Khaam implementation route | Constraints to keep |
|---|---|---|
| [Cascade typography](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/typo/cascade-wave.html) or [masked line reveal](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/typo/mask-line-reveal.html) | HyperFrames whole-line/whole-word motion; if handwriting is intended, use `reference/tegaki.md` in Remotion | Never split joined Arabic into characters; test line direction, shaping and readability. |
| [Scale slam](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/typo/scale-slam-strike.html) | HyperFrames GSAP with one focal object/text line and frame-seek-safe easing | Reserve high-impact motion for a motivated hook/peak; keep word readable and avoid excessive bounce. |
| [Multiplane push](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/camera/multiplane-push.html), [orbit](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/camera/orbit-turntable.html) or [three-plane parallax](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/camera/parallax-3plane.html) | Use the existing HyperFrames scene/camera kit for 2.5D; choose Remotion/Three only for a real 3D need | Maintain stable anchors, controlled layer depth, Arabic safe areas and deterministic frame evaluation. |
| [Count-up](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/data/count-up-punch.html), [progress ring](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/data/progress-ring.html) or [line trace](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/data/line-chart-trace.html) | Build local SVG/CSS/GSAP or a Remotion component, driven by approved real values | Never invent data; label units and source; make the sequence readable rather than widget-heavy. |
| [Match-cut](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/pairs/match-cut-in.html), [whip-pan](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/pairs/whip-pan-in.html) or [zoom portal](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/pairs/zoom-portal-in.html) | Design the outgoing and incoming shots as a pair in the existing storyboard and Khaam scene kit | Plan the shared shape/position/vector on both sides; test the real cut; transitions are not mandatory. |
| [Glow pulse](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/atmo/glow-pulse.html) or [checkmark lockup](https://github.com/gongnyang/reelforge/blob/740bf70dc1f068734e054e922c0a602e50f69ebd/skills/reelforge/references/gallery/fragments/seal/checkmark-lockup.html) | Use a restrained local layer/effect or brand end treatment when the story actually calls for it | Keep the light/finish legible, avoid default CTA tropes, and verify contrast and motion on the final render. |

When a candidate is chosen, inspect only its matching file and `.meta.json` in the local snapshot, plus the relevant route in `ROUTING.md`; do not load all 31 entries by default. The metadata's `keep`/`mutate` notes are useful clues, but its `verified` stamp is valid only for upstream's engine. Rebuild with Khaam's engine contract and keep the source identifier in the project notes.

Do not reproduce ReelForge's card/layout prohibitions, Korean-first copy rules, intensity numbers, or scene-count budgets as Khaam defaults. The user's style and the brief decide whether any candidate is used.

## Pilot the riskiest scene internally

Before a full build or expensive render, identify the highest-risk visual question: Arabic legibility, mixed-direction text, a camera/3D move, a handoff between scenes, a cutout/occlusion, or a new animation package. Build the smallest representative test in the actual chosen engine and inspect the rendered result. Fix the cause or choose a safer method before scaling to all scenes.

This is internal production QA, not an extra approval gate. Keep the three existing user gates in `SKILL.md`; do not show test fragments or ask for extra approvals unless the test changes the plan, cost, asset permissions or requested result.

## Verify before reusing

After the draft render:

- Run the existing technical checks (`check_pace.py`, `check_mix.py`, engine checks) that apply.
- Inspect a time-labelled contact sheet or snapshots for composition, contrast, text clipping, Arabic shaping and continuity. A sheet cannot prove motion or audio; watch the rendered video and listen to its mix when available.
- Check the first frame, scene boundaries, the most complex motion and the final frame. Where seeking is supported, compare a cold-start render with a backward/random seek at the same frame; investigate any mismatch.
- Distinguish a deliberate hold from accidental frozen motion. A motion percentage or frame-difference threshold is a warning only; it must not overrule a meaningful pause or the user's direction.
- Rework only scenes with a concrete defect, then recheck the affected transition and the final full video.

Only a technique that passed a real render in the current engine, with its Arabic, font, timing and seek behaviour checked, may be called a verified house pattern. Otherwise label it a sketch/test and keep its result in the user's project log; never imply that an upstream demo or a static render proves it works in Khaam.

## Reuse and boundaries

A successful one-off does not silently become a global default. With the user's consent, record reusable choices in that project's `TASTE.md`; keep project-specific choreography in the project. The pinned gallery snapshot is already available for offline study; do not copy its engine-specific fragments into a video or run the ReelForge pipeline as-is. If importing additional upstream files is ever requested, pin the commit, preserve Apache-2.0 attribution/notices, and review assets/fonts separately. Adapt a selected technique to Khaam's engine and Arabic rules, then test it before calling it available.
