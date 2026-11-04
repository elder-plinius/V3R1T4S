#!/usr/bin/env python3
"""Independent complete finite validation; standard library, no network or deletion."""
from pathlib import Path
import json, shutil, subprocess, sys

def main():
    root=Path(__file__).resolve().parent.parent
    obj=json.loads((root/'object/DECISION.json').read_text(encoding='utf-8'))
    fixed={'schema':1,'target':'windmill-kn2-harmonious-graham-sloane','partial_win':'p1',
           'n':10,'q':90,'vertices':19,'harmonious':False}
    if any(obj.get(k)!=v or type(obj.get(k)) is not type(v) for k,v in fixed.items()):
        raise ValueError('wrong graph or decision')
    counts={'nodes':91726677,'leaves':1702800,'masks':1571472,'complement_pairs':0}
    if obj.get('independent_counts')!=counts:
        raise ValueError('unexpected certificate counts')
    scope='There is no injective labeling of the 19 vertices of two copies of K10 sharing exactly one vertex by residues modulo 90 for which the 90 within-clique edge sums are all distinct modulo 90.'
    if obj.get('scope')!=scope:
        raise ValueError('scope differs')
    pwsh=shutil.which('pwsh')
    if not pwsh:
        raise RuntimeError('PowerShell 7.3+ with UInt128 support is required')
    run=subprocess.run([pwsh,'-NoProfile','-File',str(root/'verify-it-yourself/run-independent.ps1'),'-Size','10','-Seconds','600'],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',timeout=630)
    results=[]
    for line in run.stdout.splitlines():
        if line.startswith('{'):
            row=json.loads(line)
            if row.get('kind')=='result': results.append(row)
    if run.returncode!=0 or len(results)!=1:
        raise RuntimeError('independent verifier failed to return one result')
    result=results[0]
    if result.get('n')!=10 or result.get('q')!=90 or result.get('status')!='COMPLETE' or result.get('found') is not False or result.get('reason'):
        raise ValueError('incomplete or different decision')
    if any(result.get(k)!=v for k,v in counts.items()):
        raise ValueError('recomputed counts differ')
    clean={k:result[k] for k in ('n','q','status','found','nodes','leaves','masks','complement_pairs','elapsed','peak_working_bytes')}
    print(json.dumps(clean,sort_keys=True))
    print('PASS')

if __name__=='__main__':
    try: main()
    except Exception as exc:
        print(type(exc).__name__+': '+str(exc))
        print('FAIL')
        sys.exit(1)
