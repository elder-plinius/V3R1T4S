# How we found it (contributor text, unverified)

The brief: Lee and Shan verified by computer in 2002 that every tree on at most 17 vertices is super edge-magic, and
Gallian's survey (28th ed., 2025) still gives 17. The bank's partial win p1 asks for a certificate up to 20.

We used the consecutive-edge-sum form of the definition (a bijection onto 1..n whose edge sums are consecutive), so a
search only places vertex labels. A randomised backtracker with restarts (sem_direct) labelled every tree on 18
vertices and all but two on 19 quickly. At 20 vertices (823065 trees) it ran out of time on about 29% of them, so we
layered: an alpha-labeling search (every alpha-labeled tree is super edge-magic by a fixed relabeling) took a third
of the rest, a second sem_direct pass took almost all the remainder, and the last 3 trees, which are
caterpillars shaped like two big stars joined through one vertex, were labelled by the classical caterpillar
construction. The hardest trees at both 19 and 20 had that same two-hub shape. They are listed in
`object/hardest_trees_n19_n20.txt` for anyone hunting a counterexample.

What failed: sem_direct alone at n = 20 within the time cap (about 90 trees per second per core, stalling on two-hub
caterpillars); an alpha-labeling search alone (some trees have no alpha-labeling within the cap, and some may have
none at all). The scheduled run was cut off when the machine's agent host restarted, and a later session resumed it.
