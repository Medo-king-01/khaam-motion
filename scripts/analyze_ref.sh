#!/usr/bin/env bash
# Compatibility: analyze_ref.sh ref.mp4 [outdir]; flags are handled by analyze_ref.py.
# 1.7.1: Python 3.9+ (one floor); on a Mac the same search as preflight.sh (the Mac route's tools first, never Apple's stub).
set -e
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PY=""
ok() { "$1" -c 'import sys;sys.exit(0 if sys.version_info >= (3,9) else 1)' >/dev/null 2>&1; }
if [ "$(uname -s 2>/dev/null)" = Darwin ]; then
  T="${KHAAM_TOOLS:-$HOME/.cache/khaam-motion/tools}"
  for candidate in "$T/bin/python3" "$T/python/bin/python3" /opt/homebrew/bin/python3 /usr/local/bin/python3 "$(command -v python3 2>/dev/null || true)"; do
    [ -n "$candidate" ] && [ -x "$candidate" ] || continue
    if [ "$candidate" = /usr/bin/python3 ] && ! xcode-select -p >/dev/null 2>&1; then continue; fi
    if ok "$candidate"; then PY="$candidate"; break; fi
  done
  if [ -z "$PY" ]; then echo "No Python 3.9+ on this Mac yet. Run: bash \"$HERE/mac_tools.sh\" plan (no Homebrew, no password)." >&2; exit 1; fi
else
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 && ok "$candidate"; then PY="$candidate"; break; fi
  done
  if [ -z "$PY" ]; then echo "A working Python 3.9+ interpreter is required; select one or install with permission." >&2; exit 1; fi
fi
if [ "$#" -eq 2 ] && [[ "$2" != --* ]]; then exec "$PY" "$HERE/analyze_ref.py" "$1" --out "$2"; fi
exec "$PY" "$HERE/analyze_ref.py" "$@"
