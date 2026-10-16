# PREREG (p3 integrity), written 2026-10-15 at packaging time

Honest note: written AFTER the night sweep had flagged this N; the night run's own PREREG (2026-10-14T18:35:13Z) covered the record criterion only.
criterion (bank partial win p3, verbatim): "Reproduction milestone: re-derive from scu<N>.txt the 30-decimal table radius for all N <= 1000 and report any N where the posted coordinates do NOT achieve the posted radius (a data-integrity finding, which Deeter-style audits have found in other tables)."
statistic: r* = min(half min pairwise distance, 1/2 - max |coordinate|), exact (Decimal 60 / mpmath 50), from the live posted file.
threshold: finding iff r*(posted) < cell - 1e-9 (1e-9 is 1000x the 12-digit coordinate noise seen in a third of rows), or the file does not hold N centres.
null_test: not needed (deterministic check of one file against one cell).
requirements: verify-it-yourself is stdlib only; mp_recheck.py needs mpmath; hunt3.py needs numpy and scipy.
