"""Score VALIDATION predictions with the pinned official scorer (sigtypst2022.compare_words at commit 03094435,
installed in the calibrator venv of run 2026-10-16-2026; run 2026-10-18-0104 copy: --gold-root added, missing gold skipped). Family mean computed as compare_systems does
(statistics.mean over the 10 families). Reads only shared/val/<P>/<fam>/solutions.tsv (built from training files)
and the prediction files. Never reads surprise-test gold.

usage: <scorer venv python> -I tools/val_scorer.py --pred OUT --props 0.10,... --fams a,b,... [--json FILE]
"""
import argparse, json, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mplstub  # noqa: F401
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import sigtypst2022 as st

VAL = "WORKDIR/runs/2026-10-18-0202/shared/val"  # run 2026-10-18-0202 copy: only this path changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", required=True)
    ap.add_argument("--props", required=True)
    ap.add_argument("--fams", required=True)
    ap.add_argument("--json")
    ap.add_argument("--gold-root", default=VAL)
    a = ap.parse_args()
    fams = a.fams.split(",")
    res = {}
    print("%-6s %-20s %8s %8s %8s %8s" % ("prop", "family", "ED", "NED", "BCFS", "BLEU"))
    for p in a.props.split(","):
        rows = []
        for fam in fams:
            gold = os.path.join(a.gold_root, p, fam, "solutions.tsv")
            if not os.path.isfile(gold):
                print("%-6s %-20s no val gold here (lenses: P 0.50 only)" % (p, fam))
                continue
            pred = os.path.join(a.pred, "val", p, fam, "result-%s.tsv" % p)
            if not os.path.isfile(pred):
                print("%-6s %-20s missing %s" % (p, fam, pred))
                continue
            with contextlib.redirect_stdout(io.StringIO()):
                sc = st.compare_words(gold, pred, report=False)[-1][1:]
            rows.append(sc)
            res.setdefault(p, {})[fam] = sc
            print("%-6s %-20s %8.4f %8.4f %8.4f %8.4f" % (p, fam, *sc))
        if len(rows) == len(fams):
            tot = [statistics.mean([r[i] for r in rows]) for i in range(4)]
            res[p]["total"] = tot
            print("%-6s %-20s %8.4f %8.4f %8.4f %8.4f   (mean over %d families)" % (p, "TOTAL", *tot, len(fams)))
    if a.json:
        with open(a.json, "w") as f:
            json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
