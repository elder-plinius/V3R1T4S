context: Claude Code subagent, fresh context [Claude Sonnet 5.5]

# Criterion report: dna-gcrc-n10-d7-w5

Role: criterion (group codes). Files are named relative to the package folder. I used only the package plus one fetch of the King page (URL https://rambutan.umassmed.edu/king/dnacodes.html, fetched 2026-10-19T05:17:27Z, HTTP 200, sha256 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5, byte-identical to the triage fetch).

## Success criterion, clause by clause (cell A_4^GC,RC(n,d,w) = (10,7,5))
1. Cell is unmarked (not followed by a period or colon) on the King page: MET. My own parse of the live page gives the entry 17 with a superscript only, no period or colon.
2. Plain-text list, every word of length 10 over {A,C,G,T}: MET (my own checker, not shipped in this package, written from the definition).
3. Exactly w = 5 letters from {C,G} per word, w = floor(n/2) = 5: MET for the count. That w = floor(n/2) is the table's w is not stated on the King page itself (the page has no w text); it is the bank's and King 2003's convention, which I did not re-fetch. Cannot be decided from the folder; I rely on the bank text.
4. Words distinct: MET.
5. Pairwise Hamming distance at least 7: MET (minimum over all pairs = 7).
6. Reverse-complement clause (Hamming(x, rc(y)) at least 7 for ALL x, y including x = y; rc = reverse then swap A/T, C/G): MET, minimum over all ordered pairs including x = y = 7.
7. Count strictly greater than the live table entry: MET. Counted 20 words; live entry 17.
8. Count strictly greater than every post-2010 published value for the same (n,d,w): CANNOT BE DECIDED from the folder. The triage did not read Aboluion-Smith-Perkins 2012 or Montemanni-Smith-Koul 2014 (paywalled) and did not search Google Scholar; the Aboluion 2011 thesis value equals the King value. This literature clause is the novelty skeptic's; I flag that this criterion verdict is conditional on it.

## Hidden quantifier and definition checks
- No hidden quantifier found: the claim is for one fixed (n,d,w), one table, and a Full win (no partial win claimed).
- Null model: not applicable to a strict improvement of a lower bound; the object is a witness, so the checks above are exhaustive over all pairs, not a sample.
- The optimal-mark pitfall does not arise: the cell is unmarked, and the claimed size is far from any period/colon cell.
- Propagation (PR #350 rule): the claimed code was not obtained by shortening or puncturing another claimed code; I did not find a standard rule that implies this value from table values.

## Open questions in the claim record (not shipped) answered by this role
- Does an independent re-implementation agree on all conditions, in particular w = floor(n/2) and the pairwise distance? Yes: my checker (not the author's) reports size 20, GC weight 5 for every word, minimum pairwise distance 7, minimum reverse-complement distance 7, all words distinct.
- The questions about post-2010 literature and arXiv 1903.03535, 2108.02033, 2403.11551 concern novelty; this role did not read them and does not decide them.

confirmed_scope: The file object lists 20 distinct words of length 10 over ACGT, each with exactly 5 letters from C and G and pairwise Hamming distance at least 7 and Hamming(x, rc(y)) at least 7 for all x, y including x = y, which beats the live King-page entry 17 for this cell; comparison with post-2010 literature is not decided here.
pass: true
