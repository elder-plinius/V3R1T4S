# Honesty gate (dna-codes-gc-king-table)

status: CONFIRMED_SOLUTION
confirmed_scope: The file object lists 24 distinct words of length 13 over ACGT, each with exactly 6 letters from C and G and pairwise Hamming distance at least 10, which beats the live King-page entry 20 for this cell; comparison with post-2010 literature is not decided here.

## Gate notes
- Object: object/gc_13_10_6_24.txt, sha256 c83bdf57b2cd3dbf6be677cd10c11c2ac26521c670fc925a71af39df802ebef7.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The Montemanni-Smith-Koul 2014 chapter was not readable (paywalled); the novelty skeptic passed this cell because its margin over every readable value (King table, Aboluion thesis, four arXiv papers) is at least 3 codewords.
