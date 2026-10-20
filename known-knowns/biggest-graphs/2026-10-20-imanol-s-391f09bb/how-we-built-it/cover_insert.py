"""
cover_insert.py - attach new vertex/vertices to free-degree vertices of a trophy graph.

For D=4 and one new vertex x joined to a set S: dist(x,v) = 1 + min_{s in S} dist(s,v),
so x has eccentricity <= D iff every vertex lies in some closed (D-1)-ball B_{D-1}(s).
Coverage is exact set cover over bitsets; the resulting graph is verified by ddlib.exact_cost.

usage: cover_insert.py <edges> <Delta> <D> <k> <seconds>
"""
import sys, time, json
import numpy as np
from ddlib import load_graph, edges_to_adj, reach_sets, exact_cost, write_edges, adj_to_edges, add_edge

def main():
    path, Delta, D, k, secs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
    n, E = load_graph(path)
    adj, deg = edges_to_adj(n, E, Delta)
    W = (n + 63) // 64
    R = np.zeros((n, W), np.uint64); Rn = np.zeros_like(R)
    t0 = time.time()
    B = reach_sets(adj, deg, n, D - 1, W, R, Rn).copy()
    print(f"n={n} m={len(E)} Delta={Delta} D={D} reach_sets_s={time.time()-t0:.2f}", flush=True)
    covcnt = np.unpackbits(B.view(np.uint8), axis=-1).sum(1)
    print("ball sizes: min", covcnt.min(), "median", int(np.median(covcnt)), "max", covcnt.max(), flush=True)
    free = np.where(deg < Delta)[0]
    print("free-degree vertices:", len(free), flush=True)

    rng = np.random.default_rng(12345)
    best_unc = n + 1
    deadline = time.time() + secs
    tries = 0
    while time.time() < deadline:
        tries += 1
        chosen = []
        cov = np.zeros(W, np.uint64)
        if len(free) == 0:
            break
        # seed: random free vertex weighted by coverage, then greedy
        cand = free.copy(); rng.shuffle(cand)
        chosen.append(int(cand[0]))
        cov |= B[cand[0]]
        while len(chosen) < Delta:
            unc = n - int(np.unpackbits(cov.view(np.uint8)).sum())
            if unc == 0:
                break
            gains = np.unpackbits((B[cand] & ~cov[None, :]).view(np.uint8), axis=-1).sum(1)
            i = int(np.argmax(gains))
            if gains[i] == 0:
                break
            chosen.append(int(cand[i]))
            cov |= B[cand[i]]
            # avoid reusing
            cand = np.delete(cand, i)
        unc = n - int(np.unpackbits(cov.view(np.uint8)).sum())
        if unc < best_unc:
            best_unc = unc
            print(f"try {tries}: chosen={len(chosen)} uncovered={unc}", flush=True)
            # local repair: swap worst chosen for random free, keep best
            improved = True
            while improved and unc > 0 and time.time() < deadline:
                improved = False
                for pos in range(len(chosen)):
                    base = chosen[:pos] + chosen[pos+1:]
                    cov2 = np.zeros(W, np.uint64)
                    for s in base:
                        cov2 |= B[s]
                    gains = np.unpackbits((B[free] & ~cov2[None, :]).view(np.uint8), axis=-1).sum(1)
                    j = int(np.argmax(gains))
                    if gains[j] == 0:
                        continue
                    cov3 = cov2 | B[free[j]]
                    u3 = n - int(np.unpackbits(cov3.view(np.uint8)).sum())
                    if u3 < unc:
                        chosen = base + [int(free[j])]
                        unc = u3; improved = True
                        print(f"  repaired pos {pos}: uncovered={unc}", flush=True)
                        break
            if unc == 0:
                n2 = n + 1
                E2 = list(map(tuple, E))
                for s in chosen:
                    E2.append((n, s))
                E2 = np.array(E2, dtype=np.int64)
                adj2, deg2 = edges_to_adj(n2, E2, Delta)
                c, _ = exact_cost(adj2, deg2, n2, D)
                print(f"COVER_OK chosen={sorted(chosen)} cost={c}", flush=True)
                if c == 0:
                    write_edges(f"candidate_{Delta}_{D}_n{n2}.edges", E2,
                                header=f"{Delta},{D} insertion of one vertex into {path}")
                    print("WROTE", f"candidate_{Delta}_{D}_n{n2}.edges", flush=True)
                    return
    print("no exact cover found; best uncovered", best_unc, "tries", tries, flush=True)

if __name__ == '__main__':
    main()
