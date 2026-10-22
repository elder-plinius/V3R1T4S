#!/usr/bin/env python3
"""Standard-library family BLEU and B-cubed F (BCFS) with the official ST2022 aggregation (compare_words at 03094435:
per language, BLEU = mean of item bleu_score(gold, pred, n=4, trim=False) [lingrex 1.2.0], BCFS = B-cubed F of the
concatenated nw_align alignments of all its items [lingpy _get_bcubed_score both ways, 2PR/(P+R)]; family = sum over
languages with items / number of header languages; sums left to right as in 2022). Main session, run 2026-10-18-0202,
for the next session's PREREG.v2/v3 scoring and package checkers. nw_align, csv2list and load_cognate_file are run
2026-10-17-1806's stdlib versions (validated bit for bit there).
"""
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


def family_scores(gold_path, pred):
    """pred: {cogid: {language: [segments]}}. Returns (BLEU, BCFS) for the family, official aggregation, LTR sums."""
    langs, gold = load_cognate_file(gold_path)
    bl, bc = [], []
    for lg in langs:
        items, almsA, almsB = [], [], []
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
        if items:
            bl.append(ltr_sum(items) / len(items))
            bc.append(bcfs_of(almsA, almsB))
    return ltr_sum(bl) / len(langs), ltr_sum(bc) / len(langs)
