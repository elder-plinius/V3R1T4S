# Box reproduction (packaging machine, 2026-11-24 ET)

Machine: 8 vCPU, 16 GB RAM Linux VM, all jobs under nice -n 19, one at a time. Encoder: ../code/py (unchanged).
CaDiCaL 3.0.1 and drat-trim built from the run kit's third_party sources (identical to the kit shipped to the PC).

- regen_cnf.py: rebuilt the M-X problem.cnf for every k = 2..20 and compared its sha256 with the PC list
  (../../object/SHA256SUMS-files.txt): 19 of 19 equal (regen_cnf_k2-20.jsonl).
- solve_small.py (k = 2..12) and solve_big.py (k = 13..20; writes the CNF in a separate process to keep RAM low):
  rebuilt the CNF, ran `cadical problem.cnf proof.drat`, then `drat-trim problem.cnf proof.drat -t 20000`, and
  compared both sha256s with the PC list. All 19: UNSATISFIABLE, s VERIFIED, CNF and proof sha256 equal to the
  PC files (SUMMARY.tsv; per-k JSON lines in solve_k2-12.jsonl and solve_k13-20.jsonl).
- Because the proofs are byte-identical, the 19 proofs in the archive are exactly the ones drat-trim accepted here.
- Peak memory per step (ru_maxrss): CaDiCaL up to about 3.0 GB (k = 19 and 20), drat-trim up to about 1.4 GB, CNF
  generation up to about 1.7 GB (in solve_big.py) and about 2 GB or more in regen_cnf.py (one process for all k; about 1.95 GB seen near k = 15, not measured at k = 20).
