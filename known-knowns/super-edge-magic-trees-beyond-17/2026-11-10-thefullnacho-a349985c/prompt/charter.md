# Research charter v1 (2026-11-02)

## Thesis
Seeds were drawn at random (categories: neuroscience, particle physics; method cards: small-data, symmetry,
structured-family) because the human said "surprise me". One CPU machine with modest memory and no GPU is weak at
benchmark training but strong at exact, certificate-producing work. So the charter leans on long-stalled
verification bounds in graph labeling and on symmetry-restricted constructions, where a patient exact search plus a
calibrated checker beats the crowd. The two seed fields stay in as lower-weight quarries and as sources of method.

## Quarries
- id: odd-graceful-trees-beyond-12 | question: is every tree on 13..22 vertices odd-graceful (or is there a tree that is not)? | shape: bound or proof (exhaustive certificate) or counterexample | where defined: bank entry odd-graceful-trees-beyond-12; Gnanajothi's definition as given in J. A. Gallian, "A Dynamic Survey of Graph Labeling", Electronic Journal of Combinatorics DS6 (28th ed., 2025), Section 3.6 | status to confirm first: DS6 still gives order 12, and no later paper or preprint raised the bound | why us: structured-family card (alpha-labeled trees are odd-graceful) plus a fast exact search on the residue is CPU work | weight: 5 | wild: no
- id: no-three-collinear-cube-a399138 | question: a set in {0..n-1}^3 with no three collinear, larger than the best known for some n in 7..11 | shape: record | where defined: OEIS A399138; A. Kudriashov, arXiv:2609.25133 (2026) | status to confirm first: the live A399138 lower bounds (73, 94, 116, 138, 164 on 2026-10-30) | why us: symmetry card (search inside symmetry strata, then break symmetry by local repair) | weight: 4 | wild: no
- id: super-edge-magic-trees-beyond-17 | question: is every tree on 18..25 vertices super edge-magic? | shape: bound or proof (exhaustive certificate) or counterexample | where defined: bank entry super-edge-magic-trees-beyond-17; Enomoto, Llado, Nakamigawa and Ringel, SUT J. Math. 34 (1998); Gallian DS6 Section 5.2 | status to confirm first: DS6 still gives 17 (Lee and Shan 2002) | why us: same structured-family residue method, consecutive-edge-sum reformulation | weight: 3 | wild: no
- id: bci-iv-ds4-ecog-finger-flexion-strict | question: beat mean correlation 0.69 on BCI Competition IV dataset 4 test labels under a strict no-test-tuning protocol | shape: record (empirical benchmark) | where defined: bank entry bci-iv-ds4-ecog-finger-flexion-strict; BCI Competition IV results page (bbci.de/competition/iv/results) | status to confirm first: the best published strict score and whether the data can be obtained without the human accepting terms | why us: small ECoG data fits a CPU; small-data card (per-finger, per-band linear models tabulated across subjects) | weight: 2 | wild: no
- id: quark-gluon-pythia-tagging-auc-record | question: beat PELICAN's AUC 0.9252 on the Komiske-Metodiev-Thaler Pythia quark-gluon dataset | shape: record (empirical benchmark) | where defined: bank entry quark-gluon-pythia-tagging-auc-record; A. Bogatskiy et al., arXiv:2307.16506 | status to confirm first: the current best AUC with particle-ID inputs | why us: symmetry card taken literally: Lorentz-invariant hand-built features with a small model on a CPU | weight: 1 | wild: yes

## Lenses
- key: structured-family | title: Label the cheap family first | text: You split the instances into a structured family that has a known construction (for example trees with an alpha-labeling, caterpillars) and a residue. You certify the family by construction and spend exact search only on the residue. First moves: implement the construction, verify it with the checker on every family member. Dead sign: the residue is most of the instances. | skeptic: no
- key: small-data | title: Finish every small case | text: You solve every instance of the smallest open orders exhaustively, tabulate the hardest ones (most backtracks, fewest solutions) and look for the pattern that predicts where a counterexample could live. First moves: enumerate instances, run a plain backtracker with counters. Dead sign: hardness shows no structure across orders. | skeptic: no
- key: symmetry | title: Impose symmetry, then break it | text: You restrict the search to objects fixed by a subgroup, which shrinks it enough to finish, then repair or extend the best symmetric object by local moves that break the symmetry on purpose. First moves: list subgroups, solve the restricted problem, measure how far from the record it lands. Dead sign: every stratum lands well below the record and local repair never adds a point. | skeptic: no
- key: detector-calibration | title: Calibrate like a detector | text: Borrowed from experimental particle physics: before any search, you calibrate the checker on known positives and known negatives, and you measure the search's efficiency on instances whose answer is known before trusting it on open ones. First moves: injected-defect tests on the checker, known-solved orders replayed. Dead sign: calibration fails and cannot be fixed. | skeptic: no
- key: settled-already | title: Is it already settled? | text: You try to show the quarry is already settled, trivial or ill-posed: search recent literature and preprints for a higher bound, look for a general theorem that covers the open cases, and check that the definition really is the published one. Dead sign: none; this lens ends with a citation or a clean "still open as of" note. | skeptic: yes

## Scout voice
Read for the exact definition and the exact current bound with its date. Distrust survey summaries of unpublished
results; note which bound is published and which is cited only. Look for preprints that quietly extended a
verification bound.

## Attacker voice
Patient and literal. Prefers a dull complete certificate to a clever partial one. Writes the checker first, calibrates it,
then searches; counts everything; never rounds a coverage claim up.

## Heuristics
1. A certificate per object beats a theorem sketch.
2. Check the instance count against the published sequence before trusting an enumeration.
3. Calibrate every checker on one positive and one injected negative.
4. Solve the known orders first; matching known results is the efficiency measurement.
5. Search the structured family before the residue.
6. A symmetric object is a seed, not an answer.
7. Record the hardest instance per order.

## Kill criteria
1. The quarry's bound was already raised in the literature past what one machine can reach in a week.
2. The enumeration count disagrees with the published sequence and the cause cannot be found.
3. The residue after the structured family needs more than a week of nights.
4. A benchmark quarry needs data that only the human can obtain by accepting terms (record it under "Needs you").
5. A symmetry stratum search stalls below the record across three different subgroups.

## Self-critique
The verification-bound quarries may already be extended in work this charter does not know about, which would turn a
"new bound" into a replication. Exhaustive certificates are easy to get subtly wrong (missing isomorphism classes,
off-by-one label ranges), so the count check and the injected-negative calibration carry the honesty. The two
seed-field quarries are probably out of reach on a CPU; they are kept low and could be dropped.

## Method cards used
small-data, symmetry, structured-family (drawn at random), plus far-import (detector calibration) by choice.
