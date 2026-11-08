# Run it yourself

## Verify the object (fresh shell, from this folder)

    sh verify-it-yourself/run_checks.sh

Expected output (the real run is in verify-it-yourself/RECEIPTS.md):

    ok   10125 < b < 65537
    ok   b is not a perfect power
    ok   p > 1e12
    ok   p is prime (deterministic Miller-Rabin)
    ok   p does not divide b
    ok   b^(p-1) == 1 mod p^2
    b = 56350, p = 1024048960667, Fermat quotient q_p(b) mod p = 0
    PASS

Without the script:

    python3 verify-it-yourself/verify.py object/pair.json
    python3 -c "p=1024048960667; print(pow(56350, p-1, p*p))"      # prints 1

## Rebuild the object (the search that found it)

The sweep is how-we-built-it/wieferich_sweep.py, with pinned requirements in how-we-built-it/requirements.txt (gmpy2,
numpy). Make a virtual environment and install those requirements. Then run from how-we-built-it/, with the
environment variable WIEFERICH_SCREEN set to mitm (the exact screen the search used):

    WIEFERICH_SCREEN=mitm python wieferich_sweep.py sweep OUTDIR 1024040000000 20000000 1 DEADLINE 70 10126 65536 1024060000000

- OUTDIR is any empty folder.
- DEADLINE is a Unix time a few minutes ahead (for example the output of `date +%s` plus 900).
- On Windows cmd, run `set WIEFERICH_SCREEN=mitm` first.

This sweeps exactly one block of primes, 1024040000000 <= p < 1024060000000, against all 6852 non-perfect-power
70-smooth bases in 10126..65536.
- OUTDIR/hits.jsonl then contains the pair 56350 / 1024048960667.
- OUTDIR/blocks.jsonl carries the block's record. Its q-matrix sha256 matches the one in hit_block_record.json,
  which is the original run's record of that block: prime count, sha256 of the Fermat-quotient matrix, candidates
  and hits.
- On one core this takes about 1–2 minutes. how-we-built-it/REBUILD_OUTPUT.txt is the real output of this command,
  run from this package's copy of the script.

The search's frozen plan is how-we-built-it/PREREG.md. how-we-built-it/p1_known_positives.py is the pipeline's
pre-attack self-test on the same base set, run through the same screen: brute force and pipeline gave identical pair
sets in three windows (how-we-built-it/p1_known_positives_output.txt).
