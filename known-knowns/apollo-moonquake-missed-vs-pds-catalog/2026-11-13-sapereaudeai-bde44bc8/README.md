# A new member of deep-moonquake nest A38 on Apollo S14, 1971-05-13 18:40 UTC (p1)

This package replaces the unsubmitted package 2026-11-13-[credit]-dd93c774 (same object and numbers; glitch-catalogue gates added).

Target: apollo-moonquake-missed-vs-pds-catalog, partial win p1 ("A new member of a catalogued nest seen on a single
station with CC >= 0.6 and the null test passed (single-station detections are weaker evidence).").

## What

On Apollo S14 long-period channels MH1/MH2 (PDS MiniSEED, Earth-received time), the 450 s window starting 1971-05-13 18:39:33.7 UTC correlates with the S14 stack of six catalogued 1971 A38 deep-moonquake events at NCC 0.757 (MH2) and 0.727 (MH1), its two-channel mean 0.742 exceeds the 1971 days 36-365 full-span maxima of the time-reversed-data control (0.212) and of all 400 phase-randomised-template controls (best 0.287), and no dated row of any PDS Apollo seismic event catalogue table lies within +/- 5 min of it (nearest 120 min), which meets bank partial win p1 as a single-station detection of an A38 nest member absent from the PDS catalogue; the glitch-catalogue gates G1 and G2, pre-registered only after the claim's original panel and with G1 already seen, also pass but add little evidence: no S14 MH1/MH2 ACC-Spike interval of the Liu, Xiao and Li (2025) catalogue overlaps the window, yet that catalogue lists none on those channels between 09:40 and 19:30 UTC that day, and with nothing to mute G2 leaves the statistic unchanged.

## Glitch-catalogue gates (added after this claim's original panel)

**In short: both gates pass, but they add little evidence.** G1 is close to uninformative here. The catalogue lists
nothing at all on S14 MH1/MH2 from 09:39 UTC until about 21 min after the window, and silent stretches that long are
common in it (see below). So the absence of a catalogued glitch in the window says little. G2 adds no independent evidence, because there was nothing to mute. The detection
rests on the correlation, the 401-control null and the window's own glitch check, as in the original claim.

The gates check the window against the published S14 acceleration-glitch catalogue of X. Liu, Z. Xiao and J. Li
(2025), "Acceleration-Related Glitch Patterns in Apollo Seismic Data and Implications for Future Lunar Seismic
Observation", JGR Planets 130, e2025JE009277 (https://doi.org/10.1029/2025JE009277); catalogue files at
https://doi.org/10.5281/zenodo.15715187 (archive lunar_ACC-v1.0.1.zip, CC BY 4.0), of which the gates use
catalogs/S14_ACC-Spike_MH1_all.csv (sha256 78e91b83ff3f80c51706b044786420dcd41dddfa359099ac1e1123503b6ac0a1) and
catalogs/S14_ACC-Spike_MH2_all.csv (sha256 1219c0fa43fc26ff08950a217407d0b5b5c9daadcb56900565f8af08733bc9f9).

**Timing.** The glitch-catalogue gates G1 and G2 were not part of this claim's original pre-registration: they were pre-registered at the lens level at 2026-11-13T05:59:12Z, after the claim's own three-skeptic panel (run 2026-11-12-2317), with G1 already seen (a post-panel check, run 2026-11-13-0514) and G2 not yet computed at the time of the freeze. G2's outcome was already implied before its freeze, by G1 and by the claim's original glitch check (no raw sample above 8 x MAD in the window), so there was nothing to mute and G2 adds no independent evidence. Even earlier, before the original gate, the original NOVELTY panelist had noted in
passing that this catalogue lists no S14 MH1/MH2 glitch between 17:00 and 19:08:36 UTC that day
(how-we-built-it/original_panel/novelty.md). Gate texts and timing: how-we-built-it/PREREG_glitch_gates.md.

- **G1** (no catalogued S14 MH1 or MH2 ACC-Spike interval overlaps the 450 s window): pass. The nearest catalogued
  spikes start 3014 s (MH2) and 7348 s (MH1) after the onset.
- **G2** (mute from 5 s before to 5 s after every overlapping catalogued spike and every raw sample that the frozen
  glitch rule |x - median| > 8 x max(MAD, 0.5) flags; NCC over the unmuted samples, best lag within +/- 10 s; pass if
  best CC >= 0.6 and D > 0.2868, the null maximum): pass with nothing to mute. No catalogued spike overlaps, and the rule
  flags no raw sample (MAD 4 counts on MH1, 6 on MH2). NCC stays 0.7268 / 0.7567, D 0.7417, best lag 0.
- **What G1 can and cannot show.** The catalogue lists no S14 MH1 or MH2 interval of any of its three types (spike,
  step-up, step-down) from 09:39:25 to 19:08:36 UTC that day: 9.487 h, ending about 21 min after the window. Each of
  the other 15 hours of that day has 3 to 15 such intervals.
  - Gaps that long are common in the catalogue. Over 1971 days 36-365 there are 39 stretches of 9.487 h or longer
    with no S14 MH1/MH2 interval of any type. They start on 35 of the 330 days and cover 8.2% of the span, and the
    one around the onset ranks 39th by length. Sources: our own per-day counts and longest daily gap per channel,
    how-we-built-it/glitch_catalogue_daily_counts_1971d036-365.csv, and the summary
    glitch_catalogue_gap_summary.txt.
  - According to this package's CRITERION panelist (panel/criterion.md, section 3), the silent stretch around the
    onset coincides with a noisier state of the raw S14 MH1/MH2 data. That state contains excursions the catalogue
    does not list, among them the one-sided pulses the original CRITERION panelist found at 18:31 and 18:35-18:36
    UTC, about 3.5 to 8 min before the window.

  So G1 shows that the published catalogue does not flag this window; it does not show that the catalogue's detector
  covered this stretch. The window's own glitch check is the frozen rule on the raw samples (no sample flagged).
- **G3, for scale (descriptive; NOT reproducible from the shipped files).** A catalogued spike lies in
  [start - 60 s, start + 450 s] for 16.6% of random times in 1971-1977 (3327 of 20000) and for 13.6% of catalogued
  type-A deep moonquakes (898 of 6607). Passing G1 is therefore the usual outcome, and on its own weak evidence.
  Regenerate from the sources with `python3 how-we-built-it/code/scripts/g3_base_rates.py levent.1008weber.csv
  lunar_ACC-v1.0.1.zip g3.json` (numpy and pandas; levent.1008weber.csv from the PDS directory below). That command
  gives exactly these counts.
- Descriptive, not gated, computed after the gates were frozen: none of the catalogue's other seven S14 files (Spike
  MHZ; Step-Up and Step-Down on MH1, MH2 and MHZ) has an interval overlapping the window. The nearest is an MH2
  step-down starting 1713 s after the onset (how-we-built-it/glitch_catalogue_survey.json).
- **Which numbers the shipped files reproduce.** The checker recomputes the following from object/: G1, G2, the
  nearest catalogued spikes, and the spike-free stretch on 1971-05-13 (no spike starts 10:00-19:00 UTC). These
  numbers are NOT reproducible from the shipped files and need the source archive (sha256 below):
  - the all-type stretch and the hourly counts: coverage_boundaries.py, day133_hourly.py;
  - the other seven files: survey_nine_files.py;
  - the per-day counts and the gap summary: daily_counts.py;
  - G3: g3_base_rates.py, which also needs levent.

  Each is one command in RUN_IT_YOURSELF.md, run with the archive as input.
- The checker recomputes G1 and G2 from these files:
  - object/glitch_catalogue_s14_acc_spike_mh1_onset_pm24h.csv and _mh2_ are the catalogue slice. The rule:
    every catalogued interval within +/- 24 h of the onset (an interval counts if any part of it falls in that
    range), both channels, no other selection. That gives 48 MH1 and 65 MH2 rows. The start and end columns are
    copied verbatim with attribution (CC BY 4.0), and all other columns are dropped.
  - object/g2_raw_window.csv holds the raw samples of the window.
  - object/g2_prepped_window_pm10s.csv holds the prepped series over the window +/- 10 s.

  Only this window of the catalogue is shipped, because the package must not carry a copy of a third-party dataset.
  The window is enough for G1: the longest catalogued spike lasts 40 s, and the nearest catalogued spikes on both
  sides fall inside it.

  how-we-built-it/code/scripts/extract_spike_subset.py regenerates everything from the Zenodo archive (sha256
  7278ac65c926e88d14748ee6a2ff32c17fb6fde84b3ecf20fbec5a6fcd12566d). The script refuses a source whose sha256 differs
  from the values above.
  - Mode `window` gives the shipped slice.
  - Mode `year` gives the full scanned-span extract (1971 days 36-365: 9361 MH1 and 11394 MH2 rows).

  The whole gate run is how-we-built-it/COMMANDS.md step 7, on the full source files.

## Check it yourself

`sh verify-it-yourself/run_checks.sh` (Python 3 standard library; set PYTHON if `python3` is not on PATH). Expected last
line: `PASS`, in a few seconds. The script does the following:

- It recomputes both channels' NCC from the saved window and template.
- It compares the detection statistic with all 401 null maxima.
- It recomputes gates G1 and G2 from the shipped catalogue rows and samples, and checks every object file's sha256.

The full re-run from the PDS waveforms (templates, scan, null, checks, gates) is in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| PDS Apollo seismic event catalogue (levent.1008weber.csv and the other tables of the directory) | events near 1971-05-13 18:40 UTC | nearest row starts 157 min before the onset (its stop time, 16:40, is 120 min before); none within +/- 5 min | https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/ | 2026-11-13T09:18:15Z |
| Liu, Xiao and Li (2025) S14 acceleration-glitch catalogue, ACC-Spike MH1/MH2 | intervals overlapping the 450 s window | none; nearest spike start 3014 s after the onset (MH2) | https://doi.org/10.5281/zenodo.15715187 | archive 2026-11-13T08:32:39Z |

## Not claimed

- Not the full criterion: one station only (S12 shows a weaker detection near the same time, D 0.393 with the S12 A38
  stack, not claimed); no location, moveout or inter-station null.
- Membership rests on these points; correlation alone does not prove membership:
  - waveform similarity with the A38 stack (0.76 / 0.73);
  - the scores of the other 24 nest templates at that time (all <= 0.18, original CRITERION panel);
  - the anomalistic phase.
- The glitch-catalogue gates were not part of the claim's original pre-registration. G1 is a statement about the
  published catalogue only (see the coverage note above).
- Times are MiniSEED (Earth-received, nominal-rate) times; sub-second accuracy is not claimed.
- Waveforms come from the NASA PDS restoration (EarthScope FDSN was not reachable from the claimant's network).
- "Stack of six" in "## What" counts the template's members as its builder does
  (how-we-built-it/code/tools/nesttemplates2.py: six catalogued 1971 A38 events with D >= 0.3 after alignment). The
  pre-registered per-channel glitch screen (max|x|/rms > 8) leaves one of them, 1971-242 14:41, out on both channels, so
  each channel's stack averages five events. The template is the frozen one, and this package's REPRODUCE panelist
  rebuilt it byte for byte (panel/reproduce.md, section 7).

## Credits

- Apollo Passive Seismic Experiment data: NASA Apollo program; restored archive by C. Nunn, Y. Nakamura, S. Kedar and
  M. P. Panning, PSJ 3, 219 (2022), https://iopscience.iop.org/article/10.3847/PSJ/ac87af, PDS Geosciences Node
  (https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_pse/).
- Event catalogue: Y. Nakamura and co-workers (levent), expanded by R. C. Weber with the events of R. C. Bulow,
  C. L. Johnson and P. M. Shearer (2005, 2007), https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/.
- Nest locations: Y. Nakamura (2005). SP event windows checked: K. Onodera (Zenodo 8373651).
- Acceleration-glitch catalogue: X. Liu, Z. Xiao and J. Li (2025), JGR Planets 130, e2025JE009277,
  https://doi.org/10.1029/2025JE009277; catalogue https://doi.org/10.5281/zenodo.15715187 (CC BY 4.0). The two files
  in object/glitch_catalogue_*.csv are a +/- 24 h extract of that catalogue (start and end columns only), redistributed under
  CC BY 4.0 with this attribution.
