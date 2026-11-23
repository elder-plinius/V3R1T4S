# Commands that produced this object

The 15-glider RLE was composed on 2026-11-15 by a harvest script that injects already-verified cheaper seed
syntheses into Shinjuku's component graph, runs Dijkstra, and stitches a full all-glider pattern. The script in
how-we-built-it/code/harvest.py is that program with machine-absolute paths removed: it reads GLIDER_RUN (the earlier
seed harvest, with a Shinjuku checkout at data/Shinjuku, the verifier at code/verify_synthesis.py, and the verified
seed index at attempts/verified/INDEX.tsv) and HARVEST_RUN (the folder that receives INDEX.tsv and the RLEs) from the
environment. Shinjuku commit used: 3615babf001146507a1e9ec901cb3eabba9f5fd0 (2026-10-27).

```
export GLIDER_RUN=/path/to/glider-run
export HARVEST_RUN=/path/to/harvest-run
python3 -c "import lifelib,shinjuku"   # both must import
# targets file: one apgcode per line; this object is xs28_08ehlmggoz6a87066
ulimit -v 4000000
nice -n 19 python3 how-we-built-it/code/harvest.py --targets /path/to/targets.txt --deadline <epoch> --sleep 2
```

The script skips objects already marked VERIFIED in HARVEST_RUN/INDEX.tsv. Each composed RLE is checked with
how-we-built-it/code/verify_synthesis.py (lifelib + Shinjuku rewind) and a live Catagolue object-page fetch.

This packaging run did not re-run the harvest. It re-checked the already-built RLE with the standard-library checker
verify-it-yourself/life_check.py (no lifelib, no Shinjuku, no network) against a fresh live Catagolue cost, and it
kept the RLE byte-identical.
