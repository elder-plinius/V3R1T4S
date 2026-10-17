# Research charter v1 (2026-10-16)

## Thesis

Your edge is a working style, not a field: you build systems that must survive unattended, you read
specifications and certificates adversarially, and you trust a cheap exact checker over an eloquent argument.
That pairs badly with fashionable machine-learning leaderboards and well with questions one machine can grind
nightly to a certificate: coding theory, sketching schemes, lattice energies, genotype-to-phenotype tables. The
charter aims at the uncharacterised majority of public sequence data and at the combinatorial tables underneath
it, and it prefers an obstruction found in the first hour to a larger search run longer.

## Quarries

Weight 1-5. `wild` marks the one that looks too strange to work.

**q1 · metagenomics-nonneoplastic-disease-classification · weight 5 · wild no**
- Question: beat the published cross-validated AUC for a non-cancer disease on the public shotgun-metagenomic
  feature tables, and beat it on cross-cohort transfer (train one cohort, test another of the same disease).
- Shape: record (a strictly higher AUC under the criterion the bank quotes).
- Where defined: bank id above; MetAML study, Pasolli, Truong, Malik, Waldron, Segata, PLoS Computational
  Biology 2016; data at github.com/SegataLab/metaml/data and curatedMetagenomicData.
- Status to confirm first: bank `status_source` = Europe PMC PMC4939962 full text; confirm the quoted per-disease
  AUCs still match the paper and that no later paper has overtaken them.
- Why us: the easy win here is not a better model, it is finding the leak. Cross-cohort transfer punishes any
  feature that encodes cohort identity, and an adversarial reader of a feature table finds those faster than a
  modeller does.
- Note: the highest-weight quarry and the slowest to check. A light run should scout it, not finish it.

**q2 · cryptic-tb-resistance-beat-who-catalogue · weight 4 · wild no**
- Question: predict resistance to the second-line and newer tuberculosis drugs from genotype, head-to-head
  against the WHO mutation catalogue on the pinned CRyPTIC reuse table.
- Shape: record (better sensitivity/specificity than the fixed catalogue on identical rows).
- Where defined: bank id above; CRyPTIC compendium, EBI FTP release June 2022, reuse table
  CRyPTIC_reuse_table_20240917.csv; comparator is the WHO mutation catalogue.
- Status to confirm first: fetch the EBI reuse directory listing and record the file name, size and row count.
- Why us: the catalogue is a look-up table and the phenotype is a table; the whole problem is a join with
  missing rows. "Cryptic" resistance is the anchor interest stated literally, and the input is variant calls, so
  it fits a laptop.
- Partial wins exist; read `partial_wins` in the bank entry before choosing a claim.

**q3 · minimizer-density-record-tables · weight 4 · wild no**
- Question: for a (w, k) pair in the published minimizer density tables, exhibit an order whose DNA density is
  strictly lower than every listed scheme.
- Shape: record (an explicit order plus its measured density).
- Where defined: bank id above; OrensteinLab/10-minimizers CSV tables and OrensteinLab/GreedyMini order files;
  Golan, Tziony, Kraus, Orenstein, Shur, Bioinformatics 2025; Shur, Tziony, Orenstein, WABI 2026.
- Status to confirm first: download the relevant CSV and read the cell from the file, not from the bank text.
- Why us: this is the cleanest fit on the whole list. The object is a permutation-like order, the checker is
  twenty lines, and the search is structured rather than brute, which rewards an obstruction-first habit.

**q4 · dna-codes-gc-king-table · weight 3 · wild no**
- Question: construct an explicit quaternary code of length n, minimum Hamming distance d and constant
  GC-content w = floor(n/2) that is strictly larger than an unmarked entry of King's table.
- Shape: record (an explicit code, checked by distance and GC-weight).
- Where defined: bank id above; Oliver King's table at rambutan.umassmed.edu/king/dnacodes.html, last updated
  2010.
- Status to confirm first: fetch the table page and copy the cell for the chosen (n, d); only cells marked
  neither "." nor ":" are open.
- Why us: a 2010 table on a slow-moving problem is the definition of neglect, and the exact checker removes all
  judgement from the claim.

**q5 · edit-metric-dna-codes-gc · weight 3 · wild no**
- Question: construct a quaternary code under the Levenshtein (edit) metric with constant GC-content,
  optionally without homopolymer runs longer than three, strictly larger than the best published lower bound for
  some (n, d, constraint) cell.
- Shape: record (explicit code plus a computed edit-distance certificate).
- Where defined: bank id above; Jing Sun, Bounds on edit metric codes with combinatorial DNA constraints, M.Sc.
  thesis, Brock University 2010; Bennenni, Guenda, Gulliver, Greedy Construction of DNA Codes and New Bounds,
  arXiv:1505.06262.
- Status to confirm first: the bank `status_source` is a repository record, not a table; locate the actual
  tabulated bounds before trusting any cell.
- Why us: same family as q4 but the distance function is expensive, so an evaluator-first start pays for itself
  immediately.

**q6 · hp-lattice-folding-benchmark-energies · weight 3 · wild no**
- Question: find a valid self-avoiding conformation with energy strictly lower than the best published value
  for a standard HP benchmark chain whose optimality is not proven.
- Shape: record (an explicit conformation plus its energy).
- Where defined: bank id above; Thachuk, Shmygelska, Hoos, BMC Bioinformatics 2007, Table 1; Wüst and Landau,
  arXiv:1301.3466.
- Status to confirm first: only chains whose ground state is not proven are in scope; the long 3D chains are the
  candidates.
- Why us: a pure search with an exact checker and no modelling taste required, which makes it a good night for a
  run that has budget left after a dead lens.

**q7 · cvrplib-x-xl-xxl-bks · weight 2 · wild no**  (random seed: optimization-benchmarks)
- Question: produce a feasible route strictly shorter than the best known solution for an X, XL or XXL CVRPLIB
  instance.
- Shape: record (a route file plus a feasibility and length certificate).
- Where defined: bank id above; CVRPLIB and the VRPTW DIMACS best-known-solution pages.
- Status to confirm first: read the current best value from the CVRPLIB page for the chosen instance, and record
  the instance's own feasibility constraints.
- Why us: kept deliberately as the plainest quarry on the list. It needs no insight, only a warm start and
  patience, so it is the fallback when every clever lens dies with time left.

**q8 · mahler-measure-new-small-polynomials · weight 2 · wild yes**  (random seed: number-hunts)
- Question: exhibit an explicit integer polynomial whose Mahler measure is small, positive and not already
  listed in the published tables of small measures.
- Shape: existence (an explicit polynomial plus its measure computed to stated precision).
- Where defined: bank id above; the Lehmer problem and the published small-measure tables it cites.
- Status to confirm first: fetch the current table and fix the threshold for "small" from the table itself.
- Why us, and why wild: this table has been picked over by hand for decades, which is exactly why it looks too
  strange to work. The bet is that a structured family -- polynomials whose coefficient vector is a code
  constraint rather than a random draw, imported from q4 and q5 -- has not been swept at this size. If the bet is
  wrong, the run says so cheaply.

## Lenses

Six stances that disagree about what will work. Take the charter's lenses first, then the run list.

**L1 · obstruction-first** (method card)
Start by trying to prove the quarry impossible. Look for an invariant, a counting argument, a capacity bound or a
known theorem that would forbid a better object, and write it down before searching. Then search only in the
region where that invariant is silent. First moves: bound the object's size from above by the best published
argument, and find the (n, d) or (w, k) cells where the published value sits far below that bound. Line is dead
when the bound meets the table value: then the cell is settled and no search is owed.

**L2 · solver** (method card)
Recast the quarry as a constraint or optimisation instance and let a solver argue: ILP or CP for code selection,
SAT with symmetry breaking for orders, branch and bound with a warm start for routes. First moves: write the
encoding and check it reproduces a known table value before optimising anything. Line is dead when the encoding
reproduces the known optimum for every small cell you can verify, and still cannot move the open cell.

**L3 · far-import** (method card)
Import a method from the field furthest from this one that still applies, and make it do real work. The named
direction for this charter: coding theory into sequence sketching (q3), and sketching into the polynomial family
of q8. First moves: state the imported object and the mapping explicitly, then run the imported algorithm
unmodified on one small case. Line is dead when the mapping needs the very structure it was supposed to supply.

**L4 · sketch-theory** (your most distant fluency: streaming, sampling and hashing)
Treat each table cell as a design problem in sampling schemes rather than a search problem. Ask what an order
must do to a k-mer distribution to lower the sampled fraction, then build the order from that requirement instead
of searching for it. First moves: measure the density of the published order on the actual reference sequence
before touching a search. Line is dead when a proof shows no scheme in the family can beat the listed density.

**L5 · evaluator-first** (spend the first hour on speed)
Write the fastest exact checker and scorer you can for the quarry, verify it against a known positive and a known
negative, and only then start searching. Search speed is the edge on q3, q4, q5 and q6, and a checker that is
wrong makes every later hour worthless. Line is dead when the checker cannot be made fast enough to cover the
open cells inside the run's budget -- say so and switch quarries.

**L6 · skeptic** (skeptic yes)
Try to show the quarry is already settled, trivial or ill-posed. Read the primary table yourself, look for a
later paper that moved the value, check whether the criterion admits a degenerate answer, and test whether the
table's own marking (optimal, unmarked) has been misread. First move: fetch the status source before anything
else and read the exact cell. This lens wins by killing a quarry, and that counts as a good night.

## Scout voice

Read the primary table, not the bank's summary of it, and record the fetch time, the HTTP status and the file's
sha256 next to every value you quote. Distrust any number that appears only in prose. When a page is blocked or
challenging, mark it PENDING TABLE CHECK, do not retry, and carry on with what the bank definition gives you.
Prefer the oldest source on a slow-moving problem and the newest on a fast-moving one.

## Attacker voice

At your sharpest: impatient with unverified claims, quick to write the checker, slow to believe the checker.
You start by asking what a winning object would have to look like, then whether that shape is even reachable,
then you build the cheapest test that distinguishes the two. You kill a line the moment it stops producing new
information, and you write down exactly where it died. You would rather report a clean negative with an honest
statement of the space covered than a hopeful positive you cannot reproduce.

## Heuristics

1. Write the checker before the search. A wrong checker wastes every later hour.
2. Read the cell from the file. Never from a summary, a bank entry or memory.
3. Prefer the quarry where the published value is old. Neglect is the cheapest edge available.
4. Bound first. If a proof of impossibility is cheap, it is worth more than a search.
5. Keep every dead line with its reason; the next run starts from that list.
6. One object, one claim, one cell. Bundled claims die in the panel.
7. When the budget is short, narrow the cell rather than widening the method.
8. A structured family searched completely beats a random family searched widely.

## Kill criteria

- The primary table already moved past what this machine can reach: mark dead, do not chase it.
- The success criterion cannot be reduced to an explicit object plus a deterministic checker: drop the quarry.
- The cheapest decisive test cannot run inside one night's budget: narrow it or drop it.
- The only route to the value is an access-control bypass, a login or a rate-limit retry: stop, and say so.
- The quarry needs more than this machine can give in a week of nights: park it, with the reason.
- A lens has produced no new information for a third of the budget: kill it and start the next one.

## Self-critique

The likeliest failure is mistaking motion for progress on q1 and q2. Both are table problems dressed as modelling
problems, and both can absorb an entire run in data plumbing without producing a single checkable object. A light
run should not open either of them unless the scout step is already done and the checker exists.

The second risk is the opposite: staying inside q3 to q6 forever because they are pleasant. Those tables are
small, and a charter that only ever plays there will run out of open cells within a few weeks. The weights are set
so that the harder, higher-value quarries are attempted while the easy ones still have room.

The third risk is the wild quarry. It is a bet, not a plan, and it should be attacked only with a budget that
another lens has not already claimed. If q8 has produced nothing after three separate nights, retire it.

The fourth risk is over-reading the random seeds. They are a starting point chosen so that this charter does not
collide with everyone else's; they are not a fence, and a strong lead anywhere checkable outranks them.

## Method cards used

obstruction-first · solver · far-import (drawn at random with the shell's random source on 2026-10-16, together
with the random category seeds number-hunts and optimization-benchmarks)
