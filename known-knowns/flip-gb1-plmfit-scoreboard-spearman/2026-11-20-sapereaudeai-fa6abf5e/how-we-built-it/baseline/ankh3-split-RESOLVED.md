# Ankh3's GB1 split, RESOLVED — and a new paper that changes the novelty picture

Main session, 2026-11-20, at the operator's request. Read-only literature work; no outward action.

## The question

`published-values-RESOLVED-by-operator.md` left exactly one obstacle to the full success criterion on
`three_vs_rest`: the ProtEGNN paper's **Table 4b lists Ankh3 (5.7B) at 0.90** under a protocol its Appendix
A.1.2 declares to be *"the standard 3-vs-rest split"*, while run `2026-11-19-2355`'s survey had recorded that
**Ankh3's published GB1 figure, 0.9044, is on the `sampled` split**. Since 0.9044 > our 0.902852, the answer
decided whether the published ceiling is 0.8995 or something above us.

## Answer: `sampled`. Our own survey was right, and the ProtEGNN table miscites it.

Three independent lines agree, and the first is now a direct read rather than an inference.

### 1. Ankh (whose numbers Ankh3 reuses) states its split in its own words

Ankh3's Table 5 marks the Ankh and ESM2 baseline columns with an asterisk and footnotes them:
*"Sourced from the Ankh paper; standard deviation is not provided here as the original publication reported
error bars for these specific entries instead."* The body confirms it: *"The results of the previous Ankh and
ESM2 models were concluded from the original paper (Elnaggar et al., 2023)."* So Ankh3's GB1 task is Ankh's GB1
task.

Read directly from the Ankh paper (bioRxiv `10.1101/2023.01.16.524265v1`, full text, 2026-11-20):

> **"The sampled split was utilized to evaluate the investigated PLMs as it provided the most stable results."**

The same section gives the construction: 149,361 GB1 mutants with measured binding scores, down-sampled to
**8,733** because 96% of the original points were non-binders or poor binders. **8,733 is exactly our row
count**, independently re-derived in this workspace from the released file.

### 2. An independent third party measures Ankh3 on the real `three_vs_rest` and gets 0.814

HyPLM Technical Report (arXiv:2611.12000, Hyra Team / Tencent Hunyuan, 2026-11-09) evaluates 13 encoders on
FLIP GB1 `three-vs-rest` with linear probes on frozen representations, and reports **Ankh3-large at 0.814** —
0.089 below Ankh3's own 0.9030. A model does not lose 0.089 on its own split; it loses it on a harder one.

### 3. FLIP itself says the `sampled` split flatters everyone

FLIP's own framing: *"Sampled: Sequences are randomly partitioned in 80% train and 20% test"*, a split it says
serves mostly for discussion purposes, and on which almost all models perform drastically better than on the
biologically motivated splits. A ~0.90 on `sampled` and a ~0.81 on `three_vs_rest` for the same backbone is the
expected pattern, not an anomaly.

### The coincidence that nearly misled this analysis, recorded so it does not mislead the next reader

Ankh3's baseline column and HyPLM's `three-vs-rest` column happen to sit in overlapping ranges — ESM2-650M at
**82.0** in Ankh3 against **0.801** in HyPLM, which looks like agreement and is not: one is `sampled`, the other
`three_vs_rest`. Mid-analysis this was briefly read as evidence that Ankh3's numbers *were* `three_vs_rest`.
The tell that breaks the coincidence is **ESM2-15B at 57.0** in Ankh3's table, which is nothing like any
`three_vs_rest` figure for that model (PLMFit's scoreboard has it at 0.8791 with adapters). Overlapping ranges
are not split identification; only a stated protocol or a size table is.

## Consequence for the criterion

**The highest published value on `three_vs_rest` is ProtEGNN(t6) = 0.8995 ± 0.0058**, now established at both
ends: the value read from the source, and the one apparent exception positively excluded with its real split
named. Ankh3's 0.9030 / 0.9044 ± 0.0089 belong to a different column of the same benchmark.

**It changes nothing about whether we win.** As predicted before the read:

| our number | margin over 0.8995 | as a fraction of the comparator's own sd | defensible? |
|---|---|---|---|
| 0.900143 (best clean) | +0.000643 | 0.11 | no |
| 0.902852 (A, shape-contaminated) | +0.003352 | 0.58 | no — and our own 95% interval [0.898044, 0.907247] contains 0.8995 |

Run `2026-11-20-0215`'s ~**0.906** threshold stands, unrevised, now resting on a confirmed input.

**What it does buy** is the thing the Gaia run lost: a filing on this cell can now assert the published ceiling
**with a citation chain that survives checking**, including an explicit note that ProtEGNN's Table 4b places a
`sampled`-split number in a `three-vs-rest` table. That is the `PREREG` §10 failure mode closed for this cell.

**Credit where it is due:** run `2026-11-19-2355`'s survey got this right, and attributed it correctly to
"Ankh's own task table". Run `2026-11-20-0535`'s NOVELTY reopened it as an unresolved hole — on top of
fabricating the `ESMc-L` variant. **The survey was more reliable than the skeptic that doubted it**, which is
worth remembering the next time a skeptic reopens a settled item.

## The more important finding: HyPLM, and what it does to our live lead

**arXiv:2611.12000, HyPLM Technical Report, Hyra Team (Tencent Hunyuan), 2026-11-09 — eleven days old.** It was
in nobody's survey. It cuts both ways and the second way matters more.

### It strengthens the novelty case for our method class, considerably

An independent 13-model table on **this exact split**, all with frozen representations and linear probes
(closed-form ridge for regression, layer and regularisation chosen on validation):

| model | `three-vs-rest` | model | `three-vs-rest` |
|---|---|---|---|
| Ankh3-large | **0.814** | DPLM-650M | 0.777 |
| HyPLM-Flash | 0.808 | AMPLIFY-350M | 0.774 |
| ESM-1b | 0.807 | xTrimoPGLM-1B | 0.770 |
| ESM-2 650M | 0.801 | ESM3-open | 0.766 |
| Ankh-base | 0.796 | E1-600M | 0.765 |
| ProtT5-XL | 0.781 | ProtBERT | 0.765 |
| | | ESM C 600M | 0.762 |

**The best of thirteen protein language models reaches 0.814.** Our kernel ridge on the one-hot third-order
expansion of four sites, with **no pretrained model at all**, reaches 0.900143 clean. That is +0.086 over the
best of the thirteen, and it is a far stronger statement of the result than "beats the 0.8791 scoreboard entry".
It also corroborates the published language-model-free floor already on file (FLIP's own one-hot ridge 0.76,
one-hot + GP 0.850, Kermut's baseline GP 0.73–0.77).

### It pre-empts the *observation* behind our selection-criterion lead, though not the remedy

HyPLM's Appendix A excludes GB1 `two-vs-rest` and `three-vs-rest` from its summary statistics and states why:

> **"their validation data come from the training distribution while the test sets are strongly shifted"**
> **"probe selection on them is dominated by noise"**
> **"numerically equivalent runs of the same model differ by up to 0.2"**

That is the premise of our lead 1, **published eleven days before our runs measured it.** So the honest framing
changes:

- **Published:** that random-fold/in-distribution validation is mismatched to these shifted test sets, and that
  model selection on them is noise-dominated.
- **Not published, as far as this check goes:** a **shift-matched selection fold** as a *remedy* — fit on
  `no_mut <= 2`, predict `no_mut == 3`, select on that. HyPLM's response to the problem was to **exclude the
  splits from its summaries**, not to fix the selection rule.

**Any pre-registration of lead 1 must now cite HyPLM and claim only the remedy.** Asserting the observation as
novel would be exactly the error that cost the Gaia run its confirmation.

### And a caution it raises about our own margins

"Numerically equivalent runs differ by up to 0.2" is about **probe-training variance**, not test-set sampling,
so it does not touch our numbers directly: our fit is deterministic given the configuration (seed spread exactly
0, pre-registered as such) and our ±0.0046 is a bootstrap over test sequences, which is the right uncertainty
for a fixed model. But as an independent signal that **small differences on this split carry little meaning**,
it argues harder than anything we produced against chasing the +0.003 that separates our numbers from each
other — and it supports treating the ~0.906 threshold as a floor rather than a target.

## Fetch log

One honest request per resource, no retries after any failure, no challenge bypassed. WebFetch caches a URL for
15 minutes, so repeat prompts against the same URL were served from cache and are not counted as new requests.

| # | URL | status | what it gave |
|---|---|---|---|
| 1 | `arxiv.org/abs/2505.20052` | 200 | Ankh3 title, authors, abstract; GB1 named, no split |
| 2 | `arxiv.org/html/2505.20052v1` | 200 | Table 5 GB1 row and caption; the "Sourced from the Ankh paper" footnote; no split named anywhere |
| 3 | `arxiv.org/html/2301.06568v2` | **404** | nothing; not retried |
| 4 | `arxiv.org/html/2611.12000` | 200 | HyPLM: the 13-model `three-vs-rest` table, Appendix A exclusions, frozen-probe protocol |
| 5 | `ar5iv.labs.arxiv.org/html/2301.06568` | **307** | redirect to arXiv abs; followed as the tool directs, not retried |
| 6 | `arxiv.org/abs/2301.06568` | 200 | Ankh title/authors; no GB1 detail on the abs page |
| 7 | `biorxiv.org/content/10.1101/2023.01.16.524265v1.full` | 200 | **the decisive sentence**: Ankh used the `sampled` split; 149,361 → 8,733 |

Two web searches were also run (Ankh3 GB1 split; Ankh GB1 FLIP split). Search-engine summaries were treated as
pointers only — **every load-bearing quotation above was read from the source document itself**, which is the
standing rule after the `ESMc-L` fabrication.

## Still open on this cell

- **CombinGym's per-split leaderboard** is still unread. It is now the only known novelty hole.
- The **5,765-vs-5,743 test-count discrepancy** in the carried survey is unresolved; neither the ProtEGNN paper
  nor HyPLM states a `three_vs_rest` test count (HyPLM's dataset table gives 381/43/8,309, which are the
  `two_vs_rest` sizes, shared across its three GB1 rows).
