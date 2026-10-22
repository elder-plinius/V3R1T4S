# Independent certificate reproduction

context: fresh subagent

Scope: certificate validity only. No novelty or literature finding is made here. Only the claim package was read; no attempts, scout material, or other panel reports were read.

## Definition and independence

`claim/target.md` defines the object as “an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even)”. `claim/CLAIM.md` specializes this to “2225 distinct binary words of length35 and weight6, with minimum pairwise Hamming distance at least6”.

I wrote and ran `panel/reproduce-evidence/check.py` from that definition before opening `claim/verify.py`. The independent checker checks every line's alphabet, length, and weight, requires exactly 2225 distinct words, verifies the claimed SHA256, and enumerates every unordered pair using integer XOR and population count. No pairs are sampled. The author's verifier was opened only after the independent run succeeded.

## Commands and results

Run from this run directory, using relative paths:

```sh
python3 panel/reproduce-evidence/test_check.py > panel/reproduce-evidence/tests.txt
python3 panel/reproduce-evidence/check.py claim/object/A35_6_6_2225.txt --n 35 --w 6 --d 6 --count 2225 --sha256 dc410a8170c014dec4c8b728a2da9d03dd29cc55a5f1c13fae80d22858d009de > panel/reproduce-evidence/result.json
python3 claim/verify.py claim/object/A35_6_6_2225.txt 2225 > panel/reproduce-evidence/author-result.txt
```

The independent result is 2225 words, all distinct, all binary, all length 35, all weight 6. All 2,474,200 unordered pairs were checked. The actual minimum distance is exactly 6. Distance counts are 134,252 at distance 6; 526,478 at distance 8; 1,094,176 at distance 10; and 719,294 at distance 12. The counts sum to 2,474,200 = 2225 × 2224 / 2.

Actual object SHA256:

```text
dc410a8170c014dec4c8b728a2da9d03dd29cc55a5f1c13fae80d22858d009de
```

This equals the claimed hash. Full machine output is in `panel/reproduce-evidence/result.json`. The author's separate verifier also reports PASS and the same cardinality, distance, pair count, and hash, as recorded in `panel/reproduce-evidence/author-result.txt`.

## Checker tests

`panel/reproduce-evidence/test_check.py` accepts the valid code {110000, 001100, 000011} with n=6, w=2, d=4 and checks its three distances are exactly 4. It deliberately submits and requires rejection of: a distance-2 pair under a distance-4 requirement, a duplicated word, a wrong-weight word, a wrong-length word, a nonbinary symbol, an incorrect cardinality, and an incorrect SHA256. All eight tests pass; exact results are in `panel/reproduce-evidence/tests.txt`.

The certificate establishes A(35,6,6) >= 2225. Whether this is a new improvement is outside this certificate-only review.

pass: true
