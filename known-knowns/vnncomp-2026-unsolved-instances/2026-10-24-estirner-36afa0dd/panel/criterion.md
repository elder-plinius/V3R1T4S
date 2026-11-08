# CRITERION skeptic verdict: vnncomp-2026-unsolved-instance-counterexample

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

Target: `vnncomp-2026-unsolved-instance-counterexample` (criterion quoted in claim/CLAIM.md; compared mechanically with
`success_criterion` in `bank/targets.json` of the pinned public repo, commit d14b0098c7dc3c372fa861a00175d3775aa097e7:
equal after whitespace normalisation, 2101 characters each, normalised sha256
dd312464dee09d72d85e1d3443a7b89293ccbedbdc5482ab8ca5060265cb5a8b).
Instance: `challenging_certified_training_2026`, version directory 2.0, `onnx/cifar10_eps8_wide_cnn7.onnx` +
`vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib`.
Object judged: `object/cifar10_eps8_wide_cnn7_idx7490_sample8.counterexample.txt` (sha256
36afa0dd0c97274d86c6c31f0b42cfab276b522b393a8374a9bb2e18391696b4), with its VNN-LIB 2.0 twin
`object/cifar10_eps8_wide_cnn7_idx7490_sample8_v2.counterexample` (9f66bd2131f63cb25c28e2c04046374108bdf80929d7e8ad9f94185dfd26fef5).
Work window: 2026-10-24T18:20:37Z to 2026-10-24T18:30:41Z (UTC). All checker code is my own, except the official validator, which I ran unmodified.

## Preamble: files and their provenance (the head of the criterion)

- Property file. I fetched it live from
  https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/challenging_certified_training_2026/2.0/vnnlib/cifar10_eps8_wide_cnn7/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib.gz
  (HTTP 200, 33067 bytes) and also at `main` (HTTP 200, 33067 bytes). Both have sha256
  c64e879e9a88b80384dc67f3b84cd8f12a299c9488f136961cb8f226e9f01a59, the same as `inputs/vnnlib/...vnnlib.gz`; decompressed
  sha256 2fad12842961518733ccae34ef7430f08d6e653b1d7acb30671135e019c5d45e. The benchmarks repo `main` is
  303f2327a8e8411efc4457da03d2016ce42733cf (committed 2026-07-07T10:57:07Z; GitHub API HTTP 200), so "live" and the
  pinned commit are the same thing. `inputs/instances_2.0.csv` is byte-identical to the live 2.0 `instances.csv` (sha256
  eb37c71a62c9748b332c125b280f113132807bcd6551d419f4728bec16bfc08d); row 39 is the instance, timeout 550.
- Network file. It is NOT in the git tree. I fetched the recursive tree at 303f2327 (HTTP 200, not truncated, 49532
  entries): `benchmarks/challenging_certified_training_2026/2.0/onnx/` holds only `.gitkeep` and the three small cnn7
  models; the wide_cnn7 models are absent, and the repo has no checksum or manifest file. I read the repo's `setup.sh`
  once (HTTP 200, 2077 bytes, sha256 28326ff2f27198109f4f04427d95c21dbc4c2fe1a92dcd9ac8f57d0af3b0befe, the same at main).
  It downloads the public share https://rwth-aachen.sciebo.de/s/gEMDMstBiSHAAAS as a zip (via
  `scripts/download_sciebo_webdav.py`, which I also read, HTTP 200), moves `large_models/vnncomp2026/<benchmark>/<version>/*`
  to `benchmarks/<benchmark>/<version>/*`, and runs `gunzip -r benchmarks/`. I downloaded
  https://rwth-aachen.sciebo.de/public.php/dav/files/gEMDMstBiSHAAAS/challenging_certified_training_2026/2.0/onnx/cifar10_eps8_wide_cnn7.onnx.gz
  once (HTTP 200, 132594607 bytes, application/gzip, 18:21:15Z to 18:22:20Z). sha256
  7e65aeddfcace3cecb65f4c91dcf51723a862236537ae1afb1db3912f309f5f8 is the same as `inputs/onnx/cifar10_eps8_wide_cnn7.onnx.gz`;
  decompressed sha256 e3940df279250819ea8f6776458429981c29ff1bdd719083cc5b4c1e9c3ff873 (140757533 bytes). I also
  checked that the share does not overwrite the property file through setup.sh's two vnnlib paths: `.../2.0/vnnlib/...idx7490_sample8.vnnlib.gz`
  and `.../vnnlib2.0/...idx7490_sample8.vnnlib.gz` both returned HTTP 404.
- Version directory. I fetched all 11 `results.csv` files in `<tool>/2026_challenging_certified_training_2026/` at results
  commit eea564f5 (each HTTP 200). agate, n2v and vibecheck name `.../challenging_certified_training_2026/2.0/...`, and so does
  act, which is not among the 8 tools scored in results.txt. alpha_beta_crown, neuralsat, nnv, pyrat, super_simple_vnn_comp,
  cora and nnenum name 1.0. agate, n2v and vibecheck are participating tools in results.txt, so version directory 2.0
  qualifies. The claim's statement on this point is accurate.
- Judgement on "taken unmodified from https://github.com/VNN-COMP/vnncomp2026_benchmarks". Under the narrowest reading
  ("blob in the git tree"), the network file fails, and so would every network of this benchmark's wide models. The
  reading I adopt is that the clause means the file the repository's own distribution procedure places at
  `benchmarks/challenging_certified_training_2026/2.0/onnx/`. That is the path every results.csv names
  (`vnncomp2026_benchmarks/benchmarks/challenging_certified_training_2026/2.0/onnx/cifar10_eps8_wide_cnn7.onnx`), and it
  only exists after setup.sh runs. I do not think this stretches the definition. The bank's own verification method
  assumes the skeptic can "download the named ONNX (.onnx.gz) ... from the vnncomp2026_benchmarks repo", and setup.sh is
  how the repo provides it. The weak point is that the share is mutable and no hash is pinned in git, so a hash alone
  cannot prove that today's share file is the file used in July/August. I tested that functionally, with two
  competition-accepted witnesses:
  - alpha_beta_crown's witness for the sibling idx637_sample0 (`inputs/sibling_validated_witness/`, sha256
    63ca2d1b46f830a2cec0813d2ca2b9440049f4c51f4d51890c8ae0240899af37, check.json `correct`, version 1.0). I parsed it
    myself and replayed it on the claimed network (ORT CPU f32). The 10 replayed logits are within 3.397e-06 of the Y
    values alpha_beta_crown wrote. The satisfied disjunct `(<= Y[0,3] Y[0,8])` gives margin 0.00023888, which matches the
    official check.json rationale `prop #7 violated: [-0.00023888]` to all printed digits.
  - vibecheck's competition-accepted witness for idx8397_sample9 at version 2.0. I fetched it myself from the results
    repo at eea564f5: witness sha256 2b1c64aed8c3ec03e2eb18a85229fc1ec52d70cb91dc9b639f6c79e8f0cf90c4, check.json
    `"version": "2.0"`, `result: correct`, network_field `.../2.0/onnx/cifar10_eps8_wide_cnn7.onnx`. The replayed logits
    are within 4.768e-06 of vibecheck's listed Y. The unmodified official validator, run on my laid-out copy of the
    claimed network, returns `correct` for it, at abs_tol 1e-4 and at 0.
  For this network (140757533 bytes decompressed), logits agreeing to within 3.397e-06 and 4.768e-06 at two unrelated
  competition witnesses, one of them at version 2.0, is strong evidence that this file computes the network the competition used. I judge the preamble met,
  with this provenance caveat stated. sha256 of both files is recorded in CLAIM.md (gz and decompressed) and reproduced above.

## (a) Live table and tool directories: MET

- I re-fetched the live https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/main/SCORING/results.txt at
  2026-10-24T18:20:46Z (HTTP 200, 7681226 bytes, sha256 ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f).
  This is the same sha256 as the claim's fetch at 18:18:36Z. Results repo `main` = eea564f5d0a8751d8321a409214db14d03f452b8
  (committed 2026-08-03T14:03:54Z; API HTTP 200 at 18:21:28Z).
- Line 13098, in `Category 2026_challenging_certified_training_2026` (8 participating tools: agate, alpha_beta_crown, n2v,
  neuralsat, nnv, pyrat, super_simple_vnn_comp, vibecheck), reads:
  `Row: ['cifar10_eps8_wide_cnn7-cifar10_eps8_wide_cnn7_idx7490_sample8', '-', 'timeout', 'timeout', 'timeout', 'timeout', 'timeout', '-', 'timeout']`.
  It is followed by `True Result: -` and score 0 for all 8 tools. No cell contains `(h)` or `(v)`.
- My own parse of every `Row:` line (ast.literal_eval, tracking the `Category` headers): 3618 rows in 30 categories,
  127 all-tool-unsolved rows, of which 21 are in this category. Exactly one row in the whole file mentions
  idx7490_sample8, and it is in the unsolved set. The total of 127 agrees with the bank statement.
- Results tree at eea564f5 (API HTTP 200 at 18:21:39Z, not truncated, 27250 entries, response sha256
  8f7b2c70b39e468007149f341da977236ef0287d2f34700aa08456163d716960): 0 paths contain `idx7490_sample8`. So no
  counterexample and no `.check.json` exists for this instance in any tool directory. All 11 results.csv rows for the
  instance give no SAT: act unknown, agate unknown, alpha_beta_crown timeout, cora unknown, n2v run_instance_timeout,
  neuralsat timeout, nnenum error_exit_code_1, nnv timeout, pyrat timeout, super_simple_vnn_comp no_result_in_file,
  vibecheck timeout.

## (b) Strict interior, every assertion as written, margin: MET

- My own regex parser found 6145 `(assert` lines in the property: 3072 lower bounds, 3072 upper bounds, and one output
  assertion `(or ...)` with 9 single-atom disjuncts `(<= Y[0,4] Y[0,j])`, j != 4. The header gives label 4.
- The txt file has 3072 lines. Each decimal string equals its float32 value exactly (checked with Fraction). The `.npy`
  file and the X block of the v2 file are bit-identical to the txt values.
- Strict interior, in exact rationals (Fraction of the decimal bound strings against the exact float32 x): 0 violations
  in 3072 coordinates. The minimum slack is 2.379464e-07 on the lower side and 2.379689e-07 on the upper side. Comparing
  as the validator does (numpy float32 against a Python float) and comparing in float64 also give 0 strict failures.
  No coordinate equals a float32-rounded bound. Note that 2801 coordinates are more than 0.999 of the half-width from the
  centre, so the input is very close to a box vertex. The minimum slack is 1.996 float32 ulps at magnitude 1 to 2 (ulp 1.1920929e-07): strict,
  but with no room to spare. The criterion asks for strictness, not for an input margin, so this is a fragility note, not
  a failure.
- ORT 1.26.0 CPUExecutionProvider, float32, default options:
  Y = [-2.3425824642181396, -1.9580364227294922, 0.3085559606552124, -0.31000083684921265, 0.48005759716033936,
  -0.4104645848274231, 0.48046383261680603, -0.68595951795578, -4.591410160064697, -1.724597692489624]. argmax is 6.
  Y[0,6] - Y[0,4] = 0.0004062354565 (the claim's value). Only disjunct `(<= Y[0,4] Y[0,6])` holds; the next best has
  margin -1.715016e-01. The single atomic comparison on the satisfied branch has margin 4.062e-04 >= 1e-6. The v2 file's
  Y block equals my replay exactly (max abs diff 0.0).
- Robustness of the small margin inside onnxruntime: I ran 12 session variants (intra-op threads 1, 2 and 4; CPU memory
  arena on and off; graph optimisation ALL, BASIC and NONE). The margin ranged from 0.0004062354565 (ALL) to
  0.0004080533981 (BASIC/NONE, 4 threads). The maximum change was 1.818e-06, and the logits moved by at most 2.950e-06.
  The margin is 223.5 times the largest of these deviations.
- Null control: the box centre gives argmax 4, with Y4 - Y6 = 0.258622 and best disjunct margin -0.200247 at the centre.
  So the property is not violated at the clean image, and the vnnlib/onnx pairing behaves as expected.

## (c) float32 rounding, second runtime, official validator: MET

- Rounding to float32 is the identity on this input (float64 to float32 to float64 round trip exact for all 3072 values),
  so the float32-rounded re-run is the run above. The result is unchanged.
- Second runtime, not onnxruntime: onnx2torch with torch 2.9.0+cu128 on CPU, 1 thread (ops: BatchNormalization, Conv,
  Flatten, Gemm, Relu). In float32, argmax is 6 and Y6 - Y4 = 0.0004063546658. In float64, argmax is 6 and
  Y6 - Y4 = 0.0004040482089. In both, the only disjunct with margin >= 1e-6 is j = 6. The largest difference between
  torch float32 and float64 logits is 7.797e-06. The torch margins differ from the ORT margin by 1.192e-07 (float32)
  and 2.187e-06 (float64), so the margin is 185.7 times the largest cross-runtime deviation. I did not run onnx.reference myself; the criterion offers it only as an
  alternative to torch, and the REPRODUCE skeptic covers it.
- Official validator: I fetched `SCORING/counterexamples_v2.py`, `benchmark_instances.py`, `cex_checks.py`, `settings.py`
  and `counterexamples.py` live from vnncomp2026_results `main` (each HTTP 200). Their sha256 values are 5ab7a4df...faab,
  5873d783...d229, 695fcd43...c5, dbd190e5...2039 and 1d8ba5bc...4a87, and all five are byte-identical to `inputs/SCORING/`.
  I ran my own driver against those live copies, unmodified (vnnlib 1.0.2, onnxruntime 1.26.0, numpy 2.2.6), with the
  benchmark directory laid out from my own downloads, both as .gz files and gunzipped as setup.sh leaves them. With
  abs_tol 1e-4 and with 0, in both layouts, the result is `correct`, with rationale "counterexample outputs ignored; using ONNX CPU
  replay outputs; all assertions hold with input_tolerance=0.0, output_tolerance=0.0". That is `correct`, not
  `correct_up_to_tolerance`.

## (d) Not soundnessbench_2026 or test: MET

The category is `2026_challenging_certified_training_2026`.

## (e) No previously published counterexample; wording: MET as far as my search goes

I ran two live web searches: `"cifar10_eps8_wide_cnn7_idx7490_sample8"` and `VNN-COMP 2026 challenging_certified_training
cifar10_eps8_wide_cnn7 counterexample idx7490`. Neither found any page that mentions this instance or a counterexample
for it. The results repo has no file for it (see (a)). The NOVELTY skeptic owns the deeper search. The claim's wording
does not overreach: it names one instance, one version directory, one runtime and one disjunct, and its margin is
exactly the one I measured. It does not say "first", "SAT for the benchmark" or anything about other instances. "Which no
participating tool resolved" is true of the live table, and of all 11 results.csv files. As always, "unresolved"
means no result within the competition's 550 s instance timeout; it is not a hardness claim.

## Null model / statistics

No statistical claim is made. The object is one explicit input, judged by deterministic replay. My only null controls
are the box-centre replay (not violated) and the measured spread across runtimes and configurations (at most 2.187e-06 on
the margin, against margins from 0.0004040482089 to 0.0004080533981).

## Bundling / scope

The claim covers one instance. The sibling witness is offered only as provenance data and is not claimed. Partial win p1
would be subsumed, since the validator returns `correct`, not only `correct_up_to_tolerance`. p2 does not apply. The
existing trophy entries for this target are two traffic_signs_recognition_2023 instances, so this is a different
instance and is not subsumed by them.

Note on machine rules: inside the locked job, the ORT variants briefly used 2 and 4 intra-op threads, one inference each.
`sensors` after the jobs read +80.0°C and +84.0°C, then +67.0°C, all below 90°C.

No page or file I read addressed AI agents; nothing to flag for injection.

criterion_met: full
confirmed_scope: The 3072 float32 values in `object/cifar10_eps8_wide_cnn7_idx7490_sample8.counterexample.txt` lie strictly inside every input bound of `inputs/vnnlib/cifar10_eps8_wide_cnn7_idx7490_sample8.vnnlib.gz` (the live vnncomp2026_benchmarks 2.0 file, sha256 c64e879e…1a59), and on `inputs/onnx/cifar10_eps8_wide_cnn7.onnx.gz` (sha256 7e65aedd…f5f8, identical to the file served on 2026-10-24 at the public-share path that the benchmarks repo's setup.sh downloads) they satisfy the property's only output assertion through the disjunct `(<= Y[0,4] Y[0,6])` with margin 0.0004062354565 in onnxruntime CPU float32 (0.0004063546658 and 0.0004040482089 in torch float32/float64), the unmodified live `SCORING/counterexamples_v2.py` returns `correct` at zero tolerance, and the instance's row in the live results.txt (fetched 2026-10-24T18:20:46Z, sha256 ec1b6fcb…eb26f) has no `(h)` or `(v)` and the results repository holds no counterexample file for it.

pass: true
