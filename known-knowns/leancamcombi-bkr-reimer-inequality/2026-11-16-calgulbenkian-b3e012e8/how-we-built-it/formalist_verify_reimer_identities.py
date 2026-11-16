#!/usr/bin/env python3
"""Finite-model verification of the closed-form Z Butterfly vectors and parity identities."""
import itertools
import random


def popcount(x: int) -> int:
    return bin(x).count("1")


def reimer_span(mask_all: int, u: int, v: int):
    lo = u & v
    hi = u | v
    return {z for z in range(mask_all + 1) if (lo & ~z) == 0 and (z & ~hi) == 0}


def vec_ur(z: int, t: int) -> int:
    return 1 if (z & ~t) == 0 else 0


def vec_uy(z: int, t: int) -> int:
    return (-1) ** popcount(t) if (t & ~z) == 0 else 0


def vec_vb(w: int, b: int, t: int) -> int:
    if (t & ~w) == (b & ~w):
        return (-1) ** popcount(w & b & t)
    return 0


def zdot(n_states: int, f, g) -> int:
    return sum(f(t) * g(t) for t in range(n_states))


def rank_int(rows) -> int:
    if not rows:
        return 0
    mat = [list(r) for r in rows]
    m, n = len(mat), len(mat[0])
    r = 0
    for col in range(n):
        piv = None
        for i in range(r, m):
            if mat[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        for i in range(r + 1, m):
            if mat[i][col] != 0:
                p_val = mat[r][col]
                i_val = mat[i][col]
                for c in range(col, n):
                    mat[i][c] = p_val * mat[i][c] - i_val * mat[r][c]
        r += 1
    return r


def main() -> None:
    rng = random.Random(20261115)
    for k in range(0, 5):
        n_states = 1 << k
        mask_all = n_states - 1

        # 1. Exhaustive orthogonality & parity checks
        for z1 in range(n_states):
            for z2 in range(n_states):
                val = zdot(n_states, lambda t: vec_ur(z1, t), lambda t: vec_uy(z2, t))
                if z1 != z2:
                    assert val == 0

        for w in range(n_states):
            wc = mask_all ^ w
            for b in range(n_states):
                sp_r = reimer_span(mask_all, w, b)
                sp_y = reimer_span(mask_all, wc, b)
                for z in range(n_states):
                    d_ur = zdot(n_states, lambda t: vec_vb(w, b, t), lambda t: vec_ur(z, t))
                    d_uy = zdot(n_states, lambda t: vec_vb(w, b, t), lambda t: vec_uy(z, t))
                    if z not in sp_r:
                        assert d_ur == 0
                    if z not in sp_y:
                        assert d_uy == 0
                    if z == w:
                        assert d_ur % 2 == 1
                    if (w & ~z) != 0:
                        assert d_ur % 2 == 0

        # 2. Sampled Butterfly systems check full rank |W| + |S1| + |S2| and |W| <= |R cap Y'|
        trials = 1 if k == 0 else 150
        for _ in range(trials):
            w_sub = [w for w in range(n_states) if rng.random() < 0.5]
            b_map = {w: rng.randrange(n_states) for w in w_sub}
            r_union = set()
            y_union = set()
            for w in w_sub:
                r_union |= reimer_span(mask_all, w, b_map[w])
                y_union |= reimer_span(mask_all, mask_all ^ w, b_map[w])
            s1 = [z for z in range(n_states) if z not in r_union]
            s2 = [z for z in sorted(r_union) if z not in y_union]
            rows = (
                [[vec_vb(w, b_map[w], t) for t in range(n_states)] for w in w_sub]
                + [[vec_ur(z, t) for t in range(n_states)] for z in s1]
                + [[vec_uy(z, t) for t in range(n_states)] for z in s2]
            )
            rk = rank_int(rows)
            assert rk == len(rows)
            assert len(rows) <= n_states
            assert len(w_sub) <= len(r_union & y_union)

        print(f"k={k} (2^k={n_states}): exhaustive orthogonality/parity + {trials} butterfly rank checks OK")

    print("ALL_BUTTERFLY_CHECKS_PASSED")


if __name__ == "__main__":
    main()
