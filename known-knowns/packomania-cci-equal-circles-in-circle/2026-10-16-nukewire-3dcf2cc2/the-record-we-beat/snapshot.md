# The record we beat (table snapshot)

- Table: Packomania, "The best known packings of equal circles in a circle" (cci), by Eckard
  Specht. Human page: https://packomania.com/cci/cci.html — machine-readable table:
  https://packomania.com/cci/txt/radius.txt
- Fetched: 2026-10-16T09:46:29Z, plain curl (default client), one request.
- HTTP status: 200; 96415 bytes; 2735 rows.
- sha256 (radius.txt): 6c60da0a2feb2ad01f2bed8dd99646021bcfd4cbfecb5ea2a7b332ecfa0beead
- sha256 (cci.html, same session): a90494f628fb596e9aea6a6b74b852bb9ecd51f43eaeeb562dd2984b5d5a090a
- Extracted cell compared against: row 4141 = `4141 0.014601755763187308074373236782`
  (our candidate: 0.0146094714488139345759856245307, margin 7.7157e-6).
- Page state: "Last update: 25-Dec-2024"; no dated History-of-updates line mentions 4141;
  newest news line 11-Oct-2026 (N=15 optimality proofs, a different cell).
- Row provenance (cited on the live page): reference [31] "program cci, 1999-2024" — the site's
  own construction program; the posted configuration cci4141.txt reproduces this row value
  (integrity verified at 60+ digits, diff about -8.3e-31).
- Queue check same day: https://packomania.com/pending-requests.html (2026-10-16, HTTP 200,
  sha256 0d6ebbbe8e95abe7e701e1c70fbc1c0ec5bb06d611822b0b135ce3b776972384, page dated
  08-Oct-2026) lists no cci entries; the 26-Sep-2026 category-unspecified "Moki & Julio *many*"
  4666-candidate bundle remains the mandatory caveat named in the confirmed scope.
- The NOVELTY panelist re-fetched the table independently at 2026-10-16T10:08:38Z and read the
  identical row (sha256 byte-identical).
