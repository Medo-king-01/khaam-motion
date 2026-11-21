## Khaam Motion workspace (agent-neutral)

This folder is a video workspace. For a video request read `.claude/skills/khaam-motion/SKILL.md` and `.claude/skills/khaam-motion/reference/agent-compatibility.md` if present. The latter overrides Claude-specific setup and UI instructions; the `.claude` path is only the installer's legacy storage location. If the skill is absent, ask for its accessible location rather than guessing.

Read `SESSION_HANDOFF.md` explicitly, plus the active video's `PROGRESS.md` and `TASTE.md` and local taste if present. On resume, use the installed `scripts/workspace.py --state` to reconcile state with files. Store video projects under `.khaam/projects/`; copy source files from `خام/` and `إلهام/` rather than moving them. Deliver approved finals to `جاهز/` using the installed `workspace.py --deliver`. Update the handoff and progress at milestones, including before long renders and after paid requests.

Only perform actions available in this host and authorized by the user. Ask before installs, downloads, paid requests or moving existing files. Never put secrets in chat, project files or logs. If local filesystem, GUI, network or other capabilities are unavailable, explain the limitation instead of pretending they worked. Preserve the skill's licence and third-party asset licences.
