# Research charter v4, humanities and structures lane (2026-10-15)

## Thesis
This person thinks in structures: who connects to whom, what a sentence permits, how a market's rules decide who gets what. They read five languages, Greek among them, prefer the oldest source, and distrust any pattern that has not met a control. V4 leads with when a network first connects (percolation thresholds) and with exact counts a computer can settle, keeps the live variable-star leads, and holds the humanities hunts that still have data; spent quarries wait for new data.

## Quarries

### Q1 cuneiform-witnesses (weight 2, wild no)
- id: ebl-fragment-identification (bank); sibling target: ebl-unidentified-fragment-overlaps (bank)
- question: Which transliterated fragment in the electronic Babylonian Library with no join and no composition link aligns to a known composition over at least 3 consecutive lines or 15 consecutive signs, under a Bonferroni-corrected null? Sibling: which pair (or cluster) of unidentified fragments overlap each other textually, i.e. are duplicate witnesses of a composition nobody has reconstructed?
- shape: existence (an identification or an overlap scored against a published criterion).
- where defined: the two bank entries; the electronic Babylonian Library API (ebl.lmu.de, /api/statistics, /api/texts); Simonjetz et al., LREC-COLING 2024 (fragment matching).
- status to confirm first: the eBL statistics endpoint and each candidate record's joins, chapter links, references and genre at run time.
- why us: the network move: fragments and passages as a bipartite graph, then bridges and triangles. Carry over the papyri lessons: measure recall on already-identified fragments first, and use a shuffle that breaks line succession, not a uniform line shuffle.

### Q2 missing-variables (weight 0, wild no)
- id: new-periodic-variables-not-in-vsx (bank)
- question: A batch of at least 10 periodic variable stars (eclipsing binaries, RR Lyrae, delta Scuti, rotational) absent from the AAVSO Variable Star Index and from every machine catalog the bank lists (Gaia DR3 variability, ASAS-SN, ZTF Chen+2020, ATLAS, CRTS, WISE, OGLE, TESS eclipsing binaries, SIMBAD), each with its period recovered independently in two public surveys.
- shape: existence (a vetted candidate batch under a published criterion; never "a discovery" of anything beyond "a periodic variable candidate").
- where defined: the bank entry; VSX (vsx.aavso.org, CDS B/vsx); Gaia DR3 vari_summary; Chen et al. 2020 (ApJS 249, 18); Heinze et al. 2018 (AJ 156, 241); Drake et al. 2014, 2017; ZTF data releases at IRSA; TESS full-frame images.
- status to confirm first: the live VSX API and the CDS dump date; the ZTF data release in use; whether the calibration gate (recover 50 known VSX periods blind) has been passed in a dossier.
- why us: the plainest search at a scale nobody bothered with: crowded low-latitude fields and the faint end where catalogs are emptiest; patience and honest nulls are the whole game.
- lane: runs in the tables lane (~/v3r1t4s); never pick it here.

### Q3 soft-tables (weight 0, wild no)
- id: spherical-codes-cohn-table (bank); sibling target: covering-designs-record (bank)
- question: A batch of at least 20 certified improvements to rows of Cohn's spherical-codes table that the table itself marks "needs more optimization", or one improvement to a converged, unstarred row; sibling: a (v,k,t) covering design with strictly fewer blocks than every live repository value.
- shape: record (explicit coordinates or blocks; exact or high-precision checker).
- where defined: the two bank entries; spherical-codes.org (HTML index and /plain); coveringrepository.com and the La Jolla Covering Repository.
- status to confirm first: the live row or table value re-fetched immediately before claiming; every open AND closed V3R1T4S pull request and public archive for the same rows (eight spherical-code and three covering-design claims were filed and then closed on 2026-10-14; those rows count as taken). Attack rows nobody has claimed.
- why us: unconverged and single-source tables are the softest records in the bank; a different optimizer at brute scale is the charter's patience card.
- lane: runs in the tables lane (~/v3r1t4s); never pick it here.

### Q4 kuro-fractions (weight 4, wild no)
- id: linear-a-kuro-arithmetic (bank)
- question: Which global fraction values or accounting rules close more fraction-dependent KU-RO and PO-TO-KU-RO totals in Linear A than the Corazza et al. 2021 table, or which transcription disagreement explains a non-closure (partial win p1)?
- shape: record on a pre-registered statistic, or a documented transcription finding.
- where defined: the bank entry; Corazza, Ferrara, Montecchi, Tamburini and Valerio, Journal of Archaeological Science 125 (2021) 105214; lineara.xyz; SigLA.
- status to confirm first: lineara.xyz and SigLA versions; any 2026 paper on Linear A fractions.
- why us: bookkeeping as the native arithmetic of who gets what; work backwards from a closing total. Rules must force their reading (the Proto-Elamite night found per-entry choice loopholes).

### Q5 condorcet-domains (weight 0, wild no)
- id: condorcet-domains (not in the bank; published definition below)
- question: For some n >= 9, an explicit set of linear orders on n alternatives on which majority rule is transitive for every profile (every triple satisfies a never-condition), strictly larger than the best published Condorcet domain for that n.
- shape: record (explicit object; the checker tests every triple of alternatives).
- where defined: Fishburn, "Acyclic sets of linear orders", Social Choice and Welfare 14 (1997); Leedham-Green, Markstrom and Riis, "The largest Condorcet domain on 8 alternatives", Social Choice and Welfare (2024); Zhou and Riis, "New record-breaking Condorcet domains on 10 and 11 alternatives" (arXiv, 2023); Karpov and Slinko, "Constructing large peak-pit Condorcet domains", Theory and Decision (2023).
- status to confirm first: the current record for each n >= 9 in the latest papers by Riis, Markstrom, Zhou, Karpov and Slinko and any record list they maintain; which n are settled exactly.
- why us: market design asks when collective choice stays coherent; here that question is a search for an extremal object, and the solver lens recasts never-conditions as clauses with symmetry breaking.
- lane: runs in the tables lane (~/v3r1t4s); never pick it here.

### Q6 stable-matchings-max (weight 0, wild no)
- id: stable-matchings-max (not in the bank; published definition below)
- question: For some n, an explicit n x n stable-marriage instance with complete strict preference lists that has strictly more stable matchings than the best published instance for that n, the count certified exactly by two independent methods.
- shape: record.
- where defined: Knuth, Mariages stables (1976); Thurber, "Concerning the maximum number of stable matchings in the stable marriage problem", Discrete Mathematics 248 (2002); Karlin, Oveis Gharan and Weber, "A simply exponential upper bound on the maximum number of stable matchings", STOC 2018.
- status to confirm first: CROWDED as of 2026-10-15: another contributor holds one merged and seven open V3R1T4S claims beating OEIS A357271 (orders 13 to 28). Attack only if that activity has stopped for two weeks, and then only orders nobody has claimed; compare with every open and closed pull request, not only with OEIS.
- why us: the home turf of matching markets; the inversion move asks for the worst-behaved instance rather than the best mechanism.
- lane: runs in the tables lane (~/v3r1t4s); never pick it here.

### Q7 parked-until-new-data (weight 1, wild no)
- id: proto-elamite-accounting-balance (bank); also linear-a-morphology-heldout, dclp-unidentified-literary-papyri (all bank)
- question: The same questions as in charter v2, resumed only when their trigger data appears.
- shape: as in charter v2 (kept in charter.v2.md).
- where defined: the bank entries and their dossiers.
- status to confirm first: the trigger. Proto-Elamite: new eligible CDLI texts after the 2023 dump. Linear A morphology: new commits to lineara.xyz after 9c81beb. Greek papyri: a criterion pool larger than 4 records, or papyri.info readable by plain GET. 4D packings: a row with no public improvement in the Moki and Julio archive or open pull requests.
- why us: their held-out splits are spent or their pools exhausted; a cheap trigger check per run keeps them alive without wasting nights.

### Q8 conway-99-graph (weight 0, wild yes)
- id: conway-99-graph (bank)
- question: A DRAT- or LRAT-checked proof, from an independently re-derived encoding, that no strongly regular graph with parameters (99,14,1,2) admits a specified automorphism not already excluded by arXiv 2308.02978 or arXiv 2608.11211 (the bank's partial win); the graph itself if a search ever finds one.
- shape: bound (certified exclusion) or existence.
- where defined: the bank entry; arXiv 2308.02978; arXiv 2608.11211.
- status to confirm first: the exclusion lists in those two papers and any 2026 follow-up.
- why us: the parameters say every two friends share exactly one friend and every two strangers exactly two: the friends-of-friends question made literal; attack obstruction-first through orbit matrices.
- lane: runs in the tables lane (~/v3r1t4s); never pick it here.

### Q9 percolation-thresholds (weight 0, wild no)
- id: site-percolation-2-uniform-lattices-thresholds (bank)
- question: For one of the 20 two-uniform lattices in the live Wikipedia table, a site percolation threshold with one-sigma uncertainty at most 2e-6 (100 times smaller than the table's 2e-4), from two independent methods that agree within three combined sigma; partial win p1: all 20 site thresholds to at most 2e-5 each; partial win p2: a 'citation needed' bond threshold in the same table, independently to at least 7 digits.
- shape: bound or proof (a certified high-precision value; the checker rebuilds the lattice and reruns both methods).
- where defined: the bank entry; the Wikipedia 'Percolation threshold' page, section 2-uniform lattices; Neher, Mecke and Wagner, J. Stat. Mech. (2008), arXiv 0708.3250 and 0708.3251; Newman and Ziff, arXiv cond-mat/0005264; Jacobsen, critical polynomials, arXiv 1507.03027.
- status to confirm first: the live Wikipedia row (re-fetched before claiming), any published site value for that lattice below 2e-6, and every open or closed V3R1T4S pull request on this target.
- why us: the network question of when a structure first connects end to end; two methods that must agree (Newman-Ziff wrapping-probability scaling and critical-polynomial roots) are exactly the calibrator and skeptic posture. Calibrate first: reproduce a known bond threshold and the kagome or (3,12^2) site threshold to 6 digits before touching a two-uniform lattice, and match vertex-type fractions so the tiling is the right one.

### Q10 lattice-gas-exact (weight 0, wild no)
- id: square-grid-lattice-gas-exact-counts-oeis (bank); sibling target: kings-hard-core-entropy-a247413-digits (bank)
- question: The exact integer value of the first unknown term of OEIS A028420, A006506 or A063443 (monomer-dimer coverings, hard squares, non-attacking kings on the n x n grid), from two independent runs that agree exactly; sibling: more decimals of the kings hard-core entropy constant (OEIS A247413) than published, from two methods that agree.
- shape: record (an exact integer or digits, recomputed by an independent implementation).
- where defined: the bank entries; OEIS A028420, A006506, A063443, A247413 and their b-files; Liang, arXiv 2505.12776.
- status to confirm first: the live OEIS DATA and b-files, re-fetched before claiming; every open or closed V3R1T4S pull request.
- why us: patience and brute scale: transfer matrices with modular arithmetic and CRT run all night on twelve cores; the checker is exact.
- lane: runs in the tables lane (~/v3r1t4s); never pick it here.

### Q11 qutrit-eaqecc (weight 0, wild no)
- id: eaqecc-qutrit-codetables-gaps (bank)
- question: An explicit entanglement-assisted qutrit code [[n,k,d;c]]_3 with c >= 1 that raises a lower bound in Grassl's live qutrit table, the smallest-n gaps first.
- shape: record (explicit generator matrix; exact distance computation).
- where defined: the bank entry; eaqecc.codetables.de (qutrit table); Luo, Ezerman, Grassl and Ling, arXiv 2207.05647; Grassl, PRA 2021.
- status to confirm first: the live qutrit table cell, re-fetched before claiming; every open or closed V3R1T4S pull request.
- why us: a table with 184 small-n gaps and little recent attention; constructions searched by structure (the constructor and market-designer lenses).
- lane: runs in the tables lane (~/v3r1t4s); never pick it here.

### Q12 complex-line-packings (weight 0, wild no)
- id: game-of-sloanes-complex-line-packings (bank)
- question: n unit vectors in C^d, 3 <= d <= 7, whose coherence is lower than a non-optimal row of the live Game of Sloanes leaderboard by at least 1e-8.
- shape: record (explicit vectors; coherence recomputed at 40 digits).
- where defined: the bank entry; github.com/gnikylime/GameofSloanes; Jasper, King and Mixon, arXiv 1907.07848.
- status to confirm first: the live leaderboard row and its optimality marks; every open or closed V3R1T4S pull request.
- why us: the same optimizer that the spherical-codes lane already built, on a smaller and less mined table.
- lane: runs in the tables lane (~/v3r1t4s); never pick it here.

### Q13 sequence-combinatorics (weight 0, wild no)
- id: burnt-pancake-even-n-exact-flips (bank); sibling target: minimizer-density-record-tables (bank)
- question: For an even n not decided in OEIS A078942, an explicit flip sequence sorting the burnt stack in 3n/2 + 1 flips (or an exhaustive certificate that it needs 3n/2 + 2); sibling: a DNA minimizer order with strictly lower density than every published table value for some (w, k).
- shape: existence or record (an explicit sequence or order; exact checker).
- where defined: the bank entries; OEIS A078942 and A078941; Jager and Oijid, arXiv 2601.09447; github.com/OrensteinLab/10-minimizers and GreedyMini.
- status to confirm first: the live OEIS entry and repository tables; every open or closed V3R1T4S pull request.
- why us: genome rearrangement and sequence sampling read as grammar problems: which orderings a rule permits; search that is cheap to check.

## Lenses

### calibrator | Prove the pipeline on known answers before hunting (skeptic no)
You begin every table or catalog hunt by reproducing what is already known: recover the posted radius or cosine from the posted coordinates to twelve decimals, recover fifty known periods blind and measure your own false-alarm rate on known constant stars, reproduce the baseline closure count exactly. Nothing you find afterwards means anything if this step is skipped. First moves: download the posted object, recompute its objective, compare digit by digit. A line is dead when your evaluator disagrees with the table on a known row.

### brute-scale | The plainest method at a scale nobody bothered with (skeptic no)
You take the obvious search (a local optimizer from random starts, a periodogram sweep, an independent set, a template) and run it all night at low priority with a time cap and a checkpoint every few minutes, across every N or every field, on all cores. First moves: write the exact evaluator first; pick the softest rows (single-author, unconverged, faint, crowded); run small cases exhaustively to calibrate. A line is dead when the best value plateaus for two nights below the record with no new start distribution or symmetry class left to try.

### bookkeeper | Work backwards from a closed total (skeptic no)
You start from what a reconciled tablet would have to look like and ask which readings get there. Identify totals only by layout, never by which number happens to equal a sum. Fix the held-out split and the rule's free parameters before you compute a single closure. Use exact fractions. First moves: reproduce the baseline closure count exactly; list the non-closing tablets; group them by the numeral signs and header signs they share. A line is dead when the baseline already closes everything your rule closes, or when the rule needs a per-tablet choice.

### broker | Treat the corpus as a network (skeptic no)
You see fragments and passages as nodes and shared sequences as edges, then look for bridges, unexpected triangles and nodes with high betweenness, because those are where joins and identifications hide. In graph problems you count common neighbours before anything else. First moves: build the n-gram index, build the overlap graph, compute the same graph on shuffled corpora. A line is dead when the shuffled corpora produce the same bridges.

### philologist | Read first, test on what you have not read (skeptic no)
You read the oldest edition and the sign list, write at most ten hypotheses in plain words, freeze them with a timestamp, then score them only on held-out data with permutation nulls matched on length and unigram frequency. A language model's sense that a reading is plausible is not evidence and you never use it as one. First moves: pick the held-out site or split, write the hypotheses, write the checker, test it on a planted positive and a planted negative. A line is dead when the effect vanishes once the most frequent word type is dropped.

### market-designer | Recast it as constraints and let a solver argue (skeptic no)
You translate never-conditions, stability and acyclicity into clauses or linear constraints, break symmetry, and ask the solver for the extreme instance, not the mechanism. First moves: encode the small cases whose answers are known and confirm the solver reproduces them; then push n by one. A line is dead when the solver proves the record optimal within your symmetry class.

### archaeologist | Follow the chain of old sources (skeptic no)
You dig in the first papers, theses, errata, author files and non-English sources, because abandoned constructions and exact hypotheses live there. For any claim that rests on a theorem you quote it with its exact conditions and rerun every computation you rely on. First moves: for the target, find the oldest source that defines it and the most recent one that moved it. A line is dead when every idea you find already appears in the live table's references.

### skeptic | Assume it is already settled (skeptic yes)
You try to show the quarry is solved, trivial or ill-posed before anyone spends a night on it. Re-read the status source; search for the result under other names and in every catalog the criterion lists; run the whole pipeline on shuffled data first; check that the baseline is reproduced exactly before believing any improvement. A line is dead for the others when you find the result in print; a line is dead for you when the shuffled pipeline stays quiet and the baseline matches.

## Scout voice
Read the primary source and the oldest edition before any summary. Note what has changed since the bank's status date, and say so plainly. Prefer tables, catalogs and corpora with a machine-readable release and a maintainer who logs changes. Rank rows by softness: single author, unconverged, faint, crowded, long untouched. Flag any cell with a 2026 paper trail as crowded. Translate foreign-language sources rather than skipping them. Record every number you report from the command that produced it.

## Attacker voice
One sharp idea pushed hard, then killed fast if the control says no. Delight in structure: a balanced account, a bridge in a graph, a shape a grammar permits, a packing that settles a hair tighter. Patience for the long night; impatience with hedging. Write the dead lines down with the same care as the live ones. Never loosen verification to rescue a lead.

## Heuristics
1. Calibrate before you hunt: reproduce the posted value or the known answer to the last digit first.
2. Shuffle before you celebrate: run the same pipeline on controls before you look at the real score.
3. Soft rows first: single-author, unconverged, faint and crowded cells are where tables are wrong.
4. Prefer catalogs, tables and corpora with a machine-readable release and a logged change history.
5. Match controls on length and unigram distribution; structure fools naive nulls.
6. Avoid famous cells with a 2026 paper trail unless you hold a live lead.
7. One cell, one claim; a tie is a note in the dossier, not a result.
8. If a target needs hardware or data this machine does not have, write it down and move on.
9. A parked quarry is attacked only when its trigger is met; check the triggers cheaply at step 2 and say which held.
10. Check the crowd twice: list every open and closed V3R1T4S pull request for the target (and recent papers and public archives) when scouting, and again just before the gate. Closed claims are public and count against novelty.
12. This workspace is the humanities and structures lane; a second workspace (~/v3r1t4s) runs the other quarries at the same time. Never attack a quarry marked for the other lane.
11. Press the advantage: when a target proves tractable (a lens reaches progress or a partial-win-level result) and uncrowded (no rival pull requests, no recent paper on the same cells), treat it as a live lead and stay on it, run after run, with every lens the budget allows, until it yields a claim or two consecutive runs make no progress. Speed never loosens verification: the null test, the three skeptics and the gate run in full every time.

## Kill criteria
1. The baseline or the posted value is not reproduced exactly from the sources: stop; nothing above it can be trusted.
2. Any control ties or beats the real result: the lead is dead.
3. The status source shows the record moved out of reach: dead, record moved.
4. The effect depends on a single word type, tablet, fragment or survey: dead.
5. The only evidence is a model's sense that a reading is plausible: not evidence; dead.
6. Two nights on one cell with no new start distribution, symmetry class or hypothesis: rotate quarry.

## Self-critique
Where this charter most likely fools itself: a variable star absent from one index is trivial, since millions of catalogued variables are not yet in it; a find counts only if absent from every catalog the criterion lists, and a failed catalog query is "unknown", never "absent". Packing improvements of 1e-10 live at the edge of the table's rounding; the objective must be recomputed in high precision from the submitted coordinates and non-isometry shown. Accounting closure can be gamed by choosing a numeral system per tablet, so the pre-registration must forbid it. Alignment finds inflate under multiple comparisons; the Bonferroni count must include every fragment and corpus line searched. Two quarries outside the bank (Q5, Q6) rest on records not re-fetched while writing; their first run is a status check. The two table quarries (Q1, Q2) were added for tractability and override the usual ban on generic packing picks; the humanities quarries now lead by the human's choice and need hand work an unattended agent does poorly, so expect many clean negatives there. The wild quarry will almost surely yield only exclusions.

## Method cards used
Drawn at random: brute-scale (brute-scale lens; Q2, Q3), backwards (bookkeeper lens; Q4), oldest-source (archaeologist lens; Q1, Q6). Used by choice: evaluator-first (calibrator lens), solver (market-designer lens; Q5, Q6), obstruction-first (Q8). Quarry numbers refer to v3. Random category seeds: undeciphered-scripts was kept because it fits the card; ml-robustness was set aside because the card holds no fluency there and this machine has no GPU. v1 ordered by feasibility at the human's instruction; v2 puts the humanities quarries first, also at the human's instruction.

## Changelog
- v4 lanes: two parallel workspaces; each sets the other lane's quarries to weight 0. The humanities lane also takes the structure quarries Q9 and Q13.
- v4: kit and bank updated to upstream ab114dc (287 targets, approved by the human). Added Q9 percolation thresholds (5, the human's priority), Q10 lattice-gas exact counts and the kings constant (4), Q11 qutrit EAQECC gaps (4), Q12 complex line packings (3), Q13 burnt pancakes and DNA minimizers (3); none had a V3R1T4S pull request on 2026-10-15. Lowered Q1 eBL to 2 (exhaustive negative over 37,892 fragments; overlap pool structurally weak), Q3 soft tables to 3, Q5 Condorcet to 2. v3.1 kept as charter.v3.1.md.
- v3.1: crowding check of the V3R1T4S pull requests on 2026-10-15: max stable matchings parked (another contributor's claims), soft-table rows already claimed in closed pull requests count as taken; added heuristics 10 (check open and closed pull requests twice) and 11 (stay on a tractable, uncrowded target until it yields or stalls). Approved by the human. v3 kept as charter.v3.md.
- v3: after the first night, Proto-Elamite (37 eligible tablets, held-out split spent, no new data), Linear A morphology (split spent), Greek papyri (criterion pool of 4 records, site behind a challenge) and 4D packings (gains already public) were parked behind data triggers. Untried richer targets moved up: eBL fragments and unidentified overlaps (5), spherical codes and covering designs (4), Linear A KU-RO (3); market-design quarries raised to 3. Approved by the human. v2 kept as charter.v2.md.
- v2: the human said they are much more curious about the accounting tablets, the unplaced fragments and Linear A morphology. Weights: Q3 and Q4 to 5, Q1 and Q2 down to 3, Q5 stays at 3 (the human agreed it is the noisiest of the three: small corpus, statistical outcome). Quarry texts, lenses, heuristics and kill criteria unchanged. v1 is kept as charter.v1.md.
