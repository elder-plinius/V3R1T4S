# CRITERION skeptic: run 2026-11-11-1855, partial win p1

context: subagent (Claude Code Agent tool, fresh context)
started: 2026-11-11T19:06:34Z (date -u); written about 19:20Z
read: only the claim package (claim.md, prereg/PREREG.md, prereg/prereg_freeze.sha256, results/, results/sensitivity/,
baseline/README.md, null_test.md, REPRODUCE.md, code/*.py, inputs/, method_output/, lirical_output/, lirical_data/,
scout/). No other run, report or panel file was read. Nothing was fetched from the web. No outward action.
My scratch code and outputs are in ../panel/work_criterion/ (relative to claim/): crit_check.py, lir_check.py,
cluster_null.py, incl_check.py, clean_check.py and their .out files.

## Verdict in one line
p1 is met, literally, under readings I judge fair (not stretched). The win is narrow: it disappears if excluded terms
are counted, it does not hold at exactly 1 term, and it rests on a few large cohort publications. The scope below says
so.

## p1 read literally, clause by clause
p1 (verbatim, as quoted in claim.md and prereg/PREREG.md): "Beat the reference tool's MRR by >= 10% relative on the
subset of cases with <= 3 HPO terms (the information-poor regime where phenotype matching is weakest), with bootstrap
intervals and identical candidate space."

1. "the reference tool": the full criterion defines it as "a publicly available reference tool (Exomiser or LIRICAL,
   pinned version and pinned data release ...)". LIRICAL 2.4.1 is one of the two named tools. Run phenotype-only on
   unmodified phenopackets: the only sensible mode (the phenopackets list only the causal variants, so any genotype
   input would leak the answer). OK.
   - Data release: LIRICAL got the cleaned HPOA, not the stock file. I judge this fair (as the prereg's reading (a)):
     the full criterion bars the method from any resource derived from the case reports. Giving only the reference
     tool annotations taken from those reports would compare leakage, not methods. The cleaning is deterministic,
     pinned by sha256, and both tools use the same file. Checked:
     - My own re-implementation of the stated rule (../panel/work_criterion/clean_check.py: every PMID string in every
       JSON of inputs/all_phenopackets_0.1.27.zip, drop-if-any) gives 1,736 corpus PMIDs and 25,965 dropped rows. Its
       output is byte-identical to lirical_data/phenotype.hpoa (sha256 5e1a2fcf...aa14). method_output/run_info.json
       records the same hpoa sha256 for the method.
     - Evidence that LIRICAL really ran on the cleaned file: the OMIM diseases in LIRICAL's raw output (8,195) are
       exactly the OMIM diseases with any row in the cleaned HPOA (8,195), not those of the original (8,642).
   - HPO v2026-06-06 resources predate the corpus release (0.1.27 published 2026-06-09T16:47:04Z,
     scout/phenopacket-store_releases_api.json).
   - LIRICAL's version (2.4.1) and the run itself cannot be re-executed within this panel's limits (no jar; about
     1.1 GB per JVM). That belongs to REPRODUCE. Run 3's 6-chunk byte-identical re-run is declared, not seen by me.
2. "MRR": gene-level MRR, with RR = E[1/rank] under uniform random tie-breaking, computed the same way for both tools.
   LIRICAL's disease-level output is mapped to genes by the max post-test probability over linked OMIM diseases (the
   standard construction). The L2 sensitivity, which maps LIRICAL with the method's own gene map, changes nothing
   (MRR_L 0.1048, ratio 1.3207).
3. "by >= 10% relative": the ratio is 1.3218 (0.13844 / 0.10474) against a threshold of 1.10. The paired
   case-bootstrap 95% interval of the ratio, [1.2394, 1.4201], is entirely above 1.10. So the claim also passes the
   stricter reading "the 10% margin itself lies outside the interval", not only the adopted G2 reading (difference
   interval > 0).
4. "with bootstrap intervals": these are provided. The bank's own full criterion names the resampling unit:
   "95% bootstrap interval over cases". The paired case bootstrap is therefore the bank's reading, not a softened one.
   The publication-cluster intervals are reported, not gated (declared before computing): difference
   [0.0021, 0.0659], above 0; ratio [1.0236, 1.6718], which does NOT exclude ratios below 1.10.
5. "identical candidate space": both tools rank the same 19,274 HGNC approved protein-coding genes, with unlinked
   genes scored 0.
   - My own candidate loader gets 19,274 unique ids.
   - The method's rank denominator reaches 19,274 in the subset.
   - I re-scored LIRICAL from the raw outputs with my own code (../panel/work_criterion/lir_check.py), on 10 randomly
     chosen chunks covering 270 subset cases. It reproduces rr_L exactly (max abs diff 4e-11, 0 mismatches).
   - rr_M, recomputed from n_greater/n_ties in method_output/percase.tsv, matches for all 2,038 subset cases.
6. "the subset of cases with <= 3 HPO terms": the prereg reading counts DISTINCT OBSERVED terms (excluded ones not
   counted), after hp.obo v2026-06-06 mapping, kept under HP:0000118.
   - I re-derived n_terms directly from the phenopacket JSONs in the pinned zip with my own obo parser: 0 mismatches
     over 10,189 cases, and a subset of exactly 2,038.
   - S1 (raw observed ids <= 3) gives the identical 2,038 cases, so mapping, filtering and de-duplication do not
     move the subset.
   - I judge the observed-terms reading fair: "number of HPO terms" in phenotype-driven prioritization conventionally
     means the patient's positive findings, and the bank's own gloss ("where phenotype matching is weakest") points
     at the positive profile that matching uses. It also does not handicap the reference tool: LIRICAL receives the
     excluded terms too, and only the method ignores them. 1,684 of the 2,038 subset cases carry excluded terms
     (median 5).
   - It is not the only reading, though. Under S2 (observed + excluded <= 3; 493 cases) the method does not win:
     MRR 0.0345 vs 0.0352, ratio 0.98, paired case CI of the ratio [0.87, 1.11]. The claim states "observed"
     explicitly, so the scope must too.
7. Universe and exclusions: re-derived from inputs/cases.tsv with the stated rule (../panel/work_criterion/
   incl_check.py), the included set reproduces inputs/included_cases.txt exactly: 10,377 phenopackets, minus 69 with
   no single causal gene, 116 with a gene outside the candidate space, and 3 with no mappable observed term. The
   rule is pre-stated, applied to both tools, and of the kind the bank explicitly allows ("e.g. cases without HPO
   terms").
8. Top-1 is not part of p1, and the prereg correctly does not gate on it. The "published evaluation is the bar"
   clause belongs to the full criterion, not to p1. Even if it applied, the package's literature notes find no
   published MRR on this subset.

## Pre-registration
- The rules part reproduces the recorded hash: the first 112 lines of prereg/PREREG.md hash to 25573018...f1ff, and
  the whole file to c934e8ba...0cc6, as in prereg/prereg_freeze.sha256 (frozen 18:59:19Z and 19:00:41Z).
- Re-running code/p1_eval.py on the packaged inputs reproduces results/p1_eval.out, results/p1_summary.json and
  results/p1_subset_cases.tsv byte-identically.
- The prereg honestly declares it was NOT blind to the subset's point MRRs (run 3 had reported them as a stratum).
  The subset reading itself is declared to come from run 1, before LIRICAL ran. I cannot verify that timing from
  inside the package. The inputs/run1_C_percase.tsv n_terms column agrees with it.
- The gate choices (G1 point ratio, G2 case-paired difference CI, G3 null) are the fair, bank-matching readings. The
  stricter case-level ratio-interval reading also passes.

## Null models
- The prereg null (paired label-swap, 400 controls; my exact replica gives best control 0.013722 against real
  0.033707) and my own 2,000-control sign-flip (max 0.0157) agree: the real difference beats every control. As a
  conditional test on these 2,038 cases this is valid.
- A cluster-aware null is weaker (../panel/work_criterion/cluster_null.py, 20,000 controls each):
  - flipping the sign per publication: p about 0.026 (447 clusters);
  - flipping per gene: p about 0.028 (289 clusters);
  - the 10%-margin version (M - 1.10 L) per publication: p about 0.08.

  So the evidence is strong for these cases and moderate for generalization over publications. This bounds the
  scope; it does not break p1, which asks for case-level bootstrap intervals.

## Sensitivity (reported, not gates; checked against results/sensitivity/audit.out and my own runs)
- By term count, the win comes from 2- and 3-term cases (ratios 1.32 and 1.56). At exactly 1 term the method is
  slightly worse (ratio 0.92, CI [0.80, 1.05]).
- Concentration: dropping the 5 publications that contribute most removes the whole difference (ratio 1.00 on the
  remaining 1,721 cases). Leave-one-publication-out keeps the ratio between 1.24 and 1.40. Dropping the largest gene
  (277 cases) keeps the ratio at 1.48, though its publication-cluster difference CI then touches 0. The MRR advantage
  is real for this subset as a whole, but it is carried by a minority of large cohorts. Over most publications the
  two tools are on par: median per-case difference about 3e-5, and 702 cases where both tools score RR < 0.001.
- Excluding run 3's DEV cases: ratio 1.315, CI of the difference above 0. Unaffected.

## Novelty and subsumption boundary
p1 is an enumerated partial win in its own right. It is not implied by the full-corpus result (a full-corpus win does
not imply a win in a subset, and the 1-term stratum goes the other way). Whether a term-count restriction of the
published Resnik-vs-LIRICAL comparison (arXiv 2609.02473, flagged in the prereg) counts as new is the NOVELTY
skeptic's decision, not mine. This verdict is on the criterion only.

## Wording note for the claim
claim.md's sentence is accurate. Any public wording should say "at most 3 observed (non-excluded) HPO terms". It
should not say "information-poor cases" without that qualifier, because counting excluded terms reverses the result.

confirmed_scope: On the 2,038 of the 10,189 included phenopacket-store 0.1.27 cases with at most 3 distinct observed (non-excluded) HPO terms (hp.obo v2026-06-06, under HP:0000118), with both tools using the same HPOA v2026-06-06 cleaned of every row citing a corpus PMID (sha256 5e1a2fcf77d3ddf7d5d00f54ce8975ecabff3277749359f1e0636a8c6a7caa14) and the same 19,274-gene protein-coding candidate space, the frozen asymmetric-Resnik ranker reaches gene-level MRR 0.1384 against 0.1047 for LIRICAL 2.4.1 phenotype-only on the unmodified phenopackets (ratio 1.32, paired case-bootstrap 95% intervals [0.0257, 0.0420] for the difference and [1.239, 1.420] for the ratio, real difference above all 400 paired label-swap controls), a margin that does not survive counting excluded terms (493 cases, ratio 0.98) and whose publication-cluster ratio interval [1.024, 1.672] does not exclude ratios below 1.10.

pass: true
