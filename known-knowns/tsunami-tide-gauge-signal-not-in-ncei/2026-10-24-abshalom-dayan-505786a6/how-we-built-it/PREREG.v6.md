# PREREG.v6: implementation corrections (no rule change), written AFTER panel round 1

Declared as such. The REPRODUCE skeptic of panel round 1 (kept in panel_round1/reproduce.md, pass: false) found that
the code departs from the frozen text in three places. No rule of PREREG.md to PREREG.v5 changes: population, scope,
travel times, sensor list, spike rule, coverage rules, the 5x bar, the +/-10 min arrival rule, sites, the v5 control-day,
tied-sensor and overlap rules, LISTED, fake origins (o-5 h, o-7 h) and the 400-catalogue null (seed 20261024) are as
frozen. Only the code is corrected so that it does what the text says. The results are reported whichever way they go.

1. Fake-origin control days (PREREG.md section 3: "their control days are relative to the fake origin; stage 2 for
   fake detections as for real ones"; section 2: "fetch [floor_h(o-8 d-1 h), ceil_h(o+9 d)]"). For a fake origin oo,
   stage 2 reads [floor_h(oo-8 d-1 h), ceil_h(oo+9 d)], not the real origin's window (which cut day -7's 24 h
   pre-window short by 4 h at o-5 h and 6 h at o-7 h). Data access is PREREG.v4's composition (saved windows of the same
   code plus one GET per uncovered gap). The real origin's window is unchanged.
2. Stuck sensor (PREREG.md section 2: "a run of >= 60 identical consecutive raw values inside the 24 h pre-window").
   Computed on the scored sensor's raw samples (numeric slevel, duplicate time stamps dropped, sorted by time) with time
   stamps in [o-24 h, o-1 min], before gridding, gap filling and the spike rule. (The code ran it on the gridded,
   interpolated, spike-cleaned 1-min series.)
3. Gap bridging for the filter (PREREG.md section 2: "gaps <= 30 min bridged for the filter only"). A run of at most
   30 missing minutes between two present minutes is filled linearly for the filter; a longer run is not filled at
   all. (The code also filled the first 30 minutes of longer runs.) Bridged minutes return to NaN after filtering, as
   before.

Clarification, as implemented and unchanged: the "1-min grid" is time-weighted linear interpolation of the raw samples
onto whole minutes, kept only at minutes with a raw sample exactly on the minute or within 5 min on both sides.

Applied to both maps: the v5 rules (the claimed map, attempts/completeness-map-v6/out/) and the v4 rules
(attempts/completeness-map-v6/out_v4rules/), real and fake origins alike, every one of the 264 quakes. The as-run v5 and
v4 maps stay in their folders and are reported next to the corrected ones. The positive control and the main-win screen
are not rerun (no claim rests on them). The code keeps the old behaviour by default (det.IMPL6 = False) so that the
as-run outputs still reproduce; the v6 drivers set det.IMPL6 = True.
