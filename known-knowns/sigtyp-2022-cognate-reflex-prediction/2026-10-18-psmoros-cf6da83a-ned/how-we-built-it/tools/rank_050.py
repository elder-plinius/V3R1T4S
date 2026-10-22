#!/usr/bin/env python3
"""Ranking (PREREG rule 9) and selection inputs (PREREG rule 10) at proportion 0.50, run 2026-10-18-0839. Written by
the tools engineer (Opus 5.5) while the lenses were running, before any surprise-test gold was read. Standard library
only; reads only the entries JSON, the val-table JSON (tools/val_table.py --out-json) and, for --hashes, the freeze
records and the entries' val/test result files (sha256 only). Reads no gold.

Rule 9 ranking: every eligible entry by val-0.50 mean NED (the official family mean of tools/val_table.py, exact
float), ties by lower val-0.50 mean ED, then earlier freeze time (UTC strings compare in time order), then (only if
all three are equal, which the PREREG does not foresee) by name, reported as such. Writes the top-6 and top-8 entries
JSON ([{"name","dir","freeze_time"}] in ranking order: the order tools/stage2.py's tie rule uses) and the full ranked
list (markdown and JSON).

Rule 10 selection (optional, --comb NAME ...): the val-table JSON must then also hold the combinations' LOFO val
scores (run tools/val_table.py on an entries JSON that lists the stage-2 output folders, e.g. {"name": "COMB-6",
"dir": RUN/out/comb6}); candidate = the lowest val-0.50 mean NED among every eligible single entry and the named
combinations; ties: lower val ED, then singles before combinations, then earlier freeze, then the --comb order
(COMB-6 before COMB-8). With --comb-fit NAME=combiner_fit.json the combination's val NED is also checked against
stage2.py's own lofo_val_scorer_total (must be equal).

--hashes adds, for selection.md, the sha256 of every entry's freeze record (attempts/LENS/FROZEN.md for this run's
entries; for carried entries the run 2026-10-18-0202 FROZEN.md named by --carried's src) and of every entry's (and
combination's) val/0.50 and test/0.50 result files.

usage: python3 -I tools/rank_050.py --entries E.json --val-json V.json --out-dir OUT [--carried carry_entries.json]
           [--comb COMB-6 --comb COMB-8 --comb-dir COMB-6=DIR --comb-dir COMB-8=DIR
            --comb-fit COMB-6=DIR/combiner_fit.json --comb-fit COMB-8=DIR/combiner_fit.json] [--hashes]
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import q15h  # noqa: E402

P = "0.50"


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


def main():
    ap = argparse.ArgumentParser(description="PREREG rule 9 ranking and rule 10 selection inputs at P 0.50")
    ap.add_argument("--entries", required=True, help="eligible entries JSON (tools/check_freezes.py output)")
    ap.add_argument("--val-json", required=True, help="tools/val_table.py --out-json output at --props 0.50")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--carried", help="RUN/carry/carry_entries.json (freeze records of carried entries, for --hashes)")
    ap.add_argument("--comb", action="append", default=[], help="name of a stage-2 combination in --val-json (order "
                                                                 "= rule 10 tie order)")
    ap.add_argument("--comb-dir", action="append", default=[], help="NAME=stage-2 output folder (for --hashes)")
    ap.add_argument("--comb-fit", action="append", default=[], help="NAME=combiner_fit.json (cross-check)")
    ap.add_argument("--hashes", action="store_true")
    a = ap.parse_args()
    with open(a.entries) as f:
        entries = json.load(f)
    with open(a.val_json) as f:
        val = json.load(f)
    os.makedirs(a.out_dir, exist_ok=True)
    rows, missing = [], []
    for e in entries:
        tot = val.get(e["name"], {}).get(P, {}).get("total")
        if not tot:
            missing.append(e["name"])
            continue
        rows.append(dict(name=e["name"], dir=os.path.abspath(e["dir"]), freeze_time=e.get("freeze_time", ""),
                         ED=tot[0], NED=tot[1], BCFS=tot[2], BLEU=tot[3]))
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
    ent = lambda rs: [{"name": r["name"], "dir": r["dir"], "freeze_time": r["freeze_time"]} for r in rs]
    out = {"ranked": os.path.join(a.out_dir, "ranked_050.json"), "top6": os.path.join(a.out_dir, "comb6_entries.json"),
           "top8": os.path.join(a.out_dir, "comb8_entries.json"), "md": os.path.join(a.out_dir, "ranking_050.md")}
    json.dump(rows, open(out["ranked"], "w"), indent=1)
    json.dump(ent(rows[:6]), open(out["top6"], "w"), indent=1)
    json.dump(ent(rows[:8]), open(out["top8"], "w"), indent=1)
    md = ["# Rule 9 ranking at val-0.50 (run %s)" % os.path.basename(q15h.RUN), "",
          "generated %s from `%s` and `%s`; key: mean NED, then mean ED, then freeze time." % (
              q15h.utc(), os.path.abspath(a.entries), os.path.abspath(a.val_json)), "",
          "| rank | entry | val NED | val ED | val BCFS | val BLEU | freeze time | COMB-6 | COMB-8 |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append("| %d | %s | %r | %r | %.6f | %.6f | %s | %s | %s |" % (
            r["rank"], r["name"], r["NED"], r["ED"], r["BCFS"], r["BLEU"], r["freeze_time"],
            "yes" if r["rank"] <= 6 else "", "yes" if r["rank"] <= 8 else ""))
    md += ["", "ties: " + ("; ".join(notes) if notes else "none on NED"), ""]
    if len(rows) < 8:
        md.append("WARNING: fewer than 8 ranked entries (%d); COMB-8 holds all of them" % len(rows))
    # rule 10 selection
    sel = None
    if a.comb:
        fits = kv(a.comb_fit)
        cands = [dict(kind="single", order=0, **r) for r in rows]
        for i, c in enumerate(a.comb):
            tot = val.get(c, {}).get(P, {}).get("total")
            if not tot:
                raise SystemExit("--comb %s: no val-0.50 total in --val-json" % c)
            d = dict(kind="combination", name=c, NED=tot[1], ED=tot[0], BCFS=tot[2], BLEU=tot[3], freeze_time="",
                     order=i + 1)
            if c in fits:
                fj = json.load(open(fits[c]))[P]["lofo_val_scorer_total"]
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
                   "table": cands}, open(os.path.join(a.out_dir, "selection_050.json"), "w"), indent=1)
    if a.hashes:
        src = {}
        if a.carried:
            for e in json.load(open(a.carried)):
                src["r0202-" + e["name"]] = os.path.join(os.path.dirname(os.path.dirname(e["src"])), "FROZEN.md")
        md += ["## sha256 of freeze records and result files (for selection.md)", "", "```"]
        seen = set()
        for r in rows:
            fmd = src.get(r["name"]) or os.path.join(os.path.dirname(os.path.dirname(r["dir"])), "FROZEN.md")
            if fmd not in seen:
                seen.add(fmd)
                md.append("%s  %s  (freeze record of %s)" % (sha256(fmd), fmd, r["name"].split("/")[0]))
        dirs = [(r["name"], r["dir"]) for r in rows] + [(k, os.path.abspath(v)) for k, v in kv(a.comb_dir).items()]
        for name, d in dirs:
            for mode in ("val", "test"):
                for fam in q15h.FAMS:
                    q = os.path.join(d, mode, P, fam, "result-%s.tsv" % P)
                    md.append("%s  %s" % (sha256(q) if os.path.isfile(q) else "MISSING", q))
        md += ["```", ""]
    open(out["md"], "w").write("\n".join(md) + "\n")
    print("\n".join(md))
    print("wrote %s, %s (%d entries), %s (%d entries), %s" % (out["ranked"], out["top6"], min(6, len(rows)),
                                                             out["top8"], min(8, len(rows)), out["md"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
