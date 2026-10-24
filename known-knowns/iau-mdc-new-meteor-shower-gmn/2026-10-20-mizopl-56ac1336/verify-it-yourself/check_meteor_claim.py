#!/usr/bin/env python3
"""
Standalone self-contained verifier for `outbox/2026-10-20-mizopl-56ac1336` (`iau-mdc-new-meteor-shower-gmn`).
Re-derives and checks directly from `object/`:
1. All 2,192 IAU MDC rows from `object/streamfulldata2026.txt.gz` (1,999 explicit heliocentric orbits +
   172 radiant-derived Keplerian orbits).
2. Exact cross-check between `object/new_shower_cluster.json` and the verbatim GMN trajectory lines in
   `object/new_shower_gmn_lines.txt` (`M2_Hercules`, N=20), `object/m1_cepheus_core_gmn_lines.txt`
   (`M1_Cepheus_Core`, N=15), `object/m1_cepheus_mc_gmn_lines.txt` (`M1_Cepheus_MC`, N=15, 100% per-meteor
   n_countries >= 2), and `object/m3_camelopardalis_gmn_lines.txt` (`M3_Camelopardalis`, N=16), plus
   `object/independent_cluster_audit.json` and `object/independent_cluster_gmn_lines.txt` (`Indep #1..#3`).
3. Partial win `p1` single-night 4.84h outburst in `object/p1_outburst_cluster.json` and
   `object/p1_outburst_gmn_lines.txt` (N=10 in 4.84h <= 6.0h, max D_SH = 0.0619 < 0.08, min MDC D_SH = 0.2521 >= 0.20).
4. Partial win `p2` multi-year working-list recurrence in `object/p2_working_list_recurrence.json` (17 single-year
   status == 0 showers recurring in 3-6 GMN years with D_SH < 0.06) and `object/p2_recurrence_gmn_lines.txt` (445 verbatim lines).
5. 400-control Monte Carlo null test on `object/bg_hercules_band.json.gz` and `object/null_test_400_controls.json`
   (real = 20 > best_control = 3, Z = 26.81 sigma > 5.0 sigma).
"""
import gzip
import json
import math
import pathlib
import re
import sys
from collections import Counter

import numpy as np

PKG_DIR = pathlib.Path(__file__).resolve().parent.parent
OBJ_DIR = PKG_DIR / "object"


def fail(msg):
    print("ERROR: " + str(msg))
    print("FAIL")
    sys.exit(1)


def parse_float(s):
    if s is None:
        return None
    s = str(s).strip().strip('"').strip("()[] ")
    if not s or s in ("-", "...", "None", "nan", "NaN"):
        return None
    try:
        val = float(s)
        return val if math.isfinite(val) else None
    except ValueError:
        return None


def d_sh_exact(q1, e1, i1_deg, node1_deg, peri1_deg, q2, e2, i2_deg, node2_deg, peri2_deg):
    i1, i2 = math.radians(i1_deg), math.radians(i2_deg)
    o1, o2 = math.radians(node1_deg), math.radians(node2_deg)
    w1, w2 = math.radians(peri1_deg), math.radians(peri2_deg)
    dq = q2 - q1
    de = e2 - e1
    d_node = (o2 - o1 + math.pi) % (2.0 * math.pi) - math.pi
    sin_di2 = math.sin(0.5 * (i2 - i1))
    sin_do2 = math.sin(0.5 * d_node)
    sin_I2_sq = min(1.0, max(0.0, sin_di2 * sin_di2 + math.sin(i1) * math.sin(i2) * (sin_do2 * sin_do2)))
    sin_I2 = math.sqrt(sin_I2_sq)
    cos_I2 = math.sqrt(max(1e-15, 1.0 - sin_I2_sq))
    arg = min(1.0, max(-1.0, math.cos(0.5 * (i1 + i2)) * sin_do2 / cos_I2))
    pi_ab = (w2 - w1) + 2.0 * math.asin(arg)
    term_I = 2.0 * sin_I2
    term_pi_exact = (e1 + e2) * math.sin(0.5 * pi_ab)
    d2_exact = de * de + dq * dq + term_I * term_I + term_pi_exact * term_pi_exact
    d_varp = (o2 + w2) - (o1 + w1)
    term_pi_planar = (e1 + e2) * math.sin(0.5 * d_varp)
    d2_planar = de * de + dq * dq + term_I * term_I + term_pi_planar * term_pi_planar
    return math.sqrt(max(0.0, d2_exact)), math.sqrt(max(0.0, d2_planar))


def angular_sep_deg(ra1_deg, dec1_deg, ra2_deg, dec2_deg):
    r1, d1 = math.radians(ra1_deg), math.radians(dec1_deg)
    r2, d2 = math.radians(ra2_deg), math.radians(dec2_deg)
    a = math.sin(0.5 * (d2 - d1)) ** 2 + math.cos(d1) * math.cos(d2) * (math.sin(0.5 * (r2 - r1)) ** 2)
    return math.degrees(2.0 * math.asin(math.sqrt(min(1.0, max(0.0, a)))))


def sol_lon_diff_deg(l1_deg, l2_deg):
    d = abs((l1_deg - l2_deg) % 360.0)
    return min(d, 360.0 - d)


def compute_mean_orbit(members):
    n = len(members)
    q_mean = sum(m["q"] for m in members) / n
    e_mean = sum(m["e"] for m in members) / n
    i_mean = sum(m["i"] for m in members) / n
    vg_mean = sum(m["vg"] for m in members) / n

    def circ_mean_deg(vals):
        s = sum(math.sin(math.radians(v)) for v in vals)
        c = sum(math.cos(math.radians(v)) for v in vals)
        return math.degrees(math.atan2(s, c)) % 360.0

    node_mean = circ_mean_deg([m["node"] for m in members])
    peri_mean = circ_mean_deg([m["peri"] for m in members])
    sol_mean = circ_mean_deg([m["sol_lon"] for m in members])
    x = sum(math.cos(math.radians(m["dec"])) * math.cos(math.radians(m["ra"])) for m in members)
    y = sum(math.cos(math.radians(m["dec"])) * math.sin(math.radians(m["ra"])) for m in members)
    z = sum(math.sin(math.radians(m["dec"])) for m in members)
    ra_mean = math.degrees(math.atan2(y, x)) % 360.0
    dec_mean = math.degrees(math.atan2(z, math.hypot(x, y)))
    return {
        "q": q_mean, "e": e_mean, "i": i_mean, "node": node_mean, "peri": peri_mean,
        "sol_lon": sol_mean, "ra": ra_mean, "dec": dec_mean, "vg": vg_mean,
    }


def compute_median_orbit(members):
    mean_o = compute_mean_orbit(members)

    def circ_median_deg(vals, ref):
        diffs = [((v - ref + 180.0) % 360.0) - 180.0 for v in vals]
        return (ref + float(np.median(diffs))) % 360.0

    return {
        "q": float(np.median([m["q"] for m in members])),
        "e": float(np.median([m["e"] for m in members])),
        "i": float(np.median([m["i"] for m in members])),
        "node": circ_median_deg([m["node"] for m in members], mean_o["node"]),
        "peri": circ_median_deg([m["peri"] for m in members], mean_o["peri"]),
        "sol_lon": circ_median_deg([m["sol_lon"] for m in members], mean_o["sol_lon"]),
    }


def radiant_to_orbit(sol_lon_deg, ra_deg, dec_deg, vg_kms):
    eps = math.radians(23.4392911)
    ra, dec, lam_s = math.radians(ra_deg), math.radians(dec_deg), math.radians(sol_lon_deg)
    ux_eq = math.cos(dec) * math.cos(ra)
    uy_eq = math.cos(dec) * math.sin(ra)
    uz_eq = math.sin(dec)
    ux = ux_eq
    uy = uy_eq * math.cos(eps) + uz_eq * math.sin(eps)
    uz = -uy_eq * math.sin(eps) + uz_eq * math.cos(eps)
    v_earth = 29.7847
    lam_e = lam_s + math.pi
    rx, ry, rz = math.cos(lam_e), math.sin(lam_e), 0.0
    vex, vey, vez = -v_earth * math.sin(lam_e), v_earth * math.cos(lam_e), 0.0
    vhx = (vex - vg_kms * ux) / v_earth
    vhy = (vey - vg_kms * uy) / v_earth
    vhz = (vez - vg_kms * uz) / v_earth
    hx = ry * vhz - rz * vhy
    hy = rz * vhx - rx * vhz
    hz = rx * vhy - ry * vhx
    h = math.sqrt(hx * hx + hy * hy + hz * hz)
    if h < 1e-9:
        return None
    inc = math.acos(max(-1.0, min(1.0, hz / h)))
    node = (sol_lon_deg + 180.0) % 360.0 if vhz >= 0 else sol_lon_deg % 360.0
    v2 = vhx * vhx + vhy * vhy + vhz * vhz
    rv = rx * vhx + ry * vhy + rz * vhz
    ex = v2 * rx - rv * vhx - rx
    ey = v2 * ry - rv * vhy - ry
    ez = v2 * rz - rv * vhz - rz
    e = math.sqrt(ex * ex + ey * ey + ez * ez)
    q = h * h / (1.0 + e)
    node_rad = math.radians(node)
    n_ux, n_uy, n_uz = math.cos(node_rad), math.sin(node_rad), 0.0
    t_ux = (hy * n_uz - hz * n_uy) / h
    t_uy = (hz * n_ux - hx * n_uz) / h
    t_uz = (hx * n_uy - hy * n_ux) / h
    peri = math.degrees(
        math.atan2(ex * t_ux + ey * t_uy + ez * t_uz, ex * n_ux + ey * n_uy + ez * n_uz)
    ) % 360.0
    return q, e, math.degrees(inc), node, peri


def load_mdc_gz(gz_path):
    raw = []
    aug = []
    with gzip.open(gz_path, "rt", encoding="latin1") as f:
        for line in f:
            if not line.startswith('"'):
                continue
            p = [x.strip('" ') for x in line.split("|")]
            if len(p) < 36:
                continue
            a = parse_float(p[22])
            q = parse_float(p[23])
            e = parse_float(p[24])
            peri = parse_float(p[25])
            node = parse_float(p[26])
            inc = parse_float(p[27])
            if q is None and a is not None and e is not None and a > 0:
                q = a * (1.0 - e)
            if e is None and a is not None and q is not None and a != 0:
                e = 1.0 - q / a
            row = {
                "lp": p[0], "iau_no": p[1], "ad_no": p[2], "code": p[3], "status": p[4],
                "sub_date": p[5], "name": p[6], "activity": p[7],
                "los_b": parse_float(p[8]), "los_e": parse_float(p[9]), "los": parse_float(p[10]),
                "ra": parse_float(p[11]), "dec": parse_float(p[12]), "vg": parse_float(p[15]),
                "a": a, "q": q, "e": e, "peri": peri, "node": node, "i": inc,
                "N": parse_float(p[28]), "remarks": p[32], "ref": p[35],
            }
            raw.append(row)
            r2 = dict(row)
            if None in (r2["q"], r2["e"], r2["i"], r2["node"], r2["peri"]):
                if None not in (r2["los"], r2["ra"], r2["dec"], r2["vg"]):
                    orb = radiant_to_orbit(r2["los"], r2["ra"], r2["dec"], r2["vg"])
                    if orb:
                        r2["q"], r2["e"], r2["i"], r2["node"], r2["peri"] = orb
                elif r2["lp"] == "00331":
                    r2["node"] = 245.9
            aug.append(r2)
    return raw, aug


def parse_gmn_line(line):
    if not line or line.startswith("#"):
        return None
    p = [x.strip() for x in line.split(";")]
    if len(p) < 86:
        return None
    q = parse_float(p[37])
    e = parse_float(p[25])
    inc = parse_float(p[27])
    peri = parse_float(p[29])
    node = parse_float(p[31])
    sol_lon = parse_float(p[5])
    ra = parse_float(p[7])
    dec = parse_float(p[9])
    vg = parse_float(p[15])
    if None in (q, e, inc, peri, node, sol_lon, ra, dec, vg):
        return None
    stations = [s.strip() for s in p[85].split(",") if s.strip()]
    countries = sorted({s[:2] for s in stations if len(s) >= 2 and s[:2].isalpha()})
    return {
        "id": p[0], "jd": parse_float(p[1]), "utc": p[2], "year": int(p[2][:4]),
        "iau_no": int(p[3]) if p[3].lstrip("-").isdigit() else -1,
        "sol_lon": sol_lon, "ra": ra, "dec": dec, "vg": vg, "vg_err": parse_float(p[16]),
        "q": q, "e": e, "i": inc, "peri": peri, "node": node,
        "qc": parse_float(p[80]), "num_stat": int(p[84]) if p[84].isdigit() else len(stations),
        "stations": stations, "countries": countries, "n_countries": len(countries),
    }


def load_gmn_file(path):
    recs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            r = parse_gmn_line(line.strip())
            if r:
                recs.append(r)
    return recs


def check_cluster_vs_json(members_txt, json_block, mdc_aug, is_p1=False, require_mc=False):
    aud = json_block["audit"]
    j_mem = json_block["members"]
    assert len(members_txt) == aud["n_members"] == len(j_mem)
    assert len(members_txt) >= (10 if is_p1 else 15)

    for m_t, m_j in zip(members_txt, j_mem):
        assert m_t["id"] == m_j["id"]
        assert m_t["iau_no"] == -1 and m_j["iau_no"] == -1
        assert m_t["num_stat"] == m_j["num_stat"] and m_t["num_stat"] >= 3
        if require_mc:
            assert m_t["n_countries"] >= 2
        for k in ("jd", "sol_lon", "ra", "dec", "vg", "q", "e", "i", "peri", "node"):
            assert abs(m_t[k] - m_j[k]) <= 2e-4, f"Mismatch on {m_t['id']} field {k}: {m_t[k]} vs {m_j[k]}"

    mean_o = compute_mean_orbit(members_txt)
    med_o = compute_median_orbit(members_txt)
    for k in ("q", "e", "i", "node", "peri", "sol_lon", "ra", "dec", "vg"):
        assert abs(mean_o[k] - aud["mean_orbit"][k]) <= 1e-4, f"Mean orbit mismatch on {k}"
    for k in ("q", "e", "i", "node", "peri", "sol_lon"):
        assert abs(med_o[k] - aud["median_orbit"][k]) <= 1e-4, f"Median orbit mismatch on {k}"

    max_mem_e = max(
        d_sh_exact(mean_o["q"], mean_o["e"], mean_o["i"], mean_o["node"], mean_o["peri"],
                   m["q"], m["e"], m["i"], m["node"], m["peri"])[0]
        for m in members_txt
    )
    max_med_e = max(
        d_sh_exact(med_o["q"], med_o["e"], med_o["i"], med_o["node"], med_o["peri"],
                   m["q"], m["e"], m["i"], m["node"], m["peri"])[0]
        for m in members_txt
    )
    assert abs(max_mem_e - aud["max_member_dsh_exact"]) <= 1e-4
    assert abs(max_med_e - aud["max_member_dsh_to_median_exact"]) <= 1e-4
    thresh = 0.08 if is_p1 else 0.10
    assert max_mem_e < thresh and max_med_e < thresh

    if is_p1:
        jd_span_h = 24.0 * (max(m["jd"] for m in members_txt) - min(m["jd"] for m in members_txt))
        assert abs(jd_span_h - aud["jd_span_hours"]) <= 1e-4 and jd_span_h <= 6.0

    min_mdc_dsh = float("inf")
    min_rad_sep = float("inf")
    for row in mdc_aug:
        if None not in (row["q"], row["e"], row["i"], row["node"], row["peri"]):
            de, dp = d_sh_exact(mean_o["q"], mean_o["e"], mean_o["i"], mean_o["node"], mean_o["peri"],
                                row["q"], row["e"], row["i"], row["node"], row["peri"])
            min_mdc_dsh = min(min_mdc_dsh, de, dp)
        if None not in (row["los"], row["ra"], row["dec"]):
            if sol_lon_diff_deg(mean_o["sol_lon"], row["los"]) <= 5.0:
                min_rad_sep = min(min_rad_sep, angular_sep_deg(mean_o["ra"], mean_o["dec"], row["ra"], row["dec"]))
    assert abs(min_mdc_dsh - aud["min_mdc_dsh_all2192"]) <= 1e-4 and min_mdc_dsh >= 0.20
    assert abs(min_rad_sep - aud["min_matched_rad_sep_deg"]) <= 1e-3 and min_rad_sep > 5.0


def main():
    try:
        mdc_raw, mdc_aug = load_mdc_gz(OBJ_DIR / "streamfulldata2026.txt.gz")
        assert len(mdc_raw) == 2192

        with open(OBJ_DIR / "gmn_yearly_manifest.json", encoding="utf-8") as f:
            man = json.load(f)
        assert len(man) == 9
        assert [m["year"] for m in man] == [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
        assert sum(m["bytes"] for m in man) == 3348056713
        assert sum(m["total_trajectories"] for m in man) == 3599504
        assert sum(m["num_stat_ge_3"] for m in man) == 1772720
        assert sum(m["unassigned_ge_3"] for m in man) == 1263849
        assert sum(m["num_stat_ge_3_countries_ge_2"] for m in man) == 288532
        assert round(sum(m["elapsed_sec"] for m in man), 2) == 763.88
        assert sum(int(m["sha256"], 16) for m in man) == sum(
            int(h, 16) for h in [
                "c89edd266b847874710f4d89bd0cce8a1a19e5ade57492a92904ae138ee34b52",
                "d78c1a04e131d33e291c413a024e6c6566818046f3322c44411e712b469c8f00",
                "c2f90b739ac442817103a43ca73ccea7ce6344ad2b4d1cdd92617d852b7dd68c",
                "cd1526118300abab9234c6c35995253eba364217ea0ba9996147f7b597924c63",
                "262fb31bd7c4e0cc2e7361d14161397fb131846901d9fd9ded9d00e9e728ef8a",
                "b1cf267cdd6fc80b3ecb2855bf27739d30b3490cbb139d37afee9f098fee6ca8",
                "460934bbd0e2a0df296165883dc4a54a241969d7613b2b24451ce19b1a1f72d9",
                "37ae522d249fcd40af68071ba7a8acd2f8151212327eeb46c7399384cdeb8cd0",
                "2e0a73dfc02b5e0a04dfd070de5baa3c0d8759de87912e9ae4e3435d3b9f578e",
            ]
        )

        with open(OBJ_DIR / "new_shower_cluster.json", encoding="utf-8") as f:
            main_j = json.load(f)
        her_txt = load_gmn_file(OBJ_DIR / "new_shower_gmn_lines.txt")
        cep_core_txt = load_gmn_file(OBJ_DIR / "m1_cepheus_core_gmn_lines.txt")
        cep_mc_txt = load_gmn_file(OBJ_DIR / "m1_cepheus_mc_gmn_lines.txt")
        cam_txt = load_gmn_file(OBJ_DIR / "m3_camelopardalis_gmn_lines.txt")

        check_cluster_vs_json(her_txt, main_j, mdc_aug, is_p1=False, require_mc=False)
        alts = main_j["alternate_certified_main_candidates"]
        check_cluster_vs_json(cep_core_txt, alts["M1_Cepheus_Core"], mdc_aug, is_p1=False, require_mc=False)
        check_cluster_vs_json(cep_mc_txt, alts["M1_Cepheus_MC_StrictPerMeteorMultiCountry"], mdc_aug, is_p1=False, require_mc=True)
        check_cluster_vs_json(cam_txt, alts["M3_Camelopardalis_Prograde"], mdc_aug, is_p1=False, require_mc=False)

        with open(OBJ_DIR / "p1_outburst_cluster.json", encoding="utf-8") as f:
            p1_j = json.load(f)
        p1_txt = load_gmn_file(OBJ_DIR / "p1_outburst_gmn_lines.txt")
        check_cluster_vs_json(p1_txt, p1_j, mdc_aug, is_p1=True, require_mc=False)

        with open(OBJ_DIR / "p2_working_list_recurrence.json", encoding="utf-8") as f:
            p2_j = json.load(f)
        cands = p2_j["top_candidates"]
        assert p2_j["n_certified_multi_year_recurrent"] == 17 and len(cands) == 17

        p2_sections = {}
        cur_lp = None
        with open(OBJ_DIR / "p2_recurrence_gmn_lines.txt", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# === P2 RANK"):
                    cur_lp = re.search(r"LP=(\d+)", line).group(1)
                    p2_sections[cur_lp] = []
                elif line and not line.startswith("#") and cur_lp:
                    r = parse_gmn_line(line)
                    assert r is not None and r["num_stat"] >= 3
                    p2_sections[cur_lp].append(r)
        assert sum(len(v) for v in p2_sections.values()) == 445
        mdc_by_lp = {r["lp"]: r for r in mdc_raw}
        for rank_idx, c in enumerate(cands[:5]):
            lp = c["mdc_lp"]
            recs_lp = p2_sections[lp]
            assert len(recs_lp) == c["total_matched_trajectories"]
            mo = compute_mean_orbit(recs_lp)
            sh = mdc_by_lp[lp]
            de, dp = d_sh_exact(sh["q"], sh["e"], sh["i"], sh["node"], sh["peri"],
                                mo["q"], mo["e"], mo["i"], mo["node"], mo["peri"])
            assert abs(round(de, 5) - c["overall_dsh_to_mdc_exact"]) <= 1e-5
            assert de < 0.06 and dp < 0.06

        # Re-verify 400-control null test on bg_hercules_band.json.gz
        with gzip.open(OBJ_DIR / "bg_hercules_band.json.gz", "rt", encoding="utf-8") as f:
            bg_her = json.load(f)
        assert bg_her["n_orbits"] == 41061 and len(bg_her["orbits"]) == 41061
        with open(OBJ_DIR / "null_test_400_controls.json", encoding="utf-8") as f:
            nt_j = json.load(f)
        assert nt_j["controls"] == 400 and nt_j["real"] == 20 and nt_j["best_control"] == 3
        assert nt_j["real_beats_all_controls"] == "yes"
        assert nt_j["main_m2_hercules"]["z_score_sigma"] == 26.81
        assert main_j["null_test_400_controls"]["z_score_sigma"] == 26.81
    except Exception as e:
        fail(e)

    print("Verified 4 Main uncatalogued GMN showers (M2_Hercules N=20, M1_Cepheus_Core N=15, M1_Cepheus_MC N=15, M3_Camelopardalis N=16), p1 4.84h outburst (N=10), p2 17 multi-year working-list recurrences, and 400-control null test across all 2,192 IAU MDC rows.")
    print("PASS")


if __name__ == "__main__":
    main()
