# Preregistration — `conway-99-graph` (Track `p2`) — 2026-10-26T05:19:00Z

Written BEFORE any computation or proof attempt begins. This file is frozen once Stage 2 starts.

## 1. Target and track

- `problem_id`: `conway-99-graph`
- `tier`: `S`
- `domain`: `graphs-games-automata`
- `claim_targeted`: `p2`
- Why this track: Track `p2` asks for an independent machine-checked re-derivation (SAT with DRAT/LRAT-checked proof from an independent encoding) of the forced-structure reduction of `arXiv:2608.11211` Section 2.3.

## 2. Specific hypothesis (falsifiable)

- **Statement (Track `p2`):** From two independent Boolean CNF cardinality encodings (Encoding A: Sinz 2005 Linear Sequential Counter; Encoding B: Bailleux & Boufkhad 2003 Binary Tree Unary Totalizer) of the local $\mathrm{srg}(v, k, 1, 2)$ axioms $(\lambda = 1, \mu = 2)$, the negation of each forced-structure reduction proposition of `arXiv:2608.11211` Section 2.3—(`p2_1`) $1$-regular perfect matching on $\Gamma_1(0)$, (`p2_2`) bijection between $\Gamma_2(0)$ and the $M = \binom{k}{2} - k/2 = 84$ non-matched pairs of $\Gamma_1(0)$ (Constraint 1), (`p2_3`) inner-outer coordinate balance $\mathbf{1}_{m(a) \in P_u} + \deg_{\Gamma_2(0) \cap N(a)}(u) = 2$ for $a \notin P_u$ and $\deg_{\Gamma_2(0) \cap N(a)}(u) = 1$ for $a \in P_u$ (Constraint 4), (`p2_4`) outer pair common-neighbor count $(1 \text{ if } u \sim v \text{ else } 2) - |P_u \cap P_v|$ (Constraints 2 & 3), and (`p2_5`) uniqueness of the reduced outer graph on $\mathrm{srg}(9, 4, 1, 2)$—is UNSAT with a `drat-trim`-verified LRAT proof (`0` RAT lemmas).
- **What would falsify it:** If the `drat-trim` or standalone pure-Python LRAT/RUP checker rejects any generated proof, if any core clause is not in the freshly generated CNF formula, or if the positive non-vacuity control on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ fails to satisfy the unblocked formula.

## 3. Attack plan (ordered lenses)

1. **Lens 1 (`Encoding A: Sinz 2005 Linear Sequential Counter`):**
   - Implement CNF generators for the 5 forced-structure reduction propositions (`p2_1`–`p2_5`) of `arXiv:2608.11211` Section 2.3 using Sinz's (2005) sequential counter for all exact cardinality constraints $\sum L_i = k$.
   - Solve with `kissat`, extract trimmed `.cnf` cores and `.lrat` proofs via `drat-trim -L`, and verify every `.lrat` proof with a standalone pure-Python LRAT/RUP verifier.
2. **Lens 2 (`Encoding B: Bailleux & Boufkhad 2003 Binary Tree Unary Totalizer`):**
   - Implement CNF generators for the same 5 forced-structure reduction propositions (`p2_1`–`p2_5`) using Bailleux & Boufkhad's (2003) binary tree unary totalizer for all exact cardinality constraints $\sum L_i = k$.
   - Solve with `kissat`, extract trimmed `.cnf` cores and `.lrat` proofs via `drat-trim -L`, and verify every `.lrat` proof with the standalone pure-Python LRAT/RUP verifier.

## 4. Verification plan

- **Verification script:** `verify-it-yourself/verify.py` (deterministic, offline, pure Python standard library only, runtime `< 5` seconds).
- **Checks performed by `verify-it-yourself/verify.py`:**
  1. Re-generates the DIMACS CNF formulas from both independent encodings (Encoding A and Encoding B) for all 5 Track `p2` propositions (`10` formulas total) and verifies their exact variable and clause counts.
  2. Verifies that every clause in each of the 10 trimmed core files `object/proofs/p2_*_core.cnf` belongs to the freshly generated CNF from its encoder.
  3. Runs an embedded pure-Python LRAT/RUP proof checker on all 10 `.lrat` certificates (`1,879` RUP lemmas total, `0` RAT lemmas), verifying that every derived clause follows by Reverse Unit Propagation from active clauses up to the empty clause `0`.
  4. Verifies positive satisfiability controls (specifically that $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ satisfies the unblocked forced-structure encodings in both Encoding A and Encoding B).
  5. Compares all computed counts, hashes, and verification statuses against `object/certificate.json`.
- `null_test`: not needed because this is a deterministic SAT/LRAT proof-verification run with zero statistical or empirical noise; non-vacuity is established by the positive satisfiability control on $\mathrm{srg}(9, 4, 1, 2)$ and by corrupting `object/certificate.json` to confirm `verify.py` fails on tampering.

## 5. Compute and time budget

- Max wall-clock for Stage 2: 45 minutes.
- Max verification runtime for `verify-it-yourself/verify.py`: `< 5` seconds on CPU.
- Stopping rule: Stop and package once all 10 Track `p2` forced-structure proofs (`5` propositions $\times 2$ encodings) are verified by both `drat-trim` and the standalone Python LRAT/RUP verifier.

## 6. What will be logged as a dead end if this fails

- Any proposition whose SAT instance fails to yield a verified pure-RUP LRAT certificate across both encodings will be logged with exact variable/clause counts and solver statistics.
