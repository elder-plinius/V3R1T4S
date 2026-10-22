# REPRODUCE verdict

context: codex exec (fresh context via codex-fresh)

The claim passes exhaustive independent reproduction. All 9,839 nodes and 6,561 leaves were checked, including every equality stratum. The certified uniform lower bound is exactly **379/1813985280 > 0**. No missing object, hash mismatch, bound mismatch, unfinished leaf, or nondeterministic mathematical result was found.

## Definition and independence

The definition in GAME.md is:

> Start with three strictly positive real stacks (x,y,z). Independently at each round, choose one of the three unordered pairs with probability 1/3 and choose which member wins with probability 1/2. The loser transfers the smaller of the two pre-round stacks to the winner. Stop at the first zero stack. The function f(x,y,z) is the probability that player 1 is the player eliminated at that stopping time.

The saved source data/paper.txt, Section 5.3, states Conjecture 9 as “For x, y, z > 0 with x < y, f (x, y, z) > f (y, y, z).” This is the comparison in CLAIM.md and target.md; it is distinct from the paper's swapping theorem.

I wrote review/independent-design.md, review/check.py, and review/kernel.cpp before opening any supplied implementation, including portable/run.py, its geometry and integer kernels, and checker/fast_verify.py. Their pre-inspection hashes and timestamp are recorded in review/pre-code-read-receipt.json and were checked again at completion. The checker imports no supplied implementation. No delegation occurred.

## Integrity and exhaustive results

Both manifests were checked independently against file bytes and checked again after replay. SHA256.json matched all 28 entries; TRANSPORT_SHA256.json matched all 72 entries, including SHA256.json, REPRODUCE.md, QUICKSTART.md, and every portable source. The original input inventory contains exactly those 72 objects plus TRANSPORT_SHA256.json. No inference from the retry prompt was used. Detailed receipts are review/SHA256.json.receipt.json and review/TRANSPORT_SHA256.json.receipt.json.

| Certificate | Nodes | Leaves | Leaf depths | Recomputed minimum |
|---|---:|---:|---|---|
| certificates/leader.json | 128 | 86 | 86 at 7 | 181/1399680 |
| certificates/middle.json | 7 | 5 | 5 at 3 | 1/135 |
| certificates/shortest.json | 9704 | 6470 | 2260 at 12; 4210 at 13 | 379/1813985280 |

Every node was reached exactly once; every split's negative, equality, and positive closures were reconstructed with rational arithmetic. All roots, references, closures, leaf depths, and four stored bound numerators were checked. Pending and unresolved leaves are absent. The leaves comprise 1,291 points, 3,280 open segments, and 1,990 open polygons, including the external z=x and z=y strata. This is full continuous-domain coverage, not sampling.

The global minimum occurs at shortest node 2844, itself an open-segment leaf of depth 12. Its recomputed numerators are [2567485240, 2574177450, 2563485500, 2567482966]. Thus its gap is 2274/10883911680 = 379/1813985280. Every other leaf has at least this separation. Full receipts and per-leaf traces are review/leader.receipt.json, review/middle.receipt.json, review/shortest.receipt.json, and the corresponding review/leader.trace.jsonl, review/middle.trace.jsonl, review/shortest.trace.jsonl.

## Re-derived proof

The complete derivation and implementation audit are in review/analytic-audit.md. The essential implications are:

1. For each pair, an unequal smaller stack is eliminated when it loses and survives when it wins; a tie terminates in either direction. At most three of six outcomes survive, so P(T>n)<=2^-n and absorption is almost sure. At most two outcomes immediately eliminate player 1. With U=4/5, induction from H_0=0 gives H_(n+1)<=(2+3U)/6=11/15<=U. Increasing events give f=lim H_n<=U, and 0<=f-H_n<=2^-n. First-step conditioning gives the Bellman equation for the infinite-horizon f.
2. An affine form weakly nonnegative on all vertices and positive at one is strictly positive on the relative interior; all-zero vertex values mean an exact tie. Known comparisons therefore give exact game transitions throughout a region. An unresolved pair contributes at most 1+U when it contains player 1 and at most U otherwise, before division by six. Induction from [0,U] proves the computed intervals enclose infinite-horizon f. The denominator is 5*6^d at each leaf's actual depth.
3. Positive scaling commutes with every min-transfer transition. Normalizing by y+z in the leader case gives A=(a,b,1-b), B=(b,b,1-b), 0<a<b<=1/2. Normalizing by y in the other cases gives A=(a,1,c), B=(1,1,c), with 0<a<c<1 or 0<c<=a<1. The hard-coded roots exhaust precisely these domains, including their admissible equality edges.
4. A strictly crossing line partitions a parent's relative interior into the relative interiors of its two clipped closures and equality section. Exact edge intersections and convex hulls reconstruct these children. The exhaustive traversal proves that original excluded boundaries remain excluded and every admissible internal equality face is covered.
5. The independent kernel evaluates stacks at every vertex. Linear transitions and positive per-vertex common scaling preserve all subsequent comparison signs. Swapping players 2 and 3 preserves the recurrence. These facts justify its memoization without changing any bound. The explicit input/depth guards keep evaluated coordinates and numerators within signed 64-bit range; Python geometry and rational comparisons are unbounded. The supplied original kernel's coefficient-growth, path-count, and signed-128-bit dot-product bounds were also re-derived. No proof decision uses floating point.
6. Every admissible real triple reaches one verified leaf. There f(A)-f(B)>=L_A-U_B>=379/1813985280>0. Scaling back proves the claimed theorem for all positive real x<y and z. No continuity, fixed-total-stack assumption, or optimality assertion is required.

## Replay, determinism, and limits

After compiling review/kernel.cpp with C++17 and -O3, I ran python3 review/check.py twice over all certificates. Both runs passed. I also ran the exact preferred command python3 portable/run.py twice; both exited 0 and ended PASS. Their complete transcripts matched portable/expected.json and matched the independent computation at every leaf. The older checker/fast_verify.py and its dependencies were inspected; no partial run of that implementation is being counted as exhaustive evidence.

The independent jobs, geometry, integer outputs, and full per-leaf traces were byte-identical on repeat. The supplied geometry, workloads, and bound transcripts were also byte-identical. All non-timing replay stdout fields matched; elapsed-time and resource telemetry are excluded from mathematical determinism comparisons. See review/replay-audit.json, review/replay-audit.stdout, review/independent-first/, review/portable-run-1/, and review/portable-run-2/.

All proof computations ran sequentially with single-threaded kernels. The largest recorded child memory peak was 115,490,816 bytes. New disk usage was below 20 MB, well within 1 GB. The audit and this verdict were completed within the 40-minute cap. Scripts, the full analytic derivation, transcripts, and process/resource receipts are saved under review/. The original input files were unchanged.

pass: true
