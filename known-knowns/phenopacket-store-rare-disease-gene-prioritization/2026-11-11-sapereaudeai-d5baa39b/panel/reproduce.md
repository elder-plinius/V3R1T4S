# REPRODUCE skeptic verdict: run 2026-11-11-1032 (p3 leakage audit, LIRICAL 2.4.1)

context: subagent (Claude Code Agent tool, fresh context)
role: REPRODUCE
inputs read: claim.md, REPRODUCE.md, prereg/PREREG.md, PREREG.v2-v4, inputs/, lirical_output/, results/, null_test.md, and (only after my own checker had run) code/.
Scratch work (not part of the claim package): panel/work_reproduce/ (my_checker.py, check_sets_and_rerun.py, compare.py, zipcheck.py, map/, rerun/).

## 1. Own checker, written from the PREREG text before opening code/
Definitions implemented (quoted from prereg/PREREG.md, Statistics):
- "Gene score in one LIRICAL output = max post_test_proba over the output's diseases linked to the gene; a gene with no linked disease scores 0."
- "Disease to gene: ... mim2gene_medgen ..., rows of type "phenotype" with a numeric GeneID; OMIM:<MIM> -> NCBIGene:<GeneID> -> HGNC id via the entrez_id column of hgnc_complete_set 2026-06-05."
- "Rank = expected rank under uniform random tie-breaking among exactly equal scores (parsed doubles). Per case: RR = E[1/rank], top1 = P(rank = 1), top10 = P(rank <= 10)."
- "Intervals: 95% percentile bootstrap, 2000 resamples ...: case-level ... and publication-cluster (resample PMIDs)." (I used my own numpy seeds 777/778.)
- "N-SF ...: 400 controls; control k swaps each case's C and PRE values with probability 1/2 (random.Random(20261111 + k)) and recomputes dMRR."

My checker parsed every row of all 24 files in lirical_output/ (all 500 cases x 2 conditions, no sampling). Output (panel/work_reproduce/out/checker_log.txt):

    seeded sample == sample500.txt (same order): True | same set: True | n unique 500
    n groups 12 n distinct PMIDs 211
    group_order == Random(20261112).shuffle(sorted groups): True
    (all 12 groups: group_<release>.txt == sampled cases whose PRE_percase pre_release is that release: same set=True)
    problems: 0      (case sets per file, duplicate disease rows, ranks 1..n, proba non-increasing by rank)
    n cases scored 500 causal gene not in candidate space: 0
    MRR C=0.556736 PRE=0.079847 dMRR=0.476889 share=0.856580
    top1 C=0.500501 PRE=0.049035 dTop1=0.451466
    top10 C=0.662677 PRE=0.141685
    case bootstrap (B=2000, own seed): dMRR [0.4330, 0.5196] dTop1 [0.4053, 0.4965] share [0.8169, 0.8930]
    publication bootstrap (211 PMIDs, B=2000, own seed): dMRR [0.3410, 0.6209] dTop1 [0.3299, 0.5827] share [0.7611, 0.9424]
    N-SF null: real dMRR=0.476889 best control=0.158284 beats all 400: True (control mean -0.00130 sd 0.03326)

Comparison with the claim sentence:

| quantity | claim | my recomputation |
|---|---|---|
| MRR C / PRE | 0.5567 / 0.0798 | 0.556736 / 0.079847 |
| dMRR, share | 0.4769, 85.7% | 0.476889, 0.856580 |
| dMRR 95% CI cases | [0.4325, 0.5181] | [0.4330, 0.5196] (own seed) |
| dMRR 95% CI publications | [0.3422, 0.6230] | [0.3410, 0.6209] (own seed) |
| top-1 C / PRE, drop | 0.5005 / 0.0490, 0.4515 | 0.500501 / 0.049035, 0.451466 |
| dTop1 CI cases | [0.4050, 0.4965] | [0.4053, 0.4965] |
| dTop1 CI publications | [0.3297, 0.5864] | [0.3299, 0.5827] |
| N-SF: beats all 400, best | yes, 0.1063 | yes; 0.106258 with the author's case order (below), 0.158 with sample order, 0.07-0.10 in five further numpy families |

Candidate space: inputs/hgnc_protein-coding_gene.txt has 19,276 rows; the 19,274 of the claim excludes exactly two genes approved after the corpus date (HGNC:55810 RNF229, 2026-09-18; HGNC:28251 TLN2-AS2, 2026-10-09). My first pass used all 19,276; the only effect is +2 ties in the 235 case-conditions whose causal gene scores 0 (verified: "ties differ: 235 (of which by exactly +2 ...): 235"), changing per-case RR by at most 6.4e-9. 4,247 temporal-subset cases (PRE_percase.tsv rows) and 211 PMIDs confirmed.

Per-case agreement with results/percase.tsv (compare.py): gene level max |diff| rr 6.4e-9, top1 4.0e-11, top10 3.2e-11 (formatting); n_greater identical in all 1,000 case-conditions; gene score identical in all 1,000.
Disease level (secondary, not in the claim sentence): 8 case-conditions differ by about 1.2e-4 in RR. They are cases with no is_causal row in the C output: I set RR = 0, the author ranks the causal disease at score 0 among zero-score diseases (and for PRE uses the union of C and PRE causal rows). Both are readings of "best-ranked causal row; 0 if absent"; the effect on disease-level MRR is about 1e-6. My disease-level values: MRR C 0.548354, PRE 0.072689; top1 C 0.482924, PRE 0.045002 (author 0.5483549 / 0.0726897 / 0.4829235 / ...).

N-SF null: in the author's case order (rows of results/percase.tsv, group_order then group file order) the stated rule gives exactly the claimed value:

    N-SF null in author case order: real 0.476889 best control 0.106258 beats all True; theoretical sd 0.03091; control sd 0.03111

The best control depends on the order in which cases meet the RNG stream; whatever the order or RNG, the real drop is about 15 control-SDs above zero and beats every control I drew.

## 2. Provenance of the outputs (every file, every case)
- Each lirical_output/<release>_<C|PRE>.csv.gz contains exactly its group's cases (all 24 files, problems: 0).
- Condition and release of each file, from the disease sets in the output: for every case in every file, the set of disease ids equals OMIM+DECIPHER of exactly one data directory's phenotype.hpoa:

      v2022-02-14_C: ... == OMIM+DECIPHER of: ['v2026-06-06']
      v2022-02-14_PRE: ... == OMIM+DECIPHER of: ['v2022-02-14']
      ... (all 12 C files -> ['v2026-06-06']; each PRE file -> its own release only)
      v2026-02-16_PRE: n_cases=1 all case disease sets == OMIM+DECIPHER of: ['v2026-02-16']

  Disease rows per case: C 8689 everywhere; PRE 8260 (v2022-02-14), 8311, 8436, 8344, 8130, 8228, 8223, 8334, 8380, 8409, 8395, 8661 (v2026-02-16), each = that release's OMIM count + 47 DECIPHER.
- Data directories: sha256 of dd_<release>/phenotype.hpoa equals inputs/mapped_hpoa_sha256.txt for all 12 PRE releases (the v4 hashes 9586f442... and 687b5e68... for v2022-02-14 and v2022-06-11); dd_v2026-06-06/phenotype.hpoa = 9e10d...fbb3 = the unmapped v2026-06-06 release. The six .ser files, hp.json and mim2gene_medgen match inputs/lirical_data_sha256.txt; hgnc_complete_set.txt is f3051e4a... = inputs/hgnc_complete_set_2026-06-05.txt. All 13 directories hard-link the same shared files (one inode each).
- Mapping re-run (code/map_hpoa.py and blank_bad_frequency.py into my scratch, from the original releases whose hashes match inputs/lirical_data_sha256.txt): v2026-02-16 -> 250bc702..., v2025-10-22 -> 042d3b97..., v2022-06-11 -> 7ff79605... then v4 687b5e68... (blanked 1), v2022-02-14 -> 8a9369dc... then v4 9586f442... (blanked 3): all equal to inputs/mapped_hpoa_sha256.txt; counts equal inputs/map_hpoa.out. Not re-run for the other 8 releases (their data-directory hashes were checked).
- Phenopackets: corpus zip sha256 d0c70005...205a confirmed; all 500 sampled phenopacket files used are byte-identical to their zip entries (inputs/cases_files.tsv paths). Every sampled case's pre_release date is before its pubdate and no later run-1 release is.
- `sha256sum -c SHA256SUMS`: 92 of 92 OK.

## 3. Author's scorer and determinism
- REPRODUCE.md step 1 (code/score_lirical.py, run into my scratch): summary.json and percase.tsv byte-identical to results/ (sha256 00dfa4b9... and d5baa39b...).
- LIRICAL 2.4.1 re-run by me (Temurin 21.0.13, -Xmx600m, --parallelism 2, author's data directories, phenopackets from the cache):

      RERUN v2026-02-16_C: same cases=True rows saved/rerun=(8689, 8689) ... bit-identical (rank,is_causal,disease,proba string)=True
      RERUN v2026-02-16_PRE: same cases=True rows saved/rerun=(8661, 8661) ... bit-identical ...=True
      RERUN v2025-10-22_C: same cases=True rows saved/rerun=(52134, 52134) ... bit-identical ...=True
      RERUN v2025-10-22_PRE: same cases=True rows saved/rerun=(50370, 50370) ... bit-identical ...=True
      RERUN v2022-06-11_PRE (the group repaired under PREREG.v4, 16 cases): same cases True rows 132976 132976 bit-identical (rank,is_causal,disease,proba string): True

  All five JVM runs ended rc=0; each JVM was the only one running, by its recorded PID. Parallelism 2 instead of the author's 4 does not change the output.

## 4. Notes (not failures of the claim)
- inputs/lirical_data_sha256.txt lists 86cc190f... for "shared/hgnc_complete_set.txt"; that hash is the unused current HGNC file. The file actually in shared/ and in every data directory is f3051e4a... (the 2026-06-05 archive, listed on the file's last line and equal to inputs/hgnc_complete_set_2026-06-05.txt). Worth correcting in the package so that a reader checking that line does not get a false mismatch.
- lirical_output/v2022-02-14_PRE.log.summary records peak_ws_kb=8228, which no LIRICAL JVM can have; this looks like a failed working-set poll in run_lirical_group.sh. The output itself is complete (67 cases, disease set of v2022-02-14), and the data directory holds the v4 file.
- The claim covers a seeded 500-case sample of the 4,247-case temporal subset (PREREG R5); I checked that the sample is what the seed gives, not anything wider.
- Not done: LIRICAL re-runs of the 10 larger groups (time and RAM); map_hpoa.py re-run for 8 of the 13 releases.

## Verdict
Every claimed number was recomputed from the saved LIRICAL outputs for all 500 cases with my own code and agrees (point values to all printed digits; bootstrap intervals within 0.004 with different seeds; the null's best control exactly with the author's case order). The sample, groups, data hashes, phenopackets and the release behind every output file check out, the author's scorer reproduces byte for byte, and LIRICAL re-runs of the groups I tested reproduce the saved CSVs bit for bit. No mismatch, missing object or non-determinism found.

pass: true
