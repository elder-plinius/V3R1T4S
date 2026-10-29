# How we found it (contributor text, unverified)

Brief: map, for every M >= 6.5 shallow subsea earthquake of 2015-2025, whether open tide gauges show a tsunami signal by
the bank's own per-gauge test, and set that against NCEI's listing (partial win p3).

What failed before (earlier runs): a spike rule that deleted large near-field waves, an 80 % window-coverage rule that
dropped gauges with sparse event-time data, and travel times that ran early on a Dijkstra grid; detector recall against
NCEI's own tide-gauge rows was 0.19.

What we did this run, in order:
1. Fast-marching travel times on 2-arcmin ETOPO1 (flat-ocean error under 0.4 %), depth floor and offset calibrated on
   2005-2011 NCEI tide-gauge travel times, held out on 2015-2026 (0.468 of held-out rows still fall outside +/-10 min).
2. An isolated-sample spike rule, availability-based usability, and a causal-filter arrival pick (a synthetic test
   showed zero-phase pre-ringing moving a sharp 1.5 m onset 29.5 min early).
3. A positive control on listed 2012-2014 and 2026 tsunamis: event recall 0.27, misses split into rule misses and
   detection misses.
4. The pre-registered map (v4): 35 of 221 scoreable quakes, fake-origin rate 0.053.
5. Our own break-it check found 7 passes with strong control-day peaks at the wrong time, sensor-tie dependence and
   two aftershocks inside a mainshock's tsunami coda. A declared post-hoc repair (PREREG.v5: literal control-day rule,
   every tied sensor, an overlap rule) gives 26 of 188 against a fake rate of 0.027.
6. A three-skeptic panel in fresh contexts. Its first reproduction rebuilt the headline with its own code but found three
   places where our code departed from the frozen text (the fake origins' control-day window, the stuck-sensor rule,
   long-gap bridging), so it failed the claim. PREREG.v6 corrected the code only; both maps were rerun, no class changed
   at any origin, and a fresh break-it check and a fresh three-skeptic panel judged the corrected map.

What it shows: the open gauges pass the test for about one in seven scoreable quakes, nearly all of them NCEI-listed;
the two unlisted passes are single-site and at the chance rate. Recall on listed quakes is limited by both amplitude
and travel-time error (object/map_summary.txt: among listed-quake gauge rows, 136 have r <= 5 and 100 have
r > 5 but arrive outside the window).
