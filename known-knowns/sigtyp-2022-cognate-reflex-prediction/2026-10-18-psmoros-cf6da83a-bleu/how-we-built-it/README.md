# How we built it (cell L50, proportion 0.50, mean BLEU)

Stage-2 entries (frozen component systems; every entry's string is a candidate in the per-item choice, weight-0 entries included):
- broker/PRIMARY (weight 1 at 0.50)
- classifier/SECONDARY (weight 2 at 0.50)
- broker/SECONDARY (weight 3 at 0.50)
- r0202-broker/PRIMARY (weight 2 at 0.50); frozen in run 2026-10-18-0202 and carried (CARRIED.md)
- classifier/PRIMARY (weight 2 at 0.50)
- analogist/PRIMARY (weight 1 at 0.50)
- phylo/PRIMARY (weight 0 at 0.50)
- r0202-analogist/SECONDARY (weight 2 at 0.50); frozen in run 2026-10-18-0202 and carried (CARRIED.md)

- entries/LENS/ROLE/code/ (sealed_check.py itself is not included; its logs are): each entry's frozen code (system.py with `train --manifest M --model-dir D` and `predict --model-dir D --family F --jobs J`); entries/LENS/FROZEN.md: the freeze records (sha256 of every code and result file). Entries named r0202-LENS were frozen in run 2026-10-18-0202 (same val-0.50-only protocol) and carried; their CARRIED.md lists the sha256 of the test-0.50 result files made in this run (carry_setup.out: the code-hash check of the carry).
- tools/q15h.py: the harness (training manifest = the 10 surprise training-0.50.tsv files plus the development families; prediction one masked-language partition at a time). tools/stage2.py: the per-item minimum-Bayes-risk combiner (weights in combiner/combiner_fit.json, "0.50", "weights_all10"). tools/make_object.py writes object/ from the result files.
- PREREG.md (frozen before any lens of the session started), selection.md (candidate fixed before any test gold was read), null_test.md (400 paired-permutation controls against FeVeT's predictions), the sealed_check logs (every entry retrained in a sandbox and every test partition predicted alone in its own process, byte-identical).
Paths in these files that began with the workspace folder read WORKDIR.
