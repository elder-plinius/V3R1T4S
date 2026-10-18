# Panelist Report: REPRODUCE (`C(40, 16, 7) <= 7,251`)

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)

## 1. Quoted Definition and Claimed Statement

From `claim/CLAIM.md`:

> Let $V$ be a finite set of cardinality $v$, and let $v \ge k \ge t \ge 1$ be integers. A **$(v, k, t)$ covering design** is a collection $\mathcal{B}$ of $k$-element subsets of $V$ (called **blocks**) such that every $t$-element subset $T \subseteq V$ is contained in at least one block $B \in \mathcal{B}$ ($T \subseteq B$). The **covering number** $C(v, k, t)$ is the minimum number of blocks $b = |\mathcal{B}|$ in any $(v, k, t)$ covering design.
>
> The **Schonheim lower bound** (Schonheim, 1964) is defined recursively by $L(v, k, 0) = 1$ and
> $$L(v, k, t) = \left\lceil \frac{v}{k} \, L(v - 1, k - 1, t - 1) \right\rceil.$$

Claimed bound:
$$C(40, 16, 7) \le 7,251,$$
witnessed by the explicit $7,251$-block design in `claim/design_40_16_7.txt`, improving on the prior record of $7,470$ on both `coveringrepository.com` (`claim/cr_archive_vkt.txt`) and the La Jolla Covering Repository (`claim/ljcr_home.html`) by $219$ blocks ($-2.932\%$).

## 2. Independent Checker Written Before Reading Author's Code

Before inspecting `claim/author_checker_cover_check.py`, a standalone exhaustive checker `indep_reproduce_check.py` was written from scratch in Python + NumPy directly from the quoted mathematical definition:

1. **File integrity and format checks:** Reads raw bytes, computes byte size and SHA-256, parses all non-empty lines, verifies that every block has exactly $k$ space-separated integers, all $k$ integers in each block are distinct and in $\{1, \dots, v\}$, and checks that all $b$ blocks are distinct as $k$-sets.
2. **Schonheim bound re-derivation:** Computes $L(v, k, t)$ recursively from $L(v-t, k-t, 0) = 1$:
   - $L(34, 10, 1) = \lceil 34 / 10 \rceil = 4$
   - $L(35, 11, 2) = \lceil 35 \cdot 4 / 11 \rceil = \lceil 140 / 11 \rceil = 13$
   - $L(36, 12, 3) = \lceil 36 \cdot 13 / 12 \rceil = 39$
   - $L(37, 13, 4) = \lceil 37 \cdot 39 / 13 \rceil = 111$
   - $L(38, 14, 5) = \lceil 38 \cdot 111 / 14 \rceil = \lceil 4218 / 14 \rceil = 302$
   - $L(39, 15, 6) = \lceil 39 \cdot 302 / 15 \rceil = \lceil 11778 / 15 \rceil = 786$
   - $L(40, 16, 7) = \lceil 40 \cdot 786 / 16 \rceil = \lceil 31440 / 16 \rceil = 1965$
3. **Exhaustive $\binom{v}{t}$ coverage and 1-minimality check:** Uses the co-lexicographic combinadic bijection $\text{rank}(x_0, \dots, x_{t-1}) = \sum_{i=0}^{t-1} \binom{x_i}{i+1}$ over $0$-based sorted $t$-subsets to maintain an exact coverage multiplicity array `counts` of length $\binom{40}{7} = 18,643,560$. Verifies that the sum of multiplicities equals $b \times \binom{k}{t} = 7,251 \times 11,440 = 82,951,440$, counts uncovered $7$-subsets (`counts == 0`), and counts uniquely covered $7$-subsets (`counts[ranks] == 1`) per block to check $1$-minimality.

### Calibration on Known Positive and Negative Instances

- **Positive test (Fano plane $C(7, 3, 2) = 7$):**
  ```
  [SELF-TEST POSITIVE Fano (7,3,2)] blocks=7 schonheim=7 C(7,2)=21 uncovered=0 passed=True
  ```
- **Negative test (Fano plane minus 1 block, 6 blocks):**
  ```
  [SELF-TEST NEGATIVE Fano-1 (7,3,2)] blocks=6 schonheim=7 C(7,2)=21 uncovered=3 passed=False
  ```

## 3. Independent Verification of `claim/design_40_16_7.txt` (Two Runs for Determinism)

Running `indep_reproduce_check.py 40 16 7 claim/design_40_16_7.txt` twice produced identical results:

- **Run 1 (`4.261462s`):**
  ```
  file=design_40_16_7.txt
  byte_size=319951
  sha256=7db03ef01cd698f6764f590955f51732a64cd8a41dbe97efce69a6738d479985
  v=40
  k=16
  t=7
  raw_line_count=7251
  blocks=7251
  distinct_blocks=7251
  schonheim=1965
  schonheim_ok=True
  total_t_subsets=18643560
  subsets_per_block=11440
  total_inc=82951440
  uncovered=0
  min_cov=1
  max_cov=532
  redundant_blocks=0
  min_unique_per_block=6
  elapsed_sec=4.261461957823485
  passed=True
  ```
- **Run 2 (`4.345409s`):**
  ```
  file=design_40_16_7.txt
  byte_size=319951
  sha256=7db03ef01cd698f6764f590955f51732a64cd8a41dbe97efce69a6738d479985
  v=40
  k=16
  t=7
  raw_line_count=7251
  blocks=7251
  distinct_blocks=7251
  schonheim=1965
  schonheim_ok=True
  total_t_subsets=18643560
  subsets_per_block=11440
  total_inc=82951440
  uncovered=0
  min_cov=1
  max_cov=532
  redundant_blocks=0
  min_unique_per_block=6
  elapsed_sec=4.3454087499994785
  passed=True
  ```

Furthermore, inspecting the block intersection sizes $k_1 = |B \cap \{1, \dots, 16\}|$ across all $7,251$ blocks in `claim/design_40_16_7.txt` confirmed that every line is in strictly increasing order and matches the 5-chain staircase structure described in `claim/CLAIM.md`:
```
k1_distribution: {0: 84, 4: 2579, 8: 3912, 12: 675, 16: 1}
```
Here $84 + 2579 + 3912 + 675 + 1 = 7,251$ blocks (after greedy pruning of $0 + 245 + 644 + 32 + 0 = 921$ redundant blocks from the $8,172$-block raw staircase union), with $0$ redundant blocks remaining and every block uniquely covering at least $6$ of the $7$-subsets.

## 4. Verification of Saved Hashes, Archive Snapshots, and Author's Checker

All saved files in `claim/` were hashed with `shasum -a 256` and matched `claim/CLAIM.md` and `claim/REPRODUCE.md` bit-for-bit:
- `claim/design_40_16_7.txt`: `7db03ef01cd698f6764f590955f51732a64cd8a41dbe97efce69a6738d479985` (`319951` bytes, `7251` lines)
- `claim/author_checker_cover_check.py`: `dcf6f867fa3ea9d0e823640581f48d52d0a033a3a12bc1412085032f6abd82ac`
- `claim/cr_archive_vkt.txt`: `f02f5fc233aa66ca835b8f0b1b4d751fd35ad721c5264043ceb515ee95da9277` (contains record line `40	16	07	07		7470`)
- `claim/ljcr_home.html`: `a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3`

After completing independent verification, `claim/author_checker_cover_check.py` was inspected and executed via the command in `claim/REPRODUCE.md`:
```
file=design_40_16_7.txt sha256=7db03ef01cd698f6764f590955f51732a64cd8a41dbe97efce69a6738d479985 v=40 k=16 t=7
blocks=7251
distinct=7251
base=1
schonheim=1965
C_v_t=18643560
uncovered=0
COVER_CHECK: PASS
```

All properties, hashes, bounds, and exhaustive $\binom{40}{7} = 18,643,560$ subset coverage checks succeeded deterministically with zero discrepancies.

pass: true
