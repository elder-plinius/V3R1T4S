# Elephant rumbles: the 27.5% receiver accuracy against caller habits and a within-caller shuffle

## What

On the 437 Cert_ID_Bin == 1 calls of the Dryad n469 spectral file, a scikit-learn re-implementation of the paper's section-10 MODEL 1 forest (500 trees, mtry 6, leaf size 1, 60% subsampling without replacement, caller not an input) scores a mean receiver accuracy of 0.2695 over 100 fresh caller x receiver stratified 7-fold draws, within 0.02 of the paper's 27.5%; on the same draws the bank's caller-habit baseline scores 0.4922, and the 99.9th percentile of 1,000 single-draw reruns with receiver labels shuffled within caller on the same folds is 0.2426, so 27.5% exceeds that within-caller shuffle null but not the caller-habit baseline.

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library only, under a minute). It checks the hashes, then recomputes from the saved per-call predictions and the call list every accuracy of the 100 fold draws, the fold stratification, the caller-habit rule, the 1,000 shuffle controls' statistics and every statement of partial win p3. Expected last line: PASS. Rebuilding the predictions themselves takes about 2.5 hours on 4 cores; see RUN_IT_YOURSELF.md.

## Compared to

| what | value | source |
|---|---|---|
| Pardo et al. (2024) random forest | 27.5% | the paper, as quoted by the bank entry |
| our re-implementation, mean of 100 fold draws | 0.2695 | object/summary.json |
| caller-habit baseline, same draws | 0.4922 | object/summary.json |
| forest on within-caller shuffled labels, 1,000 controls: 99.9th percentile / maximum | 0.2426 / 0.2449 | object/null-rf-controls.jsonl |

Status source (Europe PMC citations of the paper) fetched 2026-11-18T22:55:56Z by the NOVELTY reviewer: 32 citing papers, none a reanalysis. See the-record-we-beat/snapshot.md.

## Not claimed

The full win: a preregistered caller-habit-plus-acoustic pipeline scored 0.4902 against the habit baseline's 0.4922, inside its own within-caller shuffle null (99.9th percentile 0.5172); its outputs are in how-we-built-it/ and it is not claimed. Not claimed either: that elephants do or do not use names, partial wins p1 and p2, or an exact replication of ranger and caret (the trees are scikit-learn CART and the folds come from our own stratified generator; a with-replacement forest scores lower, 0.258, still above its own shuffle null; panel/gate.md lists every disclosure). The shuffle null's tail is noisy: a reviewer's own 10 shuffles reached 0.2471, still below 0.275 and 0.2695. object/calls.csv lists only the sound IDs, callers and receivers of the 437 calls (three columns of the CC0 Dryad deposit, no acoustic features), because Dryad refuses scripted downloads; how-we-built-it/code/build_package.py shows how it is cut from the Dryad file, whose sha256 is in the-record-we-beat/snapshot.md.

## Credits

Data and the original analysis: Pardo, Fristrup, Lolchuragi, Poole, Granli, Moss, Douglas-Hamilton and Wittemyer, [Nature Ecology and Evolution 8:1353-1364 (2024)](https://doi.org/10.1038/s41559-024-02420-w); data on [Dryad](https://doi.org/10.5061/dryad.hmgqnk9nj) (CC0); code on [Zenodo 10576772](https://zenodo.org/records/10576772). Citation index: [Europe PMC](https://europepmc.org/). Tools: NumPy, pandas, scikit-learn. Run by the V3R1T4S kit (Claude Code as lead agent, with three fresh reviewer subagents).
