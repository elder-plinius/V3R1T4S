# panel/reproduce.md

context: subagent (same VM)

Scope: I read only files in the Mo claim folder and fetched the URLs it names. I ran code in a temp copy and wrote nothing into the claim folder. Before reading any author code, I wrote my own checker from the CLAIM.md definition. The one script I did read was `verify-it-yourself/run_checks.sh`, and only to run it, after my own check.

## 1. Own checker (written from the definition)

Definition used, quoted from CLAIM.md: the force MAE "on the leaderboard's official test split, recomputed by the checker from the benchmark json" must be "STRICTLY LOWER (direction: min) than the best MAE listed on that task's live leaderboard page ... by at least 5% relative". The model must be "trained only on the train (and val) ids". "re-running the saved model ... reproduces the predictions file to 1e-6 eV/A". The literature comparison must be stated.

The checker is my own `mychk.py` in a temp directory. It reads `mlearn_Mo_forces.json` from `inputs/benchmark.json.zip` and `object/predictions_Mo_forces_test.csv`. Output:

```
ids equal True 23 23
n comps 3567 MAE 0.09739976116095339
rel improvement 0.4716328052513491 thresh 0.1751239933564062
zero baseline 0.9496075845472385
train ids 194 194 == json train True overlap with test set()
sha faa29c3a164dca21d19a0d7221aacf5932e75f51712e87d5af69f4562e200cc7
nan False
```

- **MAE:** the recomputed value is 0.09739976116095339, which matches the claimed 0.097400 and the `INDEX.csv` value. It covers all 23 test ids and all 3567 force components, with shapes matching and no NaN.
- **Margin:** the improvement is 47.16%, rounded to 47.2% in the claim. The 5% threshold is 0.17512, so the claim clears it.
- **Zero-force baseline:** 0.9496, which matches the claim.
- **Training ids:** `how-we-built-it/train_ids.txt` has 194 unique ids, equal as a set to the benchmark json "train" keys. Its overlap with the 23 official test ids is the empty set, so none of the official test ids appear in it. The claim says "train-mean-force 0.9496" as well; I only recomputed the zero-force baseline.
- **Benchmark provenance:** I re-fetched the upstream zip from the raw GitHub URL named in `sources.json`. Its sha256 is `71f06783...f6c3`, identical to `inputs/benchmark.json.zip`, and the extracted json is byte-identical (`cmp`: JSON_SAME_AS_UPSTREAM).
- **Live leaderboard:** I fetched https://pages.nist.gov/jarvis_leaderboard/AI/MLFF/mlearn_Mo_forces/. The minimum is snap_mlearn at 0.1843, second is alignnff_mlearn_all_wt1 at 0.1853, then matgl_pretrained at 0.3181. This matches the claimed best of 0.18434.

## 2. Package checker and model re-run

I ran `sh verify-it-yourself/run_checks.sh` on a temp copy, with the cached input zips copied in and `MLFF_PYTHON` pointed at a python with the packages, `OMP_NUM_THREADS=1`. It took 32 s. Excerpts:

```
components 3567  force MAE 0.097399761160953391 eV/A
ok   MAE equals INDEX.csv value 0.09739976116095339
ok   MAE 0.097400 <= 0.95 * listed best 0.18434104563832232 (= 0.175124): improvement 47.2%
ok   training ids used == benchmark train ids (194)
ok   no test id in the training list
ok   mlearn_figshare.zip f731b3ad...8a28
max |re-run - predictions file| = 2.398e-07 eV/A over 23 test structures
PASS
```

The re-run of the three saved MACE models (float64 inference) differs from the predictions file by at most 2.4e-7 eV/A, under the 1e-6 limit.

## 3. Remaining criterion items

- **Zuo et al. 2020 / later paper:** CLAIM.md states the comparison. Zuo's errors are only in a figure and use its own split. The later paper, ALIGNN 2.0 (arXiv 2609.19487), lists 0.1121 eV/A, which is higher than 0.0974. I did not independently fetch that paper or run a literature search of my own, so the "any later paper with a lower force MAE" requirement is not verified by me. This gap is not enough on its own to fail the claim, since the package states the comparison as the criterion asks.
- **From scratch:** the claim says "no pretrained weights"; I have only the author's statement for this. The training logs are in the package, and I did not audit the training code or the logs for pretraining.
- **Determinism:** a single re-run gave 2.4e-7 against the 1e-6 limit. I did not repeat the re-run, so run-to-run determinism is not separately confirmed.

No mismatches, missing objects or non-determinism found. The checks were exhaustive over all 23 ids and 3567 components, not sampled.

pass: true
