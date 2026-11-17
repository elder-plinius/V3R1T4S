"""Shared data pipeline for the Indus temporal held-out structure run.

Loads M77 (joyboseroy CSV = the bank's M77 training source, MSg codes, reading
order R-L) and attaches object type / site / field symbol from paragorth's
im77 export (aligned by (text_no, line)). Builds the post-1977 held-out set
from paragorth's merged-corpus-reading-order.json (Wells coding), mapped to
Mahadevan codes via bridge_extended.json.

Everything here is deterministic (fixed seed, sorted iteration). No model is
fitted in this module.
"""
import csv, json, os, collections, math

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)
DATA = os.path.join(RUN, "data")  # nulltest runs from code/ (RUN=code)

def load_merged():
    return json.load(open(os.path.join(DATA, "merged-corpus-reading-order.json")))

def load_idmap():
    return json.load(open(os.path.join(DATA, "identity-directory.json")))

def load_bridge():
    return json.load(open(os.path.join(DATA, "bridge_extended.json")))

def load_m77_lines():
    """joyboseroy M77: list of dicts with obj, line_idx (0-based in-file order per obj), signs (tuple of int)."""
    rows = list(csv.DictReader(open(os.path.join(DATA, "m77_indusscript_real_corpus.csv"))))
    out = []
    for r in rows:
        o = int(r["inscription_id"].split(".")[0])
        signs = tuple(int(s.replace("MSg", "")) for s in r["sign_sequence"].split() if int(s.replace("MSg", "")) != 0)
        out.append({"obj": o, "line": int(r["line_count"]), "seq": signs, "raw": r})
    return out

def load_im77():
    rows = list(csv.DictReader(open(os.path.join(DATA, "im77_corpus_lines.csv"))))
    idx = {}
    for r in rows:
        txt = int(r["text_no"])
        idx.setdefault(txt, []).append(r)
    for v in idx.values():
        v.sort(key=lambda r: int(r["line"]) if r["line"].isdigit() else 99)
    return idx

def m77_training():
    """M77 training records: one per joyboseroy line, with im77-aligned metadata.

    Returns list of dicts: seq (tuple of Mahadevan-int codes), obj, site, otype,
    fs (family string or None), fs80, direction. Lines with object_type in
    {seal, sealing, tablet...} keep the im77 type; field symbol family mapped
    via im77_field_symbols.csv.
    """
    m77 = load_m77_lines()
    im77 = load_im77()
    # pair the k-th joyboseroy row for an object with the k-th im77 line (file order).
    # joyboseroy's line_count column is NOT a reliable 1-based line index (verified 2026-11-17:
    # object 1001 has two rows both with line_count=1). im77 lines are sorted by their `line` field.
    per_obj = collections.defaultdict(list)
    for r in m77:
        per_obj[r["obj"]].append(r)
    fsmap = {}
    for r in csv.DictReader(open(os.path.join(DATA, "im77_field_symbols.csv"))):
        fsmap[int(r["fs80"])] = (r["fs_category"], r["description"])
    fam_of = {}
    def fam(cat, desc):
        d = (desc or "").lower()
        for kw, lab in [("unicorn", "Unicorn"), ("rhinoceros", "Rhino"), ("elephant", "Elephant"),
                        ("tiger", "Tiger"), ("antelope", "Antelope"), ("buffalo", "Buffalo"),
                        ("zebu", "Zebu"), ("gaur", "Gaur"), ("bull", "Bull")]:
            if kw in d:
                return lab
        if cat == "Animals":
            return "OtherAnimal"
        if cat in ("No field symbol",):
            return None
        return "Other"
    recs = []
    n_obj_mis = 0
    for txt, rows in sorted(per_obj.items()):
        im = im77.get(txt, [])
        for j, r in enumerate(rows):
            if j < len(im):
                row = im[j]
                otype = row["object_type"]
                site = row["site"]
                fs80 = int(row["fs80"]) if row["fs80"].isdigit() else 0
                cat, desc = fsmap.get(fs80, ("", ""))
                fs = fam(cat, desc) if fs80 > 0 else None
                direction = row["direction"]
            else:
                otype, site, fs80, fs, direction = "unknown", "unknown", 0, None, "unknown"
                n_obj_mis += 1
            if not r["seq"]:
                continue
            recs.append({"seq": r["seq"], "obj": txt, "line": r["line"], "site": site,
                         "otype": otype, "fs": fs, "fs80": fs80, "direction": direction})
    return recs

def m77_object_types():
    """Map merged-corpus type strings -> 4-class object type for the full criterion."""
    def cls(t):
        t = (t or "").upper()
        if t.startswith("SEAL") or t.startswith("TAG"):
            return "Seal"
        if t.startswith("TAB") or t.startswith("BNGL") or t.startswith("ROD") or t.startswith("COPPER"):
            return "Tablet"
        if t.startswith("POT"):
            return "Pottery"
        return "Other"
    return cls

def db_symbol_family(sym):
    """DB symbol string -> family label.

    DB coding note (paragorth/Indus- STRATEGIES.md S65, read as data): the DB's "Bull1*"
    emblems are UNICORN seals ("the unicorn ('Bull1') is on 1,229 square seals"; the :W/J/S/I/L/U
    suffixes are carving-style codes, S-DARK-14.3). M77's fs80 descriptions use the animal name
    directly. The cross-coding artifact is recorded in the lens reports.
    """
    if sym in (None, "", "-"):
        return None
    sl = sym.lower()
    if sl.startswith("bull1") or sl == "bull1":
        return "Unicorn"
    for key, lab in [("unicorn", "Unicorn"), ("rhin", "Rhino"), ("elep", "Elephant"),
                     ("tigr", "Tiger"), ("antelop", "Antelope"), ("buffalo", "Buffalo"),
                     ("zebu", "Zebu"), ("gavi", "Gaur"), ("gaur", "Gaur"),
                     ("bult", "Bull"), ("bull", "Bull")]:
        if sl.startswith(key) or key in sl:
            return lab
    return "Other"

def heldout_objects(merged, bridge, m77_rec_seqs, idkeys=None, sites=None, min_len=2):
    """Post-1977 held-out objects with M77 mapping, dedup (in-M77 seq drop + identity dedup).

    Returns list of dicts: seq_w (Wells tuple), seq_m (mapped M77 tuple or None if any OOV),
    otype (4-class), site, symbol family, cisi, in_m77 (bool), identity core set, complete.
    """
    def mapseq(wells):
        out = []
        oov = False
        for s in wells:
            m = bridge.get(str(s))
            if not m:
                oov = True
                break
            # a bridge entry with several candidates is ambiguous: use the first (fixed order);
            # empty entries (832, 65, 794) mean OOV. Recorded in PREREG.v2 as a frozen rule.
            out.append(m[0])
        return tuple(out) if not oov else None
    m77seqset = set(m77_rec_seqs)
    idkeys = idkeys if idkeys is not None else identity_keys()
    kept = []
    for r in merged:
        s = [x for x in r["seq"] if x != 0]
        if len(s) < min_len:
            continue
        if sites and r.get("site") not in sites:
            continue
        seqm = mapseq(s)
        ids = set()
        st = tuple(s)
        for k in idkeys:
            for i in range(len(st) - len(k) + 1):
                if st[i:i + len(k)] == k:
                    ids.add(k)
                    break
        kept.append({
            "cisi": r.get("cisi", ""), "site": r.get("site"), "type": r.get("type", ""),
            "otype": m77_object_types()(r.get("type")), "symfam": db_symbol_family(r.get("symbol")),
            "seq_w": tuple(s), "seq_m": seqm, "in_m77": tuple(s) in m77seqset or (seqm is not None and seqm in m77seqset),
            "ids": ids, "complete": r.get("complete"), "period": r.get("period"),
        })
    # identity dedup: union-find over objects sharing an identity core
    parent = list(range(len(kept)))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def un(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    for i in range(len(kept)):
        for j in range(i + 1, len(kept)):
            if kept[i]["ids"] & kept[j]["ids"]:
                un(i, j)
    reps = []
    seen = set()
    for i in range(len(kept)):
        g = find(i)
        if g not in seen:
            seen.add(g)
            reps.append(kept[i])
    return reps, kept

def identity_keys(idmap=None):
    idmap = idmap or load_idmap()
    keys = set()
    for k in idmap:
        parts = []
        for x in k.split("+"):
            base = x.split(":")[0]
            if base.isdigit():
                parts.append(int(base))
        if parts:
            keys.add(tuple(parts))
    # drop keys of length 1 that are too generic (single-sign cores of the most common signs)
    freq = collections.Counter()
    for k in keys:
        freq[len(k)] += 1
    return sorted(keys, key=len, reverse=True)

def ent(counter, tot):
    if tot == 0:
        return 0.0
    H = 0.0
    for c in counter.values():
        if c > 0:
            p = c / tot
            H -= p * math.log2(p)
    return H
def identity_keys_minlen(idmap=None, nmin=2):
    return [k for k in identity_keys(idmap) if len(k) >= nmin]


def m77_wells_inverse(bridge):
    """Inverse of the first-candidate bridge rule (frozen; deterministic)."""
    inv = {}
    for w, cands in bridge.items():
        if cands:
            m = cands[0]
            wint = int(w)
            if m not in inv or wint < inv[m]:
                inv[m] = wint
    return inv


def build_pool_v2():
    """PREREG.v2 held-out pool (2026-11-17T03:25Z). Returns (reps, kept, info).

    Rules (frozen in PREREG.v2.md): post-1977 pool (Dholavira, Lothal, CISI-numbered objects),
    drop M77-leaked (mapped sequence in M77, or mapped length>=2 identity core attested in M77),
    seal-identity dedup via length>=2 identity cores (one rep per identity), OOV -> wildcard -999.
    """
    merged = load_merged()
    bridge = load_bridge()
    idmap = load_idmap()
    recs = m77_training()
    m77seqs = set(r["seq"] for r in recs if r["seq"])
    keys = identity_keys_minlen(idmap, 2)

    def mapseq(s):
        out = []
        for x in s:
            m = bridge.get(str(x))
            out.append(m[0] if m else -999)
        return tuple(out)

    # M77-attested identity cores (two concrete sides, union, frozen rule):
    #  (i) inverse-bridge: a Wells core K (len>=2) is M77-attested if some M77 sequence has, at
    #      some window, every position i matching bridge[str(K[i])][0];
    #  (ii) Wells side: K appears in the Wells sequence of a CISI-numbered merged object whose
    #      mapped sequence is in m77seqs (M77-era material present in the DB).
    attested = set()
    m77_objs_seqs = [tuple(r["seq"]) for r in recs if r["seq"]]
    for K in keys:
        hit = False
        Kimg = []
        for w in K:
            m = bridge.get(str(w))
            Kimg.append(m[0] if m else None)
        if None in Kimg:
            continue
        for st in m77_objs_seqs:
            for j in range(len(st) - len(K) + 1):
                if st[j:j + len(K)] == tuple(Kimg):
                    hit = True
                    break
            if hit:
                break
        if hit:
            attested.add(K)
    CISI_PREF = ("M-", "H-", "L-", "K-", "C-", "Ns-", "B-", "Ad-", "Agr-", "Blk-", "Ai-", "Krs-", "Rgr-", "Sktd-")
    for r in merged:
        cisi = str(r.get("cisi", ""))
        s = [x for x in r["seq"] if x != 0]
        if len(s) < 2 or not cisi.startswith(CISI_PREF):
            continue
        if mapseq(s) in m77seqs:
            st = tuple(s)
            for K in keys:
                for i in range(len(st) - len(K) + 1):
                    if st[i:i + len(K)] == K:
                        attested.add(K)
                        break
    info = {"identity_keys_len2": len(keys), "m77_attested_keys": len(attested)}

    kept = []
    for r in merged:
        s = [x for x in r["seq"] if x != 0]
        if len(s) < 2:
            continue
        cisi = str(r.get("cisi", ""))
        post97 = (r.get("site") in ("Dholavira", "Lothal")) or cisi.startswith(CISI_PREF)
        if not post97:
            continue
        seqm = mapseq(s)
        if seqm in m77seqs:
            continue
        st = tuple(s)
        ids = set()
        for K in keys:
            for i in range(len(st) - len(K) + 1):
                if st[i:i + len(K)] == K:
                    ids.add(K)
                    break
        if ids & attested:
            continue
        kept.append({
            "cisi": cisi, "site": r.get("site"), "type": r.get("type", ""),
            "otype": m77_object_types()(r.get("type")), "symfam": db_symbol_family(r.get("symbol")),
            "seq_w": tuple(s), "seq_m": seqm, "in_m77": False, "ids": ids,
            "complete": r.get("complete"), "period": r.get("period"),
            "post97_rule": ("Dholavira/Lothal excavation report" if r.get("site") in ("Dholavira", "Lothal")
                            else "CISI-numbered, not M77-attested"),
        })
    parent = list(range(len(kept)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def un(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for i in range(len(kept)):
        for j in range(i + 1, len(kept)):
            if kept[i]["ids"] & kept[j]["ids"]:
                un(i, j)
    reps = []
    seen = set()
    for i in range(len(kept)):
        g = find(i)
        if g not in seen:
            seen.add(g)
            reps.append(kept[i])
    info["pool_kept"] = len(kept)
    info["pool_reps"] = len(reps)
    return reps, kept, info
