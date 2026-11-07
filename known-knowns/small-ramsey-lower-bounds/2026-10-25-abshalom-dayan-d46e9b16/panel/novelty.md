context: headless claude -p session (claude-opus-5-5, effort high), fresh, started inside a copy of claim/ .

# NOVELTY verdict: R(3,3,14) >= 267

Verdict: novelty CONFIRMED. N+1 = 267 strictly beats the DS1 entry 242 (margin +25). Nothing newer found in the
literature, the repo or its open pull requests matches it, and no published general construction implies it.

## 1. Status source (one plain request per page, curl, User-Agent "V3R1T4S-novelty-skeptic/1.0 (read-only status check)")

- https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1 , requested 2026-10-25T07:58:52Z:
  `HTTP 200 bytes 17621`, sha256 0a6d60699454752bbbad69c6ce2b682b8bb661352cc0224af9ca88838b55fe5e. Page text:
  "This Version DS1: Apr 24, 2026". The sha256 differs from the scout's (ff5f...) but the byte count and version are
  the same; the page probably has a per-request token. No block, no challenge.
- https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf , requested 2026-10-25T07:59:00Z:
  `HTTP 200 bytes 585821 type application/pdf`, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc
  (same as the scout's in table_record.md), "PDF document, version 1.4, 149 pages".
- Value: section 6.1.2, Table XIb (pdftotext -layout), row k = 3, column m = 14:
  ```
          m          4      5       6      7       8        9     10     11    12    13    14    15    16
                    30    45       61     85     103      129    150   174    194   217   242   269   291
      3
                   Ka2   Ex2      ExT   Ex18    Ex18     Ex18    ExT   ExT    ExT   ExT   ExT   ExT   ExT
  ```
  So DS1 has R(3,3,14) >= 242 [ExT]. The claim's N+1 = 267 > 242. DS1 mentions R(3,3,14) nowhere else (grep).

## 2. General constructions and related cells (DS1 section 6.2, with DS1 two-colour values R(3,12) >= 53,
R(3,13) >= 61, R(3,14) >= 67 from Table Ia)

Computed with python3 (real output):
```
6.2.g  R(3,3,14) >= 4R(3,13)-3 = 241
6.2.g  max possible if R(3,13)=68 (its DS1 upper bound) = 269
6.2.q  R(3,3,14) > (R(3)-1)(R(3,14)-1) = 132 -> >= 133
6.2.q  R(3,3,14) > (R(3,3)-1)(R(14)-1) = 65 -> >= 66
6.2.r  order (3,14,3): (3+1)(R(12,3)-1) = 208 -> >= 209
6.2.j  Giraud/Rowley cyclic: L(3,3,14) >= 25*L(3,3)-12 = 113 ; ((2L(3)-1)(2L(3,14)-1)+1)/2 = 197
```
- 6.2.g would reach 267 only if R(3,13) >= 68, i.e. R(3,13) = 68 exactly; the best published lower bound is 61
  (arXiv:2603.09172), so no.
- 6.2.o reduces here to the 6.2.q values; 6.2.h needs four or more colours; 6.2.b/c/k/l/m/n/p are diagonal or
  need other parameters. None reaches 267.
- R(3,3,15) >= 269 (DS1) does not imply anything for m = 14: monotonicity gives R(3,3,14) <= R(3,3,15), an upper
  relation only.
- R(5,14) >= 267 (DS1 Table Ia, from Kuznetsov [Kuz]) does not imply R(3,3,14) >= 267 by any published result. The
  splitting idea (Exoo-Tatarevic 2015) only works when a particular K5-free colour can actually be split into two
  triangle-free parts, which has to be checked case by case. The general inequality goes the other way
  (R(3,3,k) <= R(6,k)). Kuznetsov's paper (arXiv:1505.07186v5, fetched HTTP 200) states no three-colour bound: grep for
  "3, 3, 1", "multicol" and "split" finds only a bibliography entry. I confirmed that colours 1 and 2 together are exactly
  his printed (5,14) connection set: `Kuznetsov set size 47 | colour1 u colour2 == Kuznetsov set: True | disjoint: True`.
  So the split is new, but the base graph is his. The credit for that is already in CLAIM.md.

## 3. Literature, last 24 months (2024-10-25 to 2026-10-25)

- arXiv API query (Ramsey AND lower bound AND multicolor/three colors/circulant, sorted by date), fetched
  2026-10-25T08:00:53Z, `HTTP 200 bytes 83923`, 48 entries, of which 17 are from the window. None has a
  three-colour R(3,3,k) table value in its abstract.
- Abstract pages (each fetched once, all HTTP 200), with what they actually claim:
  - 2603.09172 (Nagda, Raghavan, Thakurta, 2026-03-10): two-colour only (R(3,13) 60->61, R(3,18), R(4,k)).
  - 2608.18169 (Yu, 2026-08-17): R(4,20) >= 252, two-colour.
  - 2608.18769 (Coniglio, Furini, Ljubic, San Segundo, 2026-08-19): two-colour R(3,n), 24 <= n <= 49 (full PDF
    grepped: no three-colour bounds, no R(3,13)/R(3,14) improvements).
  - 2610.12122 (Cremer, 2026-10-08): R(6,8) >= 135, R(8,10) >= 345, two-colour.
  - 2609.28455 (Andrades, Campos, Morris, 2026-09-23): R(3,3,k) = Theta(k^3/(log k)^2), asymptotic only, no small values.
  - 2509.03784 (Wesley, 2025-09-04): R(K4,K4-e,K4-e) >= 35, R(K3,K4,C4,C4) >= 49, not R(3,3,14).
  - 2603.10851 (Boza, 2026-03-11): upper bounds only.
  - 2601.15183, 2601.05221: asymptotic multicolour bounds and a survey.
- ScaleAutoResearch-Ramsey (Yiping Wang, README via the GitHub API, HTTP 200): R(3,17) >= 93 and R(4,15) >= 160
  only, two-colour.
- Web searches ("R(3,3,14)" lower bound; new multicolour R(3,3,k) bounds 2025/2026; Rowley's multicolour tables) turned
  up only Exoo-Tatarevic 2015 (R(3,3,14) 233 -> 242 by splitting) as a source for this cell. Nothing 2024-2026 gives
  R(3,3,14) >= 243.

## 4. Repository github.com/elder-plinius/V3R1T4S (read-only, fetched 2026-10-25T08:00:03Z to 08:00:18Z)

- TROPHY_CASE.md (raw, `TROPHY HTTP 200 bytes 31235`): six families (degree-diameter, constant-weight codes, matrix
  multiplication, Lehmer, VNN-COMP, RobustBench) and cipher commitments. `grep -c -i ramsey` = 0.
- Open pull requests (API, pages 1-4, each HTTP 200; 100+100+100+53 = `total open PRs: 353`). Searching titles and bodies
  for ramsey|R(3|multicolour|clique|K_14|circulant gave 2 hits, #614 (AME states table) and #509 (qubit stabilizer
  code), neither about Ramsey numbers. I did not open the PRs' files.

## 5. Sanity check of the object (beyond novelty, short)

- `shasum -a 256 object/R_3_3_14.txt` -> d46e9b167a93492eb02cabc1d2d9f81c975ea68698cb55944a4afac2463034ba (matches CLAIM.md).
- My own exhaustive branch and bound (work/mybb.py, written before reading verify_circ.py's search; sha256
  605204cf...afdc): `S3 size 172 clique of size 13 in S3 found: False nodes 15877186` (47.66 s); control
  `clique of size 12 in S3 found: True`. So colour 3 has clique number 13: no K14, and the bound is tight.
- My own triangle check (work/mycheck.py): `colour 1 triangles through 0: 0`, `colour 2 triangles through 0: 0`. Its
  CP-SAT part did not finish within 840 s (`status FEASIBLE ... = 12.0 bound 42.0`), so it settles nothing about K14.
- Author's verify_circ.py: `proves R(3,3,14) >= 267`, `PASS`.
- Process note: one run of the author's checker went without nice (the shell said "nice(5) failed: operation not
  permitted"). It ran single-threaded with a CPU-time cap (ulimit -t). Peak memory in every run was under 150 MB.

## Conclusion

R(3,3,14) >= 267 is strictly greater than the DS1 (Apr 24, 2026) value 242, and than anything I found in 2024-2026
papers, in TROPHY_CASE.md or in the 353 open pull requests. No general construction listed in DS1 6.2 gives more than
241 with current two-colour bounds. This is not a tie; the margin is +25.

pass: true
