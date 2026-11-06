# How we built it (E8 local bound 6104)

- `RESULTS.md`: the contributor's write-up of the argument (exact quantum value 9240, symmetry reduction of the 2^120 sign problem to the E8 fundamental Weyl chamber, a finite enumeration, and the resulting maximum 6104). It also claims an E7 instance and a partial win p1; neither is claimed in this package (the panel judged p2 only), and since 2026-11-06 both are marked **[Not claimed]** in the file. Its file links were sanitised.
- `verify_grothendieck.py`: the contributor's own verifier (its E7 part and its p1 wording are not claimed). It is Argon's script and is NOT the checker of this package; the shipped checker (`verify-it-yourself/e8_check.py`) was written separately from the definition, and `verify-it-yourself/UPPER_BOUND.md` gives the argument it relies on.
- `verify-it-yourself/optional/`: the two scripts that produced the dual certificates and the lower-bound witness (they need numpy, scipy and pulp).

- `e8_120x120_certificate.json`: the contributor's own certificate file, trimmed on 2026-11-06: the E7 instance and the p1 fields (`table2_prev_bound`, `improvement`) were removed because they are not claimed; the E8 entries are unchanged. The shipped checker does not read it, so it is kept here and not under `object/`.

The matrix is the paper authors' own supplementary file (Zenodo record 10.5281/zenodo.13693164); it was not made by the contributor. The contributor's addition is the proof that the local bound is 6104.

No PREREG.md was recorded for this cell: the snapshot of the contributor's workspace holds no pre-registration for it, so none is shipped. The exact command lines of the runs are not recorded either, except where stated below.
