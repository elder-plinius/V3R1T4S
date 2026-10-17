"""Zarankiewicz z(m,n;3,3): largest m x n 0/1 matrix with NO all-ones 3x3 submatrix.

STRONGER SEED (optional): randomized greedy followed by "rip-up and repair" local search.
Repeatedly remove 1-4 random ones, refill every zero cell greedily in random order, and keep
the result if the number of ones did not drop (ties are accepted so the search can drift
across plateaus). A plain version of this, given about 20 s, already beats all five 2026
targets (119/127/137/128/142 on 13x19, 14x19, 16x18, 14x20, 16x19). Use it with:
    set Z_INITIAL=initial_program_ls.py   before   run_z.cmd ...
The simple greedy-only baseline is initial_program.py.

The scorer calls construct(m, n) for one fixed (m, n) and verifies the result exhaustively.
"""

# EVOLVE-BLOCK-START
import random
import time

TIME_BUDGET = 20.0  # seconds of search; the hard limit enforced by the scorer is 60 s


def _can_set(rows, r, c):
    """True if setting cell (r, c) to 1 creates no all-ones 3x3 submatrix.

    rows[i] is an int bitmask of the 1-columns of row i (bit c set <=> entry [i][c] == 1).
    A new 3x3 must use row r and column c, so it needs two OTHER rows a, b that both have
    a 1 in column c and share at least 2 further 1-columns with row r.
    """
    mask_r = rows[r]
    others = [rows[i] for i in range(len(rows)) if i != r and (rows[i] >> c) & 1]
    for x in range(len(others)):
        shared = others[x] & mask_r
        if shared.bit_count() < 2:
            continue
        for y in range(x + 1, len(others)):
            if (shared & others[y]).bit_count() >= 2:
                return False
    return True


def _fill(rows, m, n, rng):
    """Greedily set every zero cell that can legally become 1, in random order (in place)."""
    zeros = [(r, c) for r in range(m) for c in range(n) if not (rows[r] >> c) & 1]
    rng.shuffle(zeros)
    for r, c in zeros:
        if _can_set(rows, r, c):
            rows[r] |= 1 << c


def construct(m, n):
    """Return an m x n 0/1 matrix as a list of m lists of n ints, with no all-ones 3x3."""
    rng = random.Random(12345)  # fixed seed; the wall-clock budget still makes runs vary slightly
    cur = [0] * m
    _fill(cur, m, n, rng)
    cur_ones = sum(x.bit_count() for x in cur)
    best, best_ones = cur[:], cur_ones
    deadline = time.time() + TIME_BUDGET
    while time.time() < deadline:
        new = cur[:]
        ones = [(r, c) for r in range(m) for c in range(n) if (new[r] >> c) & 1]
        for r, c in rng.sample(ones, min(len(ones), rng.randint(1, 4))):
            new[r] &= ~(1 << c)
        _fill(new, m, n, rng)
        new_ones = sum(x.bit_count() for x in new)
        if new_ones >= cur_ones:
            cur, cur_ones = new, new_ones
            if new_ones > best_ones:
                best, best_ones = new[:], new_ones
    return [[(best[r] >> c) & 1 for c in range(n)] for r in range(m)]
# EVOLVE-BLOCK-END


if __name__ == "__main__":
    import sys
    mm, nn = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (13, 19)
    matrix = construct(mm, nn)
    print("\n".join("".join(map(str, row)) for row in matrix))
    print(f"ones = {sum(map(sum, matrix))}  (validity is checked by evaluator.py, not here)")
