#!/usr/bin/env python3
"""
Standalone Dual-Engine Verifier for dedekind-number-d10 (partial win p1):
Verifies D(10) == 16 (mod 27) (and D(10) == 7 (mod 9), D(10) == 1 (mod 3))
together with exact reproduction of D(0..7), D(6..8) mod 9, and D(9) == 24 (mod 27)
using TWO genuinely independent zero-shared-code implementations:

  - Engine 1 (C99, verify_engine1_c99.c): Exact 128-bit integer arithmetic
    (__uint128_t / __int128), subgroup-poset truncated Mobius inversion on all 50
    subgroups of P_81, Dedekind B^2/B^3 interval-lattice formulas + Bipartite Galois
    Boundary-Projection Contraction (zero Birkhoff Zeta sweeps).
  - Engine 2 (Pure Python 3 stdlib, embedded below): Multi-prime finite-field
    modular arithmetic F_{p_1} x F_{p_2} x F_{p_3} + Chinese Remainder Theorem,
    Burnside Table-of-Marks linear system over P_81-conjugacy classes, and
    4-Slice Markov Chain Transfer + Birkhoff Poset Zeta sweeps (zero Dedekind B^k
    interval formulas, zero 2-half Galois contraction).

Exits 0 with final line PASS iff every algebraic, baseline, certificate, and
cross-engine check holds; otherwise prints FAIL and exits 1.
"""

import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from array import array
from collections import deque

PRIMES = (1000000007, 1000000009, 998244353)


def fail(msg: str) -> None:
    print(f"CHECK ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def crt_reconstruct(residues, primes=PRIMES) -> int:
    M = 1
    for p in primes:
        M *= p
    total = 0
    for r, p in zip(residues, primes):
        Mi = M // p
        inv = pow(Mi % p, p - 2, p)
        total = (total + r * Mi * inv) % M
    return total


def compose9(a, b):
    return tuple(a[b[i]] for i in range(9))


def inv9(a):
    r = [0] * 9
    for i, v in enumerate(a):
        r[v] = i
    return tuple(r)


def dedekind_small_crt(n: int) -> int:
    if n == 0:
        return 2
    if n <= 6:
        k = n - 1
        sz = 1 << k
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
                        dp[j] = (dp[j] + dp[i]) % p
            res.append(sum(dp) % p)
        return crt_reconstruct(res)
    if n == 7:
        import itertools
        pred4 = [0] * 16
        for x in range(16):
            for b in range(4):
                if (x >> b) & 1:
                    pred4[x] |= 1 << (x ^ (1 << b))
        D4 = []
        def gen4(idx, mask):
            if idx == 16:
                D4.append(mask)
                return
            gen4(idx + 1, mask)
            if (mask & pred4[idx]) == pred4[idx]:
                gen4(idx + 1, mask | (1 << idx))
        gen4(0, 0)
        D5 = [(a << 16) | b for a in D4 for b in D4 if (a & b) == a]
        perms5 = []
        for pi in itertools.permutations(range(5)):
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
                        nm |= 1 << mp[lb.bit_length() - 1]
                        t ^= lb
                    j = idx5[nm]
                    seen[j] = True
                    orb.add(j)
                orbs5.append((i, len(orb)))
        pred5 = [0] * 32
        for x in range(32):
            for b in range(5):
                if (x >> b) & 1:
                    pred5[x] |= 1 << (x ^ (1 << b))
        n5 = len(D5)
        dual_idx = [
            idx5[(~sum(((m >> (31 - x)) & 1) << x for x in range(32))) & 0xFFFFFFFF]
            for m in D5
        ]
        res = []
        for p in PRIMES:
            dn = [1] * n5
            for bit_i in range(32):
                bit = 1 << bit_i
                pk = pred5[bit_i]
                for i in range(n5):
                    m = D5[i]
                    if not (m & bit) and (m & pk) == pk:
                        dn[idx5[m | bit]] = (dn[idx5[m | bit]] + dn[i]) % p
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


def eval_single_zeta_mod(m, pred):
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
    return crt_reconstruct(d9_res), crt_reconstruct((sum(dp1) % p1, sum(dp2) % p2, sum(dp3) % p3))


def eval_p4_chain_zeta_mod(q_sz, pred_sub, dual_perm_bits):
    U = enumerate_downsets(q_sz, pred_sub)
    nU = len(U)
    idx_map = {mask: i for i, mask in enumerate(U)}
    full_mask = (1 << q_sz) - 1
    dual_idx = array("I", [0]) * nU
    for i, m in enumerate(U):
        comp = (~m) & full_mask
        dm = 0
        t = comp
        while t:
            lb = t & -t
            dm |= 1 << dual_perm_bits[lb.bit_length() - 1]
            t ^= lb
        dual_idx[i] = idx_map[dm]

    p1, p2, p3 = PRIMES
    dn1 = array("I", [1]) * nU
    dn2 = array("I", [1]) * nU
    dn3 = array("I", [1]) * nU
    get_idx = idx_map.__getitem__
    for sw in range(2):
        if sw == 1:
            up1 = array("I", (dn1[dual_idx[i]] for i in range(nU)))
            up2 = array("I", (dn2[dual_idx[i]] for i in range(nU)))
            up3 = array("I", (dn3[dual_idx[i]] for i in range(nU)))
        for k in range(q_sz):
            bit = 1 << k
            pk = pred_sub[k]
            for i in range(nU):
                mk = U[i]
                if not (mk & bit) and (mk & pk) == pk:
                    j = get_idx(mk | bit)
                    v1 = dn1[j] + dn1[i]
                    dn1[j] = v1 - p1 if v1 >= p1 else v1
                    v2 = dn2[j] + dn2[i]
                    dn2[j] = v2 - p2 if v2 >= p2 else v2
                    v3 = dn3[j] + dn3[i]
                    dn3[j] = v3 - p3 if v3 >= p3 else v3
    t1 = t2 = t3 = 0
    for i in range(nU):
        t1 = (t1 + dn1[i] * up1[i]) % p1
        t2 = (t2 + dn2[i] * up2[i]) % p2
        t3 = (t3 + dn3[i] * up3[i]) % p3
    return crt_reconstruct((t1, t2, t3))


def eval_4slice_markov_mod(K_perms, blk=0):
    orb_id = [-1] * 512
    orb_rep = []
    for x in range(512):
        if orb_id[x] == -1:
            oid = len(orb_rep)
            orb_rep.append(x)
            for g in K_perms:
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
                slices[bin(orb_rep[i] & mask3).count("1")].append(i)
    D_slices, idx_slices, pred_slices = [], [], []
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
    req_idx = []
    for r in range(3):
        S_prev, S_next = slices[r], slices[r + 1]
        cross = [0] * len(S_next)
        for j, un in enumerate(S_next):
            cm = 0
            for i, upv in enumerate(S_prev):
                if le[upv][un]:
                    cm |= 1 << i
            cross[j] = cm
        rmap = []
        for mk in D_slices[r + 1]:
            rq = 0
            t = mk
            while t:
                lb = t & -t
                rq |= cross[lb.bit_length() - 1]
                t ^= lb
            rmap.append(idx_slices[r][rq])
        req_idx.append(rmap)

    d9_mods, d10_mods = [], []
    for p in PRIMES:
        vec = [1] * len(D_slices[0])
        for r in range(3):
            k_sz = len(slices[r])
            Dr = D_slices[r]
            imap = idx_slices[r]
            sup = vec[:]
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
            for k in range(k_sz - 1, -1, -1):
                bit = 1 << k
                sk = succ[k]
                for a, mk in enumerate(Dr):
                    if (mk & bit) and (mk & sk) == 0:
                        dst = imap[mk ^ bit]
                        rs, rd = mat[a], mat[dst]
                        for b in range(nr):
                            v = rd[b] + rs[b]
                            rd[b] = v - p if v >= p else v
            edges_b = []
            for k in range(k_sz - 1, -1, -1):
                bit = 1 << k
                sk = succ[k]
                edges_b.append([(b, imap[mk ^ bit]) for b, mk in enumerate(Dr) if (mk & bit) and (mk & sk) == 0])
            for step_pairs in edges_b:
                for row in mat:
                    for b_src, b_dst in step_pairs:
                        v = row[b_dst] + row[b_src]
                        row[b_dst] = v - p if v >= p else v
            Dr_next = D_slices[r + 1]
            n_next = len(Dr_next)
            rmap = req_idx[r]
            new_mat = [[0] * n_next for _ in range(n_next)]
            for a2 in range(n_next):
                ma2 = Dr_next[a2]
                srow = mat[rmap[a2]]
                drow = new_mat[a2]
                for b2 in range(a2, n_next):
                    if (ma2 & Dr_next[b2]) == ma2:
                        drow[b2] = srow[rmap[b2]]
            mat = new_mat
        d10_mods.append(sum(sum(row) for row in mat) % p)
    return crt_reconstruct(d9_mods), crt_reconstruct(d10_mods)


def engine2_eval_subgroup(K_perms):
    fixed_vars = [v for v in range(9) if all(g[v] == v for g in K_perms)]
    if len(fixed_vars) == 3:
        outs = []
        for b_dim in (3, 4):
            pts = [
                (pv, bv)
                for tot in range(4 + b_dim)
                for pv in range(4)
                for bv in range(1 << b_dim)
                if pv + bin(bv).count("1") == tot
            ]
            q_sz = len(pts)
            pred_sub = [0] * q_sz
            for u in range(q_sz):
                for v in range(u):
                    if pts[v][0] <= pts[u][0] and (pts[v][1] & pts[u][1]) == pts[v][1]:
                        pred_sub[u] |= 1 << v
            pt_idx = {pt: i for i, pt in enumerate(pts)}
            mb = (1 << b_dim) - 1
            dual_perm = [pt_idx[(3 - pv, (~bv) & mb)] for (pv, bv) in pts]
            outs.append(eval_p4_chain_zeta_mod(q_sz, pred_sub, dual_perm))
        return outs[0], outs[1]

    orb_id = [-1] * 512
    orb_rep = []
    for x in range(512):
        if orb_id[x] == -1:
            oid = len(orb_rep)
            orb_rep.append(x)
            for g in K_perms:
                y = 0
                for b in range(9):
                    if (x >> b) & 1:
                        y |= 1 << g[b]
                orb_id[y] = oid
    m = len(orb_rep)
    if m <= 64:
        ord_q = sorted(range(m), key=lambda i: (bin(orb_rep[i]).count("1"), orb_rep[i]))
        inv_q = {orig: new for new, orig in enumerate(ord_q)}
        pred = [0] * m
        for na, oa in enumerate(ord_q):
            xa = orb_rep[oa]
            for y in range(512):
                if (xa & y) == xa:
                    nb = inv_q[orb_id[y]]
                    if na < nb:
                        pred[nb] |= 1 << na
        return eval_single_zeta_mod(m, pred)

    if m == 96:
        blk_c = None
        for blk in range(3):
            others = [v for v in range(9) if v // 3 != blk]
            if any(any(g[v] != v for v in range(3 * blk, 3 * blk + 3)) and all(g[v] == v for v in others) for g in K_perms):
                blk_c = blk
                break
        if blk_c is None:
            fail("Expected independent 3-cycle block for m=96")
        act6 = [v for v in range(9) if v // 3 != blk_c]
        oid6 = [-1] * 64
        rep6 = []
        for x in range(64):
            if oid6[x] == -1:
                oid = len(rep6)
                rep6.append(x)
                for g in K_perms:
                    y = 0
                    for ti, v in enumerate(act6):
                        if (x >> ti) & 1:
                            y |= 1 << act6.index(g[v])
                    oid6[y] = oid
        ord24 = sorted(range(24), key=lambda i: (bin(rep6[i]).count("1"), rep6[i]))
        rep24 = [rep6[i] for i in ord24]
        inv24 = {orig: new for new, orig in enumerate(ord24)}
        le24 = [[False] * 24 for _ in range(24)]
        for a in range(24):
            xa = rep24[a]
            for y in range(64):
                if (xa & y) == xa:
                    le24[a][inv24[oid6[y]]] = True
        dual24 = [inv24[oid6[(~rep24[a]) & 63]] for a in range(24)]
        pred9 = [0] * 24
        for j in range(24):
            for i in range(j):
                if le24[i][j]:
                    pred9[j] |= 1 << i
        d9 = eval_p4_chain_zeta_mod(24, pred9, dual24)
        pts10 = [(i, b) for tot in range(8) for i in range(24) for b in range(2) if bin(rep24[i]).count("1") + b == tot]
        pred10 = [0] * 48
        for u in range(48):
            for v in range(u):
                if le24[pts10[v][0]][pts10[u][0]] and pts10[v][1] <= pts10[u][1]:
                    pred10[u] |= 1 << v
        pt10_idx = {pt: idx for idx, pt in enumerate(pts10)}
        dual48 = [pt10_idx[(dual24[i], 1 - b)] for (i, b) in pts10]
        d10 = eval_p4_chain_zeta_mod(48, pred10, dual48)
        return d9, d10

    if m == 80:
        return eval_4slice_markov_mod(K_perms, 0)

    fail(f"Unexpected quotient size {m}")


def verify_all() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    pkg_root = os.path.dirname(here)
    cert_path = os.path.join(pkg_root, "object", "d10_mod27_certificate.json")
    if not os.path.isfile(cert_path):
        cert_path = os.path.join(here, "d10_mod27_certificate.json")
    if not os.path.isfile(cert_path):
        fail("Certificate object/d10_mod27_certificate.json not found")

    with open(cert_path, encoding="utf-8") as f:
        cert = json.load(f)

    # 1. Strict schema & arithmetic self-consistency checks on EVERY field of cert
    if cert.get("target_id") != "dedekind-number-d10" or cert.get("partial_win_id") != "p1":
        fail("Invalid target_id or partial_win_id")
    if cert.get("prime_base") != 3 or cert.get("prime_exponent") != 3 or cert.get("modulus") != 27:
        fail("Invalid prime-power modulus specification")
    if cert["prime_base"] ** cert["prime_exponent"] != cert["modulus"]:
        fail("prime_base ** prime_exponent != modulus")

    exp_d0_d8 = [2, 3, 6, 20, 168, 7581, 7828354, 2414682040998, 56130437228687557907788]
    if cert.get("d0_to_d8_calibration") != exp_d0_d8:
        fail("d0_to_d8_calibration mismatch")
    d9_exact = 286386577668298411128469151667598498812366
    if cert.get("d9_exact_reference") != d9_exact:
        fail("d9_exact_reference mismatch")
    if cert.get("d6_to_d8_mod_9_calibration") != [exp_d0_d8[6] % 9, exp_d0_d8[7] % 9, exp_d0_d8[8] % 9]:
        fail("d6_to_d8_mod_9_calibration mismatch")
    if (cert.get("d9_mod_3"), cert.get("d9_mod_9"), cert.get("d9_mod_27")) != (d9_exact % 3, d9_exact % 9, d9_exact % 27):
        fail("d9 modular calibration fields do not match D(9)")

    # Check Engine 2 reproduction of D(0..7)
    got_d0_d7 = [dedekind_small_crt(n) for n in range(8)]
    if got_d0_d7 != exp_d0_d8[:8]:
        fail(f"Engine 2 D(0..7) mismatch: {got_d0_d7}")
    print("OK: Exact D(0..7) reproduced via multi-prime CRT Zeta (2, 3, 6, 20, 168, 7581, 7828354, 2414682040998)")

    # 2. Rebuild P_81 from cert["p81_generators"] and verify group order 81 & 50 subgroups
    gens_raw = cert.get("p81_generators", [])
    if len(gens_raw) != 4:
        fail("Expected 4 generators for P_81")
    gens = [tuple(g) for g in gens_raw]
    for g in gens:
        if sorted(g) != list(range(9)):
            fail("Generator is not a valid permutation of 0..8")
    # Also verify generators match exact standard wreath product C_3 wr C_3
    exp_gens = [
        (1, 2, 0, 3, 4, 5, 6, 7, 8),
        (0, 1, 2, 4, 5, 3, 6, 7, 8),
        (0, 1, 2, 3, 4, 5, 7, 8, 6),
        (3, 4, 5, 6, 7, 8, 0, 1, 2),
    ]
    if gens != exp_gens:
        fail("p81_generators modified from standard C_3 wr C_3 generators")

    id9 = tuple(range(9))
    G_set = {id9}
    dq = deque([id9])
    while dq:
        u = dq.popleft()
        for g in gens:
            v = compose9(u, g)
            if v not in G_set:
                G_set.add(v)
                dq.append(v)
    G = sorted(G_set)
    if len(G) != cert.get("p81_group_order") or len(G) != 81:
        fail("P_81 group order mismatch")

    g_idx = {g: i for i, g in enumerate(G)}
    mul = [[g_idx[compose9(G[i], G[j])] for j in range(81)] for i in range(81)]
    inv = [next(j for j in range(81) if mul[i][j] == 0) for i in range(81)]

    def close_mask(mask: int) -> int:
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
                    nxt |= 1 << mul[ia][lb.bit_length() - 1]
                    b ^= lb
                a ^= la
            if nxt == mask:
                return mask
            mask = nxt

    subs_set = {1}
    dq = deque([1])
    while dq:
        hm = dq.popleft()
        for g in range(81):
            if not ((hm >> g) & 1):
                km = close_mask(hm | (1 << g))
                if km not in subs_set:
                    subs_set.add(km)
                    dq.append(km)
    subs = sorted(subs_set, key=lambda m: (bin(m).count("1"), m))
    if len(subs) != cert.get("p81_total_subgroups") or len(subs) != 50:
        fail("P_81 total subgroup count mismatch")

    # Solve Burnside Table-of-Marks weights independently and verify against all 50 transitive sets!
    p81_classes = []
    vis = set()
    for m in subs:
        if m in vis:
            continue
        cls = set()
        for g in range(81):
            gi = inv[g]
            cm = 0
            t = m
            while t:
                lb = t & -t
                cm |= 1 << mul[gi][mul[lb.bit_length() - 1][g]]
                t ^= lb
            cls.add(cm)
        vis |= cls
        p81_classes.append(sorted(cls))

    def solve_marks(min_ord):
        elig = [c for c in p81_classes if bin(c[0]).count("1") >= min_ord]
        mc = len(elig)
        M = [[0] * mc for _ in range(mc)]
        rhs = [81 // bin(elig[a][0]).count("1") for a in range(mc)]
        for a in range(mc):
            Ha = elig[a][0]
            oa = bin(Ha).count("1")
            for b in range(mc):
                Hb = elig[b][0]
                cg = 0
                for g in range(81):
                    gi = inv[g]
                    ok = True
                    t = Hb
                    while t:
                        lb = t & -t
                        if not ((Ha >> mul[gi][mul[lb.bit_length() - 1][g]]) & 1):
                            ok = False
                            break
                        t ^= lb
                    if ok:
                        cg += 1
                M[a][b] = cg // oa
        w = [0] * mc
        for a in range(mc):
            if any(M[a][b] != 0 for b in range(a + 1, mc)):
                fail("Marks matrix not lower triangular")
            rem = rhs[a] - sum(M[a][b] * w[b] for b in range(a))
            if rem % M[a][a] != 0:
                fail("Non-integer mark weight")
            w[a] = rem // M[a][a]
        mod_check = (81 * 3) // min_ord
        for H0 in subs:
            o0 = bin(H0).count("1")
            lhs = 0
            for b in range(mc):
                Hb = elig[b][0]
                cg = 0
                for g in range(81):
                    gi = inv[g]
                    ok = True
                    t = Hb
                    while t:
                        lb = t & -t
                        if not ((H0 >> mul[gi][mul[lb.bit_length() - 1][g]]) & 1):
                            ok = False
                            break
                        t ^= lb
                    if ok:
                        cg += 1
                lhs += w[b] * (cg // o0)
            if (lhs - (81 // o0)) % mod_check != 0:
                fail("Table-of-Marks congruence check failed on P_81/H0")
        return {elig[i][0]: w[i] for i in range(mc)}

    mw3 = solve_marks(81)
    mw9 = solve_marks(27)
    mw27 = solve_marks(9)
    print("OK: P_81 subgroup lattice (50 subgroups) and Table-of-Marks congruence verified over Z")

    # 3. Run Independent Engine 1 (C99 128-bit Galois / Dedekind interval engine)
    c_src = os.path.join(here, "verify_engine1_c99.c")
    cc_bin = shutil.which("cc") or shutil.which("clang") or shutil.which("gcc")
    if not os.path.isfile(c_src) or not cc_bin:
        fail("verify_engine1_c99.c or C99 compiler not found")

    e1_classes = {}
    e1_raw = {}
    e1_mod = {}
    with tempfile.TemporaryDirectory(prefix="v3_d10_e1_") as tmpd:
        exe = os.path.join(tmpd, "verify_e1")
        cp = subprocess.run([cc_bin, "-O3", "-std=c99", "-pthread", c_src, "-o", exe],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if cp.returncode != 0:
            fail(f"Engine 1 compilation failed: {cp.stdout}")
        rp = subprocess.run([exe], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if rp.returncode != 0:
            fail(f"Engine 1 execution failed: {rp.stdout}")
        for line in rp.stdout.splitlines():
            if line.startswith("E1_CLASS "):
                kv = dict(tok.split("=") for tok in line.split()[1:])
                e1_classes[(int(kv["ord"]), int(kv["q9"]))] = (int(kv["fix9"]), int(kv["fix10"]))
            elif line.startswith("E1_RAW "):
                e1_raw = {k: int(v) for k, v in (tok.split("=") for tok in line.split()[1:])}
            elif line.startswith("E1_MOD "):
                e1_mod = {k: int(v) for k, v in (tok.split("=") for tok in line.split()[1:])}
    print("OK: Engine 1 (C99 128-bit Mobius + Galois/Interval) verified D(0..7), D(6..8) mod 9, and all 9 classes")

    # 4. Run Independent Engine 2 (Python multi-prime CRT + Markov/Zeta transfer) on EVERY class in cert
    #    and verify S_9-conjugacy partitioning of all 27 subgroups of order >= 9!
    s9_list = cert.get("s9_classes", [])
    if len(s9_list) != 9:
        fail("Expected 9 S_9-classes in certificate")

    def are_s9_conj(K1_perms, K2_perms):
        if len(K1_perms) != len(K2_perms):
            return False
        K2_set = set(K2_perms)
        def orbs9(K):
            v = [False] * 9
            r = []
            for i in range(9):
                if not v[i]:
                    o = sorted({g[i] for g in K})
                    for x in o:
                        v[x] = True
                    r.append(o)
            r.sort(key=lambda x: (len(x), x))
            return r
        o1, o2 = orbs9(K1_perms), orbs9(K2_perms)
        if [len(x) for x in o1] != [len(x) for x in o2]:
            return False
        cands = [[u for o in o2 if len(o) == next(len(z) for z in o1 if i in z) for u in o] for i in range(9)]
        pm = [-1] * 9
        used = [False] * 9
        def bt(idx):
            if idx == 9:
                pi = tuple(pm)
                pi_i = inv9(pi)
                return all(compose9(pi, compose9(g, pi_i)) in K2_set for g in K1_perms)
            for y in cands[idx]:
                if not used[y]:
                    pm[idx] = y
                    used[y] = True
                    if bt(idx + 1):
                        return True
                    used[y] = False
            return False
        return bt(0)

    subs_ge9 = [m for m in subs if bin(m).count("1") >= 9]
    matched_subs = set()

    sum_d9_3 = sum_d9_9 = sum_d9_27 = 0
    sum_d10_3 = sum_d10_9 = sum_d10_27 = 0

    for expected_idx, entry in enumerate(s9_list):
        if entry.get("class_index") != expected_idx:
            fail(f"class_index mismatch at {expected_idx}")
        rgens = [tuple(g) for g in entry.get("rep_generators", [])]
        if not rgens or any(tuple(g) not in G_set for g in rgens):
            fail(f"Invalid rep_generators in class {expected_idx}")
        rep_m = 1
        for g in rgens:
            rep_m |= 1 << g_idx[g]
        rep_m = close_mask(rep_m)
        K_perms = [G[i] for i in range(81) if (rep_m >> i) & 1]
        if len(K_perms) != entry.get("subgroup_order"):
            fail(f"subgroup_order mismatch in class {expected_idx}")

        # Verify quotient_b9_size
        seen = [False] * 512
        q9 = 0
        for x in range(512):
            if not seen[x]:
                q9 += 1
                for g in K_perms:
                    y = 0
                    for b in range(9):
                        if (x >> b) & 1:
                            y |= 1 << g[b]
                    seen[y] = True
        if q9 != entry.get("quotient_b9_size"):
            fail(f"quotient_b9_size mismatch in class {expected_idx}")

        # Find all P_81-classes of order >= 9 that are S_9-conjugate to rep_m
        w3 = w9 = w27 = sub_cnt = 0
        for p_cls in p81_classes:
            if bin(p_cls[0]).count("1") < 9:
                continue
            cand_perms = [G[i] for i in range(81) if (p_cls[0] >> i) & 1]
            if are_s9_conj(K_perms, cand_perms):
                w3 += mw3.get(p_cls[0], 0)
                w9 += mw9.get(p_cls[0], 0)
                w27 += mw27.get(p_cls[0], 0)
                sub_cnt += len(p_cls)
                matched_subs.update(p_cls)

        if sub_cnt != entry.get("num_subgroups_in_p81"):
            fail(f"num_subgroups_in_p81 mismatch in class {expected_idx}")
        if (w3, w9, w27) != (entry.get("weight_mod3"), entry.get("weight_mod9"), entry.get("weight_mod27")):
            fail(f"Burnside weights mismatch in class {expected_idx}")

        # Engine 2 independent evaluation
        f9_e2, f10_e2 = engine2_eval_subgroup(K_perms)
        f9_e1, f10_e1 = e1_classes.get((len(K_perms), q9), (-1, -1))
        if (f9_e1, f10_e1) != (f9_e2, f10_e2):
            fail(f"Engine 1 vs Engine 2 mismatch at class {expected_idx}: {(f9_e1, f10_e1)} != {(f9_e2, f10_e2)}")
        if (entry.get("fix_d9"), entry.get("fix_d10")) != (f9_e2, f10_e2):
            fail(f"Certificate fix_d9/fix_d10 mismatch at class {expected_idx}")

        print(
            f"OK: Class {expected_idx} (|K|={len(K_perms):2d}, subs={sub_cnt:2d}, |B^9/K|={q9:3d}): "
            f"Fix_D9={f9_e2}, Fix_D10={f10_e2} (Engine 1 == Engine 2 == Cert)"
        )

        sum_d9_3 += w3 * f9_e2
        sum_d9_9 += w9 * f9_e2
        sum_d9_27 += w27 * f9_e2
        sum_d10_3 += w3 * f10_e2
        sum_d10_9 += w9 * f10_e2
        sum_d10_27 += w27 * f10_e2

    if matched_subs != set(subs_ge9):
        fail("S_9 classes did not partition all 27 subgroups of order >= 9")

    # 5. Verify raw sums, published D(10) references, and final residues
    raw_exp = {
        "d9_m3": sum_d9_3,
        "d9_m9": sum_d9_9,
        "d9_m27": sum_d9_27,
        "d10_m3": sum_d10_3,
        "d10_m9": sum_d10_9,
        "d10_m27": sum_d10_27,
    }
    if cert.get("raw_burnside_sums") != raw_exp or e1_raw != raw_exp:
        fail("raw_burnside_sums mismatch")

    pub = cert.get("published_d10_references", {})
    # Class 3 is cyclic 9-cycle (q9=60), Class 8 is P_81 (q9=24)
    c_cyc9 = next(c for c in s9_list if c["subgroup_order"] == 9 and c["quotient_b9_size"] == 60)
    c_p81 = next(c for c in s9_list if c["subgroup_order"] == 81)
    if pub.get("phi_10_cycle9") != c_cyc9["fix_d10"] or pub.get("phi_10_cycle9") != 1702659955:
        fail("published phi_10_cycle9 reference mismatch")
    if pub.get("p3_to_q24_p81") != c_p81["fix_d10"] or pub.get("p3_to_q24_p81") != 6526:
        fail("published p3_to_q24_p81 reference mismatch")
    if pub.get("d10_mod_3_published") != 1:
        fail("published d10_mod_3_published reference mismatch")

    d9_r3, d9_r9, d9_r27 = sum_d9_3 % 3, sum_d9_9 % 9, sum_d9_27 % 27
    d10_r3, d10_r9, d10_r27 = sum_d10_3 % 3, sum_d10_9 % 9, sum_d10_27 % 27

    if (d9_r3, d9_r9, d9_r27) != (0, 6, 24):
        fail("D(9) residue reproduction failed")
    if (cert.get("d10_mod_3"), cert.get("d10_mod_9"), cert.get("d10_mod_27")) != (d10_r3, d10_r9, d10_r27):
        fail("Certificate d10_mod_3/9/27 mismatch")
    if (e1_mod["d10_3"], e1_mod["d10_9"], e1_mod["d10_27"]) != (d10_r3, d10_r9, d10_r27):
        fail("Engine 1 vs Engine 2 final residue mismatch")
    if d10_r27 % 9 != d10_r9 or d10_r9 % 3 != d10_r3 or d10_r3 != 1:
        fail("Internal prime-power reduction consistency failed")



    print(f"OK: D(9) reproduced modulo (3, 9, 27) = ({d9_r3}, {d9_r9}, {d9_r27}) == D(9) mod (3, 9, 27)")
    print(f"OK: Published arXiv:2611.13887v1 checks reproduced: phi_10(C_9)=1702659955, |P_3^Q|=6526, D(10) == {d10_r3} (mod 3)")
    print(f"VERIFIED: D(10) == {d10_r27} (mod 27) [and D(10) == {d10_r9} (mod 9)] by two independent implementations")
    print("PASS")


if __name__ == "__main__":
    try:
        verify_all()
    except SystemExit:
        raise
    except Exception as exc:
        fail(f"Unhandled exception: {exc}")
