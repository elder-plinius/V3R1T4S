#!/usr/bin/env python3
"""Run 2026-10-20-2256: SCIP orbit cover on run 1757's LIVE LP-screened jobs (ceil(LP) < table), smallest orbit count
first, korb <= 20000 only (memory). Table = min(live archive 22:56:37Z, LJCR GitHub, Zenodo v1.2), plus own values.
usage: live_mip.py cap worker nworkers outdir"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep as sw, kmcover
P = os.environ.get('V3R1T4S_LP_DIR', '.')  # the earlier run's LP-screen output folder (live_jobs.json, lp_w*.jsonl); was an absolute path
HERE = os.environ.get('V3R1T4S_RUN', '.')  # this run's folder (data/ table files); was an absolute path
OWN = {(38,6,3): 469, (35,5,3): 713, (37,6,3): 468}
def tables():
    gh = json.load(open(f'{HERE}/data/coverdata.json')); zn = json.load(open(f'{HERE}/data/zenodo_coverdata.json')); live = {}
    for ln in open(f'{HERE}/data/coveringrepo_archive_vkt.txt'):
        p = ln.split()
        if len(p) == 5: live[(int(p[0]), int(p[1]), int(p[2]))] = int(p[4])
    return gh, zn, live
def best_known(gh, zn, live, v, k, t):
    key = f'C({v},{k},{t})'; vals = [d[key]['size'] for d in (gh, zn) if key in d]
    if (v,k,t) in live: vals.append(live[(v,k,t)])
    if (v,k,t) in OWN: vals.append(OWN[(v,k,t)])
    return min(vals)
if __name__ == '__main__':
    cap, w, nw, outdir = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    live_ids = set(json.load(open(f'{P}/live_jobs.json')))
    rows = {}
    for f in ('lp_w0.jsonl', 'lp_w1.jsonl'):
        for l in open(f'{P}/{f}'):
            r = json.loads(l)
            if r['job'] in live_ids and r['status'] == 'LIVE': rows[r['job']] = r
    todo = sorted((r for r in rows.values() if r['korb'] <= 20000), key=lambda r: (r['korb'], r['job']))
    if w == 0: print(f'live {len(live_ids)} with LP row {len(rows)} korb<=20000 {len(todo)}', flush=True)
    A, J = sw.jobs(); gh, zn, live = tables()
    fn_out = f'{outdir}/mip_w{w}.jsonl'
    seen = set(json.loads(l)['job'] for l in open(fn_out)) if os.path.exists(fn_out) else set()
    mine = [r for r in todo[w::nw] if r['job'] not in seen]
    with open(fn_out, 'a') as fh:
        for n, lr in enumerate(mine):
            i = lr['job']; v, k, gname, combo = J[i]
            assert (v, k, gname, list(combo)) == (lr['v'], lr['k'], lr['group'], lr['combo']), i
            perms, sig = sw.perms_for(A, gname, combo); t0 = time.time()
            bk = best_known(gh, zn, live, v, k, 3)
            r = kmcover.solve_mip(perms, v, k, 3, cap=cap, threads=1)
            row = dict(job=i, group=gname, combo=list(combo), orbits=sig, v=v, k=k, t=3, status=r['status'], korb=r.get('korb'),
                       best=r.get('best'), bound=r.get('bound'), lp=lr['lp'], table=bk, sec=round(time.time()-t0,1))
            if r.get('best') and r['best'] < bk:
                ok = kmcover.check(r['blocks'], v, k, 3)
                fn = f"{outdir}/C{v}_{k}_3_{gname}_{'-'.join(str(a[0]) for a in sig)}_{r['best']}_job{i}.txt"
                open(fn,'w').write('\n'.join(' '.join(map(str,b)) for b in r['blocks'])+'\n'); row['file'] = os.path.basename(fn); row['selfcheck'] = ok
                print('BELOW_TABLE', json.dumps(row), flush=True)
            fh.write(json.dumps(row)+'\n'); fh.flush()
            print(f'[{n+1}/{len(mine)}]', json.dumps(row), flush=True)
