context: Claude Code subagent, fresh context [Sonnet 5.5]

# CRITERION report for 2cf4ffc7 (earth-moon-biplanar-10-chromatic, claimed p2)

All paths are relative to that folder.

## Checks run
I copied this package into my work folder and ran `sh verify-it-yourself/run_checks.sh` there. It printed [1/7] through [7/7] and `PASS` in about 8 seconds (stdlib only; networkx, drat-trim, cadical and kissat are not installed on this machine).

I also wrote my own short checker, which reads only `object/biplanar_9crit_n19_e92.json`. It confirmed:
- Graph: 92 distinct edges on 19 vertices, with E1 and E2 disjoint.
- Upper bound: the stored proper 9-colouring uses exactly 9 colours.
- Criticality, edge side: all 92 stored edge-deleted 8-colourings are proper for G minus that edge. Each of the 92 keys is an edge of G.
- Biplanarity, certificate side: both layers' rotation systems reproduce exactly their layer's edge set, and each gives V-E+F = 2 = 2C by face-walk count (C = 1, so a sphere embedding).
- Clique cutsets: a brute-force check over every clique of size 1 to 8 found none that disconnects G. The package's `run_checks.sh` only comments on this; it never tests it. The JSON invariants field asserts 0 clique cutsets.

I did not re-solve the UNSAT of 8-colouring. I have no solver and no drat-trim here. For chi >= 9 I rely on the package's own stdlib DRAT checker, which printed "VERIFIED EMPTY CLAUSE" for 763 clauses and 11963 proof lines. I did not rewrite that checker, so chi >= 9 rests on the package's own code. The edge-critical half is independently checked by my script.

## p2 clauses, word for word
- "9-critical (chromatic number exactly 9, and removing any edge lowers it)": met. chi <= 9 is confirmed by my checker. chi >= 9 is confirmed by the package's own DRAT checker only. Every edge deletion is 8-colourable, confirmed by my checker. So G is edge-critical, and so vertex-critical.
- "biplanar (explicit split into two planar layers)": met. An explicit 45/47 split is given. The per-layer sphere rotation systems pass my Euler check. The package also has Fary integer drawings, which I did not re-check beyond the package script passing. The stdlib planarity testers were the only ones that ran, since networkx is absent.
- "not isomorphic to any graph in Boutin-Gethner-Sulanke's published lists (checked by canonical labelling)": formally met, but weakly evidenced.
  - The graph's canonical hash `efe251d5...` is absent from `the-record-we-beat/bgs_published_canonical_hashes.json`.
  - That file holds 42 hashes: K6+C5 (n=11), 40 BGS graphs (n=12 to 16) and one 23-vertex Hajos sum. The README describes the set as Sulanke plus all 40 BGS graphs; it does not mention the 23-vertex Hajos sum.
  - The orders in the list are 11 to 16 and 23. G has n=19, so any order-preserving check separates it trivially. No canonical labelling is needed.
  - The 40 graphs appear to come from a third-party corpus (how-we-built-it/PREREG.md names Patil's `data/volkopat_pool/17_bgs*.edges`), not from the paper. I could not check them against the paper or confirm the list is complete.
  - The "canonical" form is a partition-refinement SHA256 written by the package. I did not independently confirm it is a true canonical form. Only the invariance direction matters here, and the order argument covers it.
  - The wider "published lists" (Gethner-Sulanke 2009 non-Hajos graphs up to n=17, Alalqam, Patil) are handled by order, "Hajos sum needs n>=21" and a Patil screen. I did not verify these.
- "exact verification of criticality and biplanarity": met. The checks are exact and finite, with no sampling and no floating point. The one reservation is that the DRAT verifier is the package's own, not an external drat-trim.

## Is README.md / INDEX.csv wording wider than p2?
Yes, in two ways.

1. Extras that p2 does not ask for.
   - "5-connected", "non-join" and "clique-cutset-free" are not part of p2.
   - "5-connected" is verified: the script's `exact_vertex_connectivity` gate rejects anything below 5, and its message prints kappa=5.
   - "non-join" is verified through the complement-connected check.
   - "clique-cutset-free" is not checked by `run_checks.sh`, and the README states it as fact ("zero clique cutsets"). My brute-force check confirms it. It remains an extra, not a p2 requirement.
   - The README also says non-join and 5-connected show the graph "cannot arise from trivial propagation rules". That is an inference, not a check. The Hajos bound (n>=21, from the n>=11 minimum) is argued, not tested. The Ore bound (n>=20) is stated in the README without a proof or a check. The graph's n=19 does satisfy it.
2. Wording in the headline "What" sentence.
   - "Certified non-isomorphic to all published BGS 9-critical biplanar graphs" depends on a list the package reconstructed itself.
   - "Both combinatorial rotation systems and Fary drawings" is true as stated.
   - "Two independent planarity testers" is only satisfied by two stdlib in-package verifiers, one topological and one geometric. An external tester (networkx or Boost) did not run. That is not required for p2.
   - README.md and `CLAIM.yaml` say fractional chi_f = 25/3, which is unverified and irrelevant to p2.
   - INDEX.csv is narrower: it only states n=19, e=92, kappa=5, 9-critical against "BGS 40 graphs n12 to 16 and Sulanke n11".

The package disclaims p1 and the full win.

## Verdict
p2 is met literally. The graph is a simple, exact, edge-critical 9-chromatic, explicitly biplanar graph on 19 vertices. The reservations:
- The non-isomorphism step is essentially trivial, since it works by order against a hash list reconstructed from third-party files.
- Novelty against later literature is outside my role.
- The DRAT proof is checked only by the package's own verifier.

confirmed_scope: An explicit simple 19-vertex, 92-edge graph (object/biplanar_9crit_n19_e92.json) is edge-critical 9-chromatic (confirmed independently for chi <= 9 and for all 92 edge-deleted 8-colourings; chi >= 9 via the package's own DRAT check, run_checks.sh printing PASS), splits into two layers (45 and 47 edges) whose rotation systems each give V-E+F = 2 on a single component, and has an order and a canonical hash different from every one of the 42 reconstructed Sulanke and BGS-pool graphs; the extras 5-connected, non-join and (by my own check) clique-cutset-free also hold, but the BGS list is reconstructed rather than taken from the paper, and these extras are not part of p2.

pass: true
