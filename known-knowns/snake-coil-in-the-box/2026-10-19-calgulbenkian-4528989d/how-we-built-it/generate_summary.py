import hashlib
import json
import os
import sys

sys.path.insert(0, "src")
import verify_snake_coil as vsc


def canon_hash(steps, is_coil):
    canon = vsc.canonical_coil(steps) if is_coil else vsc.canonical_snake(steps)
    s_b36 = vsc.steps_to_b36(canon)
    return hashlib.sha256(s_b36.encode()).hexdigest()[:16], s_b36[:36]


def parse_multi_file(path):
    seqs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if " " in line and all(tok.isdigit() for tok in line.split()):
                seqs.append([int(x) for x in line.split()])
            elif all(c.isalnum() for c in line):
                seqs.append([int(c, 36) for c in line])
    return seqs


def main():
    bank_cache = {}

    def get_bank(n, kind, L):
        key = (n, "coil" if kind in ("coil", "symmetric_coil") else "snake", L)
        if key not in bank_cache:
            raw_bank = vsc.load_reference_bank("data/seeds", key[0], key[1], key[2])
            chashes = {}
            for k, (c_tup, inv) in raw_bank.items():
                h = hashlib.sha256(vsc.steps_to_b36(c_tup).encode()).hexdigest()[:16]
                chashes[h] = (k, inv)
            bank_cache[key] = (raw_bank, chashes)
        return bank_cache[key]

    cg_files = {
        "pr79_sym12_1450": ("symmetric_coil", 12, "cg_branches/79_Q12_symcoil_1450/sym_coil_Q12_1450.txt"),
        "pr80_sym13_2870": ("symmetric_coil", 13, "cg_branches/80_Q13_symcoil_2870/sym_coil_Q13_2870.txt"),
        "pr81_coil14_5854": ("coil", 14, "cg_branches/81_Q14_coil_5854/coil_Q14_5854.txt"),
        "pr82_snake14_5854": ("snake", 14, "cg_branches/82_Q14_snake_5854/snake_Q14_5854.txt"),
        "pr83_coil10_374": ("coil", 10, "cg_branches/83_Q10_coil_374/inequiv_co10_374.txt"),
        "pr84_coil11_740": ("coil", 11, "cg_branches/84_Q11_coil_740/inequiv_co11_740.txt"),
        "pr85_coil12_1468": ("coil", 12, "cg_branches/85_Q12_coil_1468/inequiv_co12_1468.txt"),
        "pr86_coil13_2930": ("coil", 13, "cg_branches/86_Q13_coil_2930/inequiv_co13_2930.txt"),
        "pr87_snake11_750": ("snake", 11, "cg_branches/87_Q11_snake_750/inequiv_sn11_750.txt"),
        "pr88_snake12_1480": ("snake", 12, "cg_branches/88_Q12_snake_1480/inequiv_sn12_1480.txt"),
        "pr89_snake13_2946": ("snake", 13, "cg_branches/89_Q13_snake_2946/inequiv_sn13_2946.txt"),
    }

    cg_summary = {}
    cg_hashes = set()
    for name, (kind, n, path) in cg_files.items():
        seqs = parse_multi_file(path)
        recs = []
        seen_in_file = set()
        for steps in seqs:
            v = vsc.verify_steps(steps, expected_n=n)
            is_coil = (v["type"] == "coil")
            if kind == "symmetric_coil":
                assert v["is_symmetric"], f"Expected symmetric coil in {name}"
            ch, cpref = canon_hash(steps, is_coil)
            _, bank_hashes = get_bank(n, kind, v["length"])
            ineq_pub = (ch not in bank_hashes)
            distinct_in_file = (ch not in seen_in_file)
            seen_in_file.add(ch)
            cg_hashes.add(ch)
            recs.append({
                "valid": v["valid"],
                "n": v["n"],
                "type": v["type"],
                "is_symmetric": v["is_symmetric"],
                "length": v["length"],
                "canonical_hash": ch,
                "canonical_prefix": cpref,
                "dcv": list(v["invariants"]["dcv"]),
                "gap_spectrum_hash": v["invariants"]["gap_spectrum_hash"],
                "inequiv_vs_public": ineq_pub,
                "distinct_in_file": distinct_in_file,
            })
        all_val = all(r["valid"] for r in recs)
        all_ineq = all(r["inequiv_vs_public"] for r in recs)
        L = recs[0]["length"] if recs else 0
        cg_summary[name] = {
            "kind": kind,
            "dim": n,
            "path": path,
            "count": len(recs),
            "distinct_canonical_classes": len(seen_in_file),
            "all_valid": all_val,
            "all_inequiv_vs_public": all_ineq,
            "length": L,
            "records": recs,
        }
        print(f"CG {name:20s}: count={len(recs):2d} distinct={len(seen_in_file):2d} valid={all_val} inequiv_public={all_ineq} L={L}")

    our_files = [
        # p1: New Symmetric Coil World Records & Drifted Variants
        ("p1_sym11_734_r0", "symmetric_coil", 11, "results/best_sym11_drifted_r0_Q11_734.txt", 730, 734),
        ("p1_sym11_734_r1", "symmetric_coil", 11, "results/best_sym11_drifted_r1_Q11_734.txt", 730, 734),
        ("p1_sym12_1454_lift", "symmetric_coil", 12, "results/lift_sym12_Q12_1454.txt", 1434, 1450),
        ("p1_sym12_1454_ils", "symmetric_coil", 12, "results/best_sym12_Q12_1454.txt", 1434, 1450),
        ("p1_sym12_1454_drifted_r0", "symmetric_coil", 12, "results/best_sym12_v2_drifted_r0_Q12_1454.txt", 1434, 1450),
        ("p1_sym12_1454_drifted_r1", "symmetric_coil", 12, "results/best_sym12_v2_drifted_r1_Q12_1454.txt", 1434, 1450),
        ("p1_sym13_2874_ils", "symmetric_coil", 13, "results/best_sym13_Q13_2874.txt", 2830, 2870),
        ("p1_sym13_2878_ils", "symmetric_coil", 13, "results/best_sym13_v2_Q13_2878.txt", 2830, 2870),
        ("p1_sym13_2878_lift", "symmetric_coil", 13, "results/lift_sym13_from_lift_Q13_2878.txt", 2830, 2870),
        ("p1_sym13_2882_lift", "symmetric_coil", 13, "results/lift_sym13_from_ils_Q13_2882.txt", 2830, 2870),
        ("p1_sym13_2886_record", "symmetric_coil", 13, "results/best_sym13_from2882_Q13_2886.txt", 2830, 2870),
        ("p1_sym13_2886_drifted_r0", "symmetric_coil", 13, "results/best_sym13_2886_drifted_r0_Q13_2886.txt", 2830, 2870),
        ("p1_sym13_2886_drifted_r1", "symmetric_coil", 13, "results/best_sym13_2886_drifted_r1_Q13_2886.txt", 2830, 2870),
        # p2: Q14 Coil 5854 & Q14 Snake 5854 Drifted Inequivalent Records
        ("p2_coil14_5854_drifted_r0", "coil", 14, "results/best_co14_drifted_r0_Q14_5854.txt", 5750, 5854),
        ("p2_coil14_5854_drifted_r1", "coil", 14, "results/best_co14_drifted_r1_Q14_5854.txt", 5750, 5854),
        ("p2_coil14_5854_drifted_r2", "coil", 14, "results/best_co14_drifted_r2_Q14_5854.txt", 5750, 5854),
        ("p2_snake14_5854_drifted_r0", "snake", 14, "results/best_sn14_drifted_r0_Q14_5854.txt", 5850, 5854),
        ("p2_snake14_5854_drifted_r1", "snake", 14, "results/best_sn14_drifted_r1_Q14_5854.txt", 5850, 5854),
        ("p2_snake14_5854_drifted_r2", "snake", 14, "results/best_sn14_drifted_r2_Q14_5854.txt", 5850, 5854),
        # p3: New Drifted Inequivalent Equal-Record Witnesses (Q10..Q13)
        ("p3_coil10_374_drifted_r0", "coil", 10, "results/p3_co10_drifted_r0_Q10_374.txt", 374, 374),
        ("p3_coil11_740_drifted_r0", "coil", 11, "results/p3_co11_drifted_r0_Q11_740.txt", 740, 740),
        ("p3_coil12_1468_drifted_r0", "coil", 12, "results/p3_co12_drifted_r0_Q12_1468.txt", 1468, 1468),
        ("p3_coil13_2930_drifted_r0", "coil", 13, "results/p3_co13_drifted_r0_Q13_2930.txt", 2930, 2930),
        ("p3_coil13_2928_lift", "coil", 13, "results/test_co13_Q13_2928.txt", 2926, 2930),
        ("p3_snake11_750_drifted_r0", "snake", 11, "results/p3_sn11_drifted_r0_Q11_750.txt", 750, 750),
        ("p3_snake12_1480_drifted_r0", "snake", 12, "results/p3_sn12_drifted_r0_Q12_1480.txt", 1480, 1480),
        ("p3_snake13_2946_drifted_r0", "snake", 13, "results/p3_sn13_drifted_r0_Q13_2946.txt", 2946, 2946),
    ]

    our_summary = {}
    seen_our_hashes = set()
    for name, kind, n, path, pub_rec, pr_rec in our_files:
        steps = vsc.parse_input(path)
        v = vsc.verify_steps(steps, expected_n=n)
        is_coil = (v["type"] == "coil")
        if kind == "symmetric_coil":
            assert v["is_symmetric"], f"Expected symmetric coil in {name}"
        ch, cpref = canon_hash(steps, is_coil)
        _, bank_hashes = get_bank(n, kind, v["length"])
        ineq_pub = (ch not in bank_hashes)
        ineq_cg = (ch not in cg_hashes)
        distinct_prev = (ch not in seen_our_hashes)
        seen_our_hashes.add(ch)
        L = v["length"]
        gp = L - pub_rec
        gc = L - pr_rec
        r = {
            "path": path,
            "valid": v["valid"],
            "n": v["n"],
            "kind": kind,
            "type": v["type"],
            "is_symmetric": v["is_symmetric"],
            "length": L,
            "public_baseline": pub_rec,
            "cg_branch_baseline": pr_rec,
            "gain_vs_public": gp,
            "gain_vs_cg_branch": gc,
            "canonical_hash": ch,
            "canonical_prefix": cpref,
            "dcv": list(v["invariants"]["dcv"]),
            "gap_spectrum_hash": v["invariants"]["gap_spectrum_hash"],
            "inequiv_vs_public": ineq_pub,
            "inequiv_vs_cg_branches": ineq_cg,
            "distinct_from_prev_our": distinct_prev,
        }
        our_summary[name] = r
        print(
            f"OUR {name:28s}: valid={r['valid']} L={L:4d} (pub={pub_rec:4d} {gp:+4d}, PR={pr_rec:4d} {gc:+3d}) "
            f"ineq_pub={ineq_pub} ineq_cg={ineq_cg} chash={ch}"
        )

    out_data = {
        "cg_branches_audit": cg_summary,
        "wave3_new_records_and_witnesses": our_summary,
    }
    with open("results/summary.json", "w") as f:
        json.dump(out_data, f, indent=2)
    print("Saved results/summary.json successfully!")


if __name__ == "__main__":
    main()
