# Honesty gate, gentamicin (2026-10-17T11:50:07Z)

status: CONFIRMED_SOLUTION
confirmed_scope: On the single pre-fixed hash split of NCBI export PDG000000004.6366 (1623 gentamicin R/S comparisons in 1192 groups, of which 357 are PDS SNP clusters and 835 are isolates with no PDS accession treated as singletons), the saved LightGBM gentamicin predictor scores F1 96.28% and accuracy 98.64% (TP 285, FP 9, TN 1316, FN 13) against 92.41% and 97.17% (TP 280, FP 28, TN 1297, FN 18) for the reimplemented published genotype rule on the identical rows, which is 3.88 F1 points above the published 92.4% and 3.87 above the recomputed rule, with the model F1 above the rule's 95% percentile cluster-bootstrap interval (88.09% to 95.31%) and accuracy above the published 97.6%; this is a database-concordance result for gentamicin on that one partition only, carries no clinical interpretation, and rests on a published-figure re-read and NCBI file hashes that this review could not re-check.

Panel results (three Sonnet subagents on the owner's PC, fresh context each, each given only its own copy of claim/):
- reproduce: pass: true
- novelty: pass: true; novelty: nothing known ties or beats it - live bar is gentamicin F1 92.4% and accuracy 97.6% (Europe PMC Table 3, read 2026-10-17T01:25:30Z, HTTP 200), the claim is F1 96.28% and accuracy 98.64%; TROPHY_CASE.md, the repo pull requests (open and closed), Europe PMC and arXiv show no other gentamicin predictor on this benchmark (the only related pull request, number 308, is amoxicillin-clavulanic acid only)
- criterion: pass: true

Status re-check at the gate: the NOVELTY panelist's Table 3 read was more than 6 hours old, so the main session fetched
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML once more (HTTP 200, sha256 e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685): the gentamicin
row still reads F1 92.4% and accuracy 97.6%, unchanged. No other claim on this target for gentamicin in the repository's pull requests (checked
the full pull-request list the same morning; the only other claim on the target is pull request 308, amoxicillin-clavulanic acid).

Margin note: the F1 margin is 3.88 points over the published 92.4% (the criterion needs at least 3) and 3.87 over the recomputed rule; the model F1 lies above the rule's 95% cluster-bootstrap interval (88.09% to 95.31%), as CRITERION confirms. Thin but inside the pre-registered thresholds.

Gate review (main session): read all three panel files. Downgrade triggers checked (hedging panelist, reproduction mismatch,
value not strictly better than the published one, stretched criterion, scope wider than reproduced, sample presented as
complete, capped search used as an exclusion, several objects in one claim): none found. Disclosed limits, recorded in the
panel files and not hidden: isolates without a PDS accession are treated as singleton clusters (stated in the criterion);
the REPRODUCE panelist saw only Windows CRLF byte differences in rerun outputs, with identical content and pinned sha256
after LF conversion; the NOVELTY literature search covers Europe PMC and arXiv for the last 24 months.
