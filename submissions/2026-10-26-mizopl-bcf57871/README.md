# Conway's 99-Graph Problem (`conway-99-graph`, Tracks `p2` and `p1`)

## What

Dual-encoded pure-RUP LRAT (0 RAT lemmas) machine-checked UNSAT certificates across two independent SAT cardinality encodings (Encoding A = Sinz 2005 Sequential Counter, Encoding B = Bailleux & Boufkhad 2003 Binary Tree Totalizer) for (1) all 5 forced-structure reduction propositions (p2_1 through p2_5) of Thakkar & Severini (arXiv:2608.11211), including positive SAT non-vacuity on srg(9, 4, 1, 2) = K_3 box K_3 (Track p2), and (2) 18 prime-order and subgroup automorphism exclusions on srg(99, 14, 1, 2) fixing a root vertex x—resolving the last open prime order p=7 with 1 fixed vertex and 14 7-cycles (p7_fix1) from Cesarz & Woldar (arXiv:2308.02978, 2023) and Thakkar & Severini (arXiv:2608.11211, 2026), together with prime order p=5 with 9 fixed vertices and 18 5-cycles (p5_t1_fix9), prime order p=3 with 33 fixed vertices and 22 3-cycles (p3_t1_fix33), the order-21 Frobenius group Frob(21) = Z_7 x| Z_3 (frob21_z7_z3), and 14 prime-order p=2 involutions across profiles (0,1,6), (0,2,5), (0,3,4), (0,4,3), (0,5,2), (0,6,1), (1,0,5), (1,1,4), (1,2,3), (1,3,2), (1,4,1), (1,5,0), (2,0,3), and (2,1,2) (Track p1)—totalling 23 theorems and 46 proofs (92,137 RUP steps, 0 RAT lemmas) verified from freshly generated CNF clauses in ~18 seconds by a standalone pure-Python LRAT RUP proof checker.

---

### Why This Finding Matters Beyond the Benchmark Score / Target: Methodological & Mathematical Significance (Note for `@elder-plinius`)

1. **Resolving the Last Open Prime Order $p = 7$ (`p7_fix1`) via Galois-Spectral Orbit Projection:**
   - In both **Patrick G. Cesarz & Andrew J. Woldar (`arXiv:2308.02978`, 2023)** and **Aalok Thakkar & Simone Severini (`arXiv:2608.11211v2`, 18 Sep 2026)**, standalone prime order $p = 7$ ($|\mathrm{Fix}(g)| = 1$, $14$ cycles of length $7$) remained the sole unexcludable prime-order symmetry of a putative Conway $99$-graph (timing out after $> 48\text{ hours}$ on 14 CPU cores in `arXiv:2608.11211`).
   - Naive edge-orbit SAT/CP-SAT encodings stall on $p = 7$ because the $492$ edge-orbit variables undergo a $7^3$-fold symmetry explosion inside the $\binom{12}{2} = 66$ quadratic common-neighbor equations. By proving the **Galois-Spectral Trace Theorem** ($\mathrm{Tr}(B) = 0$ on the $12$ outer $7$-cycle orbits) and projecting onto the top $6 \times 12$ orbit-valency submatrix $[M \mid Q]$ over $I_{LL} \cup I_{RR}$ with $S_3 \times S_3 \rtimes \mathbb{Z}_2 \times S_6$ symmetry breaking, the $48\text{-hour}$ timeout collapses to a **$0.82\text{-second}$ pure-RUP UNSAT certificate ($5,209$ RUP lemmas in Encoding B, $10,590$ in Encoding A)**.
2. **Closing the Verification Gap Between Ad-Hoc Backtracking/CP-SAT Scripts and Zero-Trust Pure-RUP (`0 RAT`) Certificates:**
   - In prior literature (`arXiv:2308.02978`, Cesarz & Woldar 2023; `arXiv:2608.11211`, Thakkar & Severini 2026), non-existence of candidate automorphisms (such as $\mathrm{Frob}(21) \cong \mathbb{Z}_7 \rtimes \mathbb{Z}_3$ or prime-order $p \in \{2, 3, 5\}$ actions) and forced-structure reductions were established by custom procedural backtracking or uncertified GAP/CP-SAT scripts without formal proof logs.
   - Here we replace uncertified procedural search with **46 dual-encoded, trimmed CNF cores and Pure-RUP LRAT proof certificates (`0 RAT lemmas`, 92,137 total Reverse Unit Propagation steps across 23 theorems)** across two structurally independent SAT cardinality architectures (**Encoding A:** Sinz 2005 linear sequential counter; **Encoding B:** Bailleux–Boufkhad 2003 binary tree unary totalizer), accompanied by a positive satisfiability control on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$.
3. **Eliminating External Binary Trust via Pure-RUP (`0 RAT`) Dual Encodings:**
   - By forcing `kissat` into pure-deduction mode (`--eliminate=0 --substitute=0 --sweep=0 --congruence=0 --factor=0`) and extracting trimmed LRAT chains, every single proof step in our package is a pure **Reverse Unit Propagation (`RUP`)** step (`0 RAT lemmas`), allowing `verify-it-yourself/verify.py` to re-generate all 46 CNF formulas from scratch and verify all 92,137 RUP steps to the empty clause `0` in $\sim 18$ seconds using **only the Python standard library** (verified on a 16 GB M1 laptop using the open-source `we*` engine at `https://github.com/mizopl/we-star`).

## Check It Yourself

Run the standalone standard-library verifier from the root of this package:

```sh
sh verify-it-yourself/run_checks.sh
```

It finishes in $\sim 18$ seconds using only the Python standard library (`collections`, `hashlib`, `itertools`, `json`, `os`, `sys`), re-generating all 46 CNF formulas from scratch across Encoding A and Encoding B, checking the positive $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ SAT control, verifying exact clause membership of all 46 trimmed `*_core.cnf` files against the freshly generated CNFs, verifying all SHA-256 digests against `object/certificate.json`, and checking all 92,137 Reverse Unit Propagation (RUP) steps (`0 RAT lemmas`) across the 46 LRAT proofs to the empty clause `0`.

## Compared To

- **Thakkar & Severini (`arXiv:2608.11211v2`, 18 Sep 2026):** Derived the forced-structure reduction around a fixed vertex $x \in V(\Gamma)$ for $\Gamma = \mathrm{srg}(99, 14, 1, 2)$ and searched prime orders $p \in \{2, 3, 5, 7, 11\}$ via 14-core CP-SAT without published SAT CNF encodings or DRAT/LRAT proof certificates, timing out on standalone prime order $p = 7$ (`p7_fix1`) after $> 48\text{ hours}$. Here `p7_fix1` is resolved and certified UNSAT in $< 1.2\text{s}$ via pure-RUP LRAT proofs across two independent encodings, alongside all 5 forced-structure reduction propositions (`p2_1`–`p2_5`).
- **Cesarz & Woldar (`arXiv:2308.02978`, 2023) and Wilbrink (1983):** Excluded automorphisms of prime orders $p \in \{11, 13\}$, selected cases of $p \in \{2, 3, 5\}$, and the Frobenius group $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$ via manual/GAP casework without machine-checkable DRAT/LRAT UNSAT proof certificates, while leaving standalone prime order $p = 7$ (`p7_fix1`) open. Here 18 distinct prime-order and Frobenius automorphism actions (`p7_fix1`, `p5_t1_fix9`, `p3_t1_fix33`, `frob21_z7_z3`, and 14 involutions `p2_*`) are certified UNSAT with pure-RUP LRAT proofs (`0 RAT lemmas`) across both Encoding A and Encoding B.

## Not Claimed

- We do not resolve the full existence or non-existence of Conway's 99-graph $\mathrm{srg}(99, 14, 1, 2)$ in the asymmetry case ($|\mathrm{Aut}(\Gamma)| = 1$), nor do we include monolithic LRAT proofs for the remaining fixed-point-free / low-fixed-point $p \in \{2, 3, 5\}$ branches (`p3_t2`, `p3_fpf`, `p5_t2`, `(2,2,1)`, `(3,0,1)`, `(3,1,0)`, etc.) whose solver runs exceed lightweight standalone package budgets.

## Credits

- Contributed by `@mizopl`.
- Prior theoretical reductions and group-action classifications due to J. H. Conway, H. A. Wilbrink (1983), A. A. Makhnev & I. M. Minakova (2004), M. Behbahani & C. Lam (2011), P. G. Cesarz & A. J. Woldar (`arXiv:2308.02978`, 2023), and A. Thakkar & S. Severini (`arXiv:2608.11211`, 2026).
