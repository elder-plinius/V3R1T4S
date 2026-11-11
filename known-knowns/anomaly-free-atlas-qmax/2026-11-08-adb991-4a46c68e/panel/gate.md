status: CONFIRMED_SOLUTION
confirmed_scope: In the published atlas convention (family permutations within each species and overall sign identified, gcd 1, max |charge| <= Q_max, the all-zero assignment counted), the number of inequivalent anomaly-free integer U(1) charge assignments of the Standard Model fermions without right-handed neutrinos is 51237625 for Q_max = 39 and 58626334 for Q_max = 40, which goes past the published range (Q_max <= 10), with each row certified by a deterministic canonical list (count - 1 lines, sha256 in object/counts.txt) and an independent count; this skeptic reproduced the convention on all 40 published values and re-ran the independent counter at 39 and 40, but did not regenerate the lists.

Gate (RUN.md step 7), run 2026-11-08-0917, written 2026-11-08T10:02:39Z after reading all three panel files in full.

- panel/reproduce.md: pass: true. Both lists regenerated in full after the claim was frozen (SM 39: 931 s, SM 40:
  1127 s), sha256 and line counts equal to object/counts.txt, PASS from the claim's checker and from its own strict
  checker on the same bytes. Its own counter (orbcount.c, a different split) and mitm.c give 51237625 and 58626334;
  a third counter (direct.c, no join, no Burnside) agrees with the lister up to Q_max 20 and on the published values.
- panel/criterion.md: pass: true. The convention is the paper's (all 40 published values, plus the Symmetry column
  where tested); the certificate meets the charter's shape; it reads "with and without three right-handed neutrinos"
  as describing the census, extended row by row, so SM-only rows qualify. confirmed_scope above is its sentence,
  copied exactly.
- panel/novelty.md: pass: true. The atlas (arXiv v5, Zenodo v1.1.0) stops at Q_max 10; 121 citing papers, arXiv,
  Zenodo, INSPIRE full text and GitHub show no count past it.

The main session's reading found nothing to downgrade. Recorded, not decisive:
- Under the stricter reading of the criterion (every claim must hold both contents), this claim alone would fail;
  CRITERION adopted the row-by-row reading, as the 2026-10-23 SM+3nuR-only claim (17, 18) was also judged.
- REPRODUCE notes that its counter shares mitm.c's method (multisets, Burnside, Moebius) with different code and a
  different split; both are independent in method of the lister.
- checklist.c alone does not detect a missing line; completeness rests on line count + 1 = the independent count,
  which REPRODUCE.md and the package's run_checks.sh both compare.
