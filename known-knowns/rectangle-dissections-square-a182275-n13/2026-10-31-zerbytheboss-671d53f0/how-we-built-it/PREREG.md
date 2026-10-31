# Pre-Registration: Rectangle Dissections of the Square (A182275 n=13..15)

- **Target ID**: `rectangle-dissections-square-a182275-n13`
- **Registered Prior Record**:
  - `A182275` (`https://oeis.org/A182275/b182275.txt`, SHA-256 `88df1f1271f5d5be7f3393889a87386967f5f70722fd7034d551d2a030c74ab7`) ends at `n = 12` (`a(12) = 59647666241586874002530830848160043213559146735474`).
  - `A116694` (`https://oeis.org/A116694/b116694.txt`, SHA-256 `22626e21f5a25813daf3ca1cbea29161d3c14980c97396d303490ccb9a5dedcd`) lists 210 entries on antidiagonals `d = 1..20` (`m + n <= 19` in 0-based indexing), so `A116694(13, 12)` (`m + n = 25`) and `A182275(13)` (`m + n = 26`) are uncomputed.
  - `A333476` (`https://oeis.org/A333476/b333476.txt`, SHA-256 `e50bf48cd388ce7dc1ac04d0e0de6de9a50b33bfb8a5edbe786a31245b80e44f`) lists rows `0 <= k <= n <= 12` (91 entries).
- **Planned Attack & Independent Verification Protocol**:
  1. Formulate `Method 1` (1-bit broken-profile vertex-degree continuity DP over horizontal column-cut masks in `{0, 1}^{m-1}`).
  2. Formulate `Method 2` (recursive Kronecker-block divide-and-conquer on `(M_m, B_m)` without vertex profile sweep + transpose symmetry `A116694(m, n) == A116694(n, m)`).
  3. Formulate `Method 3` (classical `F(2m+1)` vertical-cut open-rectangle transfer matrix for `0 <= m, n <= 6`).
  4. Require exact agreement across all methods and byte-for-byte reproduction of `b182275.txt`, `b116694.txt` (all 210 entries), and `b333476.txt` (all 91 entries).
