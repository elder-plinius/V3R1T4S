# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 67
    r* = 0.26407220586962721960556480672169240390901697055044
    table = 0.264026543809
    gain = 0.00004566206062721960556480672169240390901697055044
    posted r* = 0.26402654380850668009937079277392085318037226010433 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.01509951569307613619652171998870448427413870483463
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-67.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
