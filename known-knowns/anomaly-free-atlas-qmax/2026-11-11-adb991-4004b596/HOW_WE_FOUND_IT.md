# How we found it (contributor text, unverified)

**Brief.** Charter quarry 5 asks to extend the Allanach-Davighi-Melville census of anomaly-free family-dependent
U(1) charge assignments past their published Q_max = 10, with the full list as the certificate. Earlier runs of
this workspace built the tools (a convention that reproduces all 40 published values, two listers, a streaming
checker and two independent counters) and confirmed SM+3 nu_R up to Q_max 20 and the SM alone up to Q_max 40, as
six separate packages. Run 2026-11-11-0917 pre-registered one claim, the SM rows 41 and 42, with the same rules as
before (`how-we-built-it/PREREG.md`, frozen 2026-11-11T09:19:52Z before any listing or counting program ran). No
count for these rows existed before.

**What worked.** Two lenses ran.
- *extender-lists* streamed `acclist 41 0` and `acclist 42 0` (in parallel, 1171 s and 1448 s, about 0.3-0.4 GB
  each) through the C checker and sha256 on the same bytes: 66526760 and 79174539 valid lines, PASS. The first
  200000 lines of a fresh stream of each row also pass the independent Python checker.
- *counters* ran `mitm.c` after the PREREG: the certified regression rows (SMnuR 12, SM 20 and SM 36..40) came out
  right, and SM 41 = 66526761, SM 42 = 79174540, equal to the line counts + 1. A power-law fit on SM 25..35 puts the
  new counts at −0.6% and +3.0%; Q = 42, like Q = 36, is a multiple of 6, where the census's period-6 modulation
  pushes the count up.

**What failed.** A launch slip: the SM 42 stream and the first counter run started before their binaries were
compiled and exited at once (kept in the lens's outputs); both were relaunched. `count.c`, the third counter of
earlier rows, needs about 10 GB at these Q and was not run. SM + 3 nu_R 21 does not fit a standard run, so this claim
has the SM rows only.

**Panel.** Three fresh-context skeptics read only the claim folder, in the same run. REPRODUCE regenerated both lists in
full (1249 s and 1529 s), with the claim's checker and its own strict checker on the same bytes, equal hashes and
line counts, and recounted both rows with its own counter (`mycount.c`) and `mitm.c`. CRITERION re-derived all 40
published values, fed the checkers corrupted lists, and read "with and without three right-handed neutrinos" as row by
row. NOVELTY searched the citing literature, full text, Zenodo, arXiv and GitHub and found nothing past Q_max 10. The
owner stopped the run before the gate; the next run (2026-11-12-0008) read the three files and wrote
CONFIRMED_SOLUTION with CRITERION's scope sentence.
