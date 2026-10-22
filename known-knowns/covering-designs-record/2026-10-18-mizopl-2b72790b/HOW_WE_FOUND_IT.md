# How We Found It (`C(68, 14, 5) <= 15,675`)

*Contributor text, unverified — narrative of the construction and pruning pipeline. The verified proof is the explicit design in `object/design_68_14_5.txt` checked exhaustively by `verify-it-yourself/run_checks.sh`.*

## 1. Nested Staircase Combining Construction

In the classical two-part combining construction for a $(v, k, t)$ covering design (Gordon, Kuperberg, and Patashnik, 1995), the ground set $V$ is split into $V_1 \sqcup V_2$ of sizes $(v_1, v_2)$, and for each $j \in \{0, \dots, t\}$ one forms the Cartesian product of a $(v_1, k_1(j), j)$ covering $\mathcal{A}_j$ with a $(v_2, k - k_1(j), t - j)$ covering $\mathcal{B}_j$. When consecutive values of $j$ are handled independently, the resulting block sets are disjoint and their sizes simply add.

However, if a contiguous interval of $j \in [p, q]$ uses a **shared block-size split** $(k_1, k - k_1)$, we can **nest** the ingredient designs in opposite directions:
- Take $\mathcal{A}_q$ to be a $(v_1, k_1, q)$ covering design on $V_1$, and for $i = q - 1, \dots, p$ extract a subset $\mathcal{A}_i \subset \mathcal{A}_{i+1}$ that still covers all $i$-subsets of $V_1$ (via lazy greedy set cover inside $\mathcal{A}_{i+1}$).
- Take $\mathcal{B}_p$ to be a $(v_2, k - k_1, t - p)$ covering design on $V_2$, and for $i = p + 1, \dots, q$ extract a subset $\mathcal{B}_i \subset \mathcal{B}_{i-1}$ that still covers all $(t - i)$-subsets of $V_2$.

Then the union of Cartesian products $\bigcup_{i=p}^{q} (\mathcal{A}_i \times \mathcal{B}_i)$ still covers every $t$-subset $T \subseteq V$ with $|T \cap V_1| \in [p, q]$, because any such $T$ has $|T \cap V_1| = i$ covered by some $A \in \mathcal{A}_i$ and $|T \cap V_2| = t - i$ covered by some $B \in \mathcal{B}_i$. Because $\mathcal{A}_p \subset \dots \subset \mathcal{A}_q$ and $\mathcal{B}_q \subset \dots \subset \mathcal{B}_p$ are nested in opposite directions, their Cartesian products overlap in a staircase pattern, so the union size is only

$$\sum_{i=p}^{q} \left(|\mathcal{A}_i| - |\mathcal{A}_{i-1}|\right) |\mathcal{B}_i| \quad (\mathcal{A}_{p-1} = \varnothing).$$

## 2. Realization on $(v, k, t) = (68, 14, 5)$

Splitting $V_{68} = V_1 \sqcup V_2$ with $v_1 = 18$ (`{1..18}`) and $v_2 = 50$ (`{19..68}`), scalar dynamic programming over staircase chains selects:
- $j = 0$, $(k_1, k_2) = (0, 14)$: $\mathcal{A}_0 = C(18, 0, 0)$ ($1$ empty block) $\times \mathcal{B}_0 = C(50, 14, 5)$ ($2,711$ blocks from LJCR) $= 2,711$ blocks.
- $j = 1$, $(k_1, k_2) = (2, 12)$: $\mathcal{A}_1 = C(18, 2, 1)$ ($9$ disjoint pairs) $\times \mathcal{B}_1 = C(50, 12, 4)$ ($773$ blocks from LJCR) $= 6,957$ blocks.
- $j \in [2, 3]$, $(k_1, k_2) = (6, 8)$ (nested staircase chain):
  * $\mathcal{A}_3 = C(18, 6, 3)$ ($48$ blocks from LJCR), with greedy nested subset $\mathcal{A}_2 \subset \mathcal{A}_3$ covering all $2$-subsets of $V_1$ ($|\mathcal{A}_2| = 12$, $|\mathcal{A}_3 \setminus \mathcal{A}_2| = 36$);
  * $\mathcal{B}_2 = C(50, 8, 3)$ ($350$ blocks from LJCR), with greedy nested subset $\mathcal{B}_3 \subset \mathcal{B}_2$ covering all $2$-subsets of $V_2$ ($|\mathcal{B}_3| = 65$);
  * Staircase union $(\mathcal{A}_2 \times \mathcal{B}_2) \cup (\mathcal{A}_3 \times \mathcal{B}_3)$ has $12 \times 350 + 36 \times 65 = 6,540$ blocks ($6,566$ before cross-chain dedupe).
- $j = 4$, $(k_1, k_2) = (12, 2)$: $\mathcal{A}_4 = C(18, 12, 4)$ ($12$ blocks from LJCR) $\times \mathcal{B}_4 = C(50, 2, 1)$ ($25$ disjoint pairs) $= 300$ blocks.
- $j = 5$, $(k_1, k_2) = (14, 0)$: $\mathcal{A}_5 = C(18, 14, 5)$ ($9$ blocks from LJCR) $\times \mathcal{B}_5 = C(50, 0, 0)$ ($1$ empty block) $= 9$ blocks.

Total blocks in the raw staircase union (`how-we-built-it/build_68_14_5.py`): **$16,543$ blocks**.

## 3. Greedy Redundant-Block Pruning (`16,543 -> 15,675`)

Because the nested staircase blocks for $j \in [2, 3]$ and the adjacent chains $j = 1$ and $j = 4$ overlap in their coverage of $5$-subsets, many blocks have all $\binom{14}{5} = 2,002$ of their $5$-subsets covered at least twice. Running `how-we-built-it/prune.c` (with `uint8` saturating coverage counts and random permutation seed `1`) removes **$868$ redundant blocks**, yielding the $1$-minimal **$15,675$-block** $(68, 14, 5)$ covering design in `object/design_68_14_5.txt` (`sha256: 2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07`), which strictly beats the $16,004$-block record in both the Covering Repository and the La Jolla Covering Repository by **$329$ blocks**.
