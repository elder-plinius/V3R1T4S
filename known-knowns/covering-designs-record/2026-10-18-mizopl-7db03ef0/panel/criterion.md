# Skeptic Panel Report — Role: CRITERION

panelist: CRITERION
target_id: covering-designs-record
cell: (40, 16, 7)
claimed_b: 7251
previous_record_b: 7470
delta_b: -219
confirmed_scope: An explicit (40,16,7) covering design object/design_40_16_7.txt (319,951 bytes, sha256 7db03ef01cd698f6764f590955f51732a64cd8a41dbe97efce69a6738d479985) with 7,251 blocks, exhaustively verified over all 18,643,560 7-subsets of a 40-set, strictly improving on the Covering Repository record of 7,470 and the La Jolla Covering Repository record of 7,470 for C(40,16,7) by 219 blocks.

## 1. Clause-by-Clause Verification of the Full Success Criterion

The target bank defines the full success criterion for `covering-designs-record` as:

> Explicit list of b blocks (each a k-subset of a v-set) covering every t-subset of the v-set, verified exhaustively by a standalone checker, with b strictly smaller than the current record on coveringrepository.com (which extends Gordon's La Jolla Covering Repository to v <= 99, k <= 25, t <= 8) AND strictly smaller than any value in the La Jolla table (dmgordon.org/covering-designs) or on GitHub/arXiv in the last 6 months, for some (v, k, t) in the table's range, and b >= Schonheim lower bound. Re-fetch both coveringrepository.com and dmgordon.org before claiming. Same-day claim only if C(v,t) <= 5e9 so exhaustive coverage check finishes in hours.

An independent verification script, written from the definition by the skeptic (not included in this package), was executed from scratch to test every clause against `object/design_40_16_7.txt`:

### Clause A: Explicit list of $b = 7,251$ blocks, each a $k = 16$-subset of a $v = 40$-set (no repeated points)
- **Artifact inspected:** `object/design_40_16_7.txt` (`319,951` bytes, `7,251` lines, `sha256: 7db03ef01cd698f6764f590955f51732a64cd8a41dbe97efce69a6738d479985`).
- **Block count and distinctness:** Exactly `7,251` non-empty lines (`b = 7251`), and all `7,251` blocks are pairwise distinct (`distinct = 7251`).
- **Block cardinality and ordering:** Every line parses into exactly `k = 16` integers in strictly increasing order (`strictly_increasing_lines = True`), confirming zero repeated points within any block.
- **Ground set:** Point values span `min = 1` to `max = 40` (`base = 1`) with all `40` ground elements present (`unique_ground_points = 40`). Point degrees across the `40` elements range from `min = 2,672` to `max = 3,167` blocks per point, summing to `116,016 = 7,251 * 16`.
- **Verdict:** **SATISFIED.**

### Clause B: Covers every $t = 7$-subset of the $v = 40$-set, verified exhaustively
- **Total $7$-subsets:** $\binom{40}{7} = 18,643,560$.
- **Incidences:** Each of the `7,251` blocks covers $\binom{16}{7} = 11,440$ distinct $7$-subsets, yielding `7,251 * 11,440 = 82,951,440` block-to-$7$-subset incidences.
- **Exhaustive colex-rank verification (the skeptic's independent script and the author's original standalone cover checker, neither included in this package):** Every one of the `18,643,560` $7$-subsets is covered at least once (`uncovered = 0`, `COVER_CHECK: PASS`, exit code `0`). Re-run on the packaged files, `sh verify-it-yourself/run_checks.sh` (which runs `verify-it-yourself/check_40_16_7.py`) passes both Fano controls and prints `v=40 k=16 t=7 blocks=7251 distinct=7251`, `schonheim_lower_bound=1965`, `total_7_subsets=18643560 uncovered=0`, `PASS` (exit code `0`).
- **Coverage multiplicity distribution across all `18,643,560` $7$-subsets:**
  - Multiplicity `0` (uncovered): `0` subsets (`0.0000%`)
  - Multiplicity `1`: `4,773,418` subsets (`25.6036%`)
  - Multiplicity `2`: `2,460,187` subsets (`13.1959%`)
  - Multiplicity `3`: `2,735,590` subsets (`14.6731%`)
  - Multiplicity `4`: `2,236,696` subsets (`11.9972%`)
  - Multiplicity `5`: `1,502,746` subsets (`8.0604%`)
  - Multiplicity `6`: `1,330,009` subsets (`7.1339%`)
  - Multiplicity `7`: `916,520` subsets (`4.9160%`)
  - Multiplicity `8`: `602,774` subsets (`3.2331%`)
  - Multiplicity `9`: `472,802` subsets (`2.5360%`)
  - Multiplicity `10` up to `max = 532`: `1,612,818` subsets (`8.6508%`)
  - Mean coverage multiplicity: `4.449335` (`82,951,440 / 18,643,560`).
- **1-Minimality:** Across all `7,251` blocks, the number of $7$-subsets uniquely covered by a given block (those with multiplicity `1` in the full design) satisfies:
  - `redundant_blocks = 0` (no block has `0` uniquely covered $7$-subsets)
  - `min_unique_per_block = 6` (achieved at 0-based block index `1413`, 1-based line `1414`)
  - `max_unique_per_block = 1962` (achieved at 0-based block index `2356`, 1-based line `2357`)
  - `mean_unique_per_block = 658.31`, summing to `4,773,418` (matching the multiplicity-`1` count).
- **Verdict:** **SATISFIED.**

### Clause C: Parameter range within table bounds ($v \le 99$, $k \le 25$, $t \le 8$)
- Here $v = 40 \le 99$, $k = 16 \le 25$, and $t = 7 \le 8$.
- **Verdict:** **SATISFIED.**

### Clause D: Strictly smaller than Covering Repository, La Jolla Covering Repository, and recent GitHub/arXiv records
- **Covering Repository (`coveringrepository.com`):** In the plain $(v,k,t)$ archive (`https://coveringrepository.com/download_archive_vkt.aspx`, fetch recorded in `the-record-we-beat/RECORD.md`), line `5135` records:
  `40	16	07	07		7470`
  (with neighboring entries line `5134`: `39 16 07 07 5806` and line `5136`: `41 16 07 07 9198`).
- **La Jolla Covering Repository (`dmgordon.org/covering-designs`):** The LJCR record for $(40, 16, 7)$ is `7,470` (`https://dmgordon.org/covering-designs/`; fetch recorded in `the-record-we-beat/RECORD.md`).
- **GitHub / arXiv (last 6 months):** No published repository or preprint reports an upper bound for $C(40, 16, 7)$ below `7,470`.
- **Comparison:** $b = 7,251$ is strictly smaller than `7,470` by `219` blocks (`-2.9317%`).
- **Verdict:** **SATISFIED.**

### Clause E: Schonheim lower bound ($b \ge L(40, 16, 7)$)
- Using the exact recurrence $L(v, k, t) = \lceil \frac{v}{k} L(v-1, k-1, t-1) \rceil$ with $L(33, 9, 0) = 1$:
  - $L(34, 10, 1) = \lceil 34 / 10 \rceil = 4$
  - $L(35, 11, 2) = \lceil 140 / 11 \rceil = 13$
  - $L(36, 12, 3) = \lceil 468 / 12 \rceil = 39$
  - $L(37, 13, 4) = \lceil 1,443 / 13 \rceil = 111$
  - $L(38, 14, 5) = \lceil 4,218 / 14 \rceil = 302$
  - $L(39, 15, 6) = \lceil 11,778 / 15 \rceil = 786$
  - $L(40, 16, 7) = \lceil 31,440 / 16 \rceil = 1,965$
- Since $b = 7,251 \ge 1,965$, the Schonheim lower bound condition holds.
- **Verdict:** **SATISFIED.**

### Clause F: Same-day verification condition ($\binom{v}{t} \le 5 \times 10^9$)
- $\binom{40}{7} = 18,643,560 \le 5,000,000,000$ (`0.3729%` of the threshold). The full exhaustive check completes in a few seconds.
- **Verdict:** **SATISFIED.**

## 2. Hidden Quantifiers, Stretched Definitions, and Null/Deletion Controls

1. **No stretched definitions or hidden quantifiers:**
   - The object is a standard, unweighted, plain $(40, 16, 7)$ covering design (`m = t = 7`, covering multiplicity $\lambda = 1$).
   - Every block has exact size `16`, and all points lie in $\{1, \dots, 40\}$.
2. **Why a statistical 400-control null model is not required:**
   - The claim is not an empirical or probabilistic correlation; it is a deterministic, finite combinatorial certificate (`object/design_40_16_7.txt`) verified exhaustively over all $\binom{40}{7} = 18,643,560$ $7$-subsets against a fixed integer table bound (`7,470`). Moreover, a random collection of $b = 7,251$ blocks of size `16` covers each $7$-subset independently with probability $11,440 / 18,643,560 \approx 6.136 \times 10^{-4}$, leaving an expected $18,643,560 \times (1 - 6.136 \times 10^{-4})^{7251} \approx 217,315$ uncovered $7$-subsets.
3. **Checker sensitivity via deterministic block-deletion controls:**
   - Because `min_unique_per_block = 6`, deleting any single block from `object/design_40_16_7.txt` leaves at least `6` uncovered $7$-subsets.
   - Running the author's original standalone cover checker on three 7,250-block deletion controls (each obtained by deleting one line of `object/design_40_16_7.txt`) confirmed exact sensitivity:
     - Deleting block `1413` (1-based line `1414`, minimum-unique block; control `sha256: 94017f418aff4f9ea2647ac4fa3e9a0b89764e26e28f4550c66dfe1aab223237`): exits with code `1` and outputs `uncovered=6` / `COVER_CHECK: FAIL 6 uncovered t-subsets`.
     - Deleting block `0` (1-based line `1`; control `sha256: 5be374f8f2aca60c9a89f86efc4e89286fdad9ecef296255b23ce0f187710b75`): exits with code `1` and outputs `uncovered=1820` / `COVER_CHECK: FAIL 1820 uncovered t-subsets`.
     - Deleting block `7250` (1-based line `7251`; control `sha256: e5f0eb040a75ed9a410b2fe5b81bccbce2604715c14342952c477bb8d401c176`): exits with code `1` and outputs `uncovered=213` / `COVER_CHECK: FAIL 213 uncovered t-subsets`.

pass: true
