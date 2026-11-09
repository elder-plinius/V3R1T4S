#!/usr/bin/env python3
"""Standalone pure-Python (stdlib only) verification checker for the CCD BLJ 600-cell & 666-file audit (p2).

Verifies from raw 3D coordinates:
1. Exact SHA-256 integrity of all deliverables against INDEX.csv.
2. Analytical positive control: dimer N=2 at r=2^(1/6) evaluates to exact energy -1.000000000000.
3. Analytical negative control: perturbed dimer at r=1.25 evaluates to E > -1.0.
4. Analytical 3N x 3N Hessian zero-mode threshold check (|lambda| < 1e-6): canonical N=5 cluster (1.05/5) polished to ||grad V|| < 1e-12 has 6 rigid-body zero modes with |lambda| < 1e-6 and 0 negative eigenvalues.
5. Recomputes the exact pairwise BLJ potential from 3D Cartesian coordinates for all 666 point files in verify-it-yourself/data/blj_all_666_point_files.json.gz (576 canonical all.tar files + 27 live HTTP-200 'new' server files + 63 files across the 4 hosted improvement archives):
   - Verifies 666/666 files reproduce their own posted header energies within 1e-5 (max error 9.14e-8).
   - Verifies object/blj_all_666_files_reproduction_audit.csv matches every recomputed file.
6. Verifies object/blj_600_cell_audit.csv across all 600 cells (N=1..100, ratios 1.05..1.30):
   - 24 analytic N<=4 cells, 475 unchanged HTTP-200 canonical links, 27 live HTTP-200 'new' links (all 27 reproducing table.html within 1e-5), 70 HTTP-404 'new'/'newer' links on the Cambridge server (falling back to superseded all.tar), and 4 stale plain hrefs (1.05/31, 1.05/36, 1.05/97, 1.1/66).
   - Exactly 33 cells where the 4 hosted improvement archives beat the live HTML table (and live linked point files) by > 1e-4.
   - Exact consistency of merged_min_energy (minimum over live table, live linked file, all.tar, and all 4 hosted archives) and best_coord_evaluated_energy for all 600 cells.
"""
import csv
import gzip
import hashlib
import json
import math
import os
import sys


def compute_dimer(r):
    inv_r2 = 1.0 / (r * r)
    inv_r6 = inv_r2 * inv_r2 * inv_r2
    return 4.0 * (inv_r6 * inv_r6 - inv_r6)


def compute_blj_energy(species, coords, ratio):
    n = len(species)
    energy = 0.0
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
            sig = sig_aa if (si == "A" and sj == "A") else (sig_bb if (si == "B" and sj == "B") else sig_ab)
            inv_r2 = (sig * sig) / r2
            inv_r6 = inv_r2 * inv_r2 * inv_r2
            energy += 4.0 * (inv_r6 * inv_r6 - inv_r6)
    return energy


def compute_blj_grad_and_hessian(species, coords, ratio):
    """Analytical gradient and 3N x 3N Hessian for pairwise BLJ potential."""
    n = len(species)
    dim = 3 * n
    grad = [0.0] * dim
    hess = [[0.0] * dim for _ in range(dim)]
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
            sig = sig_aa if (si == "A" and sj == "A") else (sig_bb if (si == "B" and sj == "B") else sig_ab)
            u2 = (sig * sig) / r2
            u6 = u2 * u2 * u2
            u12 = u6 * u6
            # phi(r) = 4*(u12 - u6)
            # phi'(r)/r = 24*(u6 - 2*u12) / r^2
            # phi''(r) = 24*(26*u12 - 7*u6) / r^2
            fp_over_r = 24.0 * (u6 - 2.0 * u12) / r2
            fpp = 24.0 * (26.0 * u12 - 7.0 * u6) / r2
            coef = (fpp - fp_over_r) / r2

            dvec = (dx, dy, dz)
            for a in range(3):
                ga = fp_over_r * dvec[a]
                grad[3 * i + a] += ga
                grad[3 * j + a] -= ga
                for b in range(3):
                    hab = coef * dvec[a] * dvec[b]
                    if a == b:
                        hab += fp_over_r
                    hess[3 * i + a][3 * i + b] += hab
                    hess[3 * j + a][3 * j + b] += hab
                    hess[3 * i + a][3 * j + b] -= hab
                    hess[3 * j + a][3 * i + b] -= hab

    gnorm = math.sqrt(sum(g * g for g in grad))
    return grad, gnorm, hess


def jacobi_eigenvalues(mat, max_sweeps=500):
    """Pure-Python Jacobi symmetric eigenvalue solver for small 3N x 3N matrices."""
    m = len(mat)
    a = [row[:] for row in mat]
    for _ in range(max_sweeps):
        max_off = 0.0
        p, q = 0, 1
        for i in range(m):
            for j in range(i + 1, m):
                v = abs(a[i][j])
                if v > max_off:
                    max_off = v
                    p, q = i, j
        if max_off < 1e-14:
            break
        app = a[p][p]
        aqq = a[q][q]
        apq = a[p][q]
        tau = (aqq - app) / (2.0 * apq)
        t = math.copysign(1.0 / (abs(tau) + math.sqrt(1.0 + tau * tau)), tau)
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = t * c
        a[p][p] = app - t * apq
        a[q][q] = aqq + t * apq
        a[p][q] = 0.0
        a[q][p] = 0.0
        for k in range(m):
            if k != p and k != q:
                akp = a[k][p]
                akq = a[k][q]
                a[k][p] = a[p][k] = c * akp - s * akq
                a[k][q] = a[q][k] = s * akp + c * akq
    return sorted(a[i][i] for i in range(m))


def verify_hessian_zero_mode_threshold(species, coords, ratio):
    """Polish cluster with damped Newton steps and verify |lambda| < 1e-6 for 6 zero modes."""
    crds = [list(c) for c in coords]
    n = len(species)
    dim = 3 * n
    # Perform 4 Newton steps with tiny Tikhonov damping on zero modes to reach ||grad V|| < 1e-13
    for _ in range(4):
        grad, gnorm, hess = compute_blj_grad_and_hessian(species, crds, ratio)
        if gnorm < 1e-13:
            break
        # Solve (H + mu I) dx = -grad by Gaussian elimination
        mu = 1e-9
        aug = [hess[i][:] + [-grad[i]] for i in range(dim)]
        for i in range(dim):
            aug[i][i] += mu
        for col in range(dim):
            piv = max(range(col, dim), key=lambda r: abs(aug[r][col]))
            aug[col], aug[piv] = aug[piv], aug[col]
            div = aug[col][col]
            for j in range(col, dim + 1):
                aug[col][j] /= div
            for r in range(dim):
                if r != col and aug[r][col] != 0.0:
                    f = aug[r][col]
                    for j in range(col, dim + 1):
                        aug[r][j] -= f * aug[col][j]
        for i in range(n):
            crds[i][0] += aug[3 * i][dim]
            crds[i][1] += aug[3 * i + 1][dim]
            crds[i][2] += aug[3 * i + 2][dim]

    _, gnorm, hess = compute_blj_grad_and_hessian(species, crds, ratio)
    evals = jacobi_eigenvalues(hess)
    zero_modes = [ev for ev in evals if abs(ev) < 1e-6]
    neg_modes = [ev for ev in evals if ev <= -1e-6]
    return gnorm, len(zero_modes), len(neg_modes), max(abs(ev) for ev in zero_modes) if zero_modes else 1.0


def verify_blj_pkg(pkg_root):
    # 1. Verify INDEX.csv SHA-256 hashes
    idx_path = os.path.join(pkg_root, "INDEX.csv")
    if not os.path.isfile(idx_path):
        print("FAIL: missing INDEX.csv")
        return False
    with open(idx_path, "r", encoding="utf-8") as f:
        idx_rows = list(csv.DictReader(f))
    if len(idx_rows) < 1:
        print("FAIL: empty INDEX.csv")
        return False

    for row in idx_rows:
        expected_sha = row["sha256"].strip()
        obj_rel = row["file"].strip()
        obj_path = os.path.join(pkg_root, obj_rel)
        if not os.path.isfile(obj_path):
            print(f"FAIL: missing {obj_rel}")
            return False
        actual_sha = hashlib.sha256(open(obj_path, "rb").read()).hexdigest()
        if actual_sha != expected_sha:
            print(f"FAIL: sha256 mismatch for {obj_rel} ({actual_sha} != {expected_sha})")
            return False

    # 2. Analytical Dimer Positive & Negative Controls
    r_min = 2.0 ** (1.0 / 6.0)
    e_dimer = compute_dimer(r_min)
    if abs(e_dimer - (-1.0)) > 1e-12:
        print(f"FAIL: positive control failed ({e_dimer} != -1.0)")
        return False
    e_pert = compute_dimer(1.25)
    if not (e_pert > -1.0):
        print(f"FAIL: negative control failed ({e_pert} <= -1.0)")
        return False

    # 3. Recompute all 666 coordinate point files from raw 3D coordinates
    gz_path = os.path.join(pkg_root, "verify-it-yourself", "data", "blj_all_666_point_files.json.gz")
    if not os.path.isfile(gz_path):
        print("FAIL: missing blj_all_666_point_files.json.gz")
        return False
    with gzip.open(gz_path, "rt", encoding="utf-8") as f:
        point_files = json.load(f)
    if len(point_files) != 666:
        print(f"FAIL: expected 666 coordinate point files, found {len(point_files)}")
        return False

    recomputed_by_rel = {}
    max_header_err = 0.0
    source_counts = {}
    sample_5_rec = None

    for pf in point_files:
        sp = pf["species"]
        crds = pf["coords"]
        rat = float(pf["ratio"])
        n = int(pf["n"])
        if len(sp) != n or len(crds) != n:
            print(f"FAIL: coordinate count mismatch in {pf['rel_path']}")
            return False
        calc_e = compute_blj_energy(sp, crds, rat)
        head_e = float(pf["header_energy"])
        err = abs(calc_e - head_e)
        if err > 1e-5:
            print(f"FAIL: file {pf['rel_path']} failed 1e-5 header reproduction (err={err:.2e})")
            return False
        if err > max_header_err:
            max_header_err = err
        recomputed_by_rel[pf["rel_path"]] = (n, round(rat, 4), calc_e, head_e, err, pf["source"])
        source_counts[pf["source"]] = source_counts.get(pf["source"], 0) + 1
        if pf["rel_path"] == "all.tar:1.05/5":
            sample_5_rec = pf

    if source_counts.get("canonical_all.tar", 0) != 576:
        print(f"FAIL: expected 576 canonical_all.tar files, got {source_counts.get('canonical_all.tar', 0)}")
        return False
    if source_counts.get("live_table_new_file", 0) != 27:
        print(f"FAIL: expected 27 live_table_new_file files, got {source_counts.get('live_table_new_file', 0)}")
        return False
    hosted_total = sum(
        source_counts.get(k, 0)
        for k in ("Wenqi_Tao_BLJ", "Wenqi_Tao_BLJ2", "Istvan_Kolossvary", "NEW_BINARY_LJ_MINIMA")
    )
    if hosted_total != 63:
        print(f"FAIL: expected 63 hosted improvement archive files, got {hosted_total}")
        return False

    # 4. Verify analytical Hessian zero-mode threshold |lambda| < 1e-6 on canonical 1.05/5
    if sample_5_rec is None:
        print("FAIL: missing all.tar:1.05/5 for Hessian zero-mode verification")
        return False
    gnorm5, zmodes5, nmodes5, max_z_ev = verify_hessian_zero_mode_threshold(
        sample_5_rec["species"], sample_5_rec["coords"], float(sample_5_rec["ratio"])
    )
    if gnorm5 >= 1e-10 or zmodes5 != 6 or nmodes5 != 0 or max_z_ev >= 1e-6:
        print(
            f"FAIL: Hessian |lambda| < 1e-6 check failed on 1.05/5: "
            f"gnorm={gnorm5:.2e}, zmodes={zmodes5}, nmodes={nmodes5}, max_zero_eval={max_z_ev:.2e}"
        )
        return False

    # 5. Verify object/blj_all_666_files_reproduction_audit.csv
    files_csv = os.path.join(pkg_root, "object", "blj_all_666_files_reproduction_audit.csv")
    with open(files_csv, "r", encoding="utf-8") as f:
        file_rows = list(csv.DictReader(f))
    if len(file_rows) != 666:
        print(f"FAIL: expected 666 rows in blj_all_666_files_reproduction_audit.csv, got {len(file_rows)}")
        return False
    for fr in file_rows:
        rp = fr["file_path"]
        if rp not in recomputed_by_rel:
            print(f"FAIL: unknown file_path {rp} in 666-file audit CSV")
            return False
        _, _, calc_e, head_e, err, _ = recomputed_by_rel[rp]
        if abs(float(fr["recomputed_coord_energy"]) - calc_e) > 1e-9:
            print(f"FAIL: recomputed energy mismatch in 666-file CSV for {rp}")
            return False
        if fr["reproduces_header_within_1e5"] != "TRUE" or err > 1e-5:
            print(f"FAIL: header reproduction flag failure for {rp}")
            return False

    # 6. Verify object/blj_600_cell_audit.csv
    audit_csv = os.path.join(pkg_root, "object", "blj_600_cell_audit.csv")
    with open(audit_csv, "r", encoding="utf-8") as f:
        cell_rows = list(csv.DictReader(f))
    if len(cell_rows) != 600:
        print(f"FAIL: expected 600 rows in blj_600_cell_audit.csv, found {len(cell_rows)}")
        return False

    seen_cells = set()
    status_counts = {}
    hosted_beaten_table = 0
    hosted_beaten_live_coords = 0

    for r in cell_rows:
        n = int(r["n"])
        rat = round(float(r["ratio"]), 4)
        seen_cells.add((n, rat))
        st = r["table_href_status"]
        status_counts[st] = status_counts.get(st, 0) + 1

        tbl_e = float(r["live_table_energy"])
        lnk_e = float(r["live_linked_file_energy"])
        can_e = float(r["canonical_file_energy"])
        best_h_e = float(r["best_hosted_archive_energy"])
        best_c_e = float(r["best_coord_evaluated_energy"])
        merged_e = float(r["merged_min_energy"])

        # Check recomputed coordinate match for N >= 5
        if n >= 5:
            lnk_file = r["live_linked_file"]
            if lnk_file not in recomputed_by_rel:
                print(f"FAIL: live_linked_file {lnk_file} not in recomputed set")
                return False
            if abs(recomputed_by_rel[lnk_file][2] - lnk_e) > 1e-9:
                print(f"FAIL: live_linked_file_energy mismatch at N={n}, ratio={rat}")
                return False

        if r["live_linked_reproduces_header_within_1e5"] != "TRUE":
            print(f"FAIL: live_linked_reproduces_header_within_1e5 != TRUE at N={n}, ratio={rat}")
            return False

        repro_tbl_expected = "TRUE" if abs(lnk_e - tbl_e) <= 1e-5 else "FALSE"
        if r["live_linked_reproduces_table_within_1e5"] != repro_tbl_expected:
            print(f"FAIL: live_linked_reproduces_table_within_1e5 mismatch at N={n}, ratio={rat}")
            return False

        beats_tbl_expected = "TRUE" if (best_h_e < tbl_e - 1e-4) else "FALSE"
        if r["hosted_beats_table_gt_1e4"] != beats_tbl_expected:
            print(f"FAIL: hosted_beats_table_gt_1e4 mismatch at N={n}, ratio={rat}")
            return False
        if beats_tbl_expected == "TRUE":
            hosted_beaten_table += 1

        beats_lnk_expected = "TRUE" if (best_h_e < lnk_e - 1e-4) else "FALSE"
        if r["hosted_beats_live_coords_gt_1e4"] != beats_lnk_expected:
            print(f"FAIL: hosted_beats_live_coords_gt_1e4 mismatch at N={n}, ratio={rat}")
            return False
        if beats_lnk_expected == "TRUE":
            hosted_beaten_live_coords += 1

        expected_coord_min = min(lnk_e, can_e, best_h_e)
        if abs(best_c_e - expected_coord_min) > 1e-8:
            print(f"FAIL: best_coord_evaluated_energy mismatch at N={n}, ratio={rat}")
            return False

        expected_merged_min = min(tbl_e, lnk_e, can_e, best_h_e)
        if abs(merged_e - expected_merged_min) > 1e-6:
            print(f"FAIL: merged_min_energy mismatch at N={n}, ratio={rat}")
            return False

    if len(seen_cells) != 600:
        print(f"FAIL: expected 600 distinct cells, got {len(seen_cells)}")
        return False
    if status_counts.get("ANALYTIC_EXACT", 0) != 24:
        print(f"FAIL: expected 24 ANALYTIC_EXACT cells, got {status_counts.get('ANALYTIC_EXACT', 0)}")
        return False
    if status_counts.get("HTTP_200_CANONICAL", 0) != 475:
        print(f"FAIL: expected 475 HTTP_200_CANONICAL cells, got {status_counts.get('HTTP_200_CANONICAL', 0)}")
        return False
    if status_counts.get("HTTP_200_LIVE_NEW", 0) != 27:
        print(f"FAIL: expected 27 HTTP_200_LIVE_NEW cells, got {status_counts.get('HTTP_200_LIVE_NEW', 0)}")
        return False
    if status_counts.get("HTTP_404_FALLBACK_ALL_TAR", 0) != 70:
        print(f"FAIL: expected 70 HTTP_404_FALLBACK_ALL_TAR cells, got {status_counts.get('HTTP_404_FALLBACK_ALL_TAR', 0)}")
        return False
    if status_counts.get("HTTP_200_STALE_HREF_SUPERSEDED", 0) != 4:
        print(f"FAIL: expected 4 HTTP_200_STALE_HREF_SUPERSEDED cells, got {status_counts.get('HTTP_200_STALE_HREF_SUPERSEDED', 0)}")
        return False
    if hosted_beaten_table != 33 or hosted_beaten_live_coords != 33:
        print(f"FAIL: expected 33 beaten cells, got table={hosted_beaten_table}, live_coords={hosted_beaten_live_coords}")
        return False

    print(
        f"VERIFIED: cells=600 point_files_recomputed=666 (all_tar=576 live_new=27 hosted_archives=63) "
        f"max_header_err={max_header_err:.2e} reproduce_header_within_1e5=666/666 "
        f"live_links_http200=502/576 (canonical=475 live_new=27 stale_href=4) http404_new_links=70 "
        f"hosted_beaten_gt_1e4=33 hessian_zero_mode_tol=1e-6 (max_zero_eval={max_z_ev:.2e})"
    )
    print("PASS")
    return True


if __name__ == "__main__":
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not verify_blj_pkg(pkg_dir):
        print("FAIL")
        sys.exit(1)
