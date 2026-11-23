# NOVELTY skeptic verdict - flip-gb1-plmfit-scoreboard-spearman (run 2026-11-20-0535)

context: subagent

skeptic: NOVELTY. Fresh context. I read only the claim bundle, the read-only repo checkout, and the public
sources listed at the bottom. I took no outward action: no issues, comments, PRs, posts, emails, logins or
sign-ups. One plain request per object, User-Agent naming V3R1T4S, no retry after any failure.

---

## 1. The live bar

Fetched once, honestly:

- `https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/README.md`, 2026-11-20T05:47:43Z, **HTTP 200**,
  14,780 bytes, sha256 `51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b`.
- Line 209 verbatim: `| GB1 - three-vs-rest | 0.8791 | Spearman's | ProGen2-M | Adapters | 50% | CLS | Linear |`
- Line 210 verbatim: `| GB1 - one-vs-rest | 0.4571 | Spearman's | ProGen2-S | FE | 75% | Mean | Linear |`

**The live three-vs-rest bar is 0.8791.** My copy is byte-identical (same sha256) to the bundle's
`status/plmfit_README_2026-11-20-0535_preclaim.md`, so the claim's status quote is accurate and the bar has not
moved between 05:42:28Z and 05:47:43Z.

I also checked that the scoreboard has no newer home that the README's tree could lag: the plmfit releases
endpoint (`gh api repos/LSSI-ETH/plmfit/releases`, 2026-11-20T05:53:18Z, HTTP 200) returns an **empty list**.
There are no release assets, so the README on `main` is the whole scoreboard. No scoreboard entry exists for
`two_vs_rest` or `low_vs_high`.

## 2. The highest published value for this exact split

I searched the last 24 months of literature and code independently and then checked the earlier runs' record in
`the-earlier-runs/related_work.md` against sources. My findings:

| Spearman | model | source | is it this 5,743-row split? |
|---|---|---|---|
| **0.90** (text), reported as 0.8995 +- 0.0058 in the earlier survey | ProtEGNN(t6) and ProtEGNN(ESMc-L) | bioRxiv 2026.05.28.728196, "Just Add Structure", Sec. 2.3.2 and Table 4 | yes, FLIP GB1 three-vs-rest |
| 0.893 +- 0.0048 (best seed 0.8980) | ESM2-3B + LoRA | Schmirler et al., Nat Commun 15:7407 (2024) | yes (their Table 2 gives 5,743) |
| 0.888 | Ankh-large + LoRA | same | yes |
| 0.880 +- 0.003 | Bradley-Terry CNN | Brookes et al., NeurIPS 2024 | yes |
| 0.8791 | ProGen2-M + adapters | PLMFit scoreboard / paper Table 2 | the paper states 2,968/5,765, not 5,743 |
| 0.850 | ESM2 48-layer embeddings | arXiv 2501.18223, Table 6 | yes |
| 0.83 (CNN), **0.76 (ridge, one-hot)** | FLIP's own baselines | FLIP 2021, NeurIPS D&B Table 4 | yes |

**I verified the ProtEGNN value exists and is for this split**, from the paper's own text: *"Both ProtEGNN(t6)
and ProtEGNN(ESMc-L) reach an SPR of 0.90, matching the best-performing 5.7B parameter Ankh3 model."* I could
**not** independently read its exact decimals: the bioRxiv PDF came back as a Flate-compressed byte stream, the
HTML full text renders the table cells as placeholders, and both OpenReview URLs returned a browser-verification
challenge page which I did **not** bypass and did not retry. So `0.8995 +- 0.0058` rests on the earlier survey's
reading, which I confirm is consistent with the paper's own prose but have not re-verified digit by digit.

**Two things I found that the earlier survey did not state, and that matter:**

1. The paper names **two** models at "an SPR of 0.90" on this split: ProtEGNN(t6) **and ProtEGNN(ESMc-L)**. The
   earlier survey's table lists ProtEGNN(t6) at 0.8995 and an *ESMc-M* variant at 0.8954, and says nothing about
   **ESMc-L**. An ESMc-L value anywhere in [0.895, 0.905) is consistent with "0.90", so the published maximum for
   this split could be above 0.902852 and I cannot rule that out. This is an open hole, not a resolved
   comparison.
2. PLMFit's own paper has a second GB1 three-vs-rest number I checked directly: **Table 3** prints "0.9" for
   ESM2-15B with LoRA, LoRA- and Adapters (and "0.8" for Adapters-), to **one decimal place and with no metric
   named**. 0.8791 rounds to 0.9, so this is consistent with the scoreboard and is **not** a separate higher
   published value. Any claim that PLMFit itself published 0.9 at four decimals would be wrong.

**Numbers I checked and ruled out as non-comparable** (each is a different split or a different quantity, so
none is a bar):

- **Ankh / Ankh3 GB1 numbers, including Ankh3's 0.9044, are on the `sampled` split** (Ankh's own task table:
  8,733 total, 6,291/670/1,772 train/valid/test; 1,772 is the `sampled` test size), which FLIP marks orange and
  forbids for comparisons. I confirmed this independently. ProtEGNN's claim of "matching Ankh3" on GB1 is
  therefore a cross-split comparison and should not be read as a three-vs-rest bar.
- **arXiv 2501.18223's 0.905 is a *train*-set rho** (ESM2, 33 layers); its test rho on this split is 0.840. A
  train-set correlation is not a bar.
- FLIP2 / FLIPv2 (bioRxiv 2026.02.23.707496) adds no GB1 rows; GB1 appears only as "Legacy FLIP". Values near
  0.90 in FLIP2 tables are **NDCG**, not Spearman (e.g. ridge one-hot Spearman 0.430 / NDCG 0.903) - a real trap
  for this cell, and the claim does not fall into it.
- HyPLM (arXiv 2611.12000) reports 0.762-0.814 on this split, and itself warns that on this split "numerically
  equivalent runs can differ by up to 0.2" because validation comes from the training distribution while the
  test set is strongly shifted. That is an independent published caution about reading small margins on this
  cell as real.
- muFormer (bioRxiv 2023.11.16.565910) remains unread (the earlier survey hit HTTP 429 and did not retry; I did
  not re-request it). Its GB1 per-split numbers appear to live in a bar chart. Recorded as unread.

**Conclusion on 2:** the highest value I can confirm as published for this exact split is **0.90 (ProtEGNN,
bioRxiv 2026.05.28.728196)**, read as 0.8995 +- 0.0058 by the earlier survey and not independently verified to
four decimals, with the ProtEGNN(ESMc-L) row unread and possibly higher. I found **nothing published above
0.902852** on this split in the last 24 months, but I cannot assert the converse either.

## 3. Is the method class already published? - the key question, and the clearest finding

**No.** Every published one-hot / non-PLM number I can find on this split is far below 0.90:

- **FLIP's own one-hot ridge on three-vs-rest is 0.76** (NeurIPS D&B 2021, Table 4) - additive one-hot only,
  80 features for the four sites.
- one-hot + GP: 0.850 (Greenman et al., bioRxiv 2023.04.17.536962).
- Kermut's baseline GP: 0.73-0.77 (NeurIPS 2024, Table H.1). Kermut's authors explicitly attribute their poor
  showing to GB1 having "only four highly epistatic mutated positions" that their structural kernel cannot
  exploit - i.e. the published record says the epistatic structure of these four sites is the thing nobody's
  non-PLM kernel was capturing.
- A public repository (`saanviiyer/leeway`) reports a one-hot ridge **floor of 0.7528** on this split and flags
  the gap to a "published 0.90" as something "nobody reports". That is an independent third party noting the
  very absence this claim fills.

I searched specifically for a published Potts-style, Walsh-Hadamard, or second/third-order one-hot interaction
regression scored by **Spearman on FLIP GB1 three-vs-rest** and found none. The nearest candidates are not it:
Zhou/Wu/McCandlish (PNAS 2022) do variance-component GP regression on the Wu landscape but with **randomly**
held-out data, not the order-based FLIP split; "Beyond Tokens" (arXiv 2608.24953, Aug 2026) fits ridge and MLPs
with Walsh diagnostics on GB1 but reports **R-squared on the 2-vs-rest setting** and no Spearman and no
three-vs-rest; GraphFLA (arXiv 2510.24826) characterises landscapes rather than scoring this split.

So: **a PLM-free one-hot third-order interaction kernel ridge reaching ~0.90 on this split is not published
anywhere I can find.** That is the genuine novelty in this bundle, and it is a real gap in the literature:
+0.14 Spearman over FLIP's own published one-hot ridge, from a model with no pretrained protein language model,
2,990 training rows and a single Cholesky solve. It is also not reachable by any of the trivial edits my
instruction lists (deletion, restriction, a propagation rule, relabelling, symmetry, numerical polish) applied
to FLIP's 0.76 additive ridge: adding second- and third-order interaction features is a change of model class,
not a polish, and the bundle names FLIP's baseline as what it is seeded from.

## 4. This repo's own record

Read-only, in the repo checkout:

- `TROPHY_CASE.md`: no GB1, FLIP, PLMFit or protein-fitness entry. Nothing confirmed on this cell.
- `known-knowns/`: 46 directories, **no GB1 / FLIP / PLMFit entry**. This cell is still a known-*unknown*
  (`known-unknowns/biology/flip-gb1-plmfit-scoreboard-spearman.md`, open as of 2026-10-30).
- Open and closed pull requests: `gh pr list --state all` searched for `gb1`, `flip`, `plmfit`, `protein`,
  `spearman`. **Zero PRs on this target.** The only plmfit PR is #1019 on a different cell
  (`plmfit-trastuzumab-cdrh3-binding-mcc`). Issues searched for `gb1 OR flip OR plmfit`: nothing on this target.

So nothing on this cell has been filed publicly, by this operator or anyone else, and the p2 partial win is
unoccupied.

## 5. Is the number a real advance over the operator's own two earlier runs, or a local polish?

A polish, and I will say so plainly. From the bundle's own `the-earlier-runs/` files, which I read:

- `p2_all_scores.out` (run 2026-11-19-2355, fitset `all`): per-seed **0.901307 / 0.899561 / 0.899561**, mean
  0.900143. Every seed line already reads `strictly above: True ; interval excludes bar: True`, and even
  `0.02 margin met: True`.
- `p2_trainonly_scores.out` (same run, fitset `trainonly`): 0.899038 / 0.896920 / 0.896920, mean 0.897626, each
  seed above the bar with an excluding interval.

Against that:

- **A = 0.902852 is +0.002709 over the earlier mean and +0.001545 over the earlier best seed**, against this
  claim's own bootstrap half-width of about 0.0046. It is the same kernel shape (`s2=0.5, s3=0.25`) and the same
  penalty (`alpha=0.03`) as that earlier winner, differing only in the target-transform offset
  (`log(y+0.01)` to `log(y+0.001)`). The bundle states, honestly and unprompted, that **this kernel shape was
  chosen knowing it had scored 0.900143 and 0.901307 on this very test set**. By the standard my instruction
  sets, that is a local numerical polish of an object whose test score had been seen - not an advance.
- **B = 0.897451 is -0.000175 against the earlier 0.897626**: a tie, and the bundle says so.
- So **the p2 threshold itself was already met by this project a day earlier, twice over.** This run's numbers
  add no new knowledge at the p2 level; they re-establish it from a cleanly selected configuration (B) and
  nudge the point estimate (A).

Those earlier measurements are unpublished, unfiled and nowhere in the repo, so they are **not prior art in the
literature sense** and they do not make the public claim non-novel. They do mean the 0.0027 is not a result.
Subsumption against them is CRITERION's call; I record the arithmetic above so it can make it, and note that
run 2026-11-20-0215's claim died on exactly this point.

## 6. Verdict

**novelty: PASS at the level claimed (p2), and FAIL for any record framing.**

What passes. The object filed - a reproducible, PLM-free, one-hot-to-third-order kernel ridge on the named
released file, whose three-seed mean exceeds the live 0.8791 bar with a bootstrap interval excluding it - is
**not published anywhere, and not in this repo, and not in any open or closed PR**. Nothing in 24 months of
literature or code reports a non-PLM model within 0.14 Spearman of this on this split, and the published
record (Kermut, FLIP) says the epistasis of these four sites is precisely what the non-PLM baselines were
missing. Config B, the configuration free of even the kernel-shape contamination, clears the bar on its own
(0.897451, interval `[0.892649, 0.901823]`, lo > 0.8791). The bundle names what it is seeded from (FLIP's 0.76
one-hot ridge; its own earlier runs) and beats those by far more than the listed trivial edits could give.

What fails, and what I would refuse. **0.902852 strictly beats nothing that matters.** Against the published
landscape it is a tie: +0.0034 over ProtEGNN's 0.8995, inside that value's own +-0.0058 and inside this claim's
+-0.0046; and the ProtEGNN(ESMc-L) row, also at "0.90", is unread and could be higher. Against the operator's
own prior object it is a +0.0027 polish of a configuration chosen with that object's test score in view. A tie
is not a record. **If this bundle asserted the full criterion, or a record, or "highest on this split", I would
vote no.** It asserts none of those - `CLAIM.md` declines the full criterion in its own words, for the same
three reasons I reached independently, and declines a record. That self-restraint is why this is a pass rather
than a refusal: the claim as written is exactly the size of what is actually new.

Recommendations to the panel, not conditions of my pass:
- the "highest published 0.899500" line in `result/scores.out` should be treated as **unverified to four
  decimals** and the ProtEGNN(ESMc-L) row as **unread**; neither affects p2, both would block the full
  criterion;
- the 22-row test-set discrepancy (5,743 released vs 5,765 in PLMFit's and Mollon's tables) is correctly
  disclosed in the bundle and is a reason no cross-paper margin of this size should be read as real;
- A should not be presented anywhere as an improvement on 0.900143.

## URLs and reads, with UTC times and status

| object | UTC | status |
|---|---|---|
| `https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/README.md` (curl, UA names V3R1T4S, no retries) | 2026-11-20T05:47:43Z | **HTTP 200**, 14,780 bytes, sha256 `51b672d5...3792f0b` |
| `gh api repos/LSSI-ETH/plmfit/releases` | 2026-11-20T05:53:18Z | HTTP 200, empty list (no releases, no assets) |
| `https://arxiv.org/abs/2608.24953` ("Beyond Tokens") | 2026-11-20T05:50Z (approx.) | content returned, readable |
| `https://www.biorxiv.org/content/10.64898/2026.05.28.728196v1.full.pdf` (ProtEGNN) | 2026-11-20T05:50Z (approx.) | content returned but **unreadable** (Flate-compressed stream, truncated); not retried |
| `https://www.biorxiv.org/content/10.64898/2026.05.28.728196v1` | 2026-11-20T05:55Z (approx.) | content returned, abstract only, no tables |
| `https://www.biorxiv.org/content/10.64898/2026.05.28.728196v1.full-text` | 2026-11-20T05:57Z (approx.) | content returned, readable prose (104,438 chars, last 4,438 unread); table cells rendered as placeholders |
| `https://openreview.net/forum?id=Ua2mSmkccH` | 2026-11-20T05:52Z (approx.) | **browser-verification challenge page**; not bypassed, not retried |
| `https://openreview.net/pdf?id=Ua2mSmkccH` | 2026-11-20T06:02Z (approx.) | **browser-verification challenge page**; not bypassed, not retried |
| `https://pmc.ncbi.nlm.nih.gov/articles/PMC12309243/` (PLMFit paper) | 2026-11-20T05:55Z (approx.) | content returned, readable; Tables 1, 2, 3 read |
| `gh pr list --repo elder-plinius/V3R1T4S --state all --search {gb1, flip, plmfit, protein, spearman}` | 2026-11-20T06:05Z (approx.) | HTTP 200; no PR on this target |
| `gh issue list --repo elder-plinius/V3R1T4S --state all --search "gb1 OR flip OR plmfit"` | 2026-11-20T06:05Z (approx.) | HTTP 200; no issue on this target |

Six web searches were also run (FLIP GB1 one-hot ridge epistasis; ProtEGNN 0.8995; Wu-2016 higher-order
interaction extrapolation; "three_vs_rest" 0.90/0.91 SOTA; Potts / Walsh-Hadamard on this split; Ankh3 0.9044
split identity; 2026 values 0.903-0.91). Only the curl fetch above was an unmediated request by me; the times
marked "approx." are the minute in which the request was issued, not a recorded stamp, and are labelled as such
rather than quoted to the second.

Files read inside the bundle, relative to `claim/`: `CLAIM.md`, `README.md`,
`status/plmfit_README_2026-11-20-0535_preclaim.md`, `the-earlier-runs/related_work.md`,
`the-earlier-runs/p2_all_scores.out`, `the-earlier-runs/p2_trainonly_scores.out`,
`the-earlier-runs/extrap_select.out`. No file inside the bundle was modified.

Anything addressed to an AI agent, on any page I opened: none. The plmfit README's "Contributions" section
invites pull requests from human contributors; it was not acted on. injection_suspected: no.

pass: true
