# NOVELTY skeptic: A084235 a(18) = 330055906058

context: subagent (fresh executor, given only claim/)

Inputs read: claim/ (CLAIM.md, candidate.md, TABLE_RECORD.md, result/a18.txt, file list), the public repo (TROPHY_CASE.md, known-knowns/, the bank entry known-unknowns/number-hunts/mertens-function-exact-values-next-terms.md), and kit-format notes. I did not read the run's report, log, other panel files or continuations notes. Scratch work is in panel/continuations/2026-11-22-followup/novelty_work/.

## Primary fetch (one request, no retries)
- URL: https://oeis.org/A084235/b084235.txt
- Time: Sun 2026-11-22 11:17:09 CST, HTTP 200
- Value: the b-file ends at "17 108500046711". There is no n = 18 line. Its sha256 is e40ebda76ec5f993ea987206d65b8b630c2c94a4a90e9aad6939d8a10ead363f, which matches the claimant's fetches at 09:23 UTC and 16:56 UTC.
- The entry page (https://oeis.org/A084235/internal) fetched the same minute shows %I #32 Mar 16 2026, data through a(17), keyword "nonn,more", and %E "a(14)-a(17) by Ashley Jordan and Luke March, Jul 22 2014". It has no later extension.

## Sources searched (all 2026-11-22, CST)
OEIS:
- OEIS search for 330055906058 and for 330,055,906,058: "Sorry, but the terms do not match anything in the table."
- A051402 (smallest k with |M(k)| = n; A084235(n) = A051402(2^n)): the b-file is n = 1..10000 and ends at "10000 902718903". It is far below n = 262144. %I #51 is from Nov 08 2026, and the Aug 2026 edit was only a Python program by Chai Wah Wu.
- A051400 and A051401 (first M = +n and M = -n): b-files are n = 1..10000 only.
- A060434 (essentially A051402): 44 terms.
- A084234 (|M| = n^2): 100 terms. Its largest value would be n = 100, |M| = 10000, which is not a power-of-2 cell beyond 2^13.
- A304241 and A304242 (record amplitude extrema between zeros, b-files to n = 65, by Dobbelaere and Hurst): terms 57 and 58 are M(297193839495) = 207478 and M(330508686218) = -294816. No listed extremum equals ±262144. These only bracket a(18): 297193839495 < a(18) < 330508686218.
- A084236 and A084237: these are isolated values M(2^n) and M(10^n), not first-hit cells.

Literature and code:
- Hurst 2018, arXiv:1610.08551 (Math. Comp. 87 (2018) 1013-1028). It sieves all x <= 1e16 and "records all extrema", but publishes only a "select list of extrema corresponding to prominent peaks". The list holds the same two bracketing peaks as above and does not give a first hit of |M| = 262144. The linked data notebook, https://wolfr.am/mertens, returned 404 when fetched today (it redirects to develop.wolframcloud.com ... HTTP 404). So whatever his raw data contain is not published.
- Hurst 2026, arXiv:2607.07566, "Practical computations of the Mertens function: M(10^24) and M(10^25)", dated 2026-07-08 and inside the 24-month window. I searched the full text. The only first-hit value it mentions is 2^15 at 7613644886, which is A084235(15). There is no 2^18 value, and it does not contain 330055906058.
- github.com/greg-hurst/mertens: I read the whole tree on main (pushed 2026-09-11), release v1.0 (no assets) and issues/PRs #1-#3. A grep for 330055906058, 262144, 2^18 and A084235 found nothing, apart from the 2^15 constant 7613644886 used in the code.
- github.com/maxieds/MertensFunctionComputations: 34 files, no 330055906058.
- arXiv:2604.23517 (Schmidt 2026, cited in A051400 and A051401): a probabilistic theory paper with no table of first hits.
- Web searches: "330055906058" returned only barcode pages. "A084235 2^18 262144", "Mertens 262144 first k Jordan March", "github mertens A084235 OR A051402 new terms" and "Mertens computation 2025 2026" found nothing that gives a(18).

V3R1T4S repo:
- TROPHY_CASE.md: no Mertens or A08423x entry, in either the local clone at 25c99686 or upstream main at 5db3547 (2026-11-19 16:48 CST).
- known-knowns/: no Mertens directory, local or upstream.
- The bank entry still lists the cell as open, and its text is the same on main.
- Pull requests, open and closed, all pages (1165 PRs): no title or body mentions Mertens, Möbius or A08423x. GitHub issue and PR search for A084235, 330055906058, mertens-function-exact-values and A084237 gave 0 hits. The one "Mobius" hit is #1166 (Dedekind numbers), which is unrelated.

## Reasoning
- The object is an exact first-hit index. It is neither an approximation nor a construction. Trivial edits of published objects (deletion, restriction, relabelling, symmetry, propagation, local polish) cannot produce it.
- Published data bound a(18) from the interval (297193839495, 330508686218), but they do not determine it. The candidate 330055906058 falls inside that interval, which is consistent but derived from nothing published.
- Neighbouring cells a(17) = 108500046711 and a(19) do not give it either: a(19) is unpublished, and a(17) is just the previous term.
- The claim is not seeded from a published object beyond these bounds.
- The only plausible prior holder is Hurst's unpublished 1e16 extrema data, which is not public: the notebook is 404, and neither paper nor the repo lists it. Under the kit, an unpublished private dataset is not a published result.
- Direction: a new term at a higher index (n = 18) than everything published (n <= 17). That strictly beats what is known, and it is not a tie.
- Scope: this verdict covers novelty only. Whether the value is correct (full sieve from 1, second independent run) is for REPRODUCE and CRITERION.
- Caveat: the OEIS b-file must be re-fetched immediately before any submission, per the bank criterion.

pass: true
