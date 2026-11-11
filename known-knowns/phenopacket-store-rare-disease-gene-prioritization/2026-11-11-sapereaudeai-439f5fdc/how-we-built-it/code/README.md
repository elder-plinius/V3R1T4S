# Code of the p1 run (Python 3.11 with numpy; scan_lit.py and the checker need only the standard library)
- p1_eval.py: the frozen p1 statistics (subset, MRRs, paired case and publication-cluster bootstrap, 400-control
  label-swap null, gate G1-G3). Output: ../logs/p1_eval.out.
- audit.py: independent re-derivation of the subset (own hp.obo parser), declared sensitivity subsets S1/S2, strata and
  concentration checks. Output: ../logs/audit.out, ../logs/audit_summary.json.
- gene_cluster.py: POST HOC (not in the prereg) gene- and publication-cluster bootstrap. Output: ../logs/gene_cluster.out.
- scan_lit.py: the pre-computation literature scan for term-count splits. Output: ../logs/scan_lit.out.
- run3_full_eval/: the frozen method, the cleaning rule, the LIRICAL commands and the head-to-head scorer that
  produced the per-case rows (object/h2h_percase_all_cases.tsv.gz); see its README.md.
