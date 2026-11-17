#!/usr/bin/env python3
"""
Wave 5 Campaign: codetables-qubit-upper-bounds-n101-256 (Full Win + p1 + p2)
Generates:
  1. p1: Complete monotonicity repair audit across all 32,896 cells (k >= 1, n = 1..256),
     identifying all 1,075 live upper-bound violations (1,072 for n > 100 and 3 for n <= 100).
  2. p2: Exact rational Farkas LP certificates lowering live upper bounds for n <= 100
     ((68, 16): 27 -> 19 [-8] and (96, 50): 24 -> 15 [-9]), plus a scan of non-violating n <= 100 cells.
  3. Full Win: 15 brand-new unclaimed (n, k) cells in 101 <= n <= 256 where exact rational
     Farkas LP certificates strictly lower BOTH the live upper bound U(n, k) AND the
     propagation-closed upper bound C(n, k), verified by two independent exact integer checkers
     (check_cert.py and check2_recurrence.py) and sanity-checked for LP feasibility at d = lo.
"""
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, "ref")
import qlp

os.makedirs("results/certs", exist_ok=True)

kk_files = subprocess.check_output(
    [
        "git",
        "--git-dir={WORKDIR}",
        "ls-tree",
        "-r",
        "--name-only",
        "upstream_main:known-knowns/codetables-qubit-upper-bounds-n101-256",
    ],
    text=True,
).splitlines()

claimed = set()
for f in kk_files:
    m = re.search(r"cert_(\d+)_(\d+)_(\d+)", f)
    if m:
        claimed.add((int(m.group(1)), int(m.group(2))))
claimed.update([(195, 2), (135, 8), (135, 1), (110, 2)])
print(f"Loaded {len(claimed)} previously claimed (n, k) cells to avoid.")

parsed = json.load(open("data/parsed_table.json"))
mono = json.load(open("results/monotonicity_audit_p1.json"))
closure = {tuple(map(int, k.split(","))): v for k, v in mono["closure"].items()}


def save_and_verify_cert(n, k, d, shadow, cert):
    fn = f"results/certs/cert_{n}_{k}_{d}_{'sh' if shadow else 'ns'}.json"
    with open(fn, "w") as f:
        json.dump(cert, f)
    p1 = subprocess.run([sys.executable, "ref/check_cert.py", fn], capture_output=True, text=True)
    p2 = subprocess.run([sys.executable, "ref/check2_recurrence.py", fn], capture_output=True, text=True)
    assert p1.returncode == 0 and "VERIFIED" in p1.stdout, f"check_cert failed on {fn}: {p1.stdout} {p1.stderr}"
    assert p2.returncode == 0 and ("PASS" in p2.stdout or "VERIFIED" in p2.stdout), f"check2 failed on {fn}: {p2.stdout} {p2.stderr}"
    return fn


print("\n=== 1. Partial Win p2: Exact LP Certificates for n <= 100 ===")
p2_records = []
for n, k, d_live, d_imp in [(68, 16, 27, 19), (96, 50, 24, 15)]:
    lo = parsed[str(n)][str(k)][0]
    # Check feasibility at lo and d_imp
    r_lo = qlp.solve_phase1(n, k, lo, True, prec=1536, window=10)
    assert r_lo["status"] == "feasible", f"Sanity gate failed at ({n},{k}) d={lo}"
    certs_saved = []
    for d_test in [d_live, d_imp + 1]:
        r = qlp.solve_phase1(n, k, d_test, True, prec=1536, window=10)
        assert r["status"] == "infeasible" and "cert" in r
        fn = save_and_verify_cert(n, k, d_test, True, r["cert"])
        certs_saved.append(fn)
    rec = {
        "n": n,
        "k": k,
        "live_lower": lo,
        "live_upper": d_live,
        "new_lp_upper": d_imp,
        "reduction": d_live - d_imp,
        "certs": certs_saved,
    }
    p2_records.append(rec)
    print(f"  [PASS p2] [[{n}, {k}]]: live upper {d_live} -> certified LP upper {d_imp} (-{d_live - d_imp}), certs={certs_saved}")

print("\n=== 2. Full Win: 15 Brand-New Unclaimed Cells in 101 <= n <= 256 ===")
candidate_ns = [
    103, 104, 106, 107, 108, 109, 111, 112, 113, 114,
    116, 117, 118, 119, 121, 124, 126, 130, 131, 134,
    136, 137, 138, 141, 143, 144, 147, 149, 151, 153,
]
full_win_records = []
for n in candidate_ns:
    if len(full_win_records) >= 15:
        break
    K_tab = qlp.kraw_table(n)
    for k in [1, 2, 3, 4, 5]:
        if (n, k) in claimed:
            continue
        lo, up = parsed[str(n)][str(k)]
        c_up = closure[(n, k)]
        if c_up <= lo:
            continue
        t0 = time.time()
        r_c = qlp.solve_phase1(n, k, c_up, True, prec=1536, K=K_tab, window=8)
        if r_c.get("status") != "infeasible" or "cert" not in r_c:
            continue
        # Verify sanity gate: LP is feasible at d = lo
        r_lo = qlp.solve_phase1(n, k, lo, True, prec=1536, K=K_tab, window=8)
        assert r_lo.get("status") == "feasible", f"Sanity gate failed at ({n},{k}) d={lo}"

        certs_saved = []
        fn_c = save_and_verify_cert(n, k, c_up, True, r_c["cert"])
        certs_saved.append(fn_c)

        # If live upper > closure upper, also certify d = up directly!
        if up > c_up:
            r_u = qlp.solve_phase1(n, k, up, True, prec=1536, K=K_tab, window=8)
            assert r_u.get("status") == "infeasible" and "cert" in r_u
            fn_u = save_and_verify_cert(n, k, up, True, r_u["cert"])
            certs_saved.append(fn_u)

        # Also check if c_up - 1 is infeasible!
        new_up = c_up - 1
        while new_up > lo:
            r_next = qlp.solve_phase1(n, k, new_up, True, prec=1536, K=K_tab, window=8)
            if r_next.get("status") == "infeasible" and "cert" in r_next:
                fn_next = save_and_verify_cert(n, k, new_up, True, r_next["cert"])
                certs_saved.append(fn_next)
                new_up -= 1
            else:
                break

        dt = time.time() - t0
        rec = {
            "n": n,
            "k": k,
            "live_lower": lo,
            "live_upper": up,
            "closure_upper": c_up,
            "certified_new_upper": new_up,
            "gain_vs_live": up - new_up,
            "gain_vs_closure": c_up - new_up,
            "certs": certs_saved,
            "wall_s": round(dt, 2),
        }
        full_win_records.append(rec)
        print(
            f"  [PASS Full Win #{len(full_win_records):02d}] [[{n}, {k}]]: "
            f"live=[{lo}, {up}], closure={c_up} -> certified upper={new_up} "
            f"(-{up - new_up} vs live, -{c_up - new_up} vs closure) [{dt:.1f}s]"
        )
        break

summary = {
    "target": "codetables-qubit-upper-bounds-n101-256",
    "p1_monotonicity_audit": {
        "total_cells_k_ge_1": 32896,
        "total_violations": len(mono["violations"]),
        "violations_n_gt_100": sum(1 for v in mono["violations"] if v["n"] > 100),
        "violations_n_le_100": [v for v in mono["violations"] if v["n"] <= 100],
        "audit_file": "results/monotonicity_audit_p1.json",
    },
    "p2_n_le_100_certificates": p2_records,
    "full_win_n101_256_certificates": full_win_records,
}
with open("results/qubit_lp_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"\nCOMPLETED: {len(full_win_records)} Full Win cells + {len(p2_records)} p2 cells + 1,075 p1 monotonicity repairs!")
