# RUN_IT_YOURSELF

From this package folder, in a fresh shell:

1. Verify the claim (stdlib only, ~2 min):

   ```sh
   sh verify-it-yourself/run_checks.sh
   ```

   Expected last line `PASS`; full expected output in verify-it-yourself/RECEIPTS.md. The
   checker verifies object/candidate_N3307.txt (sha256
   f09f5eecbb7b14f10607e97c3a74829129931cc0e0285e4372a5b4c4f61b0194 — 3307 centres), recomputes
   r* = min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) at 60 significant digits from the
   coordinate strings, and requires margin >= 1e-11 over the recorded table value. The integrity
   check accepts the LF or CRLF-materialised form of the object.

2. Full verification including posted-config integrity and non-isometry (needs numpy+scipy):
   how-we-built-it/verify_N3307.py (adjust its two data paths to this package: the candidate is
   object/candidate_N3307.txt; the posted configuration and live table must be fetched fresh —
   see the-record-we-beat/); its saved output from the finding run is
   how-we-built-it/verify_output.txt.

3. Re-check the live cell before trusting the baseline (the table can move):

   ```sh
   curl -s https://packomania.com/cci/txt/radius.txt | awk '($1==3307)'
   ```

   Expected today: `3307 0.016314899796158766989004378524`. A different value means the cell
   moved: re-verify the margin (and https://packomania.com/pending-requests.html) before citing
   this package.

4. Rebuild the object from scratch (deterministic, ~2 min with numpy):
   how-we-built-it/lens1_gap_sweep.py — the same sweep that found this cell and its sibling
   N=4141 (see how-we-built-it/README.md); it prints `CANDIDATE N=3307 quick margin +4.400e-06`.
