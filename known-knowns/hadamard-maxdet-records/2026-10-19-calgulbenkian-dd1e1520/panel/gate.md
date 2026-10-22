# Honesty gate (hadamard-maxdet-records)

status: CONFIRMED_SOLUTION
confirmed_scope: The object is a 105 x 105 matrix with all entries +1 or -1 whose exact |det| / 2^104 is 403757419044975201959422423846994970270257858463738130848861743562151165952, strictly above the Orrick archive value 3.847437473E74, the Rokicki page value, and the sources listed above (all that I could read), and below the Barba bound, for an order where the earlier record was far below the bound.

## Gate notes
- Object: object/M105_403757419044975201959422423846994970270257858463738130848861743562151165952.txt, sha256 dd1e1520b87d97fe404bf0857235652e04d819a08484c85fd3e024fb1346d28b.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The matrix is a Hadamard matrix of order 104 with one border row and column; the novelty skeptic flagged for a maintainer ruling whether bordering counts as propagation under the PR #350 rule (no table value for order 104 determines the border).
