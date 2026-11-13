# 🗺 Known unknowns

The hills nobody has climbed yet: **1152 open problems in 35 categories**. Each page says what the problem is, what counts as a win, how a win is checked, where to check it is still open, ideas to start from, and the traps that produced false wins before.

Pick one, then tell your agent:

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/<category>/<problem>.md
```

Or don't pick: your agent can roam anywhere, as long as a stranger's computer can check the answer.

| Category | Open | What's in it |
|---|---|---|
| 🕸️ [Graphs, games and automata](graphs-games-automata/README.md) | 165 | Graph records, puzzles, tilings and cellular automata. |
| 📊 [Record tables](record-tables/README.md) | 132 | Codes, designs, packings and constructions measured against public tables. |
| 🔢 [Number hunts](number-hunts/README.md) | 123 | Certified bounds, exact searches and explicit solutions in number theory and computability. |
| ✏️ [Erdős problems and proofs](erdos-and-proofs/README.md) | 69 | Erdős problems and relatives: counterexamples, small cases, machine-checked proofs. |
| ⚛️ [Physics](physics/README.md) | 64 | Statistical mechanics, lattice models, quantum information and materials: exact counts, certified bounds, constants to record precision and public leaderboards. |
| 🚚 [Optimization benchmarks](optimization-benchmarks/README.md) | 56 | Best-known solutions on public routing, scheduling and MIP benchmark libraries. |
| 🧬 [Disease research](disease-research/README.md) | 55 | Cancer, rare and neglected diseases, antimicrobial resistance and outbreaks: public data, public scorers, computational claims only. |
| 🎲 [Recreational math](recreational-math/README.md) | 48 | Puzzle records, magic squares, dissections and sequences with public tables. |
| 🦠 [Biology](biology/README.md) | 47 | Protein, DNA and evolution benchmarks and record tables with mechanical checkers. |
| 🃏 [Wildcard](wildcard/README.md) | 37 | Open, checkable problems from fields nobody else here covers. |
| ⚪ [Packings and physics](packings-physics/README.md) | 36 | Circle, sphere and point configurations and energy minima vs live tables. |
| 🔭 [Sky archives](sky-archives/README.md) | 34 | New vetted candidates in public astronomy archives (never 'a planet', only 'a candidate'). |
| 🌍 [Earth and sky](earth-and-sky/README.md) | 34 | Missed events in open geophysical and space archives, checked against live catalogs. |
| ⚡ [Algorithms](algorithms/README.md) | 27 | Fast matrix multiplication schemes and other algorithmic records. |
| 🤖 [Machine learning](machine-learning/README.md) | 27 | Small leaderboards and efficiency records a laptop can top with open models run locally. |
| 🔐 [Unbroken ciphers](unbroken-ciphers/README.md) | 20 | Historical and challenge ciphers nobody has read yet. |
| ✅ [Formal proofs](formal-proofs/README.md) | 18 | Statements waiting for a machine-checked proof: Lean's kernel is the referee. |
| 📜 [Undeciphered scripts](undeciphered-scripts/README.md) | 17 | Writing systems and corpora nobody can read; wins are frozen, checkable predictions, never interpretations. |
| 🏺 [Ancient texts and fragments](ancient-texts/README.md) | 16 | Unidentified papyri, tablet fragments, lacunae and sign detection, scored against held-out data. |
| 💊 [Drug discovery](drug-discovery/README.md) | 14 | Molecular property, binding, docking and design leaderboards scored on official splits. |
| 🧭 [Uncharted maps](uncharted/README.md) | 13 | Features missing from the maps of Earth, the ocean floor and other worlds, or events missing from their inventories, found in open sonar, LiDAR, altimetry, satellite and orbiter data and checked against live catalogs; a claim is a candidate, never a discovery. |
| 🛡️ [ML robustness](ml-robustness/README.md) | 12 | Stronger attacks and soundness counterexamples on public, locally run benchmark models. |
| 🪐 [Planets and moons](planetary-science/README.md) | 11 | Solar-system and exoplanet problems with checkable wins: new moons and minor bodies as vetted candidates, surface benchmarks, orbit and shape records, exoplanet challenges with released truth. |
| 🧫 [Genomes](genomics/README.md) | 10 | Genome assembly, variant calling, metagenome binning and comparative genomics scored against released truth sets. |
| 🐦 [Ecology and bioacoustics](ecology/README.md) | 9 | Species identification, bioacoustics, camera traps and biodiversity benchmarks with released labels. |
| 🌋 [Herculaneum scrolls](herculaneum-scrolls/README.md) | 8 | Ink detection and surface segmentation on the public Vesuvius Challenge data. |
| ⚗️ [Chemistry and materials](chemistry-materials/README.md) | 8 | Quantum-chemistry benchmark sets, crystal and molecular structure records and materials benchmarks with mechanical scorers; no toxicity or weapon-relevant endpoints. |
| 🛠️ [Engineering and chips](engineering/README.md) | 8 | Chip placement, routing and logic-synthesis benchmarks, aerodynamic, energy and structural design cases with published best results. |
| ⚓ [Wrecks and ancient sites](lost-and-hidden/README.md) | 8 | Wrecks and ancient built features as candidates in open bathymetry, LiDAR and imagery, checked against the public wreck and site records, and benchmarks with released labels. Exact locations of candidates stay sealed and go only to the responsible authority. |
| 🧠 [Neuroscience](neuroscience/README.md) | 7 | Spike sorting, connectomics, neural imaging and brain-signal decoding benchmarks with released ground truth. |
| 🗜️ [Compression and code golf](compression-and-golf/README.md) | 5 | Byte-exact compression records and shortest-program tables. |
| 💥 [Particle physics](particle-physics/README.md) | 5 | Open-data and simulation benchmarks from high-energy physics: tagging, tracking, anomaly detection and fast simulation, scored against released truth. |
| 🐋 [Animal communication](animal-communication/README.md) | 4 | Whale, dolphin, elephant and other animal signals: structure, context and prediction problems scored on held-out public recordings; never a translation. |
| 🦋 [Undescribed life](new-species/README.md) | 4 | Candidate new species and lineages in open genome, barcode and image archives, checked against the reference databases, and benchmarks with released labels for placing and flagging unseen species; a candidate, never a described species. |
| 🗝️ [Crypto math](crypto-math/README.md) | 1 | Public challenges built to be attacked, and the mathematics of cryptographic primitives. |

Tractability, compute and status dates are guesses from the day each page was written; the status page linked on each problem is the only authority. Every page is generated from [`bank/targets.json`](../bank/targets.json): `python3 bank/build_known_unknowns.py`.
