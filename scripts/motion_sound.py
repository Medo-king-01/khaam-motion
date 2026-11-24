#!/usr/bin/env python3
"""Suggest REAL recordings from this skill's CC0 library for a motion ID from lib/INDEX.md.

Usage:
    python3 scripts/motion_sound.py M-012        # one motion -> JSON suggestion
    python3 scripts/motion_sound.py --check      # library integrity: candidates exist, IDs resolve

The Alansari Motion Library suggests an SX-xx effect per motion; this skill's sound v2
is stronger: real recordings of what is shown, 3-5 per video, a real bed of the place or
none, no music unless the user asks. This tool only suggests; the user auditions, and
`check_mix.py` has the final word.
"""
import sys, json, re, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'integrations' / 'alansari-motion-library' / 'lib' / 'INDEX.md'

REAL = {
    'TXT': ['chalk-writing.flac', 'pencil-strokes.flac', 'pen-underline.flac', 'pen-signature.flac', 'chalk-short.flac', 'chalk-stroke.flac'],
    'CAP': ['chalk-writing.flac', 'pencil-strokes.flac', 'pen-underline.flac', 'chalk-short.flac'],
    'EMP': ['chalk-writing.flac', 'pencil-strokes.flac', 'pen-underline.flac'],
    'TRN': ['page-flip.flac', 'card-flip.flac', 'card-deal.flac', 'cloth-rustle.flac', 'wings-fly-away.flac'],
    'CAM': ['cloth-rustle.flac', 'wings-fly-away.flac', 'car-pass-by.flac', 'footsteps-sand.flac'],
    'FX':  ['match-ignite-flare.flac', 'match-strike-and-light.flac', 'water-spill.flac', 'water-pour.flac'],
    'SOC': ['button-click.flac', 'card-deal.flac', 'card-flip.flac', 'cardboard-tap-1.flac'],
    'LGO': ['match-ignite-flare.flac', 'card-flip.flac', 'page-flip.flac', 'wrapping-paper.flac'],
    'PER': ['footsteps-sand.flac', 'cloth-rustle.flac', 'sit-on-bed.flac', 'door-creak.flac'],
    'AUD': [],
    'SCR': ['button-click.flac', 'cardboard-tap-1.flac', 'cardboard-tap-2.flac', 'cardboard-lid.flac'],
    'TRK': ['footsteps-sand.flac', 'cloth-rustle.flac'],
    'D3':  ['wings-fly-away.flac', 'cloth-rustle.flac', 'card-flip.flac'],
    'TIM': ['rooster-crow.flac', 'amb-dawn-birds.flac', 'amb-night-crickets.flac', 'amb-night-far-dog.flac'],
    'FONTS': [], 'PALETTES': [], 'CAPSTYLES': [], 'ELEMENTS': [], 'RECIPES': [],
    'HOOKS': [], 'LUTS': [], 'BACKGROUNDS': [], 'SOUNDS': [],
}
DESIGN = {'FONTS', 'PALETTES', 'CAPSTYLES', 'ELEMENTS', 'RECIPES', 'HOOKS', 'LUTS', 'BACKGROUNDS', 'SOUNDS'}
NOT_MOTION_NOTE = 'not a motion family; choose motions from the M-xxx families instead'
SILENCE_NOTE = ('no recording maps well: the voice IS the audio. No bed, no accents; '
                'keep digital silence unless the place itself is real and quiet')
SOUND_V2 = ('sound v2: only real recordings of what is shown, 3-5 across the video, a real bed of the '
            'place or digital silence, no music unless the user asks; audition before delivery, '
            'then check_mix.py')
TOKEN = re.compile(r'([A-Z]{1,4})-(\d{1,4})(?:\.\.(?:[A-Z]{1,4}-)?(\d{1,4}))?')


def fmt_id(fam, n):
    return '%s-%0*d' % (fam, 3 if fam == 'M' else 2, n)


def parse_index(text):
    """Map 'M-012' -> 'CAP' from lib/INDEX.md. Handles 'M-001..M-005' ranges and singles."""
    mapping = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.split('|')]
        if len(cells) < 4:
            continue
        ids_cell, category = cells[1], cells[2]
        if not re.fullmatch(r'[A-Z][A-Z0-9]*', category or ''):
            continue
        for fam, a, b in TOKEN.findall(ids_cell):
            start = int(a)
            end = int(b) if b else start
            if start > end:
                start, end = end, start
            for n in range(start, end + 1):
                mapping[fmt_id(fam, n)] = category
    return mapping


def normalize_id(raw):
    m = re.fullmatch(r'([A-Za-z]{1,4})-(\d{1,4})', raw or '')
    if not m:
        return None
    return fmt_id(m.group(1).upper(), int(m.group(2)))


def suggest(motion):
    key = normalize_id(motion)
    mapping = parse_index(INDEX.read_text(encoding='utf-8'))
    category = mapping.get(key) if key else None
    if not category:
        return None
    candidates = ['sounds/library/' + name for name in REAL.get(category, [])]
    if category in DESIGN:
        note = NOT_MOTION_NOTE
    elif category == 'AUD':
        note = SILENCE_NOTE
    else:
        note = SOUND_V2
    lib = INDEX.parent / (('en' if category in DESIGN else 'ar')) / (category + '.md')
    return {
        'motion': key,
        'category': category,
        'category_file': str(lib.relative_to(ROOT)) if lib.is_file() else None,
        'real_candidates': candidates,
        'upstream_hint': 'see the «الصوت المقترح» line for this motion in lib/ar/%s.md — hint only, never automatic' % category if category not in DESIGN else 'design-side list; no sound applies',
        'note': note,
    }


def check():
    problems = []
    text = INDEX.read_text(encoding='utf-8')
    mapping = parse_index(text)
    motions = {k: v for k, v in mapping.items() if k.startswith('M-')}
    if len(motions) < 1000:
        problems.append('only %d unique motion IDs parsed from INDEX.md (expected 1000)' % len(motions))
    missing_cats = sorted({v for v in mapping.values()} - set(REAL))
    if missing_cats:
        problems.append('categories without a REAL mapping: %s' % ', '.join(missing_cats))
    for cat, names in REAL.items():
        for name in names:
            if not (ROOT / 'sounds' / 'library' / name).is_file():
                problems.append('missing real recording: sounds/library/%s' % name)
    missing_libs = sorted({v for k, v in motions.items()} -
                          {p.stem for p in (INDEX.parent / 'ar').glob('*.md')})
    if missing_libs:
        problems.append('category file missing for: %s' % ', '.join(missing_libs))
    return problems


def main():
    args = sys.argv[1:]
    if args == ['--check']:
        problems = check()
        print(json.dumps({'ok': not problems, 'problems': problems}, indent=2, ensure_ascii=False))
        return 0 if not problems else 1
    if len(args) != 1 or not normalize_id(args[0]):
        print('usage: motion_sound.py M-012 | --check', file=sys.stderr)
        return 2
    out = suggest(args[0])
    if out is None:
        print('unknown ID %r — check lib/INDEX.md' % args[0], file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
