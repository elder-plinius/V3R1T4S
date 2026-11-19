# Whale speaker turn-taking, partial win p4

## What

On the specified five REC-held-out folds of the pinned sperm-whale-dialogues.csv, the training-only-selected categorical pipeline predicts adjacent speaker-label equality at 3,418 eligible positions with 0.780267728 bits per position versus 0.850317354 for the smoothed first-order same-or-switch reference, improving by 0.070049626 bits with a positive REC-bootstrap interval and exceeding all 400 payload and 400 first-order-preserving selected-pipeline control gains.

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh`. It downloads the pinned source CSV, checks its hash, reconstructs the baseline and candidate probabilities, recomputes the recording-bootstrap interval and checks all 800 stored control receipts. Expected last line PASS.

## Compared to

The binary reference predicts same or different speaker from the previous same-or-switch value. Its smoothing is chosen by nested training-fold cross-validation. Our selector and hyperparameters also use only training-fold predictions. Each of the five selected models uses repetition context.

## Not claimed

The result concerns the bank's exact binary task. Previous research including WhaleLM already describes predictable turn-taking. This candidate shares data and campaign provenance with our next-coda PR #1159, whose scope explicitly excludes p4. The two predictions have different targets.

## Credits

Data from Sharma, Gero, Payne, Gruber, Rus, Torralba and Andreas, [Nature Communications 15:3617](https://doi.org/10.1038/s41467-024-47221-8) and [the authors' repository](https://github.com/pratyushasharma/sw-combinatoriality). Prior work includes [WhaleLM](https://doi.org/10.1101/2024.10.31.621071). See panel/novelty.md for the exact comparison and current status.

## Disclosures

The p4 candidate was first scored in the same campaign as #1159 and later frozen for a separate review. No model or threshold was changed for this review. The ordinary payload shuffle and Euler-trail surrogate each have 400 seeds. The latter preserves binary adjacent-transition counts and is a diagnostic surrogate. Review limitations are retained verbatim in panel/.
