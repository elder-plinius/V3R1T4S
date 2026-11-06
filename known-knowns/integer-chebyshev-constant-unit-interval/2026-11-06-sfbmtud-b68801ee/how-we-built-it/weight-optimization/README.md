# Reproduce the final optimization and exact exponent construction

The main norm verifier needs only the Python standard library. This optional search reproduction uses the exact dependency versions used during the research. Run these commands from the submission package root on Unix, with Python3.12:

```sh
python3 -m venv ../chebyshev-search-env
../chebyshev-search-env/bin/python -m pip install -r how-we-built-it/weight-optimization/requirements.txt
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 timeout 650 ../chebyshev-search-env/bin/python how-we-built-it/weight-optimization/optimize.py how-we-built-it/weight-optimization/inputs/v7.json ../chebyshev-rebuilt-v8 --extra-factors how-we-built-it/weight-optimization/inputs/final_extra_factors.json --iterations 20 --seconds 600
```

This is the final adaptive optimization step with its frozen candidate and complete extra pool, including restored original factors. Its objective and extrema are HEURISTIC. Floating-point solver results can vary across platforms even with the same versions; a newly produced proposal needs a new complete norm proof. The exact data used for the published object are retained as inputs/raw_v8.json.

Rebuild that object's compressed integer exponents deterministically:

```sh
python3 -S how-we-built-it/weight-optimization/build_final_object.py how-we-built-it/weight-optimization/inputs/raw_v8.json ../chebyshev-rebuilt-final.json
```

Expected SHA256: b68801eed7ca3043a7b817aa6567d92b6d73519c3be888936589519de71055ce.

Optionally repeat the exponent-scale study:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ../chebyshev-search-env/bin/python how-we-built-it/weight-optimization/rounding_study.py how-we-built-it/weight-optimization/inputs/raw_v8.json ../chebyshev-rounding-study
```

The degree-scale study is heuristic; its final selected object is separately certified. Active factor constructions have their exact replay in ../factor-construction/README.md, with only python-flint needed. PUBLIC_SOURCE_FORMATTING.json records whitespace-only formatting around matrix-multiplication operators in the distributed optimizer copies, with identical Python ASTs and both source hashes. The original frozen mathematical verifiers were not modified.
