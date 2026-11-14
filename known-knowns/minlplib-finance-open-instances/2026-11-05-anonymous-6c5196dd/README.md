# MINLPLib pricing050: a machine-checkable dual certificate within 1e-6 of the best primal

## What

With object/lambda.txt and the arb-ball interval branch-and-bound leaf log object/cert_arb_leaves.json (1958 leaves), weak Lagrangian duality certifies that max objvar for the posted pricing050 instance (instance/gms_pricing050.gms) is at most -1813.829075713452, which is <= the recorded best primal -1813.829078 plus 1e-6*|best|.

(Panel status: CONFIRMED_PARTIAL, `panel/gate.md`. The instance file named in the scope sentence is the posted MINLPLib GAMS model; this package does not copy it — `verify-it-yourself/run_checks.sh` downloads it and checks sha256 192dd92d69cdcd131462d40c137df73dc101afef0739cc7ba98c130a79313715.)

Main object: `object/cert_arb_leaves.json` (sha256 6c5196dd180aad61b9f7d0b6b489418bfa4ac7aa28ba5fd5c07a205ecbcb9348), with multipliers in `object/lambda.txt`.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (after verifying all 1958 covering leaves and reassembling the dual). About one minute on a laptop the first time (venv + python-flint install + a ~15 KB download); a few seconds afterwards. Details: `RUN_IT_YOURSELF.md`; real output: `verify-it-yourself/RECEIPTS.md`.

## Compared to

| what | value | source | fetched (UTC) |
|---|---|---|---|
| MINLPLib =best= (primal) | -1813.829078 | https://www.minlplib.org/minlplib.solu (sha256 df6732aa…) | 2026-11-05T19:50:42Z |
| MINLPLib =bestdual= | -1153.003281 | same solu file | same |
| best listed solver dual (maximisation) | -1534.3281 (SCIP) | https://www.minlplib.org/pricing050.html (sha256 f4e23f86…) | 2026-11-05T19:50:45Z |
| this object (rigorous U on max objvar) | **-1813.829075713452** | `object/` | — |

Full snapshot with hashes: `the-record-we-beat/RECORD.md`. The panel's own fetches: `panel/novelty.md`.

## Not claimed

- Not a better feasible primal point (full success criterion unmet and not claimed).
- Not a claim about saa_2, other MINLPLib instances, or other pricing* models.
- Not a claim that MINLPLib's public status page already lists this dual (it still shows a large dual gap).
- Concavity of the univariate terms (example (i) in the bank's partial-win text) is illustrated in `how-we-built-it/code/concavity_proof.py` but is not required for the confirmed scope; the certificate is the dual leaf log (example (ii)).
- Sending a certificate or point to the MINLPLib maintainer is an action for a human, not part of this package.

## Credits

- MINLPLib (Bussieck, Drud, Meeraus 2003; Vigerske et al., https://www.minlplib.org) for the instance, posted points and bounds.
- The pricing model of Davarnia and van Hoeve / Davarnia (Math. Prog. 2021).
- Tools: python-flint / Arb (F. Johansson); mpmath.
- Credit for this package: anonymous.
