#!/usr/bin/env python3
"""Standalone checker for VBCLC-152 (partial win p2), written from the definition.

Python 3 standard library only, no network, runs in ~2 seconds.
Run via: sh verify-it-yourself/run_checks.sh from the package root.

Verifies:
  0. Every file in object/ matches verify-it-yourself/MANIFEST.sha256;
  1. Hand-executability constraints on object/vbclc.py and object/HAND_PROCEDURE.md:
     16 + 20 + 96 + 20 = 152 table entries (<= 200), 1 per-folio state bit sigma_f in {0, 1},
     and deterministic encryption;
  2. Saved 200-stream evaluation (object/vbclc_200streams_evaluation.json) across all 6
     dialect x transliteration cells (A/ZL3b, B/ZL3b, A/IT2a, B/IT2a, A/RF1b-e, B/RF1b-e):
     200/200 (100.0%) joint pass rate on every cell (100/100 Latin, 100/100 Italian);
  3. Published baseline failures in object/reference_calibration.json (slot generator 0% on B /
     10% on A, Cardan grille 0% across all modes, unmodified Naibbe 0% strict-Zipf);
  4. Saved 400-control null suite (object/null_suite_400_results.json) across all 4 cells
     (A/ZL3b, B/ZL3b, A/IT2a, B/IT2a): real strictly beats all 400 controls;
  5. Live first-principles stdlib-only re-derivation of all 4 Currier signatures of
     arXiv:2604.19762 (E->S, Bilat_full, 10-chunk MI, and Zipfian Shape) on freshly generated
     Currier A (sigma_f=1) and Currier B (sigma_f=0) streams from object/vbclc.py.
Any failure exits with code 1 and prints FAIL as the final line.
"""

import collections
import hashlib
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
OBJ = os.path.join(PKG, "object")

ok = 0
bad = []


def check(cond, what, got=None):
    global ok
    if cond:
        ok += 1
    else:
        bad.append(f"{what}" + (f" (got {got})" if got is not None else ""))


# ---------------------------------------------------------------- 0. MANIFEST.sha256 check
man = {}
with open(os.path.join(HERE, "MANIFEST.sha256"), "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            h, name = line.split(None, 1)
            man[name.strip()] = h

present = sorted(
    fn for fn in os.listdir(OBJ) if os.path.isfile(os.path.join(OBJ, fn))
)
check(
    present == sorted(man),
    "object/ holds exactly the files listed in MANIFEST.sha256",
    f"{present} vs {sorted(man)}",
)
for name, want in sorted(man.items()):
    fp = os.path.join(OBJ, name)
    got = (
        hashlib.sha256(open(fp, "rb").read()).hexdigest()
        if os.path.exists(fp)
        else "missing"
    )
    check(got == want, f"object/{name} sha256 matches MANIFEST.sha256", got)

# ---------------------------------------------------------------- 1. Import object/vbclc.py & check limits
try:
    spec = importlib.util.spec_from_file_location(
        "vbclc", os.path.join(OBJ, "vbclc.py")
    )
    vbclc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vbclc)
except Exception as e:
    check(False, "import object/vbclc.py", str(e))
    print("\n".join(bad))
    print("FAIL")
    sys.exit(1)

n_t0 = len(set(vbclc.LETTER_MAP_16.values()))
n_t1 = sum(len(r) for r in vbclc.ONSET_TABLE_20)
n_t2 = len(vbclc.CORE_TABLE_96)
n_t3 = sum(len(r) for r in vbclc.CODA_TABLE_20)
total_entries = n_t0 + n_t1 + n_t2 + n_t3

check(n_t0 == 16, "Table 0 has 16 letter-group index entries", n_t0)
check(n_t1 == 20, "Table I has 20 onset entries", n_t1)
check(n_t2 == 96, "Table II has 96 core entries", n_t2)
check(n_t3 == 20, "Table III has 20 coda entries", n_t3)
check(
    total_entries == 152 and total_entries <= 200 and vbclc.TOTAL_TABLE_ENTRIES == 152,
    "Total table entries == 152 <= 200",
    total_entries,
)

hp_text = open(os.path.join(OBJ, "HAND_PROCEDURE.md"), "r", encoding="utf-8").read()
check(
    "Table 0" in hp_text and "Table I" in hp_text and "Table II" in hp_text and "Table III" in hp_text,
    "object/HAND_PROCEDURE.md documents all 4 tables",
)

# Check 1-bit state enforcement
state_err_caught = False
try:
    vbclc.encrypt_vbclc_lines("test", [["a", "b"]], sigma_f=2, seed=0)
except AssertionError:
    state_err_caught = True
check(state_err_caught, "sigma_f enforces 1-bit state in {0, 1}")

# Determinism check
sample_pt = (
    "In principio erat verbum et verbum erat apud deum et deus erat verbum "
    "hoc erat in principio apud deum omnia per ipsum facta sunt et sine ipso "
    "factum est nihil quod factum est in ipso vita erat et vita erat lux hominum "
) * 80
tmpl_small = [["w"] * 8 for _ in range(100)]
d1 = vbclc.encrypt_vbclc_lines(sample_pt, tmpl_small, sigma_f=1, seed=42)
d2 = vbclc.encrypt_vbclc_lines(sample_pt, tmpl_small, sigma_f=1, seed=42)
d3 = vbclc.encrypt_vbclc_lines(sample_pt, tmpl_small, sigma_f=1, seed=43)
check(d1 == d2 and d1 != d3, "encrypt_vbclc_lines is deterministic and seed-sensitive")

# ---------------------------------------------------------------- 2. Check saved 200-stream evaluation
eval_data = json.loads(
    open(os.path.join(OBJ, "vbclc_200streams_evaluation.json"), "r", encoding="utf-8").read()
)
check(
    eval_data.get("total_table_entries") == 152 and eval_data.get("per_folio_state_bits") == 1,
    "vbclc_200streams_evaluation.json metadata matches 152 entries and 1 state bit",
)
for cell in ("A/ZL3b", "B/ZL3b", "A/IT2a", "B/IT2a", "A/RF1b-e", "B/RF1b-e"):
    c_clean = eval_data["cells_p2_200streams"][cell]["vs_clean_ivtff_ref"]
    c_raw = eval_data["cells_p2_200streams"][cell]["vs_raw_parisel_ref"]
    by_lang = eval_data["by_language_p2"][cell]
    check(c_clean["n_streams"] == 200, f"{cell}: 200 streams evaluated", c_clean["n_streams"])
    check(
        c_clean["joint_all_criteria_pass_count"] == 200 and c_raw["adaptive_pass_count"] == 200,
        f"{cell}: 200/200 pass under all criteria",
        c_clean["joint_all_criteria_pass_count"],
    )
    check(
        by_lang["Latin_100streams"]["joint_all_criteria_pass_count"] == 100
        and by_lang["Italian_100streams"]["joint_all_criteria_pass_count"] == 100,
        f"{cell}: 100/100 Latin and 100/100 Italian streams pass",
    )
    check(
        60.0 <= c_clean["es_pct"]["min"] and c_clean["es_pct"]["max"] <= 85.0,
        f"{cell}: E->S min/max inside [60%, 85%]",
        (c_clean["es_pct"]["min"], c_clean["es_pct"]["max"]),
    )
    check(
        0.20 <= c_clean["mi_orig"]["min"] and c_clean["mi_orig"]["max"] <= 0.65,
        f"{cell}: 10-chunk MI min/max inside [0.20, 0.65]",
        (c_clean["mi_orig"]["min"], c_clean["mi_orig"]["max"]),
    )
    check(
        c_clean["zipf_r2"]["min"] > 0.85 and c_clean["cv"]["min"] > 0.80,
        f"{cell}: strict Zipfian R^2 > 0.85 and CV > 0.80 on all 200 streams",
        (c_clean["zipf_r2"]["min"], c_clean["cv"]["min"]),
    )
    check(
        c_clean["bilat_full_rate"] == 1.0 and c_clean["shapes"] == {"Zipfian": 200},
        f"{cell}: Bilat_full == 1.0 and Shape == Zipfian on 200/200 streams",
    )

# ---------------------------------------------------------------- 3. Check published baseline failures
ref_cal = json.loads(
    open(os.path.join(OBJ, "reference_calibration.json"), "r", encoding="utf-8").read()
)
pub_gen = ref_cal["published_generators_audit"]
check(
    pub_gen["slot_generator"]["template_B_ZL3b"]["pass_rate_B_ZL3b_adaptive"] == 0.0
    and pub_gen["slot_generator"]["template_B_ZL3b"]["pass_rate_B_IT2a_adaptive"] == 0.0
    and pub_gen["slot_generator"]["template_A_ZL3b"]["pass_rate_A_ZL3b_adaptive"] == 0.1,
    "Published slot generator fails joint pass (0% on Currier B, 10% on Currier A)",
)
for g_mode in ("G0_SPLIT_RANDOM", "G1_SPLIT_SHIFT", "G2_SPLIT_ROTATE", "G6_WEIGHTED_ROWS"):
    check(
        pub_gen["cardan_grille"][g_mode]["pass_rate_A_ZL3b_adaptive"] == 0.0
        and pub_gen["cardan_grille"][g_mode]["pass_rate_fixed_strict_zipf"] == 0.0,
        f"Published Cardan grille {g_mode} fails joint pass (0%)",
    )
for cell_key in ("A_ZL3b", "B_ZL3b"):
    check(
        pub_gen["naibbe_unmodified"][cell_key]["pass_rate_fixed"] == 0.0,
        f"Unmodified Naibbe fails fixed/strict-Zipf joint pass on {cell_key} (0%)",
    )

# ---------------------------------------------------------------- 4. Check saved 400-control null suite
null_data = json.loads(
    open(os.path.join(OBJ, "null_suite_400_results.json"), "r", encoding="utf-8").read()
)
for cell in ("A/ZL3b", "B/ZL3b", "A/IT2a", "B/IT2a"):
    for grp in ("manuscript_400_nulls", "vbclc152_400_nulls"):
        rec = null_data[grp][cell]
        check(
            rec["n_controls_total"] == 400
            and rec["n_word_order_controls"] == 200
            and rec["n_glyph_shuffle_controls"] == 200,
            f"{grp} {cell}: 400 controls (200 word-order + 200 glyph-shuffled)",
        )
        for mkey in ("delta_mi_10chunk", "es_x_delta_mi", "excess_edge_mi"):
            mrec = rec[mkey]
            check(
                mrec["beats_all_400"] is True and mrec["real_val"] > mrec["best_control_400"],
                f"{grp} {cell}: {mkey} real ({mrec['real_val']:.4f}) > best_400 ({mrec['best_control_400']:.4f})",
            )

# ---------------------------------------------------------------- 5. First-principles stdlib re-derivation of 4 signatures
# Exact 58-grapheme greedy EVA tokenizer from verifier.py / signatures_v27.py
GRAPHEMES = sorted(
    {
        "q", "d", "s", "t", "k", "p", "f", "c",
        "ch", "sh", "ck", "cth", "cph",
        "ok", "ot", "ol", "or",
        "k2", "t2", "p2", "f2", "d2", "s2",
        "ch2", "sh2", "ckh", "cth2", "cfh",
        "dy", "dl", "dm", "ds", "dar", "dal",
        "iin", "in", "ir", "iir", "iiir",
        "al", "am", "an", "ar", "ain", "aiin",
        "ey", "ed", "es", "edy", "eey", "eedy",
        "ly", "ry", "ny", "my", "ldy",
        "o", "a",
    },
    key=lambda x: (-len(x), x),
)

_TOK_CACHE = {}


def tokenize_word(w):
    res = _TOK_CACHE.get(w)
    if res is not None:
        return res
    tokens, i, n = [], 0, len(w)
    while i < n:
        for g in GRAPHEMES:
            lg = len(g)
            if w[i : i + lg] == g:
                tokens.append(g)
                i += lg
                break
        else:
            tokens.append(w[i])
            i += 1
    res = tuple(tokens)
    _TOK_CACHE[w] = res
    return res


def score_four_signatures_stdlib(sents):
    tok_all = [[tokenize_word(w) for w in s if len(w) > 1] for s in sents if len(s) >= 2]
    # Full-corpus bilateral extremity (>100:1)
    sc_full, ec_full = collections.Counter(), collections.Counter()
    for s in tok_all:
        for t in s:
            sc_full[t[0]] += 1
            ec_full[t[-1]] += 1
    n_se = sum(1 for g in set(sc_full) | set(ec_full) if (sc_full[g] + 1) / (ec_full[g] + 1) > 100.0)
    n_ee = sum(1 for g in set(sc_full) | set(ec_full) if (ec_full[g] + 1) / (sc_full[g] + 1) > 100.0)
    bilat_full = 1 if (n_se > 0 and n_ee > 0) else 0

    n_chunks = 10
    chunk_size = len(tok_all) // n_chunks
    es_list, mi_list, r2_list, cv_list, shapes = [], [], [], [], []
    for c_idx in range(n_chunks):
        st = c_idx * chunk_size
        en = len(tok_all) if c_idx == n_chunks - 1 else (c_idx + 1) * chunk_size
        chunk = tok_all[st:en]

        sc, ec = collections.Counter(), collections.Counter()
        for s in chunk:
            for t in s:
                sc[t[0]] += 1
                ec[t[-1]] += 1
        cls = {}
        for g in set(sc) | set(ec):
            sv, ev_c = sc[g], ec[g]
            cls[g] = "start" if sv > 2 * ev_c else ("end" if ev_c > 2 * sv else "ambig")

        es_cnt = tot_pairs = 0
        trans = collections.Counter()
        cond_c, tgt_c = collections.Counter(), collections.Counter()
        for s in chunk:
            for i in range(len(s) - 1):
                eg, sg = s[i][-1], s[i + 1][0]
                if cls.get(eg) == "end" and cls.get(sg) == "start":
                    es_cnt += 1
                tot_pairs += 1
                trans[(eg, sg)] += 1
                cond_c[eg] += 1
                tgt_c[sg] += 1

        es_list.append(100.0 * es_cnt / tot_pairs if tot_pairs else 0.0)
        h_t = -sum((v / tot_pairs) * math.log2(v / tot_pairs + 1e-15) for v in tgt_c.values())
        h_tc = -sum(
            (cnt / tot_pairs) * math.log2(cnt / cond_c[c] + 1e-15)
            for (c, _), cnt in trans.items()
        )
        mi_list.append(max(0.0, h_t - h_tc))

        freqs = sorted(sc.values(), reverse=True)
        k = len(freqs)
        mean_f = sum(freqs) / k
        var_f = sum((x - mean_f) ** 2 for x in freqs) / k
        cv = math.sqrt(var_f) / mean_f if mean_f > 0 else 0.0
        log_r = [math.log(i + 1) for i in range(k)]
        log_f = [math.log(x + 1e-10) for x in freqs]
        mr = sum(log_r) / k
        mf = sum(log_f) / k
        s_rr = sum((r - mr) ** 2 for r in log_r)
        s_rf = sum((r - mr) * (y - mf) for r, y in zip(log_r, log_f))
        slope = s_rf / s_rr if s_rr > 0 else 0.0
        intercept = mf - slope * mr
        ss_res = sum((y - (slope * r + intercept)) ** 2 for r, y in zip(log_r, log_f))
        ss_tot = sum((y - mf) ** 2 for y in log_f)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
        shp = "Zipfian" if (r2 > 0.85 and cv > 0.80) else ("Plateau" if cv < 0.50 else "Intermediate")
        r2_list.append(r2)
        cv_list.append(cv)
        shapes.append(shp)

    return {
        "es_pct": sum(es_list) / n_chunks,
        "bilat_full": bilat_full,
        "mi_10chunk": sum(mi_list) / n_chunks,
        "zipf_r2": sum(r2_list) / n_chunks,
        "cv": sum(cv_list) / n_chunks,
        "shape": collections.Counter(shapes).most_common(1)[0][0],
    }


tmpl_A = [["w"] * 7 for _ in range(1540)]
tmpl_B = [["w"] * 7 for _ in range(3260)]
for dialect_label, sigma_f, tmpl, seed in [
    ("Currier_A", 1, tmpl_A, 10000),
    ("Currier_B", 0, tmpl_B, 20000),
]:
    gen_sents = vbclc.encrypt_vbclc_lines(sample_pt, tmpl, sigma_f=sigma_f, seed=seed)
    sig = score_four_signatures_stdlib(gen_sents)
    check(
        60.0 <= sig["es_pct"] <= 85.0,
        f"Live {dialect_label} stream E->S in [60%, 85%]",
        round(sig["es_pct"], 2),
    )
    check(sig["bilat_full"] == 1, f"Live {dialect_label} stream Bilat_full == 1", sig["bilat_full"])
    check(
        0.20 <= sig["mi_10chunk"] <= 0.65,
        f"Live {dialect_label} stream 10-chunk MI in [0.20, 0.65]",
        round(sig["mi_10chunk"], 4),
    )
    check(
        sig["shape"] == "Zipfian" and sig["zipf_r2"] > 0.85 and sig["cv"] > 0.80,
        f"Live {dialect_label} stream Shape == Zipfian (R^2 > 0.85, CV > 0.80)",
        (sig["shape"], round(sig["zipf_r2"], 3), round(sig["cv"], 2)),
    )

if bad:
    for b in bad:
        print("FAIL:", b)
    print(f"{ok} checks passed, {len(bad)} failed")
    print("FAIL")
    sys.exit(1)

print(f"{ok} checks passed, 0 failed")
print("PASS")
