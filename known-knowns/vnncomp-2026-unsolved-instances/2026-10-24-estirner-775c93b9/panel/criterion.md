# CRITERION skeptic verdict: vnncomp-2026-unsolved-instance-counterexample

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

Claim judged: `claim/CLAIM.md`, one instance: VNN-COMP 2026 `challenging_certified_training_2026`, version directory 2.0,
`onnx/cifar10_eps8_wide_cnn7.onnx` + `vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib`.
Object: `object/cifar10_eps8_wide_cnn7_idx6249_sample7.counterexample.txt`, plus its VNN-LIB 2.0 form
`object/cifar10_eps8_wide_cnn7_idx6249_sample7_v2.counterexample`.

Method: I fetched the sources live (one plain request per URL, UA `V3R1T4S-research-agent (curl)`), wrote my own
results.txt parser and my own VNN-LIB s-expression evaluator (exact `fractions.Fraction` arithmetic on decimal constants
and on the float32 values), and ran onnxruntime CPU float32, onnx2torch (float32 and float64, CPU), and the unmodified
live `SCORING/counterexamples_v2.py`. I wrote my own checker and my own validator wrapper; the wrapper only supplies the
result-type names copied from the official `counterexamples.py`. I did read the claim's
`tools/official_validate_run.py` (I printed it while orienting), but I did not run it. Every check below comes from my
own scripts.

## Criterion text

The success criterion quoted in `claim/CLAIM.md` is byte-identical to `success_criterion` in the pinned bank
`bank/targets.json` (repo commit d14b0098c7dc3c372fa861a00175d3775aa097e7). My script printed `verbatim match: True`.

## Preamble: files "taken unmodified from vnncomp2026_benchmarks at the version directory a participating tool's results.csv names"

- Version directory. I fetched all 11 per-tool `results.csv` files for this category at 2026-10-24T16:37:06Z to
  16:37:11Z, each HTTP 200. Line 38 of each is this instance. agate, n2v and vibecheck name
  `vnncomp2026_benchmarks/benchmarks/challenging_certified_training_2026/2.0/onnx/cifar10_eps8_wide_cnn7.onnx` and the
  matching `2.0/vnnlib/...idx6249_sample7.vnnlib`. All three are among the 8 participating tools that results.txt lists
  for this category. act also names 2.0, but act is not in results.txt's participant list for this category. The
  claim's sentence ("named by act, agate, n2v and vibecheck") is still literally true, and the other three suffice.
  alpha_beta_crown, cora, neuralsat, nnenum, nnv, pyrat and super_simple_vnn_comp name 1.0. Version 2.0 qualifies.
- Property file: in the git tree. Live benchmarks `main` = 303f2327a8e8411efc4457da03d2016ce42733cf, committed
  2026-07-07T10:57:07Z (API, HTTP 200). The `.vnnlib.gz` fetched at 2026-10-24T16:35:22Z from both the pinned commit and
  `main` was HTTP 200, 35086 bytes, sha256 3e9340de6e0237635a572457218e5c4f74b298e20ff69dc482a627e85206d1fe, identical to
  `inputs/vnnlib/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib.gz`. Decompressed sha256
  5593601c97c83875dba34d251ba1b772f299bd4b622e5646bb520c260169bd85. The live 2.0 `instances.csv` (fetched
  2026-10-24T16:56:01Z, HTTP 200, sha256 eb37c71a62c9748b332c125b280f113132807bcd6551d419f4728bec16bfc08d, identical to
  `inputs/instances_2.0.csv`) has row 38:
  `onnx/cifar10_eps8_wide_cnn7.onnx,vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib,550`.
- Network file: not in the git tree.
  - I read the repo's own `setup.sh` once, at commit 303f2327 (2026-10-24T16:35:03Z, HTTP 200, 2077 bytes, sha256
    28326ff2f27198109f4f04427d95c21dbc4c2fe1a92dcd9ac8f57d0af3b0befe), and its helper
    `scripts/download_sciebo_webdav.py` (HTTP 200, 13672 bytes, sha256
    b24584400d1305d7a71541a9166bc2321998a50ad99a1fee48297930ec80ecb7). setup.sh downloads the public share
    https://rwth-aachen.sciebo.de/s/gEMDMstBiSHAAAS as a zip and moves each `<benchmark>/<version>/...` into
    `benchmarks/<benchmark>/<version>/...`. It would use a `seed_*` subfolder instead if one existed. It then runs
    `gunzip -r benchmarks/`.
  - WebDAV PROPFIND of the share's `challenging_certified_training_2026/` (2026-10-24T16:37:38Z, HTTP 207) lists only
    `1.0/` and `2.0/`, no `seed_*`. So setup.sh places the share's `2.0/onnx/cifar10_eps8_wide_cnn7.onnx.gz` at exactly
    the path every 2.0 results.csv names.
  - PROPFIND of `2.0/onnx/`: `cifar10_eps8_wide_cnn7.onnx.gz` has getcontentlength 132594607 and getlastmodified
    "Thu, 02 Jul 2026 14:42:13 GMT". That predates the benchmarks commit and the results (main eea564f5 committed
    2026-08-03T14:03:54Z). The share answered without a password.
- My judgement on the clause: distribution through the benchmarks repo's own `setup.sh` from the share it names is the
  repo's only distribution path for this file, and it is the file the competition's runs used. That meets "taken
  unmodified from https://github.com/VNN-COMP/vnncomp2026_benchmarks at the version directory 2.0" as written. The
  bank's verification_method itself says "download the named ONNX (.onnx.gz)". The claim records sha256 of both files:
  gz 7e65aeddfcace3cecb65f4c91dcf51723a862236537ae1afb1db3912f309f5f8, decompressed
  e3940df279250819ea8f6776458429981c29ff1bdd719083cc5b4c1e9c3ff873. I recomputed both from
  `inputs/onnx/cifar10_eps8_wide_cnn7.onnx.gz`.
- My own identity check of the network file was only partial. I sent one GET of the share file
  (2026-10-24T16:37:48Z to 16:40:51Z). curl reported `(92) HTTP/2 stream 1 reset by server (error 0x1 PROTOCOL_ERROR)`
  after HTTP 200 and 31359037 of 132594607 bytes. Following the one-request-per-URL rule, I did not retry. What I can
  confirm:
  - The received 31359037-byte prefix (sha256 365bec40772c22d59e682ba3f7a7f338ae1ed192fcdcf0bf52daeb2dc22fed9d) is
    byte-identical to the first 31359037 bytes of the claim's file. `cmp` reports only EOF on the partial file.
  - The claim's file is 132594607 bytes, equal to the share's size.
  - I did not compute a full sha256 against the live share.
- Sibling witness (`inputs/sibling_validated_witness/`): weight moderate to strong, as a functional fingerprint.
  - Its check.json says `result: correct`, version 1.0, ORT CPU replay rationale `prop #7 violated: [-0.00023888]`.
  - Replaying its 3072 X values through the claim's network (ORT CPU float32), I get the 8th disjunct (0-based #7)
    `Y[0,3] <= Y[0,8]` with margin 0.0002388805151. That reproduces the competition's recorded value to all 5 digits it
    printed.
  - The max difference from the tool's own recorded Y is 3.4e-06.
  - The competition validated that witness against the 1.0 network file. The share's `1.0/onnx/cifar10_eps8_wide_cnn7.onnx.gz`
    has the same size, 132594607 (PROPFIND 2026-10-24T16:45:53Z, HTTP 207). Its ETag differs, but Nextcloud ETags are
    not content hashes.
  - Side note, irrelevant to the claim: that sibling X is not strictly inside the sibling's 2.0 box (min slack
    -4.982910e-10), because it was checked against the 1.0 property.
  - Taken together (exact size, an identical 31359037-byte prefix of the compressed stream, a share timestamp before the
    competition, and a reproduced official replay value), modification of the network is not credible. I accept the
    file as the competition's 2.0 network, with the full-hash gap stated in confirmed_scope.

## (a) Live table and tool directories: MET

- Live `SCORING/results.txt` fetched 2026-10-24T16:34:32Z: HTTP 200, 7681226 bytes, sha256
  ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f. This is identical to both of the claim's fetches.
  Results repo main = eea564f5d0a8751d8321a409214db14d03f452b8.
- My own parse: 3618 `Row:` lines; 127 all-tool-unsolved rows (no `(h)`/`(v)` in any cell); 21 of them in
  `2026_challenging_certified_training_2026`. The target is among them.
- Exactly one row matches, at line 13087, in that category. Tools: agate, alpha_beta_crown, n2v, neuralsat, nnv, pyrat,
  super_simple_vnn_comp, vibecheck. Row: `['cifar10_eps8_wide_cnn7-cifar10_eps8_wide_cnn7_idx6249_sample7', '-',
  'timeout', 'timeout', 'timeout', 'timeout', 'timeout', '-', 'timeout']`. `has (h)/(v): False`.
- The per-tool CSVs agree: no tool returned sat or unsat on this line. Results were unknown, timeout,
  run_instance_timeout, error_exit_code_1 or no_result_in_file.
- Results repo tree at eea564f5 (API, 2026-10-24T16:36:00Z, HTTP 200, 10027325 bytes, `truncated False`, 27250 entries):
  no path contains `idx6249` anywhere. So there is no `*.counterexample.check.json`, and no witness, for this instance
  in any tool directory.
- "Re-fetched live immediately before claiming": the claim's second fetch (2026-10-24T16:29:21Z) and mine have the same
  sha256.

## (b) Strict interior, every assertion as written, output margin >= 1e-6: MET

- The property has 6145 assertions: 3072 `>=` and 3072 `<=` input bounds (no duplicates, every coordinate bounded on
  both sides) and 1 output assertion, `(or (and (<= Y[0,5] Y[0,j])) ...)` for j in {0,1,2,3,4,6,7,8,9}. The only other
  top-level forms are `vnnlib-version` and `declare-network`.
- The witness has 3072 lines. Every line is the exact decimal expansion of a float32 (round-trip `True`, Fraction
  equality `True`). It is identical to the `.npy` file and string-identical to the X block of the v2 file.
- Strict interior with Fraction at zero tolerance, all 3072 coordinates: `True`. Min slack 2.379244e-07.
- ORT 1.26.0 CPUExecutionProvider, float32, input `input` of shape [batch_size, 3, 32, 32]:
  - Y = [-1.7233030796051025, -3.504415512084961, 0.3472158908843994, 0.2884974479675293, 0.05927523970603943,
    0.3354530334472656, -0.5704138875007629, -0.7080146074295044, -2.996689796447754, -2.8960139751434326], argmax 2.
  - All 6145 assertions are true exactly as written.
  - Exactly one disjunct holds: `(<= Y[0,5] Y[0,2])` with margin 0.011762857437, which is >= 1e-6. The other eight
    margins are negative, the closest being -0.04695558548 for Y[0,3].
  - The Y recorded in the v2 file equals my replay bit for bit.
  - A session with the official options (arena off, default threads) gives the same Y2-Y5 = 0.011762857437, max |dY| 0.

## (c) Float32 rounding, second runtime, official validator returning `correct`: MET

- Float32 rounding: the input is already float32, so rounding is a no-op. The re-run gives identical input `True` and
  identical output `True`.
- Second runtime (not onnxruntime): onnx2torch on torch 2.9.0+cu128, run on CPU. The graph is opset 18 with 15 nodes:
  BatchNormalization, Conv, Flatten, Gemm, Relu.
  - float32: argmax 2, Y2-Y5 = 0.011764973402.
  - float64: argmax 2, Y2-Y5 = 0.01176085948.
  - In both precisions the same disjunct holds with margin >= 1e-6. The input-bound assertions do not depend on the
    runtime.
- Official validator. These live SCORING files, fetched 2026-10-24T16:41:52Z, all HTTP 200, are byte-identical to the
  claim's `inputs/SCORING/` copies: `counterexamples_v2.py`
  (5ab7a4df717ed1c80ec0477372eb394a4a2a460a5060f0eebe030a76d219faab), `cex_checks.py`, `benchmark_instances.py`,
  `settings.py`, `counterexamples.py`.
  - I ran the live copy unmodified, as the competition calls it: `validate_vnnlib2_counterexample(benchmark_dir, net,
    prop, ce, abs_tol, 0.0, CounterexampleResult, True)` with Settings.COUNTEREXAMPLE_ATOL = 1e-4, and again at 0.
  - Inputs: the live-fetched property file and the claim's network, laid out under a 2.0 version directory.
  - Both runs returned `correct | counterexample outputs ignored; using ONNX CPU replay outputs; all assertions hold with
    input_tolerance=0.0, output_tolerance=0.0`. That is `correct`, not `correct_up_to_tolerance`.

## (d) Not soundnessbench_2026 or test: MET

The category is `2026_challenging_certified_training_2026`.

## (e) No previously published counterexample: no overreach found (NOVELTY owns the search)

- Two web searches, for `"cifar10_eps8_wide_cnn7" counterexample` and `"idx6249_sample7" vnnlib`, returned nothing
  relevant.
- The results repo has no file for this instance.
- The pinned V3R1T4S record (`TROPHY_CASE.md` rows 51-52, `known-knowns/vnncomp-2026-unsolved-instances/INDEX.csv`)
  covers only two traffic_signs_recognition_2023 instances, so this claim is not subsumed.
- The claim's wording asserts only "no participating tool resolved" plus the replay facts. It makes no wider novelty
  claim.

## Hidden quantifiers, stretched definitions, null model, bundling

- The results.txt row merges runs on two different property files: five of the eight listed tools ran the 1.0 vnnlib.
  The claim and my scope cover only the 2.0 pair. Nothing here shows the witness satisfies the 1.0 property, and that
  is not claimed.
- "Unsolved" means only that no tool finished with a verdict within the competition run (instances.csv timeout 550).
  It does not mean the instance is hard in any further sense, and the claim does not say so.
- The input slack is strict but small (min 2.379244e-07). The criterion requires strictness only for inputs, and the
  1e-6 margin only for output comparisons, so both are met.
- Null model: not applicable. This is a deterministic replay of one explicit input, and no statistical claim is made.
  The only noise source is cross-runtime float error. Y2-Y5 spans 0.01176085948 to 0.011764973402 across ORT f32, torch
  f32 and torch f64, a spread of 4.114e-06. The smallest margin is 2859 times that spread.
- One instance, one claim, no bundling. Partial wins p1 (`correct_up_to_tolerance` only) and p2 (2025 set) do not apply,
  and the full criterion is met, so none is needed.
- injection_suspected: none. No fetched page, file or program output addressed AI agents.

criterion_met: full

confirmed_scope: The 3072 float32 values in object/cifar10_eps8_wide_cnn7_idx6249_sample7.counterexample.txt (string-identical to the X block of object/cifar10_eps8_wide_cnn7_idx6249_sample7_v2.counterexample) lie strictly inside every input bound of inputs/vnnlib/cifar10_eps8_wide_cnn7_idx6249_sample7.vnnlib.gz (VNN-COMP 2026 challenging_certified_training_2026, version 2.0, an all-tool-unsolved row in the live results.txt fetched 2026-10-24T16:34:32Z) and, on the network inputs/onnx/cifar10_eps8_wide_cnn7.onnx.gz (identity with the benchmarks repo's setup.sh share file checked by exact size, an identical 31359037-byte prefix and a reproduced official sibling replay value, not by a full sha256 of the live share file), make every assertion true at zero tolerance through the single disjunct (<= Y[0,5] Y[0,2]) with margin 0.011762857437 under onnxruntime CPU float32 (0.011764973402 and 0.01176085948 under onnx2torch float32 and float64), and the unmodified live SCORING/counterexamples_v2.py returns correct at abs_tol 1e-4 and 0.

pass: true
