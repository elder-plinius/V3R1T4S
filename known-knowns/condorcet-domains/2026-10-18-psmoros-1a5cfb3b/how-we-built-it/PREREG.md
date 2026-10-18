# PREREG: condorcet-domains, run folder 2026-10-18-0238

frozen at (date -u): 2026-10-18T02:39:26Z, before any attack output of this folder exists (no lens of this folder has started).

## What existed before this freeze

Everything in runs/2026-10-17-2220 (the session's first folder), including its panelled n = 21 claim (gate PROMISING, unchanged) and the verified objects listed in BRIEF.md. These were read by the main session before this file was written; they are inputs and are judged by the same rules as this folder's own outputs.

## Criterion (the charter's question, verbatim; target outside the bank)

"For some n >= 9, an explicit set of linear orders on n alternatives on which majority rule is transitive for every profile (every triple satisfies a never-condition), strictly larger than the best published Condorcet domain for that n."

Definition used (arXiv:2601.07336v1, Section 2, quoting Sen): D is a Condorcet domain iff the restriction of D to every triple of alternatives satisfies a never condition.

## Statistic and checker

- The object is an explicit list of distinct linear orders on [n] (one per line, most preferred first), possibly compressed. A never-condition assignment may be supplied as a by-product, but the list is the object.
- Statistic: size = number of distinct orders, after checking that every line is a permutation of 1..n and that every one of the C(n,3) triples satisfies a never condition.
- Checker of record: code/cdcheck.py (standard library), tested at 2026-10-18T02:38:26Z on Fishburn n = 9 (488, PASS), Fishburn n = 8 (222, PASS), all 6 orders on n = 3 (FAIL) and Fishburn n = 8 plus one order (FAIL): data/checker_tests_output.txt. For n >= 14 a C checker may be used if it agrees with cdcheck.py on at least three domains with n <= 12 (one of them a failing case). The REPRODUCE skeptic writes its own checker.

## Thresholds (all must hold; 2-6 as in runs/2026-10-17-2220/PREREG.md, rule 1 narrowed)

1. 9 <= n <= 22. (Narrowed from 25: a claim must be packageable under kit/SUBMIT.md, at most 1 MB per file and 50 MB per package, and an explicit list for n >= 23 has more than 35 million orders, which does not fit. Larger n stay in the dossier.)
2. size > the best published lower bound for that n: data/records_table4.tsv (Table 4 of arXiv:2601.07336v1), AND larger than any value found by a literature re-check made right before the claim (journals, the authors' pages and repositories, open and closed V3R1T4S pull requests; arXiv only through the human's hand check while arxiv.org is stopped). A tie is not a record.
3. Not derived from published domains by a published construction in a way that the publication already covers. If our domain is a published construction (S1, S2, Fishburn's product, Karpov-Slinko, set-alternating) applied to inputs that are themselves only published domains, it counts only if the paper's own table does not already list that value or more for that n.
4. One n per claim. If several n qualify, the carrier is the one with the largest relative gain size/record - 1; ties go to the smallest n. Every other qualifying n goes to the dossier and is not claimed in this folder.
5. Before the claim is built, the main session re-checks the carrier's explicit order list with its own checker (code/main_check/mcheck.c, which agrees with code/cdcheck.py on 7 domains with n <= 12, 4 of them failing: code/main_check/xcheck_output.txt). Any disagreement stops the claim.
6. The carrier must be the largest verified object for its n at the time the claim is built. The relative gain in rule 4 is computed from verified sizes only (an explicit list that passed a checker), never from DP counts or streamed checks alone.

## Null design

null_test: not needed because the claim is an explicit object (a list of linear orders) checked by a deterministic exact checker against a published value; no search statistic or chance claim is made.
