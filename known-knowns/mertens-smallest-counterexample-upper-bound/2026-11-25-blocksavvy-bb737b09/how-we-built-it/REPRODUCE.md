# REPRODUCE (claim p4)
Needs Python 3 and python-flint 0.9.0. From claim/:
1. Check the saved chunks: python code/aggregate_claim.py   (seconds) -> compare with result/aggregate_claim.json;
   expected complete true, boundary_ok true, overlaps_bzyzz_K2 true, head_overlaps_bzyzz_main true,
   contained_in_bzyzz_K2 true, K2 = [1.00030525038651 +- 5.07e-15], lower_K2_minus_E_minus_1 about 3.0525e-4 (default head dir chunks_head128;
   `python code/aggregate_claim.py chunks_head` uses the 96-bit head).
2. Recompute any chunk from scratch and compare "S" with the saved file, e.g.
   python code/k2_chunks.py 2325201 2325573 373 1 recheck 96   (vs chunks_tail/c_02325201_00373.json)
   python code/k2_chunks.py 1 400 400 1 recheck 96               (vs chunks_head/c_00000001_00400.json; use 128 for chunks_head128/)
   A random sample is a spot check only.
3. Full recomputation (about 11-13 core-hours; ~2-2.5 h wall on 6 cores):
   python code/k2_chunks.py 1 600000 400 6 chunks_head128 128 && python code/k2_chunks.py 600001 2325573 400 6 chunks_tail 96
   then step 1.
