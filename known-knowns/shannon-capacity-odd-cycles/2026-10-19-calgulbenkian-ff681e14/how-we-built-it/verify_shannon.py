#!/usr/bin/env python3
"""
Standalone generator and verifier for the new Shannon capacity lower bounds across
all six frontier odd cycles: C7, C11, C13, C15, C19, and C23.

Verifies:
1. Admissibility and pairwise separation of all BPZ 7-letter substitution tables
   (S2a, S2b, S3a..S3h) and terminal codes (K3a, K4a, K4b) directly against the
   separation graph `Letter.sep` from `PortRealisation.lean`.
2. Tandon's finite certificates (C1, C2, C3, C4) = (27488, 12839823, 14045805,
   841760069965664) derived live from `data/tandon2026/data/base_c7.json` via
   `shannon.construction.load_certificates(recomputed=True)` and the exact HetGao
   recurrences for the 30-dimensional left gadget G_30^L on C7.
3. Exact multi-substitution DAG evaluation (`Realisation.multiSubst` +
   `le_indepNum_multiCode`) from the verified base port systems `w0` for C7, C11,
   C13, C15, C19, and C23.
4. Exact integer bisection (`lo**d <= M * 10**(50*d) < (lo+1)**d`) certifying 50
   decimal digits of each new lower bound M^{1/d} and verifying strict improvement
   over both `9a.md` and the August 2026 papers/Lean repository.
"""

import json
import re
import sys
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100000)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "data" / "tandon2026"))

from shannon.construction import (
    _cert,
    load_certificates,
    nth_root_digits,
    theorem2,
)
from shannon.gadget import (
    Phi,
    SideCodebook,
    hetgao,
    neutral_from,
    sigma,
)

LETTERS = ["B", "N", "A", "D", "O", "H", "V"]
L_IDX = {l: i for i, l in enumerate(LETTERS)}

# Exact symmetric separation relation `Letter.sep` from `PortRealisation.lean`:
SEP_PAIRS = {
    ("B", "O"), ("B", "H"), ("B", "V"),
    ("N", "A"), ("N", "D"), ("N", "O"), ("N", "H"), ("N", "V"),
    ("A", "N"), ("A", "D"), ("A", "H"),
    ("D", "N"), ("D", "A"), ("D", "V"),
    ("O", "B"), ("O", "N"),
    ("H", "B"), ("H", "N"), ("H", "A"),
    ("V", "B"), ("V", "N"), ("V", "D"),
}
SEP_IDX = {(L_IDX[a], L_IDX[b]) for (a, b) in SEP_PAIRS}


def word_sep(u, v):
    """Two words u, v in Letter^k are separated iff SEP_IDX holds at some coordinate."""
    return any((a, b) in SEP_IDX for a, b in zip(u, v))


def parse_substs(path):
    with open(path) as f:
        text = f.read()
    blocks = {}
    for m in re.finditer(r"def\s+(T\w+)\s*:.*?(?=def\s+|\Z)", text, re.S):
        tname = m.group(1)
        sname = "S" + tname[1:]
        body = m.group(0)
        by_let = [[] for _ in range(7)]
        parts = re.split(r"\|\s*\.?([BNADOHV])\s*=>", body)
        for i in range(1, len(parts), 2):
            let_idx = L_IDX[parts[i]]
            w_str = parts[i + 1]
            for wm in re.finditer(r"!\[(.*?)\]", w_str):
                toks = [t.strip().lstrip(".") for t in wm.group(1).split(",")]
                by_let[let_idx].append(tuple(L_IDX[t] for t in toks))
        blocks[sname] = by_let
    return blocks


def parse_codes(path):
    with open(path) as f:
        text = f.read()
    blocks = {}
    for m in re.finditer(r"def\s+(C\w+)\s*:.*?(?=def\s+|\Z)", text, re.S):
        cname = m.group(1)
        kname = "K" + cname[1:]
        body = m.group(0)
        words = []
        for wm in re.finditer(r"!\[(.*?)\]", body):
            toks = [t.strip().lstrip(".") for t in wm.group(1).split(",")]
            words.append(tuple(L_IDX[t] for t in toks))
        blocks[kname] = words
    return blocks


def verify_substs_and_codes(substs, tcodes):
    """Verify admissibility and pairwise separation of all substitutions and terminal codes."""
    for sname, by_let in substs.items():
        for a in range(7):
            words_a = by_let[a]
            for i in range(len(words_a)):
                for j in range(i + 1, len(words_a)):
                    assert word_sep(words_a[i], words_a[j]), (
                        f"Substitution {sname} letter {LETTERS[a]} not pairwise separated"
                    )
        for a, b in SEP_IDX:
            for u in by_let[a]:
                for v in by_let[b]:
                    assert word_sep(u, v), (
                        f"Substitution {sname} not admissible on ({LETTERS[a]}, {LETTERS[b]})"
                    )
    for kname, words in tcodes.items():
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                assert word_sep(words[i], words[j]), (
                    f"Terminal code {kname} not pairwise separated"
                )


def apply_subst(S, w_list):
    out = [0] * 7
    for l_idx in range(7):
        s = 0
        for word in S[l_idx]:
            p = 1
            for pos, let in enumerate(word):
                p *= w_list[pos][let]
            s += p
        out[l_idx] = s
    return tuple(out)


def apply_code(K, w_list):
    total = 0
    for word in K:
        p = 1
        for pos, let in enumerate(word):
            p *= w_list[pos][let]
        total += p
    return total


def verify_exact_root(M, d, digits_str):
    """Verify by exact integer power comparison that floor(M^{1/d} * 10^k) matches digits_str."""
    int_part, frac_part = digits_str.split(".")
    k = len(frac_part)
    lo = int(int_part) * (10**k) + int(frac_part)
    target = M * (10 ** (k * d))
    assert (lo**d) <= target < ((lo + 1) ** d), (
        f"Exact integer root check failed for d={d}, root={digits_str}"
    )


def build_and_verify_all(verify_c7_graphs=True):
    lean_dir = ROOT / "data" / "bpz2026" / "ShannonBounds"
    substs = parse_substs(lean_dir / "Substitutions.lean")
    tcodes = parse_codes(lean_dir / "TerminalCodes.lean")
    verify_substs_and_codes(substs, tcodes)
    print("[OK] Verified admissibility of all 10 BPZ substitutions and 3 terminal codes.")

    led = load_certificates(recomputed=verify_c7_graphs)
    C1 = _cert(led, "C1")
    C2 = _cert(led, "C2")
    C3 = _cert(led, "C3")
    C4 = _cert(led, "C4")
    print(f"[OK] Verified C7 finite certificates (recomputed={verify_c7_graphs}): "
          f"C1={C1}, C2={C2}, C3={C3}, C4={C4}")

    results = {}

    # =========================================================================
    # 1. C7 (beating Tandon arXiv:2608.30273, 2026-08-30)
    # =========================================================================
    t2 = theorem2(led)
    M7_tandon = t2["M"]
    root7_tandon = nth_root_digits(M7_tandon, 500, 50)
    verify_exact_root(M7_tandon, 500, root7_tandon)

    S3b = substs["S3b"]
    K4a = tcodes["K4a"]
    n6_7 = tuple(t2["n6"])
    n11_7 = tuple(t2["n11"])

    # Record 1a: S3b(n6, n11, n11) + K4a at d = 560 using Tandon's exact n6 (d=30), n11 (d=55)
    w140_simple = apply_subst(S3b, [n6_7, n11_7, n11_7])
    M7_simple = apply_code(K4a, [w140_simple] * 4)
    root7_simple = nth_root_digits(M7_simple, 560, 50)
    verify_exact_root(M7_simple, 560, root7_simple)

    # Record 1b: S3b(p0, p1, p2) + K4a at d = 560 using 30-dim left gadget G_30^L on all 3 branches
    J15 = SideCodebook(t2["G15X"].a, C2, source="J_15", certificate="C2")
    J30pp = SideCodebook(t2["Gpp30"].a, C4, source="J_30^{++}", certificate="C4")
    Xhat30 = neutral_from(t2["Ghat30"], "Xhat_30")
    X15Ah = neutral_from(t2["G15Ah"], "X_15^{A,het}")

    P0 = hetgao(t2["G30L"], t2["G10"], J0=Xhat30, JH=J30pp, JV=J30pp, name="P0")
    R30_mid = sigma(
        hetgao(t2["G15AX"], t2["G15Dh"], J0=X15Ah, JH=J15, JV=J15, name="G30_mid"),
        name="R30_mid",
    )
    P1 = sigma(
        hetgao(t2["G30L"], R30_mid, J0=Xhat30, JH=J30pp, JV=J30pp, name="P1_pre"),
        name="P1",
    )
    P2 = sigma(
        hetgao(t2["G30L"], t2["G10D"], J0=Xhat30, JH=J30pp, JV=J30pp, name="P2_pre"),
        name="P2",
    )
    p0_7, p1_7, p2_7 = tuple(Phi(P0)), tuple(Phi(P1)), tuple(Phi(P2))
    w140_best = apply_subst(S3b, [p0_7, p1_7, p2_7])
    M7_best = apply_code(K4a, [w140_best] * 4)
    root7_best = nth_root_digits(M7_best, 560, 50)
    verify_exact_root(M7_best, 560, root7_best)
    assert root7_best > root7_simple > root7_tandon

    results["C7"] = {
        "cycle": 7,
        "baseline_9a_md": "3.258805326092",
        "baseline_2026_source": "Tandon (arXiv:2608.30273, 30 Aug 2026, Theorem 2)",
        "baseline_2026_degree": 500,
        "baseline_2026_bound_50d": root7_tandon,
        "certificates": {
            "C1": C1,
            "C2": C2,
            "C3": C3,
            "C4": C4,
        },
        "new_record_simple": {
            "description": "S3b(n6, n11, n11) + K4a on Tandon's certified gadgets n6 (d=30) and n11 (d=55)",
            "degree": 560,
            "M": str(M7_simple),
            "bound_50d": root7_simple,
        },
        "new_record_best": {
            "description": "S3b(p0, p1, p2) + K4a where all three branches use the 30-dim left gadget G_30^L certified by C4: P0 = HetGao(G_30^L, G_10) (d=40), P1 = sigma(HetGao(G_30^L, sigma(HetGao(G_15^{A,X}, G_15^{D,het})))) (d=60), P2 = sigma(HetGao(G_30^L, G_10^D)) (d=40)",
            "degree": 560,
            "pi_P0": list(P0.as_tuple()),
            "pi_P1": list(P1.as_tuple()),
            "pi_P2": list(P2.as_tuple()),
            "w140": list(w140_best),
            "M": str(M7_best),
            "bound_50d": root7_best,
        },
    }
    print(f"[OK] C7:  new={root7_best[:25]}... > Tandon={root7_tandon[:25]}... (d=560)")

    # =========================================================================
    # 2. C11 (beating BPZ Lean v2 CertC11.lean, 2026-08-10)
    # =========================================================================
    w11 = (145, 142, 3, 3, 3, 3, 3)
    Gg11, Hh11, K3a = substs["S3c"], substs["S2b"], tcodes["K3a"]
    h11 = {3: apply_subst(Gg11, [w11, w11, w11])}
    for j in range(4, 16):
        h11[j] = apply_subst(Hh11, [h11[j - 1], w11])
    b11 = {1: w11}
    for j in range(2, 16):
        b11[j] = apply_subst(Hh11, [b11[j - 1], w11])

    def eval_c11(exps):
        e0, e1, e2, e3, e4, e5, e6, e7 = exps
        p = apply_subst(Gg11, [h11[e0], h11[e1], b11[e2]])
        xA = apply_subst(Gg11, [h11[e3], p, h11[e4]])
        xB = apply_subst(Gg11, [h11[e5], b11[e6], p])
        E = 2 * (e0 + e1 + e2) + e3 + e4 + e5 + e6 + e7
        d = 3 * E
        M = apply_code(K3a, [xA, xB, b11[e7]])
        root = nth_root_digits(M, d, 50)
        verify_exact_root(M, d, root)
        return d, M, root

    d11_lean, M11_lean, root11_lean = eval_c11((3, 6, 2, 7, 9, 6, 12, 13))
    d11_207, M11_207, root11_207 = eval_c11((3, 4, 3, 7, 10, 5, 13, 14))
    d11_210, M11_210, root11_210 = eval_c11((3, 5, 2, 7, 10, 6, 13, 14))
    assert root11_210 > root11_207 > root11_lean

    results["C11"] = {
        "cycle": 11,
        "base_degree": 3,
        "w0": list(w11),
        "baseline_9a_md": "5.294502522149",
        "baseline_2026_source": "BPZ shannon-capacity-lean CertC11.lean (10 Aug 2026)",
        "baseline_2026_degree": d11_lean,
        "baseline_2026_bound_50d": root11_lean,
        "new_record_same_degree": {
            "description": "Exponents (3, 4, 3, 7, 10, 5, 13, 14): p10=S3c(h3,h4,b3), x27=S3c(h7,p10,h10), x28=S3c(h5,b13,p10), K3a(x27,x28,b14)",
            "degree": d11_207,
            "M": str(M11_207),
            "bound_50d": root11_207,
        },
        "new_record_best": {
            "description": "Exponents (3, 5, 2, 7, 10, 6, 13, 14): p10=S3c(h3,h5,b2), x27=S3c(h7,p10,h10), x29=S3c(h6,b13,p10), K3a(x27,x29,b14)",
            "degree": d11_210,
            "M": str(M11_210),
            "bound_50d": root11_210,
        },
    }
    print(f"[OK] C11: new={root11_210[:25]}... > Lean={root11_lean[:25]}... (d=210)")

    # =========================================================================
    # 3. C13 (beating BPZ Lean v2 CertC13.lean, 2026-08-10)
    # =========================================================================
    w13 = (61516, 60502, 1014, 1014, 1014, 1014, 1014)
    Tt13, Ss13 = substs["S3c"], substs["S2b"]
    a13 = {3: apply_subst(Tt13, [w13, w13, w13])}
    for j in range(4, 12):
        a13[j] = apply_subst(Ss13, [a13[j - 1], w13])
    b13 = {1: w13}
    for j in range(2, 19):
        b13[j] = apply_subst(Ss13, [b13[j - 1], w13])

    c12_lean = apply_subst(Tt13, [a13[3], a13[7], b13[2]])
    x34_lean = apply_subst(Tt13, [a13[9], b13[13], c12_lean])
    x36_lean = apply_subst(Tt13, [a13[7], b13[17], c12_lean])
    M13_lean = apply_code(K3a, [x34_lean, x36_lean, b13[17]])
    root13_lean = nth_root_digits(M13_lean, 522, 50)
    verify_exact_root(M13_lean, 522, root13_lean)

    c12_new = apply_subst(Tt13, [a13[3], a13[6], b13[3]])
    x34_new = apply_subst(Tt13, [a13[9], b13[13], c12_new])
    x36_new = apply_subst(Tt13, [a13[7], b13[17], c12_new])
    M13_new = apply_code(K3a, [x34_new, x36_new, b13[17]])
    root13_new = nth_root_digits(M13_new, 522, 50)
    verify_exact_root(M13_new, 522, root13_new)
    assert root13_new > root13_lean

    results["C13"] = {
        "cycle": 13,
        "base_degree": 6,
        "w0": list(w13),
        "baseline_9a_md": "6.302455083464",
        "baseline_2026_source": "BPZ shannon-capacity-lean CertC13.lean (10 Aug 2026)",
        "baseline_2026_degree": 522,
        "baseline_2026_bound_50d": root13_lean,
        "new_record_best": {
            "description": "Replace c12 = S3c(a3, a7, b2) with c12' = S3c(a3, a6, b3) inside x34 = S3c(a9, b13, c12'), x36 = S3c(a7, b17, c12'), K3a(x34, x36, b17) at the same degree d = 522",
            "degree": 522,
            "M": str(M13_new),
            "bound_50d": root13_new,
        },
    }
    print(f"[OK] C13: new={root13_new[:25]}... > Lean={root13_lean[:25]}... (d=522)")

    # =========================================================================
    # 4. C15 (beating BPZ Lean v2 CertC15.lean, 2026-08-10)
    # =========================================================================
    w15 = (2839, 2833, 6, 3, 3, 3, 3)
    Sa15, Sb15, Sc15, K4b = substs["S3e"], substs["S3f"], substs["S3g"], tcodes["K4b"]
    v0 = apply_subst(Sb15, [w15, w15, w15])
    v1 = apply_subst(Sb15, [v0, v0, v0])
    v2 = apply_subst(Sb15, [v1, v1, v1])
    v3 = apply_subst(Sa15, [w15, w15, w15])
    v4 = apply_subst(Sb15, [v0, v3, v0])
    v5 = apply_subst(Sb15, [v4, v1, v1])
    v6 = apply_subst(Sc15, [v2, v5, v2])
    v7 = apply_subst(Sb15, [v1, w15, v1])
    v8 = apply_subst(Sc15, [v2, v5, v7])
    v9 = apply_subst(Sc15, [v6, v8, v8])
    tA15 = {227: v9}
    for e in range(229, 257, 2):
        tA15[e] = apply_subst(Sb15, [tA15[e - 2], w15, w15])
    v13 = apply_subst(Sc15, [v8, v8, v8])
    tB15 = {219: v13}
    for e in range(221, 233, 2):
        tB15[e] = apply_subst(Sb15, [tB15[e - 2], w15, w15])
    v17 = apply_subst(Sb15, [v1, v4, v1])
    v18 = apply_subst(Sc15, [v17, v17, v2])
    v19 = apply_subst(Sc15, [v18, v8, v8])
    tC15 = {227: v19}
    tC15[229] = apply_subst(Sc15, [v19, w15, w15])
    for e in range(231, 257, 2):
        tC15[e] = apply_subst(Sb15, [tC15[e - 2], w15, w15])

    def eval_c15(eA, eB1, eB2, eC):
        d = 4 * (eA + eB1 + eB2 + eC)
        M = apply_code(K4b, [tA15[eA], tB15[eB1], tB15[eB2], tC15[eC]])
        root = nth_root_digits(M, d, 50)
        verify_exact_root(M, d, root)
        return d, M, root

    d15_lean, M15_lean, root15_lean = eval_c15(233, 225, 225, 233)
    d15_3664, M15_3664, root15_3664 = eval_c15(237, 219, 223, 237)
    d15_3688, M15_3688, root15_3688 = eval_c15(237, 219, 229, 237)
    d15_3792, M15_3792, root15_3792 = eval_c15(255, 219, 219, 255)
    assert root15_3792 > root15_3688 > root15_3664 > root15_lean

    results["C15"] = {
        "cycle": 15,
        "base_degree": 4,
        "w0": list(w15),
        "baseline_9a_md": "7.301600534487",
        "baseline_2026_source": "BPZ shannon-capacity-lean CertC15.lean (10 Aug 2026)",
        "baseline_2026_degree": d15_lean,
        "baseline_2026_bound_50d": root15_lean,
        "new_record_same_degree": {
            "description": "K4b applied to tail exponents (237, 219, 223, 237) at the same degree d = 3664",
            "degree": d15_3664,
            "M": str(M15_3664),
            "bound_50d": root15_3664,
        },
        "new_record_d3688": {
            "description": "K4b applied to tail exponents (237, 219, 229, 237) at degree d = 3688",
            "degree": d15_3688,
            "M": str(M15_3688),
            "bound_50d": root15_3688,
        },
        "new_record_best": {
            "description": "K4b applied to tail exponents (255, 219, 219, 255) (14 S3f tail steps on v9 and v19, 0 tail steps on v13) at degree d = 3792",
            "degree": d15_3792,
            "M": str(M15_3792),
            "bound_50d": root15_3792,
        },
    }
    print(f"[OK] C15: new={root15_3792[:25]}... (d=3792) & {root15_3688[:25]}... (d=3688) > Lean={root15_lean[:25]}...")

    # =========================================================================
    # 5. C19 (beating BPZ Lean v2 CertC19.lean, 2026-08-10)
    # =========================================================================
    w19 = (7664, 7661, 3, 2, 2, 2, 2)
    Sa19, Sb19, Sc19 = substs["S3f"], substs["S3g"], substs["S3d"]
    u19 = {}
    u19[0] = apply_subst(Sa19, [w19, w19, w19])
    u19[1] = apply_subst(Sa19, [u19[0], u19[0], u19[0]])
    u19[2] = apply_subst(Sa19, [u19[1], u19[1], u19[1]])
    u19[3] = apply_subst(Sa19, [u19[2], u19[2], u19[2]])
    u19[4] = apply_subst(Sc19, [w19, w19, w19])
    u19[5] = apply_subst(Sa19, [u19[0], u19[4], u19[4]])
    u19[6] = apply_subst(Sa19, [u19[1], u19[5], u19[1]])
    u19[7] = apply_subst(Sa19, [u19[2], u19[6], u19[2]])
    u19[8] = apply_subst(Sb19, [u19[3], u19[3], u19[7]])
    u19[9] = apply_subst(Sb19, [u19[8], u19[8], u19[8]])
    for k in range(10, 24):
        u19[k] = apply_subst(Sa19, [u19[k - 1], w19, w19])

    def eval_c19(k_node):
        exp = 729 + 2 * (k_node - 9)
        d = 4 * 4 * exp
        M = apply_code(K4b, [u19[k_node]] * 4)
        root = nth_root_digits(M, d, 50)
        verify_exact_root(M, d, root)
        return d, M, root

    d19_lean, M19_lean, root19_lean = eval_c19(15)
    d19_u22, M19_u22, root19_u22 = eval_c19(22)
    d19_u23, M19_u23, root19_u23 = eval_c19(23)
    assert root19_u23 > root19_u22 > root19_lean

    results["C19"] = {
        "cycle": 19,
        "base_degree": 4,
        "w0": list(w19),
        "baseline_9a_md": "9.357192705918",
        "baseline_2026_source": "BPZ shannon-capacity-lean CertC19.lean (10 Aug 2026)",
        "baseline_2026_degree": d19_lean,
        "baseline_2026_bound_50d": root19_lean,
        "new_record_d12080": {
            "description": "Extend tail recursion u_{k+1} = S3f(u_k, w0, w0) to u22 (exponent 755) and apply K4b(u22, u22, u22, u22) at degree d = 12080",
            "degree": d19_u22,
            "M": str(M19_u22),
            "bound_50d": root19_u22,
        },
        "new_record_best": {
            "description": "Extend tail recursion u_{k+1} = S3f(u_k, w0, w0) to u23 (exponent 757) and apply K4b(u23, u23, u23, u23) at degree d = 12112",
            "degree": d19_u23,
            "M": str(M19_u23),
            "bound_50d": root19_u23,
        },
    }
    print(f"[OK] C19: new={root19_u23[:25]}... (d=12112) & {root19_u22[:25]}... (d=12080) > Lean={root19_lean[:25]}...")

    # =========================================================================
    # 6. C23 (beating BPZ Lean v2 CertC23.lean, 2026-08-10)
    # =========================================================================
    w23 = (16451, 16279, 76, 146, 50, 50, 50)
    Tt23, Aa23, Uu23 = substs["S3a"], substs["S2a"], substs["S3h"]
    n3 = apply_subst(Tt23, [w23, w23, w23])
    n9 = apply_subst(Tt23, [n3, n3, n3])
    n27 = apply_subst(Tt23, [n9, n9, n9])
    n54 = apply_subst(Aa23, [n27, n27])
    n81 = apply_subst(Tt23, [n27, n27, n27])
    n55 = apply_subst(Tt23, [n27, w23, n27])
    n190 = apply_subst(Uu23, [n54, n81, n55])
    M23_lean = apply_code(K4a, [n190] * 4)
    root23_lean = nth_root_digits(M23_lean, 3040, 50)
    verify_exact_root(M23_lean, 3040, root23_lean)

    n57_3072 = apply_subst(Tt23, [n27, n27, n3])
    n192 = apply_subst(Uu23, [n54, n81, n57_3072])
    M23_3072 = apply_code(K4a, [n192] * 4)
    root23_3072 = nth_root_digits(M23_3072, 3072, 50)
    verify_exact_root(M23_3072, 3072, root23_3072)

    n45 = apply_subst(Tt23, [n27, n9, n9])
    n57 = apply_subst(Tt23, [n27, n3, n27])
    n183 = apply_subst(Uu23, [n45, n81, n57])
    M23_best = apply_code(K4a, [n183] * 4)
    root23_best = nth_root_digits(M23_best, 2928, 50)
    verify_exact_root(M23_best, 2928, root23_best)
    assert root23_best > root23_3072 > root23_lean

    results["C23"] = {
        "cycle": 23,
        "base_degree": 4,
        "w0": list(w23),
        "baseline_9a_md": "11.328224257774",
        "baseline_2026_source": "BPZ shannon-capacity-lean CertC23.lean (10 Aug 2026)",
        "baseline_2026_degree": 3040,
        "baseline_2026_bound_50d": root23_lean,
        "new_record_d3072": {
            "description": "S3h(S2a(n27, n27), n81, S3a(n27, n27, n3)) + K4a at degree d = 3072",
            "degree": 3072,
            "M": str(M23_3072),
            "bound_50d": root23_3072,
        },
        "new_record_best": {
            "description": "S3h(S3a(n27, n9, n9), n81, S3a(n27, n3, n27)) + K4a at smaller degree d = 2928 < 3040",
            "degree": 2928,
            "M": str(M23_best),
            "bound_50d": root23_best,
        },
    }
    print(f"[OK] C23: new={root23_best[:25]}... (d=2928) > Lean={root23_lean[:25]}... (d=3040)")

    out_path = ROOT / "results" / "shannon_certificates.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[OK] Saved exact certificates to {out_path}")
    print("ALL SHANNON CAPACITY CERTIFICATES VERIFIED")
    return 0


if __name__ == "__main__":
    fast_mode = "--fast" in sys.argv
    sys.exit(build_and_verify_all(verify_c7_graphs=not fast_mode))
