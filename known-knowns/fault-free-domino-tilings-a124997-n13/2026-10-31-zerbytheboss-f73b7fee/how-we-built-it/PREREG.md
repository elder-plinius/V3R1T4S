# Pre-Registration: Fault-Free Domino Tilings of the Square (A124997 n=13..15)

- **Target ID**: `fault-free-domino-tilings-a124997-n13`
- **Registered Prior Record**:
  - `A124997` (`https://oeis.org/A124997/b124997.txt`, SHA-256 `1b47e31df2879bfcd5897fb80ff7c729ce7e782fdb3245a0a8a611c8f11335c9`) ends at `n = 12` (`a(12) = 1934659183999048207708201264307215891852758175871534722685882120022644`, added by Xu Mingkuan in Dec 2016).
- **Planned Attack & Independent Verification Protocol**:
  1. Compute the base rectangle domino tiling table `D(w, h)` (`1 <= w, h <= 30`) via two independent methods: Algebraic Chebyshev-Resultant Bareiss Determinant (`D1`) and Bipartite Kasteleyn Transfer + Domino Broken-Profile DP (`D2`).
  2. Compute `A124997(1..15)` and `fault_free(24, 26)` via two distinct inclusion-exclusion reductions: `Method 1` (Integer-Partition Horizontal Fault Compression + 1D Vertical Renewal Inversion) and `Method 2` (Parity-Split Even-Composition Decomposition exploiting `D(odd, odd) = 0`).
  3. Cross-check `6 x 6`, `8 x 8`, and `10 x 10` against `Method 3` (Direct Unbroken-Line Bitmask Profile Transfer without inclusion-exclusion) and verify `A124997(13) mod (10^9 + 7)`.
