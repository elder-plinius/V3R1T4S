# How it was built

GPU self-avoiding-walk search in the skew-symmetric subspace, s[200+j] = (-1)^j s[200-j]: kernel `skew_saw` in
`code/skew_kernels.cu`, host code `code/labsgpu.py`, driver `code/search.py`. Walks run inside head run-length
restriction classes (the first three runs fixed, r1 25-29, r2 12-14, r3 9-11), with memetic recombination of the walks'
own results and 50% random restarts. Every walk starts from a random sequence; no published or constructed sequence is
ever used as a seed. Pre-registered in `PREREG.v4.md` (L = 401) and `PREREG.v5.md` (budget change before any L = 401 output).
`code/run_pass3b.sh` is the exact command (seed 3401). The sequence appeared after 130.345 s, at walk generation
1086; `search_log_L401.jsonl` is the improvement trajectory as written by the run. Hardware: one NVIDIA GeForce
RTX 5090 Laptop GPU. Requirements: `requirements.txt` (a virtual environment). Kernel tests: `SMOKE.md`.

The search is stochastic and GPU timing-dependent, so a rerun finds different sequences. The object, not the search, is
the claim. Comparison values: `code/parse_dimitrov.py`, `code/parse_hex_table.py`, `code/read_erk2025_fig2.py`,
`code/parse_erk2025.py`. Trivial-derivation frontier: `code/derivation_bar.py`, `code/deep_derivations.py`. The run's
errata, all disclosed, are in `ERRATA.md`. Paths to the run's machine were replaced by plain words.
