# Delsarte certificate: no [163,18,72] code over GF(2), upper bound 72 down to 71

## What

Exact-rational Delsarte LP dual certificate (degree 5) that no (unrestricted or linear) code of length 163, size 2^18 and minimum distance at least 72 exists over an alphabet of size 2, so U(2,163,18) is at most 71 against the live table value 72; not implied by one-step propagation from the live neighbours I fetched; the target-scope reading for q = 2 follows the literal GF(q) text of the criterion.

Path note: the sentence above is quoted word for word from `panel/gate.md` (status `CONFIRMED_PARTIAL`). The object is `object/lp_cert_q2_n163_k18_dub72.json` (sha256 ddae3a6527a7b51d1eb559e5642b5e981a3ceae5ec12ed98b83faf3f5932e0be); its programs are in `how-we-built-it/`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 1 second on the packager's machine; allow a minute or two on a slow laptop.
- **Expected last line**: `PASS`

The quick check verifies the object's hash against INDEX.csv, evaluates the Delsarte polynomial in exact fractions at every integer weight from the excluded distance to n and at 0 (taking the excluded distance from the command line, not from the object), compares with the live upper bound, applies the four one-step propagation rules to the neighbouring live cells in `the-record-we-beat/neighbours.csv`, and confirms that a certificate with a negative multiplier is rejected. The checker alone: `python3 -I verify-it-yourself/lp_delsarte_check.py object/lp_cert_q2_n163_k18_dub72.json 72`, whose last output line begins: `{"q": 2, "n": 163, "k": 18, "D": 72, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}`. Its real output is in `verify-it-yourself/RECEIPTS.md`. The checker differs from the one the panel ran only in file locations and the last output line (see RECEIPTS.md).

## Compared to

| Source | Cell | Listed value | URL | UTC fetch time |
|---|---|---|---|---|
| BKLC cell page | [163,18] over GF(2) | lower 64, upper 72 | http://www.codetables.de/BKLC/BKLC.php?q=2&n=163&k=18 | 2026-10-19T04:35:55Z (triage); 2026-10-19T05:15:33Z (novelty skeptic) |
| BKLC neighbour [162,17] | BKLC neighbour [162,17] | lower 64, upper 72 (rule: shorten: [n,k,d] gives [n-1,k-1,d]) | http://www.codetables.de/BKLC/BKLC.php?q=2&n=162&k=17 | 2026-10-19T04:37:02Z (triage); 2026-10-19T05:15:29Z (novelty skeptic) |
| BKLC neighbour [162,18] | BKLC neighbour [162,18] | lower 64, upper 72 (rule: puncture: [n,k,d] gives [n-1,k,d-1]) | http://www.codetables.de/BKLC/BKLC.php?q=2&n=162&k=18 | 2026-10-19T04:35:54Z (triage); 2026-10-19T05:15:30Z (novelty skeptic) |
| BKLC neighbour [163,17] | BKLC neighbour [163,17] | lower 65, upper 72 (rule: subcode: [n,k,d] gives [n,k-1,>=d]) | http://www.codetables.de/BKLC/BKLC.php?q=2&n=163&k=17 | 2026-10-19T04:37:03Z (triage); 2026-10-19T05:15:32Z (novelty skeptic) |
| BKLC neighbour [164,18] | BKLC neighbour [164,18] | lower 65, upper 72 (rule: pad with a zero column: [n,k,d] gives [n+1,k,>=d]) | http://www.codetables.de/BKLC/BKLC.php?q=2&n=164&k=18 | 2026-10-19T04:37:05Z (triage); 2026-10-19T05:15:35Z (novelty skeptic) |
| V3R1T4S TROPHY_CASE.md and known-knowns folders | this cell | no competing value (see `panel/novelty.md`) | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T05:15:21Z (novelty skeptic) |
| arXiv, four generic queries plus the named work 2609.37056 | this cell | no newer claim found (queries were generic, not exhaustive; see `panel/novelty.md`) | https://arxiv.org/abs/2609.37056 | 2026-10-19 (novelty skeptic) |

Ours: no [163,18,72]_2 code; upper bound 71, value 71; the table value in `INDEX.csv` is "lower 64 upper 72". Each page was fetched once, with a plain GET and no retry; snapshot metadata (HTTP status, sha256 of the page, the extracted cell) is in `the-record-we-beat/README.md`. The panel's reports are in `panel/`.

## Not claimed

- This is a partial win only (the bank's enumerated win p2: an improved upper bound). It gives no code. It does not change the lower bound, and it says nothing about whether a code with distance one less than the new bound exists.
- The certificate is a Delsarte linear-programming dual certificate in exact rational arithmetic (degree 5). It excludes the distance only at the integer weights, as the check runs over integer weights only, and it covers any code of size q^k, linear or not.
- The bar is one-step propagation only. The new bound is below the bound implied by one step of each of four rules (shorten, puncture, subcode, pad with a zero column) applied to the four live neighbouring cells the panel fetched. Longer chains of propagation, other families of bounds in the table, and bounds in the literature were not ruled out beyond what the novelty report says.
- The panel's own Delsarte checker (polynomial convolution, exact fractions) and the package checker (explicit Krawtchouk sums, exact fractions) are two programs, but they implement the same bound.
- Unresolved from the panel: whether a non-arXiv or older paper already excludes this length-distance pair (see the literature section).
- Not peer reviewed. The package was checked by three fresh Claude Code subagents (reproduce, novelty, criterion) and by the standalone checker shipped here. The object was built by a different model family (Gemini, the contributor's search agent); the skeptics and the packager are Claude.

## Filing history

New submission. The gate notes name no earlier pull request for this cell.

## Credits

- **codetables.de** (http://www.codetables.de/), the table compared against, maintained by Markus Grassl as the bank statement for this target names it.
- **Delsarte's linear programming bound** and Krawtchouk polynomials, the method of the certificate (named in the claim text and the bank's verification method).
- **Maruta's page of Griesmer-bound results** (http://mars39.lomo.jp/opu/griesmer.htm), consulted by the novelty skeptic.
- The object and the search code are by Gemini ("Argon"), an AI search agent working for the contributor. Contributor credit: `calgulbenkian`.
- The three panel reports are by fresh Claude Code subagents (`panel/`).
