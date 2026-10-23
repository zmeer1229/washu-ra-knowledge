"""Search local summaries, reference titles, and links without network access."""
from pathlib import Path
from collections import Counter
import argparse
import json
import math
import re

ROOT=Path(__file__).resolve().parents[1]
STOP={'a','an','and','are','as','at','be','for','from','how','i','in','is','it','of','on','or','the','to','what','where','with'}

def tokens(text):
    return [x for x in re.findall(r'[a-z0-9]+',text.lower()) if x not in STOP]

def search(query,limit=10):
    records=[json.loads(line) for line in (ROOT/'data'/'knowledge.jsonl').read_text(encoding='utf-8').splitlines() if line]
    terms=set(tokens(query))
    if not terms:return []
    counts=[Counter(tokens(r['title']+' '+r['text']+' '+' '.join(r['tags']))) for r in records]
    df={term:sum(term in count for count in counts) for term in terms}
    results=[]
    for r,count in zip(records,counts):
        hits=terms & count.keys()
        if not hits:continue
        score=sum((1+math.log(count[term]))*math.log(1+(len(records)+1)/(df[term]+1)) for term in hits)
        score*=len(hits)/len(terms)
        title_words=set(tokens(r['title']))
        score+=2*len(terms & title_words)
        if len(hits)==len(terms):score+=4
        results.append({**r,'score':round(score,4)})
    return sorted(results,key=lambda x:(-x['score'],x['id']))[:max(1,limit)]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('--limit',type=int,default=10)
    parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    results=search(args.query,args.limit)
    if args.json:
        print(json.dumps(results,ensure_ascii=False,indent=2))
    elif not results:
        print('No matching evidence found. Try another term or consult the original source.')
    else:
        for r in results:
            print(f"[{r['kind']}] {r['title']}\n  {r['path']}\n  Source: {r['source_url']}\n  Observed: {r['observed_on']} | Coverage: {r['coverage']}\n")

if __name__=='__main__':
    main()
