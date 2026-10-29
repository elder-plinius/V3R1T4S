# PREREG.v5: repair round for the p3 map (stricter rules, written AFTER the v4 map and the step-5 self-break)

This is a post-hoc repair, declared as such. The frozen map (PREREG.md to v4) is kept and reported unchanged; v5 is
a second map scored once, with rules that only remove SIGNALs and that apply identically to real and fake origins.
Prompted by self_break/verdict.md (FLAWED): the control-day reading, sensor ties, the stage-2 sensor re-pick and
aftershock codas. Nothing else changes: population, scope, travel times, filters, spike, stuck and coverage rules,
the 5x bar, the +/-10 min arrival rule, sites, LISTED, fake origins (o-5 h, o-7 h) and the 400-catalogue null.

1. Control days, literal reading of "signals absent on the same gauges in the same hours on control days": a
   detecting code passes only if >= 10 of its 14 control days are usable and on none of the usable ones r > 5 in the
   same window [o + k d + ETA - 10, o + k d + ETA + 120] min, whatever the arrival. (v4: no control day DETECTS.)
2. Sensor ties: per code, the sea-level sensors with the largest sample count in the stage-1 window (equal counts) are
   all scored, each on its own series, with the same sensor on its control days (stage 2 never re-picks). For each
   origin the code is USABLE if any tied sensor is usable; it DETECTS only if every usable tied sensor detects; it
   PASSES only if every usable tied sensor passes (rule 1); it is UNDECIDED if it detects, no usable tied sensor has a
   control day with r > 5, and some usable tied sensor has fewer than 10 usable control days.
3. Overlap: an origin (real or fake) is OVERLAP when any other ComCat event in data/comcat/m65_d70_2015_2025.csv
   (M >= 6.5, depth <= 70 km, land or sea) has its origin in the 24 h before it and its epicentre within 1000 km of this
   quake's epicentre. OVERLAP origins are not scored: they leave the USABLE denominator (real and fake alike), are
   counted in the bounds over 264 as unknown, and are listed with their LISTED status.
4. Classes per origin: NO_GAUGE, OVERLAP, NO_DATA, then USABLE -> SIGNAL / SIGNAL_UNDECIDED / NO_SIGNAL as before.
5. Reported: the v5 headline SIGNAL / USABLE with Wilson interval, bounds over 264, SIGNAL x LISTED, the fake-origin
   null (400 catalogues, seed 20261024, mean, best, pooled fake rate, expected chance count) and the chance-corrected
   excess, next to the v4 numbers. A main-win candidate (PREREG.v3) is checked again under v5.
6. Data: the same cached windows; any window not cached is fetched once (honest GET), within the 2 GB total.
