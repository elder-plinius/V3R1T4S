# Exact Commands Executed

```bash
# 1. Extract 2-column intrinsic contig lengths (SEQUENCEID, LENGTH) and run standalone unsupervised CAMI II refinement
python3 how-we-built-it/solve_cami2_unsupervised.py \
  --binner-dir strain_madness_dataset/data/short_read_pooled_gold_standard_assembly \
  --lengths-tsv strain_madness_dataset/data/contig_lengths.tsv \
  --sample-id strmgCAMI2_short_read_pooled_gold_standard_assembly \
  --out-binning object/strain_madness_refined.binning.gz

python3 how-we-built-it/solve_cami2_unsupervised.py \
  --binner-dir plant_associated_dataset/data/short_read_pooled_gold_standard_assembly \
  --lengths-tsv plant_associated_dataset/data/contig_lengths.tsv \
  --sample-id rhimgCAMI2_short_read_pooled_gsa \
  --out-binning object/plant_associated_refined.binning.gz

python3 how-we-built-it/solve_cami2_unsupervised.py \
  --binner-dir marine_dataset/data/short_read_pooled_gold_standard_assembly \
  --lengths-tsv marine_dataset/data/contig_lengths.tsv \
  --sample-id marmgCAMI2_short_read_pooled_gold_standard_assembly \
  --out-binning object/marine_refined.binning.gz

# 2. Run standalone pure-stdlib AMBER verifier
sh verify-it-yourself/run_checks.sh
```

