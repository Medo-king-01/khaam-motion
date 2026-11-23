<!-- Khaam Motion · reference file, loaded on demand from SKILL.md -->
# Remotion capabilities map (for Khaam)

Practical map of Remotion capabilities relevant to Khaam Motion. This is an original Khaam-oriented summary, not copied Remotion docs. For authoritative API details, consult the official Remotion docs/site for the version you install. Remotion is under the Remotion License (check company-license eligibility).

## When to pick Remotion over HyperFrames

Use Remotion when React/programmatic composition pays off:
- **3D / 2.5D**: `@remotion/three` + React Three Fiber for real 3D scenes, camera moves, lighting.
- **Data-driven / templated videos**: props, Zod schemas, `calculateMetadata`, batch variants.
- **Code-heavy animations**: code walkthroughs (Code Hike template pattern).
- **Caption-heavy short-form**: word-by-word captions timed to audio (TikTok captions template pattern).
- **Overlays for editors**: animated lower-thirds/callouts rendered as overlays.
- **Programmatic rendering pipelines**: stills, videos, batch renders, parameterized compositions.

Stay with HyperFrames for most Arabic editorial/told/story videos where its starter, scene kit, and render flow are simpler.

## Core capability areas

| Capability | Remotion packages/APIs (typical) | Khaam use |
|---|---|---|
| Composition model | `Composition`, `Still`, `Folder`, `registerRoot` | Define video/still entry points; keep one composition per deliverable variant. |
| Timing & animation | `useCurrentFrame`, `useVideoConfig`, `interpolate`, `spring`, `Easing`, `Sequence`, `Series`, `Loop` | Deterministic frame-based motion. Drive everything from frame/time, not wall clock. |
| Layout & styling | React/CSS, `AbsoluteFill`, `Img`, inline styles | Build layouts as components; keep Arabic RTL rules in text containers. |
| Text & fonts | `@remotion/google-fonts`, `@remotion/fonts`, `@font-face`, `staticFile` | Load Arabic-safe fonts; test shaping. Avoid letter-splitting Arabic text. |
| Media | `<Video>`, `<Audio>`, `<Img>`, `<OffthreadVideo>`, `staticFile`, `getAudioDurationInFrames` | Sync footage/audio; prefer `OffthreadVideo` for heavy decode; keep assets in project/public. |
| Captions/subtitles | `@remotion/captions`, caption components, word timings | Use Khaam narration timings for Arabic; do not assume English-only Whisper. See `templates/remotion/tiktok-captions/`. |
| Metadata & props | `calculateMetadata`, Zod schema (`zod`, `@remotion/zod-types`) | Data-driven durations, dimensions, and input props. Validate inputs. |
| 3D | `@remotion/three`, `three`, `@react-three/fiber`, `@react-three/drei` (as needed) | 3D scenes only when brief needs it; deterministic camera/lighting; test Arabic text as textures/overlays. |
| Transitions/effects | `@remotion/transitions` (if used), custom interpolations, Code Hike patterns | Use sparingly; keep readability and motion discipline. |
| Charts/data viz | React components + D3/vis libs as needed | Data-driven explainers; verify licences of added libs. |
| Audio visualization | frame/audio data utilities, custom canvas/SVG | Only when it serves the story; keep mix discipline. |
| Rendering | `npx remotion render`, `npx remotion still`, `@remotion/renderer`, `bundle` | Preview stills first, then short render, then final. Render from video project folder. |
| Server/cloud rendering | `@remotion/lambda`, `@remotion/cloudrun` (separate setup/cost) | Only with explicit user consent, account setup, and cost awareness. Not default. |
| Player/embed | `@remotion/player` | Useful for app previews; separate from MP4 delivery workflow. |
| Studio/dev | `npx remotion studio`, `remotion.config.ts` | Local preview/dev; install deps in project, not globally. |

## Khaam-ready starter templates

Vendored for private use in `templates/remotion/` (see `NOTICE.md`): 21 starters covering overlay, code, captions, 3D, stills, audiograms, data-driven, Skia, app shells, desktop/Vercel/recorder workflows, and AI-assisted workflow patterns.

| Template | Capability showcased | Best for |
|---|---|---|
| `overlay/` | Spring/sequence animation, overlay card, alpha/export workflow | Lower-thirds, callouts, editor overlays |
| `code-hike/` | Code Hike transitions, snippet metadata, annotations, themes | Dev explainers, code-before/after reels |
| `tiktok-captions/` | Word-timed caption pages, caption layout, audio-driven short-form | Captioned reels/shorts; Arabic via Khaam timings |
| `blank/` | Minimal Remotion composition | Clean starting point |
| `helloworld/` | Basic composition/spring/sequence | Learning, simple branded motion |
| `still/` | Remotion Still/image render | Covers, thumbnails, posters |
| `three/` | @remotion/three + React Three Fiber | 3D product/logo/camera scenes |
| `audiogram/` | Waveform + captions/audio-led layout | Podcast clips, quote videos |
| `music-visualization/` | Audio-reactive visuals | Music viz only when explicitly requested |
| `render-server/` | Programmatic render server/API | API/service render workflows (consent+security) |
| `skia/` | @remotion/skia 2D graphics | Vector/Skia visual effects |
| `prompt-to-motion-graphics/` | AI-assisted MG workflow pattern | Reference for prompt->MG pipelines (review keys/costs) |
| `prompt-to-video/` | AI-assisted video workflow pattern | Reference for prompt->video pipelines (review keys/costs) |
| `react-router/` | Remotion + React Router app | Web app embedding Remotion |
| `next-app-tailwind/` | Remotion + Next.js + Tailwind | Dashboard/preview app with Remotion |
| `stargazer/` | Data-driven recap template | Data-driven celebration/recap videos |
| `vibe-code/` | Stylized promo/code visuals | Stylized promo visuals; adapt to Khaam taste |
| `electron/` | Remotion + Electron app | Desktop Remotion tool/app workflows |
| `element-library/` | Reusable element/component library | Reusable branded motion components |
| `vercel/` | Remotion + Vercel deployment pattern | Vercel deployment/render workflows (consent/cost) |
| `recorder/` | Recorder app workflow (demo media omitted) | Recording/studio workflow reference |

Use `python scripts/use_remotion_template.py --list` and copy a starter into a video project.

## Khaam integration rules

1. **Project-local install.** `npm install` inside the copied video project, never globally. Pin versions.
2. **Deterministic frames.** No `Date.now()`, random without seed, or wall-clock animation for rendered output.
3. **Arabic-safe text.** RTL direction, whole words, Arabic fonts, no broken shaping. Code/URLs/numbers keep their correct direction.
4. **Preview ladder.** Still -> short clip -> final render. Check memory for long 3D jobs.
5. **Sound discipline.** Follow `reference/film-sound.md` / `reference/sound-library.md`; Remotion can compose audio, but Khaam sound rules still apply.
6. **License/provenance.** Record Remotion version, template source, third-party libs, fonts, and media licences in the video manifest.
7. **No secrets in code.** Do not bake API keys into templates or client bundles.

## Useful official template directions (beyond the three vendored)

When a job needs them, look up the official Remotion template/gallery for the installed version. Evaluate license and adapt to Khaam. Common patterns:
- **Audiogram/podcast clip** — waveform + captions + cover art.
- **Music visualization** — frequency/reactive visuals (careful with rights/music defaults).
- **Subtitles/captions** — SRT/caption-driven renders.
- **3D product/scene** — R3F + Three.js.
- **Data dashboard/video** — charts/maps driven by JSON/CSV.
- **Slideshow/promo** — image/video sequences with transitions.
- **Render server/Lambda** — programmatic rendering at scale (cost/credentials/consent).

Use these as pattern references; only fetch/copy code with license review and user consent.

## Local upstream docs/examples/package refs

- `reference/remotion-docs/` — MDX docs snapshot (1372 files) for API/capability lookup.
- `reference/remotion-examples/` — curated code-only examples from `packages/example` (461 files) showing practical patterns.
- `reference/remotion-package-refs/` — selected package README/package.json/license snapshots for key Remotion packages.

All are private-use snapshots; check each `NOTICE.md` for provenance and Remotion License.
