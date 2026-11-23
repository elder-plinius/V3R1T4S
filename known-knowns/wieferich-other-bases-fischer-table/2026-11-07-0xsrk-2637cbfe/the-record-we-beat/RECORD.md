# The record we compare against

This file records each page by URL, fetch time, HTTP status, selected headers, hashes and the extracted cell. The
pages themselves are not copied here. Every request used the User-Agent `V3R1T4S-agent/1.0 (open-research notebook;
one honest request)`, one request per page and fetch, with no retries.

## Richard Fischer, Fermat-quotient tables

### FermQ_Sorg.txt (bases 2..10125): the table that governs base 5481
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sorg.txt
- scout fetch, immediately before the claim: 2026-11-07T22:40:10Z, HTTP 200, 288459 bytes,
  sha256 35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4
- panel re-fetches, same sha256: NOVELTY 2026-11-07T22:45:05Z (HTTP 200); CRITERION between 2026-11-07T22:46:58Z and
  22:47:13Z (HTTP 200)
- selected headers (HEAD request at 2026-11-07T22:53:59Z, HTTP 200): `Last-Modified: Wed, 21 Oct 2026 05:59:16 GMT`,
  `Content-Length: 288459`, `Content-Type: text/plain`
- quoted lines:
  - "Die gefundenen Primzahlen (P) der Fermatquotienten von der Basis 2 bis 10125"
  - "Die Basen sind gegenwaertig durchsucht bis 4.8E+12"
  - the row of base 5481: `5481,  2^3, 751787`
  - signature "21.10.2026  Richard Fischer"

### FermQ_Sort.txt (bases 2..1052 and 65537)
- url: http://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt
- scout fetch: 2026-11-07T22:40:10Z, HTTP 200, 33141 bytes,
  sha256 bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b
- panel re-fetches, same sha256: NOVELTY 2026-11-07T22:45:14Z (HTTP 200); CRITERION between 22:46:58Z and 22:47:13Z
  (HTTP 200)
- selected headers (HEAD request at 2026-11-07T22:53:59Z, HTTP 200): `Last-Modified: Wed, 21 Oct 2026 05:59:05 GMT`,
  `Content-Length: 33141`, `Content-Type: text/plain`
- It has no row for base 5481.

### SwitchFermQ.txt (double Wieferich pairs: the headline flag)
- url: http://www.fermatquotient.com/FermatQuotienten/SwitchFermQ.txt
- scout fetch: 2026-11-07T22:40:12Z, HTTP 200, 10726 bytes,
  sha256 8190a7ca0bf2a31d9b03b77e97e5d09f45abc8b7df6f4321d706732b329f3faa
- panel re-fetches, same sha256: NOVELTY 2026-11-07T22:49:49Z; CRITERION between 22:46:58Z and 22:47:13Z
- It mentions neither 5481 nor p.

### Fischer's other files read
- ErstBasen.txt: scout fetch 2026-11-07T22:40:11Z, HTTP 200, 115771 bytes, sha256
  e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820; NOVELTY re-fetch 22:49:49Z, same sha256.
- ErstPBasen.txt: scout fetch 2026-11-07T22:40:11Z, HTTP 200, 81696 bytes, sha256
  3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362; NOVELTY re-fetch 22:49:49Z, same sha256.
- NOVELTY also fetched Fischer's index page, News.txt and FermatQ3.txt once each (panel/novelty.md, section 1).

## Extracted cell
- Base 5481 is governed by FermQ_Sorg.txt, which states one searched limit for its bases, 4.8E+12. The row carries no
  per-row note.
- The row lists the Wieferich primes 2 (written 2^3: 5481 ≡ 1 mod 8) and 751787. Table value for the cell: 2 and
  751787 below 4.8E+12.
- p = 4848813530161 is strictly greater than the stated limit, by 48813530161 (1.0%). It occurs in none of the files
  above.
- The table lists no entry above 4.8E+12 for any base from 1053 to 10125 (panel/criterion.md).

## OEIS
- url: https://oeis.org/search?q=4848813530161&fmt=data
  - 2026-11-07T22:40:12Z (scout): HTTP 200, page sha256
    124007da4c378ce70533976e1d5cbabb7d38f1acb0e887f63ecc662aca92507d.
  - 2026-11-07T22:45:19Z (NOVELTY): HTTP 200, page sha256
    d52d33b8cb6d89250b19f7d363c587eae781d3fa058663670a2716af0ebd6be8.
  - CRITERION, between 22:46:58Z and 22:47:13Z: HTTP 200, page sha256
    4bd7d4d125da3b5c2559eead8ae0d6b51ce626836ef129de349c957d45b3335d.
  - Each page carries per-request content, so the hashes differ. The result line every time is "Sorry, but the
    terms do not match anything in the table."
- A base-5481 Wieferich sequence, if one existed, would contain the row's prime 751787.
  - NOVELTY searched https://oeis.org/search?q=751787&fmt=data at 22:45:35Z (HTTP 200, page sha256
    08e126fbcd778f0fa91b693861e3683ded878713e96246281dfc8281c986b3ea). It found four sequences (A042380, A181245,
    A181241, A208267), none of them a Wieferich sequence. CRITERION found the same four.
  - NOVELTY's search for "Wieferich 5481" (22:45:30Z, HTTP 200) returned no match.
