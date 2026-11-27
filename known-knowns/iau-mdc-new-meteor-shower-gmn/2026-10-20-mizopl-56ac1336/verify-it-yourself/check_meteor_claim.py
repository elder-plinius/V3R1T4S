#!/usr/bin/env python3
"""
Standalone self-contained verifier for `2026-10-20-mizopl-56ac1336` (`iau-mdc-new-meteor-shower-gmn`).
Re-derives and checks directly from `object/`:
1. Source manifest in `object/gmn_yearly_manifest.json` (SHA-256 and URL citations for the 9 GMN
   yearly trajectory summary files 2018-2026 and the live 2026-11-03 IAU MDC `streamfulldata2026.txt`
   with 2,197 rows, `roje_lista.php`, and `new_reports.php`).
2. Verbatim GMN trajectory lines in `object/m1_cepheus_mc_gmn_lines.txt` (N=16 deduplicated
   multi-country members of `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163`):
   - splits station lists on commas, verifies valid station codes (`^[A-Z]{2}[0-9A-Z]{4}$`),
   - verifies `len(stations) == num_stat >= 3` and `len(countries) == n_countries >= 2` for every
     single member (16/16 = 100%, 15 countries, 62 distinct stations across 4 years 2023-2026),
   - verifies each meteor is counted once (`min_pairwise_time_sep_sec = 1332.405 s > 60 s`).
3. Recomputes the exact Southworth-Hawkins `D_SH` (spherical and planar) directly from the 5
   Keplerian orbital elements `(q, e, i, node, peri)` for the 16x16 pairwise matrix, mean orbit,
   median orbit, and medoid (`20260907031956_faRoT`), and verifies single-linkage connectedness
   at `D_SH <= 0.10`.
4. Recomputes `D_SH` and radiant separation against the 156 reference/neighbor IAU MDC rows in
   `object/new_shower_cluster.json` (including all 5 rows LP 02646..02650 added in the 3 November
   2026 `2,197`-row update), verifying `min D_SH = 0.2819 >= 0.20` (`min member D_SH = 0.2511 >= 0.20`)
   and `min radiant separation = 19.52 deg > 5.0 deg`.
5. Verifies the 400-control shuffled-solar-longitude and orbital-permutation Monte Carlo null test,
   cross-year window counts (2018-2022 = 0), live shuffled-solar-longitude bootstrap on the 166
   external multi-country orbits, and look-elsewhere corrections across 103 ecliptic 3.5-deg windows
   (`7.03 sigma`), 360 1-deg bins (`6.85 sigma`), 43,228 MDC-isolated multi-country seeds
   (`6.11 sigma`), and 173,358 unassigned multi-country trajectories (`5.88 sigma` > `5.0 sigma`).
"""
import hashlib
import json
import math
import pathlib
import re
import sys
from collections import deque

import numpy as np

PKG_DIR = pathlib.Path(__file__).resolve().parent.parent
OBJ_DIR = PKG_DIR / "object"
STATION_RE = re.compile(r"^[A-Z]{2}[0-9A-Z]{4}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


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
    if not p[84].isdigit():
        return None
    num_stat = int(p[84])
    stations = [s.strip() for s in p[85].split(",") if s.strip()]
    for s in stations:
        if not STATION_RE.match(s):
            fail(f"Invalid station code {s!r} in trajectory {p[0]}")
    if len(stations) != num_stat or len(set(stations)) != num_stat:
        fail(f"Station count mismatch in {p[0]}: num_stat={num_stat} vs stations={stations}")
    countries = sorted({s[:2] for s in stations})
    return {
        "id": p[0],
        "jd": parse_float(p[1]),
        "utc": p[2],
        "year": int(p[2][:4]),
        "iau_no": int(p[3]) if p[3].lstrip("-").isdigit() else -1,
        "iau_code": p[4],
        "sol_lon": sol_lon,
        "ra": ra,
        "dec": dec,
        "vg": vg,
        "vg_err": parse_float(p[16]),
        "a": parse_float(p[23]),
        "q": q,
        "e": e,
        "i": inc,
        "peri": peri,
        "node": node,
        "qc": parse_float(p[80]),
        "median_fit_err": parse_float(p[81]),
        "beg_lat": parse_float(p[51]),
        "beg_lon": parse_float(p[53]),
        "beg_ht_km": parse_float(p[55]),
        "end_lat": parse_float(p[57]),
        "end_lon": parse_float(p[59]),
        "end_ht_km": parse_float(p[61]),
        "num_stat": num_stat,
        "stations": stations,
        "countries": countries,
        "n_countries": len(countries),
    }


def load_gmn_file(path):
    recs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = parse_gmn_line(line)
            if r is None:
                fail(f"Failed to parse GMN line in {path}")
            recs.append(r)
    return recs


def main():
    try:
        req_files = [
            OBJ_DIR / "gmn_yearly_manifest.json",
            OBJ_DIR / "m1_cepheus_mc_gmn_lines.txt",
            OBJ_DIR / "new_shower_cluster.json",
            OBJ_DIR / "null_test_400_controls.json",
        ]
        for p in req_files:
            if not p.exists():
                fail(f"Missing required artifact: {p}")

        manifest = json.loads((OBJ_DIR / "gmn_yearly_manifest.json").read_text(encoding="utf-8"))
        cluster = json.loads((OBJ_DIR / "new_shower_cluster.json").read_text(encoding="utf-8"))
        null_doc = json.loads((OBJ_DIR / "null_test_400_controls.json").read_text(encoding="utf-8"))
        mc_bytes = (OBJ_DIR / "m1_cepheus_mc_gmn_lines.txt").read_bytes()
        mc_sha256 = hashlib.sha256(mc_bytes).hexdigest()

        # 1. Verify manifest citations (GMN yearly files + IAU MDC sources)
        assert manifest["target_id"] == "iau-mdc-new-meteor-shower-gmn"
        assert manifest["candidate_id"] == "GMN_NEW_SHOWER_M1_CEPHEUS_MC_163"
        assert manifest["member_lines_file"] == "object/m1_cepheus_mc_gmn_lines.txt"
        assert manifest["member_lines_sha256"] == mc_sha256
        assert cluster["raw_lines_sha256"] == mc_sha256

        mdc_src = manifest["iau_mdc_sources"]
        nov03_src = mdc_src["streamfulldata2026_nov03_live"]
        assert nov03_src["url"] == "https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt"
        assert nov03_src["total_rows"] == 2197
        assert nov03_src["explicit_orbit_rows"] == 2004
        assert nov03_src["radiant_derived_orbit_rows"] == 172
        assert nov03_src["bytes"] == 1558558
        assert nov03_src["sha256"] == "ae1a84a546be1c72ee0cf74835bc5b928a0d1d4c4e01a18a7f17bdaee299e100"
        assert nov03_src["nov03_added_lps"] == ["02646", "02647", "02648", "02649", "02650"]

        oct20_src = mdc_src["streamfulldata2026_oct20_initial"]
        assert oct20_src["url"] == "https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt"
        assert oct20_src["header_last_update_utc"] == "Oct 20, 2026"
        assert oct20_src["retrieved_utc"] == "2026-10-20T18:54:36Z"
        assert oct20_src["total_rows"] == 2192 and oct20_src["bytes"] == 1555028
        assert oct20_src["sha256"] == "08409111125e83ef2f033b27e215fb4383e0f15f6e6a3d202f7dda3a27f027fe"
        assert nov03_src["header_last_update_utc"] == "Nov 03, 20:00:00 UTC, 2026"
        assert nov03_src["retrieved_utc"] == "2026-11-07T15:14:00Z"
        assert mdc_src["roje_lista_working_list_html"] == {
            "url": "https://www.ta3.sk/IAUC22DB/MDC2022/Roje/roje_lista.php",
            "retrieved_utc": "2026-11-07T15:13:59Z",
            "bytes": 370300,
            "sha256": "3d25556bdd5cc627acab13c4baca7d9df85a30afed0ee5e29e93e80e4724c2ef",
        }
        assert mdc_src["new_reports_2023_2026_html"] == {
            "url": "https://www.ta3.sk/IAUC22DB/MDC2022/Dokumenty/new_reports.php",
            "retrieved_utc": "2026-11-07T15:14:00Z",
            "bytes": 9216,
            "sha256": "f59617319b97414766b119e0abe5922dcb6a11521855d4ee643de9a031336d93",
        }

        expected_gmn = [
            (2018, 460180, "c89edd266b847874710f4d89bd0cce8a1a19e5ade57492a92904ae138ee34b52", 497, 13, 12, 0, 0.01),
            (2019, 46498742, "d78c1a04e131d33e291c413a024e6c6566818046f3322c44411e712b469c8f00", 50263, 21163, 14649, 2056, 0.73),
            (2020, 115779832, "c2f90b739ac442817103a43ca73ccea7ce6344ad2b4d1cdd92617d852b7dd68c", 125098, 50622, 35483, 5885, 38.57),
            (2021, 196153342, "cd1526118300abab9234c6c35995253eba364217ea0ba9996147f7b597924c63", 211851, 91104, 61768, 10132, 48.05),
            (2022, 311120248, "262fb31bd7c4e0cc2e7361d14161397fb131846901d9fd9ded9d00e9e728ef8a", 334661, 159143, 106519, 19648, 50.61),
            (2023, 420839167, "b1cf267cdd6fc80b3ecb2855bf27739d30b3490cbb139d37afee9f098fee6ca8", 451903, 233386, 161237, 30547, 153.7),
            (2024, 657058618, "460934bbd0e2a0df296165883dc4a54a241969d7613b2b24451ce19b1a1f72d9", 705964, 360095, 261207, 46407, 139.69),
            (2025, 898581735, "37ae522d249fcd40af68071ba7a8acd2f8151212327eeb46c7399384cdeb8cd0", 966063, 466273, 333324, 74289, 226.86),
            (2026, 701564849, "2e0a73dfc02b5e0a04dfd070de5baa3c0d8759de87912e9ae4e3435d3b9f578e", 753204, 390921, 289650, 99568, 105.66),
        ]
        gmn_files = manifest["gmn_yearly_files"]
        assert len(gmn_files) == len(expected_gmn)
        for row, exp in zip(gmn_files, expected_gmn):
            yr, b_sz, sha, tot, ns3, un3, mc2, el = exp
            assert row["year"] == yr
            assert row["bytes"] == b_sz
            assert row["sha256"] == sha
            assert row["total_trajectories"] == tot
            assert row["num_stat_ge_3"] == ns3
            assert row["unassigned_ge_3"] == un3
            assert row["num_stat_ge_3_countries_ge_2"] == mc2
            assert abs(row["elapsed_sec"] - el) <= 1e-6
            assert row["filename"] == f"traj_summary_yearly_{yr}.txt"
            assert row["url"] == f"https://globalmeteornetwork.org/data/traj_summary_data/yearly/traj_summary_yearly_{yr}.txt"
        assert sum(r["total_trajectories"] for r in gmn_files) == 3599504
        assert sum(r["num_stat_ge_3"] for r in gmn_files) == 1772720
        assert sum(r["unassigned_ge_3"] for r in gmn_files) == 1263849
        assert sum(r["num_stat_ge_3_countries_ge_2"] for r in gmn_files) == 288532

        # 2. Verify verbatim GMN lines, per-meteor multi-station/multi-country, and deduplication
        members_txt = load_gmn_file(OBJ_DIR / "m1_cepheus_mc_gmn_lines.txt")
        aud = cluster["audit"]
        j_mem = cluster["members"]
        assert len(members_txt) == 16 and aud["n_members"] == 16 and len(j_mem) == 16
        assert [m["id"] for m in members_txt] == cluster["member_trajectory_ids"] == manifest["member_trajectory_ids"]
        assert len({m["id"] for m in members_txt}) == 16

        for idx, (m_t, m_j) in enumerate(zip(members_txt, j_mem)):
            assert m_t["id"] == m_j["id"]
            assert m_t["year"] == m_j["year"] and m_t["utc"] == m_j["utc"]
            assert m_t["iau_no"] == -1 and m_j["iau_no"] == -1
            assert m_t["num_stat"] == m_j["num_stat"] == len(m_j["stations"]) >= 3
            assert m_t["n_countries"] == m_j["n_countries"] == len(m_j["countries"]) >= 2
            assert m_t["stations"] == m_j["stations"]
            assert m_t["countries"] == m_j["countries"]
            for s in m_j["stations"]:
                assert STATION_RE.match(s)
            for k in (
                "jd", "sol_lon", "ra", "dec", "vg", "vg_err", "a", "q", "e", "i",
                "peri", "node", "qc", "median_fit_err", "beg_lat", "beg_lon",
                "beg_ht_km", "end_lat", "end_lon", "end_ht_km",
            ):
                assert abs(m_t[k] - m_j[k]) <= 1e-6, f"Mismatch on {m_t['id']} field {k}: {m_t[k]} vs {m_j[k]}"

        # Verify each meteor is counted strictly once (sorted by JD, min delta_t = 1332.405 s > 60 s)
        for a in range(len(members_txt) - 1):
            assert members_txt[a + 1]["jd"] > members_txt[a]["jd"]
        min_dt_sec = min(
            (members_txt[a + 1]["jd"] - members_txt[a]["jd"]) * 86400.0
            for a in range(len(members_txt) - 1)
        )
        assert abs(min_dt_sec - aud["min_pairwise_time_sep_sec"]) <= 0.01
        assert min_dt_sec >= 1332.0

        years_union = sorted({m["year"] for m in members_txt})
        countries_union = sorted({c for m in members_txt for c in m["countries"]})
        stations_union = sorted({s for m in members_txt for s in m["stations"]})
        assert years_union == [2023, 2024, 2025, 2026] == aud["years"]
        assert aud["n_years"] == 4 and len(years_union) >= 3
        assert aud["counts_by_year"] == {"2023": 2, "2024": 3, "2025": 4, "2026": 7}
        assert countries_union == aud["all_countries"] and len(countries_union) == 15 == aud["n_countries_cluster"]
        assert stations_union == aud["distinct_stations"] and len(stations_union) == 62 == aud["n_distinct_stations"]
        assert aud["min_num_stat"] == 3 and aud["max_num_stat"] == 8
        assert aud["min_n_countries_per_member"] == 2 and aud["max_n_countries_per_member"] == 3
        assert aud["n_multicountry_members"] == 16 and aud["all_members_multicountry"] is True

        # 3. Recompute mean, median, medoid, and 16x16 pairwise D_SH matrix from orbital elements
        mean_o = compute_mean_orbit(members_txt)
        med_o = compute_median_orbit(members_txt)
        for k in ("q", "e", "i", "node", "peri", "sol_lon", "ra", "dec", "vg"):
            assert abs(mean_o[k] - aud["mean_orbit"][k]) <= 2e-5, f"Mean orbit mismatch on {k}"
        for k in ("q", "e", "i", "node", "peri", "sol_lon"):
            assert abs(med_o[k] - aud["median_orbit"][k]) <= 2e-5, f"Median orbit mismatch on {k}"

        n = len(members_txt)
        pw_e_mat = cluster["pairwise_dsh_exact_matrix"]
        pw_p_mat = cluster["pairwise_dsh_planar_matrix"]
        assert len(pw_e_mat) == n and len(pw_p_mat) == n

        recomp_pw_e = [[0.0] * n for _ in range(n)]
        recomp_pw_p = [[0.0] * n for _ in range(n)]
        for a in range(n):
            assert len(pw_e_mat[a]) == n and len(pw_p_mat[a]) == n
            for b in range(n):
                if a == b:
                    assert pw_e_mat[a][b] == 0.0 and pw_p_mat[a][b] == 0.0
                    continue
                de, dp = d_sh_exact(
                    members_txt[a]["q"], members_txt[a]["e"], members_txt[a]["i"],
                    members_txt[a]["node"], members_txt[a]["peri"],
                    members_txt[b]["q"], members_txt[b]["e"], members_txt[b]["i"],
                    members_txt[b]["node"], members_txt[b]["peri"],
                )
                recomp_pw_e[a][b] = de
                recomp_pw_p[a][b] = dp
                assert abs(de - pw_e_mat[a][b]) <= 2e-5, f"Pairwise exact D_SH mismatch at ({a},{b})"
                assert abs(dp - pw_p_mat[a][b]) <= 2e-5, f"Pairwise planar D_SH mismatch at ({a},{b})"

        mean_row_dsh = [sum(recomp_pw_e[a]) / (n - 1) for a in range(n)]
        medoid_idx = int(np.argmin(mean_row_dsh))
        assert medoid_idx == aud["medoid_index"] == 14
        assert members_txt[medoid_idx]["id"] == aud["medoid_trajectory_id"] == "20260907031956_faRoT"
        assert abs(mean_row_dsh[medoid_idx] - aud["mean_member_dsh_to_medoid_exact"]) <= 2e-5

        max_mem_e, max_mem_p = 0.0, 0.0
        max_med_e, max_med_p = 0.0, 0.0
        max_medoid_e, max_medoid_p = 0.0, 0.0
        for idx, (m_t, m_j) in enumerate(zip(members_txt, j_mem)):
            de_mean, dp_mean = d_sh_exact(
                mean_o["q"], mean_o["e"], mean_o["i"], mean_o["node"], mean_o["peri"],
                m_t["q"], m_t["e"], m_t["i"], m_t["node"], m_t["peri"],
            )
            de_med, dp_med = d_sh_exact(
                med_o["q"], med_o["e"], med_o["i"], med_o["node"], med_o["peri"],
                m_t["q"], m_t["e"], m_t["i"], m_t["node"], m_t["peri"],
            )
            de_medoid = recomp_pw_e[medoid_idx][idx]
            dp_medoid = recomp_pw_p[medoid_idx][idx]
            assert abs(de_mean - m_j["d_sh_to_mean_exact"]) <= 2e-5
            assert abs(dp_mean - m_j["d_sh_to_mean_planar"]) <= 2e-5
            assert abs(de_med - m_j["d_sh_to_median_exact"]) <= 2e-5
            assert abs(dp_med - m_j["d_sh_to_median_planar"]) <= 2e-5
            assert abs(de_medoid - m_j["d_sh_to_medoid_exact"]) <= 2e-5
            assert abs(dp_medoid - m_j["d_sh_to_medoid_planar"]) <= 2e-5
            max_mem_e = max(max_mem_e, de_mean)
            max_mem_p = max(max_mem_p, dp_mean)
            max_med_e = max(max_med_e, de_med)
            max_med_p = max(max_med_p, dp_med)
            max_medoid_e = max(max_medoid_e, de_medoid)
            max_medoid_p = max(max_medoid_p, dp_medoid)

        assert abs(max_mem_e - aud["max_member_dsh_exact"]) <= 2e-5 and max_mem_e < 0.10
        assert abs(max_mem_p - aud["max_member_dsh_planar"]) <= 2e-5 and max_mem_p < 0.10
        assert abs(max_med_e - aud["max_member_dsh_to_median_exact"]) <= 2e-5 and max_med_e < 0.10
        assert abs(max_med_p - aud["max_member_dsh_to_median_planar"]) <= 2e-5 and max_med_p < 0.10
        assert abs(max_medoid_e - aud["max_member_dsh_to_medoid_exact"]) <= 2e-5 and max_medoid_e < 0.10
        assert abs(max_medoid_p - aud["max_member_dsh_to_medoid_planar"]) <= 2e-5 and max_medoid_p < 0.10

        # Verify single-linkage connectedness at threshold D_SH <= 0.10
        visited = {0}
        q_bfs = deque([0])
        while q_bfs:
            u = q_bfs.popleft()
            for v in range(n):
                if v not in visited and max(recomp_pw_e[u][v], recomp_pw_p[u][v]) <= 0.10:
                    visited.add(v)
                    q_bfs.append(v)
        assert len(visited) == n and aud["single_linkage_connected_at_0p10"] is True

        # 4. Verify IAU MDC isolation across the 156 reference/neighbor rows (including LP 02646..02650)
        mdc_neighbors = cluster["mdc_reference_neighbors"]
        assert len(mdc_neighbors) == 156
        nov03_lps_found = {r["lp"] for r in mdc_neighbors if int(r["lp"]) >= 2646}
        assert nov03_lps_found == {"02646", "02647", "02648", "02649", "02650"}

        min_mdc_dsh = float("inf")
        min_mem_mdc_dsh = float("inf")
        min_rad_5deg = float("inf")
        min_rad_interval = float("inf")

        for r in mdc_neighbors:
            if None not in (r["q"], r["e"], r["i"], r["node"], r["peri"]):
                de, dp = d_sh_exact(
                    mean_o["q"], mean_o["e"], mean_o["i"], mean_o["node"], mean_o["peri"],
                    r["q"], r["e"], r["i"], r["node"], r["peri"],
                )
                assert abs(de - r["d_sh_to_mean_exact"]) <= 2e-5
                assert abs(dp - r["d_sh_to_mean_planar"]) <= 2e-5
                min_mdc_dsh = min(min_mdc_dsh, de, dp)
                m_min = min(
                    min(d_sh_exact(m["q"], m["e"], m["i"], m["node"], m["peri"],
                                   r["q"], r["e"], r["i"], r["node"], r["peri"]))
                    for m in members_txt
                )
                assert abs(m_min - r["min_member_d_sh"]) <= 2e-5
                min_mem_mdc_dsh = min(min_mem_mdc_dsh, m_min)

            if None not in (r["ra"], r["dec"]):
                sep = angular_sep_deg(mean_o["ra"], mean_o["dec"], r["ra"], r["dec"])
                assert abs(sep - r["radiant_sep_deg"]) <= 2e-3
                if r["los"] is not None and sol_lon_diff_deg(mean_o["sol_lon"], r["los"]) <= 5.0:
                    min_rad_5deg = min(min_rad_5deg, sep)
                if None not in (r["los_b"], r["los_e"]):
                    span = (r["los_e"] - r["los_b"]) % 360.0
                    if span < 120.0:
                        b_lo = (r["los_b"] - 5.0) % 360.0
                        b_hi = (r["los_e"] + 5.0) % 360.0
                        sl = mean_o["sol_lon"]
                        in_int = (b_lo <= sl <= b_hi) if b_lo <= b_hi else (sl >= b_lo or sl <= b_hi)
                        if in_int:
                            min_rad_interval = min(min_rad_interval, sep)

        assert abs(min_mdc_dsh - aud["min_mdc_dsh_all2197"]) <= 2e-5 and min_mdc_dsh >= 0.20
        assert abs(min_mem_mdc_dsh - aud["min_member_mdc_dsh_all2197"]) <= 2e-5 and min_mem_mdc_dsh >= 0.20
        assert abs(min_rad_5deg - aud["min_matched_rad_sep_deg"]) <= 2e-3 and min_rad_5deg > 5.0
        assert abs(min_rad_interval - aud["min_interval_rad_sep_deg"]) <= 2e-3 and min_rad_interval > 5.0

        # 5. Verify 400-control null test, cross-year baseline, live bootstrap, and look-elsewhere correction
        nt_cluster = cluster["null_test_400_controls"]
        for k, v in nt_cluster.items():
            assert null_doc[k] == v, f"Null test mismatch on {k}"

        hist = {int(k): int(v) for k, v in null_doc["control_histogram"].items()}
        assert sum(hist.values()) == 400 == null_doc["controls"]
        assert null_doc["n_shuffle_controls"] == 200 and null_doc["n_permute_controls"] == 200
        ctrl_expanded = []
        for k, cnt in sorted(hist.items()):
            ctrl_expanded.extend([k] * cnt)
        ctrl_arr = np.array(ctrl_expanded, dtype=np.float64)
        mu_ctrl = float(np.mean(ctrl_arr))
        sd_ctrl = float(np.std(ctrl_arr, ddof=1))
        best_ctrl = int(np.max(ctrl_arr))

        assert abs(mu_ctrl - null_doc["control_mean"]) <= 1e-4
        assert abs(sd_ctrl - null_doc["control_std"]) <= 1e-4
        assert best_ctrl == null_doc["best_control"] == 7
        assert null_doc["real"] == 16 > best_ctrl and null_doc["real_beats_all_controls"] == "yes"

        sigma_eff = max(sd_ctrl, math.sqrt(mu_ctrl))
        z_score = (16.0 - mu_ctrl) / sigma_eff
        assert abs(sigma_eff - null_doc["effective_bg_sigma"]) <= 1e-4
        assert abs(z_score - null_doc["z_score_sigma"]) <= 0.02 and z_score > 5.0

        log_p_terms = [-mu_ctrl + k * math.log(mu_ctrl) - math.lgamma(k + 1) for k in range(16, 96)]
        max_lp = max(log_p_terms)
        log_p_single = max_lp + math.log(sum(math.exp(lp - max_lp) for lp in log_p_terms))
        p_single = math.exp(log_p_single)
        log10_p_single = log_p_single / math.log(10.0)
        z_pois_single = math.sqrt(max(0.0, -2.0 * log_p_single - math.log(2.0 * math.pi)))
        assert abs(log10_p_single - null_doc["poisson_log10_p"]) <= 0.02
        assert abs(z_pois_single - null_doc["poisson_equiv_sigma"]) <= 0.02 and z_pois_single > 5.0

        # Check cross-year counts in the same window (2018-2022 baseline = 0; 2023-2026 sum = 16)
        cy = null_doc["cross_year_same_window_counts"]
        assert sum(cy[str(y)] for y in range(2018, 2023)) == 0 == null_doc["non_active_baseline_years_2018_2022_count"]
        assert sum(cy[str(y)] for y in range(2023, 2027)) == 16
        assert null_doc["adjacent_20_sideband_windows_3p5deg_counts"] == [0] * 20

        # Check look-elsewhere corrections across all 4 trial counts
        lee = null_doc["look_elsewhere_correction"]
        expected_trials = {
            "ecliptic_3p5deg_windows": 103,
            "ecliptic_1deg_bins": 360,
            "mdc_isolated_multicountry_seeds": 43228,
            "all_unassigned_multicountry_hq_trajectories": 173358,
        }
        for key, n_trials in expected_trials.items():
            entry = lee[key]
            assert entry["n_windows_or_seeds_searched"] == n_trials
            p_glob = -math.expm1(n_trials * math.log1p(-p_single))
            log_pg = math.log(p_glob)
            log10_pg = log_pg / math.log(10.0)
            z_glob = math.sqrt(max(0.0, -2.0 * log_pg - math.log(2.0 * math.pi)))
            assert abs(log10_pg - entry["global_log10_p"]) <= 0.02
            assert abs(z_glob - entry["global_gaussian_equiv_sigma"]) <= 0.02
            assert z_glob > 5.0

        # Live shuffled-solar-longitude bootstrap on the 166 external multi-country reference orbits
        ext_orbs = null_doc["external_multicountry_reference_orbits"]
        assert len(ext_orbs) == 166
        mem_id_set = {m["id"] for m in members_txt}
        for r in ext_orbs:
            assert r["id"] not in mem_id_set
            assert r["num_stat"] >= 3 and r["n_countries"] >= 2
            assert 0.0 < r["q"] < 1.2 and 0.0 < r["e"] < 1.05 and 0.0 <= r["i"] <= 180.0

        rng = np.random.default_rng(20261107)
        q_ext = np.array([r["q"] for r in ext_orbs], dtype=np.float64)
        e_ext = np.array([r["e"] for r in ext_orbs], dtype=np.float64)
        i_ext = np.radians([r["i"] for r in ext_orbs])
        w_ext = np.radians([r["peri"] for r in ext_orbs])
        o_ext = np.array([r["node"] for r in ext_orbs], dtype=np.float64)
        sl_ext = np.array([r["sol_lon"] for r in ext_orbs], dtype=np.float64)

        q0, e0 = mean_o["q"], mean_o["e"]
        i0, o0, w0 = math.radians(mean_o["i"]), math.radians(mean_o["node"]), math.radians(mean_o["peri"])
        sl0 = mean_o["sol_lon"]

        boot_counts = []
        for _ in range(1000):
            sim_d_sl = rng.uniform(-30.0, 30.0, size=len(ext_orbs))
            in_win = np.abs(sim_d_sl) <= 1.75
            if not np.any(in_win):
                boot_counts.append(0)
                continue
            old_d_sl = ((sl_ext[in_win] - sl0 + 180.0) % 360.0) - 180.0
            sim_o = np.radians((o_ext[in_win] + (sim_d_sl[in_win] - old_d_sl)) % 360.0)
            dq = q0 - q_ext[in_win]
            de = e0 - e_ext[in_win]
            d_node = (o0 - sim_o + math.pi) % (2.0 * math.pi) - math.pi
            sin_di2 = np.sin(0.5 * (i0 - i_ext[in_win]))
            sin_do2 = np.sin(0.5 * d_node)
            sin_I2_sq = np.clip(sin_di2 ** 2 + np.sin(i_ext[in_win]) * math.sin(i0) * (sin_do2 ** 2), 0.0, 1.0)
            sin_I2 = np.sqrt(sin_I2_sq)
            cos_I2 = np.sqrt(np.maximum(1e-15, 1.0 - sin_I2_sq))
            arg = np.clip(np.cos(0.5 * (i_ext[in_win] + i0)) * sin_do2 / cos_I2, -1.0, 1.0)
            pi_ab = (w0 - w_ext[in_win]) + 2.0 * np.arcsin(arg)
            term_I = 2.0 * sin_I2
            term_pi = (e_ext[in_win] + e0) * np.sin(0.5 * pi_ab)
            d_ex = np.sqrt(de * de + dq * dq + term_I * term_I + term_pi * term_pi)
            boot_counts.append(int(np.sum(d_ex < 0.075)))

        assert max(boot_counts) < 16

        print(
            f"[1/4] GMN & IAU MDC Manifest Verified: 9 GMN yearly files (3,599,504 trajectories) + "
            f"live Nov 03, 2026 IAU MDC streamfulldata2026.txt (2,197 rows, sha256={nov03_src['sha256'][:12]}...)"
        )
        print(
            f"[2/4] Single-Claim Cluster Verified (M1_Cepheus_MC): N={n} deduplicated meteors across "
            f"{len(years_union)} years {years_union}, 16/16 with num_stat>=3 (3..8) & n_countries>=2 (2..3), "
            f"15 countries, 62 distinct stations, min_dt={min_dt_sec:.1f}s"
        )
        print(
            f"[3/4] Orbital D_SH & 2,197-Row MDC Isolation Verified: max_D_SH(mean)={max_mem_e:.4f}<0.10, "
            f"max_D_SH(median)={max_med_e:.4f}<0.10, medoid={members_txt[medoid_idx]['id']} "
            f"(mean={mean_row_dsh[medoid_idx]:.4f}, max={max_medoid_e:.4f}), "
            f"min_MDC_D_SH={min_mdc_dsh:.4f}>=0.20, min_rad_sep={min_rad_5deg:.2f} deg>5.0 deg"
        )
        print(
            f"[4/4] Significance & Look-Elsewhere Verified: real=16 vs best_control=7 (400 controls, "
            f"mu={mu_ctrl:.4f}), single-window Z={z_score:.2f} sigma (Poisson {z_pois_single:.2f} sigma), "
            f"global Z={lee['ecliptic_3p5deg_windows']['global_gaussian_equiv_sigma']:.2f} sigma (103 windows) / "
            f"{lee['mdc_isolated_multicountry_seeds']['global_gaussian_equiv_sigma']:.2f} sigma (43,228 seeds) > 5.0 sigma"
        )
        print("PASS")
        sys.exit(0)
    except Exception as exc:
        fail(f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
