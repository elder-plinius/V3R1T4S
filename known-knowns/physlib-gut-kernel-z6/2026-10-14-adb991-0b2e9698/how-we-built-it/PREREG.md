# Pre-registration: physlib-gut-kernel-z6 (frozen 2026-10-14T06:19:35Z, before any attack output)

frozen_utc: 2026-10-14T06:19:35Z

## Criterion (verbatim, see target.md)
A kernel-checked proof of `checker/spec_inclSM_ker.lean` (the formalisation of Physlib's informal lemma
`GeorgiGlashow.inclSM_ker` with its informal definitions `GaugeGroupI`, `inclSM`), against Physlib
be0f21e5002d6d73b87f2055530c1e8bf7151546, with no `sorry` and no axioms beyond `propext`, `Classical.choice`,
`Quot.sound`; or a counterexample to the informal lemma as stated.

## Statistic / checker
`checker/lean_claim_check.py` on `checker/spec_inclSM_ker.lean`. Decision: PASS (last line) = claim made; anything
else = no claim. The CRITERION skeptic must also judge that the frozen spec is a faithful reading of the informal
docstrings (if not, the claim is downgraded whatever the checker says).

## Thresholds
None beyond PASS/FAIL plus the fidelity judgement.

## Null design
null_test: not needed because the claim is a proof checked by a deterministic proof kernel against a frozen
statement; there is no search statistic, score or "beats chance" component.
