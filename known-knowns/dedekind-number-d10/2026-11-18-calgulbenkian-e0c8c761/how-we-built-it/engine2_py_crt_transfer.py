#!/usr/bin/env python3
"""
engine2_py_crt_transfer.py

Independent Implementation 2 for dedekind-number-d10 (partial win p1):
  - Language & Arithmetic: Pure Python 3 standard library. All DP state accumulations run
    strictly in finite-field modular arithmetic F_{p_1} x F_{p_2} x F_{p_3} across three
    31-bit primes (p_1 = 1000000007, p_2 = 1000000009, p_3 = 998244353, product ~ 9.98e26)
    and reconstruct exact integers at the end via Garner / Chinese Remainder Theorem.
  - Burnside Reduction: Orbit-type Table of Marks linear system over P_81-conjugacy classes
    of order >= 9 (zero subgroup-poset Mobius function mu(H, K)), grouped into the 9
    S_9-conjugacy classes of order >= 9.
  - Poset Decomposition (zero shared code or formulas with Engine 1):
    1. Reproduces exact D(0..7) via connected-component memoized antichain branching on B^n
       and Birkhoff Poset Zeta sweeps in F_{p_i}.
    2. Evaluates |Fix_{D_9}(K)| and |Fix_{D_10}(K)| using:
       - 4-Slice Markov Chain Transfer Matrix along block weight r in {0,1,2,3} for Class 2 (Q_80),
       - Cartesian P_4-Chain Zeta Transfer in F_{p_i} for Classes 0, 1, 5, and
       - Single-sweep Birkhoff Poset Zeta Transform on D(B^9/K) in F_{p_i} for Classes 3, 4, 6, 7, 8.
"""

import sys
import time
from array import array
from collections import deque

PRIMES = (1000000007, 1000000009, 998244353)


def crt_reconstruct(residues, primes=PRIMES):
    """Reconstruct unique integer 0 <= X < prod(primes) from X == r_i (mod p_i)."""
    M = 1
    for p in primes:
        M *= p
    total = 0
    for r, p in zip(residues, primes):
        Mi = M // p
        inv = pow(Mi % p, p - 2, p)
        total = (total + r * Mi * inv) % M
    return total


# ---------- Part 1: Small Dedekind Numbers D(0..7) via Modular Zeta Transform ----------

def dedekind_small_crt(n):
    if n == 0:
        return 2
    if n <= 6:
        # Build Boolean cube B^{n-1} (size <= 32), enumerate downsets D_{n-1}, count comparable pairs via 1 Zeta sweep mod p_i!
        k = n - 1
        sz = 1 << k
        # Topological order on B^k is 0 .. 2^k - 1 directly!
        pred = [0] * sz
        for x in range(sz):
            pm = 0
            for b in range(k):
                if (x >> b) & 1:
                    pm |= 1 << (x ^ (1 << b))
            pred[x] = pm
        D = []
        def gen(idx, mask):
            if idx == sz:
                D.append(mask)
                return
            gen(idx + 1, mask)
            if (mask & pred[idx]) == pred[idx]:
                gen(idx + 1, mask | (1 << idx))
        gen(0, 0)
        if n == 1:
            return 3
        # 1 Birkhoff Zeta sweep on D gives |D^{B^1}| = D(n)
        idx_map = {m: i for i, m in enumerate(D)}
        nD = len(D)
        res = []
        for p in PRIMES:
            dp = [1] * nD
            for bit_i in range(sz):
                bit = 1 << bit_i
                pk = pred[bit_i]
                for i in range(nD):
                    m = D[i]
                    if not (m & bit) and (m & pk) == pk:
                        j = idx_map[m | bit]
                        v = dp[j] + dp[i]
                        dp[j] = v - p if v >= p else v
            res.append(sum(dp) % p)
        return crt_reconstruct(res)
    if n == 7:
        # D(7) = |D_5^{B^2}| via 4-element diamond transfer on D_5 (7581 elements) mod p_i,
        # or 1 Zeta sweep on D_6? Even simpler: D_5 has 7581 elements (32 bits);
        # 1 Zeta sweep on D_5 gives for each d in D_5 the interval vector? No:
        # Use Birkhoff Zeta on B^5 (32 bits) -> D_5 (7581), then D_6 = {(a <= b) in D_5} (7,828,354 pairs)?
        # Faster: in D_5 (7581 elements), count 4-tuples (a <= b, c <= d) = sum_{a <= d} |[a, d]|^2 mod p_i!
        pred = [0] * 16
        for x in range(16):
            for b in range(4):
                if (x >> b) & 1:
                    pred[x] |= 1 << (x ^ (1 << b))
        D4 = []
        def gen4(idx, mask):
            if idx == 16:
                D4.append(mask)
                return
            gen4(idx + 1, mask)
            if (mask & pred[idx]) == pred[idx]:
                gen4(idx + 1, mask | (1 << idx))
        gen4(0, 0)
        D5 = []
        for a in D4:
            for b in D4:
                if (a & b) == a:
                    D5.append((a << 16) | b)
        # Wait: D(7) via S_5-orbits on D_5 (210 orbits!) x D_5 in F_{p_i}!
        # Group D_5 (7581 masks on 32 bits) into S_5-orbits!
        perms5 = []
        import itertools
        for pi in itertools.permutations(range(5)):
            # map 0..31 -> 0..31
            mp = [0] * 32
            for x in range(32):
                y = 0
                for b in range(5):
                    if (x >> b) & 1:
                        y |= 1 << pi[b]
                mp[x] = y
            perms5.append(mp)
        idx5 = {m: i for i, m in enumerate(D5)}
        seen = [False] * len(D5)
        orbs5 = []
        for i, m in enumerate(D5):
            if not seen[i]:
                orb = set()
                for mp in perms5:
                    nm = 0
                    t = m
                    while t:
                        lb = t & -t
                        bit = lb.bit_length() - 1
                        nm |= 1 << mp[bit]
                        t ^= lb
                    j = idx5[nm]
                    seen[j] = True
                    orb.add(j)
                orbs5.append((i, len(orb)))
        # Compute down[i] and up[i] in D5 mod p_i via Birkhoff Zeta on B^5!
        pred5 = [0] * 32
        for x in range(32):
            for b in range(5):
                if (x >> b) & 1:
                    pred5[x] |= 1 << (x ^ (1 << b))
        res = []
        n5 = len(D5)
        dual_idx = [idx5[((~m) & 0xFFFFFFFF)] for m in [
            sum(((m >> (31 - x)) & 1) << x for x in range(32)) for m in D5
        ]]
        for p in PRIMES:
            dn = [1] * n5
            for bit_i in range(32):
                bit = 1 << bit_i
                pk = pred5[bit_i]
                for i in range(n5):
                    m = D5[i]
                    if not (m & bit) and (m & pk) == pk:
                        j = idx5[m | bit]
                        dn[j] = (dn[j] + dn[i]) % p
            up = [dn[dual_idx[i]] for i in range(n5)]
            tot = 0
            for rep_i, mult in orbs5:
                mx = D5[rep_i]
                row = 0
                for j in range(n5):
                    my = D5[j]
                    row = (row + dn[idx5[mx & my]] * up[idx5[mx | my]]) % p
                tot = (tot + mult * row) % p
            res.append(tot)
        return crt_reconstruct(res)
    raise ValueError(n)


# ---------- Part 2: P_81 Table of Marks Reduction (Zero Subgroup Mobius Function) ----------

def compose9(a, b):
    return tuple(a[b[i]] for i in range(9))


def inv9(a):
    r = [0] * 9
    for i, v in enumerate(a):
        r[v] = i
    return tuple(r)


def build_p81_and_marks():
    gens = [
        (1, 2, 0, 3, 4, 5, 6, 7, 8),
        (0, 1, 2, 4, 5, 3, 6, 7, 8),
        (0, 1, 2, 3, 4, 5, 7, 8, 6),
        (3, 4, 5, 6, 7, 8, 0, 1, 2),
    ]
    id9 = tuple(range(9))
    G = {id9}
    dq = deque([id9])
    while dq:
        u = dq.popleft()
        for g in gens:
            v = compose9(u, g)
            if v not in G:
                G.add(v)
                dq.append(v)
    G = sorted(G)
    g_idx = {g: i for i, g in enumerate(G)}
    mul = [[g_idx[compose9(G[i], G[j])] for j in range(81)] for i in range(81)]
    inv = [next(j for j in range(81) if mul[i][j] == 0) for i in range(81)]

    def close(mask):
        mask |= 1
        while True:
            nxt = mask
            a = mask
            while a:
                la = a & -a
                ia = la.bit_length() - 1
                b = mask
                while b:
                    lb = b & -b
                    ib = lb.bit_length() - 1
                    nxt |= 1 << mul[ia][ib]
                    b ^= lb
                a ^= la
            if nxt == mask:
                return mask
            mask = nxt

    subs = {1}
    dq = deque([1])
    while dq:
        hm = dq.popleft()
        for g in range(81):
            if not ((hm >> g) & 1):
                km = close(hm | (1 << g))
                if km not in subs:
                    subs.add(km)
                    dq.append(km)
    subs = sorted(subs, key=lambda m: (bin(m).count("1"), m))

    # Group subgroups into P_81-conjugacy classes!
    p81_classes = []
    visited = set()
    for m in subs:
        if m in visited:
            continue
        cls = set()
        for g in range(81):
            gi = inv[g]
            cm = 0
            t = m
            while t:
                lb = t & -t
                k = lb.bit_length() - 1
                cm |= 1 << mul[gi][mul[k][g]]
                t ^= lb
            cls.add(cm)
        visited |= cls
        p81_classes.append(sorted(cls))

    # Keep P_81-conjugacy classes of subgroup order >= min_order and solve exact integer
    # Table-of-Marks upper-triangular system:
    #   For each P_81-class C_a (rep H_a, |H_a| >= min_order):
    #     sum_{b} w_b * |Fix_{P_81 / H_a}(H_b)| == [P_81 : H_a]
    def solve_marks_weights(min_order):
        elig = [c for c in p81_classes if bin(c[0]).count("1") >= min_order]
        m_cls = len(elig)
        # M[a][b] = |Fix_{G / H_a}(H_b)| for reps H_a = elig[a][0], H_b = elig[b][0]
        M = [[0] * m_cls for _ in range(m_cls)]
        rhs = [81 // bin(elig[a][0]).count("1") for a in range(m_cls)]
        for a in range(m_cls):
            Ha = elig[a][0]
            ord_a = bin(Ha).count("1")
            for b in range(m_cls):
                Hb = elig[b][0]
                cnt_g = 0
                for g in range(81):
                    gi = inv[g]
                    # check g^{-1} Hb g <= Ha
                    ok = True
                    t = Hb
                    while t:
                        lb = t & -t
                        k = lb.bit_length() - 1
                        if not ((Ha >> mul[gi][mul[k][g]]) & 1):
                            ok = False
                            break
                        t ^= lb
                    if ok:
                        cnt_g += 1
                M[a][b] = cnt_g // ord_a
        # Forward-substitution on lower-triangular Table of Marks (M[a][b] == 0 for b > a)!
        w = [0] * m_cls
        for a in range(m_cls):
            assert all(M[a][b] == 0 for b in range(a + 1, m_cls))
            rem = rhs[a] - sum(M[a][b] * w[b] for b in range(a))
            assert rem % M[a][a] == 0, f"Non-integer mark weight at {a}: {rem} / {M[a][a]}"
            w[a] = rem // M[a][a]
        # Verify identity modulo (81 // (min_order // 3)) across ALL 50 subgroups H0 of P_81!
        modulus = (81 * 3) // min_order
        for H0 in subs:
            ord0 = bin(H0).count("1")
            lhs = 0
            for b in range(m_cls):
                Hb = elig[b][0]
                cnt_g = 0
                for g in range(81):
                    gi = inv[g]
                    ok = True
                    t = Hb
                    while t:
                        lb = t & -t
                        k = lb.bit_length() - 1
                        if not ((H0 >> mul[gi][mul[k][g]]) & 1):
                            ok = False
                            break
                        t ^= lb
                    if ok:
                        cnt_g += 1
                lhs += w[b] * (cnt_g // ord0)
            assert (lhs - (81 // ord0)) % modulus == 0
        return elig, w

    elig81, w81 = solve_marks_weights(81)
    elig27, w27 = solve_marks_weights(27)
    elig9, w9 = solve_marks_weights(9)

    # Now group elig9 into S_9-conjugacy classes with explicit S_9 permutation witnesses!
    def find_s9_conj(K1_mask, K2_mask):
        if bin(K1_mask).count("1") != bin(K2_mask).count("1"):
            return None
        K1 = [G[i] for i in range(81) if (K1_mask >> i) & 1]
        K2_set = {G[i] for i in range(81) if (K2_mask >> i) & 1}
        # Orbit sizes on 0..8
        def orbs_on_9(K):
            vis = [False] * 9
            res = []
            for i in range(9):
                if not vis[i]:
                    o = sorted({g[i] for g in K})
                    for x in o:
                        vis[x] = True
                    res.append(o)
            res.sort(key=lambda x: (len(x), x))
            return res
        o1 = orbs_on_9(K1)
        o2 = orbs_on_9(list(K2_set))
        if [len(x) for x in o1] != [len(x) for x in o2]:
            return None
        # Check |B^9 / K| match quickly
        def q9_size(K):
            seen = [False] * 512
            c = 0
            for x in range(512):
                if not seen[x]:
                    c += 1
                    for g in K:
                        y = 0
                        for b in range(9):
                            if (x >> b) & 1:
                                y |= 1 << g[b]
                        seen[y] = True
            return c
        if q9_size(K1) != q9_size(list(K2_set)):
            return None
        cands = [[u for o in o2 if len(o) == next(len( z) for z in o1 if i in z) for u in o] for i in range(9)]
        pmap = [-1] * 9
        used = [False] * 9
        def bt(idx):
            if idx == 9:
                pi = tuple(pmap)
                pi_inv = inv9(pi)
                if all(compose9(pi, compose9(g, pi_inv)) in K2_set for g in K1):
                    return pi
                return None
            for y in cands[idx]:
                if not used[y]:
                    pmap[idx] = y
                    used[y] = True
                    r = bt(idx + 1)
                    if r is not None:
                        return r
                    used[y] = False
            return None
        return bt(0)

    s9_classes = []  # list of dicts: rep_mask, w_m3, w_m9, w_m27, p81_count, sub_count
    map_w3 = {elig81[i][0]: w81[i] for i in range(len(elig81))}
    map_w9 = {elig27[i][0]: w27[i] for i in range(len(elig27))}
    map_w27 = {elig9[i][0]: w9[i] for i in range(len(elig9))}

    for p_cls in elig9:
        rep = p_cls[0]
        placed = False
        for sc in s9_classes:
            if find_s9_conj(sc["rep_mask"], rep) is not None:
                sc["w_m3"] += map_w3.get(rep, 0)
                sc["w_m9"] += map_w9.get(rep, 0)
                sc["w_m27"] += map_w27.get(rep, 0)
                sc["sub_count"] += len(p_cls)
                placed = True
                break
        if not placed:
            s9_classes.append({
                "rep_mask": rep,
                "order": bin(rep).count("1"),
                "w_m3": map_w3.get(rep, 0),
                "w_m9": map_w9.get(rep, 0),
                "w_m27": map_w27.get(rep, 0),
                "sub_count": len(p_cls),
            })
    return G, s9_classes


# ---------- Part 3: Modular Finite-Field Poset Evaluators (F_{p_1} x F_{p_2} x F_{p_3}) ----------

def enumerate_downsets(m, pred):
    out = []
    def rec(i, mask):
        if i == m:
            out.append(mask)
            return
        rec(i + 1, mask)
        if (mask & pred[i]) == pred[i]:
            rec(i + 1, mask | (1 << i))
    rec(0, 0)
    return out


def eval_via_single_zeta_mod(m, pred):
    """For |Q| <= 64: enumerate D(Q), run 1 Birkhoff Zeta sweep in F_{p_i} for |P_3^Q|."""
    D = enumerate_downsets(m, pred)
    nD = len(D)
    d9_res = [nD % p for p in PRIMES]
    idx_map = {mask: i for i, mask in enumerate(D)}

    p1, p2, p3 = PRIMES
    dp1 = array("I", [1]) * nD
    dp2 = array("I", [1]) * nD
    dp3 = array("I", [1]) * nD

    for k in range(m):
        bit = 1 << k
        pk = pred[k]
        for i in range(nD):
            mk = D[i]
            if not (mk & bit) and (mk & pk) == pk:
                j = idx_map[mk | bit]
                v1 = dp1[j] + dp1[i]
                dp1[j] = v1 - p1 if v1 >= p1 else v1
                v2 = dp2[j] + dp2[i]
                dp2[j] = v2 - p2 if v2 >= p2 else v2
                v3 = dp3[j] + dp3[i]
                dp3[j] = v3 - p3 if v3 >= p3 else v3

    d10_res = [sum(dp1) % p1, sum(dp2) % p2, sum(dp3) % p3]
    return crt_reconstruct(d9_res), crt_reconstruct(d10_res)


def eval_via_p4_chain_zeta_mod(q_sz, pred_sub, dual_perm_bits):
    """
    Evaluate |U^{P_4}| in F_{p_i} where U = D(Q_sub) is self-dual via bit-reversal+complement!
    Uses 2 Birkhoff Zeta sweeps in F_{p_i} with duality u -> u^dual:
      dn[u] = |{u0 <= u}|   (1st Zeta sweep)
      up[u] = dn[u^dual]    (by poset self-duality!)
      s2[u2] = sum_{u1 <= u2} dn[u1]  (2nd Zeta sweep)
      |U^{P_4}| = sum_{u2 in U} s2[u2] * up[u2] (mod p_i).
    """
    U = enumerate_downsets(q_sz, pred_sub)
    nU = len(U)
    idx_map = {mask: i for i, mask in enumerate(U)}
    full_mask = (1 << q_sz) - 1

    # Compute dual index for each downset m in U: complement of m mapped by dual_perm_bits
    dual_idx = array("I", [0]) * nU
    for i, m in enumerate(U):
        comp = (~m) & full_mask
        dm = 0
        t = comp
        while t:
            lb = t & -t
            b = lb.bit_length() - 1
            dm |= 1 << dual_perm_bits[b]
            t ^= lb
        dual_idx[i] = idx_map[dm]

    p1, p2, p3 = PRIMES
    dn1 = array("I", [1]) * nU
    dn2 = array("I", [1]) * nU
    dn3 = array("I", [1]) * nU

    # Pre-build transition pairs (src, dst) per bit? Wait: 2 sweeps -> direct loop in Python
    # Even faster in Python: build flat edge arrays once? Wait: 12M edges = 96MB, or direct loop!
    # Direct loop with local bindings:
    U_list = U
    get_idx = idx_map.__getitem__
    for sw in range(2):
        if sw == 1:
            # Save up_i[u] = dn_i[dual_idx[u]] BEFORE 2nd sweep overwrites dn_i -> s2_i!
            up1 = array("I", (dn1[dual_idx[i]] for i in range(nU)))
            up2 = array("I", (dn2[dual_idx[i]] for i in range(nU)))
            up3 = array("I", (dn3[dual_idx[i]] for i in range(nU)))
        for k in range(q_sz):
            bit = 1 << k
            pk = pred_sub[k]
            for i in range(nU):
                mk = U_list[i]
                if not (mk & bit) and (mk & pk) == pk:
                    j = get_idx(mk | bit)
                    v1 = dn1[j] + dn1[i]
                    dn1[j] = v1 - p1 if v1 >= p1 else v1
                    v2 = dn2[j] + dn2[i]
                    dn2[j] = v2 - p2 if v2 >= p2 else v2
                    v3 = dn3[j] + dn3[i]
                    dn3[j] = v3 - p3 if v3 >= p3 else v3

    tot1 = 0
    tot2 = 0
    tot3 = 0
    for i in range(nU):
        tot1 = (tot1 + dn1[i] * up1[i]) % p1
        tot2 = (tot2 + dn2[i] * up2[i]) % p2
        tot3 = (tot3 + dn3[i] * up3[i]) % p3
    return crt_reconstruct((tot1, tot2, tot3))


def eval_4slice_markov_mod(G, K_mask, blk):
    """
    Evaluate |B^Q| and |P_3^Q| for Q = B^9 / K via 4-Slice Markov Chain Transfer S_0 -> S_1 -> S_2 -> S_3
    along the K-invariant 3-variable block weight r = wt(block `blk`) in {0, 1, 2, 3}, strictly in F_{p_i}!
    """
    K = [G[i] for i in range(81) if (K_mask >> i) & 1]
    orb_id = [-1] * 512
    orb_rep = []
    for x in range(512):
        if orb_id[x] == -1:
            oid = len(orb_rep)
            orb_rep.append(x)
            for g in K:
                y = 0
                for b in range(9):
                    if (x >> b) & 1:
                        y |= 1 << g[b]
                orb_id[y] = oid
    m = len(orb_rep)
    le = [[False] * m for _ in range(m)]
    for a in range(m):
        xa = orb_rep[a]
        for y in range(512):
            if (xa & y) == xa:
                le[a][orb_id[y]] = True

    mask3 = 7 << (3 * blk)
    slices = [[] for _ in range(4)]
    for r_tot in range(10):
        for i in range(m):
            if bin(orb_rep[i]).count("1") == r_tot:
                w = bin(orb_rep[i] & mask3).count("1")
                slices[w].append(i)

    # Enumerate downsets D_r of each slice S_r (sizes <= 24, |D_r| <= 562!)
    D_slices = []
    idx_slices = []
    pred_slices = []
    for r in range(4):
        S = slices[r]
        k = len(S)
        pr = [0] * k
        for j in range(k):
            for i in range(j):
                if le[S[i]][S[j]]:
                    pr[j] |= 1 << i
        Dr = enumerate_downsets(k, pr)
        D_slices.append(Dr)
        idx_slices.append({mk: idx for idx, mk in enumerate(Dr)})
        pred_slices.append(pr)

    # Cross-slice requirements from S_r to S_{r+1}: for each downset B' in D_{r+1}, req_r(B') in D_r!
    req_idx = []
    for r in range(3):
        S_prev = slices[r]
        S_next = slices[r + 1]
        cross = [0] * len(S_next)
        for j, u_next in enumerate(S_next):
            cm = 0
            for i, u_prev in enumerate(S_prev):
                if le[u_prev][u_next]:
                    cm |= 1 << i
            cross[j] = cm
        r_map = []
        for mk in D_slices[r + 1]:
            rq = 0
            t = mk
            while t:
                lb = t & -t
                b = lb.bit_length() - 1
                rq |= cross[b]
                t ^= lb
            r_map.append(idx_slices[r][rq])
        req_idx.append(r_map)

    # 1. Compute |B^Q| (D_9) by 4-slice transfer in F_{p_i}
    d9_mods = []
    d10_mods = []
    for p in PRIMES:
        # D_9 1D slice transfer
        vec = [1] * len(D_slices[0])
        for r in range(3):
            # Upward Birkhoff Zeta on D_r: sup[a0] = sum_{a >= a0} vec[a] (reverse bit order k = |S_r|-1..0?
            # Wait: superset Zeta! A subseteq B <==> (~B) subseteq (~A), OR iterate k = 0..|S_r|-1:
            # In topological order k=0..|S_r|-1, flipping bit k from 1 -> 0? Careful!
            # Let's check superset Zeta on D(S_r)! If A subseteq B are downsets of S_r, then for k = |S_r|-1 down to 0:
            # T_k = (A cap {0..k-1}) cup (B cap {k..m-1}) IS A DOWNSET OF S_r by the exact same proof!
            # At step k = |S_r|-1 down to 0: T_{k+1} has bit k from A (0), T_k has bit k from B (1),
            # so we add FROM T_k (which has bit k == 1, and T_k \ {k} in D_r) TO T_{k+1} = T_k ^ (1<<k)!!
            k_sz = len(slices[r])
            Dr = D_slices[r]
            imap = idx_slices[r]
            sup = vec[:]
            # Precompute successors mask in S_r so (mk ^ bit) is in Dr iff (mk & succ[k]) == 0!
            succ = [0] * k_sz
            for i in range(k_sz):
                for j in range(i + 1, k_sz):
                    if (pred_slices[r][j] >> i) & 1:
                        succ[i] |= 1 << j
            for k in range(k_sz - 1, -1, -1):
                bit = 1 << k
                sk = succ[k]
                for idx_d, mk in enumerate(Dr):
                    if (mk & bit) and (mk & sk) == 0:
                        dst = imap[mk ^ bit]
                        sup[dst] = (sup[dst] + sup[idx_d]) % p
            rmap = req_idx[r]
            vec = [sup[rmap[j]] for j in range(len(D_slices[r + 1]))]
        d9_mods.append(sum(vec) % p)

        # D_10 2D slice transfer on P_3^{S_r} = {(a, b) in D_r x D_r : a subseteq b}
        n0 = len(D_slices[0])
        Dr0 = D_slices[0]
        mat = [[1 if (Dr0[a] & Dr0[b]) == Dr0[a] else 0 for b in range(n0)] for a in range(n0)]
        for r in range(3):
            k_sz = len(slices[r])
            Dr = D_slices[r]
            nr = len(Dr)
            imap = idx_slices[r]
            succ = [0] * k_sz
            for i in range(k_sz):
                for j in range(i + 1, k_sz):
                    if (pred_slices[r][j] >> i) & 1:
                        succ[i] |= 1 << j
            # Step A: superset Zeta along row index `a`
            for k in range(k_sz - 1, -1, -1):
                bit = 1 << k
                sk = succ[k]
                for a, mk in enumerate(Dr):
                    if (mk & bit) and (mk & sk) == 0:
                        dst = imap[mk ^ bit]
                        row_src = mat[a]
                        row_dst = mat[dst]
                        for b in range(nr):
                            v = row_dst[b] + row_src[b]
                            row_dst[b] = v - p if v >= p else v
            # Step B: superset Zeta along col index `b`
            edges_b = []
            for k in range(k_sz - 1, -1, -1):
                bit = 1 << k
                sk = succ[k]
                step_pairs = []
                for b, mk in enumerate(Dr):
                    if (mk & bit) and (mk & sk) == 0:
                        step_pairs.append((b, imap[mk ^ bit]))
                edges_b.append(step_pairs)
            for step_pairs in edges_b:
                for row in mat:
                    for b_src, b_dst in step_pairs:
                        v = row[b_dst] + row[b_src]
                        row[b_dst] = v - p if v >= p else v
            # Step C: pull back to S_{r+1}
            Dr_next = D_slices[r + 1]
            n_next = len(Dr_next)
            rmap = req_idx[r]
            new_mat = [[0] * n_next for _ in range(n_next)]
            for a2 in range(n_next):
                ma2 = Dr_next[a2]
                src_row = mat[rmap[a2]]
                dst_row = new_mat[a2]
                for b2 in range(a2, n_next):
                    if (ma2 & Dr_next[b2]) == ma2:
                        dst_row[b2] = src_row[rmap[b2]]
            mat = new_mat
        d10_mods.append(sum(sum(row) for row in mat) % p)

    return crt_reconstruct(d9_mods), crt_reconstruct(d10_mods)


def eval_class_rep(G, K_mask):
    K = [G[i] for i in range(81) if (K_mask >> i) & 1]
    fixed_vars = [v for v in range(9) if all(g[v] == v for g in K)]

    # Case 1: Class 0 (3 fixed vars in 0..8 -> C_3 x C_3 on two 3-blocks):
    # Factor one P_4 chain -> U_9 = D(P_4 x B^3) (32 els), U_10 = D(P_4 x B^4) (64 els), evaluate |U^{P_4}| mod p_i!
    if len(fixed_vars) == 3:
        outs = []
        for b_dim in (3, 4):
            pts = []
            for tot in range(4 + b_dim):
                for pv in range(4):
                    for bv in range(1 << b_dim):
                        if pv + bin(bv).count("1") == tot:
                            pts.append((pv, bv))
            q_sz = len(pts)
            pred_sub = [0] * q_sz
            for u in range(q_sz):
                for v in range(u):
                    if pts[v][0] <= pts[u][0] and (pts[v][1] & pts[u][1]) == pts[v][1]:
                        pred_sub[u] |= 1 << v
            pt_idx = {pt: i for i, pt in enumerate(pts)}
            mask_b = (1 << b_dim) - 1
            dual_perm = [pt_idx[(3 - pv, (~bv) & mask_b)] for (pv, bv) in pts]
            outs.append(eval_via_p4_chain_zeta_mod(q_sz, pred_sub, dual_perm))
        return outs[0], outs[1]

    # Build Q = B^9 / K
    orb_id = [-1] * 512
    orb_rep = []
    for x in range(512):
        if orb_id[x] == -1:
            oid = len(orb_rep)
            orb_rep.append(x)
            for g in K:
                y = 0
                for b in range(9):
                    if (x >> b) & 1:
                        y |= 1 << g[b]
                orb_id[y] = oid
    m = len(orb_rep)

    # Case 2: |Q| <= 64 (Classes 3, 4, 5, 6, 7, 8 -> m in {24, 28, 32, 60, 64})
    # Evaluate directly via 1 Birkhoff Zeta sweep on D(Q) in F_{p_i}!
    if m <= 64:
        ord_q = sorted(range(m), key=lambda i: (bin(orb_rep[i]).count("1"), orb_rep[i]))
        inv_q = {orig: new for new, orig in enumerate(ord_q)}
        pred = [0] * m
        for new_a, orig_a in enumerate(ord_q):
            xa = orb_rep[orig_a]
            for y in range(512):
                if (xa & y) == xa:
                    new_b = inv_q[orb_id[y]]
                    if new_a < new_b:
                        pred[new_b] |= 1 << new_a
        return eval_via_single_zeta_mod(m, pred)

    # Case 3: m == 96 (Class 1 -> K = <3-cycle on blk_c, diagonal 3-cycle on other 6 vars>, Q = Q_24 x P_4!)
    if m == 96:
        # Find the independent 3-cycle block blk_c where K contains the pure 3-cycle on blk_c!
        blk_c = None
        for blk in range(3):
            # check if K restricted to outside blk fixes all other 6 vars for some non-id element of K
            other_vars = [v for v in range(9) if v // 3 != blk]
            if any(any(g[v] != v for v in range(3 * blk, 3 * blk + 3)) and all(g[v] == v for v in other_vars) for g in K):
                blk_c = blk
                break
        assert blk_c is not None
        act6 = [v for v in range(9) if v // 3 != blk_c]
        # Build Q_24 on B^6 / K
        oid6 = [-1] * 64
        rep6 = []
        for x in range(64):
            if oid6[x] == -1:
                oid = len(rep6)
                rep6.append(x)
                for g in K:
                    y = 0
                    for t_i, v in enumerate(act6):
                        if (x >> t_i) & 1:
                            img_v = g[v]
                            y |= 1 << act6.index(img_v)
                    oid6[y] = oid
        assert len(rep6) == 24
        # Sort Q_24 by rank
        ord24 = sorted(range(24), key=lambda i: (bin(rep6[i]).count("1"), rep6[i]))
        rep24 = [rep6[i] for i in ord24]
        inv24 = {orig: new for new, orig in enumerate(ord24)}
        le24 = [[False] * 24 for _ in range(24)]
        for a in range(24):
            xa = rep24[a]
            for y in range(64):
                if (xa & y) == xa:
                    le24[a][inv24[oid6[y]]] = True
        # Self-dual map on Q_24: complement in B^6!
        dual24 = [inv24[oid6[(~rep24[a]) & 63]] for a in range(24)]
        # For n=9: U = D(Q_24) (24 els), |U^{P_4}|; for n=10: U = D(Q_24 x B^1) (48 els), |U^{P_4}|!
        pred9 = [0] * 24
        for j in range(24):
            for i in range(j):
                if le24[i][j]:
                    pred9[j] |= 1 << i
        d9 = eval_via_p4_chain_zeta_mod(24, pred9, dual24)

        pts10 = []
        for tot in range(8):
            for i in range(24):
                for b in range(2):
                    if bin(rep24[i]).count("1") + b == tot:
                        pts10.append((i, b))
        pred10 = [0] * 48
        for u in range(48):
            for v in range(u):
                if le24[pts10[v][0]][pts10[u][0]] and pts10[v][1] <= pts10[u][1]:
                    pred10[u] |= 1 << v
        pt10_idx = {pt: idx for idx, pt in enumerate(pts10)}
        dual48 = [pt10_idx[(dual24[i], 1 - b)] for (i, b) in pts10]
        d10 = eval_via_p4_chain_zeta_mod(48, pred10, dual48)
        return d9, d10

    # Case 4: m == 80 (Class 2 -> 4-Slice Markov Chain Transfer along block 0!)
    assert m == 80
    return eval_4slice_markov_mod(G, K_mask, 0)


def main():
    t0 = time.time()
    exp_d = [2, 3, 6, 20, 168, 7581, 7828354, 2414682040998]
    got_d = [dedekind_small_crt(n) for n in range(8)]
    assert got_d == exp_d, f"D(0..7) mismatch: {got_d}"
    print(f"OK [Engine2]: Exact D(0..7) reproduced via modular CRT Zeta ({', '.join(map(str, got_d))})")

    G, s9_classes = build_p81_and_marks()
    print(f"OK [Engine2]: Table-of-Marks solved over Z on P_81; grouped into {len(s9_classes)} S_9-classes of order >= 9")

    tot9_m3 = tot9_m9 = tot9_m27 = 0
    tot10_m3 = tot10_m9 = tot10_m27 = 0

    for idx, sc in enumerate(s9_classes):
        ts = time.time()
        f9, f10 = eval_class_rep(G, sc["rep_mask"])
        dt = time.time() - ts
        sc["fix_d9"] = f9
        sc["fix_d10"] = f10
        print(
            f"  S9-Class {idx} (|K|={sc['order']:2d}, subs={sc['sub_count']:2d}, "
            f"w3={sc['w_m3']:2d}, w9={sc['w_m9']:2d}, w27={sc['w_m27']:3d}): "
            f"Fix_D9={f9}  Fix_D10={f10}  ({dt:.3f}s)"
        )
        tot9_m3 += sc["w_m3"] * f9
        tot9_m9 += sc["w_m9"] * f9
        tot9_m27 += sc["w_m27"] * f9

        tot10_m3 += sc["w_m3"] * f10
        tot10_m9 += sc["w_m9"] * f10
        tot10_m27 += sc["w_m27"] * f10

    print("\n=== ENGINE 2 SUMMARY ===")
    print(
        f"D(9):  raw_m3={tot9_m3}, raw_m9={tot9_m9}, raw_m27={tot9_m27}  =>  "
        f"mod 3 = {tot9_m3 % 3}, mod 9 = {tot9_m9 % 9}, mod 27 = {tot9_m27 % 27}"
    )
    print(
        f"D(10): raw_m3={tot10_m3}, raw_m9={tot10_m9}, raw_m27={tot10_m27}  =>  "
        f"mod 3 = {tot10_m3 % 3}, mod 9 = {tot10_m9 % 9}, mod 27 = {tot10_m27 % 27}"
    )
    print(f"Total Engine 2 elapsed: {time.time() - t0:.3f}s")

    assert (tot9_m3 % 3, tot9_m9 % 9, tot9_m27 % 27) == (0, 6, 24)
    assert tot10_m3 % 3 == 1


if __name__ == "__main__":
    main()
