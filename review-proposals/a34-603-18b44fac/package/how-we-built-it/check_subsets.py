#!/usr/bin/env python3
"""Alternate exact verifier: parse text supports and prohibit repeated four-subsets.
This file does not import the pairwise checker or either C++ search implementation.
"""
import argparse,hashlib,itertools,json,pathlib,sys

def check(path,minimum=603):
    p=pathlib.Path(path); result={'artifact':str(p),'method':'text supports / four-subset uniqueness','pass':False}
    try:
        raw=p.read_bytes(); result['sha256']=hashlib.sha256(raw).hexdigest()
        rows=raw.decode('ascii').splitlines(); result['word_count']=len(rows)
        if len(rows)<minimum: raise ValueError('cardinality below target')
        if len(set(rows))!=len(rows): raise ValueError('duplicate codeword')
        used={}; total=0
        for row,s in enumerate(rows):
            if len(s)!=34 or any(ch not in '01' for ch in s): raise ValueError('invalid binary word or length')
            positions=[i+1 for i,ch in enumerate(s) if ch=='1']
            if len(positions)!=7: raise ValueError('wrong weight')
            for subset in itertools.combinations(positions,4):
                total+=1
                if subset in used:
                    result['violating_pair']=[used[subset],row]; result['repeated_subset']=subset
                    raise ValueError('repeated four-subset')
                used[subset]=row
        result.update({'pass':True,'four_subsets_checked':total,'distinct_four_subsets':len(used),'repeated_four_subsets':0})
    except Exception as exc: result['error']=f'{type(exc).__name__}: {exc}'
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('path');ap.add_argument('--minimum',type=int,default=603);ap.add_argument('--output');a=ap.parse_args()
    r=check(a.path,a.minimum);s=json.dumps(r,indent=2);print(s)
    if a.output:pathlib.Path(a.output).write_text(s+'\n')
    return 0 if r['pass'] else 1
if __name__=='__main__':sys.exit(main())
