(saved by the main session from the subagent's returned text, 2026-10-16T05:09:04Z; the text between the skeptic's BEGIN/END PANEL markers, verbatim)

# CRITERION skeptic: spherical-codes-cohn-table, row (d, N) = (6, 526)

context: subagent (Agent tool), model opus, fresh context that saw only claim/

Run 2026-10-16T04:04Z to 04:12Z. I read every file in claim/ and also the bank entry (id spherical-codes-cohn-table). I wrote my own checker, which is not claim's verify/check_claim.py. Allowed requests used: 3 of 3, all HTTP 200, none blocked, so no line was added to the stop list. I did not request export.arxiv.org or papers.ssrn.com.

## Verbatim check
- I compared the criterion text programmatically with bank success_criterion. It matches exactly in CLAIM.md and in prereg/PREREG_run2026-10-16-0024.md.
- p1, p2 and p3 also match exactly in both files.
- The verification method matches exactly in CLAIM.md.
- Hashes: `shasum -c object/SHA256SUMS` gives OK. table/index_2026-10-16T03-59-09Z.html and table/plain_2026-10-16T03-59-07Z.csv hash to the sha256 values stated in CLAIM.md.

## Clause by clause

1. **N vectors in R^d.** MET.
   - object/d6_N526.txt has exactly 526 non-empty lines with 6 tokens each: plain ASCII decimals, no CR, a trailing newline.
   - There are no zero vectors and the points are distinct (smallest pairwise distance about 0.6536).

2. **The (d, N) row is present in the live /plain.** MET as of 03:59:07Z.
   - table/plain_2026-10-16T03-59-07Z.csv line 3517 reads `6,526,0.786636400242` (HTTP 200 fetch, per CLAIM.md).

3. **Coordinates given to at least 20 digits.** MET.
   - All 3,156 coordinates have exactly 26 significant digits (25 after the decimal point).
   - The clause is met whether "digits" means significant digits or decimal places.

4. **Normalise in mpmath at 50 digits; c* is the maximum pairwise inner product.** MET, recomputed independently.
   - Method (a), spec-literal: mp.dps = 50, normalise each vector, fsum over all 138,075 pairs. Result c* = 0.786430618544579725385299139732104519385, attained by points (168, 416), 0-based.
   - Method (b), exact cross-check: integer dot products from the exact decimal strings, cos = dot / sqrt(n_i n_j) at dps 80. This gives the same value to all 40 printed digits and the same pair.
   - Method (c): a float64 screen agrees (maximum 0.78643062).
   - c* is reached by a single pair: the next pair is 5.1e-12 lower.
   - Minimal angle: 38.1468127415218345891 degrees.
   - These match CLAIM.md and REPRODUCE.md.

5. **Strictly lower than the table's 12-decimal cosine by at least 1e-10.** MET against the 03:59:07Z fetch.
   - gain = 0.786636400242 - c* = 2.057816974202746e-4, which is greater than 1e-10 and strictly lower.
   - Direction check: the table lists the cosine (smaller is better). The posted (6,526) code, fetched by me (see clause 9), has maximum cosine 0.78663640024186403. That equals the table value to 1.4e-13, so the semantics and my parser are both confirmed. This is the bank checker's "posted code reproduces table to 1e-11" parser-sanity step; the package lacked it, and I did it.

6. **"Re-fetched live immediately before claiming."** NOT SATISFIABLE BY THE PANEL; the gate must re-fetch.
   - The package's /plain and index are from 03:59:07Z and 03:59:09Z. The claim is made at the gate, later.
   - The prereg (Exact statistic, gain) binds the main session to re-fetch /plain and the HTML index together at gate time.
   - At gate time the claim stands only if all of these hold:
     - row (6,526) is still present in /plain;
     - its 12-decimal cosine minus c* is still at least 1e-10;
     - the index row still has no `&ast;` and no "needs more optimization";
     - if the row's cosine or reference changed, novelty is re-checked.
   - Supporting evidence of stability: CLAIM.md reports identical sha256 values at 00:28Z, 01:44Z, 03:26Z and 03:59Z. My fetch of /data/6/526 at 04:10:25Z still returns a code whose cosine is 0.786636400242.

7. **No `&ast;` on the live HTML index row.** MET as of 03:59:09Z.
   - I parsed the full table/index_2026-10-16T03-59-09Z.html myself rather than relying on the extracted snippet. Exactly one `<tr>` carries href="/data/6/526", and its text is `6 | 526 | 0.786636400242 | Ilmari Vahteristo, New spherical codes by tuning an annealing solver, preprint, 2026, arXiv:2610.19988.`
   - It has no `&ast;`. The extracted table/index_row_6_526.html agrees.

8. **No 'needs more optimization' in the row.** MET.
   - The (6,526) reference cell is the Vahteristo citation only.
   - Rows (6,518) to (6,526) are all unlabelled Vahteristo rows. Rows (6,527) to (6,534) are "Henry Cohn, 2026, needs more optimization".
   - So the claimed row is not a p2 row.

9. **Not superseded by a newer arXiv result for (6,526).** MET on my searches; the package itself contained no arXiv search.
   - claim/ only shows that the row cites arXiv:2610.19988. archives/vahteristo_combined_D6_N525-527.json gives Vahteristo's Zenodo cosine for N = 526 as 0.7866364002418642, which equals the table, so the table already holds that paper's result.
   - My 3 requests:
     1. arxiv.org/search "spherical codes", all fields, newest first, 04:09:26Z, HTTP 200, sha256 a8a5c7e8...
     2. arxiv.org/search/advanced `"spherical code"` OR `Tammes`, newest first, 04:10:05Z, HTTP 200, sha256 b32b3762...
     3. spherical-codes.org/data/6/526, 04:10:25Z, HTTP 200, sha256 93dd533c...
   - Results:
     - 2610.19988 (Vahteristo, submitted 14 Oct 2026) appears and is the newest code-construction paper.
     - The only newer relevant hit is 2610.21263 (A. Salmon, 15 Oct 2026, asymptotic rate of the Delsarte LP bound). It has no (6,526) codes.
     - 2610.20259 (strongly-regular-graph nonexistence, 14 Oct) is not a code construction either.
   - Limits: the search covers metadata only, and only papers announced up to the latest arXiv mailing. The gate's re-fetch (clause 6) and the NOVELTY skeptic cover the rest.

10. **Not a kissing-number configuration.** MET.
    - The clause applies only if 9 <= d <= 23 and c* <= 0.5. Here d = 6 and c* = 0.786, so the clause does not apply and nothing goes to kissing-number-low-dim.

11. **No upload to /upload-code.** MET as far as the package shows. CLAIM.md claims "the verified code" only and reports no submission.

## Hidden quantifiers, subsumption, partial wins
- **One object, one row, one claim.** This is not a batch.
  - Not p1 (d is not 3).
  - Not p2 (the row is unlabelled, and a p2 batch needs 20 or more labelled rows).
  - Not p3 (this is not an exact-angle certificate).
  - So the full criterion is the only applicable category, and it is the one claimed.
- **Derived from a labelled row's code.** The object was derived from the posted (6,527) code, which is labelled "needs more optimization". The criterion only concerns the label on the claimed (d, N) row, so this is irrelevant.
  - The trivial baseline (drop a point from a 527-point code without re-optimising) is bounded by the table's (6,527) value 0.786675138796. That value is higher than the table's (6,526) value, so the gain is not a bookkeeping or monotonicity artifact of the table.
- **Implication for (6,525) — not claimed.** c* is also 4.40e-5 below the unlabelled (6,525) table cosine 0.786474636176. Deleting any point would therefore improve (6,525) as well. That row is not claimed and is outside this scope. It does not subsume the (6,526) claim: this is the stronger statement, and it implies the other.
- **Null model.** I agree with the prereg that no statistical null applies: the claim is a deterministic inequality on an explicit object.
  - The relevant null, a checker or parser bug, is ruled out by:
    - two independent computations agreeing to 40 digits;
    - the float screen agreeing;
    - the same parser reproducing the posted (6,526) code's cosine to 1.4e-13.

## Run's frozen extra conditions (prereg/)
- **Taken list.** (6,526) is not in {(29,114), (30,74), (29,72), (28,70), (30,117), (29,145), (26,232), (27,68)}. MET.
- **Public archives.** c* is below Vahteristo combined.json (N = 526, cos 0.7866364002418642) by 2.0578e-4. The Jay values recorded in that file (0.788562976701, 0.788513093183) are worse. MET.
- **No newer arXiv result with a lower cosine.** MET on my searches (clause 9).
- **The comparison came from an HTTP 200 fetch,** not a blocked or failed one. MET.
- **NOVELTY skeptic.** Not my lens.
- **Optimizer sanity control on 8 or more starred rows.** NOT EVIDENCED in claim/. The prereg calls it "required before any claim". The object's validity does not depend on the optimizer (c* was recomputed from the file), but the gate must confirm from the run record that the control was run, with no starred row beaten, for the configuration that produced this code.

confirmed_scope: The 526 vectors in R^6 of object/d6_N526.txt (sha256 9ab8021055cf16bc37eafb5ff62c65ce9a9660c1c907fca8e202f9def2d5b83a, 26 significant digits per coordinate) have, after normalisation in mpmath at 50 digits over all 138,075 pairs, maximum inner product c* = 0.78643061854457972538529914, which is 2.0578e-4 below the cosine 0.786636400242 of the unstarred, unlabelled (6,526) row of spherical-codes.org /plain and HTML index as fetched 2026-10-16T03:59Z, and arXiv metadata searches at 2026-10-16T04:10Z found no (6,526) result newer than the row's own source arXiv:2610.19988.

Verdict: the full success criterion is met for the single row (6,526) on the saved evidence. Two things are binding on the gate: (i) re-fetch /plain and the index at gate time and re-apply clauses 2, 5, 7 and 8 (clause 6); (ii) confirm the prereg optimizer sanity control exists in the run.
pass: true
