#!/usr/bin/env python3
"""Deterministic, offline UXDA concept/topic lookup. No browsing or persistent user profile.

Package metadata only describes what was inspected WHEN PACKAGED; this script
never proves the current availability, accuracy, legal applicability, or
behavioral outcomes of a source. Search terms are not saved or echoed.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

CATALOG = Path(__file__).resolve().parents[1] / 'assets' / 'offline-ux-foundations.json'
SCOPES = {'public_article_body','author_overview_only','publisher_metadata_only',
          'official_abstract_only','official_recommendation_public_text'}
DISCIPLINES={'research_methods','interaction','psychology','human_factors','sociology','marketing'}


def validate(data: dict) -> list[str]:
    e=[]
    if not isinstance(data,dict): return ['INVALID_CATALOG']
    sources=data.get('sources');cards=data.get('cards')
    if not isinstance(sources,dict) or not isinstance(cards,list) or not cards:
        return ['CATALOG_FIELDS_MISSING']
    for sid,src in sources.items():
        if not isinstance(src,dict): e.append(f'SOURCE_NOT_OBJECT:{sid}');continue
        for field in ('title','author','publisher','year','url','scope','locator','supports'):
            if not isinstance(src.get(field),str) or not src[field].strip():
                e.append(f'SOURCE_FIELD_MISSING:{sid}:{field}')
        if src.get('scope') not in SCOPES: e.append(f'BAD_SCOPE:{sid}')
        u=urlparse(src.get('url',''))
        if u.scheme!='https' or not u.hostname or u.hostname.endswith(('.invalid','.test','.example')):
            e.append(f'INVALID_SOURCE_URL:{sid}')
    ids=set()
    for c in cards:
        if not isinstance(c,dict):e.append('CARD_NOT_OBJECT');continue
        cid=c.get('id')
        if not isinstance(cid,str) or not re.fullmatch(r'F\d{2}',cid):e.append('CARD_INVALID_ID')
        if cid in ids:e.append(f'CARD_DUPLICATE:{cid}')
        ids.add(cid)
        for field in ('title','discipline','plain_meaning','research_move','boundary'):
            if not isinstance(c.get(field),str) or not c[field].strip():e.append(f'CARD_FIELD_MISSING:{cid}:{field}')
        if c.get('discipline') not in DISCIPLINES:e.append(f'BAD_DISCIPLINE:{cid}')
        if not isinstance(c.get('keywords'),list) or not all(isinstance(x,str) and x.strip() for x in c['keywords']):e.append(f'CARD_KEYWORDS:{cid}')
        if not isinstance(c.get('source_ids'),list) or not c['source_ids'] or any(x not in sources for x in c['source_ids']):e.append(f'CARD_SOURCE_MISMATCH:{cid}')
    return sorted(set(e))


def recommend(data:dict, term:str, max_results:int=3) -> dict:
    """Exact normalized substring matching, not semantic relevance or fact checking."""
    problems=validate(data)
    if problems:raise ValueError('INVALID_CATALOG:'+';'.join(problems[:5]))
    if max_results not in (1,2,3):raise ValueError('MAX_RESULTS_MUST_BE_1_TO_3')
    needle=(term or '').casefold().strip()
    if not needle:raise ValueError('TOPIC_REQUIRED')
    hits=[]
    for c in data['cards']:
        terms=[x.casefold() for x in c['keywords']]+[c['title'].casefold()]
        score=max([3 for x in terms if needle==x] or [0])
        if not score and any(needle in x or x in needle for x in terms if len(x)>1): score=1
        if score: hits.append((score,c['id'],c))
    hits.sort(key=lambda x:(-x[0],x[1]))
    out=[]
    for _,_,c in hits[:max_results]:
        out.append({'id':c['id'],'title':c['title'],'plain_meaning':c['plain_meaning'],
                    'research_move':c['research_move'],'boundary':c['boundary'],
                    'sources':[{'source_id':sid,'title':data['sources'][sid]['title'],
                                'url':data['sources'][sid]['url'],'scope':data['sources'][sid]['scope'],
                                'locator':data['sources'][sid]['locator']} for sid in c['source_ids']]})
    return {'ok':True,'offline_only':True,'matched':len(out),'cards':out,
            'verification':'pre_bundled_bibliography_not_checked_this_turn',
            'next_step':'use project-specific evidence or user-selected verification; no automatic research'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--validate',action='store_true')
    ap.add_argument('--topic',help='Local task/topic. Input is not stored or echoed.')
    ap.add_argument('--max-results',type=int,default=3)
    args=ap.parse_args()
    try:
        data=json.loads(CATALOG.read_text(encoding='utf-8'))
        if args.validate:
            errors=validate(data); result={'ok':not errors,'issues':errors,'sources':len(data.get('sources',{})),'cards':len(data.get('cards',[]))}
        else:
            if not args.topic:raise ValueError('TOPIC_REQUIRED')
            result=recommend(data,args.topic,args.max_results)
        print(json.dumps(result,ensure_ascii=False))
        return 0 if result['ok'] else 1
    except (ValueError, OSError, json.JSONDecodeError) as ex:
        print(json.dumps({'ok':False,'error':str(ex)},ensure_ascii=False));return 1

if __name__=='__main__':sys.exit(main())
