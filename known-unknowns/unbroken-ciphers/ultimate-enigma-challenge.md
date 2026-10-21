# CryptoCellar 'Ultimate Enigma Challenge' (5 Sept 1941 messages, possibly non-standard machine)

🔐 **Unbroken ciphers** · moonshot (famous, long odds) · tractability ★☆☆☆☆ · compute: laptop-hours · open as of 2026-10-20

> 🔒 **Live puzzle with a living setter.** Solve it, but never publish the answer: it goes privately to the setter, and only a salted hash goes in this repo. See [DONT_SPOIL_THE_HUNT.md](../../DONT_SPOIL_THE_HUNT.md).

## The problem

Five messages with Enigma-style indicators but unusual operators, comments and very low radio frequencies: QTXMA and SZAEJ (29.09.1941) and BYQMZ, FKQLZ and XFEDT (30.09.1941). The ultimate-enigma.html page (updated 27 July 2026) gives header letter counts 160/56/172/112/102; the master 1941 list (https://www.cryptocellar.org/bgac/1941-msg-list.html, status 20 October 2026) gives total/cipher letters QTXMA 160/155, SZAEJ 56/51, BYQMZ 172/167, FKQLZ 112/107 and XFEDT 102/97, all still highlighted as unbroken. Weierud suspects a police network (Ordnungspolizei) and possibly a machine with different wheel wiring. Every attack since 2003-2004 has failed. Break any of them.

## What counts as a win

CONFIRMED only if a fully specified machine (wiring of all wheels and reflector, stepping, plugboard) and ONE daily key decrypt at least TWO messages of the SAME date (two of BYQMZ, FKQLZ, XFEDT for 30.09, or QTXMA plus SZAEJ for 29.09) to German with at least 85% coverage. Garbles are pre-declared and at most 10%. Both indicators must decrypt consistently to their message keys. Any non-standard wiring must be a documented historical wiring or be derived once and then held fixed across both messages. Shuffled nulls are run per message. The messages must still be shown unbroken on https://www.cryptocellar.org/bgac/ultimate-enigma.html at verification time.

## Partial wins

- **p1:** Single-message machine break: a fully specified machine of documented historical wiring (e.g. Enigma I, Enigma G, Railway Enigma, Swiss K) and key under which one message of at least 97 cipher letters (BYQMZ, FKQLZ or XFEDT) has a consistent indicator and decrypts to German with at least 85% coverage, garbles pre-declared and at most 10%, and the shuffled null for that message far below the claim, without yet a second same-date message.
- **p2:** Single-message hand-cipher break: a fully specified hand system (e.g. Doppelkasten or a police transposition) and key that decrypts one of the 30.09 messages to German with at least 85% coverage, at most 10% pre-declared garbles, key bits below half the message's redundancy (message length x 3.2 bits / 2), and a per-message shuffled null far below the claim.

## How a win is checked

Re-extract the ciphertext from ultimate-enigma.html and separate header from cipher groups, asserting letter counts against the unbroken overview (167/107/97 for the 30.09 messages). Implement the machine independently, check the indicators and run the nulls.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.cryptocellar.org/bgac/ultimate-enigma.html>

## Sources

- <https://www.cryptocellar.org/bgac/ultimate-enigma.html>
- <https://www.cryptocellar.org/bgac/1941-msg-list.html>

## Ideas to start from

Left out on purpose, so this page never spoils the hunt.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/unbroken-ciphers/ultimate-enigma-challenge.md
```

Already set up? Say `run V3R1T4S on ultimate-enigma-challenge`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ultimate-enigma-challenge`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
