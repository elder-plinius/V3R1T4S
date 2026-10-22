#!/usr/bin/env python3
"""Shared harness for quarry Q15, run 2026-10-18-0104 (copied from run 2026-10-17-1806 by the main session before any
lens started; changed: RUN path, and score-val reads val gold only where it exists: lenses see val gold for P 0.50
only, the main session scores the other proportions with --gold-root after every lens has returned).

Standard library only. Scoring of VALIDATION predictions calls the pinned official scorer in the calibrator venv of
run 2026-10-16-2026 (tools/val_scorer.py). Surprise-test gold is never read by this harness.

Subcommands
  build-val
      Build shared/val/<P>/<fam>/{train,test,solutions}.tsv from data/view/surprise/<fam>/training-<P>.tsv with the
      organisers' own split rule (split_training_test_data, copied verbatim below) at VAL_RATIO.
  run --code DIR --mode val|test --out DIR [--python PY] [--props 0.10,0.20] [--fams a,b] [--train-cap S]
      [--predict-cap S] [--skip-train]
      For each proportion P: write a training manifest, run `PY DIR/system.py train --manifest M --model-dir D` once,
      make D read-only, split each family's test file into partitions by masked language (so no partition holds two
      rows of one cognate set), run `PY DIR/system.py predict --model-dir D --family F --jobs J` once per family
      (J lists "input<TAB>output" partition pairs), merge, check the format and write
      OUT/<mode>/<P>/<fam>/result-<P>.tsv in the official format.
  audit --code DIR --mode val|test --out DIR [--python PY] [--props 0.10] [--fams ...] [--rows 3]
      Isolation and determinism audit: re-predict, in fresh processes, single rows and one whole partition per
      family, each alone, and require byte-identical predictions to the merged result.
  score-val --pred OUT [--props ...] [--fams ...] [--json FILE]
      Official compare_words on shared/val gold, family mean as compare_systems computes it.
  freeze --lens NAME --role PRIMARY|SECONDARY --code DIR --out DIR
      Append a frozen record (UTC time, sha256 of every code file, of every result file, tree hashes) to
      attempts/<lens>/FROZEN.md. Run it only after `run --mode test` finished for all five proportions.

System contract (what a lens's system.py must do)
  train: read ONLY the files listed in the manifest (surprise_train: one file per family for this proportion and mode;
         dev_dir: the development families) and write anything into --model-dir.
  predict: read ONLY --model-dir and the partition files named in --jobs; predict each partition row from that row's
         visible cells plus the model, with no state carried between rows or partitions; write each output partition as
         a TSV with the same header and one line per input row: COGID, then the predicted reflex (space-separated
         segments) in the masked language's column, other columns empty. Deterministic (fixed seeds).
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import random
import stat
import subprocess
import sys
import time
from collections import defaultdict

RUN = "WORKDIR/runs/2026-10-18-0839"  # run 2026-10-18-0839 copy (of run 2026-10-18-0202): this path, the freeze cells and the audit default changed
VIEW = os.path.join(RUN, "data", "view")
VAL = os.path.join(RUN, "shared", "val")
PROPS = ["0.10", "0.20", "0.30", "0.40", "0.50"]
FAMS = ["bantubvd", "beidazihui", "birchallchapacuran", "bodtkhobwa", "bremerberta", "deepadungpalaung",
        "hillburmish", "kesslersignificance", "luangthongkumkaren", "wangbai"]
DEV_FAMS = ["abrahammonpa", "allenbai", "backstromnorthernpakistan", "castrosui", "davletshinaztecan",
            "felekesemitic", "hantganbangime", "hattorijaponic", "listsamplesize", "mannburmish"]
VAL_RATIO = 0.15
DEFAULT_PY = "WORKDIR/venvs/q15ml/bin/python"
SCORER_PY = "WORKDIR/runs/2026-10-16-2026/attempts/calibrator/venv/bin/python"


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ---- official helpers (logic copied from src/sigtypst2022.py at 03094435; lingpy's csv2list replaced by a TSV read)
def load_cognate_file(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    header = lines[0].split("\t")
    languages = header[1:]
    out = {}
    for ln in lines[1:]:
        row = ln.split("\t")
        row += [""] * (len(header) - len(row))
        out[row[0]] = {}
        for language, entry in zip(languages, row[1:]):
            out[row[0]][language] = entry.split()
    return languages, out


def write_cognate_file(languages, data, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("COGID\t" + "\t".join(languages) + "\n")
        for k, v in data.items():
            f.write("{0}".format(k))
            for language in languages:
                f.write("\t" + " ".join(v.get(language, [])))
            f.write("\n")


def split_training_test_data(data, languages, ratio=0.1):
    split_off = int(len(data) * ratio + 0.5)
    cognates = [key for key, value in sorted(
        data.items(),
        key=lambda x: sum([1 if " ".join(b) not in ["", "?"] else 0 for a, b in x[1].items()]),
        reverse=True)]
    test_, training = ({c: data[c] for c in cognates[:split_off]}, {c: data[c] for c in cognates[split_off:]})
    test = defaultdict(dict)
    solutions = defaultdict(dict)
    for i, language in enumerate(languages):
        for key, values in test_.items():
            if " ".join(test_[key][language]):
                new_key = key + "-" + str(i + 1)
                for j, languageB in enumerate(languages):
                    if language != languageB:
                        test[new_key][languageB] = test_[key][languageB]
                    else:
                        test[new_key][language] = ["?"]
                        solutions[new_key][language] = test_[key][language]
    return training, test, solutions


# ---- paths
def train_file(mode, p, fam):
    if mode == "val":
        return os.path.join(VAL, p, fam, "train.tsv")
    return os.path.join(VIEW, "surprise", fam, "training-%s.tsv" % p)


def test_file(mode, p, fam):
    if mode == "val":
        return os.path.join(VAL, p, fam, "test.tsv")
    return os.path.join(VIEW, "surprise", fam, "test-%s.tsv" % p)


def cmd_build_val(a):
    for p in PROPS:
        for fam in FAMS:
            langs, data = load_cognate_file(os.path.join(VIEW, "surprise", fam, "training-%s.tsv" % p))
            tr, te, so = split_training_test_data(data, langs, ratio=VAL_RATIO)
            d = os.path.join(VAL, p, fam)
            os.makedirs(d, exist_ok=True)
            write_cognate_file(langs, tr, os.path.join(d, "train.tsv"))
            write_cognate_file(langs, te, os.path.join(d, "test.tsv"))
            write_cognate_file(langs, so, os.path.join(d, "solutions.tsv"))
            print("val %s %-20s train sets %4d  val rows %5d" % (p, fam, len(tr), len(te)))
    with open(os.path.join(VAL, "MANIFEST.sha256"), "w") as f:
        for root, _, files in sorted(os.walk(VAL)):
            for fn in sorted(files):
                if fn.endswith(".tsv"):
                    q = os.path.join(root, fn)
                    f.write("%s  %s\n" % (sha256(q), os.path.relpath(q, VAL)))
    print("built", utc())


def masked_language(row, languages):
    m = [l for l in languages if row.get(l) == ["?"]]
    if len(m) != 1:
        raise SystemExit("row without exactly one masked cell: %r" % (row,))
    return m[0]


def make_partitions(mode, p, fam, partdir):
    langs, data = load_cognate_file(test_file(mode, p, fam))
    parts = defaultdict(dict)
    for key, row in data.items():
        parts[masked_language(row, langs)][key] = row
    os.makedirs(partdir, exist_ok=True)
    jobs = []
    for i, lang in enumerate(langs):
        if lang not in parts:
            continue
        bases = [k.rsplit("-", 1)[0] for k in parts[lang]]
        assert len(bases) == len(set(bases)), "two rows of one cognate set in a partition"
        inp = os.path.join(partdir, "part-%02d.tsv" % (i + 1))
        out = os.path.join(partdir, "pred-%02d.tsv" % (i + 1))
        write_cognate_file(langs, parts[lang], inp)
        jobs.append((inp, out))
    return langs, data, jobs


def read_prediction(path, langs, rows):
    plangs, pdata = load_cognate_file(path)
    if plangs != langs:
        raise ValueError("%s: header differs from the test header" % path)
    out = {}
    for key, row in rows.items():
        if key not in pdata:
            raise ValueError("%s: no line for %s" % (path, key))
        tgt = masked_language(row, langs)
        cell = pdata[key].get(tgt, [])
        if not cell or "?" in cell:
            raise ValueError("%s: empty or '?' prediction for %s / %s" % (path, key, tgt))
        others = [l for l in langs if l != tgt and pdata[key].get(l)]
        if others:
            raise ValueError("%s: %s has cells outside the masked column %s" % (path, key, others))
        out[key] = {tgt: cell}
    extra = set(pdata) - set(rows)
    if extra:
        raise ValueError("%s: lines for rows not in the input: %s" % (path, sorted(extra)[:3]))
    return out


def readonly(d):
    for root, dirs, files in os.walk(d):
        for fn in files:
            q = os.path.join(root, fn)
            os.chmod(q, os.stat(q).st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
    os.chmod(d, os.stat(d).st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def run_sub(cmd, cap, log):
    t0 = time.time()
    with open(log, "ab") as lf:
        lf.write(("\n### %s %s\n" % (utc(), " ".join(cmd))).encode())
        lf.flush()
        try:
            r = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, timeout=cap)
            rc = r.returncode
        except subprocess.TimeoutExpired:
            rc = -999
    return rc, time.time() - t0


def cmd_run(a):
    code = os.path.abspath(a.code)
    sysfile = os.path.join(code, "system.py")
    if not os.path.isfile(sysfile):
        raise SystemExit("no system.py in %s" % code)
    props = a.props.split(",") if a.props else PROPS
    fams = a.fams.split(",") if a.fams else FAMS
    for p in props:
        base = os.path.join(os.path.abspath(a.out), a.mode, p)
        os.makedirs(base, exist_ok=True)
        log = os.path.join(base, "harness.log")
        man = {"mode": a.mode, "proportion": p, "families": FAMS,
               "surprise_train": {f: train_file(a.mode, p, f) for f in FAMS},
               "dev_dir": os.path.join(VIEW, "dev"), "dev_families": DEV_FAMS,
               "note": "read only these files; dev_dir/<fam>/training-0.10.tsv and test-0.10.tsv"}
        mpath = os.path.join(base, "manifest.json")
        with open(mpath, "w") as f:
            json.dump(man, f, indent=1)
        model = os.path.join(base, "model")
        done = os.path.join(base, "TRAIN_DONE")
        if not (a.skip_train and os.path.exists(done)):
            if os.path.exists(done):
                os.remove(done)
            if os.path.isdir(model):
                subprocess.run(["chmod", "-R", "u+w", model])
            os.makedirs(model, exist_ok=True)
            rc, dt = run_sub([a.python, sysfile, "train", "--manifest", mpath, "--model-dir", model], a.train_cap, log)
            print("%s %s %s train rc=%s %.0fs" % (utc(), a.mode, p, rc, dt), flush=True)
            if rc != 0:
                raise SystemExit("train failed (rc %s); see %s" % (rc, log))
            readonly(model)
            with open(done, "w") as f:
                f.write(utc() + "\n")

        def one(fam):
            fdir = os.path.join(base, fam)
            pdir = os.path.join(fdir, "parts")
            langs, data, jobs = make_partitions(a.mode, p, fam, pdir)
            for _, o in jobs:
                if os.path.exists(o):
                    os.remove(o)
            jf = os.path.join(pdir, "jobs.tsv")
            with open(jf, "w") as f:
                for i, o in jobs:
                    f.write("%s\t%s\n" % (i, o))
            rc, dt = run_sub([a.python, sysfile, "predict", "--model-dir", model, "--family", fam, "--jobs", jf],
                             a.predict_cap, os.path.join(fdir, "predict.log"))
            if rc != 0:
                return fam, "predict rc=%s" % rc, dt
            merged = {}
            try:
                for i, o in jobs:
                    _, rows = load_cognate_file(i)
                    merged.update(read_prediction(o, langs, rows))
            except (ValueError, FileNotFoundError, SystemExit) as e:
                return fam, "format: %s" % e, dt
            missing = set(data) - set(merged)
            if missing:
                return fam, "missing %d rows" % len(missing), dt
            ordered = {k: merged[k] for k in data}
            write_cognate_file(langs, ordered, os.path.join(fdir, "result-%s.tsv" % p))
            return fam, "ok %d rows" % len(ordered), dt

        with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
            for fam, msg, dt in ex.map(one, fams):
                print("%s %s %s %-20s %s %.0fs" % (utc(), a.mode, p, fam, msg, dt), flush=True)


def cmd_audit(a):
    code = os.path.abspath(a.code)
    sysfile = os.path.join(code, "system.py")
    props = a.props.split(",") if a.props else ["0.50"]  # run 2026-10-18-0839: default 0.50 (was 0.10)
    fams = a.fams.split(",") if a.fams else FAMS
    rng = random.Random(20261017)
    bad = 0
    for p in props:
        base = os.path.join(os.path.abspath(a.out), a.mode, p)
        model = os.path.join(base, "model")
        adir = os.path.join(base, "audit")
        os.makedirs(adir, exist_ok=True)
        for fam in fams:
            langs, res = load_cognate_file(os.path.join(base, fam, "result-%s.tsv" % p))
            langs_t, data = load_cognate_file(test_file(a.mode, p, fam))
            keys = sorted(data)
            pick = rng.sample(keys, min(a.rows, len(keys)))
            jobs = []
            for k in pick:
                inp = os.path.join(adir, "%s-row-%s.tsv" % (fam, k))
                write_cognate_file(langs_t, {k: data[k]}, inp)
                jobs.append((inp, inp.replace(".tsv", ".pred.tsv"), [k]))
            # one whole partition (masked language chosen at random), alone, in a fresh process
            lang = rng.choice(sorted({masked_language(r, langs_t) for r in data.values()}))
            part = {k: r for k, r in data.items() if masked_language(r, langs_t) == lang}
            inp = os.path.join(adir, "%s-part.tsv" % fam)
            write_cognate_file(langs_t, part, inp)
            jobs.append((inp, inp.replace(".tsv", ".pred.tsv"), sorted(part)))
            for inp, outp, ks in jobs:
                jf = inp.replace(".tsv", ".jobs")
                with open(jf, "w") as f:
                    f.write("%s\t%s\n" % (inp, outp))
                rc, _ = run_sub([a.python, sysfile, "predict", "--model-dir", model, "--family", fam, "--jobs", jf],
                                a.predict_cap, os.path.join(adir, "audit.log"))
                ok = rc == 0 and os.path.exists(outp)
                if ok:
                    _, pd = load_cognate_file(outp)
                    for k in ks:
                        tgt = masked_language(data[k], langs_t)
                        if pd.get(k, {}).get(tgt) != res[k].get(tgt):
                            ok = False
                            print("MISMATCH %s %s %s: alone %r vs merged %r" % (p, fam, k, pd.get(k, {}).get(tgt),
                                                                                res[k].get(tgt)))
                            break
                bad += not ok
                print("%s audit %s %s %-20s %-28s %s" % (utc(), a.mode, p, fam, os.path.basename(inp),
                                                       "identical" if ok else "FAIL"), flush=True)
    print("AUDIT", "PASS" if bad == 0 else "FAIL (%d)" % bad)
    return 0 if bad == 0 else 1


def cmd_score_val(a):
    here = os.path.dirname(os.path.abspath(__file__))
    cmd = [SCORER_PY, "-I", os.path.join(here, "val_scorer.py"), "--pred", os.path.abspath(a.pred),
           "--props", a.props or ",".join(PROPS), "--fams", a.fams or ",".join(FAMS)]
    if a.json:
        cmd += ["--json", os.path.abspath(a.json)]
    if a.gold_root:
        cmd += ["--gold-root", os.path.abspath(a.gold_root)]
    env = dict(os.environ, STUB_MPL="1", MPLCONFIGDIR=os.path.join(RUN, "out", "mplcfg"),
               HOME=os.path.join(RUN, "out", "home"))
    os.makedirs(env["HOME"], exist_ok=True)
    return subprocess.run(cmd, env=env).returncode


def tree(paths, root):
    lines = []
    for q in sorted(paths):
        lines.append("%s  %s" % (sha256(q), os.path.relpath(q, root)))
    return lines, hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()


def cmd_freeze(a):
    code = os.path.abspath(a.code)
    out = os.path.abspath(a.out)
    cfiles = [os.path.join(r, f) for r, _, fs in os.walk(code) for f in fs
              if not f.endswith(".pyc") and "__pycache__" not in r]
    rfiles = [os.path.join(r, f) for r, _, fs in os.walk(out) for f in fs
              if f.startswith("result-") and f.endswith(".tsv") and os.sep + "parts" not in r]
    # run 2026-10-18-0839: required cells per PREREG rule 8 (val 0.50 and test 0.50 only)
    for mode, req in (("val", ["0.50"]), ("test", ["0.50"])):
        for p in req:
            for fam in FAMS:
                q = os.path.join(out, mode, p, fam, "result-%s.tsv" % p)
                if not os.path.isfile(q):
                    raise SystemExit("freeze refused: missing %s" % q)
    clines, ch = tree(cfiles, code)
    rlines, rh = tree(rfiles, out)
    rec = os.path.join(RUN, "attempts", a.lens, "FROZEN.md")
    with open(rec, "a") as f:
        f.write("\n## frozen %s\nROLE=%s lens=%s code=%s out=%s\ncode_tree_sha256=%s\nresults_tree_sha256=%s\n"
                % (utc(), a.role, a.lens, os.path.relpath(code, RUN), os.path.relpath(out, RUN), ch, rh))
        f.write("### code files\n" + "\n".join(clines) + "\n### result files\n" + "\n".join(rlines) + "\n")
    print("frozen", a.role, ch, rh, utc())


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("build-val")
    for name in ("run", "audit"):
        r = sp.add_parser(name)
        r.add_argument("--code", required=True)
        r.add_argument("--mode", choices=("val", "test"), required=True)
        r.add_argument("--out", required=True)
        r.add_argument("--python", default=DEFAULT_PY)
        r.add_argument("--props")
        r.add_argument("--fams")
        r.add_argument("--predict-cap", type=float, default=3600)
        if name == "run":
            r.add_argument("--train-cap", type=float, default=7200)
            r.add_argument("--workers", type=int, default=3)
            r.add_argument("--skip-train", action="store_true")
        else:
            r.add_argument("--rows", type=int, default=3)
    s = sp.add_parser("score-val")
    s.add_argument("--pred", required=True)
    s.add_argument("--props")
    s.add_argument("--fams")
    s.add_argument("--json")
    s.add_argument("--gold-root", help="main session only: folder <P>/<fam>/solutions.tsv (default shared/val)")
    z = sp.add_parser("freeze")
    z.add_argument("--lens", required=True)
    z.add_argument("--role", choices=("PRIMARY", "SECONDARY"), required=True)
    z.add_argument("--code", required=True)
    z.add_argument("--out", required=True)
    a = ap.parse_args()
    fn = {"build-val": cmd_build_val, "run": cmd_run, "audit": cmd_audit, "score-val": cmd_score_val,
          "freeze": cmd_freeze}[a.cmd]
    sys.exit(fn(a) or 0)


if __name__ == "__main__":
    main()
