# Null test: p3 completeness map under the pre-registered rules (PREREG.md to PREREG.v4, code with the PREREG.v6 corrections), fake-origin catalogs

controls: 400
best_control: 0.0780
real: 0.1584
real_beats_all_controls: yes
command: python3 how-we-built-it/code/summarize_v4_from_map.py  (on object/map.csv, the map of attempts/completeness-map-v6/code/p3_map_v6.py v4 0 1)

Statistic: SIGNAL / USABLE over the 264 subsea quakes under the v4 rules. Real: 35 / 221 (object/null.json). Controls:
400 fake catalogs (numpy default_rng, seed 20261024, map rows in time order, the draw of
attempts/completeness-map/code/summarize_map.py); each takes, per quake, the full pipeline's result at one of two fake
origins (o-5 h, o-7 h), with control days relative to the fake origin (stage-2 window [floor_h(oo-8 d-1 h),
ceil_h(oo+9 d)], PREREG.v6 item 1). Mean control 0.0523, best 0.0780. Pooled fake rate 23 / 437 = 0.0526: 14 / 219 at
o-5 h, 9 / 218 at o-7 h; expected chance SIGNALs among the 221 real USABLE quakes 11.6, among the 113 unlisted ones 5.9
(object/map_summary.txt). Deterministic worst case (a fake SIGNAL wherever either fake origin has one):
19 / 218 = 0.0872, below 0.1584 (verify-it-yourself/check_p3.py).
Limitation: the 400 catalogs are resampled from two fake runs per quake, not 400 independent pipeline runs. Binomial
tail as a check: P(X >= 35 | n 221, p 0.0526) = 6.7e-09; at the worse fake origin (p = 14/219) 7.1e-07.

The run records the same values for the as-run v4 map (before the PREREG.v6 corrections): no class changes at any origin.

Sensitivity analysis, not the claim (post-hoc PREREG.v5 rules with the same corrections, sensitivity-v5/null.json):
real 26 / 188 = 0.1383, pooled fake rate 11 / 407 = 0.0270 (6 / 202 at o-5 h, 5 / 205 at o-7 h), best of 400 0.0495,
real beats all 400. Without the PREREG.v5 overlap rule (rules 1-2 only, sensitivity-v5/no_overlap.txt): real
26 / 221 = 0.1176, fake rate 0.0320, best of 400 0.0550, real beats all.
