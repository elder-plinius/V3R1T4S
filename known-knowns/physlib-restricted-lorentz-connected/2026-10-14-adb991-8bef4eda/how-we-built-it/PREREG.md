# Pre-registration: physlib-restricted-lorentz-connected (frozen 2026-10-14T06:10:39Z, before any attack output)

frozen_utc: 2026-10-14T06:10:39Z

## Criterion (verbatim, see target.md)
A kernel-checked proof of Physlib's `semiformal_result "FXNL5" restricted_isConnected {d : ℕ} :
IsConnected (restricted d : Set (LorentzGroup d))`, for every `d : ℕ`, against Physlib
be0f21e5002d6d73b87f2055530c1e8bf7151546, with no `sorry` and no axioms beyond `propext`, `Classical.choice`,
`Quot.sound`; or a counterexample to the statement as written.

## Statistic / checker
`checker/lean_claim_check.py` on `checker/spec_restricted_isConnected.lean` (frozen in the setup dry run). Decision:
PASS (last line) = claim made; anything else = no claim. A proof for some `d` only is not a claim.

## Thresholds
None beyond PASS/FAIL.

## Null design
null_test: not needed because the claim is a proof checked by a deterministic proof kernel against a frozen
statement; there is no search statistic, score or "beats chance" component.
