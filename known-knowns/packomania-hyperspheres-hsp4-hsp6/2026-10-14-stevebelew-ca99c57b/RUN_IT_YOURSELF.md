# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 66
    r* = 0.26497636751387602328900871272524886345982755040961
    table = 0.264968466676
    gain = 0.00000790083787602328900871272524886345982755040961
    posted r* = 0.26496846667501594336072425145175369485812513743268 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.01995700387580611411250372797540624372079765447078
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-66.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
