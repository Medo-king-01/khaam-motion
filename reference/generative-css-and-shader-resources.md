# Generative CSS & Shader Resources (private-use integration + external references)

Resources for generative visual art in Khaam Motion: CSS-doodle for CSS/grid generative patterns, and The Book of Shaders as an external learning reference for GLSL/shader concepts.

## Snapshot index

| Repo | Integration dir | License | Upstream commit | Snapshot scope | Notes |
|---|---|---|---|---|---|
| [css-doodle/css-doodle](https://github.com/css-doodle/css-doodle) | `integrations/css-doodle/` | MIT | `111e783dc0f054ffb1acd3154c9c5190f8f7eb6b` | Full repo snapshot (excluding `.git`, `node_modules`) | Web component + DSL for generative CSS/grid visuals. |

## External reference (not vendored)

| Repo | License/status | Why not vendored | Safe integrative use |
|---|---|---|---|
| [patriciogonzalezvivo/thebookofshaders](https://github.com/patriciogonzalezvivo/thebookofshaders) | **All rights reserved / Other (NOASSERTION)**. Upstream LICENSE states: cannot host, display, distribute or share the Work in any form; cannot use in any commercial or non-commercial product, website or project; educational linking/screenshot allowed under stated conditions. | Vendoring/copying into this repo would violate the upstream license terms. | Use as **external learning reference only**: open the upstream site/repo to study shader concepts (shaping functions, noise, patterns, color, image operations), then implement **original** GLSL/WebGL shaders in Khaam projects. Link to upstream with attribution; do not copy book text/code/assets into the repo. |

## How to use in Khaam

### css-doodle
- **Best for:** generative backgrounds, abstract pattern fields, decorative grids, textured motion behind titles/UI/explainers.
- **Pipeline fit:** web/HTML/Remotion capture workflows where a `<css-doodle>` component can be rendered deterministically.
- **Determinism:** pin seeds/params and capture by frame/time when used in video export.
- **Design rule:** keep patterns supportive; Arabic typography and message clarity come first.

### The Book of Shaders (external only)
- **Best for:** learning/refreshing GLSL fragment-shader fundamentals before writing original shaders for Three.js/WebGL/Motion Canvas/HTML canvas pipelines.
- **Safe workflow:** study concept upstream → write original shader implementation in project → test deterministically → document your own implementation/provenance.
- **Do not:** copy book chapters, examples, images, or code into this repo.

## Cautions

- **css-doodle (MIT):** preserve LICENSE and provenance.
- **The Book of Shaders:** strict all-rights-reserved license; no hosting/distribution/sharing/copying into repo or product. Treat as external reference only.
- For all generative visuals: verify render performance and determinism before final export; keep Khaam Arabic typography, pace, sound, and QA rules.

## Provenance

- css-doodle snapshot cloned 2026-11-23, commit `111e783dc0f054ffb1acd3154c9c5190f8f7eb6b`, copied excluding `.git`/`node_modules`.
- thebookofshaders inspected 2026-11-23, commit `5a537e76d7367dbbcda537723394b5dc03114449`; **not vendored** due to license restrictions.
