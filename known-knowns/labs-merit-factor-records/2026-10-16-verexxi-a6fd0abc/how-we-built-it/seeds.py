#!/usr/bin/env python3
"""Per-L baseline (min over every printed value and every decoded sequence, all sources) and the one-element
operator seeds (append +-1 at either end of an L-1 sequence; remove either end of an L+1 sequence).
Writes baseline/baseline.tsv (L, best E, sources attaining it) and baseline/seeds/L.txt (seed sequences, best first)."""
import sys, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from labs_energy import energy

rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
def ok_parent(r):
    """Verified rows, plus printed sequences whose decode is plausible but whose printed F is inconsistent
    (kind hex-full?, energy within 0.5% of the energy implied by the printed F: a typo in F, not a bad decode)."""
    if not r["seq"]: return False
    if "?" not in r["kind"]: return True
    return r["kind"] == "hex-full?" and bool(r["implied"]) and abs(int(r["E"]) - int(r["implied"])) <= 0.005 * int(r["implied"])

out = Path(sys.argv[2]); (out / "seeds").mkdir(parents=True, exist_ok=True)
base, seqs = {}, {}
for r in rows:
    L = int(r["L"]); vals = []
    if r["implied"]: vals.append((int(r["implied"]), r["src"] + ":printed"))
    if r["E"]: vals.append((int(r["E"]), r["src"] + ":seq" + ("" if "?" not in r["kind"] else "(unverified decode)")))
    for v, s in vals:
        b = base.setdefault(L, [10 ** 9, set()])
        if v < b[0]: base[L] = [v, {s}]
        elif v == b[0]: b[1].add(s)
    if ok_parent(r):
        seqs.setdefault(L, set()).add(r["seq"])
def edits(s, L, KT=8, KA=3):
    import itertools
    n = len(s); out = []
    if 1 <= L - n <= KA:
        k = L - n
        out = [b[:i] + s + b[i:] for b in ("".join(x) for x in itertools.product("01", repeat=k)) for i in range(k + 1)]
    if 1 <= n - L <= KT:
        k = n - L
        out = [s[i:n - (k - i)] for i in range(k + 1)]
    return out
with open(out / "baseline.tsv", "w") as f, open(out / "gaps.tsv", "w") as g:
    f.write("L\tbaseline_E\tattained_by\n"); g.write("L\tbaseline_E\tbest_edit_E\tgap\tedit_from\n")
    for L in range(67, 1100):
        cands = {}
        for s in seqs.get(L, ()): cands[s] = ("published L", energy([1 if c == "0" else -1 for c in s]))
        for M in [m for m in range(L - 3, L + 9) if m != L]:
            for s in seqs.get(M, ()):
                for e in edits(s, L):
                    if e not in cands: cands[e] = (f"{abs(M - L)}-element edit of L={M}", energy([1 if c == "0" else -1 for c in e]))
        if L in base: f.write(f"{L}\t{base[L][0]}\t{','.join(sorted(base[L][1]))}\n")
        if not cands: continue
        ranked = sorted(cands.items(), key=lambda kv: kv[1][1])
        (out / "seeds" / f"{L}.txt").write_text("".join(f"{e} {s}\n" for s, (_, e) in ranked[:60]))
        bestE, src = ranked[0][1][1], ranked[0][1][0]
        if L in base: g.write(f"{L}\t{base[L][0]}\t{bestE}\t{base[L][0] - bestE}\t{src}\n")
