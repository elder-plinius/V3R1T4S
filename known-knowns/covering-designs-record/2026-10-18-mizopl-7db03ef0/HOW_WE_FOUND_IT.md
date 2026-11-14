# How We Found It: Nested Staircase Combining & Seam Redundancy Pruning on `C(40, 16, 7)`

*(contributor text, unverified)*

## 1. Nested Staircase Combining Construction

Partition the $40$-point ground set into $V_1 = \{1, \dots, 16\}$ ($v_1 = 16$) and $V_2 = \{17, \dots, 40\}$ ($v_2 = 24$), and partition $j = |T \cap V_1| \in \{0, 1, 2, 3, 4, 5, 6, 7\}$ into five nested staircase chains `[(0, 0, 0), (1, 2, 4), (3, 4, 8), (5, 6, 12), (7, 7, 16)]` (`how-we-built-it/build_40_16_7.py`):
- $j = 0$, $(k_1, k_2) = (0, 16)$: $1 \times 84 = 84$ blocks.
- $j \in \{1, 2\}$, $(k_1, k_2) = (4, 12)$: $|\mathcal{A}| = [4, 20]$, $|\mathcal{B}| = [266, 110]$, giving $4 \times 266 + 16 \times 110 = 2,824$ blocks.
- $j \in \{3, 4\}$, $(k_1, k_2) = (8, 8)$: $|\mathcal{A}| = [14, 30]$, $|\mathcal{B}| = [226, 87]$, giving $14 \times 226 + 16 \times 87 = 4,556$ blocks.
- $j \in \{5, 6\}$, $(k_1, k_2) = (12, 4)$: $|\mathcal{A}| = [14, 19]$, $|\mathcal{B}| = [48, 7]$, giving $14 \times 48 + 5 \times 7 = 707$ blocks.
- $j = 7$, $(k_1, k_2) = (16, 0)$: $1 \times 1 = 1$ block.

The raw staircase union has $8,172$ blocks.

## 2. Exact Cross-Seam Redundancy Pruning (`prune.c`)

Because adjacent staircase layers $(k_1, k_2)$ over-cover $7$-subsets across the partition boundary, running `how-we-built-it/prune.c` (`seed = 1`) removes **$921$ redundant blocks** whose $\binom{16}{7} = 11,440$ $7$-subsets are all covered at least twice ($8,172 \to 7,251$), yielding the $1$-minimal $7,251$-block design `object/design_40_16_7.txt` (improving the `7,470` record in both CR and LJCR by `219` blocks).
