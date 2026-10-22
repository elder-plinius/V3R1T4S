# Panelist Report: REPRODUCE (`C(68, 14, 5) <= 15,675`)

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
role: REPRODUCE
target_id: covering-designs-record
claim: C(68, 14, 5) <= 15,675

## 1. Quoted Mathematical Definition from `claim/CLAIM.md`

Before inspecting `claim/author_checker_cover_check.py`, I read `claim/CLAIM.md` and `claim/REPRODUCE.md` and extracted the verbatim definition from `claim/CLAIM.md` (lines 16–20):

> Let $V$ be a finite set of cardinality $v$, and let $v \ge k \ge t \ge 1$ be integers. A **$(v, k, t)$ covering design** is a collection $\mathcal{B}$ of $k$-element subsets of $V$ (called **blocks**) such that every $t$-element subset $T \subseteq V$ is contained in at least one block $B \in \mathcal{B}$ ($T \subseteq B$). The **covering number** $C(v, k, t)$ is the minimum number of blocks $b = |\mathcal{B}|$ in any $(v, k, t)$ covering design.
>
> The **Schonheim lower bound** (Schonheim, 1964) is defined recursively by $L(v, k, 0) = 1$ and
>
> $$L(v, k, t) = \left\lceil \frac{v}{k} \, L(v - 1, k - 1, t - 1) \right\rceil.$$

## 2. Independent Checker Written Before Reading Author's Code

From the quoted definition alone, I wrote a standalone Python + NumPy exhaustive verifier `panel/reproduce_work/indep_reproduce_check.py` (`sha256: 9076d3429cc0253f3e6cbc0e26d85816b3a65ec223a061153d21443e167e599b`). The verifier:
1. Reads the raw bytes of the design file, computes its SHA-256 digest, byte length, and line count.
2. Parses every line and checks that each block contains exactly $k$ distinct integers in $\{1, \dots, v\}$, with zero empty lines and zero duplicate blocks (`distinct == b`).
3. Recursively computes every step of the Schonheim lower bound $L(v, k, t)$ and checks $b \ge L(v, k, t)$.
4. Exhaustively counts the coverage multiplicity of all $\binom{v}{t}$ $t$-subsets of $\{1, \dots, v\}$ via colexicographic ranking $\text{rank}(c_0, \dots, c_{t-1}) = \sum_{r=0}^{t-1} \binom{c_r}{r+1}$ across all $\binom{k}{t}$ $t$-subsets of each block, verifying that the sum of coverage multiplicities equals $b \cdot \binom{k}{t}$ and counting how many of the $\binom{v}{t}$ $t$-subsets have multiplicity $0$ (`uncovered`).
5. Additionally checks $1$-minimality by counting, for every block $B \in \mathcal{B}$, how many of its $\binom{k}{t}$ $t$-subsets have coverage multiplicity equal to $1$ (`redundant_blocks` = number of blocks with $0$ uniquely covered $t$-subsets).

### Calibration on Known Small Positive and Negative Instances

- **Known positive (`panel/reproduce_work/fano_7_3_2_pos.txt`, `sha256: 010fab8a75c9fb2849310ad644140802846a57cd9e6f2b1bfc74e69fc21f5903`):** The $7$ blocks of the Fano plane for $(v, k, t) = (7, 3, 2)$, where $C(7, 3, 2) = L(7, 3, 2) = 7$ and $\binom{7}{2} = 21$.
  - Output: `blocks=7 distinct=7`, `schonheim=7 (b >= schonheim: True)`, `C(v,t)=21 C(k,t)=3 total_incidences=21`, `uncovered=0 min_cov=1 max_cov=1`, `redundant_blocks=0 min_unique_t_subsets_per_block=3 max_unique_t_subsets_per_block=3`, `elapsed_sec=0.0008`, `INDEP_CHECK: PASS` (exit code `0`).
- **Known negative (`panel/reproduce_work/fano_7_3_2_neg.txt`, `sha256: cc8a945db38799f175a552af422f19bf38d1bd957782802914fe910643466fe1`):** The first $6$ blocks of the Fano plane (missing block `3 5 6`, leaving $3$ pairs uncovered).
  - Output: `blocks=6 distinct=6`, `schonheim=7 (b >= schonheim: False)`, `C(v,t)=21 C(k,t)=3 total_incidences=18`, `uncovered=3 min_cov=0 max_cov=1`, `elapsed_sec=0.0006`, `INDEP_CHECK: FAIL` (exit code `1`).

## 3. Independent Exhaustive Verification of `claim/design_68_14_5.txt` (Two Runs for Determinism)

Running `panel/reproduce_work/indep_reproduce_check.py 68 14 5 claim/design_68_14_5.txt` twice produced identical results:

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
- **File integrity:** `sha256` is `2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07` and line count is `15675` (exact match to `claim/CLAIM.md` and `claim/REPRODUCE.md`; note that the actual file size on disk is `632,514` bytes rather than the prose number `632,681` bytes mentioned in `claim/CLAIM.md`, while the SHA-256 hash and all `15,675` lines match bit-for-bit).
- **Block validity and distinctness:** All `15,675` lines parse as $14$-subsets of $\{1, \dots, 68\}$ with no repeated elements within a block and `15,675` distinct blocks (`distinct=15675`).
- **Schonheim lower bound re-derivation:**
  - $L(64, 10, 1) = \lceil 64/10 \rceil = 7$
  - $L(65, 11, 2) = \lceil 65 \times 7 / 11 \rceil = \lceil 455/11 \rceil = 42$
  - $L(66, 12, 3) = \lceil 66 \times 42 / 12 \rceil = \lceil 2772/12 \rceil = 231$
  - $L(67, 13, 4) = \lceil 67 \times 231 / 13 \rceil = \lceil 15477/13 \rceil = 1191$
  - $L(68, 14, 5) = \lceil 68 \times 1191 / 14 \rceil = \lceil 80988/14 \rceil = 5785 \le 15675$.
- **Exhaustive coverage:** All $\binom{68}{5} = 10,424,128$ $5$-subsets are covered (`uncovered=0`), with coverage multiplicity ranging from `min_cov=1` to `max_cov=398` and total incidences $15,675 \times \binom{14}{5} = 15,675 \times 2,002 = 31,381,350$.
- **$1$-minimality:** `redundant_blocks=0`, and every block uniquely covers between `6` and `826` of the $5$-subsets, confirming the claim in `claim/CLAIM.md` line 41 that every block uniquely covers at least $6$ of the $5$-subsets.
- **Comparison against saved baseline snapshots:**
  - `claim/cr_archive_vkt.txt` (`sha256: f02f5fc233aa66ca835b8f0b1b4d751fd35ad721c5264043ceb515ee95da9277`) contains the line `68	14	05	05		16004`.
  - `claim/ljcr_home.html` (`sha256: a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3`) is present and matches its stated SHA-256.
  - Our verified block count $15,675$ improves on $16,004$ by $16,004 - 15,675 = 329$ blocks ($-2.0557\% \approx -2.06\%$).

## 4. Inspection and Execution of Author's Checker (`claim/author_checker_cover_check.py`)

After completing the independent verification above, I read `claim/author_checker_cover_check.py` (`sha256: dcf6f867fa3ea9d0e823640581f48d52d0a033a3a12bc1412085032f6abd82ac`) and executed the command from `claim/REPRODUCE.md`:

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

The output matches `claim/REPRODUCE.md` line-for-line and exits with code `0`.

pass: true
