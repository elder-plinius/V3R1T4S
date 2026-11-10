# PREREG: run 2026-10-18-1841, square-site-percolation-rigorous-bounds

Frozen 2026-10-18T18:43:48Z (date -u), before the claim folder, the run's own reruns and the panel.

## Criterion (verbatim from charter.md)

> Prove a new rigorous lower bound (first) or upper bound on the site percolation threshold of the square lattice, p_c^site(Z^2) (numerically 0.59274605079210(2), Jacobsen 2015), strictly better than the best published rigorous bound, with every finite computation in the proof done in exact or verified interval arithmetic and released as a certificate a stranger can recheck.

## What will be claimed, and how it is judged

Claim to be judged: p_c^site(Z^2) >= 0.5567 = 1 - 4433/10000, by the larger-window version of the van den Berg and
Ermakov (1996) comparison written in PROOF.md.

The claim stands only if all of the following hold.
1. Exact certificate. window.py (sha256 4813b5ddf7068311e918346a678a96f9adaf7ffcb170f780ee3ef1c02d1b0f0b), run at
   p = 4433/10000 and depth 3 in exact rational arithmetic (Python fractions), reports a worst margin that is
   strictly positive as an exact rational. The statistic is that exact worst margin; the threshold is > 0. Nothing
   is tuned after this file: the same p (4433/10000) and depth (3) are used. No other p or depth may be substituted
   to rescue a failure. A failure means no claim at 0.5567 from this run.
2. Independent recomputation. A second implementation, not importing window.py, gives a strictly positive exact
   worst margin at p = 4433/10000 for some depth <= 3 (the setup session's reviewer code review/indep.py, sha256
   14ba821fe8a0894491a739630afa0bbed0165530bfdd5bcdfd0f537c8d3e8bea, or the REPRODUCE skeptic's own code).
3. Proof. The REPRODUCE and CRITERION skeptics, in fresh contexts, accept every step of PROOF.md: Lemma 2.1 of the
   1996 paper, the coupling lemma, the tree-information lemma, the superset and cone argument, the root step and
   the fewer-than-three-children reduction.
4. Novelty. The NOVELTY skeptic finds no published rigorous lower bound >= 0.5567 (a tie is not a record; the
   comparison is strict).

null_test: not needed because the claim is a proof whose finite part is a deterministic exact rational computation (a certificate checked exactly), not a search, a statistic or a "beats chance" claim

## Honesty note on timing

This file is written after the exploratory work in explore/square-site-lower/ (2026-10-18, setup session with the
human). That work had already chosen p = 4433/10000 after seeing the bisection (depth 3 passes from p = 0.443214911
upward) and had already run the depth-3 check once. The check is deterministic and exact, so choosing p after
seeing it creates no statistical selection effect. It is the only p this run evaluates, and it is frozen here before
the run's own reruns and before the panel. The exploratory outputs are kept as they were, for the record.
