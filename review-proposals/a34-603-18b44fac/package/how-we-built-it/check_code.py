#!/usr/bin/env python3
"""Independent, exhaustive binary constant-weight code verifier. Standard library only."""
import argparse, hashlib, json, pathlib, sys

def check(path, n=34, w=7, d=8, minimum=603, exact=None):
    p=pathlib.Path(path)
    result={'artifact':str(p),'parameters':{'n':n,'w':w,'d_min':d,'min_words':minimum,'exact_words':exact},'pass':False}
    try:
        raw=p.read_bytes()
        result['sha256']=hashlib.sha256(raw).hexdigest()
        lines=raw.decode('ascii').splitlines()
        if not lines: raise ValueError('empty code')
        if any(len(s)!=n or set(s)-{'0','1'} for s in lines): raise ValueError('nonbinary word, blank line, or wrong length')
        words=[int(s,2) for s in lines]
        result['word_count']=len(words)
        if len(words)<minimum: raise ValueError('cardinality below target')
        if exact is not None and len(words)!=exact: raise ValueError('wrong exact cardinality')
        if len(set(words))!=len(words): raise ValueError('duplicate codeword')
        if any(v.bit_count()!=w for v in words): raise ValueError('wrong Hamming weight')
        least=n+1; pairs=0
        for i,a in enumerate(words):
            for j in range(i):
                dist=(a^words[j]).bit_count(); pairs+=1
                least=min(least,dist)
                if dist<d:
                    result['violating_pair']=[j,i]; result['distance']=dist
                    raise ValueError('minimum Hamming distance violated')
        result.update({'pass':True,'pairs_checked':pairs,'observed_min_distance':None if len(words)<2 else least})
    except Exception as exc:
        result['error']=f'{type(exc).__name__}: {exc}'
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('path'); ap.add_argument('--n',type=int,default=34)
    ap.add_argument('--w',type=int,default=7); ap.add_argument('--d',type=int,default=8)
    ap.add_argument('--minimum',type=int,default=603); ap.add_argument('--exact',type=int)
    ap.add_argument('--output'); a=ap.parse_args()
    result=check(a.path,a.n,a.w,a.d,a.minimum,a.exact)
    text=json.dumps(result,indent=2); print(text)
    if a.output: pathlib.Path(a.output).write_text(text+'\n')
    return 0 if result['pass'] else 1
if __name__=='__main__': sys.exit(main())
