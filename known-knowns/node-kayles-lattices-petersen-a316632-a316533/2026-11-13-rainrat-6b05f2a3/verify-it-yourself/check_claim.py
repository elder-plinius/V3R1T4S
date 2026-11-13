#!/usr/bin/env python3
"""Standalone verifier for 2026-11-13-rainrat-6b05f2a3."""

import json
import os
import re
import subprocess
import sys
import tempfile


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def check(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)


def lattice_adj(m: int, n: int) -> list[int]:
    adj = [0] * (m * n)
    for r in range(m):
        for c in range(n):
            u = r * n + c
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                rr, cc = r + dr, c + dc
                if 0 <= rr < m and 0 <= cc < n:
                    adj[u] |= 1 << (rr * n + cc)
    return adj


def literal_nimber(adj: list[int]) -> int:
    from functools import lru_cache
    n = len(adj)
    closed = [adj[i] | (1 << i) for i in range(n)]

    def comps(mask: int) -> list[int]:
        res = []
        rem = mask
        while rem:
            lsb = rem & -rem
            c = 0
            stk = lsb
            while stk:
                b = stk & -stk
                stk ^= b
                if not (c & b):
                    c |= b
                    stk |= (adj[b.bit_length() - 1] & rem) & ~c
            res.append(c)
            rem ^= c
        return res

    @lru_cache(maxsize=None)
    def sg(mask: int) -> int:
        if mask == 0:
            return 0
        cs = comps(mask)
        if len(cs) > 1:
            ans = 0
            for c in cs:
                ans ^= sg(c)
            return ans
        seen = set()
        rem = mask
        while rem:
            b = rem & -rem
            rem ^= b
            seen.add(sg(mask & ~closed[b.bit_length() - 1]))
        g = 0
        while g in seen:
            g += 1
        return g

    return sg((1 << n) - 1)


def parse_nk_calibrate(out: str) -> tuple[dict[int, int], dict[int, int], dict[str, int]]:
    a316632, a316533, t1 = {}, {}, {}
    sec = None
    for line in out.splitlines():
        if line.startswith("A316632"):
            sec = "a316632"
        elif line.startswith("A316533"):
            sec = "a316533"
        elif line.startswith("Table 1"):
            sec = "t1"
        else:
            if sec == "a316632":
                m = re.search(r"\bn=(\d+)\s+G=(\d+)\b", line)
                if m:
                    a316632[int(m.group(1))] = int(m.group(2))
            elif sec == "a316533":
                m = re.search(r"\bn=(\d+)\s+G=(\d+)\b", line)
                if m:
                    a316533[int(m.group(1))] = int(m.group(2))
            elif sec == "t1":
                m = re.search(r"\bL_\{(\d+x\d+)\}\s+G=(\d+)\b", line)
                if m:
                    t1[f"L_{m.group(1)}"] = int(m.group(2))
    return a316632, a316533, t1


def main() -> int:
    try:
        with open("object/table1_cells.json") as f:
            obj = json.load(f)
    except Exception as exc:
        fail(f"Cannot load object/table1_cells.json: {exc}")

    check(isinstance(obj, dict), "Root JSON must be an object")
    for req_key in ("calibration", "newly_resolved_table1_cells"):
        check(req_key in obj and isinstance(obj[req_key], dict), f"Missing or invalid key: {req_key}")

    cal = obj["calibration"]
    for req_cal in ("A316632_1_to_17", "A316533_odd_5_to_25", "table1_shaded"):
        check(req_cal in cal, f"Missing calibration key: {req_cal}")

    a316632_exp = cal["A316632_1_to_17"]
    a316533_odd_exp = cal["A316533_odd_5_to_25"]
    t1_shaded_exp = cal["table1_shaded"]
    check(isinstance(a316632_exp, list) and len(a316632_exp) == 17, "Invalid A316632_1_to_17")
    check(isinstance(a316533_odd_exp, list) and len(a316533_odd_exp) == 11, "Invalid A316533_odd_5_to_25")
    check(isinstance(t1_shaded_exp, dict) and set(t1_shaded_exp.keys()) == {"L_5x5", "L_5x6", "L_5x7"}, "Invalid table1_shaded")

    cells = obj["newly_resolved_table1_cells"]
    expected_keys = {"L_5x8", "L_6x7", "L_5x9", "L_7x7", "L_5x10"}
    check(set(cells.keys()) == expected_keys, f"Unexpected keys: {set(cells.keys())}")

    # 1. Literal Python definition check on small grids
    for n, expected in enumerate([2, 1, 1, 0, 3], start=1):
        check(literal_nimber(lattice_adj(3, n)) == expected, f"Literal check failed on L_3x{n}")

    with tempfile.TemporaryDirectory() as tmp:
        nk_bin = os.path.join(tmp, "nk_solver")
        pn_bin = os.path.join(tmp, "pn_solver")
        subprocess.run(["g++", "-O3", "-march=native", "-std=c++20", "how-we-built-it/nk_solver.cpp", "-o", nk_bin], check=True)
        subprocess.run(["g++", "-O3", "-march=native", "-std=c++20", "how-we-built-it/pn_solver.cpp", "-o", pn_bin], check=True)

        # 2. Check pn_solver calibration: A316632(1..17), A316533(5..26 all), shaded Table 1 + transposes
        for n, exp_g in enumerate(a316632_exp, start=1):
            out = subprocess.check_output([pn_bin, "grid", "3", str(n)], text=True)
            m = re.search(r"G=(\d+)", out)
            check(bool(m) and int(m.group(1)) == exp_g, f"pn_solver A316632({n}) mismatch: {out}")

        for n in range(5, 27):
            exp_g = 0 if n % 2 == 0 else a316533_odd_exp[(n - 5) // 2]
            out = subprocess.check_output([pn_bin, "gp", str(n)], text=True)
            m = re.search(r"G=(\d+)", out)
            check(bool(m) and int(m.group(1)) == exp_g, f"pn_solver A316533({n}) mismatch: {out}")

        for key, exp_g in t1_shaded_exp.items():
            mm, nn = map(int, key.split("_")[1].split("x"))
            out = subprocess.check_output([pn_bin, "grid", str(mm), str(nn)], text=True)
            m = re.search(r"G=(\d+)", out)
            check(bool(m) and int(m.group(1)) == exp_g, f"pn_solver {key} mismatch: {out}")

        # 3. Check nk_solver calibration (section-aware) + even A316533(6..26) + transposes
        nk_cal = subprocess.check_output([nk_bin, "calibrate"], text=True)
        nk_a316632, nk_a316533, nk_t1 = parse_nk_calibrate(nk_cal)
        for n, exp_g in enumerate(a316632_exp, start=1):
            check(nk_a316632.get(n) == exp_g, f"nk_solver A316632({n}) mismatch: got {nk_a316632.get(n)}, expected {exp_g}")
        for idx, exp_g in enumerate(a316533_odd_exp):
            n = 5 + 2 * idx
            check(nk_a316533.get(n) == exp_g, f"nk_solver A316533({n}) mismatch: got {nk_a316533.get(n)}, expected {exp_g}")
        for n in range(6, 27, 2):
            out = subprocess.check_output([nk_bin, "gp", str(n)], text=True)
            m = re.search(r"G=(\d+)", out)
            check(bool(m) and int(m.group(1)) == 0, f"nk_solver A316533({n}) mismatch: {out}")
        for key, exp_g in t1_shaded_exp.items():
            check(nk_t1.get(key) == exp_g, f"nk_solver {key} mismatch: got {nk_t1.get(key)}, expected {exp_g}")

        # 4. Check all 5 claimed Table 1 cells with BOTH solvers against object/table1_cells.json
        for key in ["L_5x8", "L_6x7", "L_5x9", "L_7x7", "L_5x10"]:
            entry = cells[key]
            check(isinstance(entry, dict) and "nimber" in entry and "outcome" in entry, f"Invalid entry for {key}")
            claimed_g = entry["nimber"]
            claimed_out = entry["outcome"]
            check(isinstance(claimed_g, int) and claimed_g >= 0, f"Invalid nimber for {key}")
            expected_out = "second_player_win" if claimed_g == 0 else "first_player_win"
            check(claimed_out == expected_out, f"Outcome mismatch for {key}: {claimed_out} != {expected_out}")

            mm, nn = map(int, key.split("_")[1].split("x"))
            out_nk = subprocess.check_output([nk_bin, "grid", str(mm), str(nn)], text=True)
            out_pn = subprocess.check_output([pn_bin, "grid", str(mm), str(nn)], text=True)
            g_nk = int(re.search(r"G=(\d+)", out_nk).group(1))
            g_pn = int(re.search(r"G=(\d+)", out_pn).group(1))
            check(g_nk == claimed_g and g_pn == claimed_g, f"{key}: nk={g_nk}, pn={g_pn}, claimed={claimed_g}")
            print(f"VERIFIED {key}: G={claimed_g} ({claimed_out}) [nk_solver == pn_solver]")

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
