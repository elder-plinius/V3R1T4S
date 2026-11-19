import json
import glob
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

def main():
    subprocess.run([
        "clang++", "-O3", "-std=c++17", "-Idata/SorterHunter",
        "sn_optimizer.cpp", "data/SorterHunter/prefix_processor.cpp", "data/SorterHunter/hutils.cpp",
        "-o", "sn_optimizer"
    ], check=True)

    nets = json.load(open("data/all_networks.json"))
    pareto = {}
    for x in nets:
        pareto.setdefault(x["n"], []).append((x["size"], x["depth"]))

    def is_dominated(n, s, d):
        for s0, d0 in pareto.get(n, []):
            if s0 <= s and d0 <= d:
                return True
        return False

    def max_win_size_at_depth(n, target_d):
        pts = [s0 for s0, d0 in pareto.get(n, []) if d0 <= target_d]
        if not pts:
            return None
        return min(pts) - 1

    out_dir = "{TMP}/sn_gap_hunt_v2"
    os.makedirs(out_dir, exist_ok=True)

    jobs = []
    # Collect all low-crit / positive-slack depth-drop targets from {TMP}/sn_parents_v3
    target_tags = [
        # FULL_WIN (n=13..32)
        ("Sort_14_51_10", 14, 9, 51, 5000, 800000),
        ("Sort_LS_14_51_10", 14, 9, 51, 5000, 800000),
        ("Sort_13_45_10", 13, 9, 45, 5000, 800000),
        ("Sort_15_56_10", 15, 9, 56, 8000, 800000),
        ("Sort_16_60_10", 16, 9, 60, 10000, 800000),
        ("Sort_17_71_12", 17, 11, 71, 15000, 800000),
        ("Sort_LS_17_71_12", 17, 11, 71, 15000, 800000),
        ("Sort_17_72_11", 17, 10, 73, 15000, 800000),
        ("Sort_18_77_12", 18, 11, 77, 20000, 800000),
        ("Sort_LS_18_77_12", 18, 11, 77, 20000, 800000),
        ("Sort_19_85_12", 19, 11, 86, 25000, 800000),
        ("Sort_LS_19_85_12", 19, 11, 86, 25000, 800000),
        ("Sort_20_91_12", 20, 11, 92, 30000, 800000),
        ("Sort_LS_20_91_12", 20, 11, 92, 30000, 800000),
        ("N21L99D15", 21, 14, 99, 25000, 800000),
        ("Sort_LS_21_99_15", 21, 14, 99, 25000, 800000),
        ("N21L100D12", 21, 14, 99, 25000, 800000),
        ("Sort_22_106_13", 22, 12, 106, 35000, 800000),
        ("Sort_LS_22_106_13", 22, 12, 106, 35000, 800000),
        ("Sort_23_114_14", 23, 13, 114, 40000, 800000),
        ("Sort_LS_23_114_14", 23, 13, 114, 40000, 800000),
        ("Sort_23_115_13", 23, 12, 115, 40000, 800000),
        ("Sort_24_120_13", 24, 12, 121, 45000, 800000),
        ("Sort_LS_24_120_13", 24, 12, 121, 45000, 800000),
        ("N25L130D15", 25, 14, 130, 50000, 800000),
        ("Sort_LS_25_130_15", 25, 14, 130, 50000, 800000),
        ("N25L131D13", 25, 14, 130, 50000, 800000),
        ("Sort_26_139_14", 26, 13, 140, 60000, 800000),
        ("Sort_LS_26_139_14", 26, 13, 140, 60000, 800000),
        ("Sort_LS_26_138_15", 26, 14, 138, 60000, 800000),
        ("N27L147D16", 27, 15, 147, 60000, 800000),
        ("Sort_LS_27_147_16", 27, 15, 147, 60000, 800000),
        ("N27L148D14", 27, 13, 151, 60000, 800000),
        ("N27L148D14", 27, 15, 147, 60000, 800000),
        ("Sort_28_155_14", 28, 13, 158, 70000, 800000),
        ("Sort_LS_28_155_14", 28, 13, 158, 70000, 800000),
        ("Sort_29_164_15", 29, 14, 165, 70000, 800000),
        ("Sort_LS_29_164_15", 29, 14, 165, 70000, 800000),
        # PARTIAL_WIN_P1 (n=33..64)
        ("Sort_34_211_16", 34, 15, 212, 80000, 600000),
        ("Sort_34_210_16", 34, 15, 212, 80000, 600000),
        ("Sort_34_209_17", 34, 16, 209, 80000, 600000),
        ("Sort_LS_34_209_17", 34, 16, 209, 80000, 600000),
        ("Sort_35_220_17", 35, 16, 220, 80000, 600000),
        ("Sort_LS_35_220_17", 35, 16, 220, 80000, 600000),
        ("Sort_36_227_18", 36, 17, 227, 80000, 600000),
        ("Sort_LS_36_227_18", 36, 17, 227, 80000, 600000),
        ("Sort_37_240_17", 37, 16, 242, 80000, 600000),
        ("Sort_LS_37_240_17", 37, 16, 242, 80000, 600000),
        ("Sort_38_250_17", 38, 16, 253, 80000, 600000),
        ("Sort_LS_38_250_17", 38, 16, 253, 80000, 600000),
        ("Sort_39_259_17", 39, 16, 262, 80000, 600000),
        ("Sort_LS_39_259_17", 39, 16, 262, 80000, 600000),
        ("Sort_40_265_17", 40, 16, 268, 80000, 600000),
        ("Sort_LS_40_265_17", 40, 16, 268, 80000, 600000),
        ("Sort_41_282_18", 41, 17, 282, 90000, 600000),
        ("Sort_LS_41_282_19", 41, 18, 281, 90000, 600000),
        ("Sort_42_291_18", 42, 17, 293, 90000, 600000),
        ("Sort_LS_42_291_18", 42, 17, 293, 90000, 600000),
        ("N43L303D19", 43, 18, 303, 90000, 600000),
        ("Sort_LS_43_303_19", 43, 18, 303, 90000, 600000),
        ("N44L309D19", 44, 18, 310, 90000, 600000),
        ("Sort_LS_44_309_19", 44, 18, 310, 90000, 600000),
        ("Sort_LS_45_324_19", 45, 18, 323, 90000, 600000),
        ("Sort_LS_46_332_19", 46, 18, 331, 90000, 600000),
        ("N47L340D19", 47, 18, 340, 90000, 600000),
        ("Sort_LS_47_340_19", 47, 18, 340, 90000, 600000),
        ("N48L346D19", 48, 18, 346, 90000, 600000),
        ("Sort_LS_48_346_19", 48, 18, 346, 90000, 600000),
        ("N49L365D21", 49, 20, 368, 90000, 600000),
        ("Sort_LS_49_365_21", 49, 20, 368, 90000, 600000),
        ("N50L376D21", 50, 20, 377, 90000, 600000),
        ("Sort_LS_50_376_21", 50, 20, 377, 90000, 600000),
        ("N50L378D20", 50, 19, 380, 90000, 600000),
        ("N53L411D22", 53, 21, 411, 90000, 600000),
        ("Sort_LS_53_411_22", 53, 21, 411, 90000, 600000),
        ("N53L412D21", 53, 20, 413, 90000, 600000),
        ("N61L497D22", 61, 21, 497, 90000, 600000),
        ("Sort_LS_61_497_22", 61, 21, 497, 90000, 600000),
    ]

    for tag, n, m_dp, m_sz, t_sing, iters in target_tags:
        in_p = f"{TMP}/sn_parents_v3/{tag}.txt"
        if os.path.exists(in_p):
            jobs.append((in_p, t_sing, iters, m_dp, m_sz, 777, f"{tag}_to_{m_sz}D{m_dp}"))

    # Also add reduced networks from {TMP}/sn_opt_v3 with low crit for N=17, 19, 23, 27, 28, 38, 43
    red_globs = [
        ("{TMP}/sn_opt_v3/opt_cand_*_n17_s73_d11_i1.txt", 17, 10, 73, 15000, 600000, "red_N17_73D11"),
        ("{TMP}/sn_opt_v3/opt_cand_*_n19_s86_d12_i1.txt", 19, 11, 86, 25000, 600000, "red_N19_86D12"),
        ("{TMP}/sn_opt_v3/opt_cand_*_n23_s115_d13_i1.txt", 23, 12, 115, 40000, 600000, "red_N23_115D13"),
        ("{TMP}/sn_opt_v3/opt_cand_*_n27_s148_d14_i1.txt", 27, 13, 151, 60000, 600000, "red_N27_150D14"),
        ("{TMP}/sn_opt_v3/opt_cand_*_n28_s155_d14_i1.txt", 28, 13, 158, 60000, 600000, "red_N28_157D14"),
        ("{TMP}/sn_opt_v3/opt_cand_*_n38_s249_d17_i1.txt", 38, 16, 253, 80000, 600000, "red_N38_250D17"),
        ("{TMP}/sn_opt_v3/opt_cand_*_n43_s303_d19_i1.txt", 43, 18, 303, 90000, 600000, "red_N43_303D19"),
    ]
    for pat, n, m_dp, m_sz, t_sing, iters, lbl in red_globs:
        for idx, m_in in enumerate(sorted(glob.glob(pat))[:2]):
            jobs.append((m_in, t_sing, iters, m_dp, m_sz, 888 + idx, f"{lbl}_{idx}"))

    print(f"Launching {len(jobs)} depth-ratchet & size-ratchet jobs across 12 workers...")

    def run_job(job):
        in_p, t_sing, iters, m_dp, m_sz, sd, lbl = job
        out_p = os.path.join(out_dir, f"res_{lbl}.txt")
        p = subprocess.run([
            "./sn_optimizer", in_p, str(t_sing), out_p, str(iters), str(m_dp), str(m_sz), str(sd)
        ], capture_output=True, text=True)
        out_lines = [l.strip() for l in p.stdout.splitlines() if l.strip()]
        new_pareto = [l for l in out_lines if "NEW PARETO" in l or "iter=" in l]
        with open(out_p) as f:
            first = f.readline().split()
            n, fs = int(first[0]), int(first[1])
            ces = [tuple(map(int, line.split())) for line in f if line.strip()]
        dp = [0] * n
        for u, v in ces:
            nd = max(dp[u], dp[v]) + 1
            dp[u] = dp[v] = nd
        fd = max(dp) if dp else 0
        dom = is_dominated(n, fs, fd)
        return (dom, n, fs, fd, lbl, out_p, out_lines[-1] if out_lines else "", new_pareto)

    with ThreadPoolExecutor(max_workers=12) as ex:
        for dom, n, fs, fd, lbl, out_p, last_l, np_list in ex.map(run_job, jobs):
            if not dom or len(np_list) > 0:
                status = "*** WIN (NON-DOMINATED)! ***" if not dom else "prog"
                print(f"[{status}] {lbl}: N={n} final=({fs}, {fd}) | {last_l}")
                for nl in np_list[-6:]:
                    print(f"   -> {nl}")

if __name__ == "__main__":
    main()
