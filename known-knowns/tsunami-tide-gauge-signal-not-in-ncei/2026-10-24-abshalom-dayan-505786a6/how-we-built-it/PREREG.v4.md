# PREREG.v4: data access and budget stop for the p3 map (no scoring change)

Frozen before the map summary was computed. Amends PREREG.md section 6 (budget) only; sections 0-5, PREREG.v2 and
PREREG.v3 are unchanged.

## Why
At 2026-10-24T19:52:40Z the map had 114 of 264 quake files, 567,396,116 logged bytes since the map started and
992,589,691 logged bytes for the run (fetch_log.tsv column 5). A linear projection reaches about 1.74 GB, close to the
2 GB cap in NEXT_RUN.md. Most map bytes are the 17-day stage-2 windows (stage 2 at 19:46Z: 127 fetches, 292 MB;
stage 1: 808 fetches, 110 MB).

## Data access (lib/det.py ioc_raw)
- An exact cached window (this run or runs 2026-10-24-0850 / -1501) is used as before.
- Otherwise, if saved windows of the same IOC code cover >= 25 % of the requested window with at most 3 uncovered
  gaps, the rows come from those files plus one honest GET per gap, cut to [t0, t1] by sample time. Otherwise one GET
  of the whole window, as before.
- Check before use: for anto2 and buca2 over [2015-09-09 03:00, 2015-09-26 05:00] the composed rows and the 1-min
  series are identical to the exact cached window (49172 and 48914 rows; series equal).
- This changes which bytes are downloaded, not the data or any rule.

## Budget stop
- code/budget_watch.sh stops the map shards (by recorded PID) when logged bytes exceed 2,040,109,465 (1.9 GB).
- Quakes without a file at that point are NOT_PROCESSED: listed in map.csv, excluded from the USABLE headline,
  counted as unknown in the bounds over 264, and named in the report. Processing order is unchanged (time order).

## Already seen before this file
- The shard logs print each processed quake's real/fake classes (114 quakes). No summary, fraction, crosstab or null
  was computed or read.
