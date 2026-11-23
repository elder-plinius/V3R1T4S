# Next-coda prediction on the whale dialogue benchmark

## What

On the pinned sperm-whale-dialogues.csv benchmark, the preregistered training-fold-selected categorical pipeline scored 2.564371 bits per coda over 3,418 positions versus 2.794781 for R1 and 2.850952 for its retrained one-coda twin, with a fresh paired recording-bootstrap 95% interval of 0.241386 to 0.345250 bits for the gain over the twin.

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh`. This verifies hashes, downloads the pinned dialogues CSV from the authors, checks its hash, rebuilds all three forecasts and checks thresholds against the bootstrap and saved control receipts. Expect PASS. A full control rerun is described separately.

## Compared to

Both comparators are specified by the bank's dialogue task. The reference bigram selects smoothing by inner held-out log loss. The other comparator retrains the same family with only the most recent coda. The package reports both, with recording-level uncertainty. See the-record-we-beat/snapshot.md and the novelty panel for the status check and scientific comparison.

## Not claimed

The result establishes predictive accuracy for this exact benchmark. Other datasets, whale populations, semantic interpretations and causal explanations are outside its scope. The transition-preserving controls are surrogates with fixed adjacent transitions. A separate sensitivity comparing the selected model to any family chosen after scoring each shuffled dataset is reported in the object.

## Additional evidence (not part of the panel's review)

- **Full control replay** (panel/replay-controls.md, a separate fresh reviewer, ends `pass: true`): all 800 control seeds were recomputed with the frozen code and compared with the stored receipts; see that file for the maxima and counts.
- **Lead agent's checks** (how-we-built-it/lead-agent-checks/, author evidence): on the frozen object the gain over R1 is 0.174 to 0.325 bits per coda in every one of the five folds and over the twin 0.182 to 0.415; 137 of 188 recordings gain over R1; without the five most-helped recordings the gain is still 0.221 over R1 and 0.265 over the twin. An independent re-derivation written from the bank's criterion alone (without the authors' code) finds an order-3 n-gram 0.266 bits below its own R1 (interval 0.223 to 0.319) and 0.251 below a well-tuned one-coda twin that is better than R1 (0.208 to 0.311); a repetition-aware first-order model gains only 0.054, so repeated runs of one token do not explain the gain.

## Credits

Dialogue annotations and source data: Sharma, Gero, Payne, Gruber, Rus, Torralba and Andreas, [Nature Communications 15:3617 (2024)](https://doi.org/10.1038/s41467-024-47221-8). Prior sequence modeling includes [WhaleLM](https://doi.org/10.1101/2024.10.31.621071) and [Sinha and Chavan](https://arxiv.org/abs/2606.16084).
