# CRITERION verdict: second A100-like S14 + S16 event, 1973-10-30 02:25:51.5 UTC (target apollo-moonquake-missed-vs-pds-catalog)

context: fresh subagent started with the Claude Code Agent tool (subagent_type criterion); judged only from claim/ (not the run's attempts/, the run-level PREREG.md or other skeptics' files); own scratch code and outputs in panel_work/criterion/.
injection_suspected: none

Verdict: PASS on the full success criterion (deep-moonquake branch), under readings fixed before the S14 + S16
measurement and fair. The two novelty clauses (PDS tables "re-fetched live immediately before claiming"; published
lists of the last 24 months) belong to NOVELTY; I checked them only against the tables saved 16:15-16:16Z. The
claim's own multiplicity numbers are correct. Its headline sentence leaves them out, which breaks its own PREREG
wording rule. This is a wording fix and not a criterion failure (section 5). The confirmed_scope line below includes
the multiplicity numbers.

## 1. Clause by clause (bank success criterion, deep-moonquake branch)

Freeze times: run1_PREREG.md 2026-11-12T18:50:58Z (R6, gap/glitch/thermal, PDS-URL substitution), v4 19:24:35Z
(per-channel R7, R9), v5 19:27:29Z (R8 with ATT), v14 2026-11-13T01:18:14Z and v15 03:40:56Z (lag-tolerant Dt,
own-lag R7, S14 + S16 null). The S14 + S16 scan that produced every bank-relevant number came after v15. The object's
PREREG.md (frozen 16:22:21Z) only adds attacks and multiplicity, and it lists the numbers already known. Its N0 and the
analysis chain ran 16:23-17:15Z (results/chain_times.txt). The descriptive items (G3, A6b, energy, coda) are labelled
post-freeze.

(a) Saved event package (UTC time, station/channel list, FDSN request URLs, waveforms, template or detector code).
Reading: PDS file URLs of the same Nunn et al. (2022) restoration stand in for FDSN request URLs (EarthScope was not
reachable; fixed in run1_PREREG.md; stated in the bank entry's access note). A strictly literal reading would not
accept the substitution. It is fair, because the URLs point to the official archive of the same data and the package
says so. Evidence: the day-303 S14/S16 MH1/MH2, ATT and S12 files are present and their sha256 sums match (I checked
that subset). Also present: the frozen stack (claim/frozen/nets25_1973_A100.npz), the code and the URL lists.
Met, with the substitution stated.

(b) "NCC >= 0.5 with the stack of a catalogued nest on >= 2 stations". Reading R7: the best single channel at each
station, at that station's best lag within +/- 7 samples of the common lag. Fixed before measurement (v4, v15).
Fair: this is the most favourable fair reading. Under a station-mean reading S14 passes (0.557). S16 fails (0.298)
only because S16 MH2 was unresponsive (section 3).
- My recomputation (claimant's loader and frozen preprocessing; my own NCC arithmetic; panel_work/criterion/ncc_own.py):
  S14 MH1 0.4936, MH2 0.6211 at -5 samples; S16 MH1 0.6196, MH2 -0.0235 at -3 samples. Identical to the claim.
- Other decimation phase (results/decphase_stdout.txt): S14 MH2 0.621, S16 MH1 0.5867.
- Met.
- Hidden quantifier, "the stack": the earlier S12 + S14 A100 stack gives S14 only 0.3547 / 0.3663 for the same event,
  which fails R7 (results/s12_third_stdout.txt). The 5-member S14 + S16 stack gives S14 MH2 0.621. That stack is the
  natural one for an S14 + S16 detection and was built by the builder frozen before v14, not tuned to this event. Even
  so, R7 at S14 depends on which stack is used.
- S16 rests on one channel: without S16 MH1, Dt is -0.0235 (results/glitch_rule_A100_1030.txt).

(c) "Consistent relative arrival times (within 2 s of the nest's moveout)". Reading R8: the ATT-corrected S16-minus-S14
difference lies within 2 s of the median over the nest's catalogued 1973 events above the null. Fixed before
measurement (v5, v15). Fair.
- My recomputation (claimant's ATT reader, my own driver; r8_own.py): candidate 0.714 s. The six references are -0.484,
  0.887, 0.945, -0.296, 0.920 and 0.744 s, median 0.815 s. The difference is 0.10 s.
- Met.
- It is a weak discriminator. Each station's lag is already confined to +/- 2.11 s around a template that carries the
  nest's 80 s S16-S14 moveout. It cannot separate A35 (-79 s) or A244 (-78 s) from A100 (-80 s).

(d) "Occurrence phase consistent with the nest's tidal periodicity". Reading R9: the anomalistic phase lies inside the
shortest arc that holds 95% of the 62 catalogued A100 events. Fixed before measurement (v4, v15). Fair but weak,
because the arc is 271.6 deg wide.
- My Meeus computation (phase_own.py): arc [46.71, 318.34] deg, candidate 161.49 deg, inside. Met.
- My own descriptive, post-hoc check: the 9 catalogued 1973 A100 main-sequence events fit a 27.224 d period with rms
  0.097 d.
  - The candidate lies -0.205 d from that fit. It lies -0.088 d from the time interpolated between the catalogued
    10-02 22:53 and 12-23 15:53 events (step 27.236 d, predicted 10-30 04:33).
  - A random time falls within +/- 0.205 d of a monthly prediction with probability 0.015.
  - All five uncatalogued above-null A100 peaks of 1973 (01-30, 04-22, 06-16, 10-30, 11-26) fill the gaps of that
    monthly sequence, each within 0.21 d.
  - This supports the tidal-periodicity clause much more strongly than R9 does.

(e) Null: "exceeds the maximum obtained on a null set (the same templates ... time-reversed ... shifted >= 1 h) over
the full searched span". Reading: for each template, the full-1973 maximum of C0 (all channels reversed) and of
C1..C400 (S16 rolled within each day by 3600 + 180 k s; every circular shift is >= 1 h). Fixed before measurement
(v14, v15). Fair.
- My re-derivation from results/scan12_1973.jsonl (null_check.py):
  - A100 C0 0.1574, best shift 0.1906, real 0.29806.
  - The candidate ranks 9 of 65,910 A100 forward peaks; 11 peaks lie above the null.
  - All 365 days are present (mean scanned fraction 0.814).
- Met.
- Hidden quantifier, "the same templates": if read as the unstandardised maximum over the controls of all 12 templates
  searched, 400 of 401 controls reach >= 0.298 (A20's run to 0.6247) and the claim would fail. I reject that reading as
  unfair, because the 12 statistics have different null scales (median control maxima 0.15-0.43).
- The pre-registered standardised max-T family-wise null passes (z 17.47 against a largest family-wise control of
  14.36; p_FW = 1/402). I reproduced this.

(f) Data-gap, thermal (sunrise/sunset) and instrument-glitch checks. Readings fixed in run1_PREREG.md and v15. Fair.
My own checks (gap_own.py and others):
- Gap: 100% valid samples on all four channels in [onset - 10 min, onset + 450 s + 10 min]; no timing discontinuity
  on the day.
- Glitch rule: raw-window max |x - median| is 2, 2, 3 and 4 DU; no sample exceeds 8 x max(MAD, 0.5).
- Thermal: solar elevation S14 -65.6 deg, S16 -32.4 deg (my low-precision formula).
- Liu, Xiao and Li 2025 catalogue: all files match SHA256SUMS. No Spike, Step-Up or Step-Down interval overlaps either
  window. The nearest S14 interval ends 02:05:01 and the nearest S16 interval starts 04:01:21.
- Met.

(g) "No event within +/- 5 min in levent.1008weber.csv and the other tables". Reading R6: no row within +/- 5 min
(+59 s for minute resolution) of the onset or the window start, and neither time inside a levent start-stop span.
Fixed in run1_PREREG.md. Fair.
- My own parse of the 12 tables saved 16:15-16:16Z (r6_own.py, 13,239 dated rows): no row within the window and no
  span containing either time.
- The nearest row is levent 73-303 0100 A1 (01:00-02:00), which stops 25.9 min before the onset. The energy profile
  shows that event decayed to background by 02:05-02:20 (results/coda_profile_1030.txt).
- Met for the saved tables. The live re-fetch belongs to NOVELTY.

(h) "Nor in any published expanded deep-moonquake list of the last 24 months": this belongs to NOVELTY. The saved
checks of older lists (Knapmeyer-Endrun and Hammer 2015 nearest -89.3 h; Bulow et al. 2005 nearest +146.6 h) are
reported in results/; I read them but did not re-derive them.

## 2. Null model, multiplicity and selection

- Several candidates from one template: the per-template full-span maximum covers this. Taking the second R7 event, or
  the 9th-ranked peak, adds no factor. The joint statement for both claimed events is bounded by the same value. The
  claim's argument is correct.
- Several templates: the per-template null does not cover this. M1 max-T gives p_FW = 1/402 (reproduced); Bonferroni
  gives 12/402 = 0.0299.
- Station pairs and lenses: the null does not cover this.
  - The empirical bound over the parent run's 55 two-station template-year scans is 55/402 = 0.137 (26/402 = 0.065 for
    1973). Both are limited by having 401 controls.
  - The GEV fit gives 4.655e-10 per template; my Gumbel-by-moments check gives 3.50e-10.
  - The margin is large: the real value is 0.1074 above the best control, and the A100 control maxima have median
    0.1603 and robust sd 0.0079. A chance coincidence is implausible, but any small probability over all lenses rests
    on extrapolation.
- How the pair was chosen: the S14 + S16 lens was written after this event was the strongest new A100 detection on
  S12 + S14, where it failed R7 at S14. The S16 data had not been seen, so the S16 coincidence test is a fresh one.
  What the choice did buy is a second chance at R7 with a different stack (S14 0.366 -> 0.621). CLAIM.md discloses
  this. The event is also above its own null in the S12 + S14 lens (0.3605 > 0.203), so its existence does not depend
  on the chosen pair, although S14 is shared.
- The null does not cover real signals of another source that are coherent at both stations (attribution, section 3),
  or artefacts common to both stations (the glitch checks pass).
- Stated strength: the Multiplicity section of CLAIM.md is accurate and complete. The headline "claim:" sentence
  states only the per-template result. PREREG.md says multiplicity goes "in the claim's scope sentence and headline,
  not in a footnote", with at least the 12-template family-wise result. See the fix in section 5.
- The two events are not presented as independent support. CLAIM.md says so explicitly and labels the 0.402
  reverse-search score at 11-26 as mutual similarity.

## 3. Nest attribution

Taken literally, the bank's membership tests for a deep moonquake are (b), (c) and (d). All three are met with the
A100 stack. The attribution evidence:
- Specificity (results/n0_stdout.txt, results/a6b_all_types.txt; read, not recomputed): none of the 984 catalogued
  non-A100 1973 deep moonquakes reaches the A100 null (largest 0.1409). Scored at its start time, no catalogued 1973
  event of any type exceeds the null, apart from six A100 events.
- Reverse search (results/a5_variant_b_1030.txt; read): the candidate's own window ranks catalogued A100 events 1-6 of
  998, two of them not stack members. The next is 0.148; random windows reach 0.1267 at the 99th percentile.
- C1: the other 11 stacks stay far below their nulls. C2: the maxima sit at the claimed lags.
- S16 MH2 unresponsive. My analysis of results/s16_response_1973_1030.jsonl (r2_by_nest.py):
  - Every event with a valid r2 on days 297-305 shows no MH2 response. Examples: an impact on day 297 (R_MH1 32.44,
    R_MH2 0.88); A20 on day 302 (r2 0.019, against an A20 1973 median of 0.516); A33 on day 304 (0.014, against
    0.455).
  - Catalogued A100 events have a median r2 of 1.037 (n 5).
  - Independent corroboration from the Liu et al. catalogue: zero S16 MH2 entries on days 297-304, while S16 MH1 has
    18-45 per day. MH2 entries resume on day 306 (401). The same MH2-quiet pattern recurs on days 270-275 and 324-334.
  - The dead MH2 is therefore an instrument state, not a contradiction. However, no catalogued 1973 A100 event was
    recorded in that state, so there is no direct positive control.
- Timing: the candidate lies 0.088-0.205 d from the A100 monthly sequence (1(d)).

Cannot be excluded:
- A source with no catalogued 1973 events whose waveform and moveout resemble A100's. A244 (-78 s) has no 1973
  events, and A7's single 1973 event scores 0.
- A35, which has the same moveout within 1 s. Its 1973 events score low (best 0.118, rank 81), which counts against
  it only as far as those events are well recorded.
- No location solution is claimed. Minor inaccuracy: CLAIM.md says A35 (5 N, 36.1 E) lies "inside" A100's error
  ellipse. With the listed 1-sigma errors its offset is 1.68 sigma: outside 1 sigma, inside 2 sigma. The error
  overstates the ambiguity, so it runs against the claimant's interest.

## 4. Non-subsumed

This is a distinct object. It lies 27.2 d before the earlier claimed event (1973-11-26 07:46:28.6), and package
2026-11-13-[credit]-9ff1c507 lists it explicitly as "not part of this claim". Nothing in claim/ shows it was claimed
as a partial win: the p1 claims named in prereg/ come from other runs, and the repository check belongs to NOVELTY.
It is not subsumed. It is also not independent evidence for the first claim, nor the first claim for it.

## 5. Fixes before packaging (non-blocking)

1. Headline and scope sentence: state the per-template p <= 1/402, the max-T family-wise p <= 1/402 over the 12
   templates (Bonferroni 12/402 = 0.03) and the lens history, as PREREG.md's wording rule requires.
2. Change "A35 ... inside that ellipse" to "1.7 sigma from A100's location".
3. Keep the sentence on the FDSN substitution in the package.

## Files written

panel_work/criterion/: null_check.py, ncc_own.py, r8_own.py, phase_own.py, r6_own.py, gap_own.py, r2_by_nest.py
(the inputs are the files in claim/; nothing in claim/ was modified).

confirmed_scope: In the saved PDS Apollo PSE data (Nunn et al. 2022 restoration), an S14 + S16 signal with onset 1973-10-30 02:25:51.5 UTC (MiniSEED Earth-received time) matches the frozen five-event 1973 S14 + S16 stack of catalogued deep-moonquake nest A100 with best single-channel NCC 0.621 on S14 MH2 and 0.620 on S16 MH1 (S16 MH2 unresponsive at the time; S14 reaches only 0.37 with the separate S12 + S14 A100 stack), an ATT-corrected S16-minus-S14 timing 0.10 s from the nest's median, an anomalistic phase of 161.5 deg inside the nest's 95% interval and about 0.1-0.2 d from the times predicted by the catalogued 1973 A100 monthly sequence, and a coincidence statistic of 0.298 above all 401 time-reversed and >= 1 h-shifted full-1973 controls of that template (best 0.191; p <= 1/402 per template and, by the pre-registered max-T test, family-wise over the scan's 12 templates; Bonferroni 12/402 = 0.03; the choice of the S14 + S16 lens after this event's S12 + S14 near miss is not covered, 55/402 = 0.14 over the parent run's scans), passes the pre-registered gap, thermal and glitch checks, and has no row of the 12 PDS catalogue tables as saved 2026-11-13T16:15Z within +/- 5 min or spanning it (nearest: an A1 deep moonquake 01:00-02:00), with the live re-fetch and the 24-month literature search left to NOVELTY, membership in A100 resting on the bank's tests and the attribution tests (a source without catalogued 1973 events and with A100-like waveform and moveout not excluded), and the event not independent of the earlier claimed 1973-11-26 event (same template, statistic, null and readings).
pass: true
