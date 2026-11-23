#!/usr/bin/env python3
"""Standalone checker for the ebl-fragment-identification claim
(BM.68403 -> /L/3/10/Standard Babylonian/-, partial win p2).

Stdlib only (no numpy, no network). Re-derives every claim property from the
object/ files:
  (b) top-hit alignment, using a pure-python port of the frozen C aligner
      (how-we-built-it/code/swalign.c; verified result-equivalent, see RECEIPTS.md)
  (b/attested) the attested-vs-restored split of the matched block
  (c) the frozen p-rule arithmetic from the saved K=1,000,000 null summary
  (d) eBL public ngram-matcher TF-IDF top-10 (re-implementation, commit e8918de)
  (e) recurrence of the matched block in unrelated compositions
  (a) the frozen unplaced-fragment rule (joins / manuscript link / naming)
and the sha256 of every object file against the pins below.

Last output line: PASS or FAIL.
"""
import json, math, os, re, sys, hashlib, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OBJ = os.path.join(ROOT, "object")

CLAIMED = "/L/3/10/Standard Babylonian/-"
FID = "BM.68403"

# object-file integrity pins (computed at packaging; a corrupted object fails here)
PIN_SHAS = {
    "BM.68403_signs.json": "845706d7933717f74351682c6baa62b4b39d1a3588b8970bd89e220378e1e546",
    "corpus_signs.json": "3ffd6f0485c564d15a4eaf3d34da0c20badda29ecab4c04e295b7e4d274493de",
    "corpus_toks.json": "3558b899f7050c68b0d0e6a01bfd40d0f4b5e35052740d197d61d7b03cf3af81",
    "null_result_BM.68403.json": "7ea5afa4fc44f7e45c5bb8f79ad970867cd8e047b9c173f90e666f0773deb21f",
    "object_BM.68403.json": "c68769c18bea0ad8e43b566566bef91be41150d5f9ab0875067dc699e0766200",
    "record_BM.68403.json": "373beff3f84f61283e8e9a909e0b77fd523bac73b3c45f26dfa05fd19d80f1fe",
}
PIN_HWB = {
    "data/fragments_all_signs.json": "8038665b1eb4c467d49c2ad46bd008544e84b0bac7dace24eebf856b6c77b26c",
    "code/swalign.c": "2e92d05cad100bc0a65b49766b29056425db5d7d06c2ecbbd94d98d6bf627c9e",
}

fails = []

def fail(msg):
    fails.append(msg)
    print("FAIL:", msg)

def ok(msg):
    print("ok:", msg)

# ---------------------------------------------------------------- (b) aligner
# Pure-python port of the frozen C aligner (swalign.c): Smith-Waterman local
# alignment, match +3 / mismatch -1 / gap -2 / wildcard(X vs real) +1, min_block 6,
# deterministic tie-break (diag >= up >= left: up wins a tie vs diag, left must
# strictly exceed). Result-equivalent with swalign.so on this corpus (RECEIPTS.md).
X_CODE = -1

def sw_align(a, a_line, b, b_line, match=3, mismatch=-1, gap=-2, xmatch=1, min_block=6):
    n, m = len(a), len(b)
    if n <= 0 or m <= 0:
        return None
    H = [[0] * (m + 1) for _ in range(n + 1)]
    TR = [[0] * (m + 1) for _ in range(n + 1)]
    best = 0
    bi = 0
    bj = 0
    for i in range(1, n + 1):
        ai = a[i - 1]
        Hi = H[i]
        Hm = H[i - 1]
        TRi = TR[i]
        for j in range(1, m + 1):
            bv = b[j - 1]
            if ai == bv:
                s = match
            elif ai == X_CODE or bv == X_CODE:
                s = xmatch
            else:
                s = mismatch
            d = Hm[j - 1] + s
            u = Hm[j] + gap
            l = Hi[j - 1] + gap
            v = d
            t = 0
            if u >= v:
                v = u
                t = 1
            if l > v:
                v = l
                t = 2
            Hi[j] = v
            TRi[j] = t
            if v > best:
                best = v
                bi = i
                bj = j
    if best <= 0:
        return None
    i, j = bi, bj
    aligned = 0
    mism = 0
    wild = 0
    alo = 10 ** 9
    ahi = -1
    blo = 10 ** 9
    bhi = -1
    guard = 0
    maxg = n + m + 4
    while i > 0 and j > 0 and H[i][j] > 0 and guard < maxg:
        guard += 1
        t = TR[i][j]
        if t == 0:
            ai = a[i - 1]
            bv = b[j - 1]
            aligned += 1
            if ai != bv:
                if ai == X_CODE or bv == X_CODE:
                    wild += 1
                else:
                    mism += 1
            li = a_line[i - 1]
            lj = b_line[j - 1]
            if li < alo:
                alo = li
            if li > ahi:
                ahi = li
            if lj < blo:
                blo = lj
            if lj > bhi:
                bhi = lj
            i -= 1
            j -= 1
        elif t == 1:
            i -= 1
        else:
            j -= 1
    if ahi < 0:
        ahi = 0
    if alo > ahi:
        alo = ahi
    if bhi < 0:
        bhi = 0
    if blo > bhi:
        blo = bhi
    if aligned < min_block:
        return None
    return {
        "score": best, "aligned": aligned, "mismatches": mism, "wildcards": wild,
        "consec_lines_a": ahi - alo + 1, "consec_lines_b": bhi - blo + 1,
        "a_line_span": (alo, ahi), "b_line_span": (blo, bhi),
        "mismatch_frac": (mism / aligned) if aligned else 0.0,
    }

# ------------------------------------------------------- normalisation (frozen)
def normalise_token(t):
    t = unicodedata.normalize("NFC", t).strip()
    if t == "":
        return None
    if "/" in t:
        t = t.split("/", 1)[0].strip()
        t = unicodedata.normalize("NFC", t)
    return t

def normalise_signs(signs):
    if isinstance(signs, (list, tuple)):
        signs = signs[0] if signs else ""
    if not isinstance(signs, str):
        signs = ""
    lines = []
    for raw in signs.split("\n"):
        toks = [normalise_token(x) for x in raw.split()]
        lines.append(tuple(x for x in toks if x is not None))
    return lines

# ---------------------------------------------------------------- (d) TF-IDF
def tfidf_top10(signs, chapters, n_values=(1, 2, 3)):
    """Re-implementation of eBL's public ngram-matcher TF-IDF strategy (commit
    e8918de): n-grams n in 1..3 of the raw sign tokens (X-free, X-only lines
    dropped), idf = log(N/(df+1)) + 1, N = nchapters+1. Frozen from
    how-we-built-it/code/search2.py::tfidf_top10."""
    def preprocess(signs):
        lines = [l.strip() for l in signs.split("\n")]
        lines = [l for l in lines if not re.fullmatch(r"[X\s]*", l)]
        return (" ".join(lines)).split()

    def ngrams_seq(seq, n):
        return {tuple(seq[i:i + n]) for i in range(max(0, len(seq) - n + 1))}

    def grams_doc(signs):
        toks = preprocess(signs)
        g = set()
        for n in n_values:
            g |= ngrams_seq(toks, n)
        return {g2 for g2 in g if "X" not in g2}

    fg = grams_doc(signs)
    doc_grams = [grams_doc(c["signs"]) for c in chapters]
    df = {g: sum(1 for dg in doc_grams if g in dg) for g in fg}
    N = len(chapters) + 1
    idf = {g: math.log(N / (df[g] + 1)) + 1 for g in fg}
    scores = []
    for ci, dg in enumerate(doc_grams):
        sc = sum(idf[g] for g in (fg & dg))
        scores.append((sc, ci))
    scores.sort(key=lambda x: (-x[0], x[1]))
    return [(chapters[ci]["cid"], sc) for sc, ci in scores[:10]], fg

# ---------------------------------------------------------------- (a) rule
def canon(s):
    return s.replace(".", "").replace(",", "").lower()

def strip_diac(s):
    out = []
    for ch in unicodedata.normalize("NFKD", s.lower()):
        if unicodedata.category(ch) == "Mn":
            continue
        out.append(ch)
    return "".join(out)

# frozen series names per (genre, category) (from how-we-built-it/code/check_a.py)
SERIES = {
    ("L", 1): ["lexical"], ("L", 2): ["lexical"], ("L", 3): ["lexical"],
    ("L", 10): ["anzu", "anzu list", "an-zu"], ("L", 11): ["lexical"],
    ("L", 12): ["lexical"], ("D", 1): ["enuma anu enlil", "eae", "summa alu", "almu"],
    ("D", 2): ["summa alu", "eae", "enuma anu enlil", "summa alu apical"],
    ("D", 3): ["summa alu"], ("D", 4): ["summa alu", "eae"],
    ("D", 5): ["enuma anu enlil", "eae"], ("Mag", 1): ["sui", "shuila", "prayer", "complaint"],
    ("Mag", 2): ["sui", "shuila", "prayer", "complaint"], ("Mag", 3): ["sui", "shuila"],
    ("Mag", 4): ["sui", "shuila"], ("Mag", 6): ["sui", "shuila"],
    ("Mag", 7): ["sui", "shuila"], ("Mag", 11): ["sui", "shuila"],
    ("Mag", 13): ["sui", "shuila"], ("Mag", 31): ["sui", "shuila"],
    ("Med", 1): ["medical", "diagnostic"],
}

def chapter_series(chap):
    genre, cat, idx = chap["textid"]
    names = set(SERIES.get((genre, cat), []))
    names.add(strip_diac(str(genre)))
    return {n for n in names if n}

def chapter_number_tokens(chap):
    genre, cat, idx = chap["textid"]
    nm = str(chap.get("name", "")).strip()
    toks = set()
    if nm:
        toks.add(nm)
        if nm[:1].isalpha() and nm[1:].isdigit():
            toks.add(nm[1:])
    toks.add(str(idx))
    toks.add(str(int(idx)))
    return {t for t in toks if t and len(t) >= 1}

def record_text(rec):
    parts = []
    for r in (rec.get("references") or []):
        parts.append(r.get("notes") or "")
        d = r.get("document") or {}
        parts.append(d.get("title") or "")
        parts.append(d.get("collection-title") or "")
    for u in (rec.get("uncuratedReferences") or []):
        if isinstance(u, dict):
            parts.append(u.get("notes") or "")
            parts.append(str(u.get("reference") or u.get("text") or ""))
        else:
            parts.append(str(u))
    n = rec.get("notes") or {}
    parts.append(n.get("text") or "")
    for ds in (rec.get("dossiers") or []):
        if isinstance(ds, dict):
            parts.append(ds.get("notes") or "")
            parts.append(str(ds.get("id") or ds.get("name") or ""))
        else:
            parts.append(str(ds))
    for g in (rec.get("genres") or []):
        if isinstance(g, dict):
            parts.append(" ".join(g.get("category") or []))
        elif isinstance(g, list):
            parts.append(" ".join(str(x) for x in g))
    return " || ".join(p for p in parts if p)

def names_composition(rec, chap):
    txt = strip_diac(record_text(rec))
    series = chapter_series(chap)
    nums = chapter_number_tokens(chap)
    series_hit = None
    for s in sorted(series, key=len, reverse=True):
        if len(s) >= 3 and re.search(r"(?<![a-z0-9])" + re.escape(strip_diac(s)) + r"(?![a-z0-9])", txt):
            series_hit = s
            break
    num_hit = None
    for t in sorted(nums, key=len, reverse=True):
        tt = strip_diac(t)
        if len(tt) >= 1 and re.search(r"(?<![a-z0-9])" + re.escape(tt) + r"(?![a-z0-9])", txt):
            num_hit = t
            break
    if series_hit and num_hit:
        return True, "series + number both present", False
    if series_hit:
        return False, f"series name '{series_hit}' present (genre-level), number not -> partial", True
    if num_hit:
        return False, f"number '{num_hit}' present without series name -> partial", True
    return False, "", False

# ------------------------------------------------------------ (b/attested)
def attestation(rec, fragsigns, span_a):
    """Frozen attested-position rule (how-we-built-it/code/attested.py): map the
    k-th non-empty sign line to the k-th content line of the record's text; a line
    is ATTESTED iff its content line has no BROKEN_AWAY-enclosed word."""
    slines = fragsigns.split("\n")
    nonempty = [(i, l) for i, l in enumerate(slines) if l.strip()]
    txt = rec.get("text") or {}
    content = [L for L in (txt.get("lines") or []) if L.get("type") not in ("SurfaceAtLine", "LineNumber")]
    broken = []
    for L in content:
        b = 0
        for c in (L.get("content") or []):
            if c.get("type") in ("Word", "ValueToken"):
                if any(e == "BROKEN_AWAY" for e in (c.get("enclosureType") or [])):
                    b += 1
        broken.append(b)

    def line_attested(sign_line_idx):
        k = None
        for idx, (oi, l) in enumerate(nonempty):
            if oi == sign_line_idx:
                k = idx
                break
        if k is None:
            return None
        ci = min(k, len(content) - 1) if content else 0
        return (broken[ci] == 0) if content else True

    lo, hi = span_a
    att_lines = 0
    rest_lines = 0
    n_lines = 0
    att_signs = 0
    rest_signs = 0
    for oi, l in nonempty:
        if lo <= oi <= hi:
            n_lines += 1
            a = line_attested(oi)
            nsigns = sum(1 for t in l.split() if t != "X")
            if a:
                att_lines += 1
                att_signs += nsigns
            else:
                rest_lines += 1
                rest_signs += nsigns
    tot = att_signs + rest_signs
    return {"attested_lines": att_lines, "restored_lines": rest_lines, "n_lines": n_lines,
            "attested_signs": att_signs, "restored_signs": rest_signs, "n_signs": tot,
            "attested_frac_signs": (att_signs / tot) if tot else 0.0,
            "attested_frac_lines": (att_lines / n_lines) if n_lines else 0.0}

# ------------------------------------------------------------------ main
def main():
    # integrity pins
    def sha(p):
        return hashlib.sha256(open(p, "rb").read()).hexdigest()

    for f in list(PIN_SHAS) + list(PIN_HWB):
        base = os.path.join(OBJ, f) if f in PIN_SHAS else os.path.join(ROOT, "how-we-built-it", f)
        if not os.path.isfile(base):
            fail(f"missing {base}")
            continue
        h = sha(base)
        expect = PIN_SHAS.get(f) or PIN_HWB.get(f)
        if h != expect:
            fail(f"sha mismatch {f} (expected {expect[:16]}..., got {h[:16]}...) [object corrupted?]")
    if not fails:
        ok("object-file sha256: all pins match")

    obj = json.load(open(os.path.join(OBJ, "object_BM.68403.json")))
    nr = json.load(open(os.path.join(OBJ, "null_result_BM.68403.json")))
    frag = json.load(open(os.path.join(OBJ, "BM.68403_signs.json")))
    rec = json.load(open(os.path.join(OBJ, "record_BM.68403.json")))
    corpus = json.load(open(os.path.join(OBJ, "corpus_toks.json")))
    signs = json.load(open(os.path.join(OBJ, "corpus_signs.json")))

    vocab = corpus["vocab"]
    def dec(toks):
        return [[vocab[i] for i in line] for line in toks]
    chaps = []
    for cid, c in corpus["chapters"].items():
        chaps.append({"cid": cid, "textid": tuple(c["t"]), "name": c.get("name", cid.rsplit("/", 1)[-1]),
                      "ms": c["ms"], "toks": [tuple(l) for l in dec(c["toks"])], "signs": signs[cid]})
    chaps.sort(key=lambda c: (c["textid"], c["name"]))
    claimed = [c for c in chaps if c["cid"] == CLAIMED]
    if len(claimed) != 1:
        fail(f"claimed chapter {CLAIMED} not uniquely present in corpus_toks.json")
        return report()
    claimed = claimed[0]

    # ---- (b) top-hit alignment, frozen aligner (pure-python port)
    frag_toks = normalise_signs(frag["signs"])
    res = []
    # intern
    code = {}
    def enc(lins):
        out = []
        lin = []
        for li, l in enumerate(lins):
            for t in l:
                if t not in code:
                    code[t] = len(code)
                out.append(X_CODE if t == "X" else code[t])
                lin.append(li)
        return out, lin
    fa, fl = enc([list(l) for l in frag_toks])
    chap_enc = [(c["cid"], *enc([list(l) for l in c["toks"]])) for c in chaps]
    for cid, ba, bl in chap_enc:
        r = sw_align(fa, fl, ba, bl)
        if r:
            res.append((r["score"], cid, r))
    res.sort(key=lambda t: (-t[0], t[1]))
    if not res:
        fail("(b) no alignment with score > 0 found")
        return report()
    sc, topcid, tr = res[0]
    print(f"(b) re-derived top hit: {topcid} score {sc} aligned {tr['aligned']} "
          f"misfrac {round(tr['mismatch_frac'], 4)} consec_lines_a {tr['consec_lines_a']} "
          f"a_span {tr['a_line_span']} b_span {tr['b_line_span']}")
    b = obj["alignment"]
    if not (topcid == obj["chapter"] == CLAIMED and sc == b["score"] == 612
            and tr["aligned"] == b["aligned"] == 270
            and round(tr["mismatch_frac"], 4) == b["mismatch_frac"]
            and tr["consec_lines_a"] == b["consec_lines_a"] == 24
            and tr["a_line_span"] == tuple(b["a_line_span"])
            and tr["b_line_span"] == tuple(b["b_line_span"])):
        fail("(b) re-derived top hit differs from object_BM.68403.json")
    else:
        ok("(b) top hit matches object (score/aligned/misfrac/consec/spans)")
    # (b) criterion bar: >=15 consecutive signs or >=3 consecutive lines, <=10% mismatch
    bar_b = (tr["aligned"] >= 15 or tr["consec_lines_a"] >= 3) and tr["mismatch_frac"] <= 0.10
    if not bar_b:
        fail("(b) criterion bar not met by re-derived alignment")
    else:
        ok(f"(b) criterion bar (>=15 signs or >=3 lines, <=10% mismatch): met ({tr['aligned']} signs, {tr['consec_lines_a']} lines)")

    # ---- (b/attested) split
    a = attestation(rec, frag["signs"], tr["a_line_span"])
    print(f"(b/attested) attested_lines {a['attested_lines']}/{a['n_lines']} "
          f"attested_signs {a['attested_signs']}/{a['n_signs']} "
          f"(restoration pitfall: ~{100 - round(a['attested_frac_signs'] * 100)}% of block signs restored)")
    ob = b.get("attested", {})
    if not (a["attested_lines"] == ob.get("attested_lines") == 11
            and a["attested_signs"] == ob.get("attested_signs") == 128
            and a["n_lines"] == ob.get("n_lines") == 24
            and a["n_signs"] == ob.get("n_signs") == 281):
        fail("(b/attested) re-derived split differs from object")
    else:
        ok("(b/attested) split matches object (flagged, not a (b) sub-clause)")

    # ---- (c) frozen p-rule arithmetic from the saved K=1,000,000 summary
    K, N, real = nr["K"], nr["N"], nr["real"]
    p_raw = (1 + nr["n_ge"]) / (K + 1)
    p_bonf = min(1.0, p_raw * N)
    beats = nr["control_max"] < real
    print(f"(c) K={K} N={N} real={real} control_max={nr['control_max']} n_ge={nr['n_ge']} "
          f"p_raw={p_raw:.4e} p_bonf={p_bonf:.4e} p_bonf<1e-4={p_bonf < 1e-4} beats_all={beats}")
    if not (K == 1000000 and N == 40 and real == 612 and nr["n_ge"] == 0
            and p_bonf < 1e-4 and beats and abs(p_bonf - nr["p_bonf"]) < 1e-12
            and obj["condition_c"]["pass"] is True and obj["condition_c"]["beats_all_controls"] is True):
        fail("(c) p-rule arithmetic or saved summary inconsistent")
    else:
        ok("(c) p_bonf < 1e-4 and real beats every control (frozen rule, N=|S|=40)")

    # ---- (d) TF-IDF top-10 (eBL public ngram-matcher re-implementation)
    top10, _ = tfidf_top10(frag["signs"], chaps)
    rank = next((i for i, (c, _) in enumerate(top10) if c == CLAIMED), -1)
    in_top10 = rank >= 0
    print(f"(d) TF-IDF top-10 re-derived: rank of {CLAIMED} = {rank} (in top-10: {in_top10})")
    print(f"(d) re-derived top-3: {[c for c, _ in top10[:3]]}")
    if not (in_top10 and top10[0][0] == obj["condition_d"]["tfidf_top10"][0] == CLAIMED
            and [c for c, _ in top10] == obj["condition_d"]["tfidf_top10"]):
        fail("(d) re-derived TF-IDF top-10 differs from object")
    else:
        ok("(d) re-derived TF-IDF top-10 matches object (claimed chapter rank 0; p2 requires top-10 presence)")

    # ---- (e) recurrence of the matched block in unrelated compositions
    lo, hi = tr["a_line_span"]
    block = [list(frag_toks[i]) for i in range(lo, hi + 1)]
    block_signs = sum(len(l) for l in block)
    thr = max(15, int(0.4 * block_signs))
    ba, bl = enc(block)
    hits = []
    textids = set()
    for c in chaps:
        if c["cid"] == CLAIMED:
            continue
        r = sw_align(ba, bl, *enc([list(l) for l in c["toks"]]))
        if r and r["aligned"] >= thr and r["mismatch_frac"] <= 0.10:
            textids.add(c["textid"])
            hits.append((c["cid"], r["aligned"], round(r["mismatch_frac"], 3)))
    e_pass = len(textids) < 5
    print(f"(e) block {hi - lo + 1} lines / {block_signs} signs, threshold {thr} -> "
          f"distinct unrelated textIds: {len(textids)} {sorted(textids)} e_pass(<5): {e_pass}")
    if hits:
        print(f"(e) hits: {hits[:5]}")
    oe = obj["condition_e"]
    if not (len(textids) == oe["e_n_unrelated"] == 1 and e_pass is True
            and oe["e_pass"] is True and sorted(textids) == [tuple(t) for t in oe["e_textids"]]):
        fail("(e) re-derived recurrence count differs from object")
    else:
        ok("(e) block recurs in exactly 1 unrelated textId (< 5): not a formula")

    # ---- (a) unplaced-fragment rule (frozen, offline over the saved record)
    joins = rec.get("joins") or []
    mnum = rec.get("museumNumber") or {}
    mnstr = f"{mnum.get('prefix', '')}{mnum.get('number', '')}{mnum.get('suffix', '')}"
    ms_union = set()
    for c in chaps:
        ms_union.update(c["ms"])
    ms_link = canon(mnstr) in ms_union
    named, ev, partial = names_composition(rec, claimed)
    pass_a = (not joins) and (not ms_link) and (not named)
    print(f"(a) joins==[]: {not joins}; museum-number chapter ms-link: {ms_link}; "
          f"naming: {ev or 'none'} -> pass_a={pass_a}{' (partial flagged)' if partial else ''}")
    oa = obj["condition_a"]
    if not (pass_a is True and oa["pass_a"] is True and not oa["fails"] and len(oa.get("partials", [])) == (1 if partial else 0)):
        fail("(a) re-derived unplaced check differs from object")
    else:
        ok("(a) unplaced (joins empty, no chapter manuscript link, no naming; genre-level 'lexical' partial flagged)")

    return report()

def report():
    if fails:
        print("FAIL")
        return 1
    print("PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
