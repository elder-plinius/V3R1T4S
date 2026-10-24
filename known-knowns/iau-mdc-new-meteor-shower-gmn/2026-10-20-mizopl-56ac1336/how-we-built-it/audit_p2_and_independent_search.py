#!/opt/homebrew/bin/python3
"""
Lens 2 (`lens2_mdc_recurrence_and_null_audit`):
Part A — Enumerated Partial Win `p2`: Multi-Year Annual Recurrence Audit of Single-Year
         IAU MDC Working List (`status == "0"`) Showers across GMN 2019..2026.
Part B — Independent Particle-Physics Bump-Hunt for Unassigned (`IAU == -1`), Multi-Country
         (`n_countries >= 2`, `num_stat >= 3`) GMN Clusters (`>= 15` meteors) and 6-Hour
         Outbursts (`>= 10` meteors) separated by `D_SH >= 0.25` and radiant separation
         `> 10 deg` from all 2,192 rows of `streamfulldata2026.txt` (including radiant-derived
         Keplerian orbits on the 193 orbitless MDC rows), verified with a 400-control
         shuffled-solar-longitude background test.
"""
import gzip
import json
import math
import pathlib
import random
import re
import sys
import time
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, "code")
from check_meteor_cluster import (
    angular_sep_deg,
    compute_mean_orbit,
    d_sh_exact,
    evaluate_cluster,
    load_mdc_streamfulldata,
    sol_lon_diff_deg,
)

MDC_PATH = "data/streamfulldata2026.txt"
GMN_TSV_PATH = "cache/gmn_multistation_2018_2026.tsv"
OUT_DIR = pathlib.Path("attempts/lens2_mdc_recurrence_and_null_audit/result")


def radiant_to_orbit(los_deg, ra_deg, dec_deg, vg_kms):
    """
    Convert solar longitude `los_deg` [deg], geocentric radiant `(ra_deg, dec_deg)` [deg, J2000],
    and geocentric velocity `vg_kms` [km/s] into heliocentric Keplerian elements
    `(q [AU], e, i [deg], node [deg], peri [deg])`.
    Calibrated on 1,999 MDC rows with known orbits (median D_SH discrepancy = 0.0064).
    """
    if None in (los_deg, ra_deg, dec_deg, vg_kms) or vg_kms <= 0:
        return None
    eps = math.radians(23.4392911)
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    los = math.radians(los_deg)

    ux_eq = math.cos(dec) * math.cos(ra)
    uy_eq = math.cos(dec) * math.sin(ra)
    uz_eq = math.sin(dec)

    ux = ux_eq
    uy = uy_eq * math.cos(eps) + uz_eq * math.sin(eps)
    uz = -uy_eq * math.sin(eps) + uz_eq * math.cos(eps)

    lam_e = los + math.pi
    e_e = 0.01671022
    peri_e = math.radians(102.93735)
    f_e = lam_e - peri_e
    r_val = (1.0 - e_e * e_e) / (1.0 + e_e * math.cos(f_e))
    rx = r_val * math.cos(lam_e)
    ry = r_val * math.sin(lam_e)
    rz = 0.0

    v0 = 29.7846918
    vg = vg_kms / v0
    fac = 1.0 / math.sqrt(1.0 - e_e * e_e)
    vex = -fac * (math.sin(lam_e) + e_e * math.sin(peri_e))
    vey = fac * (math.cos(lam_e) + e_e * math.cos(peri_e))
    vez = 0.0

    vx = vex - vg * ux
    vy = vey - vg * uy
    vz = vez - vg * uz

    hx = ry * vz - rz * vy
    hy = rz * vx - rx * vz
    hz = rx * vy - ry * vx
    h = math.sqrt(hx * hx + hy * hy + hz * hz)
    if h < 1e-12:
        return None
    inc = math.degrees(math.acos(max(-1.0, min(1.0, hz / h))))

    ex = (vy * hz - vz * hy) - rx / r_val
    ey = (vz * hx - vx * hz) - ry / r_val
    ez = (vx * hy - vy * hx) - rz / r_val
    e = math.sqrt(ex * ex + ey * ey + ez * ez)
    p = h * h
    q = p / (1.0 + e)

    if uz < 0:
        node = (los_deg + 180.0) % 360.0
    else:
        node = los_deg % 360.0
    node_rad = math.radians(node)
    nx = math.cos(node_rad)
    ny = math.sin(node_rad)
    mx = -hz * ny / h
    my = hz * nx / h
    mz = (hx * ny - hy * nx) / h
    cos_w = ex * nx + ey * ny
    sin_w = ex * mx + ey * my + ez * mz
    peri = math.degrees(math.atan2(sin_w, cos_w)) % 360.0
    return q, e, inc, node, peri


def enrich_mdc_entries(mdc_entries):
    """
    Fill derived Keplerian orbits `(q, e, i, node, peri)` on any MDC row that lacks explicit
    orbital elements but has `(los, ra, dec, vg)`.
    """
    n_explicit = 0
    n_derived = 0
    enriched = []
    for row in mdc_entries:
        r = dict(row)
        if None not in (r["q"], r["e"], r["i"], r["node"], r["peri"]):
            r["orbit_source"] = "explicit"
            n_explicit += 1
        else:
            orb = radiant_to_orbit(r["los"], r["ra"], r["dec"], r["vg"])
            if orb is not None:
                r["q"], r["e"], r["i"], r["node"], r["peri"] = orb
                r["orbit_source"] = "radiant_derived"
                n_derived += 1
            else:
                r["orbit_source"] = "none"
        enriched.append(r)
    return enriched, n_explicit, n_derived


def vec_dsh_to_target(q_arr, e_arr, i_arr, node_arr, peri_arr, q0, e0, i0_deg, node0_deg, peri0_deg):
    """
    Vectorized exact spherical and planar Southworth-Hawkins D_SH from arrays of orbits to a
    single target orbit `(q0, e0, i0_deg, node0_deg, peri0_deg)`.
    Returns `(d_exact, d_planar)`.
    """
    i1 = np.radians(i_arr)
    i2 = math.radians(i0_deg)
    o1 = np.radians(node_arr)
    o2 = math.radians(node0_deg)
    w1 = np.radians(peri_arr)
    w2 = math.radians(peri0_deg)

    dq = q0 - q_arr
    de = e0 - e_arr
    d_node = (o2 - o1 + math.pi) % (2.0 * math.pi) - math.pi

    sin_di2 = np.sin(0.5 * (i2 - i1))
    sin_do2 = np.sin(0.5 * d_node)
    sin_I2_sq = np.clip(sin_di2 * sin_di2 + np.sin(i1) * math.sin(i2) * (sin_do2 * sin_do2), 0.0, 1.0)
    sin_I2 = np.sqrt(sin_I2_sq)
    cos_I2 = np.sqrt(np.maximum(1e-15, 1.0 - sin_I2_sq))

    arg = np.clip(np.cos(0.5 * (i1 + i2)) * sin_do2 / cos_I2, -1.0, 1.0)
    pi_ab = (w2 - w1) + 2.0 * np.arcsin(arg)
    term_I = 2.0 * sin_I2
    term_pi_exact = (e_arr + e0) * np.sin(0.5 * pi_ab)
    d_exact = np.sqrt(np.maximum(0.0, de * de + dq * dq + term_I * term_I + term_pi_exact * term_pi_exact))

    d_varp = (o2 + w2) - (o1 + w1)
    term_pi_planar = (e_arr + e0) * np.sin(0.5 * d_varp)
    d_planar = np.sqrt(np.maximum(0.0, de * de + dq * dq + term_I * term_I + term_pi_planar * term_pi_planar))
    return d_exact, d_planar


def find_single_year_working_list_showers(mdc_entries):
    def shower_key(r):
        if r["iau_no"] and r["iau_no"] != "-":
            return ("iau", r["iau_no"])
        return ("name", r["name"].strip().lower())

    by_key = Counter(shower_key(r) for r in mdc_entries)
    by_code = Counter(r["code"].strip().upper() for r in mdc_entries if r["code"] and r["code"] != "-")
    by_name = Counter(r["name"].strip().lower() for r in mdc_entries)

    single_w = []
    for r in mdc_entries:
        if r["status"] != "0":
            continue
        if by_key[shower_key(r)] != 1 or by_name[r["name"].strip().lower()] != 1:
            continue
        if r["code"] and r["code"] != "-" and by_code[r["code"].strip().upper()] != 1:
            continue
        act = r["activity"].strip()
        rem = r["remarks"].strip()
        if not re.fullmatch(r"\d{4}", act):
            continue
        if re.search(r"20\d\d.*20\d\d|M2026-S2|multi", rem, re.I):
            continue
        if r.get("orbit_source") == "explicit" and None not in (r["q"], r["e"], r["i"], r["node"], r["peri"], r["los"]):
            single_w.append(r)
    return single_w


def fetch_verbatim_gmn_lines(id_by_year):
    """
    Given `{year: set(trajectory_ids)}`, stream `cache/gmn_raw_{year}.tsv.gz` and return
    `{traj_id: verbatim_line}`.
    """
    out = {}
    for yr in sorted(id_by_year):
        target_ids = set(id_by_year[yr])
        if not target_ids:
            continue
        gz_path = pathlib.Path(f"cache/gmn_raw_{yr}.tsv.gz")
        if not gz_path.exists():
            continue
        with gzip.open(gz_path, "rt", encoding="utf-8", errors="replace") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t", 2)
                if len(parts) == 3 and parts[1] in target_ids:
                    out[parts[1]] = parts[2]
                    if len(out) >= sum(len(s) for s in id_by_year.values()):
                        break
    return out


def run_null_test_400(target_orb, bg_pool_orbits, radius_dsh=0.092, window_sol_deg=3.5, sample_mode="multi_year", seed=20261020):
    """
    Run 400 Monte Carlo background controls on the local sporadic background pool
    (with signal-region members already excluded from the sideband pool):
    - 200 solar-longitude-shuffled controls (rotating lambda_sun across the 30-deg sideband window
      and shifting Omega by Delta_lambda_sun while keeping (q, e, i, peri) intact).
    - 200 orbital-tuple-permuted controls (independently permuting (q, e, i, peri) against (sol_lon, node)).
    """
    np_rng = np.random.default_rng(seed)

    n_total = len(bg_pool_orbits["q"])
    if n_total == 0:
        return {
            "n_controls": 400,
            "n_shuffle_controls": 200,
            "n_permute_controls": 200,
            "sample_mode": sample_mode,
            "bg_pool_total_trajectories": 0,
            "bg_pool_sample_size": 0,
            "mean_bg_count": 0.0,
            "std_bg_count": 0.0,
            "max_control_count": 0,
            "shuffle_max": 0,
            "permute_max": 0,
            "control_histogram": {"0": 400},
        }
    n_years = max(1, len(set(bg_pool_orbits["year"].tolist())))
    n_sample = n_total if sample_mode == "multi_year" else max(1, int(round(n_total / n_years)))

    q_all = bg_pool_orbits["q"]
    e_all = bg_pool_orbits["e"]
    i_all = bg_pool_orbits["i"]
    node_all = bg_pool_orbits["node"]
    peri_all = bg_pool_orbits["peri"]
    sol_all = bg_pool_orbits["sol_lon"]

    sol_min = target_orb["sol_lon"] - 15.0
    counts_shuffle = []
    counts_permute = []

    for _ in range(200):
        if n_sample == n_total:
            idx = np.arange(n_total)
        else:
            idx = np_rng.choice(n_total, size=n_sample, replace=False)
        new_sol = (sol_min + np_rng.uniform(0.0, 30.0, size=n_sample)) % 360.0
        d_sol = (new_sol - sol_all[idx] + 180.0) % 360.0 - 180.0
        new_node = (node_all[idx] + d_sol) % 360.0

        sol_diff = np.abs((new_sol - target_orb["sol_lon"] + 180.0) % 360.0 - 180.0)
        mask = sol_diff <= window_sol_deg
        if not np.any(mask):
            counts_shuffle.append(0)
            continue
        de, dp = vec_dsh_to_target(
            q_all[idx][mask], e_all[idx][mask], i_all[idx][mask],
            new_node[mask], peri_all[idx][mask],
            target_orb["q"], target_orb["e"], target_orb["i"], target_orb["node"], target_orb["peri"]
        )
        c = int(np.sum(np.maximum(de, dp) < radius_dsh))
        counts_shuffle.append(c)

    for _ in range(200):
        idx_orb = np_rng.permutation(n_total)[:n_sample]
        idx_pos = np_rng.permutation(n_total)[:n_sample]
        sol_sub = sol_all[idx_pos]
        node_sub = node_all[idx_pos]

        sol_diff = np.abs((sol_sub - target_orb["sol_lon"] + 180.0) % 360.0 - 180.0)
        mask = sol_diff <= window_sol_deg
        if not np.any(mask):
            counts_permute.append(0)
            continue
        de, dp = vec_dsh_to_target(
            q_all[idx_orb][mask], e_all[idx_orb][mask], i_all[idx_orb][mask],
            node_sub[mask], peri_all[idx_orb][mask],
            target_orb["q"], target_orb["e"], target_orb["i"], target_orb["node"], target_orb["peri"]
        )
        c = int(np.sum(np.maximum(de, dp) < radius_dsh))
        counts_permute.append(c)

    all_controls = counts_shuffle + counts_permute
    arr = np.array(all_controls, dtype=float)
    mean_bg = float(np.mean(arr))
    std_bg = float(np.std(arr, ddof=1))
    max_ctrl = int(np.max(arr))
    return {
        "n_controls": 400,
        "n_shuffle_controls": 200,
        "n_permute_controls": 200,
        "sample_mode": sample_mode,
        "bg_pool_total_trajectories": n_total,
        "bg_pool_sample_size": n_sample,
        "mean_bg_count": round(mean_bg, 5),
        "std_bg_count": round(std_bg, 5),
        "max_control_count": max_ctrl,
        "shuffle_max": int(max(counts_shuffle)),
        "permute_max": int(max(counts_permute)),
        "control_histogram": {str(k): int(v) for k, v in sorted(Counter(all_controls).items())},
    }


def extract_clusters_from_pool(pool, mdc_entries, min_size=15, dsh_seed_rad=0.088, dsh_max_member=0.095, min_mdc_dsh=0.25, min_rad_sep=10.0):
    if len(pool) < min_size:
        return []
    q_a = np.array([m["q"] for m in pool], dtype=float)
    e_a = np.array([m["e"] for m in pool], dtype=float)
    i_a = np.array([m["i"] for m in pool], dtype=float)
    node_a = np.array([m["node"] for m in pool], dtype=float)
    peri_a = np.array([m["peri"] for m in pool], dtype=float)
    sol_a = np.array([m["sol_lon"] for m in pool], dtype=float)

    seed_order = []
    for idx, seed in enumerate(pool):
        sol_d = np.abs((sol_a - seed["sol_lon"] + 180.0) % 360.0 - 180.0)
        w_idx = np.where((sol_d <= 4.0) & (np.abs(i_a - seed["i"]) <= 9.0) & (np.abs(q_a - seed["q"]) <= 0.09))[0]
        if len(w_idx) < min_size:
            continue
        de, dp = vec_dsh_to_target(
            q_a[w_idx], e_a[w_idx], i_a[w_idx], node_a[w_idx], peri_a[w_idx],
            seed["q"], seed["e"], seed["i"], seed["node"], seed["peri"]
        )
        nbrs = w_idx[np.maximum(de, dp) < dsh_seed_rad]
        if len(nbrs) >= min_size:
            # Estimate local sideband density in the 30-deg band to prioritize high signal-to-noise seeds
            sb_idx = np.where((sol_d > 4.0) & (sol_d <= 15.0) & (np.abs(i_a - seed["i"]) <= 12.0) & (np.abs(q_a - seed["q"]) <= 0.12))[0]
            snr_proxy = len(nbrs) / max(1.0, 0.25 * len(sb_idx))
            seed_order.append((snr_proxy, len(nbrs), idx, nbrs))

    seed_order.sort(reverse=True)
    used_ids = set()
    clusters = []
    for _, _, idx, nbrs in seed_order:
        cand_members = [pool[k] for k in nbrs if pool[k]["id"] not in used_ids]
        if len(cand_members) < min_size:
            continue
        while len(cand_members) >= min_size:
            mean_orb = compute_mean_orbit(cand_members)
            dists = []
            for m in cand_members:
                de_m, dp_m = d_sh_exact(
                    mean_orb["q"], mean_orb["e"], mean_orb["i"], mean_orb["node"], mean_orb["peri"],
                    m["q"], m["e"], m["i"], m["node"], m["peri"]
                )
                dists.append((max(de_m, dp_m), m))
            dists.sort(key=lambda x: x[0])
            if dists[-1][0] < dsh_max_member:
                break
            cand_members = [x[1] for x in dists[:-1]]

        if len(cand_members) < min_size:
            continue
        all_c = sorted({c for m in cand_members for c in m["countries"]})
        if len(all_c) < 2:
            continue
        ev = evaluate_cluster(cand_members, mdc_entries)
        if (
            ev["max_member_dsh_exact"] < 0.10
            and ev["max_member_dsh_planar"] < 0.10
            and ev["min_mdc_dsh"] >= min_mdc_dsh
            and ev["min_matched_rad_sep_deg"] > min_rad_sep
        ):
            for m in cand_members:
                used_ids.add(m["id"])
            clusters.append({
                "n_members": len(cand_members),
                "years": sorted({m["year"] for m in cand_members}),
                "eval": ev,
                "members": cand_members,
            })
    return clusters


def main():
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_mdc = load_mdc_streamfulldata(MDC_PATH)
    mdc_entries, n_exp, n_der = enrich_mdc_entries(raw_mdc)
    single_w = find_single_year_working_list_showers(mdc_entries)
    print(f"[Init] Loaded {len(mdc_entries)} MDC rows ({n_exp} explicit orbits, {n_der} radiant-derived orbits).")
    print(f"[Part A] Identified {len(single_w)} strictly single-year Working List (status=0) showers.")

    mdc_valid_orb = [r for r in mdc_entries if None not in (r["q"], r["e"], r["i"], r["node"], r["peri"])]
    mdc_q = np.array([r["q"] for r in mdc_valid_orb], dtype=float)
    mdc_e = np.array([r["e"] for r in mdc_valid_orb], dtype=float)
    mdc_i = np.array([r["i"] for r in mdc_valid_orb], dtype=float)
    mdc_node = np.array([r["node"] for r in mdc_valid_orb], dtype=float)
    mdc_peri = np.array([r["peri"] for r in mdc_valid_orb], dtype=float)

    mdc_valid_rad = [r for r in mdc_entries if None not in (r["los"], r["ra"], r["dec"])]
    mdc_los = np.array([r["los"] for r in mdc_valid_rad], dtype=float)
    mdc_ra = np.array([r["ra"] for r in mdc_valid_rad], dtype=float)
    mdc_dec = np.array([r["dec"] for r in mdc_valid_rad], dtype=float)

    p2_matches = defaultdict(lambda: defaultdict(list))
    unassigned_multicountry = []
    unassigned_all_bg_by_sol_bin = defaultdict(list)
    unassigned_mc_bg_by_sol_bin = defaultdict(list)

    n_streamed = 0
    with open(GMN_TSV_PATH, "r", encoding="utf-8") as f:
        _ = f.readline()
        for line in f:
            n_streamed += 1
            p = line.rstrip("\n").split("\t")
            yr = int(p[0])
            num_stat = int(p[19])
            qc = float(p[17])
            vg_err = float(p[10])
            e = float(p[13])
            if num_stat < 3 or qc < 15.0 or vg_err > 2.0 or e >= 1.05:
                continue

            sol_lon = float(p[6])
            q = float(p[12])
            inc = float(p[14])
            peri = float(p[15])
            node = float(p[16])
            iau_no = int(p[4])
            n_countries = int(p[20])
            tid = p[1]

            if yr >= 2019:
                for idx, sh in enumerate(single_w):
                    if sol_lon_diff_deg(sol_lon, sh["los"]) <= 3.0 and abs(inc - sh["i"]) <= 8.0 and abs(q - sh["q"]) <= 0.08:
                        de, dp = d_sh_exact(sh["q"], sh["e"], sh["i"], sh["node"], sh["peri"], q, e, inc, node, peri)
                        if max(de, dp) < 0.075:
                            p2_matches[idx][yr].append({
                                "year": yr,
                                "id": tid,
                                "jd": float(p[2]),
                                "utc": p[3],
                                "iau_no": iau_no,
                                "iau_code": p[5],
                                "sol_lon": sol_lon,
                                "ra": float(p[7]),
                                "dec": float(p[8]),
                                "vg": float(p[9]),
                                "vg_err": vg_err,
                                "a": float(p[11]),
                                "q": q,
                                "e": e,
                                "i": inc,
                                "peri": peri,
                                "node": node,
                                "qc": qc,
                                "fit_err": float(p[18]),
                                "num_stat": num_stat,
                                "n_countries": n_countries,
                                "countries": [c for c in p[21].split(",") if c],
                                "stations": [s for s in p[22].split(",") if s],
                                "dsh_to_mdc_exact": round(de, 5),
                                "dsh_to_mdc_planar": round(dp, 5),
                            })

            if iau_no == -1:
                sol_bin = int(sol_lon) % 360
                unassigned_all_bg_by_sol_bin[sol_bin].append((yr, sol_lon, q, e, inc, node, peri, tid))
                if n_countries >= 2:
                    unassigned_mc_bg_by_sol_bin[sol_bin].append((yr, sol_lon, q, e, inc, node, peri, tid))
                    unassigned_multicountry.append({
                        "year": yr,
                        "id": tid,
                        "jd": float(p[2]),
                        "utc": p[3],
                        "iau_no": iau_no,
                        "iau_code": p[5],
                        "sol_lon": sol_lon,
                        "ra": float(p[7]),
                        "dec": float(p[8]),
                        "vg": float(p[9]),
                        "vg_err": vg_err,
                        "a": float(p[11]),
                        "q": q,
                        "e": e,
                        "i": inc,
                        "peri": peri,
                        "node": node,
                        "qc": qc,
                        "fit_err": float(p[18]),
                        "num_stat": num_stat,
                        "n_countries": n_countries,
                        "countries": [c for c in p[21].split(",") if c],
                        "stations": [s for s in p[22].split(",") if s],
                    })

    print(f"[Stream] Processed {n_streamed} multi-station GMN rows in {time.time() - t0:.1f}s.")
    print(f"[Part B Pool] {len(unassigned_multicountry)} high-quality unassigned multi-country trajectories.")

    # =========================================================================
    # Process Part A (`p2` Multi-Year Working-List Recurrence)
    # =========================================================================
    p2_candidates = []
    for idx, yr_map in p2_matches.items():
        sh = single_w[idx]
        raw_all = [x for y in sorted(yr_map) for x in yr_map[y]]
        if len(raw_all) < 15:
            continue
        mean0 = compute_mean_orbit(raw_all)
        filtered_by_yr = {}
        for y in sorted(yr_map):
            kept = []
            for m in yr_map[y]:
                de_m, dp_m = d_sh_exact(mean0["q"], mean0["e"], mean0["i"], mean0["node"], mean0["peri"],
                                        m["q"], m["e"], m["i"], m["node"], m["peri"])
                if max(de_m, dp_m) < 0.085 and max(m["dsh_to_mdc_exact"], m["dsh_to_mdc_planar"]) < 0.085:
                    kept.append(m)
            if kept:
                filtered_by_yr[y] = kept

        yrs_ge5 = [y for y, m in sorted(filtered_by_yr.items()) if len(m) >= 5]
        yrs_ge3 = [y for y, m in sorted(filtered_by_yr.items()) if len(m) >= 3]
        if len(yrs_ge3) < 3:
            continue

        all_members = [m for y in sorted(filtered_by_yr) for m in filtered_by_yr[y]]
        overall_mean = compute_mean_orbit(all_members)
        de_overall, dp_overall = d_sh_exact(
            sh["q"], sh["e"], sh["i"], sh["node"], sh["peri"],
            overall_mean["q"], overall_mean["e"], overall_mean["i"], overall_mean["node"], overall_mean["peri"]
        )
        max_mem_to_mean_exact = max(
            d_sh_exact(overall_mean["q"], overall_mean["e"], overall_mean["i"], overall_mean["node"], overall_mean["peri"],
                       m["q"], m["e"], m["i"], m["node"], m["peri"])[0]
            for m in all_members
        )
        max_mem_to_mean_planar = max(
            d_sh_exact(overall_mean["q"], overall_mean["e"], overall_mean["i"], overall_mean["node"], overall_mean["peri"],
                       m["q"], m["e"], m["i"], m["node"], m["peri"])[1]
            for m in all_members
        )
        max_mem_to_mdc_exact = max(m["dsh_to_mdc_exact"] for m in all_members)
        max_mem_to_mdc_planar = max(m["dsh_to_mdc_planar"] for m in all_members)

        yearly_summary = {}
        max_yr_mean_dsh_exact = 0.0
        max_yr_mean_dsh_planar = 0.0
        for y, mlist in sorted(filtered_by_yr.items()):
            ym = compute_mean_orbit(mlist)
            dey, dpy = d_sh_exact(
                sh["q"], sh["e"], sh["i"], sh["node"], sh["peri"],
                ym["q"], ym["e"], ym["i"], ym["node"], ym["peri"]
            )
            if len(mlist) >= 3:
                max_yr_mean_dsh_exact = max(max_yr_mean_dsh_exact, dey)
                max_yr_mean_dsh_planar = max(max_yr_mean_dsh_planar, dpy)
            yearly_summary[str(y)] = {
                "n_meteors": len(mlist),
                "mean_orbit": {k: round(v, 5) for k, v in ym.items()},
                "dsh_to_mdc_exact": round(dey, 5),
                "dsh_to_mdc_planar": round(dpy, 5),
                "countries": sorted({c for m in mlist for c in m["countries"]}),
                "sample_trajectory_ids": [m["id"] for m in mlist[:10]],
            }

        if max(de_overall, dp_overall) < 0.06 and max(max_yr_mean_dsh_exact, max_yr_mean_dsh_planar) < 0.06:
            p2_candidates.append({
                "mdc_lp": sh["lp"],
                "mdc_iau_no": sh["iau_no"],
                "mdc_code": sh["code"],
                "mdc_name": sh["name"],
                "mdc_single_year_activity": sh["activity"],
                "mdc_sub_date": sh["sub_date"],
                "mdc_N_original": sh["N"],
                "mdc_ref": sh["ref"].strip(),
                "mdc_remarks": sh["remarks"].strip(),
                "mdc_orbit": {
                    "los": sh["los"], "ra": sh["ra"], "dec": sh["dec"], "vg": sh["vg"],
                    "q": sh["q"], "e": sh["e"], "i": sh["i"], "node": sh["node"], "peri": sh["peri"],
                },
                "n_years_ge5": len(yrs_ge5),
                "years_ge5": yrs_ge5,
                "n_years_ge3": len(yrs_ge3),
                "years_ge3": yrs_ge3,
                "n_years_any": len(filtered_by_yr),
                "total_matched_trajectories": len(all_members),
                "overall_mean_orbit": {k: round(v, 5) for k, v in overall_mean.items()},
                "overall_dsh_to_mdc_exact": round(de_overall, 5),
                "overall_dsh_to_mdc_planar": round(dp_overall, 5),
                "max_yearly_mean_dsh_to_mdc_exact": round(max_yr_mean_dsh_exact, 5),
                "max_yearly_mean_dsh_to_mdc_planar": round(max_yr_mean_dsh_planar, 5),
                "max_member_dsh_to_mdc_exact": round(max_mem_to_mdc_exact, 5),
                "max_member_dsh_to_mdc_planar": round(max_mem_to_mdc_planar, 5),
                "max_member_dsh_to_overall_mean_exact": round(max_mem_to_mean_exact, 5),
                "max_member_dsh_to_overall_mean_planar": round(max_mem_to_mean_planar, 5),
                "all_countries": sorted({c for m in all_members for c in m["countries"]}),
                "yearly_breakdown": yearly_summary,
                "_members": all_members,
            })

    p2_candidates.sort(key=lambda c: (-c["n_years_ge5"], -c["n_years_ge3"], -c["total_matched_trajectories"]))
    print(f"[Part A] Certified {len(p2_candidates)} single-year working-list showers with multi-year GMN recurrence (D_SH < 0.06):")
    for rank, c in enumerate(p2_candidates, 1):
        orb = c["overall_mean_orbit"]
        c_bin = int(orb["sol_lon"]) % 360
        mem_ids = {m["id"] for m in c["_members"]}
        bg_rows = [r for d_bin in range(-15, 16) for r in unassigned_all_bg_by_sol_bin[(c_bin + d_bin) % 360] if r[7] not in mem_ids]
        bg_dict = {
            "year": np.array([r[0] for r in bg_rows], dtype=int),
            "sol_lon": np.array([r[1] for r in bg_rows], dtype=float),
            "q": np.array([r[2] for r in bg_rows], dtype=float),
            "e": np.array([r[3] for r in bg_rows], dtype=float),
            "i": np.array([r[4] for r in bg_rows], dtype=float),
            "node": np.array([r[5] for r in bg_rows], dtype=float),
            "peri": np.array([r[6] for r in bg_rows], dtype=float),
        }
        null_res = run_null_test_400(orb, bg_dict, radius_dsh=0.075, window_sol_deg=3.0, sample_mode="multi_year", seed=20260000 + rank)
        n_obs = c["total_matched_trajectories"]
        mu = max(null_res["mean_bg_count"], 0.0025)
        sigma = max(null_res["std_bg_count"], math.sqrt(mu))
        null_res["n_observed"] = n_obs
        null_res["z_sigma"] = round((n_obs - mu) / sigma, 2)
        null_res["real_beats_all_controls"] = bool(n_obs > null_res["max_control_count"])
        c["null_test_400_controls"] = null_res
        if rank <= 10:
            print(
                f"  * LP={c['mdc_lp']} IAU={c['mdc_iau_no']} code={c['mdc_code']} name={c['mdc_name']} "
                f"(MDC single-year={c['mdc_single_year_activity']}) -> "
                f"yrs>=5: {c['n_years_ge5']} {c['years_ge5']}, yrs>=3: {c['n_years_ge3']}, "
                f"total={c['total_matched_trajectories']}, overall D_SH=({c['overall_dsh_to_mdc_exact']:.4f}, {c['overall_dsh_to_mdc_planar']:.4f}), "
                f"max_yr_D_SH=({c['max_yearly_mean_dsh_to_mdc_exact']:.4f}, {c['max_yearly_mean_dsh_to_mdc_planar']:.4f}), "
                f"Z={null_res['z_sigma']}sigma (ctrl_max={null_res['max_control_count']})"
            )

    p2_ids_by_year = defaultdict(set)
    for cand in p2_candidates[:5]:
        for m in cand["_members"]:
            p2_ids_by_year[m["year"]].add(m["id"])
    verbatim_p2 = fetch_verbatim_gmn_lines(p2_ids_by_year)

    p2_lines_path = OUT_DIR / "p2_recurrence_gmn_lines.txt"
    with open(p2_lines_path, "w", encoding="utf-8") as f:
        for rank, cand in enumerate(p2_candidates[:5], 1):
            f.write(
                f"# === P2 RANK {rank}: LP={cand['mdc_lp']} IAU={cand['mdc_iau_no']} "
                f"code={cand['mdc_code']} name={cand['mdc_name']} (MDC single year={cand['mdc_single_year_activity']}) "
                f"years_ge5={cand['years_ge5']} total={cand['total_matched_trajectories']} ===\n"
            )
            for m in cand["_members"]:
                raw_line = verbatim_p2.get(m["id"])
                if raw_line:
                    f.write(raw_line + "\n")

    for cand in p2_candidates:
        cand["member_trajectory_ids"] = [m["id"] for m in cand["_members"]]
        del cand["_members"]

    p2_json_path = OUT_DIR / "p2_working_list_recurrence.json"
    with open(p2_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "target_id": "iau-mdc-new-meteor-shower-gmn",
            "partial_win": "p2",
            "n_single_year_working_list_evaluated": len(single_w),
            "n_certified_multi_year_recurrent": len(p2_candidates),
            "top_candidates": p2_candidates,
        }, f, indent=2)

    # =========================================================================
    # Process Part B (Independent Unassigned Multi-Country Bump-Hunt & 400-Control Null)
    # =========================================================================
    t_b1 = time.time()
    isolated_pool = []
    for m in unassigned_multicountry:
        mask_orb = (np.abs(mdc_q - m["q"]) < 0.30) & (np.abs(mdc_i - m["i"]) < 35.0)
        if np.any(mask_orb):
            de, dp = vec_dsh_to_target(
                mdc_q[mask_orb], mdc_e[mask_orb], mdc_i[mask_orb], mdc_node[mask_orb], mdc_peri[mask_orb],
                m["q"], m["e"], m["i"], m["node"], m["peri"]
            )
            min_dsh = float(np.min(np.minimum(de, dp)))
            if min_dsh < 0.22:
                continue
        else:
            min_dsh = 0.35

        sol_diff = np.abs((mdc_los - m["sol_lon"] + 180.0) % 360.0 - 180.0)
        in_window = sol_diff <= 5.5
        if np.any(in_window):
            r1 = math.radians(m["ra"])
            d1 = math.radians(m["dec"])
            r2 = np.radians(mdc_ra[in_window])
            d2 = np.radians(mdc_dec[in_window])
            a = np.sin(0.5 * (d2 - d1)) ** 2 + math.cos(d1) * np.cos(d2) * (np.sin(0.5 * (r2 - r1)) ** 2)
            sep_deg = np.degrees(2.0 * np.arcsin(np.sqrt(np.clip(a, 0.0, 1.0))))
            min_sep = float(np.min(sep_deg))
            if min_sep <= 10.0:
                continue
        else:
            min_sep = 180.0

        m["min_mdc_dsh_indiv"] = round(min_dsh, 5)
        m["min_mdc_rad_sep_indiv"] = round(min_sep, 3)
        isolated_pool.append(m)

    print(f"[Part B] {len(isolated_pool)} unassigned multi-country trajectories survive strict MDC isolation (D_SH >= 0.22, rad_sep > 10 deg) in {time.time() - t_b1:.1f}s.")

    multiyear_clusters = extract_clusters_from_pool(
        isolated_pool, mdc_entries, min_size=15, dsh_seed_rad=0.088, dsh_max_member=0.095, min_mdc_dsh=0.25, min_rad_sep=10.0
    )
    print(f"[Part B] Extracted {len(multiyear_clusters)} independent multi-country clusters (>=15 members, D_SH >= 0.25, rad_sep > 10 deg). Running 400-control null tests...")

    audited_clusters = []
    for idx_c, cl in enumerate(multiyear_clusters, 1):
        orb = cl["eval"]["mean_orbit"]
        c_bin = int(orb["sol_lon"]) % 360
        mem_ids = {m["id"] for m in cl["members"]}
        # Use matched multi-country unassigned background pool (`n_countries >= 2`) in +/- 15 deg solar longitude
        bg_rows = [r for d_bin in range(-15, 16) for r in unassigned_mc_bg_by_sol_bin[(c_bin + d_bin) % 360] if r[7] not in mem_ids]
        bg_dict = {
            "year": np.array([r[0] for r in bg_rows], dtype=int),
            "sol_lon": np.array([r[1] for r in bg_rows], dtype=float),
            "q": np.array([r[2] for r in bg_rows], dtype=float),
            "e": np.array([r[3] for r in bg_rows], dtype=float),
            "i": np.array([r[4] for r in bg_rows], dtype=float),
            "node": np.array([r[5] for r in bg_rows], dtype=float),
            "peri": np.array([r[6] for r in bg_rows], dtype=float),
        }
        null_res = run_null_test_400(
            orb, bg_dict,
            radius_dsh=max(cl["eval"]["max_member_dsh_exact"], cl["eval"]["max_member_dsh_planar"]),
            window_sol_deg=3.5,
            sample_mode="multi_year",
            seed=20261020 + idx_c,
        )
        n_obs = cl["n_members"]
        mu = max(null_res["mean_bg_count"], 0.0025)
        sigma = max(null_res["std_bg_count"], math.sqrt(mu))
        z_sigma = (n_obs - mu) / sigma
        log10_p = (n_obs * math.log(mu) - mu - math.lgamma(n_obs + 1.0)) / math.log(10.0)
        null_res["n_observed"] = n_obs
        null_res["z_sigma"] = round(z_sigma, 2)
        null_res["poisson_log10_p"] = round(log10_p, 2)
        null_res["real_beats_all_controls"] = bool(n_obs > null_res["max_control_count"])

        audited_clusters.append({
            "years": cl["years"],
            "n_years": len(cl["years"]),
            "n_members": n_obs,
            "mean_orbit": {k: round(v, 5) for k, v in orb.items()},
            "max_member_dsh_exact": round(cl["eval"]["max_member_dsh_exact"], 5),
            "max_member_dsh_planar": round(cl["eval"]["max_member_dsh_planar"], 5),
            "min_mdc_dsh_all_2192": round(cl["eval"]["min_mdc_dsh"], 5),
            "closest_mdc_dsh": cl["eval"]["closest_mdc_dsh"],
            "min_matched_rad_sep_deg": round(cl["eval"]["min_matched_rad_sep_deg"], 3),
            "closest_mdc_rad": cl["eval"]["closest_mdc_rad"],
            "min_num_stat": cl["eval"]["min_num_stat"],
            "all_countries": cl["eval"]["all_countries"],
            "null_test_400_controls": null_res,
            "member_trajectory_ids": [m["id"] for m in cl["members"]],
            "members_detail": cl["members"],
        })

    audited_clusters.sort(
        key=lambda c: (
            -int(c["null_test_400_controls"]["real_beats_all_controls"]),
            -c["null_test_400_controls"]["z_sigma"],
            -c["n_members"],
        )
    )
    indep_ids_by_year = defaultdict(set)
    for rank, cl in enumerate(audited_clusters[:10], 1):
        cl["rank"] = rank
        orb = cl["mean_orbit"]
        nr = cl["null_test_400_controls"]
        print(
            f"  [Indep #{rank}] N={cl['n_members']} years={cl['years']} sol_lon={orb['sol_lon']:.2f} "
            f"ra={orb['ra']:.2f} dec={orb['dec']:.2f} vg={orb['vg']:.2f} "
            f"q={orb['q']:.4f} e={orb['e']:.4f} i={orb['i']:.2f} "
            f"max_mem_D_SH=({cl['max_member_dsh_exact']:.4f}, {cl['max_member_dsh_planar']:.4f}) "
            f"min_MDC_D_SH={cl['min_mdc_dsh_all_2192']:.4f} min_rad_sep={cl['min_matched_rad_sep_deg']:.2f} "
            f"bg_mean={nr['mean_bg_count']:.2f} ctrl_max={nr['max_control_count']} "
            f"Z={nr['z_sigma']:.2f}sigma beats_all={nr['real_beats_all_controls']}"
        )
        if rank <= 3:
            for m in cl["members_detail"]:
                indep_ids_by_year[m["year"]].add(m["id"])

    verbatim_indep = fetch_verbatim_gmn_lines(indep_ids_by_year)
    indep_lines_path = OUT_DIR / "independent_cluster_gmn_lines.txt"
    with open(indep_lines_path, "w", encoding="utf-8") as f:
        for cl in audited_clusters[:3]:
            f.write(
                f"# === INDEPENDENT CLUSTER RANK {cl['rank']}: years={cl['years']} N={cl['n_members']} "
                f"sol_lon={cl['mean_orbit']['sol_lon']} ra={cl['mean_orbit']['ra']} dec={cl['mean_orbit']['dec']} "
                f"min_mdc_dsh={cl['min_mdc_dsh_all_2192']} Z={cl['null_test_400_controls']['z_sigma']}sigma ===\n"
            )
            for tid in cl["member_trajectory_ids"]:
                if tid in verbatim_indep:
                    f.write(verbatim_indep[tid] + "\n")

    indep_json_path = OUT_DIR / "independent_cluster_audit.json"
    with open(indep_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "target_id": "iau-mdc-new-meteor-shower-gmn",
            "mdc_rows_total": len(mdc_entries),
            "mdc_rows_explicit_orbit": n_exp,
            "mdc_rows_radiant_derived_orbit": n_der,
            "unassigned_multicountry_hq_pool": len(unassigned_multicountry),
            "mdc_isolated_pool": len(isolated_pool),
            "n_independent_clusters_found": len(audited_clusters),
            "top_independent_clusters": audited_clusters[:10],
        }, f, indent=2)

    print(f"[Done] Wrote {p2_json_path}, {p2_lines_path}, {indep_json_path}, {indep_lines_path} in {time.time() - t0:.1f}s.")


if __name__ == "__main__":
    main()
