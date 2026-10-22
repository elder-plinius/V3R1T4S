context: Claude Code subagent, fresh context [claude-sonnet-5-5]
cell: bklc-q4-n163-k11-d104   role: reproduce

The contributor's hash list: 13 files listed, 0 not OK (checked from inside the package folder).

## Definition (quoted from the claim's own criterion, verbatim)
"Success means a k x n generator matrix over GF(q) with these properties. (1) Rank is exactly k over GF(q), computed independently. (2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when feasible ..., never by sampling. (3) d is STRICTLY GREATER (direction: max) than the lower bound in the live http://www.codetables.de/ cell for (q,n,k) at verification time, and at most the upper bound. (4) The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from them, and no newer arXiv claim already reaches that d."
GF(4) here: symbol v = a + 2b stands for a + b*w with w*w = w + 1 (as stated in verify-it-yourself/mindist_gf4.py). Clauses (3) and (4) concern the live table and the literature: I used only the live bounds recorded in the-record-we-beat/ (no network; currency of the table is another skeptic's job). Clause (4) is not decidable from the folder.

## My checker (written before opening verify-it-yourself/)
My enumerator (C, written from scratch, not shipped in this package): reads the 11 x n matrix (made by my own converter script from the object), packs each row as two GF(4) bit planes (a and b parts), builds the four multiples of each row (0, r, w*r, w^2*r; w*(a+bw) = b + (a+b)w; it asserts w^2*r = r + w*r), then depth-first enumerates ALL 4^k messages, XOR-accumulating (GF(4) addition), takes the weight as popcount(a OR b), and counts messages that give weight 0 (rank test: none may exist among nonzero messages). Sanity test of the program on the hexacode [6,3,4]_4: it printed min_distance=4, A_d=45, weights 4:45, 6:18 (the known enumerator), and a deliberately broken variant gave d=3.
Range checks: every matrix entry is in 0..3 and every row has length n (asserted in my converter and in the C reader).

## Command and real output
    (own converter from object/*.json to a text matrix, then own C enumerator run on it; neither is shipped in this package)
n=163 k=11 messages=4194303 expected=4194303 zero_weight_nonzero_msgs=0 rank_k=true min_distance=104 A_d=7956
lowweights: 104:7956 106:11934 108:35100 110:55089

Claimed: d = 104, A_d = 7956, live lower = 103, live upper = 113 (from the-record-we-beat/). My result: min distance 104, A_d 7956, messages enumerated = 4^11 - 1 (counter equals the expected number), no nonzero message gives the zero word (rank 11). Strictly above live lower: True; at most live upper: True.

## Author's checker, run only after mine (sh verify-it-yourself/run_checks.sh in a private copy of the package)
== mindist_gf4.py (exact minimum distance by full enumeration of all 4^11 messages; rank; comparison with the live bounds)
{"n": 163, "k": 11, "messages_nonzero": 4194303, "expected": 4194303, "rank_k": true, "min_distance": 104, "A_d": 7956, "claimed_d": 104}
PASS rank k: True; exact d=104; live lower=103 (d > lower: True); live upper=113 (d <= upper: True); A_d=7956
== second implementation in C (only if a C compiler is available)
n=163 k=11 messages=4194303 rank_deficient=no min_distance=104 A_d=7956
C implementation agrees
== negative control: generator row 2 replaced by a copy of row 1 (rank deficient) (must be rejected)
PASS (negative control rejected)
ALL CHECKS PASS
Agreement with mine: min distance, A_d and rank identical. No mismatch, no missing object, deterministic (both runs repeated the same numbers).

## Notes
The live lower bound is 103.
Open question on a structurally different method (MacWilliams or Brouwer-Zimmermann): not run; my C program is a third implementation of full enumeration (own GF(4) arithmetic and own packing), so it is independent code but the same idea. Full enumeration of all 4^k codewords is exact, and the criterion allows it when feasible (4^11 is about 4.2 million).

pass: true
