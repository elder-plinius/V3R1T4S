"""SMUGGLER lens system: pairwise rewrite transducers + ROVER/MBR system combination (see smug.py).
Harness contract: `train --manifest M --model-dir D`, `predict --model-dir D --family F --jobs J`.
Parameters come from config.json next to this file (copied into the model dir at train time; predict reads the copy
in the model dir so a frozen model and its parameters travel together)."""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import smug  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("--manifest")
    ap.add_argument("--model-dir")
    ap.add_argument("--family")
    ap.add_argument("--jobs")
    a = ap.parse_args()
    if a.cmd == "train":
        cfg = json.load(open(os.path.join(HERE, "config.json")))
        man = json.load(open(a.manifest))
        with open(os.path.join(a.model_dir, "config.json"), "w") as f:
            json.dump(cfg, f, indent=1, sort_keys=True)
        for fam in man["families"]:
            m = smug.train_family(man["surprise_train"][fam], cfg)
            smug.save(m, os.path.join(a.model_dir, fam + ".pkl"))
            print("trained", fam, flush=True)
    else:
        cfg = json.load(open(os.path.join(a.model_dir, "config.json")))
        model = smug.load_model(os.path.join(a.model_dir, a.family + ".pkl"))
        for ln in open(a.jobs, encoding="utf-8"):
            if not ln.strip():
                continue
            inp, outp = ln.rstrip("\n").split("\t")
            smug.predict_file(model, inp, outp, cfg)


if __name__ == "__main__":
    main()
