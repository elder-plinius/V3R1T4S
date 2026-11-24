# PREREG.v2 (frozen Mon Nov 23 16:30:33 UTC 2026), written AFTER the L1 smoke test
Reason (a loophole, so the change only tightens): the smoke reproduction of Dunn's own method and parameters gives
B <= 2.159321 (non-rigorous floats, attempts/reproduce/out/smoke_reproduce.txt), i.e. Dunn's published 2.1594 is his own
bound rounded up. So PREREG.md's threshold "U' <= 2.15939" could be met by recomputing Dunn's result to more digits, which
is not new. Changes (everything else in PREREG.md stands):
- Reference R := the rigorous (arb, two precisions) replay of Dunn's own parameters and method (L1, next session).
- p1 claim only if U' <= R - 1e-4 AND U' <= 2.15939 AND the improvement comes from a stated change of method or input
  (L3 a, b, or a new input), not only from re-optimising Dunn's parameters. A pure parameter re-optimisation is reported as
  "polish" and never claimed above PROMISING.
- If R itself exceeds 2.1594 (Dunn's figure not reproduced rigorously), that is a finding for the report and the comparison
  is unresolved.
null_test: not needed because the result is a deterministic interval-arithmetic bound checked by rerunning, not a search score or chance-level claim.
