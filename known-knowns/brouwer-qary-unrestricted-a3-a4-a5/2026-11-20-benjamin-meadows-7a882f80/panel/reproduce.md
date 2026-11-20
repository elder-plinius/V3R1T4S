# REPRODUCE verdict: brouwer-qary-unrestricted-a3-a4-a5, cell A4(12,7)
context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, RECORD.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-20T14:06:02Z

## Definition used

From the success criterion quoted in CLAIM.md: "an explicit list of M distinct words over {0..q-1}^n (q in {3,4,5}) such that an independent script confirms all pairwise Hamming distances >= d, and M is STRICTLY GREATER (direction: max) than the lower bound for A_q(n,d) in the corresponding live table". Here q = 4, n = 12, d = 7; bounds taken from RECORD.md: lower 256, upper 1167.

## Checker (own code, Python 3 standard library, written before reading the word list)

Run on `object/A4-12-7-320words.txt`, all pairs, no sampling. Output:

- sha256 7a882f805e40e7ef6a9565684cc1c36d616b91f2d3081be69aef2d00dfe69d82 (matches CLAIM.md)
- header lines 1 (starts with `#`), blank lines 0
- words 320, malformed lines 0 (every line exactly 12 characters from {0,1,2,3})
- distinct 320
- pairs checked 51040 of expected 51040
- minimum distance 7, pairs below 7: 0
- 320 > 256: True; 320 <= 1167: True

## Independent rebuild from the construction in words

Own implementation of the action v[p(i)] = s(w[i]) with g1 = (i -> i+2 mod 12, s1: 0->0, 1->2, 2->3, 3->1) and g2 = (i -> 11i mod 12, s2: 0<->1, 2 and 3 fixed).

- closure of the generators: group order 48 (matches the claim)
- orbit sizes of the 11 listed representatives: 24, 48, 24, 48, 48, 16, 24, 48, 12, 16, 12, each equal to the claimed size; no orbit overlaps an earlier one
- sum of orbit sizes 320, union size 320
- rebuilt set == word set of the object file: True (0 words only in the rebuild, 0 only in the file)

## Determinism

The checker was run three times with the same printed result; the full output of two of those runs was hashed and the hashes were identical (sha256 92d61633a3e70089eea24259bb8f3e5217df96654ef23cd5e31a7e7ae106051a).

## Sources

No web page was fetched for this role; the bounds 256 and 1167 are taken from RECORD.md as the brief directs. Whether the live table still shows lower bound 256, and whether the result is already known, belongs to the novelty role.

## Problems found

None. Length, alphabet, distinctness, minimum distance 7, size 320 and the orbit construction all reproduce exactly. The header line's description (generators, symbol maps 0123 -> 0231 and 0123 -> 1023) agrees with the construction in CLAIM.md.

## Reasoning

The file is a valid quaternary code of length 12, size 320, minimum distance 7, so A4(12,7) >= 320. It is reproducible from the stated group and orbit representatives alone. 320 is strictly above the recorded lower bound 256 and below the upper bound 1167, so it is consistent with the table and meets the size condition of the success criterion.

pass: true
