# Brainfuck constant 114514 — how this object was found

*Contributor text, unverified.*

## The target

The esolangs "Brainfuck constants" page lists, for each constant, the shortest known Brainfuck sequence that
leaves that value in the cell under the pointer. For 114514 — a number famous as a Japanese internet in-joke —
the page listed a 92-instruction power-series program as the shortest sequence that leaves the value in a
cell, plus two shorter sequences (58 and 78 instructions) that print the number's UTF-8 bytes instead of
leaving it in a cell, and two unnumbered variants.

## The search

The object was found by a deterministic search over a family of one-loop programs: a prefix writes small
"digit" cells, then a single drifting loop folds them right-to-left with a multiplier `b` and a bias `a`
(`[+^p > +^a [-<+^b>] <<]`), and a suffix returns the pointer to the result. For each choice of
(base, number of digits, bias, offset), an exact signed-digit dynamic program picks the digit vector that
minimises total instruction count; every candidate that survived the cost filter was run in a reference
interpreter. For 114514 the optimum in this family is base 4 with digits 2,3,3,3,1,2,2,1 and bias +1:

`>++>+++>+++>+++>+>++>++>+[>+[-<++++>]<<]>` — 41 instructions, 305,379 steps.

A second pass added the page's own "+q terminator" trick (used by the page's 30-instruction 45306 entry) to
the family; it confirmed 41 as the family optimum for 114514 and improved the companion constant 257 to 27
instructions.

## What failed along the way

- The first claim package was refused by the novelty skeptic for not naming its seed; the package was rebuilt
  with the seed (the page's own construction and its published instances) named, and the new skeptic ran a
  closure test over ~400k trivial edits of every published string on the page to confirm none reaches 41.
- An earlier search had a sign error that silently discarded every candidate with a non-zero loop bias;
  fixing it improved the companion constant 257 from 28 to 27 instructions.
- Two transcription errors in the evidence table were caught by adversarial auditors and fixed
  programmatically (quoted table codes are now extracted by script, never by hand).

## Verification

Two independently written interpreters (one Python, one Rust) plus three fresh-context panel skeptics
verified the object: 305,379 steps, final cell exactly 114514, pointer never below 0, no negative cell, no
8-bit wrap. The claim panel's reports are in panel/.
