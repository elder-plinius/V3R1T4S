---
panel_role: gate
status: CONFIRMED_SOLUTION
verdict: CONFIRMED_SOLUTION
confirmed_scope: Single-cell certificate for the open Huber-Wyderka table entry AME(17, 8) (quantum MDS code [[17, 0, 9]]_8, n = 17 parties of local dimension D = 8 = 2^3, sitting in the table's D in {2..10} column range where cell (n = 17, D = 8) is Blank at https://tp.nt.uni-siegen.de/ame/table.html), constructed as a symmetric 17x17 circulant graph state over GF(8) = GF(2)[w]/(w^3 + w + 1) with palindromic chord vector a = (1, 2, 5, 1, 5, 2, 2, 2) = (1, w, w^2+1, 1, w^2+1, w, w, w) and verified exhaustively across all C(17, 8) = 24,310 eight-party cuts over GF(8) (24,310 / 24,310 full rank 8, 0 rank-deficient cuts) and across all 24,310 eight-qudit (24-qubit) cuts of the 51-qubit binary trace-symplectic graph state [I_51 | B_51] over GF(2) (24,310 / 24,310 full rank 24).
date: 2026-11-07
target_id: ame-states-open-cells-huber-table
run_id: 2026-10-21-mizopl-d1cb5926
---

# Gate Verdict — `CONFIRMED_SOLUTION` (Single-Cell Huber–Wyderka Certificate `AME(17, 8)` / `[[17, 0, 9]]_8`)

- `status`: `CONFIRMED_SOLUTION`
- `reproduce`: `PASS`
- `novelty`: `PASS`
- `criterion`: `PASS`
- `confirmed_scope`: Single-cell certificate for the open Huber-Wyderka table entry AME(17, 8) (quantum MDS code [[17, 0, 9]]_8, n = 17 parties of local dimension D = 8 = 2^3, sitting in the table's D in {2..10} column range where cell (n = 17, D = 8) is Blank at https://tp.nt.uni-siegen.de/ame/table.html), constructed as a symmetric 17x17 circulant graph state over GF(8) = GF(2)[w]/(w^3 + w + 1) with palindromic chord vector a = (1, 2, 5, 1, 5, 2, 2, 2) = (1, w, w^2+1, 1, w^2+1, w, w, w) and verified exhaustively across all C(17, 8) = 24,310 eight-party cuts over GF(8) (24,310 / 24,310 full rank 8, 0 rank-deficient cuts) and across all 24,310 eight-qudit (24-qubit) cuts of the 51-qubit binary trace-symplectic graph state [I_51 | B_51] over GF(2) (24,310 / 24,310 full rank 24).

## Resolution of Reviewer Audit (`@elder-plinius`, `2026-11-06T18:43:53Z`)

1. **Removed all $D \ge 11$ cells (`AME(20, 11)`, `AME(19, 11)`, `AME(16, 13)`, `AME(20, 121)`, `AME(19, 289)`, etc.):**
   The Huber–Wyderka online table (`https://tp.nt.uni-siegen.de/ame/table.html`) covers local dimensions $D \in \{2..10\}$ only (`485` filled cells). All $D \ge 11$ certificates and C search programs have been removed from `object/` and `how-we-built-it/`.
2. **Scoped strictly to ONE in-range ($D \in \{2..10\}$) cell per package (`kit/SUBMIT.md` §1):**
   `object/` now contains a single certificate file, `object/ame_17_8_pure_circulant_certificate.json` (`4,176` bytes, `sha256: 0bc632480b2bfb3a90117f0676e8894dc5972ea32cb315cd47e1d04077f20a28`), certifying `AME(17, 8)` (`[[17, 0, 9]]_8`, $n = 17, D = 8 \in \{2..10\}$). Every other cell from the earlier multi-cell bundle has been removed from this pull request.
3. **Provenance against `https://tp.nt.uni-siegen.de/ame/table.html`, `https://www.codetables.de/QECC/`, and bank literature:**
   - **Huber–Wyderka live table (`https://tp.nt.uni-siegen.de/ame/table.html`):** Fetched `2026-10-20T01:10:09Z` and re-fetched `2026-11-07T15:09:42Z` (`HTTP 200`, `230,252` bytes, `sha256: e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082`). In column $D = 8$, `Yes` entries stop at $n = 14$; cell $(n = 17, D = 8)$ is **Blank** (`<td></td>`).
   - **Papers named in `bank/known-knowns/ame-states-open-cells-huber-table/`:** Neither Bidav (`arXiv:2608.05781`, Aug 2026, which covers `AME(12,5)` and $D \in \{11, 13\}$), nor `arXiv:2609.11796` / Ball (`arXiv:1907.04391`, *J. Phys. A* 2020, whose $\operatorname{AME}(2q-1, q)$ and $\operatorname{AME}(2q, q)$ theorems require **odd** characteristic $\operatorname{char}(\mathbb{F}_q) \ne 2$ and therefore do not apply to $D = 8 = 2^3$), nor `arXiv:2608.01011` ($n = 7$ only) constructs `AME(17, 8)`.
   - **Grassl's `codetables.de` (`https://www.codetables.de/QECC/QECC.php?q=64&n=17&k=0`):** Prior to `2026-10-21` (when we discovered `AME(17, 8)` on `2026-10-20`), `codetables.de` listed only lower bound $d = 8$ (`[[17, 0, 8..9]]_8`, strictly below the quantum Singleton bound $d = \lfloor 17/2 \rfloor + 1 = 9$), as recorded in `prior_status.codetables_de_best` inside `object/ame_17_8_pure_circulant_certificate.json`. On `2026-10-21` (one day before PR #614 was opened on `2026-10-22`), `@mizopl` communicated this palindromic $\mathbb{F}_8$ 17-circulant to Dr. Markus Grassl, who updated `https://www.codetables.de/QECC/QECC.php?q=64&n=17&k=0` (`last modified: 2026-10-21`, re-fetched `2026-11-07T15:09:42Z`, `HTTP 200`, `9,098` bytes, `sha256: c1565d91540ffdd9c4819f30773ced9161d9158e71e6d6aa7c4d1ce3586ee981`) to `lower bound: 9` (`[[17, 0, 9]]_8`) under **`Construction type: Gajewski`** (crediting the submitter of this PR) with the identical cyclic generator polynomial over $\mathbb{F}_8 \subset \mathbb{F}_{64}$ (verified in Step 4 of `verify-it-yourself/verify.py`).
4. **Removed invalid / withdrawn items and clarified `D31` / `D33–D35` as symmetry-restricted searches:**
   `AME(10, 10)` (`[[10, 2, 4]]_2`), the withdrawn `Q19/C20` items, and the $\mathbb{Z}_9$ reading of `AME(15, 9)` have been removed. The `D31` (`AME(8, 6)`) and `D33–D35` (`AME(7, 6)`, `AME(11, 10)`, `AME(12, 10)`) searches are symmetry-restricted searches (cyclic / circulant / group-ring ansätze), not general non-existence results across the full Hilbert space, and have been removed from `object/`.
5. **Exact exhaustive cut verification (`24,310 / 24,310` cuts, zero sampling or symmetry quotient in `verify.py`):**
   `verify-it-yourself/verify.py` iterates directly over all $\binom{17}{8} = 24,310$ eight-party cuts $S \subset \{0, \dots, 16\}$ (`|S| = 8`) and verifies full $\mathbb{F}_8$-rank `8` on `24,310 / 24,310` cuts (`0.40s`, `bad = 0`) as well as full $\mathbb{F}_2$-rank `24` across all `24,310 / 24,310` eight-qudit (`24`-qubit) cuts of the $51$-qubit binary trace-symplectic graph state $[I_{51} \mid B_{51}]$ (`0.66s`, `bad = 0`).
6. **Honest scope, receipts, and `SHA256SUMS`:**
   All multi-cell completion percentages have been removed and replaced with the exact verified single-cell counts (`24,310 / 24,310` cuts for `AME(17, 8)`), and `verify-it-yourself/RECEIPTS.md` and `SHA256SUMS` have been regenerated from clean execution outputs.
