context: subagent

# Reproduce

Definition, quoted from the claim:

> a binary code corrects s adversarial deletions when distinct codewords have disjoint sets of length n-s subsequences. Equivalently, every pair has longest common subsequence at most n-s-1. Here n=16 and s=3, so every pair must have LCS at most 12. Words are length 16 over {0,1}, distinct.

Independent checker written from that definition before reading pycheck.py. It does not import pycheck.py. It checks every word for length 16 and alphabet {0,1}, distinctness, pairwise disjoint sets of length-13 subsequences (all C(16,3) deletions), and pairwise LCS at most 12.

## Independent checker on code.txt

```
file_sha256=a272712b10be2718ba8ef2024f38207d4aa2d66ed36c29f56db9a2e2185499bb
n=16 s=3 subseq_len=13 lcs_at_most=12
size=43
distinct_subseq_13=2234
subseq_collisions=0
pairs=903
max_lcs=12
worst_pair indices=(0,1) lcs=12
worst_a=0000000000000000
worst_b=0000111100000000
lcs_violations=0
ACCEPT
size=43 max_lcs=12 limit=13 subseq_disjoint=yes
```

Exit status 0. sha256 matches the claimed object hash. All 43 words and all 903 pairs were checked. Worst pair LCS 12 agrees with the zero-count of `0000111100000000` against the all-zero word.

## Independent checker on a one-bit mutation of the first word

First word `0000000000000000` with the last bit flipped to `0000000000000001`; the other 42 words unchanged.

```
file_sha256=58963fd0111bfcc6f152fd7d1f5e65fdbba9428557b7adc48f29eef1be0b3f24
n=16 s=3 subseq_len=13 lcs_at_most=12
size=43
distinct_subseq_13=2234
subseq_collisions=1
first_subseq_collision words[0]=0000000000000001 words[34]=0000000000001111 sub=0000000000001
pairs=903
max_lcs=13
worst_pair indices=(0,34) lcs=13
worst_a=0000000000000001
worst_b=0000000000001111
lcs_violations=1
REJECT
reason: subsequence sets not pairwise disjoint
reason: pairwise LCS exceeds 12
```

Exit status 1. Hand check: those two words share the length-13 subsequence `0000000000001`.

Not every one-bit flip of the first word fails. Flipping bit 0, 1, or 2 (leftmost is bit 0) still has max LCS 12 and no length-13 subsequence collision. Flipping bits 3 through 15 is rejected. The negative control above is a real violation, not a blanket reject.

## Author checker

Command: `python3 pycheck.py 16 3 code.txt`

```
n=16 s=3 size=43
max_lcs=12 limit=13
ACCEPT
size=43 pairwise=903
```

Exit status 0.

Same checker on the last-bit mutation of the first word:

```
n=16 s=3 size=43
CONFLICT 0000000000000001 0000000000001111 lcs=13
max_lcs=13 limit=13
REJECT conflicts=1
```

Exit status 1.

pycheck.py uses the LCS equivalent (conflict if LCS >= n-s = 13). It agrees with the independent subsequence-set check on code.txt and on the mutation.

Confirmed: 43 distinct length-16 binary words, pairwise LCS at most 12, disjoint length-13 deletion-subsequence sets, and a one-bit mutation of the first word rejected by both checkers.

pass: true
