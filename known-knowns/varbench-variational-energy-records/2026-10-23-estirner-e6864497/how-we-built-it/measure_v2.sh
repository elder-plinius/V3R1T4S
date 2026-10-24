#!/bin/bash
# PREREG.v2 measurements on candidate 1 (run folder 2026-10-22-1610, ckpt/r10_J0.9_B1.pt, step 648), in order:
# S1 plain seed 31337 (screening / second re-estimate), S3 DIS seed 2718, S2 plain seed 4242 with N_eff from S3's Var(H).
set -u
W=$WORKDIR; PY=$W/storage/venvs/physics-r2/bin/python
D=$(dirname "$(readlink -f "$0")"); O=$(readlink -f "$D/../out")
CK=$W/storage/runs/2026-10-22-1610/attempts/representation-transfer/ckpt/r10_J0.9_B1.pt
NQ=$W/storage/runs/2026-10-23-1501/attempts/representation-transfer/code
L="--chains 2048 --therm 50 --gap 2 --min_rounds 50 --max_rounds 400 --neff 100000"
$PY "$D/estimator2.py" "$CK" --nqs_dir "$NQ" --mode plain --seed 31337 $L --out "$O/S1_plain_31337" > "$O/S1.stdout" 2>&1
$PY "$D/estimator2.py" "$CK" --nqs_dir "$NQ" --mode dis --seed 2718 $L --out "$O/S3_dis_2718" > "$O/S3.stdout" 2>&1
V=$($PY -c "import json;print(json.load(open('$O/S3_dis_2718.json'))['result']['varH'])")
$PY "$D/estimator2.py" "$CK" --nqs_dir "$NQ" --mode plain --seed 4242 $L --varH "$V" --out "$O/S2_plain_4242" > "$O/S2.stdout" 2>&1
echo "$(date -u +%FT%TZ) measure_v2 done" >> "$O/measure_v2.log"
