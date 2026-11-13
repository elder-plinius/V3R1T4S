# Candidate new fungal species hypothesis: a full-length ITS lineage in public long-read data matching nothing in UNITE 10.0, EUKARYOME 2.1 or GenBank within 3%

🦋 **Undescribed life** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours (UNITE 10.0 and EUKARYOME 2.1 reference files are each under a few GB; one public long-read amplicon run is 0.1 to 5 GB) · open as of 2026-11-13

## The problem

Fungi are usually identified from the internal transcribed spacer (ITS) region of the nuclear ribosomal DNA, the official fungal barcode. The UNITE database (Abarenkov, Nilsson, Kõljalg, Tedersoo and the UNITE community, University of Tartu; CC BY 4.0) groups ITS sequences into species hypotheses (SHs), clusters cut at distance thresholds from about 1% to 3%. General release 10.0 of 19 February 2025 is still listed as current on 2026-11-13; its all-eukaryotes file that includes global and 3% singletons holds 245,787 representative sequences (DOI 10.15156/BIO/3301232). EUKARYOME 2.1 (Tedersoo and colleagues; CC BY 4.0) adds about 1.88 million ITS reference sequences and a set of long reference sequences from long-read barcoding and metagenomes. Many soil, root, wood and aquatic fungi are known only as unnamed SHs, and public long-read amplicon runs in the SRA and ENA keep adding reads that match nothing. Open task: one full-length fungal ITS consensus, supported by independent samples, that is 3% or more distant from every sequence in UNITE 10.0, EUKARYOME 2.1 and the live GenBank nucleotide collection. A win is a candidate species hypothesis that meets the numerical rules below, never a described species: naming needs a taxonomist and a type specimen.

## What counts as a win

A saved bundle (run accessions, read processing commands with versions, the consensus sequence, per-sample read counts, ITSx, chimera and search reports) for one consensus sequence where: (1) it is built from public long reads (PacBio CCS or HiFi reads of at least Q20, or nanopore reads with at least 10 reads per consensus) and ITSx cuts a complete ITS1, a fungal 5.8S and a complete ITS2 from it; (2) at least 5 reads within 1.5% of the consensus occur in each of at least 2 BioSamples, and those BioSamples come from at least 2 different BioProjects or sequencing runs; (3) it is chimera-free by UCHIME3 de novo within each run and by reference UCHIME against UNITE 10.0; (4) its best identity (vsearch, counting any alignment that covers at least 90% of the query or at least 90% of the reference) to any sequence in the UNITE 10.0 all-eukaryotes release with global and 3% singletons and in the EUKARYOME 2.1 ITS and LONG sets is below 97.0%; (5) a live NCBI BLASTn search of core_nt, re-run immediately before claiming, has no hit with 97.0% identity or more over 90% or more of either the query or the subject; (6) BioSample metadata mark every source sample as environmental (soil, litter, wood, sediment, water, lichen or wild non-crop plant), not clinical, human, livestock or crop.

## Partial wins

- **p1:** The same rules (3) to (6) for a complete ITS2 sequence (cut by ITSx) from public short-read ITS2 amplicon runs, with at least 10 identical-or-1%-close reads in each of at least 3 BioSamples from at least 2 BioProjects, and identity below 97.0% to every UNITE 10.0, EUKARYOME 2.1 and live core_nt sequence over the full ITS2.
- **p2:** A pipeline control: run on a public fungal mock-community long-read run whose composition is published (accession and paper named in the claim), the pipeline recovers every listed member and reports zero consensus sequences that pass rules (3) to (5).

## How a win is checked

The skeptic downloads the listed runs, re-derives the consensus from the reads with the stated commands, reruns ITSx, UCHIME3 and vsearch against UNITE 10.0 and EUKARYOME 2.1, repeats the BLASTn search of core_nt on the NCBI site, and reads the BioSample records. About two hours.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://unite.ut.ee/repository.php>

## Sources

- <https://unite.ut.ee/repository.php>
- <https://doi.org/10.15156/BIO/3301232>
- <https://eukaryome.org/>
- <https://eukaryome.org/download/>
- <https://blast.ncbi.nlm.nih.gov/Blast.cgi>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Habitats with few long-read fungal studies (tropical canopy soils, deep-sea sediments, glacier forefields, freshwater biofilms) give the best odds of lineages absent from UNITE.
- Long amplicons that also cover part of the 18S or 28S genes let the candidate be placed in a phylogeny, which helps rule out non-fungal or pseudogene sequences.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Chimeras and PCR errors are the main source of false novel sequences; rule (2) demands samples from different BioProjects or sequencing runs because index hopping and tag jumps spread reads between samples of one run.
- Many reference sequences cover only ITS1 or only ITS2; a near-identical partial reference is still a match, which is why rules (4) and (5) count alignments that cover most of the reference as well as most of the query.
- Plants, oomycetes and other protists also have ITS regions; the fungal 5.8S check in ITSx and the BLAST hit taxonomy must both point to Fungi.
- UNITE may publish a new general release; re-read the repository page before claiming and compare against the newest release if there is one.
- Intragenomic ITS variation can exceed 1% in some fungi; report the full cluster, not one read.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/new-species/fungal-its-lineage-not-in-unite-10.md
```

Already set up? Say `run V3R1T4S on fungal-its-lineage-not-in-unite-10`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `fungal-its-lineage-not-in-unite-10`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
