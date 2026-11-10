# The record we compare against

This file records each page by URL, fetch time, HTTP status, selected headers, hashes and the extracted cell. The
pages themselves are not copied here. Every request used the User-Agent `V3R1T4S-agent/1.0 (open-research notebook;
one honest request)`, one request per page and fetch, with no retries.

## Richard Fischer, Fermat-quotient tables

### FermQ_Sorg.txt (bases 2..10125)
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt
- scout fetch: 2026-11-07T20:11:24Z, HTTP 200, 288459 bytes,
  sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
- panel re-fetches, same sha256: NOVELTY 2026-11-07T21:08:48Z (HTTP 200), CRITERION 2026-11-07T21:15:55Z (HTTP 200)
- selected headers (HEAD request at 2026-11-07T20:43:12Z, HTTP 200): `Last-Modified: Wed, 21 Oct 2026 05:59:16 GMT`,
  `Content-Length: 288459`, `Content-Type: text/plain`
- quoted lines:
  - "Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125"
  - "Die Basen sind gegenwaertig durchsucht bis 4.8E+12"
  - signature "21.10.2026  Richard Fischer"

### FermQ_Sort.txt (bases 2..1052 and 65537)
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt
- scout fetch: 2026-11-07T20:11:25Z, HTTP 200, 33141 bytes,
  sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
- panel re-fetches, same sha256: NOVELTY 2026-11-07T21:08:54Z (HTTP 200), CRITERION 2026-11-07T21:16:01Z (HTTP 200)
- selected headers (HEAD request at 2026-11-07T20:43:13Z, HTTP 200): `Last-Modified: Wed, 21 Oct 2026 05:59:05 GMT`,
  `Content-Length: 33141`, `Content-Type: text/plain`
- quoted lines:
  - "Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14"
  - "Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13"
  - "65537  P: 2^16, 3, 131, 151, 163 (>1.2E+14)"

### Fischer's other files that list pairs (checked as well)
- http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt ("Extreme first bases"): scout fetch
  2026-11-07T20:11:25Z, HTTP 200, 115771 bytes, sha256 e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820;
  NOVELTY re-fetch 2026-11-07T21:09:00Z, HTTP 200, same sha256.
- http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt ("Extreme first prime bases"): scout fetch
  2026-11-07T20:11:25Z, HTTP 200, 81696 bytes, sha256 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362;
  NOVELTY re-fetch 2026-11-07T21:09:09Z, HTTP 200, same sha256.
- NOVELTY also fetched Fischer's index page, News.txt, Generelles.txt, Statistik.txt, FermatQ3.txt, SwitchFermQ.txt and
  PQuotient_Sort.txt once each. The records are in panel/novelty.md, section 2.

## Extracted cell
- Base 28860 has no row in either table. FermQ_Sorg.txt has rows for the non-perfect-powers 2..10125, and
  FermQ_Sort.txt for 2..1052 plus 65537. No base in 10126..65536 is tabulated, so the table value for the cell is none.
- The number 1017279755641 occurs in none of Fischer's ten Fermat-quotient files or his index page, not even with
  digit separators removed, and 28860 never occurs as a number in them (panel/novelty.md, section 2). REPRODUCE and
  CRITERION found the same in the files they read (panel/reproduce.md, panel/criterion.md).

## OEIS
- url: https://oeis.org/search?q=1017279755641&fmt=data
- 2026-11-07T20:11:27Z (scout): HTTP 200, page sha256 7351e525c3e631a5f1b9b61bf5805bb61dd6e5cc534eb78aed51ad96aefe0a8b.
- 2026-11-07T21:10:36Z (NOVELTY): HTTP 200, page sha256 b518720451780beab298bf9e640fa531dc2136b315fd90a15651d88467861a8a.
- 2026-11-07T21:15:43Z (CRITERION): HTTP 200, page sha256 a507f9e958842e3ad0ab63d52d0204dca316b918c53adbec7a97b0f67d561c4c.
- Each page carries per-request content, so the three hashes differ.
- result line, every time: "Sorry, but the terms do not match anything in the table."
