# A_4^GC(10,7,5) >= 44: a DNA code with constant GC-content beating King's table (34)

## What
The 44 words in object/gc_n10_d7_m44.txt form a length-10 quaternary code with exactly 5 G/C per word, all words distinct, and minimum plain Hamming distance 7, which strictly exceeds the unmarked entry 34^v for A_4^GC(10,7,5) in the GC (non-RC) table of the re-fetched King page [not included in this package; its URL, fetch time and sha256 are recorded in the-record-we-beat/RECORD.md] (re-fetched 2026-10-19T16:38:28Z); post-2010 novelty is not covered.

Note: "post-2010 novelty is not covered" is part of the CRITERION reviewer's scope sentence (quoted verbatim above, as the kit requires) and refers only to that reviewer's remit. The NOVELTY reviewer checked post-2010 sources; they are listed below with dates and what each says about (10,7).

### Post-2010 sources checked (all dates UTC, 2026; from the run's records)
- **Montemanni, Smith and Koul 2014**, LNMS 6, 167-175, Table 1 (A4GC): full text fetched 10-19 16:56:31Z, HTTP 200. Cell (10,7): V (their result) = 34, B (previous best) = 32. Below 44.
- **Aboluion 2011 PhD thesis** (University of Glamorgan), Table 10.69, "Best known lower bounds for max_w(A4^GC(n,d,w))" (plain GC table): read by the NOVELTY reviewer (portal PDF, 10-19 17:01:05Z, HTTP 200), and checked by hand by the contributor on 10-20: (10,7) = 34 (m1). The reviewer also read (10,7) = 12 in Tables 10.65 and 10.27. Below 44.
- **arXiv 1902.04419v3** (conflict-free DNA codes): fetched 10-19 17:05:25Z, HTTP 200. Tables I-II (GC plus reverse, reverse-complement and conflict-free constraints, so their codes are also GC codes) give 16 at (10,7). Below 44.
- **arXiv 1607.00266** (Limbachiya, Rao and Gupta): fetched 10-19 17:00:13Z, HTTP 200, read in full. Only GC+RC and HD+RC tables; GC,RC (10,7) = 17. No plain GC table.
- **arXiv 2108.02033** (reversible G^k-codes): abstract page fetched 10-19 ~15:18Z, HTTP 200. New bounds only at lengths 48-72 and with reversible/RC constraints; no (10,7) value.
- **arXiv 2403.11551** (reversible DNA codes): abstract fetched 10-19 ~15:18Z, HTTP 200, with new bounds at lengths 80, 96 and 160. Full text read 10-19 16:36:23Z for a related cell; it covers long reversible codes. No (10,7) value.
- **arXiv 1903.03535** (GC-content of Galois-supplemented cyclic codes): abstract only, fetched 10-19 ~15:18Z, HTTP 200. Theory; no table values in the abstract.
- **V3R1T4S repository**: TROPHY_CASE.md (10-19 17:00:35Z, HTTP 200) has no DNA-code entry. Among the 260 open PRs (10-19 17:00:35-43Z), none is for the GC table at (10,7); #493 is a 20-word GC,RC code at (10,7), which is below 44.
- **2024-2026 literature**: web searches only (10-19). No paper with a GC (10,7) value was found.

### Post-2010 sources NOT read
- **Smith, Aboluion, Montemanni and Perkins 2011**, Discrete Math. 311: not read. The DOI led to a JavaScript redirect stub (10-19 17:00:34Z). Its constructions are summarised in the Aboluion thesis (best own (10,7) value 12), and King's table includes its 'x' entries.
- **Limbachiya, Gupta and Aggarwal 2018** (altruistic algorithm), "Family of Constrained Codes for Archival DNA Data Storage", IEEE Commun. Lett.: not read; only search-result metadata seen (it adds a no-run-length constraint). Other altruistic-algorithm papers by the same authors were not searched individually.
- **Frontiers in Genetics 2023** (doi 10.3389/fgene.2023.1158337): not read; search snippet only (GC+RC+no-run-length sets).
- Google Scholar and paywalled databases were not searched, so a recent unindexed paper cannot be ruled out.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS` (the line before it: `VALID size=44 table=34 BEATS`). Takes under a second on a laptop.

## Compared to
King's table of lower bounds for DNA codes with constant GC-content, https://rambutan.umassmed.edu/king/dnacodes.html,
first table, cell (n,d) = (10,7): 34 (superscript v), fetched 2026-10-19T17:06:28Z (HTTP 200). Details in the-record-we-beat/RECORD.md.
Also below Montemanni-Smith-Koul 2014 (Table 1: 34) and the Aboluion 2011 thesis (Table 10.69: 34).

## Not claimed
- Not optimal: no upper bound is claimed; the true maximum may be larger than 44.
- Only the plain GC-content table (Hamming distance only), not the GC,RC (reverse-complement) table.
- The search that found it was time-limited (600 s branch and bound over symmetric orbits). Rerunning it may give a different code; the claim is the object, which is checked deterministically.
- No claim about any other cell.

## Credits
- Oliver D. King, the table above, and "Bounds for DNA codes with constant GC-content", Electron. J. Combin. 10 (2003) R33, https://arxiv.org/abs/math/0306197 (the GC-content convention w = n/2 and the Plotkin-type bound used while exploring).
- Philippe Gaborit and Oliver D. King, "Linear constructions for DNA codes", Theoret. Comput. Sci. 334 (2005) 99-113.
- Roberto Montemanni and Derek H. Smith, the variable neighbourhood search value 34 in this cell (J. Math. Model. Algorithms 7 (2008) 311-326; MIC 2009), and Montemanni, Smith and Koul, LNMS 6 (2014) 167-175.
- Yeow Meng Chee and San Ling, "Improved lower bounds for constant GC-content DNA codes", IEEE Trans. Inf. Theory 54 (2008) 391-394.
- Niema Aboluion, PhD thesis (University of Glamorgan, 2011), and D. H. Smith, N. Aboluion, R. Montemanni and S. Perkins, Discrete Math. 311 (2011).
- Credit for this result: zubair_r (GitHub: jamdragon953-del, same person; a V3R1T4S run).
