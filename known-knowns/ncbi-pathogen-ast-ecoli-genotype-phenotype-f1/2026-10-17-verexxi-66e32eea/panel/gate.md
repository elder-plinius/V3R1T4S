# Honesty gate, ciprofloxacin (2026-10-17T11:50:07Z)

status: CONFIRMED_SOLUTION
confirmed_scope: On the 10,836 eligible isolates of NCBI Pathogen Detection export PDG000000004.6366 (hash-pinned in CLAIM.md) with the whole-PDS-cluster split in result/split.csv (sha256 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca), a LightGBM predictor over exported AMR-genotype tokens plus collection year, species label and epi_type scores ciprofloxacin resistant-class F1 96.13% (95% cluster-bootstrap interval 93.65% to 97.84%) and accuracy 98.35% (TP 348, FP 12, TN 1317, FN 16) on 1693 isolate comparisons in 1246 held-out clusters, against 80.36% F1 and 89.72% accuracy (TP 356, FP 166, TN 1163, FN 8) for the reimplemented published genotype-field rule on the same rows (paired F1 difference 95% interval 11.09 to 21.88 points) and 77.2% F1 and 89.9% accuracy published in Table 3 of PMC13513162, as a single-split database-concordance result for ciprofloxacin only with no clinical or treatment meaning.

Path note (added 2026-10-19 at the maintainer's request): the confirmed_scope sentence above uses the claim-folder paths the panel reviewed. In this package, CLAIM.md is README.md and verify-it-yourself/expected.json; result/split.csv and result/scores_ciprofloxacin.json are in how-we-built-it/.

Panel results (three Sonnet subagents on the owner's PC, fresh context each, each given only its own copy of claim/):
- reproduce: pass: true
- novelty: pass: true; novelty: confirmed against the live Table 3 (ciprofloxacin F1 77.2%, accuracy 89.9%, read 2026-10-17T01:25:24Z): no published or claimed predictor evaluated on the NCBI Pathogen Detection E. coli/Shigella AST benchmark ties or beats the claimed 96.13% F1, and the only same-target claim in the repo (open draft PR 308) is for amoxicillin-clavulanic acid, not ciprofloxacin; this is a benchmark-relative record
- criterion: pass: true

Status re-check at the gate: the NOVELTY panelist's Table 3 read was more than 6 hours old, so the main session fetched
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML once more (HTTP 200, sha256 e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685): the ciprofloxacin
row still reads F1 77.2% and accuracy 89.9%, unchanged. No other claim on this target for ciprofloxacin in the repository's pull requests (checked
the full pull-request list the same morning; the only other claim on the target is pull request 308, amoxicillin-clavulanic acid).

Gate review (main session): read all three panel files. Downgrade triggers checked (hedging panelist, reproduction mismatch,
value not strictly better than the published one, stretched criterion, scope wider than reproduced, sample presented as
complete, capped search used as an exclusion, several objects in one claim): none found. Disclosed limits, recorded in the
panel files and not hidden: isolates without a PDS accession are treated as singleton clusters (stated in the criterion);
the REPRODUCE panelist saw only Windows CRLF byte differences in rerun outputs, with identical content and pinned sha256
after LF conversion; the NOVELTY literature search covers Europe PMC and arXiv for the last 24 months.
