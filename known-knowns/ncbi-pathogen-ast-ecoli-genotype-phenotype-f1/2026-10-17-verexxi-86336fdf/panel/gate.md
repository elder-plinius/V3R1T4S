# Honesty gate, ampicillin (2026-10-17T11:54:52Z)

status: CONFIRMED_SOLUTION
confirmed_scope: Recomputed from the saved per-isolate file, on the hash-selected 20 percent test partition of NCBI Pathogen Detection export PDG000000004.6366 (1715 ampicillin R/S rows, one per isolate, in 1257 groups made of 365 whole PDS SNP clusters holding 823 rows plus 892 isolates with no PDS accession each kept as its own group), the saved LightGBM predictor scores F1 98.80% and accuracy 98.78% (TP 867, FP 8, TN 827, FN 13) against 94.40% F1 and 94.52% accuracy (TP 792, FP 6, TN 829, FN 88) for the reimplemented published genotype rule on the same rows and the 93.9% F1 and 94.5% accuracy in Table 3 of the saved status-source copy, with a paired 95% cluster-bootstrap interval of 3.06 to 5.88 F1 points for model minus rule, as a database-concordance result for ampicillin only (no other antibiotic, no other export, no clinical or treatment meaning).

Panel results (three Sonnet subagents on the owner's PC, fresh context each, each given only its own copy of claim/):
- reproduce: pass: true
- novelty: pass: true; novelty: CONFIRMED within the kit's scope - model F1 98.80% / accuracy 98.78% strictly beats the live-read published ampicillin F1 93.9% / accuracy 94.5% (Table 3, read 2026-10-17T01:25:29Z, HTTP 200) and the recomputed rule's 94.40%; no other predictor or claim for ampicillin on this benchmark found in 24 months of literature, TROPHY_CASE.md on main, or all 300 PRs (the only same-target PR, #308, is amoxi
- criterion: pass: true

Status re-check at the gate: the NOVELTY panelist's Table 3 read was more than 6 hours old, so the main session fetched
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML once more (HTTP 200, sha256 e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685): the ampicillin
row still reads F1 93.9% and accuracy 94.5%, unchanged. No other claim on this target for ampicillin in the repository's pull requests (checked
the full pull-request list the same morning; the only other claim on the target is pull request 308, amoxicillin-clavulanic acid).

Margin note: F1 98.80% is 4.90 points above the published 93.9% and 4.40 above the recomputed rule's 94.40%; the REPRODUCE panelist reports the paired-difference 95% interval's lower end at 3.06 points (criterion floor 3), so the margin holds but is not wide.

Gate review (main session): read all three panel files. Downgrade triggers checked (hedging panelist, reproduction mismatch,
value not strictly better than the published one, stretched criterion, scope wider than reproduced, sample presented as
complete, capped search used as an exclusion, several objects in one claim): none found. Disclosed limits, recorded in the
panel files and not hidden: isolates without a PDS accession are treated as singleton clusters (stated in the criterion);
the REPRODUCE panelist saw only Windows CRLF byte differences in rerun outputs, with identical content and pinned sha256
after LF conversion; the NOVELTY literature search covers Europe PMC and arXiv for the last 24 months.
