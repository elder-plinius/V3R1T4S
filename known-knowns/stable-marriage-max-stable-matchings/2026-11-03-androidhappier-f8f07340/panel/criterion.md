# CRITERION skeptic — stable-marriage-max-stable-matchings, n = 9
context: subagent (executor CRITERION)
inputs: claim/ only (CLAIM.md, TABLE.md, REPRODUCE.md, instance_n9.prefs, programs/, data/, closure_probe/). No attempts/, NOTES, REPORT or other panelists read.

## Literal criterion check
- n >= 6: n = 9. OK.
- Explicit complete strict lists: claim/instance_n9.prefs has 18 rows, each a permutation of 1..9; sha256 matches CLAIM.md (f8f07340…5de1). OK.
- Two independent exact methods agree: brute force over all 9! matchings (claim/programs/allperm.c) = 412; rotation-poset count (claim/programs/smcount3.c) = 412 with lattice verification 412; claim/programs/count_stable.py lattice 412 / brute 412. I also wrote my own brute-force counter (from scratch, ~15 lines), which gives 412. OK.
- Bar = composition closure, not the stale A357271 data line:
  - Published n=9 instances: A357271/A069156 data 330; A371810 288; Ong et al. file (claim/data/a357271_1.txt) 365, which I recounted from claim/data/ong_n9.prefs: 365. A web search this turn found no other published n=9 instance. The repo's known-knowns covers only n=13 and 15 (claim/TABLE.md).
  - Compositions reaching order 9 (no doubling, since 9 is odd): 3x3 lexicographic product = 93 (claim/closure_probe/p33.prefs, recounted). Disjoint unions: 268·1, 85·2 = 170, 48·3, 16·10, all < 412. Block sums with frozen within-block orders and hill-climbed cross placement: the saved best is 8 (Z2^3 Latin, 268) ⊕ 1 = **366** (claim/closure_probe/bs_8_1.prefs, recounted). I reran the probe (90 s per run): 8⊕1 hit 366 on 3 seeds; Jo7⊕2 got ≤252; Ong7⊕2 226; 6⊕3 192; 5⊕4 251. So the best closure value found is 366, and 412 > 366 > 365 strictly.
  - Null model: the seed (8⊕1 with the new agents at the bottom) = 268. The local search moved it to 412, which beats every composition baseline tested.
- Not a composition of known instances: in the 8x8 restriction to the old agents, 5 lists (m3, m8, w1, w2, w4) differ from the Z2^3 Latin seed. That matches CLAIM.md. Stronger check: I counted all 81 restrictions that delete one man and one woman. The maximum is 198, so no 8x8 sub-instance is the 268 Latin instance (or any 268 instance). I counted all 1296 restrictions to 7x7. The maximum is 54, so no 7x7 sub-instance is Jo's 85 or Ong's 81. So this is not even a broad "known block plus cross placement" of any published 7 or 8 instance. CLAIM.md says it is not a composition and names its seed. OK.
- Conjecture-exact rule: n = 9 is not in {6, 8, 10, 12, 16}, so no extra recount is needed.
- One cell: yes (n = 9 only).

## Caveats (none fail the criterion)
1. Claim wording: CLAIM.md's headline compares against 365 ("largest published"). The criterion bar is the composition closure, and the claim's own probe puts that at ≥ 366 (unpublished block sum). The headline should cite 366 as the closure value found. The margin is unaffected: 412 > 366.
2. The closure is only a lower bound from heuristic search over block-sum cross placements, not an exhaustive maximum. Even so, every structured composition (product, disjoint union, Thurber 330) is far below 412, and repeated 8⊕1 runs plateau at 366.
3. No PREREG file is in claim/, so I could not check PREREG/claim consistency from this folder. The claim is internally consistent with REPRODUCE.md and TABLE.md.

confirmed_scope: The order-9 instance claim/instance_n9.prefs (sha256 f8f0734081c8c613267257d617d9393d5ad591782b802beaa72c8b1639f35de1) has exactly 412 stable matchings, counted by brute force and by the rotation-poset method, which is strictly more than every published order-9 instance (max 365, Ong et al.) and every composition of published instances found (max 366, Z2^3 Latin order-8 ⊕ one pair block sum), and it contains no published order-7 or order-8 instance as a sub-instance.
pass: true
