# Skeptic 2 (NOVELTY) Report — `etp-finite-magma-677-255` (`p2`)

context: subagent (fresh NOVELTY skeptic)
run_id: 2026-11-01-1637
target_id: etp-finite-magma-677-255
claim_level: partial_win_claim (p2)

## 1. Scope Compliance

Per panel rules, only the contents of `claim/` (`claim/claim.md`, `claim/target.md`, `claim/REPRODUCE.md`, `claim/Equation677.lean`, `claim/separation_models.json`, `claim/check_p2.py`, `claim/status_snapshot.md`) and the primary status sources (`https://teorth.github.io/equational_theories/dashboard/`, `https://teorth.github.io/equational_theories/raw_data/finite_outcomes.json.gz`, upstream `references/equational_theories/equational_theories/ManuallyProved/Equation677.lean`, `references/equational_theories/blueprint/src/chapter/677.tex`, ETP issue/PR metadata in `data/`, and `repo/TROPHY_CASE.md`) were inspected. `BRIEF.md`, `PREREG.md`, and `attempts/` were not read.

## 2. Live Primary Source Re-Fetch Receipt

A fresh live re-fetch was executed using `curl -A "V3R1T4S/1.0"` at `2026-11-01T17:18:14Z`:

1. **ETP Dashboard (`https://teorth.github.io/equational_theories/dashboard/`)**:
   - Saved to: `data/panel_dashboard.html`
   - Timestamp (UTC): `2026-11-01T17:18:14Z`
   - HTTP Status: `200`
   - SHA-256: `0023faf95ebdf76ae257384c4987834d73f0672e4386f8a95c4a04a8167896df`
   - Finite graph table status: `no proof = 2`, `99.99999%` complete (`10,750` explicitly true, `8,168,349` implicitly true, `586,220` explicitly false, `13,268,315` implicitly false).
2. **ETP Finite Outcomes Matrix (`https://teorth.github.io/equational_theories/raw_data/finite_outcomes.json.gz`, linked from line 254 of `data/panel_dashboard.html`; note that `dashboard/finite_outcomes.json.gz` returns HTTP `404` because the dashboard hosts raw exports under `raw_data/`)**:
   - Saved to: `data/panel_finite_outcomes.json.gz`
   - Timestamp (UTC): `2026-11-01T17:18:14Z`
   - HTTP Status: `200`
   - SHA-256: `908b6220182853ff71b3b73328987c890569ab6d4da429f730e2d105129f9f36`
   - Verification of open entries: Out of all `4694 × 4694 = 22,033,636` entries in `outcomes`, exactly 2 entries are `"unknown"`:
     - `outcomes[676][254] = "unknown"` (0-indexed for `Equation677 => Equation255`)
     - `outcomes[2909][46] = "unknown"` (0-indexed for `Equation2910 => Equation47`)

## 3. Audit Against Upstream ETP Repository, Blueprint, Issues/PRs, and `TROPHY_CASE.md`

### 3.1 Upstream `equational_theories/ManuallyProved/Equation677.lean` vs `claim/Equation677.lean`
Upstream `references/equational_theories/equational_theories/ManuallyProved/Equation677.lean` (commit `2f49bdaf3d38ffb722e54ac1288c8269dac61846`, 108 lines, SHA-256 `ad46b8e3015f43da7eb602924c27c6ab22f65f206f80b6ed802aa01122e963d4`) contains only 11 basic helper lemmas in `namespace Eq677`:
- `eq677_leftMul_surj`, `eq677_leftInv_formula`, `eq255_equiv_RxLx`, `eq677_leftMul_inj`, `eq677_left_cancel`, `eq677_backward_recurrence`, `eq677_fixer_unique`, `eq255_from_fixer_exists`, `eq255_equiv_LxRx`, `eq677_key_identity`, `eq677_star_eq`.

`claim/Equation677.lean` (SHA-256 `dcc89550b0e5ce6d4e15f6e283a0401ccdaf9831289189929e67fa48cfebbe7f`, 399 lines) directly imports `equational_theories.Equations.All` and `equational_theories.ManuallyProved.Equation677` without duplicating any of the 11 existing lemmas, and adds 9 conditional implication / structural theorems plus 3 formal separation counterexamples, **none** of which exist in upstream `Equation677.lean`:
- `Eq677.eq677_leftMul_fixed_disjoint` — **New** (absent upstream)
- `Eq677.eq255_of_eq677_leftMul_has_fixed_point` (**Primary `p2` theorem**) — **New** (absent upstream)
- `Eq677.eq255_of_eq677_right_cancel` — **New** (absent upstream)
- `Eq677.eq255_of_eq677_quasigroup` — **New** (absent upstream)
- `Eq677.eq677_leftMul_faithful` — **New** (absent upstream)
- `Eq677.eq255_of_eq677_uniform_leftMul` — **New Lean formalization** (absent from `Equation677.lean`; corresponds to prose Lemma 13.3 in `677.tex` generalized to `UniformLeftMul`)
- `Eq2910.eq47_of_eq2910_rightMul_has_fixed_point` — **New** (upstream has zero `Equation2910` theorems)
- `Eq2910.eq47_of_eq2910_left_cancel` — **New** (upstream has zero `Equation2910` theorems)
- `Eq2910.eq47_of_eq2910_quasigroup` — **New** (upstream has zero `Equation2910` theorems)
- `Eq677.Separation.Sep7`, `Sep25`, `Sep55` and the 3 separation theorems (`not_leftMulHasFixedPoint_of_conjClosed`, `not_conjClosed_of_rightCancel_and_leftMulHasFixedPoint`, `not_rightCancel_and_not_conjClosed_of_leftMulHasFixedPoint`) — **New** (absent upstream).

### 3.2 Upstream Blueprint (`blueprint/src/chapter/677.tex`)
`references/equational_theories/blueprint/src/chapter/677.tex` (164 lines, SHA-256 `daeb5199018e0d8c0f063ac1b00bd989ba7321699a087df527c858380b61816c`) states in prose:
- Lemma 13.1 (`677-basic`): left multiplication invertibility, fixer uniqueness $y \diamond x = x \implies y = Sx \diamond x$, and backward recurrence.
- Lemma 13.2 (`255-equiv`): pointwise equivalences for 255 at $x$, including solvability of $R_x y = x$.
- Lemma 13.3 (`linear-obstruction`) and Lemma 13.4 (`linear-2`): linear models $x \diamond y = \alpha x + \beta y + c$ and linear extensions satisfy 255.
- Section 13.1: an order-496 ($31 \times 16$) non-right-cancellative finite 677 magma.
- Section 13.2: the infinite free 677 magma.

The primary `p2` hypothesis `EveryLeftMulHasFixedPoint` ($\forall y, \exists x, y \diamond x = x$), the fixed-point disjointness theorem (`eq677_leftMul_fixed_disjoint`), the resulting conditional implication `eq255_of_eq677_leftMul_has_fixed_point`, and the separation models `Sep25` (order 25) and `Sep55` (order 55) do not appear even in prose in `677.tex`.

### 3.3 ETP Issues and Pull Requests (`#1464`, `#1517`, PR `#1518`, and search)
- **Issue `#1464`**: Proposes a 1-point orbit lemma `(c ◇ c) ◇ c = c ◇ c ↔ c ◇ c = c` and an order-10 SAT/DRAT search. Does not contain any of the claimed conditional implication theorems or separation models.
- **Issue `#1517` and PR `#1518` (closed unmerged)**: Proves `eq255_of_eq677_leftMul_conjugacy_closed` under the hypothesis that left translations are closed under conjugation (`∀ a b, ∃ c, L_c = L_a ∘ L_b ∘ L_a⁻¹`, formalized in `claim/Equation677.lean` as `LeftMulConjugacyClosed`). Does not prove the implication under `EveryLeftMulHasFixedPoint`, `RightCancellative`, `LeftCancellative`, `IsQuasigroup`, or `UniformLeftMul`, and contains no theorems for `Equation2910 => Equation47`.
- **Other ETP issues/PRs (`data/etp_search_677_2910.json`, `data/etp_recent_issues.json`)**: No other conditional Lean proofs of `677 => 255` or `2910 => 47` appear in the searched ETP issues and PRs (`#1464`, `#1517`, `#1518`, `data/etp_search_677_2910.json`, `data/etp_recent_issues.json`).

### 3.4 `repo/TROPHY_CASE.md` and V3R1T4S PRs
- `repo/TROPHY_CASE.md` contains 53 rows across 7 families and zero entries for `etp-finite-magma-677-255` or the Equational Theories Project.
- `data/v3r1t4s_prs_search.json` confirms 0 open or closed PRs on `etp-finite-magma-677-255`.

## 4. Verification of Two-Sided Logical Independence from Issue `#1517` (`LeftMulConjugacyClosed`)

The `p2` criterion requires:
> A Lean proof of the implication under an additional natural hypothesis (e.g. the magma is a quasigroup, or left-cancellative) that is neither implied by nor equivalent to a hypothesis already proved in the ETP issues (e.g. the translation-conjugacy closure of issue #1517), stated as a separate theorem.

`claim/claim.md` scopes the primary `p2` claim specifically to `EveryLeftMulHasFixedPoint` (`eq255_of_eq677_leftMul_has_fixed_point` for `Equation677 => Equation255`), while presenting `RightCancellative`, `IsQuasigroup`, and `UniformLeftMul` as additional conditional implication theorems.

Running `python3 claim/check_p2.py claim/separation_models.json claim/Equation677.lean` (SHA-256 `3bc4c61269baed20814fd352d8f0b0fbed1cbebccb57a0c7d5d73b667ea89ec3`, `f92fb469669e9911e75fb8db65e566eea9db82d7491a581965db76b82a90f4bb`, and `dcc89550b0e5ce6d4e15f6e283a0401ccdaf9831289189929e67fa48cfebbe7f`) verifies all three finite separation witnesses on finite `Equation677` (and `Equation255`) magmas:

| Witness | Order | `Equation677` & `Equation255` | `RightCancellative` / `IsQuasigroup` | `EveryLeftMulHasFixedPoint` | `LeftMulConjugacyClosed` (#1517) | What it separates |
|---|---|---|---|---|---|---|
| `Sep7` (`Fin7`) | 7 | True | True | **False** | **True** | `LeftMulConjugacyClosed` (and `RightCancellative`) $\not\implies$ `EveryLeftMulHasFixedPoint` |
| `Sep25` (`Fin25`) | 25 | True | **True** | **True** | **False** | Neither `EveryLeftMulHasFixedPoint` nor `RightCancellative` (`IsQuasigroup`) $\implies$ `LeftMulConjugacyClosed` |
| `Sep55` (`Fin55`) | 55 | True | **False** | **True** | **False** | `EveryLeftMulHasFixedPoint` $\not\implies$ `RightCancellative` and $\not\implies$ `LeftMulConjugacyClosed` |

Specifically:
1. **Primary `p2` Hypothesis (`EveryLeftMulHasFixedPoint`) vs `LeftMulConjugacyClosed` (Issue `#1517`)**:
   - **Not implied by** `LeftMulConjugacyClosed`: `Sep7` (`not_leftMulHasFixedPoint_of_conjClosed`) satisfies `Equation677`, `Equation255`, `RightCancellative`, and `LeftMulConjugacyClosed`, and violates `EveryLeftMulHasFixedPoint`.
   - **Does not imply and is not equivalent to** `LeftMulConjugacyClosed`: `Sep25` (`not_conjClosed_of_rightCancel_and_leftMulHasFixedPoint`) and `Sep55` (`not_rightCancel_and_not_conjClosed_of_leftMulHasFixedPoint`) satisfy `Equation677`, `Equation255`, and `EveryLeftMulHasFixedPoint`, and violate `LeftMulConjugacyClosed`.
   - **Two-sided separation from `RightCancellative`**: `Sep7` is right-cancellative and violates `EveryLeftMulHasFixedPoint`, whereas `Sep55` satisfies `EveryLeftMulHasFixedPoint` and violates `RightCancellative`.
2. **Additional Conditional Implication Hypotheses (`RightCancellative`, `IsQuasigroup`, `UniformLeftMul`)**:
   - Clearly distinguished in `claim/claim.md` as additional theorems alongside the primary `EveryLeftMulHasFixedPoint` theorem, with `Sep25` proving they do not imply and are not equivalent to `LeftMulConjugacyClosed` (and explicitly noting that whether `LeftMulConjugacyClosed` implies `RightCancellative` on finite `Equation677` magmas remains open).

## 5. Verdict

The target implications `Equation677 => Equation255` and `Equation2910 => Equation47` remain `"unknown"` on the live ETP dashboard (`2026-11-01T17:18:14Z`). The updated `claim/Equation677.lean` (directly importing `equational_theories.ManuallyProved.Equation677`) and `claim/claim.md` establish `eq255_of_eq677_leftMul_has_fixed_point` under `EveryLeftMulHasFixedPoint` with complete, machine-checked two-sided separation (`neither implied by nor equivalent to` `LeftMulConjugacyClosed` of Issue `#1517` and `RightCancellative`) via `Sep7`, `Sep25`, and `Sep55`, alongside the additional conditional implication and dual theorems. None of these theorems or separation models exist in upstream `Equation677.lean`, ETP issues/PRs, or `repo/TROPHY_CASE.md`.

pass: true
