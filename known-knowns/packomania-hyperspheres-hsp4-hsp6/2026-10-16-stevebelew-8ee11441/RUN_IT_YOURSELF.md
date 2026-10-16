# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 94
    r* = 0.24594101953684519902477122077410773912161071382492
    table = 0.245932827006
    gain = 0.00000819253084519902477122077410773912161071382492
    posted r* = 0.24593282700485035414590082277414074442143812789919 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.00962392448350729396776157543381540861488982058532
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-94.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
