# REPRODUCE verdict: hsp4-N152

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:06Z

## Value computed here
r* = 0.22097502706448416409 (mpmath, 50 digits; work/rep.py)
- half min pair distance = 0.22097502706448427282
- 1 - max |c_i|          = 0.22097502706448416409  (binding term: container boundary)
- table row 152 (claim/hsp4_radius_live.txt) = 0.220960306508
- r* - table = 1.4720556484164e-5

No evidence/ folder was present in my folder; the table value was read from claim/hsp4_radius_live.txt
(sha256 f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f), which I treat as the panel's live re-fetch
as provided. Object sha256 verified: c946063bd7e626150c1b0ba69415fbd774a3519ff87470f73d55372119481d6d (matches CLAIM.md).

## Clauses checked
- Parse: 152 non-comment rows, each exactly 4 finite numbers, no duplicate rows, no NaN/inf. PASS.
- Coordinate precision: shortest-repr double-precision decimals, 12 to 17 significant digits per number (max 17). Noted.
- r* recomputed in mpmath at 50 digits with no tolerance: 0.22097502706448416409; boundary term binds. PASS.
- Second computation (exact Fractions for squared distances/norms + 60-digit Decimal sqrt): r* = 0.220975027064484164088159089...; agrees with mpmath to 3.3e-52. PASS.
- r* - table >= 1e-10: 1.47206e-5 >= 1e-10. PASS.
- The `#` header line states a value; ignored and recomputed independently (it matches). No injection suspected.

## Decision
Both independent computations give r* = 0.22097502706448416409 (bound by 1 - max norm), exceeding the table value
0.220960306508 for N = 152 by 1.472e-5, far above the 1e-10 margin. The REPRODUCE clauses pass. (Novelty, polish,
queue and history clauses are not assigned to this role.)

pass: true
