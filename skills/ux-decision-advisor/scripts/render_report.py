#!/usr/bin/env python3
"""Render a compact UXDA report payload (structured v1 or legacy Beta.4) as self-contained HTML.

Standard library only. No network access. Output must stay outside the installed
or public skill source tree.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parents[1]
STRUCTURED_SHELL = BASE / "assets" / "structured-report-shell.html"
LEGACY_SHELL = BASE / "assets" / "report-shell.html"

STRUCTURED_REQUIRED = ("title", "summary", "recommendation", "next_step", "evidence_boundary")
STRUCTURED_COLLECTIONS = ("hypotheses", "findings", "options", "metrics", "evidence", "sections")

LEGACY_REQUIRED = {"title", "recommendation", "next_step"}
LEGACY_COLLECTIONS = {"decision_options", "journey", "findings", "evidence", "opportunities", "scenario_path"}
LEGACY_ONLY_KEYS = {"decision_options", "journey", "opportunities", "scenario_path", "research_summary", "workflow_map", "validation", "analysis_mode", "problem_reframe"}
STRUCTURED_ONLY_KEYS = {"summary", "evidence_boundary", "hypotheses", "options", "metrics", "sections"}


class InputIssue(ValueError):
    pass


def _detect_format(payload: object) -> str:
    if not isinstance(payload, dict):
        raise InputIssue("INPUT_MUST_BE_OBJECT")
    keys = set(payload)
    has_structured = bool(keys & STRUCTURED_ONLY_KEYS)
    has_legacy = bool(keys & LEGACY_ONLY_KEYS)
    if has_structured and has_legacy:
        raise InputIssue("MIXED_REPORT_SCHEMA_UNSUPPORTED")
    if has_structured:
        return "structured"
    if has_legacy:
        return "legacy"
    raise InputIssue("UNKNOWN_OR_EMPTY_REPORT_SCHEMA")


def _require_rows(payload: dict, key: str, maximum: int) -> list[dict]:
    value = payload.get(key, [])
    if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
        raise InputIssue(f"{key} must be a list of objects")
    if len(value) > maximum:
        raise InputIssue(f"{key} exceeds {maximum} rows")
    return value


def _validate_evidence_rows(rows: list[dict], *, reject_placeholders: bool) -> None:
    for row in rows:
        url = row.get("url")
        if not url:
            continue
        parsed = urlsplit(url) if isinstance(url, str) else None
        if parsed is None or parsed.scheme != "https" or not parsed.hostname:
            raise InputIssue("EVIDENCE_URL_MUST_BE_HTTPS")
        if reject_placeholders:
            host = parsed.hostname.lower()
            if host in ("example.com", "example.org", "example.net", "localhost") or host.endswith((".invalid", ".local", ".internal")):
                raise InputIssue("UNVERIFIABLE_OR_PLACEHOLDER_EVIDENCE_URL")
        needed = ("source_status", "source_title", "source_publisher", "source_locator", "source_retrieval_ref", "support_excerpt")
        if row.get("source_status") != "CONTENT_INSPECTED" or any(not isinstance(row.get(k), str) or not row[k].strip() for k in needed):
            raise InputIssue("EVIDENCE_URL_WITHOUT_INSPECTION_RECORD")


def validate_structured(payload: dict) -> dict:
    for key in STRUCTURED_REQUIRED:
        if not isinstance(payload.get(key), str) or not payload[key].strip():
            raise InputIssue(f"REQUIRED_NONEMPTY_STRING:{key}")
    if payload.get("language", "en") not in {"en", "zh"}:
        raise InputIssue("LANGUAGE_MUST_BE_EN_OR_ZH")
    if "synthetic" in payload and type(payload["synthetic"]) is not bool:
        raise InputIssue("SYNTHETIC_MUST_BE_BOOLEAN")
    for key in STRUCTURED_COLLECTIONS:
        _require_rows(payload, key, 60)
    if not any(payload.get(key) for key in STRUCTURED_COLLECTIONS):
        raise InputIssue("AT_LEAST_ONE_CONTENT_SECTION_REQUIRED")
    for section in payload.get("sections", []):
        if not isinstance(section.get("heading"), str) or not section["heading"].strip():
            raise InputIssue("SECTION_HEADING_REQUIRED")
        if not isinstance(section.get("body"), str) or not section["body"].strip():
            raise InputIssue("SECTION_BODY_REQUIRED")
    for metric in payload.get("metrics", []):
        if not isinstance(metric.get("label"), str) or not metric["label"].strip():
            raise InputIssue("METRIC_LABEL_REQUIRED")
        if type(metric.get("n")) is not int or metric["n"] < 0:
            raise InputIssue("METRIC_N_INVALID")
        value = metric.get("value")
        if type(value) not in {int, float} or not math.isfinite(value):
            raise InputIssue("METRIC_VALUE_INVALID")
        if not isinstance(metric.get("unit"), str) or not metric["unit"].strip():
            raise InputIssue("METRIC_UNIT_REQUIRED")
        if not isinstance(metric.get("denominator_note"), str) or not metric["denominator_note"].strip():
            raise InputIssue("METRIC_DENOMINATOR_NOTE_REQUIRED")
    for evidence in payload.get("evidence", []):
        if not isinstance(evidence.get("title"), str) or not evidence["title"].strip():
            raise InputIssue("EVIDENCE_TITLE_REQUIRED")
        if not isinstance(evidence.get("note"), str) or not evidence["note"].strip():
            raise InputIssue("EVIDENCE_NOTE_REQUIRED")
    _validate_evidence_rows(payload.get("evidence", []), reject_placeholders=False)
    return payload


def validate_legacy(payload: dict) -> dict:
    missing = [k for k in sorted(LEGACY_REQUIRED) if not isinstance(payload.get(k), str) or not payload[k].strip()]
    if missing:
        raise InputIssue("Required nonempty strings: " + ", ".join(missing))
    for key in LEGACY_COLLECTIONS:
        _require_rows(payload, key, 40)
    _validate_evidence_rows(payload.get("evidence", []), reject_placeholders=True)

    research = payload.get("research_summary")
    if research is not None:
        if not isinstance(research, dict):
            raise InputIssue("research_summary must be an object")
        for key in ("mechanism", "evidence_status", "decision_condition"):
            if not isinstance(research.get(key), str) or not research[key].strip():
                raise InputIssue(f"research_summary.{key} requires a nonempty statement")
        if research.get("mechanism_status") not in ("observed", "supported", "hypothesis", "unknown"):
            raise InputIssue("research_summary.mechanism_status must be observed/supported/hypothesis/unknown")
        if "focus" in research and not isinstance(research["focus"], str):
            raise InputIssue("research_summary.focus must be a string")

    workflow = payload.get("workflow_map")
    if workflow is not None:
        if not isinstance(workflow, dict) or not isinstance(workflow.get("objective"), str) or not workflow["objective"].strip():
            raise InputIssue("workflow_map.objective required")
        if type(workflow.get("revision")) is not int or workflow["revision"] < 0:
            raise InputIssue("workflow_map.revision invalid")
        nodes = workflow.get("steps")
        if not isinstance(nodes, list) or not 1 <= len(nodes) <= 12:
            raise InputIssue("workflow_map.steps must have 1-12 rows")
        ids: set[str] = set()
        for node in nodes:
            if not isinstance(node, dict) or not isinstance(node.get("id"), str) or not node["id"].strip() or node["id"] in ids:
                raise InputIssue("workflow_map step id invalid or duplicated")
            ids.add(node["id"])
            if not isinstance(node.get("title"), str) or not node["title"].strip():
                raise InputIssue("workflow_map step title required")
            if node.get("state") not in ("candidate", "ready", "active", "completed", "blocked", "paused", "skipped"):
                raise InputIssue("workflow_map step state invalid")
            if type(node.get("confirmed")) is not bool:
                raise InputIssue("workflow_map step confirmed boolean required")
            if node["state"] == "candidate" and node["confirmed"]:
                raise InputIssue("workflow_map candidate cannot be confirmed")
            if node["state"] == "completed" and not node.get("evidence_refs"):
                raise InputIssue("workflow_map completed requires evidence references")
        if workflow.get("current_step") not in ids:
            raise InputIssue("workflow_map.current_step invalid")
        scope = workflow.get("analysis_scope")
        if scope is not None:
            if (
                not isinstance(scope, dict)
                or type(scope.get("confirmed")) is not bool
                or not isinstance(scope.get("detected"), list)
                or not isinstance(scope.get("selected"), list)
                or any(mode not in {"O", "E", "D", "V"} for mode in scope["detected"] + scope["selected"])
                or len(set(scope["selected"])) != len(scope["selected"])
            ):
                raise InputIssue("workflow_map.analysis_scope invalid")
            if not scope["confirmed"] or not scope["selected"]:
                raise InputIssue("UNCONFIRMED_ANALYSIS_SCOPE_CANNOT_RENDER_FULL_REPORT")
            selected = set(scope["selected"])
            content_modes: dict[str, str] = {}
            if payload.get("decision_options"):
                content_modes["D"] = "decision_options"
            if payload.get("journey") or payload.get("findings"):
                content_modes["E"] = "journey/findings"
            if payload.get("opportunities") or payload.get("scenario_path") or payload.get("problem_reframe"):
                content_modes["O"] = "opportunities/scenario_path"
            if payload.get("validation"):
                content_modes["V"] = "validation"
            for mode, field in content_modes.items():
                if mode not in selected:
                    raise InputIssue(f"UNAUTHORIZED_ANALYSIS_SECTION_{mode}: {field}")
            requested = payload.get("analysis_mode")
            if requested in ("O", "E", "D", "V") and requested not in selected:
                raise InputIssue("UNAUTHORIZED_DEFAULT_VIEW")
            if requested == "both" and not {"D", "E"}.issubset(selected):
                raise InputIssue("UNAUTHORIZED_COMBINED_VIEW")
            if requested == "all" and selected != {"O", "E", "D", "V"}:
                raise InputIssue("UNAUTHORIZED_ALL_VIEW")

    v = payload.get("validation")
    if v is not None and not isinstance(v, dict):
        raise InputIssue("validation must be an object")
    if isinstance(v, dict):
        if v.get("evidence_origin") not in ("synthetic", "respondent_observed", "administrative", "unknown"):
            raise InputIssue("validation.evidence_origin required")
        if v.get("update_status") not in ("UPHOLDS", "QUALIFIES", "CHANGES", "DOES_NOT_RESOLVE"):
            raise InputIssue("validation.update_status required")
        if not isinstance(v.get("boundary"), str) or len(v["boundary"].strip()) < 12:
            raise InputIssue("validation.boundary required")
        for k in ("task_outcomes", "themes"):
            if k in v and (not isinstance(v[k], list) or len(v[k]) > 40):
                raise InputIssue(f"validation.{k} must be <=40 rows")
        for row in v.get("task_outcomes", []):
            if not isinstance(row, dict) or not isinstance(row.get("label"), str) or not row["label"].strip():
                raise InputIssue("Task outcome needs a label")
            n, rate = row.get("n"), row.get("success_pct")
            if type(n) is not int or n <= 0 or type(rate) not in (int, float) or not math.isfinite(rate) or not (0 <= rate <= 100):
                raise InputIssue("Task outcome requires valid n and percentage")
        if v.get("task_outcomes") and not isinstance(v.get("quant_note"), str):
            raise InputIssue("Task results require quant_note with denominator and scope")
        for row in v.get("themes", []):
            if not isinstance(row, dict) or not isinstance(row.get("code"), str) or not row["code"].strip():
                raise InputIssue("Coded theme needs name")
            m, n = row.get("mentions"), row.get("respondents")
            if type(m) is not int or type(n) is not int or m < 0 or n < 0 or n > m:
                raise InputIssue("Coded theme counts invalid")

    if not (payload.get("decision_options") or payload.get("journey") or payload.get("findings") or payload.get("opportunities") or payload.get("validation")):
        raise InputIssue("At least one analysis section is required (D/E/O/V)")
    return payload


def validate(payload: object) -> dict:
    fmt = _detect_format(payload)
    assert isinstance(payload, dict)
    if fmt == "structured":
        return validate_structured(payload)
    return validate_legacy(payload)


def render(payload: dict) -> str:
    fmt = _detect_format(payload)
    shell_path = STRUCTURED_SHELL if fmt == "structured" else LEGACY_SHELL
    template = shell_path.read_text(encoding="utf-8")
    if template.count("__JSON_DATA__") != 1:
        raise InputIssue("REPORT_TEMPLATE_MARKER_INVALID")
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return template.replace("__JSON_DATA__", data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        output = args.output.resolve()
        input_abs = args.input.resolve()
        source = BASE.resolve()
        if output == input_abs:
            raise InputIssue("OUTPUT_OVERWRITES_INPUT")
        if output.exists() and args.input.exists() and os.path.samefile(output, args.input):
            raise InputIssue("OUTPUT_OVERWRITES_INPUT")
        if output == source or source in output.parents:
            raise InputIssue("OUTPUT_INSIDE_SKILL_SOURCE")
        for folder in (output.parent, *output.parents):
            if (folder / "PUBLIC_FILE_MANIFEST.json").exists():
                raise InputIssue("OUTPUT_INSIDE_PUBLIC_REPO")
        payload = validate(json.loads(args.input.read_text(encoding="utf-8")))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render(payload), encoding="utf-8")
    except Exception as exc:
        code = str(exc) if isinstance(exc, InputIssue) else "INVALID_JSON_OR_PROCESSING_ERROR"
        print("REPORT_FAIL:", code, file=sys.stderr)
        return 2
    print(f"REPORT_OK output={args.output} bytes={args.output.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
