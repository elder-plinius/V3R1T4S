context: Claude Code subagent, fresh context [Sonnet 5.5]

# Novelty report: hypercube-q8-perfect-matchings, partial win p2 (A005271(8) = 3 mod 5)

## Fetch log
- 2026-11-18T17:31:12Z  https://oeis.org/A005271  HTTP 200  sha256 41663c77a2d96e2da02a76e5efffe1dfd29043b99247134f38eaafe0f8d91f9c (single fetch, no retries)
- Page footer: "Last modified November 18 12:04 EST 2026". DATA: 1, 2, 9, 272, 589185, 16332454526976, 391689748492473664721077609089 (n=1..7). Keywords nonn,hard,more,nice. LINKS "Table of n, a(n) for n=1..7". a(8) is absent. No comment, formula or link gives any residue or congruence of a(8) (the only comment on parity is the Lovasz parity remark in the target text, not on this page's data).

## Literature and code
Web searches (standard and extended) on: perfect matchings of Q_8 and mod 5 or congruence; Ostergard-Pettersson "Enumerating Perfect Matchings in n-Cubes" (Order 30, 2013, abstract stops at n=7: total 391689748492473664721077609089 and class counts for n=5,6,7); 2024-2026 papers; GitHub code or data.
- Ostergard-Pettersson 2013: n<=7 only; no n=8 value, no modular statement found in the abstract or indexing pages.
- Alon-Balogh-Potapov (arXiv 2401.00299, 2024) lists m(d) only up to d=5 and gives asymptotic bounds; no Q_8 value or residue.
- Other hits (minimum forcing number of perfect matchings in hypercubes, Hamiltonian circuit bounds, dimer-model papers, OEIS A220904 class counts, A018926 subcube tilings) contain no Q_8 count or residue.
- GitHub and release-asset search through the web engine found no repository computing or listing the Q_8 count or a residue. This is a search-engine result only, not an exhaustive code search.
- I could not read the full text of the Ostergard-Pettersson paper (paywalled/not fetched), so a modular remark inside the body is not excluded, though nothing indexed suggests one.

## This repository (github.com/elder-plinius/V3R1T4S, read through gh, read-only)
- main tree: TROPHY_CASE.md has no hypercube or perfect-matching row; no path matching hypercube, q8 or this target under the repository's known-knowns folder (only stable-marriage matchings and unrelated hits).
- Pull requests, all states, searched for "hypercube-q8-perfect-matchings", "hypercube", "Q8", "matchings", "perfect matchings", "A005271": no claim, bank or submission PR for this target, on mod 5 or any other modulus. Unrelated hits only (snake-coil hypercube PRs, dimer-constant PRs, stable-marriage PRs).
- No other claim by anyone on p1, p2 or the full count for this target was found.

## Edits and implication check
- Nothing published gives an object to edit: no published Q_8 count, residue or fixed-point count exists to restrict, propagate or polish.
- The method (Burnside on a Sylow p-subgroup of Aut(Q_8), count = fixed points mod p) is a standard technique that the target text itself names as an example for p2; it is not a published result about Q_8. The residue is not implied by Lovasz parity (that only gives the parity) or by anything on the OEIS page.
- The specific value 3 mod 5 and the fixed-point count 743141892135168 are not found in any source I could search.

Limits: web-search-based literature check, paper body of the 2013 article unread, GitHub coverage by search engine only. Within those limits the result is new and nothing known ties or beats it. Correctness of the value is for the reproduce and criterion roles; this report covers novelty only.

pass: true
