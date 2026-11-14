#!/usr/bin/env python3
"""Standalone checker for the pricing050 weak-duality certificate.

Definition (MINLPLib pricing050.gms as posted):
  Variables x2..x51 in [0,10]; maximize objvar.
  e1: (-sum_i c_i x_i) - objvar =E= 0  =>  objvar = -sum c_i x_i
  e_j (j=2..6): (-sum_i a_ji x_i exp(-b_ji x_i^{p_ji})) =L= -rhs_j
             => sum_i a_ji x_i exp(...) >= rhs_j
  with (rhs_2..rhs_6) = (500, 651, 615, 788, 984).

Equivalent minimize F = sum c_i x_i. Weak Lagrangian duality with lambda >= 0:
  theta(lambda) = sum_j lambda_j * rhs_j + sum_i min_{x in [0,10]} h_i(x)
  h_i(x) = c_i x - sum_j lambda_j * a_ji * x * exp(-b_ji * x^{p_ji})
Any rigorous lower bound LB <= theta yields U = -LB as an upper bound on max objvar.

This checker reads object/lambda.txt and object/cert_arb_leaves.json, parses the
posted .gms (path given as argv[1]), verifies every leaf enclosure with Arb ball
arithmetic (python-flint), reassembles the dual, and checks
  U <= -1813.829075713452
  U <= best_primal + 1e-6*|best_primal|   with best_primal = -1813.829078
Exit 0 and print a line containing PASS on success; otherwise exit 1 and FAIL.
"""
from __future__ import annotations

import json
import re
import sys
from decimal import Decimal, getcontext
from pathlib import Path

try:
    from flint import arb, ctx
except ImportError:
    print("python-flint is required (pip install python-flint)", file=sys.stderr)
    print("FAIL")
    sys.exit(1)

getcontext().prec = 80
ctx.prec = 256

CLAIMED_U = Decimal("-1813.829075713452")
BEST_PRIMAL = Decimal("-1813.829078")
BAR = BEST_PRIMAL + Decimal("1e-6") * abs(BEST_PRIMAL)
EXPECTED_NLEAVES = 1958
EXPECTED_GMS_SHA256 = (
    "192dd92d69cdcd131462d40c137df73dc101afef0739cc7ba98c130a79313715"
)
RHS = {"e2": 500, "e3": 651, "e4": 615, "e5": 788, "e6": 984}


def die(msg: str) -> None:
    print("ERROR:", msg)
    print("FAIL")
    sys.exit(1)


def A(d: Decimal) -> arb:
    return arb(format(d, "f"))


def extract_eq(gms: str, name: str):
    m = re.search(rf"{name}\.\.(.*?)(?:=E=|=L=)\s*([^\n;]+)", gms, re.S)
    if not m:
        die("missing equation %s" % name)
    return re.sub(r"\s+", " ", m.group(1)).strip(), m.group(2).strip()


def parse_model(gms: str):
    body1, rhs1 = extract_eq(gms, "e1")
    if rhs1 != "0":
        die("e1 rhs is %r, expected 0" % rhs1)
    body1 = re.sub(r"-?\s*objvar", "", body1).strip()
    c = {f"x{i}": Decimal(0) for i in range(2, 52)}
    for m in re.finditer(r"([+-])\s*(?:(\d+(?:\.\d+)?)\s*\*\s*)?(x\d+)", body1):
        sign = -1 if m.group(1) == "-" else 1
        coef = Decimal(m.group(2) or "1")
        c[m.group(3)] = -(sign * coef)
    term_re = re.compile(
        r"([+-])\s*(?:(\d+(?:\.\d+)?)\s*\*\s*)?(x\d+)\s*\*\s*exp\s*\(\s*-\s*"
        r"(?:(\d+(?:\.\d+)?)\s*\*\s*)?"
        r"(?:power\s*\(\s*(x\d+)\s*,\s*(\d+)\s*\)|sqr\s*\(\s*(x\d+)\s*\)|(x\d+))"
        r"\s*\)"
    )
    rhs_pos = {}
    terms = {f"x{i}": [] for i in range(2, 52)}
    for eq, rhs_expected in RHS.items():
        body, rhs = extract_eq(gms, eq)
        if Decimal(rhs) != -rhs_expected:
            die("%s rhs %s != -%s" % (eq, rhs, rhs_expected))
        rhs_pos[eq] = Decimal(rhs_expected)
        found = list(term_re.finditer(body))
        leftover = body
        for m in reversed(found):
            leftover = leftover[: m.start()] + " " + leftover[m.end() :]
        leftover = leftover.strip()
        if leftover:
            die("%s unparsed leftover: %r" % (eq, leftover[:120]))
        for m in found:
            sign = -1 if m.group(1) == "-" else 1
            a = Decimal(m.group(2) or "1")
            var = m.group(3)
            b = Decimal(m.group(4)) if m.group(4) else Decimal(1)
            if m.group(5):
                if m.group(5) != var:
                    die("power var mismatch in %s" % eq)
                p = int(m.group(6))
            elif m.group(7):
                if m.group(7) != var:
                    die("sqr var mismatch in %s" % eq)
                p = 2
            else:
                if m.group(8) != var:
                    die("linear-exp var mismatch in %s" % eq)
                p = 1
            a_pos = -(sign * a)
            if a_pos <= 0:
                die("non-positive a in %s/%s" % (eq, var))
            terms[var].append((eq, a_pos, b, p))
        print("parsed %s: %d terms" % (eq, len(found)))
    return c, terms, rhs_pos


def phi(c, terms, lam, var, X):
    s = A(c[var]) * X
    for eq, a, b, p in terms[var]:
        lj = A(lam[eq])
        if lj == 0:
            continue
        s = s - lj * A(a) * X * ((-A(b) * X ** p).exp())
    return s


def dphi(c, terms, lam, var, X):
    s = A(c[var])
    for eq, a, b, p in terms[var]:
        lj = A(lam[eq])
        if lj == 0:
            continue
        s = s - lj * A(a) * ((-A(b) * X ** p).exp()) * (1 - A(b) * p * X ** p)
    return s


def enclose_lower(c, terms, lam, var, lo, hi):
    X = arb((lo + hi) / 2, (hi - lo) / 2)
    nat = phi(c, terms, lam, var, X)
    m = (lo + hi) / 2
    mv = phi(c, terms, lam, var, arb(m)) + dphi(c, terms, lam, var, X) * (X - m)
    return max(nat.lower(), mv.lower())


def verify_leaf(c, terms, lam, var, lo_s, hi_s, claimed_s, max_depth=48):
    claimed = arb(str(claimed_s))
    stack = [(arb(str(lo_s)), arb(str(hi_s)), 0)]
    while stack:
        lo, hi, depth = stack.pop()
        lb = enclose_lower(c, terms, lam, var, lo, hi)
        if (arb(lb) - claimed).lower() >= 0:
            continue
        X = arb((lo + hi) / 2, (hi - lo) / 2)
        up = phi(c, terms, lam, var, X).upper()
        if (claimed - arb(up)).lower() > 0:
            return False, "hardfail upper < claimed"
        wid = float((hi - lo).mid())
        if depth >= max_depth or wid < 1e-18:
            return False, "inconclusive depth=%d wid=%g" % (depth, wid)
        mid = (lo + hi) / 2
        stack.append((lo, mid, depth + 1))
        stack.append((mid, hi, depth + 1))
    return True, "ok"


def main() -> int:
    if len(sys.argv) != 4:
        die("usage: check_dual_certificate.py <gms> <lambda.txt> <cert_arb_leaves.json>")
    gms_path = Path(sys.argv[1])
    lam_path = Path(sys.argv[2])
    leaf_path = Path(sys.argv[3])
    import hashlib

    gms_bytes = gms_path.read_bytes()
    gms_sha = hashlib.sha256(gms_bytes).hexdigest()
    print("gms sha256", gms_sha)
    if gms_sha != EXPECTED_GMS_SHA256:
        die("gms sha256 mismatch (got %s)" % gms_sha)
    gms = gms_bytes.decode("utf-8", "replace")
    c, terms, rhs_pos = parse_model(gms)
    total_nl = sum(len(v) for v in terms.values())
    print("total NL terms", total_nl, "nonzero c", sum(1 for v in c.values() if v))
    if total_nl != 249:
        die("expected 249 NL terms, got %d" % total_nl)

    lam = {}
    for line in lam_path.read_text().splitlines():
        if not line.strip():
            continue
        k, v = line.split()
        lam[k] = Decimal(v)
        if lam[k] < 0:
            die("negative multiplier %s" % k)
    for k in RHS:
        if k not in lam:
            die("missing multiplier %s" % k)

    leaf = json.loads(leaf_path.read_text())
    for k, v in leaf.get("lambda", {}).items():
        if Decimal(v) != lam[k]:
            die("lambda mismatch for %s" % k)
    if leaf.get("nleaves") != EXPECTED_NLEAVES:
        die("nleaves field %s != %d" % (leaf.get("nleaves"), EXPECTED_NLEAVES))

    n_ok = 0
    n_leaves = 0
    var_mins = {}
    for vname in sorted(leaf["vars"].keys(), key=lambda s: int(s[1:])):
        info = leaf["vars"][vname]
        leaf_list = info["leaf_list"]
        if info.get("leaves") != len(leaf_list):
            die("%s leaves count mismatch" % vname)
        intervals = sorted(
            ((Decimal(a), Decimal(b), cl) for a, b, cl in leaf_list),
            key=lambda t: (t[0], t[1]),
        )
        if intervals[0][0] != 0:
            die("%s coverage starts at %s" % (vname, intervals[0][0]))
        cur = Decimal(0)
        for a, b, _ in intervals:
            if a > cur:
                die("%s coverage gap %s -> %s" % (vname, cur, a))
            if b > cur:
                cur = b
        if cur != 10:
            die("%s coverage ends at %s" % (vname, cur))
        mins = []
        for a, b, claimed in leaf_list:
            n_leaves += 1
            if Decimal(a) >= Decimal(b):
                die("%s empty interval [%s,%s]" % (vname, a, b))
            ok, msg = verify_leaf(c, terms, lam, vname, a, b, claimed)
            if not ok:
                die("%s [%s,%s] claimed=%s: %s" % (vname, a, b, claimed, msg))
            n_ok += 1
            mins.append(Decimal(claimed))
        var_mins[vname] = min(mins)

    print("n_leaves", n_leaves, "n_ok", n_ok)
    if n_leaves != EXPECTED_NLEAVES or n_ok != n_leaves:
        die("leaf count %d ok %d expected %d" % (n_leaves, n_ok, EXPECTED_NLEAVES))

    const = sum((lam[eq] * rhs_pos[eq] for eq in rhs_pos), Decimal(0))
    sum_mins = sum((var_mins[f"x{i}"] for i in range(2, 52)), Decimal(0))
    LB = const + sum_mins
    U = -LB
    print("const", const)
    print("LB from verified leaf claims", LB)
    print("U", U)
    print("claimed_U", CLAIMED_U)
    print("bar", BAR)
    print("U <= claimed_U", U <= CLAIMED_U)
    print("U <= bar", U <= BAR)
    if not (U <= CLAIMED_U and U <= BAR):
        die("dual upper bound out of tolerance")
    # JSON LB_lower must not exceed the verified LB (it may be a truncation)
    json_lb = Decimal(leaf["LB_lower"])
    if json_lb > LB + Decimal("1e-20"):
        die("JSON LB_lower %s exceeds verified LB %s" % (json_lb, LB))
    print(
        "dual certificate: max objvar <= %s (<= bar %s); leaves %d verified"
        % (CLAIMED_U, BAR, n_leaves)
    )
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
