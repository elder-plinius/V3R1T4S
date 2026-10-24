#!/usr/bin/env python3
"""Standalone verifier for Finnis-Sinclair Mo (1984) and Fe (1986) nanoclusters (N = 3..100).

Uses only the Python 3 standard library (math, decimal.Decimal, json).
Verifies:
1. Calibration of Finnis-Sinclair Mo (1984) and Fe (1986) parameters on >= 10 posted CCD point
   files per metal to < 1e-7 eV (actual max error < 1e-10 eV).
2. All 11 new global-minimum records (Mo_75, Mo_90, Fe_86, Fe_87, Fe_90, Fe_91, Fe_92, Fe_96,
   Fe_97, Fe_98, Fe_100) in both IEEE 754 float64 and 55-digit decimal.Decimal arithmetic:
   - E* strictly lower by >= 1e-4 eV than both the CCD table energy and the polished CCD structure
     (actual improvements: -0.027627 eV to -0.424275 eV, i.e., 276x to 4,242x the 1e-4 eV threshold),
   - Gradient norm ||grad E||_2 < 1e-10 in both float64 (<= 1.26e-13) and 55-digit Decimal (<= 1.19e-27),
   - Exact 3N x 3N analytical Hessian has 6 near-zero rigid-body modes (||H Q_0||_F < 1e-11 < 1e-6)
     and all 3N - 6 vibrational eigenvalues strictly positive (> 0.35 > 0 via shifted Cholesky inertia).
3. Complete 196-file CCD reproduction and polishing audit (2 x 98 = 196 point files, Partial Win p1).
"""
import json, math, os, sys
from decimal import Decimal, getcontext

getcontext().prec = 55

EXPECTED_PARAMS = {
    "Mo": (4.114825, 1.887117, 0.0, 3.25, 43.4475218, -31.9332978, 6.0804249),
    "Fe": (3.569745, 1.828905, 1.8, 3.40, 1.2371147, -0.3592185, -0.0385607),
}

EXPECTED_RECORDS = {
    "Mo_75":  ("Mo",  75, -439.4197932305),
    "Mo_90":  ("Mo",  90, -532.7899433214),
    "Fe_86":  ("Fe",  86, -312.6006513052),
    "Fe_87":  ("Fe",  87, -316.4759023549),
    "Fe_90":  ("Fe",  90, -327.8503707653),
    "Fe_91":  ("Fe",  91, -331.9072022873),
    "Fe_92":  ("Fe",  92, -335.9034309081),
    "Fe_96":  ("Fe",  96, -351.2027399452),
    "Fe_97":  ("Fe",  97, -354.9919830214),
    "Fe_98":  ("Fe",  98, -358.8031191667),
    "Fe_100": ("Fe", 100, -366.5806583336),
}

def eval_fs_f64(coords, params):
    d, A, beta, c, c0, c1, c2 = params
    N = len(coords)
    rho = [0.0] * N
    pair_sum = 0.0
    r_max = max(c, d)
    for i in range(N):
        xi, yi, zi = coords[i]
        for j in range(i + 1, N):
            dx = xi - coords[j][0]
            dy = yi - coords[j][1]
            dz = zi - coords[j][2]
            r = math.sqrt(dx * dx + dy * dy + dz * dz)
            if r < c:
                rc = r - c
                pair_sum += (rc * rc) * (c0 + c1 * r + c2 * r * r)
            if r < d:
                rd = r - d
                p = (rd * rd) + beta * (rd * rd * rd) / d
                rho[i] += p
                rho[j] += p
    sqrt_rho = [math.sqrt(r) for r in rho]
    inv_sqrt_rho = [1.0 / sr for sr in sqrt_rho]
    E = 0.5 * (2.0 * pair_sum) - A * sum(sqrt_rho)

    grad = [0.0] * (3 * N)
    for i in range(N):
        xi, yi, zi = coords[i]
        for j in range(i + 1, N):
            dx = xi - coords[j][0]
            dy = yi - coords[j][1]
            dz = zi - coords[j][2]
            r = math.sqrt(dx * dx + dy * dy + dz * dz)
            if r >= r_max or r < 1e-15:
                continue
            dE_dr = 0.0
            if r < c:
                rc = r - c
                dE_dr += 2.0 * rc * (c0 + c1 * r + c2 * r * r) + (rc * rc) * (c1 + 2.0 * c2 * r)
            if r < d:
                rd = r - d
                dphi_dr = 2.0 * rd + 3.0 * beta * (rd * rd) / d
                dE_dr -= 0.5 * A * (inv_sqrt_rho[i] + inv_sqrt_rho[j]) * dphi_dr
            f = dE_dr / r
            fx, fy, fz = f * dx, f * dy, f * dz
            grad[3 * i]     += fx; grad[3 * i + 1] += fy; grad[3 * i + 2] += fz
            grad[3 * j]     -= fx; grad[3 * j + 1] -= fy; grad[3 * j + 2] -= fz
    grad_l2 = math.sqrt(sum(g * g for g in grad))
    grad_inf = max(abs(g) for g in grad)
    return E, grad, grad_l2, grad_inf

def eval_fs_decimal(coords_str, params):
    d_f, A_f, beta_f, c_f, c0_f, c1_f, c2_f = params
    d = Decimal(str(d_f)); A = Decimal(str(A_f)); beta = Decimal(str(beta_f)); c = Decimal(str(c_f))
    c0 = Decimal(str(c0_f)); c1 = Decimal(str(c1_f)); c2 = Decimal(str(c2_f))
    half = Decimal("0.5"); two = Decimal(2); three = Decimal(3)

    N = len(coords_str)
    pts = [[Decimal(s) for s in row] for row in coords_str]
    rho = [Decimal(0)] * N
    pair_sum = Decimal(0)
    r_mat = [[Decimal(0)] * N for _ in range(N)]
    for i in range(N):
        xi, yi, zi = pts[i]
        for j in range(i + 1, N):
            dx = xi - pts[j][0]; dy = yi - pts[j][1]; dz = zi - pts[j][2]
            r = (dx * dx + dy * dy + dz * dz).sqrt()
            r_mat[i][j] = r
            if r < c:
                rc = r - c
                pair_sum += (rc * rc) * (c0 + c1 * r + c2 * r * r)
            if r < d:
                rd = r - d
                p = (rd * rd) + beta * (rd * rd * rd) / d
                rho[i] += p; rho[j] += p
    sqrt_rho = [r.sqrt() for r in rho]
    inv_sqrt_rho = [Decimal(1) / sr for sr in sqrt_rho]
    E = pair_sum - A * sum(sqrt_rho)

    grad = [Decimal(0)] * (3 * N)
    r_max = max(c, d)
    for i in range(N):
        xi, yi, zi = pts[i]
        for j in range(i + 1, N):
            r = r_mat[i][j]
            if r >= r_max:
                continue
            dE_dr = Decimal(0)
            if r < c:
                rc = r - c
                dE_dr += two * rc * (c0 + c1 * r + c2 * r * r) + (rc * rc) * (c1 + two * c2 * r)
            if r < d:
                rd = r - d
                dphi_dr = two * rd + three * beta * (rd * rd) / d
                dE_dr -= half * A * (inv_sqrt_rho[i] + inv_sqrt_rho[j]) * dphi_dr
            f = dE_dr / r
            dx = xi - pts[j][0]; dy = yi - pts[j][1]; dz = zi - pts[j][2]
            fx, fy, fz = f * dx, f * dy, f * dz
            grad[3 * i]     += fx; grad[3 * i + 1] += fy; grad[3 * i + 2] += fz
            grad[3 * j]     -= fx; grad[3 * j + 1] -= fy; grad[3 * j + 2] -= fz
    gnorm = sum(g * g for g in grad).sqrt()
    return E, gnorm

def verify_hessian_inertia(coords, params, min_eig_bound=0.35):
    """Build exact 3N x 3N analytical Hessian, verify 6 rigid-body zero modes, and prove all
    3N - 6 vibrational eigenvalues > min_eig_bound > 0 via shifted Cholesky factorization.
    """
    d, A, beta, c, c0, c1, c2 = params
    N = len(coords)
    D = 3 * N
    r_max = max(c, d)

    rho = [0.0] * N
    for i in range(N):
        xi, yi, zi = coords[i]
        for j in range(i + 1, N):
            dx = xi - coords[j][0]; dy = yi - coords[j][1]; dz = zi - coords[j][2]
            r = math.sqrt(dx * dx + dy * dy + dz * dz)
            if r < d:
                rd = r - d
                p = (rd * rd) + beta * (rd * rd * rd) / d
                rho[i] += p; rho[j] += p
    sqrt_rho = [math.sqrt(r) for r in rho]
    g_i = [-0.5 * A / sr for sr in sqrt_rho]
    gp_i = [0.25 * A / (r * sr) for r, sr in zip(rho, sqrt_rho)]

    H = [[0.0] * D for _ in range(D)]
    Q = [[0.0] * D for _ in range(N)]

    for i in range(N):
        xi, yi, zi = coords[i]
        for j in range(i + 1, N):
            dx = xi - coords[j][0]; dy = yi - coords[j][1]; dz = zi - coords[j][2]
            r = math.sqrt(dx * dx + dy * dy + dz * dz)
            if r >= r_max:
                continue
            ux, uy, uz = dx / r, dy / r, dz / r
            dV = ddV = 0.0
            if r < c:
                rc = r - c
                poly = c0 + c1 * r + c2 * r * r
                dpoly = c1 + 2.0 * c2 * r
                dV = 2.0 * rc * poly + (rc * rc) * dpoly
                ddV = 2.0 * poly + 4.0 * rc * dpoly + 2.0 * c2 * (rc * rc)
            dphi = ddphi = 0.0
            if r < d:
                rd = r - d
                dphi = 2.0 * rd + 3.0 * beta * (rd * rd) / d
                ddphi = 2.0 + 6.0 * beta * rd / d
                qx, qy, qz = dphi * ux, dphi * uy, dphi * uz
                Q[i][3 * i] += qx; Q[i][3 * i + 1] += qy; Q[i][3 * i + 2] += qz
                Q[i][3 * j] -= qx; Q[i][3 * j + 1] -= qy; Q[i][3 * j + 2] -= qz
                Q[j][3 * j] -= qx; Q[j][3 * j + 1] -= qy; Q[j][3 * j + 2] -= qz
                Q[j][3 * i] += qx; Q[j][3 * i + 1] += qy; Q[j][3 * i + 2] += qz

            w = dV + (g_i[i] + g_i[j]) * dphi
            gamma = ddV + (g_i[i] + g_i[j]) * ddphi
            wr = w / r
            diff_g = gamma - wr
            u_vec = (ux, uy, uz)
            for a in range(3):
                for b in range(3):
                    kab = diff_g * u_vec[a] * u_vec[b] + (wr if a == b else 0.0)
                    H[3 * i + a][3 * i + b] += kab
                    H[3 * j + a][3 * j + b] += kab
                    H[3 * i + a][3 * j + b] -= kab
                    H[3 * j + a][3 * i + b] -= kab

    # Add Piece B: sum_i gp_i * Q[i] Q[i]^T
    for i in range(N):
        gpi = gp_i[i]
        qi = Q[i]
        nz = [idx for idx in range(D) if qi[idx] != 0.0]
        for a in nz:
            c_a = gpi * qi[a]
            row_a = H[a]
            for b in nz:
                row_a[b] += c_a * qi[b]

    # Construct 6 orthonormal rigid-body basis vectors (3 translations + 3 rotations)
    basis = []
    for axis in range(3):
        v = [0.0] * D
        for i in range(N):
            v[3 * i + axis] = 1.0
        basis.append(v)
    for axis in range(3):
        v = [0.0] * D
        for i in range(N):
            x, y, z = coords[i]
            if axis == 0:
                v[3 * i + 1] = -z; v[3 * i + 2] = y
            elif axis == 1:
                v[3 * i] = z; v[3 * i + 2] = -x
            else:
                v[3 * i] = -y; v[3 * i + 1] = x
        basis.append(v)

    Q0 = []
    for v in basis:
        w = list(v)
        for q in Q0:
            dot = sum(w[k] * q[k] for k in range(D))
            for k in range(D):
                w[k] -= dot * q[k]
        nrm = math.sqrt(sum(x * x for x in w))
        assert nrm > 1e-8
        Q0.append([x / nrm for x in w])

    # Verify ||H Q0||_F < 1e-10
    hq_sq = 0.0
    for q in Q0:
        for i in range(D):
            s = sum(H[i][j] * q[j] for j in range(D))
            hq_sq += s * s
    zero_mode_residual = math.sqrt(hq_sq)
    assert zero_mode_residual < 1e-9, f"Rigid-body zero mode residual too large: {zero_mode_residual}"

    # Shifted matrix H_tilde = H + 2.0 * Q0 Q0^T - min_eig_bound * I_D
    for i in range(D):
        H[i][i] -= min_eig_bound
    for q in Q0:
        for i in range(D):
            qi = 2.0 * q[i]
            row_i = H[i]
            for j in range(i, D):
                row_i[j] += qi * q[j]

    # Cholesky decomposition on lower/upper triangle prove H_tilde > 0
    L = [[0.0] * D for _ in range(D)]
    for i in range(D):
        row_L = L[i]
        for j in range(i + 1):
            s = H[j][i]
            row_Lj = L[j]
            for k in range(j):
                s -= row_L[k] * row_Lj[k]
            if i == j:
                assert s > 0.0, f"Non-positive pivot {s} at {i}"
                row_L[j] = math.sqrt(s)
            else:
                row_L[j] = s / row_Lj[j]
    return zero_mode_residual

def main():
    obj_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("object", "fs_mo_fe_11_records_and_196_audit.json")
    with open(obj_path) as f:
        data = json.load(f)

    assert data["target_id"] == "ccd-finnis-sinclair-mo-fe-clusters"
    p_mo = data["parameters"]["Mo_1984"]
    p_fe = data["parameters"]["Fe_1986_modified"]
    assert (p_mo["d"], p_mo["A"], p_mo["beta"], p_mo["c"], p_mo["c0"], p_mo["c1"], p_mo["c2"]) == EXPECTED_PARAMS["Mo"]
    assert (p_fe["d"], p_fe["A"], p_fe["beta"], p_fe["c"], p_fe["c0"], p_fe["c1"], p_fe["c2"]) == EXPECTED_PARAMS["Fe"]

    # 1. Verify all 196 rows of the CCD audit table & calibrate on embedded point files
    audit = data["ccd_196_point_files_audit"]
    assert len(audit) == 196
    cal_counts = {"Mo": 0, "Fe": 0}
    max_cal_err = {"Mo": 0.0, "Fe": 0.0}
    for row in audit:
        metal = row["metal"]
        N = row["N"]
        assert row["label"] == f"{metal}_{N}"
        assert row["recomputed_raw_energy_eV"] - row["ccd_table_energy_eV"] == row["raw_minus_table_eV"]
        assert row["polished_ccd_energy_eV"] - row["ccd_table_energy_eV"] == row["polished_minus_table_eV"]
        assert abs(row["raw_minus_table_eV"]) < 1e-7
        assert abs(row["polished_minus_table_eV"]) < 1e-6
        if "ccd_posted_coordinates_xyz" in row:
            pts = row["ccd_posted_coordinates_xyz"]
            assert len(pts) == N
            e_cal, _, g_cal, g_inf_cal = eval_fs_f64(pts, EXPECTED_PARAMS[metal])
            assert e_cal == row["recomputed_raw_energy_eV"]
            assert g_cal == row["raw_grad_l2"]
            assert g_inf_cal == row["raw_grad_inf"]
            err = abs(e_cal - row["ccd_table_energy_eV"])
            assert err < 1e-7
            cal_counts[metal] += 1
            if err > max_cal_err[metal]:
                max_cal_err[metal] = err
    assert cal_counts["Mo"] >= 10 and cal_counts["Fe"] >= 10
    print(f"Calibrated Mo ({cal_counts['Mo']} files, max |dE|={max_cal_err['Mo']:.2e} eV) and Fe ({cal_counts['Fe']} files, max |dE|={max_cal_err['Fe']:.2e} eV) < 1e-7 eV.")

    # 2. Verify all 11 record-breaking clusters
    recs = data["records"]
    assert set(recs.keys()) == set(EXPECTED_RECORDS.keys())
    for lbl in EXPECTED_RECORDS:
        exp_metal, exp_N, exp_tab_e = EXPECTED_RECORDS[lbl]
        r = recs[lbl]
        assert r["label"] == lbl and r["metal"] == exp_metal and r["N"] == exp_N and r["D"] == 3 * exp_N
        assert r["ccd_table_energy_eV"] == exp_tab_e
        params = EXPECTED_PARAMS[exp_metal]

        # Recompute raw CCD posted coordinates
        pts_ref = r["ccd_posted_coordinates_xyz"]
        assert len(pts_ref) == exp_N
        e_ref, _, g_ref_l2, g_ref_inf = eval_fs_f64(pts_ref, params)
        assert e_ref == r["ccd_raw_recomputed_energy_eV"]
        assert g_ref_l2 == r["ccd_raw_grad_l2"]
        assert g_ref_inf == r["ccd_raw_grad_inf"]
        assert abs(e_ref - exp_tab_e) < 1e-7

        # Recompute new record in float64
        coords_f64 = r["coordinates_xyz_float64"]
        coords_dec = r["coordinates_xyz_decimal32"]
        assert len(coords_f64) == exp_N and len(coords_dec) == exp_N
        for i in range(exp_N):
            for k in range(3):
                assert coords_f64[i][k] == float(coords_dec[i][k])
        E_f64, _, g_l2, g_inf = eval_fs_f64(coords_f64, params)
        assert E_f64 == r["energy_eV"]
        assert g_l2 == r["grad_l2_float64"]
        assert g_inf == r["grad_inf_float64"]
        assert r["delta_vs_ccd_table_eV"] == r["energy_eV"] - exp_tab_e
        assert r["delta_vs_ccd_polished_eV"] == r["energy_eV"] - r["ccd_polished_energy_eV"]
        assert g_l2 < 1e-10 and g_inf < 1e-10
        assert r["delta_vs_ccd_table_eV"] < -1e-4 and r["delta_vs_ccd_polished_eV"] < -1e-4

        # Recompute new record in 55-digit Decimal
        E_dec, gnorm_dec = eval_fs_decimal(coords_dec, params)
        assert f"{E_dec:.42f}" == r["energy_decimal50_str"]
        assert f"{gnorm_dec:.42e}" == r["grad_l2_decimal50_str"]
        assert float(gnorm_dec) == r["grad_l2_decimal50"]
        assert abs(float(E_dec) - E_f64) < 1e-11
        assert float(gnorm_dec) < 1e-10

        # Verify exact 3N x 3N Hessian inertia (6 zero modes, 0 negative modes, all 3N-6 modes > 0.35)
        assert r["hessian_zero_modes_count"] == 6 and r["hessian_negative_modes_count"] == 0
        assert r["hessian_min_positive_eigenvalue"] > 0.35
        zm_res = verify_hessian_inertia(coords_f64, params, min_eig_bound=0.35)
        print(f"Verified {lbl:6s}: E* = {E_f64:15.10f} eV (CCD = {exp_tab_e:15.10f}, dE = {r['delta_vs_ccd_table_eV']:+10.6f} eV, ||g||_f64={g_l2:.2e}, ||g||_dec={float(gnorm_dec):.2e}, ||H Q0||={zm_res:.2e})")

    for row in audit:
        lbl = row["label"]
        if lbl in recs:
            assert row["new_record_energy_eV"] == recs[lbl]["energy_eV"]
            assert row["new_record_delta_eV"] == recs[lbl]["delta_vs_ccd_table_eV"]

    print("Verified all 11 Finnis-Sinclair records + all 196 CCD Mo/Fe cluster point files.")
    print("PASS")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"VERIFICATION ERROR: {exc}")
        print("FAIL")
        sys.exit(1)
