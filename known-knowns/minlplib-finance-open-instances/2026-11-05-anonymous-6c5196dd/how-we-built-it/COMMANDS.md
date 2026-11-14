# Commands that built the object

Pinned deps: `requirements.txt` (python-flint 0.9.0, mpmath 1.4.1). Run from the
claim / package context after downloading the posted instance to `instance/gms_pricing050.gms`
(sha256 192dd92d69cdcd131462d40c137df73dc101afef0739cc7ba98c130a79313715).

```sh
python3 -m venv venv
venv/bin/pip install -r how-we-built-it/requirements.txt
venv/bin/python how-we-built-it/code/pricing_parse.py instance/gms_pricing050.gms model.json
# multipliers in object/lambda.txt were obtained by a float dual search (dual_float.py)
# then fixed as exact decimals; the certificate is the leaf log below.
venv/bin/python how-we-built-it/code/cert_arb.py model.json object/lambda.txt object/cert_arb_leaves.json
venv/bin/python how-we-built-it/code/cert_mpiv.py model.json object/lambda.txt
venv/bin/python how-we-built-it/code/concavity_proof.py model.json
```

`cert_arb.py` prints `S1 PASS` when the rigorous upper bound U on max objvar
satisfies U <= -1813.829078 + 1e-6*1813.829078. The leaf log is deterministic for
fixed precision (ctx.prec = 200 in the builder).
