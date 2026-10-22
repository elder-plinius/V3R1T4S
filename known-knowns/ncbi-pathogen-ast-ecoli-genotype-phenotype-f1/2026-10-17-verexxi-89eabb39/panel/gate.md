# Honesty gate, ceftriaxone (2026-10-17T12:05:26Z)

status: CONFIRMED_SOLUTION
confirmed_scope: On the hash-defined test partition of NCBI Pathogen Detection export PDG000000004.6366 (1531 ceftriaxone comparisons in 1114 groups, of which 337 are PDS SNP clusters holding 754 rows and 777 are unclustered isolates treated as one-isolate groups), the LightGBM predictions saved in result/test_predictions_ceftriaxone.csv score F1 97.66% (95% cluster-bootstrap CI 96.32% to 98.69%) and accuracy 98.76% with TP 396, FP 10, TN 1116, FN 9, which is 3.06 points above the published 94.6% F1 (published accuracy 97.9%) and 3.15 points above the published genotype rule recomputed on the same rows (F1 94.51%, accuracy 97.19%, paired-difference CI 1.21 to 5.44 points), for ceftriaxone only, as a database-concordance result with no clinical interpretation, and with the margin over the 3-point bar only 0.06 points (one more test error would put it below the bar).

Path note (added 2026-10-19, matching the maintainer's request on pull request 344): the confirmed_scope sentence above uses the claim-folder paths the panel reviewed. In this package, result/test_predictions_ceftriaxone.csv is object/test_predictions_ceftriaxone.csv.

Panel results (three Sonnet subagents on the owner's PC, fresh context each, each given only its own copy of claim/):
- reproduce: pass: true
- novelty: pass: true; novelty: ceftriaxone F1 97.66% (accuracy 98.76%) strictly beats the live-read published 94.6% (accuracy 97.9%) by 3.06 points and the recomputed rule (94.51%) by 3.15 points; no other predictor on this benchmark, no TROPHY_CASE.md row and no ceftriaxone pull request found (only an open draft for amoxicillin-clavulanic acid, #308).
- criterion: pass: true

Status re-check at the gate: the NOVELTY panelist's Table 3 read was more than 6 hours old, so the main session fetched
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML once more (HTTP 200, sha256 e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685): the ceftriaxone
row still reads F1 94.6% and accuracy 97.9%, unchanged. No other claim on this target for ceftriaxone in the repository's pull requests (checked
the full pull-request list the same morning; the only other claim on the target is pull request 308, amoxicillin-clavulanic acid).

Margin note: F1 97.66% is 3.06 points above the published 94.6% (criterion floor 3) and 3.15 above the recomputed rule; the published F1 lies below the model's 95% cluster-bootstrap interval (96.32% to 98.69%), but the paired-difference interval against the recomputed rule (1.21 to 5.44 points) reaches below 3. CRITERION reads the 3-point floor as applying to the point estimate and passes; this is the thinnest margin of the four.

Gate review (main session): read all three panel files. Downgrade triggers checked (hedging panelist, reproduction mismatch,
value not strictly better than the published one, stretched criterion, scope wider than reproduced, sample presented as
complete, capped search used as an exclusion, several objects in one claim): none found. Disclosed limits, recorded in the
panel files and not hidden: isolates without a PDS accession are treated as singleton clusters (stated in the criterion);
the REPRODUCE panelist saw only Windows CRLF byte differences in rerun outputs, with identical content and pinned sha256
after LF conversion; the NOVELTY literature search covers Europe PMC and arXiv for the last 24 months.
