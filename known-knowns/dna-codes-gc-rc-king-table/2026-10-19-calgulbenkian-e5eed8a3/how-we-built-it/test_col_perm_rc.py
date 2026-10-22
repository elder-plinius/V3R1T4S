#!/usr/bin/env python3
"""
Test Column-Permutation RC-Extraction on:
1. GC(16, 12, 8) = 60  (King=24^c, Lit=26, UB_RC=30)
2. GC(15, 12, 7) = 15  (King=6^m, UB_RC=7)
3. GC(20, 16, 10) = 16 (King=7^v, Lit=7, UB_RC=8)
4. Shortened/punctured codes from GC(16, 12, 8) and GC(20, 16, 10):
   - GC,RC(19, 15, 9) (King=8^v, Lit=8, UB_RC=9)
   - GC,RC(18, 14, 9) (King=10^v, Lit=10, UB_RC=14)
   - GC,RC(17, 13, 8) (King=12^v, Lit=12)
   - GC,RC(14, 11, 7) (King=8^v, Lit=8, UB_RC=10)
"""
import random

RC_MAP = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
COMP_INT = [1, 0, 3, 2] # A=0, T=1, C=2, G=3 -> A<->T, C<->G
CHAR_TO_INT = {'A': 0, 'T': 1, 'C': 2, 'G': 3}
INT_TO_CHAR = 'ATCG'

def load_code(path):
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]

def find_rc_subcode(words, d, trials=3000):
    n = len(words[0])
    M = len(words)
    # Convert to int arrays
    W = [[CHAR_TO_INT[c] for c in w] for w in words]
    best_clq = []

    perm = list(range(n))
    for t in range(trials):
        random.shuffle(perm)
        # Under column permutation perm, word i at pos k is W[i][perm[k]],
        # and its RC at pos k is COMP_INT[W[i][perm[n - 1 - k]]].
        # So dist(perm(x), perm(y)^{RC}) = sum_{k=0}^{n-1} (W[x][perm[k]] != COMP_INT[W[y][perm[n-1-k]]])
        # Notice this only depends on the map rev_perm[p] = perm[n - 1 - perm^{-1}(p)]!
        rev_map = [0] * n
        for k in range(n):
            rev_map[perm[k]] = perm[n - 1 - k]

        # Filter words with self-RC distance >= d
        valid = []
        for i in range(M):
            wi = W[i]
            sd = sum(wi[p] != COMP_INT[wi[rev_map[p]]] for p in range(n))
            if sd >= d:
                valid.append(i)

        if len(valid) <= len(best_clq):
            continue

        # Build adjacency among `valid`: since all pairs in W already have dist(x, y) >= d,
        # two words i, j in `valid` are compatible iff dist(perm(i), perm(j)^{RC}) >= d!
        V = len(valid)
        adj = [0] * V
        for a in range(V):
            wa = W[valid[a]]
            for b in range(a + 1, V):
                wb = W[valid[b]]
                rc_d = sum(wa[p] != COMP_INT[wb[rev_map[p]]] for p in range(n))
                if rc_d >= d:
                    adj[a] |= (1 << b)
                    adj[b] |= (1 << a)

        # Fast bitmask max-clique on V <= 60 vertices
        cur_best = []
        def expand(cand_mask, chosen):
            nonlocal cur_best
            if len(chosen) > len(cur_best):
                cur_best = list(chosen)
            if len(chosen) + bin(cand_mask).count('1') <= len(cur_best):
                return
            m = cand_mask
            while m:
                lsb = m & -m
                v = lsb.bit_length() - 1
                if len(chosen) + bin(m).count('1') <= len(cur_best):
                    break
                chosen.append(v)
                expand(m & adj[v], chosen)
                chosen.pop()
                m ^= lsb

        expand((1 << V) - 1, [])
        if len(cur_best) > len(best_clq):
            best_clq = [''.join(INT_TO_CHAR[W[valid[v]][perm[k]]] for k in range(n)) for v in cur_best]
            print(f"[Trial {t}] New best RC subcode (n={n}, d={d}): size = {len(best_clq)}")

    return best_clq

c60 = load_code("results/gc_16_12_8_60.txt")
c15 = load_code("results/gc_15_12_7_15.txt")
c20 = load_code("results/gc_20_16_10_16.txt")

print("--- Testing GC(20, 16, 10) = 16 -> GC,RC(20, 16, 10) ---")
rc20 = find_rc_subcode(c20, 16, trials=2000)

print("--- Testing punctured GC(19, 15, 9) from GC(20, 16, 10) ---")
# Puncture a coordinate where all words have CG? No, in c20, some have CG and some have AT!
# Wait: if we replace any 'C' or 'G' at coordinate 0 of c20 with 'A' or 'T' and delete coordinate 0?
# Wait: if we delete coordinate 0 from c20, words with A/T at coord 0 still have GC-weight 10 (which is 19 - 9 = 10, so complementing A<->C, T<->G gives GC-weight 9!),
# while words with C/G at coord 0 already have GC-weight 9!

print("--- Testing GC(15, 12, 7) = 15 -> GC,RC(15, 12, 7) ---")
rc15 = find_rc_subcode(c15, 12, trials=2000)

print("--- Testing GC(16, 12, 8) = 60 -> GC,RC(16, 12, 8) ---")
rc16 = find_rc_subcode(c60, 12, trials=2000)
