# The record we beat: the Allanach-Davighi-Melville anomaly-free atlas

source: B. C. Allanach, J. Davighi, S. Melville, "An anomaly-free atlas: charting the space of flavour-dependent
gauged U(1) extensions of the Standard Model", JHEP 02 (2019) 082, arXiv:1812.04602 (version v5), and its erratum
JHEP 08 (2019) 064.
url: https://arxiv.org/abs/1812.04602v5
url (erratum): https://doi.org/10.1007/JHEP08(2019)064
url (data record named in both): http://doi.org/10.5281/zenodo.3345889 (not read: see below)

## How the table was obtained (no live fetch)

The contributor's machine cannot reach arxiv.org, link.springer.com or zenodo.org: one plain `curl` per URL, by the
NOVELTY skeptic at 2026-10-23T19:39:01Z, was refused by the outbound proxy (`curl: (56) CONNECT tunnel failed,
response 403`, http_code 000; earlier attempts on 2026-10-18 and 2026-10-20 ended the same way, see
`panel/novelty_round1_pending.md`). The owner of the contributor's workspace then supplied the two primary documents
as PDF files, saved unchanged on the contributor's machine at 2026-10-23T19:38:19Z (file time, UTC). The table
below was read from text extractions of those PDFs (`pdftotext -layout`). The PDFs and extractions are not copied
into this package.

http_status: none (owner-supplied files, not an HTTP fetch; the live requests above returned no HTTP status)
fetched_utc: 2026-10-23T19:38:19Z (time the owner-supplied copies were saved)
selected headers: none (no HTTP response)

| file (owner-supplied copy) | bytes | sha256 |
|---|---|---|
| arXiv-1812.04602v5.pdf | 598427 | 022355da109e4eef72fb0cb314bea3c282fe49136f2aeae133c1ca262c275b96 |
| JHEP08-2019-064-erratum.pdf | 147987 | c6fcae4107a1e7306b58d4b0821c8b2f699e5ad06b21629e897af56b341dfcb4 |
| arXiv-1812.04602v5.txt (pdftotext extraction) | 97752 | 6d5d2d827e5c9ec32f91afac05a1d9a84dd13c670892832ce8a5e0e7fcf8d56d |
| JHEP08-2019-064-erratum.txt (pdftotext extraction) | 9008 | 85a0c55771277b2501888513a20d023fe3d1370c76c86b5bff810c6460cfedc9 |

Caveat: the PDF hashes show that the files are the ones the owner supplied; they were not compared byte for byte
with the arXiv or Springer copies (unreachable from the contributor's machine). The extraction's header line reads
`arXiv:1812.04602v5 [hep-ph] 8 Jan 2020`; the erratum's reads `JHEP08(2019)064` (Published: August 12, 2019).
Anyone can check the quoted lines against https://arxiv.org/abs/1812.04602v5 and the erratum.

## Quoted lines (verbatim from the extractions)

The first line of Table 2 and of the erratum's Table 1 starts, in the extraction, with a form feed (a page break);
it is left out below. Everything else is copied byte for byte.

arXiv:1812.04602v5, section 4.2 "Results" (extraction lines 783-785):

```
of labelled, easily read ASCII files for public use on Zenodo at http://doi.org/10.5281/
zenodo.3345889 [47] for Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR . The program
itself is also made available there if a larger value of Qmax is desired by the user.
```

arXiv:1812.04602v5, Table 2, SM (extraction lines 858-872):

```
             Qmax    Solutions     Symmetry     Quadratics      Cubics    Time/sec
              1          8             8              32           8        0.0
              2         22             14            1861         161       0.0
              3         82             32           23288        1061       0.0
              4         251            56          303949        7757       0.0
              5         626           114         1966248       35430       0.0
              6        1983           144         11470333      143171      0.2
              7        3902           252         46471312      454767      0.6
              8        7068           336        176496916     1311965      2.2
              9       14354           492        539687692     3310802      6.7
              10      23800           582       1580566538     7795283       20

Table 2. Number of inequivalent solutions to the anomaly equations for SM fermion content and
different maximum U (1)F charge Qmax . Each row contains the all-zero charge solution, as well as
the solutions indicated in the rows above. The column marked “Symmetry” shows how many of the
```

arXiv:1812.04602v5, Table 3, SMνR (extraction lines 879-892):

```
         Qmax    Solutions     Symmetry        Quadratics          Cubics      Time/sec
          1          38            16              144                38          0.0
          2         358            48             31439              2829         0.0
          3         4116          154            1571716            69421         0.1
          4        24552          338           34761022           932736         0.6
          5       111152          796          442549238          7993169         6.8
          6       435305         1218         3813718154          49541883         56
          7       1358388        2332         24616693253        241368652        312
          8       3612734        3514        127878976089        978792750       1559
          9       9587085        5648        558403872034       3432486128       6584
          10     21546920        7540       2117256832910      10687426240      24748

Table 3. Number of inequivalent solutions to the anomaly equations for SMνR fermion content and
different maximum U (1)F charges Qmax . Each row contains the all-zero charge solution, as well as
```

Erratum JHEP 08 (2019) 064, abstract and Table 1, SMνR (extraction lines 32-33 and 59-66):

```
Abstract: We correct a statement in our original paper and add anomaly-free charge
assignments for SMνR with 7 ≤ Qmax ≤ 10.
```

```
                         Qmax        Solutions                      Symmetry            Quadratics                                       Cubics           Time/sec
                                 7   1358388                            2332            24616693253                                  241368652                 312
                                 8   3612734                            3514           127878976089                                  978792750                1559
                                 9   9587085                            5648           558403872034                                  3432486128               6584
                             10      21546920                           7540           2117256832910                             10687426240                  24748

Table 1. Number of inequivalent solutions to the anomaly equations for SMνR fermion content and
different maximum U(1)F charges 7 ≤ Qmax ≤ 10. Each row contains the all-zero charge solution,
```

Largest published Q_max: 10 for the SM (Solutions 23800) and 10 for SMνR (Solutions 21546920). Neither document
tabulates a row with Q_max >= 11.

## Same convention

`calibration_all_40_values.txt` (written in the contributor's workspace on 2026-10-23, after the PDFs arrived)
compares all 40 published numbers (Solutions and Symmetry columns, both contents, Q_max 1..10) with the counters
shipped in `how-we-built-it/source/` (count.c + fix.py + conventions.py): all 40 match. `verify-it-yourself/run_checks.sh`
repeats the comparison for the 20 Solutions values on every run.

## The cells compared in this package

| content | largest published row | this package |
|---|---|---|
| SMνR (SMnuR) | Q_max 10, Solutions 21546920 (Table 3; erratum Table 1) | Q_max 17: 1643386480; Q_max 18: 2720672222 |
