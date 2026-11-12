#!/usr/bin/env python3
"""Strict, OFFLINE evidence/citation audit. It never browses and never prints private text.

Requires an explicit private claim ledger for formal referenced reports. A filled ledger
is NOT proof that a remote source was actually retrieved or the assertion is true.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, unquote

CITE_RE = re.compile(r'\[SRC:([A-Za-z][A-Za-z0-9_-]{0,63})\]')
URL_RE = re.compile(r'https?://[^\s<>\]"\']+',re.I)
PLACEHOLDER = re.compile(r'(?:^|\.)((?:example\.(?:com|org|net))|(?:example\.invalid)|(?:localhost)|(?:test)|(?:invalid))$',re.I)
BLOCKED_TEXT = re.compile(r'(robot|captcha|enable javascript|access denied|verify that you.re not a robot|page not found|404 not found)',re.I)
REAL_CLASSES={'LAW','STANDARD','EMPIRICAL','PRODUCT_FACT','MARKET_FACT','QUANTITATIVE','METHOD'}
PUBLIC_KINDS={'WEB_PAGE','LAW','STANDARD','RESEARCH_ARTICLE','DATASET','PUBLIC_REPORT'}
RESERVED_KINDS={'UNVERIFIED','MODEL_INFERENCE','SYNTHETIC'}


def url_reason(url: str) -> str | None:
    if not isinstance(url,str) or not url: return 'EMPTY_URL'
    if any(t in url.lower() for t in ('your-url','placeholder','todo','tbd','<url>','[url]')):return 'PLACEHOLDER_URL'
    try: p=urlsplit(url)
    except ValueError: return 'BAD_URL'
    if p.scheme!='https' or not p.hostname or p.username or p.password:return 'NOT_PUBLIC_HTTPS'
    if PLACEHOLDER.search(p.hostname) or p.hostname.endswith(('.local','.internal','.invalid')):return 'PLACEHOLDER_OR_PRIVATE_HOST'
    if p.hostname in ('127.0.0.1','0.0.0.0','::1') or not '.' in p.hostname:return 'PRIVATE_OR_INVALID_HOST'
    if '%' in p.hostname or any(x in unquote(p.path).lower() for x in ('/your-page','/dummy-document','/fake-link')):return 'PLACEHOLDER_URL'
    if p.hostname.lower()=='doi.org' and not re.fullmatch(r'/10\.\d{4,9}/\S+', p.path):return 'INVALID_DOI'
    return None


def _norm(x: str) -> str:
    return re.sub(r'\s+',' ',str(x)).strip().casefold()


def _hash(path:Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def inspect(report: str, ledger: dict, *,private_root:Path|None=None) -> list[str]:
    """Issue codes only, never original claim/sources."""
    issues=[]
    sources=ledger.get('sources',[])
    claims=ledger.get('claims',[])
    if not isinstance(sources,list) or not isinstance(claims,list):return ['INVALID_LEDGER_COLLECTIONS']
    source_map={}
    for index,s in enumerate(sources):
        if not isinstance(s,dict):issues.append(f'SOURCE_NOT_OBJECT index={index}');continue
        sid=s.get('id')
        if not isinstance(sid,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,63}',sid):issues.append(f'INVALID_SOURCE_ID index={index}');continue
        if sid in source_map:issues.append(f'DUPLICATE_SOURCE_ID id={sid}')
        source_map[sid]=s
        kind=s.get('kind','')
        if kind in RESERVED_KINDS:issues.append(f'UNACCEPTABLE_REFERENCE_KIND id={sid}')
        elif kind=='LOCAL_DOCUMENT':
            if not s.get('title') or not s.get('locator') or not s.get('version'):issues.append(f'INCOMPLETE_LOCAL_REFERENCE id={sid}')
            path_str=s.get('path')
            if not path_str or not s.get('sha256'):issues.append(f'MISSING_LOCAL_FILE_HASH id={sid}');continue
            p=Path(path_str).expanduser()
            try:
                resolved=p.resolve(strict=True)
                if not resolved.is_file():raise ValueError('not file')
                if private_root is not None:
                    root=private_root.resolve(strict=True)
                    if resolved!=root and root not in resolved.parents:issues.append(f'LOCAL_OUTSIDE_ALLOWED_ROOT id={sid}');continue
                if _hash(resolved)!=s.get('sha256'):issues.append(f'LOCAL_HASH_CHANGED id={sid}')
                if 'line_start' in s:
                    if not resolved.suffix.lower() in ('.txt','.md','.csv','.json','.tsv'):
                        issues.append(f'LINE_ANCHOR_UNSUPPORTED_FILE id={sid}')
                    else:
                        lines=resolved.read_text(encoding='utf-8').splitlines()
                        a=s.get('line_start');b=s.get('line_end',a)
                        if not isinstance(a,int) or not isinstance(b,int) or not (1<=a<=b<=len(lines)):
                            issues.append(f'INVALID_LOCAL_LINE_RANGE id={sid}')
                        elif s.get('support_excerpt') and _norm(s['support_excerpt']) not in _norm('\n'.join(lines[a-1:b])):
                            issues.append(f'LOCAL_EXCERPT_NOT_FOUND id={sid}')
            except (OSError,ValueError,UnicodeError):issues.append(f'LOCAL_FILE_UNREADABLE id={sid}')
        elif kind in PUBLIC_KINDS:
            err=url_reason(s.get('url',''))
            if err:issues.append(f'{err} id={sid}')
            for k in ('title','publisher','locator','accessed_on','supports'):
                if not str(s.get(k,'')).strip():issues.append(f'MISSING_{k.upper()} id={sid}')
            status=s.get('access_status','UNVERIFIED')
            if status not in ('CONTENT_INSPECTED','LIMITED','INACCESSIBLE','UNVERIFIED'):
                issues.append(f'INVALID_ACCESS_STATUS id={sid}')
            if status=='CONTENT_INSPECTED':
                # A textual assertion cannot be called independently checked from a URL alone.
                if not s.get('retrieval_record') or not s.get('support_excerpt'):
                    issues.append(f'INSPECTION_PROOF_MISSING id={sid}')
                if s.get('snapshot_path'):
                    try:
                        snapshot=Path(s['snapshot_path']).resolve(strict=True)
                        if private_root is not None and private_root.resolve(strict=True) not in snapshot.parents:
                            issues.append(f'SNAPSHOT_OUTSIDE_ALLOWED_ROOT id={sid}')
                        elif not s.get('snapshot_sha256') or _hash(snapshot)!=s['snapshot_sha256']:
                            issues.append(f'SNAPSHOT_HASH_CHANGED id={sid}')
                        elif _norm(s.get('support_excerpt','')) not in _norm(snapshot.read_text(encoding='utf-8')):
                            issues.append(f'SNAPSHOT_EXCERPT_NOT_FOUND id={sid}')
                    except (OSError,ValueError,UnicodeError):issues.append(f'SNAPSHOT_UNREADABLE id={sid}')
                elif not s.get('retrieval_record'):
                    issues.append(f'NO_RETRIEVAL_TRACE id={sid}')
            if kind in ('LAW','STANDARD'):
                for k in ('jurisdiction','version','provision_locator'):
                    if not str(s.get(k,'')).strip():issues.append(f'MISSING_{k.upper()} id={sid}')
            if kind=='RESEARCH_ARTICLE':
                for k in ('authors','year','publication'):
                    if not str(s.get(k,'')).strip():issues.append(f'MISSING_{k.upper()} id={sid}')
        else:issues.append(f'UNKNOWN_SOURCE_KIND id={sid}')
    references=CITE_RE.findall(report)
    for cid in sorted(set(references)):
        if cid not in source_map:issues.append(f'UNRESOLVED_CITATION id={cid}')
    # For formal report, every registered claim must be explicitly present and source-linked.
    claim_ids=set()
    for i,c in enumerate(claims):
        if not isinstance(c,dict):issues.append(f'CLAIM_NOT_OBJECT index={i}');continue
        ident=c.get('id',f'claim{i}')
        if ident in claim_ids:issues.append(f'DUPLICATE_CLAIM_ID id={ident}')
        claim_ids.add(ident)
        if not c.get('statement') or _norm(c['statement']) not in _norm(report):issues.append(f'CLAIM_NOT_LOCATABLE id={ident}')
        refs=c.get('source_refs',[])
        if not isinstance(refs,list):issues.append(f'INVALID_CLAIM_REFS id={ident}');continue
        strong=c.get('strength') in ('SUPPORTED','CONCLUSIVE','MANDATORY')
        if c.get('claim_class') in REAL_CLASSES and not refs and strong:issues.append(f'UNSOURCED_STRONG_CLAIM id={ident}')
        if strong and c.get('claim_class') in ('LAW','STANDARD') and not c.get('applicability'):
            issues.append(f'MISSING_CLAIM_APPLICABILITY id={ident}')
        for sid in refs:
            if sid not in source_map:issues.append(f'CLAIM_SOURCE_UNKNOWN id={ident}')
            elif f'[SRC:{sid}]' not in report:issues.append(f'CLAIM_SOURCE_NOT_CITED id={ident}')
            elif strong:
                s=source_map[sid]
                if s.get('kind') in PUBLIC_KINDS and s.get('access_status')!='CONTENT_INSPECTED':
                    issues.append(f'INSUFFICIENT_WEB_EVIDENCE id={ident}')
                if s.get('kind') in PUBLIC_KINDS and (not s.get('retrieval_record') or not s.get('support_excerpt')):
                    issues.append(f'UNTRACEABLE_WEB_CLAIM id={ident}')
    # A report may not link unregistered live URLs as if sourced, even if HTTPS parses.
    known_urls={s.get('url','').rstrip('.,;') for s in sources if isinstance(s,dict)}
    for j,url in enumerate(URL_RE.findall(report)):
        url=url.rstrip('.,;，。')
        if url not in known_urls:issues.append(f'UNREGISTERED_DIRECT_URL index={j}')
    if not claims and (references or URL_RE.search(report)):
        issues.append('CITATION_WITHOUT_CLAIM_LEDGER')
    return sorted(set(issues))


def main() -> int:
    ap=argparse.ArgumentParser(description='Strict OFFLINE private citation provenance audit; no network calls')
    ap.add_argument('--report',type=Path,required=True)
    ap.add_argument('--ledger',type=Path,required=True)
    ap.add_argument('--private-root',type=Path)
    args=ap.parse_args()
    try:
        report=args.report.read_text(encoding='utf-8')
        ledger=json.loads(args.ledger.read_text(encoding='utf-8'))
        issues=inspect(report,ledger,private_root=args.private_root)
        print(json.dumps({'ok':not issues,'issues':issues,'checked_sources':len(ledger.get('sources',[])),'checked_claims':len(ledger.get('claims',[])),'note':'Structural/local-file verification only; remote retrieval trace must be independently checked, and legal/empirical interpretation reviewed'},ensure_ascii=False,indent=2))
        return 1 if issues else 0
    except (OSError,ValueError,json.JSONDecodeError,UnicodeError) as e:
        print(json.dumps({'ok':False,'issues':[f'INPUT_ERROR {type(e).__name__}'],'note':'No private source text echoed'},ensure_ascii=False))
        return 2
if __name__=='__main__':raise SystemExit(main())
