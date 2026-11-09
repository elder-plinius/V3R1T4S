# CRITERION skeptic — panel report

context: subagent
date: 2026-10-31 (America/New_York)
inputs used: the original claim workspace (not shipped in that form; see object/, verify-it-yourself/, and the-record-we-beat/). No live MinT fetch, no literature search.

## Claim as stated (the original claim document (not shipped; see README.md))
"The 17 matrices in net_F2_t11_m24_s17.txt are generator matrices C_1..C_17 in F_2^{24x24} of a digital (11,24,17)-net over F_2 (b = 2, m = 24, s = 17, t = 11)."
Cell: b=2, m=24, s=17. Claimed t=11.

## Partial wins
None named in the original claim document (not shipped; see README.md) or elsewhere in the original claim workspace (not shipped) (no "partial" text anywhere in the package). Only the full criterion applies.

## Literal checklist

### Object form
- b = 2 is in MinT's list; prime field, so no field model needed. PASS.
- 17 blocks, each 24 rows x 24 digits in {0,1}, so C_i is in F_2^{24x24}. Re-parsed independently: all 17 matrices have full rank 24 (rows 14..24 are unit-vector completion; they don't affect t=11).
- sha256 values match REPRODUCE.md (net c3c441c5…, first13rows a4b71877…). The first 13 rows of each C_i in the two files are identical.

### (1) Digital (t,m,s)-net, every composition checked: PASS
- k = m - t = 13; number of compositions of 13 into 17 non-negative parts = C(29,16) = 67,863,915.
- verify-it-yourself/netcheck_b.c (C, generic F_q arithmetic, incremental echelon basis, recompiled by me): `PASS q=2 m=24 s=17 t=11 k=13 compositions_reached=67863915` (about 21 s). Same result on the first13rows file.
- the original Python checker (not shipped; package checker: verify-it-yourself/check_net.py) (pure Python, XOR bitmask basis, prefix-monotone last block, counts certified against comb(k+s-1,s-1)): `PASS q=2 m=24 s=17 t=11 k=13 compositions_certified=67863915 expected=67863915` (about 79 s).
- I read both checkers. They use different languages, data representations, and elimination code. Both enumerate every composition. Each one stops only when a prefix is linearly dependent, which makes every extension of that prefix fail too, so the early stop is sound. Both counts equal C(29,16).

### Two independent checkers agree: PASS
Agreement confirmed by re-running both. One caveat: both checkers come from the same package author, so they are independent in implementation only, not in authorship.

Extra spot-check (the criterion spot-check script (not shipped), my own plain Gaussian elimination):
- 30,000 random compositions: 0 failures.
- All 17x17x14 compositions supported on one or two coordinates: 0 failures.

### Null models / controls: PASS
- Same net at t=10 (k=14): `FAIL` (compositions_reached=22649). So t=11 is exact for this object, and the checker can return FAIL.
- Random 17 x (24x24) F_2 matrices (seed 1) at t=11: `FAIL`, and at t=13: `FAIL`. A trivial or random object doesn't pass, even at MinT's current value.

### (2) t STRICTLY SMALLER than MinT "Constructive and digital" on the live query page: PASS on the recorded snapshot
- the original MinT query snapshot (not shipped; see the-record-we-beat/TABLE_SNAPSHOT.md) (http://mint.sbg.ac.at/query.php?b=2&m=24&s=17&p=smt) shows "(13, 24, 17)-Net over F 2 — Constructive and digital" (s-reduction of a digital (13,24,24) shift-net).
- 11 < 13 is strict. The cd/bd table (cell 13-8) and the cd/ed excerpt (Digital existence t=13) agree.
- Caveat on "live … at verification time": the evidence is a single same-day WebFetch snapshot taken by the scout on 2026-10-31 (sha256 recorded in the original table record (not shipped; see the-record-we-beat/TABLE_SNAPSHOT.md)). I did not re-fetch, because my scope is limited to the original claim workspace (not shipped). If the panel protocol requires a fresh live fetch, a non-restricted agent has to confirm it.

### (3) t >= MinT digital lower bound: PASS
- The query page gives lower bound 8 ("There is no (7,24,17)-net in base 2", LP bound for OOAs).
- The cd/bd table, labelled "Lower bound on t (digital)", shows 13-8 at m=24, s=17.
- 11 >= 8. No sign of a bug.

### (4) No paper, preprint or table already gives a digital (11,24,17)-net over F_2: NOT ASSESSED HERE (deferred to NOVELTY)
- Inside the package, nothing gives t <= 11 for this cell.
- No MinT entry makes the claim stale by propagation. In the m=24 row, digital t=11 is reached only at s <= 14 (s=13: 11-10, s=14: 11), and s=15 is already 12. So no s'>=17 entry gives t <= 11, and nothing larger subsumes the claim.
- The post-2008 literature check is NOVELTY's job. This pass does not cover (4).

## Hidden quantifiers / stretches found
- "for every composition … checked exhaustively": satisfied literally. Both checkers' counts equal C(29,16).
- "live MinT query page at verification time": met only by a same-day recorded snapshot, not a fetch at panel time. This is a minor temporal stretch. It is disclosed in the original table record (not shipped; see the-record-we-beat/TABLE_SNAPSHOT.md).
- "Two independent rank checkers": independent in code, not in authorship. My own sampled spot-check adds weak third-party support, not a third exhaustive check.
- Not a stretch, but notable: t=11 also beats MinT's "Digital" (existence) entry of 13. It doesn't only beat the constructive one. That is consistent with the claim, and it makes the novelty check in (4) more important.
- Wording: the claim says "digital (11,24,17)-net over F_2", which is exactly the criterion's object. It doesn't claim to improve a (t,s)-sequence, the m→∞ row, or non-digital nets.

confirmed_scope: The 17 explicit 24x24 F_2 matrices in object/net_F2_t11_m24_s17.txt (sha256 c3c441c5…) generate a digital (11,24,17)-net over F_2, verified exhaustively over all 67,863,915 compositions by two independently implemented checkers, which is strictly below the MinT "Constructive and digital" value t=13 and at or above the lower bound t=8 as recorded for (b,m,s)=(2,24,17) on 2026-10-31, with literature novelty (criterion 4) not assessed here.

pass: true
