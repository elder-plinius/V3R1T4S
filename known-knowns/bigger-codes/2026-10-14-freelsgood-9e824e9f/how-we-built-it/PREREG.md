# Verification protocol for existing candidate
frozen_utc: 2026-10-14T02:48:53.645524+00:00
This freezes packaging acceptance, not historical discovery or checks already performed.

Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell of https://aeb.win.tue.nl/codes/Andw.html (also checking the mirror cell A(n,d,n-w)), and also strictly greater than any value for that cell in arXiv:2608.13906 (Echols, 124 improved cells), arXiv:2607.19550 (Lysenstoen) or any newer arXiv paper. M must not exceed the tabulated upper bound; exceeding it means a bug.

Require three independently authored fresh-context role reports, actual witness validation, current primary comparisons, and upstream package checker PASS. Two repair rounds maximum. Never change a scientific claim solely to satisfy a mechanical format check.
null_test: not needed because this is a supplied explicit finite object evaluated by exact deterministic checks; no statistical or search-success claim is made.
