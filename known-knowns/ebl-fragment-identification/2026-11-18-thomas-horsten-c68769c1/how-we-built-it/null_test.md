# null_test (PREREG null_test: required)

claimant: BM.68403 -> /L/3/10/Standard Babylonian/- (partial win p2)
null: same fragment aligned (frozen C aligner, full band, min_block 6) to the 228-chapter
pool (11,461 lines / 124,324 sign tokens) with LINE ORDER SHUFFLED per seed:
np.random.default_rng(20261117 + k).permutation(11461), token content unchanged
(the literal "line order shuffled" null). p_raw = (1 + #{controls >= real}) / (K + 1);
p_bonf = min(1, p_raw x N), N = |S| = 40 (the fragments actually null-searched; frozen
PREREG rule). |S| = 40 > 39, so per the PREREG reachability clause the claimant uses
K_claim = 1,000,000.

controls: 1000000
best_control: 46
real: 612
real_beats_all_controls: yes
command: (from the run folder) python3 code/null_big2.py 1000000 output/null_claimant.json 24   (K, fids-list, workers); per-fragment summary in output/null_1000000_null_claimant.json.json, full control array in output/null_1000000_null_claimant.json.npz; p computed in output/null_big_result_1M.json (p_raw = 1/1000001 = 9.99999e-07, p_bonf = 40 x p_raw = 3.999996e-05 < 1e-4, n_ge = 0).

Diagnostics (not the claimant decision, recorded for the record):
- K=400 screen (output/null400_summary.json): 40 fragments x 400; 39/40 beat all controls;
  p_bonf floor 40/401 x p_raw = 0.0998 (by construction the screen cannot reach 1e-4).
- K=400,000 on all 10 (a)+(b)-passers (output/null_400000_null_Nset.json.json,
  output/null_big_result.json): n_ge = 0 for every one (control_max 27-85 vs real 230-612),
  p_bonf = 40/400001 = 9.9999750e-05 < 1e-4.
- p1 candidates K=400,000 (output/null_400000_null_fids_p1.json.json,
  output/null_big_result_p1.json): Sm.1309 real 27 < control_max 32 (n_ge 66, p_bonf 6.70e-3,
  beats-all no); K.9496 died at the K=400 screen (p_bonf 1.0).
