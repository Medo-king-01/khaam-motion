# Adaptive direction and review

Practical additions inspired by the user-provided Andrew Rayne Motion documents, rewritten for this project's workflow. These are creative guidance, not a new renderer or a claim that a video was produced. The user's explicit brief, host permissions, `SKILL.md` and the Arabic and sound rules take precedence. Load this guide when analysing references, planning shots, building product/UI motion or reviewing a render; keep the existing plan, storyboard and preview gates rather than creating new approval rounds.

## 1. Learn from the material actually available

- For each reference, note what was **actually inspected** (image, video, audio, page text or just a link). For video you can access and inspect, note useful time ranges and observations about staging, transitions, typography or sound. A still image cannot establish motion or sound. If a URL or playback is unavailable, say so; ask for the file or a description rather than inventing details.
- Turn each observation into a reusable principle and a new choice for this specific brief. Separate confirmed user preferences from your proposals, and ask when it is unclear what they liked. References are for study, not a blanket permission to reuse other people's media, marks, prompts, typefaces or music.
- If the current workspace includes a draft style (for example `.khaam/styles/*.md`), use it as an initial draft of the user's preferences, not a locked decision. Treat any provided palette, marks and references as inputs only; verify the font and design direction with the user before treating them as approved.

## 2. Make shots communicate

- Fit the storyboard into the existing `plan/storyboard.md`. For each shot record its time and purpose, the initial and final states, main action, foreground/background relationship, words and reading time, motivated camera/framing, entry and exit, sound cue or silence, and the main risk to test. For narration, align events to the approved voice timings.
- Give actions a causal chain: show the change and its consequence, not just an unrelated succession of effects. Compare different visual approaches where this will improve a difficult decision; don't generate 3–5 choices for every shot by default or turn the work into extra approval gates.
- Make transitions coherent with the content on **both** sides. A match cut needs aligned composition and motion; a reveal should actually expose the next material. Consider a deliberately still frame or hold when it improves meaning or readability. Apply the project's pace checks while noting justified exceptions, rather than creating motion for its own sake.
- Before a costly full build, make a short internal test of the riskiest element (for example Arabic legibility, a cutout occlusion, a collision, or an effect). Record what was tested and reuse the result; it does not replace the user's selected storyboard/preview gates.

## 3. Product, camera and identity

- For a product/UI video, use the real product details and authorised assets. Do not invent product features or numbers. Define the before/after state for each interaction; place the cursor, action, interface response and any related sound on one timeline. Keep the same content and proportions if moving between flat, layered and 3D views. A rendered demo is not proof that the actual application works.
- Use depth, light, focus and camera motion to direct attention, not as mandatory decoration. Preserve the visible identity and readability of the important subject; use restrained motion blur, depth of field or postprocessing only when the host and visual tests support them. If motion is unnecessary, keep the shot still and explain any pace-check exception.
- For a recurring character or image, record the chosen reference and stable identity features; check identity, edges and occlusion in representative frames. An existing still does not prove a moving shot or an alpha channel exists. Avoid claiming real transparency until the file has actually been checked.
- **Arabic:** follow `reference/arabic-typography.md` and `reference/hyperframes.md`. Animate shaped whole words or lines, not isolated letters; keep RTL order, avoid Arabic tracking, and test actual fonts and mixed-direction text. The source's letter-animation suggestions do not override these rules.

## 4. Sound and export

- Follow the brief and `reference/film-sound.md`: no music unless requested; use appropriate real recordings or silence as agreed. A narrated film follows its approved voice; time effects to visible actions and word cues. Do not add sound to an explicitly silent video.
- Select aspect ratio, resolution and frame rate for the platform and brief; never impose landscape 1080p60 on every project. Keep audio, visual events and frame timestamps aligned. When encoding, explicitly map intended streams and verify the end rather than blindly shortening the video to the shorter stream.
- Render from reproducible timeline states. Check at least one chosen frame after a cold start and after a backwards/random seek; simulations need a deterministic reset, bake, or fixed-step replay rather than just a seed. A video of `N` frames at `fps` samples frames `0` through `N-1`; do not add the endpoint as an extra frame. Investigate mismatches instead of claiming determinism.

## 5. Internal review and honest delivery

- Treat the first render as a draft. Where tools permit, inspect key compositions and boundaries, then watch the complete decoded export and listen to its actual mix. Check message, timing, transitions, readable Arabic, image identity, sync, audio tails and required output properties. Fix meaningful defects and re-check affected boundaries and the whole result.
- A contact sheet supports visual inspection but cannot prove motion, audio quality or sync. File metadata can establish codec/duration but not artistic quality. If playback, listening, decoding or any other check is unavailable, mark precisely what remains unverified. Do not call a silent video narrated or scored, or describe an unwatched video as reviewed.
- Record significant observations and fixes in the existing project's `LOG.md` / `PROGRESS.md`; record agreed style changes in `TASTE.md`. Respect approved assets and versions and keep diagnostic files in the project's cache. Deliver the original editable source alongside the video when requested or useful.
