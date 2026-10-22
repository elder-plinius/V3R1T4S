# Honesty gate (dna-codes-gc-rc-king-table)

status: CONFIRMED_SOLUTION
confirmed_scope: The file object lists 36 distinct words of length 18 over ACGT, each with exactly 9 letters from C and G and pairwise Hamming distance at least 13 and Hamming(x, rc(y)) at least 13 for all x, y including x = y, which beats the live King-page entry 21 for this cell; comparison with post-2010 literature is not decided here.

## Gate notes
- Object: object/gc_rc_18_13_9.txt, sha256 e5eed8a3ba787f959f144f130a6fe81dde0a14f60d6b7ed7d79a1f17df2fd852.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The Montemanni-Smith-Koul 2014 chapter was not readable (paywalled); the novelty skeptic passed this cell because its margin over every readable value (King table, Aboluion thesis, four arXiv papers) is at least 3 codewords.
