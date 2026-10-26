#!/usr/bin/env python3
"""Known answer: recompute the integer of the BPZ Lean C7 schedule (object/bpz_lean_c7_schedule.json, transcribed from
CertC7.lean) with the substitution tables and the terminal code of object/rules.json, and compare with the integer M that
the Lean source defines (table-record/records.json, id bpz_lean).  Also checks Definition 6 for the tables and codes used.
Standard library only.   Usage: python3 bpz_lean_c7_check.py OBJECT_DIR TABLE_RECORD_DIR"""
import os, sys, json, itertools
LET = "BNADOHV"


def main(od, td):
    R = json.load(open(os.path.join(od, "rules.json")))
    S = json.load(open(os.path.join(od, "bpz_lean_c7_schedule.json")))
    rec = [r for r in json.load(open(os.path.join(td, "records.json")))["records"] if r["id"] == "bpz_lean"][0]
    sep = {(a, b) for a, b in R["sep"]}
    ok = True
    sepw = lambda x, y: any((a, b) in sep for a, b in zip(x, y))
    for name in sorted({n["rule"] for n in S["nodes"]}):
        T = R["tables"][name]["words"]
        bad = 0
        for l in LET:
            for x, y in itertools.combinations([tuple(w) for w in T[l]], 2):
                bad += not sepw(x, y)
        for a in LET:
            for b in LET:
                if (a, b) in sep:
                    bad += sum(not sepw(x, y) for x in T[a] for y in T[b])
        print("  table %s: Definition 6 violations %d" % (name, bad)); ok &= bad == 0
    K = [tuple(w) for w in R["codes"][S["terminal"]["code"]]["words"]]
    bad = sum(not sepw(x, y) for x, y in itertools.combinations(K, 2))
    print("  code %s: pairwise separation violations %d" % (S["terminal"]["code"], bad)); ok &= bad == 0
    val = {"w": tuple(S["w0"]), "wf": tuple(S["w0f"])}
    exp = {"w": 1, "wf": 1}
    for nd in S["nodes"]:
        tab = R["tables"][nd["rule"]]["words"]
        ch = [val[c] for c in nd["children"]]
        val[nd["name"]] = tuple(sum(eval_prod(ch, w) for w in tab[l]) for l in LET)
        exp[nd["name"]] = sum(nd["exponents"])
        ok &= [exp[c] for c in nd["children"]] == nd["exponents"]
    ch = [val[c] for c in S["terminal"]["children"]]
    M = sum(eval_prod(ch, w) for w in R["codes"][S["terminal"]["code"]]["words"])
    E = sum(S["terminal"]["exponents"])
    ok &= [exp[c] for c in S["terminal"]["children"]] == S["terminal"]["exponents"]
    d = E * S["base_degree"]
    print("  child exponents agree with the Lean exponents; E = %d, d = %d" % (E, d))
    good = (M == int(rec["M"]) and d == rec["d"])
    print("  M (%d digits) %s the integer defined in CertC7.lean (d = %d)" % (len(str(M)), "equals" if good else "DIFFERS FROM", rec["d"]))
    ok &= good
    print("RESULT BPZ Lean C7 schedule known answer %s" % ("reproduced: d=%d, %d digits" % (d, len(str(M))) if ok else "FAILED"))
    return 0 if ok else 1


def eval_prod(ch, w):
    p = 1
    for i, c in enumerate(w):
        p *= ch[i][LET.index(c)]
    return p


if __name__ == "__main__":
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    sys.exit(main(sys.argv[1], sys.argv[2]))
