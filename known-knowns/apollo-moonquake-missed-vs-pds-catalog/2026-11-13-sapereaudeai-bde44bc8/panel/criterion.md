# CRITERION skeptic: rebuilt p1 claim (A38, S14, 1971-05-13), target apollo-moonquake-missed-vs-pds-catalog

context: subagent (fresh context, Claude Code Agent tool, subagent_type criterion)
written: 2026-11-13T09:16Z
read: CLAIM.md; every file in prereg/; original_CLAIM.md; original_panel/ (all four files); package/README.md,
HOW_WE_FOUND_IT.md, INDEX.csv, RUN_IT_YOURSELF.md, object/candidate.json, the-record-we-beat/RECORD.md,
verify-it-yourself/ (all files), how-we-built-it/PREREG.md, PREREG_glitch_gates.md, CHANGES_AFTER_FREEZE.md,
COMMANDS.md, null_test.md; results/ (gates, survey, coverage, hourly, seeds, seed checks, rebuild checks, S12 and
member-similarity files); code/tools/apollo_lib.py, scan.py, fast_null.py, seed_checks.py and
code/scripts/glitch_gates_a38.py.

Claimed: partial win p1. Bank text (CLAIM.md, verbatim): "A new member of a catalogued nest seen on a single station
with CC >= 0.6 and the null test passed (single-station detections are weaker evidence)." The null test is the
success criterion's: "the detection statistic exceeds the maximum obtained on a null set (the same templates
correlated with time-reversed data and with data circularly shifted between stations by >= 1 h) over the full
searched span".

Verdict: p1 is met literally, with a wide margin, by the same object and the same numbers as the confirmed claim. All
the timing statements about the glitch-catalogue gates are literally true. No sentence says or implies that the
catalogue was part of the original pre-registration. The package body gives the gates roughly the right weight, but
the headline sentence (CLAIM.md claim line, the README "## What" section) lists G1/G2 next to the evidence without the
coverage caveat. G2's outcome was already fixed before its freeze. The confirmed_scope below corrects both points.

## 1. p1 element by element

1. "new" (bank: no event within +/- 5 min in levent.1008weber.csv and the other PDS tables). With my own parser over
   data/catalog/ (r6.py): the nearest dated row is levent 71-133 1603 (T2=C). Its stop time (16:40) is 120.1 min
   before the onset and its start is 157.1 min before. No levent start-stop span contains the onset (9999 rows
   resolved to the next event). Every other dated table is more than 10,000 min away. The local levent copy has
   sha256 f95743b2...b9b93c, and both index copies (data/catalog_data_index.html and
   data/catalog_data_index_2026-11-13T083957Z.html) have sha256 593e0315...e2f, as CLAIM.md states. I did not
   re-fetch the tables live or search the literature; that is the NOVELTY skeptic's job.
2. "of a catalogued nest": A38 has 11 catalogued 1971 rows (T2=A, N2=38). The template is the glitch-screened stack
   of 6 of them (results/build_stdout.txt: "A38 events 11 members 6"). The candidate is not a member.
3. "member" (stretched-definition check). This rests on the original panel's evidence:
   - the other 24 nest templates score <= 0.18 at that time;
   - the anomalistic phase is 278.8 deg, against the nest's 274.6 deg mean.
   My full-span forward scan agrees: the six largest A38 daily maxima in 1971 are four catalogued A38 events (days
   187, 106, 351, 297: 0.798, 0.786, 0.771, 0.747), the candidate (0.742) and catalogued A38 day 324 (0.658). The
   next is the catalogued "impact" on day 160 (0.649), already disclosed. Waveform similarity is evidence of
   membership, not proof, and the package says so.
4. "seen on a single station": S14 MH1/MH2 only. The S12 cross-check (D 0.393) is reported and not claimed.
5. "CC >= 0.6": I recomputed both channels from the PDS waveforms with my own NCC code (indep_null.py). It reuses only
   the frozen preprocessing prep_day, because that is part of the pre-registered detector. Results:
   - window start 1971-05-13 18:39:33.736: MH1 0.72677, MH2 0.75672, D 0.74174;
   - the best lag within +/- 10 s is 0.
   Both channels pass, so the reading of "CC" (best channel, each channel or the mean) does not matter.
6. "the null test passed" (prereg R5: D above the full-span maximum of every control):
   - C0 (bank-literal, same templates on time-reversed data, 1971 days 36-365, the whole searched span): my own code
     gives 0.21237 (day 50). Over all 330 days my daily maxima equal results/null_A38_1971.jsonl to within 1.5e-8.
   - C1..C400 (phase-randomised templates): the best is 0.28679 (results/null_A38_1971.jsonl). The rebuild reran all
     400 controls with identical results (results/rebuild_rerun_checks.txt). package/verify-it-yourself/run_checks.sh
     ran here and printed PASS (D 0.7417 against 401 controls, best 0.2868).
   - The bank's "shifted between stations by >= 1 h" part cannot apply to a single-station statistic. The prereg
     declared that before the scan (prereg/run1_PREREG.md, 18:50:58Z). The closest one-station analogue is MH2 NCC
     rolled 1..23 h against MH1, every day, full span. I recomputed it: maximum 0.4857 (day 106, from a catalogued A38
     event on one channel), below 0.742.
   - Null-model adequacy for the data state at the candidate (see section 3): elevated raw-noise stretches occur on
     100 of the 330 scanned days, so the controls sample that state. Day 133's own controls are unremarkable: C0
     daily maximum 0.193 (rank 13 of 330) and best phase-randomised daily maximum 0.264 (rank 5 of 330), both far
     below 0.742.
   - Selection among 25 nests and 14 seeds (results/seeds_summary.json: 14 seeds in 11 nests; the original CRITERION
     file says 16, which is wrong, while CHANGES_AFTER_FREEZE.md and the original gate say 14). The prereg fixed
     per-nest nulls and the original panel's cross-nest null had maximum 0.306. The literal null test passes under
     the narrow and the wide reading.
7. Prereg candidate checks (not part of p1's literal text, but in the prereg's p1 rule): all pass.
   - Gap: 100% valid, no discontinuity.
   - Glitch rule on the raw window, my recomputation from package/object/g2_raw_window.csv: max |x - median| is
     6.50 x MAD on MH1 and 6.33 x MAD on MH2, and max |x - mean| is 6.22 and 6.20 x MAD, all below 8. The template
     halves give 0.743 and 0.742.
   - Thermal: solar elevation 61.3 deg.

Non-subsumed: the full criterion is not met (one station, no moveout or location), so p1 is not swallowed by a full
win. The only overlapping object is the unsubmitted earlier package of the same claim, which this one replaces. No
filed package or claim covers it (original_panel/novelty.md, section 4).

## 2. Gate timing: freeze times in prereg/ compared with the package's statements

| file / event | time (UTC) |
|---|---|
| prereg/run1_PREREG.md | 2026-11-12T18:50:58Z |
| prereg/run1_PREREG.v2.md | 19:18:57Z |
| prereg/run1_PREREG.v9.md | 22:09:31Z |
| prereg/run1_PREREG.v11.md | 22:19:50Z |
| prereg/run1_PREREG.v12.md, the operative prereg; prereg/PREREG.md is v12 verbatim plus inherited excerpts, copied 23:17:50Z (checked: v12 text is contained verbatim) | 22:44:43Z |
| original NOVELTY panel (looked at the Liu et al. catalogue: "no catalogued glitch on S14 MH1/MH2 between 17:00 and 19:08:36") | 2026-11-13T00:03Z |
| original gate, CONFIRMED_PARTIAL (original_panel/gate.md) | 01:40:38Z |
| G1 for A38 seen, run 2026-11-13-0514 (catalogue copies fetched 05:29:30-32Z) | about 05:30Z |
| prereg/run_2026-11-13-0552_PREREG_gate_definitions.md (written for an A39 object; sha256 070c9776...f441a, as PREREG_glitch_gates.md states) | 05:53:23Z |
| prereg/a38_glitch_check_lens_PREREG_frozen_2026-11-13T055912Z.md ("before G2 was computed for A38") | 05:59:12Z |
| descriptive survey of the other seven files and hourly counts (prereg/rebuild_run_PREREG.md) | 08:34-08:36Z |
| prereg/rebuild_run_PREREG.md | 08:39:50Z |

The following statements all match this table:

- CLAIM.md, README.md, HOW_WE_FOUND_IT.md, how-we-built-it/PREREG.md (added header paragraph), COMMANDS.md,
  CHANGES_AFTER_FREEZE.md and object/candidate.json ("timing") all say: "were not part of this claim's original
  pre-registration: they were pre-registered at the lens level at 2026-11-13T05:59:12Z, after the claim's own
  three-skeptic panel ..., with G1 already seen (a post-panel check, run 2026-11-13-0514) and G2 not yet computed at
  the time of the freeze."
- PREREG_glitch_gates.md adds that the lens reused definitions frozen at 05:53:23Z for another object.
- PREREG_glitch_gates.md also says that the order rests on the run records, not on file times.

Both verbatim prereg texts in PREREG_glitch_gates.md are byte-contained copies of the prereg/ files. The original
NOVELTY panelist's earlier look (before the original gate) is disclosed in CLAIM.md and README.md. In effect, G1's
outcome was known even before the original panel ended. The disclosure covers this, although "(a post-panel check)"
read alone suggests G1 was first seen after the panel.

Whether any wording implies that the catalogue was part of the original pre-registration: I found none. Every place
that names the gates carries the "not part of ... original pre-registration" sentence. Two places mention "frozen":
HOW_WE_FOUND_IT.md says "gap, glitch and thermal checks, all fixed in a pre-registration before the scan", and
README.md G2 says "the frozen glitch rule". Both refer to the original 8 x MAD raw-sample rule, which was
pre-registered (prereg/run1_PREREG.md; the max(MAD, 0.5) floor is in seed_checks.py and does not bind here, because
MAD is 4 and 6). They do not refer to the catalogue.

## 3. Weight of the gate results (recomputed)

- G1 is literally true. My own parse of the full catalogue copies in data/lit_acc/ (sha256 78e91b83...0a1 and
  1219c0fa...9f9, matching CLAIM.md) finds no MH1 or MH2 ACC-Spike interval overlapping
  [18:39:33.735, +450 s]. The nearest starts are +3013.925 s (MH2) and +7347.963 s (MH1) after the onset. The last
  ends before the window are -32440.867 s (MH2, 09:39:22.9) and -35349.093 s (MH1).
- The package extracts are correct: the object/glitch_catalogue_*.csv files are the verbatim (start, end) subset,
  in source order, of the rows starting in 1971 days 36-365, with 9361 and 11394 rows.
- G3 recomputed independently: 898 of 6607 type-A events (exact), and 16.8% of 20,000 random times with my own seed
  (the package says 16.6%).
- G1 carries almost no information for this window. The catalogue lists no MH1/MH2 spike interval between 09:39:23
  and 19:30:17 UTC that day. The package also says that none of the three types appears from 09:39:24.528 to
  19:08:36.981; I could check only the spike files, because the step files are not in the claim folder. Over
  1971 days 36-365 the spike catalogue is often silent for long stretches: 114 runs of 8 h or more with no MH1/MH2
  spike start, and zero spikes in 48.6% of quiet hours.
- On 1971-133 the silent stretch matches a distinct raw-data state of S14 MH1/MH2. Per-minute raw MAD is 0-1 counts
  before about 09:56 and after about 19:07, and mostly 2-29 counts in between (hourly 5-9). That state contains
  frequent rule-flagged excursions that the catalogue does not list, at 18:23, 18:28-18:31, 18:35-18:36 and 18:57.
  The window lies in a 21-minute clean gap between them, about 20 min before the state ends.
- README.md says this correctly: "G1 shows that the published catalogue does not flag this window; it does not show
  that the catalogue's detector covered this stretch" and "Passing G1 is therefore the usual outcome, and on its own
  weak evidence."
- G2 adds no independent evidence. Before G2's freeze (05:59:12Z), two facts were already known:
  - G1 had been seen: no overlapping catalogued spike.
  - The original pre-panel checks (results/seed_checks_final.json: spike_over_8mad false, MAD 4.0 and 6.0) had
    already shown that the same |x - median| > 8 x max(MAD, 0.5) rule flags no sample in the window.
  So nothing could be muted. G2 then reduces to the original NCC at the best lag within +/- 10 s, which is the
  declustered peak itself (lag 0). "G2 not yet computed at the time of the freeze" is literally true, but it reads
  as if G2 were a blind test, and it was not. The phrase "with nothing to mute, gate G2 leaves the mean at 0.742"
  (CLAIM.md, README.md) conveys this in substance.

## 4. Sentences I find misleading or imprecise (none changes the p1 verdict)

1. CLAIM.md claim line and package/README.md "## What": "... and no S14 MH1/MH2 ACC-Spike interval of the Liu, Xiao
   and Li (2025) acceleration-glitch catalogue overlaps the window (gate G1; with nothing to mute, gate G2 leaves the
   mean at 0.742; both gates pre-registered after the claim's original panel, with G1 already seen) ...". The timing
   is honest, but the headline presents G1 as part of the evidence for the win, with no hint that the catalogue is
   silent for about 10 hours around the window. My confirmed_scope replaces this section.
2. package/HOW_WE_FOUND_IT.md: "the catalogue happens to list nothing on S14 MH1/MH2 for nine hours around the
   event". The empty stretch (09:39:24-19:08:37, all types) ends about 21 min after the window ends, so it is not
   "around" the event. "Happens to" suggests chance, but the stretch coincides with a distinct raw-noise state
   (section 3). A better wording: "for the nine and a half hours up to about 20 minutes after the window".
3. "G2 not yet computed at the time of the freeze" (CLAIM.md, README.md, HOW_WE_FOUND_IT.md, how-we-built-it/PREREG.md,
   PREREG_glitch_gates.md, COMMANDS.md, CHANGES_AFTER_FREEZE.md, object/candidate.json "timing"). This is true but
   invites over-reading. Suggested addition: "its outcome was already implied by G1 and by the original glitch check
   (nothing to mute), so it adds no independent evidence."
4. package/README.md: "from 09:39:25 to 19:08:37 UTC". The first interval after the gap starts at 19:08:36.981, so
   the end bound should round down (19:08:36). This is trivial.
5. package/INDEX.csv value: "no Liu et al. 2025 S14 ACC-Spike interval in the window (gates G1, G2)". It has no
   post-panel or coverage qualifier. This is minor.
6. prereg/a38_glitch_check_lens_PREREG_frozen_2026-11-13T055912Z.md says "sha256 in PREREG.md". In this folder that
   means run_2026-11-13-0552_PREREG_gate_definitions.md, not prereg/PREREG.md. This is a cross-reference nit; the
   hashes are correct where they appear.

## 5. Recomputation record

Scripts and outputs are in the panel scratch area p1r_criterion, outside the claim folder:
- g1_indep.py: G1 and the extract check.
- day133_raw.py, transitions.py and state_and_null.py: the raw-noise state and day 133's null rank.
- state_vs_catalogue.py: catalogue silence against noise state.
- indep_null.py and indep_null.jsonl: own NCC and C0 over 330 days, plus the 1..23 h inter-channel shift.
- r6.py: PDS tables.
- g3_check.py: G3.
- summarise_null.py.

Key outputs, quoted above:
- own C0 full-span maximum 0.21237;
- inter-channel shift maximum 0.4857;
- day-133 window NCC 0.72677 / 0.75672, D 0.74174, best lag 0;
- nearest PDS row 120.1 min (stop) / 157.1 min (start);
- the package checker printed PASS.

Processes: one background job (indep_null.py, under a timeout), recorded in the scratch pids.txt. It exited when
done; nothing I started is still running.

confirmed_scope: On Apollo S14 long-period channels MH1/MH2 (PDS MiniSEED, Earth-received time), the 450 s window starting 1971-05-13 18:39:33.7 UTC correlates with the S14 stack of six catalogued 1971 A38 deep-moonquake events at NCC 0.757 (MH2) and 0.727 (MH1), its two-channel mean 0.742 exceeds the 1971 days 36-365 full-span maxima of the time-reversed-data control (0.212) and of all 400 phase-randomised-template controls (best 0.287), and no dated row of any PDS Apollo seismic event catalogue table lies within +/- 5 min of it (nearest 120 min), which meets bank partial win p1 as a single-station detection of an A38 nest member absent from the PDS catalogue; the glitch-catalogue gates G1 and G2, pre-registered only after the claim's original panel and with G1 already seen, also pass but add little evidence: no S14 MH1/MH2 ACC-Spike interval of the Liu, Xiao and Li (2025) catalogue overlaps the window, yet that catalogue lists none on those channels between 09:40 and 19:30 UTC that day, and with nothing to mute G2 leaves the statistic unchanged.

pass: true
