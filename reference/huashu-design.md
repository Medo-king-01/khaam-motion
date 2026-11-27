# Huashu Design ideas in Khaam Motion

Load this when directing an explainer, product/UI film, motion infographic, animated concept or visual style exploration. It adapts selected methods from the pinned Huashu Design source subset at `reference/huashu-design-upstream/` (MIT, commit `59065698ad63f87ea1532c126c87f488d4f93fd6`). It is **not** another skill, pipeline or renderer. Khaam's `SKILL.md`, project brief, approval gates, HyperFrames/Remotion rules and existing Arabic, pace, asset, sound and delivery guides stay authoritative.

## What transfers well

### Derive the look from the content

Before drawing a scene, answer briefly in its existing storyboard/design notes:

1. **Role:** hook, explanation, evidence/data, transition, UI demo, quote, or resolve?
2. **Viewing distance:** small phone, normal phone, or large screen—and what does that do to scale and information density?
3. **Temperature:** what should the audience feel, and what in the supplied material supports that feeling?
4. **Capacity:** what must be understood in this beat, how long does it take to read, and what can move to another beat?
5. **Distinctive motif:** what shape, object, comparison, or transformation belongs to this subject rather than to a generic template?

Use the answers to motivate composition, typography, palette, material and movement. They are fast design checks, not extra user gates or mandatory forms to fill for every shot. For narration-led work, align on-screen changes to approved word cues. Keep the original information and meaning intact.

### Explore styles as mechanisms, not presets

Huashu's 92-style catalogue is a strong reference library for visual mechanisms, not 92 Khaam templates. Start with the user's approved style, brand assets, content and references; consult a sample only to solve a specific visual problem. Borrow a mechanism (e.g. show a system as a transit map, make a data change reveal a human consequence, use one semantic accent to track the active subject), then rebuild its palette, type, Arabic layout, geometry and timing for this brief. Do not copy a sample's Chinese content, remote fonts, exact artwork, branded identity or entire look. See the original guide and seven overview sheets under `reference/huashu-design-upstream/`.

Selected original code samples (each has a same-named JPG preview beside it):

| Upstream source | Useful design question |
|---|---|
| `assets/style-specimens/info/02-explanation-graphics.html` | How can an explanation make relationships visible instead of stacking generic cards? |
| `assets/style-specimens/info/06-data-humanism.html` | How can a data point become a human-scale consequence without inventing evidence? |
| `assets/style-specimens/info/13-speculative-tech-diagram.html` | How can a conceptual system feel like a considered diagram rather than a dashboard? |
| `assets/style-specimens/info/16-topological-transit-map.html` | Can a complicated route or dependency become one legible, traceable path? |
| `assets/style-specimens/ppt/12-diagram-isotype.html`, `13-diagrammatic-minimalism.html` | Can repeated symbols or a minimal diagram explain scale and hierarchy? |
| `assets/style-specimens/ppt/14-narrative-sparkline.html` | Can a plotted change carry a beginning, turning point and result? |
| `assets/style-specimens/paradigm/03-time-has-shape.html` | Could time/state be represented spatially rather than by generic progress UI? |
| `assets/style-specimens/paradigm/04-one-semantic-color.html` | Can one meaning-bearing color track the active object/state through the scene? |

These examples are evidence of source approaches, not tested Khaam components. Their HTML may request Google Fonts and uses Chinese typography/content; adapt only after inspecting source. Never treat its screenshot as proof of Arabic shaping, frame determinism, audio or export quality.

### Give the motion a readable arc

Huashu's animation guide is useful for *why* and *how* a visual action communicates: anticipation → action → consequence, meaningful holds before/after a key reveal, clear easing intent, and continuity of a hero element across related scenes. Translate these into the current storyboard rather than importing its named five-stage arc or prescribed timings. A quiet hold, a sharp cut or restrained motion can be the right choice. Every movement must clarify hierarchy, state change, cause or attention; remove a flourish that explains nothing.

Use the current Khaam camera/scene kit and local GSAP core. Keep timelines seekable and deterministic; respect the chosen render engine, frame rate and aspect ratio. Do not copy instructions for Huashu's Stage/Sprite runtime, CSS transitions, camera zoom implementation or `assets/animations.jsx` into a HyperFrames/Remotion project. For camera and motion implementation, use the matching Khaam guide and existing component examples first.

### Critique the render, not only the plan

After an internal render, inspect the actual beginning, end, first second after scene changes, densest text, key state transitions, camera extremes and the full film. Ask:

- Can a new viewer say what changed and why?
- Is the intended subject the first/clearest read at the actual phone size?
- Does each text block have enough time and contrast to read?
- Are there dead or decorative elements, repeated layouts, accidental clipping, visual collisions, or a hero object that changes identity/proportion?
- Do transitions connect the outgoing and incoming states meaningfully?
- Does movement remain correct after cold start and backward/random frame seek?
- Are Arabic joins, RTL order, mixed-direction strings and the selected real font correct at full size?
- Does the complete rendered export match Khaam's audio brief and approved timing?

Log the concrete issue and fix in the existing project notes. Use existing Khaam render, pacing, Arabic, audio and export checks; do not install Huashu's lint, screenshot, review, branding or learning scripts. A contact sheet can flag composition issues but cannot certify motion, Arabic or sound.

## What deliberately does not transfer

- **No compulsory three-direction ceremony.** Khaam's current Gate A/B and storyboard selection govern. Make alternatives when the user asks, when choosing between materially different directions is useful, or when an existing Khaam gate calls for them; don't add approval loops to settled work.
- **No blanket defaults:** Huashu's universal three-candidate rule, fixed five-question form, mandatory brand-protocol files, scorecard, watermark, 60-fps export, SFX/BGM mix and “always add music” do not override Khaam. Follow the actual brief and Khaam's no-music-by-default / real-recording sound rules.
- **No borrowed runtime or downloads:** do not run Huashu setup, `design_lint.py`, `polish.py`, `fetch_images.py`, `gen_image.py`, app/PPTX exporters or other upstream scripts; do not install its React/Babel/vendor bundle; do not download its fonts/music/SFX or use its external image workflow. For scoped local comparisons/boards/memory, use the Khaam-owned helpers in `reference/visual-reference-tools.md`; all network acquisition still follows Khaam's permission and asset-provenance rules.
- **No cultural or typographic transfer by assumption:** its Chinese/East Asian palette and typography guidance is not Arabic guidance. Khaam's Arabic typography and font checks take precedence; adapt the compositional principle and test Arabic in the actual renderer.

## Source map and provenance

- Original catalogue and color reasoning: `reference/huashu-design-upstream/references/design-styles.md`.
- Original motion and camera: `animation-best-practices.md`, `camera-language.md`.
- Original direction and critique references: `directions.md`, `critique-guide.md`—read as source context only, not as Khaam workflow authority.
- Seven source style overview sheets: `assets/style-specimens/sheet-*.jpg`.
- Source boundary, exact commit and MIT license: `reference/huashu-design-upstream/SOURCE-NOTICE.md`, `LICENSE`, `UPSTREAM-MANIFEST.sha256`.
- Khaam remains authoritative: `reference/adaptive-direction.md`, `reference/verified-motion-workflow.md`, `reference/visual-design.md`, `reference/pace.md`, `reference/arabic-typography.md`, `reference/film-sound.md`, and `reference/hyperframes-registry.md`.
