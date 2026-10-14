"""Independent exhaustive constant-weight feasibility test; standard library only."""
import hashlib,itertools,json,pathlib,sys,time

def check(path):
    raw=path.read_bytes(); lines=raw.decode('ascii').splitlines()
    assert len(lines)==13026, 'wrong size'
    assert all(len(x)==27 and set(x)<={'0','1'} for x in lines), 'nonbinary or wrong length'
    assert all(x.count('1')==10 for x in lines), 'wrong weight'
    assert len(set(lines))==len(lines), 'duplicate'
    # For weight ten: distance=20-2*intersection. Distance <6 iff
    # intersection >=8, iff an eight-element subset is repeated.
    seen=set(); examined=0
    for row in lines:
        support=[i for i,b in enumerate(row) if b=='1']
        for s in itertools.combinations(support,8):
            mask=sum(1<<i for i in s)
            assert mask not in seen, 'distance below six'
            seen.add(mask); examined+=1
    return dict(status='PASS',sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),words=len(lines),length=27,weight=10,distance_at_least=6,subsets_examined=examined,unique_subsets=len(seen),check='all eight-element support subsets are distinct')
if __name__=='__main__':
    print(json.dumps(check(pathlib.Path(sys.argv[1])),indent=2))
