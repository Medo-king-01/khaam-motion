<!-- Khaam Motion · reference file, loaded on demand from SKILL.md -->
# Remotion templates: ready starters for common video jobs

Use these when the job is a Remotion job (`reference/remotion.md`) and one of these patterns fits. The 17 listed upstream starters are **third-party Remotion templates**, not Khaam defaults. `tegaki/` is a separate Khaam-authored optional starter that installs the external Tegaki package. HyperFrames remains the default engine for most Khaam work.

## License and safety (read before use)

- **Remotion license applies.** The Remotion framework and official templates are distributed under the [Remotion License](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md), **not** a blanket permissive OSS license. Free for individuals, non-profits, and for-profit organizations with up to 3 employees; a company of 4+ needs a paid Company License. Evaluate eligibility before commercial/client use.
- **Template files say `UNLICENSED` in package.json and have no separate LICENSE file** in the upstream repos at the pinned revisions below; treat the Remotion License as governing, and check upstream again before redistribution or productization.
- **No auto-install.** Fetch only with the user's explicit consent. Inspect fetched code before running `npm install`/`npm run dev`/render. Never run upstream scripts blindly.
- **Khaam adaptation rule.** When adapting a template into a Khaam video, keep Khaam's Arabic rules (`reference/arabic-typography.md`): RTL direction on word rows, whole Arabic words only, tested Arabic fonts, no broken letter joining. Replace English-only demo fonts/text with Arabic-safe choices when the output is Arabic.
- **Private-use vendored copies.** At the repository owner's request, pinned snapshots are vendored in `templates/remotion/` for private use inside this project. See `templates/remotion/NOTICE.md`. Before any redistribution/public sharing/company-license-triggering use, review the Remotion License.

## The four repos the user asked to benefit from

| Repo / source | What it gives you | Good Khaam fit | Vendored copy | Refresh/fetch |
|---|---|---|---|---|
| [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | The Remotion framework source, docs, packages, examples. Very large monorepo. | **Framework reference.** Install Remotion packages in the video project as `reference/remotion.md` describes; use capability map in `reference/remotion-capabilities.md`. | — (too large) | `npm install remotion @remotion/cli ... --save-exact` in video project |
| [template-overlay](https://github.com/remotion-dev/template-overlay) | Animated overlay card/title for compositing over footage. | Lower-thirds, callouts, name plates, overlays. | `templates/remotion/overlay/` | `python scripts/fetch_remotion_templates.py template-overlay` |
| [template-code-hike](https://github.com/remotion-dev/template-code-hike) | Animated code snippets/transitions (Code Hike). | Dev explainers, code walkthroughs; keep code LTR, Arabic captions RTL. | `templates/remotion/code-hike/` | `python scripts/fetch_remotion_templates.py template-code-hike` |
| [template-tiktok](https://github.com/remotion-dev/template-tiktok) | Word-by-word captions, Whisper.cpp helper, caption components. | Short-form captioned reels; for Arabic use Khaam timings, not English-only Whisper. | `templates/remotion/tiktok-captions/` | `python scripts/fetch_remotion_templates.py template-tiktok` |
| `packages/template-blank` (monorepo) | Minimal blank Remotion starter. | Clean starting point when other templates don't fit. | `templates/remotion/blank/` | Re-copy from pinned monorepo snapshot |
| `packages/template-helloworld` | Basic Hello World composition. | Learning/basic branded motion. | `templates/remotion/helloworld/` | Re-copy from pinned monorepo snapshot |
| `packages/template-still` | Still/thumbnail rendering with Remotion Still. | Covers, thumbnails, poster frames, social stills. | `templates/remotion/still/` | Re-copy from pinned monorepo snapshot |
| `packages/template-three` | @remotion/three + React Three Fiber 3D starter. | 3D product/logo scenes, camera moves; deterministic render. | `templates/remotion/three/` | Re-copy from pinned monorepo snapshot |
| `packages/template-audiogram` | Audiogram/waveform + captions. | Podcast clips, quote/audio-led social posts; Arabic via Khaam timings. | `templates/remotion/audiogram/` | Re-copy from pinned monorepo snapshot |
| `packages/template-music-visualization` | Audio-reactive visuals. | Only when user explicitly wants music/visualization (Khaam default: no music). | `templates/remotion/music-visualization/` | Re-copy from pinned monorepo snapshot |
| `packages/template-skia` | @remotion/skia graphics starter. | 2D vector/Skia effects; test runtime support. | `templates/remotion/skia/` | Re-copy from pinned monorepo snapshot |
| `packages/template-prompt-to-motion-graphics` | Prompt-to-motion-graphics workflow pattern. | AI-assisted MG workflow reference; review keys/costs/terms. | `templates/remotion/prompt-to-motion-graphics/` | Re-copy from pinned monorepo snapshot |
| `packages/template-prompt-to-video` | Prompt-to-video workflow pattern. | AI-assisted video workflow reference; review keys/costs/terms. | `templates/remotion/prompt-to-video/` | Re-copy from pinned monorepo snapshot |
| `packages/template-stargazer` | Data-driven Stargazer recap. | Data-driven recap/celebration videos. | `templates/remotion/stargazer/` | Re-copy from pinned monorepo snapshot |
| `packages/template-vibe-code` | Vibe-code visual style starter. | Stylized promo/code visuals; adapt to Khaam taste. | `templates/remotion/vibe-code/` | Re-copy from pinned monorepo snapshot |
| `packages/template-electron` | Remotion + Electron desktop app starter. | Desktop Remotion tool/app workflows. | `templates/remotion/electron/` | Re-copy from pinned monorepo snapshot |
| `packages/template-element-library` | Reusable Remotion element/component library. | Reusable branded motion components/elements. | `templates/remotion/element-library/` | Re-copy from pinned monorepo snapshot |
| `packages/template-recorder` | Remotion Recorder app template. | Recording/studio workflow reference (large demo media omitted). | `templates/remotion/recorder/` | Re-copy from pinned monorepo snapshot |
| Khaam + [Tegaki](https://github.com/gkurt/tegaki) | Arabic handwriting-reveal composition with frame-controlled progress. | Short hand-drawn title/word, only when the chosen look calls for it; test RTL and seeking. | `templates/remotion/tegaki/` (Khaam-authored; external Tegaki package is installed project-locally) | Follow `reference/tegaki.md`; pin and review the package/license |

## Vendored copies (private use) and refreshing

Pinned snapshots are already vendored in `templates/remotion/` for private use in this project. Use them directly when starting a Remotion video. For refreshing from upstream into gitignored cache, the fetch script downloads pinned revisions with SHA-256 verification into `.cache/creative-tools/remotion-templates/`:

```bash
# list
python scripts/fetch_remotion_templates.py --list

# fetch all three templates
python scripts/fetch_remotion_templates.py

# fetch one
python scripts/fetch_remotion_templates.py template-tiktok
```

After fetch, inspect the template:

```bash
ls .cache/creative-tools/remotion-templates/template-overlay
cat .cache/creative-tools/remotion-templates/template-overlay/README.md
```

## How to adapt a fetched template into a Khaam video

1. **Confirm the job needs Remotion.** If HyperFrames can do it, stay in HyperFrames.
2. **Pick a starter** from `templates/remotion/<name>/` (already vendored for private use) or fetch/refresh with `scripts/fetch_remotion_templates.py`. Inspect code and dependencies before running.
3. **Create a video folder** in the workspace (`python "<skill>/scripts/workspace.py" --new-video "..."`).
4. **Copy the template** into the video project (e.g. `remotion/` subfolder inside the video project), keeping upstream attribution in the video manifest/notes. Keep the skill source clean; don't copy rendered artifacts back.
5. **Install dependencies inside the video folder** with the user's OK. Pin versions. Do not install globally.
6. **Arabic pass:** apply `reference/arabic-typography.md`, use Arabic-safe fonts, keep captions/narration RTL, keep code/URLs/numbers direction-safe.
7. **Khaam delivery:** run the normal checks (framing, Arabic QA, timing, sound, export, licences/versioned output) and deliver through the normal workspace flow.

## Notes per template

### template-overlay
- Very small: one overlay component + root + config.
- Useful as a starting point for transparent/overlay renders. Verify alpha/export settings for the target editor workflow.
- Replace the demo Roboto/English text with the project's font and copy.

### template-code-hike
- Depends on `codehike` and `@code-hike/lighter`; heavier than overlay.
- Good for code walkthroughs. Keep syntax/code blocks LTR; any Arabic explanation/caption around them should follow Khaam Arabic layout rules.
- Check Code Hike and dependency licences in the fetched `package.json`/lock before shipping.

### template-tiktok
- Includes caption layout components and a `sub.mjs` captioning helper using `@remotion/install-whisper-cpp`.
- The upstream sample video is intentionally skipped by the fetch script (large demo binary). Bring your own footage into the video project.
- `public/theboldfont-license.rtf` is included upstream; read it before using the font. For Arabic projects, prefer Khaam's Arabic font flow (`reference/arabic-fonts.md`, `scripts/get_fonts.py`).
- For Arabic captions, prefer Khaam's timed-narration path over the English-only Whisper example.

### Tegaki handwriting starter
- This is original Khaam integration code, not an upstream Remotion template. It uses the external `tegaki@1.1.0` package and its bundled Amiri font, with versions pinned in `templates/remotion/tegaki/package.json`.
- Install only inside the copied project, after explaining the download and getting permission. Tegaki is MIT; Amiri is SIL OFL 1.1; Remotion has its own separate license.
- Use only for a specific handwriting-reveal direction. Arabic joins, font coverage, rendered frames and deterministic seeking must pass `reference/tegaki.md` before production use.

## What not to do

- Do not clone the full `remotion-dev/remotion` monorepo into this repo (it's very large). Use sparse checkout/capability extraction instead.
- Do not treat "template has no LICENSE file" as permission to redistribute freely.
- Vendored private-use copies in `templates/remotion/` are kept with NOTICE/attribution; before any redistribution/public sharing/company-license-triggering use, review Remotion License and third-party licences.
- Do not claim a render succeeded because the template was fetched/copied.
- Do not use English-only caption/transcription assumptions for Arabic narration.
