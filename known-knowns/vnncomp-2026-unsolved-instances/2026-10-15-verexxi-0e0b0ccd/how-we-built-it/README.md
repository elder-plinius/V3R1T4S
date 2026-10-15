# How we built it (search code, exact commands)

The files mirror the run's layout (attempts/exact-solver/code/, attempts/surrogate-attack/code/, attempts/evaluator-first-local-search/code/); `tools/hunt_seeds.py` expects the benchmark files in
`runs/2026-10-14-1953/data/{onnx,vnnlib,SCORING}` relative to the repository root it sits in (one level above
`tools/`). Requirements: requirements.txt. DATA below is that data folder.

1. Exact model check: `python -I attempts/exact-solver/code/validate_model.py DATA` (validate_model.out: max logit
   difference to onnxruntime 0.0 at 21 points in each of 7 boxes).
2. Basin hopping (surrogate PGD 45 s -> exact local search 55 s per seed): `python tools/hunt_seeds.py --start 3000
   --end 3001` (seed 3001 gave the G = -2 local optimum that led to the witness; CPU-thread timing makes reruns
   non-deterministic).
3. Which dense units vary across good optima: `python -I attempts/evaluator-first-local-search/code/ceiling.py`
   (ceiling.out).
4. Focused local search from the seed-3001 optimum on dense unit 109 (worker "B109"):
   `python -I attempts/evaluator-first-local-search/code/localsearch.py --data DATA --inst model_48_idx_6371_eps_3
   --secs 1500 --cls 9 --beta 3,3,3,3 --hard 0,0,0,0 --mu 0.05 --focus 0 --kick 30 --stall 80
   --init SEED3001_CKPT (the seed-3001 local-search checkpoint from step 2) --focus-unit 109 --mu2 0.3 --seed 502 --out OUT`
   (reached G = +2 after 265 s; its checkpoint is ckpt_model_48_idx_6371_eps_3_G2.json here).
5. Witness files from the checkpoint: `python -I attempts/exact-solver/code/validate_hit.py --data DATA --inst
   model_48_idx_6371_eps_3 --ckpt ckpt_model_48_idx_6371_eps_3_G2.json --out OUT` (x = v + off + m*d, pw = 9).
PREREG.md is the run's pre-registration (written before any attack output was scored).
