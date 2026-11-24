# Upstream permission — Alansari.Tech Motion Library

Recorded 2026-11-24.

**Upstream:** https://github.com/alansariteach/motion-library  
**Snapshot commit:** `a280b36f5ecacceac8b58cd6af72ea29d7e3db12`

## Permission (relayed by the skill owner, in Arabic, verbatim)

> لا أعترض على نسخ ملفات الذكاء lib/ داخل مهارة موشن خام للاستخدام الخاص.

So: **`lib/` is cleared for copying into the private Khaam Motion skill.** The permission explicitly covers `lib/`; it does not explicitly mention `sfx/` or `lut/`.

## Additional folders taken, and their basis

| Folder | Basis for copying | Status |
|---|---|---|
| `sfx/` | Upstream `sfx/CREDITS.md` states all sounds are **CC0 1.0** (public domain), redistributed voluntarily with credits. Khaam keeps them with their credits and uses them only as CC0 accents under sound v2. | Cleared (CC0) |
| `lut/` | No upstream licence found; the owner of the skill asked to take `lut/` under the same private-use intent as `lib/`. | **Not explicitly licensed.** Private internal use only, at the skill owner's explicit selection; recorded here honestly. Recommended follow-up: ask Ali Alansari to state `sfx/`/`lut/` rights in writing or add a LICENSE to his repository |
| `lib/` | The permission quoted above. | Cleared |

## Scope limits (apply to all of the above)

- Private use **inside this skill only**. Nothing here may leave the skill (no public release bundle, no website, no re-upload), and this note travels with the directory.
- The site, its live previews and its plugin remain the author's; the skill merely references them by URL.
- If the author adds a LICENSE file (or revises his permission), update this document and re-pin accordingly — see `KHAAM-INTEGRATION.md`.
- This document is the source of truth for lawfulness of this snapshot inside the skill; it is not a legal opinion. When in doubt, fall back to the external-reference-only route (`reference/alansari-motion-library.md` §limits) or install the author's official plugin instead of copying anything.
