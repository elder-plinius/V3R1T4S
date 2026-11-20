# RUN_IT_YOURSELF.md — BORDA-12 (2026-11-19)

Exact commands that verify the BORDA-12 claim in a fresh shell, from this
package folder. Python 3 (standard library only for the checker; the
rebuild needs pandas/scipy/numpy).

## 1. Verify the score file against the reference (the claim number)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a minute on a laptop. The checker
(verify-it-yourself/verify_borda12.py, Python standard library only)
checks the object file's sha256 against INDEX.csv, decompresses the
bundled ProteinGym reference (verify-it-yourself/reference_Matreyek_2021.csv.gz,
sha256 1c52aba95950c6d3b1ac8320df4cb99a79ae97353bd43e24c87ef78dbb02e636),
verifies the exact 5,083-mutant match with no duplicates and no NaNs,
and recomputes the Spearman (0.5682) against the 0.531 bar from
the-record-we-beat/RECORD.md. A corrupted copy of the object fails:
change one digit in object/score_borda12.csv and re-run — the last line
becomes `FAIL`.

## 2. Rebuild the score file end-to-end

The build code is in how-we-built-it/. It was run from the V3R1T4S
workspace run folder, where the fetched assay files and the reference
already live; the packaged copy is a faithful record of that code. To
rebuild exactly as the run did:

1. Fetch the two published assay score files from Zenodo record 15293562
   (https://zenodo.org/records/15293562/files/zero_shot_substitutions_scores.zip,
   1,911,045,703 bytes total) by HTTP range request — only the two assay
   entries, using how-we-built-it/fetch_scores.py (it parses the zip's
   central directory from the tail; one honest GET per range, User-Agent
   names V3R1T4S). Expected sha256: PTEN_HUMAN_Matreyek_2021.csv
   d1a3f2670ae9d111d5cfb59fb6c73589d60518a5f8572925c85fee418d45a153,
   PTEN_HUMAN_Mighell_2018.csv
   a951c5a25e7fd067ae0ca16ddaca4873153aeb71efb46f93b3a7eaab3813a822.
2. Place the Matreyek reference CSV (ProteinGym v1.3, sha256 as above)
   and the fetched assay files in the run folder's data/ layout, then run
   how-we-built-it/build_borda12.py with Python 3.12 + pandas/scipy/numpy.
   It re-runs gates G1 (checker fixtures 1.0 PASS / -1.0 FAIL), G2 (E2
   reproduction 0.3666) and G3 (label-free member check), and writes
   score_borda12.csv.
3. Verify the rebuild: `cmp` against object/score_borda12.csv is clean
   (the author's rebuild is byte-identical); sha256
   fe21f86cd41c75ce321ba511dfcdbe23888e12e1445eec27ba9e2d98ee942350.
   An independent recompute from the definition in how-we-built-it/PREREG.md
   must match rho to within 1e-6 (the run's independent recompute gave
   0.5682426644 vs the claimed 0.5682423873).

Known limitation, recorded by the REPRODUCE skeptic and fixed before
submission: as packaged at gate time, build_borda12.py resolved its run
folder as parents[3] of its own path, so run from inside this package it
landed one level too high and failed with FileNotFoundError. On
2026-11-19, after the gate and with the human's approval, the packaged
copy was replaced with a version whose only change is path resolution
(--run-dir or $V3R1T4S_RUN_DIR first, otherwise an ancestor that
actually holds the data file); the scoring logic is unchanged, and the
replaced copy was verified from its packaged location to reproduce
object/score_borda12.csv byte-identically (sha256
fe21f86cd41c75ce321ba511dfcdbe23888e12e1445eec27ba9e2d98ee942350).
The panel files are unchanged and describe the defect as found. The
numbers are unaffected.

## 3. The null test and the bootstrap

how-we-built-it/null_test.md: 400 permutations (seed 20261119), best
control 0.0398 vs real 0.5682, real beats all controls: yes. Re-run with
how-we-built-it/diagnostics.py (D5 section). The bootstrap 95% CI for
BORDA-12 is [0.5486, 0.5886] (1,000 samples, seed 20261119); the
BORDA-12-minus-M1 CI is [-0.0172, +0.0228] — the margin over M1 is
inside noise, and the claim says so in README.md ("Not claimed").

## 4. The novelty bar

M1, disclosed in V3R1T4S PR #467 (open) and #463 (closed/unmerged),
scores 0.5658 on the same assay. BORDA-12 0.5682 is 0.0024 ABOVE it.
Mighell does not replicate (BORDA-12 0.5723 vs Mighell bar 0.576), so
no multi-assay claim is made; the claim is Matreyek-only.
