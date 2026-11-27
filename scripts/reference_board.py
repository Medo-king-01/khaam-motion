#!/usr/bin/env python3
"""Make an offline contact sheet from local image references or sampled frames.

Sources are only read, never copied or edited. The output is a reference-only
visual aid; it does not grant permission to reuse any source material.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}


def _pillow():
    try:
        from PIL import Image, ImageDraw, ImageOps
    except ImportError as exc:
        raise RuntimeError(
            "This helper needs Pillow. Follow Khaam's normal permission-gated setup "
            "for optional Python packages; nothing was installed."
        ) from exc
    return Image, ImageDraw, ImageOps


def expand_sources(raw_sources: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in raw_sources:
        path = Path(raw).expanduser()
        if path.is_dir():
            found.extend(sorted(p for p in path.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS))
        elif path.is_file() and path.suffix.lower() in EXTENSIONS:
            found.append(path)
        else:
            raise ValueError(f"Not a supported local image or directory: {raw}")
    # Deduplicate without changing order. Do not follow directories recursively.
    unique: list[Path] = []
    seen: set[str] = set()
    for path in found:
        resolved = str(path.resolve())
        if resolved not in seen:
            unique.append(path)
            seen.add(resolved)
    if not unique:
        raise ValueError("No supported images found.")
    if len(unique) > 36:
        raise ValueError(f"Found {len(unique)} images; limit is 36 per board. Pass a smaller, intentional set.")
    return unique


def build_board(paths: list[Path], out: Path, *, title: str, labels: list[str], cols: int = 3,
                cell_width: int = 420, cell_height: int = 520) -> tuple[Path, Path]:
    Image, ImageDraw, ImageOps = _pillow()
    if not 1 <= cols <= 6:
        raise ValueError("Columns must be 1–6.")
    if not 160 <= cell_width <= 1200 or not 160 <= cell_height <= 1600:
        raise ValueError("Cell dimensions are outside the safe range.")
    if labels and len(labels) != len(paths):
        raise ValueError("Provide exactly one --label per expanded input image, or none.")
    out = out.expanduser()
    map_path = out.with_name(out.stem + ".sources.md")
    if out.exists() or map_path.exists():
        raise FileExistsError(f"Board or source map already exists; refusing to overwrite: {out}")
    gap, head_h, caption_h = 18, 56, 52
    rows = (len(paths) + cols - 1) // cols
    board = Image.new(
        "RGB",
        (gap + cols * (cell_width + gap), gap + head_h + rows * (cell_height + caption_h + gap)),
        "#17191d",
    )
    draw = ImageDraw.Draw(board)
    draw.text((gap, gap), title[:140], fill="#f4f4f4")
    records = ["# Reference board source map", "", "Reference-only: these entries identify local inputs; no rights to reuse them are implied.", ""]
    for index, path in enumerate(paths, 1):
        try:
            with Image.open(path) as source:
                image = ImageOps.exif_transpose(source).convert("RGB")
                image.load()
        except Exception as exc:
            raise ValueError(f"Cannot decode {path.name}: {exc}") from exc
        col, row = (index - 1) % cols, (index - 1) // cols
        x = gap + col * (cell_width + gap)
        y = gap + head_h + row * (cell_height + caption_h + gap)
        image.thumbnail((cell_width - 20, cell_height - 20), Image.Resampling.LANCZOS)
        tile = Image.new("RGB", (cell_width, cell_height), "#292c32")
        tile.paste(image, ((cell_width - image.width) // 2, (cell_height - image.height) // 2))
        board.paste(tile, (x, y))
        # Pillow's default font is not a shaping engine. Keep the tile label ASCII-safe;
        # the adjacent source map preserves the original Unicode name and description.
        safe_name = path.name.encode("ascii", "replace").decode("ascii")[:42]
        draw.text((x + 4, y + cell_height + 7), f"{index:02d} · {safe_name}", fill="#f2f2f2")
        label = labels[index - 1].replace("\n", " ").strip() if labels else ""
        if label:
            draw.text((x + 4, y + cell_height + 26), label.encode("ascii", "replace").decode("ascii")[:54], fill="#bec6d2")
        hasher = hashlib.sha256()
        with path.open("rb") as source_file:
            for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
                hasher.update(chunk)
        digest = hasher.hexdigest()
        records.extend([
            f"## {index:02d} · {labels[index - 1] if labels else path.name}",
            f"- Input name: `{path.name}`",
            f"- SHA-256: `{digest}`",
            "",
        ])
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() in {".jpg", ".jpeg"}:
        board.save(out, quality=90)
    else:
        board.save(out, format="PNG")
    map_path.write_text("\n".join(records), encoding="utf-8")
    return out, map_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", help="local image files and/or non-recursive directories")
    parser.add_argument("--out", required=True, help="new board path; existing outputs are never overwritten")
    parser.add_argument("--title", default="Khaam · Reference board")
    parser.add_argument("--label", action="append", default=[], help="one optional label per expanded image")
    parser.add_argument("--cols", type=int, default=3)
    parser.add_argument("--cell-width", type=int, default=420)
    parser.add_argument("--cell-height", type=int, default=520)
    args = parser.parse_args(argv)
    try:
        paths = expand_sources(args.sources)
        out, mapping = build_board(paths, Path(args.out), title=args.title, labels=args.label,
                                   cols=args.cols, cell_width=args.cell_width, cell_height=args.cell_height)
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Board: {out}\nSource map: {mapping}\nInputs: {len(paths)} · read-only · local-only · reference-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
