# REPRODUCE verdict: brouwer-qary-unrestricted-a3-a4-a5, cell A4(12,8)
context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, RECORD.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-20T14:06:21Z

## Definition used

A_q(n,d) is the largest number of distinct words in {0,...,q-1}^n with every pairwise Hamming distance >= d. From the success criterion in CLAIM.md: "an explicit list of M distinct words over {0..q-1}^n (q in {3,4,5}) such that an independent script confirms all pairwise Hamming distances >= d, and M is STRICTLY GREATER (direction: max) than the lower bound for A_q(n,d) in the corresponding live table". Here q = 4, n = 12, d = 8.

## Object file

- `object/A4-12-8-145words.txt`, sha256 c2fd2cd5a942d6381693303c92e3f4ad107ad0a2f5565239dc443a55a6e24d6b (matches CLAIM.md).
- 1 header line starting with `#`, 145 codeword lines, one trailing newline; no other content.

## Checker written from the definition (Python 3 standard library, all pairs, no sampling)

Output of my own program:

- malformed lines (length != 12 or a symbol outside {0,1,2,3}): 0
- distinct words: 145 of 145
- pairs checked: 10440 (= 145*144/2), minimum Hamming distance 8
- distance distribution: d=8: 5940, d=10: 3456, d=12: 1044
- M = 145; M > 128 (lower bound in RECORD.md): True; M <= 240 (upper bound in RECORD.md): True
- Two runs gave byte-identical output (deterministic).

## Independent rebuild from the construction in words

I coded the action (p, s): v[p(i)] = s(w[i]) with A: p(i) = 5i+1 mod 12, symbols fixed; B: p(i) = i+2 mod 12, s = (0)(1 2 3). Closure of {A, B} under composition gives a group of order 36 (matches the claim). Orbit sizes of the five listed representatives: 1, 36, 36, 36, 36 (matches). The union has 145 words and is equal as a set to the object file (0 words in either difference).

## Table cell (from RECORD.md only; no web page fetched in this role)

RECORD.md gives lb 128, ub 240 for n = 12, d = 8, lb not `=`. I checked the column alignment of the quoted n = 12 rows for consistency: the last three ub values 48, 9, 4 fit d = 9, 10, 11 (Plotkin-type bounds: A4(11,9) <= 12 so A4(12,9) <= 48; A4(12,11) <= 5), and lb 262144 = 4^9 fits d = 3 (shortened quaternary Hamming code). That places 240/128 at d = 8, as RECORD.md states. Whether the live table still shows 128, and whether the improvement already appears elsewhere, is the novelty role's job and was not checked here.

## Problems found

None. Every property (length, alphabet, distinctness, minimum distance 8, size 145) holds on all pairs, the construction in words reproduces the file exactly, and 128 < 145 <= 240.

pass: true
