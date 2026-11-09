# Pre-registration: physlib-gut-kernel-z6 family follow-on, run 2026-10-14-0701 (frozen 2026-10-14T07:07:55Z, before any attack output)

frozen_utc: 2026-10-14T07:07:55Z

## Criterion (verbatim, see target.md)
A kernel-checked proof of the frozen statement `2026-10-14-0701/checker/spec_patisalam_inclSM_ker.lean` (formalising the informal Physlib Pati-Salam declarations quoted
in target.md), against Physlib be0f21e5002d6d73b87f2055530c1e8bf7151546, with no `sorry` and no axioms beyond
`propext`, `Classical.choice`, `Quot.sound`; or a counterexample to the informal lemma as stated.

## Statistic / checker
`checker/lean_claim_check.py` on `2026-10-14-0701/checker/spec_patisalam_inclSM_ker.lean`. Decision: PASS (last line) = claim made; anything else = no claim. The CRITERION
skeptic must also judge that the frozen spec faithfully reads the informal docstrings (otherwise downgrade).

## Thresholds
None beyond PASS/FAIL plus the fidelity judgement.

## Null design
null_test: not needed because the claim is a proof checked by a deterministic proof kernel against a frozen
statement; there is no search statistic, score or "beats chance" component.
