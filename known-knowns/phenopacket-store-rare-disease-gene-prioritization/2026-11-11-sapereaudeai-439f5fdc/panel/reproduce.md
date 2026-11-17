# REPRODUCE skeptic verdict: partial win p1 (phenopacket-store 0.1.27, <= 3 HPO terms, frozen Resnik ranker vs LIRICAL 2.4.1)

context: subagent (Claude Code Agent tool, fresh context)

Read: claim.md, REPRODUCE.md, prereg/PREREG.md, null_test.md and the data files of the package. Author code was read
only after my own checkers existed and had been run (to explain two differences, see "Findings").
All paths below are relative to claim/; my own scripts and outputs sit in ../panel/work_reproduce/.
Machine: Python 3.11 (-I), numpy/pandas only, one process at a time, well under 400 MB. No JVM, no network.
Housekeeping: running the author's scripts wrote a code/__pycache__/ folder (2 .pyc files) into the package; I deleted
it afterwards. No packaged file was changed, and SHA256SUMS still verifies 346/346.

## My definition-based checker (quoted)

Definitions taken from REPRODUCE.md / prereg/PREREG.md, quoted in the script headers:
- n_terms: "the number of DISTINCT HPO terms obtained from the case's OBSERVED phenotypicFeatures (those without
  `excluded: true`), after mapping each id with hp.obo v2026-06-06 (alt_id -> primary id; obsolete with replaced_by ->
  replacement; otherwise dropped), keeping only terms under HP:0000118 ... and de-duplicating after mapping"; p1 = n_terms <= 3.
- RR: "(1/(n_ties+1)) * sum_{k=1..n_ties+1} 1/(n_greater+k); top1 = 1/(n_ties+1) if n_greater = 0, else 0."
- LIRICAL gene score: "max post_test_proba over OMIM diseases linked to the gene by lirical_data/mim2gene_medgen
  ('phenotype' rows), NCBIGene mapped to HGNC with lirical_data/hgnc_complete_set.txt; ... unlinked genes score 0".
- G2: "95% percentile PAIRED case-bootstrap interval of D ... 2,000 resamples ... numpy default_rng seed 20261111,
  rng.integers(0, n, n) per resample"; null N-SF: "sign -1 when r.random() < 0.5, using r = random.Random(20261111 + k)
  drawn in the subset's case order".

Core of my code (../panel/work_reproduce/my_check.py, my_lirical.py, my_resnik.py):

```python
# obo: [Term] stanzas; id, alt_id, is_a (first token), is_obsolete, replaced_by
def mapid(x, depth=0):
    if x in terms:
        d = terms[x]
        if not d['obs']: return x
        return mapid(d['rep'], depth + 1) if d['rep'] else None
    if x in alt2p: return mapid(alt2p[x], depth + 1)
    return None
under = descendants of HP:0000118 via is_a over non-obsolete terms (inclusive)
n_terms(case) = len({mapid(x) for x in observed_ids if mapid(x) in under})

H = cumulative harmonic numbers
rr(g, t) = (H[g + t + 1] - H[g]) / (t + 1);  top1 = 1/(t+1) if g == 0 else 0

# LIRICAL, per chunk (pandas, OMIM rows only), all 19,274 candidates in a dense row per case
M = zeros((n_cases_in_chunk, NG)); np.maximum.at(M, (case_code, gene_idx_of_linked_disease), post_test_proba)
s = M[c, causal]; g = (M[c] > s).sum(); t = (M[c] == s).sum() - 1      # exact float equality for ties

# statistics on the subset, in h2h_percase.tsv order
rng = np.random.default_rng(20261111)
for _ in range(2000): idx = rng.integers(0, n, n); bd.append(rm[idx].mean() - rl[idx].mean())
ci = np.percentile(bd, [2.5, 97.5])
for k in range(400):
    r = random.Random(20261111 + k); ctrl_k = mean(-d if r.random() < 0.5 else d for d in rm - rl)

# method from scratch (my_resnik.py): IC(t) = -ln(#diseases whose propagated annotation closure contains t / N),
# HPOA rows aspect P, no NOT; score(case, disease) = mean over case terms q of max IC over (anc(q) & closure(disease));
# gene score = max over OMIM diseases linked by genes_to_disease (MENDELIAN); rank with scores rounded to 1e-9.
```

## What I verified, my numbers next to the claimed ones

| Item | Mine | Claimed | Result |
|---|---|---|---|
| SHA256SUMS (346 files) | 346 OK | - | match |
| zip sha256 vs saved release API digest of 0.1.27 all_phenopackets.zip | d0c70005...205a | d0c70005...205a | match |
| inputs/cases.tsv vs raw phenopackets in the zip (10,377 files) | observed ids, excluded ids, causal genes: 0 differences | - | match |
| Inclusion rule re-derived (1 causal gene, >= 1 mappable observed term, gene in space) | 10,189, set-equal to inputs/included_cases.txt | 10,189 | match |
| n_terms for all 10,189 included cases (my obo parser) | 0 differences vs results/h2h_percase.tsv | - | match |
| p1 subset size (n_terms 1/2/3) | 2,038 (520/691/827), set-equal to results/p1_subset_cases.tsv | 2,038 (520/691/827) | match |
| "under HP:0000118" inclusive vs strict | same subset either way | - | robust |
| Method RR from method_output/percase.tsv counts, all 10,189 | 0 mismatches vs rr_M/top1_M, max abs diff 5.0e-11 | - | match |
| Method ranks from scratch (my Resnik), ALL 2,038 subset cases, full 19,274-gene re-rank | 2,038 / 2,038 equal gene_score, n_greater, n_ties (with the frozen code's obo convention, see Findings); 2,035 / 2,038 with a full-graph obo parse | - | match (note) |
| LIRICAL RR from the raw lirical_output/cNNN.csv.gz, ALL 10,189 included cases (102 chunks, every case present in its listed chunk, none missing or extra) | 0 mismatches in ngt_L, ties_L, rr_L, top1_L; max abs diff 4.9e-11 | - | match |
| MRR method (subset) | 0.138444296139 (my rows) / 0.138444296139 (h2h rows) | 0.1384 (0.13844429613937836) | match |
| MRR LIRICAL (subset) | 0.104737234286 / 0.104737234286 | 0.1047 (0.10473723428575904) | match |
| Ratio | 1.32182501365 | 1.3218 | match |
| D = difference | 0.0337070619 | 0.033707 | match |
| Paired case-bootstrap 95% of D (seed 20261111, 2,000) | [0.025726, 0.042014] | [0.0257, 0.0420] | match |
| Same, other seeds 1/2/3 (robustness) | [0.0255, 0.0419] / [0.0251, 0.0419] / [0.0254, 0.0422] | - | lower end far above 0 |
| Paired case-bootstrap 95% of ratio (reported, not a gate) | [1.2394, 1.4201] | [1.2394, 1.4201] | match |
| Null N-SF, 400 controls | best control 0.0137223, controls >= real: 0 | best 0.013722, 0 | match |
| Sign-flip null, analytic z of D | 7.73 | - | consistent |
| top-1 method / LIRICAL (not a gate) | 0.086285 / 0.047600 | 0.0863 / 0.0476 | match |
| Cleaned HPOA = original minus every row citing a corpus PMID (own code, PMIDs from cases.tsv) | exact line-sequence equality; 0 rows left citing a corpus PMID; 25,965 rows dropped | sha 5e1a2fcf...aa14 | match |
| LIRICAL used the cleaned HPOA (chunks c000, c037, c101; 289 cases) | each case scored exactly the cleaned file's 8,242 OMIM+DECIPHER diseases; none of the 447 diseases removed by cleaning appears | - | consistent |
| LIRICAL chunk logs | 102 / 102 rc=0 | - | consistent |
| Author's code/p1_eval.py re-run (REPRODUCE step 1) | stdout identical to results/p1_eval.out; p1_summary.json and p1_subset_cases.tsv byte-identical | - | deterministic |
| prereg/PREREG.md hashes | file = c934e8ba...0cc6; rules part (before the novelty section) = 25573018...f1ff, both as recorded in prereg/prereg_freeze.sha256 | - | match |

Author's code/h2h_score.py re-run on all 102 raw LIRICAL chunks and method_output/percase.tsv (REPRODUCE step 3,
about 6 minutes): h2h_percase.tsv byte-identical to results/h2h_percase.tsv (sha256 4d0f3008...80a9) and
h2h_summary.json identical to results/h2h_summary.json. My own checker, run twice, gave identical output.

## Findings (none changes a claimed number)

1. Candidate space documentation. REPRODUCE.md says "candidate genes = inputs/hgnc_protein-coding_gene.txt (19,274
   approved protein-coding genes ...)", but that file holds 19,276 approved protein-coding rows. The 19,274 comes from
   an extra rule in code/rdlib.load_hgnc that drops genes approved after 2026-06-09 (the corpus release date): RNF229
   (2026-09-18) and TLN2-AS2 (2026-10-09). My first LIRICAL pass with all 19,276 genes gave ties +2 on the 2,949 cases
   whose causal gene scores 0 (472 in the subset; max RR difference 6.2e-9, invisible at 4 decimals). With the date
   cutoff (which the claim's "19,274" and the bank's "resources whose release dates precede the corpus release" both
   imply) every row matches. The rule should be written in REPRODUCE.md.
2. The frozen method's obo parser drops is_a edges that carry axiom qualifiers (`is_a: HP:x {xref="PMID:..."} ! name`;
   46 such lines in hp.obo v2026-06-06), so 33 terms fall outside its HP:0000118 subtree (19,061 vs 19,094 terms).
   A full-graph Resnik differs from the frozen output on 3 of the 2,038 subset cases, all from one publication
   (PMID 10498624): score 2.88278 vs 2.88635 and ties 8 vs 7 on two cases, score only on the third; the n_greater of
   all three is unchanged. Effect on the subset MRR of the method: -4.76e-8 (ratio 1.3218250 -> 1.3218246). Emulating the
   frozen parser reproduces 2,038 / 2,038 exactly. This is a property of the frozen method (its outputs are what was
   evaluated, and they reproduce); it does not touch n_terms (my full-graph n_terms equals the table for all 10,189
   cases) or LIRICAL.
3. PREREG.md mentions 1,736 corpus PMIDs; the pmids column of inputs/cases.tsv gives 1,733. The cleaned HPOA I rebuild
   from those 1,733 is line-for-line identical to lirical_data/phenotype.hpoa, so the difference (if any) removes no row.

## What I could not verify

- LIRICAL 2.4.1 itself was not re-run (no jar in the package, about 1.1 GB per JVM, JVM not allowed here). Its raw
  outputs are taken as given; I checked them for completeness, the rc=0 logs, and that they were produced on the
  cleaned HPOA disease set, and I re-scored every included case from them.
- code/frozen_method.py was not run (about 1 GB). Instead I recomputed, with my own small code, the full 19,274-gene
  ranking of every one of the 2,038 subset cases from hp.obo, the cleaned HPOA and genes_to_disease (see table).
  Cases outside the subset were checked only through the counts-to-RR step.
- The freeze times in prereg/prereg_freeze.sha256 are self-reported; I can confirm the hashes, not the clock.
- The publication-cluster intervals, S1/S2 sensitivity subsets and the L2 variant are reported, not gates; I did not
  re-derive them with my own code (they were re-run only through the author's p1_eval.py and h2h_score.py, which
  reproduced byte-identically).

## Decision

Every claimed p1 number (subset size 2,038; MRR 0.1384 vs 0.1047; ratio 1.3218; paired case-bootstrap 95% interval of
the difference [0.0257, 0.0420]; real difference 0.033707 above all 400 label-swap controls, best 0.013722) is
reproduced exactly by independently written code, from the raw phenopackets (subset), the raw LIRICAL outputs (all
10,189 cases), the method's counts (all 10,189) and a from-scratch Resnik re-ranking of all 2,038 subset cases. The
author's own scripts also reproduce byte-identically (p1_eval.py and the full h2h_score.py). Runs are deterministic. The two findings are documentation / implementation-detail notes with effects below 1e-7 on the
statistics; neither is a mismatch of a claimed object or value.

This is retrospective statistics on published case reports; it is not clinical advice.

pass: true
