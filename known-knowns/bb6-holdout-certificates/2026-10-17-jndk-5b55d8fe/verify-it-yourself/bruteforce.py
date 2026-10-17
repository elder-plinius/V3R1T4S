# Independent naive sanity check (own parser, own simulator; shares no code with prove.py).
# For each rule (and mutated rules), k = lo..12, x in {0,1}, several random exteriors:
# place window inside random tape, run exactly `steps` transitions, require state A, head at marker cell,
# window == output, exterior unchanged, and head never left the window during the run.
import json, random, re, sys
RULES = json.loads(RULES_JSON)["rules"]
M = "1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB"
T = {}
for si, p in enumerate(M.split("_")):
    for r in range(2):
        t = p[3 * r:3 * r + 3]
        if t != "---":
            T[("ABCDEF"[si], r)] = (int(t[0]), 1 if t[1] == "R" else -1, t[2])

TOK = re.compile(r"A|x|[01](?:\^(?:\(([^)]*)\)|(\d+|k)(?= |$)))?")

def ev(e, kv):
    e = re.sub(r"(\d)k", r"\1*k", e).replace("^", "**")
    return eval(e, {"k": kv})

def expand(pat, kv, xv):
    cells, mark = [], None
    for tok in pat.split(" "):
        pos = 0
        while pos < len(tok):
            m = TOK.match(tok, pos)
            if not m or m.end() == pos:
                raise ValueError("cannot tokenize %r" % tok)
            s = m.group(0)
            if s == "A":
                mark = len(cells)
            elif s == "x":
                cells.append(xv)
            else:
                e = m.group(1) or m.group(2)
                n = ev(e, kv) if e else 1
                if n < 0:
                    raise ValueError("negative exponent")
                cells += [int(s[0])] * n
            pos = m.end()
    return cells, mark

def check(rule, kv, xv, rng):
    win, h0 = expand(rule["input"], kv, xv)
    out, h1 = expand(rule["output"], kv, xv)
    N = ev(rule["steps"], kv)
    if len(win) != len(out):
        return "length mismatch"
    PAD = 40
    left = [rng.randint(0, 1) for _ in range(PAD)]
    right = [rng.randint(0, 1) for _ in range(PAD)]
    tape = left + win + right
    lo, hi = PAD, PAD + len(win) - 1
    h = PAD + h0
    st = "A"
    for t in range(N):
        if not (lo <= h <= hi):
            return "head left window at step %d" % t
        key = (st, tape[h])
        if key not in T:
            return "halted at step %d" % t
        w, mv, ns = T[key]
        tape[h] = w; h += mv; st = ns
    if not (lo <= h <= hi):
        return "head outside window at end"
    if tape[:PAD] != left or tape[PAD + len(win):] != right:
        return "exterior modified"
    if st != "A":
        return "state %s at end" % st
    if h != PAD + h1:
        return "head at %d, stated %d" % (h - PAD, h1)
    if tape[lo:hi + 1] != out:
        return "window %s != stated %s" % ("".join(map(str, tape[lo:hi + 1])), "".join(map(str, out)))
    return None

def run(rules, label):
    rng = random.Random(20261017)
    print("== %s" % label)
    summary = {}
    for r in rules:
        lo = int(r["domain"].split(">=")[1])
        ok = bad = 0; first = None
        for kv in range(lo, 13):
            for xv in (0, 1):
                for rep in range(3):
                    try:
                        e = check(r, kv, xv, rng)
                    except ValueError as ex:
                        e = "parse: %s" % ex
                    if e is None:
                        ok += 1
                    else:
                        bad += 1
                        if first is None:
                            first = "k=%d x=%d: %s" % (kv, xv, e)
        summary[r["id"]] = (ok, bad)
        print("  %-11s pass=%d fail=%d %s" % (r["id"], ok, bad, ("first failure: " + first) if first else ""))
    return summary

import copy
real = run(RULES, "REAL RULES (known positives)")
print("all real pass:", all(b == 0 for _, b in real.values()))

def mut(rid, **kw):
    rs = [copy.deepcopy(r) for r in RULES if r["id"] == rid]
    rs[0].update(kw); rs[0]["id"] = rid + "*"
    return rs
MUTS = (mut("even", steps="12k-2") + mut("Eodd", steps="24k+6") + mut("odd", output="A x10 1^(2k-1) 00 110")
        + mut("Dstep", output="10 A10 1^(2k-1) 00 111") + mut("even", output="A 0 1^(2k-2) 00 111")
        + mut("even", input="x A0 1^(2k)", output="A x 1^(2k-2) 00 1") + mut("even_drain", steps="6k^2+3k+1")
        + mut("Ddrain1", steps="12k^2+14k"))
mres = run(MUTS, "MUTATED RULES (known negatives; each must have failures)")
print("all mutants caught:", all(b > 0 for _, b in mres.values()))
