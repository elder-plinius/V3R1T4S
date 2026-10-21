# Shannon capacity of C11: Theta(C_11) >= 5.295492757 from a degree-210 schedule in the Buys-Polak-Zuiddam grammar

## What

For C11 only, the schedule in object/schedule.json (BPZ grammar, d = 210, M with 153 digits) gives Theta(C_11) >= M^(1/210) strictly above the BPZ Lean repository head value and the 9a.md comment value, assuming the Lean-certified base vector and the BPZ framework; no explicit independent set is exhibited.

In numbers: M has 153 digits, so Theta(C_11) >= M^(1/210) = 5.29549275705422970542530964715933628230581897086303, against the BPZ Lean repository value 5.29549231578462014255077898586171222761333914484062 (degree 207). The exact margin is +0.00000044126960956287453066129762405469247982602241. The object is a recursion (object/schedule.json, with the substitution tables and terminal codes in object/rules.json), not a list of words.

## Check it yourself

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: python3 3.8 or later, standard library only, no network.
- **Rough laptop time**: a few seconds.
- **Expected last line**: ALL CHECKS PASS

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| BPZ Lean repository, CertC11.lean at head aa21eeb12b75 (degree 207) | C11 | 5.29549231578462014255077898586171222761333914484062 | https://github.com/spectra-research/shannon-capacity-lean | 2026-10-20T03:45:32Z (panel: 2026-10-20T03:14:57Z) |
| 9a.md comment, BPZ version 1 value | C11 | 5.294502522149 | https://github.com/teorth/optimizationproblems/blob/main/constants/9a.md | 2026-10-20T03:45:32Z (panel: 2026-10-20T03:14:29Z) |
| Ours | C11 | **5.29549275705422970542530964715933628230581897086303** (degree 210) | object/schedule.json | not applicable |

The 9a.md page prints the C11 value only in a comment under its C7 table and has not been updated to the Lean repository values. Tandon (arXiv:2608.30273), Gao (arXiv:2607.27869) and Itty, Rosin, Carstensen and Reichman (arXiv:2607.21517) treat C7 or give smaller values for this cycle. The arXiv listings were searched on 2026-10-20 and showed nothing newer than Tandon (31 Aug 2026). Source hashes, HTTP status and the re-fetch made immediately before packaging are in the-record-we-beat/. The panel's novelty report is panel/novelty.md.

## Not claimed

- The margin is small, about 4.4e-07 in the bound, and the step is a re-tuning inside the published Buys-Polak-Zuiddam framework (a different schedule with the same rules, terminal codes and base sizes as their Lean-verified CertC11). It is not a new method.
- The base seven-family vector comes from BPZ's Lean-verified data. The explicit base vertex sets are not shipped here, and this package does not re-run the Lean build. The substitution tables and terminal codes were checked for separation (Definition 6) in the checker and tested on explicit vertex sets by the panel, and the checker reproduces the Lean integer from the Lean schedule as a known answer. This exact schedule has not been through Lean's kernel.
- No explicit independent set is exhibited (it would have about 10^152 elements). Nothing is claimed for any other cycle, or for the true value of Theta(C_11).
- The literature search was limited by arXiv rate limits: the arXiv export API returned HTTP 429 and the panel used the arXiv HTML search listings instead. A newer paper that the listings missed is possible.
- Records in this field move every few weeks. Re-fetch the live records (9a.md, the Lean repository, arXiv) before merging; the comparison holds for the versions recorded in the-record-we-beat/.
- Corrections to the contributor's own write-up (how-we-built-it/RESULTS.md): wrong paper titles and dates in its prose, wrong C7 codebook sizes, wrong decimals from about digit 42 for some values. The shipped JSON is correct and agrees with the checker to the last digit; the checker here does not use the prose.
- Not peer reviewed. It was checked by a three-skeptic panel (panel/) and by the standalone checker shipped here.

## Filing history

New find, not a refile of an earlier pull request.

## Credits

- **Pjotr Buys, Sven Polak and Jeroen Zuiddam**, *Lean-verified lower bounds for the Shannon capacity of odd cycles*, arXiv:2607.29681 (submitted 31 Jul 2026), and the Lean 4 repository https://github.com/spectra-research/shannon-capacity-lean (head aa21eeb12b75): the seven-family framework, the combining rules, the terminal codes, the base port systems and the Lean-verified values this package compares against. Every schedule here is built in their grammar. Please credit them when using it.
- **Ravi Tandon**, *Strengthening Recursive Constructions for Zero-Error Shannon Capacity*, arXiv:2608.30273 (submitted 31 Aug 2026): the gadget calculus and the definitions (Definitions 4 and 6) the checker follows. Companion repository https://github.com/tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion.
- **Yu Gao**, *A Recursive Construction Improving the Lower Bound on the Shannon Capacity of C_7*, arXiv:2607.27869 (submitted 30 Jul 2026): the gadget and product lemma the later work generalises.
- **Nathaniel Itty, Christopher D. Rosin, Chase Carstensen and Daniel Reichman**, *Improved lower bounds for the Shannon capacity of odd cycles*, arXiv:2607.21517 (submitted 23 Jul 2026, last revised 30 Jul 2026).
- The independent sets that the BPZ Lean repository names as the basis of its constructions: Baumert, McEliece, Rodemich, Rumsey, Stanley and Taylor (1971); Codenotti, Gerace and Resta (2003); Polak and Schrijver (arXiv:1808.07438); De Boer, Buys and Zuiddam (arXiv:2404.16763), as listed in that repository's README.
- The optimization-constants repository https://github.com/teorth/optimizationproblems (page constants/9a.md): the primary table this claim is compared against. No person is named for it because no maintainer name was verified in a fetched source for this package.
- The search agent Gemini (called Argon), working for the contributor calgulbenkian.
