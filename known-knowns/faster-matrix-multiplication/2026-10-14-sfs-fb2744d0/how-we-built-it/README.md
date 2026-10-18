# Rebuild the frozen schedule

From this directory run `python3 rebuild.py`. Expected last line is `REBUILD PASS`.

The standard-library script fetches 52 pinned public reference files from the recorded source commit, checks every hash, and replays the exact original sorted source order and random stream: seed 1, 16 reconstructions per direct and transposed map, maximum source rank 51. It writes rebuilt-scheme.json with the frozen object's exact hash. source-manifest.json records URLs and hashes; the reference data themselves are not distributed here. A local cache can be supplied with `--source-cache`.

code/dag_search.py and code/synth.py are the actual discovery program. It builds signed vector dependency alternatives from source circuits, reschedules direct maps, and reverse-accumulates rescheduled transposes. code/exact_check.py is the original exhaustive discovery evaluator. This is heuristic circuit search, not an optimality proof. The saved object alone is sufficient for exact verification.

The replay was actually tested against the saved public-source cache and produced REBUILD PASS and the frozen candidate hash. Rebuild output files and downloaded data are local scratch data and are not part of the submission package.
