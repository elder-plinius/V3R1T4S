#!/usr/bin/env python3
"""Standalone checker (Python standard library only) for an aggregate A_BCFS claim in object/predictions-P.tsv (P = 0.10, 0.20, 0.30, 0.40, 0.50).
(Run 2026-10-18-0202, for the PREREG.v2/v3 cells; scoring code = tools/metric_tools.py, checked bit for bit against
the official compare_words on validation data. Run 2026-10-18-0839 copy (tools/check_q15_050.tmpl, tools engineer,
Opus 5.5): NED added (compare_words' item NED = mismatched alignment positions / alignment length on the same
nw_align alignment, mean per language, sum over languages with items / header languages, left-to-right sums; lower is
better: the object must be LOWER than every bar by more than 1e-9); BCFS and BLEU unchanged.)

Steps (any failure prints FAIL as the last line):
 1. calibration: Mockingbird-I1's official prediction files must reproduce every family BCFS and the total of
    results/results-surprise-P.json exactly (float equality) at every P;
 2. bars: Mockingbird-I1 only (the bar of this cell; no FeVeT value exists at 0.40 or for the aggregate);
 3. the object: one prediction per gold item; its mean BCFS must equal the claimed value exactly and be better
    (NED: lower; BCFS, BLEU: higher) than every bar by more than 1e-9;
 4. integrity: the official-format result files rebuilt from the object must have the frozen sha256 values.

usage: python3 verify-it-yourself/check_q15.py INPUT_DIR object
"""
import hashlib
import json
import os
import statistics
import math
import sys
import unicodedata

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




def ngrams(seq, order, pad="$$$"):
    s = (pad,) * (order - 1) + tuple(seq) + (pad,) * (order - 1)
    return list(zip(*[s[i:] for i in range(order)]))


def bleu_item(word, reference, n=4):
    """lingrex.util.bleu_score(word, reference, n=4, trim=False); compare_words calls it as (gold, prediction)."""
    weights = [1 / n for _ in range(n)]
    scores = []
    for i in range(1, n + 1):
        w, r = ngrams(word, i), ngrams(reference, i)
        clipped, divide = [], []
        for itm in set(w):
            clipped.append(r.count(itm))
            divide.append(w.count(itm))
        scores.append(sum(clipped) / sum(divide))
    out = 1
    for weight, score in zip(weights, scores):
        out = out * (score ** weight)
    bp = 1 if len(word) > len(reference) else math.e ** (1 - (len(reference) / len(word)))
    return bp * (out ** (1 / sum(weights)))


def bcubed(one, other):
    tmp = {}
    for x, y in zip(one, other):
        tmp.setdefault(x, []).append(y)
    bcp = 0.0
    for x in tmp:
        for y in tmp[x]:
            bcp += tmp[x].count(y) / len(tmp[x])
    return bcp / len(other)


def bcfs_of(almsA, almsB):
    p, r = bcubed(almsA, almsB), bcubed(almsB, almsA)
    return 2 * (p * r) / (p + r)


def ned_item(almA, almB):
    """compare_words' scoreD on one alignment."""
    score = 0
    for x, y in zip(almA, almB):
        if x == y and x not in "Ø?-":
            pass
        elif x != y:
            score += 1
    return score / len(almA)


def family_scores(gold_path, pred):
    """pred: {cogid: {language: [segments]}}. Returns (BLEU, BCFS, NED) for the family, official aggregation, LTR sums."""
    langs, gold = load_cognate_file(gold_path)
    bl, bc, nd = [], [], []
    for lg in langs:
        items, almsA, almsB, neds = [], [], [], []
        for key in gold:
            if lg in gold[key] and " ".join(gold[key][lg]):
                a = gold[key][lg]
                b = pred.get(key, {}).get(lg, [])
                if not b:
                    b = (2 * len(a)) * ["Ø"]
                A, B = nw_align(a, b)[:2]
                almsA += A
                almsB += B
                items.append(bleu_item(a, b))
                neds.append(ned_item(A, B))
        if items:
            bl.append(ltr_sum(items) / len(items))
            bc.append(bcfs_of(almsA, almsB))
            nd.append(ltr_sum(neds) / len(neds))
    return ltr_sum(bl) / len(langs), ltr_sum(bc) / len(langs), ltr_sum(nd) / len(langs)


FAMS = ["bantubvd", "beidazihui", "birchallchapacuran", "bodtkhobwa", "bremerberta", "deepadungpalaung",
        "hillburmish", "kesslersignificance", "luangthongkumkaren", "wangbai"]
METRIC = "BCFS"            # "NED", "BCFS" or "BLEU"
IDX = {"NED": 1, "BCFS": 2, "BLEU": 3}[METRIC]
LOWER = METRIC == "NED"         # lower is better for NED only
CLAIMED = 0.7422025452564412
HAS_FEVET = False
OWN_BARS = []          # [(package-relative object file, stated value), ...]


def fam_metric(gold_path, pred):
    b, c, n = family_scores(gold_path, pred)
    return {"BLEU": b, "BCFS": c, "NED": n}[METRIC]


def margin(obj, bar):
    return (bar - obj) if LOWER else (obj - bar)


def read_object(path):
    rows = csv2list(path)
    if rows[0] != ["family", "COGID", "language", "prediction"]:
        raise ValueError("object header unexpected: %r" % rows[0])
    pred = {f: {} for f in FAMS}
    seen, bad = set(), 0
    for r in rows[1:]:
        if len(r) != 4 or r[0] not in pred or not r[3].split():
            bad += 1
            continue
        if (r[0], r[1], r[2]) in seen:
            bad += 1
        seen.add((r[0], r[1], r[2]))
        pred[r[0]].setdefault(r[1], {})[r[2]] = r[3].split()
    return pred, seen, bad


PROPS = ["0.10", "0.20", "0.30", "0.40", "0.50"]
BAR_PREREG = 0.6797616040522236   # Mockingbird-I1's A_BCFS in the PREREG table


def fam_metric_p(gold_path, pred):
    b, c, n = family_scores(gold_path, pred)
    return {"BLEU": b, "BCFS": c, "NED": n}[METRIC]


def main(inp, objdir):
    """Aggregate: A = (S(0.10)+S(0.20)+S(0.30)+S(0.40)+S(0.50))/5, summed left to right, for the object and for
    Mockingbird-I1 (from the official totals, after reproducing them exactly at every P)."""
    ok = True
    off_tot = []
    S = []
    want = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "frozen_result_sha256.txt")) as fh:
        for ln in fh:
            s, name = ln.split()
            want[name] = s
    good = 0
    for p in PROPS:
        gold = {f: os.path.join(inp, "ST2022", "data-surprise", f, "solutions-%s.tsv" % p) for f in FAMS}
        off = json.load(open(os.path.join(inp, "ST2022", "results", "results-surprise-%s.json" % p),
                             encoding="utf-8"))["Mockingbird-I1"]
        fam = {}
        for f in FAMS:
            _, pr = load_cognate_file(os.path.join(inp, "ST2022", "systems", "mockingbird-i1", "surprise", f,
                                                   "result-%s.tsv" % p))
            fam[f] = fam_metric_p(gold[f], pr)
            if fam[f] != off[f][IDX]:
                ok = False
                print("calibration MISMATCH %s %s: %r vs official %r" % (p, f, fam[f], off[f][IDX]))
        mb = statistics.mean([fam[f] for f in FAMS])
        cal = mb == off["total"][IDX]
        print("1. %s Mockingbird-I1 mean %s recomputed %r, official %r: %s" % (p, METRIC, mb, off["total"][IDX],
                                                                            "EXACT" if cal else "MISMATCH"))
        ok &= cal
        off_tot.append(off["total"][IDX])
        try:
            pred, seen, bad = read_object(os.path.join(objdir, "predictions-%s.tsv" % p))
        except (ValueError, OSError) as e:
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
        if items != seen or bad:
            ok = False
            print("%s object rows vs gold items: %d missing, %d extra, %d bad rows" % (
                p, len(items - seen), len(seen - items), bad))
        s_p = statistics.mean([fam_metric_p(gold[f], pred[f]) for f in FAMS])
        S.append(s_p)
        print("2. %s object mean %s %r over %d items" % (p, METRIC, s_p, len(seen)))
        for f in FAMS:
            langs, test = load_cognate_file(os.path.join(inp, "ST2022", "data-surprise", f, "test-%s.tsv" % p))
            lines = ["COGID\t" + "\t".join(langs) + "\n"]
            for k, row in test.items():
                masked = [lg for lg in langs if row.get(lg) == ["?"]]
                cell = {masked[0]: pred[f].get(k, {}).get(masked[0], [])} if len(masked) == 1 else {}
                lines.append(k + "".join("\t" + " ".join(cell.get(lg, [])) for lg in langs) + "\n")
            if hashlib.sha256("".join(lines).encode("utf-8")).hexdigest() == want.get("%s/%s" % (p, f)):
                good += 1
    mb_a = ltr_sum(off_tot) / 5
    print("3. Mockingbird-I1 A_%s from the official totals %r (PREREG %r): %s" % (
        METRIC, mb_a, BAR_PREREG, "EQUAL" if mb_a == BAR_PREREG else "DIFFERENT"))
    ok &= mb_a == BAR_PREREG
    a_obj = ltr_sum(S) / 5
    print("4. object A_%s %r (claimed %r): %s" % (METRIC, a_obj, CLAIMED, "EQUAL" if a_obj == CLAIMED else "DIFFERENT"))
    ok &= a_obj == CLAIMED
    print("   margin vs Mockingbird-I1 %.12f (%s is better)" % (margin(a_obj, mb_a), "lower" if LOWER else "higher"))
    ok &= margin(a_obj, mb_a) > 1e-9
    print("5. rebuilt official-format files equal to the frozen ones: %d of %d" % (good, len(FAMS) * len(PROPS)))
    ok &= good == len(FAMS) * len(PROPS)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
