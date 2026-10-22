# How we built it (cell C30, proportion 0.30)

Stage-2 entries (frozen component systems; every entry's string is a candidate in the per-item choice, weight-0 entries included):
- broker/PRIMARY (weight 2 at 0.30)
- analogist/SECONDARY (weight 2 at 0.30)
- broker/SECONDARY (weight 0 at 0.30)
- phylo/PRIMARY (weight 3 at 0.30)
- analogist/PRIMARY (weight 0 at 0.30)
- classifier/PRIMARY (weight 3 at 0.30)

- entries/LENS/ROLE/code/ (sealed_check.py itself is not included; its logs are): each entry's frozen code (system.py with `train --manifest M --model-dir D` and `predict --model-dir D --family F --jobs J`); entries/LENS/FROZEN.md: the freeze records (sha256 of every code and result file).
- tools/q15h.py: the harness (training manifest = the 10 surprise training-0.30.tsv files plus the development families; prediction one masked-language partition at a time). tools/stage2.py: the per-item minimum-Bayes-risk combiner (weights in combiner/combiner_fit.json, "0.30", "weights_all10"). tools/make_object.py writes object/ from the combiner's result files.
- PREREG.md (frozen 2026-10-18T02:09:41Z, before any system existed), selection.md (candidate fixed before any test gold was read), null_test.md (400 paired-permutation controls), sealed_check_0.30.log and sealed2_check_0.30.log (every entry retrained in a sandbox and every test partition predicted alone in its own process, byte-identical).
Paths in these files that began with the workspace folder read WORKDIR.
