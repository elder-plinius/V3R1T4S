# PREREG: condorcet-domains, verification run for n = 14..20 and 22..25 (run folder 2026-10-18-0558)

frozen at (date -u): 2026-10-18T06:09:01Z. No lens of this folder had started, and attempts/ was empty.

## What existed before this freeze

- The candidate objects in runs/2026-10-17-2220/attempts/ (lns-low, lns-high) and runs/2026-10-18-0238/attempts/ (ledger-audit, vcycle), with those lenses' notes and ledgers.
- The confirmed n = 21 claim of runs/2026-10-18-0238.
- This folder's checker tests (data/checker_tests_output.txt, 2026-10-18T06:08:06Z).

The main session has read the earlier ledgers. They are inputs, and every number in them is re-derived from files under the rules below.

## Criterion (the charter's question, verbatim; target outside the bank)

"For some n >= 9, an explicit set of linear orders on n alternatives on which majority rule is transitive for every profile (every triple satisfies a never-condition), strictly larger than the best published Condorcet domain for that n."

Definition used (arXiv:2601.07336v1, Section 2, quoting Sen): D is a Condorcet domain if the restriction of D to every triple of alternatives satisfies a never condition (xNb, xNm or xNt).

## Rows (the human's order in charter Q5, 2026-10-17 21:36 PDT)

- ONE claim folder with eleven rows: n = 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25 (n = 21 is excluded; it is claimed in runs/2026-10-18-0238).
- Each row is a separate claim. It has its own object, its own bar (the Table 4 entry for that n) and its own check, and it is judged on its own.
- A row that fails any rule below, or any skeptic, is dropped. It is never repaired after the panel.
- The gate's confirmed_scope lists exactly the rows that pass all three skeptics. It is taken verbatim from the CRITERION skeptic's per-row scope sentences.

## Object and statistic per row

- **Type L (n = 14..20 and 22): an explicit list.** The object is a list of linear orders on 1..n, one per line, most preferred first, compressed with xz and split into parts of at most 10^6 bytes.
  - Statistic: size = number of distinct orders. It counts only if every line is a permutation of 1..n and every one of the C(n,3) triples satisfies a never condition.
  - Checker of record: code/main_check/mcheck.c. It agrees with code/cdcheck.py on 5 test domains here (3 PASS: Fishburn n = 7, 8, 9 with sizes 100, 222, 488; 2 FAIL), see data/checker_tests_output.txt, and on 7 more in runs/2026-10-18-0238.
  - The row's never-condition assignment is a by-product, not the object.
- **Type A (n = 23, 24, 25): an assignment with an exact count.** The charter allows this type where an explicit list is too big for a package. The object is a never-condition assignment A_n, one condition per triple (C(n,3) lines). The claimed set is D(A_n), the set of ALL linear orders on 1..n that obey every line of A_n.
  - Statistic: size = |D(A_n)|. Two independent methods must give it exactly:
    - (i) a subset-DP count;
    - (ii) an enumeration that emits every order of D(A_n) and passes each emitted order through a separate checker. That checker tests permutation, distinctness (strictly increasing lexicographic stream), obedience to A_n and the triple condition. The enumeration also prints the sha256 of the canonical text stream: every order as above, in lexicographic order, LF line ends. This pins the set exactly.
  - Any subset of D(A_n) obeys A_n on every triple, so D(A_n) is a Condorcet domain by Sen's condition.
  - The CRITERION skeptic rules whether this counts as "an explicit set". If it rules no, those rows fail.

## Thresholds (each row separately; all must hold)

1. The row's object passes its type's check above with 0 malformed lines, 0 duplicates and 0 violations. For type A, the two counts agree exactly and the stream check reports 0 violations.
2. size > T4(n), the n entry of data/records_table4.tsv (Table 4 of arXiv:2601.07336v1). A tie is not a record. The size must also beat any larger value found by the literature and crowd re-check made right before the claim is built: journals, the authors' pages, open and closed V3R1T4S pull requests, and arXiv only through the saved copy and the human's hand check while arxiv.org is stopped.
3. Not a published construction applied only to published inputs whose value the paper already lists. As in runs/2026-10-18-0238: if a row's object were such a construction, it counts only if Table 4 does not already list that value or more for that n.
4. The carrier for each n is the largest object for that n that passes rule 1 among the candidates in runs/2026-10-17-2220/attempts/*/result, attempts/*/out/dossier, and runs/2026-10-18-0238/attempts/{ledger-audit,vcycle}. Sizes are re-derived from the files, never taken from notes.
5. Before the claim is built, the main session re-checks every row's object with its own tools: mcheck.c for type L; for type A, its own DP count and its own streamed check. Any disagreement drops the row.

## Reported per row (information for the panel, not thresholds)

- The gain size/T4(n) - 1.
- The largest |D(A')| over the n+1 restrictions of the next row's assignment, deleting one alternative (where the next row exists in this claim, or is the n = 21 object). This shows whether a row merely follows from its neighbour.
- For type L, whether the list equals D(A) of its own assignment (|list| = |D(A)| and every order obeys A).

## Null design

null_test: not needed because every row's claim is an explicit object (an order list, or an assignment whose full domain is enumerated and counted exactly) checked by deterministic exact checkers against a published value; no search statistic or chance claim is made.
