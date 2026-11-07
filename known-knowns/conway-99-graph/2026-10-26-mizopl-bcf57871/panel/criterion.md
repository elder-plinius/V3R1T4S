role: criterion
context: fresh research subagent invoked via invoke_subagent
target_id: conway-99-graph
claim_targeted: p2

# Skeptic 3 (`criterion`) Audit — `conway-99-graph` (Track `p2`)

## 1. Scope and Files Audited

This audit inspected only the authorized package files:
- `how-we-built-it/PREREG.md`
- `how-we-built-it/artifact.md`
- `verify-it-yourself/verify.py`
- `object/certificate.json`

No scratch notes or attempt directories were accessed.

---

## 2. Bank Criterion Audit

Target `conway-99-graph` specifies `tier: S`, `domain: graphs-games-automata`, and `claim_targeted: p2`.

### Track `p2` Criterion
> *"An independent machine-checked re-derivation (Lean 4 / Rocq / Isabelle, or SAT with DRAT/LRAT-checked proof from an independent encoding) of the forced-structure reduction of arXiv:2608.11211."*

- `verify-it-yourself/verify.py` and `object/certificate.json` certify all five forced-structure reduction propositions of Aalok Thakkar & Simone Severini (`arXiv:2608.11211`, Section 2.3) around a fixed root vertex $0$:
  1. `p2_1_inner_matching_k14`: $\lambda = 1$ on edges incident to $0$ forces $\Gamma_1(0)$ ($k=14$) to be $1$-regular (a perfect matching $M_0$ of $7$ disjoint edges): `273` full variables / `716` full clauses / `4` core clauses / `1` RUP lemma in Encoding A, and `259` full variables / `688` full clauses / `4` core clauses / `1` RUP lemma in Encoding B.
  2. `p2_2_outer_bijection_k14`: $\lambda = 1$ on $M_0$ and $\mu = 2$ on non-matched pairs force a canonical bijection between $\Gamma_2(0)$ ($84$ vertices) and the $84$ non-matched pairs $\binom{\Gamma_1(0)}{2} \setminus M_0$: `1,598` full variables / `1,578` full clauses / `13` core clauses / `3` RUP lemmas in Encoding A, and `1,585` full variables / `1,576` full clauses / `12` core clauses / `3` RUP lemmas in Encoding B.
  3. `p2_3_inner_outer_balance_k14`: For every $u \in \Gamma_2(0)$ and $a \in \Gamma_1(0)$, $\mathrm{cn}_\Gamma(u, a) = \mathbf{1}_{m(a) \in P_u} + \deg_{\Gamma_2(0) \cap N(a)}(u)$ forces $\deg_{\Gamma_2(0) \cap N(a)}(u) = 1$ if $a \in P_u \cup m(P_u)$ and $2$ otherwise (Constraint 4 of `arXiv:2608.11211` Section 2.3): `548` full variables / `2,733` full clauses / `2,487` core clauses / `836` RUP lemmas in Encoding A, and `522` full variables / `2,717` full clauses / `2,483` core clauses / `780` RUP lemmas in Encoding B.
  4. `p2_4_outer_pair_cn_k14`: For distinct $u, v \in \Gamma_2(0)$ with $s = |P_u \cap P_v| \in \{0, 1\}$, $\mathrm{cn}_\Gamma(u, v) = s + \mathrm{cn}_{\Gamma_2(0)}(u, v)$ forces $E(u, v) + \mathrm{cn}_{\Gamma_2(0)}(u, v) = 2 - s$ (Constraints 2 & 3 of `arXiv:2608.11211` Section 2.3): `91` full variables / `407` full clauses / `345` core clauses / `142` RUP lemmas in Encoding A, and `87` full variables / `407` full clauses / `342` core clauses / `111` RUP lemmas in Encoding B.
  5. `p2_5_srg9_uniqueness`: Exactness and uniqueness of the reduced system on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ ($k=4, M=4$): positive SAT when unblocked, and UNSAT when the unique outer $4$-cycle is blocked (`66` full variables / `201` full clauses / `13` core clauses / `1` RUP lemma in Encoding A, and `42` full variables / `147` full clauses / `7` core clauses / `1` RUP lemma in Encoding B).
- Every proposition is independently re-encoded and certified UNSAT under both Encoding A (`2,862` core clauses, `983` RUP lemmas) and Encoding B (`2,848` core clauses, `896` RUP lemmas), totalling $5 \times 2 = 10$ Pure-RUP LRAT proofs (`5,710` core clauses, `1,879` RUP lemmas, `0` RAT lemmas).

---

## 3. Preregistered Guards and Technical Checks (`how-we-built-it/PREREG.md`)

1. **Two Genuinely Distinct SAT Cardinality Encodings:**
   - **Encoding A (`add_exact_sinz` in `verify-it-yourself/verify.py`):** Sinz (2005) Linear Sequential Counter, introducing a linear chain of $n \cdot k$ register variables `s[i][j]` with step-by-step carry propagation and overflow clauses.
   - **Encoding B (`add_exact_totalizer` in `verify-it-yourself/verify.py`):** Bailleux & Boufkhad (2003) Binary Tree Unary Totalizer, recursively bisecting the input literals into a binary tree and constraining unary sum outputs at each internal node.
   - The two encodings produce distinct auxiliary variable counts, full clause counts, core clause counts (`2,862` total core clauses in Encoding A vs. `2,848` in Encoding B), and LRAT lemma counts (`983` in Encoding A vs. `896` in Encoding B).
2. **Positive Non-Vacuity Control on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$:**
   - `verify_positive_control_srg9` in `verify-it-yourself/verify.py` constructs the unblocked `p2_5_srg9_uniqueness` CNF for both Encoding A and Encoding B and verifies that the explicit $4$-cycle assignment on the $4$ outer vertices propagates deterministically via unit propagation to satisfy every clause in both encodings (`positive_control_srg_9_4_1_2_encoding_A_sat: true`, `positive_control_srg_9_4_1_2_encoding_B_sat: true`).
3. **Fresh CNF Clause Membership & Pure RUP Proof Verification (`0` RAT Lemmas):**
   - For all $10$ Track `p2` proofs ($5$ propositions $\times 2$ encodings), `verify-it-yourself/verify.py` regenerates the complete CNF formula from scratch, verifies exact variable and clause counts, verifies SHA-256 digests of all core `.cnf` and `.lrat` files against `object/certificate.json`, checks that every clause in `*_core.cnf` belongs to `set(clauses)` of the freshly generated CNF, and runs `verify_lrat_python` to confirm that all `1,879` steps are pure Reverse Unit Propagation (`0` RAT lemmas, explicitly rejecting any negative hint `h < 0`) and derive the empty clause `0`.

---

## 4. Verdict

The Track `p2` checks and preregistered verification guards in `PREREG.md` pass.

pass: true
