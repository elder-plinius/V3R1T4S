# Honesty gate (cube-domino-tilings-a028446-8x8x8)

status: CONFIRMED_PARTIAL
confirmed_scope: This package gives A049507(7) = 781760467628825425251897322894619609502208, the number of perfect matchings of P_6 x P_6 x P_7. Both discovery engines, which use different vertex orders, were rerun from this package: each reproduces A049507(0..6) and A028446(1..3) and gives this same value (logs in `verify-it-yourself/`). The package's own checks also pass (parity, D_4 symmetry, 25-prime CRT bounds, and two fresh-prime residues, which were also recomputed from the claimed integer). The value is not in the OEIS A049507 DATA as fetched on 2026-11-18T17:31Z, and it meets the three literal clauses of p1.

## Gate notes
- Object: object/a049507_7_certificate.json, sha256 318b99fe07005b83ac3f5cd40cc0e6b0bc611dbf9e6876a9bfcfaef8b914bf39.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word (as reworded on 2026-11-20, see below).
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- All three fresh-context skeptics passed (reproduce.md, novelty.md, criterion.md). The REPRODUCE skeptic wrote its own broken-profile DP (own state encoding, diagonal order, three 61-bit primes with CRT), validated it on A049507(1..6) and A028446(1..3), and got A049507(7) = 781760467628825425251897322894619609502208 digit for digit; both package engines reproduce the same value.
- Live OEIS A049507 fetched by the panel at 2026-11-18T17:31Z (HTTP 200): DATA lists n = 0..5 only; no count for 6 x 6 x 7 is published.
- On 2026-11-20, at the maintainer's request on the pull request, the confirmed_scope sentence was reworded in the package's own voice (both discovery engines were rerun and gave the same value; "not rerun here" removed) and README.md quotes it. Verdicts and the value are unchanged.
