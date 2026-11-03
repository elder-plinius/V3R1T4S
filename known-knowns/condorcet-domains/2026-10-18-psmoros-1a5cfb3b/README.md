# A Condorcet domain on 21 alternatives with 7467760 linear orders (published best: 6674931)

## What

The three files object/n21_orders.txt.xz.part_aa, part_ab and part_ac, joined in that order and xz-decompressed (sha256 0cb0dd880cc7a0ad640634f505b7520bd2a5c0bb95fd7a2ce4d56fbeb8578e27), list 7467760 distinct linear orders on the alternatives 1..21 whose restriction to each of the 1330 triples satisfies a never condition, so they form a Condorcet domain on 21 alternatives (in the odd-profile sense of arXiv:2601.07336v1, Section 2) strictly larger than 6674931, the n = 21 entry of Table 4 of arXiv:2601.07336v1, the only version of that paper at the human's hand check of 2026-10-18T00:58Z.

In plain words: on these 7467760 rankings of 21 candidates, majority voting never produces a cycle. For any odd number of voters whose rankings all come from the list, the majority relation is a transitive ranking. The largest such set published for 21 candidates, in Table 4 of arXiv:2601.07336v1, has 6674931 rankings. Ours is +11.88 % larger.

## Check it yourself

From this package folder, run:

    sh verify-it-yourself/run_checks.sh

- **Requirements:** a C compiler (cc), python3 (standard library only) and xz (or python3's lzma module).
- **What it does:** it joins the three parts in object/ and checks the joined file's sha256. It then decompresses the file and compiles verify-it-yourself/check_condorcet.c, a standalone checker written from the definition. The checker tests:
  - every line is a permutation of 1..21 in strict format;
  - all lines are distinct (sorted 128-bit keys);
  - every one of the 1330 triples satisfies a never condition;
  - the list obeys the by-product assignment object/n21_assignment.txt.
- **Rough laptop time:** about 1 minute of CPU, about 200 MB of memory and 600 MB of temporary disk.
- **Expected last line:** `PASS`

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Karpov, Markström, Riis and Zhou, Table 4 "Maximum size of Condorcet domains" (arXiv:2601.07336v1) | n = 21 | ≥ 6674931 (ks: Karpov-Slinko construction applied to smaller domains) | 7467760 | https://arxiv.org/html/2601.07336 | 2026-10-17T22:25:36Z (sha256 13e24702...bd1b); v1 still the only version at a hand check of 2026-10-18T00:58Z |

Details are in the-record-we-beat/.

## Not claimed

- **Optimality.** Nothing here bounds the maximum size of a Condorcet domain on 21 alternatives from above.
- **Other n.** Only n = 21 is claimed, one cell per package. The same run also found verified domains above Table 4 for every n from 14 to 25. These are explicit lists for n = 14..22 and exact counts for n = 23..25. Examples: n = 16 135072 (table 131536), n = 20 3336208 (3155366) and n = 22 16571072 (15037178). Several of these rows come from the paper's own large search, not from the construction. None of them is claimed here, and each needs its own claim.
- **The by-product assignment** object/n21_assignment.txt is not the object; the explicit list is. The list is exactly the set of all orders that obey that assignment (a check, not a claim).
- **Novelty beyond the named table.** The comparison is with Table 4 of arXiv:2601.07336v1, the latest record list we could find. The search covered open and closed V3R1T4S pull requests, TROPHY_CASE.md, the authors' pages and code repository, the 2025-2026 literature by web search, and a hand check that the paper has no later version. arXiv listings could not be scanned after the rate limit.
- **Not submitted** to, or reported to, the authors.
- **Not peer reviewed.** It was checked by a three-skeptic panel (panel/) and by the standalone checker in verify-it-yourself/.

## Credits

- **Alexander Karpov, Klas Markström, Søren Riis and Bei Zhou**, "Improved lower bounds for the maximum size of Condorcet domains", arXiv:2601.07336 (2026), https://arxiv.org/abs/2601.07336. Their Table 4 is the record we compare against. Their inductive extension step (Section 5.1) is the step our search runs beyond n = 20.
- **Peter C. Fishburn**, "Acyclic sets of linear orders", Social Choice and Welfare 14 (1997) 113-124: the alternating scheme and the replacement product.
- **Amartya K. Sen**, "A possibility theorem on majority decisions", Econometrica 34 (1966) 491-499: the never-condition characterisation the checker uses.
- **Charles Leedham-Green, Klas Markström and Søren Riis**, "The largest Condorcet domain on 8 alternatives", Social Choice and Welfare (2024), https://arxiv.org/abs/2303.15002. Its 224-order domain and never conditions seeded the rebuilt record chain.
- **Alexander Karpov and Arkadii Slinko**, "Constructing large peak-pit Condorcet domains", Theory and Decision 94 (2023) 97-120, https://doi.org/10.1007/s11238-022-09878-9. This construction produced the n = 21 table value; one lens of the run re-implemented it.
- **Bei Zhou and Søren Riis**, "New record-breaking Condorcet domains on 10 and 11 alternatives", https://arxiv.org/abs/2303.06524. An earlier record list consulted.
- Submission credit: psmoros. Built and reviewed with the V3R1T4S protocol, https://github.com/elder-plinius/V3R1T4S.
