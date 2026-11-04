context: subagent (same VM)

# panel/criterion.md — Mo (mlearn_Mo_forces)

I read only files inside `panel-claim/Mo`. I ran the checks on a temp copy, using a python with the packages as interpreter only, with OMP_NUM_THREADS=1.

## Clause-by-clause verdict

1. **Strictly lower than the live best by at least 5%: met.**
   - `the-record-we-beat/snapshot.md` records the live page as fetched at 2026-10-19T22:52:53Z, HTTP 200. The best listed value is snap_mlearn at 0.18434104563832232, out of 7 entries.
   - I could not re-fetch the page. The snapshot stores only the page hash and the extracted cells, not the page itself. I accepted the snapshot as given.
   - `verify-it-yourself/check_predictions.py` returned PASS on a temp copy.
   - It recomputes the force MAE from the benchmark json: 0.097399761160953391 eV/A over 3567 components and 23 test ids.
   - The ids match the official test ids exactly. The MAE equals the `INDEX.csv` value.
   - The threshold is 0.95 × 0.18434 = 0.17512. The margin is 47.2%, far above the 5% requirement.

2. **Trained only on train/val ids, with no pretraining on data containing the test configurations: met, with one scope limit.**
   - `how-we-built-it/train_ids.txt` has 194 ids. It is identical to the benchmark's `train` list and disjoint from `test`.
   - `how-we-built-it/val_ids_used_for_selection.txt` has 19 ids, and I confirmed they are a subset of the train ids.
   - `mkxyz.py` builds val as every train structure at index i%10==5. There is no test input anywhere in selection.
   - `launch.sh` calls `mace_run_train` with a from-scratch MACE architecture. It has no foundation-model, `--multiheads_finetuning` or pretrained-checkpoint argument.
   - The training logs contain no pretrain or foundation strings. The loss starts near RMSE_F 439 meV/A at epoch 0, which is consistent with random initialisation.
   - The preregistration notes (`PREREG.md`, `PREREG.v2.md`) say the test split was scored once, after the val-only configuration choice.
   - The final training run used the val subset as its valid file while also training on it. That makes checkpoint selection in the final run optimistic about val. It does not touch test.
   - The mlearn structures in the test split come from the public mlearn dataset, which also holds the training structures. That is the standard setup for this task.
   - I cannot independently prove the absence of pretraining from the .model files alone. The evidence is the scripts, the logs and the absence of any pretrained-weight input.

3. **Re-running saved models reproduces the predictions to 1e-6 eV/A: met.**
   - `rerun_models.py` loaded the three .model files in float64 and averaged them. Against `object/predictions_Mo_forces_test.csv` it gave max |difference| = 2.398e-07 eV/A over 23 structures: PASS.
   - The sha256 hashes of the models, predictions and ensemble.json matched `expected_hashes.txt`.

4. **Comparison with Zuo et al. 2020 and later literature stated: met, but weakly.**
   - CLAIM.md cites Zuo et al. 2020 (arXiv 1906.08888). It says Zuo's errors appear only in its Figure 3, so no number is extracted. It also says Zuo uses its own split, so the numbers are not directly comparable.
   - The later paper is ALIGNN 2.0 (arXiv 2609.19487), which lists 0.1121 eV/A for mlearn-Mo force. CLAIM.md says that value is marked pending verification in the paper. Our 0.0974 is about 13% below it.
   - I could not check the completeness of the literature search or the ALIGNN 2.0 number. The clause asks that the comparison be stated, and it is. That clause does not require a quantitative Zuo number.

## Trivial baselines and seed spread

- The zero-force and train-mean-force baselines both give 0.9496, from `how-we-built-it/test_scores.json`. The claim is about 10 times better than that.
- The seed MAEs are 0.106269, 0.104097 and 0.106594, with sd 0.001358. Each single seed (worst 0.1066) already beats the 5% threshold of 0.1751 by a wide margin. The ensemble claim is therefore not a selected best-of-N.
- The only prior test-set use is the single scoring recorded in the preregistration. No hidden quantifier is evident.

## Residual doubts

- The live-page value rests on the snapshot only.
- The ALIGNN 2.0 figure is unverified.
- The win is on one element, Mo, with 23 test structures.
- The margin is large enough that none of these doubts changes the verdict.

confirmed_scope: A 3-seed ensemble of from-scratch MACE models (32 channels, r_max 4.5, trained on the 194 official train ids, seeds 1 to 3) gets a force MAE of 0.097400 eV/A on the 23 official mlearn_Mo_forces test ids. This is 47.2% below the 0.184341 best listed in the snapshot (fetched 2026-10-19T22:52:53Z). Re-running the saved models reproduces the predictions to 2.4e-7 eV/A. This covers only mlearn Mo forces, and it is not a verified comparison against the numeric results of Zuo et al. 2020 or of any other literature.

pass: true
