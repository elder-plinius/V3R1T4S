# How we found it (contributor text, unverified)

Run 1 on this target had no Java, so it audited a re-implemented Phenomizer-style ranker instead of a reference
tool. It found that scoring each published case with the HPO annotation release that predates its paper removes most
of the apparent accuracy. That was groundwork, not p3: we had decided before the results that the baseline is not
the bank's reference tool. The human then installed Java and LIRICAL 2.4.1, and this run repeated the bank's own p3
example with the reference tool.

LIRICAL has a hidden batch command (`benchmark --phenotype-only`). It ran about 8x faster per case than the
documented single-case command and gave the same rankings on a development case. Even so, all 4,247 eligible cases
under two conditions did not fit the time, so a 500-case seeded sample was fixed from the measured timing before any
audit output existed.

Three tool and data problems came up, each fixed in a timestamped pre-registration addendum before any score of the
affected cases:
- the current HGNC file breaks LIRICAL 2.4.1 (a column was removed upstream); the 2026-06-05 archive was used;
- 2022-era phenotype.hpoa files cite HPO ids that are obsolete in the v2026-06-06 ontology, which aborts every case;
  the ids were mapped onto the current ontology, which also keeps the ontology fixed between conditions;
- two releases contain four frequency cells n/m with n > m, which LIRICAL refuses to load; those cells were blanked.

What worked: paired scoring of the same cases, a gene-level expected rank over all protein-coding genes, an
independent naive re-check of every output file, and bootstraps over cases and over publications.
What the design does not isolate: the pre-publication release lacks ALL later curation, not only the case's own
paper. For 299 of the 500 cases the disease had no annotation at all before the paper.
