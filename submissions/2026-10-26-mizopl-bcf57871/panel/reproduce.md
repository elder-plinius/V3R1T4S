role: reproduce
context: fresh research subagent invoked via invoke_subagent
target_id: conway-99-graph
claim_targeted: p1 + p2

# Skeptic 1 (`reproduce`) Audit Report: `conway-99-graph` (Tracks `p2` and `p1`)

## 1. Execution & Standard-Library-Only Verification

- **Command executed:** `python3 -B verify.py` inside the `claim/` directory.
- **Standard library compliance:** Inspected `verify.py` imports (`hashlib`, `itertools`, `json`, `os`, `sys`). No third-party packages, external SAT solvers, or external C binaries are imported or invoked during verification.
- **Execution result:** Completed in $\sim 10.5$ seconds with exit code `0` and final line `VERIFY: PASS`.

```text
[PASS] Positive non-vacuity control on srg(9, 4, 1, 2) = K_3 box K_3 (Encoding A & Encoding B)
[PASS] Track p2 p2_1_inner_matching_k14: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p2 p2_2_outer_bijection_k14: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p2 p2_3_inner_outer_balance_k14: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p2 p2_4_outer_pair_cn_k14: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p2 p2_5_srg9_uniqueness: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p3_t1_fix33: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b1_c6_fix73: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b2_c5_fix51: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b0_c5_fix53: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a0_b4_c3_fix19: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b2_c3_fix21: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 p2_a1_b3_c2_fix11: Enc A & Enc B CNF membership + LRAT RUP verified
[PASS] Track p1 frob21_z7_z3: Enc A & Enc B CNF membership + LRAT RUP verified
All 26 UNSAT proofs (13 theorems x 2 encodings, 19693 RUP lemmas, 0 RAT lemmas) verified.
VERIFY: PASS
```

## 2. Independent CNF Re-Generation & Core Clause Membership Audit

- **Dual Cardinality Encoders:**
  - **Encoding A (`add_exact_sinz`):** Implements the Sinz (2005) linear sequential counter using $n \cdot k$ register variables $s_{i,j}$ with bidirectional implications enforcing $\sum_{i=1}^n L_i = k$.
  - **Encoding B (`add_exact_totalizer`):** Implements the Bailleux & Boufkhad (2003) binary tree unary totalizer recursively splitting $L$ into balanced subtrees and enforcing both upward at-most-$k$/sum propagation and downward sum-witness propagation.
- **26 Formulas Re-Generated From Scratch:**
  - `verify.py` constructs all $5$ Track `p2` propositions (`p2_1_inner_matching_k14`, `p2_2_outer_bijection_k14`, `p2_3_inner_outer_balance_k14`, `p2_4_outer_pair_cn_k14`, `p2_5_srg9_uniqueness`) and all $8$ Track `p1` automorphism exclusion cases (`p3_t1_fix33`, `p2_a0_b1_c6_fix73`, `p2_a0_b2_c5_fix51`, `p2_a1_b0_c5_fix53`, `p2_a0_b4_c3_fix19`, `p2_a1_b2_c3_fix21`, `p2_a1_b3_c2_fix11`, `frob21_z7_z3`) under both Encoding A and Encoding B ($13 \times 2 = 26$ full CNFs).
- **Exact Clause Set Membership:**
  - For each of the $26$ proof objects, `verify.py` parses `*_core.cnf` via `parse_dimacs_clauses` and checks `cl in full_clause_set` against the freshly generated CNF from its corresponding encoder. All $44,756$ core clauses in Encoding A and $31,292$ core clauses in Encoding B are verified to be exact subsets of the freshly generated formulas.

## 3. Positive Non-Vacuity Control (`srg(9, 4, 1, 2)`)

- `verify_positive_control_srg9` builds the unblocked $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ formulas (`add_blocking_clause=False`) for both Encoding A ($66$ variables, $200$ clauses) and Encoding B ($42$ variables, $146$ clauses), seeds the $6$ outer-edge variables with the explicit $4$-cycle truth assignment (`{1: True, 2: True, 3: False, 4: False, 5: True, 6: True}`), runs deterministic unit propagation across all auxiliary cardinality and conjunction variables, and confirms that every clause in both formulas is satisfied.

## 4. Pure-Python LRAT RUP Proof Checker & Hash Integrity Audit

- **Pure-Python LRAT RUP Checker (`verify_lrat_python`):**
  - Loads the $1$-indexed clauses of `*_core.cnf`, processes clause deletions (`d`) and RUP additions across single and multi-part `.lrat` files, explicitly rejects any negative hint (`any(h < 0 for h in hints)` $\implies$ error, enforcing $0$ RAT lemmas), verifies that every hint chain reaches a unit-propagation conflict from the negated lemma literals using only active clauses, and confirms that the empty clause `0` (`len(lemma_lits) == 0`) is derived in all $26$ proofs ($9,816$ RUP lemmas in Encoding A $+ 9,877$ RUP lemmas in Encoding B $= 19,693$ RUP lemmas total, $0$ RAT lemmas).
- **Hash & Artifact Cross-Check:**
  - All $26$ `core_cnf_sha256`, $26$ `core_drat_sha256`, and $31$ `core_lrat_sha256s` digests in `certificate.json` match the files on disk and are mutually distinct between Encoding A and Encoding B.
  - Every variable count, full clause count, core clause count, RUP lemma count, and cycle-structure statistic in `artifact.md` matches `certificate.json` and `verify.py` with zero discrepancies.

pass: true
