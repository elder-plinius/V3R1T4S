# How we found it (contributor text, unverified)

The run froze one detector before looking at any candidate: IOC 1-min series, harmonic de-tide plus a 120-min
high-pass, peak over 180 min after an onset that must fall within 10 min of a shallow-water travel time (ETOPO1,
32-neighbour Dijkstra), clean control days a week either side, and a 400-origin-time null. It was checked on a known
positive (2025-11-09 Sanriku, Ofunato) and a shifted negative first.

Two sweeps followed. The main-win sweep took all 960 shallow M >= 6.0 quakes of 2015-2026 that NCEI does not list and
found none with two clean near-field detections (many quakes lacked two usable gauges; several Chilean events showed
coherent arrivals about 25 min after the model time, which the frozen rule rejects). The p1 sweep took the 36 NCEI
earthquake events since 2024 and asked, gauge by gauge, whether a station without an NCEI runup row recorded the wave.
One event survived every stage: the 2024-12-17 Port Vila earthquake, at Luganville and Lifou. A false-alarm audit
(0 detections in 164 random gauge-times), live NCEI re-queries and an ERA5 weather check came next, then three fresh
skeptics, each writing its own checker.
