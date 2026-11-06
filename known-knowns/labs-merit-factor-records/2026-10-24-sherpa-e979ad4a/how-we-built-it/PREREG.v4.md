# Pre-registration v4 — pass 3: one long attempt at a published *search* value, L = 401

Sealed 2026-10-24T16:44:19Z (from `date -u`), before any search output at L = 401 exists in this session. PREREG.v2 and v3 continue to
bind passes 1 and 2.

## Why

Passes 1-2 compare against constructions or continuation sequences. A record at a length whose best published value
comes from someone's own search would be much stronger. L = 401 has the weakest such bar in 401..449: Dimitrov
arXiv:2206.12070, class B_401^{27,13,9}, E = 11456 (F = 7.0182). Calibration at L = 461 (outside every target set)
reached F 6.855 in 120 s, about 3% in energy short of that level. So this is a long shot, given as much GPU time as is
left.

## Criterion and bar

Criterion verbatim as in `target.md`. Bar B(401) = 11456 from `data/bar_351_449.json` (published value, no derivation,
no pull-request claim below it; arXiv:2011.00068v1's unverifiable L = 401 claim F = 7.0084 is higher). Record requires
E < 11456, found by search from random starts (never seeded with a published sequence).

## Method

Same as PREREG.v2 section 3 (`search.py --mode saw --walk 4000 --prandom 0.5 --pcross 0.9 --heads auto --exploit 0.7
--top-arms 6`), head ranges r1 25-29, r2 12-14, r3 9-11 (Dimitrov's class is inside), seed 3401, workspace venv. It
starts when pass 2's process exits and runs for min(2400 s, time remaining until 20:38 UTC). Code unchanged since PREREG.v2
(same sha256 as listed there).

## Forecast

About 15%: an improvement on a published search value at L ~ 400 needs far more search than calibration showed in minutes.
If it fails, that is the result and it is reported.

null_test: not needed because the claim, if any, is an explicit sequence whose exact integer energy is checked by a deterministic checker against a fixed numeric bar
