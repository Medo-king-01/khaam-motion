# Animated Diagrams source snapshot — provenance and boundaries

**Upstream:** [omkamal/animated-diagrams-skill](https://github.com/omkamal/animated-diagrams-skill), commit `3de812d90c94baa4f9761684f36c3c322f1fb38c` (reviewed 2026-11-27).

This directory preserves the upstream Apache-2.0 license, NOTICE, third-party license map, all upstream `references/*.md`, the two stdlib helpers `scripts/svg_prep.py` and `scripts/code_to_svg.py`, and source-only HTML/CSS for four examples (architecture, Arabic architecture, sequence diagram, Python code walkthrough). The source files are unchanged. `UPSTREAM-MANIFEST.sha256` checks the copied source and license files; this notice and the manifest itself are excluded from that list.

This is a **reference subset**, not a second installed skill or renderer. The project-specific Khaam adaptation is `reference/animated-diagrams.md`. Read the source helper code and output before running it on user input. `svg_prep.py` parses/re-writes SVG but is not a security sanitizer: remove scripts, event handlers, foreign objects and untrusted external links before embedding any external SVG. Keep all generated files in the user's video project, not this snapshot.

The full upstream repository also bundles fonts, Font Awesome icons, GSAP (including plugins) and rendered demos. Those assets are intentionally **not** copied here. Their separate licenses and terms are described in `licenses/THIRD_PARTY.md`; a reference to those assets is not permission to use them. Use Khaam's existing fonts, icon snapshots, renderer, setup and licensing workflow instead. Do not run the upstream `setup.sh` or `render.mjs` as the Khaam pipeline: its dependency versions and export defaults differ, and its assets/plugins are not included.
