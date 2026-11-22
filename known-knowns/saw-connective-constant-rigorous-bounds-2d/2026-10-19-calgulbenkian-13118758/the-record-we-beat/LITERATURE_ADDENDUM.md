# Addendum to the literature search (orchestrator, 2026-10-19)

The two documents the first search could not read have now been read.

## Alm, J. Phys. A: Math. Gen. 38 (2005) 2055-2080, "Upper and lower bounds for the connective constants of self-avoiding walks on the Archimedean and Laves lattices"

The author's page https://www2.math.uu.se/~sveralm/boundsabstr.html links a manuscript PDF whose link is dead (404); the PDF was read from the Internet Archive copy of that link (31 pages). Section 5.1.3 and the summary table, verbatim from the text extraction:

```
5.1.3        The (4.82 ) lattice
This semi-regular lattice, also known as the Bathroom tiling or Briarwood lattice,
has two vertex classes when computing lower bounds; see Figure 10 and note that
by vertical symmetry we need only consider vertex classes 1 and 2.
    The matrix G(19, 42), with dimension 125 094, gives the bound µ < 1.829 254,
improving the bound in [1].
    Using irreducible bridges of length N ≤ 49 gives the lower bound µ > 1.785 641.
This was recently substantially improved by Jensen, [9], to µ > 1.804 596.
    Computation of f (n) up to length 47, see Table 2, extends the previous enumer-
ation (n ≤ 29) of [1].
    The estimate µ ≈ 1.809 agrees with the estimate µ ≈ 1.808 830 given in [12].

```

```
      D(3 .4 )              10/3      3.41   2.112 899       2.152            2.186 720
              2
      D(3 .4.3.4)           10/3      3.37   2.092 579       2.132            2.168 320
      D(Bow-tie)            10/3      3.37   2.076 706       2.111            2.145 304
      (63 )                   3        3     1.841 925 [9]   1.847 759 [16]   1.868 832 [3]
            2
      (4.8 )                  3        3     1.804 596 [9]   1.808 830 [12]   1.829 254
      (4.6.12)                3        3     1.763 766       1.787 1          1.809 064
      (3.122 )                3        3     1.708 758 [9]   1.711 041 [12]   1.719 254 [3]

```

So the best published rigorous upper bound is mu(4.8^2) < 1.829254 (Alm 2005); the 1.82926 in Jensen 2004 Table 3 is this value rounded. The claimed 849051343/464433440 = 1.8281442934 is below 1.829254 by 1.1097e-3.

## Parviainen, Connectivity Properties of Archimedean and Laves Lattices, Uppsala Dissertations in Mathematics 34 (2004)

DiVA (diva2:164546) did not connect from here after several attempts; the Internet Archive copy of its full-text PDF (11 pages, the thesis summary) was read. It lists "III. Sven Erick Alm and Robert Parviainen. Bounds for the Connective Constants..." as one of its papers, i.e. the same result; the summary gives no other 4.8^2 upper bound.

## Fetch log (UTC | status | sha256 | file | URL)

```
000 |  | parviainen_thesis.pdf | http://uu.diva-portal.org/smash/get/diva2:164546/FULLTEXT01.pdf
2026-10-19T06:29:57Z | 000 |  | parviainen_thesis.pdf (retry, operator-approved) | https://uu.diva-portal.org/smash/get/diva2:164546/FULLTEXT01.pdf
2026-10-19T06:32:08Z | 200 | 042b7c5e111f9d8669b58dc2d4dc9f32d23948903f1e6d3136348f92ce811143 | alm_boundsabstr.html (operator-supplied URL) | https://www2.math.uu.se/~sveralm/boundsabstr.html
2026-10-19T06:32:21Z | 404 | 5112f74ead145fd4af149e4c7fa9702f713d0036063e91588f9e9abeb80b164e | Alm3.pdf (linked from the operator-supplied page) | http://www2.math.uu.se/research/pub/Alm3.pdf
2026-10-19T06:32:30Z | 404 | 5112f74ead145fd4af149e4c7fa9702f713d0036063e91588f9e9abeb80b164e | try_452eea | https://www2.math.uu.se/research/pub/Alm3.pdf
2026-10-19T06:32:31Z | 200 | e0b90bff2302fe60ef92180bce2ead69aca9abbbfdc8c31a695d4e047e8cd34c | try_f04add | https://www2.math.uu.se/~sveralm/
2026-10-19T06:32:55Z | 200 | cc63c1e57283462031eb0de0971cdca8cab5f27f8f71a471c2bd55299f6b286c | alm_lowandup.html (attempt 1) | https://www2.math.uu.se/~sveralm/lowandup.html
2026-10-19T06:32:56Z | 200 | 3957f1dbbd789cab7a6302f009247210af6c374284804ebeae44926e74480ac6 | alm_averagedegree.html (attempt 1) | https://www2.math.uu.se/~sveralm/averagedegree.html
2026-10-19T06:32:57Z | 200 | a3ddda13eac714eaa6c051dd6a6d57412c1f7b34c79fee86491be6736eb6d7aa | Alm3_wayback.pdf (attempt 1) | https://web.archive.org/web/2010id_/http://www2.math.uu.se/research/pub/Alm3.pdf
2026-10-19T06:33:01Z | 000 |  | parviainen_thesis.pdf (attempt 1) | https://uu.diva-portal.org/smash/get/diva2:164546/FULLTEXT01.pdf
2026-10-19T06:34:21Z | 000 |  | parviainen_thesis.pdf (attempt 2) | https://uu.diva-portal.org/smash/get/diva2:164546/FULLTEXT01.pdf
2026-10-19T06:35:41Z | 000 |  | parviainen_thesis.pdf (attempt 3) | https://uu.diva-portal.org/smash/get/diva2:164546/FULLTEXT01.pdf
2026-10-19T06:37:18Z | 200 | 161459735e1fc657a940bdc1dcea85fb6d3137c475f9b5a15c04d1be5620b5f1 | parviainen_thesis_wb.pdf (attempt 1) | https://web.archive.org/web/2020id_/http://uu.diva-portal.org/smash/get/diva2:164546/FULLTEXT01.pdf
```

Conclusion: with Alm 2005 and the thesis read, no rigorous upper bound below 1.829254 for the 4.8^2 lattice was found in Crossref, OpenAlex cited-by lists for Jensen 2004 and Alm 2005, arXiv, or these two documents. Google Scholar, MathSciNet and zbMATH were not searched.
