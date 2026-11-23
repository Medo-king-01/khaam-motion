#!/usr/bin/env python3
"""Fetch pinned Remotion template sources into the local cache (opt-in, with checksums).

These are third-party Remotion templates. They are NOT vendored into the skill source.
They are downloaded only when you run this script, into:
  .cache/creative-tools/remotion-templates/<template>/

Licensing: Remotion and its official templates are distributed under the Remotion
License (not a blanket permissive OSS license). Free for individuals, non-profits,
and companies with up to 3 employees; companies of 4+ need a Company License.
Review https://github.com/remotion-dev/remotion/blob/main/LICENSE.md before use.
Template package.json files may say UNLICENSED; treat the Remotion License as governing.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.cache' / 'creative-tools' / 'remotion-templates'

TEMPLATES = {
    'template-overlay': {
        'repo': 'remotion-dev/template-overlay',
        'revision': '39197f6535fb4878ea128cf61b3e57d41916e900',
        'sha256': '3c3f323dad93d7f20a53882123ef763f03169c2cfdc0b1a3d97627f845a31dac',
        'description': 'Overlay graphics for use in traditional video editing programs (Remotion).',
        'skip': {'.gitignore'},
        'skip_paths': set(),
    },
    'template-code-hike': {
        'repo': 'remotion-dev/template-code-hike',
        'revision': '9e47d09cef59154ac55824593f3441b0c59e5328',
        'sha256': 'ad942ef8908ec8e9efee69ea531e376a35a7e6529db476d8c3b07c84c296c1b0',
        'description': 'Beautiful animated code snippets with Code Hike + Remotion.',
        'skip': {'.gitignore'},
        'skip_paths': set(),
    },
    'template-tiktok': {
        'repo': 'remotion-dev/template-tiktok',
        'revision': 'f51c6c8c99048b08fdc48fe7a9e3a7ef46bf1cbd',
        'sha256': 'd958d6ff3d9d3504c29a9f5c75404b24c37d731cb1d1b206bc055ece55212915',
        'description': 'TikTok-style captions/subtitles with Remotion (Whisper.cpp captioning workflow).',
        'skip': {'.gitignore'},
        # Skip large demo media; keep code, font, and font license.
        'skip_paths': {'public/sample-video.mp4'},
    },
}


def fetch_one(name: str, spec: dict, *, force: bool = False) -> Path:
    dest_dir = CACHE / name
    marker = dest_dir / '.khaam-revision'
    if dest_dir.exists():
        if marker.is_file() and marker.read_text().strip() == spec['revision'] and not force:
            print(f'[ok] {name} already at pinned revision {spec["revision"][:12]}')
            return dest_dir
        if not force:
            raise SystemExit(
                f'{dest_dir} exists but is not the pinned installation. '
                'Re-run with --force to replace it.'
            )
        shutil.rmtree(dest_dir)

    url = f'https://codeload.github.com/{spec["repo"]}/tar.gz/{spec["revision"]}'
    CACHE.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=CACHE, prefix=f'{name}-dl-') as tmp:
        tmp_path = Path(tmp)
        archive = tmp_path / 'source.tar.gz'
        print(f'[dl] {spec["repo"]}@{spec["revision"][:12]}')
        with urllib.request.urlopen(url, timeout=180) as src, archive.open('wb') as out:
            shutil.copyfileobj(src, out)
        with archive.open('rb') as src:
            digest = hashlib.file_digest(src, 'sha256').hexdigest()
        if digest != spec['sha256']:
            raise SystemExit(
                f'Checksum mismatch for {name}: expected {spec["sha256"]}, got {digest}'
            )
        staging = tmp_path / 'staging'
        staging.mkdir()
        with tarfile.open(archive, 'r:gz') as tar:
            for member in tar:
                parts = PurePosixPath(member.name).parts
                if len(parts) < 2:
                    continue
                rel = PurePosixPath(*parts[1:])
                if rel.is_absolute() or '..' in rel.parts:
                    raise SystemExit(f'Unsafe archive path: {rel}')
                rel_posix = rel.as_posix()
                if rel.parts[0] in spec['skip'] or rel_posix in spec['skip_paths']:
                    continue
                target = staging.joinpath(*rel.parts)
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with tar.extractfile(member) as src, target.open('wb') as out:
                        shutil.copyfileobj(src, out)
                elif member.issym() or member.islnk():
                    raise SystemExit(f'Refusing link in archive: {rel}')
                else:
                    # skip special files
                    continue
        (staging / '.khaam-revision').write_text(spec['revision'] + '\n')
        (staging / '.khaam-source').write_text(
            f"repo={spec['repo']}\nrevision={spec['revision']}\nurl={url}\nsha256={spec['sha256']}\n"
        )
        staging.rename(dest_dir)
    print(f'[done] {name} -> {dest_dir}')
    return dest_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'templates', nargs='*',
        help=f'Templates to fetch (default: all). Choices: {", ".join(sorted(TEMPLATES))}'
    )
    parser.add_argument('--force', action='store_true', help='Replace existing non-matching installs.')
    parser.add_argument('--list', action='store_true', help='List available templates and exit.')
    args = parser.parse_args()

    if args.list:
        for name, spec in TEMPLATES.items():
            print(f'{name}\t{spec["repo"]}\t{spec["revision"][:12]}\t{spec["description"]}')
        return 0

    selected = args.templates or sorted(TEMPLATES.keys())
    unknown = [n for n in selected if n not in TEMPLATES]
    if unknown:
        parser.error(f'unknown template(s): {", ".join(unknown)}; choose from {", ".join(sorted(TEMPLATES))}')
    print('Remotion templates are third-party assets under the Remotion License.')
    print('Review: https://github.com/remotion-dev/remotion/blob/main/LICENSE.md')
    print()
    for name in selected:
        fetch_one(name, TEMPLATES[name], force=args.force)
    print()
    print(f'Cache: {CACHE}')
    print('These files are gitignored (.cache/). Inspect before using in a render.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
