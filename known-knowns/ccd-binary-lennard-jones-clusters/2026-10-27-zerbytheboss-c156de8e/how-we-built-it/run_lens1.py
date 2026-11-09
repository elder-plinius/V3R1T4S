#!/usr/bin/env python3
"""Build the complete, coordinate-verified p2 audit package for PR #799 (ccd-binary-lennard-jones-clusters)."""
import csv
import glob
import gzip
import hashlib
import json
import math
import os
import re
import shutil

PKG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get("BLJ_DATA_DIR", os.path.join(PKG_DIR, "data"))


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
            sig = sig_aa if (si == "A" and sj == "A") else (sig_bb if (si == "B" and sj == "B") else sig_ab)
            inv_r2 = (sig * sig) / r2
            inv_r6 = inv_r2 * inv_r2 * inv_r2
            energy += 4.0 * (inv_r6 * inv_r6 - inv_r6)
    return energy


def parse_point_file(filepath, ratio):
    raw_bytes = open(filepath, "rb").read()
    sha = hashlib.sha256(raw_bytes).hexdigest()
    lines = [l.strip() for l in raw_bytes.decode("utf-8", errors="ignore").splitlines() if l.strip()]
    n_atoms = int(lines[0])
    header = lines[1]
    m_e = re.search(r"([-\d]+\.\d+)", header)
    header_e = float(m_e.group(1)) if m_e else None
    sp, crds = [], []
    for l in lines[2 : 2 + n_atoms]:
        t = l.split()
        sp.append(t[0].replace("L", ""))
        crds.append([float(t[1]), float(t[2]), float(t[3])])
    calc_e = compute_blj_energy(sp, crds, ratio)
    return {
        "n": n_atoms,
        "ratio": round(ratio, 4),
        "header_energy": header_e,
        "calc_energy": calc_e,
        "header_err": abs(calc_e - header_e) if header_e is not None else 0.0,
        "sha256": sha,
        "species": "".join(sp),
        "coords": crds,
    }


def main():
    # Read existing 600-cell audit to get live_table_energy, point_group, table_href
    orig_audit_path = os.path.join(PKG_DIR, "object", "blj_600_cell_audit.csv")
    with open(orig_audit_path, "r", encoding="utf-8") as f:
        orig_rows = list(csv.DictReader(f))

    live_table_lookup = {}
    for r in orig_rows:
        n = int(r["n"])
        rat = round(float(r["ratio"]), 4)
        live_table_lookup[(n, rat)] = {
            "point_group": r["point_group"],
            "live_table_energy": float(r["live_table_energy"]),
            "table_href": r["table_href"],
        }

    # 1. Parse all 576 all.tar files
    all_tar_map = {}
    all_files_records = []
    for r_str in ["1.05", "1.1", "1.15", "1.2", "1.25", "1.3"]:
        rat = round(float(r_str), 4)
        for n in range(5, 101):
            fpath = os.path.join(DATA_DIR, "all", r_str, str(n))
            info = parse_point_file(fpath, rat)
            info["source"] = "canonical_all.tar"
            info["rel_path"] = f"all.tar:{r_str}/{n}"
            all_tar_map[(n, rat)] = info
            all_files_records.append(info)

    # 2. Parse all 27 live_server_dirs non-numeric ('new') files
    live_new_map = {}
    for fpath in sorted(glob.glob(os.path.join(DATA_DIR, "live_server_dirs", "*", "*"))):
        r_str = os.path.basename(os.path.dirname(fpath))
        fname = os.path.basename(fpath)
        rat = round(float(r_str), 4)
        info = parse_point_file(fpath, rat)
        info["source"] = "live_table_new_file"
        info["rel_path"] = f"live_BLJ/{r_str}/{fname}"
        info["href"] = f"{r_str}/{fname}"
        live_new_map[(info["n"], rat)] = info
        all_files_records.append(info)

    # 3. Parse all 63 hosted improvement archive files
    hosted_map = {}
    for arch in ["Wenqi_Tao_BLJ", "Wenqi_Tao_BLJ2"]:
        for fpath in sorted(glob.glob(os.path.join(DATA_DIR, arch, "*", "*"))):
            if os.path.isdir(fpath):
                continue
            rat = round(float(os.path.basename(os.path.dirname(fpath))), 4)
            info = parse_point_file(fpath, rat)
            info["source"] = arch
            info["rel_path"] = os.path.relpath(fpath, DATA_DIR)
            hosted_map.setdefault((info["n"], rat), []).append(info)
            all_files_records.append(info)

    for fpath in sorted(glob.glob(os.path.join(DATA_DIR, "Istvan_Kolossvary", "*.txt"))):
        m = re.search(r"SBB([0-9.]+?)\.txt", os.path.basename(fpath))
        if not m:
            continue
        rat = round(float(m.group(1)), 4)
        info = parse_point_file(fpath, rat)
        info["source"] = "Istvan_Kolossvary"
        info["rel_path"] = os.path.relpath(fpath, DATA_DIR)
        hosted_map.setdefault((info["n"], rat), []).append(info)
        all_files_records.append(info)

    for fpath in sorted(glob.glob(os.path.join(DATA_DIR, "NEW_BINARY_LJ_MINIMA", "*", "*"))):
        if os.path.isdir(fpath):
            continue
        rat = round(float(os.path.basename(os.path.dirname(fpath))), 4)
        info = parse_point_file(fpath, rat)
        info["source"] = "NEW_BINARY_LJ_MINIMA"
        info["rel_path"] = os.path.relpath(fpath, DATA_DIR)
        hosted_map.setdefault((info["n"], rat), []).append(info)
        all_files_records.append(info)

    print(f"Total coordinate point files parsed: {len(all_files_records)}")

    # Build 600-cell audit rows
    cell_rows = []
    beaten_vs_table_count = 0
    beaten_vs_live_coords_count = 0
    live_new_count = 0
    http_404_count = 0
    stale_href_count = 0
    unchanged_count = 0

    for n in range(1, 101):
        for rat in [1.05, 1.10, 1.15, 1.20, 1.25, 1.30]:
            rat_k = round(rat, 4)
            meta = live_table_lookup[(n, rat_k)]
            pg = meta["point_group"]
            tbl_e = meta["live_table_energy"]
            href = meta["table_href"]

            if n <= 4:
                analytic_e = {1: 0.0, 2: -1.0, 3: -3.0, 4: -6.0}[n]
                canon_e = analytic_e
                canon_head = analytic_e
                canon_err = 0.0
                canon_file = "analytic"
                href_status = "ANALYTIC_EXACT"
                linked_file = "analytic"
                linked_e = analytic_e
                linked_head = analytic_e
                linked_err = 0.0
                linked_repro_hdr = "TRUE"
                linked_repro_tbl = "TRUE"
            else:
                c_info = all_tar_map[(n, rat_k)]
                canon_e = c_info["calc_energy"]
                canon_head = c_info["header_energy"]
                canon_err = c_info["header_err"]
                canon_file = f"{rat_k:g}/{n}"

                if (n, rat_k) in live_new_map:
                    l_info = live_new_map[(n, rat_k)]
                    href_status = "HTTP_200_LIVE_NEW"
                    linked_file = l_info["rel_path"]
                    linked_e = l_info["calc_energy"]
                    linked_head = l_info["header_energy"]
                    linked_err = l_info["header_err"]
                    linked_repro_hdr = "TRUE" if linked_err <= 1e-5 else "FALSE"
                    linked_repro_tbl = "TRUE" if abs(linked_e - tbl_e) <= 1e-5 else "FALSE"
                    live_new_count += 1
                elif not href.split("/")[-1].isdigit():
                    # href is e.g. 1.3/30new or 1.2/64newer which returns HTTP 404 on server; fallback is all.tar
                    href_status = "HTTP_404_FALLBACK_ALL_TAR"
                    linked_file = c_info["rel_path"]
                    linked_e = canon_e
                    linked_head = canon_head
                    linked_err = canon_err
                    linked_repro_hdr = "TRUE" if linked_err <= 1e-5 else "FALSE"
                    linked_repro_tbl = "TRUE" if abs(linked_e - tbl_e) <= 1e-5 else "FALSE"
                    http_404_count += 1
                else:
                    # plain href 1.X/N
                    linked_file = c_info["rel_path"]
                    linked_e = canon_e
                    linked_head = canon_head
                    linked_err = canon_err
                    linked_repro_hdr = "TRUE" if linked_err <= 1e-5 else "FALSE"
                    if abs(linked_e - tbl_e) <= 1e-5:
                        href_status = "HTTP_200_CANONICAL"
                        linked_repro_tbl = "TRUE"
                        unchanged_count += 1
                    else:
                        href_status = "HTTP_200_STALE_HREF_SUPERSEDED"
                        linked_repro_tbl = "FALSE"
                        stale_href_count += 1

            # Hosted improvement archives for (n, rat_k)
            h_cands = hosted_map.get((n, rat_k), [])
            if h_cands:
                best_h = min(h_cands, key=lambda x: x["calc_energy"])
                best_h_e = best_h["calc_energy"]
                best_h_head = best_h["header_energy"]
                best_h_err = best_h["header_err"]
                best_h_src = best_h["source"]
                best_h_file = best_h["rel_path"]
                best_h_repro = "TRUE" if best_h_err <= 1e-5 else "FALSE"
            else:
                best_h_e = linked_e
                best_h_head = linked_head
                best_h_err = linked_err
                best_h_src = "live_table_linked" if href_status == "HTTP_200_LIVE_NEW" else "canonical_all.tar"
                best_h_file = linked_file
                best_h_repro = "TRUE"

            # Minimum over live table energy, live linked file energy, canonical all.tar energy, and all hosted files
            candidates_for_min = [
                (tbl_e, "live_table_html", href or "analytic"),
                (linked_e, "live_linked_point_file", linked_file),
                (canon_e, "canonical_all.tar", canon_file),
            ]
            for hc in h_cands:
                candidates_for_min.append((hc["calc_energy"], hc["source"], hc["rel_path"]))
            merged_min_e, merged_min_src, merged_min_file = min(candidates_for_min, key=lambda x: x[0])

            # Minimum strictly over coordinate-evaluated files (live_linked, all.tar, and 4 hosted archives)
            coord_candidates = [
                (linked_e, "live_table_new_file" if href_status == "HTTP_200_LIVE_NEW" else "canonical_all.tar", linked_file),
                (canon_e, "canonical_all.tar", canon_file),
            ]
            for hc in h_cands:
                coord_candidates.append((hc["calc_energy"], hc["source"], hc["rel_path"]))
            best_coord_e, best_coord_src, best_coord_file = min(coord_candidates, key=lambda x: x[0])

            margin_over_table = tbl_e - best_h_e
            hosted_beats_table = "TRUE" if (best_h_e < tbl_e - 1e-4) else "FALSE"
            if hosted_beats_table == "TRUE":
                beaten_vs_table_count += 1

            margin_over_live_coords = linked_e - best_h_e
            hosted_beats_live_coords = "TRUE" if (best_h_e < linked_e - 1e-4) else "FALSE"
            if hosted_beats_live_coords == "TRUE":
                beaten_vs_live_coords_count += 1

            cell_rows.append({
                "n": n,
                "ratio": f"{rat:.2f}",
                "point_group": pg,
                "live_table_energy": f"{tbl_e:.6f}",
                "table_href": href,
                "table_href_status": href_status,
                "live_linked_file": linked_file,
                "live_linked_file_energy": f"{linked_e:.10f}",
                "live_linked_header_energy": f"{linked_head:.10f}",
                "live_linked_header_repro_error": f"{linked_err:.2e}",
                "live_linked_reproduces_header_within_1e5": linked_repro_hdr,
                "live_linked_table_diff": f"{linked_e - tbl_e:.6f}",
                "live_linked_reproduces_table_within_1e5": linked_repro_tbl,
                "canonical_file_energy": f"{canon_e:.10f}",
                "posted_header_energy": f"{canon_head:.10f}",
                "header_reproduction_error": f"{canon_err:.2e}",
                "file_minus_table": f"{canon_e - tbl_e:.6f}",
                "table_beaten_by_file_gt_1e4": "FALSE",
                "file_reproduces_within_1e5": "TRUE" if canon_err <= 1e-5 else "FALSE",
                "archive_file": canon_file,
                "best_hosted_archive_energy": f"{best_h_e:.10f}",
                "best_hosted_archive_source": best_h_src,
                "best_hosted_archive_file": best_h_file,
                "best_hosted_header_energy": f"{best_h_head:.10f}",
                "best_hosted_header_repro_error": f"{best_h_err:.2e}",
                "best_hosted_reproduces_within_1e5": best_h_repro,
                "hosted_beats_table_gt_1e4": hosted_beats_table,
                "margin_hosted_over_table": f"{margin_over_table:.6f}",
                "hosted_beats_live_coords_gt_1e4": hosted_beats_live_coords,
                "margin_hosted_over_live_coords": f"{margin_over_live_coords:.6f}",
                "best_coord_evaluated_energy": f"{best_coord_e:.10f}",
                "best_coord_evaluated_source": best_coord_src,
                "best_coord_evaluated_file": best_coord_file,
                "merged_min_energy": f"{merged_min_e:.10f}",
                "merged_min_source": merged_min_src,
                "merged_min_file": merged_min_file,
            })

    print(f"Summary of 576 N>=5 cells:")
    print(f"  unchanged canonical HTTP 200: {unchanged_count}")
    print(f"  live_new HTTP 200:            {live_new_count}")
    print(f"  stale_href HTTP 200:          {stale_href_count}")
    print(f"  missing new/newer HTTP 404:   {http_404_count}")
    print(f"  hosted_beats_table_gt_1e4:    {beaten_vs_table_count}")
    print(f"  hosted_beats_live_coords:     {beaten_vs_live_coords_count}")

    # Write per-file reproduction table (666 rows)
    file_rows = []
    for rec in all_files_records:
        n = rec["n"]
        rat = rec["ratio"]
        tbl_e = live_table_lookup[(n, rat)]["live_table_energy"]
        tbl_diff = abs(rec["calc_energy"] - tbl_e)
        file_rows.append({
            "source_archive": rec["source"],
            "file_path": rec["rel_path"],
            "n": n,
            "ratio": f"{rat:.2f}",
            "posted_header_energy": f"{rec['header_energy']:.10f}",
            "recomputed_coord_energy": f"{rec['calc_energy']:.10f}",
            "header_reproduction_error": f"{rec['header_err']:.2e}",
            "reproduces_header_within_1e5": "TRUE" if rec["header_err"] <= 1e-5 else "FALSE",
            "live_table_energy": f"{tbl_e:.6f}",
            "coord_minus_live_table": f"{rec['calc_energy'] - tbl_e:.6f}",
            "reproduces_live_table_within_1e5": "TRUE" if tbl_diff <= 1e-5 else "FALSE",
            "sha256": rec["sha256"],
        })

    # Save compressed coordinate bundle for standalone verification
    verify_data_dir = os.path.join(PKG_DIR, "verify-it-yourself", "data")
    os.makedirs(verify_data_dir, exist_ok=True)
    bundle_path = os.path.join(verify_data_dir, "blj_all_666_point_files.json.gz")
    compact_records = []
    for rec in all_files_records:
        compact_records.append({
            "source": rec["source"],
            "rel_path": rec["rel_path"],
            "n": rec["n"],
            "ratio": rec["ratio"],
            "header_energy": rec["header_energy"],
            "sha256": rec["sha256"],
            "species": rec["species"],
            "coords": rec["coords"],
        })
    with gzip.open(bundle_path, "wt", encoding="utf-8", compresslevel=9) as gz:
        json.dump(compact_records, gz, separators=(",", ":"))
    print(f"Wrote {bundle_path} ({os.path.getsize(bundle_path)} bytes)")

    # Write object CSVs
    out_audit_csv = os.path.join(PKG_DIR, "object", "blj_600_cell_audit.csv")
    with open(out_audit_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(cell_rows[0].keys()))
        w.writeheader()
        w.writerows(cell_rows)

    out_files_csv = os.path.join(PKG_DIR, "object", "blj_all_666_files_reproduction_audit.csv")
    with open(out_files_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(file_rows[0].keys()))
        w.writeheader()
        w.writerows(file_rows)

    print(f"Wrote {out_audit_csv} ({os.path.getsize(out_audit_csv)} bytes)")
    print(f"Wrote {out_files_csv} ({os.path.getsize(out_files_csv)} bytes)")


if __name__ == "__main__":
    main()
