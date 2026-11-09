# Pre-registration v5 — reallocation after the pass-1 CRITERION ruling

Sealed 2026-10-24T18:43:18Z (from `date -u`), before any search output at L = 401 exists. It supersedes the *budget* in PREREG.v4.md
and the *remaining* lengths of PREREG.v3.md. It does not edit either file.

## Why (a ruling, not a result)

The pass-1 panel's CRITERION skeptic (`panel/cells/L*/criterion.md`) failed all 22 pass-1 cells on a literal reading. The
bank's criterion takes "the best published energy ... as the minimum over the tables in arXiv:2607.09688,
arXiv:2504.00987, the Boskovic et al. LABS records repository cited there, and any newer arXiv result". At lengths
where none of those lists a value the minimum is over an empty set, and the stricter bar B(L) is a substitute
definition. The same reading applies to every pass-2 length (529..585): their bars are GitHub values, not named
tables. So **no remaining pass-2 length can be confirmed, whatever it scores.**
L = 401 is different. Its bar is a published arXiv value (Dimitrov arXiv:2206.12070, E = 11456, below the borkob
archive's 11888), so it is the one cell in this session's reach that the literal criterion can confirm. This is a
change of plan driven by the claim definition, decided before seeing any further pass-2 or any L = 401 output.

## Changes

1. Pass 2 stops after the length now running (L = 533, started 18:39:12Z). Lengths 569, 581, 529, 571, 575, 577 and 579
   are **not run** and are reported as such. Completed pass-2 lengths (535, 567, 583, 585, 531, 533) are reported in full.
2. Pass 3 (L = 401, method, seed, heads and bar exactly as in PREREG.v4.md) starts as soon as the GPU is free and runs
   until 20:38 UTC. That is about 110 minutes instead of 40.

## Forecast

About 25% (up from 15%) that E < 11456 is found. Failure is reported as a failure.

null_test: not needed because the claim, if any, is an explicit sequence whose exact integer energy is checked by a deterministic checker against a fixed numeric bar
