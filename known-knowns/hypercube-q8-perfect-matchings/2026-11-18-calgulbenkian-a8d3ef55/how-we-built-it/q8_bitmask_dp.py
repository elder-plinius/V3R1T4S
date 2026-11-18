#!/usr/bin/env python3
"""
Engine A2 (Zero-Shared-Code Independent Implementation):
Direct 2^n-bit Vertex-Mask Hypercube Frontier DP on Q_n (n = 1..8).

Does NOT assume or use bipartite permanents, Ryser/Glynn, or stabilizer-quotient
matrices. Instead:
  1. Builds the actual 2^n-vertex hypercube graph Q_n = ({0..2^n-1}, E_n).
  2. Builds the explicit subgroup P <= Aut(Q_n) of vertex permutations and verifies
     directly that every g in P is a graph automorphism of Q_n and P is a group.
  3. Enumerates all P-orbits of edges O_e = { {g(u), g(v)} : g in P } for {u,v} in E_n,
     keeps ONLY those edge-orbits whose edges are pairwise vertex-disjoint on Q_n
     (verified directly on the 2^n vertices of Q_n), and encodes each valid edge-orbit
     as a 2^n-bit integer vertex mask on Q_n.
  4. Partitions V(Q_n) into connected components under valid edge-orbits, orders
     vertices in each component by (Hamming weight, vertex id) for tight frontier width,
     and counts exact P-invariant perfect matchings of Q_n via memoized 2^n-bit mask DP.
"""

import time


def popcount(x: int) -> int:
    return bin(x).count("1")


def apply_coord_perm(perm, n: int, v: int) -> int:
    out = 0
    for c in range(n):
        if (v >> c) & 1:
            out |= 1 << perm[c]
    return out


def build_group_from_generators(gens, n: int):
    """Generate full subgroup of Aut(Q_n) from coordinate-permutation generators."""
    N = 1 << n
    id_map = tuple(range(N))
    gen_maps = []
    for perm in gens:
        mp = tuple(apply_coord_perm(perm, n, v) for v in range(N))
        gen_maps.append(mp)

    seen = {id_map}
    queue = [id_map]
    while queue:
        cur = queue.pop()
        for g in gen_maps:
            nxt = tuple(g[cur[v]] for v in range(N))
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)

    group = sorted(seen)
    # Verify every element is an automorphism of Q_n and group axioms hold
    edges = set()
    for u in range(N):
        for b in range(n):
            v = u ^ (1 << b)
            if u < v:
                edges.add((u, v))
    for g in group:
        assert len(set(g)) == N, "Not a bijection!"
        for u, v in edges:
            gu, gv = g[u], g[v]
            if gu > gv:
                gu, gv = gv, gu
            assert (gu, gv) in edges, "Not a Q_n automorphism!"
    return group, edges


def count_p_invariant_matchings_on_qn(n: int, gens) -> int:
    N = 1 << n
    group, edges = build_group_from_generators(gens, n)

    # Build all distinct P-orbits of edges on Q_n and keep vertex-disjoint ones
    seen_edges = set()
    valid_orbit_masks = []
    for u, v in sorted(edges):
        if (u, v) in seen_edges:
            continue
        orb_edges = set()
        for g in group:
            a, b = g[u], g[v]
            if a > b:
                a, b = b, a
            orb_edges.add((a, b))
        seen_edges |= orb_edges

        # Check directly on Q_n whether orb_edges is a valid matching (degree <= 1 everywhere)
        vmask = 0
        collision = False
        for a, b in orb_edges:
            bit_a = 1 << a
            bit_b = 1 << b
            if (vmask & bit_a) or (vmask & bit_b):
                collision = True
                break
            vmask |= bit_a | bit_b
        if not collision:
            valid_orbit_masks.append(vmask)

    # Connected components of V(Q_n) under valid_orbit_masks
    adj_v = [0] * N
    orbits_at_v = [[] for _ in range(N)]
    for om in valid_orbit_masks:
        x = om
        verts = []
        while x:
            lsb = x & -x
            v = lsb.bit_length() - 1
            verts.append(v)
            x ^= lsb
        for v in verts:
            adj_v[v] |= om
            orbits_at_v[v].append(om)

    visited = 0
    total_ways = 1
    for start in range(N):
        if (visited >> start) & 1:
            continue
        comp_mask = 1 << start
        stack = [start]
        while stack:
            u = stack.pop()
            nbrs = adj_v[u] & ~comp_mask
            while nbrs:
                lsb = nbrs & -nbrs
                w = lsb.bit_length() - 1
                comp_mask |= lsb
                stack.append(w)
                nbrs ^= lsb
        visited |= comp_mask

        # Order vertices in this component by (Hamming weight, vertex index)
        comp_verts = []
        x = comp_mask
        while x:
            lsb = x & -x
            v = lsb.bit_length() - 1
            comp_verts.append(v)
            x ^= lsb
        comp_verts.sort(key=lambda v: (popcount(v), v))

        # Iterative layer-by-layer / pivot frontier DP over 2^n-bit masks!
        # State: exact 2^n-bit mask of ALREADY COVERED vertices inside comp_mask.
        states = {0: 1}
        for pivot in comp_verts:
            pbit = 1 << pivot
            next_states = {}
            cand_orbits = orbits_at_v[pivot]
            for cov_mask, ways in states.items():
                if (cov_mask >> pivot) & 1:
                    next_states[cov_mask] = next_states.get(cov_mask, 0) + ways
                else:
                    for om in cand_orbits:
                        if (cov_mask & om) == 0:
                            nm = cov_mask | om
                            next_states[nm] = next_states.get(nm, 0) + ways
            states = next_states

        comp_ways = states.get(comp_mask, 0)
        total_ways *= comp_ways
        if total_ways == 0:
            return 0

    return total_ways


def count_folded_cube_matchings(n: int) -> int:
    """Exact perfect matchings of folded n-cube FQ_n = Q_{n-1} + antipodal edges."""
    N = 1 << (n - 1)
    all_bits = N - 1
    edges_masks = []
    seen = set()
    for u in range(N):
        nbrs = [u ^ (1 << b) for b in range(n - 1)] + [u ^ all_bits]
        for v in nbrs:
            a, b = (u, v) if u < v else (v, u)
            if (a, b) not in seen and a != b:
                seen.add((a, b))
                edges_masks.append((1 << a) | (1 << b))
    orbits_at_v = [[] for _ in range(N)]
    for em in edges_masks:
        x = em
        while x:
            lsb = x & -x
            v = lsb.bit_length() - 1
            orbits_at_v[v].append(em)
            x ^= lsb
    # Order by min(wt(v), n - 1 - wt(v)) so antipodal pairs sit together!
    verts = sorted(range(N), key=lambda v: (min(popcount(v), (n - 1) - popcount(v)), v))
    states = {0: 1}
    for pivot in verts:
        next_states = {}
        cands = orbits_at_v[pivot]
        for cov, ways in states.items():
            if (cov >> pivot) & 1:
                next_states[cov] = next_states.get(cov, 0) + ways
            else:
                for em in cands:
                    if (cov & em) == 0:
                        nm = cov | em
                        next_states[nm] = next_states.get(nm, 0) + ways
        states = next_states
    return states.get((1 << N) - 1, 0)


def main():
    known_a005271 = {
        1: 1,
        2: 2,
        3: 9,
        4: 272,
        5: 589185,
        6: 16332454526976,
        7: 391689748492473664721077609089,
    }

    print("=== Engine A2: Full Q_n Bitmask Frontier DP (n = 1..5) ===")
    for n in range(1, 6):
        t0 = time.time()
        val = count_p_invariant_matchings_on_qn(n, [])
        dt = time.time() - t0
        assert val == known_a005271[n], f"Mismatch at n={n}: {val} != {known_a005271[n]}"
        print(f"Q_{n}: exact = {val} (matches A005271({n}), {dt:.4f}s)")

    print("\n=== Engine A2: Folded Cube FQ_n Bitmask Frontier DP (n = 2..5) ===")
    for n in range(2, 6):
        t0 = time.time()
        val = count_folded_cube_matchings(n)
        dt = time.time() - t0
        print(f"FQ_{n} ({1 << (n-1)} vertices, {n}-regular): exact = {val} ({dt:.4f}s)")

    print("\n=== Engine A2: Sylow 5-Subgroup P_5 = <(0 1 2 3 4)> on Q_5..Q_8 ===")
    gen5 = [[1, 2, 3, 4, 0, 5, 6, 7]]
    for n in range(5, 9):
        t0 = time.time()
        g_n = [[x for x in gen5[0][:n]]]
        val = count_p_invariant_matchings_on_qn(n, g_n)
        dt = time.time() - t0
        rem = val % 5
        chk = ""
        if n in known_a005271:
            exp = known_a005271[n] % 5
            assert rem == exp, f"Mod 5 mismatch at n={n}: {rem} != {exp}"
            chk = f" [MATCHES A005271({n}) mod 5 == {exp}]"
        print(f"Q_{n} |Fix(P_5)| = {val} | mod 5 = {rem}{chk} ({dt:.4f}s)")

    print("\n=== Engine A2: Sylow 7-Subgroup P_7 = <(0 1 2 3 4 5 6)> on Q_7..Q_8 ===")
    for n in range(7, 9):
        t0 = time.time()
        g_n = [[1, 2, 3, 4, 5, 6, 0] + ([7] if n == 8 else [])]
        val = count_p_invariant_matchings_on_qn(n, g_n)
        dt = time.time() - t0
        rem = val % 7
        chk = ""
        if n in known_a005271:
            exp = known_a005271[n] % 7
            assert rem == exp, f"Mod 7 mismatch at n={n}: {rem} != {exp}"
            chk = f" [MATCHES A005271({n}) mod 7 == {exp}]"
        print(f"Q_{n} |Fix(P_7)| = {val} | mod 7 = {rem}{chk} ({dt:.4f}s)")

    print("\n=== Engine A2: Sylow 3-Subgroup P_3 = <(0 1 2),(3 4 5)> on Q_6..Q_8 ===")
    for n in range(6, 9):
        t0 = time.time()
        tail = list(range(6, n))
        g_n = [[1, 2, 0, 3, 4, 5] + tail, [0, 1, 2, 4, 5, 3] + tail]
        val = count_p_invariant_matchings_on_qn(n, g_n)
        dt = time.time() - t0
        rem = val % 3
        chk = ""
        if n in known_a005271:
            exp = known_a005271[n] % 3
            assert rem == exp, f"Mod 3 mismatch at n={n}: {rem} != {exp}"
            chk = f" [MATCHES A005271({n}) mod 3 == {exp}]"
        print(f"Q_{n} |Fix(P_3)| = {val} | mod 3 = {rem}, mod 9 = {val % 9}{chk} ({dt:.4f}s)")


if __name__ == "__main__":
    main()
