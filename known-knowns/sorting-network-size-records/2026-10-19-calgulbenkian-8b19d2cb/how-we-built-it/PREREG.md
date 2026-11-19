# Preregistration: `sorting-network-size-records` (Dobbelaere Sorting Network Pareto Records)

## 1. Target & Baseline Data
- **Target ID**: `sorting-network-size-records` (Category: `record-tables`, Tractability: 3.0)
- **Baseline Data**:
  - `data/sorting_networks.html` (`SHA-256: fb08a5cd90a460607586be0f753fa19baedc1e5fe1c7d4247efc1923e6dfd0f6`)
  - `data/sorting_networks_extended.html` (`SHA-256: 5515e5d7862caaf31058225ff215850c1987704f6bcd9b5920590e2478d41a53`, last updated `2026-10-13`)
- **Strict Constraints**:
  - No external submissions, git pushes, or PRs.
  - All comparators `(i, j)` must satisfy standard orientation `0 <= i < j < n` (min goes to wire `i`, max goes to wire `j`).
  - Depth is computed by greedy ASAP layering (a comparator `(i, j)` is placed at layer `1 + max(layer_of_wire[i], layer_of_wire[j])`).
  - Every claimed sorting network must be **exhaustively verified via the 0-1 principle** over all $2^n$ binary inputs (either via direct 64-way bit-sliced $2^n$ evaluation or via exact connected-component / prefix output-set propagation where the exact set of all reachable 0-1 states from $\{0,1\}^n$ is tracked and verified to contain only the $n+1$ sorted 0-1 vectors $0^{n-k} 1^k$).
  - Sanity guard: any result below a proven lower bound listed on the page (`n <= 12` sizes, or depth `< 9` for `n=13..16`, depth `< 10` for `n=17`, etc.) is rejected as a bug.

## 2. Win Criteria
- **Full Win (`FULL_WIN`, $13 \le n \le 32$)**:
  - Produce a valid sorting network on $n \in [13, 32]$ wires with `(size, depth)` that strictly dominates or is not dominated by any `(s', d')` pair listed for that $n$ in `sorting_networks_extended.html` (i.e., no listed pair has `s' <= size` and `d' <= depth`).
- **Partial Win `p1` (`PARTIAL_WIN_P1`, $33 \le n \le 64$)**:
  - Produce one or more valid sorting networks on $n \in [33, 64]$ wires with `(size, depth)` that is not dominated by any `(s', d')` pair listed for that $n$ in `sorting_networks_extended.html`, verified exhaustively via the 0-1 principle.

## 3. Methodology
1. **Exact Component-Merging & Bit-Sliced 0-1 Engine (`sn_engine.c` + `verify_sn.py`)**:
   - Maintain a partition of wires $\{0, \dots, n-1\}$ into connected components. Initially each wire $w$ is a singleton component with 2 states `{0, 1}`.
   - When comparator `(i, j)` ($i < j$) is applied:
     - If `i` and `j` are in different components $C_a, C_b$ with state sets $S_a, S_b$, form the Cartesian product $S_a \times S_b$ (size $|S_a| \cdot |S_b|$), apply the compare-exchange `(x_i, x_j) -> (x_i & x_j, x_i | x_j)`, and deduplicate via fast 64-bit radix/hash deduplication.
     - If `i` and `j` are in the same component $C_a$, check whether `x_i <= x_j` already holds for ALL states in $S_a$ (if so, `(i, j)` is **strictly redundant**!), otherwise apply `(x_i, x_j) -> (x_i & x_j, x_i | x_j)` to all states in $S_a$ and deduplicate.
   - Once the remaining suffix does not need intermediate deduplication (or when $|S| \le 5 \times 10^7$), stream all reachable states in 64-element bit-sliced batches (`uint64_t w[64]`) through the remaining comparators using 2 CPU instructions per comparator (`a & b`, `a | b`).
   - Verify at the end that every surviving state is sorted (`(x & (x + 1)) == 0` when wire 0 is LSB and wire $n-1$ is MSB, or `x_0 <= x_1 <= ... <= x_{n-1}`), and that all $n+1$ sorted states $0^{n-k}1^k$ ($k=0\dots n$) are present.
2. **Attack Vectors**:
   - **Vector 1 (Redundant Comparator Audit)**: Scan all existing Pareto networks in `sorting_networks_extended.html` for $13 \le n \le 64$ to detect any strictly redundant comparators.
   - **Vector 2 (All-Split Boundary Wire Reduction + Redundancy Pruning)**: For every network on $N' > n$ wires ($N' - n \le 6$), test all $(N' - n + 1)$ splits of removing $a$ top wires (`fixed to 0`) and $b = (N'-n)-a$ bottom wires (`fixed to 1`), followed by exact 0-1 redundancy pruning and greedy depth repacking.
   - **Vector 3 (Window / Suffix 2-for-1 and $k$-for-$(k-1)$ Exact SAT / MCMC Compression)**: On the exact reachable state set $S_{\text{pre}}$ before the final $K$ comparators ($K \in [10, 40]$), search for a replacement suffix of size $\le K-1$ (or lower depth) that sorts all states in $S_{\text{pre}}$.
   - **Vector 4 (Updated Sub-Sorter Merges & Prefix Transplanting)**: Re-build Batcher odd-even and Van Voorhis $(4,4)$ merges using the newest Pareto networks from `sorting_networks_extended.html` (including the Oct 2026 updates) followed by exact 0-1 redundancy pruning.
