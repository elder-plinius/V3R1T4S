# PREREG (frozen 2026-10-20T22:57:10Z, before any attack output of this run)

criterion (verbatim, bank covering-designs-record): see target.md "Success criterion (verbatim from bank)".

statistic / checker: an explicit block list for C(v,k,3); tools/check_cover.py must print VALID (every 3-subset covered,
all blocks distinct k-subsets of {1..v}) and kmcover.check must return True; b >= Schonheim L(v,k,3).

threshold: b strictly below min(live coveringrepository.com archive value read 2026-10-20T22:56:37Z, LJCR GitHub
coverdata.json, Zenodo LJCR v1.2), and for C(38,6,3), C(35,5,3), C(37,6,3) strictly below our own 469, 713, 468.
A tie is not a record. A candidate is called PROMISING only after both checkers say VALID; no panel in this run (the
panel is launched separately by fresh workers).

null_test: not needed because each claim is an explicit object checked by a deterministic exhaustive checker against a
table value (no search statistic or "beats chance" claim).

capped rows: SCIP FEASIBLE and CP-SAT FEASIBLE/UNKNOWN rows are CAPPED and never used as exclusions.
