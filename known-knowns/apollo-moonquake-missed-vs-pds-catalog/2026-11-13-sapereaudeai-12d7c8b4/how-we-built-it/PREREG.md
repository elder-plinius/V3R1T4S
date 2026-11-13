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
