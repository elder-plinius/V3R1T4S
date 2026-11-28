"""Hybrid fixed-route / joint LNS. Usage: python3 -I hybrid_lns.py <inst_dir> <start.csv> <out_dir> <seconds> <seed> [workers=6] [fixed_iter_s=15] [joint_iter_s=30] [K=3]
Fixed-route slices (cheap) run while they pay; after STALL consecutive fixed iterations with no gain, up to JOINT_TRIES joint slices (routes chosen among K
candidates) are tried; a gain in either returns to fixed-route slices. Acceptance and best.csv use the exact total after re-routing; every final file must be
confirmed by evaluate_independent.py. Logs one JSON line per iteration."""
import sys, os, json, time, random, resource
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ptl, lns, joint
try: resource.setrlimit(resource.RLIMIT_AS, (8 * 1024 ** 3, 8 * 1024 ** 3))
except Exception: pass
STALL, JOINT_TRIES = 6, 6
def main():
    inst, start, out, secs, seed = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 6; fs = float(sys.argv[7]) if len(sys.argv) > 7 else 15
    js = float(sys.argv[8]) if len(sys.argv) > 8 else 30; K = int(sys.argv[9]) if len(sys.argv) > 9 else 3
    os.makedirs(out, exist_ok=True); rng = random.Random(seed)
    I = ptl.Inst(inst); pi = ptl.load_tt(start); assert ptl.feasible(I, pi), 'start infeasible'
    G = ptl.groups(I); tot, w, un = ptl.evaluate_flows(I, pi); start_total = best = tot
    log = open(os.path.join(out, 'log.jsonl'), 'w'); t0 = time.time(); it = acc = 0
    fsize, jsize = 150, 60; fstall = 0; jtries = 0
    print(json.dumps(dict(start_total=tot, events=len(I.ev), groups=len(G), K=K, seed=seed)), flush=True)
    while time.time() - t0 < secs:
        it += 1; left = secs - (time.time() - t0); use_joint = fstall >= STALL and jtries < JOINT_TRIES; t1 = time.time()
        if use_joint:
            kind, F = lns.neighbourhoods(I, G, w, rng, jsize)
            st, naff, cur, val, new = joint.solve_joint(I, pi, F, min(js, max(2.0, left)), workers, rng.randrange(10 ** 6), K, rng); mode = 'joint'; jtries += 1
        else:
            kind, F = lns.neighbourhoods(I, G, w, rng, fsize)
            st, cur, val, new = lns.solve_nb(I, pi, F, w, min(fs, max(1.0, left)), workers, rng.randrange(10 ** 6)); naff = 0; mode = 'fixed'
        rec = dict(it=it, mode=mode, kind=kind, free=len(F), status=st, affected=naff, model_gain=cur - val, sec=round(time.time() - t1, 1), t=round(time.time() - t0, 1))
        gained = False
        if new is not None and val < cur:
            p2 = dict(pi); p2.update(new)
            if ptl.feasible(I, p2):
                tot2, w2, un2 = ptl.evaluate_flows(I, p2)
                if tot2 < tot and un2 == 0:
                    pi, tot, w = p2, tot2, w2; acc += 1; gained = True; rec['total'] = tot
                    if tot < best: best = tot; ptl.save_tt(os.path.join(out, 'best.csv'), pi)
                else: rec['rejected'] = 'exact total did not improve'
            else: rec['rejected'] = 'infeasible'
        if gained: fstall = 0; jtries = 0
        elif use_joint:
            if st in ('OPTIMAL', 'NO_AFFECTED'): jsize = min(int(jsize * 1.2) + 1, len(I.ev))
            elif st == 'TOO_BIG' or st != 'OPTIMAL': jsize = max(30, int(jsize * 0.8))
            if jtries >= JOINT_TRIES: fstall = 0; jtries = 0; fsize = 150     # joint round exhausted: restart fixed-route with fresh neighbourhoods
        else:
            fstall += 1
            if st == 'OPTIMAL': fsize = min(int(fsize * 1.15) + 1, len(I.ev))
            elif fstall % 4 == 0: fsize = max(30, int(fsize * 0.85))
        log.write(json.dumps(rec) + '\n'); log.flush()
    if not os.path.exists(os.path.join(out, 'best.csv')): ptl.save_tt(os.path.join(out, 'best_unchanged.csv'), pi)
    print(json.dumps(dict(start_total=start_total, best_total=best, improved_by=start_total - best, iterations=it, accepted=acc, seconds=round(time.time() - t0, 1), seed=seed)), flush=True)
if __name__ == '__main__': main()
