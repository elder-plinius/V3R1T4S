# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 63
    r* = 0.26811487284314488862210011861673095309759404370228
    table = 0.268114739680
    gain = 1.3316314488862210011861673095309759404370228E-7
    posted r* = 0.26811473967898304591697808260870085160567490880197 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.00414227388933108307092013834254785238516157380858
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-63.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
