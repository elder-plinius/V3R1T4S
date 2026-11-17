# CRITERION skeptic: p1 claim, target apollo-moonquake-missed-vs-pds-catalog

context: subagent (fresh context, Claude Code Agent tool, subagent_type criterion)

Claimed: partial win p1. Bank text (data/target_bank_entry.md, identical in CLAIM.md): "A new member of a catalogued
nest seen on a single station with CC >= 0.6 and the null test passed (single-station detections are weaker
evidence)." The null test is the one in the success criterion: "the detection statistic exceeds the maximum obtained on
a null set (the same templates correlated with time-reversed data and with data circularly shifted between stations by
>= 1 h) over the full searched span".

Verdict: the literal p1 is met, with a margin that holds under every reading I could build of each element.

## Element by element

1. "catalogued nest": A38 is a catalogued deep-moonquake nest. It has 41 levent rows with T2=A, N2=38, and a location
   row in data/catalog/nakamura_2005_dm_locations.csv.
2. "seen on a single station": S14 MH1/MH2 only. The S12 cross-check (results/s12_crosscheck.txt, D 0.393) is
   reported but not claimed. Only S12 and S14 were operating in May 1971.
3. "CC >= 0.6": the NCC with the S14 stack of 6 catalogued 1971 A38 events (results/build_stdout.txt) is 0.757 on MH2
   and 0.727 on MH1, with a two-channel mean of 0.742. This passes on every reading (best channel, each channel or the
   mean). I recomputed the forward A38 statistic on day 133 from the waveforms: 0.7417, at window start 18:39:33.7.
4. "the null test passed" (prereg R5: D above the full-span maximum of every control):
   - Bank-literal single-station part (same templates, time-reversed data, days 36-365): the maximum is 0.2124. I
     recomputed it independently over all 330 days and got 0.2124.
   - 400 phase-randomised templates (results/null_A38_1971.jsonl): best full-span maximum 0.2868, median 0.220.
     fast_null.py replaced the prereg's frozen score_scan.py. I ran score_scan.py on day 133 with 400 controls and
     seed 20261112: all 400 control maxima and rev_max are identical to the null file (max abs diff 0.0).
   - The bank's "shifted between stations" control cannot exist for one station. The prereg declared that before the
     scan (C0 = "bank-literal for one station", prereg/run1_PREREG.md, 18:50:58Z). As a stress test I ran the closest
     analogue: MH2 NCC circularly rolled by 1..23 h against MH1, over the full span. Its maximum is 0.486, from a
     catalogued A38 member on day 106 on one channel. The candidate (0.742) still exceeds it.
5. "new": the candidate is new against the PDS catalogue. The nearest dated row in any PDS table is 120 min away (the
   end of the levent 71-133 16:03-16:40 meteoroid impact). No levent start-stop span contains the onset. The tables
   without dates (dm arrivals/locations, Weber S picks, AI arrivals) have no times to match. I re-fetched the
   catalogue data index once at 2026-11-12T23:55:27Z (HTTP 200). Its sha256 is 593e0315...e2f, identical to
   data/catalog_data_index.html, so no table changed. The Onodera S14 SP windows (data/lit/) have nothing on
   1971-133 near 18:40; the nearest is 23:03. I did not run my own 24-month literature search; that belongs to the
   novelty skeptic. The package's scout record (data/scout_record.md) lists none found.
6. "member" (a stretched-definition check: does high CC mean A38 membership?):
   - At the candidate time every one of the other 24 nest templates scores D <= 0.18 within +/- 1 h
     (results/s14_multinest_scan_1971.jsonl). The signal matches A38 specifically.
   - Over 1971, the A38 template's six highest peaks are four catalogued A38 events (0.798, 0.786, 0.771, 0.747), the
     candidate (0.742) and a fifth A38 event (0.658). The 7th is levent 71-160 17:05, catalogued as a meteoroid
     impact (T2=C), at 0.649. Every other catalogued event scores <= 0.22.
   - The candidate's anomalistic phase (mean anomaly, code/tools/ephem.py) is 278.8 deg. The A38 circular mean over
     its 41 catalogued events is 274.6 deg, so the candidate is closer to the mean than 93% of catalogued members.
     That is consistent with the nest's tidal periodicity, although p1 does not require it.
   - Caveat: the 0.649 score on a catalogued "impact" (itself at A38 phase, 270.7 deg, so probably a misclassified
     A38 event) shows that CC alone does not prove membership. The candidate is above it, and the specificity and
     phase evidence support A38.

## Selection among many (25 nests, 16 seeds)

The prereg (prereg/PREREG.md = prereg/run1_PREREG.v12.md, frozen 22:44:43Z) fixed three things: per-nest nulls, "no
cross-nest correction beyond the per-nest null", and that the number of nests searched would be stated. The claim
states 25. There were 16 seeds in 11 nests (results/seeds_summary.json), and the claimed one has the largest D. The
package holds only the A38 null; the other seeds are not claimed.

To test the wider reading of "over the full searched span" (all 25 templates), I computed a cross-nest null on the
same days 36-365: C0 for all 25 nests plus 2 phase-randomised controls per nest, with my own seeds (75 controls). Its
maximum is 0.306, and the per-nest C0 maxima range from 0.189 to 0.246. A 0.742 statistic is far above any noise
control under either the narrow or the wide reading. Choosing the largest of the 16 seeds does not weaken the literal
"null test passed".

## Prereg timing

- R4''/R5/R6 and the null design come from prereg/run1_PREREG.md (18:50:58Z), the S14 single-station rules from
  prereg/run1_PREREG.v9.md (22:09:31Z), and the glitch-screened builder from prereg/run1_PREREG.v11.md (22:19:50Z).
- v12 (22:44:43Z) says it was written before any S14 template or scan existed for these 25 nests.
- These timestamps are self-declared inside the files; the package's file times are copy times. Nothing in
  results/ contradicts the order, but I cannot independently prove it.
- Deviations: the prereg named score_scan.py for the null and fast_null.py was used; I verified exact equality on day
  133.
- The templates come from the scored year's own catalogued events. There is no dev/holdout split, but the candidate
  is not a template member and the controls use the same templates, so this does not inflate the result.

## Checks (results/seed_checks_final.json, spot-verified)

- Gap: 100% valid samples and no timing discontinuities in [onset - 10 min, onset + L + 10 min].
- Glitch: no raw sample > 8 MAD inside the template window. I located the nearest glitch clusters at 18:31:23-18:31:36
  (MH2) and 18:35:36-18:36:03 (both channels), at least 3.5 min before the window start, and outside it as the
  prereg defines the window. The half-window CCs are 0.743 and 0.742, so the match is spread over the whole window
  and not driven by one feature.
- Thermal: solar elevation at S14 is 61.3 deg, far from the terminator.
- Not a duplicated segment: the best two-channel CC with any single catalogued A38 event is 0.704
  (results/member_similarity.txt).

## Baseline

baseline/README.md says no published baseline applies. That is correct for p1, which is an existence claim tested
against the PDS catalogue and the null, not a score compared with a published score. Nothing to match on data, split
or metric.

## Non-subsumed

Bulow-style template-matched events are in levent.1008weber.csv, which was checked. The parent run's p2 package is a
different object (A1 recovery on S12). Nothing in the package subsumes this event.

## Residual limits (not blocking p1)

- Single station: no moveout or location, so the full criterion is not met.
- The onset is a convention (window start + 30 s, Earth-received time), not a phase pick.
- PDS file URLs replace FDSN URLs (declared access note in data/target_bank_entry.md).
- The 24-month literature novelty check is left to the novelty skeptic.

Scratch (outside the claim folder, in the panel scratch area p1_criterion): robust_null.py and robust_K2.jsonl
(cross-nest and inter-channel nulls), ss133.jsonl (score_scan day 133), a38_peaks.py, phase.py, near_rows.py.

confirmed_scope: On Apollo S14 long-period channels MH1/MH2 (PDS MiniSEED, Earth-received time), the 450 s window starting 1971-05-13 18:39:33.7 UTC correlates with the S14 stack of six catalogued 1971 A38 deep-moonquake events at NCC 0.757 (MH2) and 0.727 (MH1), its two-channel mean 0.742 exceeds the 1971 days 36-365 full-span maxima of the time-reversed-data control (0.212) and of all 400 phase-randomised-template controls (best 0.287), and no dated row of any PDS Apollo seismic event catalogue table lies within +/- 5 min of it (nearest 120 min), which meets bank partial win p1 as a single-station detection of an A38 nest member absent from the PDS catalogue.

pass: true
