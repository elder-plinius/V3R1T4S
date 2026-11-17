# How we found it (contributor text, unverified)

Run 2026-11-13-0233 set out to replicate, on the CDCgov RSV Forecast Hub's 2025-26 season (bank route b), a forecaster
that had beaten the HopkinsIDD archive hub's ensemble on 2024-25 (route a). It first built and checked a scorer on this
hub (reproducing arXiv 2605.16238 v2 Supplementary Table 6 with the pinned oracle-output). The forecaster, frozen
before any 2025-26 score, did not replicate (15% worse than RSVHub-ensemble; not part of this package). The scoring
table then became this object (bank partial win p3).

The table has not changed since that run's second panel round; every later panel judged text corrections:
- Run 2026-11-13-0233, round 1: REPRODUCE failed the first table (cross-model pairing without target_end_date); the
  table was repaired. Round 2: REPRODUCE and CRITERION passed; NOVELTY failed on "the only published" scores
  (ACCIDDA/EpiBenchmark had published 2-model scores).
- Run 2026-11-13-0349, panel 1: REPRODUCE and CRITERION passed; NOVELTY failed because the text said no cited source
  had UGA_flucast-INFLAenza scores while ACCIDDA/tapestry publishes them. Panel 2 (after the run's repair round):
  CRITERION passed; REPRODUCE failed (the Puerto Rico rule of a tapestry reconciliation was not stated; a unit count
  was wrong); NOVELTY failed because the text said tapestry's scores were "exactly" those listed while its Google
  comparison folder holds natural-scale WIS and plots were unlisted. Every NOVELTY skeptic judged the table new.
- Run 2026-11-13-0523 (this package): the text makes no completeness or exclusivity statement about published scores;
  it names what was reconciled or read and says that other sources may overlap. It states every reconciliation rule
  next to its values, reconciles the tapestry Google comparison exactly, lists the plots, and writes every text output
  with LF line endings (content unchanged; p3_table.csv byte-identical). A fresh three-skeptic panel judged it (panel/).
