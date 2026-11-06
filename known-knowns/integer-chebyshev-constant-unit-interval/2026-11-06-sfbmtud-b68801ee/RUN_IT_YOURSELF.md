# Reproduce from a fresh shell

Verify the rigorous upper bound:

```sh
sh verify-it-yourself/run_checks.sh
```

The final line must be PASS. The wrapper authenticates the exact object/checker bytes, then executes the frozen exact-integer Bernstein verifier with Python site packages disabled, optimized execution disabled, and temporary outputs cleaned. SHA checks alone do not establish the mathematics. See verify-it-yourself/METHOD.md.

Rebuild the exact compressed object from the retained search witness:

```sh
python3 -S how-we-built-it/weight-optimization/build_final_object.py how-we-built-it/weight-optimization/inputs/raw_v8.json rebuilt_candidate.json
```

Expected SHA256: b68801eed7ca3043a7b817aa6567d92b6d73519c3be888936589519de71055ce. Compare this with object/candidate.json, then remove the extra rebuilt file before checking the package manifest.

Reconstruct the generated factors from their precise mathematical origins:

```sh
cd how-we-built-it/factor-construction
```

Follow README.md there, using its pinned dependencies and recorded exact inputs. It replays active constructions, not an exhaustive rediscovery search. The retained optimizer can be rerun with inputs/v7.json and --extra-factors inputs/final_extra_factors.json; its exact installation and search commands are in how-we-built-it/weight-optimization/README.md with requirements.txt. Floating-point LP results may vary across library versions, and are never the proof. The exact compression builder and final certificate are deterministic.

The optional Arb checker requires python-flint==0.9.0. From the package root:

```sh
gzip -dc verify-it-yourself/saved-proofs/interval_cover.json.gz > replay_cover.json
python3 verify-it-yourself/optional_arb_checker.py --certificate object/candidate.json --threshold 0.422640947 --mode replay --method taylor --bits 384 --proof replay_cover.json --seconds 880
rm replay_cover.json
```

Both supplied partitions are gzip-compressed JSON. All saved covers are supporting evidence; the primary command constructs and checks a fresh complete cover from the object.
