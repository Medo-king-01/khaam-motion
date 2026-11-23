# The jury pass — an independent review to raise a hero piece to the ceiling

**Derived from `rubric.md` in [mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15) (MIT, © Vincentwei1021)** — paraphrased and adapted to this skill's workflow, Arabic rules and sound v2. The upstream original is cached at `.cache/creative-tools/mg-styles-15/rubric.md` (restore per `reference/mg-styles-15.md`).

Our internal QA (`scripts/check_pace.py`, `scripts/check_mix.py`, the contact sheets of `reference/reference-and-delivery.md`) is **mandatory and stays mandatory**. The jury pass is an **optional, separate ceiling** for flagship work: what the user wants sent to a client/competition, a channel launch, a piece we claim is award-bar. It costs one extra session and one extra render round (two rounds at most). Do not add it to routine reels.

## How it works (two sessions, never the making session)

The reviewer must not be the maker. A different session — ideally a different model — that never saw the making of the piece. It receives exactly: **the video path**, **the brief and the style intent** (the Gate A plan, or the `styles/` file, or the adapted signature features), and **the output spec** (duration, resolution, fps, codec, loudness).

### Pass 1 — review

Tell the reviewer to act as a harsh independent motion-design jury (think: a Motionographer-grade editor, a Buck/ManvsMachine creative director, or — for Arabic/social packaging — a top designer-account lead). Kindness is useless; specificity is everything. Its brief:

1. **Watch properly.** Extract a contact sheet (one frame every 0.5 s), filmstrips around the fastest moves and the hero moment, and full-resolution frames at 5–8 key times. Judge small details at full resolution: edges, type setting, aliasing, banding, texture, clipping.
2. **Check the spec.** Exact duration to the frame, resolution and fps as specified, audio present; loudness −14 LUFS integrated ±1 when there is a voice, or per our sound v2 when there is none; true peak ≤ −1 dBTP; no unintended black frames or dead static spans; visual hits landing on audio onsets.
3. **Score 1–10 per dimension** (anchors: 5 = competent student work, 6 = decent template level, 7 = solid professional, 8 = high-end agency, 9 = award shortlist, 10 = the best in the world). Most first renders deserve 5–7; never inflate. Dimensions:
   - **style_fidelity** — the style is nameable in one second; every signature feature present and correct;
   - **concept_wow** — one clear idea, a hook in the first 0.5 s, an unmistakable hero moment, a composed end frame;
   - **motion_craft** — easing, spacing, overlap, anticipation/follow-through, arcs, transitions, motion blur; no dead or jittery motion;
   - **design_typography** — composition, grid, hierarchy, type setting (Arabic shaping included), palette, negative space;
   - **finish_texture** — lighting, grain, glow, detail suited to the style; no banding, aliasing, artifacts;
   - **sound_sync** — musicality (if any), genre-correctness, sync to picture, mix and master against our sound v2;
   - **technical** — spec compliance, fonts loaded, no glitches, clipping or popping, no tofu/fallback glyphs.
4. **5–10 fixes**, ordered by impact on the final impression. Each: timecode(s) · what is wrong (observable) · why it matters · a concrete how (numbers: easing curves, frame counts, px values, colours, layout change). Prefer few big upgrades over many nitpicks; **at least one fix must raise the wow factor**, not just polish.
5. **Critical flags** — anything reading as generic «AI-template», unnatural Arabic copy (grammar, register, مخاطبة), fallback fonts or tofu, spec failure.

Return: the score table, the critical issues, the ordered fix list.

### Pass 2 — the maker acts

Paste the review back into the **making** session with this instruction:

1. Keep a copy of the current video and source as version N (never destroy the reviewed cut).
2. Implement every critical issue and every high-impact fix. You may substitute a better solution for a listed fix — say why. Go beyond the list where you see a bigger upgrade, especially for the wow factor. Do not regress anything the jury listed as strength.
3. Re-render at full resolution, re-check the spec, and look at the fixed frames until the fixes have truly landed. Re-run `check_mix.py` / `check_pace.py` — the jury pass never replaces them.
4. Report which fixes were applied or skipped, and why.

Repeat at most twice. If a dimension still scores under 7 after two rounds, say so honestly to the user instead of shipping claims of «award level».

## Judging the Arabic fairly

- Give the reviewer `reference/arabic-typography.md` too, or the jury will mis-score Arabic (letter-splitting «for rhythm», scrambled glyphs, tracking, Latin easing assumptions) as if they were errors — or as virtues.
- The copy must read as written by a fluent native speaker: grammar, register (فصحى vs عامية), همزات, مخاطبة consistency. «Unnatural Arabic» is a critical flag, exactly as unnatural Chinese was upstream.
- Numerals follow the project's choice (Western digits by default); RTL mirroring judged as RTL, not as a mirrored LTR reference.
- Transliteration and Latin brand names inside Arabic copy: acceptable when the brand is Latin; the rest of the line stays Arabic.

## Honest boundaries

- An AI jury is not the user's ear and eye. When the two disagree, the user wins, and we do not argue with the delivery.
- A jury score from a different model is a signal, not a verdict; «8» here and «8» elsewhere are not the same 8. Report the scores, not a claim of quality.
- Never present this pass to the user as «two independent studios approved it» — it is one extra AI reader, valuable for its specificity, nothing grander.
- Upstream's own films averaged 7.6–8.2 by their own jury after two rounds; our ceiling is similar, not infinite.
