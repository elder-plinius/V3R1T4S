controls: 400
best_control: 3.0165922022143166
real: 0.43675104854437247
real_beats_all_controls: yes
command: `& <PYTHON> (a venv with scikit-learn 1.9.1, rdkit 2026.09.2, lightgbm 4.7.0) attempts\cliff-fx\code\null_test_244.py`
(from the run folder; full log attempts/cliff-fx/output/null_test_244_log.txt, machine record
attempts/cliff-fx/output/null_test_244.json)

Protocol (PREREG.v2 §4, frozen before the candidate read): the frozen M1 recipe (members +
combiner weights from M1_read) retrained 400 times with train labels shuffled (rng seed
20261118+k, k=0..399), each scored once on the official test rows; the real M1's overall test
MSE must beat every control. Result: every control lands at 3.02-4.05 (train-mean-predictor
level, 0 structure), real 0.4368 — beats all 400. Null test satisfied.
