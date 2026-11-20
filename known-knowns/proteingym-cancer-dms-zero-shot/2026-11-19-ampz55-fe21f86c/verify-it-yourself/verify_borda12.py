#!/usr/bin/env python3
"""Standalone verifier for the BORDA-12 claim (Python standard library only).

Checks, in order:
1. object/score_borda12.csv exists and its sha256 matches INDEX.csv.
2. verify-it-yourself/reference_Matreyek_2021.csv.gz decompresses to the
   ProteinGym v1.3 reference file whose sha256 matches the-record-we-beat/RECORD.md.
3. The score file assigns exactly one real-valued prediction to every
   mutant in the reference (exact set match, no duplicates, no NaN).
4. Spearman (rank with ties averaged, then Pearson) of score vs DMS_score
   is strictly greater than the bar in the-record-we-beat/RECORD.md
   (live best + 0.015).

Prints PASS or FAIL as its last line; exit 0 on PASS, 1 on FAIL.
Usage: run from the package folder: sh verify-it-yourself/run_checks.sh
"""
import csv
import gzip
import hashlib
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def read_kv(path):
    d = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                k, v = line.split(":", 1)
                d[k.strip()] = v.strip()
    return d


def ranks(values):
    """Average ranks (1-based) with ties averaged; returns list of floats."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    r = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(xs, ys):
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    if den == 0:
        return float("nan")
    return num / den


def main():
    fails = []

    def check(cond, msg):
        print(("ok: " if cond else "FAIL: ") + msg)
        if not cond:
            fails.append(msg)

    # --- INDEX.csv: object hash and target ---
    index_path = os.path.join(PKG, "INDEX.csv")
    with open(index_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    check(len(rows) == 1, "INDEX.csv has exactly one data row")
    row = rows[0] if rows else {}
    obj_rel = row.get("file", "object/score_borda12.csv")
    obj_path = os.path.join(PKG, obj_rel)
    expected_obj_sha = row.get("sha256", "")
    actual_obj_sha = sha256_file(obj_path) if os.path.isfile(obj_path) else ""
    check(os.path.isfile(obj_path), "object file exists: %s" % obj_rel)
    check(actual_obj_sha == expected_obj_sha and expected_obj_sha != "",
          "object sha256 matches INDEX.csv (%s)" % actual_obj_sha[:16])

    # --- reference file (gzipped in the package) ---
    rec = read_kv(os.path.join(PKG, "the-record-we-beat", "RECORD.md"))
    ref_gz = os.path.join(HERE, "reference_Matreyek_2021.csv.gz")
    with gzip.open(ref_gz, "rb") as f:
        ref_bytes = f.read()
    ref_sha = sha256_bytes(ref_bytes)
    check(ref_sha == rec.get("reference_sha256", ""),
          "reference sha256 matches the-record-we-beat/RECORD.md (%s)" % ref_sha[:16])
    ref_text = ref_bytes.decode("utf-8").splitlines()
    ref_rows = list(csv.DictReader(ref_text))
    ref = {}
    for r in ref_rows:
        if r["mutant"] in ref:
            check(False, "duplicate mutant in reference: %s" % r["mutant"])
        ref[r["mutant"]] = float(r["DMS_score"])
    check(len(ref) == 5083, "reference has 5083 mutants (got %d)" % len(ref))

    # --- score file ---
    with open(obj_path, newline="", encoding="utf-8") as f:
        score_rows = list(csv.DictReader(f))
    scores = {}
    for r in score_rows:
        if r["mutant"] in scores:
            check(False, "duplicate mutant in score file: %s" % r["mutant"])
        try:
            v = float(r["score"])
        except ValueError:
            check(False, "non-numeric score for %s" % r["mutant"])
            continue
        if not math.isfinite(v):
            check(False, "non-finite score for %s" % r["mutant"])
        scores[r["mutant"]] = v
    check(set(scores) == set(ref), "mutant sets match exactly "
          "(missing %d, extra %d)" % (len(set(ref) - set(scores)),
                                      len(set(scores) - set(ref))))

    # --- Spearman vs bar (only if the sets match exactly) ---
    bar = float(rec.get("bar", "nan"))
    if set(scores) == set(ref) and not fails:
        xs = [scores[m] for m in ref]
        ys = [ref[m] for m in ref]
        rho = spearman(xs, ys)
        print("spearman=%.6f bar=%.4f n=%d" % (rho, bar, len(xs)))
        check(math.isfinite(rho) and rho > bar,
              "spearman %.6f strictly greater than bar %.4f" % (rho, bar))
    elif set(scores) != set(ref):
        print("spearman skipped: mutant sets do not match")

    print("PASS" if not fails else "FAIL")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
