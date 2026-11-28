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
    b = 24766, p = 1000747824697, Fermat quotient q_p(b) mod p = 0
    PASS

Without the script:

    python3 verify-it-yourself/verify.py object/pair.json
    python3 -c "p=1000747824697; print(pow(24766, p-1, p*p))"      # prints 1

## Rebuild the object (the search that found it)

The sweep is how-we-built-it/wieferich_sweep.py, with pinned requirements in how-we-built-it/requirements.txt (gmpy2,
numpy). Make a virtual environment, install those requirements, then run from how-we-built-it/:

    python wieferich_sweep.py sweep OUTDIR 1000740000000 20000000 1 DEADLINE 70 10126 65536 1000760000000

- OUTDIR is any empty folder.
- DEADLINE is a Unix time a few minutes ahead (for example the output of `date +%s` plus 900).

This sweeps exactly one block of primes, 1000740000000 <= p < 1000760000000, against all 6852 non-perfect-power
70-smooth bases in 10126..65536. OUTDIR/hits.jsonl then contains the pair 24766 / 1000747824697. On one core this takes
about 1–3 minutes. how-we-built-it/REBUILD_OUTPUT.txt is the real output of this command, run from this package.
hit_block_record.json is the original run's record of that block: prime count, sha256 of the Fermat-quotient matrix,
candidates and hits.

The run's frozen plan is how-we-built-it/PREREG.md. how-we-built-it/p1_known_positives.py is the pipeline's
pre-attack self-test on the same base set: brute force and pipeline gave identical pair sets in three windows.
