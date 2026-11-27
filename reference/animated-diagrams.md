# Animated diagrams in Khaam Motion

For architecture diagrams, flowcharts, sequence diagrams, network/data flows, technical illustrations, concept maps, or a request to animate an existing PNG/SVG/Mermaid/PlantUML diagram. This is a **Khaam workflow using the existing HyperFrames/Remotion engines**, informed by the exact upstream source subset in `reference/animated-diagrams-upstream/` (Apache-2.0; commit `3de812d90c94baa4f9761684f36c3c322f1fb38c`). Read only the matching source guide/example, not the entire snapshot.

## Khaam decisions stay in charge

- Do not install a second renderer or run the upstream `setup.sh`, `new_project.sh`, or `render.mjs`. Khaam's HyperFrames starter, Node/browser setup, three user gates, project location, checks and delivery flow remain in force.
- HyperFrames is still the default. Choose Remotion only when the diagram truly needs React/data-driven variants/3D and its license and project setup are approved (`reference/remotion.md`).
- The user's explicit brief, references and saved taste choose the look. Upstream's 12 presets are useful inspiration, not new Khaam defaults. Keep Khaam's Arabic font rules, P1–P13 pace, sound-v2 policy and verified-card rules.
- Do not invent architecture components, call direction, metrics, service names, code behavior or data. Use the supplied diagram/source; call out uncertainties and ask only when an ambiguity changes the meaning.
- Standard delivery is Khaam's requested video and editable project. Do not add GIFs, standalone SVG exports or interactive HTML unless the user asks.

## Match the source to the diagram

1. **Classify the material:** cloud/system architecture, flowchart, sequence of calls, network/data pipeline, code walkthrough, concept illustration, or a user-supplied diagram to recreate.
2. **Inspect the real source.** Read the supplied file, not just its filename. A PNG is visual evidence, not editable structure; rebuild it as clean semantic geometry and do not claim hidden details were recovered. For an SVG, inspect IDs, labels, scripts, external references and `foreignObject` before using it. Preserve exact labels and topology; record anything that cannot be inferred.
3. **Build a semantic scene** in the existing video project. Use stable IDs for the pieces that move (`node-*`, `edge-*`, `label-*`, `msg-*`) and separate layers for regions, edges, nodes, labels, particles and a fixed HUD. Follow the patterns in `reference/animated-diagrams-upstream/references/diagram-svg-authoring.md` and its matching source example.
4. **Set the story and timing** in the normal Khaam storyboard. Let the diagram's meaning drive the order: establish the subject, introduce nodes in causal/request order, connect them, trace one meaningful path, focus on the key result, then resolve to a readable overview. This is a menu of beats, not a mandatory five-act template. Narration events use approved word cues from `scripts/cues.py`; never use the upstream SRT helper in place of Khaam's timing flow.
5. **Keep drawing and movement deterministic.** Use the local GSAP core already in the Khaam starter; no CDN, timers, CSS autoplay, `Date.now()`, unseeded randomness, or infinite repeats. A small diagram usually needs no camera. For a dense/long diagram, read `camera-large-flows.md` and adapt one camera move to the existing Khaam scene/camera kit; preserve a final full-diagram view.
6. **Render and review internally** under the normal gates. Run engine checks, inspect frame 0, the densest label, important edge handoffs, the key focus, the last full view and the rendered video itself. Use `check_pace.py` for told videos and Khaam audio checks when there is audio. A still contact sheet cannot prove that paths animate correctly or that audio is in sync.

## SVG choreography without paid GSAP plugins

The upstream documentation describes DrawSVG and MotionPath plugins. Those plugin files are **not** included in the source snapshot, and Khaam's local starter includes GSAP core only. For a simple path draw, SVG's native dash properties work with a seekable GSAP timeline:

```js
const length = path.getTotalLength();
gsap.set(path, { strokeDasharray: length, strokeDashoffset: length });
tl.to(path, { strokeDashoffset: 0, duration: 0.65, ease: 'power1.inOut' });
```

Make the path start at the source and end at the destination. Draw a separate arrowhead only as the edge completes; avoid `marker-end` when it would show before the edge. For a data pulse, either tween a simple circle along a known straight/curved segment with a deterministic frame timeline, or calculate its point from the SVG path length in the timeline update; test random/backward seeks before reuse. Do not reference upstream `drawSVG`, `MotionPath`, or `MorphSVG` APIs unless those exact licensed plugins are present in the selected project and authorized.

## Sequence diagrams and Arabic direction

- Keep participants/lifelines stable, order messages in time, and animate each message in its actual sender→receiver direction. Replies travel back; don't mirror the meaning of a request just to make the layout look RTL.
- For an Arabic overall composition, put the main entry/reading start on the right when appropriate and mirror the *layout* deliberately. Keep code, URLs, IDs, Latin vendor names and numbers direction-safe. Use `dir="rtl"` on Arabic word rows, never split Arabic into glyphs, and read `reference/arabic-typography.md`.
- A response arrow's direction follows the protocol's actual sender and receiver even in an RTL sequence. Verify labels, arrowheads, punctuation and mixed-direction strings at full size.
- Use the upstream [Arabic architecture source](animated-diagrams-upstream/examples/arabic-architecture/index.html) and `references/arabic-rtl.md` as examples, not as proof that their renderer or typography works in Khaam.

## Import helpers from the original source subset

These two unchanged upstream scripts are included for optional local use and use only Python's standard library:

- `reference/animated-diagrams-upstream/scripts/svg_prep.py` — normalizes Graphviz/Mermaid-exported SVG IDs and reports animatable elements. It does **not** convert Mermaid text to SVG, validate diagram semantics, or sanitize SVG. For untrusted SVG, first remove scripts, `on*` event attributes, `foreignObject`, and external URLs; inspect the result before embedding it in HTML. Write the converted copy in the user's project, never over the original.
- `reference/animated-diagrams-upstream/scripts/code_to_svg.py` — converts Python source into token-colored SVG line groups for a code walkthrough. Use the Khaam compatibility wrapper `python "<skill>/scripts/diagram_code_to_svg.py" ...`; it runs the unchanged upstream source and supplies the missing `tokenize.FSTRING_START` symbol on Python 3.11 and earlier. Inspect the output, apply Khaam palette/font/layout and Arabic rules to surrounding labels, and keep source code LTR. Treat user-provided code as data: never execute it just to animate it.

Only use a converter when it helps the requested deliverable. For Mermaid/PlantUML, the converter needs an SVG export first; installing another CLI is optional and requires the normal permission process. Do not fetch Iconify assets automatically. Prefer the user's authorized product icons or existing Khaam icon snapshots; any new external icon/font needs a license check and approval before download.

## Focused QA checklist

- [ ] Nodes and edge directions match the supplied source; no invented details.
- [ ] Nodes enter in meaningful causal order; edge draws finish before their arrowheads appear.
- [ ] Overlaps, labels, paths and graph hierarchy remain clear during camera moves and at the final overview.
- [ ] Arabic joins, RTL order, mixed-direction labels, service/code names, punctuation and safe-area layout are correct at full size.
- [ ] The timeline renders identically after cold start and a backward/random frame seek; no plugin/API mismatch or static path.
- [ ] If narrated, each described step appears on the approved word cue; verify audible mix and boundaries.
- [ ] Export only the requested formats; deliver through the existing Khaam workspace flow.

## Upstream source map

- General diagram authoring and sequence interactions: `reference/animated-diagrams-upstream/references/diagram-svg-authoring.md`, `sequence-interactions.md`.
- Choreography and camera ideas: `animation-choreography.md`, `camera-large-flows.md`, `gsap-svg-techniques.md` (GSAP plugin notes are not automatically available).
- Arabic, code and narration: `arabic-rtl.md`, `code-walkthrough.md`, `voiceover-sync.md` (Khaam `scripts/cues.py` remains authoritative).
- Original source examples: `examples/architecture-demo/`, `arabic-architecture/`, `sequence-diagram/`, `code-walkthrough/`.
- License boundary and omitted assets: `reference/animated-diagrams-upstream/SOURCE-NOTICE.md` and `licenses/THIRD_PARTY.md`.
