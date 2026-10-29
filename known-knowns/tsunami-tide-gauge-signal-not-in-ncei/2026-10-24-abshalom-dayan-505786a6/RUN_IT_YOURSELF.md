# Run it yourself

## Quick check (under a second, Python 3 standard library, no network)
From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (verify-it-yourself/RECEIPTS.md has the full output). It checks the sha256 of every file in
object/, re-derives every code's DETECTS / PASSES / UNDECIDED flags and every quake's class at the real and both fake
origins from the per-sensor results in object/quakes/ under PREREG.v5, checks map.csv against them, and recomputes the
headline, Wilson interval, bounds over 264, the SIGNAL x LISTED counts, the fake-origin rate and a deterministic worst
case of the fake-catalogue null. It cannot recompute r, arrivals or control days without the raw IOC series.

## Full rebuild (about 1.2 GB of downloads, 30-60 min)
Python 3.11 with how-we-built-it/requirements.txt. Lay out how-we-built-it/code/ as a run folder (it already is:
lib/, attempts/, code/). Fetch the inputs into data/ under the paths listed in how-we-built-it/inputs.tsv (URL, sha256;
ETOPO1 slabs from NCEI THREDDS, ComCat CSV, IOC station list, NCEI events and per-event tide-gauge rows), then:

    python -c "import sys; sys.path.insert(0, 'lib'); import tt; tt.build_npy()"   # ETOPO1 2-arcmin grid
    # as-run maps (det.IMPL6 = False), needed for the comparisons the summaries print
    python -W ignore attempts/completeness-map/code/p3_map.py 0 1 && python -W ignore attempts/completeness-map/code/summarize_map.py
    python -W ignore attempts/completeness-map-v5/code/p3_map_v5.py 0 1 && python -W ignore attempts/completeness-map-v5/code/summarize_v5.py
    # the published maps (PREREG.v6 corrections, det.IMPL6 = True)
    python -W ignore attempts/completeness-map-v6/code/p3_map_v6.py v4 0 1
    V3_MAPOUT=$PWD/attempts/completeness-map-v6/out_v4rules python -W ignore attempts/completeness-map/code/summarize_map.py
    python -W ignore attempts/completeness-map-v6/code/p3_map_v6.py v5 0 1
    python -W ignore attempts/completeness-map-v6/code/summarize_v6.py
    V3_MAPOUT=$PWD/attempts/completeness-map-v6/out python attempts/completeness-map-v5/code/no_overlap.py

The map code fetches IOC SLSMF windows itself (one honest GET each, stopping on 401/403/429/503). The windows it used,
with fetch times and the sha256 of each raw JSON, are in how-we-built-it/ioc_windows_1.tsv and _2.tsv; IOC may have
revised data since, so compare by sha256 first. Compare attempts/completeness-map-v6/out/map.csv with object/map.csv.
