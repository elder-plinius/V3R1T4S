# Run it yourself

## 1. Check the numbers in object/ (seconds, Python 3 standard library only)
From this folder, in a fresh shell:

    sh verify-it-yourself/run_checks.sh          # set PYTHON=<your python> if python3 is not on PATH

Expected last line: `PASS` (full expected output in verify-it-yourself/RECEIPTS.md). The checker recomputes every
per-case reciprocal rank and top-1 value from the stored rank counts and recomputes the means, the paired drop, the
400-control null exactly and the bootstrap intervals to Monte Carlo tolerance.

## 2. Rebuild the object (about 35 minutes of JVM time plus downloads; Java 21, LIRICAL 2.4.1, Python 3.11 with numpy/scipy/pandas, see how-we-built-it/requirements.txt)
1. Corpus: phenopacket-store release 0.1.27, all_phenopackets.zip
   (https://github.com/monarch-initiative/phenopacket-store/releases/tag/0.1.27, sha256
   d0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a). The 500 sampled cases and their files in the
   zip: how-we-built-it/inputs/sample500.txt and cases_files.tsv (extract with how-we-built-it/code/extract_cases.py
   or by hand).
2. LIRICAL 2.4.1 (https://github.com/TheJacksonLaboratory/LIRICAL/releases/tag/v2.4.1) and its data directory:
   hp.json of HPO release v2026-06-06, hgnc_complete_set_2026-06-05.txt (HGNC monthly archive), mim2gene_medgen
   (NCBI), the six Jannovar .ser files of Zenodo record 5410367, and phenotype.hpoa; sha256 of each in
   how-we-built-it/inputs/lirical_data_sha256.txt.
3. One data directory per HPOA release: condition C uses phenotype.hpoa of HPO release v2026-06-06 unchanged; PRE
   uses the release named for each case in how-we-built-it/inputs (group_order.txt and the case's release in
   object/percase.tsv, column pre_release), mapped with how-we-built-it/code/map_hpoa.py and, for v2022-02-14 and
   v2022-06-11, how-we-built-it/code/blank_bad_frequency.py; expected hashes in inputs/mapped_hpoa_sha256.txt.
4. Per release group and condition:
       java -Xmx1g -jar lirical-cli-2.4.1.jar benchmark --phenotype-only --parallelism 4 -d <datadir> -o <group>_<C|PRE>.csv.gz <phenopacket files>
   The 24 output files we obtained are listed with size and sha256 in inputs/LIRICAL_OUTPUTS_not_included.txt
   (too large for this package).
5. Score: python -I how-we-built-it/code/score_lirical.py score <outputs dir> <dir with sample500.txt, group_order.txt,
   group_<release>.txt> <dir with run-1 C_percase.tsv and PRE_percase.tsv> <HGNC protein-coding list> <hgnc_complete_set_2026-06-05.txt> <mim2gene_medgen> <result dir>
   The run-1 files give each case's causal gene, PMID, publication date and release; their columns are reproduced in
   object/percase.tsv (gene, pmid, pre_release).
