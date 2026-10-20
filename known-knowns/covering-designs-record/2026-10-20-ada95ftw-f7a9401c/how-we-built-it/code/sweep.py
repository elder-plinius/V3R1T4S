#!/usr/bin/env python3
"""Lens structured: intransitive G-set orbit covers for C(v,k,3), k in {5,6,7}, v in 29..40, SCIP MIP (new space vs runs 1802/1303).
usage: sweep.py cap workers worker_id nworkers outdir   (jobs list built deterministically; round-robin split)"""
import sys, os, json, itertools, random, pickle, time
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsets, kmcover
RUN = os.environ.get('V3R1T4S_RUN', '.')  # the run folder holding the cached actions.pkl; was an absolute workspace path (only edit)
snap = json.load(open(f'{RUN}/data/coverdata.json'))
EXCL = {(29,5,3), (20,6,3)}
OLD = {'A5', 'S5', 'PSL27'}

def schon(v,k,t):
    L=1
    for i in range(t-1,-1,-1): L=-(-(v-i)*L//(k-i))
    return L

def get_actions():
    pk = f'{RUN}/attempts/structured/output/actions.pkl'
    if os.path.exists(pk): return pickle.load(open(pk,'rb'))
    A = {n: gsets.actions(n, g, 40) for n, g in gsets.all_groups().items()}
    pickle.dump(A, open(pk,'wb')); return A

def jobs():
    A = get_actions(); J = []
    for gname, (order, acts) in A.items():
        for r in (1,2,3):
            for combo in itertools.combinations_with_replacement(range(len(acts)), r):
                v = sum(acts[i][0] for i in combo)
                if not 29 <= v <= 40: continue
                nf = sum(1 for i in combo if acts[i][0]==1)
                if nf > 2 or nf == len(combo): continue
                for k in (5,6,7):
                    if (v,k,3) in EXCL: continue
                    if gname in OLD and ((k==5 and v<=32) or (k==6 and v<=30) or (k==7 and v<=30 and comb(v,7)<=700000)): continue
                    s = snap.get(f'C({v},{k},3)')
                    if not s or s['size'] <= s['low_bd']: continue
                    ratio = s['size']/schon(v,k,3)
                    if ratio < 1.05: continue
                    if comb(v,k)/order > 60000 or comb(v,k) > 6000000: continue
                    J.append((v,k,gname,combo))
    # round-robin over cells, cells ordered by ratio desc; within a cell, deterministic shuffle
    cells = {}
    for j in J: cells.setdefault((j[0],j[1]), []).append(j)
    rnd = random.Random(20261020)
    for c in cells.values(): rnd.shuffle(c)
    order = sorted(cells, key=lambda c: -snap[f'C({c[0]},{c[1]},3)']['size']/schon(c[0],c[1],3))
    out = []; i = 0
    while any(cells[c] for c in order):
        for c in order:
            if cells[c]: out.append(cells[c].pop(0))
    return A, out

def perms_for(A, gname, combo):
    order, acts = A[gname]; ng = len(acts[0][2]); perms = [[] for _ in range(ng)]; off = 0; sig = []
    for i in combo:
        d, h, pa = acts[i]; sig.append([d, h])
        for j, p in enumerate(pa): perms[j] += [x+off for x in p]
        off += d
    return perms, sig

if __name__ == '__main__':
    cap, workers, w, nw, outdir = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    A, J = jobs()
    if w == 0: print(f'total jobs {len(J)}', flush=True)
    # RESUME: phase-1 workers (4-way split, files res_w0..3.jsonl) wrote rows in job order; skip those jobs
    done = set()
    for pw in range(4):
        f = f'{outdir}/res_w{pw}.jsonl'
        n = sum(1 for _ in open(f)) if os.path.exists(f) else 0
        done |= set(range(len(J)))[pw::4][:n] if False else set(list(range(len(J)))[pw::4][:n])
    rest = [J[i] for i in range(len(J)) if i not in done]
    if w == 0: print(f'done {len(done)} remaining {len(rest)}', flush=True)
    mine = rest[w::nw]
    with open(f'{outdir}/res2_w{w}.jsonl', 'a') as fh:
        for n, (v,k,gname,combo) in enumerate(mine):
            perms, sig = perms_for(A, gname, combo); t0 = time.time()
            r = kmcover.solve_mip(perms, v, k, 3, cap=cap, threads=workers)
            s = snap[f'C({v},{k},3)']
            row = dict(group=gname, orbits=sig, v=v, k=k, t=3, status=r['status'], korb=r.get('korb'), torb=r.get('torb'),
                       best=r.get('best'), bound=r.get('bound'), snap=s['size'], low_bd=s['low_bd'], sec=round(time.time()-t0,1))
            if r.get('best') and r['best'] < s['size']:
                ok = kmcover.check(r['blocks'], v, k, 3)
                fn = f"{outdir}/C{v}_{k}_3_{gname}_{'-'.join(str(a[0]) for a in sig)}_{r['best']}.txt"
                open(fn,'w').write('\n'.join(' '.join(map(str,b)) for b in r['blocks'])+'\n'); row['file'] = os.path.basename(fn); row['selfcheck'] = ok
                print('BELOW_SNAPSHOT', json.dumps(row), flush=True)
            fh.write(json.dumps(row)+'\n'); fh.flush()
            print(f'[{n+1}/{len(mine)}]', json.dumps(row), flush=True)
