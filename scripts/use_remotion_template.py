#!/usr/bin/env python3
"""Copy a vendored Remotion starter template into a target directory (private use).

Usage:
  python scripts/use_remotion_template.py --list
  python scripts/use_remotion_template.py overlay ./my-video/remotion
  python scripts/use_remotion_template.py tiktok-captions ./my-video/remotion --force
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'templates' / 'remotion'
TEMPLATES = {
    # Original vendored starters
    'overlay': 'Animated overlay/lower-third starter (Remotion).',
    'code-hike': 'Animated code snippet transitions (Code Hike + Remotion).',
    'tiktok-captions': 'TikTok/Reels-style word-by-word captions (Remotion).',
    # Additional Remotion monorepo templates (private-use snapshots)
    'blank': 'Minimal blank Remotion starter.',
    'helloworld': 'Basic Hello World Remotion starter.',
    'still': 'Static image/still thumbnail rendering with Remotion Still.',
    'three': '3D scene starter using @remotion/three + React Three Fiber.',
    'audiogram': 'Audiogram/podcast waveform + captions visualization.',
    'music-visualization': 'Music-reactive visualization starter.',
    'render-server': 'Server-side/programmatic Remotion rendering starter.',
    'skia': 'React Native Skia / @remotion/skia graphics starter.',
    'prompt-to-motion-graphics': 'Prompt-to-motion-graphics template (AI-assisted workflow pattern).',
    'prompt-to-video': 'Prompt-to-video template (AI-assisted workflow pattern).',
    'react-router': 'Remotion + React Router app template.',
    'next-app-tailwind': 'Remotion + Next.js + Tailwind app template.',
    'stargazer': 'GitHub Stargazer data-driven video template.',
    'vibe-code': 'Vibe-code style Remotion template.',
    'electron': 'Remotion + Electron desktop app template.',
    'element-library': 'Reusable Remotion element/component library template.',
    'vercel': 'Remotion + Vercel/Next rendering template.',
    'recorder': 'Remotion Recorder app template (local recording/studio workflow; large demo media omitted).',
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('template', nargs='?', help='Template name.')
    p.add_argument('dest', nargs='?', help='Destination directory to create/copy into.')
    p.add_argument('--list', action='store_true', help='List available templates.')
    p.add_argument('--force', action='store_true', help='Overwrite destination if it exists.')
    args = p.parse_args()

    if args.list or not args.template:
        for name, desc in TEMPLATES.items():
            loc = SRC / name
            status = 'ok' if loc.is_dir() else 'missing'
            print(f'{name}\t{status}\t{desc}\t{loc}')
        if not args.template:
            return 0

    if args.template not in TEMPLATES:
        p.error(f'unknown template {args.template!r}; choose from {", ".join(TEMPLATES)}')
    if not args.dest:
        p.error('destination directory is required')

    src = SRC / args.template
    if not src.is_dir():
        raise SystemExit(f'Template not found: {src}')
    dest = Path(args.dest).expanduser().resolve()
    if dest.exists():
        if not args.force:
            raise SystemExit(f'Destination exists: {dest} (use --force to overwrite)')
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    print(f'Copied {args.template} -> {dest}')
    print('Next: cd into the project, run `npm install`, then `npm run dev` (with consent).')
    print('Read KHAAM-INTEGRATION.md and templates/remotion/NOTICE.md for license/adaptation notes.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
