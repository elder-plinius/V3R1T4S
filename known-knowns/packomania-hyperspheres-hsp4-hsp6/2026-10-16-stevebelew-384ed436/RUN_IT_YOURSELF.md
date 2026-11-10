# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 111
    r* = 0.23735957002750166280229786794662708494149688154608
    table = 0.237355353009
    gain = 0.00000421701850166280229786794662708494149688154608
    posted r* = 0.23735535300820492223693554669958508173698186289496 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.00430846191250055995816400923751310025213271940506
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-111.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
