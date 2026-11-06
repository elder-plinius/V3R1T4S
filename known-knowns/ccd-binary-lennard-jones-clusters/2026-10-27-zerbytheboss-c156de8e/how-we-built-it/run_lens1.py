#!/usr/bin/env python3
"""Lens 1: 600-Cell Cambridge Cluster Database & 4 Improvement Archives Recomputation Audit (Upgraded p2)."""
import csv
import glob
import math
import os
import random
import re
import sys
import time

def compute_blj_energy(species, coords, ratio):
    n = len(species)
    energy = 0.0
    sig_aa = 1.0
    sig_bb = ratio
    sig_ab = (1.0 + ratio) / 2.0
    
    for i in range(n):
        xi, yi, zi = coords[i]
        si = species[i]
        for j in range(i + 1, n):
            xj, yj, zj = coords[j]
            sj = species[j]
            
            dx = xi - xj
            dy = yi - yj
            dz = zi - zj
            r2 = dx * dx + dy * dy + dz * dz
            
            sig = sig_aa if (si == 'A' and sj == 'A') else (sig_bb if (si == 'B' and sj == 'B') else sig_ab)
            s2 = sig * sig
            inv_r2 = s2 / r2
            inv_r6 = inv_r2 * inv_r2 * inv_r2
            inv_r12 = inv_r6 * inv_r6
            energy += 4.0 * (inv_r12 - inv_r6)
            
    return energy

def parse_point_file(filepath, default_ratio=None):
    with open(filepath, 'r', errors='ignore') as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines:
        return None
    try:
        n_atoms = int(lines[0])
    except ValueError:
        return None
        
    header_line = lines[1] if len(lines) > 1 else ""
    m_e = re.search(r"Energy of minimum\s+\d+=\s*([-\d.]+)", header_line)
    header_energy = float(m_e.group(1)) if m_e else None
    
    ratio = default_ratio
    if ratio is None:
        parts = filepath.split(os.sep)
        try:
            ratio = float(parts[-2])
        except ValueError:
            pass
            
    species = []
    coords = []
    for l in lines[2:2 + n_atoms]:
        tokens = l.split()
        if len(tokens) < 4:
            continue
        sp = tokens[0].replace('L', '')
        species.append(sp)
        coords.append((float(tokens[1]), float(tokens[2]), float(tokens[3])))
        
    if len(coords) != n_atoms:
        return None
    return n_atoms, ratio, header_energy, species, coords

def main():
    print("=" * 70)
    print("LENS 1: 600-Cell Full Database & 4 Improvement Archives Recomputation Audit")
    print("=" * 70)
    
    run_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    data_dir = os.path.join(run_dir, "data")
    all_dir = os.path.join(data_dir, "all")
    
    # 1. Verification Controls
    print("\n--- Phase 1: Analytical Controls ---")
    r_min = 2.0 ** (1.0 / 6.0)
    dimer_coords = [(0.0, 0.0, 0.0), (r_min, 0.0, 0.0)]
    e_dimer = compute_blj_energy(['A', 'A'], dimer_coords, ratio=1.0)
    print(f"[Positive Control] Dimer N=2 (A-A) at r=2^(1/6): Energy = {e_dimer:.12f} (expected -1.0)")
    assert abs(e_dimer - (-1.0)) < 1e-12, "Dimer positive control failed!"
    
    dimer_perturbed = [(0.0, 0.0, 0.0), (1.25, 0.0, 0.0)]
    e_pert = compute_blj_energy(['A', 'A'], dimer_perturbed, ratio=1.0)
    print(f"[Negative Control] Perturbed Dimer r=1.25: Energy = {e_pert:.12f} (expected > -1.0)")
    assert e_pert > -1.0, "Dimer negative control failed!"
    
    # 2. Calibration on 10 Random Point Files from all.tar
    print("\n--- Phase 2: Calibration on 10 Random Table Point Files ---")
    all_files = sorted(glob.glob(os.path.join(all_dir, "*", "*")))
    rng = random.Random(42)
    sample_files = rng.sample(all_files, 10)
    max_calib_err = 0.0
    for fpath in sample_files:
        rel_p = os.path.relpath(fpath, all_dir)
        n, ratio, e_head, sp, coords = parse_point_file(fpath)
        e_calc = compute_blj_energy(sp, coords, ratio)
        diff = abs(e_calc - e_head)
        max_calib_err = max(max_calib_err, diff)
        print(f"  {rel_p:10s} (N={n:3d}, ratio={ratio:.2f}): E_head={e_head:.8f}, E_calc={e_calc:.8f}, diff={diff:.2e}")
        assert diff < 1e-6, f"Calibration failed on {rel_p}"
    print(f"Checker Calibration Passed (max err = {max_calib_err:.2e} < 1e-6).")
    
    # 3. Evaluate all hosted improvement archives
    print("\n--- Phase 3: Evaluating 4 Hosted Improvement Archives ---")
    hosted_candidates = {} # (n, ratio) -> list of dicts
    
    # Huang & Ye 2011 (Wenqi_Tao_BLJ & Wenqi_Tao_BLJ2)
    for arch in ['Wenqi_Tao_BLJ', 'Wenqi_Tao_BLJ2']:
        files = glob.glob(os.path.join(data_dir, arch, '*', '*'))
        for fpath in sorted(files):
            if os.path.isdir(fpath): continue
            try:
                rat = float(os.path.basename(os.path.dirname(fpath)))
            except ValueError:
                continue
            res = parse_point_file(fpath, default_ratio=rat)
            if not res: continue
            n, r_val, e_head, sp, crds = res
            e_calc = compute_blj_energy(sp, crds, rat)
            err = abs(e_calc - e_head) if e_head is not None else 0.0
            key = (n, round(rat, 4))
            if key not in hosted_candidates: hosted_candidates[key] = []
            hosted_candidates[key].append({
                'source': arch,
                'rel_path': os.path.relpath(fpath, data_dir),
                'energy': e_calc,
                'header_energy': e_head,
                'header_err': err,
                'species': sp,
                'coords': crds
            })
            
    # Istvan Kolossvary 2010
    ik_files = glob.glob(os.path.join(data_dir, 'Istvan_Kolossvary', '*.txt'))
    for fpath in sorted(ik_files):
        fname = os.path.basename(fpath)
        m = re.search(r'SBB([0-9.]+?)\.txt', fname)
        if not m: continue
        rat = float(m.group(1))
        res = parse_point_file(fpath, default_ratio=rat)
        if not res: continue
        n, r_val, e_head, sp, crds = res
        e_calc = compute_blj_energy(sp, crds, rat)
        err = abs(e_calc - e_head) if e_head is not None else 0.0
        key = (n, round(rat, 4))
        if key not in hosted_candidates: hosted_candidates[key] = []
        hosted_candidates[key].append({
            'source': 'Istvan_Kolossvary',
            'rel_path': os.path.relpath(fpath, data_dir),
            'energy': e_calc,
            'header_energy': e_head,
            'header_err': err,
            'species': sp,
            'coords': crds
        })
        
    # NEW_BINARY_LJ_MINIMA (Sicher, Mohr, Goedecker 2011)
    smg_files = glob.glob(os.path.join(data_dir, 'NEW_BINARY_LJ_MINIMA', '*', '*'))
    for fpath in sorted(smg_files):
        if fpath.endswith('preprint_link') or fpath.endswith('.ascii') or os.path.isdir(fpath):
            continue
        try:
            rat = float(os.path.basename(os.path.dirname(fpath)))
        except ValueError:
            continue
        res = parse_point_file(fpath, default_ratio=rat)
        if not res: continue
        n, r_val, e_head, sp, crds = res
        e_calc = compute_blj_energy(sp, crds, rat)
        err = abs(e_calc - e_head) if e_head is not None else 0.0
        key = (n, round(rat, 4))
        if key not in hosted_candidates: hosted_candidates[key] = []
        hosted_candidates[key].append({
            'source': 'NEW_BINARY_LJ_MINIMA',
            'rel_path': os.path.relpath(fpath, data_dir),
            'energy': e_calc,
            'header_energy': e_head,
            'header_err': err,
            'species': sp,
            'coords': crds
        })
        
    print(f"Parsed {sum(len(v) for v in hosted_candidates.values())} files across 4 improvement archives covering {len(hosted_candidates)} distinct cells.")
    
    # 4. Parse live table
    print("\n--- Phase 4: Parsing Live Table & Building Merged Audit ---")
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_audit = os.path.join(pkg_dir, "object", "blj_600_cell_audit.csv")
    
    rows = []
    beaten_count = 0
    with open(base_audit, 'r') as f:
        reader = list(csv.DictReader(f))
        
    for r in reader:
        n = int(r['n'])
        rat = float(r['ratio'])
        rat_key = round(rat, 4)
        live_tbl_e = float(r['live_table_energy'])
        canon_e = float(r['canonical_file_energy'])
        
        # Check hosted candidates
        cands = hosted_candidates.get((n, rat_key), [])
        if cands:
            best_cand = min(cands, key=lambda x: x['energy'])
            best_e = best_cand['energy']
            best_src = best_cand['source']
            best_file = best_cand['rel_path']
        else:
            best_e = canon_e
            best_src = "canonical_all.tar"
            best_file = r['archive_file']
            
        margin_hosted = live_tbl_e - best_e # positive if hosted beats live table
        hosted_beats = "TRUE" if (best_e < live_tbl_e - 1e-4) else "FALSE"
        if hosted_beats == "TRUE":
            beaten_count += 1
            
        row_out = {
            'n': n,
            'ratio': f"{rat:.2f}",
            'point_group': r['point_group'],
            'live_table_energy': f"{live_tbl_e:.6f}",
            'canonical_file_energy': f"{canon_e:.10f}",
            'posted_header_energy': r['posted_header_energy'],
            'header_reproduction_error': r['header_reproduction_error'],
            'file_minus_table': r['file_minus_table'],
            'table_beaten_by_file_gt_1e4': r['table_beaten_by_file_gt_1e4'],
            'file_reproduces_within_1e5': r['file_reproduces_within_1e5'],
            'archive_file': r['archive_file'],
            'table_href': r['table_href'],
            'best_hosted_archive_energy': f"{best_e:.10f}",
            'best_hosted_archive_source': best_src,
            'best_hosted_archive_file': best_file,
            'hosted_beats_table_gt_1e4': hosted_beats,
            'margin_hosted_over_table': f"{margin_hosted:.6f}"
        }
        rows.append(row_out)
        
    print(f"Audit table compiled for all 600 cells.")
    print(f"Cells where hosted archives beat live table by > 1e-4: {beaten_count}")
    assert beaten_count == 33, f"Expected exactly 33 beaten cells, got {beaten_count}"
    
    # Save to object/blj_600_cell_audit.csv in run directory
    out_dir = os.path.join(run_dir, "object")
    os.makedirs(out_dir, exist_ok=True)
    out_csv = os.path.join(out_dir, "blj_600_cell_audit.csv")
    fieldnames = list(rows[0].keys())
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved upgraded audit table to {out_csv}")
    print("\nLENS 1 COMPLETE: All 4 improvement archives re-evaluated and merged into 600-cell audit table.")

if __name__ == "__main__":
    main()
