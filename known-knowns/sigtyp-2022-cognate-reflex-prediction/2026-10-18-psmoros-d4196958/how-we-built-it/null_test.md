# Null test (runs/2026-10-18-0202/PREREG.v2.md rule 1), cell L30 (proportion 0.30, mean BLEU), run 2026-10-18-1249

Paired permutation null against the bar holder's per-item predictions (our own COMB-NEW at 0.30, runs/2026-10-18-0202/out/comb_new/test/0.30, mean BLEU 0.6839233380559118), 400 controls: in control c every cognate set's rows are swapped between the candidate (the BLEU-MBR object runs/2026-10-18-0202/out/bleu_new/test/0.30) and the bar holder with probability 1/2 (random.Random(20261018 + c)); d = candidate BLEU minus bar BLEU (official item BLEU and aggregation, left-to-right). Run by the main session at 2026-10-18T12:47:49Z-12:47:50Z with runs/2026-10-18-0202/tools/null_test_metric.py (working directory runs/2026-10-18-0202); full output runs/2026-10-18-0839/out/lead/null_L30.out and .json. Lines below copied from the tool's output.

controls: 400
best_control: 0.0035017194380646544
real: 0.003514400791687966
real_beats_all_controls: yes
command: cd runs/2026-10-18-0202 && python3 -I tools/null_test_metric.py --metric bleu --gold-dir WORKDIR/scratch_q15/ST2022/data-surprise --cand-dir out/bleu_new/test/0.30 --bar-dir out/comb_new/test/0.30 --prop 0.30 --out ../2026-10-18-0839/out/lead/null_L30.json

detail: candidate bleu 0.6874377388475998, bar 0.6839233380559119, d = 0.003514400791687966
note: the real difference beats the best control by 1.2681353623311686e-05 only (0.003514400791687966 vs 0.0035017194380646544, python3 subtraction): the rule is met, narrowly.
