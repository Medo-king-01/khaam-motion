#!/usr/bin/env python3
"""Evidence-aware notes inside Khaam's existing private user-taste.md.

The script never creates a second memory store, reads no conversation history,
and uses no network. Existing prose outside its marked section is preserved.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

DEFAULT_FILE = Path.home() / ".cache" / "khaam-motion" / "user-taste.md"
START = "<!-- KHAAM_TASTE_NOTES_V1:START -->"
END = "<!-- KHAAM_TASTE_NOTES_V1:END -->"
NOTE_RE = re.compile(r"^[ \t]*<!-- KHAAM_TASTE_NOTE_V1 (\{.*\}) -->[ \t]*$", re.MULTILINE)
KINDS = {"preference", "observed", "verified"}


class TasteNoteError(Exception):
    pass


def _json(value: Any) -> str:
    # Escape HTML-comment terminators and HTML metacharacters in the managed section.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")


def _clean(value: str, field: str) -> str:
    text = " ".join(value.replace("\x00", "").split())
    if not text:
        raise TasteNoteError(f"{field} cannot be empty.")
    return text


def _read(path: Path) -> str:
    if path.is_symlink():
        raise TasteNoteError(f"Refusing to follow a symlink: {path}")
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _section(text: str) -> tuple[str, str, str]:
    has_start, has_end = START in text, END in text
    if text.count(START) > 1 or text.count(END) > 1:
        raise TasteNoteError("Managed taste-note markers are duplicated; no data was changed.")
    if has_start != has_end or (has_start and text.index(START) > text.index(END)):
        raise TasteNoteError("Managed taste-note markers are incomplete or out of order; no data was changed.")
    if not has_start:
        return text.rstrip(), "", ""
    before, rest = text.split(START, 1)
    inside, after = rest.split(END, 1)
    return before.rstrip(), inside.strip(), after.lstrip("\r\n")


def _records(inside: str) -> list[dict[str, Any]]:
    records = []
    for match in NOTE_RE.finditer(inside):
        try:
            record = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise TasteNoteError(f"A managed taste note is malformed; no data was changed: {exc}") from exc
        if not isinstance(record, dict) or record.get("kind") not in KINDS or not record.get("id"):
            raise TasteNoteError("A managed taste note has an unsupported schema; no data was changed.")
        records.append(record)
    # A marker section with non-empty content but no recognized records is likely hand-edited/corrupt.
    if inside.strip() and not records:
        raise TasteNoteError("The managed section has no parseable notes; no data was changed.")
    return records


def _display_record(record: dict[str, Any]) -> str:
    topics = ", ".join(record.get("topics", []))
    return "\n".join([
        f"- **{record['id']} · {record['kind']} · {record['status']}** · scope: {html.escape(json.dumps(record['scope'], ensure_ascii=False))} · topics: {html.escape(topics)}",
        f"  - Statement: {html.escape(json.dumps(record['statement'], ensure_ascii=False))}",
        f"  - Evidence: {html.escape(json.dumps(record['evidence'], ensure_ascii=False))}",
        *([f"  - Next time: {html.escape(json.dumps(record['next_time'], ensure_ascii=False))}"] if record.get("next_time") else []),
        *([f"  - Superseded: {html.escape(json.dumps(record['superseded_reason'], ensure_ascii=False))} ({record.get('superseded_on', '')})"] if record.get("status") == "superseded" else []),
        f"  <!-- KHAAM_TASTE_NOTE_V1 {_json(record)} -->",
    ])


def _render(before: str, records: list[dict[str, Any]], after: str) -> str:
    content = "\n\n".join(_display_record(r) for r in records)
    managed = f"{START}\n## Structured taste notes (managed by `taste_notes.py`)\n\n{content}\n{END}"
    parts = [x for x in (before, managed, after) if x]
    return "\n\n".join(parts).rstrip() + "\n"


def _atomic_write(path: Path, text: str) -> None:
    if path.is_symlink():
        raise TasteNoteError(f"Refusing to replace a symlink: {path}")
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, tmp_name = tempfile.mkstemp(prefix=".taste-notes-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def add_note(path: Path, *, kind: str, statement: str, scope: str, topics: list[str],
             evidence: str, next_time: str = "") -> dict[str, Any]:
    if kind not in KINDS:
        raise TasteNoteError("Use --kind preference, observed, or verified; use `supersede` to retire an old note.")
    statement = _clean(statement, "--statement")
    scope = _clean(scope, "--scope")
    evidence = _clean(evidence, "--evidence")
    topics = list(dict.fromkeys(_clean(t, "topic") for t in topics if t.strip()))
    if not topics:
        raise TasteNoteError("Provide at least one --topic so the note can be found again.")
    before, inside, after = _section(_read(path))
    rows = _records(inside)
    number = max([0] + [int(r["id"][1:]) for r in rows if re.fullmatch(r"T\d{4,}", r["id"])]) + 1
    record = {
        "id": f"T{number:04d}", "date": date.today().isoformat(), "kind": kind,
        "status": "active", "scope": scope, "topics": topics,
        "statement": statement, "evidence": evidence,
    }
    if next_time.strip():
        record["next_time"] = _clean(next_time, "--next-time")
    rows.append(record)
    _atomic_write(path, _render(before, rows, after))
    return record


def supersede_note(path: Path, note_id: str, reason: str) -> dict[str, Any]:
    reason = _clean(reason, "--reason")
    before, inside, after = _section(_read(path))
    rows = _records(inside)
    for record in rows:
        if record["id"] == note_id:
            if record["status"] == "superseded":
                raise TasteNoteError(f"{note_id} is already superseded.")
            record["status"] = "superseded"
            record["superseded_on"] = date.today().isoformat()
            record["superseded_reason"] = reason
            _atomic_write(path, _render(before, rows, after))
            return record
    raise TasteNoteError(f"No managed taste note with ID {note_id}; nothing was changed.")


def select_notes(path: Path, *, topic: str | None, include_superseded: bool) -> list[dict[str, Any]]:
    _, inside, _ = _section(_read(path))
    rows = _records(inside)
    query = topic.casefold().strip() if topic else ""
    selected = [r for r in rows if (include_superseded or r.get("status") == "active")
                and (not query or query in " ".join([r.get("scope", ""), *r.get("topics", []), r.get("statement", "")]).casefold())]
    order = {"preference": 0, "verified": 1, "observed": 2}
    return sorted(selected, key=lambda r: (order.get(r["kind"], 9), r["id"]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", help=f"managed file (default: {DEFAULT_FILE})")
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("add", help="record an evidence-backed note without replacing existing prose")
    a.add_argument("--kind", required=True, choices=sorted(KINDS))
    a.add_argument("--statement", required=True, help="exact user wording for preference; concise observation otherwise")
    a.add_argument("--scope", required=True, help="where this applies; do not turn a project-specific note into a global rule")
    a.add_argument("--topic", action="append", required=True)
    a.add_argument("--evidence", required=True, help="e.g. user's quoted statement or project/render evidence")
    a.add_argument("--next-time", default="")
    x = sub.add_parser("supersede", help="mark an earlier note outdated but preserve its history")
    x.add_argument("id")
    x.add_argument("--reason", required=True)
    s = sub.add_parser("show", help="show active structured notes, optionally filtered by topic")
    s.add_argument("--topic")
    s.add_argument("--include-superseded", action="store_true")
    args = parser.parse_args(argv)
    path = Path(args.file).expanduser() if args.file else DEFAULT_FILE
    try:
        if args.command == "add":
            record = add_note(path, kind=args.kind, statement=args.statement, scope=args.scope,
                              topics=args.topic, evidence=args.evidence, next_time=args.next_time)
            print(f"Recorded {record['id']} ({record['kind']}, active) in {path}; existing prose was preserved.")
        elif args.command == "supersede":
            record = supersede_note(path, args.id, args.reason)
            print(f"Marked {record['id']} superseded; its evidence and history were preserved in {path}.")
        else:
            rows = select_notes(path, topic=args.topic, include_superseded=args.include_superseded)
            if not rows:
                print("No matching managed taste notes. Existing unstructured prose, if any, remains untouched.")
            else:
                print("Managed notes (the full user-taste.md remains authoritative; this is a focused index):\n")
                for row in rows:
                    print(_display_record(row))
        return 0
    except (TasteNoteError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
