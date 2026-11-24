# Khaam integration — recharts

**Upstream:** https://github.com/recharts/recharts  
**Snapshot commit:** `6a02fb6da47e419d4270947e6f6db41c734c5567`  
**License:** MIT License  
**Vendored for:** private/personal use inside this Khaam Motion project (at owner's request).

## What it is
Recharts is a charting library built with React and D3. It provides composable chart components for common data visualizations.

## Key capabilities
- Composable React chart components (line, bar, area, pie, radar, scatter, composed charts, etc.).
- Responsive containers, tooltips, legends, axes, grids, reference lines/areas.
- Useful for data-driven explainer videos, dashboards-as-video, KPI animations, and infographic motion.

## What this snapshot includes / omits
- **Included:** `src/`, root README/LICENSE/package/tsconfig/types/config files.
- **Omitted:** full git history, node_modules, tests/storybook/website/build artifacts not in sparse selection (repo is very large upstream).

## How to use in Khaam
- Use in React/Remotion projects by installing dependencies in the target project; this snapshot is source/reference.
- For video, render deterministic frames (no hover-dependent meaning). Animate data entry/progress by frame/time.
- Keep Arabic labels/numbers legible and RTL-aware; verify font, numeral style, and axis label layout.
- Prefer simple, readable charts; avoid dense dashboard clutter in short-form motion.

## Notes
- Preserve upstream LICENSE and provenance.
- Source snapshot, not installed in Khaam runtime.
- Apply Khaam rules for Arabic typography, sound discipline, pace, and QA.
