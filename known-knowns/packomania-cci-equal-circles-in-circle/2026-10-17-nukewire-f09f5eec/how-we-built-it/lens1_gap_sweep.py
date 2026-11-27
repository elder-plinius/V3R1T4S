#!/usr/bin/env python
"""Lens: symmetry, part 1 — systematic plain-window sweep over ALL 135 gap rows (N > 2600).

Quick pass: 12 windows per row (4 orientations x 3 offsets, closed-form spacing
r = 1/(1+2 rho_N)). Rows with quick margin > 1e-11 = candidates; rows > -6e-6 = near,
re-searched on the full grid (601 orientations x 36 offsets). Table values are read from
data/radius.txt; nothing is hand-typed.

Usage: python lens1_gap_sweep.py    (numpy; <= 600 s)
"""
import sys
import time
import numpy as np

SQ3 = np.sqrt(3.0)


def unit_lattice(theta, fx, fy, m):
    ct, st = np.cos(theta), np.sin(theta)
    a1 = np.array([ct, st])
    a2 = np.array([0.5 * ct - 0.5 * SQ3 * st, 0.5 * st + 0.5 * SQ3 * ct])
    off = fx * a1 + fy * a2
    idx = np.arange(-m, m + 1)
    I, J = np.meshgrid(idx, idx, indexing="ij")
    P = (I[..., None] * a1 + J[..., None] * a2 + off).reshape(-1, 2)
    n = np.hypot(P[:, 0], P[:, 1])
    return P, n


def window_r(n, N):
    if len(n) < N:
        return None
    rho = np.partition(n, N - 1)[N - 1]
    return 1.0 / (1.0 + 2.0 * rho)


def main():
    t0 = time.time()
    rows = []
    for line in open("../../data/radius.txt"):
        p = line.split()
        if p and p[0].isdigit() and int(p[0]) > 2600:
            rows.append((int(p[0]), float(p[1])))
    print(f"{len(rows)} gap rows loaded", flush=True)

    quick = [(np.radians(d), fx, fy) for d in (0, 8, 16, 30)
             for (fx, fy) in ((0.0, 0.0), (1 / 3, 1 / 3), (0.5, 0.0))]
    flagged, margins = [], []
    for N, rt in rows:
        m = int(np.sqrt(N * np.pi * SQ3 / 2.0)) + 4
        bq = -1.0
        for th, fx, fy in quick:
            _, n = unit_lattice(th, fx, fy, m)
            r = window_r(n, N)
            if r and r > bq:
                bq = r
        marg = bq - rt
        margins.append((N, marg))
        if marg > 1e-11:
            print(f"CANDIDATE N={N} quick margin {marg:+.3e}", flush=True)
            flagged.append((N, rt, marg, "CANDIDATE"))
        elif marg > -6e-6:
            flagged.append((N, rt, marg, "NEAR"))
    ms = np.array([x[1] for x in margins])
    print(f"quick sweep done in {time.time() - t0:.1f}s; {len(flagged)} rows flagged", flush=True)
    print(f"margins: max {ms.max():+.4e} at N={margins[int(ms.argmax())][0]}, "
          f"min {ms.min():+.4e}, median {np.median(ms):+.4e}")
    for lo, hi in ((1e-11, 1e9), (-6e-6, 1e-11), (-1e-5, -6e-6), (-1e-4, -1e-5), (-1e9, -1e-4)):
        print(f"  margins in [{lo:g}, {hi:g}): {int(((ms >= lo) & (ms < hi)).sum())}")

    grid_th = [np.radians(0.1 * k) for k in range(601)]
    offs = [0.0, 1 / 6, 1 / 3, 0.5, 2 / 3, 5 / 6]
    for N, rt, qm, kind in flagged[:6]:
        m = int(np.sqrt(N * np.pi * SQ3 / 2.0)) + 4
        best = (-1.0, None)
        for th in grid_th:
            for fx in offs:
                for fy in offs:
                    _, n = unit_lattice(th, fx, fy, m)
                    r = window_r(n, N)
                    if r and r > best[0]:
                        best = (r, (th, fx, fy))
        r_grid = best[0]
        print(f"{kind} N={N}: quick margin {qm:+.3e} -> full-grid margin {r_grid - rt:+.3e} "
              f"(theta {np.degrees(best[1][0]):.3f} deg, offset {best[1][1]:.3f},{best[1][2]:.3f})",
              flush=True)
        if r_grid - rt > 1e-11:
            s = 2.0 * r_grid
            P, n = unit_lattice(best[1][0], best[1][1], best[1][2], m)
            coords = s * P[np.argsort(n, kind="stable")[:N]]
            np.savetxt(f"../candidate_N{N}.txt", coords, fmt="%.18f")
            print(f"  CANDIDATE COORDS SAVED: ../candidate_N{N}.txt", flush=True)
    print(f"LENS1 SWEEP DONE ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    sys.exit(main())
