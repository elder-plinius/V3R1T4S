#!/usr/bin/env python3
"""
Builds the complete standalone certificate package in `package/` next to this script:
  - certs/scalar_lemma_u.tsv       (738 Lemma U scalar certificates, omega in 10..13)
  - certs/thmA_8p.part01.tsv ..    (Theorem A: 8 primes, all inf, 28,057 rows, <= 950KB/file)
  - certs/nine_finite.tsv          (23 basic-only 9-prime models, 736 rows, covers all 5,028 vectors)
  - certs/global_anchored.tsv      (13 anchored 10/11-prime models, 692 rows)
  - MANIFEST.json                  (sha256, byte sizes, meanings, logical cert list)

All files inside `package/` are standalone: they refer to no other file outside `package/`.
"""
import os
import sys
import json
import hashlib
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from neon_global_anchored_probe_r12 import GeneralExponentModel

PKG_DIR = os.path.join(HERE, "package")
CERTS_DIR = os.path.join(PKG_DIR, "certs")
L_TARGET = 6557114959770375
MAX_PART_BYTES = 940_000  # strictly <= 1,000,000 bytes with safe margin
# The nine-prime table written by ../nine-prime-engine/r13/publish_nine.py (override with --nine PATH).
NINE_FINITE_DEFAULT = os.path.join(HERE, "..", "nine-prime-engine", "package", "nine-finite.json")


def sha256_and_size(path):
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(65536)
            if not b:
                break
            n += len(b)
            h.update(b)
    return h.hexdigest(), n


def write_scalar_tsv(out_path):
    src = json.load(open(os.path.join(HERE, "r12_global_L_scalar_cert.json")))
    certs = src["certs"]
    lines = [
        "# format: lemma_u_v1",
        f"# L_target: {L_TARGET}",
        "# columns: id\tomega\tprimes\texps\tk0\tCs\tB_exact",
    ]
    for idx, c in enumerate(certs, 1):
        cid = f"U{idx:03d}"
        primes_s = ",".join(str(p) for p in c["primes"])
        exps_s = ",".join(str(e) for e in c["exps"])
        cs_s = ",".join(c["Cs"])
        lines.append(f"{cid}\t{c['omega']}\t{primes_s}\t{exps_s}\t{c['k0']}\t{cs_s}\t{c['B_exact']}")
    content = "\n".join(lines) + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return len(certs)


def format_anchored_header(model_id, primes, exps, C7, taus_later, U_cut, V_cut, part_str="1/1"):
    primes_s = ",".join(str(p) for p in primes)
    exps_s = ",".join("inf" if e is None else str(e) for e in exps)
    taus_s = ",".join(str(t) for t in taus_later)
    return [
        "# format: anchored_cert_v1",
        f"# id: {model_id}",
        f"# primes: {primes_s}",
        f"# exps: {exps_s}",
        f"# C7: {C7}",
        f"# taus_later: {taus_s}",
        f"# U_cut: {U_cut}",
        f"# V_cut: {V_cut}",
        f"# part: {part_str}",
        "# columns: phase\tkey\tR_exact\tS_exact",
    ]


def write_thmA_parts():
    src = json.load(open(os.path.join(HERE, "r13_cand", "A8_t8_U10_V7.json")))
    primes = [3, 5] + src["primes_later"]
    exps = src["exps"]
    C7 = src["C7"]
    taus_later = src["taus_later"]
    U_cut = src["U_cut"]
    V_cut = src["V_cut"]
    rows = src["rows"]

    row_lines = [
        f"{ph}\t{','.join(str(x) for x in key)}\t{r_s}\t{s_s}"
        for ph, key, r_s, s_s in rows
    ]

    # Estimate header size (generous upper bound) and split cleanly into parts <= MAX_PART_BYTES
    hdr_sample = "\n".join(format_anchored_header("A8", primes, exps, C7, taus_later, U_cut, V_cut, "99/99")) + "\n"
    hdr_bytes = len(hdr_sample.encode("utf-8"))

    chunks = []
    cur = []
    cur_b = hdr_bytes
    for rl in row_lines:
        lb = len(rl.encode("utf-8")) + 1
        if cur and cur_b + lb > MAX_PART_BYTES:
            chunks.append(cur)
            cur = [rl]
            cur_b = hdr_bytes + lb
        else:
            cur.append(rl)
            cur_b += lb
    if cur:
        chunks.append(cur)

    # Remove any old thmA_8p part files
    for fn in os.listdir(CERTS_DIR):
        if fn.startswith("thmA_8p."):
            os.remove(os.path.join(CERTS_DIR, fn))

    n_parts = len(chunks)
    part_rels = []
    for i, ch in enumerate(chunks, 1):
        rel = f"certs/thmA_8p.part{i:02d}.tsv"
        abs_p = os.path.join(PKG_DIR, rel)
        hdr = format_anchored_header("A8", primes, exps, C7, taus_later, U_cut, V_cut, f"{i}/{n_parts}")
        content = "\n".join(hdr + ch) + "\n"
        with open(abs_p, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        part_rels.append(rel)
    return part_rels, len(rows), primes, exps


def write_nine_finite_tsv(out_path, nine_path):
    """
    Independently compute all 23 nine-prime basic models (736 rows) in exact Fraction arithmetic,
    ensuring U_cut > v3 - 3 and V_cut > v5 - 1 on every finite cap so truncation conventions agree identically.
    """
    src = json.load(open(nine_path))
    primes = tuple(src["primes"])
    C7 = Fraction(src["C7"])
    taus_later = tuple(Fraction(t) for t in src["taus_later"])
    base_U = int(src["U"])
    base_V = int(src["V"])

    blocks_out = []
    total_rows = 0
    for idx, c in enumerate(src["certificates"], 1):
        es = tuple(c["exps"])
        uc = max(base_U, (es[0] - 2) if es[0] is not None else base_U)
        vc = max(base_V, es[1] if es[1] is not None else base_V)
        mod = GeneralExponentModel(primes[2:], es, C7=C7, taus_later=taus_later, U_cut=uc, V_cut=vc)

        mid = f"F9_{idx:02d}"
        lines = []
        if idx > 1:
            lines.append("# --- model ---")
        lines.extend(format_anchored_header(mid, primes, es, C7, taus_later, uc, vc, "1/1"))
        for a in (1, 2):
            for b in (2, 4):
                for cc in (a, 3 - a):
                    for j in range(1, 5):
                        st = (a, b, cc, -1, j, 0, 0, 0, -1)
                        R = mod.exact_reserve(st)
                        env = mod.eval_ord_envelope(st, xi=None, use_kappa=False)
                        S = sum(
                            mod.stage_expectation(env, dist, mean, t, mult_scale=1) / bt
                            for (dist, mean), t, bt in zip(mod.full, mod.taus, mod.betas)
                        )
                        assert R > S, f"Failed on {mid} {st}"
                        lines.append(f"basic\t{','.join(str(x) for x in st)}\t{R}\t{S}")
                        total_rows += 1
        blocks_out.append("\n".join(lines))

    content = "\n".join(blocks_out) + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return len(src["certificates"]), total_rows


def write_global_anchored_tsv(out_path):
    src = json.load(open(os.path.join(HERE, "r12_global_L_anchored_cert.json")))
    certs = src["certs"]
    blocks_out = []
    total_rows = 0
    for idx, c in enumerate(certs, 1):
        primes = [3, 5] + c["primes_later"]
        es = c["exps"]
        C7 = c["C7"]
        taus_later = c["taus_later"]
        # Ensure U_cut > v3 - 3 and V_cut > v5 - 1 (all 13 models have finite v3 <= 7, v5 <= 4)
        uc = max(8, (es[0] - 2) if es[0] is not None else 8)
        vc = max(6, es[1] if es[1] is not None else 6)
        mid = f"G{idx:02d}"
        lines = []
        if idx > 1:
            lines.append("# --- model ---")
        lines.extend(format_anchored_header(mid, primes, es, C7, taus_later, uc, vc, "1/1"))
        for ph, key, r_s, s_s in c["rows"]:
            lines.append(f"{ph}\t{','.join(str(x) for x in key)}\t{r_s}\t{s_s}")
            total_rows += 1
        blocks_out.append("\n".join(lines))

    content = "\n".join(blocks_out) + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return len(certs), total_rows


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build the certificate files and MANIFEST.json in package/.")
    parser.add_argument("--nine", default=NINE_FINITE_DEFAULT,
                        help="path to the nine-prime table nine-finite.json (default: %(default)s)")
    args = parser.parse_args()
    os.makedirs(CERTS_DIR, exist_ok=True)

    sc_rel = "certs/scalar_lemma_u.tsv"
    n_sc = write_scalar_tsv(os.path.join(PKG_DIR, sc_rel))

    thmA_parts, n_thmA_rows, thmA_primes, thmA_exps = write_thmA_parts()

    f9_rel = "certs/nine_finite.tsv"
    n_f9_models, n_f9_rows = write_nine_finite_tsv(os.path.join(PKG_DIR, f9_rel), args.nine)

    ga_rel = "certs/global_anchored.tsv"
    n_ga_models, n_ga_rows = write_global_anchored_tsv(os.path.join(PKG_DIR, ga_rel))

    files_list = []

    def add_file(rel, fmt, role, meaning):
        digest, size = sha256_and_size(os.path.join(PKG_DIR, rel))
        assert size <= 1_000_000, f"{rel} too big: {size}"
        files_list.append({
            "path": rel,
            "format": fmt,
            "role": role,
            "bytes": size,
            "sha256": digest,
            "meaning": meaning,
        })

    for idx, rel in enumerate(thmA_parts, 1):
        add_file(
            rel,
            "anchored_cert_v1",
            "theorem_A",
            f"Theorem A (omega(L) >= 9): anchored exclusion of (3,5,7,11,13,17,19,23) with unrestricted exponents, part {idx} of {len(thmA_parts)}.",
        )
    add_file(
        f9_rel,
        "anchored_cert_v1",
        "omega_9_cover",
        f"Nine-prime finite cover: {n_f9_models} Phase-1 (basic) anchored exclusions ({n_f9_rows} rows) on (3..29) dominating all 5,028 nine-prime exponent vectors below L_target.",
    )
    add_file(
        sc_rel,
        "lemma_u_v1",
        "scalar_r10_13",
        f"Scalar distortion (Lemma U) exclusions: {n_sc} exact rational certificates covering 1,736 of 1,754 exponent vectors for omega(L) in 10..13 below L_target.",
    )
    add_file(
        ga_rel,
        "anchored_cert_v1",
        "anchored_r10_11",
        f"Anchored exclusions for omega(L) in 10..11: {n_ga_models} models ({n_ga_rows} basic/mixed rows) dominating the 18 remaining exponent vectors below L_target.",
    )

    manifest = {
        "format": "erdos7_package_manifest_v1",
        "L_target": L_TARGET,
        "total_files": len(files_list),
        "total_bytes": sum(f["bytes"] for f in files_list),
        "files": files_list,
        "certificates": [
            {
                "id": "U1_U738",
                "kind": "lemma_u",
                "role": "scalar_r10_13",
                "count": n_sc,
                "parts": [sc_rel],
                "meaning": "738 Lemma U scalar exclusions for omega(L) in 10..13.",
            },
            {
                "id": "G01_G13",
                "kind": "anchored",
                "role": "anchored_r10_11",
                "model_count": n_ga_models,
                "total_rows": n_ga_rows,
                "parts": [ga_rel],
                "meaning": "13 basic/mixed anchored exclusions for omega(L) in 10..11 covering the 18 vectors not dominated by U1_U738.",
            },
            {
                "id": "F9",
                "kind": "anchored",
                "role": "omega_9_cover",
                "model_count": n_f9_models,
                "total_rows": n_f9_rows,
                "parts": [f9_rel],
                "meaning": "23 basic-only anchored exclusions dominating all 5,028 exponent vectors on the first 9 odd primes below L_target.",
            },
            {
                "id": "A8",
                "kind": "anchored",
                "role": "theorem_A",
                "model_count": 1,
                "total_rows": n_thmA_rows,
                "parts": thmA_parts,
                "meaning": "Excludes all odd coverings supported on the first 8 odd primes (omega(L) >= 9).",
            },
        ],
    }

    with open(os.path.join(PKG_DIR, "MANIFEST.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(f"Built package in {PKG_DIR}:")
    for fe in files_list:
        print(f"  {fe['path']:32s} {fe['bytes']:8,d} B  sha256={fe['sha256'][:16]}...")
    print(f"Total: {len(files_list)} files, {manifest['total_bytes']:,} bytes.")


if __name__ == "__main__":
    main()
