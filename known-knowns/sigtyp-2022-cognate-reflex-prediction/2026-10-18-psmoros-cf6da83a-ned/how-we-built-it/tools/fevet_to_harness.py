#!/usr/bin/env python3
"""Adapter, run 2026-10-18-0839 (tools engineer, Opus 5.5; written while the lenses were running): FeVeT's published
per-item predictions (pred_<P>_<fam>.tsv, long format: columns COGID, LANGUAGE, GOLD, PREDICTION, one row per test
item) -> the harness layout <out>/<fam>/result-<P>.tsv that tools/null_test_metric.py reads as --bar-dir.

The header, the row keys, their order and each row's masked language come from the MASKED test file (default
RUN/data/view/surprise/<fam>/test-<P>.tsv, gold-free); the masked cell gets FeVeT's PREDICTION for (COGID, LANGUAGE);
all other cells stay empty (tools/q15h.py write_cognate_file). The GOLD column is never used (it is parsed by the csv
reader, which is the same csv.DictReader(delimiter="\\t") that tools/score_test.py and tools/null_test.py use for these
files, so the strings are the ones the bar was scored with). A test row with no FeVeT prediction gets an empty cell
(the scorer then counts it as 2*len(gold) 'Ø', as compare_words does); counts of missing, extra and
language-mismatched rows are printed per family.

The real FeVeT files contain the surprise-test gold in their GOLD column: the main session runs this on them only
after selection.md exists (with the null tests). The tools engineer tested it only on mock FeVeT files built from
validation data (--test-tsv pointing at shared/val/<P>/<fam>/test.tsv).

usage: python3 -I tools/fevet_to_harness.py --prop 0.50 --out DIR [--fevet-dir D]
           [--test-tsv TEMPLATE]   (TEMPLATE with {fam} and {p}; default RUN/data/view/surprise/{fam}/test-{p}.tsv)
"""
import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import q15h  # noqa: E402

FEVET_DIR_DEFAULT = "WORKDIR/runs/2026-10-17-1806/resume/data/fevet"


def main():
    ap = argparse.ArgumentParser(description="FeVeT long-format predictions -> harness result files")
    ap.add_argument("--prop", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fevet-dir", default=FEVET_DIR_DEFAULT)
    ap.add_argument("--test-tsv", default=os.path.join(q15h.VIEW, "surprise", "{fam}", "test-{p}.tsv"))
    ap.add_argument("--fams", default=",".join(q15h.FAMS))
    a = ap.parse_args()
    p = a.prop
    tot = {"rows": 0, "filled": 0, "missing": 0, "extra": 0, "lang_mismatch": 0}
    for fam in a.fams.split(","):
        langs, data = q15h.load_cognate_file(a.test_tsv.format(fam=fam, p=p))
        pred = {}
        n = 0
        with open(os.path.join(a.fevet_dir, "pred_%s_%s.tsv" % (p, fam)), encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                n += 1
                pred[(row["COGID"], row["LANGUAGE"])] = row["PREDICTION"].split()
        out, filled, missing, mism = {}, 0, 0, 0
        keys_seen = set()
        pred_keys = {kk for kk, _ in pred}
        for k, row in data.items():
            tgt = q15h.masked_language(row, langs)
            cell = pred.get((k, tgt))
            if cell is None:
                missing += 1
                if k in pred_keys:
                    mism += 1
                cell = []
            else:
                filled += 1
                keys_seen.add((k, tgt))
            out[k] = {tgt: cell}
        extra = len(set(pred) - keys_seen)
        d = os.path.join(a.out, fam)
        os.makedirs(d, exist_ok=True)
        q15h.write_cognate_file(langs, out, os.path.join(d, "result-%s.tsv" % p))
        print("%s %-20s test rows %5d  FeVeT rows %5d  filled %5d  missing %d  extra %d  language-mismatch %d" % (
            p, fam, len(data), n, filled, missing, extra, mism))
        for k, v in (("rows", len(data)), ("filled", filled), ("missing", missing), ("extra", extra),
                     ("lang_mismatch", mism)):
            tot[k] += v
    print("TOTAL test rows %(rows)d filled %(filled)d missing %(missing)d extra %(extra)d "
          "language-mismatch %(lang_mismatch)d" % tot)
    print("FEVET_TO_HARNESS %s" % ("COMPLETE" if tot["missing"] == 0 and tot["extra"] == 0 else "INCOMPLETE"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
