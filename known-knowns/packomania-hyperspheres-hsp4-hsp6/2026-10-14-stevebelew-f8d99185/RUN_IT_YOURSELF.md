# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 35
    r* = 0.30628552449723586179906861009456921677053447814202
    table = 0.306285269828
    gain = 2.5466923586179906861009456921677053447814202E-7
    posted r* = 0.30628526982708669946072943778297907486309487239982 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.05027623337226010656351435148109694503911925071875
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-35.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
