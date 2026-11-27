#!/usr/bin/env python3
"""Describe and compare still-frame visual structure without scoring its quality.

Local-only: reads image files, performs no network access, and never modifies inputs.
Pillow is optional and is only needed when this helper is run. The measurements are
signals for human comparison, not artistic judgements or copy targets.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def _pillow():
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageOps
    except ImportError as exc:
        raise RuntimeError(
            "This helper needs Pillow. Follow Khaam's normal permission-gated setup "
            "for optional Python packages; nothing was installed."
        ) from exc
    return Image, ImageDraw, ImageFilter, ImageOps


def _load(path: str | Path):
    Image, _, _, ImageOps = _pillow()
    src = Path(path).expanduser()
    if not src.is_file():
        raise ValueError(f"Image not found: {src}")
    try:
        with Image.open(src) as im:
            return ImageOps.exif_transpose(im).convert("RGB")
    except Exception as exc:
        raise ValueError(f"Cannot read image {src}: {exc}") from exc


def palette(image, limit: int = 6) -> list[dict[str, Any]]:
    """Return reproducible dominant colours and their approximate pixel shares."""
    Image, _, _, _ = _pillow()
    sample = image.convert("RGB").resize((128, 128), Image.Resampling.LANCZOS)
    quantized = sample.quantize(colors=limit, method=Image.Quantize.MEDIANCUT)
    counts = quantized.getcolors(128 * 128) or []
    colors = quantized.getpalette()
    total = sum(n for n, _ in counts) or 1
    out = []
    for count, index in sorted(counts, reverse=True):
        rgb = tuple(colors[index * 3:index * 3 + 3])
        out.append({"hex": "#%02X%02X%02X" % rgb, "rgb": list(rgb), "share": round(count / total, 4)})
    return out


def _cosine(a: list[float], b: list[float]) -> float:
    denom = math.sqrt(sum(x * x for x in a) * sum(x * x for x in b))
    if not denom:
        return 1.0 if not any(a) and not any(b) else 0.0
    return max(-1.0, min(1.0, sum(x * y for x, y in zip(a, b)) / denom))


def measure_image(image, bands: int = 10, grid: tuple[int, int] = (4, 8)) -> dict[str, Any]:
    """Extract colour and coarse edge-density descriptors from an already-open image."""
    Image, _, ImageFilter, _ = _pillow()
    w, h = image.size
    # Edge density is a rough proxy for where visual detail lives, not a text/content detector.
    edge = image.convert("L").resize((grid[0] * 12, grid[1] * 12), Image.Resampling.LANCZOS)
    edge = edge.filter(ImageFilter.FIND_EDGES)
    px = list(edge.tobytes())
    cells = []
    for gy in range(grid[1]):
        for gx in range(grid[0]):
            values = [px[y * edge.width + x]
                      for y in range(gy * 12, (gy + 1) * 12)
                      for x in range(gx * 12, (gx + 1) * 12)]
            cells.append(sum(values) / (len(values) * 255))
    total = sum(cells) or 1.0
    norm_cells = [round(x / total, 5) for x in cells]
    bands_out = []
    for row in range(bands):
        y0 = round(row * edge.height / bands)
        y1 = max(y0 + 1, round((row + 1) * edge.height / bands))
        vals = [px[y * edge.width + x] for y in range(y0, min(y1, edge.height)) for x in range(edge.width)]
        bands_out.append(sum(vals) / (len(vals) * 255) if vals else 0.0)
    bands_total = sum(bands_out) or 1.0
    bands_out = [round(x / bands_total, 5) for x in bands_out]
    return {
        "size": [w, h],
        "aspect": round(w / h, 5) if h else 0,
        "palette": palette(image),
        "edge_density_by_vertical_band": bands_out,
        "coarse_layout_signature": norm_cells,
        "measurement_note": "Palette and edge-distribution descriptors only; not a quality score or semantic analysis.",
    }


def measure(path: str | Path) -> dict[str, Any]:
    return measure_image(_load(path))


def palette_distance(a: list[dict[str, Any]], b: list[dict[str, Any]]) -> float:
    """A simple normalized weighted nearest-colour difference (0 is closest)."""
    if not a or not b:
        return 1.0
    def directed(left, right):
        total = 0.0
        weight = 0.0
        for color in left:
            rgb = color["rgb"]
            nearest = min(math.sqrt(sum((rgb[i] - other["rgb"][i]) ** 2 for i in range(3))) / math.sqrt(3 * 255 ** 2)
                          for other in right)
            share = float(color.get("share", 0))
            total += nearest * share
            weight += share
        return total / weight if weight else 1.0
    return round((directed(a, b) + directed(b, a)) / 2, 5)


def similarity(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    la, lb = a["coarse_layout_signature"], b["coarse_layout_signature"]
    same_shape = len(la) == len(lb) and a["aspect"] > 0 and b["aspect"] > 0
    return {
        "same_aspect_ratio": abs(a["aspect"] - b["aspect"]) <= 0.02,
        "palette_distance": palette_distance(a["palette"], b["palette"]),
        "layout_cosine": round(_cosine(la, lb), 5) if same_shape else None,
        "interpretation": "Signals for a person to inspect side by side. Similarity is not quality, originality, or permission to reuse.",
    }


def make_comparison_card(reference, result, out_path: str | Path, labels=("REFERENCE", "KHAAAM FRAME")) -> None:
    Image, ImageDraw, _, _ = _pillow()
    # Portrait/landscape images fit the same box without cropping. Input files remain untouched.
    box_w, box_h = 640, 700
    pad, label_h, footer_h = 24, 34, 190
    canvas = Image.new("RGB", (pad * 3 + box_w * 2, pad * 2 + label_h * 2 + box_h + footer_h), "#17191d")
    draw = ImageDraw.Draw(canvas)
    start_y = pad
    for i, (img, label) in enumerate(((reference, labels[0]), (result, labels[1]))):
        x = pad + i * (box_w + pad)
        safe_label = label.encode("ascii", "replace").decode("ascii")
        draw.text((x, start_y), safe_label, fill="#f2f2f2")
        thumb = img.copy()
        thumb.thumbnail((box_w, box_h), Image.Resampling.LANCZOS)
        bg = Image.new("RGB", (box_w, box_h), "#25282e")
        bg.paste(thumb, ((box_w - thumb.width) // 2, (box_h - thumb.height) // 2))
        canvas.paste(bg, (x, start_y + label_h))
    y = start_y + label_h + box_h + 18
    draw.text((pad, y), "DOMINANT COLOURS (approximate area)", fill="#d0d3d9")
    y += 22
    for i, (img, _) in enumerate(((reference, labels[0]), (result, labels[1]))):
        x = pad + i * (box_w + pad)
        colors = palette(img)
        cursor = x
        for item in colors:
            width = max(1, round(box_w * item["share"]))
            draw.rectangle((cursor, y, min(cursor + width, x + box_w), y + 18), fill=item["hex"])
            cursor += width
            if cursor >= x + box_w:
                break
    y += 28
    draw.text((pad, y), "VERTICAL EDGE DENSITY · TOP TO BOTTOM", fill="#d0d3d9")
    y += 22
    for i, img in enumerate((reference, result)):
        stats = measure_image(img)
        x = pad + i * (box_w + pad)
        vals = stats["edge_density_by_vertical_band"]
        gap = 2
        width = (box_w - gap * (len(vals) - 1)) / len(vals)
        for j, val in enumerate(vals):
            bar_h = max(2, round(34 * min(1.0, val * len(vals) * 1.8)))
            bx = x + round(j * (width + gap))
            draw.rectangle((bx, y + 34 - bar_h, bx + max(1, round(width)), y + 34), fill="#9eb4d0")
    dest = Path(out_path).expanduser()
    if dest.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        raise ValueError("Comparison output must use .png, .jpg, or .jpeg.")
    if dest.exists():
        raise FileExistsError(f"Refusing to overwrite existing comparison: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.suffix.lower() in {".jpg", ".jpeg"}:
        canvas.save(dest, quality=90)
    else:
        canvas.save(dest, format="PNG")


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    m = sub.add_parser("measure", help="measure local image(s), no network")
    m.add_argument("images", nargs="+")
    m.add_argument("--json", action="store_true")
    c = sub.add_parser("compare", help="compare two images and make a visual card")
    c.add_argument("--reference", required=True)
    c.add_argument("--result", required=True)
    c.add_argument("--out", required=True, help="new output image path; never overwrites")
    c.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "measure":
            result = {str(Path(p).expanduser()): measure(p) for p in args.images}
            if args.json:
                _print_json(result)
            else:
                for path, item in result.items():
                    colors = ", ".join(f"{c['hex']} {c['share']:.0%}" for c in item["palette"][:5])
                    bands = " ".join(f"{v:.0%}" for v in item["edge_density_by_vertical_band"])
                    print(f"{path} · {item['size'][0]}×{item['size'][1]} · palette {colors}")
                    print(f"  edge density by vertical band: {bands}")
                    print(f"  {item['measurement_note']}")
            return 0
        reference = _load(args.reference)
        result = _load(args.result)
        m_ref, m_result = measure_image(reference), measure_image(result)
        stats = similarity(m_ref, m_result)
        make_comparison_card(reference, result, args.out)
        payload = {"reference": m_ref, "result": m_result, "comparison": stats, "card": str(Path(args.out).expanduser())}
        if args.json:
            _print_json(payload)
        else:
            print(f"Comparison card: {payload['card']}")
            print(f"Aspect ratios close: {stats['same_aspect_ratio']} · palette distance: {stats['palette_distance']} · coarse layout cosine: {stats['layout_cosine']}")
            print(stats["interpretation"])
        return 0
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
