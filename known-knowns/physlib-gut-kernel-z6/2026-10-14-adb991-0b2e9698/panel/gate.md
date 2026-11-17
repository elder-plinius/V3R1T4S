# Honesty gate: physlib-gut-kernel-z6 (run 2026-10-14-0616)

status: CONFIRMED_SOLUTION
confirmed_scope: Against Physlib be0f21e5002d6d73b87f2055530c1e8bf7151546 with Lean v4.34.1, object/InclSMKer.lean kernel-checks, using only the axioms propext, Classical.choice and Quot.sound, the frozen statement checker/spec_inclSM_ker.lean, a literal and unweakened formalisation of Physlib's informal lemma GeorgiGlashow.inclSM_ker (tag 6V2W2) with its informal dependencies GaugeGroupI (6V2WM) and inclSM (6V2WS), which asserts that the map StandardModel.GaugeGroupI = SU(3) × SU(2) × U(1) → Matrix.specialUnitaryGroup (Fin 5) ℂ sending (h, g, α) to blockdiag(α^3 g, α^(-2) h) (2×2 block on indices 0,1, 3×3 block on indices 2,3,4) is a group homomorphism, necessarily the unique one with these values, whose kernel equals StandardModel.gaugeGroupℤ₆SubGroup.

Read by the run's main session at 2026-10-14T07:24Z: reproduce.md, novelty.md and criterion.md, each from a fresh
subagent context that saw only claim/, each ending `pass: true`.

Downgrade checks (kit/RUN.md step 7), none triggered:
- Hedging: none. Each skeptic states its limits (NOVELTY: some literature sites were blocked by the proxy and were
  judged from search summaries; the status page itself was read on one fetch) and none conditions its pass on them.
- Reproduction: two checker runs with byte-identical output (PASS), an independent compile, a kernel replay with
  leanchecker, and the skeptic's own statement written before reading the spec, proved equivalent to it in Lean.
- Strictly better than the live record: the status page (fetched again by NOVELTY at 2026-10-14T07:00:55Z, HTTP 200,
  same sha256 34f66288e28cd4f26f1d2338bf092acb6dc5cd92ecd54fa2c129e3e567152682) still has `inclSM` and
  `inclSM_ker` as informal declarations only; no machine-checked proof was found upstream (all 1642 pull request
  heads scanned), in Mathlib, or in the literature searched. The fetch is less than 6 hours old.
- Stretched criterion or hidden quantifier: CRITERION proved in Lean that the values clause fixes f uniquely, the
  block layout and exponents match the docstring, and the ℤ₆ subgroup is neither trivial nor everything.
- Scope: the confirmed_scope sentence above is CRITERION's, verbatim; REPRODUCE independently derived the same
  statement (`spec_iff_mine`).
- One object, one statement; no sampling; no probable primes; no evasion.

Process notes (not affecting the result): REPRODUCE's `leanchecker --help` call checked the whole project and
reached about 9.6 GB for about 2 minutes inside a Lean slot before it was killed; CRITERION ran read-only
`git rev-parse/status/log` once before reading the brief's "no git" line; all three noted that CLAIM.md names the
source copy's folder as data/ on one line while it is in source/ (same sha256).
