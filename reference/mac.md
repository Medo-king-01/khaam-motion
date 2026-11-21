# A Mac (1.7.1): the tools with no Homebrew and no password

Read this on a Mac before the first install step, and whenever a tool is missing or a folder is refused there.

## Why the skill brings its own tools on a Mac
- **Apple's stubs.** On a Mac without Apple's developer tools, `/usr/bin/python3`, `git`, `pip3`, `make` and `clang` are stubs: running one opens Apple's window «The "python3" command requires the command line developer tools». macOS has had no `python` command since 12.3.
- **Homebrew needs the admin password typed in Terminal** (`sudo`). Claude's shell has no terminal to type it into, and most beginners never open Terminal. On Apple Silicon its folder `/opt/homebrew/bin` is not on the app's PATH until the user adds it by hand, and its Python refuses `pip install` («externally-managed-environment»).
- **An app started from the Dock has a bare PATH** (`/usr/bin:/bin:/usr/sbin:/sbin`), so tools installed elsewhere are not found.

So on a Mac the skill fetches Python, Node and FFmpeg itself, from their own upstreams, into one folder of the user's account: `~/.cache/khaam-motion/tools/`. Nothing is typed in Terminal and no password is asked.

## The script: `scripts/mac_tools.sh` (bash 3.2, the Mac's own; run it with `bash`)
| Command | Writes | What it does |
|---|---|---|
| `bash "<skill>/scripts/mac_tools.sh" check` | nothing | What is here, as JSON. It never runs Apple's stubs unless `xcode-select -p` (which only prints a path) says the developer tools are installed. |
| `… plan` | nothing | `check` plus each missing download with its size (`downloads`, `total_mb`, `disk_mb`), `ask_user` (one Arabic question), `next_command`, and `blocked_tell_user` on a Mac older than macOS 12. |
| `… get --yes missing` (or `python`, `node`, `ffmpeg`, `packages`) | the tools folder | Downloads, checks the SHA-256 written in the script, unpacks, runs `--version`, links into `tools/bin`, writes `tools/manifest.jsonl`. Without `--yes` it downloads nothing. |
| `… link` | `tools/bin` | No download: links the good tools already on the Mac (Homebrew's, nvm's, python.org's) into `tools/bin`. |
| `… path` | nothing | Prints `export PATH="$HOME/.cache/khaam-motion/tools/bin:$PATH"`. |

**Protocol:** `plan` → if `blocked_tell_user`, say it and stop → if `ask_user`, ask it as it is (it names every download and its size) → on a yes, `next_command` → say `tell_user`. Then begin every shell command with the `path` line, and write `python` as the rest of the skill does. A no is respected: the video cannot be made without them, so say that in one line.

## What it fetches (pinned and checked on 2026-11-18)
| Tool | Version | From | Download / on disk | Runs on | Signed | Licence |
|---|---|---|---|---|---|---|
| Python | 3.12.16 | python-build-standalone release 20261110 (github.com/astral-sh) | 25 MB / 66 MB | Apple Silicon (macOS 11+), Intel (10.15+) | ad-hoc (Apple Silicon), none (Intel) | PSF-2.0; bundled libraries their own (OpenSSL Apache-2.0, …) |
| Node | 24.22.3 on macOS 13.5+, else 22.23.5 (macOS 11+) | nodejs.org | 26–29 MB / about 200 MB | Apple Silicon, Intel | Developer ID «Node.js Foundation», hardened runtime | MIT; npm's packages their own |
| FFmpeg + ffprobe | 9.0.2 (static) | ffmpeg.martin-riedl.de | 57 MB (Apple Silicon), 68 MB (Intel) / 133–190 MB | macOS 12+ | Developer ID «Martin Riedl», hardened runtime | GPL-3.0-or-later (built with `--enable-gpl --enable-version3`) |
| NumPy, SciPy, Pillow | 2.4.1, 1.17.1, 12.1.0 with that Python; the newest a found Python allows | pypi.org | 30–54 MB / about 150 MB | as the wheels | — | BSD-3-Clause, BSD-3-Clause, MIT-CMU |
On a new Apple Silicon Mac with macOS 14 or newer: about 140 MB to download and 550 MB on disk. The packages go into a private environment (`tools/venv`), so no Python of the user's changes. Pillow is there for the time labels on a reference's contact sheets (`analyze_ref.py`).

**No binary ships in the skill.** Each one comes from its upstream at install time and must match its SHA-256 (each equal to the publisher's own list on 2026-11-18); a mismatch stops with «does not match its published hash» and nothing from it is used. Never work around it.

## Gatekeeper
A file that `curl` writes carries no quarantine flag (only apps that opt in, such as browsers, add it), so Gatekeeper has nothing to check: no «unidentified developer» window, nothing to allow in Privacy & Security. Node and FFmpeg are Developer ID signed besides. If something on a Mac flags a file this script fetched and verified anyway, the script takes the flag off that tool's own files only and records `"quarantine_removed": true` in `tools/manifest.jsonl`. Never `spctl`, and never ask the user to override Gatekeeper.

## Apple's developer tools
Never opened unasked. `xcode-select --install` opens Apple's own window (about 1–2 GB, several minutes) and gives Python 3.9, which the skill supports (its floor is 3.9; the word-timing tool needs 3.10+, so it runs on the tools' Python 3.12: `align_voice.py plan` says so), but no Node or FFmpeg: offer it only if the user asks for Apple's Python, or the downloads above are blocked on their network. When the developer tools are there, `check` uses their Python.

## The words on a Mac (say them, in the user's language)
- **Before anything first touches Downloads, Desktop or Documents:** «الماك ممكن يسألك إذا Claude يقدر يوصل لملفات «التنزيلات» أو «سطح المكتب»: اضغط «السماح» (Allow).»
- **«Operation not permitted» there, or `workspace.py` printing `"error": "mac_privacy"`:** the user pressed «Don't Allow». Say its `tell_user`, or: «الماك منع Claude من المجلد. ترجّعه كذا: إعدادات النظام (System Settings) ← الخصوصية والأمن (Privacy & Security) ← الملفات والمجلدات (Files and Folders) ← Claude، وشغّل المجلد. بعدها سكّر Claude (Cmd+Q) وافتحه من جديد، وقل «كمّل».» Then run the same command again.
- **A folder instead of the ZIP:** Safari opens a downloaded ZIP by itself. «عادي، سفاري فك الضغط بنفسه. أشتغل على المجلد.» Copy it into a new temporary folder (`ditto "<folder>" "<temp>/<its name>"`); never change or delete the user's own folder.
- **The skill is not visible:** «المهارة في مجلد مخفي (.claude) داخل مجلدك، فلو ما شفتها في Finder هذا طبيعي.» (Cmd+Shift+. shows hidden folders.)
- **Unzipping:** `ditto -x -k "<zip>" "<folder>"` (Apple's own; it keeps Arabic names and needs no Python).

## Every later chat
`workspace.py` adds «## On this Mac» to the workspace's `CLAUDE.md` on a Mac (the PATH line and the words above), so every chat in that folder starts right. The skill's Python scripts find the tools even without the line (`khaam_paths.mac_path()` puts `tools/bin` first and Homebrew's folders last on their own PATH, and their children inherit it), but `npx` typed by Claude needs the line.

## Undo
Everything lives in `~/.cache/khaam-motion/tools/`. Deleting that folder (on the user's word) undoes it; nothing else on the Mac was changed.

## When something fails
- **A download failed:** the internet; run `get --yes <that one>` again.
- **A hash did not match:** stop and tell the user; never work around it.
- **A Mac older than macOS 12:** say `blocked_tell_user` (update macOS first).
- **The optional sound library** (`install_sounds.py`) runs on the tools' Python (3.12): its Earshot half needs Python 3.10+ (Earshot's own requirement), which that Python meets.

## What only a Mac can prove
This route was built and checked on Windows (Python, and Git Bash for the script) with macOS mocked, and its downloads inspected (CPU, minimum macOS, signature) without running them; see `CHANGELOG.md` 1.7.1. What only a real Mac shows: the binaries running, Apple's windows not appearing, the privacy window's words, Safari's folder, and a whole first video.
