# The record we compared against

| URL | fetched (UTC) | HTTP | sha256 of the page as fetched |
|---|---|---|---|
| https://oeis.org/A002224 | 2026-11-27T16:27:36Z | 200 | e8763c3a42f50f8011ac20c1eadad666f169a884c247cbbcef83653f9add4861 |
| https://oeis.org/A002224/b002224.txt | 2026-11-27T16:27:36Z | 200 | 70fa340ea4ea5035017afad7742632f61ae03c75cafdcf7ab0e69f2b99579ce8 |

Re-fetched by the NOVELTY skeptic at 2026-11-27T16:44:42Z (HTTP 200, byte-identical b-file; see panel/novelty.md).
Client: curl with User-Agent "V3R1T4S-agent (research notebook)", one request each, no retries.

Extracted cell: the b-file (Michael Hortmann, n = 1..41) ends with `41 178936222537081`. There is no entry for
n = 42: the cell A002224(42) is empty. Definition on the page: "Smallest prime p of form p = 8k+1 such that first n
primes (p_1=2, ..., p_n) are quadratic residues mod p."
