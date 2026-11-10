import json,pathlib,hashlib,sys,collections
p=pathlib.Path(sys.argv[1]);obj=json.loads(p.read_text());words=obj['words'];n=obj['n'];d=obj['d'];comp=dict(zip('ACGT','TGCA'))
assert len(set(words))==len(words)
assert all(len(w)==n and set(w)<=set(comp) and sum(x in 'GC' for x in w)==n//2 for w in words)
rc=lambda w:''.join(comp[c] for c in w[::-1])
ham=lambda a,b:sum(x!=y for x,y in zip(a,b))
h=[ham(a,b) for i,a in enumerate(words) for b in words[i+1:]]
r=[ham(a,rc(b)) for a in words for b in words]
assert min(h)>=d and min(r)>=d
print(json.dumps({'valid':True,'n':n,'d':d,'gc':n//2,'size':len(words),'ordinary_pairs':len(h),'rc_ordered_pairs_including_self':len(r),'ordinary_min':min(h),'rc_min':min(r),'ordinary_hist':dict(collections.Counter(h)),'rc_hist':dict(collections.Counter(r)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},sort_keys=True))
