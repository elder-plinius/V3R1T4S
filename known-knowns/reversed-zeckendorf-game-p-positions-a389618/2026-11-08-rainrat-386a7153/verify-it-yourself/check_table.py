#!/usr/bin/env python3
"""Standalone verifier for object/reversed_zeckendorf_n2_250.tsv (Python >= 3.9 stdlib only).

Checks performed:
1. Format & domain: header 'n\\twinner\\tedges\\tvertices' and 249 contiguous rows n = 2..250.
2. Exact DAG count identities (PROVED-HERE) for all 2 <= n <= 250:
   - vertices(n) == A003107(n)
   - edges(n)    == sum_{i=2}^{12} (A003107(n - F_i) + A003107(n - 2*F_i))
3. Published baseline calibration (KNOWN) for all 2 <= n <= 129:
   - All 49 P-positions (A389618) and 79 N-positions >= 2 (A389619) from Table A1 of arXiv:2309.12748v2,
     plus 14 explicit full-triple benchmark rows (including n=64, 65, 100, 129).
4. Theorem 1.1 of Batterman et al. (KNOWN) for all n = F_{i+1} + F_{i-2} <= 250 (3 <= i <= 10).
5. Literal game-definition BFS + normal-play evaluation for 2 <= n <= 35.
6. Extension winner integrity check for all 130 <= n <= 250 (30 P-positions, 91 N-positions; independently
   recomputed from scratch by both C++ solvers in verify-it-yourself/run_checks.sh).
7. Four built-in negative controls (flipping winner at n=7, flipping frontier winner at n=130,
   perturbing edges at n=8, and perturbing vertices at n=8).
"""

from collections import deque
from pathlib import Path
import sys

# Fibonacci indexing from Batterman et al. (arXiv:2309.12748v2):
# F_1 = 1, F_2 = 2, F_3 = 3, F_4 = 5, ..., F_12 = 233
F = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]

# Published P-positions (Player 2 wins) for 2 <= n <= 129 from Table A1 of arXiv:2309.12748v2 / OEIS A389618
PUBLISHED_P_LE_129 = {
    3, 5, 8, 9, 11, 13, 14, 19, 20, 23, 31, 34, 37, 39, 47, 49, 52, 53, 55,
    56, 60, 61, 64, 66, 70, 73, 74, 76, 79, 81, 84, 88, 89, 90, 92, 97, 98,
    102, 103, 108, 109, 112, 113, 114, 120, 121, 124, 128, 129,
}

# New P-positions (Player 2 wins) for 130 <= n <= 250 (extending OEIS A389618 a(50)..a(79);
# recomputed from scratch by both C++ solvers in verify-it-yourself/run_checks.sh)
EXTENSION_P_130_250 = {
    131, 136, 137, 142, 146, 152, 156, 157, 165, 166, 167, 173, 174, 175, 190,
    197, 205, 206, 212, 220, 221, 225, 228, 231, 233, 234, 238, 240, 244, 245,
}

# Published benchmark rows (n: (winner, edges, vertices)) from Table A1 of arXiv:2309.12748v2 and OEIS A389617
PUBLISHED_BENCHMARKS = {
    2: (1, 1, 2),
    3: (2, 2, 3),
    4: (1, 4, 4),
    5: (2, 7, 6),
    6: (1, 11, 8),
    7: (1, 16, 10),
    8: (2, 24, 14),
    9: (2, 32, 17),
    20: (2, 430, 134),
    35: (1, 3881, 892),
    64: (2, 63222, 10936),
    65: (1, 68351, 11744),
    100: (1, 674725, 97075),
    129: (2, 2945040, 384715),
}


def compute_a003107(max_n: int = 250) -> list[int]:
    dp = [0] * (max_n + 1)
    dp[0] = 1
    for f in F[1:]:
        for s in range(f, max_n + 1):
            dp[s] += dp[s - f]
    return dp


def zeckendorf_tuple(n: int) -> tuple[int, ...]:
    rem = n
    counts = [0] * len(F)
    for i in range(len(F) - 1, 0, -1):
        if F[i] <= rem:
            counts[i] = 1
            rem -= F[i]
    assert rem == 0
    return tuple(counts[1:])


def literal_moves(state: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Generate all legal Split and Combine moves directly from the definition in arXiv:2309.12748v2."""
    k = len(state)
    out = []
    # Split moves:
    # i = 1: replace one F_2 with 2 F_1
    if state[1] >= 1:
        nxt = list(state)
        nxt[1] -= 1
        nxt[0] += 2
        out.append(tuple(nxt))
    # i >= 2: replace one F_{i+1} with F_i + F_{i-1}
    for i in range(2, k):
        if state[i] >= 1:
            nxt = list(state)
            nxt[i] -= 1
            nxt[i - 1] += 1
            nxt[i - 2] += 1
            out.append(tuple(nxt))
    # Combine moves:
    # i = 2: replace F_1 + F_3 with 2 F_2
    if k >= 3 and state[0] >= 1 and state[2] >= 1:
        nxt = list(state)
        nxt[0] -= 1
        nxt[2] -= 1
        nxt[1] += 2
        out.append(tuple(nxt))
    # i > 2: replace F_{i-2} + F_{i+1} with 2 F_i
    for i in range(3, k):
        if state[i - 3] >= 1 and state[i] >= 1:
            nxt = list(state)
            nxt[i - 3] -= 1
            nxt[i] -= 1
            nxt[i - 1] += 2
            out.append(tuple(nxt))
    return out


def solve_literal(n: int) -> tuple[int, int, int]:
    """Literal BFS + normal-play retrograde evaluation from the Zeckendorf decomposition of n."""
    start = zeckendorf_tuple(n)
    adj: dict[tuple[int, ...], set[tuple[int, ...]]] = {start: set()}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in literal_moves(u):
            adj[u].add(v)
            if v not in adj:
                adj[v] = set()
                q.append(v)

    memo: dict[tuple[int, ...], bool] = {}

    def is_first_player_win(u: tuple[int, ...]) -> bool:
        if u in memo:
            return memo[u]
        res = any(not is_first_player_win(v) for v in adj[u])
        memo[u] = res
        return res

    winner = 1 if is_first_player_win(start) else 2
    vertices = len(adj)
    edges = sum(len(nbrs) for nbrs in adj.values())
    return winner, edges, vertices


def verify_table_rows(rows: dict[int, tuple[int, int, int]], dp: list[int], check_literal_up_to: int = 35) -> tuple[bool, str]:
    if set(rows.keys()) != set(range(2, 251)):
        return False, f"Expected contiguous n=2..250 (249 rows), got {len(rows)} rows"

    for n in range(2, 251):
        w, e, v = rows[n]
        if w not in (1, 2):
            return False, f"Invalid winner {w} at n={n}"
        expected_v = dp[n]
        if v != expected_v:
            return False, f"Vertex count mismatch at n={n}: got {v}, expected A003107({n})={expected_v}"
        expected_e = 0
        for i in range(2, 13):
            if n >= F[i]:
                expected_e += dp[n - F[i]]
            if n >= 2 * F[i]:
                expected_e += dp[n - 2 * F[i]]
        if e != expected_e:
            return False, f"Edge count mismatch at n={n}: got {e}, expected {expected_e}"

    for n in range(2, 130):
        w, e, v = rows[n]
        expected_w = 2 if n in PUBLISHED_P_LE_129 else 1
        if w != expected_w:
            return False, f"Published Table A1 / A389618 / A389619 winner mismatch at n={n}: got {w}, expected {expected_w}"

    for n in range(130, 251):
        w, e, v = rows[n]
        expected_w = 2 if n in EXTENSION_P_130_250 else 1
        if w != expected_w:
            return False, f"Extension winner mismatch at n={n}: got {w}, expected {expected_w}"

    for n, (exp_w, exp_e, exp_v) in PUBLISHED_BENCHMARKS.items():
        if rows[n] != (exp_w, exp_e, exp_v):
            return False, f"Published benchmark mismatch at n={n}: got {rows[n]}, expected {(exp_w, exp_e, exp_v)}"

    # Theorem 1.1 of Batterman et al.: Player 1 wins for n = F_{i+1} + F_{i-2} (i >= 3)
    for i in range(3, 11):
        n_thm = F[i + 1] + F[i - 2]
        if n_thm <= 250 and rows[n_thm][0] != 1:
            return False, f"Theorem 1.1 violation at i={i}, n={n_thm}: expected winner=1, got {rows[n_thm][0]}"

    for n in range(2, check_literal_up_to + 1):
        lit = solve_literal(n)
        if rows[n] != lit:
            return False, f"Literal game definition mismatch at n={n}: table={rows[n]}, literal={lit}"

    return True, "OK"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_table.py <path-to-tsv>")
        print("FAIL")
        return 1

    tsv_path = Path(sys.argv[1])
    if not tsv_path.is_file():
        print(f"Missing file: {tsv_path}")
        print("FAIL")
        return 1

    raw_lines = tsv_path.read_text(encoding="utf-8").splitlines()
    if len(raw_lines) != 250 or raw_lines[0] != "n\twinner\tedges\tvertices":
        print("Invalid header or line count (expected 250 lines starting with 'n\\twinner\\tedges\\tvertices')")
        print("FAIL")
        return 1

    rows: dict[int, tuple[int, int, int]] = {}
    for line_no, line in enumerate(raw_lines[1:], start=2):
        parts = line.split("\t")
        if len(parts) != 4 or any(p.strip() != p or not p.isdigit() for p in parts):
            print(f"Malformed TSV row at line {line_no}: {line!r}")
            print("FAIL")
            return 1
        n, w, e, v = map(int, parts)
        if n != line_no:
            print(f"Non-contiguous n at line {line_no}: expected {line_no}, got {n}")
            print("FAIL")
            return 1
        rows[n] = (w, e, v)

    dp = compute_a003107(250)
    ok, msg = verify_table_rows(rows, dp, check_literal_up_to=35)
    if not ok:
        print(f"Verification error: {msg}")
        print("FAIL")
        return 1

    # Negative controls: verify that corrupting a baseline winner, frontier winner, edge count, or vertex count is rejected
    bad_w_base = dict(rows)
    bad_w_base[7] = (3 - bad_w_base[7][0], bad_w_base[7][1], bad_w_base[7][2])
    if verify_table_rows(bad_w_base, dp, check_literal_up_to=10)[0]:
        print("Negative control 1 failed to reject flipped baseline winner at n=7")
        print("FAIL")
        return 1

    bad_w_ext = dict(rows)
    bad_w_ext[130] = (3 - bad_w_ext[130][0], bad_w_ext[130][1], bad_w_ext[130][2])
    if verify_table_rows(bad_w_ext, dp, check_literal_up_to=10)[0]:
        print("Negative control 2 failed to reject flipped frontier winner at n=130")
        print("FAIL")
        return 1

    bad_e = dict(rows)
    bad_e[8] = (bad_e[8][0], bad_e[8][1] + 1, bad_e[8][2])
    if verify_table_rows(bad_e, dp, check_literal_up_to=10)[0]:
        print("Negative control 3 failed to reject perturbed edge count at n=8")
        print("FAIL")
        return 1

    bad_v = dict(rows)
    bad_v[8] = (bad_v[8][0], bad_v[8][1], bad_v[8][2] + 1)
    if verify_table_rows(bad_v, dp, check_literal_up_to=10)[0]:
        print("Negative control 4 failed to reject perturbed vertex count at n=8")
        print("FAIL")
        return 1

    p_130_250 = [n for n in range(130, 251) if rows[n][0] == 2]
    n_130_250 = [n for n in range(130, 251) if rows[n][0] == 1]
    print(f"Verified 249 contiguous rows (n=2..250): V(250)={rows[250][2]}, E(250)={rows[250][1]}, W(250)={rows[250][0]}")
    print(f"Verified literal BFS on n=2..35, all 128 Table A1 rows (n=2..129), Theorem 1.1, and 4 negative controls (including frontier n=130).")
    print(f"Extension n=130..250: {len(p_130_250)} P-positions (A389618), {len(n_130_250)} N-positions (A389619).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
