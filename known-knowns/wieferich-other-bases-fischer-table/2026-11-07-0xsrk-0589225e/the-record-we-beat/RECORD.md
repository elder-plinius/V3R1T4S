# The record we compare against

This is a snapshot record of the pages: their URLs, fetch times, status, selected headers, hashes and the extracted cell.
The pages themselves are not copied here. User-Agent on every request: `V3R1T4S-agent/1.0 (open-research notebook;
one honest request)`, one request per page and fetch, no retries.

## Richard Fischer, Fermat-quotient tables

### FermQ_Sorg.txt (bases 2..10125)
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt
- scout fetch: 2026-11-07T17:53:48Z, HTTP 200, 288459 bytes,
  sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
- panel re-fetches, same sha256: NOVELTY 2026-11-07T18:34:23Z (HTTP 200), REPRODUCE 2026-11-07T18:40:34Z (HTTP 200)
- selected headers (NOVELTY's fetch, HTTP 200): `Last-Modified: Wed, 21 Oct 2026 05:59:16 GMT`,
  `Content-Length: 288459`, `Content-Type: text/plain`
- quoted lines:
  - "Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125"
  - "Die Basen sind gegenwaertig durchsucht bis 4.8E+12"
  - signature "21.10.2026  Richard Fischer"

### FermQ_Sort.txt (bases 2..1052 and 65537)
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt
- scout fetch: 2026-11-07T17:53:49Z, HTTP 200, 33141 bytes,
  sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
- panel re-fetches, same sha256: NOVELTY 2026-11-07T18:34:23Z (HTTP 200), REPRODUCE 2026-11-07T18:40:34Z (HTTP 200)
- selected headers (NOVELTY's fetch, HTTP 200): `Last-Modified: Wed, 21 Oct 2026 05:59:05 GMT`,
  `Content-Length: 33141`, `Content-Type: text/plain`
- quoted lines:
  - "Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14"
  - "Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13"
  - "65537  P: 2^16, 3, 131, 151, 163 (>1.2E+14)"

### Fischer's other files that list pairs (checked as well)
- http://www.fermatquotient.com/FermatQuotienten/ErstBasen.txt ("Extreme first bases"): scout fetch 2026-11-07T17:53:49Z, HTTP 200, 115771 bytes,
  sha256 e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820; NOVELTY re-fetch 2026-11-07T18:34:24Z, same sha256.
- http://www.fermatquotient.com/FermatQuotienten/ErstPBasen.txt ("Extreme first prime bases"): scout fetch 2026-11-07T17:53:50Z, HTTP 200, 81696 bytes,
  sha256 3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362; NOVELTY re-fetch 2026-11-07T18:34:24Z, same sha256.
- NOVELTY also fetched News.txt, FermatQ3.txt, SwitchFermQ.txt, Statistik.txt, PQuotient_Sort.txt and Generelles.txt
  once each (records in panel/novelty.md, section 3).

## Extracted cell
- Base 17766 has no row in either table. The bases with rows are the non-perfect-powers 2..10125 in FermQ_Sorg.txt,
  and 2..1052 plus 65537 in FermQ_Sort.txt. No base in 10126..65536 is tabulated, so the table value for the cell is
  none.
- The number 1016845912283 occurs in no Fischer file read for this claim, neither as a number nor inside a longer one
  (panel/reproduce.md, panel/novelty.md, panel/criterion.md). 17766 never occurs as a number in them either; it occurs
  only inside the longer number 817766595407 (row 234).

## OEIS
- url: https://oeis.org/search?q=1016845912283&fmt=data
- 2026-11-07T18:30:31Z (scout), HTTP 200, page sha256 34e1541f00d72f97775ca8fd612a8d2b668b677504b8de1bd5b60ac17e915e5f
- 2026-11-07T18:34:24Z (NOVELTY), 2026-11-07T18:38:45Z (CRITERION) and 2026-11-07T18:40:34Z (REPRODUCE), all HTTP 200.
  Their hashes are in the panel files; each page carries its own per-request token, so the hashes differ.
- result line, every time: "Sorry, but the terms do not match anything in the table."
