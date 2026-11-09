# Claim

target: erdos-677-lcm-blocks (Justin Sun Prize catalog JSP-000550 = Erdős Problem 677; charter quarry 11)

claim: For every k ≥ 1, every n with 0 ≤ n ≤ 5871·k and every m ≥ n + k (no bound on m), lcm(m+1, …, m+k) ≠
lcm(n+1, …, n+k). In other words, every instance of formal-conjectures `Erdos677.erdos_677` with n ≤ 5871·k holds. The
proof is in object/PROOF.md: an argument using the explicit prime bounds of Rosser–Schoenfeld (1962) and Schoenfeld
(1976), followed by the exhaustive computation `object/range_nCk.py 5871`, whose saved output is
object/out/range_nCk_C5871.txt.

partial win claimed: the first enumerated partial win, "an exhaustive, uncapped verification of the statement for a
stated range of (n, k) with a checkable certificate". The stated range is {(n, k) : k ≥ 1, 0 ≤ n ≤ 5871·k}, with
every m ≥ n + k. This is not a full solution, and not a prize solution.

## Object files

| file | sha256 |
|---|---|
| object/PROOF.md | a6c79becb3858a3d64648aa138040aa7f8411f1c98af00787e85c5b8f2312210 |
| object/range_nCk.py | b83f0f45f0324da37bbe56575555560cdc7317fc04df92253a74c80a9a291824 |
| object/out/range_nCk_C5871.txt | 84b1d82fb5d2474686c60663817c5fb49709d7372987c4e044157aac61008d14 |

The frozen statement and judges are under checker/:

| file | role | sha256 |
|---|---|---|
| checker/spec_677.lean | the formal statement, frozen verbatim from formal-conjectures | b5a7c36ec57343836d2ef056dd88df9707c0888a110a8e57ea2c9b398f2d8536 |
| checker/spec_677_negation.lean | its negation | 7f11255c3ee311a344a1c1e796d47af366dac66b66eb42f758d30e4e4ce0b131 |
| checker/check677.py | exact-integer judge for a single triple | 03ecd782d3cfb3437f7b3915b504547b8506a74e39e88bae232e766f94760239 |

## Status record (the scout's table record)

Each source was fetched with one plain request (User-Agent V3R1T4S-research-bot). The log is source/fetch_log.txt.

| source | URL | fetched (UTC) | HTTP | sha256 | status read |
|---|---|---|---|---|---|
| prize catalog volume (status source) | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md | 2026-10-15T07:24:59Z | 200 | 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834 | JSP-000550: "Current status \| Open", "Lean proof \| No" (entry copied to source/jsp_entry_JSP-000550.txt) |
| formal-conjectures statement | https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/677.lean | 2026-10-15T07:24:59Z | 200 | cc682a41950449c693578cdfc83060505bcd482abc12ab33233eaea483681bd0 | `@[category research open, AMS 11] theorem erdos_677 ... := by sorry` (source/fc_Erdos677.lean) |
| formal-conjectures `lcmInterval` | https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjecturesForMathlib/Algebra/GCDMonoid/Finset.lean | 2026-10-15T07:25:00Z | 200 | 996f49245f3e5cc1d0beba2f575ebfe0e92413d826c11603575987026925e9b6 | definition used verbatim in checker/spec_677*.lean (source/fc_GCDMonoid_Finset.lean) |
| erdosproblems.com/677 (the problem's own page, which lists known partial results) | https://www.erdosproblems.com/677 | 2026-10-15T07:25:00Z | none (proxy: `CONNECT tunnel failed, response 403`) | none | not readable from this machine; not retried |

## Success criterion (verbatim, from target.md)

Prize catalog, JSP-000550, "Problem description": "Must two disjoint equal-length intervals of consecutive integers
have different least common multiples?"

formal-conjectures `Erdos677.erdos_677` (FormalConjectures/ErdosProblems/677.lean, fetched 2026-10-15T07:24:59Z):
"Denote by $M(n, k)$ the least common multiple of the finite set $\{n+1, \dotsc, n+k\}$. Is it true that for all
$m \geq n + k$, we get $M(m, k) \neq M(n, k)$?"
```
theorem erdos_677 :
    ∀ (m n k : ℕ), k > 0 → m ≥ n + k → lcmInterval m k ≠ lcmInterval n k
```
with `lcmInterval n k := (Finset.Ioc n (n + k)).lcm id` (FormalConjecturesForMathlib/Algebra/GCDMonoid/Finset.lean).
Success = a kernel-checked proof of this statement or of its negation (a counterexample).

Partial wins (workspace only, NOT prize solutions): an exhaustive, uncapped verification of the statement for a
stated range of (n, k) with a checkable certificate; a machine-checked proof for a fixed small k.

## The pre-registered judge for a range verification (verbatim, from the run's PREREG.md, frozen 2026-10-15T07:28:24Z)

"3. A range verification counts only if every (n, k) in the stated range is covered with no cap on m (the candidate
m's must be provably complete, e.g. via a Størmer/Lehmer argument), with the certificate saved."
