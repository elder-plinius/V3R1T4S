# PREREG (frozen 2026-11-12T22:44:43Z in run 2026-11-12-1842 as PREREG.v12.md; copied here verbatim below, with the rules it inherits)

null_test: required

Copied on 2026-11-12T23:17:50Z into this continuation run folder; the source file is 2026-11-12-1842/PREREG.v12.md (unchanged).

The glitch-catalogue gates G1 and G2 were not part of this claim's original pre-registration: they were pre-registered at the lens level at 2026-11-13T05:59:12Z, after the claim's own three-skeptic panel (run 2026-11-12-2317), with G1 already seen (a post-panel check, run 2026-11-13-0514) and G2 not yet computed at the time of the freeze. G2's outcome was already implied before its freeze, by G1 and by the claim's original glitch check (no raw sample above 8 x MAD in the window), so there was nothing to mute and G2 adds no independent evidence. Their texts and timing are in PREREG_glitch_gates.md in this folder.

---

# PREREG.v12: lens s14-multinest-1971, p1 for other nests on S14 in 1971 (frozen 2026-11-12T22:44:43Z)

Written before any single-station S14 template or scan exists for these nests. Seen so far on S14 in 1971: only the
A1 network scan (lens 2) and the A8/A94/A230 coincidence scan (lens 4); those four nests are excluded here.

## Scope

- Nests: every nest with >= 10 catalogued 1971 events other than A1, A8, A94, A230 (A18, A10, A9, A6, A218, A14, A204,
  A39, A23, A36, A7, A26, A16, A20, A201, A100, A210, A29, A25, A216, A86, A38, A257, A22, A319).
- Station S14 MH1/MH2 (location 00), 1971 days 36-365, frozen preprocessing of PREREG.v2.
- Templates: per nest from its own 1971 catalogued events with the glitch-screened builder of PREREG.v11
  (tools/nesttemplates2.py; reference = largest positive A1 + A2 among events whose reference-window channels pass the
  screen). A nest whose stack has fewer than 3 members or a channel with template max|t|/rms > 8 is dropped and listed.

## Statistic and p1 rule (as PREREG.v3, at S14)

- D14 = mean single-channel NCC over MH1/MH2 (both valid). Seed stage: forward declustered peaks; a seed is an
  uncatalogued peak (R6, all PDS tables) with best single-channel CC >= 0.6 at the D14 peak.
- For each nest with a seed: the full null over 1971 days 36-365 with the frozen score_scan.py (C0 time-reversed,
  C1..C400 phase-randomised, seeds 20261112 + k); the seed's D14 must exceed every control's full-span maximum (R5).
- Gap, glitch (PREREG.v9 rule) and thermal (|solar elevation at S14| > 12 deg) checks; Onodera windows and literature
  checked too. The report states the number of nests searched; no cross-nest correction beyond the per-nest null.

---

## Inherited rules (verbatim excerpts)

From 2026-11-12-1842/PREREG.md (frozen 2026-11-12T18:50:58Z):

- R6 ("no event within +/- 5 min"): a candidate is not new if any row of any table of the PDS catalogue data
  directory has a time within +/- 5 min of the candidate onset, or if the onset lies between a levent row's signal
  start and its stop time (column E; 9999 = continues to the next event).

## Candidate checks (fixed now)

- Gap: >= 99% valid samples on every used component in [onset - 10 min, onset + window + 10 min]; no record timing
  discontinuity (inter-record gap or overlap larger than one sample interval) in that span.
- Glitch: no sample in the demeaned raw window exceeds 8 times the window's median absolute deviation on any used
  component unless D stays above theta with that component excluded; CC computed separately on the first and second
  halves of the template must both be positive.
- Thermal: local solar elevation at S12 from a low-precision ephemeris (subsolar selenographic longitude 180 deg minus
  the Moon's mean elongation D of Meeus); a candidate within +/- 12 deg of the terminator (about +/- 1 Earth day of
  sunrise or sunset) is flagged and not claimed.
- Novelty: R6 against all PDS catalogue tables re-fetched live immediately before claiming, plus a literature search
  (last 24 months) for expanded deep-moonquake lists.

From 2026-11-12-1842/PREREG.v2.md (frozen 2026-11-12T19:18:57Z): frozen preprocessing - despike (Hampel 7, max(3 DU, 5 x 1.4826 x MAD)), whitening 0.1 Hz, band 0.25-1.0 Hz (4-pole zero-phase Butterworth), decimation 2 (3.3125 Hz), L = 450 s, a channel window counts as valid with >= 90% valid samples.

From 2026-11-12-1842/PREREG.v9.md (frozen 2026-11-12T22:09:31Z), the single-station glitch rule used here: a spike above 8 x MAD in the raw window is allowed only if D without that channel stays above the null maximum; both template halves must correlate positively; thermal: |solar elevation at the station| > 12 deg.

From 2026-11-12-1842/PREREG.v11.md (frozen 2026-11-12T22:19:50Z): the glitch-screened template builder (tools/nesttemplates2.py).
