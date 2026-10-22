The Python prover is standard-library code. For example, run from this package root:

```sh
python3 how-we-built-it/prover/adaptive.py middle 3 middle-rebuilt.json --seconds 60
python3 how-we-built-it/prover/adaptive.py leader 7 leader-rebuilt.json --seconds 60
```

For a paused generator, repeat the command with --resume. A checkpoint is complete only if pending is empty, no node is unresolved, and an independent checker verifies every region.

The optional native generator requires building bounds_fast.cpp as a shared library named bounds_fast.dylib beside native_adaptive.py (Clang: -O3 -std=c++17 -dynamiclib on macOS, or -shared -fPIC on Linux). It accepts ORDER DEPTH OUTPUT --seconds N --workers 1 and --resume. The difficult original search started at depth 12 and resumed pending regions at depth 13. The exact point of the depth change depended on the saved search checkpoint; a fresh heuristic run is not promised to produce byte-identical partitions. The complete final partition is supplied as the proof object and all of its bounds are independently recomputed by the verification command.

No generator output is evidence until independently verified. The older unbounded-integer and forward checking methods are described in object/PROOF.md; this package uses the faster independent vertex-stack checker.
