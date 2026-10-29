"""Build the explicit abstract chain H_K from a block (vertices 0..n0-1, anchors 0 and n0-1 glued onto the
previous copy's out-pair (p,q), p<q). Global vertex labels follow a merged order in which every copy keeps its own
order: copy c+1's inner vertices are placed right after copy c's vertex p. alpha(H_K) by exact max-plus DP over
the copies (states of the 2 shared vertices). Writes out/chain_K<k>.json with n, edges (global labels), alpha_dp."""
import sys, json, itertools

def build(block, n0, p, q, K):
    # returns order list of (copy, local) and edges as tuples of (copy, local) keys
    def key(c, v):
        # canonical key: anchors of copy c>0 are copy c-1's p, q
        while c > 0 and v in (0, n0 - 1):
            v = p if v == 0 else q; c -= 1
        return (c, v)
    def seq(c):
        out = []
        for v in range(n0):
            if c > 0 and v in (0, n0 - 1):
                continue
            out.append((c, v))
            if v == p and c < K:
                out.extend(seq(c + 1))
        return out
    order = seq(0)
    lab = {k: i for i, k in enumerate(order)}
    edges = []
    for c in range(K + 1):
        for e in block:
            edges.append(tuple(sorted(lab[key(c, v)] for v in e)))
    return len(order), edges, lab, key

def alpha_dp(block, n0, p, q, K):
    em = [sum(1 << v for v in e) for e in block]
    ind = [I for I in range(1 << n0) if all(I & e != e for e in em)]
    # V[t] = best count of copies c+1..K given state t of (p,q) of copy c (those two counted in copy c)
    NEG = -10**9
    V = [0, 0, 0, 0]
    for c in range(K, -1, -1):
        NV = [NEG] * 4
        best_root = NEG
        for I in ind:
            s = 2 * (I & 1) + ((I >> (n0 - 1)) & 1); t = 2 * ((I >> p) & 1) + ((I >> q) & 1)
            inner = bin(I).count("1") - (I & 1) - ((I >> (n0 - 1)) & 1)
            val = inner + (V[t] if c < K else 0)
            if val > NV[s]: NV[s] = val
            if c == 0:
                tot = val + (I & 1) + ((I >> (n0 - 1)) & 1)
                best_root = max(best_root, tot)
        V = NV
    return best_root

if __name__ == "__main__":
    block = [tuple(e) for e in json.loads(sys.argv[1])]; n0, p, q, Kmax = map(int, sys.argv[2:6])
    from fractions import Fraction as F
    for K in range(0, Kmax + 1):
        n, edges, lab, key = build(block, n0, p, q, K)
        a = alpha_dp(block, n0, p, q, K)
        r = F(a, n)
        print("K", K, "n", n, "m", len(edges), "alpha_dp", a, "ratio", r, "%.6f" % float(r), "below 5/9" if r < F(5, 9) else "")
        json.dump({"n": n, "edges": edges, "alpha_dp": a, "K": K, "block": block, "n0": n0, "p": p, "q": q},
                  open("out/chain_K%d.json" % K, "w"))
