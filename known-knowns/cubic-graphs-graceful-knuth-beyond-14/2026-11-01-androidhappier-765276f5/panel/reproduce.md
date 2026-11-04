# REPRODUCE skeptic: cubic-graphs-graceful-knuth-beyond-14

context: subagent (Grok Bot Task executor)
Date: 2026-11-01, 11:56 to ~12:25 America/New_York (EST). This was a fresh context. I read only the files under claim/ and worked on a scratch copy. The original claim/ was not written to.

## Definition used (quoted from claim/CLAIM.md, criterion (a), verbatim bank text)
"a certificate that every connected cubic graph on 16, 18, 20 and 22 vertices is graceful: one file per order giving each graph (graph6, as produced by nauty geng -c -d3 -D3 n or genreg) with a graceful labeling, where an independent checker regenerates the complete list, confirms the counts 4,060 / 41,301 / 510,489 / 7,319,447 (A002851), matches every generated graph to a certificate entry by canonical form, and checks that the labels are distinct integers in [0, 3n/2] and the edge differences are exactly {1,...,3n/2}"

## Method
I wrote my own checker without reading any author code. I did not open checkers/checkK.c, checkP.py, coverK.sh, glab.c or run_all.sh.
1. Integrity: `sha256sum -c result/SHA256SUMS.txt` passed for all 10 certificate files, cert_22.txt included.
2. My checker (C, written from the definition) reads each line of result/cert_n.txt. It does a strict graph6 decode: n must match, the length must be exact, bytes must be in 63..126, and pad bits must be zero. It then checks the following:
   - every degree is 3 and there are 3n/2 edges;
   - the graph is connected (BFS);
   - there are exactly n labels, plain decimal integers, with no extra tokens;
   - the labels are distinct and lie in [0, 3n/2];
   - the |f(u)-f(v)| over the edges are pairwise distinct and cover all of {1..3n/2}.

   It writes out the graph6 column. Negative tests failed as expected: a wrong difference set, a label above 3n/2, a missing label, a non-cubic graph6, and a disconnected cubic graph (2K4 at n=8).
3. Regeneration: I built nauty 2.8.8 geng and labelg myself from inputs/pynauty-2.8.8.1.tar.gz with plain `gcc -O3` and default MAXN, not the author's flags. I ran `geng -cq -d3 -D3 n`:
   - n ≤ 18: one unsliced run per order;
   - n = 20: res/mod slices 0/64 .. 63/64, concatenated in order;
   - n = 22: res/mod slices 0/64 .. 63/64, run 6 in parallel, all 64 finished OK, concatenated in order.
4. Matching: for each n, I first compared the certificate's graph6 column byte-for-byte with the regenerated geng list. Then I canonicalized both lists with labelg, sorted them, and checked that the canonical sets are identical and contain no duplicates.

## Results (all orders present: 4,6,8,10,12,14,16,18,20,22)
| n | cert lines | my per-line check | geng count | A002851 (inputs/b002851.txt) | direct graph6 match | canonical sets equal, all distinct |
|---|---|---|---|---|---|---|
| 4..14 | 1/2/5/19/85/509 | 0 bad | 1/2/5/19/85/509 | match | identical | yes |
| 16 | 4060 | 0 bad | 4060 | 4060 | identical | yes (4060 distinct) |
| 18 | 41301 | 0 bad | 41301 | 41301 | identical | yes (41301 distinct) |
| 20 | 510489 | 0 bad | 510489 | 510489 | identical | yes (510489 distinct) |
| 22 | 7319447 | 0 bad | 7319447 | 7319447 | identical | yes (7319447 distinct) |

The geng counts also agree with the bank's numbers 4,060 / 41,301 / 510,489 / 7,319,447.

## Determinism
- Re-running geng for n=18 gave the same sha256 (d8dc3116...).
- Re-running my checker on result/cert_22.txt gave the same output column sha256 (6fa6d454...). That value is also the sha256 of my regenerated n=22 geng list.
- My checker exited with rc=0 for every order.

## Caveats (non-blocking)
- Generation and canonical forms both rely on nauty 2.8.8 (geng and labelg), which the criterion explicitly allows. I did not do a separate non-nauty isomorphism check.
- The nauty source was taken from the pynauty sdist that ships in claim/inputs. Its tarball sha256 is 454d3b0e605d649d13478afb090daef4a152f15c4a337a391fe69fded7e683f2, and the claim does not pin this hash. The counts matching A002851 at every order is an independent anchor for the regeneration.
- Only reproduction was checked. Novelty and status, including whether 18/20/22 are already covered in the literature, are outside this file.

## Verdict
Every property in criterion (a) was checked exhaustively at n = 16, 18, 20 and 22, and at 4..14, with no mismatch, missing object or non-determinism.

pass: true
