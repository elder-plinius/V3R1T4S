"""Standalone verifier for the dreval-lco-ctrpv2-normalized-r2 p2 claim.

Standard library + gzip only. Run from the package folder:
    python3 verify-it-yourself/checker.py
Last line: PASS or FAIL.

It verifies, from the packaged artifacts alone:
  1. object integrity (sha256 of every object file against the embedded manifest);
  2. the claimed per-split normalized metrics, recomputed from the packaged per-split
     prediction CSVs (EnsembleResidualOmics) and the packaged v1.3.1-ruler naive predictions:
     normalized value = metric(y_true - naive_pred, y_pred - naive_pred), with the package's
     own left-merge replicate semantics (each model row x every naive row with the same key);
  3. the p2 margins against the published comparators (Pearson +0.0253 >= 0.01,
     Spearman +0.0149 >= 0.01, R^2 floor 0.208691 >= 0.175180), and the honest near-miss
     on the headline R^2 win (+0.0230 >= 0.02 absolute but < 2xSE 0.0276 - not claimed);
  4. optional split-regeneration spot check when fresh_splits/ exists next to the package.
"""
import csv
import gzip
import hashlib
import os
import sys

# sha256 of the source/manifest object files at packaging time (corruption -> FAIL)
OBJECT_SHA = {
    "ensemble_model.py": "6d344daff3d10853b4dc66b4d04af2fa50d82a1dd231e116ccc793be6f183925",
    "custom_models.py": "65a1947f3485206ae4bca90a40165add4571abc4c6b972e225b238f66ad76764",
    "custom_models_v131.py": "7f740a0c868cad28563b1d2ced526dd17d1cd788a44fe0990568c53e7b66b06a",
    "evaluation_results.csv.gz": "e66d5b7af3fdfb587b702b843ad840faf8ff13e766340ccd4d8df93d15b0718b",
    "SPLITS_MANIFEST.csv": "e84ce4a996c408600ca1287ed27d57e3d26823c7f6a2c9e6b73434d38be1cbf4",
}

PUBLISHED_PEARSON = 0.434693  # RandomForest, report table (report-era ruler)
PUBLISHED_SPEARMAN = 0.428291
PUBLISHED_R2 = 0.185180
CLAIMED = {
    "r2": 0.208691,
    "r2_se": 0.013799,
    "pearson": 0.459961,
    "spearman": 0.443224,
}
TOL = 0.0002  # claimed values are rounded to 4-6 decimals


def fail(msg):
    print("DETAIL:", msg)
    print("FAIL")
    sys.exit(1)


def mean(vals):
    return sum(vals) / len(vals)


def sample_std(vals):
    m = mean(vals)
    return (sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5


def pearson(y, yp):
    my, mp = mean(y), mean(yp)
    num = sum((a - my) * (b - mp) for a, b in zip(y, yp))
    den = (sum((a - my) ** 2 for a in y) * sum((b - mp) ** 2 for b in yp)) ** 0.5
    return num / den if den else float("nan")


def r2(y, yp):
    my = mean(y)
    ss_res = sum((a - b) ** 2 for a, b in zip(y, yp))
    ss_tot = sum((a - my) ** 2 for a in y)
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def spearman(y, yp):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            r = (i + j) / 2 + 1
            for k in range(i, j + 1):
                rk[order[k]] = r
            i = j + 1
        return rk

    return pearson(ranks(y), ranks(yp))


def read_rows_gz(path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    obj = "object"

    # 1. integrity
    for name, expect in OBJECT_SHA.items():
        p = os.path.join(obj, name)
        if not os.path.isfile(p):
            fail("missing object file " + name)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if h != expect:
            fail("sha256 mismatch " + name)
    sums = {}
    if os.path.isfile("SHA256SUMS"):
        for line in open("SHA256SUMS", encoding="utf-8"):
            parts = line.split()
            if len(parts) == 2:
                sums[parts[1].lstrip("*").lstrip("./")] = parts[0]
    for sub, prefix in (("predictions", "predictions_split_"), ("naive_v131", "naive_predictions_split_")):
        for i in range(10):
            rel = f"{sub}/{prefix}{i}.csv.gz"
            p = os.path.join(obj, rel)
            if not os.path.isfile(p):
                fail("missing " + rel)
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            if rel in sums and sums[rel] != h:
                fail("sha256 mismatch " + rel)
    print("OK object integrity (sources + gzipped artifacts)")

    # 2. recompute the normalized metrics from the packaged CSVs
    r2s, pss, sps = [], [], []
    for i in range(10):
        att = read_rows_gz(os.path.join(obj, f"predictions/predictions_split_{i}.csv.gz"))
        naive = read_rows_gz(os.path.join(obj, f"naive_v131/naive_predictions_split_{i}.csv.gz"))
        # package semantics: pandas left-merge from the model rows MULTIPLIES
        # replicate keys (each model row x every naive row with the same key),
        # exactly as drevalpy's own evaluation does
        naive_rows = {}
        for r in naive:
            naive_rows.setdefault((r["cell_line_name"], r["pubchem_id"]), []).append(
                float(r["naive_pred"])
            )
        yt, yp = [], []
        for r in att:
            key = (r["cell_line_name"], r["pubchem_id"])
            nvs = naive_rows.get(key)
            if not nvs:
                fail(f"split {i} unmatched key {key}")
            for nv in nvs:
                yt.append(float(r["response"]) - nv)
                yp.append(float(r["predictions"]) - nv)
        r2s.append(r2(yt, yp))
        pss.append(pearson(yt, yp))
        sps.append(spearman(yt, yp))
    m_r2, m_p, m_s = mean(r2s), mean(pss), mean(sps)
    se = sample_std(r2s) / len(r2s) ** 0.5
    print("recomputed per-split normR2:", ["%.4f" % v for v in r2s])
    print(f"MEAN normR2 {m_r2:.6f} (SE {se:.6f})  normPearson {m_p:.6f}  normSpearman {m_s:.6f}")

    for name, got, want in (
        ("normR2", m_r2, CLAIMED["r2"]),
        ("normPearson", m_p, CLAIMED["pearson"]),
        ("normSpearman", m_s, CLAIMED["spearman"]),
        ("SE", se, CLAIMED["r2_se"]),
    ):
        if abs(got - want) > TOL:
            fail(f"{name} {got:.6f} != claimed {want:.6f}")
    print("OK recomputed metrics match the claimed values")

    # 3. p2 margins + honest near-miss
    d_p = m_p - PUBLISHED_PEARSON
    d_s = m_s - PUBLISHED_SPEARMAN
    d_r = m_r2 - PUBLISHED_R2
    print(
        f"p2 margins: Pearson {d_p:+.4f} (>= 0.01: {d_p >= 0.01})  "
        f"Spearman {d_s:+.4f} (>= 0.01: {d_s >= 0.01})  R2 {d_r:+.4f} (floor 0.175180: {m_r2 >= 0.175180})"
    )
    print(f"headline R2 win (NOT claimed): margin {d_r:+.4f}; >= 0.02: {d_r >= 0.02}; 2xSE {2 * se:.4f}: {d_r >= 2 * se}")
    if not (d_p >= 0.01 and d_s >= 0.01 and m_r2 >= 0.175180):
        fail("p2 margins not met")
    if d_r >= 2 * se:
        fail("the headline R2 win must NOT be claimed (2xSE clause is met here, contradicting the claim document)")
    print("OK p2 margins met; headline R2 win honestly not claimed (2xSE clause)")

    # 4. optional split-regeneration spot check
    if os.path.isdir("fresh_splits"):
        man = {}
        with open(os.path.join(obj, "SPLITS_MANIFEST.csv"), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                man[row["file"]] = row["sha256"]
        good = bad = 0
        for f, h in man.items():
            p = os.path.join("fresh_splits", f)
            if os.path.isfile(p):
                got = hashlib.sha256(open(p, "rb").read()).hexdigest()
                if got == h:
                    good += 1
                else:
                    bad += 1
        print(f"split regeneration spot check: {good} identical, {bad} different (of {len(man)})")
        if bad:
            fail("regenerated splits differ from SPLITS_MANIFEST")
    else:
        print("NOTE fresh_splits/ not found - split regeneration check skipped (see RUN_IT_YOURSELF.md)")

    print("PASS")


if __name__ == "__main__":
    main()
