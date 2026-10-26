"""Leakage test: is the shipped potency prior a pure function of chemical structure?

If the prior encoded any CTRPv2 response, two CTRPv2 drugs with IDENTICAL fingerprints could receive
different prior values (because their CTRPv2 responses differ). A prior that is a deterministic function of
the fingerprint cannot carry drug-specific response information beyond what the fingerprint itself implies.
Also re-derives the prior from the saved weights to confirm the shipped csv is that function's output."""
import sys, os, numpy as np, pandas as pd, json, collections  # noqa
# Part 1 needs only files shipped in this package plus the dataset's own fingerprint table.
# Part 2 additionally needs the prior's weights (9.4 MB, too large to ship; reproduce them with
# how-we-built-it/h10_teacher_threshold.py 0.60, which is seeded and deterministic).
FPCSV = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
    "FP_CSV", "<DATA>/CTRPv2/drug_fingerprints/pubchem_id_to_demorgan_2048_map.csv")
WEIGHTS = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("TEACHER_PT", "")
fp = pd.read_csv(FPCSV, dtype=str)
X = {c: fp[c].astype(np.uint8).to_numpy() for c in fp.columns}
HERE = os.path.dirname(os.path.abspath(__file__))
T = pd.read_csv(os.path.join(HERE, "..", "how-we-built-it", "teacher_pred.csv"), dtype={0: str})
T = dict(zip(T.iloc[:, 0].astype(str), T.iloc[:, 1].astype(float)))

groups = collections.defaultdict(list)
for d, v in X.items(): groups[v.tobytes()].append(d)
dup = {k: v for k, v in groups.items() if len(v) > 1}
print(f"CTRPv2 drugs: {len(X)} | distinct fingerprints: {len(groups)} | fingerprints shared by >1 drug: {len(dup)}")
bad = []
for k, ds in dup.items():
    vals = [T[d] for d in ds]
    if max(vals) - min(vals) > 1e-6: bad.append((ds, vals))
print(f"groups of drugs sharing a fingerprint: {len(dup)} covering {sum(len(v) for v in dup.values())} drugs")
print(f"groups where the prior DISAGREES across identical fingerprints: {len(bad)}  <- must be 0")
for ds, vals in bad[:5]: print("   ", ds, vals)

if not WEIGHTS or not os.path.isfile(WEIGHTS):
    print("\nPart 2 skipped: the prior's weights were not supplied (pass the path as argv[2] or set "
          "TEACHER_PT). Part 1 above is the decisive test and needs only shipped files.")
    json.dump({"drugs": len(X), "distinct_fingerprints": len(groups), "shared_fp_groups": len(dup),
               "groups_with_disagreeing_prior": len(bad), "part2_run": False},
              open("teacher_structure_only.json", "w"), indent=1)
    raise SystemExit(0 if not bad else 1)
import torch
m = torch.nn.Sequential(torch.nn.Linear(2048, 1024), torch.nn.ReLU(), torch.nn.Dropout(0.3),
                        torch.nn.Linear(1024, 256), torch.nn.ReLU(), torch.nn.Dropout(0.3), torch.nn.Linear(256, 1))
m.load_state_dict(torch.load(WEIGHTS, map_location="cpu")); m.eval()
ids = list(X.keys()); A = torch.tensor(np.stack([X[d] for d in ids]).astype(np.float32))
with torch.no_grad(): raw = m(A).squeeze(1).numpy()
shipped = np.array([T[d] for d in ids])
off = shipped - raw
print(f"\nre-deriving the prior from the saved weights: shipped - f(fingerprint) has range "
      f"{off.max()-off.min():.3e} (a single constant offset, the training-set mean, is expected)")
print(f"  constant offset = {off.mean():.6f}; max deviation from constant = {np.abs(off-off.mean()).max():.3e}")
print(f"  => the shipped prior IS a deterministic function of the fingerprint: "
      f"{'YES' if np.abs(off-off.mean()).max() < 1e-4 and not bad else 'NO'}")
json.dump({"drugs": len(X), "distinct_fingerprints": len(groups), "shared_fp_groups": len(dup),
           "groups_with_disagreeing_prior": len(bad), "part2_run": True,
           "max_deviation_from_constant_offset": float(np.abs(off-off.mean()).max())},
          open("teacher_structure_only.json", "w"), indent=1)
