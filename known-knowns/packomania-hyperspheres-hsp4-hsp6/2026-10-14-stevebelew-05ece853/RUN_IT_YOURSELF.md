# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 30
    r* = 0.31599622341030283547138706854513124839625199931628
    table = 0.315990168743
    gain = 0.00000605466730283547138706854513124839625199931628
    posted r* = 0.31599016874191217977149536243310290052781092449224 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.03596693674143654880170571079436369045914598156425
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-30.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
