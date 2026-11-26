#!/usr/bin/env python3
"""Build a deterministic, installable UXDA skill ZIP and print its manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

EXCLUDED_PARTS = {"__pycache__", ".git", ".qoder"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".log"}
EXCLUDED_NAMES = {".DS_Store"}


class PackageIssue(ValueError):
    pass


def collect(source: Path) -> list[Path]:
    files = []
    for path in source.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if path.name in EXCLUDED_NAMES or path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        if path.is_symlink():
            raise PackageIssue("SYMLINK_NOT_ALLOWED")
        files.append(path)
    files.sort(key=lambda p: p.relative_to(source).as_posix())
    if not (source / "SKILL.md").is_file():
        raise PackageIssue("SKILL_MD_MISSING")
    return files


def build(source: Path, output: Path, manifest: Path | None = None) -> dict:
    source = source.resolve()
    output = output.resolve()
    manifest_abs = manifest.resolve() if manifest is not None else None
    if not source.is_dir():
        raise PackageIssue("SOURCE_NOT_DIRECTORY")
    if source.name != "ux-decision-advisor":
        raise PackageIssue("SOURCE_FOLDER_NAME_INVALID")
    if output == source or source in output.parents:
        raise PackageIssue("OUTPUT_INSIDE_SKILL_SOURCE")
    if manifest_abs is not None:
        if manifest_abs == output:
            raise PackageIssue("MANIFEST_COLLIDES_WITH_ZIP")
        if manifest_abs == source or source in manifest_abs.parents:
            raise PackageIssue("MANIFEST_INSIDE_SKILL_SOURCE")
    try:
        from validate_skill import validate as validate_skill_package
        validate_skill_package(source)
    except Exception as exc:
        raise PackageIssue("SKILL_VALIDATION_FAILED:" + str(exc)) from exc
    files = collect(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            arcname = "ux-decision-advisor/" + path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(arcname, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if path.suffix == ".py" else 0o644) << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(output) as archive:
        bad = archive.testzip()
        if bad:
            raise PackageIssue("ZIP_CRC_FAILED:" + bad)
        names = archive.namelist()
        if len(names) != len(files) or any(not name.startswith("ux-decision-advisor/") for name in names):
            raise PackageIssue("ZIP_LAYOUT_INVALID")
    if manifest_abs is not None:
        manifest_abs.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    result = {
        "output": str(output),
        "skill_name": source.name,
        "file_count": len(files),
        "uncompressed_bytes": sum(p.stat().st_size for p in files),
        "zip_bytes": output.stat().st_size,
        "sha256": digest,
        "files": [p.relative_to(source).as_posix() for p in files],
    }
    if manifest_abs is not None:
        manifest_abs.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        result = build(args.source, args.output, args.manifest)
    except Exception as exc:
        code = str(exc) if isinstance(exc, PackageIssue) else "UNEXPECTED_PACKAGE_ERROR"
        print("PACKAGE_FAIL:", code, file=sys.stderr)
        return 2
    summary = {k: v for k, v in result.items() if k != "files"}
    print("PACKAGE_OK " + json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
