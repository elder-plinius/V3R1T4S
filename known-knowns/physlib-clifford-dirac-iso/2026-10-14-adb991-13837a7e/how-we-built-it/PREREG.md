# Pre-registration: physlib-clifford-dirac-iso (frozen 2026-10-14T06:18:46Z, before any attack output)

frozen_utc: 2026-10-14T06:18:46Z

## Criterion (verbatim, see target.md)
A kernel-checked proof that `spaceTime.γ.ofCliffordAlgebra` is injective (Physlib TODO "Prove injectivity of
ofCliffordAlgebra and construct the full isomorphism."), against Physlib be0f21e5002d6d73b87f2055530c1e8bf7151546,
with no `sorry` and no axioms beyond `propext`, `Classical.choice`, `Quot.sound`.

## Statistic / checker
`checker/lean_claim_check.py` on `checker/spec_ofCliffordAlgebra_injective.lean`. Decision: PASS (last line) = claim
made; anything else = no claim.

## Thresholds
None beyond PASS/FAIL.

## Null design
null_test: not needed because the claim is a proof checked by a deterministic proof kernel against a frozen
statement; there is no search statistic, score or "beats chance" component.
