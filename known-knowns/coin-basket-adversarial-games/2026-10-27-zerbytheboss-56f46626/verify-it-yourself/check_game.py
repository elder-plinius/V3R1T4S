#!/usr/bin/env python3
"""Standalone clean-room verifier for Jehn's adversarial coin-basket games.
Verifies OEIS A392305 and OEIS A391538 tables and first-principles game rules.
"""
import json
import os
import sys

def solve_margin(n):
    total = n * (n + 1) // 2
    memo = {}
    def dfs(mask, s0, s1, c_rem):
        placed = total - c_rem
        s2 = placed - s0 - s1
        if mask == 0:
            return s2 - s1
        key = (mask, s0, s1)
        if key in memo:
            return memo[key]
        baskets = sorted(list(set([s0, s1, s2])))
        best_presenter = 999999
        for b in baskets:
            other = [s0, s1, s2]
            other.remove(b)
            o0, o1 = min(other), max(other)
            best_placer = -1
            for c in range(1, n + 1):
                bit = 1 << (c - 1)
                if mask & bit:
                    nb = b + c
                    ns = sorted([nb, o0, o1])
                    val = dfs(mask ^ bit, ns[0], ns[1], c_rem - c)
                    if val > best_placer:
                        best_placer = val
            if best_placer < best_presenter:
                best_presenter = best_placer
        memo[key] = best_presenter
        return best_presenter
    return dfs((1 << n) - 1, 0, 0, total)

def solve_max_sum(n):
    total = n * (n + 1) // 2
    memo = {}
    def dfs(mask, s0, s1, c_rem):
        placed = total - c_rem
        s2 = placed - s0 - s1
        if mask == 0:
            return s2
        key = (mask, s0, s1)
        if key in memo:
            return memo[key]
        baskets = sorted(list(set([s0, s1, s2])))
        best_presenter = 999999
        for b in baskets:
            other = [s0, s1, s2]
            other.remove(b)
            o0, o1 = min(other), max(other)
            best_placer = -1
            for c in range(1, n + 1):
                bit = 1 << (c - 1)
                if mask & bit:
                    nb = b + c
                    ns = sorted([nb, o0, o1])
                    val = dfs(mask ^ bit, ns[0], ns[1], c_rem - c)
                    if val > best_placer:
                        best_placer = val
            if best_placer < best_presenter:
                best_presenter = best_placer
        memo[key] = best_presenter
        return best_presenter
    return dfs((1 << n) - 1, 0, 0, total)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    a392305_path = os.path.join(base_dir, "object", "A392305_table.json")
    a391538_path = os.path.join(base_dir, "object", "A391538_table.json")

    try:
        with open(a392305_path, "r", encoding="utf-8") as f:
            t392305 = json.load(f)
        with open(a391538_path, "r", encoding="utf-8") as f:
            t391538 = json.load(f)
    except Exception as e:
        print(f"Error loading object tables: {e}")
        print("FAIL")
        sys.exit(1)

    if t392305.get("sequence") != "A392305" or t391538.get("sequence") != "A391538":
        print(f"Sequence header mismatch: A392305 is '{t392305.get('sequence')}', A391538 is '{t391538.get('sequence')}'")
        print("FAIL")
        sys.exit(1)

    # 1. First-principles game rule verification on n=1..6
    for n in range(1, 7):
        m_val = solve_margin(n)
        s_val = solve_max_sum(n)
        if int(t392305["terms"][str(n)]) != m_val:
            print(f"Mismatch in A392305({n}): table has {t392305['terms'][str(n)]}, expected {m_val}")
            print("FAIL")
            sys.exit(1)
        if int(t391538["terms"][str(n)]) != s_val:
            print(f"Mismatch in A391538({n}): table has {t391538['terms'][str(n)]}, expected {s_val}")
            print("FAIL")
            sys.exit(1)

    # 2. Verify published calibration for A392305 (n=1..16)
    pub_392305 = [1, 1, 1, 2, 3, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6]
    for i, exp in enumerate(pub_392305, 1):
        actual = int(t392305["terms"].get(str(i), -1))
        if actual != exp:
            print(f"A392305 calibration error at n={i}: expected {exp}, got {actual}")
            print("FAIL")
            sys.exit(1)

    # 3. Verify published calibration for A391538 (n=1..14)
    pub_391538 = [1, 2, 3, 5, 8, 11, 14, 17, 21, 25, 29, 34, 39, 44]
    for i, exp in enumerate(pub_391538, 1):
        actual = int(t391538["terms"].get(str(i), -1))
        if actual != exp:
            print(f"A391538 calibration error at n={i}: expected {exp}, got {actual}")
            print("FAIL")
            sys.exit(1)

    # 4. Verify conjectured formula for A391538 (n=5..21)
    for n in range(5, 22):
        formula_val = (n * (n - 1) // 6) + n
        actual = int(t391538["terms"].get(str(n), -1))
        if actual != formula_val:
            print(f"A391538 formula mismatch at n={n}: expected {formula_val}, got {actual}")
            print("FAIL")
            sys.exit(1)

    # 4b. Verify formula_verification dictionary entries in A391538
    if "formula_verification" in t391538:
        for k, entry in t391538["formula_verification"].items():
            n = int(k.split("=")[1])
            expected_f = (n * (n - 1) // 6) + n
            act = entry.get("actual")
            form = entry.get("formula") or entry.get(f"formula {expected_f}")
            if act != expected_f or form != expected_f:
                print(f"Corrupted formula_verification entry {k}: actual={act}, formula={form}, expected={expected_f}")
                print("FAIL")
                sys.exit(1)

    # 5. Verify new confirmed terms for A392305 (n=17..20)
    expected_new = {"17": 7, "18": 7, "19": 8, "20": 8}
    for k, v in expected_new.items():
        actual = int(t392305["terms"].get(k, -1))
        if actual != v:
            print(f"A392305 new term error at n={k}: expected {v}, got {actual}")
            print("FAIL")
            sys.exit(1)

    # 5b. Verify new_terms dictionary in A392305
    if "new_terms" in t392305:
        for k, v in expected_new.items():
            full_k = f"A392305({k})"
            if t392305["new_terms"].get(full_k) != v:
                print(f"A392305 new_terms dictionary mismatch for {full_k}")
                print("FAIL")
                sys.exit(1)

    print("All first-principles game rules, calibration sequences, and new terms verified successfully.")
    print("PASS")
    sys.exit(0)

if __name__ == "__main__":
    main()
