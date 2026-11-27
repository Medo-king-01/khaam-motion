#!/usr/bin/env python3
"""Private, non-blocking history of Khaam visual motifs and frame fingerprints.

Stores descriptors and user-supplied labels only, never frame pixels or source paths.
Use `check` as a reminder, not a blacklist: an intentional approved visual repeat is valid.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import visual_reference  # noqa: E402

DEFAULT_LEDGER = Path.home() / ".cache" / "khaam-motion" / "visual-ledger.jsonl"


class LedgerError(Exception):
    pass


def _ledger_path(raw: str | None) -> Path:
    return Path(raw).expanduser() if raw else DEFAULT_LEDGER


def read_rows(path: Path) -> list[dict[str, Any]]:
    if path.is_symlink():
        raise LedgerError(f"Refusing to follow a symlink ledger: {path}")
    if not path.exists():
        return []
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise LedgerError(f"Invalid JSON on ledger line {number}; no data was changed: {exc}") from exc
        if not isinstance(row, dict) or not isinstance(row.get("project"), str):
            raise LedgerError(f"Unexpected ledger record on line {number}; no data was changed.")
        rows.append(row)
    return rows


def add_record(frame: str, *, project: str, version: str, style: str, motif: str, motion: str,
               aspect: str, source: str, note: str, ledger: Path) -> dict[str, Any]:
    if not project.strip() or not motif.strip():
        raise LedgerError("--project and --motif must be non-empty.")
    if not style.strip() or not motion.strip():
        raise LedgerError("--style and --motion must be non-empty (use 'none' when appropriate).")
    if "://" in source.casefold():
        raise LedgerError("--source is a short label, not a URL; no URL was recorded.")
    rows = read_rows(ledger)
    if any(r.get("project") == project and r.get("version") == version for r in rows):
        raise LedgerError(f"{project} v{version} is already recorded; choose a distinct version. Nothing was overwritten.")
    try:
        image_metrics = visual_reference.measure(frame)
    except (RuntimeError, ValueError, OSError) as exc:
        raise LedgerError(str(exc)) from exc
    record = {
        "schema": 1,
        "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "project": project.strip(),
        "version": version.strip(),
        "aspect": aspect.strip() or "unspecified",
        "style": style.strip(),
        "motif": motif.strip(),
        "motion": motion.strip(),
        "source_reference": source.strip(),
        "note": note.strip(),
        "frame_metrics": {
            "size": image_metrics["size"],
            "aspect_ratio": image_metrics["aspect"],
            "palette": image_metrics["palette"],
            "edge_density_by_vertical_band": image_metrics["edge_density_by_vertical_band"],
            "coarse_layout_signature": image_metrics["coarse_layout_signature"],
        },
    }
    ledger.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if ledger.is_symlink():
        raise LedgerError(f"Refusing to write through a symlink ledger: {ledger}")
    # A new per-user history file should not be world-readable on POSIX.
    fd = os.open(ledger, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(fd, "a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    return record


def _normal(value: str) -> str:
    return " ".join(value.casefold().split())


def check_frame(frame: str, rows: list[dict[str, Any]], *, motif: str | None, last: int) -> list[dict[str, Any]]:
    current = visual_reference.measure(frame)
    candidates = rows[-last:] if last else rows
    reports = []
    for row in reversed(candidates):
        metrics = row.get("frame_metrics") or {}
        if not metrics.get("palette") or not metrics.get("coarse_layout_signature"):
            continue
        old = {"aspect": metrics.get("aspect_ratio", 0),
               "palette": metrics["palette"],
               "coarse_layout_signature": metrics["coarse_layout_signature"]}
        sim = visual_reference.similarity(current, old)
        motif_match = bool(motif and _normal(motif) == _normal(row.get("motif", "")))
        signals = []
        if sim["same_aspect_ratio"] and sim["palette_distance"] <= 0.10:
            signals.append("close palette")
        if sim["same_aspect_ratio"] and sim["layout_cosine"] is not None and sim["layout_cosine"] >= 0.86:
            signals.append("similar coarse layout")
        if motif_match:
            signals.append("same named motif")
        reports.append({"project": row.get("project"), "version": row.get("version"),
                        "style": row.get("style"), "motif": row.get("motif"),
                        "motion": row.get("motion"), "comparison": sim,
                        "signals": signals, "review": "Reminder only; not a block or a quality score."})
    return reports


def _print_rows(rows: list[dict[str, Any]], last: int) -> None:
    chosen = rows[-last:] if last else rows
    if not chosen:
        print("Visual ledger is empty. It is optional and records descriptors, not frames.")
        return
    print(f"Most recent {len(chosen)} visual records (local/private metadata):")
    for row in chosen:
        colors = ", ".join(c.get("hex", "") for c in (row.get("frame_metrics", {}).get("palette") or [])[:3])
        print(f"- {row.get('project')} v{row.get('version')} · {row.get('aspect')} · {row.get('style')}")
        print(f"  motif: {row.get('motif')} · motion: {row.get('motion')} · colors: {colors}")
        if row.get("source_reference"):
            print(f"  source note: {row['source_reference']}")
        if row.get("note"):
            print(f"  note: {row['note']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("add", help="record one approved still's visual metadata")
    a.add_argument("frame", help="local frame image; it is analyzed, not copied")
    a.add_argument("--project", required=True)
    a.add_argument("--version", default="1")
    a.add_argument("--aspect", default="unspecified", help="e.g. 9:16 or 16:9")
    a.add_argument("--style", required=True)
    a.add_argument("--motif", required=True)
    a.add_argument("--motion", required=True)
    a.add_argument("--source", default="", help="short reference label; do not put a private URL")
    a.add_argument("--note", default="")
    a.add_argument("--ledger", help=f"ledger path (default: {DEFAULT_LEDGER})")
    s = sub.add_parser("show", help="show recent style metadata")
    s.add_argument("--last", type=int, default=12)
    s.add_argument("--ledger", help=f"ledger path (default: {DEFAULT_LEDGER})")
    c = sub.add_parser("check", help="compare a candidate still to recent metadata")
    c.add_argument("frame")
    c.add_argument("--motif", help="candidate motif; exact normalized match is reported")
    c.add_argument("--last", type=int, default=12)
    c.add_argument("--ledger", help=f"ledger path (default: {DEFAULT_LEDGER})")
    args = parser.parse_args(argv)
    if getattr(args, "last", 1) < 1:
        parser.error("--last must be at least 1")
    path = _ledger_path(getattr(args, "ledger", None))
    try:
        rows = read_rows(path)
        if args.command == "show":
            _print_rows(rows, args.last)
            return 0
        if args.command == "check":
            if not rows:
                print("Visual ledger is empty; no comparison available. Nothing was changed.")
                return 0
            for report in check_frame(args.frame, rows, motif=args.motif, last=args.last):
                mark = "SIGNAL" if report["signals"] else "—"
                print(f"{mark} {report['project']} v{report['version']} · {', '.join(report['signals']) or 'no strong match signal'}")
                print(f"  palette distance={report['comparison']['palette_distance']}; layout cosine={report['comparison']['layout_cosine']}")
            print("These are prompts for visual review, not originality, quality, or rights checks. Similar work may be intentional.")
            return 0
        record = add_record(args.frame, project=args.project, version=args.version,
                            style=args.style, motif=args.motif, motion=args.motion,
                            aspect=args.aspect, source=args.source, note=args.note, ledger=path)
        print(f"Recorded {record['project']} v{record['version']} in {path}; only descriptive metadata/signatures stored, not the image path or pixels.")
        return 0
    except (LedgerError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
