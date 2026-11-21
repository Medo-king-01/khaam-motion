#!/usr/bin/env bash
# Compatibility entrypoint; all checks live in the portable Python helper.
# 1.7.1: Python 3.9+ (one floor). On a Mac it looks at the Mac route's tools and Homebrew first, and never runs Apple's
# /usr/bin/python3 stub while the developer tools are missing (it would open Apple's install window): mac_tools.sh.
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
exec "$PY" "$HERE/preflight.py" "$@"
