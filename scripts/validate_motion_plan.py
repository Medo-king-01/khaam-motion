#!/usr/bin/env python3
"""Validate a Khaam HyperFrames scene plan against the local motion catalog.

This is a read-only planning check: it does not edit compositions, resolve cues,
render video, add approval steps, or certify content/visual quality.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "templates" / "hyperframes" / "motion-catalog.json"


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read {path}: {exc}") from exc


def _check_value(value: Any, rule: dict[str, Any], label: str, errors: list[str]) -> None:
    kind = rule.get("type")
    valid = True
    if kind == "string":
        valid = isinstance(value, str)
        if valid:
            if len(value) < rule.get("minLength", 0): errors.append(f"{label}: shorter than minLength.")
            if len(value) > rule.get("maxLength", math.inf): errors.append(f"{label}: exceeds maxLength.")
    elif kind == "anchor":
        valid = ((isinstance(value, str) and bool(value.strip())) or
                 (isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)))
    elif kind in ("number", "integer"):
        valid = isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
        if kind == "integer": valid = valid and isinstance(value, int)
        if valid:
            if "minimum" in rule and value < rule["minimum"]: errors.append(f"{label}: below minimum {rule['minimum']}.")
            if "maximum" in rule and value > rule["maximum"]: errors.append(f"{label}: above maximum {rule['maximum']}.")
    elif kind == "array":
        valid = isinstance(value, list)
        if valid:
            if len(value) < rule.get("minItems", 0): errors.append(f"{label}: needs at least {rule['minItems']} item(s).")
            if len(value) > rule.get("maxItems", math.inf): errors.append(f"{label}: exceeds maxItems {rule['maxItems']}.")
            item_rule = rule.get("items")
            if item_rule:
                for index, item in enumerate(value): _check_value(item, item_rule, f"{label}[{index}]", errors)
    elif kind == "object":
        valid = isinstance(value, dict)
        if valid:
            props = rule.get("properties", {})
            for name in rule.get("required", []):
                if name not in value: errors.append(f"{label}.{name}: required field is missing.")
            for name in value:
                if name not in props:
                    errors.append(f"{label}.{name}: field is not in the catalog schema.")
            for name, child_rule in props.items():
                if name in value: _check_value(value[name], child_rule, f"{label}.{name}", errors)
    else:
        errors.append(f"{label}: catalog uses unsupported type {kind!r}.")
        return
    if not valid:
        expected = "finite number or cue string" if kind == "anchor" else kind
        errors.append(f"{label}: expected {expected}.")
        return
    if kind == "string" and isinstance(value, str) and "enum" in rule and value not in rule["enum"]:
        errors.append(f"{label}: choose one of {', '.join(rule['enum'])}.")
    if kind in ("number", "integer") and isinstance(value, (int, float)) and not isinstance(value, bool):
        if "enum" in rule and value not in rule["enum"]: errors.append(f"{label}: value is not an allowed option.")


def _catalog_map(catalog: dict[str, Any], errors: list[str]) -> dict[str, dict[str, Any]]:
    templates = catalog.get("templates")
    if not isinstance(templates, list) or not templates:
        errors.append("Catalog must contain a non-empty templates array.")
        return {}
    result = {}
    for item in templates:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            errors.append("Catalog contains a template without a string id.")
            continue
        template_id = item["id"]
        if template_id in result: errors.append(f"Catalog repeats template id {template_id!r}.")
        result[template_id] = item
        audit = item.get("layoutAudit", {})
        if not audit.get("subjectSelectors") or not audit.get("frameSelectors"):
            errors.append(f"Catalog {template_id}: layoutAudit needs subjectSelectors and frameSelectors.")
        source = ROOT / "templates" / "hyperframes" / item.get("source", "")
        if not source.is_file(): errors.append(f"Catalog {template_id}: composition source does not exist: {source}.")
    return result


def validate_plan(plan: Any, catalog: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(catalog, dict): return ["Catalog root must be an object."]
    templates = _catalog_map(catalog, errors)
    if not isinstance(plan, dict): return errors + ["Plan root must be an object."]
    allowed_top = {"version", "project", "aspectRatio", "scenes"}
    for key in set(plan) - allowed_top: errors.append(f"Plan: unsupported top-level field {key!r}.")
    if not isinstance(plan.get("version"), int) or isinstance(plan.get("version"), bool) or plan["version"] != 1:
        errors.append("Plan version must be integer 1.")
    if not isinstance(plan.get("project"), str) or not plan["project"].strip() or len(plan["project"]) > 100:
        errors.append("Plan project must be a non-empty string of at most 100 characters.")
    if plan.get("aspectRatio") not in {"9:16", "16:9", "1:1"}:
        errors.append("aspectRatio must be 9:16, 16:9, or 1:1.")
    scenes = plan.get("scenes")
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 40:
        errors.append("Plan scenes must contain between 1 and 40 entries.")
        return errors
    seen: set[str] = set()
    allowed_scene = {"id", "templateId", "timing", "sourceQuote", "intent", "layoutMode",
                     "requiredInformation", "forbiddenInformation", "variables", "note"}
    for index, scene in enumerate(scenes):
        label = f"scenes[{index}]"
        if not isinstance(scene, dict):
            errors.append(f"{label}: expected an object.")
            continue
        for key in set(scene) - allowed_scene: errors.append(f"{label}: unsupported field {key!r}.")
        for key in ("id", "templateId", "sourceQuote", "intent", "layoutMode"):
            if not isinstance(scene.get(key), str) or not scene[key].strip():
                errors.append(f"{label}.{key}: required non-empty string.")
            elif len(scene[key]) > {"id": 80, "templateId": 80, "sourceQuote": 500, "intent": 240, "layoutMode": 40}[key]:
                errors.append(f"{label}.{key}: exceeds its maximum length.")
        if isinstance(scene.get("id"), str):
            if scene["id"] in seen: errors.append(f"{label}.id: duplicate scene id {scene['id']!r}.")
            seen.add(scene["id"])
        quote = scene.get("sourceQuote")
        if isinstance(quote, str) and len(quote) > 500: errors.append(f"{label}.sourceQuote: exceeds 500 characters.")
        for list_name in ("requiredInformation", "forbiddenInformation"):
            items = scene.get(list_name)
            if not isinstance(items, list) or not 1 <= len(items) <= 12 or any(not isinstance(x, str) or not x.strip() for x in items):
                errors.append(f"{label}.{list_name}: needs 1–12 non-empty strings.")
        timing = scene.get("timing")
        if not isinstance(timing, dict):
            errors.append(f"{label}.timing: expected start/end cues or seconds.")
        else:
            cue_keys, sec_keys = {"startCue", "endCue"}, {"startSeconds", "endSeconds"}
            if set(timing) == cue_keys:
                if any(not isinstance(timing[k], str) or not timing[k].strip() for k in cue_keys): errors.append(f"{label}.timing: cue anchors must be non-empty strings.")
            elif set(timing) == sec_keys:
                a, b = timing["startSeconds"], timing["endSeconds"]
                if any(not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x) or x < 0 for x in (a, b)):
                    errors.append(f"{label}.timing: seconds must be finite and non-negative.")
                elif b <= a: errors.append(f"{label}.timing: endSeconds must be greater than startSeconds.")
            else: errors.append(f"{label}.timing: use either startCue/endCue or startSeconds/endSeconds, not a mixture.")
        template = templates.get(scene.get("templateId"))
        if template is None:
            errors.append(f"{label}.templateId: unknown catalog id {scene.get('templateId')!r}.")
            continue
        if plan.get("aspectRatio") not in catalog.get("aspectRatios", ["9:16"]):
            errors.append(f"{label}: catalog compositions currently support {', '.join(catalog.get('aspectRatios', ['9:16']))}; no automatic crop is provided.")
        if scene.get("layoutMode") not in template.get("layoutModes", []):
            errors.append(f"{label}.layoutMode: {scene.get('layoutMode')!r} is not supported by {template['id']}.")
        if "note" in scene and (not isinstance(scene["note"], str) or len(scene["note"]) > 240):
            errors.append(f"{label}.note: must be a string of at most 240 characters.")
        variables = scene.get("variables")
        if not isinstance(variables, dict):
            errors.append(f"{label}.variables: expected an object.")
        else:
            schema = template.get("variables", {})
            for name in schema.get("required", []):
                if name not in variables: errors.append(f"{label}.variables.{name}: required by catalog template.")
            for name in variables:
                if name not in schema.get("properties", {}): errors.append(f"{label}.variables.{name}: not declared for {template['id']}.")
            for name, rule in schema.get("properties", {}).items():
                if name in variables: _check_value(variables[name], rule, f"{label}.variables.{name}", errors)
            if template["id"] == "verified-card":
                card = variables.get("card", {})
                if isinstance(card, dict) and card.get("second") and not card.get("secondCredit"):
                    errors.append(f"{label}.variables.card.secondCredit: required when a translation is supplied.")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", help="motion-plan.json")
    parser.add_argument("--catalog", default=str(DEFAULT_CATALOG), help="local motion-catalog.json")
    parser.add_argument("--json", action="store_true", help="emit machine-readable validation results")
    args = parser.parse_args(argv)
    try:
        plan = _read_json(Path(args.plan))
        catalog = _read_json(Path(args.catalog))
        errors = validate_plan(plan, catalog)
    except ValueError as exc:
        errors = [str(exc)]
    if args.json:
        print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    elif errors:
        print("Motion plan needs fixes:")
        for error in errors: print("- " + error)
    else:
        print(f"Motion plan valid: {len(plan['scenes'])} scene(s) · catalogue-only check; no cue resolution or render was performed.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
