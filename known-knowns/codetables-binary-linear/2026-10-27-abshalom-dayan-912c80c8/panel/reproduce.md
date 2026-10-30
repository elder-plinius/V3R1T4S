# REPRODUCE skeptic verdict: [29,19,8] code over GF(9)

Bottom line: CONFIRMED. G in claim/object/code_q9_n29_k19_d8.json has rank 19 over GF(9). The code it generates
has minimum distance exactly 8. My own two exhaustive checkers, written before I opened claim/checkers/, show that no
nonzero codeword has weight 7 or less. I found an explicit weight-8 codeword in the row space. All of the author's
REPRODUCE.md outputs match the expected text line for line. The rebuild gives a byte-identical object
(sha256 912c80c8ee946bc6021522350a436fb9510b39e1565175a0a0fc380d0216f9e7). No mismatch, no missing object and no
non-determinism.

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

Run started 2026-10-27 01:56:51 UTC (date -u). Live cell fetched 01:59:30 UTC.

## Definition used (quoted)

- Minimum distance: "the smallest Hamming weight of a nonzero codeword", where the codewords are the row space of G
  (task statement). The success criterion asks for "two independent exact minimum-distance implementations that
  agree; never by sampling" (claim/CLAIM.md).
- Field: "GF(9) = GF(3)[w]/(w^2 - w - 1); a + b*w encoded as a + 3b (0..8)" (the object file).

## My checker (mine/, written from the definition only)

- mine/gf9.py builds the GF(9) add and multiply tables from that convention, using w^2 = w + 1. It checks
  commutativity, associativity and distributivity over all triples, and checks that every element has a unique
  inverse. w^2 - w - 1 has no root in GF(3), so the quotient ring is a field.
- mine/prep.py checks the object's shape (q=9, n=29, k=19, entries 0..8) and computes the rank by RREF. It derives a
  parity-check matrix H (the 10 x 29 null-space basis of G) and checks G*H^T = 0 and rank(H) = 10. Output:
  `rank(G) = 19`, `rows of H = 10 rank(H) = 10`, `G*H^T == 0 verified`.
- mine/mind.c runs two exact tests, each over every subset (no sampling):
  - Test A (dual side). C = ker H, so a nonzero codeword of weight <= w exists iff some w columns of H are linearly
    dependent. It tests every w-subset for w = 1..8. Real output:
    `w=1..6: dependent=0` (29 / 406 / 3654 / 23751 / 118755 / 475020 subsets),
    `A: w=7 subsets=1560780 dependent=0`, `A: w=8 subsets=4292145 dependent=1557`
    (first dependent 8-set: columns 0 1 2 3 4 5 27 28). Since d >= 8, each dependent 8-set carries exactly one
    codeword up to scaling, so A_8 = 8 * 1557 = 12456.
  - Test B (generator side). A nonzero codeword supported inside T exists iff rank(G restricted to the columns
    outside T) < 19. It tests every 7-subset T. Real output:
    `B: 7-subsets T=1560780 with rank(G restricted to complement)<19: 0`.
- Negative control. In mine/neg_control.json, G's last row is replaced by a weight-6 vector, which keeps the rank
  at 19. Both tests catch it: Test A finds `w=6 dependent=72` and `w=7 dependent=1656`, and Test B finds `1656`.
  So the checkers can detect low-weight words.
- Witness (mine/witness.py, columns 0,1,2,3,4,5,27,28). G restricted to the other 21 columns has rank 18, which
  leaves a 1-dimensional left kernel. The message m = [1,1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1] gives
  c = m*G = 1 1 1 2 2 2 0 ... 0 1 1, with support [0,1,2,3,4,5,27,28] and weight 8. So d <= 8.
- Together: d = 8 exactly. Each test ran in about 1 s of CPU.

## Author's REPRODUCE.md (run in a copy, run_author/, so claim/ stays unmodified)

| Step | Author's expected output | Observed output | Match |
|---|---|---|---|
| 1 rebuild | sha256 912c80c8...f9e7 for both files | rebuilt.json and object both 912c80c8ee946bc6021522350a436fb9510b39e1565175a0a0fc380d0216f9e7; cmp byte-identical | yes |
| 3 m3_mindist | W=7 no codeword (1560780 subsets); first weight-8 word after 253 subsets; witness 2 2 2 1 1 1 0..0 2 2 | identical lines (rank=19, W=1..7 all clear) | yes |
| 4 hdep 8 | rank=19, nodes=2182648, dependent_min=8 d=8 | identical | yes |
| 4 dualenum + macwilliams | dual_words=3486784401; sum A = 9^k; A_1..A_7 = 0; A_8 = 12456; d = 8 | identical; dual distribution sums to 3486784401 = 9^10; dual min weight 16 | yes |
| 5 witness_check | rank(G)=19; weight 8, in_rowspace=True, support [0..5,27,28] | identical | yes |
| 6 live cell | lower bound 7, upper bound 9 | HTTP 200, page sha256 fe750485b053225286430c77f5fa80a4686c4ea13208407331b2a126f5f63cf3, the same as the saved table/bklc_q9_n29_k19.html; text "lower bound: 7 upper bound: 9" | yes |

## Cross-checks between my checker and the author's

- The author's witness equals 2 times my witness, computed with my own field tables (`True`). Both are the same
  codeword up to a scalar.
- A_8 = 12456 from my subset count (8 * 1557) equals the author's MacWilliams A_8 = 12456. These come from
  different methods.
- Code reading: m3_mindist, hdep and dualenum each compute their own systematic form or H. Their logic is sound.
  The ternary Gray code in dualenum hits every element exactly once, because the digit map is triangular.

## Determinism

I ran my tests A and B and the author's m3 and hdep twice in sequence. Both runs gave the same output sha256
c6c7eaed316c5fee1e8af39b7f0bd3bb6b2eb627211538aa02a5a7bf4627bf5b. The dualenum output (run_author/dual.txt) has
sha256 dda35181c894c58cc8a213ec9a8775821f9b33a59b15c3f81157d351fecbb665.

## Scope and notes

- Rank 19 and d = 8 are verified exactly, three ways: my test A, my test B, and the author's three methods.
  8 > 7 (the live lower bound) and 8 <= 9 (the upper bound).
- Not checked here, because it is outside the reproduce role: criterion (4), novelty against LinCodeEvolve and newer
  arXiv claims.
- injection_suspected: none found.
- No background jobs left running. Scratch files are in mine/, run_author/ and live/ in the work folder.

pass: true
