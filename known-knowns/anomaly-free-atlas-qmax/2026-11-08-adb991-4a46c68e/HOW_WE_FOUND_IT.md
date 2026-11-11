# How we found it (contributor text, unverified)

**Brief.** Charter quarry 5 asks to extend the Allanach-Davighi-Melville census of anomaly-free family-dependent
U(1) charge assignments past their published Q_max = 10, with the full list as the certificate. Earlier runs of
this workspace built the tools (a convention that reproduces all 40 published values, two listers, a streaming
checker and two independent counters) and confirmed SM+3 nu_R up to Q_max 20 and the SM alone up to Q_max 38, as
five separate packages. `mitm.c` had already counted SM 39 and 40 on 2026-11-02, but nothing was listed or claimed.
Run 2026-11-08-0917 pre-registered one claim, the SM rows 39 and 40, with the same rules as before
(`how-we-built-it/PREREG.md`, frozen 2026-11-08T09:20:10Z before any listing or counting program ran).

**What worked.** Two lenses ran.
- *extender-lists* streamed `acclist 39 0` and `acclist 40 0` (in parallel, 872 s and 1072 s, about 0.3 GB each)
  through the C checker and sha256 on the same bytes: 51237624 and 58626333 valid lines, PASS. The first 200000
  lines of a fresh stream of each row also pass the independent Python checker.
- *counters* reran `mitm.c` after the PREREG: the certified regression rows (SMnuR 12 and 20, SM 20 and 36..38)
  came out right, and SM 39 = 51237625, SM 40 = 58626334, equal to the line counts + 1 and to the 2026-11-02 values.
  A power-law fit on SM 25..35 puts both new counts within +2.2% and +1.0%, inside its in-sample scatter.

**What failed.** Nothing in the claim. `count.c`, the third counter of earlier rows, needs about 10 GB at these Q and
was not run. SM + 3 nu_R 21 (about 3.3 h of listing) does not fit a standard run, so this claim has the SM rows only.
A guess that the sign of the fit residual follows Q mod 6 was wrong for Q = 40.

**Panel.** Three fresh-context skeptics read only the claim folder, in the same run. REPRODUCE regenerated both lists in
full (931 s and 1127 s), with the claim's checker and its own strict checker on the same bytes, equal hashes and line
counts, and recounted both rows with its own counter (`orbcount.c`) and `mitm.c`. CRITERION checked the convention
against all 40 published values and the paper's text, fed the checker deliberately corrupted lists, and read "with and
without three right-handed neutrinos" as row by row. NOVELTY searched the citing literature, full text, Zenodo, arXiv
and GitHub and found nothing past Q_max 10. The gate (`panel/gate.md`) wrote CONFIRMED_SOLUTION with CRITERION's scope
sentence.
