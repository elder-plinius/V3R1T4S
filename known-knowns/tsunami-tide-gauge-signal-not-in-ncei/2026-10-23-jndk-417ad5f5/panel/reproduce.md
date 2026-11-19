# REPRODUCE skeptic: NCEI event 5942, gauges luga / lifo / lifo2

context: subagent (Claude Code Agent tool, fresh context)

Scope: I read only the claim package (CLAIM.md, REPRODUCE.md, data/, and code/ only after my own checker had run).
All computation ran on the remote job queue (jobs 2382, 2387, 2390, 2391; job 2388 failed because a path was wrong
and was rerun as 2390).

## Definitions checked (quoted from CLAIM.md)

- p1: "Gauge observations (amplitude, arrival) for a listed NCEI event at >= 2 gauges where NCEI has no runup rows for those stations."
- Per-gauge evidence standard: "on each gauge, a band-passed (2-120 min) signal with peak amplitude > 5x the RMS of the preceding 24 h in the same band; arrival times at all gauges consistent within +/- 10 min with shallow-water travel times computed from the source ...; signals absent on the same gauges in the same hours on control days; and the NCEI ... runups API ... no runup row for those gauges (partial win)."
- Source: NCEI event 5942, -17.686 168.034, 2024-12-17 01:47:26 UTC (data/ncei_event_5942.json).

## My independent checker (mine/rcheck.py, mine/extra.py; written before reading code/)

- Data: re-downloaded all of 2024-12-01T00:00..2024-12-31T00:00 for luga, lifo and lifo2 from IOC SLSMF API v1 (one call each).
- Processing: 1-min grid, de-spike (11-min running median, |res| > max(8 robust sigma, 5 cm)), gaps <= 10 min interpolated, longer gaps masked. A 12-constituent harmonic tide plus trend was fitted over the 30 days and removed, then the band-pass was applied in two ways: (A) zero-phase 4th-order Butterworth high-pass at 120 min, and (B) an FFT brick-wall filter for 2-120 min. At 1-min sampling the 2-min edge is the Nyquist period.
- Travel time: my own 16-neighbour Dijkstra on ETOPO1 (NCEI THREDDS; ERDDAP timed out), c = sqrt(g h). I ran it at 1 and 2 arcmin with several minimum-depth settings, and took the gauge at the nearest water cell.
- Arrival: first minute after origin with |bp| > 3x rms24, which must fall within ETA +/- 10 min. R = max|bp| in [arrival, arrival+180 min] / rms(bp over the 24 h before origin). A variant with a fixed window [ETA-10, ETA+180] gave identical numbers.
- Controls: the same clock hours on every December day whose 24 h + 5 h window does not touch the event (27 days: Dec 2-16 and Dec 19-30). I also ran an all-hours null with origins every 30 min through December, excluding +/-36 h around the event (1238 origins).

## Job outputs (key numbers)

**Job 2382 (rcheck.py)**
- Integrity:
  - The sha256 of each decompressed saved file matches data/FETCHLOG.tsv: ioc_luga, ioc_lifo, ioc_lifo2 and ncei_runups (4/4).
  - FETCHLOG lists 3 more control-window files (ioc_*_420265.., _b722bf.., _4ba460..) that are not in the package. Job 2391 re-fetched those exact URLs, and all 3 sha256 values match the log.
- Re-download vs saved files: every overlapping sample is identical (max |diff| 0.000000) for luga/prs, lifo/prs, lifo/rad, lifo/bat and lifo2/rad. The IOC API returned the same data again.
- lifo/rad vs lifo2/rad: corr 1.0000, mean difference 0.0000. lifo2 is the same radar series as the lifo rad channel. lifo (prs, pressure) and lifo2 (rad, radar) are still two different instruments, but they sit at one site, so there are 2 independent sites: Luganville and Lifou.
- My ETAs:
  - luga: 50.28 min (1 arcmin, h >= 1 m), 49.66 (1 arcmin, h >= 5 m), 45.88 / 45.80 (2 arcmin).
  - lifo / lifo2: 38.10, 37.46, 36.35 / 36.19.
- Event results (method A; B in brackets):

| gauge/sensor | rms24 m | peak m | p2t m | R | first >3 rms | peak at |
|---|---|---|---|---|---|---|
| luga/prs | 0.0092 | 0.0777 | 0.136 | 8.45 [8.41] | +43 min | +70 |
| lifo/prs | 0.0115 | 0.0605 | 0.101 | 5.24 [5.21] | +35 | +79 |
| lifo/rad | 0.0111 | 0.0581 | 0.099 | 5.22 [5.20] | +35 | +79 |
| lifo2/rad | 0.0111 | 0.0583 | 0.100 | 5.23 [5.21] | +35 | +79 |

  Minutes are counted from the 01:47:00 grid minute, so +43 is the raw sample at 02:30:00 UTC.
- NCEI runups API (one call, tsunamiEventId=5942): HTTP 200, 1085 bytes, sha256 64268edc...c7ae, which is byte-identical to the saved scout file. totalItems 2:
  - LENAKEL, TANNA: 498 km from luga, 258 km from lifo.
  - PORT VILA, EFATE: 276 km from luga, 368 km from lifo.
  - There is no row for Luganville or Lifou.
- NCEI events API for 2024 (14 events): the only event within +/-1 day is 5942 (numRunups 2), plus an unrelated Whitehorse, Yukon entry. There is no duplicate record that could carry Lifou or Luganville rows.

**Job 2390 (extra.py)**
- Full rule (R > 5 and arrival within +/-10 min of ETA): DETECT for every sensor with both filters and both ETAs (luga 45.88/50.28, lifo 36.35/38.10).
- Same-clock-hour controls, 27 days each:
  - Zero full-rule detections on any sensor.
  - Max control R: luga 4.95 (A) or 5.01 (B, Dec 27, but its arrival is at +61, 10.7 min after ETA, so it is not a detection); lifo/prs 3.80-3.86; lifo/rad and lifo2 3.83-3.87.
- All-hours null (1238 origins), full-rule detections:
  - luga 1 (0.08%), with none reaching R 8.45 (max 6.41).
  - lifo/prs 3 (0.24%), all three with R >= 5.24 (max 5.39).
  - lifo/rad and lifo2 4 detections each, 3 of them with R >= 5.22-5.23 (max 5.64).
- Informative only (not the stated band): in a 5-120 min band the event stands out clearly against its controls.

| gauge/sensor | event R (5-120 min band) | control max |
|---|---|---|
| luga | 8.67 | 4.57 |
| lifo/prs | 8.06 | 4.84 |
| lifo/rad | 8.45 | 4.85 |
| lifo2 | 8.45 | 4.98 |

  So Lifou's slim margin in the 2-120 min band comes from short-period harbour noise in the denominator, not from a weak tsunami.

**Job 2387 (author's code/check_p1.py, run after mine)**
- luga: ETA 49.85, onset 2520 s, dt_arr -7.85, R 8.4375, DETECT True, 0 control detects (1 control day None).
- lifo: ETA 33.55, onset 2040 s, dt_arr +0.45, R 5.237, DETECT True, 0/12.
- lifo2: R 5.2273, DETECT True, 0/12.
- NCEI: 2 rows, nearest 258.3 km and 276.1 km.
- This matches REPRODUCE.md's expected output.

## Agreements with data/observations.csv

- R: luga 8.44 vs mine 8.45; lifo 5.24 vs 5.24; lifo2 5.23 vs 5.23.
- peak_m: 0.078 / 0.060 / 0.058 vs mine 0.0777 / 0.0605 / 0.0583.
- p2t_m: 0.136 / 0.101 / 0.100, which I match exactly.
- rms24_m: 0.0092 / 0.0116 / 0.0112 vs mine 0.0092 / 0.0115 / 0.0111 (method B gives 0.0116 / 0.0112).
- Onset: csv says 42.0 and 34.0 min after origin. Mine is the 02:30:00 and 02:22:00 raw samples, which are 42.6 and 34.6 min after origin, the same samples. Peaks fall on the same samples too.
- dt_arr is within +/-10 min under every ETA I computed: luga -2.9 to -7.3 min, lifo -1.6 to -3.5 min (csv: -7.6 and -1.2).
- Control-day absence: csv says 0 of 11 and 0 of 12; mine is 0 of 27 per sensor.
- NCEI has no runup row for either site, and the distances 276 km and 258 km are confirmed.

## Differences (none change the verdict)

- csv onset_utc and peak_utc carry a :26 s label. The author's 1-min bins start at the origin second, so 02:29:26 and 02:56:26 label the raw samples at 02:30:00 and 02:57:00. This is a sub-minute labelling offset.
- The model ETA depends on the solver and grid:
  - csv: luga 49.63, lifo 35.17.
  - author rerun: 49.85 and 33.55.
  - mine: 45.8-50.3 and 36.2-38.1.
  - All picks are still within +/-10 min.
- Null tests are not directly comparable: csv says lifo 2/400 and lifo2 0/400; my all-hours null gives 3/1238 for each. Both put the Lifou false-alarm rate at a few per thousand.
- "Two sensors at one site": lifo2 duplicates the lifo radar channel. The claim scores lifo on prs and lifo2 on rad, which are physically different instruments at one site, so Lifou counts as one gauge. p1 still has 2 gauges.
- Three control-window raw files appear in FETCHLOG but not in the package. They are not claimed objects, I verified them by re-fetch with matching hashes, and I re-derived all control days from my own download.

## Judgement

- **Luganville:** a clear tsunami train. R 8.4 with no control day close to it (max 5.0, all-hours max 6.4), arrival +42.6 min against an ETA of 46-50 min, and NCEI has no row. It meets the rule.
- **Lifou:** meets the stated rule, but with a small margin. R is 5.21-5.24 on the independent prs and rad sensors under two filter implementations. Arrival is +34.6 min against an ETA of 36-38 min. It beats all 27 same-hour control days (max 3.9 under the full rule). The all-hours false-alarm rate is 0.24%, and the 5-120 min band SNR of about 8 supports a genuine signal. NCEI has no row.

My independent checker reproduces every claimed observation. The p1 condition (2 gauges with amplitude and arrival, no NCEI runup row for them) holds.

pass: true
