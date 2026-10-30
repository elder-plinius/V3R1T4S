#!/usr/bin/env python3
"""Independent verifier for 3D AB off-lattice protein model (arXiv:1903.01456).

Verifies all 4 record-breaking conformations in object/ab_3d_records_F89_2EWH_1CRN_1PCH.json:
- F89  (L=89, D=173): -E* = 87.179252478342 vs Table 10 86.4318 (gain +0.747452, >= 0.5 p1 + Full Win)
- 2EWH (L=98, D=191): -E* = 257.505676299754 vs Table 10 257.0741 (gain +0.431576, Full Win)
- 1CRN (L=46, D=87):  -E* = 95.720529801173 vs Table 10 95.3159 (gain +0.404630, Full Win)
- 1PCH (L=87, D=169): -E* = 166.978883682418 vs Table 10 166.7194 (gain +0.259484, Full Win)
Plus complete reproduction of all 23 published conformations in Tables 11 and 12 of arXiv:1903.01456
and the Table 2 1PCH length discrepancy (L=87, D=169 vs printed L=88, D=171; Partial Win p2).
"""
import json, math, os, sys
from decimal import Decimal, getcontext

getcontext().prec = 55

EXPECTED_SEQS = {
    "F89": (89, 173, 86.4318, "ABBABBABABBABBABABBABABBABBABABBABBABABBABABBABBABABBABABBABBABABBABBABABBABABBABBABABBAB"),
    "2EWH": (98, 191, 257.0741, "AABABAAAAAAABBBAAAAAABAABAABBAABABAAABBBAAAABABAAABABBAAABAAABAAABAABBAABAAAAABAAABABBBABBAAABAABA"),
    "1CRN": (46, 87, 95.3159, "BBAAABAAABBBBBAABAAABABAAAABBBAAAAAAAABAAABBAB"),
    "1PCH": (87, 169, 166.7194, "ABBBAAABBBAAABABAABAAABBABBBBBABAAABBBBABABBAABAAAAAABBABBABABABABBABBAABAABBBAABBAAABA"),
}

def dec_atan(x):
    x = Decimal(x)
    if x == 0:
        return Decimal(0)
    sign = -1 if x < 0 else 1
    x = abs(x)
    inv = False
    if x > 1:
        x = Decimal(1) / x
        inv = True
    halvings = 0
    while x > Decimal("0.1"):
        x = x / (Decimal(1) + (Decimal(1) + x * x).sqrt())
        halvings += 1
    x2 = x * x
    term = x
    total = term
    k = 1
    while True:
        term = -term * x2
        step = term / Decimal(2 * k + 1)
        if abs(step) < Decimal("1e-53"):
            break
        total += step
        k += 1
    res = total * (Decimal(2) ** halvings)
    if inv:
        pi_half = dec_atan(Decimal(1)) * Decimal(2)
        res = pi_half - res
    return res * sign

PI_DEC = dec_atan(Decimal(1)) * Decimal(4)

def dec_sin_cos(rad):
    x = Decimal(rad)
    two_pi = Decimal(2) * PI_DEC
    k_wrap = (x / two_pi).to_integral_value()
    x = x - k_wrap * two_pi
    x2 = x * x
    c_term = Decimal(1)
    c_sum = c_term
    s_term = x
    s_sum = s_term
    k = 1
    while True:
        c_term = -c_term * x2 / Decimal((2 * k - 1) * (2 * k))
        s_term = -s_term * x2 / Decimal((2 * k) * (2 * k + 1))
        c_sum += c_term
        s_sum += s_term
        if abs(c_term) < Decimal("1e-53") and abs(s_term) < Decimal("1e-53"):
            break
        k += 1
    return s_sum, c_sum

def eval_float64(seq, angles_rad):
    L = len(seq)
    n_th = L - 2
    n_be = L - 3
    if len(angles_rad) != n_th + n_be:
        raise ValueError(f"Expected {n_th + n_be} angles, got {len(angles_rad)}")
    th = angles_rad[:n_th]
    be = angles_rad[n_th:]
    coords = [
        (0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (math.cos(th[0]), 1.0 + math.sin(th[0]), 0.0),
    ]
    for m in range(1, n_th):
        xp, yp, zp = coords[-1]
        cb = math.cos(be[m - 1])
        coords.append((
            xp + math.cos(th[m]) * cb,
            yp + math.sin(th[m]) * cb,
            zp + math.sin(be[m - 1]),
        ))
    max_bond_err = max(
        abs(math.sqrt((coords[i][0] - coords[i + 1][0]) ** 2 + (coords[i][1] - coords[i + 1][1]) ** 2 + (coords[i][2] - coords[i + 1][2]) ** 2) - 1.0)
        for i in range(L - 1)
    )
    E_bb = 0.25 * sum(1.0 - math.cos(t) for t in th)
    E_lj = 0.0
    gx = [0.0] * L
    gy = [0.0] * L
    gz = [0.0] * L
    for i in range(L - 2):
        pxi, pyi, pzi = coords[i]
        si = seq[i]
        for j in range(i + 2, L):
            dx = pxi - coords[j][0]
            dy = pyi - coords[j][1]
            dz = pzi - coords[j][2]
            r2 = dx * dx + dy * dy + dz * dz
            inv_r2 = 1.0 / r2
            inv_r6 = inv_r2 * inv_r2 * inv_r2
            inv_r12 = inv_r6 * inv_r6
            sj = seq[j]
            cij = 1.0 if (si == "A" and sj == "A") else (0.5 if (si == "B" and sj == "B") else -0.5)
            E_lj += 4.0 * (inv_r12 - cij * inv_r6)
            coef = 48.0 * inv_r2 * inv_r6 * (0.5 * cij - inv_r6)
            fx, fy, fz = coef * dx, coef * dy, coef * dz
            gx[i] += fx; gy[i] += fy; gz[i] += fz
            gx[j] -= fx; gy[j] -= fy; gz[j] -= fz
    grad = [0.0] * (n_th + n_be)
    sx = sy = sz = 0.0
    for m in range(n_th - 1, 0, -1):
        sx += gx[m + 2]; sy += gy[m + 2]; sz += gz[m + 2]
        ct, st = math.cos(th[m]), math.sin(th[m])
        cb, sb = math.cos(be[m - 1]), math.sin(be[m - 1])
        grad[m] = 0.25 * st + sx * (-st * cb) + sy * (ct * cb)
        grad[n_th + m - 1] = sx * (-ct * sb) + sy * (-st * sb) + sz * cb
    sx += gx[2]; sy += gy[2]
    grad[0] = 0.25 * math.sin(th[0]) + sx * (-math.sin(th[0])) + sy * math.cos(th[0])
    grad_l2 = math.sqrt(sum(g * g for g in grad))
    grad_inf = max(abs(g) for g in grad)
    return E_bb + E_lj, E_bb, E_lj, grad, grad_l2, grad_inf, max_bond_err, coords

def eval_decimal50(seq, angles_rad):
    L = len(seq)
    n_th = L - 2
    th = [Decimal(repr(v)) for v in angles_rad[:n_th]]
    be = [Decimal(repr(v)) for v in angles_rad[n_th:]]
    st0, ct0 = dec_sin_cos(th[0])
    coords = [
        (Decimal(0), Decimal(0), Decimal(0)),
        (Decimal(0), Decimal(1), Decimal(0)),
        (ct0, Decimal(1) + st0, Decimal(0)),
    ]
    E_bb = Decimal("0.25") * (Decimal(1) - ct0)
    for m in range(1, n_th):
        xp, yp, zp = coords[-1]
        stm, ctm = dec_sin_cos(th[m])
        sbm, cbm = dec_sin_cos(be[m - 1])
        coords.append((
            xp + ctm * cbm,
            yp + stm * cbm,
            zp + sbm,
        ))
        E_bb += Decimal("0.25") * (Decimal(1) - ctm)
    E_lj = Decimal(0)
    for i in range(L - 2):
        pxi, pyi, pzi = coords[i]
        si = seq[i]
        for j in range(i + 2, L):
            dx = pxi - coords[j][0]
            dy = pyi - coords[j][1]
            dz = pzi - coords[j][2]
            r2 = dx * dx + dy * dy + dz * dz
            inv_r6 = Decimal(1) / (r2 * r2 * r2)
            inv_r12 = inv_r6 * inv_r6
            sj = seq[j]
            cij = Decimal(1) if (si == "A" and sj == "A") else (Decimal("0.5") if (si == "B" and sj == "B") else Decimal("-0.5"))
            E_lj += Decimal(4) * (inv_r12 - cij * inv_r6)
    return E_bb + E_lj

def main():
    obj_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("object", "ab_3d_records_F89_2EWH_1CRN_1PCH.json")
    with open(obj_path) as f:
        data = json.load(f)

    assert data["target_id"] == "ab-offlattice-protein-3d-best-energies"
    recs = data["records"]
    assert set(recs.keys()) == {"F89", "2EWH", "1CRN", "1PCH"}

    for lbl in ["F89", "2EWH", "1CRN", "1PCH"]:
        exp_L, exp_D, exp_tab10, exp_seq = EXPECTED_SEQS[lbl]
        r = recs[lbl]
        assert r["label"] == lbl and r["L"] == exp_L and r["D"] == exp_D
        assert r["n_theta"] == exp_L - 2 and r["n_beta"] == exp_L - 3
        assert r["sequence"] == exp_seq and len(exp_seq) == exp_L
        assert r["table10_published_negE"] == exp_tab10

        angles_rad = r["angles_rad"]
        E, E_bb, E_lj, grad, grad_l2, grad_inf, max_bond_err, coords = eval_float64(exp_seq, angles_rad)
        negE = -E

        # Exact field consistency checks
        assert r["negE"] == negE, f"{lbl} negE mismatch"
        assert r["E"] == E, f"{lbl} E mismatch"
        assert r["E_bb"] == E_bb, f"{lbl} E_bb mismatch"
        assert r["E_lj"] == E_lj, f"{lbl} E_lj mismatch"
        assert r["gain_over_table10"] == negE - exp_tab10, f"{lbl} gain mismatch"
        assert r["grad_l2_norm"] == grad_l2, f"{lbl} grad_l2 mismatch"
        assert r["grad_inf_norm"] == grad_inf, f"{lbl} grad_inf mismatch"
        assert r["max_bond_length_error"] == max_bond_err, f"{lbl} max_bond_err mismatch"
        assert len(r["angles_deg"]) == exp_D
        for a_r, a_d in zip(angles_rad, r["angles_deg"]):
            assert abs(a_r * (180.0 / math.pi) - a_d) < 1e-11, f"{lbl} deg/rad mismatch"
        stored_coords = r["coordinates_xyz"]
        assert len(stored_coords) == exp_L
        for i in range(exp_L):
            for k in range(3):
                assert stored_coords[i][k] == coords[i][k], f"{lbl} coord mismatch"

        # Bond length, gradient, and 50-digit Decimal checks
        assert max_bond_err < 1e-9, f"{lbl} bond length violation: {max_bond_err}"
        assert grad_l2 < 1e-8 and grad_inf < 1e-8, f"{lbl} gradient norm too large: {grad_l2}"

        E_dec = eval_decimal50(exp_seq, angles_rad)
        negE_dec = -E_dec
        assert abs(float(negE_dec) - negE) < 1e-11, f"{lbl} float64 vs 50-digit Decimal diff"

        # 4th-order Richardson finite-difference gradient check
        h = 1e-4
        num_grad = []
        x_work = list(angles_rad)
        for k in range(exp_D):
            orig = x_work[k]
            x_work[k] = orig + h; Ep1 = eval_float64(exp_seq, x_work)[0]
            x_work[k] = orig - h; Em1 = eval_float64(exp_seq, x_work)[0]
            x_work[k] = orig + 2.0 * h; Ep2 = eval_float64(exp_seq, x_work)[0]
            x_work[k] = orig - 2.0 * h; Em2 = eval_float64(exp_seq, x_work)[0]
            x_work[k] = orig
            num_grad.append((-Ep2 + 8.0 * Ep1 - 8.0 * Em1 + Em2) / (12.0 * h))
        num_grad_l2 = math.sqrt(sum(g * g for g in num_grad))
        assert num_grad_l2 < 1e-7, f"{lbl} numeric grad norm: {num_grad_l2}"

        gain = negE - exp_tab10
        assert gain > 1e-3, f"{lbl} gain {gain} <= 1e-3"
        if lbl == "F89":
            assert gain >= 0.5, f"F89 gain {gain} < 0.5 (p1 threshold)"
        print(f"Verified {lbl:4s} (L={exp_L:2d}, D={exp_D:3d}): -E* = {negE:.12f} (Tab10={exp_tab10:.4f}, gain=+{gain:.6f}, ||g||_2={grad_l2:.2e}, bond_err={max_bond_err:.2e})")

    # Verify all 23 sequences in the embedded reproduction audit
    audit = data["arXiv_1903_01456_reproduction_audit"]
    assert len(audit) == 23
    pch_checked = False
    for row in audit:
        s = row["sequence"]
        deg = row["published_angles_deg"]
        assert len(s) == row["L_actual"] and len(deg) == row["D_actual"]
        assert row["D_actual"] == 2 * row["L_actual"] - 5
        assert row["D_table2_printed"] == 2 * row["L_table2_printed"] - 5
        rad = [v * math.pi / 180.0 for v in deg]
        e_row, _, _, _, gl2, ginf, b_err, _ = eval_float64(s, rad)
        nege_row = -e_row
        assert row["table11_12_recomputed_negE"] == nege_row
        assert row["table11_12_minus_table10"] == nege_row - row["table10_published_negE"]
        assert row["table11_12_grad_l2"] == gl2
        assert row["table11_12_grad_inf"] == ginf
        assert abs(nege_row - row["table10_published_negE"]) < 5e-5
        lbl = row["label"]
        if lbl in recs:
            assert row["improved_negE"] == recs[lbl]["negE"]
            assert row["gain_over_table10"] == recs[lbl]["gain_over_table10"]
            assert row["improved_grad_l2"] == recs[lbl]["grad_l2_norm"]
            assert row["improved_grad_inf"] == recs[lbl]["grad_inf_norm"]
            assert recs[lbl]["table11_12_recomputed_negE"] == nege_row
            assert recs[lbl]["gain_over_table11_12_unrounded"] == recs[lbl]["negE"] - nege_row
        if lbl == "1PCH":
            assert row["L_actual"] == 87 and row["L_table2_printed"] == 88
            assert row["D_actual"] == 169 and len(deg) == 169
            pch_checked = True
    assert pch_checked
    print("Verified all 23 arXiv:1903.01456 Table 11/12 conformations + 1PCH L=87/D=169 discrepancy.")
    print("PASS")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"VERIFICATION ERROR: {exc}")
        print("FAIL")
        sys.exit(1)
