# HyperFrames Craft Notes (Khaam-adapted, Batch 2)

Adapted from upstream HyperFrames skill references (Apache-2.0, commit `add940201ebe5903c540232210e8f79264ef3a86`) and rewritten for Khaam Motion. These are **craft reminders**, not a replacement for Khaam rules. When in conflict, Khaam rules win: `reference/arabic-typography.md`, `reference/pace.md`, `reference/film-sound.md`, `reference/hyperframes.md`.

## Motion defaults (use as starting points, not a template)

- **Fast moves:** 0.3–0.6s. One move = one tween. Motion blur should match the move direction/energy, not be decorative.
- **Arrive slow, leave clean:** entrances land with a long tail; exits are ~40–50% shorter than entrances. Avoid "slide, stop, then leave".
- **Ease by role:** arrivals ease out (expo/power4.out feel); camera moves and color floods ease in-out; exits/zoom-throughs ease in. Avoid the same `power2.out` everywhere.
- **Overlap/stagger:** next element can start when previous is ~30–50% done. Letters/words/items stagger lightly; avoid fully sequential robotic reveals or all-at-once cheap reveals.
- **Titles:** once landed, keep title still; motion moves to next element/camera/world. Vary entrance styles within a film. For Arabic, animate whole words/lines only.
- **Holds:** readable line holds ~0.5s + 0.3s/word; final line >=2s. One/two-word chapter lines can be shorter.
- **Rhythm:** contrast speeds. Not every scene same tempo. But keep Khaam pace rules (P1–P13): frame 0 hook, no dead stretches, visible motion/camera.

## Defaults to avoid (Khaam-adapted)

- Breathing/floating/pulsing loops as fake motion on titles/UI.
- Titles drifting/scaling after landing.
- Bounce on UI, click rings everywhere, same entrance for every scene.
- Generic fade+slide-up on every element.
- Dark void + glow/neon/purple gradient default look unless the brand/reference explicitly calls for it.
- Over-decorated HUD/corner labels/frame borders when content doesn't need them.

## Transitions with cause

Use a small set (3–5 kinds) and give each a reason. Hard cuts inside a scene are fine; avoid making every beat a hard cut. Worlds/scenes should not casually crossfade unless motivated.

Useful patterns (adapt to Khaam): zoom-through button/object, object becomes world, morph, carry-across, color flood, whip, iris from click, dip cut, blur swap on one stage. For HyperFrames registry blocks/components, check `reference/hyperframes-registry.md` before hand-building.

## Format/structure reminders

- Keep one scene per sub-composition; stable ids; timed elements in HTML.
- Copy, brand colors, swappable media as variables.
- `data-track-index` is lane organization, not paint order (z-index is paint).
- Use `fromTo` in GSAP for reliable seek behavior; register timelines after tweens.
- No `Date.now()`, unseeded randomness, timers, or `repeat:-1` for rendered content.
- Fonts: only bundled/declared fonts are reliable; other families need `@font-face` from `assets/fonts/`.
- Audio elements need ids; no `crossorigin` on media.

## Look/spec discipline

- Settle look before first scene: ground/ink/accent, display/body faces, material/medium, light/depth, banned defaults.
- Turn adjectives into numbers (sizes, durations, eases, opacity, spacing, color values).
- For branded work, use real brand tokens/fonts/screens where available; don't invent brand.
- Keep a "BANNED" list for defaults the project must not fall into; update it after review.

## Review pass (quick)

- Snapshot frame 0, hook moment, transitions, dense text, end card.
- Check Arabic shaping/RTL order/harakat placement/full-size readability.
- Check for dead stretches, over-busy motion, unreadable text, and sound/visual sync.
- Run `check_pace.py` for told videos; use HyperFrames check/snapshot for engine-level issues.
- If using upstream registry components, verify RTL adaptation, font substitution, and no LTR layout bleed.

## Provenance

Adapted for Khaam from HyperFrames upstream skill references (`skills/hyperframes/references/*`), Apache-2.0, commit `add940201ebe5903c540232210e8f79264ef3a86`. Not a verbatim copy.
