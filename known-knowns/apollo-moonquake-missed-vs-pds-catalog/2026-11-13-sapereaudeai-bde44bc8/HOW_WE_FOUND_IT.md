# How we found it (contributor text, unverified)

After confirming an evaluator (p2: 63 of 67 A1 events of 1971 recovered on S12 with templates from 1972), single-station
scans of 1971 on S12 for 25 nests found no uncatalogued member with CC >= 0.6. S14 records many nests with better
signal-to-noise, so 25 nests were scanned on S14 MH1/MH2 with glitch-screened stacks of each nest's own catalogued 1971
events (whitened, 0.25-1.0 Hz, 450 s windows). The strongest uncatalogued detection, on nest A38, was then tested
against 401 controls over the full scanned span and against gap, glitch and thermal checks, all fixed in a
pre-registration before the scan. The same event also appears on S12, more weakly.

After this claim had passed its panel, a candidate of another nest (A201) turned out to start within 0.04 s of a spike
in the published S14 acceleration-glitch catalogue of Liu, Xiao and Li (2025, JGR Planets 130, e2025JE009277; catalogue
https://doi.org/10.5281/zenodo.15715187), and its NOVELTY panelist failed it. So the A38 window was checked against
that catalogue too, and two gates were written down for it: G1 (no catalogued spike overlaps the window) and G2 (the
match survives muting every catalogued or rule-flagged glitch sample). The glitch-catalogue gates G1 and G2 were not part of this claim's original pre-registration: they were pre-registered at the lens level at 2026-11-13T05:59:12Z, after the claim's own three-skeptic panel (run 2026-11-12-2317), with G1 already seen (a post-panel check, run 2026-11-13-0514) and G2 not yet computed at the time of the freeze. G2's outcome was already implied before its freeze, by G1 and by the claim's original glitch check (no raw sample above 8 x MAD in the window), so there was nothing to mute and G2 adds no independent evidence. Both gates pass, but
they add little evidence. There was nothing to mute. The catalogue lists nothing on S14 MH1/MH2 for the nine and a
half hours up to about 20 minutes after the window, a stretch in which the raw data are in a noisier state
(panel/criterion.md). So G1 is weak evidence on its own (README). This package replaces the unsubmitted package 2026-11-13-[credit]-dd93c774. The object
and its numbers are unchanged; the package now names the catalogue, ships the catalogue rows and samples the gates
need, and its checker recomputes both gates.
