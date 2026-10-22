# Honesty gate (dna-codes-gc-king-table)

status: CONFIRMED_SOLUTION
confirmed_scope: The file object lists 52 distinct words of length 13 over ACGT, each with exactly 6 letters from C and G and pairwise Hamming distance at least 9, which beats the live King-page entry 46 for this cell; comparison with post-2010 literature is not decided here.

## Gate notes
- Object: object/gc_13_9_6.txt, sha256 d41bbb3417f3d8da02bb9440e86e05c86a24e2d1829ebe115440a902b62e531e.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The Montemanni-Smith-Koul 2014 chapter was not readable (paywalled); the novelty skeptic passed this cell because its margin over every readable value (King table, Aboluion thesis, four arXiv papers) is at least 3 codewords.
