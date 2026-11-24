#!/usr/bin/env python3
"""Standalone check of object/p1_certified_values.json against the printed
Kim-Nguyen Tables 1-2 and against verify-it-yourself/expected.json.

Stdlib only (decimal). Recomputes the 19-row comparison under rounding (half
away from zero) and truncation (toward zero). Last line: PASS or FAIL.
Run from the package folder: python3 verify-it-yourself/check_p1.py
"""
from __future__ import print_function
import json, os, re, sys
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, getcontext

getcontext().prec = 80
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OBJECT = os.path.join(ROOT, "object", "p1_certified_values.json")
EXPECTED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expected.json")
EXCERPT = os.path.join(ROOT, "how-we-built-it", "inputs", "kn_arxiv_v1_tables_excerpt.txt")
PINCH = os.path.join(ROOT, "how-we-built-it", "inputs", "Test-Pinch.txt")
ST = os.path.join(ROOT, "how-we-built-it", "inputs", "Test-ST.txt")
ROW_RE = re.compile(r"^\s*(\d+\.\d+)\s+(-?\d+\.\d+)\s+([\d.]+)\s+\u00d7\s+10(\d+)\s")
BALL_RE = re.compile(r"\[([+-]?\d+\.\d+)\s+\+/-\s+([0-9.eE+-]+)\]")


def fail(msg):
    print(msg)
    print("FAIL")
    sys.exit(1)


def parse_excerpt(text):
    tables = {1: [], 2: []}
    cur, n = None, {1: 0, 2: 0}
    for line in text.splitlines():
        if "Table 1." in line:
            cur = 1
            continue
        if "Table 2." in line:
            cur = 2
            continue
        if cur is None:
            continue
        m = ROW_RE.match(line)
        if not m:
            continue
        n[cur] += 1
        tables[cur].append({"table": cur, "row": n[cur], "y": m.group(1), "printed": m.group(2)})
    return tables


def parse_ball(s):
    m = BALL_RE.match(s)
    if not m:
        fail("unparsed ball: %s" % s)
    mid = Decimal(m.group(1))
    rad = Decimal(m.group(2))
    return mid, mid - rad, mid + rad


def ndp(p):
    return len(p.split(".", 1)[1]) if "." in p else 0


def apply(x, d, mode):
    q = Decimal(1).scaleb(-d)
    rnd = ROUND_HALF_UP if mode == "round" else ROUND_DOWN
    return x.quantize(q, rounding=rnd)


def classify(lo, hi, printed, mode):
    d = ndp(printed)
    P = Decimal(printed)
    rl, rh = apply(lo, d, mode), apply(hi, d, mode)
    if rl == rh == P:
        return "MATCH"
    if rl != P and rh != P:
        return "MISMATCH"
    return "AMBIGUOUS"


def ys(path):
    return [l.split()[0] for l in open(path) if l.strip()]


def main():
    obj = json.load(open(OBJECT))
    exp = json.load(open(EXPECTED))
    if obj["N_gamma_lt_74000"] != 98625 or obj["N_gamma_lt_14000"] != 14950:
        fail("zero counts: N(74000)=%s N(14000)=%s" % (obj["N_gamma_lt_74000"], obj["N_gamma_lt_14000"]))
    if len(obj.get("values", [])) != 19:
        fail("expected 19 values, got %d" % len(obj.get("values", [])))
    if exp["N_gamma_lt_74000"] != 98625 or exp["N_gamma_lt_14000"] != 14950:
        fail("expected.json counts are wrong")
    if len(exp["values"]) != 19:
        fail("expected.json does not have 19 rows")
    for a, b in zip(obj["values"], exp["values"]):
        for k in ("file", "y", "k", "h_256", "h_320"):
            if a.get(k) != b.get(k):
                fail("object/%s != expected for y=%s (%s vs %s)" % (k, a.get("y"), a.get(k), b.get(k)))
        if a.get("overlap") is False:
            fail("shipped 256/320-bit balls do not overlap at y=%s" % a["y"])

    tables = parse_excerpt(open(EXCERPT, encoding="utf-8").read())
    if [r["y"] for r in tables[1]] != ys(PINCH):
        fail("excerpt Table 1 y values do not match Test-Pinch.txt")
    if [r["y"] for r in tables[2]] != ys(ST):
        fail("excerpt Table 2 y values do not match Test-ST.txt")
    balls = {v["y"]: v["h_320"] for v in obj["values"]}
    if set(balls) != {r["y"] for t in tables.values() for r in t}:
        fail("object y set does not match the excerpt")

    n_round = {"MATCH": 0, "MISMATCH": 0, "AMBIGUOUS": 0}
    n_trunc = {"MATCH": 0, "MISMATCH": 0, "AMBIGUOUS": 0}
    neither, only_r, only_t = [], [], []
    for t in (1, 2):
        for r in tables[t]:
            mid, lo, hi = parse_ball(balls[r["y"]])
            sr, stt = classify(lo, hi, r["printed"], "round"), classify(lo, hi, r["printed"], "trunc")
            n_round[sr] += 1
            n_trunc[stt] += 1
            key = "T%d r%d" % (t, r["row"])
            if sr == "MISMATCH" and stt == "MISMATCH":
                neither.append(key)
            elif sr == "MISMATCH" and stt == "MATCH":
                only_r.append(key)
            elif sr == "MATCH" and stt == "MISMATCH":
                only_t.append(key)
            print("%s printed %s  rounding=%s  truncation=%s  3dp %s / %s" % (
                key, r["printed"], sr, stt, apply(mid, 3, "round"), apply(mid, 3, "trunc")))

    print("rounding", n_round)
    print("truncation", n_trunc)
    print("corrections at printed precision (either convention):", neither)
    print("convention-dependent (rounding only):", only_r)
    print("mismatch under truncation only:", only_t)
    if n_round != {"MATCH": 11, "MISMATCH": 8, "AMBIGUOUS": 0}:
        fail("rounding counts %s" % n_round)
    if n_trunc != {"MATCH": 13, "MISMATCH": 6, "AMBIGUOUS": 0}:
        fail("truncation counts %s" % n_trunc)
    if neither != ["T2 r1", "T2 r4", "T2 r12", "T2 r14"]:
        fail("corrections %s" % neither)
    if only_r != ["T2 r2", "T2 r7", "T2 r9", "T2 r10"]:
        fail("rounding-only %s" % only_r)
    if only_t != ["T1 r4", "T2 r6"]:
        fail("truncation-only %s" % only_t)
    print("PASS")


if __name__ == "__main__":
    main()
