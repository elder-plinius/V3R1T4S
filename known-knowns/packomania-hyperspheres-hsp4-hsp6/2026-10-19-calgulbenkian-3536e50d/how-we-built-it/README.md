# How we built it (hsp4, N = 170)

Code (copied from the contributor's snapshot, absolute paths replaced; nothing else changed):

- `transplant_scan.c`: stage 1. Two-stage frozen-shell inner-core transplant: 20 inner spheres taken from the N = 166 packing are rotated in O(4) inside the frozen 150-sphere outer shell of the N = 169 packing, then all 170 spheres are unfrozen and jammed with a soft-sphere L-BFGS. The contributor's note gives r* = 0.2156371457737953995400180 for this stage.
- `hsp_basin_opt.c`: stage 2. An 80-bit long double log-sum-exp L-BFGS continuation up to beta = 2,000,000 with annealing micro-jitter, which polished the N = 170 packing to r* = 0.2156450594683900081281903 (the object here).

The N = 166 and N = 169 packings used as inputs are the posted Packomania files (third-party data, not shipped; the contributor's workspace read them from a local copy of the posted coordinate archive).

Build line, as written in the header of `hsp_basin_opt.c` (the path before the file name is the contributor's):

```sh
cc -O3 -march=native -Wall -Wextra -o hsp_basin_opt hsp_basin_opt.c -lm
```

`transplant_scan.c` is built the same way. Needs a C compiler only.

What is not recorded: the command lines (arguments, seeds, input paths) of the runs that produced the object. The snapshot holds the two sources and the contributor's method summary only. No PREREG.md was recorded for this cell: the snapshot of the contributor's workspace holds no pre-registration for it, so none is shipped. The exact command lines of the runs are not recorded either, except where stated below.

Contributor's own method summary (unverified):

1. Lens 1, `transplant_scan.c`: inner-core transplant from N = 166 into the N = 169 outer shell, then unfrozen soft-sphere jamming (r* = 0.2156371457737953995400180).
2. Lens 2, `hsp_basin_opt.c`: log-sum-exp L-BFGS continuation with micro-jitter, polishing N = 170 to r* = 0.2156450594683900081281903.
