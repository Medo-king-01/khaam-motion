# Remotion templates — NOTICE (private use)

These templates were vendored into this repository at the repository owner's request for **private/personal use inside this Khaam Motion project**. They are **not** original Khaam code.

## Upstream sources (pinned/snapshotted)

| Local folder | Upstream source | Revision | License signal |
|---|---|---|---|
| `overlay/` | https://github.com/remotion-dev/template-overlay | `39197f6535fb` | No LICENSE file upstream; package.json UNLICENSED; README points to Remotion License |
| `code-hike/` | https://github.com/remotion-dev/template-code-hike | `9e47d09cef59` | No LICENSE file upstream; package.json UNLICENSED; README points to Remotion License |
| `tiktok-captions/` | https://github.com/remotion-dev/template-tiktok | `f51c6c8c9904` | No LICENSE file upstream; package.json UNLICENSED; README points to Remotion License; theboldfont license included |
| `blank/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-blank | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `helloworld/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-helloworld | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `still/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-still | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `three/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-three | `0e4c50cc9326` | LICENSE.md preserved |
| `audiogram/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-audiogram | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `music-visualization/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-music-visualization | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `skia/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-skia | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `prompt-to-motion-graphics/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-prompt-to-motion-graphics | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `prompt-to-video/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-prompt-to-video | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `stargazer/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-stargazer | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `vibe-code/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-vibe-code | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `electron/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-electron | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `element-library/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-element-library | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |
| `recorder/` | https://github.com/remotion-dev/remotion/tree/0e4c50cc93265b92eaaa40892c86b19c9fc07a0f/packages/template-recorder | `0e4c50cc9326` | No LICENSE file in template dir; verify against Remotion repo terms |

## Remotion License

Remotion is distributed under the Remotion License: https://github.com/remotion-dev/remotion/blob/main/LICENSE.md

Summary (not legal advice): free for individuals, non-profits, and for-profit organizations with up to 3 employees; companies of 4+ employees need a Company License. **Before any redistribution, public sharing, client/commercial team use, or resale, review the Remotion License and obtain any required license.**

## Third-party components / notes

- `code-hike/` depends on `codehike` / `@code-hike/lighter` packages — check their licences before distribution.
- `tiktok-captions/public/theboldfont.ttf` includes `theboldfont-license.rtf` from upstream. Read it before using the font; for Arabic projects prefer Khaam Arabic fonts (`reference/arabic-fonts.md`).
- Large demo media files were intentionally skipped in some templates to control repo size (e.g. `three/demo.gif`, `audiogram/public/dialogue.wav`, `music-visualization/public/demo-song-cover.jpeg`, `tiktok-captions/public/sample-video.mp4`, several recorder demo media files). Add your own assets when using those templates.
- Some templates include their own `LICENSE`/`LICENSE.md`. Preserve them.

## Khaam adaptation

These copies are starting points. When using them in Khaam videos:
- Follow `reference/remotion.md`, `reference/remotion-templates.md`, and `reference/remotion-capabilities.md`.
- Apply Arabic rules from `reference/arabic-typography.md` (RTL rows, whole words, Arabic-safe fonts).
- Keep dependency installs inside the video project folder, not global.
- Record versions/licences in the video manifest/delivery notes.
