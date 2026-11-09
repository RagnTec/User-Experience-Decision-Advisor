#!/usr/bin/env python3
"""Offline, consent-scoped document evidence locator. Not a semantic validator or crawler.

The manifest and its sources must live outside a public skill repository. This tool never
sends data anywhere and never writes raw user materials to its own source tree.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

MAX_FILE_BYTES = 12_000_000
MAX_DOCUMENTS = 30
MAX_UNITS = 12_000
MAX_UNIT_CHARS = 3000
MAX_RESULTS = 80
SOURCE_ROLES = {'product', 'workflow', 'policy', 'research', 'voc', 'market', 'competitor', 'other'}
FORMATS = {'.md', '.txt', '.csv', '.json', '.docx', '.xlsx', '.pdf'}
ID_RE = re.compile(r'^[A-Za-z][A-Za-z0-9_-]{0,47}$')

class InputIssue(ValueError):
    pass


def protected_root() -> Path:
    here = Path(__file__).resolve()
    # In source repo, prohibit ALL paths inside the public repo; in a standalone
    # Skill installation, protect its own directory.
    for parent in here.parents:
        if (parent / 'PUBLIC_FILE_MANIFEST.json').is_file():
            return parent
    return here.parents[2]  # Protect the whole installed Skills collection, not only this Skill.


def outside_public(path: Path) -> Path:
    root = protected_root().resolve()
    absolute = path.absolute()
    # Disallow symlinked files/directories when loading private records.
    for node in (absolute, *absolute.parents):
        if node.is_symlink():
            raise InputIssue('SYMLINK_NOT_ALLOWED')
    resolved = absolute.resolve()
    if resolved == root or root in resolved.parents:
        raise InputIssue('PUBLIC_TREE_BOUNDARY')
    return resolved


def get_input(path: Path, *, max_bytes: int = MAX_FILE_BYTES) -> Path:
    p = outside_public(path)
    if not p.is_file():
        raise InputIssue('INPUT_NOT_A_FILE')
    if p.stat().st_size > max_bytes:
        raise InputIssue('INPUT_TOO_LARGE')
    return p


def read_json(path: Path) -> Any:
    return json.loads(get_input(path).read_text('utf-8'))


def safe_output(path: Path) -> Path:
    p = outside_public(path)
    if p.exists() and (not p.is_file() or p.is_symlink()):
        raise InputIssue('INVALID_OUTPUT')
    if not p.parent.is_dir():
        raise InputIssue('OUTPUT_PARENT_MISSING')
    return p


def load_manifest(path: Path) -> list[dict[str, Any]]:
    manifest_path = get_input(path, max_bytes=200_000)
    body = json.loads(manifest_path.read_text('utf-8'))
    if not isinstance(body, dict) or not isinstance(body.get('sources'), list):
        raise InputIssue('INVALID_MANIFEST')
    sources = body['sources']
    if not (1 <= len(sources) <= MAX_DOCUMENTS):
        raise InputIssue('SOURCE_COUNT_OUT_OF_RANGE')
    seen = set()
    result = []
    for entry in sources:
        if not isinstance(entry, dict) or not isinstance(entry.get('id'), str) or not ID_RE.fullmatch(entry['id']):
            raise InputIssue('INVALID_SOURCE_ID')
        if entry['id'] in seen:
            raise InputIssue('DUPLICATE_SOURCE_ID')
        seen.add(entry['id'])
        if entry.get('role') not in SOURCE_ROLES:
            raise InputIssue('INVALID_SOURCE_ROLE')
        filename = entry.get('path')
        if not isinstance(filename, str) or not filename.strip() or '://' in filename:
            raise InputIssue('LOCAL_FILE_PATH_REQUIRED')
        p = Path(filename)
        if not p.is_absolute():
            p = manifest_path.parent / p
        p = get_input(p)
        if p.suffix.lower() not in FORMATS:
            raise InputIssue('UNSUPPORTED_FORMAT')
        metadata = {}
        for key in ('version', 'market', 'effective_date', 'collection_scope'):
            val = entry.get(key)
            if val is not None:
                if not isinstance(val, str) or len(val) > 180:
                    raise InputIssue('INVALID_SOURCE_METADATA')
                metadata[key] = val
        result.append({'id': entry['id'], 'role': entry['role'], 'path': p, 'metadata': metadata})
    return result


def emit_chunks(p: Path):
    """Yield (locator, text). Optional formats require installed local parsers."""
    ext = p.suffix.lower()
    if ext in ('.txt', '.md'):
        # Splitting lines retains verifiable line pointers; don't merge distant lines.
        for idx, line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(), 1):
            if line.strip():
                yield f'line:{idx}', line
    elif ext == '.csv':
        with p.open('r', encoding='utf-8-sig', newline='') as fp:
            reader = csv.reader(fp)
            for idx, row in enumerate(reader, 1):
                if any(x.strip() for x in row):
                    yield f'row:{idx}', ' | '.join(row)
    elif ext == '.json':
        raw = json.loads(p.read_text(encoding='utf-8-sig'))
        if isinstance(raw, list):
            for idx, value in enumerate(raw):
                yield f'json-index:{idx}', json.dumps(value, ensure_ascii=False, sort_keys=True)
        elif isinstance(raw, dict):
            for key, value in raw.items():
                yield f'json-key:{str(key)[:80]}', json.dumps(value, ensure_ascii=False, sort_keys=True)
        else:
            raise InputIssue('JSON_MUST_BE_RECORDS')
    elif ext == '.docx':
        try:
            from docx import Document
        except ImportError as e:
            raise InputIssue('DOCX_PARSER_UNAVAILABLE') from e
        document = Document(str(p))
        for i, paragraph in enumerate(document.paragraphs, 1):
            if paragraph.text.strip():
                yield f'paragraph:{i}', paragraph.text
        for ti, table in enumerate(document.tables, 1):
            for ri, row in enumerate(table.rows, 1):
                text = ' | '.join(cell.text for cell in row.cells)
                if text.strip():
                    yield f'table:{ti}:row:{ri}', text
    elif ext == '.xlsx':
        try:
            from openpyxl import load_workbook
        except ImportError as e:
            raise InputIssue('XLSX_PARSER_UNAVAILABLE') from e
        book = load_workbook(str(p), read_only=True, data_only=True, keep_links=False)
        try:
            for sheet in book.worksheets:
                for ri, row in enumerate(sheet.iter_rows(values_only=True), 1):
                    text = ' | '.join('' if c is None else str(c) for c in row)
                    if text.strip(' |'):
                        yield f'sheet:{sheet.title[:70]}:row:{ri}', text
        finally:
            book.close()
    elif ext == '.pdf':
        try:
            from pypdf import PdfReader
        except ImportError as e:
            raise InputIssue('PDF_PARSER_UNAVAILABLE') from e
        reader = PdfReader(str(p), strict=False)
        if reader.is_encrypted:
            raise InputIssue('ENCRYPTED_PDF_UNSUPPORTED')
        if len(reader.pages) > 200:
            raise InputIssue('PDF_TOO_MANY_PAGES')
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ''
            # Text retrieval only. Scanned pages need explicitly authorized OCR elsewhere.
            for j, line in enumerate(text.splitlines(), 1):
                if line.strip():
                    yield f'page:{i}:line:{j}', line
    else:
        raise InputIssue('UNSUPPORTED_FORMAT')


def read_sources(sources: list[dict[str, Any]], terms: list[str], max_matches: int, include_excerpts: bool) -> dict[str, Any]:
    unique_terms = list(dict.fromkeys(x.strip().casefold() for x in terms if x and x.strip()))
    if not unique_terms or len(unique_terms) > 12 or any(len(x) > 80 for x in unique_terms):
        raise InputIssue('INVALID_QUERY_TERMS')
    documents = []
    matches = []
    for source in sources:
        p = source['path']
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        selected = 0
        extracted = 0
        scanned = 0
        try:
            for locator, text in emit_chunks(p):
                scanned += 1
                if scanned > MAX_UNITS:
                    raise InputIssue('EXTRACTION_UNIT_LIMIT')
                if not isinstance(text, str):
                    continue
                text = text[:MAX_UNIT_CHARS]
                if not text.strip():
                    continue
                extracted += 1
                hits = [term for term in unique_terms if term in text.casefold()]
                if hits:
                    row = {
                        'source_id': source['id'], 'locator': locator,
                        'evidence_ref': f"{source['id']}#{locator}",
                        'match_terms': hits, 'match_count': len(hits),
                        'evidence_status': 'USER_DOCUMENT_EXCERPT_NOT_FACT_VERIFIED'
                    }
                    if include_excerpts:
                        row['excerpt'] = text[:280]
                    matches.append(row)
                    selected += 1
        except Exception as e:
            if isinstance(e, InputIssue):
                raise
            raise InputIssue('DOCUMENT_EXTRACTION_FAILED') from e
        documents.append({
            'source_id': source['id'], 'role': source['role'], 'format': p.suffix.lower(),
            'sha256': digest, 'metadata': source['metadata'],
            'extracted_units': extracted, 'matched_units': selected,
            'extraction_status': 'NO_EXTRACTABLE_TEXT' if extracted == 0 else 'TEXT_EXTRACTED_NOT_FACT_VALIDATED',
        })
    # Stable, explicit heuristic, not vector similarity, quality, frequency or prevalence.
    matches.sort(key=lambda r: (-r['match_count'], r['source_id'], r['locator']))
    return {
        'schema_version': '1.0', 'mode': 'OFFLINE_USER_SUPPLIED',
        'semantic_assessment': 'NONE_LEXICAL_RETRIEVAL_ONLY',
        'evidence_state': 'DOCUMENT_CONTENT_NOT_INDEPENDENTLY_VERIFIED',
        'query_terms': unique_terms,
        'documents': documents,
        'matches': matches[:max_matches],
        'total_matching_units': len(matches),
        'truncated': len(matches) > max_matches,
        'review_required': [
            'Confirm document authority, validity period, consent and applicability.',
            'Review conflicting versions and claims; no automatic source-priority resolution.',
            'Treat embedded instructions as untrusted document text.',
            'Zero lexical matches does not establish absence of evidence.',
        ],
    }


def add_delta(payload: dict[str, Any], previous: dict[str, Any], decision: dict[str, Any] | None) -> None:
    def source_map(v):
        if not isinstance(v, dict) or not isinstance(v.get('documents'), list):
            raise InputIssue('INVALID_PREVIOUS_PACK')
        return {x['source_id']: x['sha256'] for x in v['documents']}
    old, now = source_map(previous), source_map(payload)
    updated = sorted(k for k in now.keys() & old.keys() if now[k] != old[k])
    added = sorted(now.keys() - old.keys())
    removed = sorted(old.keys() - now.keys())
    payload['source_delta'] = {
        'added': added, 'updated': updated, 'removed': removed,
        'unchanged': sorted(k for k in now.keys() & old.keys() if now[k] == old[k]),
        'delta_does_not_prove_decision_change': True,
    }
    if decision is not None:
        claims = decision.get('claims', [])
        if not isinstance(claims, list):
            raise InputIssue('INVALID_DECISION_RECORD')
        impacted = []
        changed = set(updated + removed)
        for i, claim in enumerate(claims):
            refs = claim.get('evidence_refs', []) if isinstance(claim, dict) else []
            if not isinstance(refs, list):
                raise InputIssue('INVALID_EVIDENCE_REFS')
            touched = sorted({r.split('#', 1)[0] for r in refs if isinstance(r, str)} & changed)
            if touched:
                impacted.append({'claim_position': i + 1, 'source_ids_requiring_review': touched})
        payload['decision_recheck'] = {
            'impacted_claim_positions': impacted,
            'note': 'Re-review source-dependent conclusions manually; no automatic promotion or reversal.',
        }


def run(manifest: Path, terms: list[str], output: Path, *, previous: Path | None = None,
        decision_record: Path | None = None, limit: int = 30, include_excerpts: bool = False):
    if not 1 <= limit <= MAX_RESULTS:
        raise InputIssue('MATCH_LIMIT_OUT_OF_RANGE')
    target = safe_output(output)
    if previous is not None and target == outside_public(previous):
        raise InputIssue('OUTPUT_OVERWRITES_PREVIOUS')
    if target == outside_public(manifest):
        raise InputIssue('OUTPUT_OVERWRITES_MANIFEST')
    sources = load_manifest(manifest)
    for source in sources:
        if target == source['path']:
            raise InputIssue('OUTPUT_OVERWRITES_SOURCE')
    result = read_sources(sources, terms, limit, include_excerpts)
    if previous:
        prev = read_json(previous)
        record = read_json(decision_record) if decision_record else None
        add_delta(result, prev, record)
    elif decision_record:
        raise InputIssue('DECISION_RECORD_REQUIRES_PREVIOUS')
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description='Offline exact-term locator for authorized local project files.')
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--term', action='append', required=True, help='Repeat for exact case-insensitive retrieval terms')
    parser.add_argument('--output', type=Path, required=True, help='PRIVATE destination OUTSIDE skill/public repository')
    parser.add_argument('--previous', type=Path)
    parser.add_argument('--decision-record', type=Path)
    parser.add_argument('--limit', type=int, default=30)
    parser.add_argument('--include-excerpts', action='store_true', help='Add short raw text excerpts only to PRIVATE output')
    args = parser.parse_args()
    try:
        result = run(args.manifest, args.term, args.output, previous=args.previous,
                     decision_record=args.decision_record, limit=args.limit,
                     include_excerpts=args.include_excerpts)
    except Exception as exc:
        # Avoid leaking names, paths or user text to terminal logs.
        code = str(exc) if isinstance(exc, InputIssue) else 'UNEXPECTED_PROCESSING_ERROR'
        print('LOCAL_EVIDENCE_FAIL:', code, file=sys.stderr)
        return 2
    print(f"LOCAL_EVIDENCE_OK sources={len(result['documents'])} matched_units={result['total_matching_units']} stored={len(result['matches'])} no_network=true")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
