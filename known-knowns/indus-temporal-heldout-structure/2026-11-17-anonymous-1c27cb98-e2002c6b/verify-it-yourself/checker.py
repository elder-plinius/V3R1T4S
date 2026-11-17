#!/usr/bin/env python3
"""Standalone checker for the Indus temporal held-out object-type claim.

Stdlib only. Run from the package root via `sh verify-it-yourself/run_checks.sh`
or directly: `python3 verify-it-yourself/checker.py` (any cwd).

What it verifies, written from the claim definition in object/claim_object.json:
  C1  object/output_sweep_main.json pool_detail (1,613 held-out objects, one per dedup
      representative) re-derives the stored per-site 4-class accuracies of the claim
      model, the tuned KN3 baseline and the SIGIL-style synthetic control at pooled,
      Mohenjo-daro and Harappa (and the other listed sites), to the stored rounding.
  C2  The 2-class Seal-vs-Tablet sub-property re-derives from the same rows.
  C3  Pool bookkeeping: len(pool_detail) == stored pooled n == stored pool_reps;
      per-site stored counts == actual per-site counts (n>=20 for the two required sites).
  C4  object/claim_model_frozen.json: seed == stored seed; class_priors re-derived from
      the package's M77 + im77 data (the exact TemplateModel prior formula (n_c+1)/(T+4))
      equal the frozen priors; ctx_counts_sha256 equal to object/claim_object.json.
  C5  object/output_nulltest.json: real > best_control and real > each real baseline
      accuracy at pooled/MD/Harappa; p == 0.0 < 0.001; B == 10000 (>=400 controls).
  C6  Threshold: p < 0.001 at pooled AND Mohenjo-daro AND Harappa, each n >= 20, claim
      accuracy strictly above BOTH baselines at each.
Any single failure -> last line FAIL, exit 1. All pass -> last line PASS, exit 0.
"""
import json, os, sys, csv, collections, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OBJ = os.path.join(ROOT, "object")
DATA = os.path.join(ROOT, "how-we-built-it", "data")

# Integrity pins (sha256 of every file in object/, as frozen at package build time).
PINNED = {
    "claim_model_frozen.json": "19d4a4f4a02417955fd1c2e9350f4e21aac57210249221d74226e8eb13a6950c",
    "claim_object.json": "e2002c6be4971c2e2575dac3cd39c2c57ba0111eafe14dd04cb8671fe57b33da",
    "output_baseline_repro.json": "1d79f1a15b56fa407c16f3c3df378a3bbf117c9a1185523463468f04dbdcb833",
    "output_direction_check.json": "252daa7c3f5029a1334a94cb35023a7f7fc9e1963df0b2065bfbdc230ddf9c85",
    "output_novelty_diff.json": "8b7e2b4ade84aeeb70b9d3990f61ce9d92653dfd2a9c8c15eba0c22efbaa886c",
    "output_nulltest.json": "2f3c6832638d1754f2db9f9fb1d24155d17cd7d5a97060708e0bd8ef95190cb7",
    "output_probes.json": "d67e854ab6b516dbc9a4d077df2a00d85ecf192a3af1e154400debad2d45b5c5",
    "output_sweep_main.json": "2f43fc5f60bdd62c7508c3fef7f8a6420373ed33ec6cd9e61cea5c8f3b2c89d9",
    "output_sweep_secondary.json": "a4db5e42c46b9635975657b7e5a9fc55edd436a1669f2e238b09f73da2111338",
}

def J(name):
    with open(os.path.join(OBJ, name)) as f:
        return json.load(f)

def integrity_check():
    """Return a list of failures for any object/ file whose sha256 drifted from the pins."""
    bad = []
    for name, pin in PINNED.items():
        p = os.path.join(OBJ, name)
        if not os.path.isfile(p):
            bad.append("object/%s missing" % name)
            continue
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if h != pin:
            bad.append("object/%s sha256 %s != pinned %s (file altered)" % (name, h[:16], pin[:16]))
    return bad

def main():
    fails = integrity_check()
    def check(cond, msg):
        if not cond:
            fails.append(msg)
    if fails:
        for f_ in fails[:12]:
            print("FAIL:", f_)
        print("FAIL")
        return 1

    obj = J("claim_object.json")
    sweep = J("output_sweep_main.json")
    frz = J("claim_model_frozen.json")
    ntl = J("output_nulltest.json")
    pd = sweep["pool_detail"]

    # ---- C3 pool bookkeeping ----
    check(len(pd) == obj["result"]["pooled"]["n"], "pooled n %s != len(pool_detail) %d" % (obj["result"]["pooled"]["n"], len(pd)))
    check(len(pd) == obj["pool"]["poolinfo"]["pool_reps"], "pool_reps %s != len(pool_detail) %d" % (obj["pool"]["poolinfo"]["pool_reps"], len(pd)))
    actual = collections.Counter(r["site"] for r in pd)
    for site, n in obj["pool"]["by_site"].items():
        check(actual.get(site) == n, "by_site %s stored %s != actual %s" % (site, n, actual.get(site)))
    for site in ("Mohenjo-daro", "Harappa"):
        check(obj["result"][site]["n"] >= 20, "%s n < 20" % site)

    # ---- C1 per-site 4-class re-derivation ----
    for site in ("pooled", "Mohenjo-daro", "Harappa", "Dholavira", "Lothal"):
        rows = pd if site == "pooled" else [r for r in pd if r["site"] == site]
        n = len(rows)
        st = obj["result"][site]
        acc_c = round(sum(1 for r in rows if r["ok_claim"]) / n, 4)
        acc_k = round(sum(1 for r in rows if r["pred_kn"] == r["otype"]) / n, 4)
        acc_s = round(sum(1 for r in rows if r["pred_synth"] == r["otype"]) / n, 4)
        check(st["n"] == n, "%s stored n %s != %d" % (site, st["n"], n))
        check(st["acc_claim"] == acc_c, "%s acc_claim stored %s != re-derived %s" % (site, st["acc_claim"], acc_c))
        check(st["acc_kn3"] == acc_k, "%s acc_kn3 stored %s != re-derived %s" % (site, st["acc_kn3"], acc_k))
        check(st["acc_synth"] == acc_s, "%s acc_synth stored %s != re-derived %s" % (site, st["acc_synth"], acc_s))
        # ---- C6 threshold ----
        if site in ("pooled", "Mohenjo-daro", "Harappa"):
            check(st["p_boot_claim_vs_both"] < 0.001, "%s p %s not < 0.001" % (site, st["p_boot_claim_vs_both"]))
            check(st["acc_claim"] > st["acc_kn3"] and st["acc_claim"] > st["acc_synth"],
                  "%s claim not above BOTH baselines" % site)

    # ---- C2 2-class re-derivation (Seal vs Tablet; other classes folded) ----
    for key, site in (("two_class_pooled", "pooled"), ("two_class_MD", "Mohenjo-daro"), ("two_class_Harappa", "Harappa")):
        rows = pd if site == "pooled" else [r for r in pd if r["site"] == site]
        rows2 = [r for r in rows if r["otype"] in ("Seal", "Tablet")]
        n2 = len(rows2)
        st = obj["result"][key]
        acc_c2 = round(sum(1 for r in rows2 if r["pred_claim"] == r["otype"]) / n2, 4)
        acc_k2 = round(sum(1 for r in rows2 if r["pred_kn"] == r["otype"]) / n2, 4)
        acc_s2 = round(sum(1 for r in rows2 if r["pred_synth"] == r["otype"]) / n2, 4)
        check(st["n"] == n2, "%s n %s != %d" % (key, st["n"], n2))
        check(st["acc_claim_2c"] == acc_c2, "%s 2c claim stored %s != re-derived %s" % (key, st["acc_claim_2c"], acc_c2))
        check(st["acc_kn3_2c"] == acc_k2, "%s 2c kn stored %s != re-derived %s" % (key, st["acc_kn3_2c"], acc_k2))
        check(st["acc_synth_2c"] == acc_s2, "%s 2c synth stored %s != re-derived %s" % (key, st["acc_synth_2c"], acc_s2))
        check(st["p_boot_2c"] < 0.001, "%s 2c p not < 0.001" % key)

    # ---- C4 frozen model record ----
    check(frz["seed"] == obj["seed"] == 20261117, "seed mismatch: %s / %s" % (frz["seed"], obj["seed"]))
    check(frz["ctx_counts_sha256"] == obj["frozen_model_ctx_sha256"], "frozen ctx_counts_sha256 mismatch with claim_object")

    # Re-derive the TemplateModel class priors from the package data.
    def mco(otype):
        if otype in ("seal", "sealing"):
            return "Seal"
        if otype in ("miniature tablet", "copper tablet", "ivory/bone rod", "bronze implement"):
            return "Tablet"
        if otype == "pottery graffito":
            return "Pottery"
        return "Other"

    per = collections.defaultdict(list)
    with open(os.path.join(DATA, "m77_indusscript_real_corpus.csv")) as f:
        for r in csv.DictReader(f):
            o = int(r["inscription_id"].split(".")[0])
            signs = tuple(int(s.replace("MSg", "")) for s in r["sign_sequence"].split()
                          if int(s.replace("MSg", "")) != 0)
            per[o].append(signs)
    im77 = {}
    with open(os.path.join(DATA, "im77_corpus_lines.csv")) as f:
        for r in csv.DictReader(f):
            im77.setdefault(int(r["text_no"]), []).append(r)
    for v in im77.values():
        v.sort(key=lambda r: int(r["line"]) if r["line"].isdigit() else 99)
    tot = collections.Counter()
    nlines = 0
    for txt, rows2 in sorted(per.items()):
        im = im77.get(txt, [])
        for j, s in enumerate(rows2):
            if not s:
                continue
            nlines += 1
            otype = im[j]["object_type"] if j < len(im) else "unknown"
            tot[mco(otype)] += 1
    check(nlines == sweep["m77"]["lines"], "M77 training lines re-derived %d != stored %s" % (nlines, sweep["m77"]["lines"]))
    T = sum(tot.values())
    C = 4
    for c in ("Seal", "Tablet", "Pottery", "Other"):
        derived = (tot.get(c, 0) + 1.0) / (T + C)
        stored = frz["class_priors"].get(c)
        check(stored is not None and abs(stored - derived) < 1e-9,
              "class prior %s: frozen %s != re-derived %s" % (c, stored, derived))

    # ---- C5 null test record ----
    check(ntl["B"] >= 400, "null test B %s < 400" % ntl["B"])
    for site in ("pooled", "Mohenjo-daro", "Harappa"):
        d = ntl[site]
        check(d["real"] > d["best_control"], "%s real %s <= best_control %s" % (site, d["real"], d["best_control"]))
        check(d["real"] > d["real_kn"] and d["real"] > d["real_synth"], "%s real not above both baselines" % site)
        check(d["real_beats_all_controls"] in (True, "true"), "%s real_beats_all_controls false" % site)
        check(d["p"] == 0.0 and d["p"] < 0.001, "%s null p %s not < 0.001" % (site, d["p"]))

    # cross-consistency of the three accuracy ledgers
    for site in ("pooled", "Mohenjo-daro", "Harappa"):
        check(ntl[site]["real"] == obj["result"][site]["acc_claim"],
              "%s nulltest real %s != claim_object acc_claim %s" % (site, ntl[site]["real"], obj["result"][site]["acc_claim"]))
        check(ntl[site]["real_kn"] == obj["result"][site]["acc_kn3"],
              "%s nulltest KN %s != claim_object %s" % (site, ntl[site]["real_kn"], obj["result"][site]["acc_kn3"]))
        check(ntl[site]["real_synth"] == obj["result"][site]["acc_synth"],
              "%s nulltest synth %s != claim_object %s" % (site, ntl[site]["real_synth"], obj["result"][site]["acc_synth"]))

    if fails:
        for f_ in fails[:12]:
            print("FAIL:", f_)
        print("FAIL")
        return 1
    print("pooled claim %.4f vs KN %.4f / synth %.4f (p=%.3f); Mohenjo-daro %.4f (p=%.3f); Harappa %.4f (p=%.3f); frozen priors re-derived from M77+im77; pool n=%d"
          % (obj["result"]["pooled"]["acc_claim"], obj["result"]["pooled"]["acc_kn3"], obj["result"]["pooled"]["acc_synth"],
             obj["result"]["pooled"]["p_boot_claim_vs_both"],
             obj["result"]["Mohenjo-daro"]["acc_claim"], obj["result"]["Mohenjo-daro"]["p_boot_claim_vs_both"],
             obj["result"]["Harappa"]["acc_claim"], obj["result"]["Harappa"]["p_boot_claim_vs_both"], len(pd)))
    print("PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
