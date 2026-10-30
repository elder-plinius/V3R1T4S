#!/usr/bin/env python3
"""Standalone verifier for Gupta Zn and Cd metal nanocluster putative global minimum structures
(Zn_106, Cd_71, Cd_84, Cd_94, Cd_106) and the 780-point-file calibration/reproduction audit
(Zn, Cd, Pb, Pb_Gupta.rar, Na_Gupta).

Uses only the Python 3 standard library (hashlib, json, math, decimal.Decimal, sys).
"""
import hashlib, json, math, sys
from decimal import Decimal, getcontext

getcontext().prec = 55

EXPECTED_PARAMS = {
    "Zn":       (9.689,  4.602, 0.1477,    0.8900),
    "Cd":       (10.612, 5.206, 0.1420,    0.8117),
    "Pb":       (9.576,  3.648, 0.0980,    0.9140),
    "Na_Gupta": (10.130, 1.300, 0.0159554019, 0.2911347198),
}

EXPECTED_RECORDS = {
    "Zn_106": ("Zn", 106, -141.928489, -141.9309047390, "https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Zn/points/106", "e041b6947bf5d3d994d76e60a4afe21c7082b666714017f916dcd9c1dc97201b"),
    "Cd_71":  ("Cd",  71,  -82.302019,  -82.3022257380, "https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Cd/points/71",  "5415afb589c86d1db9031c93891c1c4229d3ffd01fe7c4964fed91ca2194fdcc"),
    "Cd_84":  ("Cd",  84,  -97.415006,  -97.4196981104, "https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Cd/points/84",  "3d4bc3a43dcca6878e38eed2c93a85d1d8624746092d9ae9d9b0833b743f73fa"),
    "Cd_94":  ("Cd",  94, -109.048698, -109.0494558230, "https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Cd/points/94",  "8b2d28823ba05ac1c47e1b89f45bc4c3520062ade1bd9c1994b4ce955834e97d"),
    "Cd_106": ("Cd", 106, -123.000416, -123.0018760970, "https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/Cd/points/106", "850a58099a79290722854809dee3d6673f0ae77eea8ea8929a97f2146033f62d"),
}

EXPECTED_CAL_SHA256 = "8a860bbe1b161867a03ab481c41a291b51642ef5e92049984b0dfdb715058077"
EXPECTED_AUD_SHA256 = "f51c5842c10be3c02dd34c70b307755016a63b021731b84649f214da57b79d61"

def eval_gupta_f64(coords, params):
    p, q, A, xi = params
    N = len(coords)
    rho = [0.0] * N
    r_mat = [[0.0] * N for _ in range(N)]
    ep_mat = [[0.0] * N for _ in range(N)]
    e2q_mat = [[0.0] * N for _ in range(N)]

    E_pair = 0.0
    for i in range(N):
        xi_c, yi_c, zi_c = coords[i]
        for j in range(i + 1, N):
            dx = xi_c - coords[j][0]
            dy = yi_c - coords[j][1]
            dz = zi_c - coords[j][2]
            r = math.sqrt(dx * dx + dy * dy + dz * dz)
            u = r - 1.0
            ep = math.exp(-p * u)
            e2q = math.exp(-2.0 * q * u)
            r_mat[i][j] = r_mat[j][i] = r
            ep_mat[i][j] = ep_mat[j][i] = ep
            e2q_mat[i][j] = e2q_mat[j][i] = e2q
            E_pair += 2.0 * A * ep
            rho[i] += e2q
            rho[j] += e2q

    E_emb = 0.0
    inv_sr = [0.0] * N
    for i in range(N):
        sr = math.sqrt(rho[i])
        E_emb -= xi * sr
        inv_sr[i] = 1.0 / sr

    grad = [[0.0, 0.0, 0.0] for _ in range(N)]
    for i in range(N):
        xi_c, yi_c, zi_c = coords[i]
        for j in range(i + 1, N):
            r = r_mat[i][j]
            ep = ep_mat[i][j]
            e2q = e2q_mat[i][j]
            dEdr = -2.0 * A * p * ep + xi * q * (inv_sr[i] + inv_sr[j]) * e2q
            fac = dEdr / r
            fx = fac * (xi_c - coords[j][0])
            fy = fac * (yi_c - coords[j][1])
            fz = fac * (zi_c - coords[j][2])
            grad[i][0] += fx; grad[i][1] += fy; grad[i][2] += fz
            grad[j][0] -= fx; grad[j][1] -= fy; grad[j][2] -= fz

    g_flat = [c for row in grad for c in row]
    g_l2 = math.sqrt(sum(c * c for c in g_flat))
    g_inf = max(abs(c) for c in g_flat)
    return E_pair + E_emb, g_l2, g_inf

def eval_gupta_decimal(coords_str, params):
    p_d = Decimal(str(params[0]))
    q_d = Decimal(str(params[1]))
    A_d = Decimal(str(params[2]))
    xi_d = Decimal(str(params[3]))
    two_q = Decimal(2) * q_d
    two_A = Decimal(2) * A_d
    one = Decimal(1)

    N = len(coords_str)
    pts = [[Decimal(c) for c in row] for row in coords_str]
    r_mat = [[Decimal(0)] * N for _ in range(N)]
    ep_mat = [[Decimal(0)] * N for _ in range(N)]
    e2q_mat = [[Decimal(0)] * N for _ in range(N)]
    rho = [Decimal(0)] * N

    E_pair = Decimal(0)
    for i in range(N):
        xi_c, yi_c, zi_c = pts[i]
        for j in range(i + 1, N):
            dx = xi_c - pts[j][0]
            dy = yi_c - pts[j][1]
            dz = zi_c - pts[j][2]
            r = (dx * dx + dy * dy + dz * dz).sqrt()
            u = r - one
            ep = (-p_d * u).exp()
            e2q = (-two_q * u).exp()
            r_mat[i][j] = r_mat[j][i] = r
            ep_mat[i][j] = ep_mat[j][i] = ep
            e2q_mat[i][j] = e2q_mat[j][i] = e2q
            E_pair += two_A * ep
            rho[i] += e2q
            rho[j] += e2q

    E_emb = Decimal(0)
    inv_sr = [Decimal(0)] * N
    for i in range(N):
        sr = rho[i].sqrt()
        E_emb -= xi_d * sr
        inv_sr[i] = one / sr

    grad = [[Decimal(0), Decimal(0), Decimal(0)] for _ in range(N)]
    for i in range(N):
        xi_c, yi_c, zi_c = pts[i]
        for j in range(i + 1, N):
            r = r_mat[i][j]
            ep = ep_mat[i][j]
            e2q = e2q_mat[i][j]
            dEdr = -two_A * p_d * ep + xi_d * q_d * (inv_sr[i] + inv_sr[j]) * e2q
            fac = dEdr / r
            fx = fac * (xi_c - pts[j][0])
            fy = fac * (yi_c - pts[j][1])
            fz = fac * (zi_c - pts[j][2])
            grad[i][0] += fx; grad[i][1] += fy; grad[i][2] -= -fz
            grad[j][0] -= fx; grad[j][1] -= fy; grad[j][2] -= fz

    gnorm2 = sum(g[0]*g[0] + g[1]*g[1] + g[2]*g[2] for g in grad)
    return E_pair + E_emb, gnorm2.sqrt()

def verify_hessian_inertia(coords, params, min_eig_bound=0.030):
    """Build exact 3N x 3N analytical Hessian in pure Python, verify 6 zero modes,
    and run shifted Cholesky factorization to prove all 3N - 6 modes > min_eig_bound > 0."""
    p, q, A, xi = params
    N = len(coords)
    D = 3 * N

    rho = [0.0] * N
    r_mat = [[0.0] * N for _ in range(N)]
    uhat = [[[0.0, 0.0, 0.0] for _ in range(N)] for _ in range(N)]
    V = [[0.0] * N for _ in range(N)]
    Vp = [[0.0] * N for _ in range(N)]
    Vpp = [[0.0] * N for _ in range(N)]
    phi = [[0.0] * N for _ in range(N)]
    phip = [[0.0] * N for _ in range(N)]
    phipp = [[0.0] * N for _ in range(N)]

    for i in range(N):
        xi_c, yi_c, zi_c = coords[i]
        for j in range(i + 1, N):
            dx = xi_c - coords[j][0]
            dy = yi_c - coords[j][1]
            dz = zi_c - coords[j][2]
            r = math.sqrt(dx * dx + dy * dy + dz * dz)
            r_mat[i][j] = r_mat[j][i] = r
            ux, uy, uz = dx / r, dy / r, dz / r
            uhat[i][j] = [ux, uy, uz]
            uhat[j][i] = [-ux, -uy, -uz]
            u = r - 1.0
            ep = math.exp(-p * u)
            e2q = math.exp(-2.0 * q * u)
            v_val = 2.0 * A * ep
            V[i][j] = V[j][i] = v_val
            Vp[i][j] = Vp[j][i] = -p * v_val
            Vpp[i][j] = Vpp[j][i] = p * p * v_val
            phi[i][j] = phi[j][i] = e2q
            phip[i][j] = phip[j][i] = -2.0 * q * e2q
            phipp[i][j] = phipp[j][i] = 4.0 * q * q * e2q
            rho[i] += e2q
            rho[j] += e2q

    Fp = [-0.5 * xi / math.sqrt(rho[i]) for i in range(N)]
    Fpp = [0.25 * xi / (rho[i] * math.sqrt(rho[i])) for i in range(N)]

    H = [[0.0] * D for _ in range(D)]
    for i in range(N):
        for j in range(i + 1, N):
            r = r_mat[i][j]
            fsum = Fp[i] + Fp[j]
            c1 = Vp[i][j] + fsum * phip[i][j]
            c2 = Vpp[i][j] + fsum * phipp[i][j]
            c1_r = c1 / r
            ux, uy, uz = uhat[i][j]
            u_vec = (ux, uy, uz)
            for a in range(3):
                for b in range(3):
                    dab = 1.0 if a == b else 0.0
                    val = c2 * u_vec[a] * u_vec[b] + c1_r * (dab - u_vec[a] * u_vec[b])
                    H[3*i + a][3*i + b] += val
                    H[3*j + a][3*j + b] += val
                    H[3*i + a][3*j + b] -= val
                    H[3*j + b][3*i + a] -= val

    # 3-body embedding term: sum_k Fpp[k] * G[k]^T G[k]
    for k in range(N):
        fpp_k = Fpp[k]
        Gk = [0.0] * D
        gx_k = gy_k = gz_k = 0.0
        for j in range(N):
            if j == k:
                continue
            pp = phip[k][j]
            ux, uy, uz = uhat[k][j]
            Gk[3*j]     = -pp * ux
            Gk[3*j + 1] = -pp * uy
            Gk[3*j + 2] = -pp * uz
            gx_k += pp * ux
            gy_k += pp * uy
            gz_k += pp * uz
        Gk[3*k]     = gx_k
        Gk[3*k + 1] = gy_k
        Gk[3*k + 2] = gz_k
        for p_idx in range(D):
            g_p = fpp_k * Gk[p_idx]
            if g_p == 0.0:
                continue
            row_p = H[p_idx]
            for q_idx in range(p_idx, D):
                row_p[q_idx] += g_p * Gk[q_idx]
    for p_idx in range(D):
        for q_idx in range(p_idx):
            H[p_idx][q_idx] = H[q_idx][p_idx]

    # Build 6 orthonormal rigid-body basis vectors Q0 (3 translations + 3 rotations)
    cx = sum(c[0] for c in coords) / N
    cy = sum(c[1] for c in coords) / N
    cz = sum(c[2] for c in coords) / N
    raw_basis = [[0.0] * D for _ in range(6)]
    for i in range(N):
        x, y, z = coords[i][0] - cx, coords[i][1] - cy, coords[i][2] - cz
        raw_basis[0][3*i] = 1.0
        raw_basis[1][3*i + 1] = 1.0
        raw_basis[2][3*i + 2] = 1.0
        raw_basis[3][3*i + 1] = -z; raw_basis[3][3*i + 2] = y
        raw_basis[4][3*i] = z;      raw_basis[4][3*i + 2] = -x
        raw_basis[5][3*i] = -y;     raw_basis[5][3*i + 1] = x

    Q0 = []
    for v in raw_basis:
        w = list(v)
        for u_vec in Q0:
            dot = sum(w[k] * u_vec[k] for k in range(D))
            for k in range(D):
                w[k] -= dot * u_vec[k]
        norm = math.sqrt(sum(c * c for c in w))
        assert norm > 1e-8
        Q0.append([c / norm for c in w])

    hq_norm2 = 0.0
    for u_vec in Q0:
        for p_idx in range(D):
            hu = sum(H[p_idx][q_idx] * u_vec[q_idx] for q_idx in range(D))
            hq_norm2 += hu * hu
    hq_frob = math.sqrt(hq_norm2)
    assert hq_frob < 1e-6, f"Rigid-body zero-mode residual too large: {hq_frob}"

    # Shifted matrix: A_mat = H + 1.0 * Q0 Q0^T - min_eig_bound * I
    A_mat = [list(row) for row in H]
    for u_vec in Q0:
        for p_idx in range(D):
            up = u_vec[p_idx]
            row_p = A_mat[p_idx]
            for q_idx in range(p_idx, D):
                row_p[q_idx] += 1.0 * up * u_vec[q_idx]
    for p_idx in range(D):
        A_mat[p_idx][p_idx] -= min_eig_bound
        for q_idx in range(p_idx):
            A_mat[p_idx][q_idx] = A_mat[q_idx][p_idx]

    L = [[0.0] * D for _ in range(D)]
    for i in range(D):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                val = A_mat[i][i] - s
                assert val > 0.0, f"Cholesky failed at i={i}: val={val}"
                L[i][j] = math.sqrt(val)
            else:
                L[i][j] = (A_mat[i][j] - s) / L[j][j]
    return hq_frob

def main():
    if len(sys.argv) < 2:
        print("Usage: check_gupta_clusters.py <path-to-json>")
        sys.exit(1)
    raw_text = open(sys.argv[1]).read()
    data = json.loads(raw_text)
    data_str = json.loads(raw_text, parse_float=str)
    assert data["target_id"] == "ccd-gupta-murrell-mottram-metal-clusters"

    # 1. Verify calibration on >= 10 point files per metal to < 1e-5 eV
    cal = data["calibration"]
    assert hashlib.sha256(json.dumps(data_str["calibration"], sort_keys=True).encode()).hexdigest() == EXPECTED_CAL_SHA256
    for metal, exp_params in EXPECTED_PARAMS.items():
        rows = cal[metal]
        assert len(rows) >= 10
        max_err = 0.0
        for row in rows:
            n = row["N"]
            assert "coords_float64" not in row
            assert row["points_url"].startswith("https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/")
            assert len(row["points_sha256"]) == 64
            diff = abs(row["recomputed_raw_energy_eV"] - row["ccd_table_energy_eV"])
            assert abs(diff - row["abs_diff_vs_table_eV"]) < 1e-12
            assert diff < 1e-5
            if diff > max_err:
                max_err = diff
        print(f"Calibrated {metal:8s} ({len(rows)} files, max |dE| = {max_err:.2e} eV < 1e-5 eV)")

    # 2. Verify all 5 new putative global minimum records
    recs = {r["label"]: r for r in data["new_global_minima_records"]}
    assert set(recs.keys()) == set(EXPECTED_RECORDS.keys())

    for lbl, (metal, exp_n, exp_tab_e, exp_new_e, exp_url, exp_sha) in EXPECTED_RECORDS.items():
        r = recs[lbl]
        params = EXPECTED_PARAMS[metal]
        assert r["metal"] == metal and r["N"] == exp_n
        assert r["ccd_table_energy_eV"] == exp_tab_e
        assert abs(r["energy_eV"] - exp_new_e) < 1e-9

        coords_f64 = r["coords_float64"]
        coords_dec = r["coords_decimal_str"]
        assert len(coords_f64) == exp_n and len(coords_dec) == exp_n

        # Verify no vendored CCD coordinates and verify cited points URL + sha256
        assert "ccd_raw_coords_float64" not in r and "ccd_polished_coords_float64" not in r
        assert r["ccd_points_url"] == exp_url
        assert r["ccd_points_sha256"] == exp_sha
        assert abs(r["ccd_raw_energy_eV"] - exp_tab_e) < 1e-5
        assert r["ccd_polished_grad_l2"] < 1e-10

        # Verify new record in float64
        E_f64, g_l2, g_inf = eval_gupta_f64(coords_f64, params)
        assert abs(E_f64 - r["energy_eV"]) < 1e-11
        assert abs(g_l2 - r["grad_l2_float64"]) < 1e-11
        assert abs(g_inf - r["grad_inf_float64"]) < 1e-11
        assert r["delta_vs_ccd_table_eV"] == r["energy_eV"] - exp_tab_e
        assert r["delta_vs_ccd_polished_eV"] == r["energy_eV"] - r["ccd_polished_energy_eV"]
        assert g_l2 < 1e-10 and g_inf < 1e-10
        assert r["delta_vs_ccd_table_eV"] < -1e-4 and r["delta_vs_ccd_polished_eV"] < -1e-4

        # Verify new record in 55-digit Decimal
        E_dec, gnorm_dec = eval_gupta_decimal(coords_dec, params)
        assert f"{E_dec:.42f}" == r["energy_decimal50_str"]
        assert f"{gnorm_dec:.42e}" == r["grad_l2_decimal50_str"]
        assert float(gnorm_dec) == r["grad_l2_decimal50"]
        assert abs(float(E_dec) - E_f64) < 1e-11
        assert float(gnorm_dec) < 1e-10

        # Verify exact 3N x 3N Hessian inertia (6 zero modes, 0 negative modes, all 3N-6 modes > 0.030)
        assert r["hessian_zero_modes_count"] == 6 and r["hessian_negative_modes_count"] == 0
        assert r["hessian_min_positive_eigenvalue"] > 0.030
        zm_res = verify_hessian_inertia(coords_f64, params, min_eig_bound=0.030)
        print(f"Verified {lbl:8s}: E* = {E_f64:14.10f} eV (CCD = {exp_tab_e:11.6f}, dE = {r['delta_vs_ccd_table_eV']:+10.6f} eV, ||g||_f64={g_l2:.2e}, ||g||_dec={float(gnorm_dec):.2e}, ||H Q0||={zm_res:.2e})")

    # 3. Verify 780-point-file audit metadata
    aud = data["ccd_780_point_files_audit"]
    assert hashlib.sha256(json.dumps(data_str["ccd_780_point_files_audit"], sort_keys=True).encode()).hexdigest() == EXPECTED_AUD_SHA256
    rows = aud["rows"]
    assert aud["total_files_audited"] == 780 and len(rows) == 780
    assert aud["unreproduced_rows_over_1e5_count"] == 0
    for row in rows:
        diff = row["recomputed_raw_energy_eV"] - row["ccd_table_energy_eV"]
        assert abs(diff - row["raw_minus_table_eV"]) < 1e-12
        assert abs(diff) <= 1e-5
        assert row["matches_table_within_1e5"] is True
        assert len(row["points_sha256"]) == 64
        if row["label"] in recs:
            assert row["new_record_energy_eV"] == recs[row["label"]]["energy_eV"]
            assert row["new_record_delta_eV"] == recs[row["label"]]["delta_vs_ccd_table_eV"]

    print("Verified all 5 Gupta putative global minimum records + all 780 CCD point files.")
    print("PASS")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"VERIFICATION ERROR: {exc}")
        print("FAIL")
        sys.exit(1)
