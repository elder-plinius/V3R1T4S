# How we found it (contributor text, unverified)

The bank target asks for a zero-shot score on a cancer-gene deep mutational scan that beats every model in ProteinGym's
per-assay table by 0.015 Spearman, without using that protein's labels. The labels are public, so the risk is leakage, not
compute.

1. We froze a split by UniProt id: 13 assays of the 8 bank-named cancer proteins as targets, 17 assays of 16 further
   oncology-related proteins left out entirely, and the remaining 187 assays for fitting.
2. On the 187 fitting assays only, a leave-protein-out comparison of simple ensembles chose equal-weight averaging of the
   top-12 columns, z-scored. Held-out fitting assays beat their own table maximum by >= 0.015 in 16% of cases.
   Family-deduplicated ensembles and Spearman-weighted ensembles did no better.
3. We wrote PREREG.md, then scored all 13 targets once. 4 cleared the bar. PTEN_HUMAN_Matreyek_2021 had the largest margin
   (+0.0498).
4. Checks before the panel: rebuilding with every target label replaced by noise gave bit-identical predictions. Nearby
   settings (K 8-16, rank vs z) kept the win, but dropping the ProSST family cut it to +0.007.

What failed: the method does badly on ERBB2, BRCA2 and RASK abundance (single models such as ProSST K=1024, RITA L and
Progen2 XL are much better there), and it misses the MSH2 partial win (+0.012 vs +0.02 needed).
