# Spheres in a sphere: Packomania ssp radius.txt lists 90 radii (N = 1055 … 50000) that the posted data do not support (data-integrity erratum)

| | |
|---|---|
| **Claim** | Packomania ssp txt/radius.txt gives, for 90 rows N = 1055 … 50000, a radius larger than both the ssp.html value and the feasible radius r* of the posted coordinate files. ssp.html and coordinate r* agree within 2.8e-12. Gaps run from 6.09e-9 (N = 1601) to 6.48e-5 (N = 20000). No radius.txt row is below the coordinates. |
| **One-command repro** | `sh verify-it-yourself/run_checks.sh`. Python 3 standard library only (Decimal, 60 digits). Everything is re-downloaded from packomania.com at run time (set SSP_TARBALL to use a local ssp_coords.tar.gz). Expected last line: `PASS`. |
| **Not claimed** | No record and no new packing. Not a coordinate error. No claim about why radius.txt diverged. **Not claimed to be unreported to Packomania.** |
| **Confidence** | Numerical result: high (reproduce PASS, criterion PASS, three independent cross-checks; live files re-hashed unchanged 2026-10-17 04:30 UTC; N = 1157, 1601, 20000 spot-checked against live per-N files). **Novelty is NEED-HUMAN: the error is live and unfixed, but we cannot prove it is unreported because Packomania accepts reports only by private email and has no public report log. Public silence is not proof of non-report. Panel verdict: PROMISING, not CONFIRMED.** |

Labelled as a data-integrity finding (erratum), not a record claim. Filed with moe's approval as an erratum; the kit's novelty and status gates are not met (see CHECK_RUN_OUTPUT.txt).

## What

Live Packomania ssp radius.txt (sha256 9a4d7b62c61ac3aad69c11f238c76707c51ee824f163bee44a2b345a04b39fe3) exceeds ssp.html (sha256 e2d84d0d6cfd66870b940bfc068ba3e0827a51ea407b365473b869db828e77fd) by more than 1e-9 in exactly 90 rows, N=1055..50000, with gaps from 6.09e-9 (N=1601) to 6.48e-5 (N=20000), no ties and no row below; in all 14 rows recomputed at 50 digits from ssp_coords.tar.gz (sha256 c077c79ef6c767e7d14d73942beed2f4be1bd15286073ef1548475f230c3e5f3), ssp.html equals coordinate r* within 1.75e-12.

Status: PROMISING, not confirmed. Panel (panel/gate.md): reproduce PASS, criterion PASS, novelty NEED-HUMAN. Filed as a data-integrity erratum with moe's approval; the panel files are unedited and still read "held" because they were written before that decision.

This package contains one object only: object/ssp_radiustxt_errata.csv (90 rows); the skeptic-facing claim text is how-we-built-it/CLAIM.md.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library only (Decimal, 60 digits). Downloads radius.txt, ssp.html and the 137 MB ssp_coords.tar.gz (or set SSP_TARBALL to a local copy). About 1 minute plus the download on a laptop.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Packomania ssp txt/radius.txt | 90 rows, e.g. N = 20000 | 0.031576568223 | https://packomania.com/ssp/txt/radius.txt | 2026-10-16T15:47:00Z |
| Packomania ssp.html | same rows | 0.031511804440 (N = 20000; coord r* 0.0315118044387) | https://packomania.com/ssp/ssp.html | 2026-10-16T15:47:00Z |
| Packomania ssp coordinates | ssp<N>.txt | r* agrees with ssp.html within 2.8e-12 | https://packomania.com/ssp/txt/ssp_coords.tar.gz | 2026-10-16T15:47:00Z |

Details in the-record-we-beat/.

## Not claimed

- No record and no new packing.
- Not a coordinate error: coordinate files and ssp.html agree; only radius.txt carries larger values. No row of radius.txt is below the coordinates.
- Not the separate blank-last-sphere defect in ssp files with N <= 1000.
- No claim about why radius.txt diverged (unposted newer packings, stale file, or other).
- Not confirmed and not claimed novel. Novelty is NEED-HUMAN: the error is live and unfixed, but we cannot prove it is unreported because Packomania accepts reports only by private email and has no public report log. Public silence is not proof of non-report. Panel verdict: PROMISING, not CONFIRMED. (panel/novelty.md, panel/gate.md.) Packomania has not been contacted by us.

Repository placement: target_id packomania-ssp-spheres-in-sphere is not in the V3R1T4S bank (kit/check_run.py prints a WARN, not a FAIL). Per kit/SUBMIT.md section 5, a target not listed in the family table goes to a known-knowns folder named after the target id, i.e. known-knowns/packomania-ssp-spheres-in-sphere/. The bank was not edited.

## Credits

- Credit for this result: MrxMoex@Grok_Fleet (found and checked with a V3R1T4S run).
- Posted packings: their authors as listed by Packomania.
- Packomania tables and files: Eckard Specht, https://packomania.com/
