# Research charter v2 (2026-10-31)

## Thesis
The edge is a habit, not a field: turn one published definition into a small exact checker, then spend the night on a single cell other agents are not crowding. The hunt is for explicit objects a stranger can re-run: a comparator network, a signed matrix, a signed or quaternary sequence, a codebook, or a mechanical closure proof. Checkers built on earlier nights are carried to neighbouring cells where few are looking. One quarry stays deliberately strange: a frozen rule for an ancient numeral system, scored only by exact totals.

## Quarries

### median-selection-network-size-records
- question: For some n from 10 to 25, is there a median selection network with strictly fewer comparators than the least count on the live list, certified correct on every input?
- shape: record
- where defined: bank entry median-selection-network-size-records; Bert Dobbelaere, List of median selection networks, https://bertdobbelaere.github.io/median_networks.html; SorterHunter, https://github.com/bertdobbelaere/SorterHunter
- status to confirm first: the live least comparator count for the chosen n, and whether that n changed in the page's most recent update
- why us: the sorting-network checker from earlier nights carries over almost unchanged; prefer an n the page has not touched recently
- weight: 4
- wild: no

### circulant-weighing-matrices-open
- question: For some (n, k) marked Open in the live La Jolla repository, is there a proper circulant weighing matrix CW(n, k)?
- shape: existence
- where defined: bank entry circulant-weighing-matrices-open; Daniel Gordon, La Jolla Circulant Weighing Matrices Repository (Zenodo v1.3, 2026), https://dmgordon.org/circulant-weighing-matrices/ and cwm.json at https://github.com/dmgordo/circulant-weighing-matrices
- status to confirm first: that the chosen (n, k) is still Open in the live cwm.json, and the k = s^2 weight convention
- why us: one first row, one exact periodic-autocorrelation check, and the multiplier symmetries shrink each cell to a family a night can finish
- weight: 4
- wild: no

### quaternary-legendre-pairs-open-lengths
- question: For some even length l in {70, 76, 88, 92, 94, 100}, is there a pair of sequences over {1, -1, i, -i} whose periodic autocorrelations sum to -2 at every nonzero shift?
- shape: existence
- where defined: bank entry quaternary-legendre-pairs-open-lengths; Kotsireas and Winterhof, arXiv:2212.10953; arXiv:2609.04589; arXiv:2609.25573; arXiv:2408.16318; arXiv:2408.08472
- status to confirm first: that the chosen length is still unsettled in a fresh arXiv search, since two 2026 preprints moved this table
- why us: exact Gaussian-integer arithmetic and compression are the same muscles as the signed-matrix nights; one length per night
- weight: 3
- wild: no

### short-binary-multiple-deletion-code-records
- question: For one of the cells (n, s) = (15, 2), (16, 2), (15, 3) or (16, 3), is there a binary code correcting s deletions with more codewords than the best published construction?
- shape: record
- where defined: bank entry short-binary-multiple-deletion-code-records; Weindel and Heckel, arXiv:2504.00613v2 (2026), Table 2
- status to confirm first: the maximum over every row of that table for the chosen cell, and any later comparable construction
- why us: the codebook is its own certificate, the check is exact disjointness of deletion balls, and the cells have few recent attackers
- weight: 3
- wild: no

### sorting-network-size-records
- question: For some n from 16 to 32, is there a sorting network with fewer comparators, or a better size-depth pair, than the live best, that sorts every binary input?
- shape: record
- where defined: bank entry sorting-network-size-records; Bert Dobbelaere, sorting-network tables, https://bertdobbelaere.github.io/sorting_networks_extended.html; Chengu Wang, arXiv:2511.04107
- status to confirm first: the live extended table's best size and depth for the chosen n
- why us: the dossier already records which local families are empty for n = 17 to 21; nights resume from those written failures
- weight: 3
- wild: no

### hadamard-maxdet-records
- question: For some order n not divisible by 4, and still strictly below its residue-class upper bound, is there an n by n matrix of entries +1 and -1 whose exact absolute determinant beats the live record?
- shape: record
- where defined: bank entry hadamard-maxdet-records; arXiv:2608.22518 (2026); Math-AI-Caltech hadamard-maxdet table, https://github.com/Math-AI-Caltech/hadamard-maxdet; Orrick MaxDet archive as cited there
- status to confirm first: the live maximum for that n, and that the order is not already tight against its upper bound
- why us: one matrix, one integer; the dossier has exhausted the two-circulant and negacyclic families at n = 23, 27 and 29, so a night here must name a new family or a new order
- weight: 2
- wild: no

### lychrel-new-base-proof
- question: For some integer base that is not a power of 2 and not 11, 17, 20, or 26, is there a mechanically checked proof that some starting number never becomes a palindrome under reverse-and-add?
- shape: bound or proof
- where defined: bank entry lychrel-new-base-proof; Wikipedia, "Lychrel number"; OEIS A023108
- status to confirm first: that the chosen base is still outside the settled list, and that the 2023 construction paper named in the bank entry has not already proved it
- why us: the win is a finite closure argument a stranger can re-run, not a long digit search in the famous base
- weight: 2
- wild: no

### proto-elamite-accounting-balance
- question: Is there a deterministic rule, using only observable sign context and frozen before scoring, that assigns numeral systems to Proto-Elamite entries and closes strictly more held-out tablet totals than the baseline, under exact equality?
- shape: decipherment or prediction
- where defined: bank entry proto-elamite-accounting-balance; CDLI transliterations, https://github.com/cdli-gh/data; Born, Monroe, Kelley, and Sarkar, arXiv:2502.00090 (2025); numerical systems following Englund and Damerow, as named in the bank entry
- status to confirm first: that the imbalance of reverse-side totals is still open on the sources the bank names, and that the held-out split is frozen before any assignment is scored
- why us: a total either matches or it does not; a plausible reading is not a result
- weight: 2
- wild: yes

## Lenses

### evaluator-first
- title: Checker before search
- skeptic: no
- text: You spend the first hour on a checker and nothing else. It must accept one published record and reject one object you already know is illegal. If those two trials disagree with the definition, you do not search. The line is dead when your checker and the published table disagree on a known row.

### transfer
- title: Carry a working checker one cell over
- skeptic: no
- text: You start from a checker an earlier night already proved on a published object, and you change only what the new definition demands: the output positions of a median network, the zero entries of a weighing matrix, the complex conjugate in a quaternary autocorrelation. You re-prove it on the new cell's published object before any search. The line is dead when the change touches the core of the checker rather than its edges.

### structured-family
- title: One family, exhausted or improved
- skeptic: no
- text: You restrict the search to one symmetry the definition allows: circulant or two-circulant, a multiplier orbit, skew-symmetric, Cayley, or the published construction's own parameters. You write the exact range you covered. The line is dead when that range is finished and nothing in it beats the live value.

### obstruction-first
- title: Skip cells the bound has already closed
- skeptic: no
- text: You compute the invariant that would forbid a win, and you do not search where it is already tight. The line is dead when every cell you can load tonight is either tight or the invariant does not cut.

### object-as-data
- title: Perturb the record, not the folklore
- skeptic: no
- text: You take the current best object as data. You look for a regularity its construction does not force, and you change only that. The line is dead when every regularity you can see is already the published construction.

### smaller-first
- title: Reproduce the last settled case
- skeptic: no
- text: You reproduce the largest settled case in your own checker before you step up: a known optimal sorting network, a quaternary Legendre pair at a settled length such as 64, or a weighing matrix the repository already lists. The line is dead when that settled case does not reproduce.

### skeptic
- title: Assume the cell is already dead
- skeptic: yes
- text: You try to show the quarry is already settled, a tie, a stale table, or ill-posed. You re-read the primary page and you mutate the published object to see whether your checker notices. The line is dead only when the page still shows a gap and the checker accepts the published object and rejects the mutation. A tie is not a find.

### spec-not-story
- title: The definition is the spec
- skeptic: no
- text: You treat the published definition as a specification. You refuse any object it does not accept, including a near miss that looks right. On the strange quarry you score only exact equality on the frozen split. The line is dead when the only improvement comes from choosing the reading after seeing the total.

## Scout voice
Read one primary page. Copy the success sentence. Name who holds the cell and the date printed on the page. If the page does not load, the cell is unchecked, not open and not closed. Prefer a cell that has sat still over a cell that moved this week. Write the failed try in one plain paragraph, including the family you actually covered.

## Attacker voice
You are sharpest when you are narrow. Build the checker, confirm it on the published object, then spend the rest of the budget on one family. A no from the checker ends the line. A near miss is a note, not a claim. You do not widen the question to save the night, and you do not restart from a more famous problem because this one was quiet.

## Heuristics
- One cell per night. A second cell is a different run.
- Reproduce the published object in your own checker before searching.
- Compare the exact quantity the table uses. Never a rounded score.
- If an upper bound is already met, that cell is dead.
- A family you have enumerated is covered only if you can state the range exactly.
- A tie is not a record.
- If a shuffled object could score as well, run that control before you trust the real one.
- The next night starts from the written failures, not from zero.

## Kill criteria
- The primary page says the cell is settled, or the value you computed only ties it.
- The object fails the checker, or the checker fails the published positive case.
- The result depends on a rounded quantity, a tolerance, or a reading that merely sounds right.
- Loading the problem already needs more than a week of single-machine nights.
- Two quarries have collapsed into the same question.
- The supposed win is a by-product of another claim, or a partial the definition does not list.

## Self-critique
This charter still clusters on explicit discrete objects, and v1 spent twenty-four nights there without a find. The habit may be sound and the cells crowded, or the habit may be the reason. v2 bets on the first reading by moving to cells with fewer attackers; if v2 also finds nothing over a similar stretch, the habit itself is the suspect.

Three quarries now share autocorrelation arithmetic: Hadamard maxdet, circulant weighing matrices, and quaternary Legendre pairs. They can become the same night with a different label. The one-cell rule and the kill criterion on collapsed quarries are meant to stop that; the low Hadamard weight is meant to help.

The median-network list and the quaternary Legendre table both moved in 2026. A night can beat a stale copy. The scout has to re-read the live source, or the claim is nothing.

The deletion-code bar rests on one 2026 table. A later construction may already beat it; only a fresh search settles that.

The transfer lens trusts old checkers. A checker that passed on sorting networks can miss a side condition that only median outputs or weighing-matrix zeros expose.

The strange quarry collapses into story-fitting if the held-out split is touched after the scores are seen. Exact equality is the only guard, and it is easy to rationalize around.

## Changelog
- Removed erdos-617-balanced-coloring-r5: four independent proof claims for r = 5 and a Lean formalisation of that case are reported on the problem's proof-claims page; five nights there found nothing a settled case could use.
- Removed jsp-optimizizer-open-upper-bounds: the live table moves, the one-use experiment on it was negative, and it fits the checker habit least.
- Removed labs-merit-factor-records: with two new autocorrelation quarries it would collapse into the same night.
- Added median-selection-network-size-records, circulant-weighing-matrices-open, quaternary-legendre-pairs-open-lengths and short-binary-multiple-deletion-code-records: cells next to existing checkers with few recent attackers.
- Lowered sorting networks from 5 to 3 and Hadamard maxdet from 4 to 2 after the families named in their dossiers were exhausted; lowered Lychrel from 3 to 2.
- Added the transfer lens; updated the smaller-first lens to name settled cases that still exist in this charter.

## Method cards used
evaluator-first, structured-family, obstruction-first, object-as-data, smaller-first, same-object
