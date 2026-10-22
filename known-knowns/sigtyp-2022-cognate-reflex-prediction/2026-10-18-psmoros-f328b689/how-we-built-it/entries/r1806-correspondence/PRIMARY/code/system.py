"""CORRESPONDENCE lens system (harness contract of tools/q15h.py).

train --manifest M --model-dir D : for every surprise family in the manifest, align each training cognate set (lingpy
    SCA progressive alignment), derive per-target column examples (corr.split_target) and fit one column classifier
    per target language (corr.train_family). Reads only the manifest's surprise_train files.
predict --model-dir D --family F --jobs J : for each row of each partition, align the visible reflexes, classify each
    column, concatenate labels. Each row depends only on itself and the model. Deterministic.
Options come from config.json next to this file.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[v] = "2"
os.environ["HOME"] = "WORKDIR/runs/2026-10-17-1806/attempts/correspondence/home"
os.makedirs(os.environ["HOME"], exist_ok=True)
sys.path.insert(0, HERE)

import argparse, json, pickle, time
from multiprocessing import Pool

import corr


def _fit_family(args):
    fam, path, opts = args
    t0 = time.time()
    langs, data = corr.load(path)
    keys = list(data)
    lps = [[l for l in langs if data[k][l]] for k in keys]
    mats = [corr.msa([data[k][l] for l in lp]) for k, lp in zip(keys, lps)]
    t1 = time.time()
    if opts.get("algo", "rank") == "rank":
        models = corr.train_family_rank(list(zip(lps, mats)), langs, opts)
    else:
        models = corr.train_family(list(zip(lps, mats)), langs, opts)
    return fam, langs, models, "%s align %.1fs fit %.1fs" % (fam, t1 - t0, time.time() - t1)


def train(manifest, model_dir):
    man = json.load(open(manifest))
    opts = json.load(open(os.path.join(HERE, "config.json")))
    fams = list(man["families"])
    # largest training file first so the two workers finish close together
    fams.sort(key=lambda f: (-os.path.getsize(man["surprise_train"][f]), f))
    with Pool(2) as pool:
        for fam, langs, models, msg in pool.imap_unordered(_fit_family,
                                                           [(f, man["surprise_train"][f], opts) for f in fams]):
            with open(os.path.join(model_dir, fam + ".pkl"), "wb") as f:
                pickle.dump({"langs": langs, "opts": opts, "models": models}, f)
            print(msg, flush=True)


def predict(model_dir, fam, jobs):
    with open(os.path.join(model_dir, fam + ".pkl"), "rb") as f:
        m = pickle.load(f)
    opts = m["opts"]
    for ln in open(jobs):
        inp, outp = ln.rstrip("\n").split("\t")
        langs, data = corr.load(inp)
        tasks = []
        for key, row in data.items():
            tgt = [l for l in langs if row[l] == ["?"]][0]
            lp = [l for l in langs if l != tgt and row[l] and row[l] != ["?"]]
            mat = corr.msa([row[l] for l in lp])
            tasks.append((key, tgt, lp, mat))
        if opts.get("algo", "rank") == "rank":
            if opts.get("mbr"):
                preds = corr.predict_rows_rank_mbr(m["models"], tasks, opts)
            else:
                preds = corr.predict_rows_rank(m["models"], tasks, opts)
        else:
            preds = corr.predict_rows(m["models"], tasks, opts)
        with open(outp, "w", encoding="utf-8") as f:
            f.write("COGID\t" + "\t".join(langs) + "\n")
            for key, tgt, _, _ in tasks:
                f.write(key + "".join("\t" + (" ".join(preds[key]) if l == tgt else "") for l in langs) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("--manifest")
    ap.add_argument("--model-dir")
    ap.add_argument("--family")
    ap.add_argument("--jobs")
    a = ap.parse_args()
    if a.cmd == "train":
        train(a.manifest, a.model_dir)
    else:
        predict(a.model_dir, a.family, a.jobs)
