controls: 400
best_control: 21.103452698344363
real: 130.01362711367162
real_beats_all_controls: yes
command: cd [workspace]/runs/2026-10-15-1739/attempts/calibrator-v3/a2 && OMP_NUM_THREADS=1 [workspace]/venv/bin/python -I code/run_many.py out/var.jsonl 3 data/lc_var/*.json && OMP_NUM_THREADS=1 [workspace]/venv/bin/python -I code/run_many.py out/cst.jsonl 3 data/lc_cst/*.json && OMP_NUM_THREADS=1 [workspace]/venv/bin/python -I code/run_many.py out/gaia.jsonl 3 data/lc_gaia/*.json && [workspace]/venv/bin/python -I code/decide.py
