# Criterion skeptic: cubic-graphs-graceful-knuth-beyond-14

context: subagent (Grok Bot Task executor)
Read only: claim/ (CLAIM.md, REPRODUCE.md, checkers/, inputs/, result/). Scratch copy: /workspace/crit-cubic/ (not part of the claim).

## What was checked this session (2026-11-01, America/New_York)
1. `sha256sum -c result/SHA256SUMS.txt`: all 10 certificates OK.
2. Built geng and labelg from inputs/pynauty-2.8.8.1.tar.gz (nauty 2.8.8) following REPRODUCE.md. Sanity check: `geng -cu -d3 -D3 16` gave 4060 and `geng -cu -d3 -D3 18` gave 41301.
3. My own C checker (mycheck.c, written here without looking at glab.c) does its own graph6 decode, requires zero padding bits, exactly n vertices, 3n/2 edges, every degree 3, connectivity by union-find, exactly n non-negative integer labels, labels distinct and in [0,3n/2], and the multiset of edge differences equal to {1..3n/2}, each once. Result: bad=0 for every order. Line counts: n=4:1, 6:2, 8:5, 10:19, 12:85, 14:509, 16:4060, 18:41301, 20:510489, 22:7319447. Negative test: one label changed in a cert_16 line was rejected.
4. checkers/coverK.sh (checkK + labelg canonical forms + a fresh full geng regeneration; n=22 used 64 res/mod slices) printed:
   - COVERK n=16 cert_lines=4060 dup_canon=0 geng_count=4060 A002851=4060 sets_equal=yes PASS
   - COVERK n=18 cert_lines=41301 dup_canon=0 geng_count=41301 A002851=41301 sets_equal=yes PASS
   - COVERK n=20 cert_lines=510489 dup_canon=0 geng_count=510489 A002851=510489 sets_equal=yes PASS
   - COVERK n=22 cert_lines=7319447 dup_canon=0 geng_count=7319447 A002851=7319447 sets_equal=yes PASS
   I did not run checkers/checkP.py. The literal criterion does not need it.

## Criterion (a), clause by clause
- "one file per order": result/cert_16.txt, cert_18.txt, cert_20.txt, cert_22.txt. Met.
- "each graph (graph6, as produced by nauty geng -c -d3 -D3 n …)": the canonical-form set of each file equals the canonical-form set of a fresh geng -c -d3 -D3 n run. Met.
- "an independent checker regenerates the complete list": coverK regenerates the full geng list. It shares nauty with the producer but not glab.c. Separately, the list is complete without relying on geng: there are 7,319,447 pairwise distinct canonical forms (n=22, likewise for the other orders), each a connected cubic graph, and that number equals A002851. Met.
- "confirms the counts 4,060 / 41,301 / 510,489 / 7,319,447": all four counts match. Met.
- "matches every generated graph to a certificate entry by canonical form": sets_equal=yes and dup_canon=0, so the match is a bijection. Met.
- "labels are distinct integers in [0, 3n/2] and the edge differences are exactly {1,...,3n/2}": checked by two separate checkers (checkK and mine), 0 bad. Met.
- Hidden quantifiers: "every connected cubic graph" means simple graphs, which is what geng and A002851 count. Each of the four orders is fully covered, with no sampling and no "up to" hedge. A null model is not relevant here: the criterion asks for an exhaustive certificate, and each labeling is verified exactly.
- Re-read clause ("orders already covered there do not count"): CLAIM.md's status record says DS6 28th ed. (Oct 30, 2025) gives 4..14, and Knuth's pre-fascicle 7A (Dec 5, 2024, exercise 96) covers the 4060 connected cubic graphs on 16 vertices. So order 16 does not count as new, and p1 alone would earn nothing. The clause discounts covered orders. It does not cancel a certificate that also settles uncovered ones. Orders 18, 20 and 22 are not covered by any cited source (Kennedy 2021 and OEIS A337965 also stop at 16), and the certificate settles all three. Under the hard reading, where the presence of 16 voids (a), (a) could never be met once 16 was known. Even then, the result is strictly stronger than p2 and p3 and subsumes both. Either way it is a non-subsumed win: (a) is the top tier, and the new content (18, 20, 22) is not contained in any partial or in the literature. Caveat: I did not reopen DS6 or Knuth's pages myself (out of scope). The novelty of 18–22 rests on the status record in CLAIM.md.
- Option (b) is not claimed and not relevant.

## Verdict
The full criterion (a) is met as literally written. The contribution beyond the literature is orders 18, 20 and 22. Order 16 is included but already known (Knuth 7A).

confirmed_scope: Every connected (simple) cubic graph on 16, 18, 20 and 22 vertices is graceful, as certified by result/cert_16.txt, cert_18.txt, cert_20.txt and cert_22.txt (4,060 / 41,301 / 510,489 / 7,319,447 graphs, canonically identical to a fresh nauty 2.8.8 geng -c -d3 -D3 n run with no duplicates, every labeling verified graceful by two checkers), of which orders 18, 20 and 22 are new relative to the sources cited in CLAIM.md.
pass: true
