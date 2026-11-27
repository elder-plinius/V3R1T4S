from itertools import combinations
from math import log2
from pathlib import Path
import json
from nine_boxes import certificate

current={tuple(c):rows for c,rows in json.loads(Path("r13/nine-boxes.json").read_text())["boxes"]}
failed=set()
def union(a,b): return tuple(None if x is None or y is None else max(x,y) for x,y in zip(a,b))
def size(a): return sum(log2(30 if x is None else x) for x in a)
def fits(a,b): return all(y is None or x is not None and x<=y for x,y in zip(a,b))
def save():
    Path("r13/nine-compact.json").write_text(json.dumps({"boxes":list(current.items())},separators=(",",":"))+"\n")
save()
while True:
    candidates=[]
    caps=list(current)
    for a,b in combinations(caps,2):
        c=union(a,b)
        if c in failed: continue
        candidates.append((size(c)-min(size(a),size(b)),a,b,c))
    changed=0
    for _,a,b,c in sorted(candidates,key=lambda t:t[0]):
        if a not in current or b not in current or c in failed: continue
        rows=current.get(c) or certificate(c,False)
        if rows is None: failed.add(c); continue
        for sub in list(current):
            if fits(sub,c): del current[sub]
        current[c]=rows
        changed+=1
        save()
    print("remain",len(current),"merged",changed,"invalid tested",len(failed),flush=True)
    if not changed: break
