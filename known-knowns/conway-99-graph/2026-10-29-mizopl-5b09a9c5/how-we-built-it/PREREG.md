# Preregistration — `conway-99-graph` — 2026-10-26T05:19:00Z

Written BEFORE any computation or proof attempt begins. This file is frozen once Stage 2 starts.

## 1. Target and track

- `problem_id`: `conway-99-graph`
- `tier`: `S`
- `domain`: `graphs-games-automata`
- `claim_targeted`: `p1` and `p2`
- Why this track: Both `p2` (an independent machine-checked SAT + DRAT/LRAT re-derivation of the forced-structure reduction of `arXiv:2608.11211`) and `p1` (a DRAT/LRAT-checked, independently re-encoded proof excluding a specified prime-order automorphism with stated fixed-point/cycle structure not already excluded by `arXiv:2308.02978` or `arXiv:2608.11211`) can be attacked directly by hanging the Section 2.3 forced-structure reduction at a fixed vertex $x$ of the automorphism and certifying the resulting CNF encodings with `kissat` + `drat-trim` (generating both DRAT and LRAT proofs).

## 2. Specific hypothesis (falsifiable)

- **Statement (Lens 1, Track `p2`):** From two independent Boolean CNF encodings (Encoding A: direct clause expansion; Encoding B: auxiliary Tseitin / sequential-counter cardinality encoding) of the local $\mathrm{srg}(v, k, 1, 2)$ axioms $(\lambda = 1, \mu = 2)$, the negation of each forced-structure reduction proposition of `arXiv:2608.11211` Section 2.3—(R1) $1$-regular perfect matching on $\Gamma_1(0)$, (R2) bijection between $\Gamma_2(0)$ and the $M = \binom{k}{2} - k/2$ non-matched pairs of $\Gamma_1(0)$, (R3) inner-outer coordinate balance $[m(a) \in P_u] + \deg_{\Gamma_2(0) \cap N(a)}(u) = 2$ for $a \notin P_u$ and $\deg_{\Gamma_2(0) \cap N(a)}(u) = 1$ for $a \in P_u$, (R4) outer pair common-neighbor count $(1 \text{ if } u \sim v \text{ else } 2) - |P_u \cap P_v|$, and (R5) uniqueness of the reduced outer graph on $\mathrm{srg}(9, 4, 1, 2)$—is UNSAT with a `drat-trim`-verified DRAT and LRAT proof.
- **Statement (Lens 2, Track `p1`):** Combining the forced-structure reduction at a fixed vertex $x$ with two independent Boolean CNF encodings of prime-order automorphisms fixing $x$ yields `drat-trim`-verified DRAT and LRAT UNSAT certificates excluding specified prime-order automorphism structures (including prime-order $p = 3$ automorphisms fixing $x$ with specified fixed-point/cycle structure on $\Gamma_1(x)$ and $\Gamma_2(x)$, the Frobenius extension $\mathrm{Frob}(21)$, and/or the single-fixed-point prime-order $p = 7$ automorphism with 1 fixed vertex and 14 cycles of length 7) that are not already excluded with DRAT/LRAT proofs in `arXiv:2308.02978` or `arXiv:2608.11211`.
- **What would falsify it:** If a satisfying assignment is found (which would construct $\mathrm{srg}(99, 14, 1, 2)$ and win Track `full`!), or if `drat-trim` / the independent LRAT/RUP checker rejects any generated proof, or if the two independent encodings disagree on any test case.

## 3. Attack plan (ordered lenses)

1. **Lens 1 (`attempts/lens1_p2_forced_structure_drat_lrat/`):**
   - Implement two independent CNF generators (Encoding A and Encoding B) for the forced-structure reduction propositions (R1)–(R5) of `arXiv:2608.11211`.
   - Solve with `kissat`, extract trimmed `.drat` and `.lrat` proofs via `drat-trim`, and verify every `.lrat` proof both with `drat-trim` and with a standalone pure-Python LRAT/RUP verifier.
2. **Lens 2 (`attempts/lens2_p1_automorphism_drat_lrat_exclusions/`):**
   - Implement two independent CNF generators (Encoding A and Encoding B) for prime-order automorphisms fixing vertex $0$ in the forced-structure coordinates on $\Gamma_1(0) \cup \Gamma_2(0)$:
     - Prime $p = 3$ automorphisms fixing vertex $0$ (examining all possible fixed-point counts $|\mathrm{fix}(g) \cap \Gamma_1(0)| \in \{0, 2, 4, 6, 8, 10, 12, 14\}$ and cycle structures on $\Gamma_1(0)$ and $\Gamma_2(0)$, which were NOT analyzed in `arXiv:2308.02978` and NOT solved in `arXiv:2608.11211`, where `arXiv:2608.11211` only tested fixed-point-free $p=3$ and timed out).
     - Prime $p = 7$ single-fixed-point automorphism ($|\mathrm{fix}(g)| = 1$, fourteen $7$-cycles) and its $\mathrm{Frob}(21)$ / QR(9)-subconstituent refinements.
   - Solve with `kissat`, verify UNSAT certificates with `drat-trim` (`s VERIFIED`), and export both `.drat` and `.lrat` certificates verified by the standalone pure-Python LRAT/RUP checker.

## 4. Verification plan

- **Verification script:** `claim/verify.py` (deterministic, offline, pure Python stdlib + `numpy`/`scipy`/`sympy`, runtime `< 60` seconds).
- **Checks performed by `claim/verify.py`:**
  1. Re-generates the DIMACS CNF formulas from both independent encodings (Encoding A and Encoding B) for all claimed `p2` and `p1` propositions and verifies their structural equivalence and exact clause/variable counts.
  2. Runs an embedded, complete pure-Python LRAT/RUP proof checker on every `.lrat` / `.drat` certificate in `claim/`, verifying that every derived clause follows by Reverse Unit Propagation (RUP) from active clauses up to the empty clause `0`.
  3. Verifies positive satisfiability controls (specifically that $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ satisfies all forced-structure and $\mathbb{Z}_3$-automorphism encodings before the blocking clause is added).
  4. Compares all computed counts, hashes, and verification statuses against `claim/certificate.json`.
- `null_test`: not needed because this is a deterministic mathematical and SAT/LRAT proof-verification run with zero statistical or empirical noise; non-vacuity is established by positive satisfiability controls ($\mathrm{srg}(9, 4, 1, 2)$ satisfying the unblocked forced-structure and automorphism encodings) and by corrupting `claim/certificate.json` to confirm `verify.py` fails on tampering.

## 5. Compute and time budget

- Max wall-clock for Stage 2: 45 minutes.
- Max verification runtime for `claim/verify.py`: `< 60` seconds on CPU.
- Stopping rule: Stop and package once all `p2` forced-structure proofs and `p1` prime-order automorphism exclusion proofs are verified by both `drat-trim` and the standalone Python LRAT/RUP verifier across two independent CNF encodings.

## 6. What will be logged as a dead end if this fails

- Any prime-order automorphism subcase whose SAT instance exceeds the 45-minute Stage 2 wall-clock budget without yielding a verified DRAT/LRAT certificate will be logged honestly in `attempts/.../NOTES.md` with exact variable/clause counts and solver statistics.
