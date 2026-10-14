#!/usr/bin/env python3
"""Completely self-contained mathematical verifier. No external dependencies."""
from pathlib import Path
import hashlib,sys,itertools,collections,json
C=Path(__file__).resolve().parents[1]
EXPECT='18b44fac5d5ff1d4895fd9de1240669eb71543b3e15599f7f864e090aa1491ad'
BASE='1a1d0958047e78b8d29752ccb0210518b170663b6862f84d57669c7b0c02d81e'
def sha(b):return hashlib.sha256(b).hexdigest()
def check(p):
    data=p.read_bytes();rows=data.decode('ascii').splitlines();assert data.endswith(b'\n')
    assert len(rows)==603 and len(set(rows))==603,'count or distinctness'
    assert all(len(x)==34 and set(x)<={'0','1'} and x.count('1')==7 for x in rows),'format/weight'
    nums=[int(x,2) for x in rows];counts=collections.Counter()
    for a,b in itertools.combinations(nums,2):
        d=(a^b).bit_count();assert d>=8,('distance',d);counts[d]+=1
    assert sum(counts.values())==181503
    supports=set()
    for w in rows:
        p=[i for i,ch in enumerate(w) if ch=='1']
        for four in itertools.combinations(p,4):
            assert four not in supports,('four-subset reused',four)
            supports.add(four)
    assert len(supports)==21105
    assert sha(data)==EXPECT,'witness hash mismatch'
    print('count=603 pair_checks=181503 min_distance='+str(min(counts))+' four_subsets=21105 collisions=0')
    print('histogram='+json.dumps(dict(sorted(counts.items()))))
    return data

def replay():
    p=C/'how-we-built-it/A34_8_7_602.txt'; seed=p.read_bytes();assert sha(seed)==BASE
    old=seed.decode('ascii').splitlines();delta=json.loads((C/'how-we-built-it/seed_to_result_delta.json').read_text())
    remove=set(delta['remove']);add=set(delta['add'])
    assert len(old)==len(set(old))==602
    assert len(remove)==38 and len(add)==39 and remove<=set(old) and not add.intersection(old)
    got=('\n'.join(sorted(set(old)-remove|add))+'\n').encode('ascii')
    assert sha(got)==EXPECT and got==(C/'object/A34_8_7_603.txt').read_bytes(),'delta replay mismatch'
    # verify inverse certificate as well
    restored=('\n'.join(sorted((set(got.decode('ascii').splitlines())-add)|remove))+'\n').encode('ascii')
    assert restored==seed,'inverse replay mismatch'
    print('delta remove=38 add=39 reconstructed_sha256='+sha(got))

if __name__=='__main__':
    try:
        check(C/'object/A34_8_7_603.txt');replay();print('PASS')
    except Exception as e:
        print('FAIL:',repr(e));sys.exit(1)
