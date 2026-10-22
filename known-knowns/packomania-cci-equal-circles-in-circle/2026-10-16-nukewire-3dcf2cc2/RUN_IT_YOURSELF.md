# RUN_IT_YOURSELF

From this package folder, in a fresh shell:

1. Verify the claim (stdlib only, ~2 min):

   ```sh
   sh verify-it-yourself/run_checks.sh
   ```

   Expected last line `PASS`; full expected output in verify-it-yourself/RECEIPTS.md. The
   checker verifies object/candidate_N4141.txt (sha256
   b5cc9aef50c8aac1bdfa51107f030ca3f7e2ddf0f1483eb0c9336ee91095039e — 4141 centres), recomputes
   r* = min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) at 60 significant digits from the
   coordinate strings, and requires margin >= 1e-11 over the recorded table value.

2. Independent recomputation with mpmath at exactly 50 digits (needs `pip install mpmath`, or
   numpy+scipy+mpmath for the pair-locating pass): the run's verifier is
   how-we-built-it/verify_candidates.py (also covers the integrity and non-isometry checks);
   its saved real output from the finding run is in the submitting workspace's run record.

3. Re-check the live cell before trusting the baseline (the table can move):

   ```sh
   curl -s https://packomania.com/cci/txt/radius.txt | awk '$1==4141'
   ```

   Expected today: `4141 0.014601755763187308074373236782`. A different value means the cell
   moved: re-verify the margin (and the pending list at https://packomania.com/pending-requests.html)
   before citing this package.

4. Rebuild the object from scratch (~2 min with numpy; no randomness — deterministic):

   ```sh
   python how-we-built-it/lens1_gap_sweep.py   # reads radius.txt placed next to it; see its header
   ```

   The sweep prints `CANDIDATE N=4141 quick margin +7.716e-06` and writes the same coordinates
   (byte-identical up to float formatting) as candidate_N4141.txt. See how-we-built-it/README.md.
