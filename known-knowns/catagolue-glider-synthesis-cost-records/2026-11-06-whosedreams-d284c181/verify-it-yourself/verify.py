#!/usr/bin/env python3
from pathlib import Path
import hashlib,sys
from life_check import parse_rle,check,step,BASE_GLIDER,glider_direction,decode_apgcode,components
from strict_partition import stable_subsets,controls

def main():
    p=Path('object/xs28_69a4owgzxol5d1d96.rle')
    expected='d284c181264957fe8995ca244ea095542d9c326da9908c72f6e1091b3abe0961'
    if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
        print('object integrity mismatch');return False
    rule,cells=parse_rle(p.read_text())
    assert rule.upper().replace('/','')=='B3S23'
    block={(0,0),(1,0),(0,1),(1,1)}
    assert step(block)==block and step({(0,0)})==set()
    assert glider_direction(BASE_GLIDER)==(1,1)
    controls()
    r=check(cells,'xs28_69a4owgzxol5d1d96')
    assert r['ok'] and r['n_gliders']==7 and r['period']==1 and r['final_population']==28
    target_cells=decode_apgcode('xs28_69a4owgzxol5d1d96')[2]
    islands=components(target_cells)
    print('target islands:', sorted(map(len,islands)), 'stable independently:', [step(c)==c for c in islands])
    assert len(islands)==2 and all(step(c)!=c for c in islands)
    s=stable_subsets(target_cells);print('exact strictness:',s)
    assert s['strict']
    print('numerical synthesis and exact strictness verified; live table absence is a dated panel record, not asserted anew by this offline checker')
    return True
if __name__=='__main__':
    try: good=main()
    except Exception as e: print(type(e).__name__+': '+str(e));good=False
    print('PASS' if good else 'FAIL');sys.exit(0 if good else 1)
