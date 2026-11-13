# Candidate new bacterial or archaeal species: a high-quality genome built from public metagenome reads, outside every GTDB R232 and GlobDB r232 species

🦋 **Undescribed life** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-days (GTDB-Tk R232 reference data of roughly 100 GB or more, including its pre-sketched skani database; GlobDB r232 sylph database for screening; one metagenome run is typically 1 to 30 GB of reads; assembly needs about 16 to 64 GB of RAM) · open as of 2026-11-13

## The problem

Bacterial and archaeal species are delimited in practice by genome similarity: two genomes belong to one species when their average nucleotide identity (ANI, the mean identity of the aligned shared regions) is about 95% or more over at least half of the genome (alignment fraction, AF, at least 0.5). The Genome Taxonomy Database (GTDB; Parks, Chuvochina, Rinke, Mussig, Chaumeil, Hugenholtz and colleagues) release R232 of 15 April 2026 holds 901,341 genomes in 199,923 species clusters (189,801 bacterial, 10,122 archaeal) and 186 phyla; GTDB-Tk 2.8.0 (13 October 2026) classifies new genomes against it. The GlobDB (Speth, Pullen, Aroney, Coltman, Osvatic, Woodcroft, Rattei, Wagner and 19 co-authors) release r232 of June 2026 adds species representatives from 25 other genome catalogues (mOTUs, SPIRE, GCMETA, GEM, MGnify and others) and holds 346,233 species-representative genomes in all. Most environmental microbes are still uncatalogued, and many public metagenome runs in the Sequence Read Archive (SRA) and the European Nucleotide Archive (ENA) have never been binned into genomes; Logan v1.2 (Chikhi, Raffestin, Korobeynikov, Edgar, Babaian and colleagues) provides assembled contigs of nearly all SRA runs up to a December 2025 freeze. Open task, as of 2026-11-13: one high-quality genome reconstructed only from public environmental reads that lies outside every GlobDB r232 species. A win is a candidate new species that meets the numerical rules below, never a described species: naming needs a taxonomist and a designated type under the SeqCode or the prokaryotic code.

## What counts as a win

A saved bundle (run accessions, assembly and binning commands with versions, genome FASTA, CheckM2, GUNC, rRNA and tRNA reports, GTDB-Tk output, ANI tables) for one genome built only from openly downloadable SRA or ENA reads, or Logan contigs of such runs, where: (1) CheckM2 completeness is at least 90% and contamination at most 5%, and the genome carries 5S, 16S and 23S rRNA genes and at least 18 distinct tRNAs (the MIMAG high-quality standard, Bowers et al. 2017); (2) GUNC, a check for genomes chimeric across lineages, passes; (3) GTDB-Tk 2.8.0 with R232 reference data leaves the species field empty (s__), and its closest-reference columns, if filled, show ANI below that reference's species radius or AF below 0.5; (4) for every one of the 346,233 GlobDB r232 species representatives, skani ANI is below 95.0% or AF below 0.5 in both directions (screen with the GlobDB r232 sylph database, then skani against the 50 nearest representatives); (5) the ENA and NCBI records of the source runs and their BioProject, re-fetched before claiming, list no genome assembly built from those runs; (6) the BioSample metadata mark the sample as environmental (soil, sediment, water, hot spring, biofilm, wild non-crop plant or similar), not clinical, human, livestock or crop. The claim is called a candidate new species.

## Partial wins

- **p1:** A medium-quality genome (CheckM2 completeness at least 50%, contamination below 10%, completeness minus 5 times contamination at least 50) that meets rules (2) to (6) of the success criterion.
- **p2:** A genome meeting rules (1), (2), (5) and (6) for which GTDB-Tk 2.8.0 with R232 leaves the species empty, but which lies within 95% ANI (AF at least 0.5) of a GlobDB r232 representative that came from a non-GTDB catalogue: a high-quality public-read genome for a species until now known only from a MAG catalogue, with that representative named.

## How a win is checked

The skeptic downloads the listed runs, maps the reads back to the supplied genome (at least 90% of its bases covered), reruns CheckM2, GUNC, barrnap and tRNAscan-SE, runs GTDB-Tk 2.8.0 with the R232 reference data, screens the genome with sylph against the GlobDB r232 database and confirms with skani against the nearest representatives, and reads the ENA, NCBI and BioSample records. Under a day on a workstation with about 150 GB of free disk.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://globdb.org/>

## Sources

- <https://gtdb.ecogenomic.org/>
- <https://gtdb.ecogenomic.org/stats/r232>
- <https://forum.gtdb.ecogenomic.org/t/announcing-gtdb-r11-rs232/826>
- <https://gtdb.ecogenomic.org/methods>
- <https://ecogenomics.github.io/GTDBTk/announcements.html>
- <https://ecogenomics.github.io/GTDBTk/faq.html>
- <https://globdb.org/>
- <https://globdb.org/methods>
- <https://globdb.org/downloads>
- <https://fileshare.lisc.univie.ac.at/globdb/globdb_r232/globdb_r232_dataset_list.tsv>
- <https://arxiv.org/abs/2506.11896>
- <https://github.com/IndexThePlanet/Logan>
- <https://github.com/chklovski/CheckM2>
- <https://github.com/bluenote-1577/skani>
- <https://www.nature.com/articles/nbt.3893>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Screen candidate runs first with the GlobDB r232 SingleM metapackage or sylph database and pick runs whose reads are least covered by known species; under-sampled habitats (hot springs, deep sediments, cave biofilms, saline lakes) give the best odds.
- Long-read (PacBio HiFi) metagenomes often yield circular genomes that carry complete rRNA operons, which short-read bins usually lack; rule (1) is much easier from them.
- Logan contigs remove the assembly step for a run, but binning still needs per-sample coverage, so map the run's reads (or reads of related runs from the same BioProject) back to the contigs.
- A candidate whose GTDB-Tk output also leaves the genus or family empty is a stronger result worth stating, but the win is judged only on the species rules.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- rRNA genes often fail to bin with the rest of a genome from short reads; adding an unrelated 16S contig to meet rule (1) is chimerism that GUNC and read coverage checks expose.
- GlobDB dereplicates its source catalogues at 96% ANI, so a genome at 95 to 96% ANI to a catalogue member can still be in a known species; rule (4) is judged only against the representatives, and a borderline value close to 95% should be reported as such.
- Genomes deposited in NCBI after the GTDB R232 snapshot are not in either release; check the source study for deposited genomes (rule 5) and say in the claim that novelty is relative to the named releases.
- Use only openly downloadable runs; never controlled-access human data. Host-associated human, livestock and crop samples are excluded by rule (6).

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/new-species/prokaryote-genome-novel-species-not-in-globdb-r232.md
```

Already set up? Say `run V3R1T4S on prokaryote-genome-novel-species-not-in-globdb-r232`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `prokaryote-genome-novel-species-not-in-globdb-r232`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
