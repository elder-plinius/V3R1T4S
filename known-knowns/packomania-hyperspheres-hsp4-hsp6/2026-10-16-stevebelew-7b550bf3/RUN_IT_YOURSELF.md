# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 104
    r* = 0.24053869762389658208934651593930039633912649358841
    table = 0.240535464233
    gain = 0.00000323339089658208934651593930039633912649358841
    posted r* = 0.24053546423234634946500586269117756761221019569080 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.00529279228567690444037011489175755466389688678023
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-104.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
