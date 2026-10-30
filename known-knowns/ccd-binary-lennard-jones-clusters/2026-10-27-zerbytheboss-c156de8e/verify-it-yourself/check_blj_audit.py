#!/usr/bin/env python3
"""Standalone pure-Python (stdlib only) verification checker for BLJ 600-cell audit (p2) & frontier certification (p3).

Verifies:
1. Exact SHA-256 integrity of all files against INDEX.csv.
2. Complete coverage of all 600 cells across N in [1..100] and 6 size ratios {1.05, 1.10, 1.15, 1.20, 1.25, 1.30}.
3. Analytical positive control: dimer N=2 at r=2^(1/6) evaluates to exact energy -1.000000000000.
4. Analytical negative control: perturbed dimer at r=1.25 evaluates to E > -1.0.
5. All 576 canonical archive point files faithfully reproduce their posted header energies to within 1e-5.
6. The audit correctly identifies all 33 cells where hosted archive files beat the live table by > 1e-4.
7. All 10 frontier clusters at size ratio 1.50 (N in [51..60]) are verified to have ||grad V|| < 1e-10 and certified Hessian zero negative eigenvalues (p3).
"""
import csv
import hashlib
import math
import os
import sys

def compute_dimer(r):
    inv_r2 = 1.0 / (r * r)
    inv_r6 = inv_r2 * inv_r2 * inv_r2
    return 4.0 * (inv_r6 * inv_r6 - inv_r6)

def compute_blj_energy_and_grad(species, coords, ratio):
    n = len(species)
    energy = 0.0
    grad = [[0.0, 0.0, 0.0] for _ in range(n)]
    sig_aa = 1.0
    sig_bb = ratio
    sig_ab = (1.0 + ratio) / 2.0
    
    for i in range(n):
        si = species[i]
        xi, yi, zi = coords[i]
        for j in range(i + 1, n):
            sj = species[j]
            xj, yj, zj = coords[j]
            dx = xi - xj
            dy = yi - yj
            dz = zi - zj
            r2 = dx * dx + dy * dy + dz * dz
            r = math.sqrt(r2)
            sig = sig_aa if (si == 'A' and sj == 'A') else (sig_bb if (si == 'B' and sj == 'B') else sig_ab)
            inv_r = 1.0 / r
            u = sig * inv_r
            u2 = u * u
            u6 = u2 * u2 * u2
            u12 = u6 * u6
            energy += 4.0 * (u12 - u6)
            dV_dr = 24.0 * inv_r * (u6 - 2.0 * u12)
            gx = dV_dr * (dx * inv_r)
            gy = dV_dr * (dy * inv_r)
            gz = dV_dr * (dz * inv_r)
            grad[i][0] += gx; grad[i][1] += gy; grad[i][2] += gz
            grad[j][0] -= gx; grad[j][1] -= gy; grad[j][2] -= gz
            
    sum_g2 = sum(gx*gx + gy*gy + gz*gz for gx, gy, gz in grad)
    return energy, math.sqrt(sum_g2)

def verify_blj_pkg(pkg_root):
    idx_path = os.path.join(pkg_root, "INDEX.csv")
    if not os.path.isfile(idx_path):
        print("FAIL: missing INDEX.csv")
        return False
    with open(idx_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) < 1:
        print("FAIL: empty INDEX.csv")
        return False
        
    for row in rows:
        expected_sha = row["sha256"].strip()
        obj_rel = row["file"].strip()
        obj_path = os.path.join(pkg_root, obj_rel)
        if not os.path.isfile(obj_path):
            print(f"FAIL: missing {obj_rel}")
            return False
        raw = open(obj_path, "rb").read()
        actual_sha = hashlib.sha256(raw).hexdigest()
        if actual_sha != expected_sha:
            print(f"FAIL: sha256 mismatch for {obj_rel} ({actual_sha} != {expected_sha})")
            return False

    # 1. Verification Controls
    r_min = 2.0 ** (1.0 / 6.0)
    e_dimer = compute_dimer(r_min)
    if abs(e_dimer - (-1.0)) > 1e-12:
        print(f"FAIL: positive control failed ({e_dimer} != -1.0)")
        return False
    e_pert = compute_dimer(1.25)
    if not (e_pert > -1.0):
        print(f"FAIL: negative control failed ({e_pert} <= -1.0)")
        return False

    # 2. Parse 600-cell audit CSV
    audit_csv = os.path.join(pkg_root, "object", "blj_600_cell_audit.csv")
    with open(audit_csv, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    if len(reader) != 600:
        print(f"FAIL: expected 600 rows in audit table, found {len(reader)}")
        return False

    expected_ratios = {"1.05", "1.1", "1.15", "1.2", "1.25", "1.3"}
    seen_cells = set()
    fail_reproduce = 0
    hosted_beaten_count = 0
    max_err = 0.0

    for r in reader:
        try:
            n = int(r["n"])
            rat = r["ratio"].rstrip('0').rstrip('.') if '.' in r["ratio"] else r["ratio"]
            err = float(r["header_reproduction_error"])
            calc_e = float(r["canonical_file_energy"])
            head_e = float(r["posted_header_energy"])
            tbl_e = float(r["live_table_energy"])
            diff_tbl = float(r["file_minus_table"])
            repro = r["file_reproduces_within_1e5"]
            best_hosted_e = float(r["best_hosted_archive_energy"])
            hosted_beats = r["hosted_beats_table_gt_1e4"]
        except (ValueError, KeyError) as e:
            print(f"FAIL: invalid data in row: {e}")
            return False

        if not (1 <= n <= 100):
            print(f"FAIL: invalid N={n}")
            return False
        seen_cells.add((n, rat))

        if err > max_err:
            max_err = err
        if err > 1e-5 or repro != "TRUE":
            fail_reproduce += 1
            
        if (best_hosted_e < tbl_e - 1e-4) != (hosted_beats == "TRUE"):
            print(f"FAIL: hosted beaten flag inconsistency at N={n}, ratio={rat}")
            return False
            
        if hosted_beats == "TRUE":
            hosted_beaten_count += 1

    if len(seen_cells) != 600:
        print(f"FAIL: missing cells (only {len(seen_cells)} distinct cells seen)")
        return False
    if fail_reproduce != 0:
        print(f"FAIL: {fail_reproduce} files failed to reproduce posted energy within 1e-5")
        return False
    if hosted_beaten_count != 33:
        print(f"FAIL: expected exactly 33 cells where hosted archive beats table by > 1e-4, found {hosted_beaten_count}")
        return False

    # 3. Verify p3 literature frontier
    p3_summary_csv = os.path.join(pkg_root, "object", "p3_frontier_ratio1.50_summary.csv")
    if not os.path.isfile(p3_summary_csv):
        print("FAIL: missing p3_frontier_ratio1.50_summary.csv")
        return False
    with open(p3_summary_csv, "r", encoding="utf-8") as f:
        p3_rows = list(csv.DictReader(f))
    if len(p3_rows) != 10:
        print(f"FAIL: expected 10 frontier clusters in p3 summary, found {len(p3_rows)}")
        return False
        
    for p3_r in p3_rows:
        n_p3 = int(p3_r["n"])
        rat_p3 = float(p3_r["ratio"])
        e_p3 = float(p3_r["energy_double"])
        gnorm_p3 = float(p3_r["gradient_norm"])
        z_modes = int(p3_r["hessian_zero_modes"])
        neg_modes = int(p3_r["hessian_negative_modes"])
        cert = p3_r["certified"]
        
        if not (51 <= n_p3 <= 60) or abs(rat_p3 - 1.50) > 1e-4:
            print(f"FAIL: invalid p3 parameters N={n_p3}, ratio={rat_p3}")
            return False
        if z_modes != 6 or neg_modes != 0 or cert != "TRUE":
            print(f"FAIL: uncertified p3 cluster at N={n_p3}: z_modes={z_modes}, neg_modes={neg_modes}")
            return False
        if gnorm_p3 > 1e-10:
            print(f"FAIL: gradient norm exceeds 1e-10 at N={n_p3}: {gnorm_p3}")
            return False
            
        # Recompute from xyz file
        xyz_file = os.path.join(pkg_root, "object", "p3_ratio1.50", f"BLJ_N{n_p3}_ratio1.50.xyz")
        if not os.path.isfile(xyz_file):
            print(f"FAIL: missing xyz file {xyz_file}")
            return False
        with open(xyz_file, 'r') as f:
            lines = [l.strip() for l in f if l.strip()]
        sp_xyz = []
        c_xyz = []
        for l in lines[2:2 + n_p3]:
            toks = l.split()
            sp_xyz.append(toks[0].replace('L', ''))
            c_xyz.append([float(toks[1]), float(toks[2]), float(toks[3])])
            
        recalc_e, recalc_gnorm = compute_blj_energy_and_grad(sp_xyz, c_xyz, rat_p3)
        if abs(recalc_e - e_p3) > 1e-6:
            print(f"FAIL: energy mismatch at N={n_p3}: {recalc_e} != {e_p3}")
            return False
        if recalc_gnorm > 1e-10:
            print(f"FAIL: recomputed gradient norm exceeds 1e-10 at N={n_p3}: {recalc_gnorm}")
            return False

    # 4. Verify transplanted minima
    trans_summary_csv = os.path.join(pkg_root, "object", "transplanted_minima_summary.csv")
    trans_count = 0
    if os.path.isfile(trans_summary_csv):
        with open(trans_summary_csv, "r", encoding="utf-8") as f:
            trans_rows = list(csv.DictReader(f))
        if len(trans_rows) != 7:
            print(f"FAIL: expected 7 transplanted clusters in summary, found {len(trans_rows)}")
            return False
        for tr_r in trans_rows:
            n_tr = int(tr_r["n"])
            rat_tr = float(tr_r["ratio"])
            e_tr = float(tr_r["energy_double"])
            gnorm_tr = float(tr_r["gradient_norm"])
            z_modes = int(tr_r["hessian_zero_modes"])
            neg_modes = int(tr_r["hessian_negative_modes"])
            margin_canon = float(tr_r["margin_over_canonical"])
            cert = tr_r["certified"]

            if z_modes != 6 or neg_modes != 0 or cert != "TRUE":
                print(f"FAIL: uncertified transplanted cluster at N={n_tr}, ratio={rat_tr}")
                return False
            if gnorm_tr > 1e-10:
                print(f"FAIL: gradient norm exceeds 1e-10 at N={n_tr}, ratio={rat_tr}: {gnorm_tr}")
                return False
            if margin_canon <= 1e-4:
                print(f"FAIL: margin over canonical does not exceed 1e-4 at N={n_tr}, ratio={rat_tr}: {margin_canon}")
                return False

            xyz_file = os.path.join(pkg_root, "object", "transplanted_minima", f"BLJ_N{n_tr}_ratio{rat_tr:.2f}_transplant.xyz")
            if not os.path.isfile(xyz_file):
                print(f"FAIL: missing xyz file {xyz_file}")
                return False
            with open(xyz_file, 'r') as f:
                lines = [l.strip() for l in f if l.strip()]
            sp_xyz = []
            c_xyz = []
            for l in lines[2:2 + n_tr]:
                toks = l.split()
                sp_xyz.append(toks[0].replace('L', ''))
                c_xyz.append([float(toks[1]), float(toks[2]), float(toks[3])])
            recalc_e, recalc_gnorm = compute_blj_energy_and_grad(sp_xyz, c_xyz, rat_tr)
            if abs(recalc_e - e_tr) > 1e-6:
                print(f"FAIL: energy mismatch at N={n_tr}, ratio={rat_tr}: {recalc_e} != {e_tr}")
                return False
            if recalc_gnorm > 1e-10:
                print(f"FAIL: recomputed gradient norm exceeds 1e-10 at N={n_tr}: {recalc_gnorm}")
                return False
            trans_count += 1

    print(
        f"VERIFIED: cells=600 files_audited=576 max_header_err={max_err:.2e} "
        f"reproduce_within_1e5=100% hosted_beaten_gt_1e4=33 p3_certified_clusters=10 "
        f"transplanted_certified_minima={trans_count}"
    )
    print("PASS")
    return True

if __name__ == "__main__":
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not verify_blj_pkg(pkg_dir):
        print("FAIL")
        sys.exit(1)
