# Honesty gate (kit/RUN.md step 7), written by the run's main session

status: CONFIRMED_PARTIAL
confirmed_scope: With the Gupta potential A = 0.0950 eV, xi = 1.4880 eV, p = 11.604, q = 2.286 (r in units of r0), which reproduces all ten Co.zip energies within 4.8e-7 eV as posted and 198 of 199 table energies within 6e-8 eV after polishing (N = 102 lies 1.1e-6 eV below its posted value), object/ccd_cobalt_audit.csv correctly recomputes all 199 CCD cobalt table point files in data/points.tgz (sha256-identical to the live CCD download of 2026-10-19) and all ten Co.zip files, and the only N whose posted table energy is not reproduced within 1e-5 eV are N = 163, 175, 179, 183, 185, 188, 189 and 190 for the coordinates as posted (all within 1e-5 eV after polishing), while no posted table or Co.zip structure polishes lower than its own posted energy by more than 1e-4 eV.
partial_win: p1
target: ccd-gupta-cobalt-clusters-n200
panel: reproduce pass: true, novelty pass: true, criterion pass: true; three fresh sub-agent contexts (delegations) started 2026-10-19T04:55:24Z, each given only claim/ and its kit/RUN.md instruction
table fetch: the novelty skeptic fetched the status page at 2026-10-19T04:56:43Z (sha256 unchanged from TABLE_RECORD.md); this gate was written at 2026-10-19T05:20:19Z, less than 6 hours later

Read by the main session: all three files in full. Downgrade checks: no hedging verdict (each skeptic states its limits
and passes on what it verified); no reproduction mismatch (both object-level skeptics recomputed all 209 structures and
every CSV field); no stretched criterion (the criterion skeptic reads "calibrated potential" as polish-then-compare,
which is the bank's own checker recipe, and its confirmed_scope states the exact numbers, including N = 102); scope no
wider than reproduced; no sample presented as complete (the per-N points/N files were byte-compared for 11 sizes only,
and the scope speaks of the files in points.tgz); no table value obtained by evasion; one object (the audit table).
Carried into the package: (1) the target's calibration clause cannot be met on the files as posted (84 of 199 within
1e-6 eV), and after polishing N = 102 misses 1e-6 eV by 1.1e-7 eV; (2) verify/check_p1.py does not assert the Co.zip half
of "no posted structure polishes lower" (both object-level skeptics verified it); (3) the literature half of the novelty
check is provisional (limits listed in novelty.md), the repository half is complete; (4) CLAIM.md named but did not write
out the potential's formula; the package README states it.
