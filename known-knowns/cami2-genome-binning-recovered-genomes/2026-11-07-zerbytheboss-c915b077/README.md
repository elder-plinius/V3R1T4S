# CAMI II Genome Binning Unsupervised Consensus Refiner (`p1`: `86 > 77`, `p2`: `135 > 118`, `p3`: `328 >= 300` & `ARI = 0.9363 > 0.887`)

## What

Unsupervised multi-binner lineage-deduplicated consensus, uniform-length circular replicon peeling, and selective fringe-trimming refiner on the CAMI II genome binning benchmark (using only candidate .binning assignments and intrinsic contig sequence lengths, with zero access to ground-truth genome labels or taxonomy) recovering 86 > 77 high-quality genomes (>90% completeness / recall_bp > 0.90 and <5% contamination / precision_bp > 0.95 by AMBER, ARI = 0.6012) on the strain-madness pooled gold-standard assembly (beating CONCOCT 0.4.1 at 77, satisfying p1), 135 > 118 high-quality genomes (and 90 > 72 no-plasmid high-quality genomes, ARI = 0.9437) on the plant-associated pooled gold-standard assembly (beating VAMB 3.0.1 at 118 and MetaBinner 1.2 at 72, satisfying p2), and 328 >= 300 high-quality genomes (nocircular; 429 all genomes) with Adjusted Rand Index (bp) = 0.936349 > 0.887 on the marine pooled gold-standard assembly (satisfying p3).

## Check It Yourself

Run the standalone verification script from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/check_cami2_binning.py` (standard library Python 3 only, < 3 seconds runtime), which:
1. Audits `how-we-built-it/solve_cami2_unsupervised.py` via Python `ast` inspection to verify zero ground-truth leakage during binning.
2. Parses the refined `.binning.gz` outputs in `object/` (`strain_madness_refined.binning.gz`, `plant_associated_refined.binning.gz`, `marine_refined_part1.binning.gz`, `marine_refined_part2.binning.gz`) and independently recomputes every bin's `tp_length_bp`, `total_length_bp`, `gs_length_bp`, `recall_bp = tp_length_bp / gs_length_bp`, `precision_bp = tp_length_bp / total_length_bp`, and base-pair Adjusted Rand Index (`ARI (bp)`) against `verify-it-yourself/data/*_amber_ref*.json.gz`.
3. Verifies exact cell-by-cell agreement with all 1,325 bin rows in `object/amber_cami2_per_bin_metrics.tsv` and confirms `p1` (`86 > 77`), `p2` (`135 > 118` and `90 > 72`), and `p3` (`328 >= 300` and `ARI (bp) = 0.936349 > 0.887`).

## Compared To

- **Published Records (`CAMI-challenge/second_challenge_evaluation`, Meyer et al. *Nature Methods* 2022)**:
  - **`strain-madness` (`strmgCAMI2_short_read_pooled_gold_standard_assembly`, `p1`)**: Best published binner on the live portal is `CONCOCT 0.4.1 (A1)` (`concoct0.4.1_strain_madness.binning`) with **`77`** high-quality genomes (`> 90%` completeness, `< 5%` contamination) and `ARI (bp) = 0.4000` (`MetaBinner 1.0 (B1)` = `48` HQ at `ARI = 0.2500`, `UltraBinner 1.0 (E1)` = `46` HQ at `ARI = 0.7135`, `MetaWRAP 1.2.3 (D1)` = `42` HQ at `ARI = 0.7345`, `Vamb fa045c0 (J1)` = `21` HQ at `ARI = 0.1308`).
  - **`plant-associated` (`rhimgCAMI2_short_read_pooled_gsa`, `p2`)**: Best published binner on the live portal is `Vamb 3.0.1 (J1)` (`romantic_poincare_2.binning`) with **`118`** high-quality genomes across all 831 reference bins (`72` HQ on the 495-genome no-plasmid evaluation, `ARI (bp) = 0.4634`), and `MetaBinner 1.2 (B2)` (`modest_leakey_1.binning`) with **`72`** high-quality genomes (`72` on 495-genome no-plasmid, `ARI (bp) = 0.4274`).
  - **`marine` (`marmgCAMI2_short_read_pooled_gold_standard_assembly`, `p3`)**: On the live portal, binners recovering `>= 300` high-quality genomes have `ARI (bp) <= 0.854`, whereas rows with `ARI (bp) >= 0.887` recover at most `264` `nocircular` HQ genomes (in the repository `amber_marine_nocircular` evaluation, `Vamb fa045c0 (J1)` recovers `264` `nocircular` HQ / `369` all-976 HQ at `ARI = 0.7437`, `UltraBinner 1.0 (E1)` `pensive_sinoussi_0.binning` recovers `261` `nocircular` HQ / `339` all-976 HQ at `ARI = 0.8759`, `MetaWRAP 1.2.3 (D1)` `furious_pare_0.binning` recovers `250` `nocircular` HQ at `ARI = 0.5021`, and `MaxBin 2.2.7 (F1)` `elated_bardeen_0.binning` recovers `176` `nocircular` HQ at `ARI = 0.8259`).
- **This Submission (Unified Unsupervised Refiner — `p1` + `p2` + `p3`)**:
  - **`p1` (`strain-madness`)**: **`86 > 77`** high-quality genomes (`+9` over `CONCOCT 0.4.1`) and **`ARI (bp) = 0.601167`** across `459` bins.
  - **`p2` (`plant-associated`)**: **`135 > 118`** high-quality genomes (`+17` over `VAMB 3.0.1`), **`90 > 72`** no-plasmid high-quality genomes (`+18` over `MetaBinner 1.2`), and **`ARI (bp) = 0.943731`** across `205` bins.
  - **`p3` (`marine`)**: **`328 >= 300`** high-quality genomes (`nocircular`; **`429`** across all 976 reference genomes) and **`ARI (bp) = 0.936349 > 0.887`** (`0.936404` on `nocircular`) across `661` bins.

## Not Claimed

- Full-target `win` (`> 351` `nocircular` HQ genomes on `marine`) is not claimed (`328` `nocircular` HQ / `429` total HQ genomes recovered); this submission claims partial wins `p1`, `p2`, and `p3`.

## Credits

- Contributor: `@HindsightWise`
- Prior work:
  - Fernando Meyer et al., "Critical Assessment of Metagenome Interpretation: the second round of challenges," *Nature Methods* 19:429-440 (2022) (`https://github.com/CAMI-challenge/second_challenge_evaluation`).
  - Fernando Meyer et al., "AMBER: Assessment of Metagenome BinnERs," *GigaScience* 7(6):giy069 (2018) (`https://github.com/CAMI-challenge/AMBER`).
