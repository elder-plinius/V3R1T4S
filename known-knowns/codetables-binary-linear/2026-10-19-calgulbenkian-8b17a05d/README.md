# Delsarte certificate: no [153,7,111] code over GF(4), upper bound 111 down to 110

## What

Exact-rational Delsarte LP dual certificate (degree 3) that no (unrestricted or linear) code of length 153, size 4^7 and minimum distance at least 111 exists over an alphabet of size 4, so U(4,153,7) is at most 110 against the live table value 111; not implied by one-step propagation from the live neighbours I fetched; the target-scope reading for q = 4 follows the literal GF(q) text of the criterion (the target id and merged precedent are binary).

Path note: the sentence above is quoted word for word from `panel/gate.md` (status `CONFIRMED_PARTIAL`). The object is `object/lp_cert_q4_n153_k7_dub111.json` (sha256 8b17a05d526aa1c9c9a60a151ddcbddf0c59d09fd98333cc798c1ed6b23bd8e2); its programs are in `how-we-built-it/`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: about 1 second on the packager's machine; allow a minute or two on a slow laptop.
- **Expected last line**: `PASS`

The quick check verifies the object's hash against INDEX.csv, evaluates the Delsarte polynomial in exact fractions at every integer weight from the excluded distance to n and at 0 (taking the excluded distance from the command line, not from the object), compares with the live upper bound, applies the four one-step propagation rules to the neighbouring live cells in `the-record-we-beat/neighbours.csv`, and confirms that a certificate with a negative multiplier is rejected. The checker alone: `python3 -I verify-it-yourself/lp_delsarte_check.py object/lp_cert_q4_n153_k7_dub111.json 111`, whose last output line begins: `{"q": 4, "n": 153, "k": 7, "D": 111, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}`. Its real output is in `verify-it-yourself/RECEIPTS.md`. The checker differs from the one the panel ran only in file locations and the last output line (see RECEIPTS.md).

## Compared to

| Source | Cell | Listed value | URL | UTC fetch time |
|---|---|---|---|---|
| BKLC cell page | [153,7] over GF(4) | lower 107, upper 111 | http://www.codetables.de/BKLC/BKLC.php?q=4&n=153&k=7 | 2026-10-19T04:35:50Z (triage); 2026-10-19T05:15:49Z (novelty skeptic) |
| BKLC neighbour [152,6] | BKLC neighbour [152,6] | lower 109, upper 112 (rule: shorten: [n,k,d] gives [n-1,k-1,d]) | http://www.codetables.de/BKLC/BKLC.php?q=4&n=152&k=6 | 2026-10-19T04:37:13Z (triage); 2026-10-19T05:15:44Z (novelty skeptic) |
| BKLC neighbour [152,7] | BKLC neighbour [152,7] | lower 106, upper 110 (rule: puncture: [n,k,d] gives [n-1,k,d-1]) | http://www.codetables.de/BKLC/BKLC.php?q=4&n=152&k=7 | 2026-10-19T04:37:14Z (triage); 2026-10-19T05:15:46Z (novelty skeptic) |
| BKLC neighbour [153,6] | BKLC neighbour [153,6] | lower 110, upper 112 (rule: subcode: [n,k,d] gives [n,k-1,>=d]) | http://www.codetables.de/BKLC/BKLC.php?q=4&n=153&k=6 | 2026-10-19T04:37:16Z (triage); 2026-10-19T05:15:47Z (novelty skeptic) |
| BKLC neighbour [154,7] | BKLC neighbour [154,7] | lower 108, upper 111 (rule: pad with a zero column: [n,k,d] gives [n+1,k,>=d]) | http://www.codetables.de/BKLC/BKLC.php?q=4&n=154&k=7 | 2026-10-19T04:37:18Z (triage); 2026-10-19T05:15:50Z (novelty skeptic) |
| V3R1T4S TROPHY_CASE.md and known-knowns folders | this cell | no competing value (see `panel/novelty.md`) | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T05:15:21Z (novelty skeptic) |
| arXiv, four generic queries plus the named work 2609.37056 | this cell | no newer claim found (queries were generic, not exhaustive; see `panel/novelty.md`) | https://arxiv.org/abs/2609.37056 | 2026-10-19 (novelty skeptic) |

Ours: no [153,7,111]_4 code; upper bound 110, value 110; the table value in `INDEX.csv` is "lower 107 upper 111". Each page was fetched once, with a plain GET and no retry; snapshot metadata (HTTP status, sha256 of the page, the extracted cell) is in `the-record-we-beat/README.md`. The panel's reports are in `panel/`.

## Not claimed

- Scope question. The bank target codetables-binary-linear is named for binary codes, but its success criterion and partial-win text are written for codes over GF(q), and the live codetables.de table has this cell. No claim over a field other than GF(2) has been merged on this target yet, so whether this cell counts under this target is for the maintainer to rule. The package follows the literal GF(q) text of the criterion.
- This is a partial win only (the bank's enumerated win p2: an improved upper bound). It gives no code. It does not change the lower bound, and it says nothing about whether a code with distance one less than the new bound exists.
- The certificate is a Delsarte linear-programming dual certificate in exact rational arithmetic (degree 3). It excludes the distance only at the integer weights, as the check runs over integer weights only, and it covers any code of size q^k, linear or not.
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
