# The record we compare against

This is a snapshot record of the pages: their URLs, fetch times, status, selected headers, hashes and the extracted cell.
The pages themselves are not copied here.

## Richard Fischer, Fermat-quotient tables

### FermQ_Sorg.txt (bases 2..10125)
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt
- scout fetch: 2026-11-07T11:58:09Z, HTTP 200, 288459 bytes,
  sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
- panel re-fetch (NOVELTY): 2026-11-07T12:18:47Z, HTTP 200, same sha256
- selected headers (panel re-fetch): `Last-Modified: Wed, 21 Oct 2026 05:59:16 GMT`, `Content-Length: 288459`
- quoted lines:
  - "Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125"
  - "Die Basen sind gegenwaertig durchsucht bis 4.8E+12"
  - last base row "10125,  2, 7, 17093, 123151337"
  - signature "21.10.2026  Richard Fischer"

### FermQ_Sort.txt (bases 2..1052 and 65537)
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt
- scout fetch: 2026-11-07T11:58:10Z, HTTP 200, 33141 bytes,
  sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
- panel re-fetch (NOVELTY): 2026-11-07T12:18:48Z, HTTP 200, same sha256
- selected headers (panel re-fetch): `Last-Modified: Wed, 21 Oct 2026 05:59:05 GMT`, `Content-Length: 33141`
- quoted lines:
  - "Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14"
  - "Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13"
  - "65537  P: 2^16, 3, 131, 151, 163 (>1.2E+14)"

## Extracted cell
- Base 24766 has no row in either file.
- The bases with rows are the non-perfect-powers 2..10125 in FermQ_Sorg.txt, and 2..1052 plus 65537 in FermQ_Sort.txt.
- The number 1000747824697 occurs in neither file: token, substring and digit-stream searches all came back empty
  (panel/criterion.md, panel/reproduce.md).

## OEIS
- url: https://oeis.org/search?q=1000747824697&fmt=data
- 2026-11-07T12:15:50Z (scout), HTTP 200, page sha256 2118262b0a4cb689524fa5252f2a465556c12f8a99dac1e75272b079e3156cb5
- 2026-11-07T12:22:21Z (NOVELTY) and 2026-11-07T12:24:27Z (CRITERION), both HTTP 200. Their hashes are in the panel
  files; each page carries its own timestamp, so the hashes differ.
- result line, every time: "Sorry, but the terms do not match anything in the table."
