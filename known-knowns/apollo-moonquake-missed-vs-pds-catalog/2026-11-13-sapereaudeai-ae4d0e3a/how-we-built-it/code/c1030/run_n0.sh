#!/bin/bash
# N0 (PREREG.md): rerun the 12-nest S14 + S16 lag-tolerant scan of 1973 with 400 shifts, one process, 1 FFT thread.
# Run from the run folder (a100_1030_claim_run_...). APOLLO_WF points at the waveform folder (sha256-checked).
PY=${PY:-python3}
export V3_WORKERS=1
nice -n 10 $PY -I -W ignore tools/code/scripts/run_capped.py tools/code/scripts/lagtol_scan_1416.py tools/frozen/nets25_1973.npz 1973 1 365 attempts/null-multiplicity/out/scan12_1973.jsonl 400 > attempts/null-multiplicity/out/scan12_run.out 2>&1
echo "N0_DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> attempts/null-multiplicity/out/scan12_run.out
