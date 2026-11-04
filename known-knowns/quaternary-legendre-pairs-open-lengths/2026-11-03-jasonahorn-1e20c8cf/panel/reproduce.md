# REPRODUCE

context: subagent

Claim checked: no quaternary Legendre pair of length 70 whose two sequences are both constant on the orbits of either order-12 subgroup of (Z/70Z)* that does not contain -1. Partial win is that empty exhaustion, not a new pair.

## Definition used

From CLAIM.md. Digits 0,1,2,3 mean 1, i, -1, -i. PAF_X(k) = sum_j X_j conj(X_{j+k mod 70}). A pair requires PAF_A(k) + PAF_B(k) = -2 + 0i for every k = 1..69. Constant on the orbits means x[h*j mod 70] = x[j] for every h in the group and every j in Z/70Z.

Named groups, as sorted tuples:

- H1 = (1, 3, 9, 11, 13, 17, 27, 29, 33, 39, 47, 51)
- H2 = (1, 9, 11, 23, 29, 37, 39, 43, 51, 53, 57, 67)

Independent check, before reading search_two_groups.py: both are subgroups of (Z/70Z)*, neither contains 69, and they are exactly the two subgroups of order 12 that do not contain -1. There is no third such group.

## Checker, written before their script

Two PAF implementations, no shared acceptance code: direct Gaussian multiplication of (re, im) pairs, and residue counts of e_j - e_{j+k} mod 4 giving (c0-c2) + i(c1-c3). They agree on the recorded length-42 pair, on random length-42 and length-70 sequences, and on random H-invariant sequences. The length-42 pair passes both (sum -2+0i at every nonzero shift, |sum A|^2 + |sum B|^2 = 2). A one-digit mutation is rejected. No fetch.

Necessary filter used, not as a substitute for the search: |sum A|^2 + |sum B|^2 = 2, so each sequence has sum-norm in {0, 1, 2}. A full base-4 scan shows norm 1 never occurs. The filter does not empty the family.

## Full enumeration (not a sample)

Every assignment of fourth roots to the orbits was generated. Two generators (iterative base-4 scan and pruned recursion) agreed on the survivor counts. Survivors were then matched by full-shift residue PAF, k = 1..69, not by orbit representatives alone. A complement lookup over the whole survivor set, including same-norm pairs, found no match. A first pass that hashed PAF only on orbit representatives also found none; invariance of PAF under H was checked on 40 random invariant sequences per group and holds algebraically because multiplication by h is a bijection.

| group | orbits | assignments | norm 0 | norm 1 | norm 2 | ordered PAF matches |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | 10 | 1048576 | 2304 | 0 | 6528 | 0 |
| H2 | 12 | 16777216 | 36864 | 0 | 99840 | 0 |

H1 orbit sizes 1,12,12,12,6,4,6,4,12,1. H2 orbit sizes 1,12,12,12,3,12,4,3,4,3,3,1. Distinct full PAF keys: H1 533, H2 7576.

## Author script

From the claim directory, `python3 search_two_groups.py`, run twice. The two outputs are byte-identical. One block per group, then TOTAL_HITS 0. Counts match the independent scan exactly: H1 norm0 2304, norm1 0, norm2 6528, unique_paf0 188, unique_paf2 345 (188+345=533); H2 norm0 36864, norm1 0, norm2 99840, unique_paf0 2275, unique_paf2 5301 (2275+5301=7576); hits 0 and 0. Their complement test is norm-2 keys against norm-0 keys, which is complete here because norm 1 is empty and the two norms must add to 2. The independent search did not rely on that split and also returned no pair.

No missing object: the claim is emptiness of these two families, and both the groups and search_two_groups.py are present. No non-determinism. No mismatch between the definition, the independent exhaustion, and the author run.

pass: true
