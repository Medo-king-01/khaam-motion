# Tegaki Remotion example snapshot — provenance and use

**Upstream:** [gkurt/tegaki](https://github.com/gkurt/tegaki), release tag `tegaki@1.1.0`, commit `32654a4cfb0fa6a2873264cf693316acd59d1627` (published 2026-10-11).

`examples/remotion/` is copied unchanged from that commit as a read-only reference. The upstream MIT license is preserved as `UPSTREAM_LICENSE`; `FONTS-LICENSE.md` is retained for the font bundles. The example is English-first and its package manifest uses the upstream monorepo's `workspace:*` dependency, so it is not a standalone Khaam project. Do not run its soundtrack scripts or copy demo code into a delivered project without inspecting it and adapting the content, licenses, deterministic frame timing, Arabic text and Khaam sound rules.

The separate Khaam starter at `templates/remotion/tegaki/` is an original, small adapter that uses the published `tegaki@1.1.0` npm package and the upstream-controlled-frame pattern. It is not a copy of this upstream example. `UPSTREAM-MANIFEST.sha256` records hashes for the preserved source/license files (excluding this notice). See `reference/tegaki.md` for setup and acceptance checks.
