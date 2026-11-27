"""Compare all 19 certified values (result/p1_certified_values.json: 14 Table 2 rows =
Test-ST.txt, 5 Table 1 rows = Test-Pinch.txt) with the values printed in Kim-Nguyen
arXiv:2502.21021v1, Tables 1-2, parsed from inputs/kn_arxiv_v1_tables_excerpt.txt.

The paper mixes rounding and truncation (including in its y+sqrt(y) column). This
script reports the h-cell comparison under BOTH conventions, at the printed number
of decimals:

  rounding    = round half away from zero (Decimal ROUND_HALF_UP)
  truncation  = toward zero (Decimal ROUND_DOWN)

A row is MATCH if every point of the certified ball maps to the printed value,
MISMATCH if none does, AMBIGUOUS otherwise. It also classifies the paper's
y+sqrt(y) column (4 significant figures in the excerpt) under the same two
conventions. Usage: python compare_printed.py > compare_printed.md
"""
import json, os, re
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, getcontext

getcontext().prec = 80
H = os.path.dirname(os.path.abspath(__file__))
EXCERPT = os.path.join(H, "..", "inputs", "kn_arxiv_v1_tables_excerpt.txt")
RESULT = os.path.join(H, "..", "result", "p1_certified_values.json")
FILES = {"Test-ST.txt": 2, "Test-Pinch.txt": 1}

# Cross-check: printed h strings as they appear in the excerpt / PDF.
PRINTED = {
    "Test-ST.txt": ["-0.974798", "-0.9949", "-1.007", "-0.9949", "-1.02",
                    "-0.9998977", "1.025", "-0.997", "0.997", "1.0017",
                    "-1.0002", "1.00057", "1.0079", "-1.00004"],
    "Test-Pinch.txt": ["0.991", "-0.993", "-1.012", "1.0019", "1.0004"],
}

ROW_RE = re.compile(r"^\s*(\d+\.\d+)\s+(-?\d+\.\d+)\s+([\d.]+)\s+×\s+10(\d+)\s")


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
        tables[cur].append({
            "table": cur, "row": n[cur], "y": m.group(1), "printed": m.group(2),
            "ysqrt_coeff": m.group(3), "ysqrt_exp": int(m.group(4)),
        })
    return tables


def parse_ball(s):
    m = re.match(r"\[([+-]?\d+\.\d+)\s+\+/-\s+([0-9.eE+-]+)\]", s)
    if not m:
        raise ValueError("unparsed ball: %s" % s)
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


def to_sci(val):
    e = int(val.adjusted())
    return val / (Decimal(10) ** e), e


def ysqrt(y):
    Y = Decimal(y)
    return Y + Y.sqrt()


def main():
    tables = parse_excerpt(open(EXCERPT, encoding="utf-8").read())
    res = json.load(open(RESULT))
    ys = {f: [l.split()[0] for l in open(os.path.join(H, "..", "inputs", f)) if l.strip()]
          for f in FILES}
    assert [r["y"] for r in tables[1]] == ys["Test-Pinch.txt"]
    assert [r["y"] for r in tables[2]] == ys["Test-ST.txt"]
    assert [r["printed"] for r in tables[1]] == PRINTED["Test-Pinch.txt"]
    assert [r["printed"] for r in tables[2]] == PRINTED["Test-ST.txt"]
    balls = {v["y"]: v["h_320"] for v in res["values"]}
    assert set(balls) == {r["y"] for t in tables.values() for r in t}

    rows, ysqrt_rows = [], []
    for t in (1, 2):
        for r in tables[t]:
            mid, lo, hi = parse_ball(balls[r["y"]])
            d = ndp(r["printed"])
            rec = {
                "table": t, "row": r["row"], "y": r["y"], "printed": r["printed"],
                "decimals": d, "ball": balls[r["y"]],
                "certified_7dp": str(apply(mid, 7, "round")),
                "certified_at_printed_dp_rounding": str(apply(mid, d, "round")),
                "certified_at_printed_dp_truncation": str(apply(mid, d, "trunc")),
                "certified_3dp_rounding": str(apply(mid, 3, "round")),
                "certified_3dp_truncation": str(apply(mid, 3, "trunc")),
                "abs_diff": "%.1e" % abs(float(mid - Decimal(r["printed"]))),
                "status_rounding": classify(lo, hi, r["printed"], "round"),
                "status_truncation": classify(lo, hi, r["printed"], "trunc"),
            }
            rows.append(rec)
            val = ysqrt(r["y"])
            mant, e = to_sci(val)
            pc, pe, pd = Decimal(r["ysqrt_coeff"]), r["ysqrt_exp"], ndp(r["ysqrt_coeff"])
            mr, mt = apply(mant, pd, "round"), apply(mant, pd, "trunc")
            fit_r = (e == pe and mr == pc)
            fit_t = (e == pe and mt == pc)
            if fit_r and fit_t:
                tag = "both"
            elif fit_r:
                tag = "rounding"
            elif fit_t:
                tag = "truncation"
            else:
                tag = "neither"
            ysqrt_rows.append({
                "table": t, "row": r["row"], "printed": "%s e%d" % (r["ysqrt_coeff"], pe),
                "mantissa_rounded": str(mr), "mantissa_truncated": str(mt),
                "exponent": e, "fits": tag,
            })

    def count(key, label):
        return {s: sum(r[key] == s for r in rows) for s in ("MATCH", "MISMATCH", "AMBIGUOUS")}

    n_round = count("status_rounding", "rounding")
    n_trunc = count("status_truncation", "truncation")
    neither = [r for r in rows if r["status_rounding"] == "MISMATCH" and r["status_truncation"] == "MISMATCH"]
    only_r = [r for r in rows if r["status_rounding"] == "MISMATCH" and r["status_truncation"] == "MATCH"]
    only_t = [r for r in rows if r["status_rounding"] == "MATCH" and r["status_truncation"] == "MISMATCH"]

    print("| table | row | y (exact, as published) | printed | certified (7 dp) | at printed dp (round / trunc) | certified (3 dp, round / trunc) | |diff| | rounding | truncation |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        print("| %d | %d | %s | %s | %s | %s / %s | %s / %s | %s | %s | %s |" % (
            r["table"], r["row"], r["y"], r["printed"], r["certified_7dp"],
            r["certified_at_printed_dp_rounding"], r["certified_at_printed_dp_truncation"],
            r["certified_3dp_rounding"], r["certified_3dp_truncation"],
            r["abs_diff"], r["status_rounding"], r["status_truncation"]))
    print()
    print("rows: %d; rounding %s; truncation %s" % (len(rows), n_round, n_trunc))
    print("wrong under either convention (corrections at printed precision): %s" % (
        ["T%d r%d" % (r["table"], r["row"]) for r in neither],))
    print("mismatch under rounding only (convention-dependent): %s" % (
        ["T%d r%d" % (r["table"], r["row"]) for r in only_r],))
    print("mismatch under truncation only (convention-dependent the other way): %s" % (
        ["T%d r%d" % (r["table"], r["row"]) for r in only_t],))
    print()
    print("## y+sqrt(y) column (4 significant figures as printed in the excerpt)")
    print()
    print("| table | row | printed | rounded mantissa | truncated mantissa | fits |")
    print("|---|---|---|---|---|---|")
    for r in ysqrt_rows:
        print("| %d | %d | %s | %s | %s | %s |" % (
            r["table"], r["row"], r["printed"], r["mantissa_rounded"],
            r["mantissa_truncated"], r["fits"]))
    y_round = ["T%d r%d" % (r["table"], r["row"]) for r in ysqrt_rows if r["fits"] == "rounding"]
    y_trunc = ["T%d r%d" % (r["table"], r["row"]) for r in ysqrt_rows if r["fits"] == "truncation"]
    print()
    print("y+sqrt(y) rounding only: %s; truncation only: %s; neither: %s" % (
        y_round, y_trunc, [r for r in ysqrt_rows if r["fits"] == "neither"]))

    out = {
        "rows": rows,
        "counts": {"rounding": n_round, "truncation": n_trunc},
        "corrections_either_convention": ["T%d r%d" % (r["table"], r["row"]) for r in neither],
        "mismatch_rounding_only": ["T%d r%d" % (r["table"], r["row"]) for r in only_r],
        "mismatch_truncation_only": ["T%d r%d" % (r["table"], r["row"]) for r in only_t],
        "ysqrt": ysqrt_rows,
    }
    json.dump(out, open(os.path.join(H, "compare_printed.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
