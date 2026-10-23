# Rebuild the frozen schedule

From this directory run `python 3 rebuild.py`. Expected last line: REBUILD PASS.

The standard-library script fetches 52 pinned public source files, checks every hash, and replays the original sorted source order and random stream: seed 1,16 reconstructions per direct and transposed map, maximum source rank 51. source-manifest.json records URLs and hashes; reference data are not distributed. Use --source-cache for a local saved source cache.

The files code/dag_search.py and code/synth.py are the actual discovery program. code/exact_check.py is its exhaustive discovery evaluator. This is heuristic circuit synthesis, not a proof of optimality. The replay was actually tested against the saved public source cache and reproduced the frozen object hash. Downloads and replay outputs are local scratch data and excluded from this package.
