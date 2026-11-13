# Glitch-catalogue gates G1 and G2 for this object: their pre-registration and its timing

**Timing, in plain words.** These gates are not part of this claim's original pre-registration (PREREG.md in this
folder, frozen 2026-11-12T22:44:43Z). They were pre-registered for this object at the lens level at
2026-11-13T05:59:12Z, after the claim's own three-skeptic panel (run 2026-11-12-2317, gate written
2026-11-13T01:40:38Z), when G1 had already been seen (a post-panel check in run 2026-11-13-0514) and G2 had not yet
been computed. The lens applied unchanged the G1/G2 definitions that run 2026-11-13-0552 had frozen at
2026-11-13T05:53:23Z for a different object (an A39 candidate). The freeze times are written inside the files; the
file times on disk are copy times, so the order rests on the run records. G2's outcome was already implied before its freeze, by G1 and by the claim's original glitch check (no raw sample above 8 x MAD in the window), so there was nothing to mute and G2 adds no independent evidence. Even before the original gate, the
original NOVELTY panelist had noted in passing that this catalogue lists no S14 MH1/MH2 glitch between 17:00 and
19:08:36 UTC that day (original_panel/novelty.md). In Verbatim 1 below, "sha256 in PREREG.md" refers to the run
2026-11-13-0552 pre-registration (Verbatim 2), not to PREREG.md in this folder.

**Catalogue.** X. Liu, Z. Xiao and J. Li (2025), "Acceleration-Related Glitch Patterns in Apollo Seismic Data and
Implications for Future Lunar Seismic Observation", Journal of Geophysical Research: Planets 130(10), e2025JE009277,
https://doi.org/10.1029/2025JE009277. Catalogue files: https://doi.org/10.5281/zenodo.15715187 (record "lunar_ACC: ACC
codes and catalogs", v1.0.1, 2025-06-22, CC BY 4.0; one archive, lunar_ACC-v1.0.1.zip, 109655361 bytes, md5
38e162c8e4407e750de3c5cb126fdcfd, sha256 7278ac65c926e88d14748ee6a2ff32c17fb6fde84b3ecf20fbec5a6fcd12566d). The gates
use two files of its catalogs/ folder:

- catalogs/S14_ACC-Spike_MH1_all.csv, 6722534 bytes, sha256 78e91b83ff3f80c51706b044786420dcd41dddfa359099ac1e1123503b6ac0a1
- catalogs/S14_ACC-Spike_MH2_all.csv, 6580287 bytes, sha256 1219c0fa43fc26ff08950a217407d0b5b5c9daadcb56900565f8af08733bc9f9

The gate run used copies fetched from the code repository behind that record on 2026-11-13T05:29:30-32Z; they are
byte-identical to the files inside the Zenodo archive (archive fetched 2026-11-13T08:32:39-08:33:09Z, members hashed).

**What the gates found** (glitch_gates_A38.json, recomputed by verify-it-yourself/check_p1.py from object/):

- G1: no catalogued S14 MH1 or MH2 ACC-Spike interval overlaps the 450 s window starting 1971-05-13 18:39:33.735 UTC;
  the nearest catalogued spikes start 3013.925 s (MH2) and 7347.963 s (MH1) after the onset. Pass.
- G2: nothing to mute (no overlapping catalogued spike; the frozen glitch rule flags no raw sample in the window); NCC
  0.7268 (MH1) / 0.7567 (MH2), D 0.7417 at lag 0, unchanged; best lag 0. Pass (needs best CC >= 0.6 and D > 0.2868).
- G3 (descriptive, no gate): a catalogued S14 MH1/MH2 spike lies in [start - 60 s, start + 450 s] for 3327 of 20000
  random times in 1971-02-05..1977-09-30 (16.6%) and for 898 of 6607 catalogued type-A deep moonquakes (13.6%).
  The shipped files cannot reproduce these counts. They come from the full source files and levent, and
  code/scripts/g3_base_rates.py regenerates them exactly (RUN_IT_YOURSELF.md).

The two pre-registration texts follow verbatim: first the lens pre-registration for this object, then the run
pre-registration whose G1/G2 definitions it applies.

---

## Verbatim 1: lens pre-registration (run 2026-11-13-0552, attempts/a38-glitch-check/PREREG.md)

# Lens prereg: glitch-catalogue gates for the CONFIRMED A38 p1 object (package 2026-11-13-[credit]-dd93c774)

frozen: 2026-11-13T05:59:12Z (before G2 was computed for A38)
Object: S14 MH1/MH2 window start 1971-05-13T18:39:33.735Z (onset 18:40:03.735), A38 stack of 6 catalogued 1971 events;
null maximum 0.2868 (best of 401 controls; run 2026-11-12-2317).
Same gates as this run's PREREG.md, applied unchanged:
- G1: no catalogued S14 ACC-Spike interval (Liu, Xiao and Li 2025; copies in data/lit_acc, sha256 in PREREG.md)
  overlaps the 450 s window. Already seen (run 2026-11-13-0514, attempts/glitch-catalogue, post-panel): nearest spike
  starts 3014 s (MH2) and 7348 s (MH1) from the onset, none in the window.
- G2: mute +/- 5 s every overlapping catalogued spike and every raw sample flagged by the frozen glitch rule
  (|x - median| > 8 x max(MAD, 0.5)); NCC over unmuted samples, best lag within +/- 10 s; pass if best CC >= 0.6 and
  D > 0.2868. Not computed before this prereg.
Result recorded in out/; the existing package is not modified. This lens does not change any gate.

---

## Verbatim 2: run pre-registration whose G1/G2 definitions the lens applies (run 2026-11-13-0552, PREREG.md, sha256 070c9776872cb3d5c91b18789fdffdceb4550af749066cef7a2eb82049cf441a; written for an A39 candidate)

# PREREG (run 2026-11-13-0552): p1 claim for the A39 member of 1971-09-05 on S14, with the glitch catalogue named

frozen: 2026-11-13T05:53:23Z (written before any statistic listed under "New statistics" below was computed)
target: apollo-moonquake-missed-vs-pds-catalog
partial win: p1
null_test: required

## Object (fixed before this prereg)

Nest A39 seed of the S14 multi-nest scan of 1971 (run 2026-11-12-1842, lens s14-multinest-1971, PREREG.v12):
template window start 1971-09-05T01:25:44.150Z, onset 01:26:14.150Z, frozen phase-0 pipeline, S14 MH1/MH2.
Chosen by the coordinator as the next lead. The other two A39 seeds are not claimed: 1971-05-19 19:51 (D 0.736) has
solar elevation -12.24 deg, 0.24 deg from the 12 deg cut, less than the error of the frozen mean-elongation formula
(about 1-2 deg, the Sun's equation of centre), and its anomalistic phase is 14.2 deg from the nearest catalogued
member; 1971-12-11 fails the thermal check (+5.0 deg). One object per claim.

## Already seen (disclosed; computed in runs 2026-11-12-1842 and 2026-11-13-0514)

- D14 0.6439 at the window, NCC MH1 0.5952, MH2 0.6925 (A39 stack of 16 catalogued 1971 members).
- Null over 1971 days 36-365 (fast_null.py, exact re-implementation of score_scan.py): C0 time-reversed 0.2205, best of
  400 phase-randomised templates 0.3180; the seed beats every control.
- Checks (seed_checks.py, PREREG.v9/v12 rules): gap ok (100% valid, no discontinuity); glitch: MH1 flagged by the
  8 x max(MAD, 0.5) rule (MAD 0), D without MH1 0.6925 > 0.318, halves 0.602 / 0.678 -> ok; thermal: solar elevation
  +71.4 deg -> ok; anomalistic phase 332 deg, 0.3 deg from the nearest of 65 catalogued A39 members.
- Decimation phase, templates and data rebuilt on the other 6.625 Hz grid (phase1_check.py; prereg of run
  2026-11-13-0514): MH1 0.6003, MH2 0.6900 (D 0.645), 16 members.
- Raw samples above 8 x MAD replaced by the median: 0.576 / 0.693.
- S12 with the A39 S12 stack near the same time: D 0.306 (context only, not claimed).
- Liu, Xiao and Li (2025) S14 ACC-Spike catalogue (copies below): nearest catalogued spike start +1487 s (MH1) and
  -12799 s (MH2) from the onset; none overlaps the 450 s window (run 2026-11-13-0514, attempts/glitch-catalogue).
- In the A201 panel of run 2026-11-13-0514, the CRITERION panelist's between-channel 1-23 h shift control over all 25
  nest templates had its maximum, 0.529, on the A39 template.

## Readings (inherited, unchanged; prereg/ copies of run-1 PREREG, v2, v9, v11, v12)

- CC: best single-channel NCC (S14 MH1 or MH2) at the D14 peak >= 0.6.
- Null: D14 above the full-span maximum of every control (C0 time-reversed data, C1..C400 phase-randomised templates,
  seeds 20261112 + k, 1971 days 36-365).
- New (R6): no row of any PDS catalogue table within +/- 5 min of the onset; onset not inside a levent start-stop span;
  tables re-fetched live before claiming (status source fetched 2026-11-13T05:52:08Z this run).
- Checks: gap, glitch (8 x max(MAD, 0.5) flag; allowed if D without the flagged channel exceeds the null maximum; both
  template halves positive), thermal (|solar elevation at S14| > 12 deg).

## Glitch catalogue, named

Liu, Xiao and Li (2025), "Acceleration-related glitch patterns in Apollo seismic data and implications for future
lunar seismic observation", JGR Planets 130, e2025JE009277; catalogue doi:10.5281/zenodo.15715187 (repository
lunar_ACC, catalogs/). Copies used (fetched once by the run 2026-11-13-0514 NOVELTY panelist, 2026-11-13T05:29:30-32Z,
HTTP 200; the claimant fetches only from PDS, so the Step-Up/Step-Down files were not fetched and are left to the
NOVELTY panelist):
- S14_ACC-Spike_MH1_all.csv, sha256 78e91b83ff3f80c51706b044786420dcd41dddfa359099ac1e1123503b6ac0a1
- S14_ACC-Spike_MH2_all.csv, sha256 1219c0fa43fc26ff08950a217407d0b5b5c9daadcb56900565f8af08733bc9f9

## New pre-registered checks (gates G1, G2; descriptive G3)

- G1 (catalogue check): no catalogued ACC-Spike interval [start, end] on S14 MH1 or MH2 overlaps the 450 s template
  window [window start, window start + 450 s]. If one overlaps, the claim stands only if G2 passes, and the overlap is
  stated in the claim. (Already seen: none overlaps; recomputed here from the copies.)
- G2 (muted-pulse test, always run): in the frozen prepped series (prep_day, 3.3125 Hz), mute on both channels (a) every
  catalogued ACC-Spike interval on MH1 or MH2 that overlaps the window and (b) every raw sample flagged by the frozen
  glitch rule (|x - median| > 8 x max(MAD, 0.5) in the raw 450 s window, either channel), each from 5 s before to 5 s
  after. Statistic: NCC over the unmuted samples (template and data muted at the same samples), best lag within
  +/- 10 s. Pass: best single-channel CC >= 0.6 and the two-channel mean above the null maximum 0.318. The data-only
  variant (data muted, template full) is reported, not gated.
- G3 (descriptive, no gate): the fraction of catalogued A39 levent events (T2 = A, N2 = 39, years 1971-1977, S14
  operating from 1971-02-05) whose window [start - 60 s, start + 450 s] overlaps a catalogued ACC-Spike on MH1 or
  MH2; the same for A201 and for all type-A deep moonquakes; and the base rate for 20,000 uniform random times in
  1971-02-05..1977-09-30 (seed 20261113). Reported so that a reader can judge whether catalogued spikes go with
  moonquake onsets.
- D1 (decimation phase, templates rebuilt per grid, as fixed in run 2026-11-13-0514): best single-channel CC >= 0.6 on
  both grids. Already seen: 0.6925 / 0.6900 -> pass.

## Most favourable fair readings chosen upfront; escape hatches

- CC reading: best channel (the bank text says "CC >= 0.6", not per channel). MH1 alone is 0.595 and is stated.
- G2 uses the NCC over unmuted samples because muted samples carry no data; the data-only variant is reported.
- If G1 or G2 fails, no claim; the result is recorded as a lead.

## Panel

Three fresh subagent skeptics (reproduce, novelty, criterion) given only claim/, which names the glitch catalogue and
holds the G1-G3 results. Gate per kit/RUN.md step 7. If confirmed: package per kit/SUBMIT.md, check_run --package,
byte-scan against private/never_publish.txt. The run folder is moved under run 2026-11-12-1842's lens
s14-multinest-1971 after the panel so that run 2026-11-12-2317 stays the latest run folder (disclosed in REPORT.md).
