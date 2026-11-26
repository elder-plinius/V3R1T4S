# Status Snapshot (`the-record-we-beat/snapshot.md`)

## 1. Live Equational Theories Project Dashboard

- **URL**: `https://teorth.github.io/equational_theories/dashboard/`
- **Fetched (UTC)**: `2026-11-02T19:55:52Z` (pre-submission re-fetch; bank criterion requires a live fetch immediately before claiming)
- **HTTP Status**: `200`
- **Selected headers**: `content-type: text/html; charset=utf-8`, `last-modified: Mon, 02 Nov 2026 02:44:51 GMT`, `etag: "6ae7f923-29d4"`, `content-length: 10708`
- **Page SHA-256**: `5afe452a033cc43c692c30f0fdcf8d50166e3cba240d7a005bb5e63c7ec2d90d`
- **Extracted Finite Graph Status**:
  - Total equations: `4694` (`22,033,636` directed pairs)
  - Explicitly true: `10,750`; implicitly true: `8,168,349`
  - Explicitly false: `586,220`; implicitly false: `13,268,315`
  - Explicitly unknown / no proof: `2` (`99.99999%` complete)

## 2. Finite Outcomes Matrix (`finite_outcomes.json.gz`)

- **URL**: `https://teorth.github.io/equational_theories/raw_data/finite_outcomes.json.gz`
- **Fetched (UTC)**: `2026-11-02T19:55:56Z`
- **HTTP Status**: `200`
- **Selected headers**: `content-type: application/gzip`, `last-modified: Mon, 02 Nov 2026 02:44:53 GMT`, `etag: "6ae7f925-20d644"`, `content-length: 2152004`
- **File SHA-256**: `e9c6bcc5031f0d329fc75075f23513364925361515c80ba0498630bad73463e4`
- **Extracted Cells** (parsed `4694 x 4694` matrix; full value counts `implicit_proof_true: 8168349, explicit_proof_false: 586220, implicit_proof_false: 13268315, explicit_proof_true: 10750, unknown: 2`):
  - `outcomes[676][254] = "unknown"` (`Equation677 => Equation255`)
  - `outcomes[2909][46] = "unknown"` (`Equation2910 => Equation47`)

## 3. Upstream Formalization & Issue Baseline (`teorth/equational_theories`)

- **Repository Commit**: `2f49bdaf3d38ffb722e54ac1288c8269dac61846`
- **`equational_theories/ManuallyProved/Equation677.lean` SHA-256**: `dc1050b709dfe6c5ce33b9c2afa264dd70041308356df4045739061942ebbf3f` (108 lines; contains only basic Blueprint Lemmas 13.1–13.2 and zero conditional implication theorems)
- **`blueprint/src/chapter/677.tex` SHA-256**: `e25f4c8e3ecfe454ad303782b68af69e41eb0572f780c5a7203cc8210b4b152e`
- **ETP Issue #1517 / PR #1518**: Proved `Equation677 => Equation255` under `LeftMulConjugacyClosed` (`L_{y₁}⁻¹ ∘ L_{y₂} ∘ L_{y₁} = L_z`). Our package proves `Equation677 => Equation255` under `EveryLeftMulHasFixedPoint` (`eq255_of_eq677_leftMul_has_fixed_point`) and formally proves by `decide` on `Sep7` (order 7), `Sep25` (order 25), and `Sep55` (order 55) that `EveryLeftMulHasFixedPoint` is neither implied by nor equivalent to `LeftMulConjugacyClosed` (nor implied by or equivalent to `RightCancellative`), alongside additional conditional implication theorems under `RightCancellative`, `IsQuasigroup`, and `UniformLeftMul` (proved non-equivalent to `LeftMulConjugacyClosed` by `Sep25`) and dual `Equation2910 => Equation47` theorems.
