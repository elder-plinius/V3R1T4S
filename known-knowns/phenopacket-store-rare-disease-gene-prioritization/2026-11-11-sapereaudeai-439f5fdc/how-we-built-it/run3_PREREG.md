# PREREG (run 2026-11-11-1222; written before any DEV-case output of either tool exists)

Third run on `phenopacket-store-rare-disease-gene-prioritization`. This run is the DEVELOPMENT and FREEZE step for
the bank's full success criterion. It is not the final evaluation and makes no claim.

Before this file existed, only these were run:
- the HPOA cleaning and resource census;
- a regression check of the frozen driver with the ORIGINAL HPOA on 50 non-DEV cases (identical rank counts to run 1);
- a 5-case smoke test of LIRICAL and the frozen method with the cleaned data on 5 non-DEV cases. This only checked
  that the files load; its numbers are not used for any decision.

No DEV case has been scored by either tool.

## Criterion (verbatim, bank; also in target.md)
> Success means a released ranking method plus saved per-case ranked candidate lists over a FIXED candidate space (all protein-coding genes, or all diseases, stated in advance) for every case in a pinned phenopacket-store release (tag and asset sha256 published), using only ontology/annotation resources whose release dates precede the corpus release and excluding any resource derived from the case reports themselves, such that mean reciprocal rank AND top-1 recall both strictly exceed (direction: max) the values obtained by a publicly available reference tool (Exomiser or LIRICAL, pinned version and pinned data release, run by the claimant AND reproduced by the skeptic on the same corpus and candidate space), by at least 10% relative on MRR and outside a 95% bootstrap interval over cases. If a published evaluation on the same release exists, its best value is the bar instead. Cases must not be filtered after seeing results; any exclusion rule (e.g. cases without HPO terms) must be pre-stated and applied to every method identically.

## Readings fixed now: the most favourable fair reading, chosen before any result

### Reading (a): both tools use the SAME cleaned annotations
The criterion forbids the claimant "any resource derived from the case reports themselves". Read literally, it lets
the reference tool keep those resources.
- Run 2 measured that 86% of LIRICAL's gene-level MRR on this corpus disappears with pre-publication annotations
  (0.5567 -> 0.0798).
- A comparison in which only the claimant is denied the case-derived annotations therefore measures that leakage
  advantage, not ranking skill. No honest method can win it.
- The bank's own first pitfall says an apparent win without such controls "measures curation overlap".

The fair reading is therefore a head-to-head in which BOTH tools use the same cleaned HPOA. LIRICAL stays pinned:
- version 2.4.1;
- unchanged code;
- every other data file unchanged (run 2's pinned files, same sha256).

Only its phenotype.hpoa is replaced by the cleaned derivative of the pinned release v2026-06-06. That derivative is
built by a published, deterministic rule and has a published sha256, so it is itself a "pinned data release" in the
sense of a fixed, hashed input.
- Risk stated now: a skeptic may read "pinned data release" as "an official upstream release only". If the
  CRITERION skeptic rejects reading (a), no full-win claim is made. There is no fallback reading.

### Cleaning rule (fixed; built at 12:25Z; the file depends on no tool output)
- Corpus PMIDs: every `PMID:<digits>` string appearing anywhere in any phenopacket JSON of the pinned 0.1.27
  all_phenopackets.zip (sha256 d0c70005...205a). This covers all 10,377 phenopackets, not only included cases, and
  gives 1,736 PMIDs; 1,733 of them come from metaData.externalReferences.
- An HPOA data row is DROPPED if ANY of its references is a corpus PMID ("drop if any").
  - This is stricter than "drop only if all its references are corpus PMIDs".
  - It was chosen because a row that cites a case report was at least partly derived from it. That is the defensible
    reading of "excluding any resource derived from the case reports".
- All aspects (P, I, C, M, H) and NOT rows are treated alike. Every other line is kept byte-for-byte, in order.
- Result (clean_census.json):
  - 25,965 of 284,703 rows dropped (24,148 of them phenotype rows).
  - 455 diseases (all OMIM) are left with no phenotype annotation.
  - P disease-term pairs: 265,538 -> 241,543.
  - Candidate genes left with no annotated disease: 284 under the method's map, 281 under LIRICAL's map.
  - Output sha256 5e1a2fcf77d3ddf7d5d00f54ce8975ecabff3277749359f1e0636a8c6a7caa14, 31,788,673 bytes.
- Declared limitation (judged by the criterion skeptic later):
  - "Derived from the case reports" is put into practice as citing a corpus PMID.
  - Rows citing only OMIM/ORPHA/DECIPHER entries are kept, and so are the gene-disease maps, although OMIM synopses
    and gene-disease links can summarise the same papers. OMIM's own reference lists are not public data here, so
    this residual cannot be removed by any rule this run can apply.
  - The residual is shared by both tools.

### Reading (b): which published value can be the bar
"If a published evaluation on the same release exists, its best value is the bar instead."
- Reading (b): a published value sets the bar only if it was obtained under the same conditions the criterion
  imposes on the claimant. That means:
  - the same cleaned-resource conditions (no annotations derived from the corpus case reports);
  - the same case set;
  - the same candidate space.
- Why:
  - The criterion forbids the claimant leaky resources, so a published value computed WITH them is a different
    comparison. Using it as the bar would require beating leakage, which reading (a) already rules out as unfair.
  - A value on another case set or candidate space is not "on the same release" in the sense of the same evaluation.
- Known published values on 0.1.27 (from runs 1-2; context only), none of which meets (b):
  - arXiv 2609.02473, LIRICAL 2.4.1:
    - full HPOA (leaky): Recall@1 0.4868;
    - leave-one-publication-out: Recall@1 0.1724.
    - Both are on 2,227 cases. LOPO still keeps annotations from the other corpus papers, so it is leakier than the
      cleaned condition here.
- For information only (not a gate), the final run will also report whether the method's full-corpus numbers exceed
  that published LOPO Recall@1.
- If the CRITERION skeptic rejects reading (b), no full-win claim is made.

### Reading (c): "by at least 10% relative on MRR and outside a 95% bootstrap interval over cases"
Gate, the most favourable fair reading, fixed now. All four must hold:
1. MRR(method) >= 1.10 x MRR(LIRICAL), as point estimates. The 10% margin is on MRR only, as the sentence says
   "on MRR".
2. top-1(method) > top-1(LIRICAL), as point estimates.
3. The 95% percentile paired bootstrap interval over cases of MRR(method) - MRR(LIRICAL) lies strictly above 0.
4. The same holds for top-1.

Bootstrap: 2,000 resamples of cases, seed 20261111, both tools on the same resampled cases. Paired, because both
tools rank the same cases.

Reported but NOT gates: the stricter reading (the lower end of the bootstrap interval of the MRR ratio >= 1.10); the
top-1 ratio; publication-cluster intervals; top-10.

### Reading (d): reference tool and gene level
- The reference tool is LIRICAL 2.4.1, run as in run 2 (confirmed scorer, unchanged):
  - phenotype-only, with LIRICAL's own `benchmark --phenotype-only` batch command;
  - the unmodified phenopacket (observed and excluded terms, as the tool reads them);
  - defaults, except --parallelism 4.
- Primary gene level (LIRICAL's own data): gene score = max post_test_proba over its output's OMIM diseases linked to
  the gene by the data directory's mim2gene_medgen.
- Sensitivity, not a gate: the same LIRICAL output mapped with the method's gene map (L2).
- Candidate space for both: run 1's 19,274 HGNC approved protein-coding genes. Expected rank under uniform random
  tie-breaking for both.

## The frozen method (no tuning on any evaluation case)
Run 1's published Phenomizer-style asymmetric Resnik ranker:
- rdlib.py, byte-identical to runs/2026-11-11-0916/attempts/evaluator-first/code/rdlib.py;
- driver frozen_method.py. Every design choice is in its docstring:
  - observed terms only;
  - IC computed FROM THE CLEANED HPOA over all its P-annotated diseases;
  - asymmetric best-match average of Resnik similarity, rounded to 1e-9;
  - gene = max over OMIM diseases linked by HPO genes_to_disease v2026-06-06 (MENDELIAN) with >= 1 cleaned P annotation;
  - expected rank under ties.
- Regression check: with the original HPOA, the driver reproduces run 1's (n_greater, n_ties) on 50/50 non-DEV
  cases (output/regression_vs_run1.out).
- Frozen code sha256 (work/code_freeze.sha256):
  - frozen_method.py 3d3624b3edeb6a7cce21af0b3e60b6287275cd67d2531511970d11e16a6197bb
  - rdlib.py a75ddd4847de66b8349af2e25e353d114d264500b8af26fa22b6efd0ff2efdbb
  - h2h_score.py aa346d0b0ffe7668f62b1b290b01143afb3f115457b1cc1580c11bfad9748f9b
  - score_lirical_run2.py 3455b92cdf663375e86e1c5e06b6ead5284977491ff46bb4037d9c832207734c (run 2's scorer, unchanged)
- Resources of the method, all released before 0.1.27 (2026-06-09):
  - hp.obo v2026-06-06;
  - genes_to_disease.txt v2026-06-06;
  - the cleaned phenotype.hpoa v2026-06-06;
  - the candidate list: run 1's HGNC file filtered to genes approved on or before 2026-06-09. This is a list of gene
    ids, not an annotation resource.

## Cases and exclusions (pre-stated, identical for both tools)
- Included cases: run 1's rule on 0.1.27, giving 10,189 cases. The rule: exactly one causal gene, >= 1 mappable
  observed HPO term, and the gene in the candidate space. List in work/included_cases.txt, sha256 da029585...6a39.
- DEV sample: `sorted(random.Random(202611111222).sample(sorted(included), 500))`, in work/dev500.txt, sha256
  7303e8e8...191f0f. The seed is new; it was not used in runs 1-2.
- The DEV cases are part of the full corpus. Decisions taken on them are go/no-go only, never tuning.

## DEV head-to-head (this run)
- LIRICAL: 5 chunks of 100 DEV cases in a fixed order, one JVM at a time, -Xmx1g, 4 threads, cleaned data directory
  (cache/raredisease-run-2026-11-11-1222/lirical/dd_cleaned).
- Method: frozen_method.py on the same 500 cases with the cleaned HPOA.
- Statistics:
  - MRR, top-1 and top-10 for both tools;
  - paired bootstrap intervals of the differences and of the MRR ratio;
  - publication-cluster intervals (descriptive);
  - the four gate items of reading (c).
- Go/no-go rule (fixed now):
  - **GO**: all four gate items hold on DEV.
  - **MARGINAL**: the method is above LIRICAL on both MRR and top-1 (point), but at least one gate item fails. The
    report states the size of the gap, and the human decides.
  - **NO-GO**: the method's MRR or top-1 point is <= LIRICAL's. The report recommends parking the full win.
- The method is not changed in response to the DEV result. A bug is fixed only if the code contradicts the design
  written above. The fix goes in a timestamped PREREG.v2.md, applies to both tools where relevant, and the report
  names it.

## Null design
null_test: required
- N-SF, paired sign-flip: 400 controls. Control k flips the sign of each case's RR(method) - RR(LIRICAL) with
  probability 1/2 (random.Random(20261111 + k)) and recomputes the mean. The real mean difference must beat all 400
  controls.
- For DEV this is descriptive (go/no-go). The final run repeats it on all cases.

## Escape hatches (declared now)
- E1: LIRICAL rejects a phenopacket, or a case is missing from an output. The case is dropped from BOTH tools,
  counted and listed.
- E2: LIRICAL fails to load the cleaned data on a DEV chunk. The 5-case smoke test loaded it, so this is not expected.
  The chunk is rerun once. If it fails again, the failure is diagnosed and the minimal repair goes in PREREG.v2.md
  before any DEV score is read.
- E3, time cap: no new LIRICAL chunk starts after 13:25:00 UTC. The analysis uses the chunks complete with rc=0, on
  the same cases for both tools, and lists the missing cases.
- E4: a causal gene that is unannotated after cleaning stays in. It scores 0 for whichever tool cannot link it; no
  exclusion.

## Final evaluation (next run; designed and frozen in this run, not started)
All 10,189 included cases. Both tools are run exactly as above, with the scripts and command written in
attempts/final-design/ (FINAL_RUN.md), timed from the DEV throughput. The same gate (reading (c)), the same null and
the same readings apply.

## Published baseline (step 3c)
The comparator is the reference tool itself, run by us on the same cases, candidate space and cleaned data. Run 2's
reproduction of LIRICAL's behaviour (benchmark output equal to the single-case command; an independent gene-rank
re-check) is the baseline record (baseline/README.md). No published score is compared against (reading (b)).
