# Khaam integration — anything2explainer

**Upstream:** https://github.com/Vincentwei1021/anything2explainer  
**Snapshot commit:** `dc2186667b2a7c4722f6a42bb0abd0ae18db0ec9`  
**Vendored for:** private/personal use inside this Khaam Motion project (at owner's request).

## What it is

`anything2explainer` is a Claude Code/Codex skill that turns any topic into a narrated motion-graphics explainer video (black-canvas MG style), with TTS voiceover, subtitles, and chapter progress bar. Every frame is drawn in code with Remotion. It includes a full pipeline: research → narration → TTS timeline → storyboard → parallel shot build → QC → render.

## Key capabilities to reuse in Khaam

- **Narration-first explainer pipeline**: sourced research, narration script, TTS-generated frame timeline, storyboard tokens, shot-by-shot build.
- **Remotion template** (`template/`): black-canvas explainer project with overlays (HUD, chapter bar, subtitles), primitives, lighting/fx, fonts (SIL OFL).
- **Scripts** (`template/scripts/`): `tts_build.py`, `render_storyboard.py`, `preview.sh`, `render.sh`, `still.sh`, `motion_check.py`, `frame_metrics.py`, `selfcheck.py`, `sheet.py`.
- **Reference rules** (`reference/`): build rules, QC rules, composition/light, motion vocabulary, narration guidance, storyboard format, research brief, prompts, lessons.
- **Examples** (`examples/`): contrast examples and full RAG sample (frames, storyboard, QC, shots source) as quality bar.

## License / notices (important)

- Upstream LICENSE is **PolyForm Noncommercial License 1.0.0** with required notice: noncommercial use is free; **commercial use of the toolkit requires prior authorization from the author**.
- Fonts under `template/public/fonts/` are licensed separately under **SIL Open Font License 1.1** (see `template/public/fonts/LICENSE.md`).
- Videos produced with the toolkit belong to their creators, but the toolkit itself remains under upstream license terms.
- This snapshot was added for **private/personal use** in this repo; before redistribution, public sharing, or commercial use, review upstream license and obtain required authorization.

## How to use inside Khaam

1. **As a reference skill**: read `integrations/anything2explainer/SKILL.md` and its `reference/` files when building explainer videos.
2. **As a template source**: copy `integrations/anything2explainer/template/` into a working video project (not back into skill source except intentional updates), then adapt to Khaam Arabic/brand/taste rules.
3. **Borrow scripts/patterns**: reuse motion/QC/storyboard/TTS workflow ideas; verify dependencies and paths before running.
4. **Arabic adaptation**: Khaam Arabic rules still apply (`reference/arabic-typography.md`) — RTL, whole-word shaping, Arabic-safe fonts, no broken kashida/letter splitting. The upstream style is optimized for Chinese/English black-canvas MG; adapt carefully for Arabic.

## Integration notes

- Keep this directory as upstream snapshot + Khaam note; avoid destructive edits unless intentionally patching.
- When updating from upstream, record new commit hash and review LICENSE/NOTICE changes.
- Do not present PolyForm NC material as MIT/Apache/free-for-commercial redistribution.
