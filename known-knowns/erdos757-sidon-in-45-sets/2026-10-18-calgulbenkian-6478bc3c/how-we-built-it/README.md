# How the witness was built

The set was made by algebraic gluing, not by random search. Files, all copied from the contributor's snapshot (read-only, taken 2026-10-18T13:45:35Z) and sanitised:

- `PREREG.md`: the frozen plan and thresholds for the target (written 2026-10-14).
- `glue_a14_b8.py`: the route that produced this witness. It glues the Ma-Tang 14-set to an 8-element shell at one shared vertex, adds two cross-block 3-term progressions, and solves the resulting 8 x 8 linear system over the rationals; the contributor reports 223 distinct 21-element solutions, one of which is `object/witness_n21_s12.json`. It imports the contributor's own verifier `verify_erdos757.py` (copied here beside it, because the script cannot run without it). The script writes its result to `../result/` relative to its own folder.
- `contributor_how_we_found_it.md`: the contributor's own short account of the same route (unverified).
- `erdos757_explore.py`: later exploration by the same agent (enumerating all gluings, double and triple gluings that gave a 35-element witness, and searches for a ratio below 4/7 that found none). It is included because the brief for this package named it; it did not produce the shipped witness. It reads `verify_erdos757.py` from a path in the contributor's workspace, so it needs that path adjusted to run.
- `sa_erdos757.c`: the contributor's earlier simulated-annealing and exact-bitmask program (compile line in its header: `clang -O3 -pthread sa_erdos757.c -o sa_erdos757`). It searched hypergraphs and integer sets; it is not the route of this witness.

The exact command lines of the original run are not recorded in the snapshot beyond what the script headers say. We ran `glue_a14_b8.py` on 2026-10-18 in a scratch folder (python 3.9, standard library); it wrote a `witness_n21_s12.json` whose sha256 equals the shipped object's (6478bc3c...f2539), so the route reproduces the witness byte for byte.
