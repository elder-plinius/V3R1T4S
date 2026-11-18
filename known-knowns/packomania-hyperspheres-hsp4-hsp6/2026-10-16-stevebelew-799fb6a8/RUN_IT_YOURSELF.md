# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 79
    r* = 0.25656578313445631327569697675743472477008114347708
    table = 0.256468324828
    gain = 0.00009745830645631327569697675743472477008114347708
    posted r* = 0.25646832482658934891806610250239858444145357249253 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.01576311991365440431215448094500931457071053187825
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-79.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
