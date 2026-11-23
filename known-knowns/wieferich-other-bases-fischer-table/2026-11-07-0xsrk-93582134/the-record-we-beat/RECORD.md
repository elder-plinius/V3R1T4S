# The record we compare against

This file records each page by URL, fetch time, HTTP status, selected headers, hashes and the extracted cell. The
pages themselves are not copied here. Every request used the User-Agent `V3R1T4S-agent/1.0 (open-research notebook;
one honest request)`, one request per page and fetch, with no retries.

## Richard Fischer, Fermat-quotient tables

### FermQ_Sorg.txt (bases 2..10125)
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt
- scout fetch: 2026-11-07T23:19:19Z, HTTP 200, 288459 bytes,
  sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
- panel re-fetches, same sha256: NOVELTY 2026-11-07T23:26:16Z (HTTP 200); CRITERION 2026-11-07T23:29:42Z (HTTP 200)
- selected headers (HEAD request at 2026-11-07T23:39:27Z, HTTP 200): `Last-Modified: Wed, 21 Oct 2026 05:59:16 GMT`,
  `Content-Length: 288459`
- quoted lines:
  - "Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125"
  - "Die Basen sind gegenwaertig durchsucht bis 4.8E+12"
  - signature "21.10.2026  Richard Fischer"

### FermQ_Sort.txt (bases 2..1052 and 65537)
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt
- scout fetch: 2026-11-07T23:19:20Z, HTTP 200, 33141 bytes,
  sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
- panel re-fetches, same sha256: NOVELTY 2026-11-07T23:26:24Z (HTTP 200); CRITERION 2026-11-07T23:29:44Z (HTTP 200)
- selected headers (HEAD request at 2026-11-07T23:39:28Z, HTTP 200): `Last-Modified: Wed, 21 Oct 2026 05:59:05 GMT`,
  `Content-Length: 33141`
- quoted lines:
  - "Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14"
  - "Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13"
  - "65537  P: 2^16, 3, 131, 151, 163 (>1.2E+14)"

### Fischer's other files that list pairs (checked as well)
- ErstBasen.txt ("Extreme first bases"): scout fetch 2026-11-07T23:19:20Z, HTTP 200, 115771 bytes, sha256
  e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820; NOVELTY re-fetch 23:26:32Z, same sha256.
- ErstPBasen.txt ("Extreme first prime bases"): scout fetch 2026-11-07T23:19:21Z, HTTP 200, 81696 bytes, sha256
  3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362; NOVELTY re-fetch 23:26:39Z, same sha256.
- NOVELTY also fetched Fischer's index page, News.txt, SwitchFermQ.txt, FermatQ3.txt, Statistik.txt,
  PQuotient_Sort.txt and Generelles.txt once each (panel/novelty.md, section 1).

## Extracted cell
- Base 36260 has no row in either table. FermQ_Sorg.txt has rows for the non-perfect-powers 2..10125, and
  FermQ_Sort.txt for 2..1052 plus 65537. No base in 10126..65536 is tabulated, so the table value for the cell is none.
- The number 1026120862861 occurs in none of Fischer's ten Fermat-quotient files, not even with digit separators
  removed, and 36260 never occurs as a number in them (panel/novelty.md, section 3).

## OEIS
- url: https://oeis.org/search?q=1026120862861&fmt=data
- 2026-11-07T23:19:21Z (scout): HTTP 200, page sha256 fd8c2d7674701b25dad8e075262044adc7ce14c53a97f33e290fd123f309d0ce.
- 2026-11-07T23:26:47Z (NOVELTY): HTTP 200, page sha256 487100a0990c88ea5d45f533903edf64fd871e3e6faea6bfd807a71a9ca92156.
- 2026-11-07T23:29:46Z (CRITERION): HTTP 200, page sha256 5de2872d3163db421f9d6301ec0b038ec5a2a33bbe32a08bd6452a193f27993f.
- Each page carries per-request content, so the three hashes differ.
- result line, every time: "Sorry, but the terms do not match anything in the table."
