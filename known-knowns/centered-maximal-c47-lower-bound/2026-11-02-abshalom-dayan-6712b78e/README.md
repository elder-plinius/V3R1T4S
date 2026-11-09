# c_2 >= 1.71101182367: a thick-row periodic measure for the centered maximal constant on squares (C_47)

## What

The explicit 344-atom periodic dyadic measure in object/measure.json gives, by the period-cell reduction in PROOF.md and exact rectangle-union area agreed by two separately coded checkers, c_2 >= 5422547985449268449657817/3169205443485515833671680 = 1.71101182367196..., strictly above the largest lower bound on the live page 47a (1.6855099933, fetched 2026-11-02T18:29:05Z) and any bound in open pull requests touching constants/47a.md (none listed in table/pr_files.md), and above Tomar's off-page 1.7027237335, with no claim of optimality or of being the largest value public anywhere.

Path note: claim/object/ = object/, CLAIM.md = README.md, REPRODUCE.md = RUN_IT_YOURSELF.md, PROOF.md = object/PROOF.md, family/ = object/family/, checkers/ = verify-it-yourself/, tests/ = verify-it-yourself/tests/, rebuild/ = how-we-built-it/, table/ = the-record-we-beat/. Not shipped: panel/claim.sha256, panel/scratch_*, panel/round1_criterion.txt, runs/ (earlier run folders), outbox/, attempts/, data/, object_in/. Tomar's exact rational file, read by verify-it-yourself/tests/mk_cal.py, is not shipped; tests/tomar40.json is its rounding to 40 bits.

The measure is object/measure.json: 344 atoms per cell, all coordinates and masses integers over 2^30. The proof is object/PROOF.md; object/family/FAMILY.md states the family by formula and how the value changes with discretization. Those changes are NUMERICAL, and no limit in the number of levels is established.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Last line PASS. About 2 minutes on a laptop, 200 MB. It runs check_a.py, check_b.c and third/vsweep.c, expects area_num = 10845095970898536899315634 and mass_num = 5629639765, and requires the value to be above the bar. RUN_IT_YOURSELF.md has the calibrations (Lin 1.685509993354 against his formula 1.68550999335553; Tomar 1.702723733601 against his file's 1.7027237336036), and the quadtree enclosure from the definition, [1.7110116654, 1.7110119658] at depth 26.

## Compared to

| source | value | margin |
|---|---|---|
| Tomar, Zenodo doi:10.5281/zenodo.23716077, version 5, off the page, the bar: the highest public lower bound found | 1.7027237335 | 0.00828809 |
| live page 47a (Lin 2026) | 1.6855099933 | 0.02550183 |

Page: https://teorth.github.io/optimizationproblems/constants/47a.html. Fetch times, HTTP status and sha256 are in the-record-we-beat/record.md. No open pull request of teorth/optimizationproblems lists constants/47a.md, as read on the dates in that file.

## Not claimed

No optimality and no formal verification. The value is a lower bound on c_2 and not the sup of any family. A rerun of the same search at L = 3 gave 1.711218535323 (object/family/FAMILY.md; that object is not shipped), so this object is not the best in its family, and search has not converged. No limit in L is stated as proved. The upper bound is untouched. Unrefereed.

## Credits

- Yongxi Lin (2026), lower bound 1.6855099933, the two-mass frame on alternating columns: https://github.com/CoolRmal/centered-maximal-constant and page 47a. The two-mass frame here is his.
- Tejasvi Singh Tomar (2026), lower bound 1.7027237335 by adding rows of small atoms to that frame: https://doi.org/10.5281/zenodo.23716077 and https://github.com/tejasvi/square-maximal-weak-type . The rows here continue his construction, on the same two heights; the search started from the frame 3.3, 2.75, 4.0, which is his frame values rounded; his measure is the L = 1 member with n = (6, 12) of the family formula. New here: each row is replaced by a staggered band of L = 3 levels with more columns, n = (9, 39) against his (6, 12), and the object's atoms are not his. The same reduction from a periodic measure to c_2 is Lemma 6.2 of his paper, following Lin's formalization, which adapts the smoothing of point masses in Aldaz (2000), Lemma 1.1.
- Aldaz (2000), 1.6211915: https://dml.cz/handle/10338.dmlcz/127554 ; Melas (2003), c_1 = (11 + sqrt 61)/12: https://doi.org/10.4007/annals.2003.157.647 ; both as cited on page 47a.
- Terence Tao and contributors, optimization constants repository: https://github.com/teorth/optimizationproblems .
- Credit for this package: Abshalom Dayan.
