# Packomania SCU N=344 Sphere Packing Record

## What

Breakthrough sphere packing record for N=344 equal spheres in unit cube [-1/2, 1/2]^3 achieving 50-digit feasible radius r* = 0.0751108346348785... strictly exceeding Packomania live table record 0.075110834623 by +1.18785e-11 >= 1.0e-11, non-isometric to posted configuration (max distance difference 0.026011 >> 1e-4), and unqueued on pending-requests.html; accompanied by 50-digit data-integrity audit across all N <= 1000 scu files (p3) and missing-center reconstruction for ssp N=20 (p2).

## Check It Yourself

Run the standalone verification suite:

```bash
sh verify-it-yourself/run_checks.sh
```

This verifies the exact coordinates of all 344 sphere centers in 50-digit arbitrary precision arithmetic (`mpmath`), verifying:
1. Every sphere is strictly contained within the unit cube $[-1/2, 1/2]^3$.
2. All pairwise distances between sphere centers satisfy $d_{ij} \ge 2 r^*$.
3. The achieved radius $r^* = 0.0751108346348785...$ strictly improves the published record by $+1.187854 \times 10^{-11}$.

## Compared To

- **Repository**: Eckard Specht's Packomania (`https://packomania.com/scu/txt/radius.txt`)
- **Previous Record Holder**: Lu Peng ($r = 0.075110834623$)
- **New V3R1T4S Feasible Radius**: $r^* = 0.075110834634878543968199277409296619659795377423474$
- **Margin**: $+1.1878543968 \times 10^{-11} \ge 1.0 \times 10^{-11}$
- **Non-Isometry**: The sorted pairwise distance multiset differs from Lu Peng's posted coordinates by up to $0.02601077 \gg 10^{-4}$.
- **Submission Status**: Zero pending submissions exist in category `scu` on `pending-requests.html`.

## Not Claimed

- No claims are made for $N \ne 344$ exceeding table records (other than certifying the data-integrity audit for $N \le 1000$ and repairing the $N=20$ coordinate truncation for `ssp`).
- Global optimality for $N = 344$ is not claimed; this is an improved feasible configuration certified to 50 decimal digits.

## Credits

- V3R1T4S project contributors.
- Eckard Specht for curating the Packomania benchmark repository.
- Lu Peng for the previous record construction.
