# Shannon capacity of C7: Theta(C_7) >= 3.258834775 from a degree-560 schedule, above Tandon's 3.258832620

## What

Under ruling R9, the 3-branch S3b schedule with Tandon's 30-dimensional left gadget and terminal code K4a gives, via Tandon's Lemma 1, Theorem 1 and the BPZ combining rules (re-derived in writing and instance-tested here) and with every finite ingredient (G5, C1 to C4, codebook independence, condition 33, tables) verified computationally, an independent set of size M (288 digits) in C_7^{box 560}, so Theta(C_7) >= M^(1/560) = 3.25883477557614484751818055569792750605282670056114, strictly above the live record 3.25883262035326630912153905181047543760538759432195 as of 2026-10-20 04:46 UTC; the 560-dimensional set itself is not enumerated.

In numbers: the margin over Tandon (arXiv:2608.30273, d = 500) is +0.00000215522287853839664150388745206844743910623919, about 2.2e-06. The object is a recursion (object/schedule.json, with the substitution tables and terminal codes in object/rules.json), not a list of words. Tandon's own top-level schedule S3b joins three gadgets of dimensions 30, 55 and 40; here it joins three of dimensions 40, 60 and 40, all three built on his 30-dimensional left gadget.

## Check it yourself

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: python3 3.8 or later, standard library only, no network.
- **Rough laptop time**: about 2 to 3 minutes.
- **Expected last line**: ALL CHECKS PASS

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| 9a.md, top C7 entry (Tandon, d = 500, shown there to 8 decimals as 3.25883262) | C7 | 3.25883262035326630912153905181047543760538759432195 (recomputed by the checker from Tandon's Theorem 2 integer) | https://github.com/teorth/optimizationproblems/blob/main/constants/9a.md | 2026-10-20T04:53:02Z (panel: 2026-10-20T03:14:29Z; criterion skeptic: 2026-10-20T04:46Z) |
| Tandon, arXiv:2608.30273 abstract page (v1 only, submitted 31 Aug 2026) | C7 | same value | https://arxiv.org/abs/2608.30273 | 2026-10-20T04:53:03Z (panel: 2026-10-20T03:14:31Z) |
| BPZ Lean repository, CertC7.lean at head aa21eeb12b75 (degree 500) | C7 | 3.258827985920007 | https://github.com/spectra-research/shannon-capacity-lean | 2026-10-20T03:14:57Z |
| 9a.md rows for BPZ and Gao | C7 | 3.258805369885 and 3.258789153908 | same 9a.md | same as the first row |
| Ours | C7 | **3.25883477557614484751818055569792750605282670056114** (degree 560) | object/schedule.json | not applicable |

Itty, Rosin, Carstensen and Reichman (134,753 in C7^10, about 3.258020) and Polak and Schrijver (367 in C7^5, about 3.257866) are lower. The arXiv listings were searched by the panel on 2026-10-20 and showed nothing newer than Tandon (31 Aug 2026). Source hashes, HTTP status and the re-fetch made immediately before checking this package are in the-record-we-beat/. The panel's reports are in panel/.

## Not claimed

- **Ruling R9.** This claim stands only under a ruling by the orchestrator of this panel, quoted here: "Ruling: the composition rules may rest on a published theorem whose proof the panel re-derives in writing and tests on explicit instances; machine formalisation of the theorem is not required. Every FINITE ingredient (base gadgets, finite certificates, tables, terminal codes, and any finite admissibility conditions on codebooks) must be verified computationally in or by the panel." Without that ruling the cell would not have been confirmed.
- **The composition theorems are used as published results, not formalised.** Lemma 1, Theorem 1 and Proposition 1 are taken from Tandon's arXiv:2608.30273, which is a version 1 preprint by a single author. They are not machine-checked. The panel re-derived their proofs in writing (the criterion skeptic's written proofs are in panel/criterion.md, section 4, and verify-it-yourself/DERIVATION.md) and tested them on explicit vertex sets in small dimensions (verify-it-yourself/set_level_test.py, run by three agents). That is evidence, not a formal proof. A flaw in the preprint would break this claim.
- **Two earlier criterion reviews failed this cell.** Two earlier criterion skeptics judged it under a stricter reading, in which a machine-checked composition theorem is required, and failed it. This was before ruling R9 and before the claim folder was extended with the finite checks now shipped. The third review passed it under R9. The panel's reproduce and novelty reports were written before that extension; the object (schedule and integer M) did not change, and the live record was re-fetched by the third criterion skeptic at 2026-10-20T04:46Z.
- **What is verified by computer.** Every finite ingredient: the base gadget G5 (exhaustive), the certificates C1 to C4 (re-derived without Tandon's script), codebook independence and condition (33) at dimension 30 (by box structure), the separation property of every substitution table and terminal code, and the exact integer M and degree 560. The 560-dimensional independent set itself (about 10^287 words) is never enumerated.
- **The step is small and the cascade moves fast.** The gain is 2.2e-06 in the bound, a decimal step on a famous constant, obtained by using Tandon's 30-dimensional left gadget in all three branches of his top-level schedule instead of one. It is not a new method. Records for this constant have moved several times between July and September 2026 and are likely to move again within weeks. Re-fetch 9a.md and arXiv before relying on the comparison.
- Nothing is claimed about the true value of Theta(C_7), or about any other cycle.
- The literature search was limited: the arXiv export API returned HTTP 429, so the panel used arXiv's HTML search listings. A newer paper that those listings missed is possible.
- Corrections to the contributor's own write-up (how-we-built-it/RESULTS.md): wrong paper titles and dates in its prose, wrong codebook sizes, wrong decimals from about digit 42 for some values. The shipped JSON is correct and agrees with the checker to the last digit; the checker does not use the prose.
- Not peer reviewed. It was checked by a three-skeptic panel (panel/) and by the standalone checkers shipped here. The panel's skeptics are Claude Code subagents; the object's builder (Gemini, called Argon) is a different model family.
- In the claim files copied into verify-it-yourself/ (CLAIM.md, DERIVATION.md, REPRODUCE.md, RECEIPTS.md), the folder name table-record/ means the-record-we-beat/ in this package.

## Filing history

New find, not a refile of an earlier pull request.

## Credits

- **Ravi Tandon**, *Strengthening Recursive Constructions for Zero-Error Shannon Capacity*, arXiv:2608.30273 (submitted 31 Aug 2026): the gadget calculus, Lemma 1, Theorem 1, the 30-dimensional left gadget and its certificates, the S3b schedule, and the d = 500 value this package compares against. Companion repository https://github.com/tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion.
- **Pjotr Buys, Sven Polak and Jeroen Zuiddam**, *Lean-verified lower bounds for the Shannon capacity of odd cycles*, arXiv:2607.29681 (submitted 31 Jul 2026), and their Lean 4 repository https://github.com/spectra-research/shannon-capacity-lean (head aa21eeb12b75): the seven-family framework, the combining rules, the terminal codes and the base data. Please credit them when using this package.
- **Yu Gao**, *A Recursive Construction Improving the Lower Bound on the Shannon Capacity of C_7*, arXiv:2607.27869 (submitted 30 Jul 2026): the gadget and product lemma (Lemma 1) that the later work generalises.
- **S. C. Polak and A. Schrijver**, *New lower bound on the Shannon capacity of C_7 from circular graphs*, Information Processing Letters 143 (2019), 37 to 40 (arXiv:1808.07438): the 367-word independent set in C_7^5 that is the base gadget G5.
- **Nathaniel Itty, Christopher D. Rosin, Chase Carstensen and Daniel Reichman**, *Improved lower bounds for the Shannon capacity of odd cycles*, arXiv:2607.21517: the 134,753-word independent set in C_7^10 on which Gao's and Tandon's constructions build; compared against.
- The optimization-constants repository https://github.com/teorth/optimizationproblems (page constants/9a.md): the primary table this claim is compared against. No person is named for it because no maintainer name was verified in a fetched source for this package.
- The search agent Gemini (called Argon), working for the contributor calgulbenkian.
