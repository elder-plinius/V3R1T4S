# Run it yourself

## Quick check (seconds, Python 3 standard library only)

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (set PYTHON if `python3` is not on PATH). It checks the object's sha256, that the 31
published values are recorded, that stage S2 is within 1% everywhere (28 cells to < 1e-9, the three Epiforecasts
cells below 2e-4), that S0 and S1 each leave 6 cells outside 1% or undefined, and the WIS identity.

## Full rebuild from the public files (about 15 minutes, mostly polite downloads; Python 3.11 with numpy and pandas)

From an empty folder that holds a copy of `how-we-built-it/` (paths below are relative to that folder):

    mkdir -p run/data && cp -r how-we-built-it/code run/ && cp -r how-we-built-it/fetch_lists run/
    cd run
    python -I code/fetch_hub.py fetch_lists/eval_fetch_list.tsv data data/eval_fetch_log.tsv 2
    python -I code/fetch_hub.py fetch_lists/hub_fetch_list.tsv data/hub data/hub_fetch_log.tsv 2
    python -I code/wis_selftest.py
    python -I code/p3_reproduce.py . out
    python -I code/frozen_baseline_check.py . out/frozen_baseline_check.txt
    python -I code/rederive_exclusions.py . out/rederive_exclusions.txt

Expected (copied from the run's own output, how-we-built-it/outputs/):
- `SELFTEST PASS`
- `truth check: published rows 57596 hub-recomputed rows 57596 in both 57596 ... max |diff| on common 0.0`
- `== S0: cells 31, within 1%: 25`, `== S1: cells 31, within 1%: 25`, `== S2: cells 31, within 1%: 31, max |rel diff| 1.031e-04`
  and `out/p3_ladder.csv` byte-identical to `object/p3_reproduction_table.csv` (sha256 0d068173...83ee4)
- `baseline targets 106053; equal to raw-truncation 7-day sums: 106053; differ: 0`
- `Epiforecasts: re-derived missing 696, released list 696, equal sets: True` (and the same for MeanEnsemble 368,
  MedianEnsemble 368, SZ 3312)

Optional provenance of the evaluation's assembly against every hub file the released loader reads (1,404 more files,
about 35 minutes at a polite rate):

    python -I code/fetch_hub.py fetch_lists/hub_fetch_list_full.tsv data/hub data/hub_fetch_log_full.tsv 1.2
    python -I code/p3_provenance.py . out _full

Expected: `files_checked=1593 hub_rows=7592953 key_mismatches=0 value_mismatches=0 files_with_any_difference=0`.

`p3_reproduce.py` peaks at about 1 GB of memory. The fetcher sends one request per file with a User-Agent naming
V3R1T4S, does not retry, and stops on 401/403/429/503.
