# NOVELTY verdict: brouwer-qary-unrestricted-a3-a4-a5, cell A3(15,10)
context: fresh reviewer (new context started for the NOVELTY role only; saw only CLAIM.md, RECORD.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-20T14:09:03Z

## Live table (one plain curl GET, no retries)

| item | value |
|---|---|
| URL | https://aeb.win.tue.nl/codes/ternary-1.html |
| fetched (UTC) | 2026-11-20T14:05:45Z |
| HTTP status | 200 |
| Date header | Fri, 20 Nov 2026 14:05:46 GMT |
| Last-Modified header | Sat, 17 Oct 2026 19:57:34 GMT |
| ETag | "2727-65e0eb1272e91" |
| Content-Length | 10023 |
| sha256 of bytes | 72a5f8906bbfdd9046dec9413901c0c44deb3124ac40530b0eb41214d5c91642 |

Row n = 15 (columns d = 3..14): ub `434815 149585 29213 9904 2204 685 165 39 10 6 3 3`, lb `354294 83106 7929 3321 729 243 81 27 = = = =`. Cell d = 10: **lb 27, ub 39**; open (not `=`). This matches RECORD.md byte-for-byte (same sha256, Last-Modified and ETag).

Notes under the table naming the cell: only `A3(14,10) ≤ 13 and hence A3(15,10) ≤ 39, A3(16,10) ≤ 117` (Kaski and Östergård 2001), an upper bound. No note gives a lower bound for A3(15,10) above 27. The most recent note (Oscar Sanchez, 2026-10-17) covers A3(14,8) and A3(15,5) only.

## The object (own stdlib script)

`object/A3-15-10-31words.txt`, sha256 86da3f818e06cbe15a35aabf63c8849ee96e1ccf3dd36c9964113732876d9555 (matches CLAIM.md).
- 31 words, 31 distinct, all of length 15 over {0,1,2}.
- All 465 pairs checked: distance distribution {10: 360, 11: 75, 12: 30}; minimum 10.
- Rebuilt from the stated construction (cyclic shift x the 1<->2 symbol swap, order 30; orbits of `000000000000000` and `001111201221012`): 31 words, identical to the file.

## Neighbouring cells (propagation from the live grid, own script)

Largest lower bounds for A3(15,10) implied by other cells of the same fetched table, via padding (A3(n,d) for n < 15, d >= 10), puncturing (A3(n,d) >= A3(n+1,d+1)) and shortening (A3(n,d) >= A3(n+1,d)/3), alone or combined:
- A3(16,11) >= 18, punctured: 18
- A3(16,10) >= 54, shortened: 18
- A3(14,10) = 13, padded: 13
- A3(15,11) = 10: 10

None reaches 27, let alone 31. Ternary codes have no parity-extension rule, so A3(14,9) >= 36 implies nothing for d = 10.

## Literature and code search (2024-11 to 2026-11 and older standard sources)

- Laaksonen and Östergård, "New lower bounds on q-ary error-correcting codes", Cryptography and Communications 2019 (full text read once from aaltodoc.aalto.fi, 2026-11-20T14:07:49Z): its Table 1 gives A3(15,10) lower bound 27, upper bound 39. Not improved there.
- Laaksonen results page https://www.cs.helsinki.fi/u/ahslaaks/codes/ (read once, 2026-11-20T14:07:39Z): the ternary list (A3(13,4) to A3(16,8)) does not include (15,10).
- github.com/owhs/code-table-improvements (the October 2026 ternary/5-ary/mixed improvements; tree and README read via gh, 2026-11-20T14:08:18Z): ternary files are only `ternary_n14_d8.txt` and `ternary_n15_d5.txt` plus mixed codes; nothing for (15,10). No releases.
- Web searches (2026-11-20 ~14:06-14:08Z) for "A3(15,10)", "A_3(15,10) >= 31", "(15,31,10)" ternary, the orbit representative `001111201221012`, ternary code length 15 distance 10 lower bound, and 2025-2026 arXiv lower bounds for ternary/nonbinary codes: no source gives A3(15,10) above 27. Hits were Brouwer's table, the V3R1T4S target description (which itself lists the cell as 27-39 on 2026-10-28), the 2017/2019 Laaksonen-Östergård papers, and unrelated binary/constant-weight work.
- GitHub code search for "A3(15,10)" and "A_3(15,10)": no results.

## V3R1T4S repository (gh, read-only, 2026-11-20T14:06-14:07Z)

- Pull requests: all 1151 (open, merged, closed) scanned by title and body for brouwer/qary/A3(/ternary-1/aeb.win; none concerns target brouwer-qary-unrestricted-a3-a4-a5 or any A3(n,d) cell. Searches for `brouwer-qary`, `qary-unrestricted`, `A3(15,10)` returned nothing relevant.
- TROPHY_CASE.md on main (sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113): no A3 / ternary-table entry.
- known-knowns/ (tree of main): no folder or file for this target or any ternary A3 cell.
- Releases: none.
- known-unknowns/record-tables/brouwer-qary-unrestricted-a3-a4-a5.md lists the cell as open at 27-39.

## Trivial-edit check

The best published object for this cell has 27 words (attributed to Bitan and Etzion 1995 via the 1998 table). Deletion, restriction, relabelling, symmetry and propagation cannot increase a code's size, and the neighbour propagations above reach at most 18. A 31-word code cannot come from trivial edits of any published object. The claim does not name a seed; the construction is a union of two orbits under a group of order 30, built from scratch.

## Problems found

None for novelty. The claim notes the code was sent to the table maintainer on 2026-11-20; it is not yet in the table (confirmed by the fetch above), so it does not pre-empt itself.

## Reasoning

The live table gives lb 27 (open cell, ub 39); no note, neighbouring cell, paper from the last 24 months, the 2019 literature tables, or V3R1T4S PR, trophy or known-knowns entry gives 28 or more. The object is a valid (15, 31, 10) ternary code, verified over all pairs. 31 > 27 is a strict improvement by 4 words and stays below the upper bound 39.

pass: true
