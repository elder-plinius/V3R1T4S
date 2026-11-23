# The record we compare against

This file records each page by URL, fetch time, HTTP status, selected headers, hashes and the extracted cell. The
pages themselves are not copied here. Every request used the User-Agent `V3R1T4S-agent/1.0 (open-research notebook;
one honest request)`, one request per page and fetch, with no retries.

## Richard Fischer, Fermat-quotient tables

### FermQ_Sorg.txt (bases 2..10125)
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt
- scout fetch: 2026-11-07T21:59:02Z, HTTP 200, 288459 bytes,
  sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
- panel re-fetches, same sha256: NOVELTY 2026-11-07T22:05:41Z (HTTP 200); CRITERION before 2026-11-07T22:06:28Z
  (HTTP 200)
- selected headers (HEAD request at 2026-11-07T22:16:10Z, HTTP 200): `Last-Modified: Wed, 21 Oct 2026 05:59:16 GMT`,
  `Content-Length: 288459`, `Content-Type: text/plain`
- quoted lines:
  - "Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125"
  - "Die Basen sind gegenwaertig durchsucht bis 4.8E+12"
  - signature "21.10.2026  Richard Fischer"

### FermQ_Sort.txt (bases 2..1052 and 65537)
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt
- scout fetch: 2026-11-07T21:59:03Z, HTTP 200, 33141 bytes,
  sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
- panel re-fetches, same sha256: NOVELTY 2026-11-07T22:05:47Z (HTTP 200); CRITERION before 2026-11-07T22:06:28Z
  (HTTP 200)
- selected headers (HEAD request at 2026-11-07T22:16:10Z, HTTP 200): `Last-Modified: Wed, 21 Oct 2026 05:59:05 GMT`,
  `Content-Length: 33141`, `Content-Type: text/plain`
- quoted lines:
  - "Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14"
  - "Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13"
  - "65537  P: 2^16, 3, 131, 151, 163 (>1.2E+14)"

### Fischer's other files that list pairs (checked as well)
- http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt ("Extreme first bases"): scout fetch
  2026-11-07T21:59:03Z, HTTP 200, 115771 bytes, sha256 e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820;
  NOVELTY re-fetch 2026-11-07T22:05:55Z, same sha256.
- http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt ("Extreme first prime bases"): scout fetch
  2026-11-07T21:59:04Z, HTTP 200, 81696 bytes, sha256 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362;
  NOVELTY re-fetch 2026-11-07T22:06:01Z, same sha256.
- The panel also fetched Fischer's index page, News.txt, FermatQ3.txt and SwitchFermQ.txt once each. The records are
  in panel/novelty.md, section 2, and panel/criterion.md.

## Extracted cell
- Base 56350 has no row in either table. FermQ_Sorg.txt has rows for the non-perfect-powers 2..10125, and
  FermQ_Sort.txt for 2..1052 plus 65537. No base in 10126..65536 is tabulated, so the table value for the cell is none.
- The number 1024048960667 occurs in none of Fischer's files read by the panel, not even with digit separators
  removed, and 56350 never occurs as a number in them (panel/reproduce.md, panel/novelty.md, panel/criterion.md).

## OEIS
- url: https://oeis.org/search?q=1024048960667&fmt=data
- 2026-11-07T21:59:04Z (scout): HTTP 200, page sha256 16e532e890dfd9d6f7860c97bf297cb54ca1b5486d9608a759e249b18cad0716.
- 2026-11-07T22:06:13Z (NOVELTY): HTTP 200, page sha256 107b5fb7daf9672e5a83a0d7a92413ac942992f681e06c7851a7a2dbdc692000.
- CRITERION, before 2026-11-07T22:06:28Z: HTTP 200, page sha256
  74c62b0d98fe2d8122341ec64a57825b08d639379a7ee9a4e064dccdb8eb39b2.
- Each page carries per-request content, so the three hashes differ.
- result line, every time: "Sorry, but the terms do not match anything in the table."
