# Criterion skeptic: queens-graph-domatic-numbers, partial win p1

context: subagent (Claude Code Agent tool, fresh context)

Inputs read: claim/CLAIM.md, claim/REPRODUCE.md, claim/dom-Q11-19-partition.txt. Nothing else on disk was opened.
Own code: panel/criterion-code/check_dom.py (main checker) and panel/criterion-code/neg_controls.py (sensitivity
controls). Both were run with `python -I`.

## Conditions and findings

1. **Object identity.** sha256 of claim/dom-Q11-19-partition.txt =
   cb53d4061c8e751eef8943e967c5f42f3ef47a3f8d46b7c975a5e8f6cd2f56e4, the same as CLAIM.md and REPRODUCE.md.
   The file has 11 CRLF-terminated lines of 11 integer tokens each and no other content. MET.

2. **Explicit partition of ALL n^2 squares.** Strict parse: exactly 11 rows of 11 integers. All 121 squares carry a label,
   and the classes are pairwise disjoint and cover the board (asserted in code). MET.

3. **k classes with k above the current lower bound.** There are 19 distinct labels (0..18). Table 1 of the Corrigendum,
   as recorded in the claim, gives dom(Q_11) as 18-20, so the lower bound is 18 and 19 > 18. Class sizes are 6 (x14),
   7 (x3) and 8 (x2), summing to 121, which matches REPRODUCE.md. MET.

4. **Right invariant (plain domination, not independent or total).** The checker uses closed-neighbourhood domination:
   a square passes if it is in the class or shares a row, column or diagonal (|dr| = |dc|) with a member. All 19 classes
   dominate Q_11. dom needs no independence or totality condition, and the claim asks for none. MET.
   Checker sanity results:
   - The adjacency predicate gives deg(corner) = 30 = 3(n-1) and deg(centre) = 40 = 4(n-1).
   - A single corner square leaves 90 squares undominated, so it is correctly rejected.
   - With rook-only adjacency the partition is rejected, so the diagonal rule is actually exercised.
   - Every one of the 19 classes is a minimal dominating set: removing any one of the 84 members of the size-6 classes
     breaks domination. The checker is therefore sensitive to single-square changes.

5. **n = 11 and the pair is one of the six open pairs.** dom(Q_11) in {18,19,20} is the first pair listed in the bank
   criterion. MET.

6. **Interval still open, re-fetched immediately before claiming.** Status: PARTLY DOCUMENTED, judged adequate for p1.
   - What the claim records:
     - A Corrigendum PDF re-fetch at 2026-11-05T00:50Z: HTTP 200, a sha256 unchanged since 00:19Z, and Table 1 still
       listing 18-20.
     - An OEIS A292192 re-fetch at the same time: HTTP 200, data stopping at n = 10.
     - A GitHub search for duplicate V3R1T4S claims at 00:19Z.
   - What it does not record:
     - A search for any later erratum or paper. The bank asks that the interval be open "in any later erratum or paper
       found by a search".
     - Any OEIS entries "related" to A292192 beyond A292192 itself.
   - My own spot check: two web searches, with no page fetches. They found the original paper (DML 16, 2025) and the
     Corrigendum (DML 18, 2026), both giving dom(Q_11) in {18,19,20}. They found no later source raising this bound.
     The one 2026 arXiv hit about queen domination (2604.03793) is about 3D domination numbers, not domatic numbers.
   - Search-engine summaries mention corrected values for n = 9 and n = 10 that may differ from the A292192 terms quoted
     in the claim. These snippets are unverified and do not bear on n = 11.
   - Recommendation, not a blocker: add one line to CLAIM.md recording the literature search (query, time, result).

7. **Wording: says only what is proven.**
   - The claim states dom(Q_11) >= 19 and explicitly calls 18 the previous lower bound.
   - It does not claim dom(Q_11) = 19. It does not claim any upper bound, which would need the bank's CNF + DRAT/LRAT
     path. It does not claim an extension of A292192, which needs an exact value.
   - It claims only p1, even though raising the lower bound also narrows the interval to {19,20}. This is conservative.
   - The definitions match the bank's: plain domination, and the domatic number as the maximum number of disjoint
     dominating sets.
   - MET.

8. **Credit.** The claim credits Juho Lauri for the bounds and Table 1, and cites the Corrigendum with its DOI. It does
   not cite the original 2025 paper. That is acceptable because the bank criterion names the Corrigendum as the
   reference. MET.

confirmed_scope: The file with sha256 cb53d4061c8e751eef8943e967c5f42f3ef47a3f8d46b7c975a5e8f6cd2f56e4 is an explicit partition of all 121 squares of the 11x11 board into 19 classes, each dominating Q_11, which proves dom(Q_11) >= 19, one above the lower bound 18 in Table 1 of Lauri's Corrigendum (DML 18 (2026) 34-35), and says nothing about the upper bound 20.

Verdict: p1 is met as written. The object is a valid explicit 19-class domatic partition of Q_11, k = 19 exceeds the
Corrigendum's lower bound of 18, the invariant and n are right, and the claim states only the lower bound with credit to
the source. The only gap is documentary: the claim records no search for later errata or papers (see condition 6). My
own spot search found nothing that closes the interval, so I do not treat this gap as a blocker.

pass: true
