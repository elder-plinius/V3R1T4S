# LJ_662: E = -4581.205775329242 (below CCD LJ562-1000 table -4581.204895)

## What

The 662-atom configuration in LJ662_candidate_mp.txt is a certified Lennard-Jones local minimum (gradient 7.3e-27, 6 zero modes, no negative modes) with mpmath 30-digit energy -4581.20577532924205838854566916, which is 8.80e-4 below the LJ562-1000 table value -4581.204895 as fetched 2026-10-16T00:26:35Z and 8.62e-4 below the polished table point file, with no lower published N=662 value found in the recorded arXiv search and first-page Google Scholar check.

## Check it yourself

Python 3.8+ and a POSIX shell, no third-party packages:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. About 2 seconds on a laptop. Checks N = 662, energy and gradient norm in 40-digit decimal arithmetic, and the margin to the table value. The Hessian check (6 zero modes, none negative) needs numpy: see RUN_IT_YOURSELF.md.

## Compared to

Cambridge Cluster Database / Doye LJ562-1000 table, https://doye.chem.ox.ac.uk/jon/structures/LJ/LJ562-1000.html, cell N = 662, value -4581.204895, fetched 2026-10-16T00:37:44Z (HTTP 200). Margin 8.80e-4. The table's own point file 662.TXT polishes to -4581.204913257864 (8.62e-4 higher, distinct basin). Snapshot details in the-record-we-beat/.

## Not claimed

Not claimed to be the global minimum for N = 662. No exhaustive literature search: one arXiv web search and the first page of Google Scholar (checked by hand by the human), plus the bank-named Barron page; arXiv API queries timed out. The stdlib checker does not compute the Hessian. Reviewers were fresh contexts of the same assistant, not humans. Maintainer acceptance is separate.

## Credits

Submission credit: SwimingUpstairs. Comparison table: D. J. Wales, J. P. K. Doye et al., Cambridge Cluster Database (https://doye.chem.ox.ac.uk/jon/structures/LJ.html); table values for N = 562..1000 from Xiang, Cheng, Cai, Shao, J. Phys. Chem. A 108, 9516 (2004). Also checked: C. Barron's page https://academicos.azc.uam.mx/cbr/LennardJones/nw537-548.htm. Protocol: V3R1T4S, https://github.com/elder-plinius/V3R1T4S, commit c8ba8bc4258164998de76ab939b0748fe80f73a2.
