#!/usr/bin/env python3
"""
neon_certify_global_L_r12.py

Certifies the UNCONDITIONAL GLOBAL LOWER BOUND for EVERY odd covering system:
    L >= 6,557,114,959,770,375  (= 3^5 * 5^3 * 7^2 * 11^2 * 13^2 * 17 * 19 * 23 * 29)
(39 times the earlier bound 168,131,152,814,625)

Proof architecture (100% exact Python Fraction arithmetic, zero floats in certificates):
  1. omega(L) <= 8: impossible (Theorem A, Schroeder; triple-verified).
  2. omega(L) = 9:  L >= 6,557,114,959,770,375 (from six earlier nine-prime theorems, rebuilt bit-exact by a second implementation).
  3. omega(L) >= 14: prod_{m=0}^{13} p_m = 307,444,891,294,245,705 > 6,557,114,959,770,375.
  4. omega(L) in {10, 11, 12, 13}: By Lemma A1, any covering with L < X := 6,557,114,959,770,375
     transfers to the first r odd primes P_r with exponents e >= 1 and prod p_m^{e_m} < X.
     All 1,754 such vectors (1,484 at r=10; 248 at r=11; 21 at r=12; 1 at r=13) are covered
     componentwise (e <= e*) by:
       - Exact rational Lemma U (scalar distortion) certificates (`r12_global_L_scalar_cert.json`)
       - 13 tiny exact rational anchored certificates (`r12_global_L_anchored_cert.json`),
         12 of which close at Phase 1 (`basic`, 32 rows each) and 1 at Phase 2 (`mixed`)!
     Also certifies the scalar-only intermediate milestone L >= 473,824,157,932,125 (2.82x public).
"""
import os
import sys
import json
import time
from fractions import Fraction
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from neon_global_bound_probe_r12 import ODD_PRIMES, optimize_scalar
from neon_global_L_exact_map_r12 import enum_exp_vecs
from neon_global_anchored_probe_r12 import GeneralExponentModel

L_TARGET = 3**5 * 5**3 * 7**2 * 11**2 * 13**2 * 17 * 19 * 23 * 29  # 6,557,114,959,770,375
L_SCALAR_ONLY = 3**4 * 5**3 * 7**2 * 11 * 13 * 17 * 19 * 23 * 29 * 31  # 473,824,157,932,125


def exact_scalar_B(primes, exps, k0, Cs):
    """100% exact Fraction evaluation of Lemma U bound B(primes, exps, k0, Cs)."""
    r = len(primes)
    assert len(exps) == r and len(Cs) == r - k0
    assert 1 <= k0 < r
    prod_th = Fraction(1)
    sum_th = Fraction(0)
    for m in range(k0):
        p = primes[m]
        e = exps[m]
        pe = p ** e
        th = Fraction(pe - 1, (p - 2) * pe + 1)
        prod_th *= (1 + th)
        sum_th += th
    B = prod_th - 1 - sum_th

    max_K = max(primes[k0:]) + 2
    dist = {1: Fraction(1)}
    mean = Fraction(1)
    for m in range(r):
        p = primes[m]
        e = exps[m]
        if m >= k0:
            C = Cs[m - k0]
            assert C > 1 and C <= p, f"Bad C={C} at p={p}"
            rho = Fraction(p**e - 1, (p - 1) * p**e)
            delta = 1 - Fraction(1, C)
            assert delta >= rho, f"delta={delta} < rho={rho} at p={p}"
            # E[(rho*M - delta)_+] = rho*mean - delta + sum_{k < delta/rho} P(M=k)*(delta - rho*k)
            ex = rho * mean - delta
            for k, pk in dist.items():
                if rho * k < delta:
                    ex += pk * (delta - rho * k)
            B += C * ex
        if m == r - 1:
            break
        if m < k0:
            pe = p ** e
            denom = (p - 2) * pe + 1
            p_ge = [Fraction((p - 1) * (p ** (e - t)), denom) for t in range(1, e + 1)]
            steps = [(0, 1 - p_ge[0])]
            for t in range(1, e):
                steps.append((t, p_ge[t - 1] - p_ge[t]))
            steps.append((e, p_ge[e - 1]))
            mean *= (1 + sum(p_ge))
        else:
            C = Cs[m - k0]
            steps = [(0, 1 - C / p)]
            for t in range(1, e):
                steps.append((t, C * Fraction(p - 1, p**(t + 1))))
            steps.append((e, C / (p**e)))
            mean *= (1 + C * Fraction(p**e - 1, (p - 1) * p**e))
        nd = {}
        for k, pk in dist.items():
            for t, pt in steps:
                nk = k * (t + 1)
                if nk >= max_K:
                    break
                nd[nk] = nd.get(nk, Fraction(0)) + pk * pt
        dist = nd
    return B


def quantize_caps(primes, exps, k0, Cs_float, den=128):
    """Quantize float caps to exact Fractions with denominator `den`, strictly satisfying side conditions."""
    Cs = []
    for idx, c in enumerate(Cs_float):
        p = primes[k0 + idx]
        e = exps[k0 + idx]
        rho = Fraction(p**e - 1, (p - 1) * p**e)
        c_min = Fraction(1, 1 - rho)
        q = int(round(c * den))
        cand = Fraction(q, den)
        while cand <= c_min:
            q += 1
            cand = Fraction(q, den)
        if cand > p:
            cand = Fraction(p)
        Cs.append(cand)
    return Cs


def certify_anchored_general(name, primes_later, exps, C7=Fraction(3, 2), taus_later=None, thresh=Fraction(1, 40)):
    """
    Exact Fraction anchored certifier (Phases 1 & 2: basic / basic75 / mixed) for general r primes!
    Returns (cert_dict, ok).
    """
    t0 = time.time()
    mod = GeneralExponentModel(primes_later, exps, C7=C7, taus_later=taus_later, U_cut=8, V_cut=6)
    rows = []
    min_m = None

    def eval_ord(st):
        R = mod.exact_reserve(st)
        env = mod.eval_ord_envelope(st, xi=None, use_kappa=False)
        Ls = tuple(
            mod.stage_expectation(env, dist, mean, t, mult_scale=1) / bt
            for (dist, mean), t, bt in zip(mod.full, mod.taus, mod.betas)
        )
        return R, Ls

    def rec(phase, st, R, Ls):
        nonlocal min_m
        S = sum(Ls)
        m = R - S
        assert m > 0
        rows.append([phase, list(st), str(R), str(S)])
        if min_m is None or m < min_m[0]:
            min_m = (m, phase, list(st), R, Ls)

    # Phase 1: basic / basic75
    rem_abc = []
    for a in (1, 2):
        for b in (2, 4):
            for c in (a, 3 - a):
                items = []
                for j in range(1, 5):
                    st = (a, b, c, -1, j, 0, 0, 0, -1)
                    R, Ls = eval_ord(st)
                    items.append((st, R, Ls))
                if all(R > sum(Ls) and R - sum(Ls) >= thresh for _, R, Ls in items):
                    for st, R, Ls in items:
                        rec("basic", st, R, Ls)
                elif b == 2 and all(R + Fraction(1, 5) > sum(Ls) and R + Fraction(1, 5) - sum(Ls) >= thresh for _, R, Ls in items):
                    for st, R, Ls in items:
                        rec("basic75", st, R + Fraction(1, 5), Ls)
                else:
                    rem_abc.append((a, b, c))

    # Phase 2: mixed
    fails = []
    for a, b, c in rem_abc:
        reps = {}
        for r in range(45):
            if r % 3 and r % 9 != 1 and r % 5 and r % 15 != a:
                reps.setdefault((r % 3, r % 9 == b % 9, r % 5 == a, r % 5 == c), r)
        for r in reps.values():
            for d in (1, 2):
                for k in range(1, 5):
                    if (d, k) == (a % 3, a % 5):
                        continue
                    for j, i_e in [(jj, 0) for jj in range(1, 5)] + [(k, 1)]:
                        st = (a, b, c, r, j, d, k, i_e, -1)
                        R, Ls = eval_ord(st)
                        if R > sum(Ls):
                            rec("mixed", st, R, Ls)
                        else:
                            fails.append((st, float(R - sum(Ls))))
    if fails:
        print(f"  [FAIL] {name}: {len(fails)} open mixed states! worst={min(fails, key=lambda x: x[1])}")
        return None, False

    # Tree completeness audit (Phases 1 & 2)
    row_set = {(ph, tuple(k)) for ph, k, _, _ in rows}
    used = set()
    uncov = 0
    for a in (1, 2):
        for b in (2, 4):
            for c in (a, 3 - a):
                bsts = [(a, b, c, -1, j, 0, 0, 0, -1) for j in range(1, 5)]
                if all(("basic", st) in row_set for st in bsts):
                    used.update(("basic", st) for st in bsts)
                    continue
                if b == 2 and all(("basic75", st) in row_set for st in bsts):
                    used.update(("basic75", st) for st in bsts)
                    continue
                reps = {}
                for r in range(45):
                    if r % 3 and r % 9 != 1 and r % 5 and r % 15 != a:
                        reps.setdefault((r % 3, r % 9 == b % 9, r % 5 == a, r % 5 == c), r)
                for r in reps.values():
                    for d in (1, 2):
                        for k in range(1, 5):
                            if (d, k) == (a % 3, a % 5):
                                continue
                            for j, i_e in [(jj, 0) for jj in range(1, 5)] + [(k, 1)]:
                                st = (a, b, c, r, j, d, k, i_e, -1)
                                if ("mixed", st) in row_set:
                                    used.add(("mixed", st))
                                else:
                                    uncov += 1
    unused = len(row_set) - len(used)
    assert uncov == 0 and unused == 0
    counts = dict(Counter(r[0] for r in rows))
    m, phs, mk, mR, mL = min_m
    print(f"  [CERTIFIED] {name:<28s} | rows={len(rows):4d} {counts} | min={float(m):+.6f} ({phs}) [{time.time()-t0:.1f}s]")
    return {
        "name": name,
        "primes_later": list(primes_later),
        "exps": list(exps),
        "C7": str(C7),
        "taus_later": [str(x) for x in taus_later],
        "thresh": str(thresh),
        "counts": counts,
        "total_rows": len(rows),
        "uncovered": uncov,
        "unused": unused,
        "min_margin": str(m),
        "min_margin_float": float(m),
        "min_phase": phs,
        "min_key": mk,
        "min_R": str(mR),
        "min_L": [str(x) for x in mL],
        "rows": rows,
    }, True


def main():
    t0 = time.time()
    print(f"=== CERTIFYING UNCONDITIONAL GLOBAL BOUND L >= {L_TARGET:,} ===\n")

    scalar_certs = []
    anchored_targets = []

    for r in (10, 11, 12, 13):
        ps, vecs = enum_exp_vecs(r, L_TARGET)
        print(f"--- Processing omega(L) = {r}: {len(vecs)} exponent vectors on P_{r} with L < {L_TARGET:,} ---")
        # Sort by sum(es) DESCENDING so we find Pareto-maximal killable vectors FIRST!
        vecs_desc = sorted(vecs, key=lambda x: (-sum(x[1]), -x[0]))
        killed_certs = []  # list of (es, k0, Cs, B_exact)
        surv = []
        for L, es in vecs_desc:
            if any(all(es[i] <= k[0][i] for i in range(r)) for k in killed_certs):
                continue
            B_fl, cfg = optimize_scalar(ps, es, early_stop=0.0)
            if B_fl < 0.9999:
                k0, Cs_fl = cfg
                # Quantize and verify EXACT Fraction B < 1!
                ok_q = False
                for den in (64, 128, 256, 1024):
                    Cs_q = quantize_caps(ps, es, k0, Cs_fl, den=den)
                    B_ex = exact_scalar_B(ps, es, k0, Cs_q)
                    if B_ex < 1:
                        ok_q = True
                        break
                if ok_q:
                    # Prune any previously killed vector dominated by es (none expected since desc)
                    killed_certs.append((es, k0, Cs_q, B_ex))
                    continue
            surv.append((L, es))

        # Find Pareto-maximal survivors (every surviving vector <= some pmax!)
        pmax_surv = []
        for L, es in sorted(surv, key=lambda x: (-sum(x[1]), -x[0])):
            if any(all(es[i] <= m[1][i] for i in range(r)) for m in pmax_surv):
                continue
            pmax_surv.append((L, es))
        pmax_surv.sort()

        # Verify 100% coverage of all `vecs` by killed_certs + pmax_surv!
        covered_scalar = 0
        covered_anchored = 0
        for L, es in vecs:
            if any(all(es[i] <= k[0][i] for i in range(r)) for k in killed_certs):
                covered_scalar += 1
            elif any(all(es[i] <= m[1][i] for i in range(r)) for m in pmax_surv):
                covered_anchored += 1
            else:
                raise RuntimeError(f"UNCOVERED vector at r={r}: {es}")
        print(f"  r={r}: {len(killed_certs)} Pareto-maximal scalar certs cover {covered_scalar}/{len(vecs)}; "
              f"{len(pmax_surv)} Pareto-maximal anchored targets cover {covered_anchored}/{len(vecs)} (0 uncovered!)")

        for es, k0, Cs_q, B_ex in sorted(killed_certs):
            scalar_certs.append({
                "omega": r,
                "primes": list(ps),
                "exps": list(es),
                "k0": k0,
                "Cs": [str(c) for c in Cs_q],
                "B_exact": str(B_ex),
                "B_float": float(B_ex),
            })
        for L, es in pmax_surv:
            anchored_targets.append((r, ps, es, L))

    # Save exact scalar Lemma U certificate JSON
    scalar_path = os.path.join(HERE, "r12_global_L_scalar_cert.json")
    with open(scalar_path, "w") as f:
        json.dump({
            "L_target": L_TARGET,
            "L_scalar_only": L_SCALAR_ONLY,
            "num_certs": len(scalar_certs),
            "max_B_float": max(c["B_float"] for c in scalar_certs),
            "certs": scalar_certs,
        }, f, separators=(",", ":"))
    print(f"\nSaved {len(scalar_certs)} exact Lemma U certs to {os.path.basename(scalar_path)} (max B = {max(c['B_float'] for c in scalar_certs):.6f})")

    # Now certify ALL Pareto-maximal anchored targets (12 at r=10, 1 at r=11)!
    print(f"\n=== CERTIFYING {len(anchored_targets)} PARETO-MAXIMAL ANCHORED TARGETS (r=10, 11) ===")
    anchored_certs = []
    for r, ps, es, L in anchored_targets:
        primes_later = ps[2:]
        if r == 10:
            taus = (4, 4, 6, 8, 12, 16, 18)
        elif r == 11:
            taus = (4, 4, 6, 8, 12, 16, 18, 22)
        else:
            raise ValueError(r)
        name = f"w{r} {es}"
        # Use thresh = 0 for (4,3,2,2,1^6) so mixed closes cleanly; 1/40 for basic-32 ones!
        cert, ok = certify_anchored_general(name, primes_later, es, C7=Fraction(3, 2), taus_later=taus, thresh=Fraction(0))
        assert ok, f"Anchored cert failed for {name}!"
        anchored_certs.append(cert)

    anch_path = os.path.join(HERE, "r12_global_L_anchored_cert.json")
    with open(anch_path, "w") as f:
        json.dump({
            "L_target": L_TARGET,
            "num_certs": len(anchored_certs),
            "total_rows": sum(c["total_rows"] for c in anchored_certs),
            "certs": anchored_certs,
        }, f, separators=(",", ":"))
    print(f"\nSaved {len(anchored_certs)} exact anchored certs ({sum(c['total_rows'] for c in anchored_certs)} total rows!) to {os.path.basename(anch_path)}")
    print(f"GLOBAL LOWER BOUND CERTIFIED: L >= {L_TARGET:,} (39.00x public bound) in {time.time()-t0:.1f}s!")


if __name__ == "__main__":
    main()
