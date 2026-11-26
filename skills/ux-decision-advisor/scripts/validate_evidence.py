#!/usr/bin/env python3
"""Validate the minimal UXDA evidence contract and its cross-references."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "uxda-evidence-v1"
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{0,127}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FORBIDDEN_KEYS = {"confidence", "confidence_score", "probability"}
TOP_KEYS = {"schema_version", "synthetic", "studies", "evidence", "claims", "decisions"}
OBJECT_KEYS = {
    "study": {"study_id", "decision_id", "title", "question", "method", "sample_frame", "analysis_unit", "status", "limitations"},
    "evidence": {"evidence_id", "study_id", "source_type", "source_locator", "evidence_status", "access_class", "authorized_for_use", "consent_scope", "participant_pseudonym", "timecode", "version", "note"},
    "claim": {"claim_id", "study_id", "statement", "support_type", "evidence_refs", "conflict_refs", "status", "boundary"},
    "decision": {"decision_id", "owner", "review_date", "recommendation", "reversal_condition", "claim_refs", "status", "authorization_boundary", "outcome"},
    "outcome": {"implemented", "actual_result", "result_evidence_refs", "overturned_claim_refs", "reviewed_on"},
}
REQUIRED = {
    "study": ("study_id", "decision_id", "title", "question", "method", "sample_frame", "analysis_unit", "status"),
    "evidence": ("evidence_id", "study_id", "source_type", "source_locator", "evidence_status", "access_class", "authorized_for_use"),
    "claim": ("claim_id", "study_id", "statement", "support_type", "evidence_refs", "status"),
    "decision": ("decision_id", "owner", "review_date", "recommendation", "reversal_condition", "claim_refs", "status"),
    "outcome": ("implemented", "actual_result"),
}
ENUMS = {
    "method": {"existing_evidence", "interview", "survey", "usability", "experiment", "analytics", "mixed", "human_factors", "other"},
    "study_status": {"planned", "active", "completed", "stopped"},
    "source_type": {"interview", "survey", "usability", "telemetry", "document", "observation", "computation", "standard", "other"},
    "evidence_status": {"supplied", "observed", "verified", "computed", "unverified"},
    "access_class": {"public", "internal", "restricted"},
    "support_type": {"supports", "contradicts", "qualifies", "unknown"},
    "claim_status": {"hypothesis", "supported", "contested", "rejected", "unresolved"},
    "decision_status": {"open", "decided", "implemented", "reviewed", "stopped"},
}


class EvidenceIssue(ValueError):
    pass


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise EvidenceIssue("DUPLICATE_JSON_KEY:" + key)
        result[key] = value
    return result


def load(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys)
    except EvidenceIssue:
        raise
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise EvidenceIssue("INVALID_JSON:" + str(exc)) from exc
    if not isinstance(payload, dict):
        raise EvidenceIssue("ROOT_NOT_OBJECT")
    return payload


def _check_forbidden(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in FORBIDDEN_KEYS:
                raise EvidenceIssue("UNDEFINED_CONFIDENCE_FIELD:" + path + "." + key)
            _check_forbidden(item, path + "." + key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _check_forbidden(item, f"{path}[{index}]")


def _require_object(item: Any, kind: str, path: str) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise EvidenceIssue("OBJECT_REQUIRED:" + path)
    unknown = set(item) - OBJECT_KEYS[kind]
    if unknown:
        raise EvidenceIssue("UNKNOWN_FIELD:" + path + "." + sorted(unknown)[0])
    for key in REQUIRED[kind]:
        if key not in item:
            raise EvidenceIssue("REQUIRED_FIELD_MISSING:" + path + "." + key)
    return item


def _require_string(item: dict[str, Any], key: str, path: str) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise EvidenceIssue("STRING_REQUIRED:" + path + "." + key)
    return value


def _require_id(item: dict[str, Any], key: str, path: str) -> str:
    value = _require_string(item, key, path)
    if not ID_RE.fullmatch(value):
        raise EvidenceIssue("ID_INVALID:" + path + "." + key)
    return value


def _require_bool(item: dict[str, Any], key: str, path: str) -> bool:
    if not isinstance(item.get(key), bool):
        raise EvidenceIssue("BOOLEAN_REQUIRED:" + path + "." + key)
    return item[key]


def _require_refs(item: dict[str, Any], key: str, path: str) -> list[str]:
    value = item.get(key)
    if not isinstance(value, list) or any(not isinstance(ref, str) or not ID_RE.fullmatch(ref) for ref in value):
        raise EvidenceIssue("REFERENCE_LIST_INVALID:" + path + "." + key)
    if len(value) != len(set(value)):
        raise EvidenceIssue("DUPLICATE_REFERENCE:" + path + "." + key)
    return value


def _check_date(value: Any, path: str) -> None:
    if not isinstance(value, str) or not DATE_RE.fullmatch(value):
        raise EvidenceIssue("DATE_INVALID:" + path)
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise EvidenceIssue("DATE_INVALID:" + path) from exc


def _check_enum(item: dict[str, Any], key: str, allowed: set[str], path: str) -> None:
    if not isinstance(item.get(key), str) or item[key] not in allowed:
        raise EvidenceIssue("ENUM_INVALID:" + path + "." + key)


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    _check_forbidden(payload)
    if set(payload) != TOP_KEYS:
        unknown = set(payload) - TOP_KEYS
        missing = TOP_KEYS - set(payload)
        if unknown:
            raise EvidenceIssue("UNKNOWN_FIELD:$." + sorted(unknown)[0])
        raise EvidenceIssue("REQUIRED_FIELD_MISSING:$." + sorted(missing)[0])
    if payload["schema_version"] != SCHEMA_VERSION:
        raise EvidenceIssue("SCHEMA_VERSION_UNSUPPORTED")
    _require_bool(payload, "synthetic", "$")
    for key in ("studies", "evidence", "claims", "decisions"):
        if not isinstance(payload[key], list):
            raise EvidenceIssue("ARRAY_REQUIRED:$." + key)
    if not payload["studies"] or not payload["decisions"]:
        raise EvidenceIssue("STUDY_AND_DECISION_REQUIRED")

    ids: dict[str, str] = {}

    def register(identifier: str, kind: str) -> None:
        if identifier in ids:
            raise EvidenceIssue("DUPLICATE_ID:" + identifier)
        ids[identifier] = kind

    studies: dict[str, dict[str, Any]] = {}
    evidence: dict[str, dict[str, Any]] = {}
    claims: dict[str, dict[str, Any]] = {}
    conflict_refs: dict[str, list[str]] = {}
    decisions: dict[str, dict[str, Any]] = {}

    for index, raw in enumerate(payload["studies"]):
        path = f"$.studies[{index}]"
        item = _require_object(raw, "study", path)
        identifier = _require_id(item, "study_id", path)
        register(identifier, "study")
        _require_id(item, "decision_id", path)
        for key in ("title", "question", "sample_frame", "analysis_unit"):
            _require_string(item, key, path)
        _check_enum(item, "method", ENUMS["method"], path)
        _check_enum(item, "status", ENUMS["study_status"], path)
        if "limitations" in item and (
            not isinstance(item["limitations"], list)
            or any(not isinstance(x, str) or not x.strip() for x in item["limitations"])
        ):
            raise EvidenceIssue("STRING_LIST_INVALID:" + path + ".limitations")
        studies[identifier] = item

    for index, raw in enumerate(payload["evidence"]):
        path = f"$.evidence[{index}]"
        item = _require_object(raw, "evidence", path)
        identifier = _require_id(item, "evidence_id", path)
        register(identifier, "evidence")
        _require_id(item, "study_id", path)
        _require_string(item, "source_locator", path)
        _check_enum(item, "source_type", ENUMS["source_type"], path)
        _check_enum(item, "evidence_status", ENUMS["evidence_status"], path)
        _check_enum(item, "access_class", ENUMS["access_class"], path)
        if not _require_bool(item, "authorized_for_use", path):
            raise EvidenceIssue("EVIDENCE_NOT_AUTHORIZED:" + identifier)
        for key in ("consent_scope", "participant_pseudonym", "timecode", "version", "note"):
            if key in item:
                _require_string(item, key, path)
        if item["access_class"] == "restricted" and not item.get("consent_scope"):
            raise EvidenceIssue("RESTRICTED_EVIDENCE_REQUIRES_CONSENT_SCOPE:" + identifier)
        evidence[identifier] = item

    for index, raw in enumerate(payload["claims"]):
        path = f"$.claims[{index}]"
        item = _require_object(raw, "claim", path)
        identifier = _require_id(item, "claim_id", path)
        register(identifier, "claim")
        _require_id(item, "study_id", path)
        _require_string(item, "statement", path)
        refs = _require_refs(item, "evidence_refs", path)
        conflicts = _require_refs(item, "conflict_refs", path) if "conflict_refs" in item else []
        _check_enum(item, "support_type", ENUMS["support_type"], path)
        _check_enum(item, "status", ENUMS["claim_status"], path)
        if item["status"] in {"supported", "contested", "rejected"} and not refs:
            raise EvidenceIssue("SUPPORTED_CLAIM_REQUIRES_EVIDENCE:" + identifier)
        if item["status"] == "supported" and item["support_type"] == "contradicts":
            raise EvidenceIssue("SUPPORTED_CLAIM_CONTRADICTS_EVIDENCE:" + identifier)
        if identifier in conflicts:
            raise EvidenceIssue("SELF_CONFLICT_REFERENCE:" + identifier)
        if "boundary" in item:
            _require_string(item, "boundary", path)
        conflict_refs[identifier] = conflicts
        claims[identifier] = item

    for index, raw in enumerate(payload["decisions"]):
        path = f"$.decisions[{index}]"
        item = _require_object(raw, "decision", path)
        identifier = _require_id(item, "decision_id", path)
        register(identifier, "decision")
        for key in ("owner", "recommendation", "reversal_condition"):
            _require_string(item, key, path)
        _check_date(item["review_date"], path + ".review_date")
        refs = _require_refs(item, "claim_refs", path)
        _check_enum(item, "status", ENUMS["decision_status"], path)
        if item["status"] in {"decided", "implemented", "reviewed"} and not refs:
            raise EvidenceIssue("DECIDED_RECORD_REQUIRES_CLAIM:" + identifier)
        if "authorization_boundary" in item:
            _require_string(item, "authorization_boundary", path)
        if "outcome" in item:
            outcome_path = path + ".outcome"
            outcome = _require_object(item["outcome"], "outcome", outcome_path)
            implemented = _require_bool(outcome, "implemented", outcome_path)
            if item["status"] == "implemented" and not implemented:
                raise EvidenceIssue("DECISION_IMPLEMENTATION_MISMATCH:" + identifier)
            _require_string(outcome, "actual_result", outcome_path)
            for key in ("result_evidence_refs", "overturned_claim_refs"):
                if key in outcome:
                    _require_refs(outcome, key, outcome_path)
            if "reviewed_on" in outcome:
                _check_date(outcome["reviewed_on"], outcome_path + ".reviewed_on")
        decisions[identifier] = item

    for item in studies.values():
        if item["decision_id"] not in decisions:
            raise EvidenceIssue("BROKEN_STUDY_DECISION_REFERENCE:" + item["study_id"])
    for item in evidence.values():
        if item["study_id"] not in studies:
            raise EvidenceIssue("BROKEN_EVIDENCE_STUDY_REFERENCE:" + item["evidence_id"])
    for item in claims.values():
        if item["study_id"] not in studies:
            raise EvidenceIssue("BROKEN_CLAIM_STUDY_REFERENCE:" + item["claim_id"])
        for ref in item["evidence_refs"]:
            if ref not in evidence:
                raise EvidenceIssue("BROKEN_CLAIM_EVIDENCE_REFERENCE:" + ref)
            if evidence[ref]["study_id"] != item["study_id"]:
                raise EvidenceIssue("CROSS_STUDY_CLAIM_EVIDENCE_REFERENCE:" + ref)
        for ref in conflict_refs[item["claim_id"]]:
            if ref not in claims:
                raise EvidenceIssue("BROKEN_CONFLICT_REFERENCE:" + ref)
            if claims[ref]["study_id"] != item["study_id"]:
                raise EvidenceIssue("CROSS_STUDY_CONFLICT_REFERENCE:" + ref)
    for item in decisions.values():
        allowed_studies = {study_id for study_id, study in studies.items() if study["decision_id"] == item["decision_id"]}
        for ref in item["claim_refs"]:
            if ref not in claims:
                raise EvidenceIssue("BROKEN_DECISION_CLAIM_REFERENCE:" + ref)
            if claims[ref]["study_id"] not in allowed_studies:
                raise EvidenceIssue("CROSS_DECISION_CLAIM_REFERENCE:" + ref)
        outcome = item.get("outcome")
        if outcome:
            for ref in outcome.get("result_evidence_refs", []):
                if ref not in evidence:
                    raise EvidenceIssue("BROKEN_RESULT_EVIDENCE_REFERENCE:" + ref)
                if evidence[ref]["study_id"] not in allowed_studies:
                    raise EvidenceIssue("CROSS_DECISION_RESULT_EVIDENCE_REFERENCE:" + ref)
            for ref in outcome.get("overturned_claim_refs", []):
                if ref not in claims:
                    raise EvidenceIssue("BROKEN_OVERTURNED_CLAIM_REFERENCE:" + ref)
                if claims[ref]["study_id"] not in allowed_studies:
                    raise EvidenceIssue("CROSS_DECISION_OVERTURNED_CLAIM_REFERENCE:" + ref)

    return {
        "schema_version": SCHEMA_VERSION,
        "synthetic": payload["synthetic"],
        "studies": len(studies),
        "evidence": len(evidence),
        "claims": len(claims),
        "decisions": len(decisions),
        "reference_checks": "passed",
        "truth_verification": "not_performed",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        result = validate(load(args.input))
    except EvidenceIssue as exc:
        print("EVIDENCE_VALIDATION_FAIL:", exc, file=sys.stderr)
        return 2
    print("EVIDENCE_VALIDATION_OK " + " ".join(f"{key}={value}" for key, value in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
