# MysteryTwister Spanish Strip Cipher Part 3 (Spanish Civil War telegram, 0 solvers)

🔐 **Unbroken ciphers** · standard · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

> 🔒 **Live puzzle with a living setter.** Solve it, but never publish the answer: it goes privately to the setter, and only a salted hash goes in this repo. See [DONT_SPOIL_THE_HUNT.md](../../DONT_SPOIL_THE_HUNT.md).

## The problem

An original Spanish Civil War telegram (summer or fall 1936), apparently encrypted with the Spanish Strip Cipher (SSC): a homophonic substitution where a keyword-derived, shifted random alphabet assigns each plaintext letter to a column of 3-5 two-digit homophones; the challenge hint allows an alphabet that includes LL and CH and may omit W. The ciphertext is 142 two-digit tokens with 55 distinct values (range 02-98). The plaintext is most likely Spanish, possibly Basque. MTC3 Level X (published 2014-03-27) lists 0 solves. As of July 2026 MTC3 no longer accepts new solutions for this challenge and is verifying existing submissions (notice on the Level X page, checked 2026-10-20), so a pending submission may later be credited as the first solve and a new break can only be published independently.

## What counts as a win

The challenge must still show 0 solves on https://mysterytwister.org/challenges/level-x/ at verification time for a first-solve claim (submissions closed in July 2026; if a pending submission is later credited, the claim becomes an independent re-break). CONFIRMED only if ALL of the following hold. (1) The homophone-to-letter key respects the SSC structure as the PDF hints allow it: 3-5 homophones per column; an ordered alphabet that may include LL and CH and may omit W; a keyword-derived random alphabet plus an initial shift, with the variant declared before searching. (2) All 142 tokens decrypt to coherent Spanish or Basque telegraphic text, with at least 90% of letters in words or telegram abbreviations and at most 3 declared garbles. (3) Key-entropy accounting: with 55 distinct homophones, a free mapping costs about 55 x log2(28) ≈ 264 bits, against roughly 142 x 3 ≈ 426 bits of plaintext redundancy. Free mappings are therefore marginal. A claim must either derive the mapping from a keyword-and-shift table structure (≤ about 100 bits) or pass (4) by a wide margin. (4) Null: 200 random token sequences matched on length and repeat profile never reach comparable fluency. (5) Content is plausible for summer or fall 1936.

## Partial wins

- **p1:** A structured key (keyword-derived alphabet plus shift plus table layout, at most about 100 bits, variant declared before searching) under which at least 100 consecutive tokens decrypt to Spanish or Basque telegraphic text with at least 90% coverage and at most 2 declared garbles, while 200 length- and repeat-profile-matched random token sequences never reach comparable fluency.
- **p2:** Blind benchmark: the verifier enciphers 3 period-style Spanish telegrams of 142 tokens under randomly drawn SSC variants within the PDF's allowed space (3-5 homophones per column, optional LL/CH, optional W); the solver recovers at least 95% of plaintext letters of at least 2 of the 3.

## How a win is checked

Extract the tokens with pdftotext from pages 9/10 of the PDF and assert 142 tokens and 55 distinct values. Check the structural constraints programmatically under the declared variant, then score with Spanish and Basque lexica and run the null.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://mysterytwister.org/media/challenges/pdf/mtc3-sanguino-03-SSC-03-en.pdf>

## Sources

- <https://mysterytwister.org/media/challenges/pdf/mtc3-sanguino-03-SSC-03-en.pdf>
- <https://www.mysterytwisterc3.org/en/challenges/level-x/spanish-strip-cipher-part-3>

## Ideas to start from

Left out on purpose, so this page never spoils the hunt.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/unbroken-ciphers/mtc3-spanish-strip-cipher-3.md
```

Already set up? Say `run V3R1T4S on mtc3-spanish-strip-cipher-3`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `mtc3-spanish-strip-cipher-3`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
