# PREREG — A089980 antidiagonal 79 (p2), run 2026-10-17-2208. Frozen Sat Oct 17 22:10:57 UTC 2026 (date -u), before any attack output of this run.

## Measured this run
(a) extender: exact T(w,79-w) for w=35,36 assembled from the frozen hs_mod residues in
runs/2026-10-17-1913/attempts/extender/res/ (plus w=37 if complete) with the frozen assemble.py;
(b) agreement table: extender value vs second-decomposition (far.py) value for every w where both exist (w=17..34 now);
(c) status re-check.

## Frozen acceptance rule, extender cell (unchanged from runs 1754/1913)
A width-w result is ACCEPTED only if (a) every published cell T(w,m), m=0..78-w, equals the b-file value (0 mismatches);
(b) the CRT check-prime assertion passes; (c) primes and CRT logic are exactly hs_mod.exact()'s. hs_mod.py and
assemble.py are frozen, never edited.

## Frozen rule, two-run agreement (unchanged from run 1913)
A second-decomposition cell AGREES only if its CRT value equals the extender value exactly (string equality of the
decimal integers), where far.py (i) was written in a fresh context without reading hs_mod.py, (ii) uses a different
state encoding, (iii) uses primes < 2^30, disjoint from hs_mod's primes in (2^30, 2^31), (iv) reproduced every
published cell of that width with 0 mismatches and passed its check prime. Any disagreement is reported as such and
blocks that cell; nothing is re-run to "fix" a disagreement without a new PREREG.

## Confirmed-partial bar (p2) — not reachable this run
All 40 cells w=0..39 accepted AND agreed AND a three-skeptic panel pass. Otherwise PROGRESS.

null_test: not needed because the results are explicit exact integers checked by deterministic recomputation and by exact equality with published b-file cells; there is no search or statistical claim.

ratchet_budget: n/a (no ratchet; deterministic computation)
