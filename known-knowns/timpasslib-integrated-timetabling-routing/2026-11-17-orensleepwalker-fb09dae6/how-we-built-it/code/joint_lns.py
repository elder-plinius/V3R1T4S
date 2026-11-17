"""Joint route + timetable LNS loop. Usage: python3 -I joint_lns.py <inst_dir> <start.csv> <out_dir> <seconds> <seed> [workers=6] [iter_seconds=15] [size0=120] [K=3]
Same loop as lns.py but each slice is solved with joint.solve_joint (routes chosen among K candidates per affected OD pair).
Acceptance and the saved best.csv use the exact total after re-routing (ptl.evaluate_flows); the independent evaluator must confirm the final file."""
import sys, os, json, time, random, resource, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ptl, lns, joint
try: resource.setrlimit(resource.RLIMIT_AS, (8 * 1024 ** 3, 8 * 1024 ** 3))
except Exception: pass
def main():
    inst, start, out, secs, seed = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 6; iter_s = float(sys.argv[7]) if len(sys.argv) > 7 else 15
    size = int(sys.argv[8]) if len(sys.argv) > 8 else 120; K = int(sys.argv[9]) if len(sys.argv) > 9 else 3
    os.makedirs(out, exist_ok=True); rng = random.Random(seed)
    I = ptl.Inst(inst); pi = ptl.load_tt(start); assert ptl.feasible(I, pi), 'start infeasible'
    G = ptl.groups(I); tot, w, un = ptl.evaluate_flows(I, pi); start_total = best = tot
    log = open(os.path.join(out, 'log.jsonl'), 'w'); t0 = time.time(); it = acc = stall = 0
    print(json.dumps(dict(start_total=tot, events=len(I.ev), groups=len(G), K=K)), flush=True)
    while time.time() - t0 < secs:
        it += 1; kind, F = lns.neighbourhoods(I, G, w, rng, size); t1 = time.time()
        st, naff, cur, val, new = joint.solve_joint(I, pi, F, min(iter_s, max(2.0, secs - (time.time() - t0))), workers, rng.randrange(10 ** 6), K, rng)
        rec = dict(it=it, kind=kind, free=len(F), status=st, affected=naff, model_gain=cur - val, sec=round(time.time() - t1, 1), t=round(time.time() - t0, 1))
        if new is not None and val < cur:
            p2 = dict(pi); p2.update(new)
            if ptl.feasible(I, p2):
                tot2, w2, un2 = ptl.evaluate_flows(I, p2)
                if tot2 < tot and un2 == 0:
                    pi, tot, w = p2, tot2, w2; acc += 1; stall = 0; rec['total'] = tot
                    if tot < best: best = tot; ptl.save_tt(os.path.join(out, 'best.csv'), pi)
                else: rec['rejected'] = 'exact total did not improve'
            else: rec['rejected'] = 'infeasible'
        else:
            stall += 1
            if st in ('OPTIMAL', 'NO_AFFECTED'): size = min(int(size * 1.15) + 1, len(I.ev))
            elif st == 'TOO_BIG' or (st != 'OPTIMAL' and stall % 4 == 0): size = max(30, int(size * 0.8))
        log.write(json.dumps(rec) + '\n'); log.flush()
    if not os.path.exists(os.path.join(out, 'best.csv')): ptl.save_tt(os.path.join(out, 'best_unchanged.csv'), pi)
    print(json.dumps(dict(start_total=start_total, best_total=best, improved_by=start_total - best, iterations=it, accepted=acc, seconds=round(time.time() - t0, 1), seed=seed, final_size=size, K=K)), flush=True)
if __name__ == '__main__': main()
