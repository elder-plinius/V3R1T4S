# How we found it

**Contributor text, unverified.** A plain account of the process. Everything load-bearing is in `README.md`
and checkable by `sh verify-it-yourself/run_checks.sh`.

## The brief

DrEval's leave-drug-out setting asks a model to predict how cancer cell lines respond to a compound it has
never seen. The published report is blunt about how that goes: the best of eleven models reaches a
normalized R² of **0.0235**, and most are negative — worse than a baseline that predicts each cell line's
average sensitivity and nothing about the drug at all. DrEval's own supplement says models "fail to capture
even this pronounced signal in mean drug potency".

This target was picked after a previous run on a toy lattice problem ended in a withdrawn claim, when the
user asked directly whether that work was advancing anything. It was not. This one is a real unsolved
problem in cancer pharmacology, and an honest answer either way is worth having.

## First: find out what the metric actually measures

Before building anything, we measured what the benchmark scores. In leave-drug-out the reference baseline
sets an unseen drug's effect to **zero**, so the residual the metric grades is dominated by the held-out
drug's *average potency across cell lines*: **69%** of residual variance, on development data.

That reframed the problem. The benchmark is mostly asking: **from a molecule's structure, how potent is it?**
A model that perfectly predicted cell-line-specific effects and nothing about potency could score at most
about 0.31; a model that predicted only potency could reach 0.69.

The literature search afterwards found this point is already in print — DrEval's own supplement and a 2026
preprint both say it qualitatively. So the measurement motivated the method; it is not a discovery, and the
write-ups say so.

## What failed

**Structure alone, from inside the benchmark.** Kernel ridge regression on Morgan fingerprints over the
~420 training drugs reaches +0.073 on development data, which looked like a 3× improvement — until it was
broken down. On single agents alone it was +0.017, and its potency correlation on drugs with no close
analogue in training was **0.14**. The apparent gain lived in drug combinations (whose single-agent
components sit in training) and in close analogues. That is exactly the pitfall the target warns about, and
it is not a defensible result.

**Physicochemical descriptors.** Twelve RDKit descriptors in an RBF kernel: the inner cross-validation gave
them **zero** weight. Dead.

**Mechanism similarity alone.** A target-pathway Jaccard kernel helped, but modestly: +0.073 → +0.096, and
novel-scaffold potency correlation 0.14 → 0.22.

## What worked

**Learn potency somewhere else.** ~420 compounds is far too few to learn structure-to-potency. The public
NCI-60 screen has about 55,000. We trained a small network on **53,486 NCI-60 compounds** to predict
panel-mean log10 GI50 from fingerprints, then fed its prediction into the benchmark model as one extra
similarity channel. Development result: +0.096 → **+0.163**, and novel-scaffold potency correlation
0.22 → **0.45**.

The idea is not ours: Lavelle et al. (2026) raised drug-blind global R² from 0.03 to 0.22 by adding NCI-60
compounds to training. What we added is doing it under an exclusion rule strict enough to be checkable.

## The part we got wrong, and how it was caught

The first exclusion rule removed any NCI-60 compound sharing a PubChem CID with a CTRPv2 drug, or within
Tanimoto 0.85 of one. A leak audit — stripping salts and comparing InChIKey skeletons — found **three CTRPv2
compounds still inside the prior's training data**, as salt forms: counter-ions add fingerprint bits and
push a salt below 0.85.

So the rule was rewritten before any result under it was scored: salt-stripped skeleton match **or**
Tanimoto ≥ 0.60, removing 474 compounds. And because the point of the audit is honesty about how much of
the prior's power is analogue knowledge rather than transfer, the result is reported at four thresholds:

| exclusion | development normalized R² |
|---|---:|
| 0.85 (the original, leaky rule) | +0.227 |
| 0.70 | +0.172 |
| **0.60 (frozen)** | **+0.163** |
| 0.50 (strictest) | +0.123 |

It is monotone. Part of the gain *is* analogue knowledge. A substantial part survives at the strictest
setting, where no training compound is within Tanimoto 0.50 of any benchmark drug.

## Two defects found in the benchmark's own tooling

**The split seed does nothing in leave-drug-out.** The pre-registration required a repeat on a second split
generation. Generating one with a different seed produced per-split numbers suspiciously close to the
first — and the test drug sets turned out to be **identical in all ten folds**. The package shuffles rows
with the seed and then calls `GroupKFold`, whose fold assignment ignores row order. Anyone asking for a
second leave-drug-out generation this way gets the same held-out drugs. We built a genuinely independent
generation instead and accepted it only after a pre-committed independence check.

**The normalized metric double-counts duplicated pairs.** The ruler is attached by a key merge, and CTRPv2
has 4,118 duplicated (cell line, drug) keys, so 235,974 predictions become 245,122 scored rows. The effect
is small (+0.2249 versus +0.2244 row-aligned) and both numbers are reported.

## What a reviewer pushed back on, and we agreed with

An independent novelty review passed the number but objected to the framing, and the objections are right:

- **"Ten times the published best" is a misleading way to say it.** The DrEval paper's own LDO Friedman test
  over all 11 models gives **p = 0.742**: none of those models differs significantly from any other, naive
  baselines included. A ratio against a maximum over statistically indistinguishable near-zero values
  carries no effect-size meaning. The absolute value, the across-split spread, and the margin over our own
  same-splits re-runs are the defensible statements.
- **The comparison is not like-for-like on training data.** Every leaderboard model learns from CTRPv2's 545
  compounds; this method adds ~53,500 external ones. The finding is that the **training distribution was the
  binding constraint** — not that the modelling is better on the same data.
- **The frontier was uncontested, not hard-won.** The page has been frozen for a year, the authors dropped
  LDO from their October 2026 leaderboard, and none of the 27 newer algorithms there has been run in LDO.
- **The credit belongs upstream.** Lavelle et al. (arXiv:2608.11444) published the NCI-60 idea; NCI-60
  potency QSAR is an established field. Our addition is the exclusion rule and its sensitivity curve. That
  citation was originally only in this file — the one marked "contributor text, unverified" — and has been
  carried into the load-bearing documents.

## What we think this is worth

On the benchmark's own terms the number is about ten times the published best, it survives an independent
split generation, 400 permutation controls, and a vault of drugs never looked at during development.

But the benchmark measures something narrower than its name suggests. Most of what it scores is a
compound's average potency, we measured that **26.5%** of that potency variance tracks the maximum
concentration the experimenters chose to test, and the cell-line-specific part — which is what
"personalised response" would actually mean — is untouched by this model, which predicts a single number
per drug. The honest summary is that transfer from a large public cytotoxicity screen largely solves the
unseen-drug problem **as this benchmark defines it**, and leaves the harder half open.
