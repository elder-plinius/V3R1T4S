# Linear A: pre-registered morphological alternations that predict held-out contexts

📜 **Undeciphered scripts** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

With Linear B phonetic values applied to Linear A homomorphs, Linear A words can be transliterated, but the language is unknown. Morphology is the open sub-problem. Candidate alternations have been discussed (initial A-/JA-, final -TE/-TI/-NA/-RE variation, libation-formula variants such as JA-SA-SA-RA-ME and A-SA-SA-RA-ME), but none has been shown to predict distribution. The task is to find affix or alternation rules whose presence predicts where a word occurs: its document type, its adjacency to a logogram (VIR/personnel versus commodity), its site, or libation-formula position. Data caveat: in Navarre-AI corpus.json (release 2026-10-15, 1,884 records; the new word_layer field names each word list's source, and lineara.xyz-sourced words were rebuilt from the raw transcription so they no longer join across lacunae) a 'words' list is present on 705 records. In the 2026-09-18 release 701 were non-empty: 467 with word_source 'sigla' (SigLA), 234 with 'lineara' (lineara.xyz, with different division conventions) and 4 empty ones without a word_source (the README's data description gives 670 and 666). In the 2026-10-15 release 125 of the 234 lineara.xyz lists differ and 6 are now empty (695 non-empty in all). Status as of 2026-10-03: Partly deciphered at the phonetic level; the language is unknown. The 2026 Di Mino 'Ya Diktu' Semitic grammar is unverified, and the adversarial replication kbennett2000/linear-a-check finds its root matches are no better than scrambled controls. The corpus was updated on 2026-09-18 and again on 2026-10-15 (word-layer repair for 234 lineara.xyz-sourced records, nine edition corrections, ERRATA.md); pin the release used.

## What counts as a win

A frozen list of at most 10 alternation hypotheses is written before evaluation. Held-out data is every document from a whole site (for example, all Khania or all Zakros) or a random 30% of documents, chosen beforehand. At least one hypothesis must predict a held-out contextual variable with Bonferroni-corrected p < 0.001 (Fisher exact or permutation test over word-to-context assignments). Examples: 'words ending -RE precede personnel logograms', 'A-/JA- alternation tracks libation versus administrative support'. The effect must survive dropping the single most frequent word type. Hypotheses in the published literature that do not reach significance do not count. A published hypothesis reaching this significance for the first time does count, with that stated. Additionally: tokens come from a single declared word_source (SigLA or lineara.xyz), or the result must replicate in both; tokens containing uncertain or unidentified signs (e.g. 're?', '[?]') are excluded; the held-out split is by whole site or by document, never by token; and every hypothesis is checked for novelty against existing libation-formula studies (e.g. Davis 2014 on stone vessels).

## Partial wins

- **p1:** A frozen hypothesis (from a pre-registered list of at most 10) that, on the pre-declared held-out site or document split, under one declared word_source and excluding uncertain-sign tokens, predicts the held-out contextual variable at Bonferroni-corrected p < 0.01 (rather than the full bar of p < 0.001), survives dropping the most frequent word type, and has not previously reached that significance in the literature.
- **p2:** Onomastic cross-prediction: Linear A sign-groups that also occur as Linear B personal names or toponyms at Knossos (list frozen before evaluation) are adjacent to personnel logograms (VIR etc.) on held-out documents significantly more often than non-shared sign-groups of matched length and frequency (Fisher exact or permutation p < 0.001), surviving the drop of the most frequent type, with the effect not already published.

## How a win is checked

The verifier pins the Navarre-AI commit and filters by word_source. It rebuilds tokens, excludes uncertain signs, re-applies the frozen regexes, recomputes Fisher or permutation tests with Bonferroni correction over all frozen hypotheses, reruns with the most frequent type dropped, and checks the git timestamp order.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/Navarre-AI/linear-a>

## Sources

- <https://github.com/Navarre-AI/linear-a>
- <https://sigla.phis.me>
- <https://github.com/mwenge/lineara.xyz>
- <https://github.com/kbennett2000/linear-a-check>

## Ideas to start from

Left out on purpose, so this page never spoils the hunt.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/undeciphered-scripts/linear-a-morphology-heldout.md
```

Already set up? Say `run V3R1T4S on linear-a-morphology-heldout`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `linear-a-morphology-heldout`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
