#!/usr/bin/env python3
"""Ranking (PREREG rule 9) and selection inputs (PREREG rule 10) of run 2026-10-18-1758: val-0.50 ranking of every
eligible entry and the COMB-6, COMB-8, COMB-10 entry lists for tools/stage2x.py. Written by the tools engineer of
session 2026-10-18-1758 (Opus 5.5) while the lenses were running, before any surprise-test gold was read in this
session. Reads VALIDATION gold only (RUN/shared/val/0.50/FAM/solutions.tsv, through tools/val_scorer.py); never
reads surprise-test gold. Runs under any python3 (standard library); the scoring runs in the pinned scorer venv.

Copied from tools/rank_050.py (run 2026-10-18-0839). Unchanged: the rule 9 sort key (val-0.50 mean NED, then mean
ED, then freeze time as UTC strings, then name, the last reported as such), the tie notes, the entries-list format
([{"name","dir","freeze_time"}] in ranking order, json indent 1: the order the stage-2 tie rule uses), the rule 10
selection logic for --comb (singles before combinations, then earlier freeze, then the --comb order) and the
--comb-fit cross-check. Changed for this run, and nothing else:
  1. scores are computed by this tool unless --val-json is given: for every entry (and every --comb-dir) it runs
     q15h.SCORER_PY -I tools/val_scorer.py --pred DIR --props 0.50 --fams (the 10 surprise families) --gold-root G
     --json TMP (G default RUN/shared/val), the same program and arguments that `q15h.py score-val` and
     `val_table.py --home` run, with HOME=--home (default OUT/home), MPLCONFIGDIR=HOME/mplcfg, STUB_MPL=1. The per-entry
     results are saved as OUT/val050_scores.json in tools/val_table.py's --out-json format ({name: {"0.50": {FAM:
     [ED, NED, BCFS, BLEU], "total": [...]}}}), which can be passed back as --val-json. With --val-json the totals are
     read from that file as in rank_050.py.
  2. the ranking key is val_scorer.py's "total" (statistics.mean over the 10 families, exactly what q15h.py score-val
     prints and what compare_systems computes; this is the "score-val" value the PREREG names). For information the
     table also gives the family-mean NED summed left to right and with Python's builtin sum (each divided by 10),
     and a note says whether the ranking order would be the same under either (only the statistics.mean key decides).
  3. it writes COMB-10 too: OUT/comb6_entries.json, comb8_entries.json, comb10_entries.json (the 6, 8, 10 best in
     ranking order), OUT/ranked_040.json (every ranked entry with its totals and the two summation-mode NED means)
     and OUT/ranking_040.md; a warning is printed and written if fewer than 10 entries are ranked.
  4. --comb accepts COMB-10; a combination's val total comes from --val-json if it holds the name, otherwise it is
     scored from --comb-dir NAME=DIR (DIR/val/0.50/FAM/result-0.50.tsv, the LOFO val files of tools/stage2x.py).
     --comb-fit reads ["0.50"]["lofo_val_scorer_total"] of a combiner_fit.json (as before), or the top-level
     "lofo_val_scorer_total" if there is no "0.50" key. Output OUT/selection_040.json.
  5. --hashes: freeze records are RUN/attempts/LENS/FROZEN.md for this session's entries (names without an r0202-/
     r0839- prefix; --attempts-root overrides the folder) and the carry file's src_frozen for carried entries
     (--carried RUN/carry/carry_entries.json); the result files hashed are each entry's and combination's val/0.50 and
     test/0.40 files (was val/0.50 and test/0.50).
  6. the markdown title names this run and the key; docstrings avoid angle brackets.

usage: python3 -I -B tools/rank_040.py --entries E.json --out-dir OUT [--val-json V.json] [--home DIR]
           [--gold-root RUN/shared/val] [--carried RUN/carry/carry_entries.json]
           [--comb COMB-6 --comb COMB-8 --comb COMB-10 --comb-dir COMB-6=DIR ... --comb-fit COMB-6=DIR/combiner_fit.json
            ...] [--hashes]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import q15h  # noqa: E402

P = "0.50"        # validation proportion of the ranking
TESTP = "0.40"    # run 1758: test proportion of the hashed result files
TOPS = (6, 8, 10)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def kv(items):
    out = {}
    for s in items or []:
        k, v = s.split("=", 1)
        out[k] = v
    return out


def score_dir(pred_dir, gold_root, home):
    """run 1758 (change 1): val-0.50 scores of one folder, by tools/val_scorer.py in the pinned scorer venv."""
    os.makedirs(os.path.join(home, "mplcfg"), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        oj = os.path.join(tmp, "s.json")
        cmd = [q15h.SCORER_PY, "-I", os.path.join(HERE, "val_scorer.py"), "--pred", os.path.abspath(pred_dir),
               "--props", P, "--fams", ",".join(q15h.FAMS), "--json", oj, "--gold-root", gold_root]
        env = dict(os.environ, STUB_MPL="1", MPLCONFIGDIR=os.path.join(home, "mplcfg"), HOME=home)
        r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        res = json.load(open(oj)) if os.path.isfile(oj) else {}
    if r.returncode != 0:
        print("WARNING scorer rc=%d for %s: %s" % (r.returncode, pred_dir, r.stderr.strip()[:300]))
    return res


def ltr_mean(xs):
    """left-to-right sum / n."""
    s = 0.0
    for x in xs:
        s += x
    return s / len(xs)


def main():
    ap = argparse.ArgumentParser(description="PREREG rule 9 ranking at val 0.50 and COMB-6/8/10 lists (run 1758)")
    ap.add_argument("--entries", required=True, help="eligible entries JSON (tools/check_freezes_040.py output)")
    ap.add_argument("--val-json", help="optional: tools/val_table.py --out-json output at --props 0.50 (or this "
                                       "tool's OUT/val050_scores.json); default: score with tools/val_scorer.py")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--home", help="HOME for the scorer (default OUT/home)")
    ap.add_argument("--gold-root", default=q15h.VAL, help="validation gold root P/FAM/solutions.tsv (default "
                                                         "RUN/shared/val)")
    ap.add_argument("--attempts-root", default=os.path.join(q15h.RUN, "attempts"))
    ap.add_argument("--carried", help="RUN/carry/carry_entries.json (freeze records of carried entries, for --hashes)")
    ap.add_argument("--comb", action="append", default=[], help="name of a stage-2 combination (order = rule 10 tie "
                                                                 "order: COMB-6, COMB-8, COMB-10)")
    ap.add_argument("--comb-dir", action="append", default=[], help="NAME=stage-2 output folder")
    ap.add_argument("--comb-fit", action="append", default=[], help="NAME=combiner_fit.json (cross-check)")
    ap.add_argument("--hashes", action="store_true")
    a = ap.parse_args()
    with open(a.entries) as f:
        entries = json.load(f)
    os.makedirs(a.out_dir, exist_ok=True)
    home = os.path.abspath(a.home or os.path.join(a.out_dir, "home"))
    gold_root = os.path.abspath(a.gold_root)
    comb_dirs = kv(a.comb_dir)
    if a.val_json:
        with open(a.val_json) as f:
            val = json.load(f)
    else:
        val = {}
        for e in entries:
            val[e["name"]] = score_dir(e["dir"], gold_root, home)
            tot = val[e["name"]].get(P, {}).get("total")
            print("scored %-32s %s" % (e["name"], ("NED %r ED %r" % (tot[1], tot[0])) if tot else "INCOMPLETE"),
                  flush=True)
    scored_comb = False
    for c in a.comb:
        if c in comb_dirs and not val.get(c, {}).get(P, {}).get("total"):
            val[c] = score_dir(comb_dirs[c], gold_root, home)
            scored_comb = True
            tot = val[c].get(P, {}).get("total")
            print("scored %-32s %s" % (c, ("NED %r ED %r" % (tot[1], tot[0])) if tot else "INCOMPLETE"),
                  flush=True)
    if not a.val_json or scored_comb:
        with open(os.path.join(a.out_dir, "val050_scores.json"), "w") as f:
            json.dump(val, f, indent=1)
    rows, missing = [], []
    for e in entries:
        res = val.get(e["name"], {}).get(P, {})
        tot = res.get("total")
        if not tot:
            missing.append(e["name"])
            continue
        neds = [res[fam][1] for fam in q15h.FAMS] if all(fam in res for fam in q15h.FAMS) else None
        rows.append(dict(name=e["name"], dir=os.path.abspath(e["dir"]), freeze_time=e.get("freeze_time", ""),
                         ED=tot[0], NED=tot[1], BCFS=tot[2], BLEU=tot[3],
                         NED_ltr=ltr_mean(neds) if neds else None,
                         NED_builtin=(sum(neds) / len(neds)) if neds else None))
    if missing:
        print("WARNING: no val-0.50 total for %s (not ranked)" % ", ".join(missing))
    rows.sort(key=lambda r: (r["NED"], r["ED"], r["freeze_time"], r["name"]))
    notes = []
    for x, y in zip(rows, rows[1:]):
        if x["NED"] == y["NED"]:
            how = ("lower ED" if x["ED"] != y["ED"] else "earlier freeze" if x["freeze_time"] != y["freeze_time"]
                   else "NAME (all PREREG keys equal)")
            notes.append("tie on NED between %s and %s broken by %s" % (x["name"], y["name"], how))
    for i, r in enumerate(rows):
        r["rank"] = i + 1
    # run 1758 (change 2): would either summation mode order the entries differently?
    alt = {}
    for k in ("NED_ltr", "NED_builtin"):
        if all(r[k] is not None for r in rows):
            order = sorted(rows, key=lambda r: (r[k], r["ED"], r["freeze_time"], r["name"]))
            alt[k] = [r["name"] for r in order] == [r["name"] for r in rows]
    ent = lambda rs: [{"name": r["name"], "dir": r["dir"], "freeze_time": r["freeze_time"]} for r in rs]
    out = {"ranked": os.path.join(a.out_dir, "ranked_040.json"), "md": os.path.join(a.out_dir, "ranking_040.md")}
    json.dump(rows, open(out["ranked"], "w"), indent=1)
    for n in TOPS:
        out["top%d" % n] = os.path.join(a.out_dir, "comb%d_entries.json" % n)
        json.dump(ent(rows[:n]), open(out["top%d" % n], "w"), indent=1)
    md = ["# Rule 9 ranking at val-0.50 (run %s)" % os.path.basename(q15h.RUN), "",
          "generated %s from `%s` (%s); key: val_scorer.py total mean NED (statistics.mean, as q15h.py score-val), "
          "then mean ED, then freeze time." % (
              q15h.utc(), os.path.abspath(a.entries),
              ("scores from `%s`" % os.path.abspath(a.val_json)) if a.val_json else
              ("scored here against `%s`" % gold_root)), "",
          "| rank | entry | val NED | val ED | val BCFS | val BLEU | NED left-to-right | NED builtin sum | freeze time "
          "| COMB-6 | COMB-8 | COMB-10 |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append("| %d | %s | %r | %r | %.6f | %.6f | %r | %r | %s | %s | %s | %s |" % (
            r["rank"], r["name"], r["NED"], r["ED"], r["BCFS"], r["BLEU"], r["NED_ltr"], r["NED_builtin"],
            r["freeze_time"], "yes" if r["rank"] <= 6 else "", "yes" if r["rank"] <= 8 else "",
            "yes" if r["rank"] <= 10 else ""))
    md += ["", "ties: " + ("; ".join(notes) if notes else "none on NED"),
           "same order under the left-to-right / builtin-sum NED means: %s" % (
               ", ".join("%s %s" % (k, "yes" if v else "NO") for k, v in alt.items()) or "-"), ""]
    if len(rows) < max(TOPS):
        w = "WARNING: fewer than %d ranked entries (%d); the larger COMB lists hold all of them" % (max(TOPS), len(rows))
        md.append(w)
        print(w)
    # rule 10 selection
    if a.comb:
        fits = kv(a.comb_fit)
        cands = [dict(kind="single", order=0, **r) for r in rows]
        for i, c in enumerate(a.comb):
            tot = val.get(c, {}).get(P, {}).get("total")
            if not tot:
                raise SystemExit("--comb %s: no val-0.50 total (give --comb-dir %s=DIR or --val-json)" % (c, c))
            d = dict(kind="combination", name=c, NED=tot[1], ED=tot[0], BCFS=tot[2], BLEU=tot[3], freeze_time="",
                     order=i + 1)
            if c in fits:
                J = json.load(open(fits[c]))
                fj = (J[P] if P in J else J).get("lofo_val_scorer_total")
                d["stage2_lofo_val_scorer_total"] = fj
                d["matches_stage2"] = (fj == tot)
                if fj != tot:
                    print("WARNING: %s val total %r differs from stage2's lofo_val_scorer_total %r" % (c, tot, fj))
            cands.append(d)
        cands.sort(key=lambda r: (r["NED"], r["ED"], r["kind"] != "single", r["freeze_time"], r["order"]))
        sel = cands[0]
        md += ["## Rule 10 selection (singles: frozen val-0.50 files; combinations: LOFO val files)", "",
               "| order | candidate | kind | val NED | val ED | val BCFS | val BLEU | stage2 cross-check |",
               "|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(cands):
            md.append("| %d | %s | %s | %r | %r | %.6f | %.6f | %s |" % (
                i + 1, r["name"], r["kind"], r["NED"], r["ED"], r["BCFS"], r["BLEU"],
                {True: "equal", False: "DIFFERENT"}.get(r.get("matches_stage2"), "-")))
        md += ["", "CANDIDATE (rule 10): %s (%s), val-0.50 mean NED %r" % (sel["name"], sel["kind"], sel["NED"]), ""]
        json.dump({"candidate": sel["name"], "kind": sel["kind"], "order": [r["name"] for r in cands],
                   "table": cands}, open(os.path.join(a.out_dir, "selection_040.json"), "w"), indent=1)
    if a.hashes:
        src = {}
        if a.carried:
            for e in json.load(open(a.carried)):
                src[e["name"]] = os.path.abspath(e["src_frozen"])
        md += ["## sha256 of freeze records and result files (for selection.md)", "", "```"]
        seen = set()
        for r in rows:
            fmd = src.get(r["name"]) or os.path.join(os.path.abspath(a.attempts_root), r["name"].split("/")[0],
                                                     "FROZEN.md")
            if fmd not in seen:
                seen.add(fmd)
                md.append("%s  %s  (freeze record of %s)" % (sha256(fmd) if os.path.isfile(fmd) else "MISSING", fmd,
                                                             r["name"].split("/")[0]))
        dirs = [(r["name"], r["dir"]) for r in rows] + [(k, os.path.abspath(v)) for k, v in comb_dirs.items()]
        for name, d in dirs:
            for mode, p in (("val", P), ("test", TESTP)):
                for fam in q15h.FAMS:
                    q = os.path.join(d, mode, p, fam, "result-%s.tsv" % p)
                    md.append("%s  %s" % (sha256(q) if os.path.isfile(q) else "MISSING", q))
        md += ["```", ""]
    open(out["md"], "w").write("\n".join(md) + "\n")
    print("\n".join(md))
    print("wrote %s, %s, %s" % (out["ranked"], ", ".join("%s (%d entries)" % (out["top%d" % n], min(n, len(rows)))
                                                          for n in TOPS), out["md"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
