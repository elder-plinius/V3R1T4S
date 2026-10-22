# A Condorcet domain on 24 alternatives with 81912986 linear orders (published best: 73279872)

## What

The confirmed scope of the claim this package comes from (panel/gate.md), word for word:

For each n in {14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25}, this folder's row-n object (for n <= 22 the explicit list object/nN_orders.txt.xz, and for n = 23, 24, 25 the full domain D(A_n) of all linear orders on 1..n obeying object/nN_assignment.txt, of exactly counted size with a hash-pinned canonical enumeration) is a Condorcet domain on n alternatives of size 27040, 60956, 135072, 300388, 675512, 1497276, 3336208, 16571072, 36894088, 81912986 and 178950728 respectively, each strictly larger than the n entry of Table 4 of arXiv:2601.07336v1 (27026, 59430, 131536, 292015, 649079, 1432836, 3155366, 15037178, 33162136, 73279872 and 160316046), with the n = 14, 15, 18 and 19 domains being one-alternative restrictions of the n = 15, 16, 19 and 20 domains.

This package carries the n = 24 row only (one table cell per package). The CRITERION skeptic's sentence for this row:

The set D(A_24) of all linear orders on the alternatives 1..24 that obey every one of the 2024 never conditions in object/n24_assignment.txt has exactly 81912986 elements (canonical enumeration sha256 54baf18b85aecce8a420ce8c1b7350f86b3bf27590741ba9b23193ca0e4a0605) and is a Condorcet domain on 24 alternatives (majority relation transitive for every odd profile), strictly larger than the n = 24 entry 73279872 of Table 4 of arXiv:2601.07336v1.

The object here is the set D(A_24) of all linear orders on 1..24 obeying the 2024 never conditions in object/n24_assignment.txt (exactly 81912986 orders; canonical enumeration sha256 54baf18b85aecce8a420ce8c1b7350f86b3bf27590741ba9b23193ca0e4a0605).

In plain words: on the 81912986 rankings of 24 candidates that obey the listed never conditions, majority voting never produces a cycle. For any odd number of voters whose rankings all come from this set, the majority relation is a transitive ranking. The largest such set published for 24 candidates (Table 4 of arXiv:2601.07336v1) has 73279872 rankings; this one is +11.78 % larger.

## Check it yourself

From this package folder, run:

    sh verify-it-yourself/run_checks.sh

- **Requirements:** python3 (standard library only); FULL=1 also needs a C compiler.
- **What it does:** verify-it-yourself/dpcount.py (standard library) checks that the assignment has exactly one well-formed never condition for each of the 2024 triples and counts D(A) exactly; with FULL=1 it also enumerates all of D(A) with verify-it-yourself/mdom.c, streams it through verify-it-yourself/mstream.c (format, strictly increasing, obeys the assignment, every triple has a never condition) and prints the stream's sha256.
- **Rough laptop time:** under a second (FULL=1: 10-30 minutes)
- **Expected last line:** `PASS` (the real output is in verify-it-yourself/RECEIPTS.md)

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Karpov, Markström, Riis and Zhou, Table 4 "Maximum size of Condorcet domains" (arXiv:2601.07336v1) | n = 24 | ≥ 73279872 (ks) | 81912986 | https://arxiv.org/html/2601.07336 | 2026-10-17T22:25:36Z (sha256 13e24702...bd1b); v1 still the only version at a hand check of 2026-10-18T00:58Z |

Details are in the-record-we-beat/.

## Not claimed

- **Optimality.** Nothing here bounds the maximum size of a Condorcet domain on 24 alternatives from above.
- **Other n.** Only n = 24 is claimed in this package. The same claim folder passed rows n = 14..20 and 22..25, each packaged separately; n = 21 is a separate earlier package. Rows 14, 15, 18 and 19 are restrictions of rows 15, 16, 19 and 20: the eleven rows come from seven independent objects.
- **No literal list is shipped.** An explicit list for n = 24 is too large for a package; the object is the assignment, the claimed set is D(A), and verify-it-yourself/mdom.c lists it (FULL=1 sh verify-it-yourself/run_checks.sh streams it through a checker and prints its sha256). The CRITERION skeptic ruled that this is an explicit set.
- **Novelty beyond the named table.** The comparison is with Table 4 of arXiv:2601.07336v1, the latest record list found. The NOVELTY skeptic searched all V3R1T4S pull requests, TROPHY_CASE.md, GitHub, the authors' pages and data, the 2025-2026 literature by web search and the Puppe-Slinko book draft; arXiv itself could only be covered by the saved copy and a hand check, because arxiv.org had rate-limited the workspace.
- **Not submitted** to, or reported to, the authors. **Not peer reviewed:** checked by a three-skeptic panel (panel/) and by the standalone checkers in verify-it-yourself/.

## Credits

- **Alexander Karpov, Klas Markström, Søren Riis and Bei Zhou**, "Improved lower bounds for the maximum size of Condorcet domains", arXiv:2601.07336 (2026), https://arxiv.org/abs/2601.07336. Their Table 4 is the record compared against; their inductive extension step (Section 5.1) is the step the search ran beyond n = 20.
- **Peter C. Fishburn**, "Acyclic sets of linear orders", Social Choice and Welfare 14 (1997) 113-124: the alternating scheme used to test the checkers.
- **Amartya K. Sen**, "A possibility theorem on majority decisions", Econometrica 34 (1966) 491-499: the never-condition characterisation the checkers use.
- **Charles Leedham-Green, Klas Markström and Søren Riis**, "The largest Condorcet domain on 8 alternatives", Social Choice and Welfare (2024), https://arxiv.org/abs/2303.15002: the n = 8 domain that seeded the rebuilt record chain.
- **Alexander Karpov and Arkadii Slinko**, "Constructing large peak-pit Condorcet domains", Theory and Decision 94 (2023) 97-120, https://doi.org/10.1007/s11238-022-09878-9: the construction behind the table's n >= 21 values.
- **Bei Zhou and Søren Riis**, "New record-breaking Condorcet domains on 10 and 11 alternatives", https://arxiv.org/abs/2303.06524: an earlier record list consulted.
- Submission credit: psmoros. Built and reviewed with the V3R1T4S protocol, https://github.com/elder-plinius/V3R1T4S.
