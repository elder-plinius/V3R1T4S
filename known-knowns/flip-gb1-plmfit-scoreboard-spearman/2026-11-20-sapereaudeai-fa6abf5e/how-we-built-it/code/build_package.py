"""Build the object/ files of the p2 submission package and print the submission-id.

Reads: the released plmfit file (read-only, in place) and the two panel-verified prediction
files.  Writes a compact, machine-readable object/ into a staging directory.

Why the object is compact: each panel-verified prediction file is 1,602,414 bytes because it
repeats the full 265-residue sequence on every row, and kit/SUBMIT.md caps a packaged file at
1 MB.  Only four residues of that sequence vary in this benchmark, so the object keys every row
by those four letters instead.  The expansion back to the full-sequence files, whose sha256 the
REPRODUCE panellist verified, is exact and is checked by verify-it-yourself when the released
file is supplied.

Usage: python -I build_package.py <released_csv> <predA> <predB> <stage_dir>
"""
import csv
import hashlib
import io
import json
import os
import sys

SITES = (38, 39, 40, 53)          # 0-indexed; 1-indexed 39, 40, 41, 54
AA = "ACDEFGHIKLMNPQRSTVWY"
SPLIT = "three_vs_rest"

csv_path, predA, predB, stage = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
obj = os.path.join(stage, "object")
os.makedirs(obj, exist_ok=True)


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


raw = open(csv_path, "rb").read()
data_sha = hashlib.sha256(raw).hexdigest()
rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
te = [r for r in rows if r[SPLIT] == "test"]
counts = {}
for r in rows:
    counts[r[SPLIT]] = counts.get(r[SPLIT], 0) + 1

keys = [''.join(r["aa_seq"][p] for p in SITES) for r in te]
scores = [r["score"] for r in te]
assert len(set(keys)) == len(keys) == 5743, (len(keys), len(set(keys)))
assert all(len(k) == 4 and all(c in AA for c in k) for k in keys)

# the fixed part of the construct, so the full-sequence form can be rebuilt exactly
seq0 = te[0]["aa_seq"]
assert len(seq0) == 265
for r in te:
    s = r["aa_seq"]
    assert len(s) == 265
    for i, c in enumerate(s):
        if i not in SITES:
            assert c == seq0[i], i

preds = {}
for tag, path in (("A", predA), ("B", predB)):
    with open(path, newline="") as fh:
        d = {r["aa_seq"]: r["prediction"] for r in csv.DictReader(fh)}
    assert len(d) == 5743
    preds[tag] = [d[r["aa_seq"]] for r in te]


def write(name, header, cols):
    p = os.path.join(obj, name)
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(header + "\n")
        for tup in zip(*cols):
            fh.write(",".join(tup) + "\n")
    return p


pA = write("predictions_A.csv", "sites_39_40_41_54,prediction", (keys, preds["A"]))
pB = write("predictions_B.csv", "sites_39_40_41_54,prediction", (keys, preds["B"]))
pS = write("scored_pairs.csv", "sites_39_40_41_54,score", (keys, scores))

summary = {
    "target_id": "flip-gb1-plmfit-scoreboard-spearman",
    "claim_level": "partial win p2",
    "split_column": SPLIT,
    "released_file": "gb1_data_full.csv",
    "released_file_sha256": data_sha,
    "released_file_bytes": len(raw),
    "split_counts": counts,
    "n_test": len(te),
    "sequence_length": 265,
    "varying_sites_1indexed": [39, 40, 41, 54],
    "alphabet": AA,
    "constant_part_of_construct_sha256":
        hashlib.sha256(''.join(c for i, c in enumerate(seq0) if i not in SITES)
                       .encode()).hexdigest(),
    "claim_object": "object/predictions_A.csv",
    "configurations": {
        "A": {"role": "claim object", "fit_set": "train+validation", "n_fit": 2990,
              "s2": 0.5, "s3": 0.25, "alpha": 0.03, "objective": "squared error",
              "target_transform": "log(y+0.001)", "seeds": [1, 2, 3],
              "spearman_per_seed": [0.902852, 0.902852, 0.902852],
              "spearman_mean": 0.902852, "spearman_sd_ddof0": 0.0,
              "bootstrap95_of_mean": [0.898044, 0.907247],
              "full_sequence_prediction_file_sha256":
                  "30ad1d2601a2f3edaa8d1b7950988f1627f514ea0d7c2edcf3943e7a553221f2"},
        "B": {"role": "additional measurement, not the claim object",
              "fit_set": "train", "n_fit": 2691,
              "s2": 1.0, "s3": 1.0, "alpha": 0.001, "objective": "squared error",
              "target_transform": "log(y+0.01)", "seeds": [1, 2, 3],
              "spearman_per_seed": [0.897451, 0.897451, 0.897451],
              "spearman_mean": 0.897451, "spearman_sd_ddof0": 0.0,
              "bootstrap95_of_mean": [0.892649, 0.901823],
              "full_sequence_prediction_file_sha256":
                  "e323a6a3d9c60d95fbdd2ffd348a8bb0653411399a482a751d15ebc015ebc490"},
    },
    "determinism": {
        "statement": "with the configuration given rather than searched, nothing in the fit is "
                     "random, so the three seeds produce byte-identical predictions and the "
                     "seed-to-seed standard deviation is exactly 0; this was pre-registered "
                     "before the fits were run",
        "distinct_prediction_file_sha256_per_configuration": 1,
    },
    "leakage_witness": {
        "statement": "refitting both configurations on a copy of the released file in which the "
                     "score of all 5743 test rows is the literal nan gives byte-identical "
                     "prediction files",
        "nan_copy_sha256":
            "c50240964016608e53869bee05e7c3071a6734cb52c6fdfae70adf5469464497",
        "nan_refit_A_sha256":
            "30ad1d2601a2f3edaa8d1b7950988f1627f514ea0d7c2edcf3943e7a553221f2",
        "nan_refit_B_sha256":
            "e323a6a3d9c60d95fbdd2ffd348a8bb0653411399a482a751d15ebc015ebc490",
    },
    "bars": {
        "plmfit_scoreboard_three_vs_rest": 0.8791,
        "scoreboard_fetched_utc": "2026-11-20T05:42:28Z",
        "scoreboard_http_status": 200,
        "scoreboard_page_sha256":
            "51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b",
        "full_criterion_threshold_bar_plus_0.02": 0.8991,
        "highest_published_value_same_split": 0.8995,
        "highest_published_value_pm": 0.0058,
        "highest_published_value_model": "ProtEGNN(t6), ICLR 2026 LMRL Workshop, OpenReview Ua2mSmkccH, Table 1 (89.95 +- 0.58)",
    },
}
ps = os.path.join(obj, "summary.json")
io.open(ps, "w", encoding="utf-8", newline="\n").write(
    json.dumps(summary, indent=2, sort_keys=True) + "\n")

print("released file sha256:", data_sha)
print("split counts:", counts)
for p in (pA, pB, pS, ps):
    print("%-22s %9d bytes  sha256 %s" % (os.path.basename(p), os.path.getsize(p), sha(p)))
main = sha(pA)
print("MAIN OBJECT FILE: object/predictions_A.csv")
print("SUBMISSION_ID: 2026-11-20-sapereaudeai-%s" % main[:8])
