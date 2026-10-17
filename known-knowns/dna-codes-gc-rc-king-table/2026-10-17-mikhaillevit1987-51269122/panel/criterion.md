# Skeptic: criterion (protocol 2)

context: fresh subagent spawned by the run coordinator with only the claim/ folder as input (no prior run context), instructed to decide literally whether the result meets the full success criterion or a named partial win; network read-only.

## Checks performed

1. Object validity (own checker written before reading checker/check_dna.py, then author checker run too).
   - object/code_20_15_16.json sha256 = e3a3a885c67a9a34329ed2247d32dfe004b64645b8d2bd97ef528009a77e2de7 (matches CLAIM.md).
   - 16 words, 16 distinct, all length 20 over ACGT, GC count 10 for every word (= floor(20/2)).
   - min pairwise Hamming = 15; min over all x,y (x=y included) of H(x, rc(y)) = 15. No word's reverse complement is in the code.
   - checker/check_dna.py --self-test: PASS; on the object: {"valid": true, "n": 20, "d": 15, "w": 10, "size": 16}. Both checkers agree.
2. Live table re-fetch (2026-10-17T23:07:40Z UTC): https://rambutan.umassmed.edu/king/dnacodes.html, HTTP 200, 18096 bytes, sha256 25d6e9f8...18c5 (identical to table_record/fetch.json; Last-Modified 2024-06-07; page says "Last updated June 23, 2010").
   - Second table, Lower bounds for A4^GC,RC(n,d,w), row n=20, column d=15: `15` with superscript `v`, no period, no colon -> unmarked, eligible. 16 > 15.
3. Post-2010 published values for (n,d)=(20,15), GC,RC:
   - sources/montemanni_smith_koul_2014_lnms6.pdf, Table 2 (image, read by rendering): row 20 V=15^N, B=14 -> 15.
   - sources/aboluion_smith_perkins_2012_dm312.pdf, Table 9 (max over w of A4^GC,RC): row 20, d=15 = 15_m3 -> 15. Note: this table is max_w, a weaker quantifier than w=10; it still does not exceed 15.
   - sources/aboluion_phd_thesis_2011.pdf, Table 10.72 (max_w): row 20, d=15 = 15_m3 -> 15.
   - arXiv 1607.00266 (2016 survey), GC+RC table: row 20, d=15 = 15.
   - arXiv 1903.03535 (named in the criterion): improvements only for (17,4), (17,7), (13,5), (29,11); nothing for (20,15).
   - arXiv 1902.04419 (n <= 10), arXiv 2108.02033 (n in {16,24,32,...}), arXiv 2409.06519 (n=20 only for d=4,6), arXiv 2403.11551, arXiv 2510.01750 (no bound tables): no (20,15) GC,RC value.
   - Largest post-2010 published value found: 15. 16 is strictly greater.
4. Hidden quantifiers / stretched definitions:
   - "GC count = floor(n/2)": satisfied exactly (w=10), not max over w.
   - RC self-pairs: included in both checkers (x=y); verified by the self-test negative case.
   - "re-fetched immediately before claiming": author fetch 2026-10-17T22:36Z; my re-fetch is byte-identical, so the entry is current.
   - Null model / subsumption: the GC-only table gives A4^GC(20,15,10) >= 33, so 16 is below the trivial halving ceiling (16.5) and is not the halving-gap partial win; it is a direct full-criterion claim. An RC-only (no GC) bound of 16 at (20,15) appears in the 2016 survey (Table XIV), but that is a different, less constrained quantity and does not subsume a GC,RC code. No published GC,RC code of size >= 16 found.
5. Novelty caveat: a literature search cannot be exhaustive. One possibly relevant post-2010 paper could not be read (see below); it concerns algebraic conflict-free codes with extra constraints, and its abstract does not name (20,15).

## Sources that could not be read (paywall / login / block)

- S. T. Dougherty, A. Korban, S. Sahinkaya, D. Ustun, "Construction of DNA Codes From Composite Matrices and a Bio-Inspired Optimization Algorithm", IEEE Trans. Inf. Theory 69(3) (2023) 1588-1603, https://doi.org/10.1109/TIT.2022.3217518 -> https://ieeexplore.ieee.org/document/9931134/ : IEEE Xplore answered HTTP 202 with an empty body (bot challenge / paywall); not readable.
  - Repository copy https://acikerisim.tarsus.edu.tr/items/78e7ee6c-4410-4507-858f-d10490425fdb/full : TLS handshake failed (schannel), and search metadata lists it as restricted access.
  - Repository copy https://aperta.ulakbim.gov.tr/records/273382 : open record but holds only a bibliographic .txt, no full text.
- The three PDFs in claim/sources/ were blocked to automated clients (HTTP 403, per sources/SOURCES.md) but were supplied by the human and were read in full here.

## Verdict

Meets the full success criterion (not merely a partial win): valid code, unmarked live entry 15, size 16 strictly greater than the live entry and than every post-2010 published value located (all 15). Residual risk: the unread IEEE TIT 2023 paper and unpublished/unindexed code files.

confirmed_scope: The 16-word list in object/code_20_15_16.json is a valid length-20 DNA code with GC count 10, minimum Hamming distance 15 and reverse-complement distance at least 15 (self-pairs included), so A_4^GC,RC(20,15,10) >= 16, exceeding the unmarked live King-table entry 15 (re-fetched 2026-10-17T23:07Z) and every post-2010 published value for (20,15) found in the sources checked (all 15), with one paywalled 2023 IEEE TIT paper unread.

pass: true
