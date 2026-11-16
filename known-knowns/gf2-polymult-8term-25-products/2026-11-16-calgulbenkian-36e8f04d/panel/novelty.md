context: Claude Code subagent, fresh context [Sonnet 5.5]

# Novelty report: 81-gate GF(2^7) multiplier, modulus x^7+x^3+1 (object/gf128_0x89_81gates.slp.txt)

## Status source (read once, no retries)
- 2026-11-16T02:43:03Z https://csrc.nist.gov/projects/circuit-complexity/list-of-circuits, HTTP 200: "GF(2^7) mod x^7+x^3+1, 40 AND, 45 XOR, 85 total, depth 5". Same page: x^7+x^4+1 is 84. (The circuit-complexity project page, 02:43:24Z, also HTTP 200.)
- 2026-11-16T02:43:25Z https://www.cs.yale.edu/homes/peralta/CircuitStuff/CMT.html, HTTP 200: x^7+x^3+1, "circuit with 85 gates and depth 5"; best earlier published is 100 gates.
- 2026-11-16T02:44:18Z onward, GitHub API for usnistgov/Circuits tree (master, not truncated): data/slp/gf holds gf128-730-mult.slp (header: X^7+X^3+1), gf128-740, gf256, gf64 only. The NIST repository's last commits (14 Nov 2026) concern S-boxes. No GF(2^7) circuit under 85 there.
So the status source is readable and the baseline is 85. The claim's 81 is strictly below it.

## Closest prior object: Swapnil Jain, gf2m-circuits (Oct 2026)
Fetched the repo metadata, commits, releases (none), branches (main only), and raw multipliers/circuits/final_f73.slp and final_f73_d6.slp (2026-11-16T02:44Z, HTTP 200). Header: "GF(2^7) poly 0x89 gates=83 K=32"; 32 AND + 51 XOR, depth 6. Last push 2026-10-11. The repo's other GF(2^7) circuit is final_f7 (0x91, 87 gates), and nothing in the tree is a 0x89 multiplier under 83. Poly 0x89 is x^7+x^3+1. So the best published object I found is 83, and 81 beats it by 2. The package already names Jain as the bar.

## Trivial-edit test
I ran the object through the package's checker: PASS, 81 gates (32 AND, 49 XOR), 16384 pairs, depth 6. I compared its 32 AND-product forms (as pairs of linear forms of the inputs) with Jain's 83-gate circuit. Both have the same product count (32) and the same style of 14 input-side XORs, so the family is shared. The set of products is not identical: about 18 of 32 forms coincide and the rest differ. The post-AND linear layer is different, with 35 XORs against 37. This is therefore not a deletion, relabelling or local polish of Jain's netlist. It is a different split (the package says 3+4 with 3x3 schoolbook plus a 4x4 Karatsuba, against Jain's orientation) feeding a better reduction layer. A reader could still call it a same-family variant that wins 2 gates by changing the split orientation, since the multiplicative core is the same size and technique. That is a mild risk, not a defeat: it beats the published object by an explicit, verified margin, which a symmetry or relabelling of Jain's circuit would not give. The package does not say it was seeded from Jain, and I found no evidence it was copied.

## Searches (named)
- WebSearch: "Swapnil Jain GF(2^7) multiplier 83 gates circuit 2026"; "low gate count GF(2^7) multiplier circuit x^7+x^3+1 AND XOR gate count improved Peralta"; "gf2m-circuits ... Lean 4 preprint Jain"; "arXiv 2026 GF(2^8) multiplier 115 gates AES polynomial fewer than 117 gates circuit". None found any GF(2^7) x^7+x^3+1 multiplier under 85 other than Jain's repo (which search did not surface; I found it through the package pointer). Jain's accompanying preprint could not be located by search, so I could not read what it states for GF(2^7). I rely on the repo files above.
- V3R1T4S repo, read-only gh: PR searches for "GF(2^7)", "gf128", "gf2 multiplier", "polymult", "multiplier gates", "83 gates", "x^7", "swapnil" returned only closed bank PR #667 (the target entry) and unrelated PRs. TROPHY_CASE.md has no GF multiplier rows. Tree search for gf2/gf128/jain found only a working file (not shipped). No competing or earlier merged circuit for this cell.
- NIST list also shows no smaller published count for neighbouring cells that would restrict to this one (GF(2^7) x^7+x^4+1 is 84, GF(2^6) 57); a different modulus is a different function, so it gives no bar.

## Limits
Jain's preprint, and any paywalled literature (none specific identified), were not read. Web search is weak for new arXiv or ePrint items, so a very recent unlisted paper cannot be ruled out. The package's own fetch of Jain's head (9daf883e) was not independently re-pinned by me beyond the files above.

novelty verdict: the claim strictly beats the NIST/CMT 85 and Jain's 83 under the same metric; I found nothing at or below 81 published.

pass: true
