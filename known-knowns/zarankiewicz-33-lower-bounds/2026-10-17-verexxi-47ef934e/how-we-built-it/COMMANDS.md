# Commands (run from this folder, Python 3.8+, standard library only)

The check of the object itself is `sh ../verify-it-yourself/run_checks.sh` from the package folder. Everything here is
supporting evidence. The file PREREG.md is the frozen judging rule as written; its paths starting with claim/ now
correspond to object/ and verify-it-yourself/ in this package.

0. Third-party data (public witness matrices, the table data for closure.py / lb_closure.py) is not in this package. Fetch it once,
   with every sha256 checked: `python fetch_third_party.py` (URLs and hashes: third_party_sources.md). It fills baseline/wit/ and
   status_source/. Steps 2, 3 and 4 need it; step 1 and the whole verify-it-yourself/ folder do not.
1. Find a 142-one matrix from scratch (random, 10 minutes cap, not deterministic in time):
   `python search/zsearch.py 16 19 142 10 101 out_search`
   The saved reruns are in search/output/ (seeds 101 to 106, each reached 142; times in search/output/log_seed*.txt, which use local clock time, UTC minus 4 hours; launch 2026-10-17T12:11:22Z).
   Compare them with the object: `python search/compare_reruns.py ../object/z_16x19_142.txt search/output`
2. Trivial-surgery baseline on the 12 public matrices in baseline/wit/ (after step 0) (about 7 minutes per seed):
   `python baseline/surgery_baseline.py 16 19 --runs 4000 --seed 1 --max-seconds 1500 --save best_seed1.txt`
   Saved output for seeds 1 to 4 (192000 runs, best 141, none at 142): baseline/output/.
3. Exact sub-matrix copy test (0 copies expected): `python baseline/derivability.py ../object/z_16x19_142.txt baseline`
   and its self-test `python baseline/derivability.py --selftest`.
4. Published-number closures: `cd status_source && python closure.py && python lb_closure.py`.

The claimed file itself came from an earlier 20-second run of search/initial_program_ls.py; its seed was not recorded.
