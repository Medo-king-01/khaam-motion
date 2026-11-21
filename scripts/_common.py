"""Shared helpers for the khaam-motion scripts (Windows, macOS, Linux; Python >= 3.9, stdlib only)."""
import os, shutil, subprocess, sys
from khaam_paths import executable, install_hint
for _s in (sys.stdout, sys.stderr):  # Windows consoles (cp1252) can't print ✅/❌ -> force UTF-8
    try: _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
KEYS = ['PIXABAY_API_KEY', 'FREESOUND_CLIENT_ID', 'FREESOUND_API_KEY', 'UNSPLASH_APPLICATION_ID', 'UNSPLASH_ACCESS_KEY',
        'UNSPLASH_SECRET_KEY', 'FIRECRAWL_API_KEY']  # ElevenLabs uses ~/.cache/khaam-motion/elevenlabs-key.txt (key_setup.py)
def load_env(path='.env'):
    """read NAME=value lines into a dict (values are never printed)"""
    env = {}
    if os.path.exists(path):
        for ln in open(path, encoding='utf-8-sig'):
            ln = ln.strip()
            if ln and not ln.startswith('#') and '=' in ln:
                k, v = ln.split('=', 1); env[k.strip()] = v.strip().strip('"').strip("'")
    return env
def which(*names):
    for n in names:
        p = shutil.which(n)
        if p: return p
    return None
def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)
# 1.7.1: the Python libraries the scripts use. A fresh Windows Python has none of them; the install step asks once for the
# missing ones (START-HERE step 6). A script that still finds one missing says so in one plain line, never a traceback.
PACKAGES = {'numpy': ('numpy', 'NumPy'), 'scipy': ('scipy', 'SciPy'), 'PIL': ('pillow', 'Pillow')}   # module: (pip name, said as)
def missing_packages(*mods):
    """Which of these modules this Python lacks (default: the three the skill uses), as (pip name, said as) pairs."""
    import importlib.util
    out = []
    for m in mods or tuple(PACKAGES):
        try: ok = importlib.util.find_spec(m) is not None
        except (ImportError, ValueError): ok = False
        if not ok: out.append(PACKAGES.get(m, (m, m)))
    return out
def packages_fix(miss):
    """The command that installs them into the Python running this script. On a Mac: the Mac route, never pip."""
    if sys.platform == 'darwin': return install_hint('')
    return '"%s" -m pip install %s' % (sys.executable, ' '.join(p for p, _ in miss))
def packages_line(tool, miss, why=''):
    """The one plain line: what is missing, the command that fixes it (after the user's yes), and the user's sentence."""
    said = ' and '.join(s for _, s in miss)
    return (f"{tool}: {said} {'is' if len(miss) == 1 else 'are'} missing from the Python that runs this"
            f"{(' (' + why + ')') if why else ''}. Fix it first, after the user's yes (ask once: «ناقص {' و'.join(s for _, s in miss)}"
            f" عشان أكمّل. أثبّتها؟»): {packages_fix(miss)} · the user's own sentence for it: «ثبّت الناقص». Then run this again.")
def need_packages(tool, *mods, why=''):
    """Stop with one plain line when a library this script needs is missing, instead of a traceback (1.7.1)."""
    miss = missing_packages(*mods)
    if miss:
        sys.exit(packages_line(tool, miss, why))
def ffmpeg(): return executable('ffmpeg') or sys.exit('ffmpeg not found on PATH (install: ' + install_hint('winget install Gyan.FFmpeg / brew install ffmpeg / sudo apt install ffmpeg') + ')')
def ffprobe(): return executable('ffprobe') or sys.exit('ffprobe not found on PATH (' + install_hint('comes with ffmpeg') + ')')
