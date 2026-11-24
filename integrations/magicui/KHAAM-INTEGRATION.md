# Khaam integration — magicui

**Upstream:** https://github.com/magicuidesign/magicui  
**Snapshot commit:** `b0b2e4974b1b68cd5278277c6837a27736e20c3a`  
**License:** MIT License  
**Vendored for:** private/personal use inside this Khaam Motion project (at owner's request).

## What it is
Magic UI is a UI library for design engineers: animated React/Tailwind/shadcn-style components and effects that can be copied/adapted into apps.

## Key capabilities
- Registry of animated components/effects in `apps/www/registry/` (1.7M).
- Component/effect patterns for landing pages, promos, product UI, text effects, backgrounds, buttons, badges, device mocks, etc.
- Useful as source/reference for polished web motion components in Remotion/React/Next projects.

## What this snapshot includes / omits
- **Included:** root meta files, `registry.json`, `skills/`, and selected `apps/www/` files: `registry/`, `registry.json`, `components.json`, `lib/`, `hooks/`, `types/`, config/package files.
- **Omitted for size:** docs site app/content/public bulk (`apps/www/app`, `content`, `public`) and git history/node_modules.

## How to use in Khaam
- Treat as a **source/reference registry**: copy/adapt specific components into a target React/Remotion project and install its required deps (React, Tailwind, motion/framer-motion, shadcn utilities as needed).
- For video export, ensure animations are deterministic/frame-driven where possible; avoid scroll/hover-only effects.
- Adapt styling to Khaam taste and Arabic typography rules; do not let decorative UI effects overpower message.
- Check component dependencies before reuse.

## Notes
- Preserve upstream LICENSE and provenance.
- Source snapshot, not installed in Khaam runtime.
- Apply Khaam rules for Arabic typography, sound discipline, pace, and QA.
