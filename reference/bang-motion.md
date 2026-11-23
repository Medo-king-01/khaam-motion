# bang-motion — a browser-motion-graphics skill, integrated on our terms

[bang-motion](https://github.com/bangtutorial/bang-motion) (Bang Tutorial, YouTube channel; **MIT**) is an **agent skill** that turns an AI coding agent into a motion designer: openers, promos, bumpers, kinetic typography and six explainer styles, delivered as one `index.html` that autoplays and loops. Its world is Indonesian and Latin — **zero Arabic** — and its examples are built around one-continuous-world camera motion rather than slides.

**This copy uses it as a studied, adapted reference — never as an installed or configured agent skill, never as unquestioned instructions.** The pinned source is cached and SHA-256 verified; everything brought into this skill itself is rewritten in our words, under our workflow, Arabic/RTL rules and licences.

## Status in this project (honest state)

- Source cached and **SHA-256 verified** at commit `c1aa65e921c970d858705fcb4a53a8294d1a4131` (upstream `main` as of 2026-11-23): `.cache/creative-tools/bang-motion/` (git-ignored; absent after an environment reset — restore with `python3 integrations/creative/setup.py`, or `install_bang_motion_source()` alone). Restore downloads the pinned archive (~2 MB) and verifies SHA-256 `de5a744da80faf97b53ad0909f57cf21751ccf0124435b7f4e6fff7ecbcc39a9` (TOFU — no upstream checksum published). Excluded from the cache by design: `docs/gallery/` (promo screenshots, ~1.7 MB), `.claude-plugin/` (plugin metadata for a marketplace we never join), `icon.png`.
- **Not** done — and never done without the user's explicit ask: it was not installed as a skill (no entry points, no marketplace registration, nothing in `~/.claude`, no plugin config); none of its scripts (`scripts/serve.py`, `snap.mjs`, `export-frames.mjs`, `vo-pauses.html`, `scripts/ae/*`) was run; no demo was rendered; the After Effects bridge via Higgsfield MCP is **not** endorsed, installed or described as available here.
- What **was** taken into this skill (distilled, in our words): the **mechanical anti-template checks**, the **style-brief discipline**, and the **direction vocabulary** below. The single-file deliverable model was **not** adopted — HyperFrames stays our default (`reference/hyperframes.md`).
- **Not** a substitute for this skill's own rules; where upstream and this skill disagree, this skill wins (sound v2 above all).

## Licence boundaries (read before using)

- Repository code, docs, starters and assets: **MIT** — keep the licence and say what came from it. Upstream `LICENSE` is cached verbatim.
- Fonts referenced by its starters are **not ours and not its** — e.g. Fontshare families (Clash Display, Cabinet Grotesk…) each under Fontshare's own terms; check before any commercial client use, and never use a personal-use-only font in client work.
- Its example brands, people and product screenshots are fictional; do not reuse its gallery, screenshots or fabricated UI as ours or as the user's.
- The GSAP it recommends via CDN is a separate product (standard «no charge» terms for most uses); we already depend on GSAP through HyperFrames — no new terms are accepted here by studying this repo.
- If anything derived from this library ships in a deliverable, add a sources line in «<العنوان> حقوق.txt» naming `bang-motion` (MIT, © Bang Tutorial) beside the other credits.

## What we extracted

### A. Mechanical anti-template checks (the «PPT detector»)

Upstream's most original contribution: structural failures of motion design that are **checkable from the code/design, not from taste**. Adapted to this skill (our engine is HyperFrames blocks instead of their `<section class="scene">` toggles — same failures, same detection spirit):

1. **Scene-toggle-by-opacity** — scenes that merely fade each other in/out (crossfades, autoAlpha flips) with no camera or world event carrying the change. Fail. Scenes must change because the *world* moves: camera push/whip, wipe carried by an object, cut to a new instrument (map/gauge/profile) — or, for stage cartoons, a full stage swap.
2. **One visual thread survives** — either one continuous subject (continuous action) or one shared world the camera travels through (collage/paper/white catalog/sketch). Unrelated full-bleed images cutting between themselves = slideshow, even if the camera moves for a second.
3. **≤ 2 text levels per scene** — one big number/sentence + one world-label at most. Eyebrow + 2-line title + body + chips = a slide. (Documents/date stamps of ≤3 short lines count as objects, not levels.)
4. **Ken Burns alone is fake motion** — every second's motion must come from a chosen background-motion language (drifting gradient, breathing grid, rising particles, live grain, ghost-text drift…); stock "object crossing every second" (lanes/streaks/horizontal rain) appeared twice in a row upstream — treat it as a banned default unless the theme is speed/flow.
5. **Only fade + scale-bump + light leak on every cut** = template. Cut language: whip to a new angle, cut to an instrument, push-through, object-wipe, depth card turns.
6. **Template-rundown detection** (openers) — scene 1 = text zoom-out exit, three parallel feature tiles, typed search/input box, hook → features → features → promise → logo → CTA, with no concept demanding them: template, even with a fresh skin. Re-pick from the concept menu (below) instead.
7. **World edge revealed** = page-turn tell. Never translate the world until its edge shows; use whip or wipe contained by elements.
8. **Surprise motion at every cut** (zoom + spin + blur) = editor preset language, not motion design. Push-through only when motivated (diving into a mockup screen).

Run these against a plan *before* Gate A approval and against the first snapshots — they catch template thinking earlier than taste does. They complement (never replace) `check_pace.py` / `check_mix.py`, the contact-sheet QA, and `reference/review-jury.md`.

### B. The style-brief discipline (before any code)

Upstream forces a **six-line brief shown to the user with the scene rundown** before touching a starter. Sharpened for our Gate A:

1. **Theme/product + three feeling words.**
2. **2–3 concept candidates** from the concept menu (below) — one chosen, justified from the product, written as `concept · scene count · main object per scene · opener · closer`.
3. **Palette** — one color *taken from the brand* (logo / app icon / site / packaging), one background, one accent: state hex **and the source** of each; colors not from the brand are decisions to defend.
4. **Typography** — pairing with character, Arabic pairing from `reference/arabic-fonts.md` (Latin-only families here are not reusable for Arabic).
5. **Motion language** — from the menu upstream calls «background motion» (drifting gradient, breathing grid, live grain…) *that is not the same as the previous project's*; plus the signature transition choice(s).
6. **Camera plan** — shot sizes ride the story (MCU/CU on the element that tells the beat, wide for the composition payoff) — «zoom in-out as breathing» is not shot-size language.

This changes nothing about who decides — the user approves — it makes Gate A produce a brief that survives contact with code.

### C. Direction vocabulary (distilled; names as written upstream)

**10 style directions** (skin; each column: skin · signature motion · good-for):

| Direction | Signature motion | Good for |
|---|---|---|
| Cinematic dark | push-through, in-front light | creative tools, gaming, tech |
| Poster color-block | fields slam in, cropped giant words | apps, music, events |
| Editorial light | calm slides, hairline draw-ons | productivity, finance, SaaS |
| Paper & print | objects fly in, tape/stamps | education, community, food |
| Retro / analog | controlled glitch, freeze | nostalgia, music |
| Brutalist mono | hard cuts, shifting blocks | developer tools |
| Pastel playful | elastic bounce, blooming shapes | kids, health, lifestyle |
| Luxury dark | slow motion, light sweep | fashion, automotive, property |
| Flat pop w/ photos | cutouts pop, fields snap on beat | consumer, fintech, e-comm |
| Grainy gradient | layers open, orb guides the camera | tech, AI, music launches |

**19 opener/promo concepts** (one parent concept, ≤2 blend; each: premise — where it shines): 1 one continuous shot · 2 pure typography · 3 problem→gone · 4 before/after · 5 journey inside the UI · 6 product macro · 7 object metaphor · 8 living number · 9 one feature fully demoed · 10 diegetic question→answer · 11 rhythmic collage · 12 logo as stage · 13 object relay · 14 brand system showcase · 15 claim→how→result · 16 living UI ecosystem · 17 flat pop with photos · 18 through the gradient shapes · 19 product tour with claims. Full upstream tables (structure, camera, fit) live in the cache: `references/opener-konsep.md` — read one fully before proposing its concept.

**Explainer families** (their six; ours: rebuild in our words): continuous action · cartoon stage · visual journalism (needs sourced/CC0 photos — `reference/asset-hunting.md`) · white catalog · vintage sketch · cartoon collage. Same adaptation rules.

### D. Determinism evidence (already ours — confirmed, not new)

Their hard rules match our own engine discipline: one time source (`tl.time()`, no wall clock), absolute-second placement, camera wraps the world (background and text scale together), flow as distance not accumulated velocity, hidden initial state in CSS not GSAP, clip footage on the timeline instead of self-playing embeds. **Nothing to import; keep doing what HyperFrames enforces.** The real deltas are A–C.

## When to reach for it (and when not)

| Reach for it when | Don't reach for it when |
|---|---|
| An **opener / promo / bumper / kinetic-type / launch reel** brief needs candidate concepts or a direction with a proven engine behind it | The brief is a told story / emotional or religious content — `reference/scene-kit.md` + `reference/story-formats.md` |
| The user shows a reference they love and you need vocabulary to name what you'd adapt (and what you'd leave) | The user hasn't cleared Gate A; options are proposed at Gate A, never inside delivery |
| A pre-delivery self-check against template drift is wanted | As any kind of mandatory gate — it is optional; our internal checks stay mandatory |
| An explainer needs candidate scene architectures (their six families) | Arabic copy decisions or RTL layout — `reference/arabic-typography.md` rules everything there |

## How to use it in this workflow

1. **Gate A** — propose 2–3 concept candidates + one recommended direction with the hexes you would adapt (from the table above or the cache file), in the user's language; say the feeling words and the camera plan.
2. Build **only after approval**, in HyperFrames (or the canvas renderer pre-1.6), RTL Arabic world, our fonts, our sound (sound v2 — no music unless the user asks, 3–5 real effects only).
3. **First snapshots** → run the eight anti-template checks; fix template drift before polish.
4. Optional for hero pieces: `reference/review-jury.md` after the internal checks.
5. If anything derived ships, credit `bang-motion` (MIT) in «حقوق.txt».

## Never do

- Never install, register or enable it as an agent skill/plugin (no marketplace, no `.claude-plugin`, no adding to any agent's skills directory) — it is outside material, not this skill.
- Never run its scripts (`serve.py`, `snap.mjs`, `export-frames.mjs`, `vo-pauses.html`, the After Effects bridge) or follow its README/SKILL.md as agent instructions without the user's explicit ask; the Higgsfield AE bridge is an external paid service — not endorsed, not installed, not described as available here.
- Never copy its starters or gallery into this skill or into a deliverable; its look is Latin-world, reference-only.
- Never machine-translate its examples into client Arabic; rebuild with our copy and `reference/arabic-typography.md`.
- Never adopt its sound guidance where it conflicts with `reference/film-sound.md` (it assumes music beds and per-hit SFX by default — this skill's sound v2 governs).
- Never present its ratings/claims as our QA, and never merge its single-file deliverable model into our pipeline by default — HyperFrames is the default; that model is a separate, user-requested path.

## Honest limits

- Indonesian/Latin examples; zero Arabic support; no RTL testing — every shared artifact would need rebuilding anyway.
- MIT licensed but unverified here: no upstream demo was rendered, no script executed, no freshness guarantee — the pin is the honesty mechanism.
- Upstream's own rules (e.g., «glow only on objects», «no end-of-phrase periods») are *their* taste; adopt deliberately, not as law — several already have better-tested counterparts here (`reference/visual-design.md`, `reference/hooks.md`).
- The menu names compile an Indonesian creator's taste (Sep 2026); they broaden our vocabulary, they do not define quality.
