# Research charter v1 (2026-10-14)

## Thesis
Edge: an eye for hidden structure, both physical (packings, energy minima, light curves) and symbolic (ciphers, accounting tablets, undeciphered signs), plus patience for one machine grinding every night. Charter weights those two clusters, prefers neglected quarries over famous ones, and keeps a breadth door open: any strong, stranger-checkable result in another bank category counts. Wants a surprising object or an old question settled, reported plainly. No hype, no rote grinding.

## Quarries
1. **thomson-problem-live-tables**. Question: lower the best known Coulomb energy for some N ≤ 1500 in a live Thomson table. Shape: record. Defined in: bank id thomson-problem-live-tables (tables at deetour.net/oppp/thomson and Wales CCD Thomson tables). Status to confirm first: current per-N energies in both tables. Why us: we can recast it as a structure problem (symmetry seeds, defect motifs) and patient nightly basin-hopping. Weight 4. Wild: no.
2. **packomania-cci-equal-circles-in-circle**. Question: beat a per-N record radius for equal circles in a circle. Shape: record. Defined in: bank id packomania-cci-equal-circles-in-circle (packomania.com/cci, radius.txt). Status to confirm first: radius.txt and recent author.txt entries for the chosen N. Why us: treating the best known object as data and searching structured families. Weight 3. Wild: no.
3. **new-periodic-variables-not-in-vsx**. Question: find ≥10 periodic variables or eclipsing binaries absent from AAVSO VSX, each with a bundle that can be checked. Shape: existence. Defined in: bank id new-periodic-variables-not-in-vsx (VSX, Gaia DR3, ZTF). Status to confirm first: absence from VSX on the day of the claim. Why us: finding patterns in public archive data is plain, patient work. Weight 4. Wild: no.
4. **proto-elamite-accounting-balance**. Question: assign numeral-system and commodity values that make the totals on held-out Proto-Elamite tablets balance under a pre-registered rule. Shape: decipherment. Defined in: bank id proto-elamite-accounting-balance (CDLI data; arXiv:2502.00090). Status to confirm first: the latest published numeral-system analyses. Why us: here, decoding a script is arithmetic that can be checked. Weight 5. Wild: no.
5. **linear-a-kuro-arithmetic**. Question: reconcile KU-RO totals and the values of fraction signs on fully preserved sections, pre-registered. Shape: decipherment/prediction. Defined in: bank id linear-a-kuro-arithmetic (SigLA; Ferrara, Montecchi & Valério, JAS 2021). Status to confirm first: published fraction-sign value proposals. Why us: a constraint solver applied to numbers on tablets. Weight 4. Wild: no.
6. **mtc3-hutton-cipher-part-5**. Question: recover keywords K1 and K2 that decrypt the whole 4,250-letter Hutton Part 5 ciphertext. Shape: decipherment. Defined in: bank id mtc3-hutton-cipher-part-5 (MysteryTwister challenge PDF; IACR ePrint 2023/1113). Status to confirm first: the solver list on MysteryTwister. Why us: write a fast exact evaluator first, then a patient keyspace search. Weight 3. Wild: no.
7. **ebl-unidentified-fragment-overlaps**. Question: find ≥1 overlapping pair among unidentified eBL cuneiform fragments, meeting the bank's criteria. Shape: existence. Defined in: bank id ebl-unidentified-fragment-overlaps (eBL API; ngram-matcher). Status to confirm first: joins and corpus links for candidate pairs at verification time. Why us: n-gram structure search at scale. Weight 3. Wild: no.
8. **linear-elamite-residual-signs**. Question: propose a value for one of the 4 still-undeciphered Linear Elamite signs that predicts readings in held-out inscriptions. Shape: decipherment/prediction. Defined in: bank id linear-elamite-residual-signs (elamicon corpus; Balmer et al. 2020, OCLEI concordance). Status to confirm first: whether the Aug 2026 Desset et al. volume still lists the sign as unassigned. Why us: the most distant blend of physical and symbolic structure, and the least likely to work. Weight 2. Wild: **yes**.

Breadth clause: a stranger-checkable result in record-tables, graphs-games-automata, number-hunts, erdos-and-proofs, algorithms, optimization-benchmarks or ml-robustness is welcome when a run finds a real opening there. It must cite a real bank id or a published definition.

## Lenses
- **object-as-data** (skeptic: no). Treat the best known configuration or text as data. First moves: download the record object or corpus and measure its symmetries, defects, repeats and residual errors. Dead sign: no regularity beyond what the source paper already reports.
- **evaluator-first** (skeptic: no). Spend the first hour building a fast exact scorer (energy, radius, decryption fitness, balance check). Dead sign: you can't score 10⁵ candidates per minute, so the search can't outrun the crowd.
- **constraint-solver** (skeptic: no). Recast the tablet arithmetic or packing contacts as constraints and let a solver argue. Dead sign: the solver proves the system is underdetermined, or that it is satisfied only by values already published.
- **far-import** (skeptic: no). Carry methods across the divide: physics-style annealing and defect analysis applied to ciphers and sign inventories, and code-breaking statistics (n-grams, hill-climbing on keys) applied to light curves and packings. Dead sign: the imported method does no better than the field's native baseline on a known case.
- **smaller-first** (skeptic: no). Solve the smallest open N, the shortest fragment or the simplest tablet exactly, then look for the pattern that scales. Dead sign: no pattern survives to the next size.
- **settled-already** (skeptic: **yes**). Try to show the quarry is already solved, trivial, ill-posed or contaminated by leaked answers. First moves: recent arXiv, the table changelog, the solver lists. Dead sign for the quarry: any credible prior result, in which case drop it.

## Scout voice
Read for structure first: the table, the corpus or the solver list before any commentary. Short, dense notes. Record the one fact that has changed and the one opening nobody seems to have tried. Leave out hype and summaries of summaries.

## Attacker voice
Calm, persistent and slightly contrarian. Assume there is a regularity the incumbents left unused, and hunt for it with an exact evaluator. Prefer one surprising object over many marginal gains. Verification is never relaxed.

## Heuristics
- Neglected beats famous: a quiet table entry outranks a celebrity cipher.
- Build the exact evaluator before the clever search.
- In decipherment, pre-register before you look at held-out data.
- Symmetry seeds first, then break the symmetry on purpose.
- When a mechanical search would need weeks of rote grinding, change the representation instead.
- Write negative results into the dossier: dead angles are progress.
- Report the margin honestly, including how small it is.

## Kill criteria
- Three nights with no improvement in the evaluator score and no new structural insight.
- A credible prior result is found (settled-already lens).
- A decipherment needs post-hoc rule changes to fit the held-out data.
- A record margin sits inside the table's own numerical tolerance.
- The compute needed is beyond one machine for a week of nights.

## Self-critique
The two loved clusters may be chosen for taste, not for edge: packings and cipher keyspaces are crowded with strong solvers. Decipherment quarries tempt pattern-seeing in noise, so pre-registration is the only defence. "Structure in nature" may drift into exhaustive grinding the user dislikes. The wild quarry probably fails.

## Method cards used
object-as-data, evaluator-first, solver, far-import, smaller-first, symmetry
