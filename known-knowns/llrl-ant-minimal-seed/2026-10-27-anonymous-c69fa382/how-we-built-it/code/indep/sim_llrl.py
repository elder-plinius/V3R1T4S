#!/usr/bin/env python3
"""Independent LLRL ant simulator + highway certificate.
Written from scratch for the k=6 claim; shares no code with ant.c or ccheck.py.
Conventions (target statement):
  colours 0..3; on colour c turn L for c in {0,1,3}, R for c=2;
  write c+1 mod 4; step one cell; ant starts at (0,0) facing north; y grows down.
  onset = least t such that from update t the read-colour sequence is the period-384
  highway forever (checked by an exact translate certificate).
"""
from __future__ import annotations

# headings: 0=N, 1=E, 2=S, 3=W; y increases south
DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
# LLRL: L,L,R,L  -> delta heading: L=-1 (≡3), R=+1
TURN = (3, 3, 1, 3)  # indexed by colour


def simulate(seed: dict[tuple[int, int], int], n_steps: int):
    """Return (reads, poses) for n_steps updates. pose before each update."""
    grid = dict(seed)
    x = y = h = 0
    reads = []
    poses = []
    for _ in range(n_steps):
        poses.append((x, y, h))
        c = grid.get((x, y), 0)
        reads.append(c)
        h = (h + TURN[c]) & 3
        grid[(x, y)] = (c + 1) & 3
        dx, dy = DIRS[h]
        x += dx
        y += dy
    return reads, poses, grid


def state_after(seed: dict[tuple[int, int], int], t: int):
    grid = dict(seed)
    x = y = h = 0
    for _ in range(t):
        c = grid.get((x, y), 0)
        h = (h + TURN[c]) & 3
        grid[(x, y)] = (c + 1) & 3
        dx, dy = DIRS[h]
        x += dx
        y += dy
    return grid, (x, y, h)


def translate_cert(seed: dict[tuple[int, int], int], t: int, period: int) -> tuple[bool, tuple[int, int]]:
    """Exact translate certificate at time t with given period.
    Advance one period from the state at t; require same heading, nonzero drift D,
    and that every cell on the period's path, projected along D, matches after shift by D
    whenever the projection is at most the max support projection (tube argument).
    """
    g0, (x, y, h) = state_after(seed, t)
    g = dict(g0)
    path = []
    for _ in range(period):
        path.append((x, y))
        c = g.get((x, y), 0)
        h = (h + TURN[c]) & 3
        g[(x, y)] = (c + 1) & 3
        dx, dy = DIRS[h]
        x += dx
        y += dy
    x0, y0, h0 = state_after(seed, t)[1]
    D = (x - x0, y - y0)
    if h != h0 or D == (0, 0):
        return False, D
    # max projection of nonzero support of g0 and g along D
    support = [k for k, v in g0.items() if v] + [k for k, v in g.items() if v]
    if support:
        mp = max(a * D[0] + b * D[1] for a, b in support)
    else:
        mp = -(10**18)
    for cx, cy in set(path):
        while cx * D[0] + cy * D[1] <= mp:
            if g.get((cx + D[0], cy + D[1]), 0) != g0.get((cx, cy), 0):
                return False, D
            cx += D[0]
            cy += D[1]
    return True, D


def find_onset(seed: dict[tuple[int, int], int], n_steps: int = 30000, pmax: int = 1000):
    reads, poses, _ = simulate(seed, n_steps)
    # find least period that holds on a long tail
    period = None
    for p in range(1, pmax + 1):
        lo = max(0, n_steps - 5000)
        if all(reads[u] == reads[u + p] for u in range(lo, n_steps - p)):
            period = p
            break
    if period is None:
        return None
    t = n_steps - period
    while t > 0 and reads[t - 1] == reads[t - 1 + period]:
        t -= 1
    ok, D = translate_cert(seed, t, period)
    ok1, _ = translate_cert(seed, t - 1, period) if t > 0 else (None, None)
    return {
        "onset": t,
        "period": period,
        "drift": D,
        "cert_at_onset": ok,
        "cert_at_onset_minus_1": ok1,
        "heading_at_onset": poses[t][2] if t < len(poses) else None,
        "n_nonzero_seed": sum(1 for v in seed.values() if v),
    }


def parse_seed(s: str) -> dict[tuple[int, int], int]:
    out = {}
    for part in filter(None, s.split(";")):
        a, b, c = map(int, part.split(","))
        out[(a, b)] = c
    return out


if __name__ == "__main__":
    import sys
    seed_s = sys.argv[1] if len(sys.argv) > 1 else ""
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 30000
    seed = parse_seed(seed_s)
    r = find_onset(seed, n)
    if r is None:
        print("NO_PERIOD")
        sys.exit(1)
    print(
        f"INDEP onset={r['onset']} P={r['period']} D={r['drift']} "
        f"cert_onset={r['cert_at_onset']} cert_onset-1={r['cert_at_onset_minus_1']} "
        f"heading={r['heading_at_onset']} k={r['n_nonzero_seed']}"
    )
