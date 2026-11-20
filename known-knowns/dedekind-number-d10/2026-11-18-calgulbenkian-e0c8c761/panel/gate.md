# Honesty gate (dedekind-number-d10)

status: CONFIRMED_PARTIAL
confirmed_scope: D(10) == 16 (mod 27) (hence == 7 mod 9), obtained by a truncated Burnside-Mobius sum over the 27 subgroups of order >= 9 of the Sylow 3-subgroup C3 wr C3 of S_9, agreed by two separately coded engines (C99 128-bit and Python CRT), which also give D(9) == 24 (mod 27) matching the exact value; not the full D(10), and not any other modulus.

## Gate notes
- Object: object/d10_mod27_certificate.json, sha256 e0c8c761bd684d577f82d22d078f9f6269571d1756b2dfe797c723b037774ce8.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- All three fresh-context skeptics passed (reproduce.md, novelty.md, criterion.md). The REPRODUCE skeptic derived the truncation lemma (orbits with stabiliser of order at most 3 contribute 0 mod 27), enumerated the 50 subgroups of C3 wr C3 itself, counted fixed points with its own programs, reproduced D(0..7) exactly and D(9) mod 27 = 24, and got D(10) mod 27 = 16; every per-class value equals the package's.
- Published congruences checked by the panel (arXiv:2611.13887, fetched 2026-11-18T17:31:16Z; arXiv:2302.04615): D(10) is 106 mod 210 (primes 2, 3, 5, 7 only); no modulus 9 or 27 is published, and 16 mod 27 is 1 mod 3, consistent with it.
