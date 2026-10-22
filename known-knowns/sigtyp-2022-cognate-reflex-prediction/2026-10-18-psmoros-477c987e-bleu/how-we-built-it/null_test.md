# Null test, cell L40 (PREREG rule 13; session 2026-10-18-1758)

Paired permutation null against Mockingbird-I1's official per-item predictions at 0.40 (pinned clone systems/mockingbird-i1/surprise/FAM/result-0.40.tsv), 400 controls, per-cognate-set swaps with probability 1/2 (random.Random(20261018 + c)); candidate = classifier/PRIMARY's frozen test-0.40 predictions (selection.md). Run by the main session at 2026-10-18T21:17:52Z-21:18:14Z (date -u), after selection.md. Lines copied from the tool's output (runs/2026-10-18-1758/out/null_L40.out; JSON out/null_L40.json):

controls: 400
best_control: 0.013304732573755529
real: 0.08103648513804473
real_beats_all_controls: yes
command: CALIBRATOR_VENV_PYTHON -I tools/null_test_metric.py --metric bleu --gold-dir PINNED_CLONE/data-surprise --cand-dir newent/classifier-PRIMARY/test/0.40 --bar-dir PINNED_CLONE/systems/mockingbird-i1/surprise --prop 0.40 --out out/null_L40.json

(run from runs/2026-10-18-1758; CALIBRATOR_VENV_PYTHON = runs/2026-10-16-2026/attempts/calibrator/venv/bin/python, PINNED_CLONE = the sigtyp/ST2022 clone at 03094435.)
