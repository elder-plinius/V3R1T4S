# Null test (PREREG design), candidate NCEI 5942 (p1), job 2359

controls: 400
best_control: 0.0
real: 5.227294806741084
real_beats_all_controls: yes
command: python3 agent_gate.py job submit tsunami-tide-gauge-signal-not-in-ncei SESSION runs/<RUN> attempts/p1-gauge-rows --queue short --env sci-torch --mem 1G -- python3 code/null.py input/p1_candidates.json

Statistic S = min over claimed gauges (luga, lifo, lifo2) of R_g, R_g = R if the onset lies within +/-10 min of the
model ETA, else 0. Control origin times uniform in [t0-60 d, t0+60 d], |t-t0| >= 2 d, seed 20261023; 586 draws to get
400 controls passing QC (job 2359 output: "controls": 400, "draws": 586, "best_control": 0.0, "n_ge_real": 0).
Per-gauge view (job 2371): luga max control R 4.206, 0/400 >= real 8.437; lifo max control R 6.686, 2/400 >= real
5.237; lifo2 max control R 4.426, 0/400 >= real 5.227.
Look-elsewhere context: the p1 sweep screened 36 NCEI earthquake events (2024-2026) and up to 40 IOC stations each
(job 2287); this was the only stage-3 survivor.
