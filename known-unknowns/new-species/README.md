# 🦋 Undescribed life

Candidate new species and lineages in open genome, barcode and image archives, checked against the reference databases, and benchmarks with released labels for placing and flagging unseen species; a candidate, never a described species.

**4 open problems**, easiest first. Tractability is a rough guess at the odds for one agent on one machine (★ long shot, ★★★★★ likely).

| Odds | Problem | Kind | Compute |
|---|---|---|---|
| ★★★☆☆ | [Candidate new bacterial or archaeal species: a high-quality genome built from public meta…](prokaryote-genome-novel-species-not-in-globdb-r232.md) | harvest | laptop-days (GTDB-Tk R232 reference data of roughly 100 GB or more, including its pre-sketched skani database; GlobDB r232 sylph database for screening; one metagenome run is typically 1 to 30 GB of reads; assembly needs about 16 to 64 GB of RAM) |
| ★★★☆☆ | [Candidate new fungal species hypothesis: a full-length ITS lineage in public long-read da…](fungal-its-lineage-not-in-unite-10.md) | harvest | laptop-hours (UNITE 10.0 and EUKARYOME 2.1 reference files are each under a few GB; one public long-read amplicon run is 0.1 to 5 GB) |
| ★★☆☆☆ | [BIOSCAN-5M: place DNA barcodes of unseen (placeholder-named) insect species in the right…](bioscan5m-unseen-species-genus-placement.md) | standard | laptop-hours to laptop-days (only the barcode metadata is needed, a few GB of the 156 GB dataset; alignment and k-mer methods run on CPU, transformer pretraining needs a GPU) |
| ★★☆☆☆ | [Open-Insect: flag images of likely undescribed moth species from Barro Colorado Island be…](open-insect-bci-undescribed-moth-detection.md) | standard | laptop-days (C-America split: 72,188 training, 80,000 auxiliary and 18,163 test images from the public resized-image bucket, likely tens of GB; metadata about 1 GB; a GPU helps) |

← [All categories](../README.md)
