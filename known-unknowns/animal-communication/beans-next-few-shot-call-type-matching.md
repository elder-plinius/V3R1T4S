# BEANS-Next in-context call-type matching: beat NatureLM-audio T4 on both the giant otter (0.645) and carrion crow (0.715) four-way tasks

🐋 **Animal communication** · standard · tractability ★★★★☆ · compute: laptop-hours (only the 400 Otters and Crows examples are needed, five short clips each; the full Hugging Face test split has 37,718 examples) · open as of 2026-11-13

## The problem

BEANS-Next is an audio-language benchmark for bioacoustics with 45 tasks and 37,718 examples. It was built by Plachouras, Robinson, Miron, Narula, Laisne, Fine, Weck, Gilsenan-McMahon, Kim, Hay Mack, Cusimano, Keen, Rauch, Hoffman, Chemla, Benetos, Pauwels, Alizadeh, Geist and Pietquin (Earth Species Project and partners; arXiv 2610.10663 v1, 7 October 2026). Tier 4 tests in-context learning, meaning that the model learns from examples given with the question. Two of its tasks are four-way call-type matching. Otters uses the giant otter vocal repertoire of Mumm and Knörnschild (PLoS One 2014). Crows uses the carrion crow vocal repertoire of Cusimano, Hoffman and colleagues (bioRxiv 2026). Each task has 200 examples. Each example gives four labelled support clips, one per candidate call type, and a query clip, and the system must name the query's call type. Chance is 0.25. This is the core step of repertoire analysis: learning a call category from a single example. Best values in the paper's Table 6 (accuracy, Otters then Crows): NatureLM-audio T4 0.645 and 0.715. T4 is a tier-specific fine-tune trained on synthetic multi-audio data from the ROOTS set, which the authors say is strictly disjoint from BEANS-Next audio. Qwen3-Omni scored 0.535 and 0.620, NatureLM-audio v1.1 0.200 and 0.240, and Audio Flamingo Next 0.255 and 0.225. The appendix Table 14a gives Qwen3-Omni 0.492 and 0.580. Data: Hugging Face EarthSpeciesProject/BEANS-Next, not gated, CC BY-NC-SA 4.0 plus the source datasets' terms, one test split with the expected answer in the messages column, last modified 2026-10-19. Evaluation library: github.com/earthspecies/beans-next (Apache-2.0), with no leaderboard or prize. On 2026-11-13 arXiv held no later paper that reports BEANS-Next.

## What counts as a win

For both Otters and Crows, submit answers to all 200 test examples of the task in the BEANS-Next release of 2026-10-19 (or a later release in which the task is unchanged). Score them with the beans-next evaluation library. Accuracy must be STRICTLY GREATER (direction: max) than the NatureLM-audio T4 value by at least 0.05, that is, above 0.695 on Otters and above 0.765 on Crows. It must also beat any value for the same task that the NOVELTY check finds. Each answer may use only that example's four support clips, their labels and its query clip. Nothing may be shared across test examples, no other test item may be used, and the expected answers may not be read before scoring. Pretrained models are allowed if their training data exclude all BEANS-Next audio, the giant otter recordings of Mumm and Knörnschild (2014), the carrion crow repertoire recordings (doi 10.64898/2026.04.02.715916) and the carrion crow files of FASD13 (Zenodo 15843741). Stochastic systems report the mean over 3 seeds. Deliverables: code, model identifiers and training-data declarations, per-example predictions and the scorer output.

## Partial wins

- **p1:** On one of the two tasks, accuracy strictly above the NatureLM-audio T4 value by at least 0.05 (Otters above 0.695 or Crows above 0.765), under the same rules.
- **p2:** On both tasks, accuracy strictly above Qwen3-Omni's Table 6 values by at least 0.05 (Otters above 0.585 and Crows above 0.670), under the same rules.
- **p3:** A frozen public audio encoder with no fine-tuning on any call-type data, plus a nearest-support-clip rule, beats the NatureLM-audio T4 value on one task by at least 0.02, under the same rules.

## How a win is checked

The skeptic downloads only the Otters and Crows rows of the Hugging Face test split. They rerun the claimant's code in a harness that passes one example at a time and hides the expected answer. They score with the beans-next library. Finally, they check the declared pretraining data against the two source repertoires, the FASD13 crow files and BEANS-Next. This takes under an hour plus model inference time.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://export.arxiv.org/api/query?search_query=all:%22BEANS-Next%22&sortBy=submittedDate&sortOrder=descending&max_results=25>

## Sources

- <https://arxiv.org/abs/2610.10663>
- <https://arxiv.org/html/2610.10663v1>
- <https://huggingface.co/datasets/EarthSpeciesProject/BEANS-Next>
- <https://github.com/earthspecies/beans-next>
- <https://earthspecies.github.io/beans-next/>
- <https://doi.org/10.1371/journal.pone.0112562>
- <https://doi.org/10.64898/2026.04.02.715916>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Prototype matching: embed the query and the four supports with a frozen bioacoustic encoder (several layers averaged) and pick the nearest support by cosine similarity.
- Augment each support clip (small pitch and time shifts, gain changes) to build a richer prototype, then match.
- Cross-domain import (keyword spotting): query-by-example with dynamic time warping on frame embeddings, which keeps the time structure that pooled embeddings lose.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- With 200 examples per task, one standard error is about 0.03, so gains under 0.05 are not counted.
- The paper gives two sets of Qwen3-Omni values (Table 6 and Table 14a); this entry uses Table 6.
- The expected answers are in the same parquet file as the prompts. A harness that loads them before scoring is leakage.
- The FASD13 carrion crow set comes from the same research group and crow population as the Crows task, so audio overlap cannot be ruled out; do not train or tune on it.
- The Unseen, Gibbons and DCASE Tier 4 tasks are left out on purpose: they are species identification or detection, which other bank entries already cover.
- The dataset licence is non-commercial share-alike, and each row's license column carries its source's own terms, some of which read CC BY-NC 4.0.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/animal-communication/beans-next-few-shot-call-type-matching.md
```

Already set up? Say `run V3R1T4S on beans-next-few-shot-call-type-matching`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `beans-next-few-shot-call-type-matching`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
