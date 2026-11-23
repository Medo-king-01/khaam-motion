# Remotion templates (vendored starters)

Ready-to-copy Remotion starters integrated into Khaam Motion for personal/private project use. They complement Khaam's default HyperFrames engine; use them when the job actually needs Remotion.

> **License:** These are third-party Remotion templates/snapshots. Remotion License applies (free for individuals/non-profits/companies <=3 employees; company 4+ needs a Company License). See `NOTICE.md`.

## Included templates (21)

| Template | What it gives | Best for |
|---|---|---|
| `overlay/` | Animated overlay card/lower-third | Overlays, callouts, name plates |
| `code-hike/` | Code snippet animations with Code Hike | Dev explainers, code walkthroughs |
| `tiktok-captions/` | Word-by-word captions (TikTok/Reels style) | Short-form captioned videos |
| `blank/` | Minimal blank starter | Starting from scratch |
| `helloworld/` | Basic Hello World composition | Learning/basic motion |
| `still/` | Still/thumbnail rendering | Covers, thumbnails, posters |
| `three/` | @remotion/three + R3F 3D starter | 3D scenes, product/logo 3D |
| `audiogram/` | Audiogram/waveform + captions | Podcast/audio-led clips |
| `music-visualization/` | Audio-reactive visuals | Music visualizations (only when requested) |
| `render-server/` | Programmatic render server pattern | API/service rendering workflows |
| `skia/` | @remotion/skia graphics | 2D vector/Skia effects |
| `prompt-to-motion-graphics/` | Prompt-to-motion-graphics workflow | AI-assisted MG workflow reference |
| `prompt-to-video/` | Prompt-to-video workflow | AI-assisted video workflow reference |
| `react-router/` | Remotion + React Router app | Web app embedding Remotion |
| `next-app-tailwind/` | Remotion + Next.js + Tailwind | Web app/dashboard embedding Remotion |
| `stargazer/` | Data-driven Stargazer recap | Data-driven recap videos |
| `vibe-code/` | Vibe-code visual style | Stylized promo/code visuals |
| `electron/` | Remotion + Electron desktop app | Desktop Remotion tools/apps |
| `element-library/` | Reusable Remotion element library | Reusable branded motion components |
| `vercel/` | Remotion + Vercel template | Vercel deployment/render patterns |
| `recorder/` | Remotion Recorder app template | Recording/studio workflow reference (demo media omitted) |

## Quick use

```bash
python3 scripts/use_remotion_template.py --list
python3 scripts/use_remotion_template.py three ./my-video/remotion
cd ./my-video/remotion && npm install && npm run dev
```

## Khaam rules

- HyperFrames remains the default engine; use Remotion when the job needs it.
- Follow `reference/arabic-typography.md` for Arabic text.
- Follow `reference/remotion.md` / `reference/remotion-capabilities.md` for render and capability guidance.
- Keep installs inside the copied video project, not global.
