# Verification Receipts (`verify-it-yourself/RECEIPTS.md`)

## 1. Command Executed

```sh
sh verify-it-yourself/run_checks.sh
```

## 2. Exact Output

```text
[1/4] Checked toroidal table for n=1..16 (direct game-tree solve for n=1..12) in 0.52s
[2/4] Verified 21-orbit ply-3 strategy certificate for G(TQ_14) = 1 (all 144 replies in H_14 refuted) in 3.65s
[3/4] Checked planar margin tables (direct R_8, R_10, R_12 solves and the R_14 mutual-reply certificate) in 9.08s
[4/4] Checked planar A344227 table for n=0..16 (exact mex solve for n=0..8) in 0.35s
All checks passed in 13.61s.
PASS
```

## 3. Dual Independent C++ Bitboard Solver Receipts

- **Solver A (`how-we-built-it/solver_a_full.cpp`)**:
  - `G(TQ_1..16)` = `1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0`; $H_n$ winning replies: $H_{12} = 20/100$ (`0.027s`, `23,095` nodes), $H_{14} = 0/144$ (`0.077s`, `631,430` nodes), $H_{16} = 196/196$ (`1.801s`, `22,764,105` nodes).
  - Central-strike refutation margins: $R_8 = 0/36$ (`0.023s`, `77` nodes), $R_{10} = 8/64$ (`0.014s`, `13,517` nodes), $R_{12} = 100/100$ (`0.041s`, `349,103` nodes), $R_{14} = 140/144$ (`1.921s`, `27,500,211` nodes; non-refuting `(4,7), (7,4), (7,8), (8,7)`), $R_{16} = 146/196$ (`360.248s`, `3,549,497,298` nodes; 50 non-refuting squares).
  - Planar OEIS A344227($0 \dots 16$) calibration: `0, 1, 1, 2, 1, 3, 1, 2, 3, 1, 0, 1, 0, 1, 0, 1, 0` (`121.736s` at $n=15$, `465.369s` at $n=16$).
- **Solver B (`how-we-built-it/solver_b_tq.cpp` and `how-we-built-it/solver_b_margins.cpp`)**:
  - `G(TQ_1..16)` = `1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0`; $H_n$ winning replies: $H_{12} = 20/100$ (`0.261s`, `26,552` nodes), $H_{14} = 0/144$ (`1.367s`, `744,999` nodes), $H_{16} = 196/196$ (`58.373s`, `28,894,016` nodes).
  - Central-strike refutation margins: $R_8 = 0/36$ (`0.051s`, `77` nodes), $R_{10} = 8/64$ (`0.036s`, `13,508` nodes), $R_{12} = 100/100$ (`0.054s`, `346,222` nodes), $R_{14} = 140/144$ (`2.054s`, `28,523,070` nodes; non-refuting `(4,7), (7,4), (7,8), (8,7)`), $R_{16} = 146/196$ (`348.254s`, `4,243,114,244` nodes; exact same 50 non-refuting squares).
  - Planar OEIS A344227($0 \dots 16$) calibration: `0, 1, 1, 2, 1, 3, 1, 2, 3, 1, 0, 1, 0, 1, 0, 1, 0` (`239.450s` at $n=15$, `374.488s` at $n=16`).
