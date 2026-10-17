"""Standalone checker (Python standard library only) for one antibiotic of the NCBI E. coli/Shigella genotype-phenotype claim.
Downloads the sha256-pinned NCBI export and cluster list, recomputes eligibility, R/S phenotypes, the cluster split, the published
genotype rule (PMC13513162, as reimplemented), and scores the saved per-isolate model predictions. Last line: PASS or FAIL."""
import csv, hashlib, json, os, random, re, sys, urllib.request
csv.field_size_limit(1 << 30)
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE)
E = json.load(open(os.path.join(HERE, "expected.json"), encoding="utf-8")); AB = E["antibiotic"]
def fail(m): print("reason:", m); print("FAIL"); sys.exit(1)
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
for f, h in E["object_sha256"].items():
    if sha(os.path.join(PKG, "object", f)) != h: fail("sha256 mismatch for object/" + f)
print("object files: sha256 OK")
cache = os.path.join(HERE, ".cache"); os.makedirs(cache, exist_ok=True)
def get(url, h):
    p = os.path.join(cache, url.rsplit("/", 1)[1])
    if not (os.path.exists(p) and sha(p) == h):
        req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-package-checker"})
        with urllib.request.urlopen(req, timeout=600) as r, open(p, "wb") as f:
            while True:
                b = r.read(1 << 22)
                if not b: break
                f.write(b)
    if sha(p) != h: fail("sha256 of " + url + " differs (see README for where NCBI keeps this export)")
    return p
meta = get(E["metadata_url"], E["metadata_sha256"]); cl = get(E["clusters_url"], E["clusters_sha256"])
pds = {}
with open(cl, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter="\t"): pds.setdefault(row["target_acc"], row["PDS_acc"])
present = lambda s: s.strip() not in ("", "NULL")
truth, geno, clus = {}, {}, {}
with open(meta, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        if not (present(row["asm_acc"]) and present(row["AMR_genotypes"]) and present(row["AST_phenotypes"])): continue
        iso = row["target_acc"]; c = pds.get(iso) or "NOPDS_" + iso
        if int(hashlib.sha256(("V3R1T4S-ecoli-2026-10-16|" + c).encode()).hexdigest(), 16) % 100 >= 20: continue   # TEST only
        calls = set()
        for t in row["AST_phenotypes"].split(","):
            t = t.strip()
            if "=" in t:
                n, v = t.rsplit("=", 1)
                if n == AB and v in ("R", "S"): calls.add(v)
        for v in calls: truth[(iso, v)] = 1
        if calls: geno[iso] = row["AMR_genotypes"]; clus[iso] = c
def toks(field):   # name=STATUS tokens; a bare name means COMPLETE (FTP TSV convention)
    out = []
    for t in field.split(","):
        t = t.strip()
        if t and t != "NULL": out.append(tuple(t.rsplit("=", 1)) if "=" in t else (t, "COMPLETE"))
    return [n for n, s in out if s in ("COMPLETE", "POINT")]
PAT = {"acq": r"^bla(?!EC\b|EC-|HER)",
       "esc": r"^bla(CTX-M|CMY|DHA|KPC|NDM|VIM|IMP|VEB|GES|PER|ACC|FOX|MOX|ACT|OXA-(48|181|232|244|162|204|370|484|1397)\b)",
       "carba": r"^bla(KPC|NDM|VIM|IMP|OXA-(48|181|232|244|162|204|370|484)\b|GES-(2|4|5|6|14|16|20)\b)",
       "quin": r"^(gyrA_|parC_(S80|E84)|parE_|qnr|qepA|oqx|aac\(6'\)-Ib-cr)",
       "gen": r"^(aac\(3\)|aac\(6'\)-(Ib|IIc|Il)|ant\(2''\)|armA|rmt|npmA)", "tet": r"^tet\("}
KEY = {"ampicillin": "acq", "amoxicillin-clavulanic acid": "acq", "ceftriaxone": "esc", "meropenem": "carba",
       "ciprofloxacin": "quin", "gentamicin": "gen", "tetracycline": "tet"}
def rule(field):
    n = toks(field)
    if AB == "trimethoprim-sulfamethoxazole": return "R" if any(x.startswith("dfr") for x in n) and any(x.startswith("sul") for x in n) else "S"
    return "R" if any(re.match(PAT[KEY[AB]], x) for x in n) else "S"
rows = list(csv.DictReader(open(os.path.join(PKG, "object", E["predictions_file"]), newline="", encoding="utf-8")))
got = {(r["isolate"], r["AST_call"]) for r in rows}
if got != set(truth): fail(f"TEST rows differ from the recomputed split/phenotypes ({len(got)} vs {len(truth)})")
for r in rows:
    if r["rule_pred"] != rule(geno[r["isolate"]]): fail("published-rule prediction differs for " + r["isolate"])
    if r["cluster"] != clus[r["isolate"]]: fail("cluster differs for " + r["isolate"])
    if (float(r["model_prob"]) >= E["threshold"]) != (r["model_pred"] == "R"): fail("model_pred inconsistent with model_prob and threshold")
print(f"recomputed TEST rows: {len(rows)} comparisons, {len(set(clus.values()))} clusters; rule predictions and clusters identical")
def stats(idx, col):
    tp = fp = tn = fn = 0
    for i in idx:
        y = rows[i]["AST_call"] == "R"; p = rows[i][col] == "R"
        tp += y and p; fp += (not y) and p; tn += (not y) and (not p); fn += y and (not p)
    return 2 * tp / max(2 * tp + fp + fn, 1), (tp + tn) / max(len(idx), 1), (tp, fp, tn, fn)
allidx = list(range(len(rows)))
f1m, accm, cm = stats(allidx, "model_pred"); f1r, accr, cr = stats(allidx, "rule_pred")
print(f"model F1 {100*f1m:.2f} acc {100*accm:.2f} TP/FP/TN/FN {cm} | rule F1 {100*f1r:.2f} acc {100*accr:.2f} TP/FP/TN/FN {cr}")
byc = {}
for i, r in enumerate(rows): byc.setdefault(r["cluster"], []).append(i)
keys = sorted(byc); rng = random.Random(20261016); bm, bd = [], []
for _ in range(E["bootstrap_reps"]):
    idx = [i for _ in keys for i in byc[keys[rng.randrange(len(keys))]]]
    a = stats(idx, "model_pred")[0]; b = stats(idx, "rule_pred")[0]; bm.append(a); bd.append(a - b)
bm.sort(); bd.sort(); lo = lambda v: v[int(0.025 * len(v))]
print(f"cluster bootstrap ({E['bootstrap_reps']} reps, stdlib RNG): model F1 2.5% {100*lo(bm):.2f}; paired diff 2.5% {100*lo(bd):.2f}")
pf, pa = E["published_F1"], E["published_accuracy"]
checks = {f"F1 {100*f1m:.2f} >= published {pf} + 3": 100 * f1m >= pf + 3,
          f"F1 {100*f1m:.2f} >= recomputed rule {100*f1r:.2f} + 3": f1m >= f1r + 0.03,
          f"bootstrap 2.5% {100*lo(bm):.2f} > max(published, rule)": 100 * lo(bm) > max(pf, 100 * f1r),
          "paired-difference 2.5% > 0": lo(bd) > 0,
          f"accuracy {100*accm:.2f} >= published {pa}": 100 * accm >= pa,
          "matches claimed F1/accuracy": abs(f1m - E["claimed_F1"]) < 1e-9 and abs(accm - E["claimed_accuracy"]) < 1e-9}
for k, v in checks.items(): print(("ok   " if v else "FAIL ") + k)
if not all(checks.values()): fail("a criterion threshold is not met")
print("PASS")
