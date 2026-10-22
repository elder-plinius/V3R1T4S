# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from the claim folder with the system python3 (3.9.6, standard library only) on 2026-10-19 (UTC) on the builder's Mac Studio. Run time about 2 seconds.

```
== part 0: INDEX.csv lists every object file with its sha256
ok    INDEX.csv header
ok    sha256 of all 50 indexed files
ok    INDEX.csv lists exactly the files in object/ (50 files)
ok    every object file is below 1,000,000 bytes
== part 1: open strips + Wynn epsilon (recipe of PREREG_B3.md) at 80 digits
ok    open_strips holds widths 3..29, ln(lambda) with 71 characters each
ok    hprun_open.out agrees with the json values to 50 characters, widths 3..29
      mmax 21: 17 terms, eps_16, mine 6627989728337459151551962343971926608927..., agrees with B3_result.txt on 48 of its 48 decimals
      mmax 22: 18 terms, eps_16, mine 6627989728337459151551962343976923270840..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 23: 19 terms, eps_18, mine 6627989728337459151551962343977254411390..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 24: 20 terms, eps_18, mine 6627989728337459151551962343977255632605..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 25: 21 terms, eps_20, mine 6627989728337459151551962343977255659275..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 26: 22 terms, eps_20, mine 6627989728337459151551962343977255661007..., agrees with B3_result.txt on 48 of its 48 decimals
      mmax 27: 23 terms, eps_22, mine 6627989728337459151551962343977255660932..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 28: 24 terms, eps_22, mine 6627989728337459151551962343977255660932..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 29: 25 terms, eps_24, mine 6627989728337459151551962343977255660932..., agrees with B3_result.txt on 47 of its 48 decimals
ok    my E3(mmax) for mmax = 21..29 reproduce B3_result.txt (terms, eps index, at least 44 of 48 printed decimals)
ok    my four-term window counts equal those in B3_result.txt wherever mmax >= 21
ok    mmax = 26, 27, 28, 29 share exactly 36 decimals (claimed 36; the 37th decimal differs)
ok    VALUE.txt gives 36 decimals: 0.662798972833745915155196234397725566
ok    the 36 decimals of VALUE.txt are the first 36 decimals of E3(26), E3(27), E3(28), E3(29)
== part 2: method A (CTM) ladders and the A versus B3 agreement
ok    ladder rungs chi = 12, 16, 20, 24, 28, 32, 36, 40, 44, 48
ok    pre-registered ladder, last four rungs chi = 16, 20, 24, 28 share 30 decimals (claimed 30)
ok    extended ladder, last four rungs chi = 36, 40, 44, 48 share 43 decimals (claimed 43)
ok    chi = 36, 40, 44, 48 all begin with the 36 decimals of VALUE.txt
ok    A (chi = 48) versus E3(26..29): shared decimals {26: 36, 27: 40, 28: 40, 29: 43}, equal to B3_vs_A.txt {26: 36, 27: 40, 28: 40, 29: 43}
ok    rule D = min(A stable 43, B3 stable 36, A versus B3 43) = 36
      for information, with the pre-registered A rungs: E3(29) shares [30, 33, 37, 39] decimals with the A values chi = 16, 20, 24, 28
== part 3: Kong's bracket
ok    0.662798972833745915155196234397725566 lies inside [0.662798972831, 0.662798972845]
ok    rounded to 12 decimals the value is 0.662798972834 = Kong's printed value
ok    E3(29) at 60 decimals also lies inside the bracket
== part 4: definition check, matchings of n x n grids against A028420
ok    n = 0: explicit enumeration of edge sets gives 1, A028420(0) = 1
ok    n = 1: explicit enumeration of edge sets gives 1, A028420(1) = 1
ok    n = 2: explicit enumeration of edge sets gives 7, A028420(2) = 7
ok    n = 3: explicit enumeration of edge sets gives 131, A028420(3) = 131
ok    n = 4: explicit enumeration of edge sets gives 10012, A028420(4) = 10012
ok    n = 5: explicit enumeration of edge sets gives 2810694, A028420(5) = 2810694
ok    n = 1: cell-by-cell count gives 1, A028420(1) = 1
ok    n = 2: cell-by-cell count gives 7, A028420(2) = 7
ok    n = 3: cell-by-cell count gives 131, A028420(3) = 131
ok    n = 4: cell-by-cell count gives 10012, A028420(4) = 10012
ok    n = 5: cell-by-cell count gives 2810694, A028420(5) = 2810694
ok    n = 6: cell-by-cell count gives 2989126727, A028420(6) = 2989126727
failed checks: 0
PASS
```

## Package run (2026-10-19, from the package folder)

In this package the per-file index of object/ is verify-it-yourself/object_files.csv and the checker reads Kong values from the-record-we-beat/README.md (two path edits to check_md.py; nothing else changed). Real output of sh verify-it-yourself/run_checks.sh from the package folder:

```
== part 0: INDEX.csv lists every object file with its sha256
ok    INDEX.csv header
ok    sha256 of all 50 indexed files
ok    INDEX.csv lists exactly the files in object/ (50 files)
ok    every object file is below 1,000,000 bytes
== part 1: open strips + Wynn epsilon (recipe of PREREG_B3.md) at 80 digits
ok    open_strips holds widths 3..29, ln(lambda) with 71 characters each
ok    hprun_open.out agrees with the json values to 50 characters, widths 3..29
      mmax 21: 17 terms, eps_16, mine 6627989728337459151551962343971926608927..., agrees with B3_result.txt on 48 of its 48 decimals
      mmax 22: 18 terms, eps_16, mine 6627989728337459151551962343976923270840..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 23: 19 terms, eps_18, mine 6627989728337459151551962343977254411390..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 24: 20 terms, eps_18, mine 6627989728337459151551962343977255632605..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 25: 21 terms, eps_20, mine 6627989728337459151551962343977255659275..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 26: 22 terms, eps_20, mine 6627989728337459151551962343977255661007..., agrees with B3_result.txt on 48 of its 48 decimals
      mmax 27: 23 terms, eps_22, mine 6627989728337459151551962343977255660932..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 28: 24 terms, eps_22, mine 6627989728337459151551962343977255660932..., agrees with B3_result.txt on 47 of its 48 decimals
      mmax 29: 25 terms, eps_24, mine 6627989728337459151551962343977255660932..., agrees with B3_result.txt on 47 of its 48 decimals
ok    my E3(mmax) for mmax = 21..29 reproduce B3_result.txt (terms, eps index, at least 44 of 48 printed decimals)
ok    my four-term window counts equal those in B3_result.txt wherever mmax >= 21
ok    mmax = 26, 27, 28, 29 share exactly 36 decimals (claimed 36; the 37th decimal differs)
ok    VALUE.txt gives 36 decimals: 0.662798972833745915155196234397725566
ok    the 36 decimals of VALUE.txt are the first 36 decimals of E3(26), E3(27), E3(28), E3(29)
== part 2: method A (CTM) ladders and the A versus B3 agreement
ok    ladder rungs chi = 12, 16, 20, 24, 28, 32, 36, 40, 44, 48
ok    pre-registered ladder, last four rungs chi = 16, 20, 24, 28 share 30 decimals (claimed 30)
ok    extended ladder, last four rungs chi = 36, 40, 44, 48 share 43 decimals (claimed 43)
ok    chi = 36, 40, 44, 48 all begin with the 36 decimals of VALUE.txt
ok    A (chi = 48) versus E3(26..29): shared decimals {26: 36, 27: 40, 28: 40, 29: 43}, equal to B3_vs_A.txt {26: 36, 27: 40, 28: 40, 29: 43}
ok    rule D = min(A stable 43, B3 stable 36, A versus B3 43) = 36
      for information, with the pre-registered A rungs: E3(29) shares [30, 33, 37, 39] decimals with the A values chi = 16, 20, 24, 28
== part 3: Kong's bracket
ok    0.662798972833745915155196234397725566 lies inside [0.662798972831, 0.662798972845]
ok    rounded to 12 decimals the value is 0.662798972834 = Kong's printed value
ok    E3(29) at 60 decimals also lies inside the bracket
== part 4: definition check, matchings of n x n grids against A028420
ok    n = 0: explicit enumeration of edge sets gives 1, A028420(0) = 1
ok    n = 1: explicit enumeration of edge sets gives 1, A028420(1) = 1
ok    n = 2: explicit enumeration of edge sets gives 7, A028420(2) = 7
ok    n = 3: explicit enumeration of edge sets gives 131, A028420(3) = 131
ok    n = 4: explicit enumeration of edge sets gives 10012, A028420(4) = 10012
ok    n = 5: explicit enumeration of edge sets gives 2810694, A028420(5) = 2810694
ok    n = 1: cell-by-cell count gives 1, A028420(1) = 1
ok    n = 2: cell-by-cell count gives 7, A028420(2) = 7
ok    n = 3: cell-by-cell count gives 131, A028420(3) = 131
ok    n = 4: cell-by-cell count gives 10012, A028420(4) = 10012
ok    n = 5: cell-by-cell count gives 2810694, A028420(5) = 2810694
ok    n = 6: cell-by-cell count gives 2989126727, A028420(6) = 2989126727
failed checks: 0
PASS
```
