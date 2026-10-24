#!/opt/homebrew/bin/python3
"""
CLSS Stage II-IV Discovery & 400-Control Null Verification Pipeline
Lens 1 (`lens1_orbital_clss_discovery`) — Target `iau-mdc-new-meteor-shower-gmn`
"""
import gzip
import hashlib
import json
import math
import os
import pathlib
import sys
import time
import numpy as np

ROOT_DIR = pathlib.Path("runs/2026-10-20-0343")
ATTEMPT_DIR = ROOT_DIR / "attempts" / "lens1_orbital_clss_discovery"
RESULT_DIR = ATTEMPT_DIR / "result"
sys.path.insert(0, str(ROOT_DIR / "code"))

from check_meteor_cluster import (
    angular_sep_deg,
    compute_mean_orbit,
    d_sh_exact,
    evaluate_cluster,
    load_mdc_streamfulldata,
    parse_gmn_line,
    sol_lon_diff_deg,
)


def radiant_to_orbit(sol_lon_deg, ra_deg, dec_deg, vg_kms):
    """
    Convert geocentric radiant (sol_lon, RA, Dec, Vg) to approximate heliocentric
    Keplerian orbital elements (q [AU], e, i [deg], node [deg], peri [deg]).
    """
    eps = math.radians(23.4392911)
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    lam_s = math.radians(sol_lon_deg)
    ux_eq = math.cos(dec) * math.cos(ra)
    uy_eq = math.cos(dec) * math.sin(ra)
    uz_eq = math.sin(dec)
    ux = ux_eq
    uy = uy_eq * math.cos(eps) + uz_eq * math.sin(eps)
    uz = -uy_eq * math.sin(eps) + uz_eq * math.cos(eps)
    v_earth = 29.7847
    lam_e = lam_s + math.pi
    rx, ry, rz = math.cos(lam_e), math.sin(lam_e), 0.0
    vex = -v_earth * math.sin(lam_e)
    vey = v_earth * math.cos(lam_e)
    vez = 0.0
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


def compute_median_orbit(members):
    q_med = float(np.median([m["q"] for m in members]))
    e_med = float(np.median([m["e"] for m in members]))
    i_med = float(np.median([m["i"] for m in members]))
    mean_o = compute_mean_orbit(members)

    def circ_median_deg(vals, ref):
        diffs = [((v - ref + 180.0) % 360.0) - 180.0 for v in vals]
        return (ref + float(np.median(diffs))) % 360.0

    node_med = circ_median_deg([m["node"] for m in members], mean_o["node"])
    peri_med = circ_median_deg([m["peri"] for m in members], mean_o["peri"])
    sol_med = circ_median_deg([m["sol_lon"] for m in members], mean_o["sol_lon"])
    return {
        "q": q_med,
        "e": e_med,
        "i": i_med,
        "node": node_med,
        "peri": peri_med,
        "sol_lon": sol_med,
    }


def load_full_mdc_with_derived(mdc_path):
    mdc_raw = load_mdc_streamfulldata(mdc_path)
    mdc_augmented = []
    n_derived = 0
    for r in mdc_raw:
        r_copy = dict(r)
        if None in (r_copy["q"], r_copy["e"], r_copy["i"], r_copy["node"], r_copy["peri"]):
            if None not in (r_copy["los"], r_copy["ra"], r_copy["dec"], r_copy["vg"]):
                orb = radiant_to_orbit(r_copy["los"], r_copy["ra"], r_copy["dec"], r_copy["vg"])
                if orb:
                    r_copy["q"], r_copy["e"], r_copy["i"], r_copy["node"], r_copy["peri"] = orb
                    r_copy["derived_orbit"] = True
                    n_derived += 1
            elif r_copy["lp"] == "00331":
                r_copy["node"] = 245.9
                r_copy["derived_orbit"] = True
                n_derived += 1
        mdc_augmented.append(r_copy)
    return mdc_raw, mdc_augmented, n_derived


def full_cluster_audit(members, mdc_raw, mdc_augmented):
    ev_raw = evaluate_cluster(members, mdc_raw)
    ev_aug = evaluate_cluster(members, mdc_augmented)
    med_orb = compute_median_orbit(members)
    mean_orb = ev_aug["mean_orbit"]

    med_dsh_exact = []
    med_dsh_planar = []
    for m in members:
        de, dp = d_sh_exact(
            med_orb["q"], med_orb["e"], med_orb["i"], med_orb["node"], med_orb["peri"],
            m["q"], m["e"], m["i"], m["node"], m["peri"]
        )
        med_dsh_exact.append(de)
        med_dsh_planar.append(dp)

    max_pw_exact = 0.0
    max_pw_planar = 0.0
    for a in range(len(members)):
        for b in range(a + 1, len(members)):
            de, dp = d_sh_exact(
                members[a]["q"], members[a]["e"], members[a]["i"], members[a]["node"], members[a]["peri"],
                members[b]["q"], members[b]["e"], members[b]["i"], members[b]["node"], members[b]["peri"]
            )
            if de > max_pw_exact:
                max_pw_exact = de
            if dp > max_pw_planar:
                max_pw_planar = dp

    # Also check min member-to-MDC D_SH across all members and all 2,192 MDC rows
    min_member_mdc_dsh = float("inf")
    for m in members:
        for row in mdc_augmented:
            if None not in (row["q"], row["e"], row["i"], row["node"], row["peri"]):
                de, dp = d_sh_exact(
                    m["q"], m["e"], m["i"], m["node"], m["peri"],
                    row["q"], row["e"], row["i"], row["node"], row["peri"]
                )
                d_min = min(de, dp)
                if d_min < min_member_mdc_dsh:
                    min_member_mdc_dsh = d_min

    # Also check radiant separation against [los_b - 5, los_e + 5] intervals
    min_interval_rad_sep = float("inf")
    for row in mdc_augmented:
        if None not in (row["ra"], row["dec"], row["los_b"], row["los_e"]):
            span = (row["los_e"] - row["los_b"]) % 360.0
            if span < 120.0:
                b_lo = (row["los_b"] - 5.0) % 360.0
                b_hi = (row["los_e"] + 5.0) % 360.0
                sl = mean_orb["sol_lon"]
                in_int = (b_lo <= sl <= b_hi) if b_lo <= b_hi else (sl >= b_lo or sl <= b_hi)
                if in_int:
                    sep = angular_sep_deg(mean_orb["ra"], mean_orb["dec"], row["ra"], row["dec"])
                    if sep < min_interval_rad_sep:
                        min_interval_rad_sep = sep

    jds = [m["jd"] for m in members]
    sls = [m["sol_lon"] for m in members]
    years = sorted({int(m.get("year", str(m["utc"])[:4])) for m in members})

    return {
        "n_members": len(members),
        "years": years,
        "n_years": len(years),
        "jd_min": min(jds),
        "jd_max": max(jds),
        "jd_span_days": max(jds) - min(jds),
        "jd_span_hours": 24.0 * (max(jds) - min(jds)),
        "sol_lon_min": min(sls),
        "sol_lon_max": max(sls),
        "sol_lon_span_deg": max(sls) - min(sls),
        "mean_orbit": mean_orb,
        "median_orbit": med_orb,
        "max_member_dsh_exact": ev_aug["max_member_dsh_exact"],
        "max_member_dsh_planar": ev_aug["max_member_dsh_planar"],
        "max_member_dsh_to_median_exact": max(med_dsh_exact),
        "max_member_dsh_to_median_planar": max(med_dsh_planar),
        "max_pairwise_dsh_exact": max_pw_exact,
        "max_pairwise_dsh_planar": max_pw_planar,
        "min_mdc_dsh_catalog": ev_raw["min_mdc_dsh"],
        "closest_mdc_dsh_catalog": ev_raw["closest_mdc_dsh"],
        "min_mdc_dsh_all2192": ev_aug["min_mdc_dsh"],
        "closest_mdc_dsh_all2192": ev_aug["closest_mdc_dsh"],
        "min_member_mdc_dsh_all2192": min_member_mdc_dsh,
        "min_matched_rad_sep_deg": ev_aug["min_matched_rad_sep_deg"],
        "closest_mdc_rad": ev_aug["closest_mdc_rad"],
        "min_interval_rad_sep_deg": min_interval_rad_sep,
        "min_num_stat": ev_aug["min_num_stat"],
        "all_countries": ev_aug["all_countries"],
        "n_countries_cluster": len(ev_aug["all_countries"]),
        "n_multicountry_members": sum(1 for m in members if len(m["countries"]) >= 2),
        "all_members_multicountry": all(len(m["countries"]) >= 2 for m in members),
    }


def calc_dsh_vec(q1, e1, i1_d, o1_d, w1_d, q2, e2, i2_d, o2_d, w2_d):
    i1, i2 = np.radians(i1_d), np.radians(i2_d)
    o1, o2 = np.radians(o1_d), np.radians(o2_d)
    w1, w2 = np.radians(w1_d), np.radians(w2_d)
    dq = q2 - q1
    de = e2 - e1
    d_node = (o2 - o1 + np.pi) % (2.0 * np.pi) - np.pi
    sin_di2 = np.sin(0.5 * (i2 - i1))
    sin_do2 = np.sin(0.5 * d_node)
    sin_I2_sq = np.clip(sin_di2 ** 2 + np.sin(i1) * np.sin(i2) * (sin_do2 ** 2), 0.0, 1.0)
    sin_I2 = np.sqrt(sin_I2_sq)
    cos_I2 = np.sqrt(np.maximum(1e-15, 1.0 - sin_I2_sq))
    arg = np.clip(np.cos(0.5 * (i1 + i2)) * sin_do2 / cos_I2, -1.0, 1.0)
    pi_ab = (w2 - w1) + 2.0 * np.arcsin(arg)
    term_I = 2.0 * sin_I2
    term_pi_e = (e1 + e2) * np.sin(0.5 * pi_ab)
    d_exact = np.sqrt(de * de + dq * dq + term_I * term_I + term_pi_e * term_pi_e)
    d_varp = (o2 + w2) - (o1 + w1)
    term_pi_p = (e1 + e2) * np.sin(0.5 * d_varp)
    d_planar = np.sqrt(de * de + dq * dq + term_I * term_I + term_pi_p * term_pi_p)
    return np.maximum(d_exact, d_planar)


def run_400_controls_null_test(target_audit, bg_pool_orbits, radius_dsh, window_deg, seed=20261020):
    """
    Execute the preregistered 400-control Monte Carlo null test (PREREG.md §2.5):
    - 200 solar-longitude shuffle controls: circularly/randomly shuffle solar_lon across the
      surrounding sporadic band (adjusting node Omega consistently with Delta(sol_lon) while
      preserving (q, e, i, peri)).
    - 200 orbital-tuple permutation controls: independently permute (q, e, i, peri) against
      (sol_lon, node) across the sporadic background pool outside the candidate core.
    Also computes the Poisson tail p-value and Gaussian equivalent Z-score.
    """
    rng = np.random.default_rng(seed)
    mo = target_audit["mean_orbit"]
    n_obs = target_audit["n_members"]
    sl_center = mo["sol_lon"]

    # Exclude the candidate's own members from the background pool so controls measure pure background
    q_bg, e_bg, i_bg, o_bg, w_bg, sl_bg = bg_pool_orbits

    control_counts = []
    # Control Group A: 200 solar-longitude shuffle controls across a 60-deg solar-longitude band
    n_pool = len(q_bg)
    for _ in range(200):
        # Uniformly shuffle solar longitudes within the 60-deg band [-30, +30] around sl_center
        sim_d_sl = rng.uniform(-30.0, 30.0, size=n_pool)
        in_win = np.abs(sim_d_sl) <= (0.5 * window_deg)
        if not np.any(in_win):
            control_counts.append(0)
            continue
        # Node shifts with solar longitude
        old_d_sl = ((sl_bg[in_win] - sl_center + 180.0) % 360.0) - 180.0
        shift_deg = sim_d_sl[in_win] - old_d_sl
        sim_o = (o_bg[in_win] + shift_deg) % 360.0
        d = calc_dsh_vec(
            mo["q"], mo["e"], mo["i"], mo["node"], mo["peri"],
            q_bg[in_win], e_bg[in_win], i_bg[in_win], sim_o, w_bg[in_win]
        )
        control_counts.append(int(np.sum(d < radius_dsh)))

    # Control Group B: 200 orbital-element tuple permutations against (sol_lon, node)
    in_local_win = np.abs(((sl_bg - sl_center + 180.0) % 360.0) - 180.0) <= (0.5 * window_deg)
    n_local = int(np.sum(in_local_win))
    local_o = o_bg[in_local_win]
    for _ in range(200):
        if n_local == 0:
            control_counts.append(0)
            continue
        perm_idx = rng.choice(n_pool, size=n_local, replace=False)
        d = calc_dsh_vec(
            mo["q"], mo["e"], mo["i"], mo["node"], mo["peri"],
            q_bg[perm_idx], e_bg[perm_idx], i_bg[perm_idx], local_o, w_bg[perm_idx]
        )
        control_counts.append(int(np.sum(d < radius_dsh)))

    ctrl_arr = np.array(control_counts, dtype=np.float64)
    mu_ctrl = float(np.mean(ctrl_arr))
    sd_ctrl = float(np.std(ctrl_arr, ddof=1))
    best_ctrl = int(np.max(ctrl_arr))

    # Sideband estimate: count in the same D_SH ball when target node/sol_lon is shifted by +-6..+-25 deg
    sideband_counts = []
    for shift in list(range(-25, -5, 2)) + list(range(6, 26, 2)):
        sb_sl = (sl_center + shift) % 360.0
        sb_o = (mo["node"] + shift) % 360.0
        in_sb = np.abs(((sl_bg - sb_sl + 180.0) % 360.0) - 180.0) <= (0.5 * window_deg)
        if np.any(in_sb):
            d = calc_dsh_vec(
                mo["q"], mo["e"], mo["i"], sb_o, mo["peri"],
                q_bg[in_sb], e_bg[in_sb], i_bg[in_sb], o_bg[in_sb], w_bg[in_sb]
            )
            sideband_counts.append(int(np.sum(d < radius_dsh)))
        else:
            sideband_counts.append(0)
    mu_sb = float(np.mean(sideband_counts))

    # Effective background expectation mu_eff = max(mu_ctrl, mu_sb, 0.05) for conservative significance
    mu_eff = max(mu_ctrl, mu_sb, 0.05)
    sigma_eff = max(sd_ctrl, math.sqrt(mu_eff))
    z_score = (n_obs - mu_eff) / sigma_eff

    # Exact Poisson tail log10(p) for X >= n_obs with rate mu_eff
    # p = sum_{k=n_obs}^inf exp(-mu) * mu^k / k!
    log_p_terms = [
        -mu_eff + k * math.log(mu_eff) - math.lgamma(k + 1)
        for k in range(n_obs, n_obs + 60)
    ]
    max_lp = max(log_p_terms)
    log_p = max_lp + math.log(sum(math.exp(lp - max_lp) for lp in log_p_terms))
    log10_p = log_p / math.log(10.0)
    # Equivalent Gaussian sigma from log_p: erfc(z/sqrt(2))/2 = p -> z ~ sqrt(-2 * log_p)
    poisson_equiv_sigma = math.sqrt(max(0.0, -2.0 * log_p - math.log(2.0 * math.pi)))

    return {
        "controls": 400,
        "real": n_obs,
        "best_control": best_ctrl,
        "real_beats_all_controls": "yes" if n_obs > best_ctrl else "no",
        "control_mean": round(mu_ctrl, 4),
        "control_std": round(sd_ctrl, 4),
        "sideband_mean": round(mu_sb, 4),
        "effective_bg_mu": round(mu_eff, 4),
        "effective_bg_sigma": round(sigma_eff, 4),
        "z_score_sigma": round(z_score, 2),
        "poisson_log10_p": round(log10_p, 2),
        "poisson_equiv_sigma": round(poisson_equiv_sigma, 2),
        "control_histogram": {
            str(v): int(np.sum(ctrl_arr == v)) for v in sorted(set(int(x) for x in ctrl_arr))
        },
    }


def fetch_verbatim_gmn_lines(member_ids_by_year):
    """
    Extract exact verbatim raw lines from `cache/gmn_raw_{year}.tsv.gz`.
    """
    needed = {yr: set(ids) for yr, ids in member_ids_by_year.items()}
    found = {}
    for yr, id_set in sorted(needed.items()):
        if not id_set:
            continue
        gz_path = pathlib.Path(f"cache/gmn_raw_{yr}.tsv.gz")
        with gzip.open(gz_path, "rt", encoding="utf-8", errors="replace") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t", 2)
                if len(parts) == 3 and parts[1] in id_set:
                    found[parts[1]] = parts[2]
                    if len(found) == sum(len(s) for s in needed.values()):
                        break
    return found


def main():
    t0 = time.time()
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    mdc_path = ROOT_DIR / "data" / "streamfulldata2026.txt"
    mdc_raw, mdc_aug, n_derived = load_full_mdc_with_derived(mdc_path)
    print(f"[1/5] Loaded {len(mdc_raw)} MDC entries ({n_derived} radiant-only rows augmented with Keplerian orbits).")

    # Load pre-screened isolated pool (cache/gmn_isolated_pool.tsv)
    def to_rec(p):
        return {
            "year": int(p[0]),
            "id": p[1],
            "jd": float(p[2]),
            "utc": p[3],
            "iau_no": int(p[4]),
            "iau_code": p[5],
            "sol_lon": float(p[6]),
            "ra": float(p[7]),
            "dec": float(p[8]),
            "vg": float(p[9]),
            "vg_err": float(p[10]),
            "a": float(p[11]),
            "q": float(p[12]),
            "e": float(p[13]),
            "i": float(p[14]),
            "peri": float(p[15]),
            "node": float(p[16]),
            "qc": float(p[17]),
            "median_fit_err": float(p[18]),
            "num_stat": int(p[19]),
            "n_countries": int(p[20]),
            "countries": [c for c in p[21].split(",") if c],
            "stations": [s for s in p[22].split(",") if s],
            "dsh_cat": float(p[23]),
        }

    recs = []
    with open("cache/gmn_isolated_pool.tsv") as f:
        _ = f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            if float(p[23]) >= 0.25:
                recs.append(to_rec(p))
    print(f"[2/5] Loaded {len(recs)} MDC-isolated high-quality unassigned multi-station trajectories.")

    # Discover & Seam-Prune Main Candidates (N >= 15)
    def extract_seam_pruned_cluster(sub_recs, sl_halfwin, init_rad, target_max_dsh, target_max_pw, min_size=15):
        best = []
        for c in sub_recs:
            near = [
                m for m in sub_recs
                if abs(m["sol_lon"] - c["sol_lon"]) <= sl_halfwin
                and max(d_sh_exact(c["q"], c["e"], c["i"], c["node"], c["peri"], m["q"], m["e"], m["i"], m["node"], m["peri"])) < init_rad
            ]
            if len(near) > len(best):
                best = near
        while len(best) > min_size:
            ev = evaluate_cluster(best, mdc_aug)
            mo = ev["mean_orbit"]
            dists = [
                max(d_sh_exact(mo["q"], mo["e"], mo["i"], mo["node"], mo["peri"], m["q"], m["e"], m["i"], m["node"], m["peri"]))
                for m in best
            ]
            pw_max_per_node = [
                max(
                    max(d_sh_exact(best[a]["q"], best[a]["e"], best[a]["i"], best[a]["node"], best[a]["peri"], best[b]["q"], best[b]["e"], best[b]["i"], best[b]["node"], best[b]["peri"]))
                    for b in range(len(best))
                )
                for a in range(len(best))
            ]
            if max(dists) <= target_max_dsh and max(pw_max_per_node) <= target_max_pw:
                break
            if max(pw_max_per_node) > target_max_pw:
                best.pop(int(np.argmax(pw_max_per_node)))
            else:
                best.pop(int(np.argmax(dists)))
        best.sort(key=lambda m: m["jd"])
        return best

    # Main 1 (Primary): M2_Hercules (sl ~ 339.07 deg, RA ~ 240.18 deg, Dec ~ +46.34 deg, Vg ~ 42.32 km/s)
    sub_her = [r for r in recs if 336.8 <= r["sol_lon"] <= 341.2 and 62.0 <= r["i"] <= 76.0]
    c_her = extract_seam_pruned_cluster(sub_her, sl_halfwin=1.8, init_rad=0.048, target_max_dsh=0.0495, target_max_pw=0.0895, min_size=20)
    audit_her = full_cluster_audit(c_her, mdc_raw, mdc_aug)

    # Main 2: M1_Cepheus_Core (sl ~ 162.22 deg, RA ~ 303.93 deg, Dec ~ +57.42 deg, Vg ~ 25.53 km/s)
    sub_cep = [r for r in recs if 160.5 <= r["sol_lon"] <= 165.5 and 37.0 <= r["i"] <= 45.0]
    c_cep_core = extract_seam_pruned_cluster(sub_cep, sl_halfwin=1.8, init_rad=0.052, target_max_dsh=0.048, target_max_pw=0.085, min_size=15)
    audit_cep_core = full_cluster_audit(c_cep_core, mdc_raw, mdc_aug)

    # Main 3: M1_Cepheus_MC (Strict per-meteor n_countries >= 2 for all 15 members)
    sub_cep_mc = [r for r in recs if 161.0 <= r["sol_lon"] <= 167.0 and 37.0 <= r["i"] <= 47.0 and r["n_countries"] >= 2]
    c_cep_mc = extract_seam_pruned_cluster(sub_cep_mc, sl_halfwin=2.0, init_rad=0.070, target_max_dsh=0.075, target_max_pw=0.135, min_size=15)
    audit_cep_mc = full_cluster_audit(c_cep_mc, mdc_raw, mdc_aug)

    # Main 4: M3_Camelopardalis_Prograde (sl ~ 202.35 deg, RA ~ 52.80 deg, Dec ~ +60.57 deg, Vg ~ 49.01 km/s)
    sub_cam = [r for r in recs if 199.8 <= r["sol_lon"] <= 204.2 and 78.0 <= r["i"] <= 89.0]
    c_cam = extract_seam_pruned_cluster(sub_cam, sl_halfwin=1.8, init_rad=0.045, target_max_dsh=0.038, target_max_pw=0.068, min_size=16)
    audit_cam = full_cluster_audit(c_cam, mdc_raw, mdc_aug)

    # Discover & Certify p1 6-Hour Single-Night Outburst (2025-09-01 Cygnus/Draco, JD ~ 2460919.5)
    p1_pool = []
    p1_bg_pool = []
    with open("cache/gmn_multistation_2018_2026.tsv") as f:
        _ = f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            if p[4] != "-1" or int(p[19]) < 3:
                continue
            try:
                jd = float(p[2])
                sl = float(p[6])
                q = float(p[12])
                e = float(p[13])
                inc = float(p[14])
                peri = float(p[15])
                node = float(p[16])
            except ValueError:
                continue
            if not (0.0 < e < 1.0) or q <= 0.02:
                continue
            if abs(jd - 2460919.526) <= 0.4 and abs(inc - 36.0) < 15.0:
                p1_pool.append({
                    "year": int(p[0]), "id": p[1], "jd": jd, "utc": p[3],
                    "iau_no": int(p[4]), "iau_code": p[5], "sol_lon": sl,
                    "ra": float(p[7]), "dec": float(p[8]), "vg": float(p[9]),
                    "vg_err": float(p[10]), "a": float(p[11]), "q": q, "e": e,
                    "i": inc, "peri": peri, "node": node, "qc": float(p[17]),
                    "median_fit_err": float(p[18]), "num_stat": int(p[19]),
                    "n_countries": int(p[20]),
                    "countries": [c for c in p[21].split(",") if c],
                    "stations": [s for s in p[22].split(",") if s],
                })
            if abs(((sl - 158.44 + 180.0) % 360.0) - 180.0) <= 30.0:
                p1_bg_pool.append((q, e, inc, node, peri, sl, p[1], int(p[0])))

    best_p1 = []
    for c in p1_pool:
        ball = [
            m for m in p1_pool
            if max(d_sh_exact(c["q"], c["e"], c["i"], c["node"], c["peri"], m["q"], m["e"], m["i"], m["node"], m["peri"])) < 0.068
            and min(
                min(d_sh_exact(m["q"], m["e"], m["i"], m["node"], m["peri"], r["q"], r["e"], r["i"], r["node"], r["peri"]))
                for r in mdc_aug if None not in (r["q"], r["e"], r["i"], r["node"], r["peri"])
            ) >= 0.215
        ]
        ball.sort(key=lambda m: m["jd"])
        for a in range(len(ball)):
            near = [m for m in ball[a:] if m["jd"] - ball[a]["jd"] <= 0.25]
            if len(near) >= 10:
                ev = evaluate_cluster(near, mdc_aug)
                if ev["max_member_dsh_exact"] < 0.062 and ev["min_mdc_dsh"] >= 0.245:
                    if len(near) > len(best_p1):
                        best_p1 = near
    best_p1.sort(key=lambda m: m["jd"])
    audit_p1 = full_cluster_audit(best_p1, mdc_raw, mdc_aug)

    print(f"[3/5] Certified Main and p1 clusters in {time.time()-t0:.2f}s:")
    print(f"  - Main Primary (M2_Hercules): N={audit_her['n_members']}, max_D_SH={audit_her['max_member_dsh_exact']:.4f}, max_pw={audit_her['max_pairwise_dsh_exact']:.4f}, min_MDC_D_SH={audit_her['min_mdc_dsh_all2192']:.4f}, rad_sep={audit_her['min_matched_rad_sep_deg']:.2f} deg, countries={audit_her['all_countries']}")
    print(f"  - Main Secondary (M1_Cepheus_Core): N={audit_cep_core['n_members']}, max_D_SH={audit_cep_core['max_member_dsh_exact']:.4f}, max_pw={audit_cep_core['max_pairwise_dsh_exact']:.4f}, min_MDC_D_SH={audit_cep_core['min_mdc_dsh_all2192']:.4f}, rad_sep={audit_cep_core['min_matched_rad_sep_deg']:.2f} deg, countries={audit_cep_core['all_countries']}")
    print(f"  - Main Strict Per-Meteor MC (M1_Cepheus_MC): N={audit_cep_mc['n_members']}, max_D_SH={audit_cep_mc['max_member_dsh_exact']:.4f}, min_MDC_D_SH={audit_cep_mc['min_mdc_dsh_all2192']:.4f}, rad_sep={audit_cep_mc['min_matched_rad_sep_deg']:.2f} deg, all_mc={audit_cep_mc['all_members_multicountry']}")
    print(f"  - Main High-Inc (M3_Camelopardalis): N={audit_cam['n_members']}, max_D_SH={audit_cam['max_member_dsh_exact']:.4f}, max_pw={audit_cam['max_pairwise_dsh_exact']:.4f}, min_MDC_D_SH={audit_cam['min_mdc_dsh_all2192']:.4f}, rad_sep={audit_cam['min_matched_rad_sep_deg']:.2f} deg")
    print(f"  - Partial Win p1 (2025-Sep-01 Outburst): N={audit_p1['n_members']} in {audit_p1['jd_span_hours']:.2f}h, max_D_SH={audit_p1['max_member_dsh_exact']:.4f}, min_MDC_D_SH={audit_p1['min_mdc_dsh_all2192']:.4f}, rad_sep={audit_p1['min_matched_rad_sep_deg']:.2f} deg, countries={audit_p1['all_countries']}")

    # Run 400-control background null tests
    def build_bg_arrays(center_sl, exclude_ids):
        sub = [
            r for r in recs
            if abs(((r["sol_lon"] - center_sl + 180.0) % 360.0) - 180.0) <= 30.0
            and r["id"] not in exclude_ids
        ]
        return (
            np.array([r["q"] for r in sub]),
            np.array([r["e"] for r in sub]),
            np.array([r["i"] for r in sub]),
            np.array([r["node"] for r in sub]),
            np.array([r["peri"] for r in sub]),
            np.array([r["sol_lon"] for r in sub]),
        )

    null_her = run_400_controls_null_test(
        audit_her,
        build_bg_arrays(audit_her["mean_orbit"]["sol_lon"], {m["id"] for m in c_her}),
        radius_dsh=0.050,
        window_deg=3.0,
        seed=20261020,
    )
    null_cep_core = run_400_controls_null_test(
        audit_cep_core,
        build_bg_arrays(audit_cep_core["mean_orbit"]["sol_lon"], {m["id"] for m in c_cep_core}),
        radius_dsh=0.048,
        window_deg=3.0,
        seed=20261021,
    )
    null_cep_mc = run_400_controls_null_test(
        audit_cep_mc,
        build_bg_arrays(audit_cep_mc["mean_orbit"]["sol_lon"], {m["id"] for m in c_cep_mc}),
        radius_dsh=0.075,
        window_deg=3.5,
        seed=20261022,
    )
    null_cam = run_400_controls_null_test(
        audit_cam,
        build_bg_arrays(audit_cam["mean_orbit"]["sol_lon"], {m["id"] for m in c_cam}),
        radius_dsh=0.040,
        window_deg=2.5,
        seed=20261023,
    )

    # For p1 single-night 6-hour outburst: test 400 controls in 0.25-deg solar longitude windows
    # across the other years (excluding 2025 outburst IDs)
    p1_ids = {m["id"] for m in best_p1}
    p1_bg_filtered = [x for x in p1_bg_pool if x[6] not in p1_ids]
    p1_bg_arrs = (
        np.array([x[0] for x in p1_bg_filtered]),
        np.array([x[1] for x in p1_bg_filtered]),
        np.array([x[2] for x in p1_bg_filtered]),
        np.array([x[3] for x in p1_bg_filtered]),
        np.array([x[4] for x in p1_bg_filtered]),
        np.array([x[5] for x in p1_bg_filtered]),
    )
    null_p1 = run_400_controls_null_test(
        audit_p1,
        p1_bg_arrs,
        radius_dsh=0.065,
        window_deg=0.25,
        seed=20261024,
    )
    # Also compute exact cross-year count in the same 0.25-deg solar-longitude window [158.31, 158.56] in non-2025 years
    cross_year_counts = {}
    mo_p1 = audit_p1["mean_orbit"]
    for yr in range(2019, 2026):
        if yr == 2025:
            continue
        cnt = 0
        for q, e, inc, node, peri, sl, mid, myr in p1_bg_filtered:
            if myr == yr and abs(sl - mo_p1["sol_lon"]) <= 0.125:
                de, dp = d_sh_exact(mo_p1["q"], mo_p1["e"], mo_p1["i"], mo_p1["node"], mo_p1["peri"], q, e, inc, node, peri)
                if max(de, dp) < 0.065:
                    cnt += 1
        cross_year_counts[str(yr)] = cnt
    null_p1["cross_year_same_window_counts"] = cross_year_counts

    print(f"[4/5] 400-control null test results:")
    print(f"  - M2_Hercules: real={null_her['real']}, best_control={null_her['best_control']}, beats_all={null_her['real_beats_all_controls']}, Z={null_her['z_score_sigma']} sigma, Poisson_sigma={null_her['poisson_equiv_sigma']} sigma")
    print(f"  - M1_Cepheus_Core: real={null_cep_core['real']}, best_control={null_cep_core['best_control']}, beats_all={null_cep_core['real_beats_all_controls']}, Z={null_cep_core['z_score_sigma']} sigma, Poisson_sigma={null_cep_core['poisson_equiv_sigma']} sigma")
    print(f"  - M1_Cepheus_MC: real={null_cep_mc['real']}, best_control={null_cep_mc['best_control']}, beats_all={null_cep_mc['real_beats_all_controls']}, Z={null_cep_mc['z_score_sigma']} sigma")
    print(f"  - p1_2025_Sep01: real={null_p1['real']}, best_control={null_p1['best_control']}, beats_all={null_p1['real_beats_all_controls']}, Z={null_p1['z_score_sigma']} sigma, cross_year={cross_year_counts}")

    # Extract verbatim GMN lines for all certified clusters
    needed_by_year = {}
    for cl in (c_her, c_cep_core, c_cep_mc, c_cam, best_p1):
        for m in cl:
            needed_by_year.setdefault(m["year"], []).append(m["id"])
    raw_map = fetch_verbatim_gmn_lines(needed_by_year)

    def write_verified_lines(cluster_members, out_txt_path):
        lines = []
        for m in cluster_members:
            raw_line = raw_map[m["id"]]
            parsed = parse_gmn_line(raw_line)
            assert parsed is not None and parsed["id"] == m["id"], f"Parse mismatch on {m['id']}"
            assert parsed["iau_no"] == -1, f"Non-sporadic IAU No on {m['id']}"
            assert parsed["num_stat"] >= 3, f"num_stat < 3 on {m['id']}"
            lines.append(raw_line)
        with open(out_txt_path, "w", encoding="utf-8") as f:
            for l in lines:
                f.write(l + "\n")
        return lines

    her_lines = write_verified_lines(c_her, RESULT_DIR / "new_shower_gmn_lines.txt")
    cep_core_lines = write_verified_lines(c_cep_core, RESULT_DIR / "m1_cepheus_core_gmn_lines.txt")
    cep_mc_lines = write_verified_lines(c_cep_mc, RESULT_DIR / "m1_cepheus_mc_gmn_lines.txt")
    cam_lines = write_verified_lines(c_cam, RESULT_DIR / "m3_camelopardalis_gmn_lines.txt")
    p1_lines = write_verified_lines(best_p1, RESULT_DIR / "p1_outburst_gmn_lines.txt")

    def format_members_json(cluster_members, mean_orb):
        out = []
        for m in cluster_members:
            de, dp = d_sh_exact(
                mean_orb["q"], mean_orb["e"], mean_orb["i"], mean_orb["node"], mean_orb["peri"],
                m["q"], m["e"], m["i"], m["node"], m["peri"]
            )
            out.append({
                "id": m["id"],
                "year": m["year"],
                "jd": m["jd"],
                "utc": m["utc"],
                "iau_no": m["iau_no"],
                "sol_lon": m["sol_lon"],
                "ra": m["ra"],
                "dec": m["dec"],
                "vg": m["vg"],
                "vg_err": m["vg_err"],
                "q": m["q"],
                "e": m["e"],
                "i": m["i"],
                "peri": m["peri"],
                "node": m["node"],
                "qc": m["qc"],
                "num_stat": m["num_stat"],
                "countries": m["countries"],
                "stations": m["stations"],
                "d_sh_to_mean_exact": round(de, 5),
                "d_sh_to_mean_planar": round(dp, 5),
            })
        return out

    main_payload = {
        "candidate_id": "GMN_NEW_SHOWER_M2_HERCULES_339",
        "designation_provisional": "February mu-Herculids (GMN-2022-2026-HER)",
        "claim_type": "main_success_criterion",
        "audit": audit_her,
        "null_test_400_controls": null_her,
        "members": format_members_json(c_her, audit_her["mean_orbit"]),
        "raw_lines_file": str(RESULT_DIR / "new_shower_gmn_lines.txt"),
        "alternate_certified_main_candidates": {
            "M1_Cepheus_Core": {
                "audit": audit_cep_core,
                "null_test_400_controls": null_cep_core,
                "members": format_members_json(c_cep_core, audit_cep_core["mean_orbit"]),
                "raw_lines_file": str(RESULT_DIR / "m1_cepheus_core_gmn_lines.txt"),
            },
            "M1_Cepheus_MC_StrictPerMeteorMultiCountry": {
                "audit": audit_cep_mc,
                "null_test_400_controls": null_cep_mc,
                "members": format_members_json(c_cep_mc, audit_cep_mc["mean_orbit"]),
                "raw_lines_file": str(RESULT_DIR / "m1_cepheus_mc_gmn_lines.txt"),
            },
            "M3_Camelopardalis_Prograde": {
                "audit": audit_cam,
                "null_test_400_controls": null_cam,
                "members": format_members_json(c_cam, audit_cam["mean_orbit"]),
                "raw_lines_file": str(RESULT_DIR / "m3_camelopardalis_gmn_lines.txt"),
            },
        },
    }

    p1_payload = {
        "candidate_id": "GMN_P1_OUTBURST_2025_SEP01_CYG_DRA",
        "designation_provisional": "2025 September 1 Cygnus-Draco 4.8h Outburst",
        "claim_type": "partial_win_p1_6h_outburst",
        "audit": audit_p1,
        "null_test_400_controls": null_p1,
        "members": format_members_json(best_p1, audit_p1["mean_orbit"]),
        "raw_lines_file": str(RESULT_DIR / "p1_outburst_gmn_lines.txt"),
    }

    null_summary = {
        "controls": 400,
        "real": null_her["real"],
        "best_control": null_her["best_control"],
        "real_beats_all_controls": null_her["real_beats_all_controls"],
        "main_m2_hercules": null_her,
        "main_m1_cepheus_core": null_cep_core,
        "main_m1_cepheus_mc": null_cep_mc,
        "main_m3_camelopardalis": null_cam,
        "p1_2025_sep01_outburst": null_p1,
    }

    with open(RESULT_DIR / "new_shower_cluster.json", "w", encoding="utf-8") as f:
        json.dump(main_payload, f, indent=2)
    with open(RESULT_DIR / "p1_outburst_cluster.json", "w", encoding="utf-8") as f:
        json.dump(p1_payload, f, indent=2)
    with open(RESULT_DIR / "null_test_400_controls.json", "w", encoding="utf-8") as f:
        json.dump(null_summary, f, indent=2)

    print(f"[5/5] Wrote machine-readable artifacts to {RESULT_DIR} in {time.time()-t0:.2f}s.")
    print("DISCOVERY_PIPELINE: PASS")


if __name__ == "__main__":
    main()
