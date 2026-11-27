# Record compared against (metadata only, no page copies)

Each URL fetched once with curl (user agent "V3R1T4S-kit (whosedreams)"), no retries.

## Packaging-time fetch, 2026-11-23T23:39:09Z (2026-11-23 18:39:09 ET, America/Toronto, UTC-5)
- Sequence entry (JSON): https://oeis.org/search?q=id:A334497&fmt=json
  HTTP 200, 1708 bytes, sha256 149cd9be2665bd90edee91c34b625f0ab18ffed4b9d547916d5d2a883bf260ae (byte-identical to the 2026-11-22 fetch below).
  Name: "Maximum value of eventual period for any starting configuration for a rule 30 cellular automaton in a cyclic universe of width n."
  Revision 40, last edited 2026-06-12T18:55:01-04:00. DATA has 36 terms, ending a(34)=5656002, a(35)=18480630, a(36)=2237472. No a(37).
- Sequence b-file: https://oeis.org/A334497/b334497.txt
  HTTP 200, 338 bytes, sha256 7339a6ff9bd1784e65389af0b1c40de0f308d57dc1b30f6be925ee8b8c26b6f4. Largest index present: 36 (a(36)=2237472). Index 37: absent.
- Floor sequence A334496 (eventual period of a single cell, Rule 30, cyclic width n), JSON https://oeis.org/search?q=id:A334496&fmt=json
  HTTP 200, 1307 bytes, sha256 730cb5f2d04d5adaf365015166afb6b83bd727c74efb2873354757b4726a0309, revision 24 (2020-05-09). a(37)=49276415.
  b-file https://oeis.org/A334496/b334496.txt: HTTP 200, 602 bytes, sha256 41bab2d2d541daac64910658d6173cf1179aec069ed2102a5c9fffaa345a2b25, line "37 49276415".
- Value search https://oeis.org/search?q=49276415&fmt=json: HTTP 200, one result, A334496 only.

## Published sampled value (not a table of exhaustive terms)
- Stephen Wolfram, "Random sequence generation by cellular automata", Adv. Appl. Math. 7 (1986) 123-169: https://content.wolfram.com/sw-publications/2020/07/random-sequence-generation-cellular-automata.pdf
  fetched 2026-11-23T23:46:57Z (18:46:57 ET), HTTP 200, 36010752 bytes, sha256 6db3ca1269cec7e50597fd1023d52f7ec83d17277e57447e8591530f9682719a. Table 9.2, column CA30, row N=37: 49276415 (log2 25.6). Caption: "In the former case, a selection of seeds, including single nonzero sites, were used." So it is a lower bound. Same table, for comparison: N=22 3256, N=27 67554, N=30 306120, all below the later exhaustive or larger values now in A334497 (3553, 240300, 374265).

## Pre-registration fetch, 2026-11-22T16:49:14Z (2026-11-22 11:49:14 ET), before the run
- A334497 JSON: HTTP 200, 1708 bytes, sha256 149cd9be2665bd90edee91c34b625f0ab18ffed4b9d547916d5d2a883bf260ae.
- A334497 b-file: HTTP 200, 338 bytes, sha256 7339a6ff9bd1784e65389af0b1c40de0f308d57dc1b30f6be925ee8b8c26b6f4 (the copy used by the self-test, see how-we-built-it/logs/kit_sha256.txt, data/b334497.txt).

Cell compared: A334497(37); not listed at either fetch; last published term a(36)=2237472; claimed value 49276415, which equals the floor A334496(37)=49276415 and Wolfram's 1986 sampled value for N=37.
