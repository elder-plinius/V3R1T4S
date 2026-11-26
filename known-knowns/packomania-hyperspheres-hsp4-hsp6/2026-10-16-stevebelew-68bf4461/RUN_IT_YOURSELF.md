# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 81
    r* = 0.25408038179177490302490222756670917019602502200718
    table = 0.254058669351
    gain = 0.00002171244077490302490222756670917019602502200718
    posted r* = 0.25405866935045098640760589110865608346550841384954 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.0645733303491195234824830163736031918214437108778
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-81.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
