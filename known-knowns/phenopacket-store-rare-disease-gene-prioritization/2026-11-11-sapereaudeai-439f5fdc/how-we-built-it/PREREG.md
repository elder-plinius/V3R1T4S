# PREREG (run 2026-11-11-1855): partial win p1, frozen before any p1 statistic of this run is computed

Fourth run on `phenopacket-store-rare-disease-gene-prioritization`. The human asked for the p1 check. Rules part
written 2026-11-11T18:58:20Z (date -u); its sha256 is recorded in work/prereg_freeze.sha256 at the moment of freezing.
The novelty section at the end is appended afterwards, still before any p1 number of this run exists, with its own
time stamp.

## Partial win p1 (verbatim, bank `repo/bank/targets.json`)
> Beat the reference tool's MRR by >= 10% relative on the subset of cases with <= 3 HPO terms (the information-poor regime where phenotype matching is weakest), with bootstrap intervals and identical candidate space.

p1 has no "a published evaluation on the same release is the bar" clause (that clause belongs to the full success
criterion only). Novelty is still judged by the NOVELTY skeptic in the usual way.

## What has already been seen (declared honestly)
- Run 3 (runs/2026-11-11-1222) reported, as a DESCRIPTIVE stratum of its full evaluation, the point values on the
  subset defined below: 2,038 cases, MRR 0.1384 (frozen method) vs 0.1047 (LIRICAL), top-1 0.0863 vs 0.0476
  (attempts/full-eval/report.md of that run). So this prereg is NOT blind to the subset's point MRRs (ratio about
  1.32). It is blind to everything else: no bootstrap interval, cluster interval, null control, ratio interval or
  sensitivity subset has been computed for this subset by anyone.
- The subset definition was NOT chosen after seeing that value: it is run 1's census definition, written in
  runs/2026-11-11-0916/attempts/evaluator-first/code/run_contemporary.py (`p1 = nt <= 3`) before LIRICAL existed on
  this machine. It is carried over unchanged.

## The subset (fixed now)
- Universe: run 3's 10,189 included cases (work/included_cases.txt of run 3, sha256 da029585...6a39), with run 1's
  inclusion rule (exactly one causal gene; >= 1 mappable observed HPO term; gene in the candidate space).
- Term count n_terms (run 1's definition): the number of DISTINCT HPO terms obtained from the case's OBSERVED
  phenotypicFeatures (those without `excluded: true`; excluded terms are not counted), after mapping each id with
  hp.obo v2026-06-06 (alt_id -> primary id; obsolete with replaced_by -> replacement; otherwise dropped), keeping
  only terms under HP:0000118 Phenotypic abnormality, and de-duplicating after mapping.
- p1 subset: included cases with n_terms <= 3 (that is 1, 2 or 3 terms, as every included case has >= 1).
- Source of n_terms: the `n_terms` column of run 3's head-to-head table
  (runs/2026-11-11-1222/attempts/full-eval/output/h2h/h2h_percase.tsv, sha256 4d0f3008...80a9, identical to the
  panelled claim/results/h2h_percase.tsv). Before any p1 statistic, the script checks that this column equals run 1's
  per-case n_terms (runs/2026-11-11-0916/work/C_percase.tsv, sha256 1e36379c...b08b6f) for every case; a mismatch
  stops the computation (escape hatch E2).
- Why this is the most favourable FAIR reading: "HPO terms" of a case most naturally means its recorded phenotypic
  findings; observed terms are the positive evidence both tools score; mapping and de-duplication count what a tool
  can actually use. It was fixed in run 1 and is carried over, not chosen now.
- Sensitivity subsets (reported, NOT gates; computed with the same statistics):
  - S1: raw count of observed HPO ids in the phenopacket (before mapping and de-duplication) <= 3, from run 1's
    cases.tsv (sha256 afd59db4...24c1), within the included cases.
  - S2: observed plus excluded terms (all phenotypicFeatures, raw ids) <= 3, within the included cases.

## Readings carried over from run 3 (unchanged)
- Reading (a): both tools use the SAME cleaned HPOA (v2026-06-06 minus every row citing any of the 1,736 corpus
  PMIDs, drop-if-any; sha256 5e1a2fcf...aa14). Run 3's CRITERION skeptic judged it fair.
- Reading (d): LIRICAL 2.4.1, phenotype-only `benchmark --phenotype-only`, unmodified phenopackets, defaults except
  --parallelism 4; gene score = max post-test probability over the OMIM diseases linked to the gene by the data
  directory's mim2gene_medgen. Sensitivity L2 (LIRICAL mapped with the method's gene map) is reported, not a gate.
- The frozen method: run 1's asymmetric Resnik ranker (rdlib.py a75ddd48...efdbb) with driver frozen_method.py
  (3d3624b3...97bb), IC from the cleaned HPOA. Unchanged; no tuning; nothing is re-run.
- Candidate space for both tools: the same 19,274 HGNC approved protein-coding genes; rank of the causal gene by
  expected rank under uniform random tie-breaking; RR = E[1/rank]; MRR = mean RR over the subset.
- Per-case values are REUSED UNCHANGED from run 3's panelled full evaluation (h2h_percase.tsv above: columns rr_M,
  rr_L, top1_M, top1_L, rr_L2). No new LIRICAL run and no new method run is planned.
- Reading (b) of run 3 (which published values can be the bar) is not needed: p1 has no bar clause.

## Metric and gate (fixed now; commit only to what p1 requires)
Statistic: R = MRR_method / MRR_LIRICAL on the p1 subset; D = MRR_method - MRR_LIRICAL (paired, same cases).
The fair reading of "beat ... by >= 10% relative ... with bootstrap intervals", chosen now:
- G1: R >= 1.10 as point estimates.
- G2: the 95% percentile PAIRED case-bootstrap interval of D lies strictly above 0 (2,000 resamples of cases, numpy
  default_rng seed 20261111, `rng.integers(0, n, n)` per resample, both tools on the same resampled cases; the
  same resampler as run 3's h2h_score.py, applied to the subset's n cases).
- G3 (kit requirement for a statistical claim, not a p1 addition): the null test below; the real D must beat all
  400 controls.
p1 holds iff G1, G2 and G3 all hold. Top-1 is NOT a gate (p1 names MRR only).
Reported, NOT gates:
- the paired case-bootstrap 95% interval of R (same resamples), and whether its lower end is >= 1.10 (the stricter
  reading of "with bootstrap intervals"; not adopted, because the bank's full criterion itself only asks the beat to be
  "outside a 95% bootstrap interval", i.e. the difference interval excludes 0, which is reading (c) of run 3, judged
  fair by its CRITERION skeptic);
- publication-cluster bootstrap 95% intervals (2,000 resamples of source PMIDs, numpy default_rng seed 20261112,
  exactly as run 3's h2h_score.py does) of D and of R;
- top-1 and top-10 for both tools, with the paired case interval of the top-1 difference;
- L2 sensitivity; S1/S2 sensitivity subsets; the complement (> 3 terms) for context.
If the CRITERION skeptic rejects the G2 reading and the stricter ratio reading fails, no claim is made.

## Null design
null_test: required
- N-SF, the paired label-swap (sign-flip) null, 400 controls, as in run 3: control k (k = 0..399) swaps the two tools'
  RR on each subset case independently with probability 1/2 (equivalently flips the sign of RR_M - RR_L: sign -1
  when r.random() < 0.5), using r = random.Random(20261111 + k) drawn in the subset's case order (the order of
  h2h_percase.tsv), and recomputes the mean difference. The real D must exceed every
  control. null_test.md records controls, best_control, real, real_beats_all_controls and the command.

## Escape hatches (declared now)
- E1 (novelty): if the literature check below finds that a Resnik/Phenomizer-type ranker vs LIRICAL comparison on a
  few-terms (<= 3, or a comparable small-profile) subset of phenopacket-store 0.1.27 is already published, p1 is
  reported as not new whatever the numbers: no panel, status at most PROMISING.
- E2 (integrity): if any reused file's sha256 differs from the values above, or the n_terms cross-check fails, the
  p1 computation stops; the per-case rows are rebuilt from run 3's raw outputs with the frozen scorer
  (h2h_score.py 3ac4aa72...a9e) only if time allows, and the report says so.
- E3 (time): the hard stop is 20:54 UTC. If the three-skeptic panel cannot be completed by about 20:15 UTC, the
  status stays PROMISING (single-context, unpanelled) and nothing is packaged.
- E4 (DEV overlap): run 3's 500 DEV cases are inside the corpus and some fall in the subset. They were used only for a
  go/no-go decision, never for tuning, so they stay in (no exclusion).

## Known risk stated now (not a hatch)
arXiv 2609.02473 Table 1 publishes Resnik > LIRICAL 2.4.1 on 0.1.27 under leave-one-publication-out for both tools on
all ranking-eligible test cases. The kit's NOVELTY instruction lists "restriction" among trivial edits of a published
object. A NOVELTY skeptic may therefore judge a p1 win on a term-count subset to be a restriction of that published
comparison. That judgement belongs to the panel; it is recorded here before any p1 number.

## Published baseline (step 3c)
The comparator is the reference tool itself (LIRICAL 2.4.1, pinned data, cleaned HPOA), run in run 3 on the same
cases and candidate space and re-run byte-identically by run 3's REPRODUCE skeptic on 6 chunks it chose. No published
score is compared against. The baseline record is run 3's baseline/README.md; this run's baseline/README.md points to
it.

This is retrospective statistics on published case reports; it is not clinical advice.

## Novelty check before computing (appended 2026-11-11T19:00:41Z; no p1 statistic of this run exists yet)
Rules part above is unchanged (sha256 25573018...f1ff in work/prereg_freeze.sha256). Sources read, and what they say
about a few-terms subset (lens novelty-scan; attempts/novelty-scan/output/scan_lit.out lists every term-count line):
- arXiv 2609.02473v1 (the HTML copy fetched once in run 3, data/lit/, sha256 2cbd5910...). Table 1 (Phenomizer,
  Resnik, LIRICAL 2.4.1; uncorrected and LOPO; 2,227 test cases, disease level, Recall@1) is NOT split by term count.
  Table 2 splits by matched deletion and gold-profile survival, not term count. The only term-count split is Table 8:
  Phenomizer alone (capped vs uncapped diagnostic variant), cases over the native 10-term cap (n=681) vs at or under
  it (n=1,546). No Resnik-vs-LIRICAL number on any small-profile subset. Table 6 gives only the corpus median (15
  terms per case).
- arXiv 2608.14683 (saved copy from run 3's NOVELTY skeptic): stratifies its own IC-overlap retriever by MATCHED-term
  count (flag rate 0% at 1-3 matched terms; strata 10-25 and >= 26). No LIRICAL or Resnik result by term count;
  Exomiser 14.0.0 is reported by prevalence stratum only.
- arXiv 2610.33592 and arXiv 2607.24878 (saved copies): no term-count stratification of LIRICAL or Resnik on 0.1.27.
- Repos named by run 3's NOVELTY file (P2GX/hpoadj, P2GX/esid4hpo-analysis, phenorank READMEs): no such result
  (phenorank reports Resnik on 22 synthetic cases).
- Two web searches (19:00Z, queries in attempts/novelty-scan/NOTES.md). Snippets name: an LLM benchmark on
  phenopacket-store 0.1.14 (5,213 cases) grouping cases by HPO-term count (< 5, 6-10, 11-20) for Exomiser vs LLMs
  (different release, different tool, no Resnik; snippet only, not opened); Phen2Disease, claiming gains in cohorts
  with fewer average terms (older, other corpora; snippet only); phentrieve issue #451 (fetched once via the GitHub
  API: HTTP 301 then HTTP 200 at the moved URL; an evaluation plan, no results).
- bioRxiv 10.64898/2026.08.30.748028 (named by run 3's NOVELTY file from snippets): phenopacket-store v0.1.26, 50-gene
  candidate lists; not the same release or candidate space; not fetched in this run.
Finding: no source read reports Resnik/Phenomizer vs LIRICAL on a <= 3-term (or other small-profile) subset of
phenopacket-store 0.1.27. Escape hatch E1 is NOT triggered. The known risk above stands: Table 1 of 2609.02473 is the
published object a NOVELTY skeptic may say p1 restricts.
