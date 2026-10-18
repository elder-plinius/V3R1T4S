# Null test (PREREG rule 13), cell L50 (proportion 0.50, mean BLEU), run 2026-10-18-0848

Paired permutation null against FeVeT's published per-item 0.50 predictions (the bar holder), 400 controls: in control c every cognate set's rows are swapped between the candidate (COMB-8, runs/2026-10-18-0839/out/comb8/test/0.50) and FeVeT with probability 1/2 (random.Random(20261018 + c)); d = candidate's advantage on the cell metric, left-to-right summation. Run by the main session at 2026-10-18T11:27Z after selection.md existed; tool runs/2026-10-18-0839/tools/null_test_metric.py (working directory runs/2026-10-18-0839); full output runs/2026-10-18-0839/out/null_L50.out and .json. Lines below copied from the tool's output.

controls: 400
best_control: 0.01251243685677561
real: 0.07520064450460762
real_beats_all_controls: yes
command: /opt/homebrew/opt/python@3.14/bin/python3.14 -I tools/null_test_metric.py --metric bleu --gold-dir WORKDIR/scratch_q15/ST2022/data-surprise --cand-dir out/comb8/test/0.50 --bar-dir work/fevet050 --prop 0.50 --out out/null_L50.json

detail: candidate bleu 0.6520222200978465, bar 0.5768215755932389, d = 0.07520064450460762
