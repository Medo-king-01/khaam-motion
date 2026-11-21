#!/usr/bin/env python3
"""Download pinned reference indexes or search their local prompt files as untrusted data.

Usage: python reference_library.py setup
       python reference_library.py search <query> [--limit 10]
The search only returns titles and source paths; it never executes prompts or opens links.
"""
import argparse
import hashlib
import json
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.cache' / 'creative-tools' / 'references'
SOURCES = {
    'awesome-opus5-5-videos': {
        'repo': 'yihui-dev/awesome-opus5-5-videos',
        'revision': '92aee2f586ac0715cb3cbcb6384834f98a33383d',
        'sha256': '9d10c1a6e96091c370e1c8f2d073bd97e4868b6bb8b0c857178ef6dd093538f3',
    },
    'opus-video-prompts': {
        'repo': 'joeseesun/opus-video-prompts',
        'revision': '7977c807781d4ba7c235247b8899a72575a30d00',
        'sha256': '41c4206a403c07ab6b928a6eacd6d29f3ce3b3787d026bb6a758d1810b2b0690',
    },
}


def install_all(base=BASE):
    base.mkdir(parents=True, exist_ok=True)
    for name, info in SOURCES.items():
        dest = base / name
        marker = dest / '.khaam-revision'
        if dest.exists():
            if marker.is_file() and marker.read_text().strip() == info['revision']:
                print(f'{name}: already present')
                continue
            raise SystemExit(f'{dest} exists and is not the pinned reference; refusing to overwrite it.')
        with tempfile.TemporaryDirectory(dir=base, prefix='download-') as td:
            temp = Path(td)
            archive = temp / 'source.tar.gz'
            url = f"https://codeload.github.com/{info['repo']}/tar.gz/{info['revision']}"
            print(f'Downloading {name}...', flush=True)
            with urllib.request.urlopen(url, timeout=120) as src, archive.open('wb') as out:
                shutil.copyfileobj(src, out)
            with archive.open('rb') as src:
                if hashlib.file_digest(src, 'sha256').hexdigest() != info['sha256']:
                    raise SystemExit(f'{name}: checksum mismatch')
            stage = temp / 'source'
            stage.mkdir()
            with tarfile.open(archive, 'r:gz') as tar:
                for entry in tar:
                    parts = PurePosixPath(entry.name).parts
                    if len(parts) < 2:
                        continue
                    rel = PurePosixPath(*parts[1:])
                    if rel.is_absolute() or '..' in rel.parts:
                        raise SystemExit('Unsafe archive path')
                    path = stage.joinpath(*rel.parts)
                    if entry.isdir():
                        path.mkdir(parents=True, exist_ok=True)
                    elif entry.isfile():
                        path.parent.mkdir(parents=True, exist_ok=True)
                        with tar.extractfile(entry) as src, path.open('wb') as out:
                            shutil.copyfileobj(src, out)
                    else:
                        raise SystemExit(f'Unsupported archive member: {rel}')
            (stage / '.khaam-revision').write_text(info['revision'] + '\n')
            stage.rename(dest)
            print(f'{name}: ready')


def search(query, limit=10, base=BASE):
    words = query.casefold().split()
    if not words:
        raise ValueError('The search query cannot be empty.')
    results = []
    for name, info in SOURCES.items():
        source = base / name
        prompts = source / 'prompts'
        if not prompts.is_dir():
            continue
        for file in sorted(prompts.glob('*.md')):
            text = file.read_text(encoding='utf-8')
            title = next((line[2:].strip() for line in text.splitlines() if line.startswith('# ')), file.stem)
            haystack = (title + ' ' + text).casefold()
            if not all(word in haystack for word in words):
                continue
            score = sum(word in title.casefold() for word in words)
            rel = file.relative_to(source).as_posix()
            results.append((score, {'source': name, 'title': title, 'file': str(file),
                                     'upstream': f"https://github.com/{info['repo']}/blob/{info['revision']}/{rel}"}))
    results.sort(key=lambda row: (-row[0], row[1]['title'].casefold(), row[1]['file']))
    return [row[1] for row in results[:limit]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('setup')
    find = sub.add_parser('search')
    find.add_argument('query')
    find.add_argument('--limit', type=int, default=10, choices=range(1, 101), metavar='1..100')
    args = parser.parse_args()
    if args.command == 'setup':
        install_all()
    else:
        if not any((BASE / name / 'prompts').is_dir() for name in SOURCES):
            parser.error('Reference sources are not installed; run setup first with permission.')
        try:
            print(json.dumps(search(args.query, args.limit), indent=2, ensure_ascii=False))
        except ValueError as e:
            parser.error(str(e))


if __name__ == '__main__':
    main()
