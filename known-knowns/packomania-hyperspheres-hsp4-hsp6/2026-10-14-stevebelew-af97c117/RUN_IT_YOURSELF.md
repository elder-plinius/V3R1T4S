# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 54
    r* = 0.27679869568710738565880773628465980659885013899553
    table = 0.276798004181
    gain = 6.9150610738565880773628465980659885013899553E-7
    posted r* = 0.27679800418036796411544721627064705633758830553134 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.00373620480078476003238556236970620751440417372928
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-54.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
