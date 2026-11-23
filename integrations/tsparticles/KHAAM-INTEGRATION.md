# Khaam integration — tsParticles

**Upstream:** https://github.com/tsparticles/tsparticles  
**Snapshot commit:** `814efd3b661df2e0594168430926331ff753a0e6`  
**License:** MIT License  
**Vendored for:** private/personal use inside this Khaam Motion project (at owner's request).

## What it is
tsParticles is a highly customizable particles/confetti/fireworks/background effects ecosystem for the web, with framework integrations and many plugin packages in the full monorepo.

## Key capabilities
- Particle/confetti/fireworks/background visual effects.
- Config-driven particle systems with plugins/shapes/updaters/interactions (in full upstream).
- Web component/framework integrations in upstream ecosystem.

## What this snapshot includes / omits
- **Included:** `engine/`, `bundles/`, `utils/`, `interactions/`, `plugins/`, `shapes/`, `updaters/`, `effects/`, `paths/`, `presets/`, `cli/`, root config/docs files.
- **Omitted for size/low benefit:** `demo/` (≈324M), `palettes/` (≈38M, large color-data set), `wrappers/`, `websites/`, `templates/`, `markdown/`, `scripts/`.

## How to use in Khaam
- Use for particle background/effect references or web prototypes.
- For video rendering, make particle motion deterministic (frame/time-seeded), avoid interactive-only behavior in final export.
- Consider lighter alternatives (particles.js) for simple cases; tsParticles for richer configs.

## Notes
- Preserve MIT license. Verify any added plugin/package licences when pulling more from upstream.
