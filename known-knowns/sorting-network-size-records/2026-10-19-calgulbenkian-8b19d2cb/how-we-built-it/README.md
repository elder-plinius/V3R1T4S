# How the object was built (contributor text, unverified)

Source: the contributor's search workspace for the target sorting-network-size-records, copied from the agent's read-only
snapshot of 2026-10-19. Local absolute paths were replaced by {WORKDIR}, {HOME} and {TMP}.

- `PREREG.md`: the run's pre-registration (win tiers, exact 0-1 propagation engine, four attack vectors).
- `sn_check.c`, `verify_sn.py`: the contributor's exact checkers (connected-group reachable-set propagation, depth by greedy layering).
- `sn_reduce_scan.c`, `run_full_reduce_loo_sweep.py`: wire-deletion reductions of the listed networks of wider sorters, with exact redundancy pruning.
- `sn_optimizer.cpp`, `hunt_pareto_gaps.py`: local-search optimiser (a stochastic comparator-removal and depth/size ratchet in the
  style of SorterHunter) and the driver that launches it on parent networks. `sn_optimizer.cpp` includes SorterHunter's headers
  (htypes.h, hutils.h, prefix_processor.h) and links its prefix_processor.cpp and hutils.cpp; those third-party files are not copied here.
  SorterHunter is by Bert Dobbelaere: https://github.com/bertdobbelaere/SorterHunter
- `sn_exact_beam.cpp`, `run_exact_beam_sweep.py`: exact-state beam search over comparator suffixes.

## This object

The snapshot records which programs were run on this target but not which program produced which of the eight networks of the
run (the results file lists only the final comparator lists and their checker lines). This object, n=51 (size,depth)=(387,21), is the file
`N51_S387_D21.txt` of that run. Its parents are networks of the live Dobbelaere table, as the driver scripts read them from the
table's data file; the exact command lines are not recorded. The driver scripts show the compile lines (`clang++ -O3 -std=c++17 ...`
for the optimiser, `clang -O3 sn_reduce_scan.c` for the reduction scan) and the job lists; the paths in them point to scratch
folders that are not part of the snapshot.

## Not included

The Dobbelaere table data, the SorterHunter sources and the intermediate candidate networks are not copied; see
`the-record-we-beat/` for the table by name, link and checksum.
