#!/usr/bin/env python3
"""PREREG rule 11 test scoring, run 2026-10-18-0104: a copy of run 2026-10-17-1806's tools/score_test.py (written
there by the main session after its selection.md existed). Copied by the tools engineer of run 2026-10-18-0104 while
the lenses were running; never run by the tools engineer. Changes, and nothing else: the entry list comes from
--entries FILE (JSON list of {"name": str, "dir": folder holding test/<P>/<fam>/result-<P>.tsv}); an entry is scored
at P only if its test/<P>/ folder exists (else one "skipped" line; a missing family file inside an existing folder is
an error); FeVeT's published predictions are read from --fevet-dir (default: run 2026-10-17-1806's
resume/data/fevet); the claim walk at the end prints every entry against the bar (rule 12 (i) only) and adds the AGG
aggregate (mean over the five P of the per-P mean NED, summed left to right; bar = the five per-P bars of PREREG:
FeVeT at 0.10, 0.30, 0.50, Mockingbird-I1 at 0.20, 0.40).
Original description:

(a) Reproduces Mockingbird-I1's official totals (and every family value) at all five proportions bit for bit with
    left-to-right summation; if any total differs, nothing is scored (charter kill criterion 1).
(b) Rescores FeVeT's published per-item predictions (Wientzek 2025; files fetched 2026-10-16 from
    github.com/TGH-2020/FeVeT at 31898c53, copies in resume/data/fevet) at 0.10, 0.30, 0.50.
(c) Scores every eligible entry of selection.md at every proportion.
Every value is computed in both summation modes: 'ltr' (left-to-right sum shadowing the builtin in sigtypst2022 and
lingrex.util, as Python < 3.12 did in 2022) and 'builtin' (Python 3.13 compensated sum). The scorer is the pinned
repository's own compare_words; the family total is statistics.mean over the 10 families, as compare_systems does.

usage: STUB_MPL=1 <calibrator venv python> -I tools/score_test.py --entries E.json --json OUT.json [--fevet-dir DIR]
"""
import argparse
import builtins
import contextlib
import csv
import io
import json
import os
import statistics
import sys
import tempfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mplstub  # noqa: F401,E402
with contextlib.redirect_stdout(io.StringIO()):
    import sigtypst2022 as st  # noqa: E402
import lingrex.util  # noqa: E402

RUN = os.path.dirname(HERE)
CLONE = "WORKDIR/scratch_q15/ST2022"
PROPS = ["0.10", "0.20", "0.30", "0.40", "0.50"]
FAMS = ["bantubvd", "beidazihui", "birchallchapacuran", "bodtkhobwa", "bremerberta", "deepadungpalaung",
        "hillburmish", "kesslersignificance", "luangthongkumkaren", "wangbai"]
FEVET_PROPS = ["0.10", "0.30", "0.50"]
FEVET_DIR_DEFAULT = "WORKDIR/runs/2026-10-17-1806/resume/data/fevet"
AGG_BAR_HOLDER = {"0.10": "FeVeT-published", "0.20": "Mockingbird-I1", "0.30": "FeVeT-published",
                  "0.40": "Mockingbird-I1", "0.50": "FeVeT-published"}


def naive_sum(iterable, start=0):
    acc = start
    for x in iterable:
        acc = acc + x
    return acc


def set_mode(mode):
    f = naive_sum if mode == "ltr" else builtins.sum
    st.sum = f
    lingrex.util.sum = f


def gold(p, fam):
    return os.path.join(CLONE, "data-surprise", fam, "solutions-%s.tsv" % p)


def score_dir(p, resdir_of):
    fam_scores = {}
    for fam in FAMS:
        with contextlib.redirect_stdout(io.StringIO()):
            fam_scores[fam] = list(st.compare_words(gold(p, fam), resdir_of(fam), report=False)[-1][1:])
    tot = [statistics.mean([fam_scores[f][i] for f in FAMS]) for i in range(4)]
    return fam_scores, tot


def fevet_files(p, tmp, fevet_dir):
    paths = {}
    checks = {}
    for fam in FAMS:
        with contextlib.redirect_stdout(io.StringIO()):
            langs, _, g = st.load_cognate_file(gold(p, fam))
        pred = defaultdict(dict)
        n = mism = 0
        with open(os.path.join(fevet_dir, "pred_%s_%s.tsv" % (p, fam)), encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                n += 1
                pred[row["COGID"]][row["LANGUAGE"]] = row["PREDICTION"].split()
                gg = g.get(row["COGID"], {}).get(row["LANGUAGE"])
                if gg is None or gg != row["GOLD"].split():
                    mism += 1
        missing = sum(1 for k in g for lg in langs if g[k].get(lg) and lg not in pred.get(k, {}))
        out = os.path.join(tmp, "fevet", p, fam, "result-%s.tsv" % p)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("COGID\t" + "\t".join(langs) + "\n")
            for k in g:
                fh.write(k + "".join("\t" + " ".join(pred.get(k, {}).get(lg, [])) for lg in langs) + "\n")
        paths[fam] = out
        checks[fam] = {"rows": n, "missing": missing, "gold_column_mismatches": mism}
    return paths, checks


def main():
    ap = argparse.ArgumentParser(description="PREREG rule 11 test scoring (reads surprise-test gold; main session "
                                             "only, after selection.md exists)")
    ap.add_argument("--json", required=True)
    ap.add_argument("--entries", required=True, help="JSON list of {name, dir}; dir holds test/<P>/<fam>/result-<P>.tsv")
    ap.add_argument("--fevet-dir", default=FEVET_DIR_DEFAULT, help="folder with pred_<P>_<fam>.tsv (FeVeT published)")
    a = ap.parse_args()
    with open(a.entries) as f:
        ENTRIES = [(e["name"], os.path.abspath(e["dir"])) for e in json.load(f)]
    res = {"ltr": {}, "builtin": {}}
    with tempfile.TemporaryDirectory() as tmp:
        for mode in ("ltr", "builtin"):
            set_mode(mode)
            R = res[mode]
            # (a) calibration on Mockingbird-I1
            bad = 0
            for p in PROPS:
                off = json.load(open(os.path.join(CLONE, "results", "results-surprise-%s.json" % p)))["Mockingbird-I1"]
                fs, tot = score_dir(p, lambda fam: os.path.join(CLONE, "systems", "mockingbird-i1", "surprise", fam,
                                                                 "result-%s.tsv" % p))
                exact_tot = tot == off["total"]
                exact_fam = all(fs[f] == off[f] for f in FAMS)
                R.setdefault(p, {})["Mockingbird-I1"] = {"total": tot, "families": fs, "official_total": off["total"],
                                                         "total_bit_identical": exact_tot,
                                                         "families_bit_identical": exact_fam}
                print("%s %s Mockingbird-I1 NED %r official %r total %s families %s" % (
                    mode, p, tot[1], off["total"][1], "EXACT" if exact_tot else "DIFF", "EXACT" if exact_fam else "DIFF"),
                    flush=True)
                bad += not exact_tot
            if mode == "ltr" and bad:
                print("CALIBRATION FAILED in ltr mode: nothing is scored (kill criterion 1)")
                with open(a.json, "w") as f:
                    json.dump(res, f, indent=1)
                return 1
            # (b) FeVeT published predictions
            for p in FEVET_PROPS:
                paths, checks = fevet_files(p, os.path.join(tmp, mode), a.fevet_dir)
                fs, tot = score_dir(p, lambda fam: paths[fam])
                R[p]["FeVeT-published"] = {"total": tot, "families": fs, "checks": checks}
                print("%s %s FeVeT NED %r (checks: missing %d, gold mismatches %d)" % (
                    mode, p, tot[1], sum(c["missing"] for c in checks.values()),
                    sum(c["gold_column_mismatches"] for c in checks.values())), flush=True)
            # (c) eligible entries
            for e, edir in ENTRIES:
                for p in PROPS:
                    if not os.path.isdir(os.path.join(edir, "test", p)):
                        print("%s %s %-30s skipped (no test/%s folder)" % (mode, p, e, p), flush=True)
                        continue
                    fs, tot = score_dir(p, lambda fam: os.path.join(edir, "test", p, fam, "result-%s.tsv" % p))
                    R[p][e] = {"total": tot, "families": fs}
                    print("%s %s %-30s ED %.6f NED %r BCFS %.6f BLEU %.6f" % (mode, p, e, tot[0], tot[1], tot[2],
                                                                            tot[3]), flush=True)
    # bars and claim walk (rule 12 (i) only; (ii)-(iv) are checked separately)
    print()
    # (C10's own bar, run 2026-10-17-1806's confirmed 0.19710919181751296, is applied by the main session: an entry
    # that does not beat the published bar here cannot beat it either)
    for e, _ in ENTRIES:
        for p in ["0.10", "0.20", "0.40", "0.30", "0.50"]:
            if e not in res["ltr"].get(p, {}):
                continue
            line = []
            for mode in ("ltr", "builtin"):
                R = res[mode][p]
                bar = R["Mockingbird-I1"]["official_total"][1] if mode == "ltr" else R["Mockingbird-I1"]["total"][1]
                holder = "Mockingbird-I1"
                if "FeVeT-published" in R and R["FeVeT-published"]["total"][1] < bar:
                    bar, holder = R["FeVeT-published"]["total"][1], "FeVeT-published"
                c = R[e]["total"][1]
                line.append("%s: bar %s %r candidate %r margin %.9f -> %s" % (
                    mode, holder, bar, c, bar - c, "MEETS (i)" if bar - c > 1e-9 else "fails (i)"))
            print("%s cell P=%s | %s" % (e, p, " | ".join(line)))
        if all(e in res["ltr"].get(p, {}) for p in PROPS):
            line = []
            for mode in ("ltr", "builtin"):
                R = res[mode]
                bars = [(R[p][AGG_BAR_HOLDER[p]]["official_total"][1] if (mode == "ltr" and
                         AGG_BAR_HOLDER[p] == "Mockingbird-I1") else R[p][AGG_BAR_HOLDER[p]]["total"][1])
                        for p in PROPS]
                bar = naive_sum(bars) / len(PROPS)
                c = naive_sum([R[p][e]["total"][1] for p in PROPS]) / len(PROPS)
                res[mode].setdefault("AGG", {})[e] = {"aggregate_ned": c, "bar": bar, "bar_parts": bars}
                line.append("%s: bar %r candidate %r margin %.9f -> %s" % (
                    mode, bar, c, bar - c, "MEETS (i)" if bar - c > 1e-9 else "fails (i)"))
            print("%s cell AGG | %s" % (e, " | ".join(line)))
    with open(a.json, "w") as f:
        json.dump(res, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
