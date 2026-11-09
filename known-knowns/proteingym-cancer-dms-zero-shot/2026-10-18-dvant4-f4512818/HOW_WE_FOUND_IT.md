# How we found it (contributor text, unverified)

Same method and files as the single-assay claim on PTEN_HUMAN_Matreyek_2021 (draft PR #463).
- We froze a split by UniProt id (13 cancer-gene target assays, 17 oncology-related assays left out, 187 fitting assays).
- On the fitting assays only, a leave-protein-out comparison chose an equal-weight mean of the 12 best-ranked columns, z-scored.
- We pre-registered the method and all 13 targets, then scored each target once.
- Four assays on three proteins (PTEN twice, TP53, BRCA1) cleared the +0.015 bar. Nine did not.
- Before the panel: a label-randomised rebuild was bit-identical, and K = 8-16 kept 3-5 wins.
