#!/usr/bin/env python3
"""Standalone checker (Python standard library only) for the claim in object/predictions-0.30.tsv.
(Written for run 2026-10-18-0202 from run 2026-10-17-1806's checker: the scoring functions are unchanged.)

Definition (SIGTYP 2022 shared task on cognate reflex prediction, repository sigtyp/ST2022 at commit 03094435,
src/sigtypst2022.py): compare_words(solutions, prediction) aligns every gold reflex with the predicted one by
Needleman-Wunsch (lingpy nw_align: match +1, mismatch -1, gap -1, ties resolved gap-in-first, then match, then
gap-in-second, exactly as lingpy's pure-Python _malign.nw_align), counts mismatched alignment positions, and divides by
the alignment length (an empty prediction is replaced by 2 x len(gold) symbols "Ø"); the per-language mean of these
item values is summed over the languages that have items and divided by the number of languages in the gold header;
compare_systems takes statistics.mean over the 10 surprise families. Files are read as lingpy's csv2list does
(utf-8-sig, NFC, lines stripped of CR/LF, empty and '#' lines skipped, cells stripped). Sums run left to right, as
the 2022 interpreter did.

Steps (any failure prints FAIL as the last line):
 1. calibration: Mockingbird-I1's official prediction files must reproduce every family NED and the total NED of
    results/results-surprise-0.30.json exactly (float equality);
 2. other published bars: Mockingbird-I1 (step 1); FeVeT's published 0.30 predictions are scored the same way;
 3. the object: one prediction per gold item (no missing, extra or empty row); its mean NED must equal the claimed
    value exactly and be lower than every bar above by more than 1e-9;
 4. integrity: the official-format result files rebuilt from the object (header and row order of test-0.30.tsv)
    must have the sha256 values of the frozen result files (verify-it-yourself/frozen_result_sha256.txt).

usage: python3 verify-it-yourself/check_q15.py INPUT_DIR object/predictions-0.30.tsv
"""
import hashlib
import json
import os
import statistics
import sys
import unicodedata

FAMS = ["bantubvd", "beidazihui", "birchallchapacuran", "bodtkhobwa", "bremerberta", "deepadungpalaung",
        "hillburmish", "kesslersignificance", "luangthongkumkaren", "wangbai"]
P = "0.30"
CLAIMED = 0.22327922550091464
HAS_FEVET = True
PREV = None   # (package-relative object file of an earlier system, its claimed mean NED) or None


def ltr_sum(xs):
    acc = 0
    for x in xs:
        acc = acc + x
    return acc


def csv2list(path):
    out = []
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = unicodedata.normalize("NFC", line.strip("\r\n"))
            if line and not line.startswith("#"):
                out.append([c.strip() for c in line.split("\t")])
    return out


def load_cognate_file(path):
    data = csv2list(path)
    languages = data[0][1:]
    out = {}
    for row in data[1:]:
        out[row[0]] = {lg: entry.split() for lg, entry in zip(languages, row[1:])}
    return languages, out


def nw_align(seqA, seqB, gap=-1):
    M, N = len(seqA), len(seqB)
    matrix = [[0 for _ in range(M + 1)] for _ in range(N + 1)]
    tb = [[0 for _ in range(M + 1)] for _ in range(N + 1)]
    for i in range(1, M + 1):
        matrix[0][i] = matrix[0][i - 1] + gap
        tb[0][i] = 2
    for i in range(1, N + 1):
        matrix[i][0] = matrix[i - 1][0] + gap
        tb[i][0] = 3
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            m = 1.0 if seqA[j - 1] == seqB[i - 1] else -1.0
            gapA = matrix[i - 1][j] + gap
            gapB = matrix[i][j - 1] + gap
            match = matrix[i - 1][j - 1] + m
            if gapA >= match and gapA >= gapB:
                matrix[i][j], tb[i][j] = gapA, 3
            elif match >= gapB:
                matrix[i][j], tb[i][j] = match, 1
            else:
                matrix[i][j], tb[i][j] = gapB, 2
    i, j = N, M
    almA, almB = [], []
    while i > 0 or j > 0:
        if tb[i][j] == 3:
            almA.append("-")
            almB.append(seqB[i - 1])
            i -= 1
        elif tb[i][j] == 1:
            almA.append(seqA[j - 1])
            almB.append(seqB[i - 1])
            i -= 1
            j -= 1
        else:
            almA.append(seqA[j - 1])
            almB.append("-")
            j -= 1
    return almA[::-1], almB[::-1]


def family_ned(gold_path, pred):
    """pred: {key: {language: [segments]}}; returns compare_words' TOTAL NED for one family."""
    languages, first = load_cognate_file(gold_path)
    per_lang = []
    for lg in languages:
        vals = []
        for key in first:
            if lg in first[key]:
                entryA = first[key][lg]
                if " ".join(entryA):
                    entryB = pred.get(key, {}).get(lg, [])
                    if not entryB:
                        entryB = (2 * len(entryA)) * ["Ø"]
                    almA, almB = nw_align(entryA, entryB)
                    score = 0
                    for a, b in zip(almA, almB):
                        if a == b and a not in "Ø?-":
                            pass
                        elif a != b:
                            score += 1
                    vals.append(score / len(almA))
        if vals:
            per_lang.append(ltr_sum(vals) / len(vals))
    return ltr_sum(per_lang) / len(languages)


def read_object(path):
    rows = csv2list(path)
    if rows[0] != ["family", "COGID", "language", "prediction"]:
        raise ValueError("object header unexpected: %r" % rows[0])
    pred = {f: {} for f in FAMS}
    seen = set()
    bad = 0
    for r in rows[1:]:
        if len(r) != 4 or r[0] not in pred or not r[3].split():
            bad += 1
            print("bad object row: %r" % r[:4])
            continue
        if (r[0], r[1], r[2]) in seen:
            bad += 1
            print("duplicate object row: %r" % r[:3])
        seen.add((r[0], r[1], r[2]))
        pred[r[0]].setdefault(r[1], {})[r[2]] = r[3].split()
    return pred, seen, bad


def main(inp, obj):
    ok = True
    gold = {f: os.path.join(inp, "ST2022", "data-surprise", f, "solutions-%s.tsv" % P) for f in FAMS}
    # 1. calibration on Mockingbird-I1
    off = json.load(open(os.path.join(inp, "ST2022", "results", "results-surprise-%s.json" % P), encoding="utf-8"))
    off = off["Mockingbird-I1"]
    fam = {}
    for f in FAMS:
        _, pred = load_cognate_file(os.path.join(inp, "ST2022", "systems", "mockingbird-i1", "surprise", f,
                                                 "result-%s.tsv" % P))
        fam[f] = family_ned(gold[f], pred)
        if fam[f] != off[f][1]:
            ok = False
            print("calibration MISMATCH %s: %r vs official %r" % (f, fam[f], off[f][1]))
    mb = statistics.mean([fam[f] for f in FAMS])
    cal = mb == off["total"][1]
    print("1. Mockingbird-I1 mean NED recomputed %r, official %r: %s" % (mb, off["total"][1],
                                                                       "EXACT" if cal else "MISMATCH"))
    ok &= cal
    bars = [("Mockingbird-I1", off["total"][1], fam)]
    # 2. other bars
    if HAS_FEVET:
        fv = {}
        for f in FAMS:
            pred = {}
            rows = csv2list(os.path.join(inp, "FeVeT", f, "s2s_reflex_%s_predictions.tsv" % P))
            h = rows[0]
            for r in rows[1:]:
                d = dict(zip(h, r))
                pred.setdefault(d["COGID"], {})[d["LANGUAGE"]] = d["PREDICTION"].split()
            fv[f] = family_ned(gold[f], pred)
        fvt = statistics.mean([fv[f] for f in FAMS])
        print("2. FeVeT published predictions mean NED %r" % fvt)
        bars.append(("FeVeT", fvt, fv))
    else:
        print("2. FeVeT published no predictions at proportion %s" % P)
    if PREV:
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ppred, _, pbad = read_object(os.path.join(here, PREV[0]))
        pv = {f: family_ned(gold[f], ppred[f]) for f in FAMS}
        pvt = statistics.mean([pv[f] for f in FAMS])
        eq = pvt == PREV[1] and pbad == 0
        print("2. earlier system %s mean NED %r (stated %r): %s" % (PREV[0], pvt, PREV[1], "EQUAL" if eq else "DIFFERENT"))
        ok &= eq
        bars.append(("earlier system", pvt, pv))
    # 3. the object
    try:
        pred, seen, bad = read_object(obj)
    except ValueError as e:
        print(e)
        print("FAIL")
        return 1
    ok &= bad == 0
    items = set()
    for f in FAMS:
        langs, g = load_cognate_file(gold[f])
        for k, v in g.items():
            for lg in langs:
                if lg in v and " ".join(v[lg]):
                    items.add((f, k, lg))
    if items != seen:
        ok = False
        print("object rows vs gold items: %d missing, %d extra" % (len(items - seen), len(seen - items)))
    ob = {f: family_ned(gold[f], pred[f]) for f in FAMS}
    obt = statistics.mean([ob[f] for f in FAMS])
    print("3. object mean NED %r over %d items (claimed %r): %s" % (obt, len(seen), CLAIMED,
                                                                   "EQUAL" if obt == CLAIMED else "DIFFERENT"))
    ok &= obt == CLAIMED
    for f in FAMS:
        print("   %-20s object %.6f  " % (f, ob[f]) + "  ".join("%s %.6f" % (n, d[f]) for n, _, d in bars))
    for n, v, _ in bars:
        print("   margin vs %s %.12f" % (n, v - obt))
        ok &= v - obt > 1e-9
    # 4. integrity against the frozen result files
    want = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "frozen_result_sha256.txt")) as fh:
        for ln in fh:
            s, name = ln.split()
            want[name] = s
    good = 0
    for f in FAMS:
        langs, test = load_cognate_file(os.path.join(inp, "ST2022", "data-surprise", f, "test-%s.tsv" % P))
        lines = ["COGID\t" + "\t".join(langs) + "\n"]
        for k, row in test.items():
            masked = [lg for lg in langs if row.get(lg) == ["?"]]
            cell = {masked[0]: pred[f].get(k, {}).get(masked[0], [])} if len(masked) == 1 else {}
            lines.append(k + "".join("\t" + " ".join(cell.get(lg, [])) for lg in langs) + "\n")
        h = hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()
        if h == want.get(f):
            good += 1
        else:
            print("   rebuilt result file of %s: sha256 %s, frozen %s" % (f, h, want.get(f)))
    print("4. rebuilt official-format files equal to the frozen ones: %d of %d" % (good, len(FAMS)))
    ok &= good == len(FAMS)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
