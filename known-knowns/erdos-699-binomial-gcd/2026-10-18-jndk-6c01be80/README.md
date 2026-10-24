## What

For every integer n>=65536 and every integer j with 4<=j<=floor(n/2) and 2^36*(n-2j)^6<=n^5, there exists an odd prime dividing both C(n,3) and C(n,j).

PROVED-HERE: the written proof passed three fresh independent agent reviews. The p1 qualification uses the bank's line-by-line refereeing process. This is a local research assessment, not journal acceptance or a priority claim.

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh` from this folder with Python 3. Expected last line: `PASS`. The small exact checks should take seconds on an ordinary laptop; no dependency installation is needed.

The checker binds the files to the reviewed versions, independently checks polynomial identities, exact constants, localization examples, finite gcd examples and deliberate algebraic mutants. The hash guard detects edits; it does not establish mathematical correctness. The universal prime/divisibility argument requires reading object/PROOF.md and the line-by-line review. This is not a full proof-assistant formalization.

## Compared to

| Cell | Prior scope | Source and fetch |
|---|---|---|
| Erdős #699 p1 | j<=3i/2 or n=2j; wider preliminary theorem excludes i=3 | [Primary record](https://www.erdosproblems.com/699), 2026-10-18T20:39:10.977979+00:00 |

Both complete user-supplied manuscripts and wider prior results were compared, including the general Euclidean and orbit bounds. Details and limitations are preserved in panel/novelty.md and the-record-we-beat/COMPARISON.md.

## Not claimed

No complete conjecture, all-j cubic theorem, uniform varying-i theorem, exhaustive all-i verification record, journal refereeing, first-ever priority, or formal proof-assistant certificate. Finite checks corroborate the written proof and do not establish its infinite quantifiers. A general GCD publisher page was blocked; the accessible primary author record and indexed primary theorem do not state this explicit universal application. Full-paper review of that general lead was not completed.

## Credits

Credit: jndk; proof developed with Codex. Erdős and Szekeres posed the [problem](https://www.erdosproblems.com/699). Liam Price with GPT 5.6 Sol Pro supplied the ratio/centre proof and localization background; Stefano Rocca's manuscript attributes its supporting arguments to Price and explicitly leaves i=3. The human supplied both complete texts and confirmed the [project identity](https://www.overleaf.com/project/6a5bc0371d4854c975df1efb). Full positional localization, single-3 cancellation, parity exclusions and thin-family viewpoint are prior work in the [pinned frontier atlas](https://github.com/techno-optimist/erdos-frontier-atlas/tree/5e1f513b5383ed986b1543708ca7f3d1d80e6240); its constant-width strip, nearby diagonals and finite computations are credited as overlap. [Bergman's orbit work](https://arxiv.org/abs/0806.0607) supplies related cancellation background. Del Pin, MaxDKaos and Cong Lu's forum contributions are compared in the novelty report. None of these shared ingredients is presented as newly invented here.
