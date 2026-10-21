# Spherical codes (Tammes problem and higher dimensions): beat an entry in Cohn's spherical-codes.org table

⚪ **Packings and physics** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Henry Cohn's table at spherical-codes.org lists the best known spherical codes (maximize the minimal angle between N unit vectors) for dimensions 3..32 (plus one entry each in 52 and 64) and N up to 1024: 15,985 entries on the HTML index (checked 2026-10-20; 16,446 on 2026-10-08), each with the cosine of the minimal angle to 12 decimals, a coordinates file /data/<d>/<N> (16-17 digits per coordinate, one point per line), references, a '*' (HTML entity &ast;) after N for proven-optimal cases, and in 4,859 entries (2026-10-20; 11,996 on 2026-10-08) the per-row reference text 'needs more optimization' (dims 3..32; in dim 3 only N = 842, 893, 907 and 952), meaning the posted code has not converged. A plain CSV is at /plain (15,894 rows on 2026-10-20: d,N,cos[,minimal polynomial]; it carries NO star marks and no labels). Dimension 3 is the Tammes problem (/plain lists N = 7..1024; proven only for small N and N = 24). The table is actively maintained (entries dated 'Henry Cohn, 2026', 'Antoine Jay, 2026'; Numaro records cited). Sloane's original tables (neilsloane.com/packings) return HTTP 403 to curl and are superseded. EinsteinArena's Tammes N=50 leaderboard (checked 2026-10-08) tops out at 0.51347176 rad, consistent with the table's cos 0.868173209127 (= 0.5134721 rad); never use that leaderboard as a record source.

## What counts as a win

Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code.

## Partial wins

- **p1:** A certified improvement (same rule, margin 1e-10, no star, no 'needs more optimization' label) in dimension 3 (Tammes problem) for an N listed in /plain; only four 3D entries (N = 842, 893, 907, 952) carry the 'needs more optimization' label and they do not count here, so this is the hardest sub-case.
- **p2:** A batch of at least 20 certified improvements (margin 1e-10 each) to rows labeled 'needs more optimization' in one dimension d in 4..32, delivered as one file set with the largest improvement reported; these rows are flagged unconverged by the table, so the batch is a partial win, never a claim.
- **p3:** An exact-angle certificate for an unstarred, unlabeled row that has no minimal polynomial listed: a configuration whose minimal-angle cosine is shown (mpmath findpoly/PSLQ at 60 digits, confirmed at 100 digits) to be an algebraic number matching the table value to 1e-12, with the contact structure verified rigid; adds a polynomial the table lacks.

## How a win is checked

Checker (< 5 minutes per entry): curl https://spherical-codes.org/plain and parse the (d,N) row (CSV: d,N,cos). curl https://spherical-codes.org/ and locate the row via its link href="/data/<d>/<N>": assert no '&ast;' follows the link and the row's reference cell does not contain 'needs more optimization'. Load the claimed vectors; mpmath mp.dps=50; normalize; compute all N(N-1)/2 inner products; c* = max. Assert c_table - c* >= 1e-10. Also curl /data/<d>/<N> and compute the posted code's c (must reproduce the table to 1e-11; parser sanity). Report c* to 20 digits and the minimal angle in degrees.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://spherical-codes.org/>

## Sources

- <https://spherical-codes.org/>
- <https://spherical-codes.org/plain>
- <https://spherical-codes.org/data/3/50>
- <https://spherical-codes.org/data/3/60>
- <https://einsteinarena.com/problems/tammes-problem>
- <https://www.hars.us/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Harvest the 4,859 'needs more optimization' entries (2026-10-20 count; the table is being re-optimized quickly): for each (d, N) download /data/<d>/<N>, run a smooth-max (log-sum-exp of inner products with increasing sharpness) L-BFGS descent followed by an active-set SLSQP on the true min-angle objective, then mpmath polish; 10 cores can sweep thousands of entries in hours. Prioritize dims 5..12 where N is moderate and gains are typically 1e-6..1e-3.
- Structured codes: for d = 4..8 use orbits of finite reflection groups (W(F4), W(E6), W(E7), W(E8)) and their subgroups; union-of-orbits codes with one continuous parameter per orbit often beat unstructured numerical codes at N near 100..1024.
- Lifting/projection: good codes in dimension d+1 projected or sliced to d, and codes in d lifted by adding a small coordinate, give fresh basins; also antipodal doubling (N -> 2N) of a good code in d.
- 3D Tammes (p1): seed with Hars' N <= 60 point sets and Deeter-style symmetric (D_n, T, O, I subgroup) starts, run 10^5 restarts per N in 60..150, polish active contacts to 30 digits; the 2025 N = 60 gain (6e-9) shows tiny improvements still exist.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Direction: the table lists the COSINE of the minimal angle; smaller cosine = larger angle = better.
- Normalization: vectors must be exactly unit length in mpmath before computing inner products.
- Starred (proven optimal) entries cannot be beaten; the star exists ONLY on the HTML index (/plain has none), so the checker must parse the index, not /plain.
- 'needs more optimization' rows are the table's own admission of an unconverged entry; beating one is p2, not a record.
- Kissing-number overlap: configurations with c* <= 0.5 in dims 9..23 belong to kissing-number-low-dim.
- EinsteinArena leaderboards have had verifier exploits; never cite a leaderboard without recomputing from coordinates.
- Literature scooping: re-fetch /plain and search arXiv immediately before claiming; uploading to /upload-code needs explicit permission from the human.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/packings-physics/spherical-codes-cohn-table.md
```

Already set up? Say `run V3R1T4S on spherical-codes-cohn-table`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `spherical-codes-cohn-table`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
