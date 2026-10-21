#!/usr/bin/env python3
"""Standard-library checker for a recursive independent-set construction in a strong
power of an odd cycle (Buys-Polak-Zuiddam seven-family framework, Gao gadgets, Tandon's
heterogeneous refinement).

Usage:  python3 shannon_check.py OBJECT_DIR TABLE_RECORD_DIR

OBJECT_DIR holds rules.json (separation relation, substitution tables, terminal codes),
schedule.json (the recursion DAG) and argon_shannon_certificates.json (the contributor's
claimed integer).  TABLE_RECORD_DIR holds records.json (the values compared against).

What it does, all in exact integer arithmetic:
  1. Checks the label-separation relation against the table printed in the papers.
  2. Checks Definition 6 (admissibility: conditions (i) and (ii)) for every substitution
     table, and the pairwise-separation property for every terminal code, that the
     schedule uses.
  3. Recomputes the cardinality vectors along the schedule and the final integer M, and
     the degree d.
  4. Compares M with the contributor's claimed M.
  5. Compares M^(1/d) with every record in records.json using exact integer arithmetic
     (certified integer floors of 10^50 * root, and, when affordable, the direct
     cross-multiplied powers).
Exit status 0 only if every check passes.
"""
import sys, os, json, time
from decimal import Decimal, getcontext

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

LETTERS = "BNADOHV"
# Definition 4 of arXiv:2608.30273 (identical to the BPZ Letter.sep relation).
PAPER_SEP = {"B": "OHV", "N": "ADOHV", "A": "NDH", "D": "NAV", "O": "BN", "H": "BNA", "V": "BND"}
DIGITS = 50

FAILS = []


def check(cond, msg):
    if cond:
        print("  [ok]   " + msg)
    else:
        print("  [FAIL] " + msg)
        FAILS.append(msg)
    return cond


def prod(xs):
    r = 1
    for x in xs:
        r *= x
    return r


# ----------------------------------------------------------------------------- rules
def load_rules(path):
    R = json.load(open(path))
    sep = set((a, b) for a, b in R["sep"])
    return R, sep


def words_sep(sep, x, y):
    return any((a, b) in sep for a, b in zip(x, y))


def check_relation(sep):
    paper = set((a, b) for a in PAPER_SEP for b in PAPER_SEP[a])
    check(sep == paper, "label separation relation equals Definition 4 of the paper (%d ordered pairs)" % len(paper))
    check(all((b, a) in sep for a, b in sep), "separation relation is symmetric")


def check_table(name, tab, sep):
    """Definition 6: (i) distinct tuples of one T_lambda are separated in some coordinate;
    (ii) lambda separated from mu implies every tuple of T_lambda is separated from every
    tuple of T_mu in some coordinate."""
    q = tab["arity"]
    words = tab["words"]
    n_words = 0
    bad = 0
    for l in LETTERS:
        ws = [tuple(w) for w in words[l]]
        n_words += len(ws)
        if len(set(ws)) != len(ws):
            bad += 1
        for w in ws:
            if len(w) != q or any(c not in LETTERS for c in w):
                bad += 1
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                if not words_sep(sep, ws[i], ws[j]):
                    bad += 1
    for a in LETTERS:
        for b in LETTERS:
            if (a, b) in sep:
                for x in words[a]:
                    for y in words[b]:
                        if not words_sep(sep, x, y):
                            bad += 1
    return check(bad == 0, "table %s (arity %d, %d words): Definition 6 (i) and (ii), %d violations" % (name, q, n_words, bad)), n_words


def check_code(name, code, sep):
    q = code["arity"]
    ws = [tuple(w) for w in code["words"]]
    bad = 0
    if len(set(ws)) != len(ws):
        bad += 1
    for w in ws:
        if len(w) != q or any(c not in LETTERS for c in w):
            bad += 1
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            if not words_sep(sep, ws[i], ws[j]):
                bad += 1
    return check(bad == 0, "terminal code %s (arity %d, %d words): pairwise separated, %d violations" % (name, q, len(ws), bad))


def apply_rule(R, name, vecs):
    tab = R["tables"][name]
    assert tab["arity"] == len(vecs), name
    out = []
    for l in LETTERS:
        s = 0
        for w in tab["words"][l]:
            p = 1
            for i, c in enumerate(w):
                p *= vecs[i][LETTERS.index(c)]
            s += p
        out.append(s)
    return tuple(out)


def apply_code(R, name, vecs):
    code = R["codes"][name]
    assert code["arity"] == len(vecs), name
    s = 0
    for w in code["words"]:
        p = 1
        for i, c in enumerate(w):
            p *= vecs[i][LETTERS.index(c)]
        s += p
    return s


# ----------------------------------------------------------------------------- roots
def floor_root_scaled(M, d, k=DIGITS):
    """Return lo with lo**d <= M*10**(k*d) < (lo+1)**d, i.e. lo = floor(10**k * M**(1/d)),
    certified by two exact integer powers."""
    T = M * 10 ** (k * d)
    getcontext().prec = k + 40
    approx = (Decimal(M).ln() / Decimal(d)).exp()
    lo = int(approx * (Decimal(10) ** k))
    while lo ** d > T:
        lo -= 1
    while (lo + 1) ** d <= T:
        lo += 1
    assert lo ** d <= T < (lo + 1) ** d
    return lo


def fmt(lo, k=DIGITS):
    s = str(lo).rjust(k + 1, "0")
    return s[:-k] + "." + s[-k:]


def decimal_parts(s):
    ip, fp = s.split(".")
    return int(ip + fp), len(fp)


# ----------------------------------------------------------------------------- Tandon calculus
def prof(a, t, s, o, h, v):
    assert o + h + v == s, "profile: o+h+v != s"
    assert 0 <= t <= a and min(a, t, s, o, h, v) >= 0, "profile: range"
    return (a, t, s, o, h, v)


def sigma(p):
    a, t, s, o, h, v = p
    return prof(a, t, s, o, v, h)


def gao(L, Rr):
    a1, t1, s1, o1, h1, v1 = L
    a2, t2, s2, o2, h2, v2 = Rr
    return prof((a1 - t1) * (a2 - t2) + t1 * s2 + s1 * t2, t1 * o2 + o1 * t2, s1 * s2,
                o1 * o2 + (h1 + v1) * (h2 + v2), h1 * o2 + o1 * v2, v1 * o2 + o1 * h2)


def hetgao(L, Rr, J0, JH, JV):
    """Theorem 1, eqs (38)-(39).  J0 = (j0,o0,h0,v0); JH = (jH,qH); JV = (jV,qV)."""
    aL, tL, sL, oL, hL, vL = L
    aR, tR, sR, oR, hR, vR = Rr
    j0, o0, h0, v0 = J0
    jH, qH = JH
    jV, qV = JV
    assert o0 + h0 + v0 == j0 and 0 <= qH <= jH and 0 <= qV <= jV
    return prof((aL - tL) * (aR - tR) + tL * sR + sL * tR, tL * oR + oL * tR,
                j0 * oR + jH * hR + jV * vR, o0 * oR + qH * hR + qV * vR,
                h0 * oR + (jV - qV) * vR, v0 * oR + (jH - qH) * hR)


def phi(p):
    a, t, s, o, h, v = p
    return (a - t, o, v, h, t, t, t)


def run_gadgets(sched, certs):
    G = {}
    dim = {}
    for name, spec in sched["gadgets"].items():
        G[name] = prof(*spec["profile"])
        dim[name] = spec["dim"]
    for st in sched["steps"]:
        op, name = st["op"], st["name"]
        if op == "sigma":
            G[name] = sigma(G[st["of"]])
            dim[name] = dim[st["of"]]
        elif op == "gao":
            G[name] = gao(G[st["left"]], G[st["right"]])
            dim[name] = dim[st["left"]] + dim[st["right"]]
        elif op == "hetgao":
            def cb(spec):
                kind = spec["kind"]
                if kind == "neutral_of":      # (j0,o0,h0,v0) of an auxiliary set carried by gadget
                    s, o, h, v = G[spec["gadget"]][2:]
                    return (s, o, h, v)
                if kind == "own_of":          # J = X_G itself: (s, s - o)
                    p = G[spec["gadget"]]
                    return (p[2], p[2] - p[3])
                if kind == "cert":            # J of size a(gadget) with certified q
                    return (G[spec["size_from_a_of"]][0], certs[spec["cert"]])
                if kind == "cert_s":          # J of size s(gadget) with certified q
                    return (G[spec["size_from_s_of"]][2], certs[spec["cert"]])
                raise ValueError(kind)
            J0 = cb(st["J0"])
            JH = cb(st["JH"])
            JV = cb(st["JV"])
            G[name] = hetgao(G[st["left"]], G[st["right"]], J0, JH, JV)
            dim[name] = dim[st["left"]] + dim[st["right"]]
        else:
            raise ValueError(op)
        if "expect_profile" in st:
            check(G[name] == tuple(st["expect_profile"]), "gadget %s profile equals the value printed in the paper" % name)
        if "expect_sigma_of" in st:
            check(G[name] == sigma(G[st["expect_sigma_of"]]), "gadget %s equals sigma(%s)" % (name, st["expect_sigma_of"]))
        if "expect_nf" in st:
            check(tuple(G[name][2:]) == tuple(st["expect_nf"]), "gadget %s (s,o,h,v) equals Table 6(a) of the paper" % name)
    return G, dim


# ----------------------------------------------------------------------------- DAG
def run_dag(R, sched):
    """sched: w0 (7 ints), base_degree, nodes (topologically ordered list of [name, rule, kids]),
    terminal {code, children}.  Returns (M, E, vals, exps)."""
    vals = {"w": tuple(sched["w0"])}
    exps = {"w": 1}
    for name, rule, kids in sched["nodes"]:
        vals[name] = apply_rule(R, rule, [vals[k] for k in kids])
        exps[name] = sum(exps[k] for k in kids)
    t = sched["terminal"]
    M = apply_code(R, t["code"], [vals[k] for k in t["children"]])
    E = sum(exps[k] for k in t["children"])
    return M, E, vals, exps


def rules_used(*scheds):
    tabs, codes = set(), set()
    for s in scheds:
        if s is None:
            continue
        for name, rule, kids in s["nodes"]:
            tabs.add(rule)
        codes.add(s["terminal"]["code"])
    return tabs, codes


def main(objdir, trdir):
    t0 = time.time()
    R, sep = load_rules(os.path.join(objdir, "rules.json"))
    sched = json.load(open(os.path.join(objdir, "schedule.json")))
    argon = json.load(open(os.path.join(objdir, "argon_shannon_certificates.json")))
    recs = json.load(open(os.path.join(trdir, "records.json")))
    cyc = sched["cycle"]
    claim = argon[cyc][sched["argon_key"]]
    print("== claim %s (%s), key %s" % (cyc, sched["description"], sched["argon_key"]))

    print("-- 1. separation relation")
    check_relation(sep)

    kind = sched["kind"]
    used_tabs, used_codes = set(), set()
    if kind == "bpz_dag":
        t_, c_ = rules_used(sched["schedule"], sched.get("baseline"))
        used_tabs |= t_
        used_codes |= c_
    else:
        used_tabs |= set(sched["tables_used"])
        used_codes |= set(sched["codes_used"])
    print("-- 2. admissibility of every table and terminal code used: %s ; %s" % (sorted(used_tabs), sorted(used_codes)))
    for n in sorted(used_tabs):
        check_table(n, R["tables"][n], sep)
    for n in sorted(used_codes):
        check_code(n, R["codes"][n], sep)

    kat_ok = True
    if kind == "bpz_dag":
        print("-- 3. recompute M along the schedule")
        M, E, vals, exps = run_dag(R, sched["schedule"])
        d = E * sched["base_degree"]
        # base-block check: the recorded base vector is an input (Lean-verified in the BPZ repository)
        print("  base seven-family cardinality vector (B,N,A,D,O,H,V) in C_%d^(box %d): %s" % (sched["m"], sched["base_degree"], list(sched["schedule"]["w0"])))
        check(all(exps[k] >= 1 for k in exps), "all node exponents positive")
        print("  M computed: %d digits, degree d = %d x %d = %d" % (len(str(M)), E, sched["base_degree"], d))
        # baseline (BPZ Lean schedule) as evaluator known-answer
        if sched.get("baseline"):
            Mb, Eb, _, _ = run_dag(R, sched["baseline"])
            db = Eb * sched["base_degree"]
            rec_lean = [r for r in recs["records"] if r.get("id") == "bpz_lean"][0]
            check(Mb == int(rec_lean["M"]) and db == rec_lean["d"],
                  "known-answer: BPZ Lean schedule (%d nodes) recomputes the Lean integer exactly (d=%d, %d digits)" % (len(sched["baseline"]["nodes"]), db, len(str(Mb))))
    else:
        print("-- 3. recompute M along the schedule (Tandon gadget calculus + BPZ top level)")
        certs = sched["certificates"]
        G, dim = run_gadgets(sched, certs)
        # known-answer test: Tandon's own d=500 construction
        kat = sched["tandon_known_answer"]
        n6 = phi(G["G30_6"]); n8 = phi(G["G40_8"]); n11 = phi(sigma(G["G55"]))
        check(n6 == tuple(kat["n6"]), "known-answer: Tandon n6 vector equals eq. (119)/(160) of the paper")
        check(n8 == tuple(kat["n8"]), "known-answer: Tandon n8 vector equals eq. (127)/(162) of the paper")
        check(n11 == tuple(kat["n11"]), "known-answer: Tandon n11 vector equals eq. (142)/(161) of the paper")
        n25 = apply_rule(R, "S3b", [n6, n11, n8])
        M500 = apply_code(R, "K4a", [n25] * 4)
        check(M500 == int(kat["M500"]), "known-answer: Tandon's d=500 integer (%d digits) recomputed equals Theorem 2 of the paper" % len(str(M500)))
        lo500 = floor_root_scaled(M500, 500)
        check(fmt(lo500).startswith(kat["bound_prefix"]), "known-answer: M500^(1/500) = %s starts with the paper's %s" % (fmt(lo500), kat["bound_prefix"]))
        # BPZ's own Lean-verified C7 schedule (eq. (103) of the paper) as a second known answer
        w = phi(G["G5"]); sw = phi(sigma(G["G5"]))
        q2 = apply_rule(R, "S2a", [w, sw]); n3 = apply_rule(R, "S3a", [w, w, w])
        n4 = apply_rule(R, "S3a", [q2, w, w]); n5 = apply_rule(R, "S3a", [n3, w, w])
        b6 = apply_rule(R, "S3a", [n3, w, q2]); b8 = apply_rule(R, "S3a", [n4, q2, q2])
        b11 = apply_rule(R, "S3a", [n5, n3, n3]); b25 = apply_rule(R, "S3b", [b6, b11, b8])
        Mb = apply_code(R, "K4a", [b25] * 4)
        rec_lean = [r for r in recs["records"] if r.get("id") == "bpz_lean"][0]
        check(Mb == int(rec_lean["M"]), "known-answer: BPZ Lean C7 schedule recomputes the Lean integer (%d digits)" % len(str(Mb)))
        # the claimed object
        top = sched["top"]
        vecs = []
        total_dim = 0
        for gname in top["children"]:
            vecs.append(phi(G[gname]))
            total_dim += dim[gname]
        n_top = apply_rule(R, top["rule"], vecs)
        M = apply_code(R, top["code"], [n_top] * R["codes"][top["code"]]["arity"])
        d = total_dim * R["codes"][top["code"]]["arity"]
        for gname in top["children"]:
            print("  child %-4s dim %d profile %s" % (gname, dim[gname], list(G[gname])))
        print("  top vector w%d = %s" % (total_dim, list(n_top)))
        check(list(n_top) == claim["w140"], "top 140-dimensional vector equals the contributor's claimed vector")
        for gname, k in zip(top["children"], ("pi_P0", "pi_P1", "pi_P2")):
            check(list(G[gname]) == claim[k], "profile of %s equals the contributor's %s" % (gname, k))

    print("-- 4. M and degree against the contributor's claim")
    check(str(M) == claim["M"], "recomputed M equals the contributor's M (%d digits)" % len(str(M)))
    check(d == claim["degree"], "recomputed degree d = %d equals the contributor's degree" % d)
    print("  the set lives in C_%d^(box %d)" % (sched["m"], d))

    if FAILS:
        print("FAIL %s: %d check(s) failed before the comparison; stopping" % (cyc, len(FAILS)))
        return 1
    print("-- 5. bound and exact comparison with every record")
    lo = floor_root_scaled(M, d)
    print("  bound M^(1/d) with d=%d: %s (floor at %d digits, certified by exact integer powers)" % (d, fmt(lo), DIGITS))
    check(fmt(lo) == claim["bound_50d"], "bound equals the contributor's 50-digit value")
    margins = []
    all_beaten = True
    for r in recs["records"]:
        if r["kind"] == "exact":
            Mr, dr = int(r["M"]), r["d"]
            lor = floor_root_scaled(Mr, dr)
            strict = lo >= lor + 1
            direct = None
            if len(str(M)) * dr + len(str(Mr)) * d <= 30000000:
                direct = M ** dr > Mr ** d
                strict = strict and direct
            mg = lo - lor
            print("  record %-34s d=%-5d bound %s  margin %s%s" % (r["id"], dr, fmt(lor), ("+" if mg >= 0 else "-") + fmt(abs(mg)),
                                                                   "" if direct is None else "  direct M^d_rec > M_rec^d: %s" % direct))
            ok = check(strict, "bound strictly greater than %s (exact integer test)" % r["label"])
            if r.get("headline"):
                margins.append((r["id"], mg))
        else:
            v, nd = decimal_parts(r["value"])
            ok = check(lo * 10 ** nd > (v + 1) * 10 ** DIGITS,
                       "bound strictly greater than %s = %s (even after rounding the displayed decimal up one unit in its last place)" % (r["label"], r["value"]))
            mg = lo - v * 10 ** (DIGITS - nd)
            print("  record %-34s decimal %s  margin over the displayed decimal %s" % (r["id"], r["value"], fmt(mg)))
        all_beaten = all_beaten and ok

    dt = time.time() - t0
    head = [m for m in margins]
    print("")
    if FAILS:
        print("FAIL %s: %d check(s) failed" % (cyc, len(FAILS)))
        return 1
    hm = head[0] if head else None
    print("RESULT %s d=%d M_digits=%d bound=%s headline_margin_vs_%s=+%s all_records_beaten=%s time=%.1fs" %
          (cyc, d, len(str(M)), fmt(lo), hm[0] if hm else "none", fmt(hm[1]) if hm else "n/a", all_beaten, dt))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
