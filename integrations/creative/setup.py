#!/usr/bin/env python3
"""Restore the optional creative tools locally; downloads packages and the Lemo library.

Run only with the user's consent. No agent or Blender configuration is changed.
The browser, FFmpeg, Blender application and Blender add-on are not installed.
"""
import hashlib
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CACHE = ROOT / '.cache' / 'creative-tools'
LEMO = CACHE / 'lemo-opuscar'
REVISION = 'f9e204293930952b61ba921cd8944d05f121beee'
SHA256 = '772bc329cc32754574fba25f98c652ed0ccc0ec5807ab9db80e582458535d7b2'
URL = 'https://codeload.github.com/lemomo-ai/lemo-opuscar/tar.gz/' + REVISION
SHOTCRAFT = CACHE / 'video-shotcraft'
SHOTCRAFT_REVISION = '59f3e9b9e936ff2bce0e18446226d770a3f2f61f'
SHOTCRAFT_SHA256 = '4f3f7027dcba2d34418797668237cdd80d03fa332d867acef10bd4f196c2c7a5'
SHOTCRAFT_URL = 'https://codeload.github.com/Vincentwei1021/video-shotcraft/tar.gz/' + SHOTCRAFT_REVISION


def run(*args):
    print('+', ' '.join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), cwd=ROOT, check=True)


def venv_python(path):
    return path / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')


def install_lemo_source():
    marker = LEMO / '.khaam-revision'
    if LEMO.exists():
        if marker.is_file() and marker.read_text().strip() == REVISION:
            return
        raise SystemExit(f'{LEMO} already exists and is not the pinned installation; refusing to overwrite it.')
    with tempfile.TemporaryDirectory(dir=CACHE, prefix='lemo-download-') as tmp:
        tmp = Path(tmp)
        archive = tmp / 'source.tar.gz'
        print('Downloading Lemo-Opuscar source to a temporary local cache...', flush=True)
        with urllib.request.urlopen(URL, timeout=120) as src, archive.open('wb') as dest:
            shutil.copyfileobj(src, dest)
        with archive.open('rb') as src:
            digest = hashlib.file_digest(src, 'sha256').hexdigest()
        if digest != SHA256:
            raise SystemExit('Lemo source archive checksum mismatch; installation stopped.')
        staging = tmp / 'library'
        staging.mkdir()
        with tarfile.open(archive, 'r:gz') as tar:
            for member in tar:
                parts = PurePosixPath(member.name).parts
                if len(parts) < 2:
                    continue
                rel = PurePosixPath(*parts[1:])
                if rel.is_absolute() or '..' in rel.parts:
                    raise SystemExit('Unsafe archive path')
                p = rel.parts
                if p[0] in ('.github', 'styleboard') or p[:2] == ('docs', 'readme'):
                    continue
                if len(p) >= 3 and p[0] == 'styles' and (p[2] == 'demo' or p[2] == 'poster.jpg'):
                    continue
                dest = staging.joinpath(*p)
                if member.isdir():
                    dest.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    with tar.extractfile(member) as src, dest.open('wb') as out:
                        shutil.copyfileobj(src, out)
                else:
                    raise SystemExit(f'Unexpected link or special archive member: {rel}')
        (staging / '.khaam-revision').write_text(REVISION + '\n')
        staging.rename(LEMO)


def install_shotcraft_source():
    marker = SHOTCRAFT / '.khaam-revision'
    if SHOTCRAFT.exists():
        if marker.is_file() and marker.read_text().strip() == SHOTCRAFT_REVISION:
            return
        raise SystemExit(f'{SHOTCRAFT} exists and is not the pinned installation; refusing to overwrite it.')
    with tempfile.TemporaryDirectory(dir=CACHE, prefix='shotcraft-download-') as tmp:
        tmp = Path(tmp)
        archive = tmp / 'source.tar.gz'
        print('Downloading video-shotcraft source to a temporary local cache...', flush=True)
        with urllib.request.urlopen(SHOTCRAFT_URL, timeout=120) as src, archive.open('wb') as dest:
            shutil.copyfileobj(src, dest)
        with archive.open('rb') as src:
            if hashlib.file_digest(src, 'sha256').hexdigest() != SHOTCRAFT_SHA256:
                raise SystemExit('video-shotcraft source archive checksum mismatch; installation stopped.')
        staging = tmp / 'library'
        staging.mkdir()
        workbench_link = False
        with tarfile.open(archive, 'r:gz') as tar:
            for member in tar:
                parts = PurePosixPath(member.name).parts
                if len(parts) < 2:
                    continue
                rel = PurePosixPath(*parts[1:])
                if rel.is_absolute() or '..' in rel.parts:
                    raise SystemExit('Unsafe archive path')
                if rel.parts[0] == '.github':
                    continue
                dest = staging.joinpath(*rel.parts)
                if member.isdir():
                    dest.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    with tar.extractfile(member) as src, dest.open('wb') as out:
                        shutil.copyfileobj(src, out)
                elif member.issym() and rel.as_posix() == 'workbench/demosrc' and member.linkname == '../demos':
                    workbench_link = True
                else:
                    raise SystemExit(f'Unexpected link or special archive member: {rel}')
        if workbench_link:
            try:
                (staging / 'workbench' / 'demosrc').symlink_to('../demos', target_is_directory=True)
            except OSError:
                print('Could not create workbench/demosrc link; the workbench needs manual setup on this host.')
        (staging / '.khaam-revision').write_text(SHOTCRAFT_REVISION + '\n')
        staging.rename(SHOTCRAFT)


def main():
    if sys.version_info < (3, 11):
        raise SystemExit('Python 3.11+ is required.')
    if not shutil.which('npm'):
        raise SystemExit('Node 22+ and npm are required.')
    CACHE.mkdir(parents=True, exist_ok=True)
    # Node can use the system trust store in this environment without disabling TLS verification.
    ca = Path('/etc/ssl/certs/ca-certificates.crt')
    if ca.is_file() and not os.environ.get('NODE_EXTRA_CA_CERTS'):
        os.environ['NODE_EXTRA_CA_CERTS'] = str(ca)
    run('npm', 'ci', '--prefix', HERE, '--ignore-scripts', '--no-audit', '--no-fund')
    install_lemo_source()
    install_shotcraft_source()
    run(sys.executable, HERE / 'reference_library.py', 'setup')
    run('npm', 'ci', '--prefix', LEMO, '--ignore-scripts', '--no-audit', '--no-fund')
    for env, lock in ((LEMO / '.venv', HERE / 'requirements-lemo.lock'),
                      (CACHE / 'blender-env', HERE / 'requirements-blender.lock'),
                      (CACHE / 'audio-env', HERE / 'requirements-audio.lock')):
        if not venv_python(env).is_file():
            run(sys.executable, '-m', 'venv', env)
        run(venv_python(env), '-m', 'pip', 'install', '--disable-pip-version-check', '-r', lock)
    print('Installed local packages. Browser, FFmpeg, Blender, its add-on and MCP client connection remain separate.')


if __name__ == '__main__':
    main()
