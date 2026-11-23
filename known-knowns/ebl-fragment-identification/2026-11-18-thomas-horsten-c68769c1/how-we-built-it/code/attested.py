#!/usr/bin/env python3
"""Attested-position re-check (bank pitfall): the public 'signs' field encodes editorial
restorations like attested signs. For each claimed match, map the fragment's sign lines to
its record's content lines (i-th non-empty sign line -> i-th content line; both are the
fragment's own line sequence), and treat a sign line as ATTESTED if its content line has no
BROKEN_AWAY-enclosed word. Report the attested vs restored split of every claimed match and
the attested-only (b) metric."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data"
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/output"

def attestation(fid, span_a):
    """span_a: (lo, hi) inclusive sign-line indices (from the alignment, 0-based into the
    non-empty sign lines). Returns dict with per-line attested flags + split counts over the
    block."""
    rec = json.load(open(f"{DATA}/records/{fid.replace('/','_').replace(',','_')}.json"))
    signs = json.load(open(f"{DATA}/fragments_all_signs.json"))
    # load fragment signs
    import json as _j
    fragsigns = None
    for x in _j.load(open(f"{DATA}/fragments_all_signs.json")):
        if x["_id"] == fid:
            fragsigns = x["signs"]; break
    slines = fragsigns.split("\n")
    # non-empty sign lines, with their original index
    nonempty = [(i, l) for i, l in enumerate(slines) if l.strip()]
    txt = rec.get("text") or {}
    content = [L for L in (txt.get("lines") or []) if L.get("type") not in ("SurfaceAtLine", "LineNumber")]
    # per content line: number of BROKEN_AWAY words
    broken = []
    for L in content:
        b = 0
        for c in (L.get("content") or []):
            if c.get("type") in ("Word", "ValueToken"):
                if any(e == "BROKEN_AWAY" for e in (c.get("enclosureType") or [])):
                    b += 1
        broken.append(b)
    # map: k-th non-empty sign line -> min(k, len(content)-1)-th content line
    def line_attested(sign_line_idx):
        # find which non-empty ordinal this sign line is
        k = None
        for idx, (oi, l) in enumerate(nonempty):
            if oi == sign_line_idx:
                k = idx; break
        if k is None:
            return None
        ci = min(k, len(content) - 1) if content else 0
        return (broken[ci] == 0) if content else True
    lo, hi = span_a
    # block = non-empty sign lines with index in [lo,hi]
    att_lines = 0; rest_lines = 0; n_lines = 0
    att_signs = 0; rest_signs = 0
    for oi, l in nonempty:
        if lo <= oi <= hi:
            n_lines += 1
            a = line_attested(oi)
            toks = [t for t in l.split()]
            nsigns = sum(1 for t in toks if t != "X")
            if a:
                att_lines += 1; att_signs += nsigns
            else:
                rest_lines += 1; rest_signs += nsigns
    tot = att_signs + rest_signs
    return {
        "fid": fid, "span_a": [lo, hi],
        "attested_lines": att_lines, "restored_lines": rest_lines, "n_lines": n_lines,
        "attested_signs": att_signs, "restored_signs": rest_signs, "n_signs": tot,
        "attested_frac_signs": (att_signs / tot) if tot else 0.0,
        "attested_frac_lines": (att_lines / n_lines) if n_lines else 0.0,
    }

if __name__ == "__main__":
    S = json.load(open(f"{OUT}/S.json"))
    checka = json.load(open(f"{OUT}/check_a.json"))
    passA = {x["fid"]: x for x in checka if x["pass_a"]}
    res = []
    for s in S:
        b = s["best"]
        a = attestation(s["fid"], b["a_line_span"])
        # attested-only (b): does the block still clear the bar using ATTESTED lines/signs?
        att_full = (a["attested_lines"] >= 3 or a["attested_signs"] >= 15)
        res.append({**a, "chapter": b["chapter"], "pass_a": s["fid"] in passA,
                    "score": b["score"], "aligned": b["aligned"], "mismatch_frac": b["mismatch_frac"],
                    "consec_lines_a": b["consec_lines_a"],
                    "attested_full_bar": att_full})
    json.dump(res, open(f"{OUT}/attested.json", "w"), indent=1)
    print(f"{'fid':>16} {'a':>4} {'score':>5} {'aligned':>6} {'misfrac':>7} {'attL/restL':>10} {'attS/restS':>10} {'attFull':>7}")
    for r in res:
        print(f"{r['fid']:>16} {'Y' if r['pass_a'] else 'n':>4} {r['score']:>5} {r['aligned']:>6} "
              f"{r['mismatch_frac']:>7.3f} {r['attested_lines']}/{r['restored_lines']:>7} "
              f"{r['attested_signs']}/{r['restored_signs']:>8} {'Y' if r['attested_full_bar'] else 'n':>7}")
