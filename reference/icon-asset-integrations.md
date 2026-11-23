# Icon / Asset Integrations (private-use snapshots)

Vendored icon/asset libraries for use inside Khaam Motion projects (private/personal use at owner's request). These are **static SVG asset sources**, not animation engines — animate them through Khaam's normal pipelines (Remotion, Motion Canvas, HTML/CSS/SVG, After Effects handoff assets, etc.).

## Snapshot index

| Repo | Integration dir | License | Upstream commit | Snapshot scope | Notes |
|---|---|---|---|---:|---|
| [simple-icons/simple-icons](https://github.com/simple-icons/simple-icons) | `integrations/simple-icons/` | CC0-1.0 | `c01109118e134e061c9bdf2e1a7f814117f1f032` | Full repo snapshot (excluding `.git`, `node_modules`) | 3475 brand SVG icons. Brand trademarks may still apply. |
| [lucide-icons/lucide](https://github.com/lucide-icons/lucide) | `integrations/lucide-icons/` | ISC (see LICENSE) | `c26ce5515667640ca2753e095ba319d225fc0d8d` | Full repo snapshot (excluding `.git`, `node_modules`) | 2104+ consistent UI icons; default general icon set. |
| [tabler/tabler-icons](https://github.com/tabler/tabler-icons) | `integrations/tabler-icons/` | MIT | `53635822b021190128f32b2c198dcf1b2b66a4c7` | Full repo snapshot (excluding `.git`, `node_modules`) | 6563 icons, outline+filled; broad fallback set. |

## How to choose

- **Brand/platform logo:** `simple-icons` first. Use neutral/accurate brand presentation; do not imply endorsement. Check trademark/context.
- **General UI/feature/step/concept icon:** `lucide-icons` first (consistent stroke style).
- **Missing symbol / need filled+outline variant / broader coverage:** `tabler-icons`.
- **Do not mix icon families randomly** in the same frame; pick one primary family and only mix intentionally.

## Khaam usage notes

- These are SVG assets: they can be recolored, stroked, masked, morphed, staggered, or path-animated in Remotion/Motion Canvas/HTML pipelines.
- Keep Arabic typography/layout rules separate from icon artwork; icons support the message, they don't replace clear Arabic text.
- For product/UI promo shots, combine with `reference/shotcraft.md` and keep icon motion purposeful (not decorative noise).
- For explainer/told videos, use icons as semantic anchors at the word/beat that carries the meaning (see `reference/pace.md`).
- Preserve upstream LICENSE/NOTICE files. Record source repo+commit when an asset is adapted into deliverables.

## Cautions

- **simple-icons (CC0):** artwork license is permissive, but third-party brand trademarks/names have their own rules.
- **lucide (ISC):** permissive; review upstream LICENSE for any brand-derived icon notes.
- **tabler (MIT):** permissive; keep copyright/license notice.

## Provenance

Snapshots were shallow-cloned from upstream on 2026-11-23 and copied into `integrations/` excluding `.git` and `node_modules`. See each `integrations/*/KHAAM-INTEGRATION.md` for details.
