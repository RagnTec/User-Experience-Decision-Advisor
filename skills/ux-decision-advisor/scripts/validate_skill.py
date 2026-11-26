#!/usr/bin/env python3
"""Validate integrated UXDA skill packaging, frontmatter, links, runtime deps, and script syntax."""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]+$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
REQUIRED_RUNTIME = (
    "LICENSE",
    "scripts/render_markdown_report.py",
    "assets/markdown-report-shell.html",
    "scripts/render_report.py",
    "assets/report-shell.html",
    "assets/structured-report-shell.html",
    "scripts/validate_evidence.py",
    "assets/uxda-evidence-v1.schema.json",
    "assets/uxda-evidence-example.json",
    "assets/qualitative-coding.md",
    "scripts/analyze_synthetic.py",
    "scripts/local_evidence.py",
    "references/core-reasoning.md",
    "references/business-facing-output-contract.md",
    "references/bilingual-parity.md",
)


class ValidationIssue(ValueError):
    pass


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValidationIssue("FRONTMATTER_MISSING")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValidationIssue("FRONTMATTER_UNCLOSED")
    header, body = text[4:end], text[end + 5:]
    fields: dict[str, str] = {}
    current_parent: str | None = None
    for line in header.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValidationIssue("FRONTMATTER_LINE_INVALID")
        indent = len(line) - len(line.lstrip(" "))
        key, value = line.split(":", 1)
        k = key.strip()
        v = value.strip().strip('"').strip("'")
        if indent == 0:
            current_parent = k if not v else None
            fields[k] = v
        elif current_parent:
            fields[f"{current_parent}.{k}"] = v
        else:
            fields[k] = v
    return fields, body


def validate(skill_dir: Path) -> dict:
    skill_dir = skill_dir.resolve()
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise ValidationIssue("SKILL_MD_MISSING")
    text = skill_file.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(text)
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not NAME_RE.fullmatch(name):
        raise ValidationIssue("NAME_INVALID")
    if name != skill_dir.name:
        raise ValidationIssue("FOLDER_NAME_MISMATCH")
    if not description or len(description) > 1024 or "\n" in description or description.startswith(">"):
        raise ValidationIssue("DESCRIPTION_INVALID")
    if len(body.splitlines()) > 500:
        raise ValidationIssue("SKILL_BODY_TOO_LONG")
    for relative in REQUIRED_RUNTIME:
        if not (skill_dir / relative).is_file():
            raise ValidationIssue("REQUIRED_RUNTIME_MISSING:" + relative)
    for marker in ("TODO:", "TBD:", "FIXME:"):
        if marker in text:
            raise ValidationIssue(f"UNRESOLVED_MARKER:{marker}")
    references = sorted((skill_dir / "references").glob("*.md")) if (skill_dir / "references").is_dir() else []
    scripts = sorted((skill_dir / "scripts").glob("*.py")) if (skill_dir / "scripts").is_dir() else []
    link_count = 0
    for markdown in [skill_file, *references, *sorted((skill_dir / "assets").glob("*.md"))]:
        content = markdown.read_text(encoding="utf-8")
        if "TODO:" in content or "TBD:" in content:
            raise ValidationIssue(f"UNRESOLVED_MARKER:{markdown.name}")
        for target in LINK_RE.findall(content):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            link_count += 1
            if not (markdown.parent / path_part).resolve().exists():
                raise ValidationIssue(f"BROKEN_LINK:{markdown.relative_to(skill_dir)}:{target}")
    for script in scripts:
        try:
            ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
        except SyntaxError as exc:
            raise ValidationIssue(f"SCRIPT_SYNTAX_ERROR:{script.name}:{exc.lineno}") from exc
    all_files = [p for p in skill_dir.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]
    return {
        "name": name,
        "version": fields.get("metadata.version", fields.get("version", "")),
        "skill_body_lines": len(body.splitlines()),
        "description_chars": len(description),
        "references": len(references),
        "scripts": len(scripts),
        "assets": len([p for p in (skill_dir / "assets").rglob("*") if p.is_file()]) if (skill_dir / "assets").is_dir() else 0,
        "files": len(all_files),
        "local_links_checked": link_count,
        "total_bytes": sum(p.stat().st_size for p in all_files),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = validate(args.skill_dir)
    except Exception as exc:
        code = str(exc) if isinstance(exc, ValidationIssue) else "UNEXPECTED_VALIDATION_ERROR"
        print("SKILL_VALIDATION_FAIL:", code, file=sys.stderr)
        return 2
    print("SKILL_VALIDATION_OK " + " ".join(f"{key}={value}" for key, value in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
