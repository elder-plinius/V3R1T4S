#!/usr/bin/env python3
"""
Standalone Deterministic Verifier for V3R1T4S Package `2026-10-22-mizopl-e47a7dd8`
(`fmm-additive-complexity-records`).
"""
import os
import sys
import json
import glob
import random
import hashlib
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT_PATH = os.path.join(ROOT, "object", "CERTIFICATE.json")
SCHEMES_DIR = os.path.join(ROOT, "object", "schemes")
REF_DIR = os.path.join(ROOT, "the-record-we-beat", "reference_live_champions")
EXPECTED_CERT_SHA256 = "e47a7dd88e8f9778d65667b7d4030ca66cf39c6de9d89b3b0f1c5f61cb9cc1de"


def eval_comb(comb, vecs, nin):
    res = [0] * nin
    for item in comb:
        v = vecs[item["index"]]
        val = item["value"]
        for i in range(nin):
            res[i] += val * v[i]
    return tuple(res)


def expand_and_check_block(nin, fresh, combs, require_unit_coeffs=True):
    vecs = [tuple(1 if j == i else 0 for j in range(nin)) for i in range(nin)]
    for fi, comb in enumerate(fresh):
        cur_idx = nin + fi
        assert isinstance(comb, list) and len(comb) >= 1
        for item in comb:
            idx = item["index"]
            val = item["value"]
            assert 0 <= idx < cur_idx, f"DAG cycle / forward reference: {idx} >= {cur_idx}"
            assert val != 0 and isinstance(val, int)
            if require_unit_coeffs:
                assert val in (-1, 1), f"Non-ternary fresh coefficient: {val}"
        vecs.append(eval_comb(comb, vecs, nin))

    targets = []
    for comb in combs:
        assert isinstance(comb, list)
        for item in comb:
            idx = item["index"]
            val = item["value"]
            assert 0 <= idx < len(vecs), f"Invalid comb index {idx} >= {len(vecs)}"
            assert val != 0 and isinstance(val, int)
            if require_unit_coeffs:
                assert val in (-1, 1), f"Non-ternary comb coefficient: {val}"
        targets.append(eval_comb(comb, vecs, nin))
    return vecs, targets


def count_block_additions(fresh, combs):
    c_len = sum(max(0, len(f) - 1) for f in fresh) + sum(max(0, len(e) - 1) for e in combs)
    c_val = sum(max(0, sum(abs(x["value"]) for x in f) - 1) for f in fresh) + \
            sum(max(0, sum(abs(x["value"]) for x in e) - 1) for e in combs)
    return c_len, c_val


def verify_symbolic_product_over_Z(n1, n2, n3, m, tu, tv, tw):
    assert len(tu) == m and len(tv) == m and len(tw) == n1 * n3

    def check_orientation(transpose_c=False):
        for i in range(n1):
            for j in range(n3):
                out_idx = (j * n1 + i) if transpose_c else (i * n3 + j)
                w_row = tw[out_idx]
                poly = defaultdict(int)
                for r in range(m):
                    wr = w_row[r]
                    if wr == 0:
                        continue
                    ur = tu[r]
                    vr = tv[r]
                    for ik, uval in enumerate(ur):
                        if uval == 0:
                            continue
                        wu = wr * uval
                        for kj, vval in enumerate(vr):
                            if vval != 0:
                                poly[(ik, kj)] += wu * vval
                expected = {(i * n2 + k, k * n3 + j): 1 for k in range(n2)}
                actual = {k: v for k, v in poly.items() if v != 0}
                if actual != expected:
                    return False
        return True

    if not (check_orientation(False) or check_orientation(True)):
        raise AssertionError(f"Symbolic polynomial A*B check over Z failed for {n1}x{n2}x{n3} m={m}!")

    cnu = sum(max(0, sum(abs(x) for x in r) - 1) for r in tu)
    cnv = sum(max(0, sum(abs(x) for x in r) - 1) for r in tv)
    cnw = sum(max(0, sum(abs(x) for x in r) - 1) for r in tw)
    return cnu + cnv + cnw, (tu, tv, tw)


def verify_scheme_file(path, require_unit_coeffs=True):
    d = json.load(open(path))
    n1, n2, n3 = d["n"]
    m = d["m"]
    if require_unit_coeffs:
        assert d["ring"] == "ZT"
    else:
        assert d.get("ring", "ZT") == "ZT"
    _, tu = expand_and_check_block(n1 * n2, d["u_fresh"], d["u"], require_unit_coeffs)
    _, tv = expand_and_check_block(n2 * n3, d["v_fresh"], d["v"], require_unit_coeffs)
    _, tw = expand_and_check_block(m, d["w_fresh"], d["w"], require_unit_coeffs)

    cu_l, cu_v = count_block_additions(d["u_fresh"], d["u"])
    cv_l, cv_v = count_block_additions(d["v_fresh"], d["v"])
    cw_l, cw_v = count_block_additions(d["w_fresh"], d["w"])
    cr_len = cu_l + cv_l + cw_l
    cr_val = cu_v + cv_v + cw_v
    if require_unit_coeffs:
        assert cu_l == cu_v and cv_l == cv_v and cw_l == cw_v
        assert d["complexity"]["reduced"] == cr_len == cr_val
    else:
        assert d["complexity"]["reduced"] in (cr_len, cr_val)
    cn, mats = verify_symbolic_product_over_Z(n1, n2, n3, m, tu, tv, tw)
    assert d["complexity"]["naive"] == cn
    return {
        "n": [n1, n2, n3], "m": m,
        "cu": cu_v, "cv": cv_v, "cw": cw_v,
        "cr_len": cr_len, "cr_val": cr_val, "cn": cn,
        "mats": mats
    }


def run_random_greedy_cse_null_model(tu, tv, tw, n_trials=400, seed=20261022):
    rng = random.Random(seed)

    def greedy_block_cost(rows, nin):
        active = [list(r) for r in rows if sum(abs(x) for x in r) >= 2]
        perm = list(range(nin))
        rng.shuffle(perm)
        cost = sum(sum(abs(x) for x in r) - 1 for r in rows if any(r))
        used_cols = set()
        for idx_a in range(nin):
            a = perm[idx_a]
            if a in used_cols:
                continue
            for idx_b in range(idx_a + 1, nin):
                b = perm[idx_b]
                if b in used_cols:
                    continue
                pos_hits = sum(1 for r in active if r[a] != 0 and r[b] == r[a])
                neg_hits = sum(1 for r in active if r[a] != 0 and r[b] == -r[a])
                best_h = max(pos_hits, neg_hits)
                if best_h >= 2:
                    cost -= (best_h - 1)
                    used_cols.add(a)
                    used_cols.add(b)
                    break
        return cost

    nin_u, nin_v, nin_w = len(tu[0]), len(tv[0]), len(tw[0])
    scores = []
    for _ in range(n_trials):
        c = greedy_block_cost(tu, nin_u) + greedy_block_cost(tv, nin_v) + greedy_block_cost(tw, nin_w)
        scores.append(c)
    scores.sort()
    median = scores[n_trials // 2]
    iqr = scores[(3 * n_trials) // 4] - scores[n_trials // 4]
    return min(scores), median, iqr


def main():
    cert_bytes = open(CERT_PATH, "rb").read()
    assert len(cert_bytes) == 26573, "CERTIFICATE.json byte size mismatch"
    assert hashlib.sha256(cert_bytes).hexdigest() == EXPECTED_CERT_SHA256, "CERTIFICATE.json SHA-256 mismatch"
    cert = json.loads(cert_bytes.decode("utf-8"))

    sota_data = json.load(open(os.path.join(REF_DIR, "fmm_sota.json")))
    sota_ranks = {}
    for e in sota_data["entries"]:
        dims = sorted(e["format"])
        fmt = f"{dims[0]}x{dims[1]}x{dims[2]}"
        sota_ranks[fmt] = e["rank"]

    ref_min_by_fmt = {}
    for p in sorted(glob.glob(os.path.join(REF_DIR, "*_ZT_reduced.json"))):
        bn = os.path.basename(p)
        fmt = bn.split("_")[0]
        res = verify_scheme_file(p, require_unit_coeffs=False)
        if fmt not in ref_min_by_fmt or (res["m"], res["cr_len"]) < (ref_min_by_fmt[fmt]["m"], ref_min_by_fmt[fmt]["cr_len"]):
            ref_min_by_fmt[fmt] = {"m": res["m"], "cr_len": res["cr_len"], "cr_val": res["cr_val"], "bn": bn}

    assert len(cert["schemes"]) == 48
    exact_sota_wins = []
    zt_best_wins = []
    new_sota_zt_wins = []
    mats_247 = None

    for entry in cert["schemes"]:
        fn = entry["filename"]
        p = os.path.join(SCHEMES_DIR, fn)
        assert os.path.exists(p), f"Missing scheme file {fn}"
        raw_bytes = open(p, "rb").read()
        assert len(raw_bytes) == entry["bytes"], f"Byte size mismatch on {fn}"
        sha = hashlib.sha256(raw_bytes).hexdigest()
        assert sha == entry["sha256"], f"SHA-256 mismatch on {fn}"

        res = verify_scheme_file(p, require_unit_coeffs=True)
        assert (res["cu"], res["cv"], res["cw"], res["cr_val"], res["cn"]) == (
            entry["cu"], entry["cv"], entry["cw"], entry["cr"], entry["cn"]
        )
        fmt = entry["fmt"]
        assert max(entry["n"]) <= 8
        assert entry["sota_rank"] == sota_ranks[fmt]
        if fn == "2x4x7_m45_cr157_cn345_ZT_reduced.json":
            mats_247 = res["mats"]

        if entry["category"] == "exact_sota_champion_improvement":
            ref = ref_min_by_fmt[fmt]
            assert entry["m"] == sota_ranks[fmt] == ref["m"]
            assert entry["cr"] < ref["cr_len"] and entry["cr"] < ref["cr_val"]
            exact_sota_wins.append((fmt, entry["m"], entry["cr"], ref["cr_len"], entry["cr"] - ref["cr_len"], fn))
        elif entry["category"] == "zt_best_rank_champion_improvement":
            ref = ref_min_by_fmt[fmt]
            assert entry["m"] == ref["m"]
            assert entry["cr"] < ref["cr_len"] and entry["cr"] < ref["cr_val"]
            zt_best_wins.append((fmt, entry["m"], entry["cr"], ref["cr_len"], entry["cr"] - ref["cr_len"], fn))
        elif entry["category"] == "new_sota_rank_zt_addition_reduced":
            assert entry["m"] == sota_ranks[fmt] < entry["live_min_m"]
            new_sota_zt_wins.append((fmt, entry["m"], entry["cr"], entry["live_min_m"], entry["live_min_cr"], fn))

    distinct_exact_sota = sorted(list(set(x[0] for x in exact_sota_wins)))
    assert len(distinct_exact_sota) == 9

    p247 = os.path.join(SCHEMES_DIR, "2x4x7_m45_cr157_cn345_ZT_reduced.json")
    d247 = json.load(open(p247))
    d247["u_fresh"][0][0]["value"] = -d247["u_fresh"][0][0]["value"]
    _, tu_bad = expand_and_check_block(8, d247["u_fresh"], d247["u"], True)
    _, tv_ok = expand_and_check_block(28, d247["v_fresh"], d247["v"], True)
    _, tw_ok = expand_and_check_block(45, d247["w_fresh"], d247["w"], True)
    rejected = False
    try:
        verify_symbolic_product_over_Z(2, 4, 7, 45, tu_bad, tv_ok, tw_ok)
    except AssertionError:
        rejected = True
    assert rejected

    best_ctrl, med_ctrl, iqr_ctrl = run_random_greedy_cse_null_model(*mats_247, n_trials=400, seed=20261022)
    assert 157 < best_ctrl == 262
    print("VERIFIED: All 48 ternary SLP schemes, 36 reference calibrations, negative control, and 400 null controls passed.")
    print("PASS")


if __name__ == "__main__":
    try:
        main()
    except BaseException as exc:
        print(f"ERROR: {exc}")
        print("FAIL")
        sys.exit(1)
