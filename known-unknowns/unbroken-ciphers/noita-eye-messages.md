# Noita Eye Messages (designed game cipher, developer-confirmed real)

🔐 **Unbroken ciphers** · moonshot (famous, long odds) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

> 🔒 **Live puzzle with a living setter.** Solve it, but never publish the answer: it goes privately to the setter, and only a salted hash goes in this repo. See [DONT_SPOIL_THE_HUNT.md](../../DONT_SPOIL_THE_HUNT.md).

## The problem

Nine messages of eye glyphs in five orientations (5 East, 4 West) in the game Noita (2020). Read as trigrams in base 5, they give an 83-symbol alphabet with values 0-82 and no gaps. Known structure includes no immediately doubled trigrams, shared aligned sections and isomorphs across messages, and a distinct first character per message. The developers say the messages contain a real message. The leading model is a deck or group-autokey style polyalphabetic cipher over S_83. Recover the plaintext and method. The developers' 'real message' confirmation is older; wiki.gg (last edited 9 Oct 2026) shows no new developer statement and still lists the messages as unsolved.

## What counts as a win

CONFIRMED only if a single fully specified algorithm and key (or key-derivation rule) decrypts ALL nine messages from the community's standard trigram transcription into readable text in a natural language (English or Finnish most likely). Each message must have at least 90% of characters in dictionary words. The method must reproduce the observed isomorph alignments and the no-doubles property as consequences, and must not use per-message ad hoc tables. Decrypting with the same method on symbol-shuffled messages must give no readable text. The puzzle must still be listed unsolved on the community tracker at verification time.

## Partial wins

- **p1:** Frozen held-out structure prediction: a fully specified cipher family and key-update rule fitted on at most 8 of the 9 messages (fitting set and model hash committed before the held-out message is scored) that predicts specific symbol relations in the held-out message beyond the already-documented isomorphs and alignments, with those predictions holding at p < 1e-6 against a shuffled-message null.
- **p2:** A single fully specified algorithm and key that decrypts at least one complete message (from the standard trigram transcription) to a natural language with at least 90% dictionary-word coverage, reproduces the no-doubles property as a consequence, and gives no readable text on symbol-shuffled messages, even if it does not yet decrypt all nine.

## How a win is checked

Take the transcription from the wiki or community data files, re-derive the trigram values with the verifier's own parser from the glyph orientation data, implement the claimed algorithm, decrypt all 9, check language coverage, check the isomorph-explanation property, and run the shuffled null.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://noita.wiki.gg/wiki/Eye_Messages>

## Sources

- <https://noita.wiki.gg/wiki/Eye_Messages>
- <https://unsolved-puzzles.github.io/unsolved-puzzles/noita/eye-puzzle.html>
- <https://noita.fandom.com/wiki/Eye_Messages>

## Ideas to start from

Left out on purpose, so this page never spoils the hunt.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/unbroken-ciphers/noita-eye-messages.md
```

Already set up? Say `run V3R1T4S on noita-eye-messages`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `noita-eye-messages`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
