# Visual reference and memory helpers

Optional, local-only tools adapted from useful ideas in Huashu Design. They complement Khaam's existing `analyze_ref.py`, `preview.mjs`, `check_pace.py`, `check_mix.py` and user-taste memory; they do not replace a render review or create new approval gates. Load this guide when comparing a visual reference, reviewing style repetition across projects, or recording a durable user preference.

All image commands need Pillow. If unavailable, stop and follow the existing permission-gated package setup; these commands never install it. None of the helpers below accesses the network. The board reads local image files only, and all outputs are reference/diagnostic material unless separately approved for final use.

## 1. Measure a frame or compare it to a reference

`visual_reference.py` reads a local still and reports approximate dominant colours, vertical edge-density bands and a coarse spatial signature. These are observable descriptors—not semantics, quality, similarity proof or originality checks. Image dimensions and crop should be comparable; for video, choose the same aspect ratio and a meaningful representative frame.

```bash
python "<skill>/scripts/visual_reference.py" measure "<reference.png>" "<project-frame.png>"
python "<skill>/scripts/visual_reference.py" measure --json "<project-frame.png>"
python "<skill>/scripts/visual_reference.py" compare \
  --reference "<reference.png>" --result "<project-frame.png>" \
  --out "<project>/cache/reference-comparison-v1.png"
```

The compare command produces a side-by-side card and prints a concise metric summary; add `--json` for the full descriptors. It refuses to overwrite an existing card. Use this only to make questions concrete (for example, “the reference is mostly quiet at the top; our frame puts equal detail everywhere”), not to mechanically make a render match. It cannot read motion, understand labels or assess Arabic shaping. Inspect the image itself and the actual video.

## 2. Build a contact sheet from local reference images

`reference_board.py` composes selected local stills, user-provided screenshots or frames already extracted by `analyze_ref.py`. It does not visit websites or download anything. Pass image files and/or non-recursive folders:

```bash
python "<skill>/scripts/reference_board.py" "<project>/assets/refs" \
  --title "Visual references · concept A" --cols 3 \
  --out "<project>/cache/reference-board-v1.jpg"
```

It creates a `.sources.md` sidecar with each source filename, SHA-256 and its reference-only status. It never changes or copies the source images, caps a board at 36 images, and refuses to overwrite the board or sidecar. Keep boards and their inputs in project cache/reference folders; don't publish or include them in a final video unless separately cleared. For an online page, capture a still using the user's approved/browser workflow first, then give that local screenshot to this helper.

## 3. Check repetition without banning an approved look

`visual_ledger.py` stores only a chosen still's derived palette/layout descriptors and short style labels in the local, private `~/.cache/khaam-motion/visual-ledger.jsonl`. It does **not** store the frame, its path, or a URL. Use it when helpful—especially for a run of unrelated videos or deliberate style exploration—not as a mandatory production step.

```bash
python "<skill>/scripts/visual_ledger.py" show --last 12
python "<skill>/scripts/visual_ledger.py" check "<candidate-frame.png>" \
  --motif "paper map with one highlighted route" --last 12
python "<skill>/scripts/visual_ledger.py" add "<approved-frame.png>" \
  --project "video-slug" --version 1 --aspect 9:16 \
  --style "editorial diagram" --motif "one highlighted route" \
  --motion "route draws, then settles" --source "user's approved reference"
```

Record only after an approved project outcome, and use neutral, short labels. `check` reports possible palette/layout/tag overlaps as review prompts; it never blocks a render. Repeating a user-approved look is valid. Khaam's current project and the user's explicit taste outrank the ledger. Pass `--ledger <path>` to use a project-specific file or a test ledger. No command deletes or rewrites previous records; duplicate project/version entries are rejected.

## 4. Keep evidence and scope in the existing taste file

`taste_notes.py` adds a machine-readable, human-visible section inside the existing `user-taste.md`; it creates no parallel memory store and preserves all text outside its managed markers. Use it only for durable cross-project notes. A one-off correction belongs in that project's `TASTE.md`/`LOG.md`, not global memory.

```bash
python "<skill>/scripts/taste_notes.py" add \
  --kind preference --statement "«أبغى العناوين أقصر»" \
  --scope "explainer hooks only" --topic Arabic --topic hooks \
  --evidence "user's exact statement in this conversation" \
  --next-time "keep the opening title to one short line"
python "<skill>/scripts/taste_notes.py" show --topic hooks
python "<skill>/scripts/taste_notes.py" supersede T0001 \
  --reason "user changed this preference on a later project"
```

Kinds distinguish an explicit **preference**, a one-project **observation**, and a repeated or measured **verification**. Evidence and scope are required; preference statements should preserve the user's exact words. Superseding preserves the old note with its reason/date instead of silently erasing it. The helper only edits its own marked section. It does not read chat history, infer consent or copy notes into the public skill. Keep the existing project-level `TASTE.md` §9 in sync for a current video and keep secrets/sensitive personal details out of both files.

## 5. Optional quantitative video-reference report

For a local video reference, `analyze_ref.py --metrics` adds a small report to the existing frame sheets, cut list, extracted audio and spectrogram. It records low-resolution average luminance about every 0.5 s, audio RMS about every 0.25 s, simple transient candidates, and the scene-cut times already detected by the analyzer. Add `--bpm <known-value> [--phase <source-seconds>]` only when a beat grid is already known; the tool reports each cut's offset from that grid and never estimates BPM.

```bash
python "<skill>/scripts/analyze_ref.py" "<project>/assets/refs/reference.mp4" \
  --start 0 --dur 15 --metrics --bpm 120 --phase 0 \
  --out "<project>/cache/reference-analysis-v1"
```

Outputs: `measurements.json` (structured data) and `measurements.txt` (readable summary). The run record in `analysis.json` identifies whether metrics were produced. These are descriptive signals, not a quality score, semantic reading, synchronization proof, rights check, beat detector, or substitute for viewing/listening. The feature is optional and adds no user approval round; it uses local FFmpeg output and the already-extracted audio. The analyzer removes only its known generated outputs within the analysis directory on rerun, as documented in `reference/reference-and-delivery.md`.

**Source distinction:** this feature extends Khaam's existing `scripts/analyze_ref.py`; the measurement code is implemented locally and does not copy Herk source. The idea of reporting luminance/RMS/transient and beat-offset measurements was informed by [Herk Edit Kit's reference analyzer](https://github.com/nateherkai/herk-edit-kit/blob/10511e5af86fc47756ea89803b397422e2d89284/.agents/skills/motion-showreel/scripts/analyze-reference.mjs). That repository's separate licenses and third-party exclusions do not change Khaam's tool or grant rights to reuse reference media.

## Provenance and limits

- These are Khaam-specific tools, not Huashu's original scripts. The reference-measurement idea was informed by the pinned Huashu `scripts/ref_card.py`; local boards by `scripts/ref_board.py`; and scoped/evidence-backed memory by `scripts/learn.py`. See `reference/huashu-design-upstream/SOURCE-NOTICE.md` for the MIT source subset boundary.
- No website capture, scraping, image download, API call, font install, AI judge, or new browser runtime is performed by these scripts.
- Pillow pixels cannot identify content, distinguish important from decorative edges, confirm licensing, evaluate movement/sound, or guarantee that two works are artistically different. Numeric thresholds are deliberately only hints.
