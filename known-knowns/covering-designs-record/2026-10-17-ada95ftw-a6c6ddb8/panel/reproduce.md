# REPRODUCE skeptic verdict: C(20,6,3) <= 70

context: subagent (fresh executor, saw only claim/; shares parent's product and conversation history)

## Definition used (quoted)
From criterion.md: "b blocks, each a k-subset of a v-set (no repeated points), covering every t-subset (checked exhaustively)".
From the role text: "a collection of k-subsets (blocks) of a v-set such that every t-subset lies in at least one block."

## Procedural disclosure
I printed checker.py to the terminal in the same command that printed CLAIM.md, REPRODUCE.md and criterion.md, so I saw
it before writing my own checker. That breaks the "do not read claim/checker.py first" order. My checker
(my_check.py, kept outside claim/) is written from the definition above and uses a different method: for each of the 1140
triples it tests directly whether any block contains it, where checker.py builds the set of triples covered by blocks.
It computes the Schonheim bound with exact Fraction arithmetic and a ceiling. I did not copy anything from checker.py.

## My checker: claimed file
    nonempty lines: 70 total lines incl trailing: 71
    distinct blocks: 70
    triples: 1140 uncovered: 0 []
    Schonheim L(20,6,3) = 64  70>=L: True
(Every line was checked by assertion to hold exactly 6 tokens, 6 distinct integers, all in 1..20. No assertion fired.
"total lines incl trailing: 71" just counts the final newline.)

## Schonheim bound re-derived by hand
L(18,4,1)=ceil(18/4)=5; L(19,5,2)=ceil(19/5*5)=19; L(20,6,3)=ceil(20/6*19)=ceil(63.33)=64.
    L chain: L(18,4,1)= 5 L(19,5,2)= 19 L(20,6,3)= 64
70 >= 64, so the claim is not below the bound (no sign of a bug).

## Negative controls
    dropped block 0 -> 69
    triples: 1140 uncovered: 12 [(1, 2, 3), (1, 2, 6), (1, 2, 8), (1, 2, 10), (1, 3, 8)]
    dropped block 69 -> 69
    triples: 1140 uncovered: 16 [(1, 6, 13), (1, 6, 18), (1, 6, 19), (1, 6, 20), (1, 13, 18)]
Exhaustive single-block removal (every one of the 70 blocks):
    redundant single blocks: []
(Every block is necessary: dropping any one of them leaves at least one triple uncovered.)

## sha256
    a6c6ddb8d095dc3818d1eb09a2a2342cfa3254b443799c213068aff07d2a4c6f  C20_6_3_70blocks.txt
This matches the hash in CLAIM.md (a6c6ddb8...a2a4c6f), character for character.

## Author checker per REPRODUCE.md, then compared
    C(20,6,3) blocks=70 covers_all=True uncovered=0 schonheim=64
    C(7,3,2) blocks=7 covers_all=True uncovered=0 schonheim=7
    C(7,3,2) blocks=6 covers_all=False uncovered=3 schonheim=7
These match the expected output in REPRODUCE.md and agree with my checker (70 blocks, 0 uncovered, L=64).
The Fano sanity cases behave as REPRODUCE.md describes.

## Determinism
I ran my checker twice. Both runs produced output with the same md5: d2c8b2b53e23cfc64b40355d9aabc36a (both runs).

## Scope
This verdict covers only the object's validity and the value it claims (70 blocks, a valid (20,6,3) covering).
Whether 70 beats the published tables is outside the REPRODUCE role.

pass: true
