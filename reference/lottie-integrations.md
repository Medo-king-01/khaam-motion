# Lottie Integrations (private-use snapshots / references)

Lottie-related libraries and references for Khaam Motion. Lottie is useful for embedding After Effects-exported vector motion as JSON in web-based renders.

## Snapshot index

| Repo | Integration dir | License | Upstream commit | Snapshot scope | Notes |
|---|---|---|---|---|---|
| [airbnb/lottie-web](https://github.com/airbnb/lottie-web) | `integrations/lottie-web/` | MIT | `bede03d25d232826e0c9dca1733d542d8a7754fb` | Selective: `build/player/`, `player/`, `docs/`, `tasks/`, `projects/`, root metadata | Omitted `demo/`, `test/`, `gifs/`, `build/extension/`, `build/old_parser/` for size/value. |
| [LottieFiles/awesome-lottie](https://github.com/LottieFiles/awesome-lottie) | `integrations/awesome-lottie/` | **No clear license found** (no LICENSE file; GitHub API reported no license at 2026-11-23 inspection) | `bccdc5deeb1301950444a1f15b299c42958ff7ee` | Full repo snapshot (README-only list) | Vendored at owner's explicit request for private/personal use only; **do not redistribute** without clear permission/license. |

## How to use in Khaam

- **Web/Remotion/HTML capture:** embed `lottie-web` player build (`integrations/lottie-web/build/player/`) and control animation by frame/time for deterministic capture.
- **Renderer choice:** `svg` for crisp vector/UI, `canvas` for many elements/perf, `light` for smaller footprint when features allow. Test the chosen renderer in the actual output pipeline.
- **Arabic text caution:** avoid relying on AE/Lottie-rendered Arabic text for final typography; render Arabic in Khaam's controlled text pipeline and use Lottie for decorative/motion graphics.
- **Asset rights:** Lottie JSON animation files are separate assets with their own licenses/rights. Verify before using third-party Lottie files.

## Cautions

- `lottie-web` is MIT for the library code. Embedded animation assets may have different licenses.
- For deterministic video export, avoid real-time playback dependence; drive by frames/time.
- Large/complex Lottie files can hurt render performance; pretest before full render.

## Provenance

Snapshot cloned from upstream on 2026-11-23 and copied selectively into `integrations/lottie-web/`. See `integrations/lottie-web/KHAAM-INTEGRATION.md`.
