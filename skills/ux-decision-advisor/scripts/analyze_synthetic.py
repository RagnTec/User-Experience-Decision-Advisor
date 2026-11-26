#!/usr/bin/env python3
"""Descriptive, reproducible analysis of a participant-condition-task CSV.

No network, no automatic deletion, no inferential p-values. Intended for clearly
labeled synthetic demonstrations or explicitly authorized local data.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REQUIRED = {"participant_id", "condition", "task", "success", "duration_seconds"}
MISSING = {"", "na", "n/a", "null", "none", "nan"}
SKILL_ROOT = Path(__file__).resolve().parents[1]


class InputIssue(ValueError):
    pass


def parse_bool(value: str) -> bool | None:
    v = value.strip().casefold()
    if v in {"1", "true", "yes", "y"}:
        return True
    if v in {"0", "false", "no", "n"}:
        return False
    if v in MISSING:
        return None
    raise InputIssue("INVALID_SUCCESS_VALUE")


def parse_duration(value: str) -> float | None:
    v = value.strip().casefold()
    if v in MISSING:
        return None
    try:
        number = float(v)
    except ValueError as exc:
        raise InputIssue("INVALID_DURATION_VALUE") from exc
    if not math.isfinite(number) or number < 0:
        raise InputIssue("INVALID_DURATION_VALUE")
    return number


def percentile(values: list[float], q: float) -> float:
    if not values:
        raise InputIssue("EMPTY_PERCENTILE_INPUT")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def describe(values: list[float]) -> dict[str, Any] | None:
    if not values:
        return None
    q1 = percentile(values, 0.25)
    q3 = percentile(values, 0.75)
    return {
        "n": len(values),
        "mean": round(statistics.fmean(values), 6),
        "median": round(statistics.median(values), 6),
        "q1": round(q1, 6),
        "q3": round(q3, 6),
        "min": round(min(values), 6),
        "max": round(max(values), 6),
    }


def read_rows(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not path.is_file():
        raise InputIssue("INPUT_NOT_A_FILE")
    raw = path.read_bytes()
    if len(raw) > 20_000_000:
        raise InputIssue("INPUT_TOO_LARGE")
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    fields = reader.fieldnames or []
    missing = sorted(REQUIRED - set(fields))
    if missing:
        raise InputIssue("MISSING_COLUMNS:" + ",".join(missing))
    rows: list[dict[str, Any]] = []
    seen: Counter[tuple[str, str, str]] = Counter()
    for line_no, source in enumerate(reader, 2):
        if not any((v or "").strip() for v in source.values()):
            continue
        participant = (source.get("participant_id") or "").strip()
        condition = (source.get("condition") or "").strip()
        task = (source.get("task") or "").strip()
        if not participant or not condition or not task:
            raise InputIssue(f"MISSING_KEY_FIELD:line:{line_no}")
        key = (participant, condition, task)
        seen[key] += 1
        if seen[key] > 1:
            raise InputIssue(f"DUPLICATE_PARTICIPANT_CONDITION_TASK:line:{line_no}")
        rows.append({
            "row_number": line_no,
            "participant_id": participant,
            "condition": condition,
            "task": task,
            "success": parse_bool(source.get("success") or ""),
            "duration_seconds": parse_duration(source.get("duration_seconds") or ""),
        })
    if not rows:
        raise InputIssue("NO_DATA_ROWS")
    if len(rows) > 100_000:
        raise InputIssue("TOO_MANY_ROWS")
    return rows, fields


def tukey_flags(rows: list[dict[str, Any]]) -> tuple[list[int], dict[str, float] | None]:
    values = [r["duration_seconds"] for r in rows if r["duration_seconds"] is not None]
    if len(values) < 4:
        return [], None
    q1 = percentile(values, 0.25)
    q3 = percentile(values, 0.75)
    iqr = q3 - q1
    if iqr == 0:
        return [], {"q1": q1, "q3": q3, "lower": q1, "upper": q3, "iqr": 0.0}
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    flagged = [r["row_number"] for r in rows if r["duration_seconds"] is not None and not lower <= r["duration_seconds"] <= upper]
    return flagged, {"q1": q1, "q3": q3, "lower": lower, "upper": upper, "iqr": iqr}


def paired_differences(rows: list[dict[str, Any]], conditions: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    if len(conditions) != 2:
        return [], ["Paired differences skipped: exactly two conditions are required."]
    by_key: dict[tuple[str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_key[(row["participant_id"], row["task"])][row["condition"]] = row
    grouped: dict[str, list[float]] = defaultdict(list)
    for (_, task), conditions_map in by_key.items():
        if all(c in conditions_map for c in conditions):
            a, b = (conditions_map[c] for c in conditions)
            if a["duration_seconds"] is not None and b["duration_seconds"] is not None:
                grouped[task].append(b["duration_seconds"] - a["duration_seconds"])
    output = []
    for task, diffs in sorted(grouped.items()):
        if diffs:
            output.append({
                "task": task,
                "condition_a": conditions[0],
                "condition_b": conditions[1],
                "n_complete_duration_pairs": len(diffs),
                "median_b_minus_a": round(statistics.median(diffs), 6),
                "mean_b_minus_a": round(statistics.fmean(diffs), 6),
                "note": "Descriptive participant-level duration differences; failures with valid durations remain included.",
            })
    if not output:
        warnings.append("No participant-task pairs had valid durations in both conditions.")
    return output, warnings


def paired_success(rows: list[dict[str, Any]], conditions: list[str]) -> list[dict[str, Any]]:
    if len(conditions) != 2:
        return []
    by_key: dict[tuple[str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_key[(row["participant_id"], row["task"])][row["condition"]] = row
    grouped: dict[str, list[tuple[bool, bool]]] = defaultdict(list)
    for (_, task), conditions_map in by_key.items():
        if all(c in conditions_map for c in conditions):
            a, b = (conditions_map[c] for c in conditions)
            if a["success"] is not None and b["success"] is not None:
                grouped[task].append((a["success"], b["success"]))
    output = []
    for task, pairs in sorted(grouped.items()):
        n = len(pairs)
        if not n:
            continue
        both_success = sum(a and b for a, b in pairs)
        a_only = sum(a and not b for a, b in pairs)
        b_only = sum(b and not a for a, b in pairs)
        both_failure = sum((not a) and (not b) for a, b in pairs)
        output.append({
            "task": task,
            "condition_a": conditions[0],
            "condition_b": conditions[1],
            "n_complete_outcome_pairs": n,
            "both_success": both_success,
            "a_success_b_failure": a_only,
            "a_failure_b_success": b_only,
            "both_failure": both_failure,
            "a_success_pct_within_complete_pairs": round(100 * (both_success + a_only) / n, 6),
            "b_success_pct_within_complete_pairs": round(100 * (both_success + b_only) / n, 6),
            "note": "Complete-pair description only; participants with a missing outcome are excluded and counted separately.",
        })
    return output


def analyze(rows: list[dict[str, Any]], *, synthetic: bool, duration_unit: str, outlier_method: str) -> dict[str, Any]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["condition"], row["task"])].append(row)
    group_output = []
    all_outlier_rows: list[int] = []
    for (condition, task), members in sorted(groups.items()):
        success_values = [r["success"] for r in members if r["success"] is not None]
        n_success = sum(success_values)
        n_failure = len(success_values) - n_success
        valid_durations = [r["duration_seconds"] for r in members if r["duration_seconds"] is not None]
        success_durations = [r["duration_seconds"] for r in members if r["success"] is True and r["duration_seconds"] is not None]
        if outlier_method == "tukey":
            flagged, fences = tukey_flags(members)
        else:
            flagged, fences = [], None
        all_outlier_rows.extend(flagged)
        flagged_set = set(flagged)
        sensitivity_durations = [
            r["duration_seconds"] for r in members
            if r["duration_seconds"] is not None and r["row_number"] not in flagged_set
        ]
        group_output.append({
            "condition": condition,
            "task": task,
            "n_records": len(members),
            "n_success": n_success,
            "n_failure": n_failure,
            "n_missing_success": len(members) - len(success_values),
            "success_rate_pct": round(100 * n_success / len(success_values), 6) if success_values else None,
            "success_denominator": "records with observed success; missing success excluded and reported",
            "success_rate_pct_bounds_all_records": {
                "missing_as_failure": round(100 * n_success / len(members), 6),
                "missing_as_success": round(100 * (n_success + len(members) - len(success_values)) / len(members), 6),
                "note": "Sensitivity bounds, not imputed estimates.",
            },
            "n_valid_duration": len(valid_durations),
            "n_missing_duration": len(members) - len(valid_durations),
            "duration_all_observed": describe(valid_durations),
            "duration_all_observed_excluding_flagged": describe(sensitivity_durations),
            "duration_success_only": describe(success_durations),
            "tukey_outlier_row_numbers": flagged,
            "tukey_fences": fences,
            "zero_duration_row_numbers": [r["row_number"] for r in members if r["duration_seconds"] == 0],
        })
    conditions = sorted({r["condition"] for r in rows})
    paired, warnings = paired_differences(rows, conditions)
    outlier_rows = set(all_outlier_rows)
    paired_sensitivity, sensitivity_warnings = paired_differences(
        [r for r in rows if r["row_number"] not in outlier_rows], conditions
    )
    warnings.extend(sensitivity_warnings)
    success_pairs = paired_success(rows, conditions)
    warnings.extend([
        "Descriptive output only; no p-values, equivalence, or population inference are produced.",
        "Outlier flags are review markers, not automatic exclusions.",
        "Analysis unit is participant-condition-task; do not treat repeated task rows as independent participants.",
    ])
    if not synthetic:
        warnings.append("Data are not marked synthetic; confirm authorization, provenance, and privacy before sharing.")
    return {
        "schema_version": "1.0",
        "synthetic": synthetic,
        "duration_unit": duration_unit,
        "row_count": len(rows),
        "analysis_unit": "participant-condition-task",
        "outlier_method": outlier_method,
        "groups": group_output,
        "paired_success": success_pairs,
        "paired_differences": paired,
        "paired_differences_excluding_flagged_rows": paired_sensitivity,
        "tukey_outlier_row_numbers": sorted(set(all_outlier_rows)),
        "warnings": warnings,
        "interpretation_boundary": "Synthetic demonstration only; no real product effect." if synthetic else "Authorized data description only; inference requires a justified design.",
    }


def load_config(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    if not path.is_file():
        raise InputIssue("CONFIG_NOT_A_FILE")
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise InputIssue("INVALID_CONFIG_JSON") from exc
    if not isinstance(body, dict):
        raise InputIssue("INVALID_CONFIG_OBJECT")
    return body


def run(input_path: Path, output_path: Path, config_path: Path | None, synthetic_flag: bool | None, outlier_method: str | None) -> dict[str, Any]:
    output_abs = output_path.resolve()
    if output_abs == SKILL_ROOT or SKILL_ROOT in output_abs.parents:
        raise InputIssue("OUTPUT_INSIDE_SKILL_SOURCE")
    protected_inputs = [input_path.resolve()]
    if config_path is not None:
        protected_inputs.append(config_path.resolve())
    if output_abs in protected_inputs:
        raise InputIssue("OUTPUT_OVERWRITES_INPUT")
    rows, fields = read_rows(input_path)
    config = load_config(config_path)
    synthetic = config.get("synthetic", False) if synthetic_flag is None else synthetic_flag
    if type(synthetic) is not bool:
        raise InputIssue("CONFIG_SYNTHETIC_MUST_BE_BOOLEAN")
    unit = config.get("duration_unit", "seconds")
    if not isinstance(unit, str) or not unit.strip():
        raise InputIssue("CONFIG_DURATION_UNIT_INVALID")
    if unit.strip().casefold() not in {"s", "sec", "secs", "second", "seconds"}:
        raise InputIssue("DURATION_COLUMN_UNIT_MISMATCH")
    unit = "seconds"
    method = outlier_method or config.get("outlier_method", "tukey")
    if method not in {"tukey", "none"}:
        raise InputIssue("OUTLIER_METHOD_INVALID")
    result = analyze(rows, synthetic=synthetic, duration_unit=unit, outlier_method=method)
    result["input"] = {
        "sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "columns": fields,
        "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest() if config_path else None,
    }
    if output_abs.exists() and output_abs.is_dir():
        raise InputIssue("OUTPUT_IS_DIRECTORY")
    output_abs.parent.mkdir(parents=True, exist_ok=True)
    output_abs.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--synthetic", action="store_true", default=None)
    parser.add_argument("--outlier-method", choices=["tukey", "none"])
    args = parser.parse_args()
    try:
        result = run(args.input, args.output, args.config, args.synthetic, args.outlier_method)
    except Exception as exc:
        code = str(exc) if isinstance(exc, InputIssue) else "UNEXPECTED_PROCESSING_ERROR"
        print("ANALYSIS_FAIL:", code, file=sys.stderr)
        return 2
    print(f"ANALYSIS_OK rows={result['row_count']} groups={len(result['groups'])} synthetic={str(result['synthetic']).lower()} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
