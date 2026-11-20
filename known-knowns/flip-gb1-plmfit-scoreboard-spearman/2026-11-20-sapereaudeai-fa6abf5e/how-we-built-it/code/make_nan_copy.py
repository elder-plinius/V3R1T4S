"""Empirical leakage audit (PREREG section 7): write a copy of the released CSV in which the
`score` of every row whose `three_vs_rest` value is `test` is replaced by the literal `nan`,
every other byte unchanged in meaning.  The fitting program is then run on this copy; its
prediction files must be byte-identical to the real ones, which proves no test target can have
influenced any prediction.

Usage: python -I make_nan_copy.py <csv> <split> <out.csv>
"""
import csv
import hashlib
import sys


def main():
    src, split, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(src, "rb") as fh:
        raw = fh.read()
    print("source sha256:", hashlib.sha256(raw).hexdigest())
    text = raw.decode("utf-8")
    rows = list(csv.DictReader(text.splitlines()))
    fields = list(rows[0].keys())
    n = 0
    for r in rows:
        if r[split] == "test":
            r["score"] = "nan"
            n += 1
    with open(dst, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    with open(dst, "rb") as fh:
        h = hashlib.sha256(fh.read()).hexdigest()
    print("wrote %s  sha256 %s" % (dst, h))
    print("rows %d ; test-row scores replaced by nan: %d" % (len(rows), n))
    # prove the replacement really happened and nothing else did
    with open(dst, newline="") as fh:
        back = list(csv.DictReader(fh))
    bad = [i for i, (a, b) in enumerate(zip(rows, back))
           if a["aa_seq"] != b["aa_seq"] or a[split] != b[split]]
    nan_ok = all(b["score"] == "nan" for b in back if b[split] == "test")
    other_ok = all(b["score"] != "nan" for b in back if b[split] != "test")
    print("sequence/split columns unchanged: %s ; every test score is nan: %s ; "
          "no non-test score is nan: %s" % (not bad, nan_ok, other_ok))


if __name__ == "__main__":
    main()
