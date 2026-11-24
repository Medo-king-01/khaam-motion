# GSAP — vendored inside this template

`gsap.min.js` in this folder is a byte-identical copy of the skill's vendored GSAP snapshot:

- Source in the skill: `integrations/gsap/dist/gsap.min.js`
- Upstream: https://github.com/greensock/GSAP
- Snapshot commit: `5e6c35ff8eedea12d4f229129def635277d8b0f2`
- Version: 3.15.1 (`integrations/gsap/package.json`)
- SHA-256: `3d1bea374ab1b703cc5c4105358eec63c4465efdc573931dc116e34a0a190c1b`
- License: **GSAP Standard License** — not MIT/Apache. See https://gsap.com/standard-license/
  and `integrations/gsap/KHAAM-INTEGRATION.md` for the usage boundaries recorded when it was vendored.

Why it is here: the Arabic HyperFrames starter must preview and render offline and must not
depend on a CDN's availability. This copy exists so the template uses the same GSAP the skill
owns locally — not a different build from the network.

Update policy: do not fetch a newer GSAP ad hoc. If the skill's snapshot is updated, re-copy the
file and refresh this notice (version, commit, SHA-256) in the same change.
