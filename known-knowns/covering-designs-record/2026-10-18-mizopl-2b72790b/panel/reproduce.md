# Panelist Report: REPRODUCE (`C(68, 14, 5) <= 15,675`)

role: REPRODUCE
target_id: covering-designs-record
claim: C(68, 14, 5) <= 15,675

## 1. Quoted Mathematical Definition

Before inspecting the author's checker, I extracted the verbatim definition from the author's claim statement:

> Let $V$ be a finite set of cardinality $v$, and let $v \ge k \ge t \ge 1$ be integers. A **$(v, k, t)$ covering design** is a collection $\mathcal{B}$ of $k$-element subsets of $V$ (called **blocks**) such that every $t$-element subset $T \subseteq V$ is contained in at least one block $B \in \mathcal{B}$ ($T \subseteq B$). The **covering number** $C(v, k, t)$ is the minimum number of blocks $b = |\mathcal{B}|$ in any $(v, k, t)$ covering design.
>
> The **Schonheim lower bound** (Schonheim, 1964) is defined recursively by $L(v, k, 0) = 1$ and
>
> $$L(v, k, t) = \left\lceil \frac{v}{k} \, L(v - 1, k - 1, t - 1) \right\rceil.$$

## 2. Independent Checker Written Before Reading Author's Code

From the quoted definition alone, I wrote a standalone Python + NumPy exhaustive verifier (not included in this package). The verifier:
1. Reads the raw bytes of the design file, computes its SHA-256 digest, byte length, and line count.
2. Parses every line and checks that each block contains exactly $k$ distinct integers in $\{1, \dots, v\}$, with zero empty lines and zero duplicate blocks (`distinct == b`).
3. Recursively computes every step of the Schonheim lower bound $L(v, k, t)$ and checks $b \ge L(v, k, t)$.
4. Exhaustively counts the coverage multiplicity of all $\binom{v}{t}$ $t$-subsets of $\{1, \dots, v\}$ via colexicographic ranking $\text{rank}(c_0, \dots, c_{t-1}) = \sum_{r=0}^{t-1} \binom{c_r}{r+1}$ across all $\binom{k}{t}$ $t$-subsets of each block, verifying that the sum of coverage multiplicities equals $b \cdot \binom{k}{t}$ and counting how many of the $\binom{v}{t}$ $t$-subsets have multiplicity $0$ (`uncovered`).
5. Additionally checks $1$-minimality by counting, for every block $B \in \mathcal{B}$, how many of its $\binom{k}{t}$ $t$-subsets have coverage multiplicity equal to $1$ (`redundant_blocks` = number of blocks with $0$ uniquely covered $t$-subsets).

### Calibration on Known Small Positive and Negative Instances

- **Known positive:** The $7$ blocks of the Fano plane for $(v, k, t) = (7, 3, 2)$, where $C(7, 3, 2) = L(7, 3, 2) = 7$ and $\binom{7}{2} = 21$.
  - Output: `blocks=7 distinct=7`, `schonheim=7 (b >= schonheim: True)`, `C(v,t)=21 C(k,t)=3 total_incidences=21`, `uncovered=0 min_cov=1 max_cov=1`, `redundant_blocks=0 min_unique_t_subsets_per_block=3 max_unique_t_subsets_per_block=3`, `elapsed_sec=0.0008`, `INDEP_CHECK: PASS` (exit code `0`).
- **Known negative:** The first $6$ blocks of the Fano plane (missing block `3 5 6`, leaving $3$ pairs uncovered).
  - Output: `blocks=6 distinct=6`, `schonheim=7 (b >= schonheim: False)`, `C(v,t)=21 C(k,t)=3 total_incidences=18`, `uncovered=3 min_cov=0 max_cov=1`, `elapsed_sec=0.0006`, `INDEP_CHECK: FAIL` (exit code `1`).

## 3. Independent Exhaustive Verification of `object/design_68_14_5.txt` (Two Runs for Determinism)

Running the independent verifier with `v=68 k=14 t=5` on the design file twice produced identical results:

```
bytes=632514 lines=15675 sha256=2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07
params: v=68 k=14 t=5
blocks=15675 distinct=15675
  schonheim_step: L(64,10,1) = ceil(64/10) = 7
  schonheim_step: L(65,11,2) = ceil(455/11) = 42
  schonheim_step: L(66,12,3) = ceil(2772/12) = 231
  schonheim_step: L(67,13,4) = ceil(15477/13) = 1191
  schonheim_step: L(68,14,5) = ceil(80988/14) = 5785
schonheim=5785 (b >= schonheim: True)
C(v,t)=10424128 C(k,t)=2002 total_incidences=31381350
uncovered=0 min_cov=1 max_cov=398
redundant_blocks=0 min_unique_t_subsets_per_block=6 max_unique_t_subsets_per_block=826
elapsed_sec=1.6641 (run 1) / 1.8455 (run 2)
INDEP_CHECK: PASS
```

Every claimed property is independently confirmed:
- **File integrity:** `sha256` is `2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07`, size is `632,514` bytes and line count is `15675`.
- **Block validity and distinctness:** All `15,675` lines parse as $14$-subsets of $\{1, \dots, 68\}$ with no repeated elements within a block and `15,675` distinct blocks (`distinct=15675`).
- **Schonheim lower bound re-derivation:**
  - $L(64, 10, 1) = \lceil 64/10 \rceil = 7$
  - $L(65, 11, 2) = \lceil 65 \times 7 / 11 \rceil = \lceil 455/11 \rceil = 42$
  - $L(66, 12, 3) = \lceil 66 \times 42 / 12 \rceil = \lceil 2772/12 \rceil = 231$
  - $L(67, 13, 4) = \lceil 67 \times 231 / 13 \rceil = \lceil 15477/13 \rceil = 1191$
  - $L(68, 14, 5) = \lceil 68 \times 1191 / 14 \rceil = \lceil 80988/14 \rceil = 5785 \le 15675$.
- **Exhaustive coverage:** All $\binom{68}{5} = 10,424,128$ $5$-subsets are covered (`uncovered=0`), with coverage multiplicity ranging from `min_cov=1` to `max_cov=398` and total incidences $15,675 \times \binom{14}{5} = 15,675 \times 2,002 = 31,381,350$.
- **$1$-minimality:** `redundant_blocks=0`, and every block uniquely covers between `6` and `826` of the $5$-subsets, confirming the claim (stated in `README.md`) that every block uniquely covers at least $6$ of the $5$-subsets.
- **Comparison against the record (see `the-record-we-beat/RECORD.md`):**
  - The Covering Repository plain $(v,k,t)$ archive (`https://coveringrepository.com/download_archive_vkt.aspx`) contains the line `68	14	05	05		16004`.
  - The La Jolla Covering Repository (`https://dmgordon.org/covering-designs/`) lists the same record, $16,004$.
  - Our verified block count $15,675$ improves on $16,004$ by $16,004 - 15,675 = 329$ blocks ($-2.0557\% \approx -2.06\%$).

## 4. Inspection and Execution of Author's Checker

After completing the independent verification above, I read the author's original standalone cover checker (not included in this package) and executed it on the design:

```
file=design_68_14_5.txt sha256=2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07 v=68 k=14 t=5
blocks=15675
distinct=15675
base=1
schonheim=5785
C_v_t=10424128
uncovered=0
COVER_CHECK: PASS
```

The output matches the author's stated expected output line-for-line and exits with code `0`.

Re-run on the packaged files, `sh verify-it-yourself/run_checks.sh` (which runs `verify-it-yourself/check_68_14_5.py`) prints:

```
control_positive_fano_7_3_2: PASS (21/21 covered, uncovered=0)
control_negative_fano_minus_1: PASS (rejected with uncovered=3)
sha256=2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07
v=68 k=14 t=5 blocks=15675 distinct=15675
schonheim_lower_bound=5785
previous_cr_record=16004 previous_ljcr_record=16004 delta=-329
total_5_subsets=10424128 uncovered=0
PASS
```

pass: true
