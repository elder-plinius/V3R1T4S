"""
pivot_cover.py - add one vertex x to a regular graph without wasting the cut.

For a cover S (balls of radius D-1 cover V), each s in S must give up one incident edge (s,t).
Instead of deleting (s,t), the edge is PIVOTED to a deficient vertex u: delete (s,t), add (t,u),
which keeps every degree legal (t unchanged, u gains its free slot). x then joins every s.
Cut target and pivot partner are chosen greedily by exact bad-pair count.

usage: pivot_cover.py <edges> <Delta> <D> <out_prefix> [cover_trials]
"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ddlib import load_graph, edges_to_adj, reach_sets, bad_pairs, write_edges


def cost_of(n, E, Delta, D, adj_free=None):
    adj, deg = edges_to_adj(n, E, Delta)
    W = (n + 63) // 64
    R = np.zeros((n, W), np.uint64); Rn = np.zeros_like(R)
    defic = np.zeros(n, np.int64)
    return int(bad_pairs(adj, deg, n, D, W, R, Rn, defic))


def greedy_cover(n, W, B, picks, trials=60, seed=0):
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(trials):
        cand = np.arange(n); rng.shuffle(cand)
        cov = np.zeros(W, np.uint64); chosen = []
        for _ in range(picks):
            gains = np.unpackbits((B[cand] & ~cov[None, :]).view(np.uint8), axis=-1).sum(1)
            i = int(np.argmax(gains))
            if gains[i] == 0:
                break
            chosen.append(int(cand[i])); cov |= B[cand[i]]; cand = np.delete(cand, i)
        unc = n - int(np.unpackbits(cov.view(np.uint8)).sum())
        if best is None or (unc, len(chosen)) < (best[0], len(best[1])):
            best = (unc, chosen)
    return best


def main():
    path, Delta, D, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    trials = int(sys.argv[5]) if len(sys.argv) > 5 else 60
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    n, E = load_graph(path)
    adj, deg = edges_to_adj(n, E, Delta)
    W = (n + 63) // 64
    R = np.zeros((n, W), np.uint64); Rn = np.zeros_like(R)
    B = reach_sets(adj, deg, n, D - 1, W, R, Rn).copy()
    unc, S = greedy_cover(n, W, B, Delta, trials)
    print(f"n={n} cover size={len(S)} uncovered={unc} free={int((deg<Delta).sum())}", flush=True)
    if unc != 0:
        return
    Eset = set(tuple(sorted(map(int, e))) for e in E)
    cur = sorted(Eset)
    free = [v for v in range(n) if deg[v] < Delta]
    # free slots per vertex
    slots = {v: int(Delta - deg[v]) for v in free}
    print(f"total free slots {sum(slots.values())}", flush=True)
    deadline = time.time() + 1200
    for s in S:
        if time.time() > deadline:
            break
        present = [e for e in Eset if s in e]
        # 1) cheapest edge to delete on its own
        scored = []
        for e in present:
            base = [x for x in cur if x != e]
            scored.append((cost_of(n, base, Delta, D), e))
        scored.sort()
        best = (scored[0][0], scored[0][1], None)
        # 2) pivot the two cheapest edges to each free vertex
        for base_cost, e in scored[:2]:
            t = e[0] if e[1] == s else e[1]
            base = [x for x in cur if x != e]
            for u in free:
                if slots.get(u, 0) <= 0 or u in (t, s) or tuple(sorted((t, u))) in Eset:
                    continue
                trial = base + [tuple(sorted((t, u)))]
                c = cost_of(n, trial, Delta, D)
                if c < best[0]:
                    best = (c, e, u)
        if best is None:
            break
        c, e, u = best
        cur = [x for x in cur if x != e]; Eset.discard(e)
        t = e[0] if e[1] == s else e[1]
        if u is not None:
            cur.append(tuple(sorted((t, u)))); Eset.add(tuple(sorted((t, u))))
            slots[u] -= 1
        print(f"pivot {e} -> {u}: cost {c}", flush=True)
        if c == 0 and len(cur) == len(E) - 1 + (1 if u else 0):
            pass
    x = n
    for s in S:
        cur.append((min(x, s), max(x, s)))
    final = cost_of(n + 1, cur, Delta, D)
    print(f"final cost N={n+1}: {final}", flush=True)
    write_edges(out + f"_N{n+1}_c{final}.edges", np.array(cur, np.int64),
                f"{Delta},{D} N={n+1} pivot-cover cost={final}")


if __name__ == '__main__':
    main()
