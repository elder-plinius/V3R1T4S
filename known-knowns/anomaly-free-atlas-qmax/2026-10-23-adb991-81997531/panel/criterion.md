# Criterion skeptic (panel 2)

Criterion (verbatim, CLAIM.md): "extend the exact census of anomaly-free U(1) charge assignments of the Standard
Model fermions (with and without three right-handed neutrinos) with integer charges bounded by `Q_max`, beyond the
largest `Q_max` tabulated by Allanach, Davighi and Melville; new exact counts, with the full solution list as the
certificate." No enumerated partial wins exist, so the question is whether the full criterion is met, literally.

## Checks run (scratch copy of claim/, 1 core, nice 10)

- count.c + conventions.py, SM Q_max 1..13 and SMnuR Q_max 1..12: column prim_incl0 reproduces all ten published
  values listed in status.md (SM 1:8, 3:82, 5:626, 7:3902, 10:23800; SMnuR 6:435305, 7:1358388, 8:3612734,
  9:9587085, 10:21546920), and gives SM 12: 67968, SM 13: 100388, SMnuR 12: 95067546, as in object/counts.txt.
- acclist | sha256sum | checklist, regenerated from scratch: SM 12, 13, 20, 31 and SMnuR 12. All five sha256 values
  equal the ones in object/counts.txt, checker PASS, line counts = count - 1 (SMnuR 12: 95067545 lines, about 2 min).
- acclist on the published SM points (Q_max 1, 3, 5, 7, 10) gives 7, 81, 625, 3901, 23799 lines = published - 1.
- Not run here: SMnuR 13..16 (memory/time), csenum, count2.c, the Python checker.

## Point by point

1. Both contents ("with and without three right-handed neutrinos"): met. SMnuR rows 12..16, SM rows 12..31.
   Uneven reach (SMnuR to 16, SM to 31) is fine; the criterion asks for an extension of each, not a common range.

2. Starting point ("beyond the largest Q_max tabulated by ADM"): the value 10 comes from web-search text; the
   primary table and the Zenodo record were not fetched (status.md says PENDING TABLE CHECK). Mitigations: the ten
   search-text values are mutually consistent with one convention across both contents (reproduced above), which
   they would hardly be if garbled; and the claim starts at 12, so it remains "beyond" even if the true largest
   tabulated value were 11. Residual risk: if ADM in fact tabulated SM at Q_max >= 12 (the SM case is cheap), the
   low SM rows would not be beyond it. Not refuted by anything in claim/, but not primary-verified either.

3. Q_max 11 is skipped. Counts at 11 are trivially computable with the same tools (I get SM 37006 and SMnuR 45378378
   under the same convention, as a by-product, not part of the claim). The literal criterion is "beyond the largest",
   which rows 12+ satisfy; but the result is a gapped extension, not a contiguous continuation of the table. The scope
   must therefore name 12..16 and 12..31 exactly and must not say "the census through Q_max 16/31". Not fatal.

4. Convention ("inequivalent", "in the convention of the atlas"): inferred, not read from the paper. conventions.py
   tries five candidate conventions and keeps the one that matches; that is a fit, but one discrete choice against ten
   exact integers in two contents, so a wrong convention matching by chance is not a credible null model. The "+1"
   (all-zero assignment) is an inferred constant offset: the count includes it, the list does not (list = count - 1
   lines; the zero has gcd 0 and is not a listable line). So the list certifies count - 1 and the +1 is convention.
   Independent family permutations per species and overall sign are likewise pinned only by this calibration.

5. "the full solution list as the certificate": the lists are not in claim/; each is a deterministic output
   identified by the sha256 of its uncompressed stream, regenerable by two separately written listers and checked by
   an independent streaming checker (validity, bound, canonical form, gcd 1, strict order). I regenerated five of them
   byte-identically. That is a full list that any reader can reproduce and check, so the certificate exists in the
   reproducible sense; it has not been deposited as a file, which a publication would need. Completeness is not
   something the checker can show; it rests on agreement with the no-list counters (count.c, and count2.c with a
   different split), which is adequate. counts.txt has no per-row checker column, so a checker PASS on the rows I
   did not rerun (notably SMnuR 13..16) is asserted by REPRODUCE, not recorded.

6. Bundle or one claim: 25 rows. The criterion itself asks for a census table, so a table is the natural single
   claim, not a bundle of unrelated results. Support per row is uneven and the table says so honestly: SMnuR 14..16
   have one lister (csenum), SM 21..31 one lister (acclist); every row has the independent count. No weak row is
   presented as stronger than it is.

7. "new exact counts" / not subsumed: a parametrisation of all solutions (general-solution papers) does not give
   bounded exact counts, so the table is not subsumed by it. Whether any later work already published counts past
   ADM's range was not checked in claim/; the criterion is anchored to ADM's tabulation, which is the reading used here.
   The SM rows are computationally cheap, but the criterion does not ask for difficulty.

8. Stretched wording in CLAIM.md: "each row certified by a complete canonical solution list" is right in the
   reproducible sense only (see 5); "in the convention of the atlas" really means "the convention that reproduces the
   atlas values available here" (see 4). The scope below uses the narrower wording.

Verdict: within the stated scope the result meets the full criterion literally: both contents, exact counts at
Q_max beyond the largest reported published value, each backed by a regenerable, checkable full list and by an
independent count. Remaining conditions: primary-source confirmation of ADM's largest Q_max, and depositing the
lists if the result is published.

confirmed_scope: Under the inequivalence convention inferred from, and reproducing all ten of, the Allanach-Davighi-Melville values available here (SM Q_max 1, 3, 5, 7, 10 and SMnuR Q_max 6..10, as reported by search-tool text, not primary-checked), the exact counts in object/counts.txt for SM plus three right-handed neutrinos at Q_max = 12..16 and for the SM at Q_max = 12..31 (Q_max = 11 not included) each agree with an independent no-list counter and with a deterministic canonical solution list of count - 1 lines (the all-zero assignment is counted but not listed), regenerable from source and identified by the sha256 of its uncompressed stream rather than stored, and all lie beyond Q_max = 10, the largest value that source reports for either content.
context: subagent (fresh, saw only claim/)
pass: true
