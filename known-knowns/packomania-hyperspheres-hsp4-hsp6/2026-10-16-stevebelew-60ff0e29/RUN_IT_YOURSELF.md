# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 91
    r* = 0.24699818287380882063495515293045887856895962747508
    table = 0.246960900415
    gain = 0.00003728245880882063495515293045887856895962747508
    posted r* = 0.24696090041418810620039171094692623694478183604276 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.00858147704625424668205982118199419684862339371181
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-91.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
