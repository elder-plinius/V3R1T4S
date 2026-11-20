"""Reading-direction check (joyboseroy documents a reversal bug; verify before scoring).

Diagnostic (from joyboseroy/indus_decipher analysis/direction_test.py and the M77
fingerprint of Rao/Yadav): in the correctly-oriented corpus the FINAL sign position
is more strongly constrained (lower entropy) than the INITIAL position. We compute
the initial-vs-final positional entropy gap on (a) M77 as stored, (b) the post-1977
merged corpus as stored, and (c) both reversed, and record which orientation matches
the fingerprint. Run BEFORE any claim measurement.
"""
import sys, csv, json, os, math, collections, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pipeline as P

def ent(counter, tot):
    if tot == 0:
        return 0.0
    return -sum((c / tot) * math.log2(c / tot) for c in counter.values() if c > 0)

def pos_entropy(seqs, pos):
    c = collections.Counter()
    for s in seqs:
        if pos == "first" and len(s) >= 1:
            c[s[0]] += 1
        elif pos == "last" and len(s) >= 1:
            c[s[-1]] += 1
    return ent(c, sum(c.values()))

def main():
    out = {"fetched": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    # M77 (joyboseroy CSV, stored R-L; im77: stored in reading order)
    recs = P.m77_training()
    seqs = [r["seq"] for r in recs if len(r["seq"]) >= 2]
    rev = [list(reversed(s)) for s in seqs]
    e1 = pos_entropy(seqs, "first")
    el = pos_entropy(seqs, "last")
    e1r = pos_entropy(rev, "first")
    elr = pos_entropy(rev, "last")
    out["M77"] = {
        "as_stored_first": round(e1, 4), "as_stored_last": round(el, 4),
        "reversed_first": round(e1r, 4), "reversed_last": round(elr, 4),
        "as_stored_final_minus_initial": round(el - e1, 4),
        "fingerprint": "final position more constrained (lower entropy) than initial (Rao/Yadav M77 fingerprint)",
        "as_stored_matches": el < e1,
    }
    # merged corpus (Wells coding, as stored in merged-corpus-reading-order.json)
    merged = P.load_merged()
    mseqs = [tuple(x for x in r["seq"] if x != 0) for r in merged]
    mseqs = [s for s in mseqs if len(s) >= 2]
    mrev = [list(reversed(s)) for s in mseqs]
    out["merged"] = {
        "as_stored_first": round(pos_entropy(mseqs, "first"), 4),
        "as_stored_last": round(pos_entropy(mseqs, "last"), 4),
        "reversed_first": round(pos_entropy(mrev, "first"), 4),
        "reversed_last": round(pos_entropy(mrev, "last"), 4),
        "as_stored_matches": pos_entropy(mseqs, "last") < pos_entropy(mseqs, "first"),
    }
    # per-direction-code check on im77 (the M77 export carries per-line direction codes)
    rows = list(csv.DictReader(open(os.path.join(P.DATA, "im77_corpus_lines.csv"))))
    dc = collections.Counter(r["direction"] for r in rows)
    out["im77_direction_code_counts"] = dict(dc)
    print(json.dumps(out, indent=2))
    with open(os.path.join(HERE, "output", "direction_check.json"), "w") as f:
        json.dump(out, f, indent=2)

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    main()
