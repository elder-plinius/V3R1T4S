# Run it yourself

## Quick check (under a second, Python 3 standard library, no network)
From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (verify-it-yourself/RECEIPTS.md has the full output). It checks the sha256 of every file in
object/ and sensitivity-v5/; re-derives every code's DETECTS / PASSES / UNDECIDED flags and every quake's class at the
real and both fake origins from the per-sensor results in object/quakes/ (plus object/v4_ctrl_refetch.json for 13
codes), under the v4 rules for the headline map object/map.csv and under the PREREG.v5 rules for
sensitivity-v5/map.csv; re-derives LISTED and the NCEI ids from how-we-built-it/ncei_2026-11-07/; checks the IOC
request list how-we-built-it/ioc_requests.csv against the quakes (one stage-1 row per gauge with its ETA, a stage-2 row
per v4 control-day window, every response a line of ioc_windows_1/2.tsv with that sha256); and recomputes the headline,
Wilson interval, bounds over 264, the SIGNAL x LISTED counts, the fake-origin rate and a deterministic worst case of the
fake-catalog null for both maps. It cannot recompute r, arrivals or control days without the raw IOC series.

Other offline scripts, from this folder:

    python3 how-we-built-it/code/summarize_v4_from_map.py    # object/map_summary.txt and object/null.json (needs numpy)
    python3 how-we-built-it/code/relist_ncei.py              # LISTED against the 2026-11-07 NCEI pages (standard library)
    python3 how-we-built-it/code/list_ioc_requests.py        # how-we-built-it/ioc_requests.csv (standard library)

## Without our code
how-we-built-it/ioc_requests.csv gives, for every quake and gauge code in scope, the model arrival time (ETA, minutes
after the origin), the tied sensors and the sensor the v4 rules score, and each UTC window read: stage 1
[floor_h(o-31 h), ceil_h(o+7 h)] for the real and both fake origins, and stage 2 (control days, days -7..-1 and +2..+8)
[floor_h(oo-8 d-1 h), ceil_h(oo+9 d)] for each origin where the scored sensor detects. Each IOC response is named by
its line in ioc_windows_1.tsv or _2.tsv (URL, UTC fetch time, HTTP status, sha256 of the raw JSON). Requests are
`https://www.ioc-sealevelmonitoring.org/service.php?query=data&code=CODE&timestart=...&timestop=...&format=json`; a
response holds every sensor of the station. object/quakes/ has the code's coordinates, snapped water cell, site
grouping (codes within 2 km), and the per-sensor coverage, r, peak, RMS24, arrival and control-day r. IOC may have
revised data since 2026-10-24, so compare each response by sha256 first; the 39 re-fetched on 2026-11-07 with an
original URL were unchanged (how-we-built-it/refetch_2026-11-07.tsv).

## Full rebuild (about 1.4 GB of downloads, 30-60 min)
Python 3.11 with how-we-built-it/requirements.txt. Lay out how-we-built-it/code/ as a run folder (it already is:
lib/, attempts/, code/). Fetch the inputs into data/ under the paths listed in how-we-built-it/inputs.tsv (URL, sha256;
ETOPO1 slabs from NCEI THREDDS, ComCat CSV, IOC station list, NCEI events and per-event tide-gauge rows), then:

    python -c "import sys; sys.path.insert(0, 'lib'); import tt; tt.build_npy()"   # ETOPO1 2-arcmin grid
    # the headline map (v4 rules, PREREG.v6 corrections, det.IMPL6 = True)
    python -W ignore attempts/completeness-map-v6/code/p3_map_v6.py v4 0 1
    V3_MAPOUT=$PWD/attempts/completeness-map-v6/out_v4rules python -W ignore attempts/completeness-map/code/summarize_map.py
    # the sensitivity map (post-hoc PREREG.v5 rules, same corrections)
    python -W ignore attempts/completeness-map-v6/code/p3_map_v6.py v5 0 1
    python -W ignore attempts/completeness-map-v6/code/summarize_v6.py
    V3_MAPOUT=$PWD/attempts/completeness-map-v6/out python attempts/completeness-map-v5/code/no_overlap.py
    # as-run maps (det.IMPL6 = False), for the comparisons the summaries print
    python -W ignore attempts/completeness-map/code/p3_map.py 0 1 && python -W ignore attempts/completeness-map/code/summarize_map.py
    python -W ignore attempts/completeness-map-v5/code/p3_map_v5.py 0 1 && python -W ignore attempts/completeness-map-v5/code/summarize_v5.py

The map code fetches IOC SLSMF windows itself (one GET each, stopping on 401/403/429/503); the PREREG.v4 data access
composes a window from saved windows of the same code where they cover it, which is why ioc_requests.csv can list
more than one response per window. Compare attempts/completeness-map-v6/out_v4rules/map.csv with object/map.csv and
attempts/completeness-map-v6/out/map.csv with sensitivity-v5/map.csv.

## Re-fetch check of 2026-11-07
    python how-we-built-it/code/recheck_refetch.py RUN .

with RUN a copy of how-we-built-it/code/ (needs numpy, pandas, scipy). It fetches the 107 windows listed in
how-we-built-it/refetch_2026-11-07.tsv (sequentially, 1 s apart, stopping on 401/403/429/503), recomputes stage 1 for
the 94 codes in how-we-built-it/refetch_stage1_check.tsv and the v4 control days in object/v4_ctrl_refetch.json.
