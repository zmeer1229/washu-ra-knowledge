"""Validate source provenance, retrieval data, local links, and publication boundaries."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json
import re

ROOT=Path(__file__).resolve().parents[1]

def main():
    files=list(ROOT.rglob('*.json'))
    data={p.name:json.loads(p.read_text(encoding='utf-8')) for p in files}
    sources={x['id'] for x in data['sources.json']}
    for filename in ['topics.json','links.json','documents.json']:
        ids=[]
        for row in data[filename]:
            ids.append(row['id'])
            assert row.get('observed_on'),(filename,row['id'],'missing date')
            refs=row.get('source_ids',[row.get('source_id')])
            assert all(ref in sources for ref in refs),(filename,row['id'],'unknown source')
            url=row.get('url',row.get('source_url'))
            assert urlsplit(url).scheme in {'http','https'},url
        assert len(ids)==len(set(ids)),filename
    assert len(data['campus-resources.json'])==30
    assert data['coverage.json']['site_pages_listed']==len(data['coverage.json']['page_filenames_observed'])==15
    for topic in data['topics.json']:
        assert (ROOT/topic['path']).is_file(),topic['path']
    chunks=[json.loads(l) for l in (ROOT/'data'/'knowledge.jsonl').read_text(encoding='utf-8').splitlines() if l]
    assert len(chunks)==len({x['id'] for x in chunks})
    assert all(set(x['source_ids']) <= sources for x in chunks)
    for doc in data['documents.json']:
        assert 'not extracted' in doc['content_status']
    for p in ROOT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if re.match(r'https?://',target):continue
            dest=(p.parent/unquote(target.split('#')[0])).resolve()
            assert dest.is_relative_to(ROOT.resolve()) and dest.exists(),(p,target)
    # Disallow unreviewed source captures and access-bearing URL formats in public output.
    for p in ROOT.rglob('*'):
        if not p.is_file() or '.git' in p.parts or '__pycache__' in p.parts:continue
        if p.suffix not in {'.md','.json','.jsonl','.txt'}:continue
        text=p.read_text(encoding='utf-8')
        assert not re.search(r'https?://[^\s"<>]*\.box\.com/s/',text),p
        assert not re.search(r'[?&](?:login_hint|authkey|code_challenge|migratedSettings|access_token)=',text,re.I),p
        assert '"snapshot":' not in text and '"headings":' not in text,p
        assert not re.search(r'Homebase code[^\n]*:\s*[A-Z0-9]{5,}',text),p
    from search import search
    for query,wanted in [('roommate mediation','document_reference'),('winter meeting','topic_summary'),('maintenance','link')]:
        results=search(query,20)
        assert results and any(x['kind']==wanted for x in results),(query,wanted)
    print(f'Validated {len(data["topics.json"])} topics, {len(data["links.json"])} links, {len(data["documents.json"])} document references, {len(chunks)} retrieval chunks, provenance, and local links.')

if __name__=='__main__':
    main()
