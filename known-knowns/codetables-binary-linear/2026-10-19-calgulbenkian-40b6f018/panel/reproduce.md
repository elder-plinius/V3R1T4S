context: Claude Code subagent, fresh context [claude-sonnet-5-5]
cell: bklc-q4-n157-k10-d102   role: reproduce

The contributor's hash list: 13 files listed, 0 not OK (checked from inside the package folder).

## Definition (quoted from the claim's own criterion, verbatim)
"Success means a k x n generator matrix over GF(q) with these properties. (1) Rank is exactly k over GF(q), computed independently. (2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when feasible ..., never by sampling. (3) d is STRICTLY GREATER (direction: max) than the lower bound in the live http://www.codetables.de/ cell for (q,n,k) at verification time, and at most the upper bound. (4) The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from them, and no newer arXiv claim already reaches that d."
GF(4) here: symbol v = a + 2b stands for a + b*w with w*w = w + 1 (as stated in verify-it-yourself/mindist_gf4.py). Clauses (3) and (4) concern the live table and the literature: I used only the live bounds recorded in the-record-we-beat/ (no network; currency of the table is another skeptic's job). Clause (4) is not decidable from the folder.

## My checker (written before opening verify-it-yourself/)
My enumerator (C, written from scratch, not shipped in this package): reads the 11 x n matrix (made by my own converter script from the object), packs each row as two GF(4) bit planes (a and b parts), builds the four multiples of each row (0, r, w*r, w^2*r; w*(a+bw) = b + (a+b)w; it asserts w^2*r = r + w*r), then depth-first enumerates ALL 4^k messages, XOR-accumulating (GF(4) addition), takes the weight as popcount(a OR b), and counts messages that give weight 0 (rank test: none may exist among nonzero messages). Sanity test of the program on the hexacode [6,3,4]_4: it printed min_distance=4, A_d=45, weights 4:45, 6:18 (the known enumerator), and a deliberately broken variant gave d=3.
Range checks: every matrix entry is in 0..3 and every row has length n (asserted in my converter and in the C reader).

## Command and real output
    (own converter from object/*.json to a text matrix, then own C enumerator run on it; neither is shipped in this package)
n=157 k=10 messages=1048575 expected=1048575 zero_weight_nonzero_msgs=0 rank_k=true min_distance=102 A_d=5304
lowweights: 102:5304 104:8109 106:20358 108:25347

Claimed: d = 102, A_d = 5304, live lower = 101, live upper = 110 (from the-record-we-beat/). My result: min distance 102, A_d 5304, messages enumerated = 4^10 - 1 (counter equals the expected number), no nonzero message gives the zero word (rank 10). Strictly above live lower: True; at most live upper: True.

## Author's checker, run only after mine (sh verify-it-yourself/run_checks.sh in a private copy of the package)
== mindist_gf4.py (exact minimum distance by full enumeration of all 4^10 messages; rank; comparison with the live bounds)
{"n": 157, "k": 10, "messages_nonzero": 1048575, "expected": 1048575, "rank_k": true, "min_distance": 102, "A_d": 5304, "claimed_d": 102}
PASS rank k: True; exact d=102; live lower=101 (d > lower: True); live upper=110 (d <= upper: True); A_d=5304
== second implementation in C (only if a C compiler is available)
n=157 k=10 messages=1048575 rank_deficient=no min_distance=102 A_d=5304
C implementation agrees
== negative control: generator row 2 replaced by a copy of row 1 (rank deficient) (must be rejected)
PASS (negative control rejected)
ALL CHECKS PASS
Agreement with mine: min distance, A_d and rank identical. No mismatch, no missing object, deterministic (both runs repeated the same numbers).

## Notes

Open question on a structurally different method (MacWilliams or Brouwer-Zimmermann): not run; my C program is a third implementation of full enumeration (own GF(4) arithmetic and own packing), so it is independent code but the same idea. Full enumeration of all 4^k codewords is exact, and the criterion allows it when feasible (4^11 is about 4.2 million).

pass: true
