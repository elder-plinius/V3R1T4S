# Null test, cell LA (PREREG rule 13; session 2026-10-18-1758)

Paired permutation null against Mockingbird-I1's official per-item predictions at all five proportions (pinned clone systems/mockingbird-i1/surprise/FAM/result-P.tsv), 400 controls; in control c one random.Random(20261018 + c) draws per P in the order 0.10, 0.20, 0.30, 0.40, 0.50 (families in the fixed order, cognate sets in order of first appearance in that P's gold), swapping the two systems' predictions for all rows of a set with probability 1/2; d = (left-to-right sum over P of the candidate's advantage at P) / 5. Candidate = classifier/PRIMARY's test predictions at every P (selection.md; newent/classifier-PRIMARY/test/P). Run by the main session at 2026-10-18T21:33:36Z (date -u start), after selection.md and the aggregate scoring. Lines copied from the tool's output (runs/2026-10-18-1758/out/null_LA.out; JSON out/null_LA.json):

controls: 400
best_control: 0.006990622234683363
real: 0.07140001314178449
real_beats_all_controls: yes
command: CALIBRATOR_VENV_PYTHON -I tools/null_test_metric_x.py --agg --metric bleu --gold-dir PINNED_CLONE/data-surprise --cand-dir newent/classifier-PRIMARY/test --bar-dir PINNED_CLONE/systems/mockingbird-i1/surprise --out out/null_LA.json

(run from runs/2026-10-18-1758; CALIBRATOR_VENV_PYTHON = runs/2026-10-16-2026/attempts/calibrator/venv/bin/python, PINNED_CLONE = the sigtyp/ST2022 clone at 03094435.)
