# The record we beat: the Allanach-Davighi-Melville anomaly-free atlas

source: B. C. Allanach, J. Davighi, S. Melville, "An anomaly-free atlas: charting the space of flavour-dependent
gauged U(1) extensions of the Standard Model", JHEP 02 (2019) 082, arXiv:1812.04602 (version v5), and its erratum
JHEP 08 (2019) 064.
url: https://arxiv.org/abs/1812.04602v5
url (erratum): https://doi.org/10.1007/JHEP08(2019)064
url (data record named in both): http://doi.org/10.5281/zenodo.3345889

## Live fetches (earlier runs of this target and run 2026-11-11-0917)

| URL | fetched (UTC) | HTTP | sha256 of the response body | what it shows |
|---|---|---|---|---|
| https://export.arxiv.org/abs/1812.04602 | 2026-11-03T09:19:21Z (claim run scout) | 200 | 3cce96fa1ab6826f9e8f0879fda2f474d2ca7d075e8466e8016be33863f23b93 | versions v1..v5, no v6 |
| https://export.arxiv.org/abs/1812.04602 | 2026-11-04T09:19:34Z (panel run scout) | 200 | 3cce96fa1ab6826f9e8f0879fda2f474d2ca7d075e8466e8016be33863f23b93 (byte-identical) | same |
| https://arxiv.org/abs/1812.04602 | 2026-11-04T09:21:08Z (NOVELTY skeptic) | 200 | 3cce96fa1ab6826f9e8f0879fda2f474d2ca7d075e8466e8016be33863f23b93 (byte-identical) | same |
| https://zenodo.org/api/records/3345889 | 2026-11-04T09:21:29Z (NOVELTY skeptic) | 200 | 32001b2a5fa4d3e62336a3a1cfd8db4a72c1753d644a68c31809e740453aee1e | version 1.1.0, the last; files SMcharges0..10 and SMnuRcharges0..10 |
| https://arxiv.org/abs/1812.04602 | 2026-11-08T09:19:36Z (run 2026-11-08-0917 scout) | 200 | 3cce96fa1ab6826f9e8f0879fda2f474d2ca7d075e8466e8016be33863f23b93 (byte-identical) | same: v5 is the latest version |
| https://arxiv.org/abs/1812.04602 | 2026-11-11T09:19:08Z (run 2026-11-11-0917 scout) | 200 | e0d5ff800478a38c38113f8b7e251180ad36d8daf14379cdd7c0f401420490e0 | still v1..v5; differs from earlier fetches only in arXiv's page template |

selected headers: not recorded by the run (only URL, time, status and body hash were logged). The fetched pages are
not copied into this package. Details and the other searches: `panel/novelty.md`.

## The table itself (owner-supplied PDFs)

The tables were read from the paper and the erratum as PDF files supplied by the workspace owner on 2026-10-23
(the container could not reach arXiv PDFs or link.springer.com then), saved unchanged at 2026-10-23T19:38:19Z (file
time, UTC), and from their text extractions (`pdftotext -layout`). The PDFs and the extractions are not copied into
this package.

http_status: none for the PDFs (owner-supplied files, not an HTTP fetch)
fetched_utc: 2026-10-23T19:38:19Z (time the owner-supplied copies were saved)

| file (owner-supplied copy) | bytes | sha256 |
|---|---|---|
| arXiv-1812.04602v5.pdf | 598427 | 022355da109e4eef72fb0cb314bea3c282fe49136f2aeae133c1ca262c275b96 |
| JHEP08-2019-064-erratum.pdf | 147987 | c6fcae4107a1e7306b58d4b0821c8b2f699e5ad06b21629e897af56b341dfcb4 |
| arXiv-1812.04602v5.txt (pdftotext extraction) | 97752 | 6d5d2d827e5c9ec32f91afac05a1d9a84dd13c670892832ce8a5e0e7fcf8d56d |
| JHEP08-2019-064-erratum.txt (pdftotext extraction) | 9008 | 85a0c55771277b2501888513a20d023fe3d1370c76c86b5bff810c6460cfedc9 |

Caveat: the PDF hashes show that the files are the ones the owner supplied; they were not compared byte for byte
with the arXiv or Springer copies. The extraction's header line reads `arXiv:1812.04602v5 [hep-ph] 8 Jan 2020`; the
erratum's reads `JHEP08(2019)064` (Published: August 12, 2019). Anyone can check the quoted lines against
https://arxiv.org/abs/1812.04602v5 and the erratum.

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
tabulates a row with Q_max >= 11, and the Zenodo data record (version 1.1.0, the last) holds files up to Q_max 10
for both contents.

## Same convention

`calibration_all_40_values.txt` (the run's `claim/source/atlas/table_comparison.txt`, copied unchanged) compares
all 40 published numbers (Solutions and Symmetry columns, both contents, Q_max 1..10) with this workspace's
counters: all 40 match. `verify-it-yourself/run_checks.sh` repeats the comparison for the 20 Solutions values with
`mitm.c` on every run.

## The cells compared in this package

| content | largest published row | this package |
|---|---|---|
| SM | Q_max 10, Solutions 23800 (Table 2) | Q_max 41: 66526761; 42: 79174540 |

Rows in between (SM 11..40, and SMnuR 11..20) are earlier submissions of the same census from this workspace
(`2026-10-23-adb991-99e267ca`, `2026-10-23-adb991-81997531`, `2026-10-23-adb991-0728c1c8`, `2026-10-28-adb991-f28c78af`,
`2026-11-04-adb991-12f0deb4`, `2026-11-08-adb991-4a46c68e`).
