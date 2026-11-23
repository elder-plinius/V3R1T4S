# The published-value question, RESOLVED — source document read 2026-11-20

**Supersedes `published-values-correction.md` in this folder**, which left the question open. That file's
conclusion ("a published value above 0.902852 cannot be ruled out, because two models are reported at 0.90 and
one of them is unread") rested on two misreadings of our own, both corrected below.

## Provenance, stated honestly

**Canonical source, supplied by the operator:** `https://openreview.net/pdf?id=Ua2mSmkccH`

**Cite it as the workshop paper, not the preprint.** The document's own running header reads *"Published at LMRL
Workshop at ICLR 2026"*, so the correct citation is the ICLR 2026 LMRL Workshop paper (OpenReview
`Ua2mSmkccH`), with bioRxiv `10.64898/2026.05.28.728196` as the preprint. This also settles the DOI-prefix
oddity that confused the earlier survey (the live prefix is `10.64898`, not the `10.1101` the citation implied):
the authoritative venue is OpenReview. **For novelty purposes a workshop paper at ICLR is published**, so these
values count against the full criterion's "any published value" clause.

The text was **read and transcribed by the operator** into the session on 2026-11-20, after every automated
route failed (bioRxiv PDF streams would not decode, the HTML rendered the table cells as placeholders, and two
OpenReview URLs served a browser-verification challenge which the NOVELTY skeptic correctly did not bypass and
did not retry). This is therefore **an operator transcription of the source, not a hashed fetch by this
workspace.** It is not a `curl` with a sha256 and must not be written up as one. A future run with working
access to that URL should re-verify Table 1's GB1 column and record the fetch properly.

Integrity checks that the transcription passes, which is why it is trusted here:
- The title, author list, affiliations and venue match the citation (*"Just Add Structure: Protein Language
  Models Combined With Structural Equivariance Excel At Protein Tasks"*, Qurat-ul-ain, Outeiral, Cagiada, Teh,
  Deane; LMRL Workshop at ICLR 2026).
- **Table 1 and Table 4b agree internally**: Table 1's GB1 figures 89.95 and 89.51 both round to the 0.90 that
  Table 4b prints at two decimals. A fabricated or garbled transcription would not be consistent across two
  tables at two different precisions.
- Appendix A.1.2's description of the dataset matches our data object independently (see below).

## 1. The comparator, confirmed to four significant figures

**Table 1** ("Effect of PLM scale and explicit geometric modeling across tasks"), GB1 column, values in percent:

| sequence model | method | GB1 (SPR) |
|---|---|---|
| ESM2-T6 (8M) | Pre-trained | 81.80 ± 0.41 |
| ESM2-T6 (8M) | Fine-tuned | 88.30 ± 0.95 |
| ESM2-T6 (8M) | **ProtEGNN** | **89.95 ± 0.58** |
| ESMc (6B) | Pre-trained | 83.01 ± 0.21 |
| ESMc (6B) | Fine-tuned | 89.44 ± 0.07 |
| ESMc (6B) | **ProtEGNN** | **89.51 ± 0.30** |

So **ProtEGNN(t6) = 0.8995 ± 0.0058**. The carried survey's figure was **exactly right**, to the last digit, and
is now confirmed at source rather than second-hand. Item 5a of `NEEDS-YOU-2026-11-20.md` is resolved.

Evaluation protocol, from §5: *"All ProtEGNN models are evaluated using 3-fold cross-validation over random
seeds 97, 98, 99"* — a three-seed mean with a seed-to-seed spread, the same **form** as our own three-seed mean,
which is what makes the comparison legitimate at all.

## 2. Our own two errors, corrected

**There is no `ProtEGNN(ESMc-L)` and no `ProtEGNN(ESMc-M)`.** The paper has exactly two ProtEGNN variants,
`ProtEGNN(t6)` (ESM2-T6, 8M) and `ProtEGNN(ESMc)` (ESMc, 6B), named consistently in §5, Table 1, Table 4b and
Appendix A.2. Both suffixes were invented by us:

| our claim | where | the truth |
|---|---|---|
| "ProtEGNN(ESMc-**L**)" is a second model at 0.90 and is unread, so a published value above 0.902852 cannot be ruled out | run `2026-11-20-0535` NOVELTY, and `published-values-correction.md` | no such model; the real second variant is `ProtEGNN(ESMc)` at **0.8951 ± 0.0030**, which is **below** our 0.902852 |
| "ESMc-**M** ProtEGNN 0.8954" | run `2026-11-19-2355` survey, carried into `related_work-carried.md` | the value is **0.8951 ± 0.0030**, and the variant has no `-M` |

**The consequence is that the central worry was ours, not the literature's.** The second model at "0.90" in
Table 4b does not threaten anything: Table 4b simply prints two decimals, and Table 1 shows that both
ProtEGNN variants sit at 0.8995 and 0.8951. Nothing in this paper is above 0.902852 except possibly item 3.

## 3. The one question this paper opens rather than closes: Ankh3's split

**Table 4b** (GB1, ascending SPR, two decimals):

| model | # parameters | SPR |
|---|---|---|
| SaProt | 650M | 0.81 |
| PRIME | 653M | 0.82 |
| ESM2-T48 | 15B | 0.85 |
| PLM-Fit | 6.4B | 0.88 |
| ESM2-T36-FT | 7.7M | 0.89 |
| ProtEGNN(ESMc) | 1M | 0.90 |
| ProtEGNN(t6) | 400K | 0.90 |
| **Ankh3** | **5.7B** | **0.90** |

§5.3.2: *"Both ProtEGNN(t6) and ProtEGNN(ESMc) reach an SPR of 0.90, matching the best-performing 5.7B parameter
Ankh3 model."* Appendix A.1.2 states the GB1 split for this table is *"the standard 3-vs-rest split, where
single, double, and triple mutants are used for training and more distant variants for testing."*

**But run `2026-11-19-2355`'s survey established that Ankh3's own published GB1 number, 0.9044, is on the
`sampled` split** (6,291/670/1,772), not this one. **0.9044 > 0.902852.** So exactly one of these holds:

- **(a)** The ProtEGNN authors carried Ankh3's `sampled`-split figure into a 3-vs-rest comparison table. Then it
  is a citation error in their paper and **not a published value on our split**, and the highest published
  3-vs-rest value remains their own 0.8995 ± 0.0058.
- **(b)** Ankh3 genuinely reports ~0.90 on 3-vs-rest somewhere. Then the published maximum is at or above our
  number and clause 6 fails outright.

**This is answered from Ankh3's paper (arXiv 2505.20052), not from this one.** It is the only remaining novelty
hole on this cell, alongside the unread CombinGym leaderboard. The paper gives no explicit test-row count, so
the carried survey's **5,765-vs-5,743 discrepancy is still unresolved** from this source.

## 4. A worry this paper retires

`NEEDS-YOU` §5a flagged that **PLMFit's own Table 3 prints "0.9"** for GB1 three-vs-rest, raising the
possibility that the bank's live bar of 0.8791 is the wrong number for the cell. Table 4b above lists
**PLM-Fit (6.4B) at 0.88** on this split — an independent third party reading PLMFit's GB1 3-vs-rest result as
0.88, which is 0.8791 rounded, **not** 0.9. Combined with ESM2-T48 15B appearing separately at 0.85, the "0.9"
in PLMFit's Table 3 is not a Spearman for this cell. **The bank's bar of 0.8791 is corroborated.**

## 5. Independent confirmation that the benchmark object is the same

Appendix A.1.2: *"the GB1 landscape from the FLIP benchmark (Dallago et al., 2021), which measures binding
affinity of ∼8,700 variants of the immunoglobulin-binding domain of Protein G. Mutations are introduced at four
positions, producing a highly epistatic landscape."* Our data object, re-derived in the main session from the
released file: 8,733 rows, four varying positions (residues 39/40/41/54), wild type `VDGV`, split tally
2,691 `train` / 299 `validation` / 5,743 `test`. Same object, same split family.

## 6. What this does and does not change for our standing

**It does not move the threshold.** Run `2026-11-20-0215` computed a defensible beat of this cell at about
**0.906** *from* 0.8995 ± 0.0058. That input is now confirmed exact, so the 0.906 figure is **confirmed rather
than revised**, and our position is unchanged:

| our number | vs 0.8995 | separable? |
|---|---|---|
| 0.902852 (A, shape-contaminated) | +0.003352 | **no** — inside ProtEGNN's own ±0.0058 and inside A's own ±0.0046 |
| 0.900143 (best clean, run `2026-11-19-2355`) | +0.000643 | **no** — about 1/9 of the comparator's sd |

So clause 6 is *nominally* satisfiable against 0.8995 and **not defensibly** so, which is exactly the judgement
runs `2026-11-19-2355` and `2026-11-20-0215` already reached. **No run should be spent chasing this number**:
the ceiling analysis (about 2,166 free pairwise terms against 2,990 training rows, a badly underdetermined
third-order block, and `C(m,4)` being the identity on distinct genotypes) says the family is near its limit, and
the one run that tried for the record went backwards by 0.0053.

**What is worth a run is the selection-criterion lead**, which is a methodological result that transfers to
every train-shallow / test-deep benchmark in the bank, and which these data leave genuinely open.
