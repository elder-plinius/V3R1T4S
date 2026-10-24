# Connective constant of the 4.8^2 lattice: an exact-rational upper bound 169287/92732 = 1.825551051 (partial win p1, pocket-pruned loop length 34)

## What

Assuming the exact ratio 169287/92732 on the matrix defined by object/AUTOMATON.md and the shipped vector is reproduced, mu(4.8^2) <= 1.825551050339 is a proved rigorous upper bound (Grimmett-Li Theorem 4.3 and Proposition 4.2 for bridge growth, a complete pocket-pruning proof), below Alm's published 1.829254 and the bank's 1.82926 by about 3.7e-3, meeting p1 for the 4.8^2 lattice only.

(The first clause is the criterion skeptic's wording, quoted by the gate. The reproduce skeptic then reproduced the exact ratio; see panel/reproduce.md.)

The object is the rounded positive test vector (16-bit mantissa) of a finite-memory loop-avoiding-walk automaton with loop length 34 on the square-octagon (4.8^2) lattice, with two finite-pocket pruning tests. The states are not shipped: the checker rebuilds the 16,873,086 states from the definition in object/AUTOMATON.md, applies the two pocket tests to every move (26,331,184 moves kept, 2,507,806 pruned by test 1, 1,217,699 pruned by test 2), verifies the ordered subset-inclusion condition of object/THEOREM.md on every candidate it examines, and computes max (Px)_i / x_i exactly as a fraction. The proof that the pruned matrix still bounds mu is object/THEOREM.md; it uses the Grimmett-Li bridge theorem (see Not claimed).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- Requirements: python3 3.8 or later, standard library only, the fork start method (Linux or macOS); about 8 GB of memory in the coordinating process (7.6 GB peak measured) and under 1 GB in each of 3 worker processes; about 150 MB of temporary disk; no network.
- Time: about 35 to 45 minutes on an Apple-silicon Mac (the builder's runs took 2,025 s and 2,550 s on a machine shared with other jobs), longer on a slower or busy machine. A driver that enforces a timeout needs at least 3000 s (5400 s is safer on slow machines).
- Expected last line: ALL CHECKS PASS (the line before it is PASS, and above that: exact max (P x)_i / x_i = 710041141248 / 388946198528 = 169287/92732 = 1.825551050339).

The object is kept as 15 binary parts (13,312,188 bytes in all, each part at most 900,000 bytes) listed with their sha256 in object/SHA256_PARTS.txt. The script first checks every object file against SHA256SUMS, then reassembles the parts and checks the sha256 of the whole (13118758b86bc0f0daef592d3e85d353851556e54dcd07ad93b6a1c52fc26e54) and of every part, runs two negative controls on the first 3000 states, and then runs the full check.

The submission id (2026-10-19-calgulbenkian-13118758) takes its last eight hex digits from the sha256 of the main object, the reassembled whole vector object (the concatenation of object/vector_part_00.bin to vector_part_14.bin, the file vector.xz), which is 13118758b86bc0f0daef592d3e85d353851556e54dcd07ad93b6a1c52fc26e54 (the line WHOLE in object/SHA256_PARTS.txt). The first eight hex digits of that whole-object hash are 13118758; FIRST8 is not taken from any single part.

## Compared to

The bar is Alm's published 1.829254. Jensen's Table 3 prints the same figure rounded as 1.82926.

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| S. E. Alm, J. Phys. A 38 (2005) 2055-2080, section 5.1.3 and summary table (manuscript copy read from the Internet Archive) | 4.8^2 rigorous upper bound | 1.829254 (the bar used here) | https://web.archive.org/web/2010id_/http://www2.math.uu.se/research/pub/Alm3.pdf | 2026-10-19T06:32:57Z |
| I. Jensen, J. Phys. A 37 (2004) 11521, Table 3 (arXiv cond-mat/0409381) | 4.8^2 upper bound | 1.82926 (Alm's figure, rounded; credited there to Alm via a private communication from Parviainen) | https://arxiv.org/abs/cond-mat/0409381 | 2026-10-19T05:20:01Z |
| R. Parviainen, Uppsala Dissertations in Mathematics 34 (2004), thesis summary (Internet Archive copy) | no other 4.8^2 upper bound in the summary | none | https://web.archive.org/web/2020id_/http://uu.diva-portal.org/smash/get/diva2:164546/FULLTEXT01.pdf | 2026-10-19T06:37:18Z |
| arXiv API queries on connective constants of Archimedean lattices, Alm-type bounds, finite-memory automata and pocket pruning, run by the novelty skeptic for this claim | no later 4.8^2 bound | none found | https://export.arxiv.org/api/query | 2026-10-19T15:51:36Z to 15:51:49Z |
| arXiv 2601.12571v2 and two further arXiv queries (criterion skeptic) | no 4.8^2 numeric bound | none found | https://arxiv.org/pdf/2601.12571v2 | 2026-10-19T16:04:07Z |
| Open pull request #534 of this repository (the k = 32 bound this package replaces), listing seen by the novelty skeptic | 4.8^2 upper bound | 18108999119/9912056861 = 1.826966832 | https://github.com/elder-plinius/V3R1T4S/pull/534 | 2026-10-19T15:52Z |

This claim: 169287/92732 = 1.825551050339 (rounded up; the true quotient is 1.82555105033861). Below Alm's 1.829254 by 3.703e-3 (below the rounded 1.82926 by 3.709e-3), and below the k = 32 bound of #534 by 1.416e-3. The bank's required margin is 1e-6. Metadata for every fetch (HTTP status, sha256) and the literature search are in the-record-we-beat/ and panel/novelty.md. The panel's criterion report is panel/criterion.md.

## Not claimed

- Only the 4.8^2 lattice and only loop length 34 with the two pocket tests of object/AUTOMATON.md. No claim for the square lattice (the main criterion of the target), the triangular or kagome lattices, or any other loop length. This is the partial win p1 only, not the target's main criterion.
- The certified bound is for the shipped vector, which is rounded to a 16-bit mantissa to fit the package limit. It sits 2.8e-5 above the figure the contributor's team reported for the same automaton with its full-precision vector (19360805483/10605620094 = 1.825523195381). That lower figure is not claimed and not shipped. Other mantissa lengths computed on the same automaton and not shipped: 12 bits 1.825968878, 14 bits 1.825634611, 15 bits 1.825578906.
- The bound is only as good as the written proof in object/THEOREM.md, which is the contributor team's own and is not published or peer reviewed. The proof rests on a published theorem we did not prove: the Grimmett-Li bridge theorem (Theorem 4.3 with Proposition 4.2 of "Locality of connective constants"), which says bridge growth equals the connective constant for graphs with a unimodular graph height function. THEOREM.md checks each hypothesis for the 4.8^2 lattice (translations by 3Z^2, four orbits, free action, difference-invariant height x, neighbours of greater and smaller height). The panel skeptics re-derived those checks against the fetched text and found them right, but a reader who doubts that application doubts this bound. The checker does not check the proof; it checks the matrix, the pocket decisions, the subset-inclusion invariant and the exact ratio.
- The pocket-pruning tests are new relative to the k = 30 and k = 32 bounds. No published source for this exact pruning was found; the novelty skeptic found only related ideas (see Credits) and says it cannot exclude a published treatment, because Alm 2005 and Parviainen's thesis were not readable to it in full and Google Scholar, MathSciNet and zbMATH were not searched.
- The pruned automaton bounds bridges, not all self-avoiding walks; it reaches mu only through the Grimmett-Li theorem. The matrix does not bound the walk counts c_n.
- Cross-family review: before the panel, the proof and checker were reviewed read-only by a model of a different family (OpenAI gpt-6.1-sol, verdict clean with fixes, seven findings, all applied before the panel and confirmed present by the reproduce skeptic). That review was not repeated after the fixes, and its text is not in this package. The three panel skeptics are Claude Code subagents; the object's builder (Gemini, Argon) is a different family from every skeptic. Not peer reviewed.
- The contributor's generator (how-we-built-it/saw_bounds_2d.c) has an indexing slip in its second pass (candidate lists are indexed by all free neighbours, not only kept ones). A corrected copy gives the same 16,873,086 states and the same ratio, and the checker follows the corrected definition in AUTOMATON.md. The shipped generator is the original, uncorrected file; the corrected copy is not shipped. In the checked run no second-pass candidate is present in the final state set (count 0), so the slip, and the generator's 32-candidate limit that the definition drops, have no numerical effect here.
- The certificate is the rounded vector alone; the states and transitions come from the written definition. This is a weaker form of certificate than a shipped transition list. The vector's tie to the states is the breadth-first state order of AUTOMATON.md; the evidence for that order is that the checker, a second program written by the reproduce skeptic from the definition, and the compiled generator copy all give the same exact fraction.
- The decision "infinite component" in the pocket tests follows the generator (breadth-first search with an enlarged bounding box and a cap of 4096 discovered vertices). The cap could only turn a finite component into "infinite", which keeps a move (the safe direction); the checker fails on any cap hit and reports 0, and THEOREM.md section 5 shows the cap is unreachable by counting.
- The lattice and symmetry checks run on finite windows (+-9 and +-12) and rely on period 3 of the lattice.
- The search for a later, better bound covered the indexed record only (arXiv queries, Crossref and OpenAlex cited-by lists for the k = 30 claim, and the full texts of Jensen 2004, Couronne 2022, He 2025, arXiv 2509.04568, Alm 2005 as a manuscript copy and a summary of Parviainen's thesis). Google Scholar, MathSciNet and zbMATH were not searched. Absence of a better bound in unindexed or paywalled sources cannot be excluded.
- The certificate (a 3,250,641,775-byte text file) was regenerated by the orchestrator from the contributor's generator (how-we-built-it/saw_bounds_2d.c, command saw_bounds_2d 482 34 cert_482_k34.txt 2) and is byte-identical (sha256 7079b8598c07cfe5724b5a126210c224082600b4c96c6015626f92949f19a204) to the file on the contributor's laptop, as reported to us. Only a rounded copy of its vector is shipped, and the checker does not trust the generator.
- The choice of loop length 34 is post hoc (the operator chose it to replace k = 32 and k = 30 in #534). The claim is one exact certified number.

## Filing history

- PR #534 was first filed on 2026-10-19 with the k = 30 bound 1.8281442934 (package 2026-10-19-calgulbenkian-5b68e2eb).
- It was updated the same day to the k = 32 bound 18108999119/9912056861 = 1.826966832 (package 2026-10-19-calgulbenkian-90ff73f1).
- It now carries the k = 34 pruned bound 169287/92732 = 1.825551051 (this package, 2026-10-19-calgulbenkian-13118758), which is strictly stronger than both.

This package replaces the k = 32 package inside the open PR #534, on the operator's in-session instruction to update #534 in place. #534 is not a refile of a closed pull request. Nothing has been pushed or posted from this folder.

## Credits

- **Sven Erick Alm**, "Upper and lower bounds for the connective constants of self-avoiding walks on the Archimedean and Laves lattices", J. Phys. A 38 (2005) 2055-2080 (section 5.1.3: mu < 1.829254 for the 4.8^2 lattice; the transfer-matrix upper-bound method; his remark on discarding dead-end walks is the closest published relative of the pruning here, as described in He's paper, Remark 2.5). Read from https://web.archive.org/web/2010id_/http://www2.math.uu.se/research/pub/Alm3.pdf. This is the bar we compare against.
- **Olivier Couronne**, "New upper bound for the connective constant for square-lattice self-avoiding walks", arXiv 2211.16146 (2022), https://arxiv.org/abs/2211.16146: a modified finite-memory automaton for the square lattice that excludes areas enclosed by a small loop, the same family of idea as the pocket pruning here, by a different rule. Read in full text by the novelty skeptic.
- **Andre Ponitz and Peter Tittmann**, "Improved upper bounds for self-avoiding walks in Z^d", Electron. J. Combin. 7 (2000), Research Paper 21 (title and venue as cited in Couronne's reference list; we have not read this paper): the finite-memory automaton for self-avoiding walks that the automaton used here is a variant of.
- **Qidong He**, "Upper bounds for the connective constant of weighted self-avoiding walks", arXiv 2508.01993 (2025), https://arxiv.org/abs/2508.01993, with the open software https://github.com/qidong-he/weighted_connective_constant: an Alm-type method with public code. Read in full text; it contains no 4.8^2 bound and none of its code was used.
- **Geoffrey R. Grimmett and Zhongyang Li**, "Locality of connective constants", https://www.statslab.cam.ac.uk/~grg1000/papers/loc-6.pdf (fetched and read by the builder and by two skeptics): the Bridge theorem (Theorem 4.3 with Proposition 4.2) on which the proof of the bound for mu rests.
- **Iwan Jensen**, "Improved lower bounds on the connective constants for two-dimensional self-avoiding walks", J. Phys. A 37 (2004) 11521, https://arxiv.org/abs/cond-mat/0409381: Table 3, where the 4.8^2 upper bound 1.82926 is listed (the baseline table).
- **Robert Parviainen**, thesis "Connectivity Properties of Archimedean and Laves Lattices", Uppsala Dissertations in Mathematics 34 (2004): the figure 1.82926 in Jensen's table is credited to Alm via Parviainen's private communication. Read as an 11-page summary from an Internet Archive copy.
- The pocket pruning (the two finite-pocket tests, the ordered subset-inclusion invariant and the proof in THEOREM.md) is the contributor team's own adaptation of ideas of Alm, Couronne and Ponitz-Tittmann, as far as we found; no published source for this exact pruning was found.
- Contributor credit: calgulbenkian. The search code is by the contributor's AI search agent (Gemini, called Argon); see how-we-built-it/.
