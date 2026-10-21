# The last 7 unbroken German Army Truppenschlüssel (TS) hand-cipher messages, 1941 (CryptoCellar)

🔐 **Unbroken ciphers** · standard · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Frode Weierud's CryptoCellar keeps the master status of the 1941 Heeresgruppe Nord traffic on 1941-msg-list.html (status 20 Oct 2026). TS (Truppenschlüssel) is a hand substitution cipher using two 5x5 squares (25-letter alphabet, J written as II), described in Ostwald and Weierud's Cryptologia article 'Modern Cryptanalysis of the Truppenschlüssel'. Of the 137 TS rows on that list, all but 7 are now marked Broken: most of the July 1941 TS messages fell in September 2026 (Norbert Paefgen from 17 Sep, then several AI-assisted solvers credited on the page). The older TS-only page g-army-ts-messages.html still shows its 27 Jul 2026 state, so do not use it for status. The 7 still-unbroken TS messages (green on the master list) are: EHNPZ (08.07.1941, Nr. 123, 87 letters), AFUVO (13.07, Nr. 26, 14), ZUBZE (10.08, Nr. 8, 62), MZXNX (17.08, Nr. 21, 88), BCUCC (05.09, Nr. 20 NF, 64), AAXYN (05.09, Nr. 31, 72) and AOXST (23.09, Nr. 91, 152). These are the ones that resisted everyone, so expect garbles, short or unfavourable plaintext, or ciphering errors. Break any one qualifying message: recover its key and plaintext. (Status corrected on 2026-10-20 after a contributor's report.)

## What counts as a win

Target message must be one of the 7 listed above and must still be listed as unbroken (green, no 'Broken' marker) on https://www.cryptocellar.org/bgac/1941-msg-list.html at verification time (otherwise the result is reported as a non-first re-break). CONFIRMED only if ALL of the following hold. (1) The full key (both 5x5 squares) and the exact TS procedure are given, with the procedure cited to Ostwald and Weierud's Cryptologia article 'Modern Cryptanalysis of the Truppenschlüssel' (section and page). (2) Deterministic decryption of the CryptoCellar transcription (re-extracted fresh) gives connected German military text, with at least 85% of letters inside German words or standard Wehrmacht abbreviations. (3) A garble list is declared BEFORE scoring: at most 8% of letters, each Morse-plausible, with red J positions treated as unknown symbols. (4) Length gate: only messages of at least 80 cipher letters qualify alone. A shorter message qualifies only if the SAME key also decrypts another same-date message to German meeting (2), AND the Cryptologia description confirms that same-day messages share a key. Messages under 40 letters are never CONFIRMED. (5) A shuffled-ciphertext null: 200 shuffles, same pipeline and budget, best score at least 5 SD below the claim. (6) Historical coherence with June to September 1941 traffic of the same net. A custodian 'Broken' marker counts as final external confirmation.

## Partial wins

- **p1:** Blind garble-tolerance benchmark: the verifier enciphers 3 period-style German military texts of 60-100 letters with the TS procedure as implemented from the Cryptologia paper (validated on its worked example), using random squares and injecting about 8% Morse-plausible garbles; the solver, given only the ciphertexts, recovers at least 95% of the plaintext letters of all 3 within a declared compute budget.
- **p2:** A pair of 5x5 squares under which a contiguous run of at least 70 cipher letters of one unbroken message (at least 80 letters long) decrypts to German with at least 85% word/abbreviation coverage, with a garble list declared before scoring and the 200-shuffle null at least 5 SD below, even if the rest of the message exceeds the 8% garble cap.
- **p3:** Same-key evidence: one pair of squares decrypts two unbroken messages of the same date to German meeting criterion (2) on each, with the null at least 5 SD below on each; this counts as a partial win when the Cryptologia description does not confirm daily key sharing (so the full criterion's same-day clause cannot be invoked).

## How a win is checked

Implement TS from the Cryptologia paper's description and worked example. No broken keys are public, so validate the implementation by encrypting and decrypting the paper's own example, and if possible ask the custodian (a human action) for one broken key. Re-scrape the page with a script and assert each message's length against the page's stated length. Apply the claimed key and declared garbles, compute German coverage with a lexicon plus an abbreviation list, rerun the shuffled null with the verifier's own solver, and check same-day key consistency where it is used.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.cryptocellar.org/bgac/1941-msg-list.html>

## Sources

- <https://www.cryptocellar.org/bgac/1941-msg-list.html>
- <https://www.cryptocellar.org/bgac/g-army-ts-messages.html>
- <https://www.cryptocellar.org/bgac/the-fmngi-break.html>
- <https://www.cryptocellar.org/bgac/>
- <https://www.cryptocellar.org/bgac/the-awtzk-znlzt-breaks.html>

## Ideas to start from

Left out on purpose, so this page never spoils the hunt.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/unbroken-ciphers/cryptocellar-truppenschluessel-1941.md
```

Already set up? Say `run V3R1T4S on cryptocellar-truppenschluessel-1941`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `cryptocellar-truppenschluessel-1941`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
