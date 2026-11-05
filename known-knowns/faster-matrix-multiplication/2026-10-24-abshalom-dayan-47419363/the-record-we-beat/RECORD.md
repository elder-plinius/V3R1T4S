# The record compared against (snapshot, not the page)

All fetches: one plain GET, User-Agent "V3R1T4S-research-agent (honest single GET)", no cookies, no retries.

## fmm_sota.json (Sedoglavic's digest of the Lille catalogue), named by partial win p1
- URL: https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json
- fetched (UTC): 2026-10-24T17:37:57Z by the run before claiming (also 15:58:56Z by the scout and 18:05:47Z by the
  NOVELTY skeptic, same sha256)
- HTTP status: 200
- selected headers (18:05:47Z fetch): date: Sat, 24 Oct 2026 18:05:47 GMT; content-type: text/plain; charset=utf-8
- sha256 of the body: 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae
- extracted cell: {"format": [18, 19, 19], "rank": 3633, "exponent": 2.801315}; createdAt 2026-10-19T20:46:33

## Lille per-format page, named by partial win p1
- URL: https://fmm.univ-lille.fr/18x19x19.html
- fetched (UTC): 2026-10-24T17:37:57Z by the run (also 18:05:47Z by the NOVELTY skeptic, same sha256)
- HTTP status: 200
- selected headers: Server: Apache; Content-Type: text/html; Last-Modified: Fri, 19 Jun 2026 21:23:26 GMT
- sha256 of the body: 7de98cb2a073dcfaa8ee3a879caaa3f6c02c1d1ab9828b9da1cf016828161490
- extracted cell: "Description of fast matrix multiplication algorithm: <18x19x19:3816>", a block decomposition
  <9x10x10:597> + <9x10x9:534> + <9x9x10:534> + ...

## Lille catalogue index (the bank's status_source; holds the 'construction' column)
- URL: https://fmm.univ-lille.fr/
- fetched (UTC): 2026-10-24T18:05:46Z by the NOVELTY skeptic (also 15:58:56Z by the scout, same sha256);
  Last-Modified: Tue, 20 Oct 2026 08:14:45 GMT
- HTTP status: 200
- sha256 of the body: 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9
- extracted cell: row 18x19x19, rank 3633, construction Proj([[19, 0], [0]], <19x19x19:3633>) (a coordinate
  projection of LITA's 19x19x19 scheme)

## Lowest other public value found
- matmulcatalog docs/catalog.json (Chatain Lacelle, arXiv 2606.13408),
  https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json, fetched 2026-10-24T18:06:50Z,
  HTTP 200, sha256 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b: [18,19,19] rank 3595 over Q
  (lineage "19x19x19 minus row 9"), then 3798.
