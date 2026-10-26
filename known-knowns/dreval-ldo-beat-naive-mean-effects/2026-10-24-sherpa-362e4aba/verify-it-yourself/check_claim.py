#!/usr/bin/env python3
"""Standalone checker for the dreval-ldo claim. **Python 3 standard library only** -- no numpy, no pandas,
no drevalpy, no network, no dataset download. Written from the success criterion.

It recomputes the benchmark's own statistic from the shipped per-split test predictions:

  normalized R^2 = R^2 of (y_true - ruler) against (y_pred - ruler), per CV split, then averaged, where the
  ruler is the NaiveMeanEffectsPredictor's prediction for the same test pair in the same split. This is
  drevalpy's `_normalize_metrics_by_mean_effects` reduced to the quantity it produces, with predictions
  aligned row for row (drevalpy left-merges on keys, which double-counts CTRPv2's duplicated
  (cell line, drug) pairs; both figures are reported in RECEIPTS.md).
"""
import csv, gzip, hashlib, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(HERE, os.pardir, "object")
PUBLISHED_MAX = 0.0235
MARGIN = 0.02
GENS = ("seed42", "independent")


def rows(path):
    with gzip.open(path, "rt", newline="") as fh:
        for r in csv.DictReader(fh):
            yield r


def split_file(tag, i, what="test_predictions"):
    return os.path.join(OBJ, "%s_split_%d_%s.csv.gz" % (tag, i, what))


def r2(pairs):
    """pairs: iterable of (y, p). Returns 1 - SS_res/SS_tot about the mean of y."""
    ys = [y for y, _ in pairs]
    n = len(ys)
    if n < 2:
        return float("nan")
    mu = sum(ys) / n
    ss_tot = sum((y - mu) ** 2 for y in ys)
    ss_res = sum((y - p) ** 2 for y, p in pairs)
    return float("nan") if ss_tot == 0 else 1.0 - ss_res / ss_tot


def mean_se(v):
    n = len(v)
    m = sum(v) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in v) / (n - 1)) if n > 1 else float("nan")
    return m, sd / math.sqrt(n), min(v), sum(1 for x in v if x > 0)


def load_roles(tag):
    out = {}
    for r in rows(os.path.join(OBJ, "%s_split_drug_roles.csv.gz" % tag)):
        out.setdefault(int(r["CV_split"]), {}).setdefault(r["role"], set()).add(r["pubchem_id"])
    return out


def score(tag, keep=None):
    vals = []
    for i in range(10):
        pr = []
        for r in rows(split_file(tag, i)):
            if keep and not keep(r):
                continue
            b = float(r["pred_NaiveMeanEffectsPredictor"])
            pr.append((float(r["response"]) - b, float(r["pred_PotencyTransfer"]) - b))
        if len(pr) >= 2:
            vals.append(r2(pr))
    return vals


def main():
    fail = 0
    combos = {r["pubchem_id"] for r in csv.DictReader(open(os.path.join(OBJ, "drug_names.csv")))
              if "mol-mol" in r["drug_name"]}
    print("=" * 78)
    print("0. object integrity: every shipped file must match object/MANIFEST.sha256")
    man = os.path.join(OBJ, "MANIFEST.sha256")
    listed, bad, missing = 0, [], []
    with open(man) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            want, name = line.split(None, 1)
            name = name.lstrip("*").strip()
            fp = os.path.join(OBJ, name)
            if not os.path.isfile(fp):
                missing.append(name); continue
            listed += 1
            h = hashlib.sha256()
            with open(fp, "rb") as g:
                for chunk in iter(lambda: g.read(1 << 20), b""):
                    h.update(chunk)
            if h.hexdigest() != want:
                bad.append(name)
    present = [f for f in sorted(os.listdir(OBJ)) if f != "MANIFEST.sha256"]
    extra = sorted(set(present) - {l.split(None, 1)[1].lstrip("*").strip()
                                   for l in open(man).read().splitlines() if l.strip()})
    print("   %d files listed, %d verified, %d mismatched, %d missing, %d unlisted"
          % (listed + len(missing), listed - len(bad), len(bad), len(missing), len(extra)))
    if bad or missing or extra:
        for n in (bad + missing + extra)[:5]:
            print("   FAILED: %s" % n)
        print("   FAILED: the object does not match its manifest -- it has been altered"); fail += 1
    else:
        print("   ok: the object is byte-for-byte as shipped")

    print("\n1. leave-drug-out property: no test drug may appear in train or validation")
    for tag in GENS:
        roles = load_roles(tag)
        bad = []
        for i in range(10):
            te, trv = roles[i].get("test", set()), roles[i].get("train", set()) | roles[i].get("validation", set())
            pred = {r["pubchem_id"] for r in rows(split_file(tag, i))}
            if te & trv:
                bad.append((i, "test drug in train/validation", sorted(te & trv)[:3]))
            if pred - te:
                bad.append((i, "predicted drug outside the test fold", sorted(pred - te)[:3]))
            if te - pred:
                bad.append((i, "test drug with no prediction (abstention)", sorted(te - pred)[:3]))
        print("   %-12s %s" % (tag, "ok, all 10 splits drug-disjoint and complete" if not bad else "FAILED: %s" % bad))
        fail += bool(bad)

    print("\n2. ruler authenticity: regress the shipped ruler on a replay built from the object")
    for tag in GENS:
        roles = load_roles(tag)
        allrows = []
        for i in range(10):
            allrows += [(r["pubchem_id"], r["cell_line_name"], float(r["response"])) for r in rows(split_file(tag, i))]
        worst_s = worst_i = 0.0
        for i in range(10):
            tr = roles[i].get("train", set())
            va = roles[i].get("validation", set())
            obs = {}
            for r in rows(split_file(tag, i)):
                obs.setdefault(r["cell_line_name"], set()).add(round(float(r["pred_NaiveMeanEffectsPredictor"]), 6))
            if any(len(v) > 1 for v in obs.values()):
                print("   FAILED: the ruler varies within a cell line, so it is not a cell-line mean"); fail += 1; break
            obs = {c: next(iter(v)) for c, v in obs.items()}
            # drevalpy 1.3.5 mutates the stored split in place, so a model in position k of a run is fitted
            # on train + k copies of validation. Try each k; the ruler must match one with slope 1, which
            # still rejects any RESCALING of the cell-line effects (that changes the slope for every k).
            best = None
            for k in range(1, 13):
                s = {}
                for d, c, y in allrows:
                    w = 1 if d in tr else (k if d in va else 0)
                    if w:
                        a = s.setdefault(c, [0.0, 0])
                        a[0] += w * y; a[1] += w
                rep = {c: a[0] / a[1] for c, a in s.items() if a[1]}
                xs = [(rep[c], obs[c]) for c in obs if c in rep]
                if len(xs) < 3:
                    continue
                n = len(xs); sx = sum(x for x, _ in xs); sy = sum(y for _, y in xs)
                sxx = sum(x * x for x, _ in xs); sxy = sum(x * y for x, y in xs)
                den = n * sxx - sx * sx
                if den == 0:
                    continue
                slope = (n * sxy - sx * sy) / den
                inter = (sy - slope * sx) / n
                cand = (abs(slope - 1.0), abs(inter))
                if best is None or sum(cand) < sum(best):
                    best = cand
            if best:
                worst_s = max(worst_s, best[0]); worst_i = max(worst_i, best[1])
        print("   %-12s worst |slope-1| = %.5f   worst |intercept| = %.5f" % (tag, worst_s, worst_i))
        if worst_s > 0.02 or worst_i > 0.02:
            print("   FAILED: the ruler is not an unscaled cell-line mean over the training drugs"); fail += 1

    print("\n3. tamper check: the model's predictions must actually differ from the ruler's")
    for tag in GENS:
        same = sum(1 for i in range(10)
                   if all(abs(float(r["pred_PotencyTransfer"]) - float(r["pred_NaiveMeanEffectsPredictor"])) < 1e-9
                          for r in rows(split_file(tag, i))))
        print("   %-12s splits whose predictions equal the ruler's: %d/10%s" % (tag, same, "   <- ok" if not same else "   <- FAILED"))
        if same:
            print("   FAILED: a split's predictions are identical to the ruler, so they are not this model's output"); fail += 1

    print("\n4. the benchmark statistic, recomputed from the shipped predictions")
    res = {}
    for tag in GENS:
        v = score(tag); m, se, mn, pos = mean_se(v); res[tag] = (m, se)
        print("   %-12s PotencyTransfer  normalized R^2 = %+.4f  (SE %.4f, %d splits, %d/%d positive, worst %+.4f)"
              % (tag, m, se, len(v), pos, len(v), mn))
        rv = []
        for i in range(10):
            pr = [(float(r["response"]) - float(r["pred_NaiveMeanEffectsPredictor"]), 0.0) for r in rows(split_file(tag, i))]
            rv.append(r2(pr))
        bm, bse, _, _ = mean_se(rv)
        print("   %-12s ruler            normalized R^2 = %+.4f  (SE %.4f)   <- published -0.0169" % (tag, bm, bse))
        if not (-0.06 < bm < 0.0):
            print("   FAILED: the ruler is not reproducing its published behaviour"); fail += 1

    print("\n5. margin over the published maximum (%+.4f)" % PUBLISHED_MAX)
    for tag in GENS:
        m, se = res[tag]
        c1, c2 = m > PUBLISHED_MAX + MARGIN, m > PUBLISHED_MAX + 2 * se
        print("   %-12s > max+0.02 (%+.4f): %-3s   > max+2SE (%+.4f): %s"
              % (tag, PUBLISHED_MAX + MARGIN, "yes" if c1 else "NO", PUBLISHED_MAX + 2 * se, "yes" if c2 else "NO"))
        fail += not (c1 and c2)

    print("\n6. the published leader's own same-splits re-run, from the shipped predictions")
    for tag in GENS:
        mv, lv = [], []
        for i in range(10):
            ruler = {}
            for r in rows(split_file(tag, i)):
                ruler[(r["cell_line_name"], r["pubchem_id"])] = float(r["pred_NaiveMeanEffectsPredictor"])
            pr = [(float(r["response"]) - float(r["pred_NaiveMeanEffectsPredictor"]),
                   float(r["pred_PotencyTransfer"]) - float(r["pred_NaiveMeanEffectsPredictor"]))
                  for r in rows(split_file(tag, i))]
            mv.append(r2(pr))
            lp = []
            for r in rows(split_file(tag, i, "leader_predictions")):
                b = ruler.get((r["cell_line_name"], r["pubchem_id"]))
                if b is None:
                    print("   FAILED: a leader prediction has no matching ruler value"); fail += 1; lp = None; break
                lp.append((float(r["response"]) - b, float(r["pred_MultiOmicsNeuralNetwork"]) - b))
            if lp is None:
                break
            lv.append(r2(lp))
        if len(lv) < 10:
            continue
        d = [a - b for a, b in zip(mv, lv)]
        lm, lse, _, _ = mean_se(lv)
        print("   %-12s leader re-run %+.4f (SE %.4f)   claim - leader %+.4f   claim wins %d/10 splits"
              % (tag, lm, lse, sum(d) / len(d), sum(1 for x in d if x > 0)))
        if not all(x > 0 for x in d):
            print("   FAILED: the claim must beat the leader's same-splits re-run on every split"); fail += 1

    print("\n7. the gain is not carried by the drug-combination leak (drevalpy issue #300)")
    for tag in GENS:
        s = mean_se(score(tag, lambda r: r["pubchem_id"] not in combos))
        c = mean_se(score(tag, lambda r: r["pubchem_id"] in combos))
        print("   %-12s single agents %+.4f (SE %.4f) | combinations %+.4f (SE %.4f)" % (tag, s[0], s[1], c[0], c[1]))
        if s[0] <= PUBLISHED_MAX + MARGIN:
            print("   FAILED: single agents alone must still clear the bar"); fail += 1

    print("\n" + "=" * 78)
    print("PASS" if fail == 0 else "FAIL (%d problems)" % fail)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
