# REPRODUCE verdict

context: codex exec (fresh context via codex-fresh)

The exact mathematical verification completed, but the submitted package fails the requested mismatch-free criterion. `SHA256.json` contains an incorrect hash for the saved `REPRODUCE.md`. No supplied files were repaired.

Definition quoted from `GAME.md`: “Independently at each round, choose one of the three unordered pairs with probability 1/3 and choose which member wins with probability 1/2. The loser transfers the smaller of the two pre-round stacks to the winner. Stop at the first zero stack. The function f(x,y,z) is the probability that player 1 is the player eliminated at that stopping time.”

I checked this against the saved source `data/paper.txt`, abstract, Section 1, and Conjecture 9 in Section 5.3. I wrote `review/independent.py`, including its rational geometry and game recurrence, before opening any supplied implementation. I subsequently translated that recurrence into `review/affine.cpp`; neither fresh checker imports supplied checker or prover code.

All 9,839 nodes and all 6,561 leaves were checked. Geometry was reconstructed using exact rational hulls and edge intersections. The roots cover all three orderings, including the open edges for `z=y` and `z=x`; every split includes its equality child. All nodes are uniquely reachable, and none are unfinished. Every leaf's four integer bounds was independently recomputed, including every depth override. No sample or incomplete node range was accepted.

| Ordering | Nodes | Leaves | Depth: leaf count | Recomputed minimum |
|---|---:|---:|---|---|
| leader | 128 | 86 | 7: 86 | 181/1399680 |
| middle | 7 | 5 | 3: 5 | 1/135 |
| shortest | 9704 | 6470 | 12: 2260, 13: 4210 | 379/1813985280 |

Thus the completed certificate checks establish `f(x,y,z)-f(y,y,z) >= 379/1813985280 > 0` for every admissible real triple. The derivation of each analytic step is saved in `review/proof_derivation.md`: six-outcome Bellman recurrence; survival bound `2^-n`; the universal `4/5` enclosure; all resolved, tied, and unresolved pair bounds; relative-interior sign tests; normalization and partition coverage; strict separation; and integer-range safety. In particular, the general affine dot-product bound is below `2^111` in signed 128-bit arithmetic, and `5*6^18=507799783342080<2^49`.

The supplied `portable/run.py` also completed every leaf and reported `PASS`; all three complete transcript hashes matched `portable/expected.json`. Its full transcript was compared leaf by leaf with the fresh affine transcript. A second full fresh affine run exited zero and reproduced the first transcript byte for byte:
`9812fc60a9f2bb0ba9464850ecc64a32c4c0a6205479105bf93d71cf6bca658c`.
The fresh kernel made 2,838,620,577 recursive calls, with a maximum memo size of 11,572, maximum absolute affine coefficient 8,128, and maximum absolute sign dot product 7,936. It uses one CPU thread; the repeat recorded peak resident memory of 3,538,944 bytes. Review and portable outputs occupied 2,588,925 bytes when measured. No delegation was used.

The integrity failure is exact:

- Manifest: `SHA256.json`; entry: `REPRODUCE.md`.
- Recorded SHA-256: `910223b4d085dc448cf0ef8a447fa3389080ed19633c2e0665792d0907cb960f`.
- Actual SHA-256: `4db1cc257dd48cdf14f6a9731cc0bf47f3bf06df1e5c0dce3ebc5ebb6730463d`.

The other 27 entries in that manifest match. All 71 entries in `TRANSPORT_SHA256.json` match, including its different, correct hash for `REPRODUCE.md`; no listed object is missing. This does not remove the contradiction in the supplied older manifest. Under “Fail on any mismatch,” the overall verdict is false despite the completed mathematical reproduction.

Evidence: `review/summary.json`, `review/geometry.json`, `review/affine.bounds.txt`, `review/affine.repeat.bounds.txt`, `review/affine.repeat.json`, `review/portable.first.stdout`, `review/integrity.json`, and `review/proof_derivation.md`. The first fresh run reached `ALL_VERIFIED 6561`; its external timing wrapper then failed on an unavailable system-statistics query. The clean repeat supplies the successful child exit receipt and identical full transcript.

pass: false