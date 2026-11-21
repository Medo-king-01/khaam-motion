#!/usr/bin/env bash
# «موشن خام» 1.7.1: the Mac route for the tools the skill runs on: Python 3, Node 22+, FFmpeg with ffprobe, and
# NumPy, SciPy and Pillow. No Homebrew, no password, nothing typed in Terminal: Claude runs it, after the user's yes.
#
#   bash mac_tools.sh check            what is here, as JSON (read-only, offline; never opens Apple's install window)
#   bash mac_tools.sh plan             check + each missing download with its size, the next command, and the one question
#   bash mac_tools.sh get --yes WHAT   download, verify, unpack, test and link. WHAT: missing (what plan lists) | python |
#                                      node | ffmpeg | packages, several allowed. Without --yes it downloads nothing.
#   bash mac_tools.sh link             no download: put the tools found on this Mac into the tools' bin folder
#   bash mac_tools.sh path             the line that puts the tools first on a command's PATH
#
# Where: ~/.cache/khaam-motion/tools/ (KHAAM_TOOLS overrides): python/, node/, ffmpeg/, venv/ (NumPy, SciPy, Pillow) and
# bin/, the one folder Claude puts first on the PATH. Nothing outside it changes; deleting it undoes everything.
# Sources: each download comes from its own upstream (below) and must match the SHA-256 written here (each equal to the
# publisher's own list on 2026-11-18), or nothing from it is used. No binary ships inside the skill.
# Gatekeeper: a file curl writes carries no quarantine flag, so there is nothing for Gatekeeper to stop; Node and FFmpeg
# are Developer ID signed besides. If something on this Mac flagged a file this run fetched and verified anyway, the flag
# is taken off that file only, and the result says so.
# Apple's stubs: on a Mac without the developer tools, /usr/bin/python3, /usr/bin/git and friends open Apple's install
# window. This script never runs them unless `xcode-select -p` (which only prints a path) says the tools are there.
# Written for bash 3.2, the Mac's own. Tests only: KHAAM_MAC_TOOLS_MIRROR=<dir or URL> serves the same files from
# elsewhere (their SHA-256 must still match); KHAAM_MAC_TOOLS_TRUST_OWN=1 takes this script's own unpacked tools as working
# without running them (a Linux test box cannot run a Mac binary).

if [ -z "$HOME" ] && [ -z "$KHAAM_TOOLS" ]; then echo '{"error": "no_home", "detail": "HOME is not set"}'; exit 1; fi
TOOLS="${KHAAM_TOOLS:-$HOME/.cache/khaam-motion/tools}"
case "$TOOLS" in /|/*/..*|*/../*) echo '{"error": "bad_tools_dir"}'; exit 1 ;; esac
BIN="$TOOLS/bin"
PATH_LINE='export PATH="$HOME/.cache/khaam-motion/tools/bin:$PATH"'
[ -n "$KHAAM_TOOLS" ] && PATH_LINE="export PATH=\"$KHAAM_TOOLS/bin:\$PATH\""

# ---- the pinned downloads (checked 2026-11-18; sizes in bytes)
PY_VERSION=3.12.16
PY_SOURCE='python-build-standalone 20261110 (github.com/astral-sh/python-build-standalone): CPython, PSF-2.0; its bundled libraries keep their own licences (OpenSSL Apache-2.0, …)'
PY_FILE_arm64='cpython-3.12.16+20261110-aarch64-apple-darwin-install_only_stripped.tar.gz'
PY_URL_arm64='https://github.com/astral-sh/python-build-standalone/releases/download/20261110/cpython-3.12.16%2B20261110-aarch64-apple-darwin-install_only_stripped.tar.gz'
PY_SHA_arm64=2f11b8aa3726bdbd87dd9eb76568412faddf4f47e26913fa45d6a2e424972acd
PY_BYTES_arm64=25237581
PY_FILE_x86_64='cpython-3.12.16+20261110-x86_64-apple-darwin-install_only_stripped.tar.gz'
PY_URL_x86_64='https://github.com/astral-sh/python-build-standalone/releases/download/20261110/cpython-3.12.16%2B20261110-x86_64-apple-darwin-install_only_stripped.tar.gz'
PY_SHA_x86_64=b78a4c479f1964ec484880bee567568266f68da102269fb93a05fe8716b45f91
PY_BYTES_x86_64=24957926
PY_DISK_MB=66

NODE_SOURCE='nodejs.org (official build, Developer ID «Node.js Foundation»): Node.js, MIT; npm and its bundled packages keep their own licences'
# Node 24 LTS needs macOS 13.5 or newer; below that, Node 22 LTS (macOS 11+). HyperFrames needs 22 or newer.
NODE24_VERSION=24.22.3
NODE24_FILE_arm64='node-v24.22.3-darwin-arm64.tar.xz'
NODE24_SHA_arm64=1d64136c8a43d648d1b3bad10797a4c995b1ca032d2bde8799de43b37f058fe5
NODE24_BYTES_arm64=27519132
NODE24_FILE_x86_64='node-v24.22.3-darwin-x64.tar.xz'
NODE24_SHA_x86_64=4daeec962855c1a6e66cda398a25037319dc1bbd4a0939188b3547afbbfb6490
NODE24_BYTES_x86_64=29287204
NODE22_VERSION=22.23.5
NODE22_FILE_arm64='node-v22.23.5-darwin-arm64.tar.xz'
NODE22_SHA_arm64=d0c68c321161bb2c6483efea9a343010dea8e5e7f60d73c6a7eba140016d662f
NODE22_BYTES_arm64=25919840
NODE22_FILE_x86_64='node-v22.23.5-darwin-x64.tar.xz'
NODE22_SHA_x86_64=d68bf234a07781141dfca61ae4461c24560f70bd53223d76a41529eb02e8554e
NODE22_BYTES_x86_64=27448564
NODE_DISK_MB=200

FF_VERSION=9.0.2
FF_SOURCE='ffmpeg.martin-riedl.de (static release build, Developer ID «Martin Riedl»; FFmpeg built with --enable-gpl --enable-version3): GPL-3.0-or-later'
FF_DIR_arm64='https://ffmpeg.martin-riedl.de/download/macos/arm64/1789931890_9.0.2'
FF_SHA_arm64=c8ed4c4e6978a03c485edbfe4e0a5dc2380f8a30bba5150531b31b094492d924
FF_BYTES_arm64=28395699
FP_SHA_arm64=fcbe839537485eaee7a7a8bc5cbc0f90d53617e80943e8a5b2e31cb851197ea6
FP_BYTES_arm64=28317701
FF_DIR_x86_64='https://ffmpeg.martin-riedl.de/download/macos/amd64/1789931006_9.0.2'
FF_SHA_x86_64=7c6b4125b191cbf773832dc51f424cf2b6bb7da43007d1e066f95909e47cacd4
FF_BYTES_x86_64=33816391
FP_SHA_x86_64=2322438ed2f6319a691291b247d09c69dcaa3a982460d1f269a7e1af335cfdfd
FP_BYTES_x86_64=33719233
FF_DISK_MB_arm64=133
FF_DISK_MB_x86_64=190

# The packages, from PyPI: the versions this skill's release checks ran on, for this script's Python 3.12; another Python
# gets the newest its version allows. NumPy BSD-3-Clause, SciPy BSD-3-Clause, Pillow MIT-CMU.
PKG_PINNED='numpy==2.4.1 scipy==1.17.1 pillow==12.1.0'
PKG_PLAIN='numpy scipy pillow'
PKG_DISK_MB=150

# ---- small helpers (bash 3.2)
js() {  # a JSON string (newlines kept as \n)
  printf '"%s"' "$(printf '%s' "$1" | tr -d '\r' | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/	/\\t/g' | awk 'BEGIN { ORS = "" } NR > 1 { print "\\n" } { print }')"
}
jb() { if [ "$1" = 1 ]; then printf true; else printf false; fi; }
mb() { echo $(( ($1 + 500000) / 1000000 )); }
say() { printf '%s\n' "$*" >&2; }

is_mac() { [ "$(uname -s 2>/dev/null)" = Darwin ]; }
mac_version() { sw_vers -productVersion 2>/dev/null || echo 0; }
mac_arch() { if [ "$(sysctl -n hw.optional.arm64 2>/dev/null)" = 1 ]; then echo arm64; else echo x86_64; fi; }
ver_ge() {  # ver_ge A B: dotted version A >= B (three parts)
  local a1 a2 a3 b1 b2 b3
  IFS=. read -r a1 a2 a3 <<< "$1"; IFS=. read -r b1 b2 b3 <<< "$2"
  a1=${a1:-0}; a2=${a2:-0}; a3=${a3:-0}; b1=${b1:-0}; b2=${b2:-0}; b3=${b3:-0}
  case "$a1$a2$a3$b1$b2$b3" in *[!0-9]*) return 1 ;; esac
  [ "$a1" -gt "$b1" ] && return 0; [ "$a1" -lt "$b1" ] && return 1
  [ "$a2" -gt "$b2" ] && return 0; [ "$a2" -lt "$b2" ] && return 1
  [ "$a3" -ge "$b3" ]
}
clt_present() {  # Apple's developer tools: `xcode-select -p` only prints a path, it never opens Apple's window
  local d; d=$(xcode-select -p 2>/dev/null) || return 1
  [ -n "$d" ] && [ -d "$d" ]
}
apple_stub() {  # a /usr/bin tool that opens Apple's window while the developer tools are missing
  case "$1" in /usr/bin/python3|/usr/bin/pip3|/usr/bin/git|/usr/bin/make|/usr/bin/clang|/usr/bin/cc|/usr/bin/gcc|/usr/bin/xcrun) ! clt_present ;; *) return 1 ;; esac
}
own() { case "$1" in "$TOOLS"/*) return 0 ;; *) return 1 ;; esac; }
trusted_own() { [ "$KHAAM_MAC_TOOLS_TRUST_OWN" = 1 ] && own "$1" && [ -f "$1" ]; }
is_exe() { [ -x "$1" ] || trusted_own "$1"; }   # tests on Windows: a Mac binary is not «executable» there

py_ok() { trusted_own "$1" && return 0; "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; }
py_pkgs() { trusted_own "$1" && [ -f "$TOOLS/.packages-ok" ] && return 0; "$1" -c 'import numpy, scipy, PIL' >/dev/null 2>&1; }
py_version() { if trusted_own "$1"; then echo "$PY_VERSION"; else "$1" -c 'import sys; print(sys.version.split()[0])' 2>/dev/null; fi; }
node_major() {
  local v
  if trusted_own "$1"; then v=$(sed -n 's/.*"tool": *"node", *"version": *"\([0-9.]*\)".*/\1/p' "$TOOLS/manifest.jsonl" 2>/dev/null | tail -1); v=${v:-0}
  else v=$("$1" --version 2>/dev/null) || return 1; fi
  v=${v#v}; echo "${v%%.*}"
}
ff_ok() { trusted_own "$1" && return 0; "$1" -version >/dev/null 2>&1; }

find_python() {  # the first Python 3.9+ here; Apple's stub only when the developer tools are installed. $1=base: not the venv
  local c
  for c in "$TOOLS/venv/bin/python3" "$TOOLS/python/bin/python3" "$(command -v python3 2>/dev/null)" \
           /opt/homebrew/bin/python3 /usr/local/bin/python3 /Library/Frameworks/Python.framework/Versions/Current/bin/python3 \
           /usr/bin/python3; do
    [ -n "$c" ] && is_exe "$c" || continue
    case "$c" in "$BIN"/*) continue ;; esac   # our own wrapper: look at what it points to instead
    [ "$1" = base ] && case "$c" in "$TOOLS/venv/"*) continue ;; esac
    apple_stub "$c" && continue
    py_ok "$c" && { echo "$c"; return 0; }
  done
  return 1
}
find_node() {  # Node 22 or newer
  local c m
  for c in "$TOOLS/node/bin/node" "$(command -v node 2>/dev/null)" /opt/homebrew/bin/node /usr/local/bin/node \
           "$HOME"/.nvm/versions/node/v*/bin/node "$HOME/.volta/bin/node"; do
    [ -n "$c" ] && is_exe "$c" || continue
    case "$c" in "$BIN"/*) continue ;; esac
    m=$(node_major "$c") || continue
    [ -n "$m" ] && [ "$m" -ge 22 ] 2>/dev/null && { echo "$c"; return 0; }
  done
  return 1
}
find_ff() {  # $1 = ffmpeg | ffprobe
  local c
  for c in "$TOOLS/ffmpeg/$1" "$(command -v "$1" 2>/dev/null)" "/opt/homebrew/bin/$1" "/usr/local/bin/$1"; do
    [ -n "$c" ] && is_exe "$c" || continue
    case "$c" in "$BIN"/*) continue ;; esac
    ff_ok "$c" && { echo "$c"; return 0; }
  done
  return 1
}

# ---- what is here
scan() {
  OSV=$(mac_version); ARCH=$(mac_arch); CLT=0; clt_present && CLT=1
  PY=$(find_python); PYV=""; PKG=0
  if [ -n "$PY" ]; then PYV=$(py_version "$PY"); py_pkgs "$PY" && PKG=1; fi
  NODE=$(find_node); NODEV=""; [ -n "$NODE" ] && NODEV=$(node_major "$NODE")
  FF=$(find_ff ffmpeg); FP=$(find_ff ffprobe)
  if ver_ge "$OSV" 13.5.0; then NODE_PICK=24; else NODE_PICK=22; fi
  MISSING=""   # in the order get installs them (the packages need the Python)
  [ -z "$PY" ] && MISSING="$MISSING python"
  [ -z "$NODE" ] && MISSING="$MISSING node"
  { [ -z "$FF" ] || [ -z "$FP" ]; } && MISSING="$MISSING ffmpeg"
  [ "$PKG" = 1 ] || MISSING="$MISSING packages"
  MISSING=${MISSING# }
  BLOCKED=""
  case " $MISSING " in *" ffmpeg "*) ver_ge "$OSV" 12.0.0 || BLOCKED="ffmpeg" ;; esac
  case " $MISSING " in *" packages "*) [ "$ARCH" = arm64 ] && ! ver_ge "$OSV" 12.0.0 && BLOCKED="$BLOCKED packages" ;; esac
  case " $MISSING " in *" node "*) ver_ge "$OSV" 11.0.0 || BLOCKED="$BLOCKED node" ;; esac
  case " $MISSING " in *" python "*) if [ "$ARCH" = arm64 ]; then ver_ge "$OSV" 11.0.0 || BLOCKED="$BLOCKED python"; else ver_ge "$OSV" 10.15.0 || BLOCKED="$BLOCKED python"; fi ;; esac
  BLOCKED=${BLOCKED# }
}

status_json() {
  printf '{"platform": %s, "arch": %s, "apple_developer_tools": %s, "tools_dir": %s,\n' "$(js "macOS $OSV")" "$(js "$ARCH")" "$(jb $CLT)" "$(js "$TOOLS")"
  printf ' "python": {"path": %s, "version": %s, "numpy_scipy_pillow": %s},\n' "$(js "$PY")" "$(js "$PYV")" "$(jb $PKG)"
  printf ' "node": {"path": %s, "major": %s, "minimum": 22},\n' "$(js "$NODE")" "$(js "$NODEV")"
  printf ' "ffmpeg": {"path": %s}, "ffprobe": {"path": %s},\n' "$(js "$FF")" "$(js "$FP")"
  printf ' "missing": [%s], "blocked": [%s],\n' "$(list_json "$MISSING")" "$(list_json "$BLOCKED")"
  printf ' "path_line": %s, "bin_ready": %s' "$(js "$PATH_LINE")" "$(jb "$( [ -d "$BIN" ] && echo 1 )")"
}
list_json() { local out="" w; for w in $1; do out="$out, $(js "$w")"; done; printf '%s' "${out#, }"; }

# the size of each download for this Mac (bytes), and on disk (MB)
size_of() {
  case "$1" in
    python) eval "echo \$PY_BYTES_$ARCH" ;;
    node) eval "echo \$NODE${NODE_PICK}_BYTES_$ARCH" ;;
    ffmpeg) eval "echo \$(( FF_BYTES_$ARCH + FP_BYTES_$ARCH ))" ;;
    packages) pkg_bytes ;;
  esac
}
pkg_bytes() {  # the wheels pip picks for this Mac (PyPI sizes, 2026-11-18); another Python: about the same
  if [ "$ARCH" = arm64 ]; then if ver_ge "$OSV" 14.0.0; then echo 30204397; else echo 45204082; fi
  else if ver_ge "$OSV" 14.0.0; then echo 34516118; else echo 53530484; fi; fi
}
disk_of() {
  case "$1" in python) echo $PY_DISK_MB ;; node) echo $NODE_DISK_MB ;; ffmpeg) eval "echo \$FF_DISK_MB_$ARCH" ;; packages) echo $PKG_DISK_MB ;; esac
}
label_of() {
  case "$1" in
    python) echo "Python $PY_VERSION" ;;
    node) eval "echo Node \$NODE${NODE_PICK}_VERSION" ;;
    ffmpeg) echo "FFmpeg $FF_VERSION (ffmpeg + ffprobe)" ;;
    packages) echo "NumPy, SciPy, Pillow" ;;
  esac
}
ar_of() {
  case "$1" in python) echo 'Python' ;; node) echo 'Node' ;; ffmpeg) echo 'FFmpeg (مع ffprobe)' ;; packages) echo 'مكتبات الصوت والصور (NumPy وSciPy وPillow)' ;; esac
}
from_of() {
  case "$1" in python) echo 'github.com/astral-sh/python-build-standalone' ;; node) echo 'nodejs.org' ;; ffmpeg) echo 'ffmpeg.martin-riedl.de' ;; packages) echo 'pypi.org' ;; esac
}

plan_json() {
  local w total=0 disk=0 dl="" lines="" n=0 b d ask nextc
  for w in $MISSING; do
    case " $BLOCKED " in *" $w "*) continue ;; esac
    b=$(size_of "$w"); d=$(disk_of "$w"); total=$((total + b)); disk=$((disk + d)); n=$((n + 1))
    dl="$dl, {\"what\": $(js "$w"), \"name\": $(js "$(label_of "$w")"), \"from\": $(js "$(from_of "$w")"), \"mb\": $(mb "$b"), \"disk_mb\": $d}"
    lines="$lines
- $(ar_of "$w"): حوالي $(mb "$b") ميقا"
  done
  if [ "$n" = 0 ] && [ -z "$BLOCKED" ]; then
    ask=""; nextc="bash \"$0\" link"
  elif [ "$n" = 0 ]; then
    ask=""; nextc=""
  else
    ask="ناقص جهازك برامج يحتاجها «موشن خام». أنزّلها لك من مواقعها الرسمية لمجلد خاص فيها داخل حسابك، بدون Homebrew وبدون كلمة سر وبدون Terminal:$lines
المجموع حوالي $(mb "$total") ميقا تنزيل، وتاخذ حوالي $disk ميقا من جهازك. أنزّلها؟"
    nextc="bash \"$0\" get --yes missing"
  fi
  local blk="" names=""
  for w in $BLOCKED; do names="$names، $(ar_of "$w")"; done
  [ -n "$BLOCKED" ] && blk="${names#، } يحتاج macOS 12 أو أحدث، وجهازك على $OSV. حدّث النظام من «إعدادات النظام ← عام ← تحديث البرامج» (System Settings ← General ← Software Update)، وبعدها قل «ثبّت الناقص»."
  printf ',\n "downloads": [%s],\n "total_mb": %s, "disk_mb": %s, "next_command": %s,\n "ask_user": %s, "blocked_tell_user": %s}\n' \
    "${dl#, }" "$(mb "$total")" "$disk" "$(js "$nextc")" "$(js "$ask")" "$(js "$blk")"
}

# ---- getting things
mirror_url() {  # $1 real URL, $2 file name: the URL to fetch (KHAAM_MAC_TOOLS_MIRROR is for tests)
  if [ -n "$KHAAM_MAC_TOOLS_MIRROR" ]; then
    case "$KHAAM_MAC_TOOLS_MIRROR" in *://*) echo "$KHAAM_MAC_TOOLS_MIRROR/$2" ;; *) echo "file://$KHAAM_MAC_TOOLS_MIRROR/$2" ;; esac | sed 's/ /%20/g'
  else echo "$1"; fi
}
sha256_of() {
  if command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | cut -d' ' -f1
  elif command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1
  else openssl dgst -sha256 "$1" | sed 's/.*= *//'; fi
}
fetch() {  # url file sha256 bytes: download into $DL/<file> and check its SHA-256
  local url file="$2" sha="$3" got
  url=$(mirror_url "$1" "$2")
  say "download $(mb "$4") MB: $1"
  if ! curl -fL --retry 2 --connect-timeout 20 --silent --show-error -o "$DL/$file" "$url"; then
    rm -f "$DL/$file"; ERR="the download failed ($1): check the internet and try again"; return 1
  fi
  got=$(sha256_of "$DL/$file")
  if [ "$got" != "$sha" ]; then
    rm -f "$DL/$file"; ERR="STOP: $file does not match its published hash. Nothing was installed from it"; return 2
  fi
  return 0
}
unquarantine() {  # $1 a folder this run fetched and verified, $2 its main binary
  if xattr -p com.apple.quarantine "$2" >/dev/null 2>&1; then xattr -dr com.apple.quarantine "$1" 2>/dev/null; echo true; else echo false; fi
}
put_in_place() {  # staging folder -> $TOOLS/<name>, replacing this script's own older copy
  local from="$1" to="$TOOLS/$2"
  rm -rf "$to.old"; [ -e "$to" ] && mv "$to" "$to.old"
  if mv "$from" "$to"; then rm -rf "$to.old"; return 0; fi
  [ -e "$to.old" ] && mv "$to.old" "$to"; return 1
}
record() {  # tool version url sha256 bytes licence quarantine_removed
  printf '{"tool": %s, "version": %s, "url": %s, "sha256": %s, "bytes": %s, "source_and_licence": %s, "quarantine_removed": %s, "installed": %s}\n' \
    "$(js "$1")" "$(js "$2")" "$(js "$3")" "$(js "$4")" "${5:-0}" "$(js "$6")" "${7:-false}" "$(js "$(date -u +%Y-%m-%dT%H:%M:%SZ)")" >> "$TOOLS/manifest.jsonl"
}

get_python() {
  local f u s b st q
  eval "f=\$PY_FILE_$ARCH; u=\$PY_URL_$ARCH; s=\$PY_SHA_$ARCH; b=\$PY_BYTES_$ARCH"
  fetch "$u" "$f" "$s" "$b" || return 1
  st="$TOOLS/.staging-python"; rm -rf "$st"; mkdir -p "$st"
  tar -xzf "$DL/$f" -C "$st" || { ERR="could not unpack $f"; return 1; }
  [ -f "$st/python/bin/python3" ] || { ERR="$f did not hold python/bin/python3"; return 1; }
  put_in_place "$st/python" python || { ERR="could not move Python into $TOOLS"; return 1; }
  rm -rf "$st"
  q=$(unquarantine "$TOOLS/python" "$TOOLS/python/bin/python3")
  py_ok "$TOOLS/python/bin/python3" || { ERR="the downloaded Python does not start on this Mac"; return 1; }
  record python "$PY_VERSION" "$u" "$s" "$b" "$PY_SOURCE" "$q"
}
get_node() {
  local f u s b v st q d
  eval "v=\$NODE${NODE_PICK}_VERSION; f=\$NODE${NODE_PICK}_FILE_$ARCH; s=\$NODE${NODE_PICK}_SHA_$ARCH; b=\$NODE${NODE_PICK}_BYTES_$ARCH"
  u="https://nodejs.org/dist/v$v/$f"
  fetch "$u" "$f" "$s" "$b" || return 1
  st="$TOOLS/.staging-node"; rm -rf "$st"; mkdir -p "$st"
  tar -xJf "$DL/$f" -C "$st" || { ERR="could not unpack $f"; return 1; }
  d="$st/${f%.tar.xz}"
  [ -f "$d/bin/node" ] || { ERR="$f did not hold bin/node"; return 1; }
  put_in_place "$d" node || { ERR="could not move Node into $TOOLS"; return 1; }
  rm -rf "$st"
  q=$(unquarantine "$TOOLS/node" "$TOOLS/node/bin/node")
  record node "$v" "$u" "$s" "$b" "$NODE_SOURCE" "$q"
  local m; m=$(node_major "$TOOLS/node/bin/node")
  [ -n "$m" ] && [ "$m" -ge 22 ] 2>/dev/null || { ERR="the downloaded Node does not start on this Mac"; return 1; }
}
unzip_to() { if command -v ditto >/dev/null 2>&1; then ditto -x -k "$1" "$2"; else unzip -q -o "$1" -d "$2"; fi; }
get_ffmpeg() {
  local base s1 b1 s2 b2 st q
  eval "base=\$FF_DIR_$ARCH; s1=\$FF_SHA_$ARCH; b1=\$FF_BYTES_$ARCH; s2=\$FP_SHA_$ARCH; b2=\$FP_BYTES_$ARCH"
  fetch "$base/ffmpeg.zip" "ffmpeg-$FF_VERSION-$ARCH.zip" "$s1" "$b1" || return 1
  fetch "$base/ffprobe.zip" "ffprobe-$FF_VERSION-$ARCH.zip" "$s2" "$b2" || return 1
  st="$TOOLS/.staging-ffmpeg"; rm -rf "$st"; mkdir -p "$st/ffmpeg"
  unzip_to "$DL/ffmpeg-$FF_VERSION-$ARCH.zip" "$st/ffmpeg" && unzip_to "$DL/ffprobe-$FF_VERSION-$ARCH.zip" "$st/ffmpeg" \
    || { ERR="could not unpack FFmpeg"; return 1; }
  [ -f "$st/ffmpeg/ffmpeg" ] && [ -f "$st/ffmpeg/ffprobe" ] || { ERR="the FFmpeg archives did not hold ffmpeg and ffprobe"; return 1; }
  chmod 755 "$st/ffmpeg/ffmpeg" "$st/ffmpeg/ffprobe"
  put_in_place "$st/ffmpeg" ffmpeg || { ERR="could not move FFmpeg into $TOOLS"; return 1; }
  rm -rf "$st"
  q=$(unquarantine "$TOOLS/ffmpeg" "$TOOLS/ffmpeg/ffmpeg")
  ff_ok "$TOOLS/ffmpeg/ffmpeg" && ff_ok "$TOOLS/ffmpeg/ffprobe" || { ERR="the downloaded FFmpeg does not start on this Mac"; return 1; }
  record ffmpeg "$FF_VERSION" "$base/ffmpeg.zip" "$s1" "$b1" "$FF_SOURCE" "$q"
  record ffprobe "$FF_VERSION" "$base/ffprobe.zip" "$s2" "$b2" "$FF_SOURCE" "$q"
}
get_packages() {  # a private environment (venv) from the Python found, so no Python of the user's changes
  local base pk vp
  base=$(find_python base) || { ERR="no Python 3.9+ here yet: get python first"; return 1; }
  is_exe "$TOOLS/venv/bin/python3" && [ -f "$TOOLS/.venv-base" ] && base=$(cat "$TOOLS/.venv-base")
  if [ "$base" = "$TOOLS/python/bin/python3" ]; then pk=$PKG_PINNED; else pk=$PKG_PLAIN; fi
  if [ "$KHAAM_MAC_TOOLS_TRUST_OWN" = 1 ] && own "$base"; then  # tests on a non-Mac box: the venv step is not run
    mkdir -p "$TOOLS/venv/bin"; : > "$TOOLS/venv/bin/python3"; chmod 755 "$TOOLS/venv/bin/python3"; : > "$TOOLS/.packages-ok"
    record packages "$pk" pypi.org - 0 'PyPI: NumPy BSD-3-Clause, SciPy BSD-3-Clause, Pillow MIT-CMU (test mode: not installed)' false
    return 0
  fi
  if [ ! -x "$TOOLS/venv/bin/python3" ] || ! py_ok "$TOOLS/venv/bin/python3"; then
    rm -rf "$TOOLS/venv"
    "$base" -m venv "$TOOLS/venv" || { ERR="could not make the private Python environment"; return 1; }
    printf '%s\n' "$base" > "$TOOLS/.venv-base"
  fi
  vp="$TOOLS/venv/bin/python3"
  [ "$pk" = "$PKG_PLAIN" ] && "$vp" -m pip install --disable-pip-version-check --no-input -q --upgrade pip >/dev/null 2>&1
  say "download about $(mb "$(pkg_bytes)") MB from pypi.org: $pk"
  # shellcheck disable=SC2086
  "$vp" -m pip install --disable-pip-version-check --no-input -q $pk || { ERR="pip could not install $pk"; return 1; }
  py_pkgs "$vp" || { ERR="NumPy, SciPy or Pillow does not load"; return 1; }
  : > "$TOOLS/.packages-ok"
  record packages "$pk" https://pypi.org/simple/ - 0 'PyPI: NumPy BSD-3-Clause, SciPy BSD-3-Clause, Pillow MIT-CMU' false
}

wrapper() {  # $1 name, $2 the Python it runs: a tiny script (a symlink would hide a venv from Python)
  local q; q=$(printf '%s' "$2" | sed "s/'/'\\\\''/g")
  printf "#!/bin/sh\n# made by «موشن خام» mac_tools.sh: the Python the skill uses on this Mac\nexec '%s' \"\$@\"\n" "$q" > "$BIN/$1"
  chmod 755 "$BIN/$1"
}
link_bin() {  # tools/bin: python3/python (wrappers), node/npm/npx, ffmpeg/ffprobe (links), whatever was found or fetched
  local py nd ff fp d n
  mkdir -p "$BIN" || return 1
  py=""; is_exe "$TOOLS/venv/bin/python3" && py_pkgs "$TOOLS/venv/bin/python3" && py="$TOOLS/venv/bin/python3"
  [ -z "$py" ] && py=$(find_python)
  if [ -n "$py" ]; then wrapper python3 "$py"; wrapper python "$py"; fi
  nd=$(find_node)
  if [ -n "$nd" ]; then
    d=$(dirname "$nd")
    ln -sf "$nd" "$BIN/node"
    for n in npm npx; do [ -e "$d/$n" ] && ln -sf "$d/$n" "$BIN/$n"; done
  fi
  ff=$(find_ff ffmpeg); fp=$(find_ff ffprobe)
  [ -n "$ff" ] && ln -sf "$ff" "$BIN/ffmpeg"
  [ -n "$fp" ] && ln -sf "$fp" "$BIN/ffprobe"
  return 0
}

usage() { sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; }

main() {
  local cmd="${1:-}"; shift 2>/dev/null
  case "$cmd" in
    -h|--help|help|"") usage; return 0 ;;
    path) echo "$PATH_LINE"; return 0 ;;
  esac
  if ! is_mac; then
    printf '{"error": "not_a_mac", "detail": %s}\n' "$(js "This is the Mac route. On Windows and Linux follow START-HERE.md step 6.")"
    return 2
  fi
  case "$cmd" in
    check) scan; status_json; printf '}\n' ;;
    plan) scan; status_json; plan_json ;;
    link) scan; link_bin; scan; status_json; printf ',\n "linked": true}\n' ;;
    get)
      local yes=0 want="" w a
      for a in "$@"; do case "$a" in --yes|-y) yes=1 ;; *) want="$want $a" ;; esac; done
      [ -z "$want" ] && want=" missing"
      if [ "$yes" != 1 ]; then
        printf '{"error": "no_yes", "detail": %s}\n' "$(js "Nothing was downloaded. Ask the user with plan's ask_user line first; on a yes run: get --yes$want")"
        return 3
      fi
      scan
      case " $want " in *" missing "*) want=" $MISSING" ;; esac
      local done_="" failed="" errs="" free
      mkdir -p "$TOOLS" || { printf '{"error": "no_folder", "detail": %s}\n' "$(js "could not make $TOOLS")"; return 1; }
      free=$(df -Pk "$TOOLS" 2>/dev/null | awk 'NR==2 {print $4}')
      if [ -n "$free" ] && [ "$free" -lt 800000 ] 2>/dev/null; then
        printf '{"error": "no_space", "detail": %s, "free_mb": %s}\n' "$(js "about 800 MB free is needed while installing")" "$((free / 1000))"
        return 1
      fi
      DL="$TOOLS/_downloads"; mkdir -p "$DL"
      for w in python node ffmpeg packages; do   # this order: packages need the Python
        case " $want " in *" $w "*) ;; *) continue ;; esac
        case " $BLOCKED " in *" $w "*) failed="$failed $w"; errs="$errs, $(js "$w: needs a newer macOS")"; continue ;; esac
        ERR=""
        if "get_$w"; then done_="$done_ $w"; else failed="$failed $w"; errs="$errs, $(js "$w: $ERR")"; fi
      done
      rm -rf "$DL"
      link_bin
      scan
      local ok=1 tell
      [ -n "$failed" ] && ok=0
      if [ "$ok" = 1 ] && [ -z "$done_" ]; then
        tell="البرامج اللي يحتاجها «موشن خام» موجودة في جهازك ✅"
      elif [ "$ok" = 1 ]; then
        tell="جهّزت البرامج اللي يحتاجها «موشن خام» ✅ كلها في مجلد خاص فيها داخل حسابك، وما تغيّر شي ثاني في جهازك."
      else
        tell="ما قدرت أكمّل تنزيل: $(for w in $failed; do printf '%s، ' "$(ar_of "$w")"; done | sed 's/، $//'). ما تغيّر شي في جهازك، وأقدر أحاول مرة ثانية."
      fi
      status_json
      printf ',\n "installed": [%s], "failed": [%s], "errors": [%s], "ok": %s,\n "tell_user": %s}\n' \
        "$(list_json "$done_")" "$(list_json "$failed")" "${errs#, }" "$(jb $ok)" "$(js "$tell")"
      [ "$ok" = 1 ]
      ;;
    *) usage; return 2 ;;
  esac
}

main "$@"
