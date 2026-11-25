# PREREG (written after the search; contributor text)

frozen: 2026-11-25T00:30:00Z (packaging time). The contributor's run kit did not freeze a pre-registration
before the SAT runs (2026-11-03 to 2026-11-05 ET). This file only freezes how the packaging run judges the
already-computed result; it cannot show that the criterion was fixed before measuring.

criterion: bank target polyform-compatibility-open-pairs, partial win p3, verbatim: "A computer-certified
impossibility (SAT/DLX exhaustive, with checkable proof) up to a stated figure size for a '?' pair, clearly
labelled as bounded."
statistic: per k = 2..20, the CaDiCaL 3.0.1 verdict on the joint cover CNF for M-X on board_for_k(k), and the
drat-trim verdict on its DRAT proof.
thresholds: claim only if all of k = 2..20 are UNSAT with "s VERIFIED"; the live 7compat.html M-X cell must be
'?'; each CNF must regenerate byte for byte from the shipped encoder; the proofs must be in a public archive whose
sha256 is listed.
null_test: not needed because the claim is a deterministic machine-checked certificate (UNSAT with a DRAT proof),
not a statistical detection; the positive control (M-B, listed 2, has a common 2-tile figure) checks that the
search can find compatibility.
