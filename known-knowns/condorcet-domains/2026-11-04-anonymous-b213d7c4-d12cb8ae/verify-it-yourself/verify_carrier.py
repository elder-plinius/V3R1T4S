"""Run from a final package root; metadata and object are read, never changed."""
from pathlib import Path
import csv, hashlib, json, sys
import prefix_count, suffix_count

try:
    with Path('INDEX.csv').open() as stream:
        rows=list(csv.DictReader(stream))
    if len(rows)!=1 or rows[0]['target_id']!='condorcet-domains':raise ValueError('one target cell required')
    info=rows[0];path=Path(info['file']);expected=int(info['value'])
    if path.is_absolute() or '..' in path.parts or path.parts[0]!='object':raise ValueError('invalid object path')
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=info['sha256']:raise ValueError('object hash mismatch')
    n,rules=prefix_count.parse(path)
    if n!=25:raise ValueError('wrong n')
    p,ps=prefix_count.count(n,rules)
    srules=suffix_count.parse(path,n);s,ss=suffix_count.count(n,srules)
    if p!=expected or s!=expected or expected<=186216544:raise ValueError('exact count or threshold mismatch')
    print(json.dumps(dict(n=n,count=p,independent_suffix_count=s,prefix_states=ps,suffix_states=ss,sha256=digest),sort_keys=True))
    print(json.dumps(dict(prefix_calibration=prefix_count.selftest(),suffix_calibration=suffix_count.calibrate()),sort_keys=True))
    for n0,value in [(9,488),(20,2115186)]:
        triples=prefix_count.combinations(range(n0),3)
        fish=[(t,1,0 if (t[1]+1)%2==0 else 2) for t in triples]
        assert prefix_count.count(n0,fish)[0]==value
    sub=[r for r in rules if max(r[0])<9]
    assert prefix_count.count(9,sub)[0]==prefix_count.brute(9,sub)
    print('PASS')
except Exception as error:
    print(type(error).__name__+': '+str(error));print('FAIL');sys.exit(1)
