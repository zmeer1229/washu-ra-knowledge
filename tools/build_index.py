"""Build deterministic retrieval chunks from the curated topic and catalog data."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))

def build():
    chunks = []
    for topic in load('topics.json'):
        text = topic['content']
        for section in re.split(r'(?m)(?=^## )', text):
            section = section.strip()
            if not section:
                continue
            heading = section.splitlines()[0].removeprefix('## ')
            identifier = hashlib.sha256((topic['id']+'\n'+section).encode()).hexdigest()[:14]
            chunks.append({'id':'topic-'+identifier,'kind':'topic_summary','title':topic['title']+' — '+heading,
                           'text':section,'path':topic['path'],'source_ids':[topic['source_id']],
                           'source_url':topic['source_url'],'observed_on':topic['observed_on'],
                           'tags':topic['tags'],'coverage':topic['coverage']})
    for link in load('links.json'):
        chunks.append({'id':link['id'],'kind':'link','title':link['title'],
                       'text':link['title']+'\n'+link['url']+'\n'+link['access'],
                       'path':'LINKS.md','source_ids':link['source_ids'],'source_url':link['url'],
                       'observed_on':link['observed_on'],'tags':link['source_ids'],
                       'coverage':link['verification']})
    for doc in load('documents.json'):
        chunks.append({'id':doc['id'],'kind':'document_reference','title':doc['title'],
                       'text':doc['title']+'\nCategory: '+doc['category']+'\n'+doc['content_status'],
                       'path':'DOCUMENTS.md','source_ids':[doc['source_id']],'source_url':doc['source_url'],
                       'observed_on':doc['observed_on'],'tags':[doc['category']],
                       'coverage':doc['content_status']})
    for item in load('extractions.json'):
        text = (ROOT/item['path']).read_text(encoding='utf-8')
        # Bounded overlapping text windows preserve table cells and long paragraphs.
        for offset in range(0, len(text), 2200):
            section = text[offset:offset+2500]
            chunks.append({'id':item['id']+'-'+str(offset),'kind':item['kind'],
                           'title':item['title'],'text':section,'path':item['path'],
                           'source_ids':[item['source_id']],'source_url':item['source_url'],
                           'observed_on':item['observed_on'],'tags':[item['kind']],
                           'coverage':item['status'],'character_offset':offset})
    (ROOT/'data'/'knowledge.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False,sort_keys=True)+'\n' for c in chunks),encoding='utf-8')
    print(f'Built {len(chunks)} retrieval chunks.')
    return chunks

if __name__=='__main__':
    build()
