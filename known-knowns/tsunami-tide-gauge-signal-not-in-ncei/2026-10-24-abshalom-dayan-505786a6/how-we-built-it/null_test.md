# Null test: p3 completeness map, v5 rules with the PREREG.v6 implementation corrections (the claimed map), fake-origin catalogues

controls: 400
best_control: 0.0495
real: 0.1383
real_beats_all_controls: yes
command: .venvtsu/bin/python -W ignore attempts/completeness-map-v6/code/summarize_v6.py  (after attempts/completeness-map-v6/code/p3_map_v6.py v5 0 2 and v5 1 2)

Statistic: SIGNAL / USABLE over the 264 subsea quakes under PREREG.v5's rules, implemented as corrected by PREREG.v6.
Real: 26 / 188 (attempts/completeness-map-v6/out/null.json). Controls: 400 fake catalogues (seed 20261024); each takes,
per quake, the full pipeline's result at one of two fake origins (o-5 h, o-7 h), with control days relative to the fake
origin (stage-2 window [floor_h(oo-8 d-1 h), ceil_h(oo+9 d)], PREREG.v6 item 1) and the same OVERLAP rule. Mean control
0.0271, best 0.0495. Pooled fake rate 0.0270: 6 / 202 at o-5 h, 5 / 205 at o-7 h; expected chance SIGNALs among the 188
real USABLE quakes 5.1 (map_summary.txt).
Limitation: the 400 catalogues are resampled from two fake runs per quake, not 400 independent pipeline runs. Binomial
tail as a check (scipy.stats.binom): P(X >= 26 | n 188, p 0.0270) = 1.3e-11; at the worse fake origin (p = 6/202)
9.9e-11.

The corrections change no class at any origin of any quake (map_summary.txt, "as-run v5 -> v6"), so these values equal
the as-run v5 map's. Under the v4 rules with the same corrections (attempts/completeness-map-v6/out_v4rules/): real
35 / 221 = 0.1584, pooled fake rate 0.0526, best of 400 0.078, real beats all 400 (as the pre-registered v4 map as run).

Without the PREREG.v5 overlap rule (rules 1-2 only, attempts/completeness-map-v6/out/no_overlap.txt): real 26 / 221 =
0.1176, fake rate 0.0320, best of 400 0.0550, real beats all.
