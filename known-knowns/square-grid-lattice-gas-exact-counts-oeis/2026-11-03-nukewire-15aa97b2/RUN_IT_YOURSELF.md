# RUN IT YOURSELF

From this folder in a fresh shell (Python 3.8+, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (~1 minute). Every step of the checker is
independent of the build code: it re-derives small counts from the definition
(own big-integer DP), then CRTs the two packaged residue files against the
object, the published snapshot, and the a(28) anchor.

Rebuilding the object from scratch (numpy 1.2x+, ~4-5 h per run on one core;
see how-we-built-it/COMMANDS.md for the exact session commands):

    python how-we-built-it/runA_rowsweep.py gate      # exact self-checks
    python how-we-built-it/runB_chunked.py gate       # lineage check
    python how-we-built-it/runB_chunked.py gate-chunk # sliced-path check
    python how-we-built-it/runB_chunked.py validate   # cross-check vs runA
    python how-we-built-it/runA_rowsweep.py work out/runA.txt 2026-11-04T00:00:00Z
    python how-we-built-it/runB_chunked.py work out/runB.txt 2026-11-04T00:00:00Z
    # then CRT both (see how-we-built-it/crt_ab.py; edit the two path
    # constants at the top) — the two runs' CRT values agree on every cell.
