# Optional creative tools — local installation

These tools are optional and separate from the original skill. This folder records pinned dependencies and a restoration script; it does not bundle Lemo-Opuscar. Running setup downloads third-party packages, so run it only after the user's approval. The upstream licences remain in force; consult `reference/external-creative-tools.md` and the upstream licences before use, especially Lemo-Opuscar's restrictions on its docs and style prompts.

## Restore after environment reset

The environment excludes `node_modules` and `.cache` from persistent snapshots, so installed binaries and downloaded source may disappear even though this folder and its lockfiles remain. On an authorized machine with Python 3.11+, Node 22+ and network access to npm, PyPI and codeload.github.com:

```sh
python3 integrations/creative/setup.py
node integrations/creative/smoke.mjs
```

The script installs:

- Three.js 0.187.0 and PixelFX 0.3.1 at its pinned GitHub commit in `integrations/creative/node_modules` using `package-lock.json`.
- Lemo-Opuscar source at commit `f9e204293930952b61ba921cd8944d05f121beee` in `.cache/creative-tools/lemo-opuscar`, with its Node dependencies and a local `.venv` for the core Python requirements. Demo sources, posters and gallery files are omitted. It verifies the source archive SHA-256 before extraction.
- `mcp-for-blender` 2.3.1 and locked Python dependencies in `.cache/creative-tools/blender-env`.
- React 19.3.1, React Three Fiber 9.8.2, React Three Rapier 2.2.0 and React Postprocessing 3.2.2 plus postprocessing 6.39.6 in the same local `node_modules`.
- librosa 0.11.0 and locked Python dependencies in `.cache/creative-tools/audio-env`.
- video-shotcraft source at commit `59f3e9b9e936ff2bce0e18446226d770a3f2f61f` in `.cache/creative-tools/video-shotcraft`; its SHA-256 is verified. This does not register the skill with any agent or install its template/workbench dependencies.
- mg-styles-15 source at commit `46fd009ff0988be7ab1d9a64dfe14e501c6c2521` in `.cache/creative-tools/mg-styles-15`; its SHA-256 (TOFU, pinned in the script) is verified. Videos, the showcase site and its images, the HDRI/textures and the mgaudio synthesis toolkit are deliberately not extracted. See `reference/mg-styles-15.md` for what was extracted into this skill (the independent-jury method and the fifteen-style vocabulary) and the licence boundaries (MIT; fonts not included).
- Two pinned video prompt collections in `.cache/creative-tools/references/`. These are local reference files only; their original videos are not downloaded. Search and licensing guidance: `reference/video-prompt-libraries.md`. To restore only those collections: `python3 integrations/creative/reference_library.py setup`.

The cache is local/private and excluded from snapshots; the script refuses to overwrite an existing unrecognized Lemo directory. No agent configuration or Blender installation is changed. Use of installed package code is not a security audit. The lockfiles are reproducible version selections, not a guarantee against vulnerabilities or future upstream availability.

## Readiness limits

- The smoke test checks Three.js geometry, PixelFX update/draw, a Rapier gravity step and React postprocessing imports on the CPU. It does **not** check WebGL, React rendering in a browser, or video rendering.
- The audio environment can run `scripts/audio_tag.py <audio-file> --onsets` for approximate onset candidates; refine manually. The separate audio classification models are not installed.
- video-shotcraft is a downloaded source library, not a configured agent integration. Its template and workbench dependencies, Remotion rendering, page capture and video export have not been tested.
- mg-styles-15 is a downloaded source library, not a configured agent integration. No film was rendered or any of its scripts executed; the extracted value is the review method (`reference/review-jury.md`) and the distilled style vocabulary (`reference/mg-styles-15.md`), both rewritten in our words. Its mgaudio toolkit is excluded by design (our sound v2 forbids code-made sounds for anything on screen and music unless the user asks).
- Lemo's core Python and Node packages are present after setup, but its headless Chromium and FFmpeg are separate and not installed by this script. Voice and music tiers are also separate. No film render is claimed.
- The Blender MCP Python server was tested with a temporary stdio MCP client and listed its tools. Blender itself, its add-on, and an actual connection to Blender are **not** configured or tested. Do not expose its unauthenticated socket publicly. Use `BLENDER_MCP_SAFE_MODE=1` where appropriate; it does not eliminate risk. Consult upstream documentation and seek consent before changing client configuration or installing the add-on.
- On a remote agent environment, a local MCP server and the user's desktop Blender are separate machines; do not assume a connection exists.

Project files can import `three` and `pixelfx` from this folder's package scope, or install their pinned packages in the actual video project after approval. Do not create duplicated dependencies or copy restricted documents/assets into a distributable project without checking licence terms.
