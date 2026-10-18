#!/usr/bin/env python3
"""Validation score table for a set of frozen entries (run 2026-10-18-0202). Written by the tools engineer (Opus 5.5)
while the lenses were running; standard library only.

For an entries JSON ([{"name","dir"}], e.g. the output of tools/check_freezes.py, or a hand-written list that also
names COMB-NEW / COMB-ALL10 stage-2 output folders) and a list of proportions P, it calls, once per entry,
    <python> -I tools/q15h.py score-val --pred <entry dir> --props <P,...> [--gold-root G] --json <tmp>
(the entry's dir must hold val/<P>/<fam>/result-<P>.tsv; q15h.score-val runs the pinned official scorer in the
calibrator venv on the validation gold). It then writes two markdown tables:
  - totals: mean ED, NED, BCFS, BLEU over the 10 families, per entry and P (NED is the claim metric; lower better);
  - per-family NED: one row per (entry, P), one column per surprise family, last column = family-mean NED.
Gold for P 0.50 is in shared/val/0.50 (q15h default, no --gold-root). Gold for P < 0.50 lives in
RUN/main_only/val_gold (main session only) and must be passed with --gold-root; the lenses and this tool's author
never read it.

usage: python3 -I tools/val_table.py --entries E.json --props 0.10,0.20,0.30 --gold-root RUN/main_only/val_gold \
           --out-md val_table.md [--out-json val_table.json]
       python3 -I tools/val_table.py --entries E.json --props 0.50 --out-md val050.md
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import q15h  # noqa: E402

METRICS = ["ED", "NED", "BCFS", "BLEU"]


def score_entry(pyexec, pred_dir, props, gold_root, out_json):
    cmd = [pyexec, "-I", os.path.join(HERE, "q15h.py"), "score-val", "--pred", pred_dir,
           "--props", ",".join(props), "--json", out_json]
    if gold_root:
        cmd += ["--gold-root", gold_root]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def fmt(x):
    return "%.6f" % x if isinstance(x, (int, float)) else "-"


def main():
    ap = argparse.ArgumentParser(description="Validation score table for frozen entries (calls q15h.py score-val)")
    ap.add_argument("--entries", required=True, help="JSON list of {name, dir}; dir holds val/<P>/<fam>/result-<P>.tsv")
    ap.add_argument("--props", required=True, help="comma list, e.g. 0.10,0.20,0.30 or 0.50")
    ap.add_argument("--gold-root", help="solutions root <P>/<fam>/solutions.tsv (default: q15h's shared/val). "
                                        "P < 0.50 needs RUN/main_only/val_gold (main session only).")
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-json")
    ap.add_argument("--python", default=sys.executable, help="interpreter for q15h.py (std-lib; default this one)")
    a = ap.parse_args()
    with open(a.entries) as f:
        entries = json.load(f)
    props = a.props.split(",")
    gold_root = os.path.abspath(a.gold_root) if a.gold_root else None
    results = {}   # name -> {p -> {"total": [...], fam: [...]}}
    with tempfile.TemporaryDirectory() as tmp:
        for e in entries:
            name, d = e["name"], os.path.abspath(e["dir"])
            oj = os.path.join(tmp, name.replace("/", "__") + ".json")
            rc, so, se = score_entry(a.python, d, props, gold_root, oj)
            if os.path.isfile(oj):
                with open(oj) as f:
                    results[name] = json.load(f)
            else:
                results[name] = {}
            print("scored %-30s rc=%s%s" % (name, rc, "" if rc == 0 else " STDERR " + se.strip()[:200]), flush=True)

    # ---- table 1: totals per entry and P ----
    t1 = ["| entry | P | ED | NED | BCFS | BLEU |", "|---|---|---|---|---|---|"]
    for e in entries:
        name = e["name"]
        for p in props:
            tot = results.get(name, {}).get(p, {}).get("total")
            if tot:
                t1.append("| %s | %s | %s | %s | %s | %s |" % (name, p, fmt(tot[0]), fmt(tot[1]),
                                                               fmt(tot[2]), fmt(tot[3])))
            else:
                t1.append("| %s | %s | (incomplete: some family gold or prediction missing) | | | |" % (name, p))

    # ---- table 2: per-family NED ----
    t2 = ["| entry | P | " + " | ".join(q15h.FAMS) + " | mean |",
          "|---|---|" + "---|" * (len(q15h.FAMS) + 1)]
    for e in entries:
        name = e["name"]
        for p in props:
            pr = results.get(name, {}).get(p, {})
            cells = []
            for fam in q15h.FAMS:
                sc = pr.get(fam)
                cells.append(fmt(sc[1]) if sc else "-")
            tot = pr.get("total")
            cells.append(fmt(tot[1]) if tot else "-")
            t2.append("| %s | %s | %s |" % (name, p, " | ".join(cells)))

    md = ("# Validation score table (run 2026-10-18-0202)\n\nentries: `%s`\nprops: %s\ngold-root: %s\ngenerated: %s\n\n"
          "## Totals (mean over 10 families; NED is the claim metric, lower is better)\n\n%s\n\n"
          "## Per-family NED\n\n%s\n" % (
              os.path.abspath(a.entries), a.props, gold_root or "(q15h default: shared/val)", q15h.utc(),
              "\n".join(t1), "\n".join(t2)))
    os.makedirs(os.path.dirname(os.path.abspath(a.out_md)), exist_ok=True)
    with open(a.out_md, "w") as f:
        f.write(md)
    if a.out_json:
        with open(a.out_json, "w") as f:
            json.dump(results, f, indent=1)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
