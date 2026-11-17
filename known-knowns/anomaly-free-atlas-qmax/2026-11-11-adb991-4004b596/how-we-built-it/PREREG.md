# PREREG: anomaly-free-atlas-qmax, SM Q_max 41 and 42, run 2026-11-11-0917

Frozen at: 2026-11-11T09:19:52Z (date -u), before any listing or counting program of this run was started.

## Criterion (verbatim, from target.md)
"extend the exact census of anomaly-free U(1) charge assignments of the Standard Model fermions (with and without
three right-handed neutrinos) with integer charges bounded by `Q_max`, beyond the largest `Q_max` tabulated by
Allanach, Davighi and Melville; new exact counts, with the full solution list as the certificate."

## Planned claim
"In the Allanach-Davighi-Melville convention, the SM census (no right-handed neutrinos) at Q_max = 41 and 42 is
N41 and N42, each certified by a complete canonical solution list identified by sha256."
Made only if, for each of q = 41, 42, computed in this run after this timestamp:
1. acclist q 0 streamed through checklist q 0 prints "valid solutions: L" and PASS, with pipeline exit 0, and the
   sha256 of the same stream is recorded;
2. mitm.c gives inequivalent = L + 1 (no value is registered in advance for these rows; mitm.c is first rerun on the
   certified rows SMnuR 12, SM 20 and SM 36..40, which must come out equal to their confirmed values);
3. check_list.py on the first 200000 lines of a fresh stream reports 0 errors.
Gate (RUN.md step 7): CONFIRMED_SOLUTION only if REPRODUCE, NOVELTY and CRITERION all pass in fresh contexts and the
main session finds nothing to downgrade; otherwise PROMISING (or lower). REPRODUCE must regenerate both lists in full.
The claim covers SM only (SM+3nuR 21 needs a heavy run); whether that satisfies "with and without" is CRITERION's call.

null_test: not needed because the claim is an exhaustive deterministic enumeration judged by exact integer checks and an independent counter; no statistical or search-score claim is made.
