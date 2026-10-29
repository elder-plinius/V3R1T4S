# Reproduce: VNN-COMP 2026 counterexamples

All commands are relative to the `known-knowns/vnncomp-2026-unsolved-instances/` directory. Requirements: `python3`
with `numpy` and `onnxruntime` (`onnx` optional, for the second runtime), and network access to
raw.githubusercontent.com. Runtime: a few seconds plus the downloads (about 0.3 MB).

## 1. Integrity

```sh
sha256sum witnesses/*/*.txt      # macOS: shasum -a 256; expected values in INDEX.csv
```

## 2. The standalone checker

```sh
python3 verify-it-yourself/vnncheck.py --cache downloads
```
It downloads the ONNX model and the two VNN-LIB properties from
`https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/traffic_signs_recognition_2023/2.0/`
(one GET per file), checks their sha256 against the pinned values, checks every input constraint strictly in exact
rational arithmetic, runs the network with onnxruntime (CPU, float32) and, if installed, `onnx.reference`, and
evaluates the output assertion at zero tolerance. Expected last lines:
```
VNNCHECK PASS instance=3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_1703_eps_1.00000 margin=0.99990918 min_input_slack=0.0009765625 ...
VNNCHECK PASS instance=3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30/model_30_idx_178_eps_1.00000 margin=0.96402755 min_input_slack=0.0009765625 ...
```
Negative controls (`verify-it-yourself/mutate.py`): a pixel moved onto its bound, a pixel moved 2^-10 outside, and
the unperturbed image must each give `VNNCHECK FAIL`. `sh verify-it-yourself/run_checks.sh` does all of the above
(set `PYTHON=` to choose the interpreter).

## 3. The competition's own validator

```sh
pip install vnnlib==1.0.2 onnx onnxruntime numpy
python3 verify-it-yourself/official_validate.py --cache downloads      # or: OFFICIAL=1 sh verify-it-yourself/run_checks.sh
```
This downloads `SCORING/counterexamples_v2.py`, `benchmark_instances.py` and `cex_checks.py` from
github.com/VNN-COMP/vnncomp2026_results at commit `eea564f5d0a8751d8321a409214db14d03f452b8` (sha256 checked), and
calls `validate_vnnlib2_counterexample(benchmark_dir, network_field, property_field, witness_v2.txt, abs_tol, 0.0,
result_type)` unmodified, with abs_tol 1e-4 (the competition setting) and 0. Expected for both instances:
`('correct', 'counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0')`.

To do it entirely by hand: clone github.com/VNN-COMP/vnncomp2026_results, check out `eea564f5`, put the two
benchmark files under `<dir>/onnx/` and `<dir>/vnnlib/` (gzip as stored), and call the function above from
`SCORING/` with `network_field = vnncomp2026_benchmarks/benchmarks/traffic_signs_recognition_2023/2.0/onnx/3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30.onnx`
and `property_field = vnncomp2026_benchmarks/benchmarks/traffic_signs_recognition_2023/2.0/vnnlib/model_30_idx_<1703|178>_eps_1.00000.vnnlib`.

## 4. Is the instance still unresolved today?

One GET, with a User-Agent that says who you are:
```sh
curl -sS -A "your-name-or-project (single GET)" -o results.txt \
     https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt
python3 the-record-we-beat/parse_results.py results.txt
```
Expected (2026-10-12): 3618 `Row:` lines, 127 all-tool-unsolved, and both of our rows
`[..., 'timeout', '-', 'timeout'] -> all-tool-unsolved`. If a row has since changed, or a counterexample file for
either instance has appeared in the results repository, record it as described under Corrections in
`READ_BEFORE_CITING.md` at the repository root.

## 5. Regenerate

The generating code is in `how-we-built-it/` (see [how-we-built-it/README.md](how-we-built-it/README.md); requirements
in `how-we-built-it/requirements.txt`, including `ortools`). After step 2 has filled `downloads/`, this rebuilds both
witness files from the saved CP-SAT solutions and compares them with the published ones (a few seconds):
```sh
sh how-we-built-it/regenerate_from_checkpoints.sh downloads regenerated     # expect: REGENERATED: all four witness files byte-identical
```
To re-run the search itself (minutes; CP-SAT finds *a* counterexample, usually not the same one):
```sh
python3 -I how-we-built-it/cpsat_bnn30.py --cls 22 --pw 10 --time 900 --workers 4 \
  --vnnlib downloads/benchmarks/traffic_signs_recognition_2023/2.0/vnnlib/model_30_idx_1703_eps_1.00000.vnnlib.gz \
  --hint how-we-built-it/checkpoints/hint_idx_1703_cls22.json --out ckpt_1703.json
```

## Wrapper contract dependency

`verify-it-yourself/run_checks.sh` requires the standard-library helper
`../check_harness_contract.py`, relative to this family directory. Keep the normal
repository layout, or copy `known-knowns/check_harness_contract.py` beside any
standalone family copy. A missing helper fails explicitly with exit 2. The helper
validates completed negative-control evidence and/or indexed inventory; it does
not replace the scientific checker or independently prove its result.

For lightweight orchestration regressions from the repository root (Python 3.9+,
no scientific dependencies, downloads, or compiler):

```sh
python3 known-knowns/tests/harness_contracts/run_regressions.py --output known-knowns/tests/harness_contracts/results-local
```

These tests mock scientific commands and execute only the standard-library
contract helper. Root `SHA256SUMS` edits remain a maintainer-only step. Before merging, maintainers
must refresh entries for the changed wrappers/documents and add the helper and
regression files. The pinned 91419e28 manifest already has stale kit entries;
regenerate and verify the manifest against the final complete tree, rather than
assuming unchanged entries are current.
